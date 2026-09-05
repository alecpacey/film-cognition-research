#!/usr/bin/env python3
"""
Watch a stage-02 Space run and surface anything that goes wrong.

TRIBE fails silently more often than it crashes, and the Space fails in ways that
never reach stdout at all — run 00's log records "Scheduling failure: not enough
hardware capacity" and clips silently dropped by .gitignore. So this watches BOTH
the runtime stage and the log stream, and treats silence as suspicious rather than
as success.

Emits one line per event. Exits when every expected clip has reported, or when the
run enters a terminal error state.
"""
import json, socket, sys, time, urllib.request
from huggingface_hub import HfApi, get_token

SPACE = "alecnpacey/tribe-probe"
EXPECTED = int(sys.argv[1]) if len(sys.argv) > 1 else 4
POLL = 60
api = HfApi()

BAD_STAGE = {"BUILD_ERROR", "RUNTIME_ERROR", "CONFIG_ERROR", "DELETING", "PAUSED", "STOPPED"}
ERR_PAT = ("Traceback", "Error", "ERROR", "FAILED", "Scheduling failure",
           "not enough hardware", "CUDA", "OutOfMemory", "Killed", "PROBE FAILED",
           "No clips found", "401", "403")


def logs(deadline=25, idle=5):
    """Snapshot the log without hanging.

    The first version of this function blocked forever and reported nothing while
    the run finished underneath it, leaving the Space idling on billed hardware.
    `/logs/run` is a LIVE SSE stream: it does not close while the Space is RUNNING,
    so `for raw in r:` never terminates. Read to a wall-clock deadline, stop when
    the socket goes quiet, and always close.
    """
    req = urllib.request.Request(
        f"https://huggingface.co/api/spaces/{SPACE}/logs/run",
        headers={"Authorization": f"Bearer {get_token()}"})
    out, t0 = [], time.time()
    try:
        r = urllib.request.urlopen(req, timeout=20)
    except Exception as e:
        print(f"[watch] log fetch failed: {type(e).__name__}: {e}", flush=True)
        return out
    try:
        try: r.fp.raw._sock.settimeout(idle)
        except Exception: pass
        while time.time() - t0 < deadline:
            try:
                raw = r.readline()
            except (socket.timeout, TimeoutError, OSError):
                break
            if not raw:
                break
            l = raw.decode("utf-8", "replace")
            if l.startswith("data: "):
                try: out.append(json.loads(l[6:])["data"])
                except Exception: pass
    finally:
        r.close()
    return out


def main():
    seen_stage, seen_lines, done, t0 = None, set(), set(), time.time()
    print(f"[watch] {SPACE}, expecting {EXPECTED} clips", flush=True)
    while True:
        el = (time.time() - t0) / 60
        try:
            rt = api.space_info(SPACE).runtime
            stage, hw = rt.stage, (rt.hardware or "unallocated")
        except Exception as e:
            print(f"[watch] {el:5.1f}m  space_info failed: {type(e).__name__}: {e}", flush=True)
            time.sleep(POLL); continue

        if stage != seen_stage:
            print(f"[watch] {el:5.1f}m  stage -> {stage}  (hw {hw})", flush=True)
            seen_stage = stage
        if stage in BAD_STAGE:
            print(f"[watch] {el:5.1f}m  TERMINAL STAGE {stage} — stopping", flush=True)
            return 1

        if stage == "RUNNING":
            for l in logs():
                if l in seen_lines:
                    continue
                seen_lines.add(l)
                if l.startswith("PARCELCOUNT\t"):
                    _, clip, n = l.split("\t")
                    done.add(clip)
                    flag = "" if n.strip() == "180" else f"  ** expected 180, got {n.strip()}"
                    print(f"[watch] {el:5.1f}m  CLIP DONE {clip}: {n.strip()} parcels{flag}  "
                          f"({len(done)}/{EXPECTED})", flush=True)
                elif any(p in l for p in ERR_PAT):
                    print(f"[watch] {el:5.1f}m  ERROR LINE: {l.strip()[:200]}", flush=True)
                elif l.startswith("timeline ") or "reduced to" in l:
                    print(f"[watch] {el:5.1f}m  {l.strip()[:160]}", flush=True)

            if len(done) >= EXPECTED:
                print(f"[watch] {el:5.1f}m  ALL {EXPECTED} CLIPS REPORTED — harvest now", flush=True)
                return 0

        if el > 120:
            print(f"[watch] {el:5.1f}m  TIMEOUT — {len(done)}/{EXPECTED} clips after 2 h", flush=True)
            return 1
        time.sleep(POLL)


if __name__ == "__main__":
    sys.exit(main())
