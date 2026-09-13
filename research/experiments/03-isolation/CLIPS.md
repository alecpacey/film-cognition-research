# 03 — Clips

## Base scenes — generated 13 September 2026

Generator `minimax/h3-max/text-to-video` for segment 1, `…/image-to-video` chained on the
previous segment's last frame for segments 2–4. 4 × 15 s per base, 768P, 16:9,
`prompt_expansion_mode: balanced`, safety checker on. Per-segment `expanded_prompt` and
`timings` in `generation_record.json`. Script `generate_bases.py`.

### Prompts as sent (style suffix appended to both)

**face:** Two people in conversation at a kitchen table, medium close-up on both, warm interior light, locked-off camera on a tripod, "
         "natural back-and-forth dialogue in the audio, expressive faces, eye contact. 

**landscape:** A wide river valley at late afternoon — hills, trees, water, moving cloud shadow — the camera drifting very slowly and "
              "continuously, no people, no animals. Audio: wind and distant water only, no voices, no music. 

**style suffix:** Photographic, live-action look, 35 mm film grain. ONE SINGLE CONTINUOUS TAKE with NO cuts, NO edits, NO scene changes, NO camera switches: the same shot held unbroken for the whole duration. No text, no captions.

| base | seeds (seg 1–4) | endpoints | res | duration s | audio | regenerations |
|---|---|---|---|---|---|---|
| face | 20260920,20260921,20260922,20260923 | t2v → i2v ×3 | 768P | 60.40 | native (H3 Max) | 0 |
| landscape | 20260930,20260931,20260932,20260933 | t2v → i2v ×3 | 768P | 60.40 | native (H3 Max) | 0 |

**Spend:** 8 × 15 s = 120 s × $0.02 = **$2.40** (promotional rate, last day). Cap $2.40, not
exceeded. No regeneration was needed.

## Single-take precondition — measured before any use

README requires `n_cuts` ≤ 4 over 60 s (≤ 1 real cut beyond the three chain seams).
`cinemetrics.py` run from `02-index/` (needs `yunet.onnx`), nested keys.

| base | n_cuts | cuts_per_min | duration s | face_area_frac | verdict |
|---|---|---|---|---|---|
| face | 0 | 0.00 | 60.40 | 0.0352 | **PASS** |
| landscape | 0 | 0.00 | 60.40 | null (no face) | **PASS** |

Zero cuts detected on both, including the three chain seams — the explicit
"one single continuous take, no cuts" instruction held, unlike 01b's prompts, which
did not ask for it and drew 7–15 cuts/min. The seams are therefore below the cut
detector's threshold: last-frame chaining produced visually continuous joins.

**Noted for the ladder, not a blocker:** the face base's largest-face fraction is 0.035 —
a wide two-shot, not the medium close-up asked for (01b's face clip measured 0.158).
Content is held fixed across cut levels by construction, so the manipulation is unaffected;
but the face/place contrast between the two bases is smaller than 01b's.

## Intercut conditions — not yet built
