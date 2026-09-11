# 01b — Clips

**Fixed before generation.** Prompts are in `README.md`; this file holds the audio
inputs, then fills with generation IDs, provenance and cinemetrics once clips exist.

## Audio

**11 September correction:** the text-to-video endpoint generates its own synchronised
audio and takes no audio input, so the tracks below are **not** supplied to the generator.
The dialogue is placed in the face-clip *prompt* instead; ambient and walla are requested
in the other two prompts. The tracks remain as a fallback, regenerable from
`make_audio.sh`, and their use would be reported.

### Fallback tracks — prepared, held

All three tracks: 60.0 s exactly, 48 kHz stereo AAC, loudness-normalised to the
same integrated level (−16 LUFS), so audio level cannot differ across clips.

| clip | track | content |
|---|---|---|
| landscape | ambient | wind (brown noise, low-passed, 10 s tremolo) over a river band (pink noise, 1.6 kHz). No voices, no music, no birds — the spec's "occasional bird" was dropped: a synthesised chirp would not be a bird, and a false one is worse than none. |
| crowd | walla | eight overlapping low-content sentences in eight different voices at staggered offsets and rates, low-passed and mixed at low gain with light echo; two distant two-note chimes at 20 s and 45 s. No intelligible words at mix level. |
| face | speech | the dialogue below, macOS `say` voices **Daniel** (A) and **Flo** (B) at 165 wpm, 0.55 s gaps, no music, no effects. |

**Route: free and local** — macOS `say` + ffmpeg, script `make_audio.sh`, reproducible.
Chosen on cost for a probe whose criteria are the place-chain / voice-chain contrasts,
not audio realism. Limitation inherited knowingly: synthetic voices are themselves
out of distribution for an audio branch trained on real speech.

**Why walla for the crowd and not silence.** Run 00's crowd clip had ambient crowd
sound. The three tracks mirror run 00's audio *categories* — environment, many voices,
two voices — so that the audio branch sees the same kind of contrast it saw on live
action. Intelligible speech appears only in the face clip; that is the run-00 design and
the § 5.1 caveat is inherited knowingly.

### Face-clip dialogue (≈ 60 s at conversational pace)

> **A:** You kept the letter, then.
> **B:** I kept all of them. I just never answered.
> **A:** That's worse, you know. Keeping them.
> **B:** Is it? I thought it was the kinder thing.
> **A:** Kinder for whom?
> **B:** *(pause)* For me, probably.
> **A:** At least that's honest.
> **B:** You always said I wasn't. Honest.
> **A:** I said you were careful. It isn't the same.
> **B:** It felt the same, from where I was sitting.
> **A:** And where was that?
> **B:** Across a table from you, mostly. Like this.
> **A:** *(laughs quietly)* Then nothing's changed.
> **B:** Everything's changed. That's why I came.
> **A:** So say it.
> **B:** I'm trying to. Give me a second.
> **A:** You've had eleven years.
> **B:** I've had eleven years of not saying it. That's different.
> **A:** *(pause)* All right. I'm listening.

Content is deliberately plain, present-tense, two-hander, no proper nouns, no plot
requiring context — so the auditory/language response is to *speech between two
people*, not to a story.

## Generation record — 11 September 2026

Endpoint `minimax/h3-max/text-to-video` for segment 1 of each clip, then
`minimax/h3-max/image-to-video` for segments 2–4 conditioned on the previous segment's
last frame. Four 15 s generations per clip; seams at 15.1 / 30.2 / 45.3 s, identical
across clips. `prompt_expansion_mode: balanced`, safety checker on. Full per-segment
record incl. `expanded_prompt` and `timings` in `generation_record.json`.

| clip | seeds (seg 1–4) | endpoints | res | duration s | audio provenance | regenerations |
|---|---|---|---|---|---|---|
| landscape | 20260911,20260912,20260913,20260914 | t2v→i2v×3 | 768P | 60.45 | native (H3 Max) | 0 |
| crowd | 20260912,20260913,20260914,20260915 | t2v→i2v×3 | 768P | 60.45 | native (H3 Max) | 0 |
| face | 20260913,20260914,20260915,20260916 | t2v→i2v×3 | 768P | 60.45 | native (H3 Max) | 0 |

**Spend:** 12 × 15 s = 180 s × $0.02 = **$3.60** (promotional rate; user-verified on the
model page 11 Sep). **Cap $3.60, not exceeded.**

**Incident, recorded rather than tidied.** The first run aborted after landscape
segment 1: the last-frame extraction for chaining failed (`ffmpeg … -sseof -0.05 …
exit 234` — a single-image write without `-update 1`). The segment itself was valid and
was kept; the script gained resume-by-existing-file and the extraction was fixed
(`-sseof -1 -update 1`) and tested on that segment before relaunch. No segment was
generated twice. Seed spaces overlap across clips (bases one apart, +0…3 per segment);
harmless, since seeds only need to be recorded, but noted.

**Also recorded:** two empty-body POSTs were accidentally accepted (HTTP 200) earlier the
same day by `fal-ai/minimax/h3-max/director` and `fal-ai/minimax/h3-max` while probing
for the endpoint id. Expected to have failed validation at $0; **not verified against
the fal dashboard.**

## Cinemetrics — measured 11 September, before any scoring

| clip | face_area_frac | frames with a face | cuts/min | camera_pan | median_luma | mean_sat |
|---|---|---|---|---|---|---|
| landscape | 0.0000 | 0 | 7.0 | +0.00004 | 47.0 | 88.5 |
| crowd | 0.0000 | 99 | 9.9 | −0.00031 | 74.0 | 69.4 |
| face | 0.1584 | 716 | 14.9 | +0.00005 | 53.0 | 151.3 |

**Pre-check verdict: FAIL as literally written; the failure is mostly in the check.**
(1) `face > crowd > landscape` on `face_area_frac` fails only because the crowd clip's
faces are below YuNet's size floor, so its largest-face measure is null → 0, tying
landscape. On *presence* (frames with any face: 0 / 99 / 716) the crowd sits between
the other two as intended. (2) "`face_hit_rate` highest on crowd" was mis-specified:
run 00 ranked crowd on face *count per frame*, which cinemetrics does not report; on
frames-with-any-face a two-person close-up trivially wins. That criterion is withdrawn
as unmeasurable with this tool, not softened.

**A real confound, not a technicality: the generator cuts.** Cuts per minute are
7.0 / 9.9 / 14.9, not the ~3 seams per clip assumed. H3 Max edits within a 15 s
generation, and the face clip — prompted as shot-reverse-shot — cuts twice as often
as the landscape. "Cuts held identical across clips" is therefore **violated**, and
cut rate covaries with content in this probe. Any 01b result must carry this: a
difference between clips is a difference in content *and* in cutting.

