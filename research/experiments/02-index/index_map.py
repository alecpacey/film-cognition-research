#!/usr/bin/env python3
"""
EXPLORATORY — reproduces PAPER § 6.7 ("The index as a map") from committed data, and adds the
baseline the 16 Sep review asked for (M2). § 6.7 was written on 9–10 Sep with no script or output
file committed; this is that script. Registered verdict unchanged.

Object: B, the 180 x 14 matrix of full-data elastic-net coefficients in analysis_result.json.
Column k is the cortical pattern of dial k; col(B) is the set of profiles technique can reach.

  1  SVD of B: singular values, variance shares, participation ratio; survivors only
  2  axis loadings on dials and parcels
  3  axis 1 vs run 00's face - landscape contrast, with a parcel-permutation null
  4  variance of the observed 70 x 180 profiles retained by col(B), vs a random 14-dim subspace
     and the top-14 principal components; single-axis version
  5  NEW — label-permuted baseline: refit the same elastic net to row-permuted Y, and ask how
     concentrated B_perm is and how much of the true Y its column space retains. A random
     subspace is the wrong floor: any B fitted to Y has columns built from Y's own rows.

Every § 6.7 figure is compared with the paper's value; mismatches are listed at the end.
    .venv-analysis/bin/python index_map.py
"""
import json, hashlib
from pathlib import Path
import numpy as np
from sklearn.linear_model import ElasticNet
from joblib import Parallel, delayed

H = Path(__file__).parent
ALPHA, L1, N_PERM, N_RAND, SEED = 0.1, 0.5, 200, 200, 20260920
raw = (H / "parcel_vectors.json").read_bytes(); assert hashlib.sha256(raw).hexdigest().startswith("93807b80")
pv = json.loads(raw); sel = json.loads((H / "selection.json").read_text()); dt = json.loads((H / "dial_table.json").read_text())
ar = json.loads((H / "analysis_result.json").read_text())
dials, clips = sel["dials"], sorted(sel["selected"]); films = np.array([dt[c]["film"] for c in clips]); parcels = sorted(pv[clips[0]])

def cw(M):
    M = M.astype(float).copy()
    for f in np.unique(films): M[films == f] -= M[films == f].mean(axis=0)
    return M
X = cw(np.array([[float(dt[c][d]) for d in dials] for c in clips])); sd = X.std(0, ddof=1); sd[sd == 0] = 1; X = X / sd
Y = cw(np.array([[pv[c][p]["z"] for p in parcels] for c in clips]))
B = np.array([[ar["per_parcel"][p]["coef"][d] for d in dials] for p in parcels])          # 180 x 14
surv = np.array([ar["per_parcel"][p]["survives"] for p in parcels])

# sanity: B is what the registered model gives
Bfit = np.array([ElasticNet(alpha=ALPHA, l1_ratio=L1, max_iter=10000).fit(X, Y[:, j]).coef_ for j in range(180)])
assert np.abs(Bfit - B).max() < 1e-6, "B does not match a refit of the registered model"

out, checks = {}, []
def chk(name, got, paper, tol):
    ok = abs(got - paper) <= tol; checks.append((name, got, paper, ok)); return got

def spectrum(M):
    U, S, Vt = np.linalg.svd(M, full_matrices=False); v = S ** 2 / (S ** 2).sum()
    return U, S, Vt, v, float((S ** 2).sum() ** 2 / (S ** 4).sum())

# ---- 1
U, S, Vt, v, pr = spectrum(B)
out["singular_values"] = S.tolist(); out["variance_share"] = v.tolist(); out["participation_ratio"] = pr
for i, pv_ in enumerate([3.34, 1.52, 1.01]): chk(f"singular value {i+1}", S[i], pv_, 0.006)
chk("4th singular value (paper: nothing above 0.74)", S[3], 0.74, 0.006)
for i, pv_ in enumerate([69.4, 14.3, 6.4]): chk(f"axis {i+1} share %", 100 * v[i], pv_, 0.06)
chk("3 components %", 100 * v[:3].sum(), 90.1, 0.06); chk("5 components %", 100 * v[:5].sum(), 95.9, 0.06)
chk("participation ratio of B", pr, 5.56, 0.006)
Us, Ss, Vts, vs, prs = spectrum(B[surv])
out["survivors"] = {"n": int(surv.sum()), "singular_values": Ss.tolist(), "participation_ratio": prs, "three_components": float(vs[:3].sum())}
chk("survivors: '4.76' read as participation ratio", prs, 4.76, 0.006); chk("survivors: 3 components %", 100 * vs[:3].sum(), 92.7, 0.06)
print(f"1  S = {np.round(S[:5],3)}  shares % = {np.round(100*v[:5],1)}  PR = {pr:.2f}   survivors: S1 = {Ss[0]:.2f}, PR = {prs:.2f}, 3 comps = {100*vs[:3].sum():.1f}%")

