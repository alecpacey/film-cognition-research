#!/usr/bin/env python3
"""Freeze the reference quantities for 03b from COMMITTED stage-03 data, before any 03b clip exists.
Reference = stage 03 S- arm (hard cuts, face<->landscape, continuous ambient audio).
    ../02-index/.venv-analysis/bin/python make_reference.py  ->  reference_mode.json"""
import json, hashlib, itertools, numpy as np
from pathlib import Path
H = Path(__file__).parent; src = H.parent / "03-isolation" / "parcel_vectors.json"; raw = src.read_bytes(); pv = json.loads(raw)
parcels = sorted(next(iter(pv.values()))); LV = ["cut01", "cut03", "cut07", "cut15", "cut31"]; x = np.log([1, 3, 7, 15, 31])
CLUSTER, AUD = ["IFJa", "IFJp", "IFSp", "8C"], ["A4", "A1", "MBelt"]
Z = lambda pre: np.array([[pv[f"{pre}{c}"][p]["z"] for p in parcels] for c in LV])
def slope(Zm, xx): xc = xx - xx.mean(); return (xc @ (Zm - Zm.mean(0))) / (xc @ xc)
def stats(Zm, m):
    ci, ai = [parcels.index(p) for p in CLUSTER], [parcels.index(p) for p in AUD]
    f = lambda xx: (lambda b: (b[ci].mean(), b[ai].mean(), (b @ m) / (m @ m)))(slope(Zm, xx))
    obs = f(x); null = np.array([f(x[list(p)]) for p in itertools.permutations(range(5))])
    return {"cluster_slope": float(obs[0]), "p_cluster_pos": float((null[:, 0] >= obs[0] - 1e-12).mean()),
            "auditory_slope": float(obs[1]), "p_auditory_neg": float((null[:, 1] <= obs[1] + 1e-12).mean()),
            "gain": float(obs[2]), "p_gain": float((null[:, 2] >= obs[2] - 1e-12).mean())}
m = slope(Z("Sminus_"), x)
out = {"source": "03-isolation/parcel_vectors.json", "source_sha256": hashlib.sha256(raw).hexdigest(), "levels": [1, 3, 7, 15, 31], "x": "natural log of constructed cut count",
       "parcels": parcels, "reference_slopes_Sminus": m.tolist(), "cluster": CLUSTER, "auditory": AUD,
       "calibration": {"stage03_Sminus_on_itself": stats(Z("Sminus_"), m), "stage03_Splus_on_Sminus": stats(Z("Splus_"), m)}}
(H / "reference_mode.json").write_text(json.dumps(out, indent=1))
for k, v in out["calibration"].items(): print(k, {a: round(b, 3) for a, b in v.items()})
