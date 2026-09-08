#!/usr/bin/env python3
"""
Staged, resumable batch runner for stage 02.

Why batches rather than one long run: at ~10 min per 60 s segment, 40 segments is
nearly seven hours of continuous GPU. A single run that dies at hour six loses
everything, and this project has already lost a full result set to the Space's
ephemeral filesystem.

The checkpoint granularity is the clip: the Space prints each segment's 180 parcel
values to stdout as soon as it finishes, and logs survive. So a batch that dies
half-way still banks its completed clips.

Resume is by omission — we upload only segments that have no saved vector yet, so
a re-run never re-scores completed work.

Candidates come from selection.json, NOT from whatever is sitting in segments/.
This matters: segments/ holds all 244 cut windows, and taking "the first N unscored"
alphabetically would score four consecutive segments from the opening of one film —
convenience sampling silently substituted for the stratified design fixed in
README.md, with nothing in the output to reveal it. If selection.json is missing,
this refuses to run rather than guess.

    python run_batch.py --plan          # what would run, no cost
    python run_batch.py --batch 10      # upload 10 unscored segments and run
    python run_batch.py --harvest       # fetch logs, save, pause. Safe any time.
"""
import argparse, json, re, socket, time, urllib.request
from pathlib import Path
from huggingface_hub import HfApi, get_token, hf_hub_download

SPACE = "alecnpacey/tribe-probe"
SEGMENTS = Path("segments")
VECTORS = Path("parcel_vectors.json")
SELECTION = Path("selection.json")
api = HfApi()


def saved():
    return json.loads(VECTORS.read_text()) if VECTORS.exists() else {}


def selected():
    """The pre-registered stratified sample. Absent means the design has not been
    fixed yet, and scoring anything now would be sampling on convenience."""
    if not SELECTION.exists():
        raise SystemExit(
            f"STOP: {SELECTION} not found.\n"
            "  Segments must be chosen by the stratified design in README.md\n"
            "  before any GPU is spent. Run:  python analyse_dials.py --n 60")
    names = json.loads(SELECTION.read_text())["selected"]
    missing = [n for n in names if not (SEGMENTS / f"{n}.mp4").exists()]
    if missing:
        raise SystemExit(f"STOP: {len(missing)} selected segments absent from "
                         f"{SEGMENTS}/, first: {missing[0]}")
    return names


def pending():
    """Unscored selected segments, interleaved round-robin across films.

    Order matters beyond tidiness. Alphabetical order would make batch 0 four
    consecutive segments from one film — no proof the pipeline handles the other
    two prints' encodes — and, worse, would leave any interrupted collection
    unbalanced across films. Dials and parcels are centred WITHIN FILM, so a run
    that dies with one film barely represented cannot estimate that film's mean and
    loses more than the segments it missed. Round-robin makes every prefix balanced.
    """
    done = set(saved())
    sel = selected()
    todo = [n for n in sel if n not in done]

    # Order by which film is FURTHEST BEHIND its share, not plain round-robin.
    # Batch 2 was truncated by the Space's sleep timer, and because the Space
    # processes each batch alphabetically the cut always fell on the end of the
    # alphabet: royal_wedding finished with 3 of 23 while jungle_book had 13.
    # Dials and parcels are centred WITHIN FILM, so a film with three segments
    # has no stable mean. Deficit-first ordering self-corrects that instead of
    # compounding it.
    quota, have = {}, {}
    for n in sel:
        quota[n.rsplit("_", 1)[0]] = quota.get(n.rsplit("_", 1)[0], 0) + 1
    for n in done:
        have[n.rsplit("_", 1)[0]] = have.get(n.rsplit("_", 1)[0], 0) + 1
    by_film = {}
    for n in todo:
        by_film.setdefault(n.rsplit("_", 1)[0], []).append(n)

    order = []
    counts = {f: have.get(f, 0) for f in by_film}
    while any(by_film[f] for f in by_film):
        # the film with the smallest completed fraction of its quota goes next
        f = min((f for f in by_film if by_film[f]),
                key=lambda f: (counts[f] / quota[f], f))
        order.append(by_film[f].pop(0))
        counts[f] += 1
    return [SEGMENTS / f"{n}.mp4" for n in order]


def fetch_logs(deadline=45, idle=5):
    """Snapshot the Space log.

    The endpoint is a LIVE SSE stream: while the Space is RUNNING it never closes,
    so `for raw in r:` blocks forever. That is the real reason run 00's background
    log pollers "were killed silently with no output" — they were not killed, they
    were hanging, and a foreground call hangs identically once the app is live.

    So: read with a hard wall-clock deadline and a socket idle timeout, then close.
    History has already replayed itself here once; this is the fix.
    """
    req = urllib.request.Request(
        f"https://huggingface.co/api/spaces/{SPACE}/logs/run",
        headers={"Authorization": f"Bearer {get_token()}"})
    out, t0 = [], time.time()
    r = urllib.request.urlopen(req, timeout=20)
    try:
        try: r.fp.raw._sock.settimeout(idle)
        except Exception: pass
        while time.time() - t0 < deadline:
            try:
                raw = r.readline()
            except (socket.timeout, TimeoutError, OSError):
                break                      # stream went quiet: we have the backlog
            if not raw:
                break
            l = raw.decode("utf-8", "replace")
            if l.startswith("data: "):
                try: out.append(json.loads(l[6:])["data"])
                except Exception: pass
    finally:
        r.close()
    return out


