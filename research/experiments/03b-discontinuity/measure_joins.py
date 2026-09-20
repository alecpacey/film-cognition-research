#!/usr/bin/env python3
"""Preconditions for 03b, measured before scoring: per clip, constructed joins vs cuts detected by
cinemetrics.cuts() (unchanged), discontinuity size at each join, duration, and decoded-audio MD5.
REF (stage 03 S-) is measured the same way for the magnitude axis.   python3 measure_joins.py -> joins.json"""
import json, subprocess, sys, hashlib
from pathlib import Path
import numpy as np, cv2
H = Path(__file__).parent; sys.path.insert(0, str(H.parent.parent / "cinematography"))
from cinemetrics import read_frames, cuts
LADDERS = {"REF": H.parent / "03-isolation" / "clips" / "Sminus", "B": H / "clips" / "B", "C": H / "clips" / "C", "D": H / "clips" / "D"}
def hist(bgr):
    h = cv2.calcHist([cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)], [0, 1, 2], None, [16, 4, 4], [0, 180, 0, 256, 0, 256]).ravel(); return h / max(h.sum(), 1)
def audio_md5(p):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-t", "59.9", "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True)
    return hashlib.md5(r.stdout).hexdigest(), len(r.stdout)
out = {}
for lad, d in LADDERS.items():
    for n in (1, 3, 7, 15, 31):
        p = d / f"cut{n:02d}.mp4"; fr = list(read_frames(str(p), 480, 1)); fps = 24.0
        det, scores = cuts(iter(fr)); det_t = np.array(det) / fps; joins = np.arange(1, n + 1) * ((len(fr) / fps) / (n + 1))   # actual duration: the builder's clips run slightly short at high cut counts
        hs = np.array([hist(b) for _, b in fr]); sc = np.array(scores)
        hit = sum(bool(np.any(np.abs(det_t - j) <= 0.35)) for j in joins)
        peak, hd = [], []
        for j in joins:
            k = int(round(j * fps)); lo, hi = max(1, k - 8), min(len(sc), k + 8); peak.append(float(sc[lo - 1:hi].max()))
            a, b = hs[max(0, k - 30):max(1, k - 10)].mean(0), hs[min(len(hs) - 1, k + 10):min(len(hs), k + 30)].mean(0); hd.append(float(0.5 * np.abs(a - b).sum()))
        md5, nbytes = audio_md5(p)
        out[f"{lad}_cut{n:02d}"] = {"constructed": n, "detected_total": len(det), "joins_detected": hit, "stray_detections": int(len(det) - hit),
                                     "peak_frame_delta_at_joins_mean": float(np.mean(peak)), "hist_dist_across_joins_mean": float(np.mean(hd)),
                                     "median_frame_delta": float(np.median(sc)), "n_frames": len(fr), "duration_s": len(fr) / fps, "audio_md5": md5, "audio_bytes": nbytes}
        o = out[f"{lad}_cut{n:02d}"]
        print(f"{lad:3} cut{n:02d}  detected {o['joins_detected']:2}/{n:2} joins (+{o['stray_detections']} stray)  peak Δ at joins {o['peak_frame_delta_at_joins_mean']:6.1f}  hist dist {o['hist_dist_across_joins_mean']:.3f}  dur {o['duration_s']:.2f}s  audio {md5[:8]}", flush=True)
(H / "joins.json").write_text(json.dumps(out, indent=1))
md = {v["audio_md5"] for v in out.values()}; print(f"\ndistinct decoded-audio MD5s across all 20 clips: {len(md)}")
for lad in LADDERS:
    v = [out[f"{lad}_cut{n:02d}"] for n in (1, 3, 7, 15, 31)]
    print(f"{lad:3} joins detected {sum(x['joins_detected'] for x in v)}/{57}  = {100*sum(x['joins_detected'] for x in v)/57:.0f}%   mean peak Δ {np.mean([x['peak_frame_delta_at_joins_mean'] for x in v]):.1f}   mean hist dist {np.mean([x['hist_dist_across_joins_mean'] for x in v]):.3f}")
