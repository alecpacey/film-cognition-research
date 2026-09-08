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
import argparse, json, re, socket, subprocess, sys, time, urllib.request
from pathlib import Path
from huggingface_hub import HfApi, get_token

SPACE = "alecnpacey/tribe-probe"
POLL = 60
MAX_MIN_PER_CLIP = 25          # generous: ~10 min is normal, this only catches hangs

# The Space's own sleep timer (gcTimeout) is 7200 s and it fires on INACTIVITY —
# which, for a run driven by an AUTORUN background thread, means no HTTP traffic
# even while the GPU is flat out. Batch 2 was cut off at exactly 2.0 h with 11 of
# 20 clips scored. HANDOFF.md's standing rule ("sleep timer is 7200 s so it will
# not nap mid-run") was formed when runs were ~45 min and is false beyond ~11 clips.
#
# The timer is left ON deliberately: it is what stopped 6.75 h of stalled run from
# costing anything. Batches are kept comfortably inside it instead.
SLEEP_TIMER_S = 7200
# Measured: ~10.9 min/clip plus ~10 min startup (manifest fetch, model load), so
# 10 clips is ~120 min — exactly the timer, no margin. Batch 6 lost its 10th clip
# to it. Eight clips is ~97 min, leaving ~20 min spare.
SAFE_BATCH = 8

# The Space sleeps on HTTP INACTIVITY. Pinging its URL each poll resets that clock,
# so the timer can no longer cut a healthy run short — while still firing if this
# process dies and the pings stop. That turns it from a hazard into a dead-man's
# switch, which is what it should have been all along.
SPACE_URL = "https://alecnpacey-tribe-probe.hf.space/"


def keepalive():
    try:
        req = urllib.request.Request(SPACE_URL, headers={"Authorization": f"Bearer {get_token()}"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status
    except Exception as e:
        return f"{type(e).__name__}"
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


def fetch(deadline=90, idle=6):
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


def flush_vectors(pending):
    """Merge streamed parcel vectors into parcel_vectors.json. Idempotent."""
    if not pending: return
    p = Path("parcel_vectors.json")
    data = json.loads(p.read_text()) if p.exists() else {}
    for clip, vec in pending.items():
        if len(vec) == 180:                 # only bank complete vectors
            data.setdefault(clip, {}).update(vec)
    p.write_text(json.dumps(data, indent=1))


RESULTS_REPO = "alecnpacey/tribe-probe-results"


def result_files():
    """Clips whose vectors are already durable in the results repo (prefix stripped)."""
    try:
        return {re.sub(r"^\d{2}_", "", Path(f).stem)
                for f in api.list_repo_files(RESULTS_REPO, repo_type="dataset")
                if f.startswith("results/") and f.endswith(".json")}
    except Exception as e:
        log(f"results listing failed: {type(e).__name__}: {e}"); return None


def wait_for(n_expected, batch_clips):
    """Poll until every clip's RESULT FILE exists, or something goes wrong.

    Completion is judged by files in the results repo, NOT by the log: the log
    goes blind after ~5 clips (HF serves a bounded window from its start), so a
    log-based count would time out on a batch that had in fact finished. The log
    is still read, for error signatures only.
    """
    t0, done, seen = time.time(), set(), set()
    pending_vecs = {}
    want = set(batch_clips)
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
            ka = keepalive()
            if ka != 200 and int(el) % 10 == 0:
                log(f"keepalive: {ka}")
            for l in fetch():
                if l in seen: continue
                seen.add(l)
                if l.startswith("PARCEL\t"):
                    # Bank the vector AS IT STREAMS PAST. The overnight run lost
                    # eight paid clips because harvesting happened at the end of
                    # the batch: HF's /logs/run does NOT retain the full backlog,
                    # so clips the watcher had already seen live were unreadable
                    # minutes later. "Results survive only in logs" is true only
                    # while you are watching. So persist immediately.
                    try:
                        _, clip, parcel, rawv, zv = l.split("\t")
                    except ValueError:
                        continue
                    clip = re.sub(r"^\d{2}_", "", clip)
                    pending_vecs.setdefault(clip, {})[parcel] = {
                        "raw": float(rawv), "z": float(zv)}
                elif l.startswith("PARCELCOUNT\t"):
                    _, clip, cnt = l.split("\t")
                    if cnt.strip() != "180":
                        log(f"** {clip} reported {cnt.strip()} parcels, not 180 **")
                    flush_vectors(pending_vecs)          # log-path fallback banking
                elif l.startswith("RESULT_UPLOAD\t") and "FAILED" in l:
                    log(f"UPLOAD FAILED: {l.strip()[:160]}")
                elif l.startswith("PROBE FAILED"):
                    # The scoring thread died at startup (7 Sep: osf.io refused MNE's
                    # 1.5 GB sample dataset). Gradio stays up so the stage reads
                    # RUNNING forever; without this the batch bills for its full
                    # timeout doing nothing.
                    log("PROBE FAILED at startup — scoring never began; stopping")
                    return False
                elif any(p in l for p in ERR_PAT) and not _benign(l, seen):
                    log(f"ERROR: {l.strip()[:180]}")
        # authoritative completion check: durable files, not log lines
        have = result_files()
        if have is not None:
            newly = (have & want) - done
            for c in sorted(newly):
                done.add(c)
                log(f"clip {len(done)}/{n_expected}: {c} -> result file present")
            if want <= have:
                log(f"all {n_expected} result files present after {el:.0f} min"); return True
        if el > budget:
            log(f"TIMEOUT after {el:.0f} min with {len(done)}/{n_expected}"); return False
        time.sleep(POLL)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=SAFE_BATCH)
    ap.add_argument("--loop", action="store_true", help="continue until nothing is pending")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()

    if a.status:
        run(["run_batch.py", "--plan"]); raise SystemExit

    if a.batch > SAFE_BATCH:
        est_h = a.batch * 10 / 60
        log(f"REFUSING --batch {a.batch}: ~{est_h:.1f} h of scoring against a "
            f"{SLEEP_TIMER_S/3600:.1f} h Space sleep timer. The Space would nap "
            f"mid-run and the tail of the batch would be lost. Use --batch "
            f"{SAFE_BATCH} or lower.")
        raise SystemExit(2)

    while True:
        rc = run(["run_batch.py", "--batch", str(a.batch)])
        if rc != 0:
            log("upload/restart failed — stopping"); raise SystemExit(1)
        vecs = json.loads(Path("parcel_vectors.json").read_text()) if Path("parcel_vectors.json").exists() else {}
        before = len(vecs)
        # which clips did run_batch just stage? read the manifest it wrote
        from huggingface_hub import hf_hub_download
        m = hf_hub_download("alecnpacey/tribe-probe-clips", "batch.json",
                            repo_type="dataset", force_download=True)
        staged = json.loads(Path(m).read_text())["clips"]
        clean = wait_for(len(staged), staged)
        harvest_and_pause("clean finish" if clean else "failure or timeout")
        after = len(json.loads(Path("parcel_vectors.json").read_text()))
        log(f"banked {after - before} new clips this batch; {after}/70 total")
        if not clean:
            log("stopping after a non-clean batch — inspect before continuing"); raise SystemExit(1)
        if not a.loop or after >= 70:
            break
    log("done")
