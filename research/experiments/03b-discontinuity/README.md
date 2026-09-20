# 03b — Discontinuity or switch: what does the sensor's cut response respond to?

**Written before any clip is built or scored. Criteria are not to be softened afterwards.**
Drafted 20 September 2026 from stage 03, `02-index/frontal_miss.md`, `02-index/scene_switches.md`
and review comment M5. The reference values below were frozen from committed stage-03 data by
`make_reference.py` into `reference_mode.json` before this file was committed. The commit that
adds this file is the timestamp; nothing here has been run.

## The question

Stage 03 showed that intercutting two unrelated scenes drives inferior-frontal cortex up and
auditory cortex down, with content and audio held fixed. In that ladder three things change
together at every cut: **a hard temporal discontinuity** in the picture, **a change of scene**,
and a large change in the pixels. The paper reads the frontal response as cognitive-control
cortex answering a switch. The cheaper reading, never yet tested, is that the video encoder
responds to temporal discontinuity and the encoding head maps that to frontal cortex — that the
sensor has a **cut detector**. The corpus result bears on this and cuts the other way: real
cinema is full of hard cuts and shows no frontal effect.

This stage pulls the first two apart. It cannot fully separate "scene change" from "large
pixel change"; § Limits says what it does about that.

## Design — three new ladders against one existing reference

All ladders use stage 03's bases (`face_close.mp4`, `landscape.mp4`, single takes, 0 cuts
measured), the same five levels (**1, 3, 7, 15, 31** constructed cuts), the same 60 s length,
and **the landscape base's continuous ambient audio over the whole clip**, as in stage 03's S−
arm — no speech, no audio discontinuity at any cut, identical sound in every clip of every
ladder. Scoring path unchanged: `audio_only=True`, whole-clip mean per parcel, within-clip z.

| ladder | picture at each cut | hard cut | scene change |
|---|---|---|---|
| **REF** · stage 03 S− (already scored) | face ↔ landscape | yes | yes |
| **B** · same-scene, face | `face_close` ↔ `face_close` mirrored and shifted 30 s | yes | **no** |
| **C** · same-scene, landscape | `landscape` ↔ `landscape` mirrored and shifted 30 s | yes | **no** |
| **D** · dissolve switch | face ↔ landscape, each join a 0.5 s cross-dissolve | **no** | yes |

**B and C** are built with `01-cutrate/build_conditions.py` unchanged, source A the base and
source B the same base horizontally mirrored and offset by 30 s (wrapping), so each clip holds
the whole 60 s of one scene, half of it mirrored. Mirroring makes the jump large in pixels —
the two people swap sides — while scene, palette, lighting and location stay the same. Two
scenes, so that a result is not a property of one.

**D** uses the REF segment layout with every hard join replaced by a 0.5 s cross-dissolve,
segments extended 0.25 s each side so the clip stays 60 s. At 31 switches about a quarter of
the clip is in blend; stated, not corrected.

**Measured, not assumed, before scoring** (`cinemetrics.py` and `02-index/scene_switches.py`,
recorded in `CLIPS.md`): constructed cut count per clip; detected cuts; mean frame delta and
histogram distance at each join. Expected: B and C detected ≈ constructed with histogram
distance near zero; D detected ≤ 10% of constructed. If D's dissolves are detected as cuts at
more than 25% of joins, the dissolve is lengthened to 1.0 s once and re-measured; if it still
fails, D is dropped and the reason recorded. The regressor is always the **constructed** count.

**REF is rescored** (5 clips) under the patched app that also saves timelines. This is the
identity test: every parcel's raw value must match the committed stage-03 S− result to
|Δ| ≤ 1e-4, and the time-mean of each saved parcel timeline must equal that parcel's raw value
to 1e-5. **If identity fails, stop**: nothing scored under the patched app is comparable.

Twenty clips in one session: 5 REF + 5 B + 5 C + 5 D.

## Statistics — fixed now

For a ladder, **b** is the per-parcel OLS slope of z on natural-log constructed cut count over
the five levels. Reference values, frozen in `reference_mode.json`:

| | REF (stage 03 S−) | stage 03 S+ projected on REF, for scale |
|---|---|---|
| frontal cluster slope, mean of IFJa · IFJp · IFSp · 8C | **+0.251** (perm *p* 0.017) | +0.371 (0.008) |
| auditory slope, mean of A4 · A1 · MBelt | **−0.422** (0.008) | −0.407 (0.008) |
| whole-map gain, (**b**·**m**)/(**m**·**m**) with **m** the REF slopes | 1.000 | 0.811 (0.008) |

**Primary statistic: the frontal ratio ρ_F** = ladder's frontal cluster slope ÷ 0.251, with a
one-sided level-permutation *p* (all 120 orderings of the five levels; floor 1/120 = 0.008).
The count of parcels at |*r*| > 0.9 is *not* used: the 16 Sep review showed its null is
mis-specified. **Secondary, reported:** auditory ratio ρ_A (÷ −0.422) with its *p*; whole-map
gain and *r*(**b**, **m**) with *p*; participation ratio across levels.

