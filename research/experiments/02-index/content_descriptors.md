# Content descriptors and the frontal sign flip — consolidation step 3a (review F5)

**Exploratory. Not registered.** The registered stage-02 verdict (PARTIAL) is unaffected by
anything here. This file was written and committed **before any descriptor was computed**; the
plan below is fixed, and results are appended under it, separately.

## The question

Within film, the frontal cluster's relation to cut rate differs in sign between films:
IFJa *r* −0.25 in *Jungle Book* (*n* 24, *p* 0.24), +0.32 in *Nothing Sacred* (*n* 23,
*p* 0.14), −0.11 in *Royal Wedding*; IFSp and 8C the same pattern (`per_film.json`). The
auditory quartet is negative in all three. The dial set has no audio or semantic dial, so the
flip may be carried by content the dials do not measure. F5 names two candidates: **how much
speech** a segment holds, and **how much the scene's meaning changes** at its cuts. If, in one
film, fast cutting goes with dialogue and in another with wordless action, a frontal response to
either would appear as opposite-signed cut-rate slopes.

Note before anything is computed: neither film's frontal correlation is significant on its own,
so **whether there is a flip to explain is itself the first question (Q0)**.

## Descriptors — computed on all 244 segments, without reading any parcel data

Primary (two, fixed):

- **`speech_prop`** — fraction of the segment's duration inside speech spans from Silero VAD
  (the ONNX model bundled with `faster-whisper`), threshold 0.5, minimum silence 500 ms,
  speech padding 100 ms.
- **`sem_change_per_min`** — for every cut already detected in `scene_switches_corpus.jsonl`
  (cinemetrics detector, unchanged), the CLIP ViT-B/32 cosine distance between the frames
  12 before and 12 after the cut frame (≈ 0.5 s, clear of the transition); summed over cuts,
  per minute. Continuous: no threshold to choose. It is cut count weighted by how much the
  *meaning* of the picture changes across each cut — the semantic proxy `scene_switches.md`
  named.

Secondary (reported, labelled, no inference drawn from them alone):

- `words_per_min` — word count from Whisper (`faster-whisper` `small`, int8, English, VAD on).
- `sem_dispersion` — mean CLIP cosine distance of frames sampled at 0.5 Hz to the segment's
  mean embedding: how much the picture's meaning moves within the minute, cuts or not.
- `sem_pc1..3` — first three principal components of the segment-mean CLIP embedding, PCA
  fitted on the 244 segments (no brain data involved).

## Outcomes

- **Frontal cluster** = mean of IFJa, IFJp, IFSp, 8C (`z` values), as in 03b. Per-parcel
  results reported alongside.
- **Control: auditory cluster** = mean of A1, A4, A5, MBelt, whose cut-rate sign does not flip.
  A descriptor that "explains" the frontal flip should leave the auditory relation intact.

## Analysis — fixed

All on the 70 scored segments, within film (each film's means removed).

**Q0 · Is the flip real?** OLS: frontal ~ film + cut + cut × film; the statistic is the *F* on
the two interaction df, its *p* by 10,000 permutations of cut rate within film (seed 0).
Labels: **RELIABLE** *p* ≤ 0.05 · **MARGINAL** 0.05 < *p* ≤ 0.20 · **NOT DEMONSTRATED**
*p* > 0.20. The named contrast F5 asks about, *Nothing Sacred* − *Jungle Book* within-film *r*,
is reported with a bootstrap 95% CI (2,000 resamples within film, seed 0).

**Q1 · Confound structure.** Per film, *r*(cut rate, D) for each primary descriptor D. A
descriptor can carry the flip only if this sign differs between *Nothing Sacred* and *Jungle
Book*, or the films differ greatly in its size.

**Q2 · Does D carry the flip?** Per film, the partial *r*(frontal, cut | D). Shrinkage
*S* = 1 − Δ′/Δ, where Δ is the *Nothing Sacred* − *Jungle Book* difference in marginal *r* and
Δ′ the same difference in partial *r*; bootstrap 95% CI as in Q0. And per film, the partial
*r*(frontal, D | cut). Classes, per primary descriptor:

| class | rule |
|---|---|
| **CARRIES** | *S* ≥ 0.50, its CI lower bound > 0, **and** *r*(frontal, D \| cut) the same sign in all three films |
| **DOES NOT CARRY** | *S* < 0.25 |
| **PARTIAL** | otherwise |

Then both primary descriptors together, reported the same way without a class. The auditory
cluster is run through Q2 as the control.

**Fixed reading rules.** If Q0 is NOT DEMONSTRATED, every Q2 result is reported as accounting
for a difference not shown to exist, and a CARRIES is weak evidence at most. Two primary
results (two descriptors × frontal cluster); per-parcel and secondary results are exploratory
and uncorrected. Effect sizes lead; *n* is 23–24 per film, so any per-film *r* below ≈ 0.4 is
inside noise.

**Validation, before the corpus analysis is read.** `sem_change_per_min` must distinguish
cuts that change scene from cuts that do not. Where the 03b clips are available locally, the
CLIP distance at REF's joins (scene change) must exceed that at B's and C's joins (same scene)
for every ladder level; if it does not, the descriptor is reported as failed and Q1–Q2 for it
are not interpreted.

## Amendment — 7 Oct, after the descriptors were computed, before any parcel data was read

A descriptor-only check (no brain data) found that **`sem_change_per_min` correlates with cut
rate at *r* = 0.94** across the 244 segments. Built as a sum over cuts, it is close to a copy of
the variable it was meant to explain: it cannot carry a sign flip (that needs its correlation
with cut rate to differ in sign between films) and partialling it out leaves little cut-rate
variance, so its *S* will be unstable. This is a flaw in the plan, not in the data. It is
**run as fixed and reported, with this caveat attached.**

Added, as a third descriptor run through Q1–Q2 with the same class rules but labelled as an
amendment: **`sem_dist_per_cut`** — the mean CLIP distance across a segment's cuts, i.e. how much
the meaning of the picture changes at a *typical* cut, independent of how many cuts there are.
This is the quantity F5 was reaching for: in one film fast cutting may mean small continuity
cuts, in another large scene jumps. Undefined for segments with no cuts; the five such scored
segments (all *Royal Wedding*) are dropped for this descriptor only, leaving *Royal Wedding*
*n* = 18 and the *Nothing Sacred* / *Jungle Book* contrast untouched.

Two properties of the method found by the synthetic self-test (speech planted to carry the
flip entirely, a pure-noise semantic descriptor alongside): the planted case scores *S* +0.67
(CI 0.41–1.00, CARRIES) rather than ≈ 1, because partial correlations under near-collinearity
retain residual structure — **the 0.50 bar is conservative**; and the noise case scores
*S* 0.00 (DOES NOT CARRY). The auditory cluster has no flip, so its *S* divides by ≈ 0 and is
meaningless; **the auditory control is read from its partial *r*s staying negative, not from
*S*.**

Validation (`content_validation.json`): **PASS.** CLIP distance across 03b's scene-change joins
(REF) 0.42–0.49 against 0.02–0.07 across same-scene joins (B, C) at every level. The stricter
check (every REF join above every B/C join) fails at cut31 on one join of 0.006, attributable
to joins being located by formula on clips that run slightly short; the corpus uses detected
cut frames. Live-action cuts sit between the two calibration groups (median 0.229, 10th–90th
percentile 0.12–0.37), so the continuous measure is the right form and no threshold is used.

## Results

*Not yet computed.*
