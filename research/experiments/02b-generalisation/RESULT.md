# 02b — Generalisation: does the fitted index predict generated clips?

**Exploratory. n = 3. Not pre-registered; counts toward no pass criterion.** Run 13 September
2026, script `generalise.py`, output `result.json`. Per `ROADMAP.md` § 02b: measure dials on
out-of-medium segments, predict their parcel vectors from the **already-fitted** stage-02 index
(no refitting), compare predicted with actual.

## Method

The three 01b clips (MiniMax H3 Max, 60 s, 768P) supply both sides: 14 dials from
`cinemetrics.py` (same mapping as stage 02, incl. `shot_scale.hit_rate`), 180-parcel vectors
from the same Space and settings as stage 02. Preprocessing is the index's own: dials centred
within the clip set and divided by stage 02's within-film SD (`analyse.py` D3); parcels centred
within the clip set. Prediction Ŷ = X·Bᵀ with B the 180 × 14 full-data coefficient matrix.
B was fitted on 70 real-film segments and has never seen these clips — this is out-of-sample
and out-of-medium.

## Result — the index predicts the generated clips

| | landscape | crowd | face |
|---|---|---|---|
| profile *r*, predicted vs actual, 180 parcels | 0.41 | **0.90** | **0.89** |
| same, 101 surviving parcels | 0.48 | 0.92 | 0.92 |

Face − landscape contrast, predicted vs actual: ***r* = +0.77** (survivors +0.84), against a
parcel-permutation null with 95th percentile 0.15.

**Which clip is which is recoverable from dials alone.** Across all six assignments of the three
dial vectors to the three response vectors, the true assignment gives the highest mean profile
*r* (0.73); the runner-up swaps crowd and landscape (0.62, both wide shots); every assignment
that misplaces the face clip is negative.

## Reading, and its limits

The crosswalk fitted on 1937–1951 Technicolor predicts a 2026 generator's output at *r* ≈ 0.9 on
two of three clips. That is the strongest evidence yet that the index is a property of how this
sensor reads technique, not an artefact of one corpus — and it is what stage 03's plan to
regress on measured technique in generated clips requires.

The landscape clip is the weak case (0.41), consistent with 01b, where it also transferred
least faithfully (+0.41 vs its run-00 counterpart). One dial sits **outside stage 02's range** —
`contrast_p5_p95` — so the prediction extrapolates on it. The 01b confound is inherited: the
generator's own cutting covaries with content (7 / 10 / 15 cuts per min), so part of what is
predicted here is cutting, not only the intended content contrast. n = 3 permits none of this
to be a finding; it is a reason to expect stage 03 to work, and a warning about landscapes.

## Spend

$0. No generation, no GPU.
