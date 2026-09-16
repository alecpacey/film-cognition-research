#!/usr/bin/env python3
"""
EXPLORATORY, 16 Sep 2026. Between-scene vs within-scene cuts.

frontal_miss.md left one hypothesis standing: inferior-frontal cortex tracks *scene
switches*, which equal cuts in the stage-01/03 intercut ladders and mostly do not in cinema.
CORPUS.md specified a per-segment scene-boundary count that was never implemented. This is it.

Cuts are detected with cinemetrics.cuts() unchanged (same frames, same parameters), so the
cut count reproduces the registered dial. Each cut is then scored by how different the shot
after it is from the shot before it — the mean HSV histogram (16x4x4, L1-normalised) and an
8x8 grey thumbnail of each shot, frames within 2 of a cut excluded — and a cut is called
BETWEEN-scene when the histogram distance exceeds a threshold. The threshold is calibrated on
stage 01's ladder, where the 1/3/7/15/31 imposed face<->landscape cuts are between-scene by
construction and the sources' own ~22 internal cuts are within-scene, and checked on stage
03's ladder, where every cut is between-scene and the single-take bases have none.

    python3 scene_switches.py --validate            # stage 01 + 03 clips -> scene_switches_validation.json
    python3 scene_switches.py --corpus [--workers N] # 244 segments -> scene_switches_corpus.jsonl (append, resumable)
"""
import argparse, json, sys, time
from pathlib import Path
from multiprocessing import Pool
import numpy as np, cv2
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "cinematography"))
from cinemetrics import read_frames, cuts   # noqa: E402  identical cut detector

H_BINS, S_BINS, V_BINS, THUMB, GUARD = 16, 4, 4, 8, 2


def frame_signature(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [H_BINS, S_BINS, V_BINS], [0, 180, 0, 256, 0, 256]).ravel()
    hist /= max(hist.sum(), 1.0)
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    thumb = cv2.resize(g, (THUMB, THUMB), interpolation=cv2.INTER_AREA).astype(np.float32).ravel() / 255.0
    return hist.astype(np.float32), thumb


def analyse(path):
    path = str(path)
    hists, thumbs, idxs = [], [], []
    def gen():                      # single pass; no frame is retained (memory)
        for idx, bgr in read_frames(path, 480, 1):
            h, t = frame_signature(bgr)
            hists.append(h); thumbs.append(t); idxs.append(idx)
            yield idx, bgr
    cut_idx, scores = cuts(gen())
    hists, thumbs, idxs = np.array(hists), np.array(thumbs), np.array(idxs)
    n = len(idxs)
    # shot boundaries in positional terms
    cut_pos = [int(np.searchsorted(idxs, c)) for c in cut_idx]
    bounds = [0] + cut_pos + [n]
    shots = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        lo, hi = a + (GUARD if a > 0 else 0), b - (GUARD if b < n else 0)
        if hi <= lo: lo, hi = a, b
        shots.append((lo, hi))
    sig_h = np.array([hists[lo:hi].mean(0) for lo, hi in shots])
    sig_t = np.array([thumbs[lo:hi].mean(0) for lo, hi in shots])
    per_cut = []
    for k, c in enumerate(cut_idx):
        dh = float(0.5 * np.abs(sig_h[k + 1] - sig_h[k]).sum())           # 0..1
        dt = float(np.sqrt(((sig_t[k + 1] - sig_t[k]) ** 2).mean()))     # 0..1
        per_cut.append({"frame": int(c), "hist_dist": round(dh, 4), "thumb_dist": round(dt, 4),
                        "shot_len_before": int(shots[k][1] - shots[k][0]), "shot_len_after": int(shots[k + 1][1] - shots[k + 1][0])})
    cap = cv2.VideoCapture(path); fps = cap.get(cv2.CAP_PROP_FPS) or 24.0; cap.release()
    dur = n / fps
    return {"clip": Path(path).stem, "n_frames": int(n), "duration_s": round(dur, 3), "n_cuts": len(cut_idx),
            "cuts_per_min": round(len(cut_idx) / dur * 60, 2), "cuts": per_cut}


def summarise(rec, thresholds):
    d = np.array([c["hist_dist"] for c in rec["cuts"]]) if rec["cuts"] else np.array([])
    out = {"n_cuts": rec["n_cuts"], "cuts_per_min": rec["cuts_per_min"],
           "sum_hist_dist": float(d.sum()), "mean_hist_dist": float(d.mean()) if d.size else 0.0,
           "max_hist_dist": float(d.max()) if d.size else 0.0}
    for t in thresholds:
        out[f"between_scene_ge_{t}"] = int((d >= t).sum())
    return out


def _work(p):
    try:
        return analyse(p)
    except Exception as e:
        return {"clip": Path(p).stem, "error": f"{type(e).__name__}: {e}"}


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--validate", action="store_true"); g.add_argument("--corpus", action="store_true")
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    t0 = time.time()
    if a.validate:
        clips = sorted((HERE.parent / "01-cutrate" / "clips").glob("cut*.mp4"))
        clips += sorted((HERE.parent / "03-isolation" / "clips" / "Splus").glob("cut*.mp4"))
        clips += [HERE.parent / "03-isolation" / "clips" / n for n in ("face_close.mp4", "landscape.mp4")]
        clips = [c for c in clips if c.exists()]
        with Pool(a.workers) as pool:
            recs = pool.map(_work, [str(c) for c in clips])
        out = {}
        for c, r in zip(clips, recs):
            key = f"{c.parent.parent.name if c.parent.name in ('Splus','clips') and '03' in str(c) else c.parent.parent.name}/{c.stem}"
            out[key] = r
            if "error" in r: print(key, r["error"]); continue
            d = sorted(cc["hist_dist"] for cc in r["cuts"])
            print(f"{key:28} cuts {r['n_cuts']:3}  hist_dist: " + " ".join(f"{x:.2f}" for x in d))
        (HERE / "scene_switches_validation.json").write_text(json.dumps(out, indent=1))
        print(f"wrote scene_switches_validation.json ({time.time()-t0:.0f}s)")
    else:
        segs = sorted((HERE / "segments").glob("*.mp4"))
        outp = HERE / "scene_switches_corpus.jsonl"
        done = set()
        if outp.exists():
            done = {json.loads(l)["clip"] for l in outp.read_text().splitlines() if l.strip()}
        todo = [str(s) for s in segs if s.stem not in done]
        print(f"{len(segs)} segments, {len(done)} done, {len(todo)} to do, {a.workers} workers", flush=True)
        with Pool(a.workers) as pool, outp.open("a") as f:
            for i, r in enumerate(pool.imap_unordered(_work, todo), 1):
                f.write(json.dumps(r) + "\n"); f.flush()
                if i % 10 == 0 or "error" in r:
                    print(f"[{time.strftime('%H:%M:%S')}] {i}/{len(todo)} {r['clip']} " + (r.get("error") or f"cuts {r['n_cuts']}"), flush=True)
        print(f"done ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
