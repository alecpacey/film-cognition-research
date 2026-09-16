#!/usr/bin/env python3
"""
EXPLORATORY, 16 Sep 2026. Does inferior-frontal cortex track scene switches rather than cuts?
Reads scene_switches_corpus.jsonl (from scene_switches.py) and the frozen stage-02 data.
Registered verdict unchanged. Output: scene_switches_result.json, printed summary.
    .venv-analysis/bin/python scene_switches_analysis.py
"""
import json, hashlib
from pathlib import Path
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression

H = Path(__file__).parent
CLUSTER = ["IFJa", "IFJp", "IFSp", "8C"]; AUD = ["A4", "A1", "MBelt", "A5"]; FOCUS = CLUSTER + AUD
THR = [0.5, 0.6, 0.7]

raw = (H / "parcel_vectors.json").read_bytes()
assert hashlib.sha256(raw).hexdigest().startswith("93807b80")
pv = json.loads(raw); sel = json.loads((H / "selection.json").read_text()); dt = json.loads((H / "dial_table.json").read_text())
clips = sorted(sel["selected"]); films = np.array([dt[c]["film"] for c in clips]); parcels = sorted(pv[clips[0]])
recs = {}
for l in (H / "scene_switches_corpus.jsonl").read_text().splitlines():
    if l.strip():
        r = json.loads(l)
        if "error" not in r: recs[r["clip"]] = r
print(f"{len(recs)} segments with scene-switch measurements; {sum(c in recs for c in clips)}/70 scored segments covered")


def feats(r):
    d = np.array([c["hist_dist"] for c in r["cuts"]]) if r["cuts"] else np.zeros(0)
    f = {"cuts": r["n_cuts"], "sum_dist": float(d.sum()), "mean_dist": float(d.mean()) if d.size else 0.0}
    for t in THR:
        f[f"between_{t}"] = int((d >= t).sum()); f[f"within_{t}"] = int((d < t).sum())
    return f


def cw(M):
    M = M.astype(float).copy()
    for f in np.unique(films): M[films == f] -= M[films == f].mean(axis=0)
    return M


out = {"note": "EXPLORATORY; registered verdict unchanged", "thresholds": THR}
# ---- descriptive, all segments ----
alld = np.concatenate([[c["hist_dist"] for c in r["cuts"]] for r in recs.values()])
out["corpus_cut_distances"] = {"n_cuts": int(alld.size), "quantiles": {q: float(np.quantile(alld, q)) for q in (0.1, 0.25, 0.5, 0.75, 0.9)},
                               "frac_ge": {t: float((alld >= t).mean()) for t in THR}}
print("\nall corpus cuts:", out["corpus_cut_distances"])
perfilm = {}
for f in np.unique(films):
    rs = [recs[c] for c in recs if dt.get(c, {}).get("film") == f or c.startswith(f)]
    F = [feats(r) for r in rs]
    perfilm[f] = {"n_segments": len(F), "cuts_per_seg": float(np.mean([x["cuts"] for x in F])),
                  **{f"between_{t}_per_seg": float(np.mean([x[f"between_{t}"] for x in F])) for t in THR}}
    print(f"  {f:15} segs {len(F):3}  cuts/seg {perfilm[f]['cuts_per_seg']:5.2f}  between≥0.5 {perfilm[f]['between_0.5_per_seg']:5.2f}  ≥0.6 {perfilm[f]['between_0.6_per_seg']:5.2f}  ≥0.7 {perfilm[f]['between_0.7_per_seg']:5.2f}")
out["per_film"] = perfilm

# ---- the 70 scored segments ----
sc = [c for c in clips if c in recs]
assert len(sc) == 70, f"only {len(sc)} scored segments measured"
F = {c: feats(recs[c]) for c in clips}
# detector reproduces the registered dial?
reg = np.array([float(dt[c]["cuts_per_min"]) for c in clips]); mine = np.array([recs[c]["cuts_per_min"] for c in clips])
out["dial_reproduction"] = {"max_abs_diff_cuts_per_min": float(np.abs(reg - mine).max()), "r": float(np.corrcoef(reg, mine)[0, 1])}
print(f"\ncut dial reproduced: max |Δ cuts/min| {out['dial_reproduction']['max_abs_diff_cuts_per_min']:.2f}, r {out['dial_reproduction']['r']:.4f}")

Y = cw(np.array([[pv[c][p]["z"] for p in parcels] for c in clips]))
names = ["cuts", "sum_dist", "mean_dist"] + [f"between_{t}" for t in THR] + [f"within_{t}" for t in THR]
X = {n: cw(np.array([F[c][n] for c in clips])[:, None])[:, 0] for n in names}
Xlog = {n: cw(np.log1p(np.array([F[c][n] for c in clips]))[:, None])[:, 0] for n in names}
print("\ncorrelation of predictors (within-film centred): cuts vs", {n: round(float(np.corrcoef(X["cuts"], X[n])[0, 1]), 2) for n in names if n != "cuts"})
out["predictor_corr_with_cuts"] = {n: float(np.corrcoef(X["cuts"], X[n])[0, 1]) for n in names}

