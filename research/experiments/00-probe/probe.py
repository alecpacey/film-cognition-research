#!/usr/bin/env python3
"""
00 — Discrimination probe.

Does TRIBE distinguish a landscape from a crowd from a face?

Everything downstream assumes it does. Run this before spending anything.
Pass criteria are in README.md and were written before the first run.

    python probe.py clips/landscape.mp4 clips/crowd.mp4 clips/face.mp4

Notes on the choices here, all of which are guarding against something specific:

  * Clips shorter than 30 s are REFUSED, not warned about. TRIBE was trained on
    100-second windows; below ~30 s it returns diffuse low-intensity output and
    raises nothing. A silent wrong answer is worse than a crash.
  * Everything is ranked on z-scored values. The training target was per-sample
    z-scored and detrended, so absolute magnitudes carry no meaning, and the real
    magnitudes are tiny — a natural face drives fusiform to about +0.080 z.
    Any absolute threshold would simply never fire.
  * preds.shape is printed rather than assumed. The shipped config says 1 Hz but
    the paper does not state the TR in the retrievable section, and a typical
    1.49 s TR would imply ~0.67 Hz. One run settles it.
  * Video-only inference is the default. It skips the Llama-3.2-3B branch, which
    also skips the gated Meta licence, the HF_TOKEN requirement, and a whisperx
    subprocess per clip.
"""

import argparse
import json
import os
import subprocess
import sys
from itertools import combinations
from pathlib import Path

MIN_SECONDS = 30.0        # below this TRIBE returns noise without erroring
TRAINED_SECONDS = 100.0   # duration_trs=100 — the window it actually learned on
TOP_K = 10


def die(msg):
    print(f"\n  STOP: {msg}\n", file=sys.stderr)
    sys.exit(1)


