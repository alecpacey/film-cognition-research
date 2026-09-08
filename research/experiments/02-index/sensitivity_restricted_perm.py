#!/usr/bin/env python3
"""
EXPLORATORY SENSITIVITY CHECK — NOT THE PRE-REGISTERED TEST.

The registered test ran once (analyse.py, verdict PARTIAL, analysis_result.json)
and is not re-run, re-tuned or superseded by anything here. Under the registration's
exploratory clause, anything in this file is labelled exploratory and may not be
reported as a confirmatory finding.

THE ONE QUESTION. analyse.py D7 permuted segment labels across all 70 segments,
as literally registered, and flagged the restricted alternative as a limitation:

    "With three films, any within-film structure not removed by centring — segments
     from one scene are not independent — makes this null lenient, and 101 of 180
     is a large fraction. A within-film (restricted) permutation would be the
     conservative test. It was not registered and was not run."

This runs it. Everything is identical to analyse.py — same data, same frozen-SHA
check, same alpha, l1_ratio, folds, CV seed, statistic, FDR, attribution rule and
criterion logic — EXCEPT that each permutation shuffles segment labels WITHIN each
film rather than across all 70.

Why that is the more faithful null: the three films differ in dial distribution and
in response variance. An unrestricted permutation lands one film's response rows on
another film's dial rows, breaking a structure the design never claimed to break —
within-film centring removes each film's MEAN, not its variance or its covariance.
The restricted null preserves film membership and asks only whether the dial-parcel
correspondence within a film is better than chance.

WHAT IT DOES NOT ADDRESS, stated so the check is not oversold: segments adjacent in
time within a film are not independent either, and shuffling within a film does not
preserve that autocorrelation. A block or circular-shift permutation would go
further. This is one step more conservative than registered, not the conservative
limit.

r_obs is unchanged by construction — X and Y are untouched. That it comes out
identical to the registered run is the correctness check on this script.

    .venv-analysis/bin/python sensitivity_restricted_perm.py
"""
import hashlib, json, time
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


def restricted_perm(rng, films):
    """Shuffle indices WITHIN each film. The only difference from analyse.py."""
    idx = np.arange(len(films))
    out = idx.copy()
    for f in np.unique(films):
        m = np.where(films == f)[0]
        out[m] = rng.permutation(m)
    return out


