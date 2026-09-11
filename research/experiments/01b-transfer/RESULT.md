# 01b — Result

**Verdict: <PENDING — filled by evaluate_01b.py after harvest>**

Run 11 September 2026 against `README.md` criteria as fixed before generation
(bar for criterion 3: *r* ≥ 0.50). Generator `minimax/h3-max/text-to-video`, three
60.45 s clips (4 × 15 s each, last-frame chained), 768P, native audio. Scored on
`alecnpacey/tribe-probe`, A10G, `audio_only=True`, 180 parcels. Evaluation script
`evaluate_01b.py`, self-tested on run 00's vectors (PASS, axis *r* +0.936).

## Criteria

| criterion | required | found | |
|---|---|---|---|
| 1 · separation, mean top-10 Jaccard | < 0.60 | — | — |
| 2 · direction, place chain on landscape / voice chain on face | both | — | — |
| 3 · axis, corr(face − landscape, index axis 1) | ≥ +0.50 | — | — |

Reported, not gating: correlation with run 00's live-action contrast; per-clip
correlation with the run-00 counterpart.

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
