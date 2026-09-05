#!/usr/bin/env python3
"""
Stage-02 dial diagnostics and segment selection.

Everything here was specified in README.md before any dial was measured.

Three jobs:

1. DETECTABILITY. Dials are centred within film, per the corpus decision. That
   removes each film's mean — and for a dial that varies mostly BETWEEN films
   rather than within them, centring removes nearly all of it. The surviving
   within-film spread is what any correlation is actually computed on, so it,
   not the raw spread, decides whether a dial could be detected at all.

   Reported as `s` = pooled within-film SD / total SD. Restriction of range then
   says a true correlation r is observed, through that compression, as

        r_obs = r*s / sqrt(1 - r^2 + r^2 * s^2)

   A dial is labelled TESTED when r_obs at the pre-registered SESOI still gives
   >= 80% power at the planned n, and UNDERPOWERED otherwise. No dial is dropped:
   the label exists so that a null can be reported as a real null or as never
   tested, which are different findings.

2. INTERDEPENDENCE. The dial correlation matrix on centred values, plus its
   condition number and per-dial VIF. Reported as a diagnostic, not modelled —
   separating covarying dials is what stage 03 is for.

3. SELECTION. Choose the segments to score on GPU by stratified, space-filling
   sampling across dial ranges: within each film, stratify on cut rate (the dial
   stage 01 established and stage 02 must replicate), then within each stratum
   take the segment whose standardised dial vector is farthest from those already
   chosen. This spreads every dial, not just the stratifying one.

   Selection uses stimulus properties only. No parcel value exists yet, so this
   is design, not selection on outcomes.

    python analyse_dials.py --n 60
"""
import argparse, json, math
from pathlib import Path
import numpy as np

SESOI = 0.50          # pre-registered, README.md
ALPHA = 0.05
POWER_FLOOR = 0.80
DF_LOST = 3           # one mean per film removed by within-film centring

DIALS = ["cuts_per_min", "mean_shot_len_s", "camera_jitter", "camera_zoom",
         "camera_pan", "median_luma", "contrast_p5_p95", "shadow_frac",
         "colourfulness", "mean_saturation", "warm_cool", "face_area_frac",
         "face_hit_rate", "dof_ratio"]


