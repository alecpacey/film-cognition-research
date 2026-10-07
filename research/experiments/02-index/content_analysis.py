#!/usr/bin/env python3
"""
EXPLORATORY (7 Oct 2026; consolidation 3a, review F5). Implements Q0-Q2 of content_descriptors.md
exactly as fixed in commit 55a8515, on the 70 scored segments, within film.
    .venv-content/bin/python content_analysis.py  ->  content_analysis.json
Reads: parcel_vectors.json, selection.json, dial_table.json, content_av.jsonl, content_words.jsonl.
"""
import json
from pathlib import Path
import numpy as np
from scipy import stats

H = Path(__file__).parent
FRONTAL, AUDITORY = ["IFJa", "IFJp", "IFSp", "8C"], ["A1", "A4", "A5", "MBelt"]
PRIMARY = ["speech_prop", "sem_change_per_min"]
AMENDED = ["sem_dist_per_cut"]   # amendment of 7 Oct, before any parcel data was read (content_descriptors.md)
SECONDARY = ["words_per_min", "sem_dispersion", "sem_pc1", "sem_pc2", "sem_pc3"]
NS, JB = "nothing_sacred", "jungle_book"
N_PERM, N_BOOT = 10_000, 2_000

pv = json.load(open(H / "parcel_vectors.json")); sel = json.load(open(H / "selection.json")); dt = json.load(open(H / "dial_table.json"))
clips = sorted(sel["selected"]); films = np.array([str(dt[c]["film"]) for c in clips]); FILMS = sorted(set(films.tolist()))
cut = np.array([float(dt[c]["cuts_per_min"]) for c in clips])
outcome = {"frontal": np.array([np.mean([pv[c][p]["z"] for p in FRONTAL]) for c in clips]),
           "auditory": np.array([np.mean([pv[c][p]["z"] for p in AUDITORY]) for c in clips])}
for p in FRONTAL: outcome[p] = np.array([pv[c][p]["z"] for c in clips])

# descriptors: all 244 for the PCA, the 70 for analysis
av = {r["clip"]: r for r in map(json.loads, open(H / "content_av.jsonl"))}
wd = {r["clip"]: r for r in map(json.loads, open(H / "content_words.jsonl"))} if (H / "content_words.jsonl").exists() else {}
all_clips = sorted(av); M = np.array([av[c]["mean_embedding"] for c in all_clips]); Mc = M - M.mean(0)
U, S, Vt = np.linalg.svd(Mc, full_matrices=False); pcs = Mc @ Vt[:3].T; pc_var = (S[:3] ** 2 / (S ** 2).sum()).tolist()
desc = {"speech_prop": [av[c]["speech_prop"] for c in clips], "sem_change_per_min": [av[c]["sem_change_per_min"] for c in clips],
        "sem_dispersion": [av[c]["sem_dispersion"] for c in clips],
        "sem_dist_per_cut": [float(np.mean(av[c]["cut_clip_dist"])) if av[c]["cut_clip_dist"] else np.nan for c in clips]}
for k in range(3): desc[f"sem_pc{k+1}"] = [pcs[all_clips.index(c), k] for c in clips]
if all(c in wd for c in clips): desc["words_per_min"] = [wd[c]["words_per_min"] for c in clips]
desc = {k: np.array(v, float) for k, v in desc.items()}


def resid(y, Z):
    if Z is None: return y - y.mean()
    X = np.column_stack([np.ones(len(y)), Z]); return y - X @ np.linalg.lstsq(X, y, rcond=None)[0]


def r_within(y, x, Z=None):
    """Pearson r of y and x within one film, optionally partialling out Z (n x k)."""
    a, b = resid(y, Z), resid(x, Z); return float(a @ b / np.sqrt((a @ a) * (b @ b)))


def by_film(y, x, Zs=None, idx=None):
    idx = np.arange(len(y)) if idx is None else idx
    out = {}
    for f in FILMS:
        m = idx[films[idx] == f]; Z = None if Zs is None else np.column_stack([z[m] for z in Zs])
        out[f] = r_within(y[m], x[m], Z)
    return out


def interaction_F(y, x, f=films):
    """Within-film centred: full model = per-film slope; restricted = common slope. F on 2 df."""
    yc, xc = y.copy(), x.copy()
    for g in FILMS: yc[f == g] -= yc[f == g].mean(); xc[f == g] -= xc[f == g].mean()
    b = (xc @ yc) / (xc @ xc); rss_r = np.sum((yc - b * xc) ** 2)
    rss_f = sum(np.sum((yc[f == g] - (xc[f == g] @ yc[f == g]) / (xc[f == g] @ xc[f == g]) * xc[f == g]) ** 2) for g in FILMS)
    df_f = len(y) - 2 * len(FILMS)
    return ((rss_r - rss_f) / (len(FILMS) - 1)) / (rss_f / df_f)


def perm_within(rng, x):
    xp = x.copy()
    for g in FILMS: m = np.where(films == g)[0]; xp[m] = x[rng.permutation(m)]
    return xp


def boot_idx(rng, base=None):
    base = np.arange(len(films)) if base is None else base
    return np.concatenate([rng.choice(base[films[base] == g], (films[base] == g).sum(), replace=True) for g in FILMS])


def ci(a):
    a = np.asarray(a); a = a[np.isfinite(a)]; return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]