# ---- 2  (singular-vector sign is arbitrary; orient to the paper's convention)
orient = [("face_area_frac", +1), ("camera_pan", -1), ("mean_saturation", +1)]
axes = {}
paper_d = [{"face_area_frac": .80, "mean_saturation": -.43, "camera_zoom": -.27}, {"camera_pan": -.65, "median_luma": .51, "cuts_per_min": .35},
           {"mean_saturation": .58, "face_area_frac": .46, "camera_zoom": .32}]
paper_p = [{"STSdp": .35, "A5": .30, "VMV2": -.25, "PHA2": -.22}, {"V4t": .30, "MST": .30, "MT": .29, "FST": .28}, {"PCV": -.31, "PIT": .24, "A5": -.23, "V8": .23}]
for k in range(3):
    sgn = np.sign(Vt[k, dials.index(orient[k][0])]) * orient[k][1]
    dl, pl = sgn * Vt[k], sgn * U[:, k]
    axes[k + 1] = {"dials": dict(zip(dials, dl.tolist())), "top_parcels": sorted(zip(parcels, pl.tolist()), key=lambda t: -abs(t[1]))[:6]}
    for d, val in paper_d[k].items(): chk(f"axis {k+1} dial {d}", dl[dials.index(d)], val, 0.006)
    for p, val in paper_p[k].items(): chk(f"axis {k+1} parcel {p}", pl[parcels.index(p)], val, 0.006)
    print(f"2  axis {k+1}: dials " + ", ".join(f"{d} {x:+.2f}" for d, x in sorted(zip(dials, dl), key=lambda t: -abs(t[1]))[:3]) +
          "  |  parcels " + ", ".join(f"{p} {x:+.2f}" for p, x in axes[k + 1]["top_parcels"][:4]))
out["axes"] = axes
ax1 = np.sign(Vt[0, dials.index("face_area_frac")]) * U[:, 0]

# ---- 3
p00 = json.loads((H.parent / "00-probe" / "parcel_vectors.json").read_text())
vec = lambda c: np.array([(p00[c][p]["z"] if isinstance(p00[c][p], dict) else p00[c][p]) for p in parcels])
r00 = {c: float(np.corrcoef(vec(c), ax1)[0, 1]) for c in ("face", "landscape", "crowd")}
rc = float(np.corrcoef(vec("face") - vec("landscape"), ax1)[0, 1])
rng = np.random.default_rng(SEED); con = vec("face") - vec("landscape")
null = np.array([abs(np.corrcoef(rng.permutation(con), ax1)[0, 1]) for _ in range(10000)])
out["run00"] = {"contrast_r": rc, **r00, "perm95_abs": float(np.percentile(null, 95))}
chk("run-00 contrast r", rc, .936, .0006); chk("face alone", r00["face"], .704, .0006); chk("landscape alone", r00["landscape"], -.684, .0006)
chk("crowd alone", r00["crowd"], -.135, .0006); chk("parcel-permutation 95th pct", out["run00"]["perm95_abs"], .144, .006)
print(f"3  axis 1 vs run-00 contrast r = {rc:+.3f}  (face {r00['face']:+.3f}, landscape {r00['landscape']:+.3f}, crowd {r00['crowd']:+.3f}; null95 {out['run00']['perm95_abs']:.3f})")

# ---- 4
def retained(Q):                                   # Q: 180 x k orthonormal
    return float(((Y @ Q) ** 2).sum() / (Y ** 2).sum())
def colspace(M):
    Uq, Sq, _ = np.linalg.svd(M, full_matrices=False); return Uq[:, Sq > 1e-10 * Sq[0]]
QB = colspace(B); tech = retained(QB)
rnd = np.array([retained(np.linalg.qr(rng.standard_normal((180, QB.shape[1])))[0]) for _ in range(N_RAND)])
_, Sy, Vty = np.linalg.svd(Y, full_matrices=False); vy = Sy ** 2 / (Sy ** 2).sum()
ceil14, best1, one = float(vy[:QB.shape[1]].sum()), float(vy[0]), retained(ax1[:, None])
pry = float((Sy ** 2).sum() ** 2 / (Sy ** 4).sum())
out["retained"] = {"technique": tech, "dim": int(QB.shape[1]), "random_mean": float(rnd.mean()), "random_sd": float(rnd.std(ddof=1)), "random_max": float(rnd.max()),
                   "ceiling_top_pcs": ceil14, "ratio_to_ceiling": tech / ceil14, "axis1": one, "pc1": best1, "participation_ratio_Y": pry,
                   "axis1_vs_pc1_abs_r": float(abs(np.corrcoef(ax1, Vty[0])[0, 1]))}
