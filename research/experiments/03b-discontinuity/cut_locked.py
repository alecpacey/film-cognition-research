#!/usr/bin/env python3
"""EXPLORATORY, reported not gating (README). Cut-locked response from the saved 1 Hz parcel timelines.
At each time point the 180 parcel values are standardised across parcels (as the clip-level z is), projected on the
unit REF mode, and epoched -3..+12 s around each constructed join for levels 1, 3, 7 (joins >= 7.5 s apart),
baseline = mean of -3..-1. Also the sustained level: mean projection over the whole clip, per level.
    ../02-index/.venv-analysis/bin/python cut_locked.py -> cut_locked.json"""
import json, numpy as np
from pathlib import Path
H = Path(__file__).parent; REF = json.loads((H / "reference_mode.json").read_text()); parcels = REF["parcels"]
m = np.array(REF["reference_slopes_Sminus"]); mh = m / np.linalg.norm(m)
tl = json.loads((H / "timelines.json").read_text()); pv = json.loads((H / "parcel_vectors.json").read_text())
LV = {"cut01": 1, "cut03": 3, "cut07": 7, "cut15": 15, "cut31": 31}; PRE, POST = 3, 12
out = {}
for lad in ("REF", "B", "C", "D"):
    ep, sustained = [], {}
    for c, n in LV.items():
        T = np.array([tl[f"{lad}_{c}"]["parcel_timeline"][p] for p in parcels]).T          # (60, 180)
        Zt = (T - T.mean(1, keepdims=True)) / np.maximum(T.std(1, keepdims=True), 1e-6); proj = Zt @ mh
        sustained[c] = float(proj.mean())
        if n > 7: continue
        dur = len(proj); joins = [(k + 1) * dur / (n + 1) for k in range(n)]
        for j in joins:
            k = int(round(j)); lo, hi = k - PRE, k + POST + 1
            if lo < 0 or hi > dur: continue
            seg = proj[lo:hi]; ep.append(seg - seg[:PRE].mean())
        # sanity: time-mean of the timeline equals the clip vector's projection direction
    E = np.array(ep); mean = E.mean(0); sem = E.std(0, ddof=1) / np.sqrt(len(E))
    t = np.arange(-PRE, POST + 1); pk = int(np.argmax(np.abs(mean[PRE:]))) + PRE
    out[lad] = {"n_epochs": len(E), "t": t.tolist(), "mean": mean.tolist(), "sem": sem.tolist(),
                "peak_t": int(t[pk]), "peak": float(mean[pk]), "late_mean_8_12": float(mean[PRE + 8:].mean()), "sustained_projection_by_level": sustained}
    print(f"{lad:3} epochs {len(E):2}  peak {mean[pk]:+.3f} at +{t[pk]} s  late(+8..+12) {mean[PRE+8:].mean():+.3f}  | sustained proj by level: " + " ".join(f"{c[3:]}:{v:+.2f}" for c, v in sustained.items()))
print("\nt(s):  " + " ".join(f"{x:+5d}" for x in range(-PRE, POST + 1)))
for lad in out: print(f"{lad:5}  " + " ".join(f"{v:+5.2f}" for v in out[lad]["mean"]))
(H / "cut_locked.json").write_text(json.dumps(out, indent=1))
