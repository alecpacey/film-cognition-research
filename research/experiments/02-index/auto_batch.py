#!/usr/bin/env python3
"""
Run stage-02 batches end to end, unattended, and never leave the GPU idling.

Batch 0 cost about $0.60 more than it should have, because the run finished and
then sat on billed hardware until a human noticed. That gap — between "done" and
"paused" — is the only real money leak in this pipeline, and it is bigger than any
saving from choosing a different batch size. So it is closed here in code:

    upload -> restart -> poll until every clip has reported -> harvest -> pause

Idle exposure is one poll interval, not however long until somebody looks.

Why it still polls rather than trusting a duration: TRIBE fails silently. A clip
that returns 179 parcels, or NaN, or nothing at all, must surface as a failure
rather than as a run that merely looks slow. And the log endpoint is a live SSE
stream that never closes while the Space is RUNNING, so every read is bounded by a
wall-clock deadline — the bug that caused the idling in the first place.

Safety: on ANY terminal error, or on the timeout, it harvests what exists and
pauses regardless. The Space is never left running by a failure path.

    python auto_batch.py --batch 10          # one batch, then pause
    python auto_batch.py --batch 10 --loop   # keep going until all 70 are scored
    python auto_batch.py --status            # no cost, no side effects
"""
import argparse, json, socket, subprocess, sys, time, urllib.request
from pathlib import Path
from huggingface_hub import HfApi, get_token

SPACE = "alecnpacey/tribe-probe"
POLL = 60
MAX_MIN_PER_CLIP = 25          # generous: ~10 min is normal, this only catches hangs
BAD_STAGE = {"BUILD_ERROR", "RUNTIME_ERROR", "CONFIG_ERROR", "DELETING"}
ERR_PAT = ("Traceback", "Scheduling failure", "not enough hardware", "OutOfMemory",
           "CUDA error", "Killed", "PROBE FAILED", "No clips found")
api = HfApi()


def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)


# Gradio/uvicorn emit asyncio event-loop teardown noise on every restart:
#   Exception ignored in: <function BaseEventLoop.__del__ ...>
#   ValueError: Invalid file descriptor: -1
# Python has already swallowed these — "Exception ignored in" says so — and they
# are not on the scoring path. Filtered by their own marker rather than by
# dropping "Traceback" from the patterns, because a real traceback must still
# surface. Better a false positive than a missed failure; this is a KNOWN one.
BENIGN = ("Exception ignored in", "Invalid file descriptor",
          "BaseEventLoop.__del__", "asyncio/", "selectors.py", "selector_events.py",
          "unix_events.py", "base_events.py")


def _benign(line, seen):
    if any(b in line for b in BENIGN):
        return True
    # a bare "Traceback" line is benign only if the ignored-exception marker
    # immediately preceded it
    if line.strip().startswith("Traceback"):
        return any("Exception ignored in" in s for s in list(seen)[-3:])
    return False


def fetch(deadline=25, idle=5):
    req = urllib.request.Request(
        f"https://huggingface.co/api/spaces/{SPACE}/logs/run",
        headers={"Authorization": f"Bearer {get_token()}"})
    out, t0 = [], time.time()
    try:
        r = urllib.request.urlopen(req, timeout=20)
    except Exception as e:
        log(f"log fetch failed: {type(e).__name__}: {e}"); return out
    try:
        try: r.fp.raw._sock.settimeout(idle)
        except Exception: pass
        while time.time() - t0 < deadline:
            try: raw = r.readline()
            except (socket.timeout, TimeoutError, OSError): break
            if not raw: break
            l = raw.decode("utf-8", "replace")
            if l.startswith("data: "):
                try: out.append(json.loads(l[6:])["data"])
                except Exception: pass
    finally:
        r.close()
    return out


def run(cmd):
    r = subprocess.run([sys.executable] + cmd, capture_output=True, text=True)
    # flush=True: without it these sit in Python's buffer under nohup, so the log
    # looks empty while the work is plainly happening on the Space.
    if r.stdout.strip(): print(r.stdout.strip(), flush=True)
    if r.stderr.strip(): print(r.stderr.strip(), file=sys.stderr, flush=True)
    return r.returncode


def harvest_and_pause(why):
    log(f"harvesting and pausing ({why})")
    rc = run(["run_batch.py", "--harvest"])
    try:
        st = api.space_info(SPACE).runtime.stage
        log(f"space stage now {st}")
        if st not in ("PAUSED", "STOPPED", "SLEEPING"):
            api.pause_space(SPACE); log("forced pause")
    except Exception as e:
        log(f"pause check failed: {type(e).__name__}: {e}")
    return rc


def wait_for(n_expected):
    """Poll until every clip reports, or something goes wrong. Returns True if clean."""
    t0, done, seen = time.time(), set(), set()
    budget = n_expected * MAX_MIN_PER_CLIP + 20
    while True:
        el = (time.time() - t0) / 60
        try:
            stage = api.space_info(SPACE).runtime.stage
        except Exception as e:
            log(f"space_info failed: {type(e).__name__}: {e}"); time.sleep(POLL); continue
        if stage in BAD_STAGE:
            log(f"TERMINAL STAGE {stage}"); return False
        if stage == "RUNNING":
            for l in fetch():
                if l in seen: continue
                seen.add(l)
                if l.startswith("PARCELCOUNT\t"):
                    _, clip, cnt = l.split("\t")
                    done.add(clip)
                    ok = cnt.strip() == "180"
                    log(f"clip {len(done)}/{n_expected}: {clip} -> {cnt.strip()} parcels"
                        + ("" if ok else "   ** NOT 180 **"))
                elif any(p in l for p in ERR_PAT) and not _benign(l, seen):
                    log(f"ERROR: {l.strip()[:180]}")
            if len(done) >= n_expected:
                log(f"all {n_expected} clips reported after {el:.0f} min"); return True
        if el > budget:
            log(f"TIMEOUT after {el:.0f} min with {len(done)}/{n_expected}"); return False
        time.sleep(POLL)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=10)
    ap.add_argument("--loop", action="store_true", help="continue until nothing is pending")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()

    if a.status:
        run(["run_batch.py", "--plan"]); raise SystemExit

    while True:
        rc = run(["run_batch.py", "--batch", str(a.batch)])
        if rc != 0:
            log("upload/restart failed — stopping"); raise SystemExit(1)
        vecs = json.loads(Path("parcel_vectors.json").read_text()) if Path("parcel_vectors.json").exists() else {}
        before = len(vecs)
        clean = wait_for(a.batch)
        harvest_and_pause("clean finish" if clean else "failure or timeout")
        after = len(json.loads(Path("parcel_vectors.json").read_text()))
        log(f"banked {after - before} new clips this batch; {after}/70 total")
        if not clean:
            log("stopping after a non-clean batch — inspect before continuing"); raise SystemExit(1)
        if not a.loop or after >= 70:
            break
    log("done")
