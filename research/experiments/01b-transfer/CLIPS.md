# 01b — Clips

**Fixed before generation.** Prompts are in `README.md`; this file holds the audio
inputs, then fills with generation IDs, provenance and cinemetrics once clips exist.

## Target audio — prepared before generation, supplied as H3 Max input

All three tracks: 60.0 s exactly, 48 kHz stereo AAC, loudness-normalised to the
same integrated level (−16 LUFS), so audio level cannot differ across clips.

| clip | track | content |
|---|---|---|
| landscape | ambient | wind through trees, distant river, occasional bird. No voices, no music, no rhythmic events. |
| crowd | crowd murmur | station-concourse walla: many overlapping indistinct voices, footsteps, a distant announcement chime. No intelligible words. |
| face | speech | the dialogue below, two synthetic voices (one lower, one higher register), conversational pace, natural pauses. No music, no effects. |

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

## Generation record — filled after the run

| clip | generation id | resolution | duration (s, ffprobe) | audio provenance | regenerations |
|---|---|---|---|---|---|
| landscape | | | | | |
| crowd | | | | | |
| face | | | | | |

## Cinemetrics — filled after generation, before scoring

Required ordering before any clip is scored: `face_area_frac` face > crowd > landscape;
`face_hit_rate` highest on crowd.

| clip | face_area_frac | face_hit_rate | cuts_per_min | camera_pan | median_luma |
|---|---|---|---|---|---|
| landscape | | | | | |
| crowd | | | | | |
| face | | | | | |
