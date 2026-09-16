#!/usr/bin/env python3
"""
Stage, score and harvest the eight x1 blocks on the existing TRIBE Space.

Deliberately NOT run_batch.py / auto_batch.py: their harvest merges every file in
the results repo into 02-index/parcel_vectors.json, which is frozen and whose hash
is in the OSF registration. This driver writes only to x1-av-emotion/results/.

The Space itself is unchanged — same app, same scoring path as stage 02. A batch is
still a manifest (batch.json in the clips repo) plus a restart.

    python run_x1.py --run        # upload, restart, poll, harvest, pause
    python run_x1.py --harvest    # fetch whatever x1 results exist, then pause
    python run_x1.py --migrate    # move the 11 Sep pilot's x1 files out of the shared
                                  # stage-02 results repo into x1's own repo (copy,
                                  # verify, then delete), after local copies are verified

RESULTS REPO SPLIT (15 Sep 2026). x1 writes to its own results repo,
`alecnpacey/x1-av-emotion-results`. The Space's app reads RESULTS_REPO from its
environment at start-up, so --run sets that Space variable while the Space is paused,
verifies it, restarts, and restores it to the programme's shared repo on every exit
path. The programme's own scorers keep using `alecnpacey/tribe-probe-results` with
exact-name matching. Reason: on 14 Sep a stage-03 watcher matching "03_" anywhere
harvested x1's files from the shared repo and paused the run at 6/12.
"""
import argparse, json, re, socket, time, urllib.request
from pathlib import Path
from huggingface_hub import HfApi, get_token, hf_hub_download, CommitOperationAdd, CommitOperationDelete

HERE = Path(__file__).parent
SPACE = "alecnpacey/tribe-probe"
SPACE_URL = "https://alecnpacey-tribe-probe.hf.space/"
CLIPS_REPO = "alecnpacey/tribe-probe-clips"
RESULTS_REPO = "alecnpacey/x1-av-emotion-results"          # x1's own, from 15 Sep 2026
SHARED_RESULTS_REPO = "alecnpacey/tribe-probe-results"     # the programme's; never write here
RESULTS = HERE / "results"
POLL = 60
MAX_MIN_PER_CLIP = 25
BAD_STAGE = {"BUILD_ERROR", "RUNTIME_ERROR", "CONFIG_ERROR", "DELETING"}
ERR_PAT = ("Scheduling failure", "not enough hardware", "OutOfMemory", "CUDA error",
           "Killed", "PROBE FAILED", "No clips found")
# face blocks first: C1 needs only these four
ORDER = ["x1_A_HAP_face", "x1_A_ANG_face", "x1_B_HAP_face", "x1_B_ANG_face",
         "x1_A_HAP_blank", "x1_A_ANG_blank", "x1_B_HAP_blank", "x1_B_ANG_blank"]
api = HfApi()


def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)


