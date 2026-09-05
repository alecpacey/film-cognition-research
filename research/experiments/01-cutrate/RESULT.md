# 01 — Cut rate · RESULT

**Run 2 September 2026 · HF Space `alecnpacey/tribe-probe` · A10G Small · video mode, `audio_only=True`**

## Verdict: PASS on both criteria

**Technique moves the sensor.** Identical footage — every condition contains exactly
the same 30 s of each source scene — and only the number of cuts differs. The
response moved monotonically in 51 parcels.

The control claim survives. Stage 02 is unblocked.

## Criterion 1 — count

**51 of 180 parcels** reach `|r| > 0.9` against `log2(added cuts)`.
Bar was 15; chance expectation with n = 5 is ~7. **Seven times chance.**

## Criterion 2 — anatomy

**3 of 7** dorsal-attention parcels survive (LIPv, PEF, VIP) against 1.98 expected
by base rate. Over-represented, as predicted.

## The strongest responders are not where the literature pointed

| parcel | r | cut01 → cut31 |
|---|---|---|
| **IFJa** | +0.996 | +1.36 · +1.75 · +2.02 · +2.17 · +2.39 |
| **IFSp** | +0.995 | +0.45 · +0.70 · +1.04 · +1.29 · +1.45 |
| **8C** | +0.990 | +0.61 · +0.81 · +0.96 · +1.25 · +1.34 |
| **IFJp** | +0.984 | +0.92 · +1.15 · +1.27 · +1.34 · +1.59 |
| **p9-46v** | +0.986 | +0.05 → +0.74 |
| **45** | +0.985 | −0.40 → +0.16 |
| **8BM** | +0.985 | −0.18 → +0.42 |
| **7AL** | −0.990 | +0.66 → +0.25 |
| **6a** | −0.989 | +1.11 → +0.59 |
| **V3B** | −0.978 | +2.70 → +1.88 |

The top responders — IFJa, IFJp, IFSp, 8C, 45, 44, p9-46v — are **inferior frontal
junction and inferior frontal sulcus**: cognitive control and task-switching cortex,
not the dorsal attention network the literature predicted.

Read plainly, that is coherent. **Every cut is a switch.** IFJ is the region most
associated with updating task set when input changes, so faster cutting means more
switching. And the monotonicity is near-perfect — IFJa rises across all five
conditions without a single reversal.

Meanwhile **V3B falls** (+2.70 → +1.88): shorter shots give less sustained visual
processing per shot.

Hitting a *different* coherent signature is a better outcome than hitting the
predicted one by luck. But it is a post-hoc reading of an unpredicted result, and
should be treated as a hypothesis for stage 02 rather than a finding.

## Also reported

Whole-vector correlation `cut01` vs `cut31` = **+0.8934**. Well below the 0.99
that would have meant the manipulation did nothing, while remaining high — as it
should, since the content is identical by design.

## Caveats

1. **The effective range was 2.1×, not 31×.** The source scenes carry ~22–24 cuts
   of their own, so detected totals ran 25 → 53 rather than 1 → 31. This makes the
   pass **conservative**: the effect appeared despite a compressed manipulation.
2. **One dial, one film, one pair of scenes.** A passing gate says technique *can*
   move the sensor. It says nothing about whether lighting, shot scale or camera
   movement do. That is stage 02.
3. **The IFJ reading is post-hoc.** It was not predicted in the README.
4. **n = 5 conditions.** With five points, `r = 0.9` is p ≈ 0.037; the defence is
   the count (51 ≫ 7) and the anatomical coherence, not any single parcel.
5. Text branch skipped (gated Llama). Video + audio only.

## Cost

5 conditions × ~10 min ≈ 50 min ≈ **$0.85**. Space paused after the run.
