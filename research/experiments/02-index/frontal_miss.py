#!/usr/bin/env python3
"""
EXPLORATORY — NOT THE REGISTERED TEST. Written 15 Sep 2026 after stage 03.

Why did the stage-02 index (osf.io/dg7fe, PARTIAL) miss the frontal half of the cut
effect that stage 03 shows to be causal in both speech arms (IFJa/IFSp/8C up, A4/A1/MBelt
down)? The index recovered the auditory half (negative cut-rate weights in A4/A1/MBelt/A5)
and nothing frontal. This script asks, on the frozen stage-02 data:

  A  what the registered fits say for the frontal cluster and the auditory quartet
  B  how much cut-rate variance each film contributes after within-film centring
  C  marginal (within-film) correlation of each parcel with cut rate, overall and per film
  D  whether the elastic-net penalty zeroed a real cut-rate weight: OLS and ridge refits,
     and the elastic-net coefficient along a shrinking alpha path (labelled exploratory)
  E  whether the auditory parcels carry the frontal parcels' variance
  F  whole-map comparison: stage-02 observational cut-rate map vs the causal maps of
     stage 01 (live action) and stage 03 (generated, S+ and S−) across 180 parcels

Nothing here changes the registered verdict. Output: frontal_miss.json; note: frontal_miss.md.
    .venv-analysis/bin/python frontal_miss.py
"""
import json, hashlib
from pathlib import Path
import numpy as np
from scipy import stats
from sklearn.linear_model import ElasticNet, Ridge, LinearRegression

H = Path(__file__).parent
FROZEN_SHA = "93807b80a8ec33a42b853a285cd629e663cdb429658ff115a20885cb053a3189"
CLUSTER = ["IFJa", "IFJp", "IFSp", "8C"]
AUD = ["A4", "A1", "MBelt", "A5"]
FOCUS = CLUSTER + AUD


def centre_within(M, films):
    M = M.astype(float).copy()
    for f in np.unique(films):
        m = films == f
        M[m] -= M[m].mean(axis=0)
    return M


def r_p(x, y):
    r, p = stats.pearsonr(x, y)
    return float(r), float(p)


raw = (H / "parcel_vectors.json").read_bytes()
assert hashlib.sha256(raw).hexdigest() == FROZEN_SHA
pv = json.loads(raw)
sel = json.loads((H / "selection.json").read_text())
dt = json.loads((H / "dial_table.json").read_text())
ar = json.loads((H / "analysis_result.json").read_text())
dials, clips = sel["dials"], sorted(sel["selected"])
films = np.array([dt[c]["film"] for c in clips])
parcels = sorted(pv[clips[0]])
assert len(parcels) == 180
i_cut = dials.index("cuts_per_min")

Xraw = np.array([[float(dt[c][d]) for d in dials] for c in clips])
Xc = centre_within(Xraw, films)
sd = Xc.std(axis=0, ddof=1); sd[sd == 0] = 1.0
X = Xc / sd                                          # exactly the registered design matrix
Y = centre_within(np.array([[pv[c][p]["z"] for p in parcels] for c in clips]), films)
cut_raw = Xraw[:, i_cut]
cut_c = Xc[:, i_cut]
logcut_c = centre_within(np.log1p(cut_raw)[:, None], films)[:, 0]
out = {"note": "EXPLORATORY, not the registered test; verdict unchanged", "n": len(clips)}

# ---------------- A: registered fits ----------------
out["A_registered"] = {p: {"cv_r": ar["per_parcel"][p]["r_obs"], "null95": ar["per_parcel"][p]["p95_null"],
                           "p_perm": ar["per_parcel"][p]["p_perm"], "q": ar["per_parcel"][p]["q"],
                           "survives": ar["per_parcel"][p]["survives"],
                           "coef_nonzero": {d: round(v, 3) for d, v in ar["per_parcel"][p]["coef"].items() if v != 0}}
                       for p in FOCUS}
print("A  registered elastic-net fits")
for p, v in out["A_registered"].items():
    print(f"   {p:6} cv r {v['cv_r']:+.3f}  null95 {v['null95']:+.3f}  q {v['q']:.3f}  {'SURV' if v['survives'] else '  - '}  "
          f"cuts {ar['per_parcel'][p]['coef']['cuts_per_min']:+.3f}  shotlen {ar['per_parcel'][p]['coef']['mean_shot_len_s']:+.3f}")