def keepalive():
    try:
        req = urllib.request.Request(SPACE_URL, headers={"Authorization": f"Bearer {get_token()}"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status
    except Exception as e:
        return type(e).__name__


def fetch_logs(deadline=60, idle=6):
    """The logs endpoint is a live SSE stream that never closes: bound every read."""
    req = urllib.request.Request(f"https://huggingface.co/api/spaces/{SPACE}/logs/run",
                                 headers={"Authorization": f"Bearer {get_token()}"})
    out, t0 = [], time.time()
    try:
        r = urllib.request.urlopen(req, timeout=20)
    except Exception as e:
        log(f"log fetch failed: {type(e).__name__}"); return out
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


def x1_result_files(repo=RESULTS_REPO):
    try:
        return {re.sub(r"^\d{2}_", "", Path(f).stem): f
                for f in api.list_repo_files(repo, repo_type="dataset")
                if f.startswith("results/") and f.endswith(".json") and "x1_" in f}
    except Exception as e:
        log(f"results listing failed: {type(e).__name__}"); return None


def bank(have, repo=RESULTS_REPO):
    """Download any x1 result not yet local. Health checks only — no analysis here."""
    RESULTS.mkdir(exist_ok=True)
    for clip, f in have.items():
        dst = RESULTS / f"{clip}.json"
        if dst.exists(): continue
        p = json.loads(Path(hf_hub_download(repo, f, repo_type="dataset",
                                            force_download=True)).read_text())
        zs = [v["z"] for v in p["parcels"].values()]
        bad = []
        if len(zs) != 180: bad.append(f"{len(zs)} parcels")
        if any(z != z for z in zs): bad.append("NaN")
        elif max(abs(z) for z in zs) > 8: bad.append(f"|z| {max(abs(z) for z in zs):.1f}")
        dst.write_text(json.dumps(p, indent=1))
        log(f"banked {clip}  timeline {p.get('timeline_shape')}  "
            + ("HEALTH OK" if not bad else "HEALTH PROBLEM: " + ", ".join(bad)))


def pause(why):
    log(f"pausing ({why})")
    try:
        api.pause_space(SPACE)
    except Exception as e:
        log(f"pause call failed: {type(e).__name__}: {e}")
    for _ in range(5):
        st = api.space_info(SPACE).runtime.stage
        if st in ("PAUSED", "STOPPED", "SLEEPING"):
            log(f"space stage {st} — billing stopped"); return
        time.sleep(10)
    log(f"** space stage still {st} — CHECK MANUALLY, it may be billing **")


IDLE = ("PAUSED", "STOPPED", "SLEEPING")


def space_results_repo():
    v = api.get_space_variables(SPACE)
    x = v.get("RESULTS_REPO")
    return None if x is None else str(getattr(x, "value", x))


def point_space_results_repo(repo):
    """Set the Space's RESULTS_REPO variable and read it back. Only meaningful while the
    Space is paused: the app reads the variable once, at start-up."""
    api.add_space_variable(SPACE, "RESULTS_REPO", repo)
    cur = space_results_repo()
    if cur != repo:
        raise SystemExit(f"STOP: Space RESULTS_REPO reads {cur!r} after setting {repo!r}")
    log(f"Space RESULTS_REPO -> {repo}")


def restore_shared_results_repo():
    try:
        point_space_results_repo(SHARED_RESULTS_REPO)
    except SystemExit as e:
        log(f"** {e} — the programme's scorers expect {SHARED_RESULTS_REPO}; FIX MANUALLY **")
    except Exception as e:
        log(f"** restore of RESULTS_REPO failed: {type(e).__name__}: {e} — FIX MANUALLY **")


def wait_free(max_min, other_pid):
    """The Space is shared. On 11 Sep a 01b scorer staged its own batch on it while
    this run was in flight. Wait until it is paused AND the other driver has exited."""
    import os
    t0 = time.time()
    while True:
        try:
            st = api.space_info(SPACE).runtime.stage
        except Exception as e:
            # a DNS drop killed the first wait on 11 Sep; waiting must survive the network
            log(f"space_info failed while waiting: {type(e).__name__} — retrying"); time.sleep(POLL); continue
        alive = False
        if other_pid:
            try: os.kill(other_pid, 0); alive = True
            except OSError: alive = False
        if st in IDLE and not alive:
            log(f"Space {st}, other driver {'n/a' if not other_pid else 'exited'} — free"); return
        if (time.time() - t0) / 60 > max_min:
            raise SystemExit(f"STOP: Space still {st} (other driver alive={alive}) after {max_min} min")
        time.sleep(POLL)


def run():
    st = api.space_info(SPACE).runtime.stage
    if st not in IDLE:
        raise SystemExit(f"STOP: Space is {st}, not paused — something else may be using it")
    # Stage only what has no banked result. The 11 Sep run lost clip 4 onward to a
    # Space stop; completed clips are never re-scored.
    todo = [n for n in ORDER if not (RESULTS / f"{n}.json").exists()]
    if not todo:
        log("all 8 already banked — nothing to run"); return True
    blocks = [HERE / "blocks" / f"{n}.mp4" for n in todo]
    missing = [b.name for b in blocks if not b.exists()]
    if missing:
        raise SystemExit(f"STOP: blocks missing: {missing}")
    have_remote = {Path(f).stem for f in api.list_repo_files(CLIPS_REPO, repo_type="dataset")
                   if f.startswith("clips/x1_")}
    ops = [CommitOperationAdd(path_in_repo=f"clips/{b.name}", path_or_fileobj=str(b))
           for b in blocks if b.stem not in have_remote]
    ops.append(CommitOperationAdd(path_in_repo="batch.json",
                                  path_or_fileobj=json.dumps({"clips": todo}).encode()))
    api.create_commit(CLIPS_REPO, operations=ops, repo_type="dataset",
                      commit_message=f"x1: {len(todo)} remaining blocks")
    listed = {Path(f).stem for f in api.list_repo_files(CLIPS_REPO, repo_type="dataset")
              if f.startswith("clips/x1_")}
    staged = json.loads(Path(hf_hub_download(CLIPS_REPO, "batch.json", repo_type="dataset",
                                             force_download=True)).read_text())["clips"]
    if staged != todo or not set(todo) <= listed:
        raise SystemExit(f"STOP: staging did not verify. batch.json={staged} listed={sorted(listed)}")
    log(f"staged and verified: {len(todo)} clips {todo} + batch.json in {CLIPS_REPO}")
    # 15 Sep 2026: results go to x1's own repo. Set while paused, restored in `finally`.
    point_space_results_repo(RESULTS_REPO)

    t0, seen, done, last_stage, foreign = time.time(), set(), set(), None, [False]
    budget = len(todo) * MAX_MIN_PER_CLIP + 20
    try:
        api.restart_space(SPACE)
        log("Space restart requested")
        while True:
            el = (time.time() - t0) / 60
            try:
                stage = api.space_info(SPACE).runtime.stage
            except Exception as e:
                log(f"space_info failed: {type(e).__name__}"); time.sleep(POLL); continue
            if stage != last_stage:
                # the 11 Sep run went silent for an hour because transitions were not logged
                log(f"space stage -> {stage}"); last_stage = stage
            if stage in IDLE and el > 3:
                log(f"Space went {stage} mid-run — stopped externally"); return False
            if stage in BAD_STAGE:
                log(f"TERMINAL STAGE {stage}"); return False
            if stage == "RUNNING":
                keepalive()
                for l in fetch_logs():
                    if l in seen: continue
                    seen.add(l)
                    s = l.strip()
                    if s.startswith(("BATCH_FETCH", "clips:", "mode=", "--- ", "timeline ", "top 10",
                                     "PARCELCOUNT", "RESULT_UPLOAD", "loading model")):
                        if "x1_" in s or s.startswith(("BATCH_FETCH", "clips:", "mode=", "loading")):
                            log(f"space: {s[:200]}")
                        if s.startswith("clips:") and "x1_" not in s:
                            log("** the Space fetched a batch that is not x1 — another driver staged it; stopping **")
                            foreign[0] = True
                            return False
                    if s.startswith("PROBE FAILED"):
                        log("PROBE FAILED at startup — stopping"); return False
                    if any(p in s for p in ERR_PAT) and "Exception ignored" not in s:
                        log(f"ERROR: {s[:200]}")
            have = x1_result_files()
            if have is not None:
                mine = {k: v for k, v in have.items() if k in todo}
                for c in sorted(set(mine) - done):
                    done.add(c); log(f"clip {len(done)}/{len(todo)} scored: {c}")
                bank(mine)
                if set(todo) <= set(mine):
                    log(f"all {len(todo)} scored after {el:.0f} min"); return True
            if el > budget:
                log(f"TIMEOUT after {el:.0f} min with {len(done)}/{len(todo)}"); return False
            time.sleep(POLL)
    finally:
        if foreign[0]:
            log("NOT pausing — the Space is running another driver's batch")
            log(f"** that batch started with RESULTS_REPO={RESULTS_REPO}; its results may land in x1's repo — CHECK **")
        else:
            pause("run ended")
        restore_shared_results_repo()


def migrate():
    """Move the 11 Sep pilot's x1 result files from the shared stage-02 results repo into
    x1's own repo: copy the original bytes, verify the listing, then delete the originals.
    Refuses unless every remote file is already banked locally."""
    have = x1_result_files(SHARED_RESULTS_REPO) or {}
    local = {p.stem for p in RESULTS.glob("x1_*.json")}
    if not set(have) <= local:
        raise SystemExit(f"STOP: not every shared-repo x1 result is banked locally: {sorted(set(have) - local)}")
    if not have:
        log(f"nothing to migrate: no x1 files in {SHARED_RESULTS_REPO}"); return
    already = x1_result_files(RESULTS_REPO) or {}
    ops = []
    for clip, f in have.items():
        if f in already.values(): continue
        src = hf_hub_download(SHARED_RESULTS_REPO, f, repo_type="dataset", force_download=True)
        ops.append(CommitOperationAdd(path_in_repo=f, path_or_fileobj=src))
    if ops:
        api.create_commit(RESULTS_REPO, repo_type="dataset", operations=ops,
                          commit_message=f"x1: {len(ops)} pilot results moved from {SHARED_RESULTS_REPO}")
    now = x1_result_files(RESULTS_REPO) or {}
    missing = set(have.values()) - set(now.values())
    if missing:
        raise SystemExit(f"STOP: copy did not verify in {RESULTS_REPO}: {sorted(missing)} — nothing deleted")
    api.create_commit(SHARED_RESULTS_REPO, repo_type="dataset",
                      operations=[CommitOperationDelete(path_in_repo=f) for f in have.values()],
                      commit_message="x1: pilot results moved to alecnpacey/x1-av-emotion-results")
    log(f"moved {len(have)} x1 files {SHARED_RESULTS_REPO} -> {RESULTS_REPO} (local copies in {RESULTS})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--run", action="store_true")
    g.add_argument("--harvest", action="store_true")
    g.add_argument("--migrate", action="store_true")
    ap.add_argument("--wait-free", type=int, default=0, metavar="MIN",
                    help="before --run, wait up to MIN minutes for the Space to be paused")
    ap.add_argument("--other-pid", type=int, default=0, help="another driver that must exit first")
    a = ap.parse_args()
    if a.run:
        if a.wait_free:
            wait_free(a.wait_free, a.other_pid)
        ok = run(); log("CLEAN FINISH" if ok else "NON-CLEAN FINISH — inspect before re-running")
    elif a.harvest:
        have = x1_result_files() or {}
        bank({k: v for k, v in have.items() if k in ORDER}); pause("harvest")
        restore_shared_results_repo()
    else:
        migrate()
