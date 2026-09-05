# 02 — The observational index

**Written before the run. Criteria are not to be softened afterwards.**

This is the stage that produces the actual deliverable: **a crosswalk from
cinematographic technique to cortical response profile.** Stage 01 proved one dial
can move the sensor. This measures how *all* the dials relate to it, across real
cinema.

## Design

| | |
|---|---|
| **Sources** | 2–3 public-domain features, deliberately different in style |
| **Segments** | 60 s, non-overlapping, sampled across each film |
| **Dials** | measured by `cinemetrics.py` — free, **~28 s** per 60 s segment at 720p — measured, not the ~2 s previously assumed |
| **Response** | 180-parcel vector per segment from TRIBE |
| **Model** | elastic net per parcel, regressing parcel z on dials |
| **Null** | permutation over segment labels |

### Why multiple films

Directors covary their dials on purpose — close-ups arrive with shallow focus and
quieter sound; fast cutting arrives with camera movement and high contrast.
Kauttonen 2015 hit exactly this with 37 cinematic features and needed elastic net
to cope. **Varying the director is the cheapest way to break that covariance
without a lab.**

**Corpus resolved — see `CORPUS.md`.** *His Girl Friday* was rejected for being
black and white, which would have made saturation a perfect proxy for film identity.
The animated-Technicolor assumption that replaced it has also been dropped: its
premise, that public-domain animated colour titles are more available than
live-action ones, is false. Three public-domain **live-action Technicolor** features:

| Film | Buys us |
|---|---|
| *Nothing Sacred* (1937) | dense overlapping dialogue, interiors, fast cutting — the colour replacement for *His Girl Friday* |
| *Jungle Book* (1942) | landscape, exteriors, slow cutting, wide shots |
| *Royal Wedding* (1951) | sustained camera movement, high-key luminance, moving long takes |

Segments are **fixed 60 s, non-overlapping**, and every print is normalised to a
common resolution and codec before dials are measured — resolution otherwise leaks
into the depth-of-field proxy. Dials and parcels are centred **within film**.

### On the null

Stage 02 regresses parcel values on dial values **across segments**. That is not a
map-to-map comparison, so the correct null is **permutation of segment labels**, not
a spin test. Spin tests become necessary only when comparing our resulting
technique-maps against external maps such as Neurosynth terms — that is stage 03+.
(The roadmap previously said spin test here; that was wrong.)

## Pass criteria

For each dial, fit a cross-validated elastic net predicting each parcel's z from
the dial set, and compare against 1,000 label permutations.

**PASS** requires:

1. **At least 3 of the measured dials** have ≥1 parcel whose cross-validated
   predictive `r` exceeds the 95th percentile of its permutation null, after
   FDR correction across 180 parcels.
2. **Cut rate replicates.** The inferior-frontal cluster from stage 01 (IFJa, IFJp,
   IFSp, 8C) should associate with cut rate here too. If a controlled result does
   not reappear observationally, one of the two is wrong and that must be resolved
   before anything is built on it.

**FAIL** if fewer than 3 dials survive, or if cut rate fails to replicate.

**PARTIAL** — dials survive but cut rate does not replicate — means the
observational and controlled tracks disagree, which is itself the most important
possible finding and would redirect the project.

## Effect size, sample size, and what counts as testable

**Written before any dial was measured and before any segment was scored.**

### The smallest effect worth calling a finding

Lakens' rule is that a smallest effect size of interest must be *justified*, not
merely stated. Ours is justified by the measurement chain, because our parcel
values are not brain data — they are TRIBE's predictions of brain data, and the
link from those predictions to real cortex is measured and published.

From the Algonauts 2025 results, TRIBE achieves mean Pearson **r = 0.3195**
in-distribution (Friends s7) and **r = 0.2146 out-of-distribution**; normalised
against the noise ceiling it explains 54% of explainable variance. **Our corpus is
out of distribution** — 1937–1951 Technicolor features are not *Friends*, and are
arguably further out than the challenge's own OOD films, so 0.2146 is an optimistic
upper bound for our case.

