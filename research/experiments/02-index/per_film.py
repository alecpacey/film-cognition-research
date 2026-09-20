#!/usr/bin/env python3
"""
EXPLORATORY (20 Sep 2026; review M7). Per-film relation of named parcels to the cut-rate and
face-area dials. Within-film centring removes film means, not film slopes; this shows the slopes.
Marginal Pearson r within each film, and the same elastic net (alpha 0.1, l1 0.5) fitted per film.
    .venv-analysis/bin/python per_film.py  ->  per_film.json
"""
import json, numpy as np
from pathlib import Path
from scipy import stats
from sklearn.linear_model import ElasticNet
H = Path(__file__).parent
pv = json.load(open(H / "parcel_vectors.json")); sel = json.load(open(H / "selection.json")); dt = json.load(open(H / "dial_table.json"))
dials, clips = sel["dials"], sorted(sel["selected"]); films = np.array([dt[c]["film"] for c in clips]); parcels = sorted(pv[clips[0]])
NAMED = ["IFJa", "IFJp", "IFSp", "8C", "A4", "A1", "MBelt", "A5", "STSdp", "STSvp", "VMV2", "PHA2", "MT"]
Xr = np.array([[float(dt[c][d]) for d in dials] for c in clips]); Yr = np.array([[pv[c][p]["z"] for p in parcels] for c in clips])
out = {}
for dial in ("cuts_per_min", "face_area_frac"):
    k = dials.index(dial); out[dial] = {}
    print(f"\n{dial}: within-film marginal r  (elastic-net coef per film in brackets)")
    print(f"{'parcel':7}" + "".join(f"{f[:14]:>26}" for f in np.unique(films)) + f"{'pooled r':>12}")
    for p in NAMED:
        j = parcels.index(p); row = {}; line = f"{p:7}"
        for f in np.unique(films):
            m = films == f; X = Xr[m] - Xr[m].mean(0); sd = X.std(0, ddof=1); sd[sd == 0] = 1; X = X / sd; y = Yr[m, j] - Yr[m, j].mean()
            r, pp = stats.pearsonr(X[:, k], y); c = float(ElasticNet(alpha=.1, l1_ratio=.5, max_iter=10000).fit(X, y).coef_[k])
            row[f] = {"n": int(m.sum()), "r": float(r), "p": float(pp), "en_coef": c}; line += f"{r:+14.2f} (p {pp:.2f}) [{c:+.2f}]"
        Xc, yc = Xr[:, k].copy(), Yr[:, j].copy()
        for f in np.unique(films): Xc[films == f] -= Xc[films == f].mean(); yc[films == f] -= yc[films == f].mean()
        rp = float(stats.pearsonr(Xc, yc)[0]); signs = {np.sign(row[f]["r"]) for f in row if abs(row[f]["r"]) >= 0.2}
        row["pooled_r"] = rp; row["sign_conflict_at_abs_r_ge_0.2"] = len(signs) > 1; out[dial][p] = row
        print(line + f"{rp:+12.2f}" + ("   <- sign conflict" if row["sign_conflict_at_abs_r_ge_0.2"] else ""))
(H / "per_film.json").write_text(json.dumps(out, indent=1)); print("\nwrote per_film.json")