def main():
    t0 = time.time()
    raw = Path("parcel_vectors.json").read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    assert sha == FROZEN_SHA, f"parcel_vectors.json is not the frozen copy: {sha}"
    pv = json.loads(raw)
    sel = json.loads(Path("selection.json").read_text())
    dt = json.loads(Path("dial_table.json").read_text())
    dials, clips = sel["dials"], sorted(sel["selected"])
    films = np.array([dt[c]["film"] for c in clips])
    parcels = sorted(pv[clips[0]])

    X = centre_within(np.array([[float(dt[c][d]) for d in dials] for c in clips]), films)
    sd = X.std(axis=0, ddof=1); sd[sd == 0] = 1.0
    X = X / sd
    Y = centre_within(np.array([[pv[c][p]["z"] for p in parcels] for c in clips]), films)
    n, P, D = Y.shape[0], Y.shape[1], X.shape[1]
    print(f"n={n} parcels={P} dials={D} films={dict(zip(*np.unique(films, return_counts=True)))}")
    print(f"frozen data verified: sha256 {sha[:16]}…")

    print("observed CV r (must match the registered run exactly)…", flush=True)
    r_obs = np.array(Parallel(n_jobs=-1)(delayed(cv_r)(X, Y[:, j]) for j in range(P)))

    reg = json.loads(Path("analysis_result.json").read_text())
    reg_r = np.array([reg["per_parcel"][p]["r_obs"] for p in parcels])
    max_dev = float(np.abs(r_obs - reg_r).max())
    print(f"  max |r_obs - registered r_obs| = {max_dev:.2e}  "
          f"{'OK' if max_dev < 1e-9 else '** MISMATCH — STOP **'}")
    assert max_dev < 1e-9, "observed statistics differ from the registered run"

    rng = np.random.default_rng(SEED)
    perms = [restricted_perm(rng, films) for _ in range(N_PERM)]
    same_film = all((films[p] == films).all() for p in perms[:50])
    print(f"restricted permutations preserve film membership: {same_film}")
    assert same_film

    print(f"{N_PERM} WITHIN-FILM permutations × {P} parcels…", flush=True)
    def one_perm(pi):
        Yp = Y[pi]
        return [cv_r(X, Yp[:, j]) for j in range(P)]
    r_null = np.array(Parallel(n_jobs=-1)(delayed(one_perm)(pi) for pi in perms))

    p_perm = (1 + (r_null >= r_obs[None, :]).sum(axis=0)) / (1 + N_PERM)
    q = false_discovery_control(p_perm, method="bh")
    survive = q < Q
    p95 = np.percentile(r_null, 95, axis=0)

    coefs = np.zeros((P, D))
    for j in range(P):
        coefs[j] = ElasticNet(alpha=ALPHA, l1_ratio=L1, max_iter=10000).fit(X, Y[:, j]).coef_
    surv_idx = np.where(survive)[0]
    dial_hits = {d: [parcels[j] for j in surv_idx if coefs[j, i] != 0] for i, d in enumerate(dials)}
    n_dials = sum(1 for d in dials if dial_hits[d])

    i_cut, i_len = dials.index("cuts_per_min"), dials.index("mean_shot_len_s")
    cluster = {}
    for p in CLUSTER:
        j = parcels.index(p)
        cluster[p] = {"r_obs": float(r_obs[j]), "p95_null": float(p95[j]), "q": float(q[j]),
                      "survives": bool(survive[j]), "coef_cuts_per_min": float(coefs[j, i_cut]),
                      "coef_mean_shot_len_s": float(coefs[j, i_len])}
    replicates = any(v["survives"] and (v["coef_cuts_per_min"] > 0 or v["coef_mean_shot_len_s"] < 0)
                     for v in cluster.values())

    reg_surv = set(p for p in parcels if reg["per_parcel"][p]["survives"])
    now_surv = set(parcels[j] for j in surv_idx)
    out = {"EXPLORATORY": True,
           "note": "Not the pre-registered test. Restricted (within-film) permutation. "
                   "The registered result in analysis_result.json stands unchanged.",
           "registered_verdict": reg["verdict"],
           "exploratory_criterion_1_dials": n_dials, "exploratory_criterion_1_met": n_dials >= 3,
           "exploratory_criterion_2_replicates": replicates,
           "n_surviving_registered": len(reg_surv), "n_surviving_restricted": len(now_surv),
           "retained": sorted(reg_surv & now_surv), "lost": sorted(reg_surv - now_surv),
           "gained": sorted(now_surv - reg_surv),
           "median_p95_null_registered": float(np.median([reg["per_parcel"][p]["p95_null"] for p in parcels])),
           "median_p95_null_restricted": float(np.median(p95)),
           "per_dial": {d: len(dial_hits[d]) for d in dials},
           "cluster": cluster,
           "per_parcel": {parcels[j]: {"r_obs": float(r_obs[j]), "p95_null": float(p95[j]),
                                       "q": float(q[j]), "survives": bool(survive[j])} for j in range(P)},
           "runtime_s": time.time() - t0}
    Path("sensitivity_restricted_perm.json").write_text(json.dumps(out, indent=1))

    print("\n" + "=" * 62)
    print("EXPLORATORY — restricted (within-film) permutation")
    print("=" * 62)
    print(f"registered verdict stands: {reg['verdict']}   (unchanged, not re-run)")
    print(f"surviving parcels: registered {len(reg_surv)}/180  ->  restricted {len(now_surv)}/180")
    print(f"  retained {len(reg_surv & now_surv)}   lost {len(reg_surv - now_surv)}   gained {len(now_surv - reg_surv)}")
    print(f"median 95th-pct null r: registered {out['median_p95_null_registered']:+.3f}  "
          f"restricted {out['median_p95_null_restricted']:+.3f}")
    print(f"dials with >=1 surviving parcel: {n_dials}/14  (registered 14/14)")
    print(f"cut rate replicates in cluster: {'YES' if replicates else 'NO'}  (registered NO)")
    print("\nper dial (restricted):")
    for d in dials:
        print(f"  {d:18} {len(dial_hits[d]):3}")
    print("\ncluster (restricted):")
    for p, v in cluster.items():
        print(f"  {p:5} r_obs {v['r_obs']:+.3f}  null95 {v['p95_null']:+.3f}  q {v['q']:.3f}  "
              f"{'SURVIVES' if v['survives'] else 'no'}")
    print(f"\nwrote sensitivity_restricted_perm.json  ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