# ---------------- B: cut-rate spread per film ----------------
B = {}
for f in np.unique(films):
    m = films == f; x = cut_raw[m]
    B[f] = {"n": int(m.sum()), "mean": float(x.mean()), "sd": float(x.std(ddof=1)), "min": float(x.min()),
            "max": float(x.max()), "range_ratio_max_over_min": float(x.max() / max(x.min(), 1.0))}
B["all"] = {"n": len(clips), "mean": float(cut_raw.mean()), "sd": float(cut_raw.std(ddof=1)),
            "within_film_sd": float(cut_c.std(ddof=1)),
            "within_share_of_variance": float(cut_c.var(ddof=1) / cut_raw.var(ddof=1)),
            "s_ratio": float(cut_c.std(ddof=1) / cut_raw.std(ddof=1))}
out["B_cut_spread"] = B
print("\nB  cuts_per_min by film (selected 70)")
for f, v in B.items():
    if f == "all": print(f"   ALL  n={v['n']} sd {v['sd']:.2f}  within-film sd {v['within_film_sd']:.2f}  within share {v['within_share_of_variance']:.3f}  s={v['s_ratio']:.2f}")
    else: print(f"   {f:15} n={v['n']:2} mean {v['mean']:5.2f} sd {v['sd']:4.2f}  range {v['min']:.0f}–{v['max']:.0f}")

# ---------------- C: marginal within-film correlations ----------------
C = {}
print("\nC  marginal within-film r with cuts_per_min (and log cuts); per film")
for p in FOCUS:
    y = Y[:, parcels.index(p)]
    r_lin, p_lin = r_p(cut_c, y); r_log, p_log = r_p(logcut_c, y)
    per = {}
    for f in np.unique(films):
        m = films == f
        per[f] = r_p(cut_c[m], y[m])[0]
    C[p] = {"r_cuts": r_lin, "p_cuts": p_lin, "r_logcuts": r_log, "p_logcuts": p_log, "per_film_r_cuts": per,
            "sd_z_within": float(y.std(ddof=1))}
    print(f"   {p:6} r {r_lin:+.3f} (p {p_lin:.3f})  log r {r_log:+.3f}  per film " +
          " ".join(f"{k[:6]} {v:+.2f}" for k, v in per.items()) + f"   sd(z) {y.std(ddof=1):.3f}")
out["C_marginal"] = C

# ---------------- D: did the penalty zero a real cut weight? ----------------
D = {}
print("\nD  refits on the registered design matrix (14 standardised dials): OLS / ridge / EN alpha path")
alphas = [0.1, 0.03, 0.01, 0.003, 0.001]
for p in FOCUS:
    j = parcels.index(p); y = Y[:, j]
    ols = LinearRegression().fit(X, y)
    resid = y - ols.predict(X); dof = len(y) - X.shape[1] - 1
    s2 = resid @ resid / dof
    cov = s2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov)); t = ols.coef_ / se
    pvals = 2 * stats.t.sf(np.abs(t), dof)
    r2 = float(ols.score(X, y))
    ridge = Ridge(alpha=1.0).fit(X, y)
    path = {a: float(ElasticNet(alpha=a, l1_ratio=0.5, max_iter=50000).fit(X, y).coef_[i_cut]) for a in alphas}
    # univariate OLS on cuts alone
    uni = LinearRegression().fit(X[:, [i_cut]], y)
    D[p] = {"ols_coef_cuts": float(ols.coef_[i_cut]), "ols_t_cuts": float(t[i_cut]), "ols_p_cuts": float(pvals[i_cut]),
            "ols_coef_shotlen": float(ols.coef_[dials.index("mean_shot_len_s")]),
            "ols_r2_full": r2, "ols_largest_abs": sorted(((d, float(c), float(pp)) for d, c, pp in zip(dials, ols.coef_, pvals)),
                                                         key=lambda x: -abs(x[1]))[:3],
            "ridge1_coef_cuts": float(ridge.coef_[i_cut]), "en_coef_cuts_by_alpha": path,
            "univariate_ols_slope_cuts": float(uni.coef_[0])}
    print(f"   {p:6} OLS cuts {ols.coef_[i_cut]:+.3f} (t {t[i_cut]:+.2f}, p {pvals[i_cut]:.3f})  ridge {ridge.coef_[i_cut]:+.3f}  "
          f"EN a=.1 {path[0.1]:+.3f} .01 {path[0.01]:+.3f} .001 {path[0.001]:+.3f}   R² {r2:.2f}  "
          f"top OLS: " + ", ".join(f"{d} {c:+.2f}" for d, c, _ in D[p]["ols_largest_abs"]))