print(f"\n{'parcel':6} | " + " | ".join(f"{n:>11}" for n in names))
tab = {}
for p in FOCUS:
    y = Y[:, parcels.index(p)]; row = {}
    for n in names:
        r, pp = stats.pearsonr(X[n], y); rl = stats.pearsonr(Xlog[n], y)[0]
        row[n] = {"r": float(r), "p": float(pp), "r_log": float(rl)}
    tab[p] = row
    print(f"{p:6} | " + " | ".join(f"{row[n]['r']:+.2f} ({row[n]['p']:.2f})" for n in names))
out["marginal_r_70"] = tab

# partials: between given within, within given between (threshold 0.6 primary, others reported)
def resid(y, z):
    return y - LinearRegression().fit(z[:, None], y).predict(z[:, None])
part = {}
print("\npartial r: between-scene cuts | within-scene cuts   and   within | between")
for t in THR:
    part[t] = {}
    for p in FOCUS:
        y = Y[:, parcels.index(p)]; b, w = X[f"between_{t}"], X[f"within_{t}"]
        rb, pb = stats.pearsonr(resid(b, w), resid(y, w)); rw, pw = stats.pearsonr(resid(w, b), resid(y, b))
        part[t][p] = {"between_given_within": float(rb), "p_b": float(pb), "within_given_between": float(rw), "p_w": float(pw)}
    print(f"  thr {t}: " + "  ".join(f"{p} b|w {part[t][p]['between_given_within']:+.2f} w|b {part[t][p]['within_given_between']:+.2f}" for p in FOCUS))
out["partials"] = part

# per film, IFJa/IFSp/8C vs between_0.6
pf = {}
for p in CLUSTER:
    pf[p] = {}
    for f in np.unique(films):
        m = films == f
        pf[p][f] = {t: float(stats.pearsonr(X[f"between_{t}"][m], Y[m, parcels.index(p)])[0]) for t in THR}
print("\nper-film r with between-scene count (0.5/0.6/0.7):")
for p in CLUSTER: print(f"  {p:5} " + "  ".join(f"{f[:6]} " + "/".join(f"{pf[p][f][t]:+.2f}" for t in THR) for f in pf[p]))
out["per_film_cluster"] = pf

# whole-map: r-map of each predictor vs stage 01 / 03 causal maps
def ladder(pvx, prefix):
    cts = {"cut01": 1, "cut03": 3, "cut07": 7, "cut15": 15, "cut31": 31}; x = np.log(list(cts.values()))
    g = lambda c, p: pvx[c][p]["z"] if isinstance(pvx[c][p], dict) else pvx[c][p]
    return np.array([np.corrcoef(x, [g(f"{prefix}{c}", p) for c in cts])[0, 1] for p in parcels])
pv01 = json.loads((H.parent / "01-cutrate" / "parcel_vectors.json").read_text()); pv03 = json.loads((H.parent / "03-isolation" / "parcel_vectors.json").read_text())
causal = {"stage01": ladder(pv01, ""), "stage03_Splus": ladder(pv03, "Splus_"), "stage03_Sminus": ladder(pv03, "Sminus_")}
maps = {n: np.array([stats.pearsonr(X[n], Y[:, j])[0] for j in range(180)]) for n in names}
mc = {n: {k: float(np.corrcoef(maps[n], v)[0, 1]) for k, v in causal.items()} for n in names}
out["whole_map_corr"] = mc
print("\nwhole-map r (180 parcels) of each corpus predictor's marginal map vs causal maps:")
for n in names: print(f"  {n:12} st01 {mc[n]['stage01']:+.2f}  st03 S+ {mc[n]['stage03_Splus']:+.2f}  S− {mc[n]['stage03_Sminus']:+.2f}")
# frontal cluster mean and auditory mean vs each predictor
fr = Y[:, [parcels.index(p) for p in CLUSTER]].mean(1); au = Y[:, [parcels.index(p) for p in AUD]].mean(1)
out["cluster_means"] = {n: {"frontal_r": float(stats.pearsonr(X[n], fr)[0]), "frontal_p": float(stats.pearsonr(X[n], fr)[1]),
                            "auditory_r": float(stats.pearsonr(X[n], au)[0]), "auditory_p": float(stats.pearsonr(X[n], au)[1])} for n in names}
print("\ncluster means:")
for n in names: v = out["cluster_means"][n]; print(f"  {n:12} frontal {v['frontal_r']:+.3f} (p {v['frontal_p']:.2f})  auditory {v['auditory_r']:+.3f} (p {v['auditory_p']:.3f})")
(H / "scene_switches_result.json").write_text(json.dumps(out, indent=1))
print("\nwrote scene_switches_result.json")