That gives a bottleneck. If a dial correlates with a TRIBE parcel at `r_DP`, and
that parcel tracks real BOLD at `r_PY`, then a dial's implied association with real
cortex is roughly `r_DP × r_PY`. To imply even a conventionally small real effect
of r = 0.10:

| via | r_PY | required dial→parcel r |
|---|---|---|
| raw out-of-distribution accuracy | 0.2146 | **0.47** |
| noise-ceiling-normalised accuracy | 0.54 | 0.19 |

**SESOI is set at r ≥ 0.5**, from the conservative row rounded up. The normalised
row is the more generous reading and is recorded here so the choice is visible
rather than buried: it would put the SESOI near 0.19 and demand ~200 segments.
We take the conservative reading because the raw figure is what governs a claim
about actual cortex, and because our material is further out of distribution than
the figure was measured on.

Note what this argues: a *higher* SESOI, and therefore a **cheaper** study. A dial
that only reaches r = 0.3 in a measurement with no noise in it would be worth
almost nothing after passing through a 0.21 bottleneck.

### Sample size

Power for a Pearson r at α = .05 two-tailed, with 3 df lost to within-film centring:

| n segments | r=0.3 | r=0.4 | r=0.5 | r=0.6 | min r at 80% power |
|---|---|---|---|---|---|
| 20 | 0.21 | 0.35 | 0.54 | 0.74 | 0.63 |
| 40 | 0.44 | 0.70 | 0.89 | 0.98 | 0.45 |
| 60 | 0.62 | 0.88 | 0.98 | 1.00 | 0.36 |
| **70** | 0.68 | 0.92 | **0.99** | 1.00 | **0.33** |
| 100 | 0.85 | 0.98 | 1.00 | 1.00 | 0.28 |

**Target: 70 segments** (jungle_book 24, nothing_sacred 23, royal_wedding 23).

Originally set at 60. Raised to 70 once the dials were measured: at 60 the two
cut-rate dials came in at 0.79 and 0.80 power — *below the floor* — because a third
of cut rate's variance is between-film and within-film centring removes it. Cut rate
is the dial pass criterion 2 requires to replicate, so at 60 that check could not
have failed informatively. At 70 **all 14 dials clear the floor**. The evidence is
in `DIALS.md`; the cost of the fix was $1.70.

SESOI of 0.5 would be met by 40, which has 89% power there. The headroom above that
is deliberate, for two reasons that would otherwise bite silently:

1. The mediation estimate above is a first-order approximation. If the true
   bottleneck is kinder than 0.2146, the SESOI belongs lower, and 60 segments
   still has 80% power down to r = 0.36.
2. **The pass criteria's quantity is not a marginal correlation.** It is a
   cross-validated predictive `r` for a parcel from the whole dial set — a
   multivariate quantity whose null is established by permutation, not by the
   table above. The power table is therefore indicative, not exact, and the
   headroom absorbs that imprecision.

Cost: 70 segments ≈ $11.90, ~11.7 h wall-clock, run in resumable batches of 10.

### No dial is dropped. Dials are classified.

The earlier plan was to drop dials that vary too little to be tested, before
spending GPU on them. **That was wrong on its own terms:** GPU cost is per
*segment*, and `cinemetrics.py` returns every dial in one pass whatever we intend
to do with them, so dropping a dial saves no GPU and no measurement time either. It would also have created a reporting error this
stage explicitly forbids — a dropped dial and a tested-null dial become
indistinguishable, when *Reporting the nulls* below requires that a dial which does
not move the sensor be reported as a finding. **"Did not move the sensor" and
"never varied enough to test" are different results and must not be merged.**

So every dial is measured, entered in the model, and reported, each carrying a
pre-registered label derived from its realised range:

- **Tested** — the dial's realised within-film range gives ≥ 80% power at the
  SESOI. A null here is a real null and is reported as one.
