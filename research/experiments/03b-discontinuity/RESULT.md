# 03b — Result

**Verdict: GRADED**, against `README.md` as fixed in commit `221faad` before any clip was built.
Run 20–25 September 2026 in three Space sessions. Data `parcel_vectors.json` (20 clips × 180
parcels) and `timelines.json` (20 × 60 × 180); evaluator `evaluate_03b.py` (committed before any
result existed, self-tested on the frozen calibration), full output `evaluation.json`. Preconditions
in `CLIPS.md` / `joins.json`. Audio identical in all twenty clips (one decoded MD5).

**Identity test: PASS.** The timeline-saving app reproduced stage 03's S− values exactly (max raw
|Δ| 0.0e+00); each parcel's saved 60-point timeline averages to its raw value to 4.3e-08.
Every result below is therefore on the same footing as stages 01–03.

## Against the criteria

Frontal ratio ρ_F = ladder's mean frontal-cluster slope (IFJa · IFJp · IFSp · 8C on ln constructed
cuts) ÷ REF's +0.251; *p* one-sided over the 120 level orderings (floor 0.008). REPRODUCES: ρ_F ≥ 0.50
and *p* ≤ 0.05; ABSENT: ρ_F ≤ 0.25; else PARTIAL.

| ladder | ρ_F | *p* | class | ρ_A (*p*) | whole-map gain (*p*) | *r* with REF mode | PR across levels |
|---|---|---|---|---|---|---|---|
| **REF** · hard cut + scene change (stage 03 S−, rescored) | +1.00 | 0.017 | **REPRODUCES** | +1.00 (0.008) | +1.00 (0.008) | +1.00 | 1.20 |
| **B** · hard cut, same scene — face | +0.44 | 0.008 | **PARTIAL** | +0.62 (0.008) | +0.67 (0.008) | +0.86 | 1.05 |
| **C** · hard cut, same scene — landscape | +0.18 | 0.017 | **ABSENT** | +0.38 (0.008) | +0.47 (0.008) | +0.73 | 1.03 |
| **D** · scene change, no hard cut — 0.5 s dissolves | +0.48 | 0.042 | **PARTIAL** | +0.17 (0.075) | +0.50 (0.008) | +0.62 | 1.25 |

Per-parcel frontal slopes: REF IFJa +0.29 · IFJp +0.18 · IFSp +0.25 · 8C +0.28 · B IFJa +0.14 · IFJp +0.13 · IFSp +0.07 · 8C +0.10 · C IFJa +0.06 · IFJp +0.06 · IFSp +0.02 · 8C +0.05 · D IFJa +0.18 · IFJp +0.13 · IFSp +0.08 · 8C +0.09.

Same-scene (B and C jointly): one PARTIAL, one ABSENT → **PARTIAL**. Dissolve: PARTIAL. By the
table, **GRADED — no categorical claim; ratios reported as measured.**

## Reading — written after the verdict, separately from it

**Neither a pure cut detector nor a pure switch detector.** A hard cut with no change of scene
gives 44% of the frontal effect in the face scene and 18% in the landscape; a change of scene
with no hard cut gives 48%. The two contributions are close to additive: B + D ≈ 0.92 of REF,
C + D ≈ 0.66. Every ladder's whole-map response pattern resembles REF's (*r* +0.62 to +0.86, all
*p* = 0.008), so what varies across ladders is the size of one response, not its shape.

**The two signatures of cutting come apart.** The auditory decrease follows the hard
discontinuity: 62% and 38% for same-scene cuts, and only 17% (*p* 0.075) under dissolves. The
frontal increase does not need the discontinuity: dissolves carry 48% of it. Stage 03 and the
16 Sep review read "frontal up, auditory down" as one mode with two signs (participation ratio
≈ 1.2); across the four ladders here they dissociate. **The auditory signature is a
discontinuity response; the frontal one is partly that and partly a response to the scene
changing.**