out["D_refits"] = D

# ---------------- E: does the auditory signature carry the frontal variance? ----------------
E = {}
print("\nE  frontal ~ auditory across the 70 segments (within-film centred z)")
Ya = np.column_stack([Y[:, parcels.index(a)] for a in AUD])
for p in CLUSTER:
    y = Y[:, parcels.index(p)]
    rr = {a: r_p(Y[:, parcels.index(a)], y)[0] for a in AUD}
    reg = LinearRegression().fit(Ya, y); r2 = float(reg.score(Ya, y))
    # partial r of frontal with cuts controlling A4
    a4 = Y[:, parcels.index("A4")]
    ry = y - LinearRegression().fit(a4[:, None], y).predict(a4[:, None])
    rc = cut_c - LinearRegression().fit(a4[:, None], cut_c).predict(a4[:, None])
    partial = r_p(rc, ry)[0]
    E[p] = {"r_with_auditory": rr, "r2_on_auditory_quartet": r2, "partial_r_cuts_given_A4": partial}
    print(f"   {p:6} r(A4) {rr['A4']:+.2f} r(A1) {rr['A1']:+.2f} r(MBelt) {rr['MBelt']:+.2f} r(A5) {rr['A5']:+.2f}  "
          f"R² on quartet {r2:.2f}  partial r(cuts | A4) {partial:+.3f}")
# and in stage 03: frontal vs auditory anti-correlation across the ladder
out["E_frontal_vs_auditory"] = E

# ---------------- F: whole-map comparison ----------------
def ladder_r(pvx, prefix):
    cuts = {"cut01": 1, "cut03": 3, "cut07": 7, "cut15": 15, "cut31": 31}
    x = np.log([cuts[c] for c in cuts])
    lv = [f"{prefix}{c}" for c in cuts]
    g = lambda c, p: pvx[c][p]["z"] if isinstance(pvx[c][p], dict) else pvx[c][p]
    return np.array([np.corrcoef(x, [g(c, p) for c in lv])[0, 1] for p in parcels])

pv01 = json.loads((H.parent / "01-cutrate" / "parcel_vectors.json").read_text())
pv03 = json.loads((H.parent / "03-isolation" / "parcel_vectors.json").read_text())
assert set(parcels) <= set(next(iter(pv01.values()))) and set(parcels) <= set(next(iter(pv03.values())))
m01 = ladder_r(pv01, ""); m03p = ladder_r(pv03, "Splus_"); m03m = ladder_r(pv03, "Sminus_")
m02_marg = np.array([r_p(cut_c, Y[:, j])[0] for j in range(180)])
m02_marg_log = np.array([r_p(logcut_c, Y[:, j])[0] for j in range(180)])
m02_en = np.array([ar["per_parcel"][p]["coef"]["cuts_per_min"] for p in parcels])
m02_ols = np.array([LinearRegression().fit(X, Y[:, j]).coef_[i_cut] for j in range(180)])
maps = {"stage01_r": m01, "stage03_Splus_r": m03p, "stage03_Sminus_r": m03m,
        "stage02_marginal_r": m02_marg, "stage02_marginal_r_log": m02_marg_log,
        "stage02_EN_coef": m02_en, "stage02_OLS_coef": m02_ols}
names = list(maps)
corr = {a: {b: float(np.corrcoef(maps[a], maps[b])[0, 1]) for b in names} for a in names}
print("\nF  whole-map correlations across 180 parcels")
print("   " + " " * 22 + "".join(f"{n[:14]:>15}" for n in names))
for a in names:
    print(f"   {a:22}" + "".join(f"{corr[a][b]:+15.2f}" for b in names))

# which parcels stage 03 moves in both arms, and how stage 02 sees them
both = [(parcels[j], m03p[j], m03m[j], m02_marg[j], m02_en[j]) for j in range(180)
        if abs(m03p[j]) > 0.9 and abs(m03m[j]) > 0.9 and np.sign(m03p[j]) == np.sign(m03m[j])]
