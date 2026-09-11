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