Each new ladder is classified on ρ_F:

- **REPRODUCES** — ρ_F ≥ 0.50 **and** *p* ≤ 0.05
- **ABSENT** — ρ_F ≤ 0.25, whatever *p*
- **PARTIAL** — anything else

"Same-scene" is classified on B and C together: REPRODUCES only if both do; ABSENT only if both
are; otherwise PARTIAL, with both reported.

## Verdicts, fixed now — outcomes only, no mechanisms attached

| same-scene hard cuts (B, C) | dissolve switches (D) | verdict |
|---|---|---|
| REPRODUCES | ABSENT or PARTIAL | **DISCONTINUITY** — a hard cut is sufficient without a change of scene |
| REPRODUCES | REPRODUCES | **EITHER** — a hard cut or a change of scene is each sufficient |
| ABSENT | REPRODUCES | **SWITCH** — a change of scene is sufficient without a hard cut |
| ABSENT | ABSENT | **CONJUNCTION** — neither alone; the response needs a hard cut between different scenes |
| any PARTIAL not covered above | | **GRADED** — no categorical claim; ratios reported as measured |

If D is dropped at the precondition, the verdict is read from B and C alone as DISCONTINUITY
(REPRODUCES), NOT-DISCONTINUITY (ABSENT) or GRADED, and says so.

What each verdict would mean for the paper is written in `RESULT.md` *after* the verdict, as a
reading, separately from it. Stage 03's README attached a mechanism to a verdict cell and the
data then contradicted the mechanism while satisfying the cell; that is not repeated here.

## Reported, not gating

- **Cut-locked response.** The patched app saves each clip's 61 × 180 parcel timeline. For
  levels 1, 3 and 7 of every ladder, where cuts are ≥ 7.5 s apart, the timeline is projected on
  the unit REF mode and averaged from −3 s to +12 s around each join. Exploratory; describes
  whether the response is a transient locked to the join or a sustained shift. No threshold.
- Whole-vector *r* between level 1 and level 31 within each ladder.
- The measured discontinuity size at joins (frame delta, histogram distance) per ladder, so the
  four ladders can be read as points on a magnitude axis as well as cells of a 2 × 2.

## Limits, stated before the data

- **Scene change and pixel change are not fully separated.** B and C make the pixel jump large
  by mirroring while holding the scene; they cannot make it as large as a change of scene
  without changing the scene. A DISCONTINUITY verdict is clean. SWITCH or CONJUNCTION leaves
  "large visual change" as an alternative to "change of scene", and the magnitude axis above
  is the only evidence on it.
- **A dissolve is not only the absence of a cut**: it is 0.5 s of blended imagery the encoder
  has rarely seen. An ABSENT in D could be the blend rather than the missing discontinuity.
- **Five levels, permutation floor 0.008**, one generator, two scenes, text branch off.
- **Different content per ladder.** B holds only the face scene and C only the landscape; REF
  and D hold both. Slopes are within-ladder, so content is constant within every slope, but the
  baseline each slope rides on differs.
- Everything is about TRIBE.

## Second session, optional — text branch on (review M6)

Run only if ≥ $3.00 of credit remains after the first session, as a separate restart, with a
hard cap of **75 minutes** wall-clock after which the Space is paused whatever has happened.
Five clips with the text branch enabled: stage 00's face, landscape and crowd; `face_close`;
stage 03 `Splus_cut31`. Reported per clip: whole-vector *r* between text-on and text-off, and Δz
on STSdp, A5, STSvp, A4, IFJa, VMV2, PHA2. No pass criterion: the result is a measured size of
the missing-modality effect, or, if the run produces nothing inside the cap, that bound stated
as a limitation. The 13 Sep attempt produced 0 / 12 in 189 min; the cap exists because of it.

## Cost and wall-clock

| | |
|---|---|
| Clip construction, measurement | $0 (ffmpeg, local) |
| Session 1: 20 clips on A10G at ≈ 10 min each, plus start-up | ≈ 3.5 h, **≈ $3.60** |
| Session 2: text branch, capped | ≤ 75 min, **≤ $1.25** |
| **Total** | **≤ $4.85** against $8.53 of credit on 20 Sep 2026 |

Results are harvested from `alecnpacey/tribe-probe-results` by **exact name** (`03b_<ladder>_cutNN`),
the Space is paused on every exit path, and the watcher is one short process per minute, nothing
resident — the machine killed heavier watchers twice on 14 Sep.

## Done when

This README unchanged from its first commit; `CLIPS.md` with construction commands and the
measured preconditions; the patched app's diff and the identity-test numbers; `evaluate_03b.py`
and `evaluation.json`; `RESULT.md` with the verdict against the table above, then the reading;
`../LOG.md` lines for every run including failures; `../../CONSOLIDATION.md` step 2 ticked.