- **Underpowered** — realised range is too compressed to detect the SESOI. A null
  here is *uninformative* and must be reported as untested, never as evidence of
  absence.

The threshold is computed, not chosen by eye. Restriction of range attenuates a
true r = 0.5 as follows, so the label follows directly from measured range:

| range retained | a true r=0.5 is observed as |
|---|---|
| 100% | 0.50 |
| 70% | 0.37 |
| 50% | 0.28 |
| 30% | 0.17 |

**Interdependence between dials** is reported as a pre-registered diagnostic — the
dial correlation matrix and its condition number — not modelled. Interaction terms
are excluded from the primary model: with 6 dials, all pairwise interactions is 21
terms at n = 60, the interactions are more collinear than the main effects, and
adding them after seeing data is the forking-paths problem the no-peeking rule
exists to prevent. **Separating covarying dials is what stage 03 is for**;
observational data structurally cannot do it.

### Segment selection

All 244 available segments are cut and dialled — both free. The 60 scored on GPU
are chosen by **stratified sampling across each dial's range**, not at random and
not at the extremes.

This is a design choice on *predictors*, made before any parcel value exists.
Selecting on outcomes would be p-hacking; selecting on stimulus properties is
ordinary experimental design. The real caveat is different and is stated here in
advance: deliberately spreading a dial inflates its variance relative to a random
sample, so estimates are **design-conditional** and must not be read as "the effect
in typical cinema". Stratifying across deciles rather than taking extreme groups
keeps that mild.

## Reporting the nulls

Dials with **no** reliable parcel association are as valuable as those with one,
and must be reported with equal prominence. A dial that does not move the sensor is
a dial you cannot direct with, and knowing that early is worth more than a
plausible story about it.

## Cost and wall-clock

| segments | GPU cost | wall-clock |
|---|---|---|
| 40 (20/film) | ~$6.80 | ~6.7 h |
| 60 (30/film) | ~$10 | ~10 h |
| 100 | ~$17 | ~17 h |

**Wall-clock is the real constraint, not money.** At ~10 min per 60 s segment on an
A10G, 60 segments is a working day of continuous GPU. Options: batch across several
runs, or move to A100-large ($2.50/hr) which should cut wall-clock roughly
proportionally for similar total cost.

Start at **40 segments** — enough to detect a strong association, cheap enough to
absorb if the pipeline needs a fix.

### Not taken: local Apple-silicon scoring

`src/tribescore/mps.py` in the Space repo is explicitly built for this — "Local
Apple-silicon (MPS) enablement, applied OFF the Space". It monkeypatches
neuralset's device resolution so V-JEPA 2, Wav2Vec2-BERT and the brain head land
on Metal, because the shipped `config.yaml` hardcodes `device: cuda` and
`HuggingFaceMixin` only re-resolves when the value is the literal `"auto"`.

Scoring locally would make the remaining segments **free**. It was considered on
4 Sep 2026 and **not taken** — the decision was to stay on paid HF hardware and
top up. Recorded because the option remains valid if budget becomes the binding
constraint.

**If it is ever taken, one test comes first.** Mixing CUDA-scored and MPS-scored
clips in one dataset is the same silent confound as mixing two scoring
configurations, and would land numerical differences in the data as if they were
signal. So: rescore an *already-scored* clip locally — `jungle_book_000` — and
compare its 180-parcel vector against the Space's. Tight agreement means mixing is
safe; disagreement means all 70 must be scored locally, which is still free.

Unknowns, stated as unknowns: MPS speed is untested here (plausibly 2–5× slower
than an A10G, so 20–50 h for the remaining set), and nothing in `LOG.md` records a
local run — every entry to date is on the Space.

## Staging and checkpointing

Runs in batches, resumable. Driven by `run_batch.py`.

| batch | segments | purpose | cost |
|---|---|---|---|
| **0 · pipeline** | 4 | Prove the pipeline end-to-end on new material. **The run is not a look at the result** — see below. | ~$0.70 |
| **1–4 · collection** | 10 each | Accumulate the dataset | ~$1.70 each |

