# 01b — Result

**Verdict: PASS — all three criteria met.**

Run 11 September 2026 against `README.md` criteria as fixed before generation
(bar for criterion 3: *r* ≥ 0.50). Generator `minimax/h3-max/text-to-video`, three
60.45 s clips (4 × 15 s each, last-frame chained), 768P, native audio. Scored on
`alecnpacey/tribe-probe`, A10G, `audio_only=True`, 180 parcels. Evaluation script
`evaluate_01b.py`, self-tested on run 00's vectors (PASS, axis *r* +0.936).

## Criteria

| criterion | required | found | |
|---|---|---|---|
| 1 · separation, mean top-10 Jaccard | < 0.60 | **0.083** | met |
| 2 · direction, place chain on landscape / voice chain on face | both | **both** | met |
| 3 · axis, corr(face − landscape, index axis 1) | ≥ +0.50 | **+0.699** | met |

Reported, not gating. Correlation of the generated face − landscape contrast with run
00's live-action contrast: **+0.831**. Per clip against its run-00 counterpart:
face **+0.885**, landscape +0.412, crowd +0.347.

## Reading

Generated imagery from this generator moves the same face/place axis real film moves,
at about three-quarters of the live-action alignment (+0.699 against a reference of
+0.936) — comfortably over the bar and 4.9× the 180-parcel permutation null (0.144).
Separation is *tighter* than run 00's (0.083 vs 0.146). The head sees the generated
face clip almost as it sees the real one (+0.885); it sees the generated landscape and
crowd less faithfully (+0.41, +0.35), which is where the confound below most plausibly
bites and where stage 03 should expect the weakest transfer.

**Consequence for the roadmap.** Stage 03 may proceed on all axes with `minimax/h3-max`,
and stage 04's dependence on the face/place axis is met — subject to deviation 2: this
PASS was earned with cutting confounded with content, so the *first* stage-03 design
must control cutting per shot (image-to-video per shot, or single-shot prompts) before
any dial is isolated.

## Deviations, disclosed before the result was seen

1. **The stimulus pre-check failed as literally written.** `face_area_frac` ordering
   face > crowd > landscape did not hold because the crowd clip's faces sit below
   YuNet's size floor (largest-face measure null → 0, tying landscape at 0). On
   presence — frames with any face, 0 / 99 / 716 — the crowd sits between the other
   two as intended. The check's second half ("hit rate highest on crowd") was
   mis-specified against what cinemetrics measures and is withdrawn as
   unmeasurable, not softened. Decision taken before scoring: score as generated,
   with this disclosed. See `CLIPS.md`.
2. **Cut rate covaries with content.** The generator cuts within its own 15 s
   outputs: 7.0 / 9.9 / 14.9 cuts per minute for landscape / crowd / face. "Cuts held
   identical across clips" is violated. Any difference between clips below is a
   difference in content *and* in cutting. This is the principal limitation of this
   run and could not be removed without per-shot generation control.
3. **Audio is generated, not matched to run 00's.** Native H3 Max audio from the
   prompts; synthetic speech on the face clip. The silent diagnostic arm was dropped
   on cost, so an auditory-only failure of criterion 2 could not be attributed.
4. **Two accidental empty requests** to fal endpoints earlier the same day, expected
   $0, **not verified** against the dashboard.

## Spend

Generation $3.60 (cap $3.60, not exceeded). Scoring ≈ $0.50. Total ≈ $4.10.

## What a PASS here would and would not establish

That H3 Max output moves the same face/place axis real film moves, in this probe,
with cutting confounded with content. Not that generated imagery is in-distribution
for the head, and nothing about lighting, motion or colour dials.
