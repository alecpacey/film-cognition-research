# 01b — Synthetic-imagery transfer gate

**Written before generation. Criteria are not to be softened afterwards.**
Respecifies the gate held in `../OBJECTIVES.md` § O2, which was written for
*animated* material and reclassified in `../ROADMAP.md` as a stage-03 prerequisite.
Three things changed since it was held, and each changes the design:

1. Stage 03 will **generate** clips, so the gate must test generated imagery — not
   animation, whose out-of-distribution character may differ.
2. Stage 02 found that fourteen dials resolve to about three cortical axes and that the
   first — the **face/place axis** — carries 69% of the index and all of the inversion
   thesis (`../../PAPER.md` § 6.7). A gate that tests three-way discrimination without
   testing *that axis* could pass while leaving the thing stage 04 depends on unverified.
   So a third criterion is added, anchored on a live-action reference.
3. The generator is fixed by the film brief: **MiniMax Hailuo (H3 Max) via fal.ai**.
   Its constraints are stated below rather than assumed.

## The question

TRIBE's encoding head was fitted on 121 h of live action, 64.5 h of it *Friends*.
Generated video is out of distribution for it in ways live action is not — non-physical
motion, synthetic faces, flat fields, hard edges — and the head fails silently, returning
plausible numbers. **Does the head respond to generated imagery the way it responds to
live action, and in particular along the axis the programme depends on?**

## Method

Run 00's three-way content probe, on **generated** material. Same harness
(`space_app.py`, `mode="video"`, `audio_only=True`), same reduction to 180 parcels,
same 60 s clip length. Three clips, matching run 00's categories, each generated from a
prompt fixed here before anything is generated:

| clip | prompt (fixed) |
|---|---|
| **landscape** | *A wide, slowly drifting view across a river valley at late afternoon: hills, trees, water, moving cloud shadow. No people, no animals, no text. Photographic, live-action look, natural light, 35 mm film grain.* |
| **crowd** | *A busy railway-station concourse seen from a mezzanine: dozens of people crossing in every direction, no single face close to camera, ambient bustle. Photographic, live-action look, natural light, 35 mm film grain.* |
| **face** | *Two people in conversation at a kitchen table, medium close-up, shot-reverse-shot framing held on one speaker at a time, expressive faces, eye contact. Photographic, live-action look, warm interior light, 35 mm film grain.* |

The prompts ask for a **photographic live-action look** deliberately. The out-of-
distribution question stage 03 faces is "generated footage that is trying to look like
film", not "cartoons". Style words are held identical across the three so that content
is the only thing varying, exactly as `../00-probe/CLIPS.md` argued for run 00.

**Generated content is measured, not trusted.** Every clip is run through
`cinemetrics.py` before scoring. The face clip must have the highest `face_area_frac`,
the landscape clip the lowest, and the crowd clip the highest `face_hit_rate` with a
smaller `face_area_frac` than the face clip — the same gradient run 00 established by
YuNet ranking (24.1% → 1.5% → 0.6%). A clip that fails this is regenerated before
scoring; the number of regenerations is reported. This is a stimulus-side check and
touches no outcome.

### Generator constraints, and how they are handled

- **Maximum generation length is 10 s** (6 s standard) at the time of writing — read
  from fal's model pages, not assumed. A 60 s clip is therefore **6 to 10 generations
  concatenated**, which introduces cuts. Cuts are a dial. They are held **identical
  across the three clips** — same number of generations, same durations, same join
  points — so that the three-way contrast is not confounded by cutting, and the
  concatenation count is recorded in `CLIPS.md`. Stage 03 faces the same constraint
  and 01b establishes the protocol for it.
- **Native audio: unverified.** Whether H3 Max returns an audio track is to be
  established at generation time and recorded. See *Audio*, below.
- **Cost is not $0.50.** The roadmap's figure covered scoring only. At $0.08/s (Pro,
  1080p) a 60 s clip is ≈ $4.80 to generate, or ≈ $2.70 at 768p ($0.045/s); three
  clips ≈ $8–15, six ≈ $16–29, plus ≈ $0.17 per clip to score. **Figures read from
  fal's pricing pages on 9 September 2026 and may have moved.**

