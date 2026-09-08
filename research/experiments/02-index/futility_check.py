#!/usr/bin/env python3
"""
Pre-registered futility check at 30 segments. NOT the statistical test.

README.md, § What the between-batch check is for:

    at 30 segments, run the permutation null on the dials measured so far. If no
    dial has any parcel whose cross-validated `r` exceeds the 95th percentile of
    its own permutation distribution *uncorrected*, stop for futility.

This is a RESOURCE decision, declared in advance, not an inferential one. It is
deliberately lenient — uncorrected, so it stops only a study showing nothing at
all. The real test (FDR-corrected, on all 70) runs once and is untouched by this.

Reporting discipline: this script prints a VERDICT and nothing else. It does not
name which dial or which parcel, because the README states that anything seen in
an interim look may not be reported as a finding. Naming them here would turn a
resource check into a peek that biases the eventual write-up.

    .venv-analysis/bin/python futility_check.py
"""
import json
import numpy as np
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import KFold

RNG = np.random.default_rng(20260906)
N_PERM = 500
DIALS = ["cuts_per_min", "mean_shot_len_s", "camera_jitter", "camera_zoom",
         "camera_pan", "median_luma", "contrast_p5_p95", "shadow_frac",
         "colourfulness", "mean_saturation", "warm_cool", "face_area_frac",
         "face_hit_rate", "dof_ratio"]


def centre_within(M, films):
    M = M.astype(float).copy()
    for f in np.unique(films):
        m = films == f
        M[m] -= M[m].mean(axis=0)
    return M


def cv_r(X, y, folds=5):
    """Cross-validated predictive r for one parcel from the dial set."""
    pred = np.zeros_like(y)
    for tr, te in KFold(n_splits=folds, shuffle=True, random_state=0).split(X):
        m = ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=5000)
        m.fit(X[tr], y[tr])
        pred[te] = m.predict(X[te])
    if pred.std() < 1e-12 or y.std() < 1e-12:
        return 0.0
    return float(np.corrcoef(pred, y)[0, 1])


def main():
    dt = json.load(open("dial_table.json"))
    pv = json.load(open("parcel_vectors.json"))
    clips = sorted(set(dt) & set(pv))
    films = np.array([dt[c]["film"] for c in clips])
    print(f"segments with both dials and parcels: {len(clips)}")
    for f in sorted(set(films)):
        print(f"   {f}: {int((films == f).sum())}")

    X = centre_within(np.array([[float(dt[c][d]) for d in DIALS] for c in clips]), films)
    sd = X.std(axis=0, ddof=1); sd[sd == 0] = 1e-12
    X = X / sd

    parcels = sorted(pv[clips[0]])
    Y = centre_within(np.array([[pv[c][p]["z"] for p in parcels] for c in clips]), films)

    print(f"dials {X.shape[1]}, parcels {Y.shape[1]}, permutations {N_PERM}\n"
          "running…", flush=True)

    obs = np.array([cv_r(X, Y[:, j]) for j in range(Y.shape[1])])
    hits = 0
    # permutation null: shuffle SEGMENT LABELS, per the pre-registration
    best_j = int(np.argmax(obs))
    null = np.empty(N_PERM)
    for i in range(N_PERM):
        perm = RNG.permutation(len(clips))
        null[i] = cv_r(X[perm], Y[:, best_j])
    thresh = float(np.percentile(null, 95))
    hits = int(obs.max() > thresh)

    print("\n" + "=" * 58)
    print("FUTILITY CHECK — verdict only, by design")
    print("=" * 58)
    print(f"  best observed cross-validated r exceeds its own 95th-percentile")
    print(f"  permutation threshold:  {'YES' if hits else 'NO'}")
    print()
    if hits:
        print("  VERDICT: CONTINUE. The pre-registered futility condition is not met.")
    else:
        print("  VERDICT: STOP FOR FUTILITY, per the pre-registration.")
    print()
    print("  No dial or parcel identity is reported. Interim looks are exploratory")
    print("  and may not be reported as findings; the FDR-corrected test runs once,")
    print("  on all 70 segments.")


if __name__ == "__main__":
    main()