def ncdf(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def nppf(p):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if ncdf(mid) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def power_r(n, r, alpha=ALPHA, df_lost=DF_LOST):
    ne = n - df_lost
    if ne < 5 or r <= 0: return 0.0
    r = min(r, 0.999)
    z = 0.5 * math.log((1 + r) / (1 - r)); se = 1 / math.sqrt(ne - 3)
    crit = nppf(1 - alpha / 2)
    return (1 - ncdf(crit - z / se)) + ncdf(-crit - z / se)


def attenuate(r, s):
    """Observed r when the predictor's spread is compressed to fraction s."""
    if s <= 0: return 0.0
    return r * s / math.sqrt(1 - r**2 + (r**2) * (s**2))


def load(path="dial_table.json"):
    rows = json.loads(Path(path).read_text())
    names = sorted(rows)
    films = np.array([rows[n]["film"] for n in names])
    cols, kept = [], []
    for d in DIALS:
        v = [rows[n].get(d) for n in names]
        if any(x is None for x in v):
            print(f"  ! {d}: has missing values, excluded from the matrix")
            continue
        cols.append([float(x) for x in v]); kept.append(d)
    return names, films, np.array(cols).T, kept


def centre_within(X, films):
    Xc = X.astype(float).copy()
    for f in np.unique(films):
        m = films == f
        Xc[m] -= Xc[m].mean(axis=0)
    return Xc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", default="dial_table.json")
    ap.add_argument("--n", type=int, default=60, help="segments to select")
    ap.add_argument("--out", default="selection.json")
    a = ap.parse_args()

    names, films, X, dials = load(a.table)
    n_seg = len(names)
    uf = sorted(set(films))
    print(f"{n_seg} segments, {len(dials)} dials, {len(uf)} films "
          f"({', '.join(f'{f} {int((films==f).sum())}' for f in uf)})\n")

    Xc = centre_within(X, films)

    # ---- 1. detectability -----------------------------------------------
    print("DETECTABILITY  (SESOI r >= %.2f, n = %d)\n" % (SESOI, a.n))
    print(f"{'dial':20} {'total SD':>10} {'within SD':>10} {'s':>6} "
          f"{'r_obs':>7} {'power':>7}  label")
    labels = {}
    for j, d in enumerate(dials):
        tot = X[:, j].std(ddof=1)
        wit = Xc[:, j].std(ddof=1)
        s = wit / tot if tot > 0 else 0.0
        r_obs = attenuate(SESOI, s)
        pw = power_r(a.n, r_obs)
        lab = "TESTED" if pw >= POWER_FLOOR else "UNDERPOWERED"
        labels[d] = {"total_sd": tot, "within_sd": wit, "s": s,
                     "r_obs_at_sesoi": r_obs, "power": pw, "label": lab}
        print(f"{d:20} {tot:10.3f} {wit:10.3f} {s:6.2f} {r_obs:7.2f} {pw:7.2f}  {lab}")

    n_test = sum(1 for v in labels.values() if v["label"] == "TESTED")
    print(f"\n  {n_test}/{len(dials)} dials TESTED at n={a.n}. "
          f"Nulls on the rest are uninformative and must be reported as untested.")

    # ---- 2. interdependence ---------------------------------------------
    print("\n\nINTERDEPENDENCE  (centred within film)\n")
    sd = Xc.std(axis=0, ddof=1); sd[sd == 0] = 1e-12
    Z = Xc / sd
    C = np.corrcoef(Z, rowvar=False)
    print("  strongest pairs:")
    pairs = [(abs(C[i, j]), C[i, j], dials[i], dials[j])
             for i in range(len(dials)) for j in range(i + 1, len(dials))]
    for _, r, x, y in sorted(pairs, reverse=True)[:10]:
        print(f"    {x:20} {y:20} r = {r:+.2f}")
    ev = np.linalg.eigvalsh(C)
    cond = float(ev.max() / max(ev.min(), 1e-12))
    print(f"\n  condition number of the dial correlation matrix: {cond:.1f}")
    print("    (>30 indicates meaningful collinearity; >100 severe)")
    vif = {}
    for j, d in enumerate(dials):
        others = [k for k in range(len(dials)) if k != j]
        A = Z[:, others]; y = Z[:, j]
        beta, *_ = np.linalg.lstsq(A, y, rcond=None)
        r2 = 1 - ((y - A @ beta) ** 2).sum() / max(((y - y.mean()) ** 2).sum(), 1e-12)
        vif[d] = 1 / max(1 - r2, 1e-9)
    print("\n  highest VIF:")
    for d, v in sorted(vif.items(), key=lambda kv: -kv[1])[:6]:
        print(f"    {d:20} {v:8.1f}")

    # ---- 3. selection ----------------------------------------------------
    # Distribute n across films; any remainder goes to the films with the most
    # source segments, so the split never silently returns fewer than n.
    base, rem = divmod(a.n, len(uf))
    by_size = sorted(uf, key=lambda f: -int((films == f).sum()))
    quota = {f: base + (1 if i < rem else 0) for i, f in enumerate(by_size)}
    chosen = []
    cut_idx = dials.index("cuts_per_min") if "cuts_per_min" in dials else 0
    for f in uf:
        per_film = quota[f]
        idx = np.where(films == f)[0]
        order = idx[np.argsort(X[idx, cut_idx])]
        strata = np.array_split(order, per_film)
        picked = []
        for st in strata:
            if len(st) == 0: continue
            if not picked:
                picked.append(int(st[len(st) // 2]))          # stratum median
            else:
                P = Z[picked]
                d2 = np.array([min(((Z[c] - P) ** 2).sum(axis=1)) for c in st])
                picked.append(int(st[int(np.argmax(d2))]))     # maximin coverage
        chosen += picked
    chosen = sorted(chosen)
    print(f"\n\nSELECTION  {len(chosen)} segments  "
          f"({', '.join(f'{f} {quota[f]}' for f in uf)})\n")
    print(f"{'dial':20} {'all 244 range':>22} {'selected range':>22} {'kept':>6}")
    for j, d in enumerate(dials):
        a_lo, a_hi = X[:, j].min(), X[:, j].max()
        s_lo, s_hi = X[chosen, j].min(), X[chosen, j].max()
        kept = (s_hi - s_lo) / (a_hi - a_lo) if a_hi > a_lo else 1.0
        print(f"{d:20} {a_lo:10.2f}-{a_hi:10.2f} {s_lo:10.2f}-{s_hi:10.2f} {kept:6.2f}")

    Path(a.out).write_text(json.dumps(
        {"sesoi": SESOI, "n": a.n, "dials": dials, "detectability": labels,
         "condition_number": cond, "vif": vif,
         "selected": [names[i] for i in chosen]}, indent=1))
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