### Audio — a decision this gate has to make for stage 03

Run 00's face clip was two people *talking* with the audio branch live, and § 5.1 of the
paper records that its voice-chain response (A4, A5, STSdp) may be speech rather than
faces. Generated clips may be silent. If they are, the auditory half of criterion 2 can
fail for lack of sound rather than lack of transfer, and the gate would be uninformative.

**Decision (10 September 2026): one arm, audio-matched. Three clips.** Audio is added to
mirror run 00 — synthetic speech on the face clip, ambient on the landscape, crowd murmur
on the crowd — so the gate tests the full pipeline stage 03 will actually run. A silent
arm was specified and **dropped on cost**, halving generation spend. Consequence stated
rather than hidden: if criterion 2 fails on the auditory parcels only, this design
cannot say whether the head failed to see the generated faces or merely heard nothing
distinctive — the silent arm would have separated those, and would be the first thing
to add if that outcome occurs. If H3 Max returns native audio, it is replaced, not
layered, so that the audio provenance is identical across clips.

## Pass criteria — fixed now, before generation

Criteria 1 and 2 are **held unchanged** from the version fixed
before O1 ran. Criterion 3 is new and its anchor is stated.

1. **Separation.** Mean pairwise top-10 Jaccard overlap across the three clips
   **< 0.60**. Same bar as run 00, which scored 0.15.

2. **Direction.** The landscape clip ranks the place chain — VMV1–3, PHA1–3 — above
   the other two clips; the face clip ranks the voice chain — A4, A5, STSdp, STSvp —
   above the other two. Both must hold.

3. **Axis.** The generated `face − landscape` contrast vector, correlated across the
   180 parcels with **axis 1 of the stage-02 index** (first left-singular vector of the
   180 × 14 coefficient matrix, oriented so that `face_area_frac` loads positive), must
   reach ***r* ≥ +0.50.**

   *Anchor.* The live-action reference is run 00's own contrast vector against the same
   axis: ***r* = +0.936** (face alone +0.704, landscape alone −0.684, crowd −0.135). The
   180-parcel permutation null has a 95th percentile of 0.144. The threshold is set at
   roughly half the live-action reference and three and a half times the null: a
   generated contrast that reaches half the alignment of real film is enough for stage
   03 to interpret its results on this axis; one that does not is not moving the axis
   the programme depends on, whatever criteria 1 and 2 say.

**PASS** — all three. Generated imagery from this generator is an admissible stimulus
for stage 03 on every axis, and for stage 04.

**PARTIAL** — criteria 1 and 2 pass, criterion 3 fails. The head discriminates
generated content in sensible directions but does not reproduce the face/place axis.
Stage 03 may proceed on **motion and colour dials only** (axes 2 and 3); the face-area
dial and stage 04 are **not** admissible with this generator until a further gate
passes. This outcome must be written up as what the head *does* respond to.

**FAIL** — criterion 1 or 2 fails. This generator is out for stage 03. The corpus
question for generated material reopens.

**Reported, not gating.** Correlation between the generated contrast and run 00's
live-action contrast directly. Per-clip correlation with its run-00 counterpart.
Number of regenerations.

## What a PASS does not establish

That generated imagery is in-distribution for the head. A pass means the head's response
to *these three categories* lies on the axis real film puts them on; it says nothing
about lighting, motion or colour dials, which stage 03 will manipulate and 01b does not
test. It is a gate on the axis stage 04 needs, not a certificate for the generator.

## Cost

| | |
|---|---|
| Generation, 3 × 60 s at 1080p Pro | ≈ $15 *(≈ $8 at 768p)* — fal pricing, 9 Sep 2026, unverified since |
| Scoring, 3 clips on A10G | ≈ $0.50, ≈ 30 min |
| Regenerations | reported; budget one round |

## Done when

`01b-transfer/` holds this README unchanged from before generation, `CLIPS.md` with the
prompts as sent, generation IDs, concatenation counts, audio provenance and cinemetrics
measurements, `RESULT.md` with the verdict against the criteria as fixed, and
`../LOG.md` carries a line — including if it crashed.