def duration_of(path):
    """Seconds, via ffprobe. Returns None if it cannot be determined."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)],
            capture_output=True, text=True, timeout=60,
        )
        return float(out.stdout.strip())
    except Exception:
        return None


def check_clips(paths):
    print("Input clips")
    print("-" * 68)
    problems = []
    for p in paths:
        if not Path(p).exists():
            problems.append(f"{p} does not exist")
            continue
        d = duration_of(p)
        if d is None:
            problems.append(f"{p}: could not read duration (is ffmpeg installed?)")
            continue
        if d < MIN_SECONDS:
            flag = "TOO SHORT — will return noise"
            problems.append(f"{p} is {d:.1f}s, under the {MIN_SECONDS:.0f}s floor")
        elif d < TRAINED_SECONDS:
            flag = f"ok, but under the {TRAINED_SECONDS:.0f}s training window"
        else:
            flag = "ok"
        print(f"  {Path(p).name:<24} {d:7.1f}s   {flag}")
    print()
    if problems:
        die("clip problems:\n    - " + "\n    - ".join(problems))


def load_tribe(cache_folder):
    try:
        from tribev2 import TribeModel
    except ImportError as e:
        die(
            "cannot import tribev2.\n"
            "    Install it with:\n"
            '      pip install "git+https://github.com/facebookresearch/tribev2@refs/pull/67/head"\n'
            "    Upstream main does not import — exca is left unpinned and a removed API breaks it.\n"
            f"    Underlying error: {e}"
        )
    print("Loading TRIBE (first run downloads several GB of backbones)...")
    return TribeModel.from_pretrained("facebook/tribev2", cache_folder=cache_folder)


def score(model, clip):
    """Return predictions as (T, n_vertices) float array."""
    df = model.get_events_dataframe(video_path=str(clip))
    result = model.predict(events=df)
    # predict() returns (ndarray, list) — segments are not needed here
    preds = result[0] if isinstance(result, tuple) else result
    import numpy as np
    return np.asarray(preds, dtype="float32")


def top_regions(preds, k=TOP_K):
    """
    Z-score over the timeline, average, and rank HCP parcels.

    Returns (ranked_names, per_parcel_zscores_dict).
    Falls back to raw vertex indices if the shipped helpers are unavailable,
    so a helper-API change degrades the output rather than killing the run.
    """
    import numpy as np

    # z-score each vertex over time; absolute values are meaningless, only dynamics
    mu = preds.mean(axis=0, keepdims=True)
    sd = preds.std(axis=0, keepdims=True)
    sd = np.maximum(sd, 1e-3)          # floor, or quiet vertices explode
    z = (preds - mu) / sd
    mean_z = z.mean(axis=0)            # one value per vertex

    try:
        from tribev2 import utils as tu
        ranked = tu.get_topk_rois(mean_z, k=k)
        names = [r[0] if isinstance(r, (tuple, list)) else str(r) for r in ranked]
        parcels = {}
        try:
            summary = tu.summarize_by_roi(mean_z)
            labels = tu.get_hcp_labels()
            parcels = {str(l): float(v) for l, v in zip(labels, np.asarray(summary).ravel())}
        except Exception:
            pass
        return names, parcels
    except Exception as e:
        print(f"  ! tribev2.utils unavailable ({e}); falling back to vertex indices")
        idx = np.argsort(mean_z)[::-1][:k]
        return [f"vertex_{i}" for i in idx], {}


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if (a | b) else 1.0


def main():
    ap = argparse.ArgumentParser(description="TRIBE discrimination probe")
    ap.add_argument("clips", nargs="+", help="video files, each >= 30s")
    ap.add_argument("--cache", default="./cache", help="model cache folder")
    ap.add_argument("--out", default="out/probe_results.json")
    ap.add_argument("--k", type=int, default=TOP_K)
    args = ap.parse_args()

    os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "300")
    os.environ.setdefault("HF_HUB_HTTP_TIMEOUT", "300")

    check_clips(args.clips)
    model = load_tribe(args.cache)

    results, shapes = {}, {}
    for clip in args.clips:
        name = Path(clip).stem
        print(f"Scoring {name} ...")
        preds = score(model, clip)
        shapes[name] = list(preds.shape)
        # This line answers the disputed prediction rate. Record it.
        dur = duration_of(clip)
        rate = preds.shape[0] / dur if dur else float("nan")
        print(f"  preds.shape = {preds.shape}   ->  {rate:.2f} rows/second")
        names, parcels = top_regions(preds, k=args.k)
        results[name] = {"top": names, "parcels": parcels,
                         "shape": list(preds.shape), "rows_per_second": rate}
        print(f"  top {args.k}: {', '.join(names[:args.k])}\n")

    # ---- pass criteria, as written in README.md before the first run ----
    print("=" * 68)
    print("Separation")
    print("-" * 68)
    overlaps = []
    for a, b in combinations(results, 2):
        j = jaccard(results[a]["top"], results[b]["top"])
        overlaps.append(j)
        print(f"  {a:<14} vs {b:<14} Jaccard overlap {j:.2f}")
    mean_overlap = sum(overlaps) / len(overlaps) if overlaps else 1.0
    separated = mean_overlap < 0.6
    print(f"\n  mean overlap {mean_overlap:.2f}  ->  "
          f"{'SEPARATED (criterion 1 met)' if separated else 'NOT SEPARATED (criterion 1 failed)'}")
    print("\n  Criterion 2 (direction) is a judgement call — inspect the region")
    print("  names above against the expectations in README.md and record the")
    print("  verdict in RESULT.md. Do not soften the criteria after the fact.")
    print("=" * 68)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump({"results": results, "shapes": shapes,
                   "mean_top_k_overlap": mean_overlap,
                   "criterion_1_separation": separated}, f, indent=2)
    print(f"\nWrote {args.out}")
    print("Now write RESULT.md and add a line to ../LOG.md — including if this crashed.")


if __name__ == "__main__":
    main()
