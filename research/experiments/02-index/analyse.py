#!/usr/bin/env python3
"""
STAGE 02 — THE PRE-REGISTERED TEST. Runs once.

Registered 8 Sep 2026, osf.io/dg7fe. Implements README.md § Pass criteria as
written. Where the registration is SILENT, the choice is declared here, before
the run, and reported as a declared choice in RESULT.md — never tuned, never
revisited.

REGISTERED (implemented verbatim)
  - centre every dial and every parcel within film; parcels use the z field;
    cut count as measured, no log transform
  - per parcel: cross-validated elastic net of centred parcel on all 14 centred
    dials; 180 models; no dial dropped; no interactions; no dimension reduction;
    no model selection
  - null: 1,000 permutations of segment labels, full CV refit each time
  - statistic: cross-validated predictive r per parcel; survives if it exceeds
    the 95th percentile of its own permutation distribution, after FDR across 180
  - PASS: >=3 dials with >=1 surviving parcel AND cut rate replicates in
    {IFJa, IFJp, IFSp, 8C}; PARTIAL: first but not second; FAIL otherwise

DECLARED (registration silent; fixed before running)
  D1  Elastic net alpha=0.1, l1_ratio=0.5 — the values the pre-registered
      30-segment futility check used, so "the same machinery as the final test"
      holds. Fixed, not selected.
  D2  5-fold KFold, shuffled, random_state=0. Same as the futility check.
  D3  Dials are STANDARDISED (divided by their within-film-centred SD) before the
      elastic net. This is not a data transformation but a penalty necessity:
      dials span 1e-4 to 1e2, and an unscaled L1/L2 penalty would zero the small
      ones by units alone. Parcels are not rescaled.
  D4  Permutation p per parcel = (1 + #{r_perm >= r_obs}) / (1 + 1000), one-sided,
      since "exceeds the 95th percentile" is one-sided. FDR: Benjamini-Hochberg
      across 180 parcels, q = 0.05, scipy.stats.false_discovery_control.
      The SAME permutation of segment labels is applied to all 180 parcels within
      a given iteration (rows of Y permuted, X fixed), which preserves the
      parcels' correlation structure under the null.
  D5  Attribution of a surviving parcel to a dial: that dial's coefficient is
      non-zero in the parcel's elastic net fitted on all 70 segments. This is
      the only per-dial quantity the registered model produces.
  D6  "Cut rate replicates": at least one of {IFJa, IFJp, IFSp, 8C} survives FDR
      AND, in its full-data fit, has a non-zero coefficient on cuts_per_min with
      POSITIVE sign (stage 01: IFJa r = +0.996 with cut count) OR on
      mean_shot_len_s with NEGATIVE sign (its inverse). All four parcels are
      reported whatever the verdict.
  D7  Permutation is unrestricted across all 70 segments, as literally
      registered. Restricted (within-film) permutation would respect the
      blocking; it was not registered and is listed as a limitation.
  D8  Seed 20260908 for the permutation stream.

    .venv-analysis/bin/python analyse.py
"""
import hashlib, json, sys, time
from pathlib import Path
import numpy as np
from scipy.stats import false_discovery_control
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import KFold
from joblib import Parallel, delayed

FROZEN_SHA = "93807b80a8ec33a42b853a285cd629e663cdb429658ff115a20885cb053a3189"
N_PERM, ALPHA, L1, FOLDS, SEED, Q = 1000, 0.1, 0.5, 5, 20260908, 0.05
CLUSTER = ["IFJa", "IFJp", "IFSp", "8C"]


def centre_within(M, films):
    M = M.astype(float).copy()
    for f in np.unique(films):
        m = films == f
        M[m] -= M[m].mean(axis=0)
    return M


def cv_pred(X, y):
    pred = np.zeros_like(y)
    for tr, te in KFold(n_splits=FOLDS, shuffle=True, random_state=0).split(X):
        m = ElasticNet(alpha=ALPHA, l1_ratio=L1, max_iter=10000)
        m.fit(X[tr], y[tr]); pred[te] = m.predict(X[te])
    return pred


def cv_r(X, y):
    p = cv_pred(X, y)
    return 0.0 if p.std() < 1e-12 or y.std() < 1e-12 else float(np.corrcoef(p, y)[0, 1])