pos = [b for b in both if b[1] > 0]; neg = [b for b in both if b[1] < 0]
def summ(lst):
    if not lst: return {}
    m2 = np.array([b[3] for b in lst]); en = np.array([b[4] for b in lst]); s3 = np.sign(lst[0][1])
    return {"n": len(lst), "stage02_marginal_r_mean": float(m2.mean()), "stage02_marginal_r_median": float(np.median(m2)),
            "sign_concordant_frac": float((np.sign(m2) == s3).mean()),
            "n_EN_nonzero": int((en != 0).sum()), "n_EN_concordant": int(((en != 0) & (np.sign(en) == s3)).sum()),
            "parcels": [b[0] for b in lst]}
F_sets = {"stage03_up_both_arms": summ(pos), "stage03_down_both_arms": summ(neg)}
print(f"\n   stage 03 parcels moving the same way in both arms at |r|>0.9: {len(pos)} up, {len(neg)} down")
for k, v in F_sets.items():
    if v: print(f"   {k:24} n={v['n']:2}  stage02 marginal r mean {v['stage02_marginal_r_mean']:+.3f} median {v['stage02_marginal_r_median']:+.3f}  "
                f"sign-concordant {v['sign_concordant_frac']:.2f}  EN nonzero {v['n_EN_nonzero']} (concordant {v['n_EN_concordant']})")
# frontal vs auditory: stage-02 marginal r among the two named sets
sub = {"cluster": CLUSTER, "auditory": AUD}
F_named = {k: {p: {"stage01": float(m01[parcels.index(p)]), "stage03_Splus": float(m03p[parcels.index(p)]),
                   "stage03_Sminus": float(m03m[parcels.index(p)]), "stage02_marginal": float(m02_marg[parcels.index(p)]),
                   "stage02_EN": float(m02_en[parcels.index(p)])} for p in v} for k, v in sub.items()}
print("\n   named parcels across stages (r with log cuts / stage-02 within-film marginal r / EN coef):")
for k, v in F_named.items():
    for p, w in v.items():
        print(f"   {k:8} {p:6} st01 {w['stage01']:+.3f}  st03 S+ {w['stage03_Splus']:+.3f} S− {w['stage03_Sminus']:+.3f}  |  st02 marginal {w['stage02_marginal']:+.3f}  EN {w['stage02_EN']:+.3f}")
# stage-02 map restricted to the parcels stage 03 moves, split by sign
out["F_maps"] = {"whole_map_corr": corr, "stage03_both_arm_sets": F_sets, "named": F_named,
                 "stage02_marginal_r_abs_max": float(np.abs(m02_marg).max()),
                 "stage02_marginal_r_top": sorted(((parcels[j], float(m02_marg[j])) for j in range(180)), key=lambda x: -abs(x[1]))[:10]}
print("\n   stage-02 marginal cut-rate map, top |r|:", [(p, round(v, 2)) for p, v in out["F_maps"]["stage02_marginal_r_top"]])

# frontal-minus-auditory contrast in stage 02 vs stage 03
fr = np.array([Y[:, parcels.index(p)] for p in CLUSTER]).mean(axis=0)
au = np.array([Y[:, parcels.index(p)] for p in AUD]).mean(axis=0)
contrast = fr - au
r_con, p_con = r_p(cut_c, contrast); r_fr, p_fr = r_p(cut_c, fr); r_au, p_au = r_p(cut_c, au)
out["G_cluster_means"] = {"r_cuts_frontal_mean": r_fr, "p": p_fr, "r_cuts_auditory_mean": r_au, "p_aud": p_au,
                          "r_cuts_frontal_minus_auditory": r_con, "p_con": p_con,
                          "r_frontal_mean_vs_auditory_mean": r_p(fr, au)[0]}
print(f"\nG  cluster means across 70 segments: r(cuts, frontal mean) {r_fr:+.3f} (p {p_fr:.3f}); r(cuts, auditory mean) {r_au:+.3f} (p {p_au:.3f}); "
      f"r(cuts, frontal−auditory) {r_con:+.3f} (p {p_con:.3f}); r(frontal, auditory) {out['G_cluster_means']['r_frontal_mean_vs_auditory_mean']:+.3f}")

(H / "frontal_miss.json").write_text(json.dumps(out, indent=1, default=str))
print("\nwrote frontal_miss.json")