chk("technique retained %", 100 * tech, 90.8, .06); chk("random subspace mean % (seed-dependent)", 100 * rnd.mean(), 7.9, .5)
chk("top-14 PCs %", 100 * ceil14, 99.4, .06); chk("ratio to ceiling %", 100 * tech / ceil14, 91.3, .06)
chk("axis 1 retained %", 100 * one, 57.7, .06); chk("PC1 %", 100 * best1, 61.8, .06); chk("participation ratio of Y", pry, 8.35, .006)
print(f"4  retained by col(B) [{QB.shape[1]}-dim]: {100*tech:.1f}%   random {100*rnd.mean():.1f}% (sd {100*rnd.std(ddof=1):.1f}, max {100*rnd.max():.1f})   "
      f"top PCs {100*ceil14:.1f}%   axis1 {100*one:.1f}% vs PC1 {100*best1:.1f}%  |r(axis1, PC1)| {out['retained']['axis1_vs_pc1_abs_r']:.3f}   PR(Y) {pry:.2f}")

# ---- 5  label-permuted baseline
def one_perm(seed):
    r = np.random.default_rng(seed); Yp = Y[r.permutation(len(Y))]
    Bp = np.array([ElasticNet(alpha=ALPHA, l1_ratio=L1, max_iter=10000).fit(X, Yp[:, j]).coef_ for j in range(180)])
    if not np.any(Bp): return None
    Up, Sp, _ = np.linalg.svd(Bp, full_matrices=False); vp = Sp ** 2 / (Sp ** 2).sum(); Q = Up[:, Sp > 1e-10 * Sp[0]]
    return {"frob": float(np.sqrt((Bp ** 2).sum())), "dim": int(Q.shape[1]), "share1": float(vp[0]), "share3": float(vp[:3].sum()),
            "pr": float((Sp ** 2).sum() ** 2 / (Sp ** 4).sum()), "retained": retained(Q), "axis1_retained": retained(Up[:, :1]),
            "axis1_vs_pc1": float(abs(np.corrcoef(Up[:, 0], Vty[0])[0, 1]))}
perm = [p for p in Parallel(n_jobs=-1)(delayed(one_perm)(SEED + i) for i in range(N_PERM)) if p]
def q(key): a = np.array([p[key] for p in perm]); return {"mean": float(a.mean()), "p05": float(np.percentile(a, 5)), "p95": float(np.percentile(a, 95)), "max": float(a.max()), "min": float(a.min())}
obs = {"frob": float(np.sqrt((B ** 2).sum())), "dim": int(QB.shape[1]), "share1": float(v[0]), "share3": float(v[:3].sum()), "pr": pr, "retained": tech,
       "axis1_retained": one, "axis1_vs_pc1": out["retained"]["axis1_vs_pc1_abs_r"]}
out["permuted_label_baseline"] = {"n": len(perm), "observed": obs, "null": {k: q(k) for k in obs},
                                  "p_ge": {k: float((1 + sum(p[k] >= obs[k] for p in perm)) / (1 + len(perm))) for k in ("frob", "share1", "share3", "retained", "axis1_retained", "axis1_vs_pc1")},
                                  "p_le_pr": float((1 + sum(p["pr"] <= obs["pr"] for p in perm)) / (1 + len(perm)))}
print(f"\n5  label-permuted baseline, {len(perm)} refits of the same elastic net")
print(f"   {'quantity':34}{'observed':>10}{'null mean':>11}{'null 5–95%':>17}{'null max':>10}{'p':>8}")
lab = {"frob": "‖B‖ (total coefficient mass)", "dim": "rank of col(B)", "share1": "axis-1 share of B", "share3": "3-axis share of B", "pr": "participation ratio of B",
       "retained": "Y variance retained by col(B)", "axis1_retained": "Y variance retained by axis 1", "axis1_vs_pc1": "|r(axis 1, PC1 of Y)|"}
for k in obs:
    n = out["permuted_label_baseline"]["null"][k]; pp = out["permuted_label_baseline"]["p_le_pr"] if k == "pr" else out["permuted_label_baseline"]["p_ge"].get(k, float("nan"))
    print(f"   {lab[k]:34}{obs[k]:10.3f}{n['mean']:11.3f}{n['p05']:9.3f}–{n['p95']:<7.3f}{n['max']:10.3f}{pp:8.3f}")

bad = [c for c in checks if not c[3]]
out["paper_checks"] = [{"figure": n, "reproduced": float(g), "paper": float(p), "match": bool(ok)} for n, g, p, ok in checks]
print(f"\n§ 6.7 figures reproduced: {len(checks)-len(bad)}/{len(checks)}")
for n, g, p, ok in bad: print(f"   MISMATCH  {n}: reproduced {g:+.4f}  paper {p:+.4f}")
(H / "index_map.json").write_text(json.dumps(out, indent=1)); print("wrote index_map.json")