RESULTS_REPO = "alecnpacey/tribe-probe-results"
CLIPS_REPO = "alecnpacey/tribe-probe-clips"


def harvest():
    """Merge every result file in the dataset repo into the saved set. Idempotent.

    Results are FILES now, uploaded by the Space the moment each clip is scored.
    The log is read only as a fallback. Reason: HF's /logs/run serves a bounded
    window from the start of the log, so once a run passes ~1,500 lines nothing
    printed later is ever readable again — two collection runs were lost to that
    before the cause was found.
    """
    data = saved()
    added = 0
    try:
        files = [f for f in api.list_repo_files(RESULTS_REPO, repo_type="dataset")
                 if f.startswith("results/") and f.endswith(".json")]
    except Exception as e:
        print(f"  ! could not list {RESULTS_REPO}: {type(e).__name__}: {e}")
        files = []
    for f in files:
        clip = re.sub(r"^\d{2}_", "", Path(f).stem)     # drop the upload ordinal
        if clip in data and len(data[clip]) == 180:
            continue                                     # already banked
        try:
            local = hf_hub_download(RESULTS_REPO, f, repo_type="dataset")
            payload = json.loads(Path(local).read_text())
        except Exception as e:
            print(f"  ! {f}: {type(e).__name__}: {e}"); continue
        vec = payload.get("parcels", {})
        if len(vec) == 180:
            data[clip] = {k: {"raw": float(v["raw"]), "z": float(v["z"])} for k, v in vec.items()}
            added += 1
        else:
            print(f"  ! {f}: {len(vec)} parcels, not banked")
    # fallback: anything only in the log window
    for l in fetch_logs():
        if l.startswith("PARCEL\t"):
            _, clip, parcel, raw, z = l.split("\t")
            clip = re.sub(r"^\d{2}_", "", clip)
            if clip in data and len(data[clip]) == 180:
                continue
            data.setdefault(clip, {})[parcel] = {"raw": float(raw), "z": float(z)}
    # never bank a partial vector
    data = {c: v for c, v in data.items() if len(v) == 180}
    VECTORS.write_text(json.dumps(data, indent=1))
    return data, added


def verify(data):
    """Between-batch checkpoint. Pipeline sanity only — NOT the statistical test."""
    problems = []
    # Clips are uploaded with an ordinal prefix (00_, 01_ ...) so the Space's own
    # alphabetical sort follows our deficit-first order; harvest() strips it back
    # off. If that strip ever fails, results would bank under keys that match no
    # segment and silently drop out of the analysis. Catch it here, loudly.
    known = set(json.loads(SELECTION.read_text())["selected"]) if SELECTION.exists() else set()
    if known:
        stray = sorted(set(data) - known)
        if stray:
            problems.append(f"{len(stray)} banked keys match no selected segment "
                            f"(prefix strip failed?): {stray[:3]}")
    for clip, v in data.items():
        if len(v) != 180:
            problems.append(f"{clip}: {len(v)} parcels, expected 180")
        zs = [p["z"] for p in v.values()]
        if any(z != z for z in zs):
            problems.append(f"{clip}: contains NaN")
        elif max(abs(z) for z in zs) > 8:
            problems.append(f"{clip}: |z| up to {max(abs(z) for z in zs):.1f} — implausible")
    return problems


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=0, help="how many unscored segments to run")
    ap.add_argument("--harvest", action="store_true")
    ap.add_argument("--plan", action="store_true")
    a = ap.parse_args()

    data = saved()
    todo = pending()
    print(f"selected: {len(selected())}   scored: {len(data)}   pending: {len(todo)}   "
          f"est. remaining: {len(todo)*10/60:.1f} h GPU, ${len(todo)*0.17:.2f}")

    if a.plan:
        for p in todo[:20]: print("  ", p.name)
        raise SystemExit

    if a.harvest:
        data, added = harvest()
        print(f"harvested — now hold {len(data)} clips ({added} new)")
        for p in verify(data): print("  PROBLEM:", p)
        api.pause_space(SPACE)
        print("Space paused, billing stopped")
        raise SystemExit

    if a.batch:
        batch = todo[:a.batch]
        if not batch:
            print("nothing pending"); raise SystemExit
        # A batch is a MANIFEST, not an upload. Clips live in CLIPS_REPO (uploaded
        # once); the Space reads batch.json at start, fetches those clips, and scores
        # them in manifest order via an ordinal prefix that harvest() strips again.
        # Pushing mp4s into the Space repo hit its 1 GB storage cap on 6 Sep.
        names = [p.stem for p in batch]
        have = {Path(f).stem for f in api.list_repo_files(CLIPS_REPO, repo_type="dataset")
                if f.startswith("clips/")}
        missing = [n for n in names if n not in have]
        if missing:
            raise SystemExit(f"STOP: {len(missing)} batch clips absent from {CLIPS_REPO}: {missing[:3]}")
        api.upload_file(path_or_fileobj=json.dumps({"clips": names}).encode(),
                        path_in_repo="batch.json", repo_id=CLIPS_REPO, repo_type="dataset",
                        commit_message=f"batch: {len(names)} clips")
        print(f"uploaded {len(batch)}: {names}")
        api.restart_space(SPACE)
        print(f"Space restarting — ~{len(batch)*10 + 5} min. "
              f"Then: python run_batch.py --harvest")
