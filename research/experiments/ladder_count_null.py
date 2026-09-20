#!/usr/bin/env python3
"""
EXPLORATORY (20 Sep 2026; review M1). The correct null for the "parcels at |r| > 0.9" count in
the 5-level ladders of stages 01 and 03. The stage READMEs took chance as ~7 of 180 (p ~ 0.037
per parcel, parcels independent). Parcels are not independent: across the ladder the cortex
moves along roughly one direction, so the count is close to a single event. The right null
permutes the five level labels (120 orderings). Pre-fixed verdicts are unchanged.
    02-index/.venv-analysis/bin/python ladder_count_null.py  ->  ladder_count_null.json
"""
import json, itertools, numpy as np
from pathlib import Path
H = Path(__file__).parent
pv01 = json.load(open(H / "01-cutrate" / "parcel_vectors.json")); pv03 = json.load(open(H / "03-isolation" / "parcel_vectors.json"))
parcels = sorted(next(iter(pv03.values()))); levels = ["cut01", "cut03", "cut07", "cut15", "cut31"]; x = np.log([1, 3, 7, 15, 31])
g = lambda pvx, c, p: pvx[c][p]["z"] if isinstance(pvx[c][p], dict) else pvx[c][p]
Z = lambda pvx, pre: np.array([[g(pvx, f"{pre}{c}", p) for p in parcels] for c in levels])
def count(Zm, xx):
    xc, zc = xx - xx.mean(), Zm - Zm.mean(0)
    return int((np.abs((xc @ zc) / np.sqrt((xc @ xc) * (zc * zc).sum(0))) > 0.9).sum())
out = {}
for name, Zm in [("stage01", Z(pv01, "")), ("stage03_Splus", Z(pv03, "Splus_")), ("stage03_Sminus", Z(pv03, "Sminus_"))]:
    obs = count(Zm, x); null = np.array([count(Zm, x[list(p)]) for p in itertools.permutations(range(5))])
    ev = np.linalg.eigvalsh(np.cov((Zm - Zm.mean(0)).T)); ev = ev[ev > 1e-9]
    out[name] = {"observed": obs, "null_median": float(np.median(null)), "null_p95": float(np.percentile(null, 95)), "null_max": int(null.max()),
                 "n_orderings_ge_observed": int((null >= obs).sum()), "p": float((null >= obs).mean()),
                 "frac_orderings_clearing_bar_15": float((null >= 15).mean()), "participation_ratio_across_levels_max4": float(ev.sum() ** 2 / (ev ** 2).sum())}
    o = out[name]; print(f"{name:15} observed {obs:3} | null median {o['null_median']:.0f}, 95th {o['null_p95']:.0f}, max {o['null_max']} | p = {o['n_orderings_ge_observed']}/120 = {o['p']:.3f} | orderings clearing the >=15 bar: {100*o['frac_orderings_clearing_bar_15']:.0f}% | PR {o['participation_ratio_across_levels_max4']:.2f}")
out["note"] = "identity and reversed orderings give identical |r|, so the p-floor of a 5-level design is 2/120 = 0.017"
(H / "ladder_count_null.json").write_text(json.dumps(out, indent=1))