res = {"n": len(clips), "n_per_film": {f: int((films == f).sum()) for f in FILMS}, "sem_pca_variance": pc_var}

# ---------- Q0 ----------
rng = np.random.default_rng(0); F0 = interaction_F(outcome["frontal"], cut)
Fp = np.array([interaction_F(outcome["frontal"], perm_within(rng, cut)) for _ in range(N_PERM)])
p0 = float((1 + np.sum(Fp >= F0)) / (1 + N_PERM))
r0 = by_film(outcome["frontal"], cut); d0 = r0[NS] - r0[JB]
rng = np.random.default_rng(0); bd = []
for _ in range(N_BOOT):
    i = boot_idx(rng); rb = by_film(outcome["frontal"], cut, idx=i); bd.append(rb[NS] - rb[JB])
label = "RELIABLE" if p0 <= .05 else "MARGINAL" if p0 <= .20 else "NOT DEMONSTRATED"
res["Q0"] = {"F_interaction": float(F0), "p_perm": p0, "label": label, "r_frontal_cut_by_film": r0,
             "NS_minus_JB": float(d0), "NS_minus_JB_ci95": ci(bd)}
Fa = interaction_F(outcome["auditory"], cut); rng = np.random.default_rng(0)
Fap = np.array([interaction_F(outcome["auditory"], perm_within(rng, cut)) for _ in range(N_PERM)])
res["Q0"]["auditory_control"] = {"F_interaction": float(Fa), "p_perm": float((1 + np.sum(Fap >= Fa)) / (1 + N_PERM)),
                                 "r_auditory_cut_by_film": by_film(outcome["auditory"], cut)}
print(f"Q0  frontal cut x film F = {F0:.2f}, perm p = {p0:.3f} -> {label};  r by film {({k: round(v, 2) for k, v in r0.items()})};"
      f"  NS-JB = {d0:+.2f} {[round(x, 2) for x in ci(bd)]}")

# ---------- descriptives ----------
res["descriptives"] = {d: {f: {"mean": float(desc[d][films == f].mean()), "sd": float(desc[d][films == f].std(ddof=1))} for f in FILMS} for d in desc}


# ---------- Q1, Q2 ----------
def q2(y_name, D_names, classify):
    y = outcome[y_name]; Zs = [desc[d] for d in D_names]
    base = np.where(np.all([np.isfinite(z) for z in Zs], axis=0))[0]   # drops undefined values (sem_dist_per_cut: zero-cut segments)
    marg = by_film(y, cut, idx=base); part = by_film(y, cut, Zs, idx=base)
    dm, dp = marg[NS] - marg[JB], part[NS] - part[JB]; S_ = 1 - dp / dm
    rng = np.random.default_rng(0); bs = []
    for _ in range(N_BOOT):
        i = boot_idx(rng, base); m_ = by_film(y, cut, idx=i); p_ = by_film(y, cut, Zs, idx=i)
        den = m_[NS] - m_[JB]; bs.append(1 - (p_[NS] - p_[JB]) / den if abs(den) > 1e-9 else np.nan)
    out = {"marginal_r_cut": marg, "partial_r_cut_given_D": part, "delta": float(dm), "delta_partial": float(dp),
           "S": float(S_), "S_ci95": ci(bs)}
    if len(D_names) == 1:
        d = desc[D_names[0]]
        out["r_cut_D"] = by_film(cut, d, idx=base)
        out["partial_r_y_D_given_cut"] = by_film(y, d, [cut], idx=base)
        out["n_per_film"] = {f: int((films[base] == f).sum()) for f in FILMS}
        signs = {np.sign(v) for v in out["partial_r_y_D_given_cut"].values()}
        if classify:
            lo = out["S_ci95"][0]
            out["class"] = ("CARRIES" if (S_ >= .5 and lo > 0 and len(signs) == 1) else "DOES NOT CARRY" if S_ < .25 else "PARTIAL")
    return out


res["Q2"] = {}
for y_name in ["frontal", "auditory"] + FRONTAL:
    res["Q2"][y_name] = {}
    for D in PRIMARY + AMENDED + [s for s in SECONDARY if s in desc]:
        res["Q2"][y_name][D] = q2(y_name, [D], classify=(y_name == "frontal" and D in PRIMARY + AMENDED))
    res["Q2"][y_name]["both_primary"] = q2(y_name, PRIMARY, classify=False)

for y_name in ["frontal", "auditory"]:
    print(f"\n{y_name}: marginal r(cut) by film {({k: round(v, 2) for k, v in res['Q2'][y_name]['speech_prop']['marginal_r_cut'].items()})}")
    for D, o in res["Q2"][y_name].items():
        tag = o.get("class", "")
        rcd = o.get("r_cut_D"); ryd = o.get("partial_r_y_D_given_cut")
        print(f"  {D:20} partial r(cut|D) {({k: round(v, 2) for k, v in o['partial_r_cut_given_D'].items()})}  S {o['S']:+.2f} "
              f"{[round(x, 2) for x in o['S_ci95']]}" + (f"  r(cut,D) {({k: round(v, 2) for k, v in rcd.items()})}" if rcd else "")
              + (f"  r(y,D|cut) {({k: round(v, 2) for k, v in ryd.items()})}" if ryd else "") + (f"  -> {tag}" if tag else ""))

(H / "content_analysis.json").write_text(json.dumps(res, indent=1))
print("\nwrote content_analysis.json")
