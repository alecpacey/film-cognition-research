#!/usr/bin/env python3
"""
POST-HOC (7 Oct 2026; 3a). Written AFTER content_analysis.py had run once and its results were read.
Nothing here alters a fixed result; it characterises what the secondary columns showed.
    .venv-content/bin/python content_posthoc.py  ->  content_posthoc.json
1. Are the semantic descriptors that track the frontal cluster (sem_pc1, sem_pc2, sem_dispersion)
   new information, or existing dials under another name? Within-film r with each of the 14 dials.
2. Does adding speech_prop and the semantic descriptors to the 14 dials raise within-film explained
   variance for the frontal and auditory clusters? Leave-one-out CV R^2 (OLS, film-centred), dials
   alone vs dials + content.
3. The auditory cut-rate relation with and without speech_prop, pooled within film.
"""
import json
from pathlib import Path
import numpy as np

H = Path(__file__).parent
exec(compile((H / "content_analysis.py").read_text().split("def resid")[0], "content_analysis_head", "exec"))   # same loaders, same data
dials = sel["dials"]
Xd = np.array([[float(dt[c][d]) for d in dials] for c in clips])


def centre(a):
    a = np.array(a, float).copy()
    for g in FILMS: a[films == g] -= a[films == g].mean(0)
    return a


def pooled_r(a, b):
    a, b = centre(a), centre(b); m = np.isfinite(a) & np.isfinite(b); a, b = a[m], b[m]
    return float(a @ b / np.sqrt((a @ a) * (b @ b)))


out = {"note": "post-hoc, after the fixed analysis was read"}
out["descriptor_vs_dials_pooled_within_film_r"] = {
    D: {d: round(pooled_r(desc[D], Xd[:, k]), 3) for k, d in enumerate(dials)} for D in ["sem_pc1", "sem_pc2", "sem_pc3", "sem_dispersion", "speech_prop"]}
for D, row in out["descriptor_vs_dials_pooled_within_film_r"].items():
    top = sorted(row.items(), key=lambda kv: -abs(kv[1]))[:3]
    print(f"{D:15} strongest dial correlates (within film): " + ", ".join(f"{k} {v:+.2f}" for k, v in top))


def loo_r2(y, X):
    y, X = centre(y), centre(X); X = (X - X.mean(0)) / np.where(X.std(0) > 0, X.std(0), 1)
    pred = np.empty_like(y)
    for i in range(len(y)):
        m = np.arange(len(y)) != i; A = np.column_stack([np.ones(m.sum()), X[m]])
        b = np.linalg.lstsq(A, y[m], rcond=None)[0]; pred[i] = b[0] + X[i] @ b[1:]
    return float(1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2))


content = np.column_stack([desc["speech_prop"], desc["sem_pc1"], desc["sem_pc2"], desc["sem_dispersion"]])
out["loo_cv_r2"] = {}
for y_name in ["frontal", "auditory"]:
    y = outcome[y_name]
    r = {"dials_only": loo_r2(y, Xd), "content_only": loo_r2(y, content), "dials_plus_content": loo_r2(y, np.column_stack([Xd, content])),
         "dials_plus_speech": loo_r2(y, np.column_stack([Xd, desc["speech_prop"]]))}
    out["loo_cv_r2"][y_name] = r
    print(f"{y_name:9} LOO-CV R2 within film: dials {r['dials_only']:+.3f} | content (speech, PC1, PC2, dispersion) {r['content_only']:+.3f} | "
          f"dials + content {r['dials_plus_content']:+.3f} | dials + speech {r['dials_plus_speech']:+.3f}")

y = outcome["auditory"]
a = centre(y); x = centre(cut); s = centre(desc["speech_prop"])
def pr(a, b, z):
    ra = a - z * (z @ a) / (z @ z); rb = b - z * (z @ b) / (z @ z); return float(ra @ rb / np.sqrt((ra @ ra) * (rb @ rb)))
out["auditory_cut_pooled_within_film"] = {"marginal_r": pooled_r(y, cut), "partial_r_given_speech": pr(a, x, s),
                                          "r_cut_speech": pooled_r(cut, desc["speech_prop"]), "r_auditory_speech": pooled_r(y, desc["speech_prop"])}
print("auditory ~ cut, pooled within film:", {k: round(v, 2) for k, v in out["auditory_cut_pooled_within_film"].items()})
out["frontal_cut_pooled_within_film"] = {"marginal_r": pooled_r(outcome["frontal"], cut),
                                         "partial_r_given_speech": pr(centre(outcome["frontal"]), x, s)}
print("frontal ~ cut, pooled within film:", {k: round(v, 2) for k, v in out["frontal_cut_pooled_within_film"].items()})
(H / "content_posthoc.json").write_text(json.dumps(out, indent=1)); print("wrote content_posthoc.json")

# 4. (added 8 Oct, post-hoc) Q0's interaction test per frontal parcel, since PAPER names IFJa. Same
#    statistic and permutation scheme as content_analysis.py Q0, 10,000 within-film permutations, seed 0.
src = (H / "content_analysis.py").read_text()
exec(compile(src[src.index("def resid"):src.index("res = {")], "content_analysis_fns", "exec"))
out["Q0_per_parcel"] = {}
for p in FRONTAL:
    rng = np.random.default_rng(0); F = interaction_F(outcome[p], cut)
    Fp = np.array([interaction_F(outcome[p], perm_within(rng, cut)) for _ in range(10_000)])
    out["Q0_per_parcel"][p] = {"F": float(F), "p_perm": float((1 + np.sum(Fp >= F)) / 10_001), "r_by_film": by_film(outcome[p], cut)}
    print(f"Q0 {p:5} cut x film F = {F:.2f}, perm p = {out['Q0_per_parcel'][p]['p_perm']:.3f}  r by film "
          + " ".join(f"{k[:2]} {v:+.2f}" for k, v in out["Q0_per_parcel"][p]["r_by_film"].items()))
(H / "content_posthoc.json").write_text(json.dumps(out, indent=1))
