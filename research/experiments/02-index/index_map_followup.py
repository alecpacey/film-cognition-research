#!/usr/bin/env python3
"""
EXPLORATORY companion to index_map.py (20 Sep 2026). Which parts of the § 6.7 map are specific
to technique, under the label-shuffled null? (a) participation ratios under both definitions;
(b) run 00's face - landscape contrast against PC1 of Y with no dials involved; (c) the null
distribution of face_area's loading on axis 1 and of axis 1's agreement with run 00.
    .venv-analysis/bin/python index_map_followup.py   ->  index_map_followup.json
"""
import json, numpy as np
from pathlib import Path
from sklearn.linear_model import ElasticNet
from joblib import Parallel, delayed
H = Path(__file__).parent; SEED, N = 20260920, 200
pv = json.load(open(H / "parcel_vectors.json")); sel = json.load(open(H / "selection.json")); dt = json.load(open(H / "dial_table.json")); ar = json.load(open(H / "analysis_result.json"))
dials, clips = sel["dials"], sorted(sel["selected"]); films = np.array([dt[c]["film"] for c in clips]); parcels = sorted(pv[clips[0]])
def cw(M):
    M = M.astype(float).copy()
    for f in np.unique(films): M[films == f] -= M[films == f].mean(0)
    return M
X = cw(np.array([[float(dt[c][d]) for d in dials] for c in clips])); X = X / X.std(0, ddof=1)
Y = cw(np.array([[pv[c][p]["z"] for p in parcels] for c in clips]))
B = np.array([[ar["per_parcel"][p]["coef"][d] for d in dials] for p in parcels]); surv = np.array([ar["per_parcel"][p]["survives"] for p in parcels])
sv = lambda M: np.linalg.svd(M, compute_uv=False)
pr_s = lambda M: float(sv(M).sum() ** 2 / (sv(M) ** 2).sum()); pr_v = lambda M: float((sv(M) ** 2).sum() ** 2 / (sv(M) ** 4).sum())
p00 = json.load(open(H.parent / "00-probe" / "parcel_vectors.json"))
vec = lambda c: np.array([(p00[c][p]["z"] if isinstance(p00[c][p], dict) else p00[c][p]) for p in parcels]); con = vec("face") - vec("landscape")
_, Sy, Vty = np.linalg.svd(Y, full_matrices=False); U, S, Vt = np.linalg.svd(B, full_matrices=False); fi = dials.index("face_area_frac")
def one(seed):
    r = np.random.default_rng(seed); Yp = Y[r.permutation(len(Y))]
    Bp = np.array([ElasticNet(alpha=.1, l1_ratio=.5, max_iter=10000).fit(X, Yp[:, j]).coef_ for j in range(180)])
    Up, _, Vp = np.linalg.svd(Bp, full_matrices=False)
    return abs(Vp[0, fi]), int(np.argmax(np.abs(Vp[0]))), abs(np.corrcoef(con, Up[:, 0])[0, 1])
res = Parallel(n_jobs=-1)(delayed(one)(SEED + i) for i in range(N))
fl, lead, rc = (np.array([r[k] for r in res]) for k in range(3)); obs_f, obs_r = abs(Vt[0, fi]), abs(np.corrcoef(con, U[:, 0])[0, 1])
out = {"participation_ratio": {"on_singular_values_as_first_draft": {"B": pr_s(B), "survivors": pr_s(B[surv]), "Y": pr_s(Y)},
                               "on_variances_conventional": {"B": pr_v(B), "survivors": pr_v(B[surv]), "Y": pr_v(Y)}},
       "run00_contrast_vs_PC1_of_Y_abs_r": float(abs(np.corrcoef(con, Vty[0])[0, 1])),
       "face_loading_axis1": {"observed": float(obs_f), "null_mean": float(fl.mean()), "null_p95": float(np.percentile(fl, 95)),
                              "p": float((1 + (fl >= obs_f).sum()) / (N + 1)), "face_leads_frac_null": float((lead == fi).mean())},
       "axis1_vs_run00_contrast": {"observed": float(obs_r), "null_mean": float(rc.mean()), "null_p05": float(np.percentile(rc, 5)),
                                   "null_p95": float(np.percentile(rc, 95)), "p": float((1 + (rc >= obs_r).sum()) / (N + 1))}}
(H / "index_map_followup.json").write_text(json.dumps(out, indent=1)); print(json.dumps(out, indent=1))
