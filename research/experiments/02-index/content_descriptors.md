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

## Results — run once, 7 Oct 2026

Descriptors `content_av.jsonl`, `content_words.jsonl` (244/244 each); analysis
`content_analysis.py` → `content_analysis.json`, `content_analysis.log`. Convergent check: VAD
`speech_prop` and Whisper `words_per_min` correlate at *r* 0.96 (Spearman 0.98) over the 244 —
not independent (Whisper ran behind the same VAD), but it shows the VAD's speech spans contain
words, not music.

### Q0 · Is the flip real? **NOT DEMONSTRATED**

| | *Jungle Book* | *Nothing Sacred* | *Royal Wedding* | cut × film *F* (perm *p*) | NS − JB (95% CI) |
|---|---|---|---|---|---|
| frontal cluster, within-film *r* with cut rate | −0.27 | +0.26 | −0.05 | 1.38 (**0.279**) | +0.53 (−0.14, +1.08) |
| auditory cluster (control) | −0.47 | −0.24 | −0.11 | 0.03 (0.971) | — |

The three films' frontal slopes are more scattered than the auditory ones, but not more than
chance allows. **There is no demonstrated sign flip to explain**: the "flip" is three noisy
estimates around zero, of which two happen to fall on opposite sides of it. By the fixed
reading rule every Q2 result below accounts for a difference not shown to exist.

### Q1–Q2 · Does a descriptor carry it? **DOES NOT CARRY, all three**

| descriptor | *r*(cut, D) JB / NS / RW | partial *r*(frontal, cut \| D) JB / NS / RW | *S* (95% CI) | *r*(frontal, D \| cut) JB / NS / RW | class |
|---|---|---|---|---|---|
| `speech_prop` | −0.42 / −0.28 / +0.18 | −0.20 / +0.38 / −0.14 | −0.09 (−2.17, +1.62) | +0.12 / +0.40 / +0.41 | **DOES NOT CARRY** |
| `sem_change_per_min` | +0.88 / +0.86 / +0.97 | −0.27 / +0.20 / −0.27 | +0.13 (−3.08, +2.63) | +0.16 / −0.07 / +0.27 | **DOES NOT CARRY** |
| `sem_dist_per_cut` *(amendment; RW n = 18)* | +0.46 / +0.45 / +0.65 | −0.25 / +0.31 / −0.03 | −0.06 (−1.91, +2.00) | +0.02 / −0.18 / +0.06 | **DOES NOT CARRY** |
| both primary together | — | −0.27 / +0.30 / −0.12 | −0.07 (−4.33, +3.99) | — | *(no class)* |

Neither speech nor semantic change has a correlation with cut rate that differs in sign between
*Nothing Sacred* and *Jungle Book*, which is what carrying the flip would need. Faster cutting
goes with *less* speech in both, and with cuts that change the picture's meaning *more* in all
three films (`sem_dist_per_cut` +0.45 to +0.65) — the opposite of "fast cutting is small
continuity cuts". The *S* intervals are enormous because the difference they divide by is
itself indistinguishable from zero. Auditory control: its partial *r* with cut rate stays at or
below zero given every descriptor (given speech −0.28 / 0.00 / −0.40; given `sem_dist_per_cut`
−0.38 / −0.27 / −0.26).

### Reading — written after the classes, separately from them

**The question F5 asked dissolves rather than being answered.** The frontal cluster's relation
to cut rate in this corpus is zero within film (pooled *r* −0.02), and its per-film estimates
scatter around zero within what three samples of 23–24 would produce. Together with 03b — which
puts the expected corpus effect at only *r* ≈ +0.05 to +0.20 — the simplest account of the
frontal miss is now an effect expected to be small, not detected, with nothing film-specific
about it. The paper's repeated statement that the frontal sign "flips between films" is
descriptively true and statistically empty, and should be worded as such.

### Secondary and post-hoc — exploratory, uncorrected

Post-hoc means written after the fixed analysis was read (`content_posthoc.py` →
`content_posthoc.json`).