**The same-scene result is scene-dependent, and not because of the size of the jump.** B and C
have near-identical discontinuity magnitudes (peak frame Δ 40 vs 39; histogram distance 0.16 vs
0.23) yet ρ_F 0.44 vs 0.18. Cutting inside a scene of two people at a table moves the frontal
cluster more than cutting inside a landscape. What is interrupted matters, not only that
something is.

**On review comment M5 (encoder artefact).** The pure form — "the head maps temporal
discontinuity to frontal cortex, nothing more" — is weakened: half the frontal effect arrives
with no discontinuity at all, while the auditory half is what tracks discontinuity. The
alternative is not excluded in a broader form (a response to any large visual change, gradual or
abrupt), which this design cannot separate from "change of scene" (README § Limits).

**On the frontal miss in real cinema.** Cinema's within-scene hard cuts should, by B and C,
produce 0.2–0.45 of REF's frontal slope per unit ln cuts. `frontal_miss.md` showed REF's full
slope would have been detectable in the corpus at *r* ≈ +0.3–0.45; at 0.2–0.45 of it the
expected corpus *r* is ≈ +0.08–0.20 — small, and within what a sign that flips between films
could hide. **The miss is smaller than it looked, and no longer needs a special explanation
beyond corpus heterogeneity; it is not resolved.**

## Reported, not gating — cut-locked response (exploratory, `cut_locked.py`)

Timelines projected on the unit REF mode, epoched −3 … +12 s around the 10 joins of levels 1,
3 and 7 per ladder. No clean join-locked transient emerges: all four ladders show a small rise into
the join, a dip near +3 s and a larger one near +10 s, of similar shape whatever the join type
(REF peak -1.56, B -4.40, C -3.00, D -2.10, all at +10 to +11 s). A shape that recurs at fixed lags across
ladders with different join types is more likely a property of the model's windowing than of the
join; with ten epochs per ladder this is descriptive only. The effect the slopes measure is in the
**sustained level**: mean projection per level rises with cut count in REF (-1.84 → -1.34 → -0.76 → +0.88 → +4.07) and B (+0.95 → +1.28 → +2.09 → +4.23 → +4.66),
weakly in C (-2.45 → -2.41 → -1.50 → -0.42 → +0.36) and D (-1.70 → -1.26 → -0.59 → +0.02 → +0.22). The saved timelines exist for a better-designed
analysis; this one does not license a claim.

## Limitations

- Five levels, *p*-floor 0.008; one generator; two scenes; text branch off; everything is about TRIBE.
- Scene change and large gradual visual change are not separated (README § Limits); a dissolve is
  also 0.5 s of blended imagery, 26% of the clip at 31 switches.
- B and C are single-scene clips, REF and D two-scene: slopes are within-ladder, baselines differ.
- Clip length shrinks with cut count in REF, B, C (59.9 → 58.5–58.9 s), a property of
  `build_conditions.py` inherited from stages 01 and 03; D is 60.00 s throughout.
- B carries the face base's one generator seam at every level (constant, cannot affect a slope).
- The whole-map gain *p*-values all sit at the floor, so the gain ordering (B 0.67 > D 0.50 > C 0.47) is not resolved statistically.

## Spend and missteps, recorded

Three sessions. **Session 1 (20–21 Sep) overspent**: 20 clips staged as one batch against the
project's documented safe size of 8, the Space stalled after clip 10 while still billing, and the
budget guard lived in a laptop watcher that slept — ≈ 5.5–8.2 h, ≈ $5.50–8.20 against a $3.60
estimate (exact figure on the HF billing page only). Fixed for sessions 2 and 3 by a
**server-side** guard in the app (self-pause on completion, 80-min watchdog), a 30-min Space
sleep timeout, batches of 5, and a stall-detecting watcher. **Session 2 (D, 21 Sep): 63 min,
Space paused itself. Session 3 (C, 21 Sep): 62 min, Space paused itself.** ≈ $2.10 for the two.
Original app restored byte-identically and sleep timeout reset to 7200 s on 25 Sep. The optional
text-branch session (README) has **not** been run.
