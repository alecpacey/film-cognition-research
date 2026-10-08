#!/usr/bin/env python3
"""
EXPLORATORY (8 Oct 2026; consolidation 4b, review M3). The SESOI of §3.2 was derived for a
*marginal* dial->parcel correlation; §5.3.5 compared it with each parcel's cross-validated
14-dial elastic-net r, a different quantity. This computes the quantity the SESOI applies to,
on the frozen stage-02 data with the registered preprocessing (dials and parcels centred within
film, parcels' z field):
  - marginal r of each dial with each parcel (pooled after within-film centring), and
  - semi-partial r: each dial's unique share given the other 13 (dial residualised on the rest).
Counts against |r| >= 0.5 by point estimate and by the lower bound of a Fisher 95% interval
(n_eff = 70 - 3 for the three film means removed).
    .venv-analysis/bin/python sesoi_marginal.py  ->  sesoi_marginal.json
"""
import json
from pathlib import Path
import numpy as np

H = Path(__file__).parent
pv = json.load(open(H / "parcel_vectors.json")); sel = json.load(open(H / "selection.json"))
dt = json.load(open(H / "dial_table.json")); res = json.load(open(H / "analysis_result.json"))
dials, clips = sel["dials"], sorted(sel["selected"])
films = np.array([dt[c]["film"] for c in clips]); parcels = sorted(pv[clips[0]])
SESOI, N_EFF = 0.5, len(clips) - len(set(films))


def centre_within(M):
    M = np.array(M, float).copy()
    for f in set(films): M[films == f] -= M[films == f].mean(0)
    return M


X = centre_within([[float(dt[c][d]) for d in dials] for c in clips])
Y = centre_within([[pv[c][p]["z"] for p in parcels] for c in clips])
Xs, Ys = X / X.std(0), Y / Y.std(0)
R = Xs.T @ Ys / len(clips)                                         # 14 x 180 marginal r

SR = np.empty_like(R)                                              # semi-partial r
for k in range(len(dials)):
    others = np.delete(X, k, axis=1); A = np.column_stack([np.ones(len(clips)), others])
    e = X[:, k] - A @ np.linalg.lstsq(A, X[:, k], rcond=None)[0]
    SR[k] = (e / np.linalg.norm(e)) @ (Y - Y.mean(0)) / np.linalg.norm(Y - Y.mean(0), axis=0)

z_half = 1.96 / np.sqrt(N_EFF - 3)
def ci_low_abs(r):                                                 # lower bound of |r|'s Fisher 95% interval
    z = np.arctanh(np.abs(r)); return np.tanh(np.maximum(z - z_half, 0))

surv = np.array([res["per_parcel"][p]["survives"] for p in parcels])
out = {"n": len(clips), "n_eff_for_ci": N_EFF, "sesoi": SESOI, "n_pairs": int(R.size)}
for name, M in (("marginal", R), ("semipartial", SR)):
    hit, firm = np.abs(M) >= SESOI, ci_low_abs(M) >= SESOI
    o = {"pairs_at_or_above_sesoi": int(hit.sum()), "pairs_ci_lower_above_sesoi": int(firm.sum()),
         "parcels_with_any_dial_at_sesoi": int(hit.any(0).sum()),
         "survivors_with_any_dial_at_sesoi": int((hit.any(0) & surv).sum()),
         "max_abs_r": float(np.abs(M).max()), "median_abs_r": float(np.median(np.abs(M))),
         "per_dial": {}}
    for k, d in enumerate(dials):
        j = int(np.argmax(np.abs(M[k])))
        o["per_dial"][d] = {"parcels_at_sesoi": int(hit[k].sum()), "max_abs_r": float(abs(M[k, j])),
                            "max_parcel": parcels[j], "max_signed_r": float(M[k, j])}
    out[name] = o
    print(f"\n{name}: {o['pairs_at_or_above_sesoi']} of {R.size} dial-parcel pairs at |r| >= {SESOI} "
          f"({o['pairs_ci_lower_above_sesoi']} with the 95% CI lower bound above it); "
          f"parcels with any dial there: {o['parcels_with_any_dial_at_sesoi']} of 180 "
          f"({o['survivors_with_any_dial_at_sesoi']} of the 101 survivors); max |r| {o['max_abs_r']:.2f}, median {o['median_abs_r']:.3f}")
    for d, v in sorted(o["per_dial"].items(), key=lambda kv: -kv[1]["max_abs_r"]):
        print(f"   {d:16} parcels at SESOI {v['parcels_at_sesoi']:3}   max {v['max_signed_r']:+.2f} ({v['max_parcel']})")
(H / "sesoi_marginal.json").write_text(json.dumps(out, indent=1)); print("\nwrote sesoi_marginal.json")