def main():
    t0 = time.time()
    raw = Path("parcel_vectors.json").read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    assert sha == FROZEN_SHA, f"parcel_vectors.json is not the frozen copy: {sha}"
    pv = json.loads(raw)
    sel = json.loads(Path("selection.json").read_text())
    dt = json.loads(Path("dial_table.json").read_text())
    dials, clips = sel["dials"], sel["selected"]
    assert set(clips) == set(pv) and len(clips) == 70, "clip set is not the registered 70"
    clips = sorted(clips)
    films = np.array([dt[c]["film"] for c in clips])
    parcels = sorted(pv[clips[0]])
    assert len(parcels) == 180 and all(set(pv[c]) == set(parcels) for c in clips)
    for p in CLUSTER: assert p in parcels, p

    X = centre_within(np.array([[float(dt[c][d]) for d in dials] for c in clips]), films)
    sd = X.std(axis=0, ddof=1); sd[sd == 0] = 1.0
    X = X / sd                                                  # D3
    Y = centre_within(np.array([[pv[c][p]["z"] for p in parcels] for c in clips]), films)
    n, P, D = Y.shape[0], Y.shape[1], X.shape[1]
    print(f"n={n} parcels={P} dials={D} films={dict(zip(*np.unique(films, return_counts=True)))}")
    print(f"frozen data verified: sha256 {sha[:16]}…")

    # observed
    print("observed CV r for 180 parcels…", flush=True)
    r_obs = np.array(Parallel(n_jobs=-1)(delayed(cv_r)(X, Y[:, j]) for j in range(P)))

    # null: same label permutation for all parcels within an iteration (D4)
    rng = np.random.default_rng(SEED)
    perms = [rng.permutation(n) for _ in range(N_PERM)]
    print(f"{N_PERM} permutations × {P} parcels…", flush=True)
    def one_perm(pi):
        Yp = Y[pi]
        return [cv_r(X, Yp[:, j]) for j in range(P)]
    r_null = np.array(Parallel(n_jobs=-1, verbose=0)(delayed(one_perm)(pi) for pi in perms))  # (N_PERM, P)

    p_perm = (1 + (r_null >= r_obs[None, :]).sum(axis=0)) / (1 + N_PERM)     # D4
    q = false_discovery_control(p_perm, method="bh")
    survive = q < Q
    p95 = np.percentile(r_null, 95, axis=0)

    # full-data fits for attribution (D5, D6)
    coefs = np.zeros((P, D))
    for j in range(P):
        m = ElasticNet(alpha=ALPHA, l1_ratio=L1, max_iter=10000).fit(X, Y[:, j])
        coefs[j] = m.coef_
    surv_idx = np.where(survive)[0]
    dial_hits = {d: [parcels[j] for j in surv_idx if coefs[j, i] != 0] for i, d in enumerate(dials)}
    n_dials = sum(1 for d in dials if dial_hits[d])

    i_cut, i_len = dials.index("cuts_per_min"), dials.index("mean_shot_len_s")
    cluster = {}
    for p in CLUSTER:
        j = parcels.index(p)
        cluster[p] = {"r_obs": float(r_obs[j]), "p95_null": float(p95[j]), "p_perm": float(p_perm[j]),
                      "q": float(q[j]), "survives": bool(survive[j]),
                      "coef_cuts_per_min": float(coefs[j, i_cut]), "coef_mean_shot_len_s": float(coefs[j, i_len])}
    replicates = any(v["survives"] and (v["coef_cuts_per_min"] > 0 or v["coef_mean_shot_len_s"] < 0)
                     for v in cluster.values())                                  # D6

    c1 = n_dials >= 3
    verdict = "PASS" if (c1 and replicates) else ("PARTIAL" if (c1 and not replicates) else "FAIL")

    out = {"verdict": verdict, "criterion_1_dials_with_surviving_parcel": n_dials, "criterion_1_met": c1,
           "criterion_2_cut_rate_replicates": replicates, "n_surviving_parcels": int(survive.sum()),
           "declared": {"alpha": ALPHA, "l1_ratio": L1, "folds": FOLDS, "n_perm": N_PERM, "q": Q, "seed": SEED},
           "per_dial": {d: {"n_surviving_parcels_attributed": len(dial_hits[d]), "parcels": dial_hits[d],
                            "label": sel["detectability"][d]["label"]} for d in dials},
           "cluster": cluster,
           "per_parcel": {parcels[j]: {"r_obs": float(r_obs[j]), "p95_null": float(p95[j]),
                                       "p_perm": float(p_perm[j]), "q": float(q[j]), "survives": bool(survive[j]),
                                       "coef": {d: float(coefs[j, i]) for i, d in enumerate(dials)}}
                          for j in range(P)},
           "runtime_s": time.time() - t0, "sha256_parcel_vectors": sha}
    Path("analysis_result.json").write_text(json.dumps(out, indent=1))

    print("\n" + "=" * 60)
    print(f"VERDICT: {verdict}")
    print("=" * 60)
    print(f"criterion 1: {n_dials}/14 dials with >=1 surviving parcel (need >=3) -> {'met' if c1 else 'NOT met'}")
    print(f"criterion 2: cut rate replicates in inferior-frontal cluster -> {'YES' if replicates else 'NO'}")
    print(f"surviving parcels (FDR q<{Q}): {int(survive.sum())}/180")
    print("\nper dial:")
    for d in dials:
        print(f"  {d:18} {len(dial_hits[d]):3} surviving parcel(s)  [{sel['detectability'][d]['label']}]")
    print("\ncluster:")
    for p, v in cluster.items():
        print(f"  {p:5} r_obs {v['r_obs']:+.3f}  null95 {v['p95_null']:+.3f}  q {v['q']:.3f}  "
              f"{'SURVIVES' if v['survives'] else 'no'}  coef(cuts) {v['coef_cuts_per_min']:+.3f}  coef(shotlen) {v['coef_mean_shot_len_s']:+.3f}")
    print(f"\nwrote analysis_result.json  ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
