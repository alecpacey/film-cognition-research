# 01 — Cut rate on identical footage · THE GATE

**Written before the run. Criteria are not to be softened afterwards.**

## The question

Does *cinematographic technique* move TRIBE's response, with content held constant?

Run 00 established the sensor discriminates **content**. Every clip there differed
in what was depicted. This is the first test of the actual thesis — that technique
moves the response — and it is the first thing in the project that could kill it.

## Design

Two 60-second scenes already characterised in run 00, chosen because they are the
most orthogonal pair we have (whole-vector r = −0.098):

- **face** — two people talking in close-up, drives the voice chain
- **landscape** — jungle and water, drives the place chain

Intercut them at five rates. Each condition is 60 s and contains **exactly 30 s of
each scene, in order**. Only the number of cuts differs:

| condition | alternations | cuts | segment length |
|---|---|---|---|
| `cut01` | 1 | 1 | 30.0 s |
| `cut03` | 2 | 3 | 15.0 s |
| `cut07` | 4 | 7 | 7.5 s |
| `cut15` | 8 | 15 | 3.75 s |
| `cut31` | 16 | 31 | 1.875 s |

Total content is identical across all five. Colour, luminance, motion, subject
matter, audio — all held. The **only** variable is cut count.

This is the cleanest manipulation available anywhere in the project: no generator,
no prompt adherence, no confound. It is also the strongest — montage context
carries the largest measured effect of any dial in the literature (η²p 0.715).

## Predictions

If cutting has no effect beyond its content, all five conditions should look like
the mean of face and landscape, and differ from one another only by noise.

If cutting has an effect, the literature predicts **dorsal attention** — IPS1, FEF,
LIPv, VIP, V7, PEF, IP0 — should scale with cut rate, along with transient
responses in early visual cortex.

Note the strongest documented cut effect is *hippocampal* (event boundaries), and
the hippocampus is subcortical. Our cortical checkpoint cannot see it. We are
looking for the second-strongest signal.

## Measured, not assumed — the sources carry their own cuts

`cinemetrics.py` on the built conditions detects **25, 27, 31, 36, 53** cuts, not
1, 3, 7, 15, 31. The two source scenes already contain ~22–24 cuts between them,
so the manipulation adds to a roughly constant baseline rather than starting from
zero.

Consequences, both recorded rather than smoothed over:

- **The regressor is the manipulated variable** — added cuts (1, 3, 7, 15, 31) —
  because the inherent baseline is approximately constant across conditions and
  therefore not a confound. Detected totals are reported as a check.
- **The effective range is compressed.** Total cut rate varies about 2.1× across
  conditions, not 31×. This weakens the manipulation, so a null result here is
  *less* conclusive than the design intended: it would mean "cutting did not move
  the sensor over a 2.1× range", not "over a 31× range". A clean negative would
  need source material without inherent cuts.
- Duration is exact (60.03 s) and median luminance identical (24) across all five,
  so neither length nor exposure varies with condition.

## Pass criteria

Correlate each parcel's z-score against `log2(cut count)` across the five conditions.

**PASS** requires both:

1. **Count.** At least **15** of 180 parcels reach `|r| > 0.9`. With n = 5, r = 0.9
   is p ≈ 0.037, so roughly 7 parcels are expected by chance — the bar is twice that.
2. **Anatomy.** The dorsal-attention family (IPS1, FEF, LIPv, VIP, V7, PEF, IP0) is
   over-represented among the survivors relative to its 7/180 base rate.

**FAIL** if fewer than 15 parcels survive, or if the survivors are anatomically
arbitrary — which would indicate noise rather than signal.

**PARTIAL** — count met, anatomy not — means cutting moves *something* other than
what the literature predicts. Informative, and grounds for a redesign rather than
either conclusion.

Also reported, not gating: whole-vector correlation between `cut01` and `cut31`.
If that is above 0.99, the manipulation did nothing at all.

## Why this is a gate and not the index

It tests one dial. It cannot produce the technique→profile crosswalk, which needs
many dials across many scenes — that is stage 02. This exists so that stage 02's
larger spend is not made on a dead hypothesis.

## Cost

5 conditions × ~10 min on an A10G ≈ 50 min ≈ **$0.85**.