Each clip is already a checkpoint: the Space prints its 180 parcel values to stdout
the moment it finishes, and logs survive a crash. A batch that dies half-way still
banks its completed clips. Resume is by omission — `run_batch.py` uploads only
segments with no saved vector, so nothing is ever scored twice.

```sh
python run_batch.py --plan       # what would run, no cost
python run_batch.py --batch 10   # upload 10 unscored segments, start
python run_batch.py --harvest    # fetch, save, verify, pause. Safe any time.
```

### Does batch 0 count toward n?

"Not for analysis" was ambiguous and is resolved here, in writing, rather than by
judgement after the fact.

**Batch-0 segments count toward the 70, provided the batch required no change to
the scoring path.** They are drawn from the same pre-registered selection, scored
by the same pipeline at the same settings; nothing about their provenance differs
from batch 1's. Discarding them would waste the spend and four segments of power
for no methodological gain.

The phrase means **the batch-0 run is not a look at the answer** — its purpose is
to prove the pipeline, and no dial→parcel relationship may be inspected from it.

**The conditional is load-bearing.** If batch 0 had revealed a problem requiring a
change to how segments are scored — different flags, a different `mode`, a patched
`app.py` — then its clips came from a different pipeline than the rest and **must be
discarded and rescored**. Mixing two scoring configurations in one dataset is a
silent confound. Batch 0 on 4 Sep 2026 required no such change, so its four clips
stand.

*(Recorded for completeness: the batch-0 health check inspected parcel counts, NaN,
z-magnitudes, and the pairwise whole-vector correlation between the four clips —
that last to confirm the sensor discriminates at all rather than returning one
vector for everything. None of these is a dial→parcel relationship, so none is an
outcome peek.)*

### What the between-batch check is for — and what it is not

`--harvest` verifies **pipeline health only**: 180 parcels per clip, no NaN, no
implausible z-values, filenames aligning between the dial table and the parcel table.

**It is not a look at the result.** Peeking at an accumulating dataset and stopping
when it looks good inflates false positives, and this project would be worthless if
its headline finding were an artefact of when we chose to stop. So:

- The statistical test in *Pass criteria* is run **once, on the complete set**.
- Interim looks are exploratory, and anything seen in one may not be reported as a
  finding.
- **One pre-specified exception**, which is a resource decision rather than a test.
  It has been **restated**, because the original was arithmetically inert: *"if
  after 20 segments no dial reaches |r| > 0.3, stop"* fires about one time in five
  under pure noise — at n = 20 the null probability of a single dial exceeding
  |r| = 0.3 is 0.247, and across 6 dials the chance at least one does so is 0.82.
  A rule that almost never triggers is not a stopping rule.

  **Restated:** at 30 segments, run the permutation null on the dials measured so
  far. If no dial has any parcel whose cross-validated `r` exceeds the 95th
  percentile of its own permutation distribution *uncorrected*, stop for futility.
  That is a real threshold with a real false-trigger rate, it uses the same
  machinery as the final test, and being uncorrected it is deliberately lenient —
  it stops only a study showing nothing at all. The full FDR-corrected test still
  runs **once**, on the complete set.

## Prerequisites

- [ ] Source the three films at the identifiers listed in `CORPUS.md`
- [ ] Verify each print is actually in colour, and normalise the encode
- [ ] Segment all three, verify duration and that segments do not straddle reels
- [ ] `cinemetrics.py` over all segments → dial table
- [x] Classify each dial tested/underpowered from its realised range — **no dial
      is dropped**; 14/14 TESTED at n=70, see `DIALS.md`
- [x] Report the dial correlation matrix and condition number — 58.8, see `DIALS.md`
- [x] Select 70 segments by stratified sampling across dial ranges → `selection.json`
- [ ] Batch upload, single run, foreground log collection