**Speech is a large content dial the index lacks — on the auditory side.** Within film, the
auditory cluster tracks `speech_prop` at *r* +0.78 pooled (partial on cut rate +0.59 / +0.86 /
+0.81 by film, the same sign and size everywhere). Leave-one-out within-film *R*²: the 14 visual
dials alone −0.09 (OLS at *n* = 70 overfits; the registered model was an elastic net, so this
is not a re-run of stage 02), the 14 dials plus speech **+0.54**, and four content descriptors
alone (speech, semantic PC1, PC2, dispersion) **+0.60**. One audio descriptor explains more
within-film auditory variance out of sample than the whole visual dial set. That is unsurprising
for a sensor with an audio branch, and it is a measured fact the paper does not yet contain.

**Part of the corpus's auditory cut-rate signature is speech.** Faster cutting goes with less
dialogue (pooled within-film *r* −0.20), and auditory cortex follows dialogue, so some of the
negative auditory–cut relation is speech: pooled *r* −0.27 marginal, −0.19 given speech. Most
of it survives, consistent with stage 03, where cutting lowered auditory response with no
speech at all (S−). The index's auditory cut-rate coefficient is therefore partly a speech
coefficient; stage 03's causal result is unaffected.

**What the frontal cluster does track is the picture's content, not its cutting.** Given cut
rate, the frontal cluster follows semantic PC2 at +0.55 / +0.55 / +0.34 and PC1 at +0.17 /
+0.60 / +0.52, and falls with semantic dispersion at −0.43 / −0.35 / −0.24 — the same sign in
every film. PC2 is partly faces (within-film *r* with `face_area_frac` +0.40, with
`face_hit_rate` −0.39), PC1 partly colour (`mean_saturation` −0.46); neither is a dial under
another name. Leave-one-out within-film *R*² for the frontal cluster: content descriptors alone
+0.19, the 14 dials −0.15. These columns were not planned tests; they mark where a frontal
dial would have to come from, not what it is.

**Speech may mask a frontal cut effect slightly — direction only.** Partialling speech moves
the frontal cluster's cut-rate *r* towards stage 03's sign in *Nothing Sacred* (+0.26 → +0.38)
and *Jungle Book* (−0.27 → −0.20), and the pooled value from −0.02 to +0.04. IFSp moves most
(*Nothing Sacred* +0.12 → +0.50). Because fast cutting carries less speech and speech raises
these parcels, a positive cut effect would be partly cancelled in cinema. The pooled change is
small and nothing here is tested; it is reported as a direction for paper two's corpus.

### What this changes in `PAPER.md` (for consolidation step 4)

1. Every statement that the frontal relation to cutting "flips sign between films" should read
   that the per-film estimates differ in sign but **do not differ significantly** (*F* 1.38,
   *p* 0.28); the scene-switch and content hypotheses were answers to a difference not shown
   to exist. Occurrences on 7 Oct: abstract ×3 ("flips sign between films"; two in the 03b
   paragraph, "a sign that flips between films"), § 6.8 ×2, § 6.9 ×1, § 9 ×1 — `grep -n "flips" PAPER.md`.
2. The abstract's account of stage 02's miss — cutting measured "where it co-occurs with
   dialogue, close-ups and interiors" — is contradicted for dialogue as well as for close-ups:
   faster cutting goes with *less* speech (−0.20) and smaller faces (§6.5).
3. Speech belongs in §8 (a missing content dial, with the auditory *R*² figures) and in future
   work, and qualifies "the index's cut-rate column should be read as the auditory half of the
   effect": partly cutting, partly speech.

### Limitations

Three films, 23–24 segments each: a within-film *r* below ≈ 0.4 is inside noise, and Q0 has
little power to detect a real heterogeneity of modest size — "not demonstrated" is not "absent".
One VAD and one CLIP model; CLIP is trained on photographs and captions, not cinema. The
semantic scene-change measure was validated on generated footage, where live-action cuts fall
between the two calibration groups. `sem_change_per_min` was nearly collinear with cut rate by
construction (see the amendment). The text branch is off throughout, so the sensor never saw
words as text, only heard them.
