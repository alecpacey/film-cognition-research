# 03 — Isolation: does cutting alone move the sensor on generated footage?

**Written before any generation. Criteria are not to be softened afterwards.**
Drafted 13 September 2026 from stages 00–02, 01b and 02b. Nothing here has been run.

## The question

Stage 01 varied cut count on identical live-action footage and the sensor answered in
inferior-frontal cortex (IFJa *r* = +0.996). Stage 02 measured cut rate across real cinema
and found no frontal association at all; cut rate loaded on auditory (negative) and early
visual cortex. The measured dials do not explain the disagreement — cut rate is the most
nearly independent dial (max |*r*| 0.194). The candidates left are (a) stage 01's result
was specific to its two scenes, (b) the observational signature is confounded by something
unmeasured, speech above all, since the text branch was off and dialogue reached the model
only as sound.

**Stage 03 tests both with one design:** stage 01's manipulation, on generated footage,
crossed with a speech factor. Only generated footage allows this — 01b established that the
sensor reads it on the axis that matters (*r* = +0.699), and 02b that the index predicts it.

## Design — 2 × 5, content held fixed by construction

**Base scenes.** Two generated scenes, mirroring stage 01's pair: a **face** scene (two
people at a table, medium close-up) and a **landscape** scene. Each 60 s, single continuous
take, static or slowly moving camera. Same generator and route as 01b
(`minimax/h3-max/text-to-video`, 768P, 4 × 15 s chained).

**Precondition, measured not assumed.** The generator cuts within its own outputs (01b:
7–15 cuts/min). Each base scene is run through `cinemetrics.py` and must show
**`cuts_per_min` ≤ 1 excluding the three chain seams** — i.e. one continuous take per
segment. A base that fails is regenerated with a first-frame image and a "single
continuous take, locked-off camera" prompt; if it still fails after two attempts, that
scene is abandoned and the reason recorded. **This is the step 01b showed cannot be
skipped.**

**Factor 1 — cutting (5 levels), imposed by us, exactly as stage 01.** The two base scenes
are intercut at **1, 3, 7, 15, 31** added cuts using `01-cutrate/build_conditions.py`
unchanged. Every condition contains exactly the same 30 s of each scene; only the cutting
differs. Content, lighting, motion and shot scale are identical across levels by
construction, which is what observational data could never give.

**Factor 2 — speech (2 levels).** Same ten clips with (S+) the face scene's native dialogue
audio, and (S−) the face scene's audio replaced by the landscape scene's ambient track, so
no speech is present. Audio is otherwise unchanged. This is the unmeasured confound, made a
factor. Text branch stays `audio_only=True` (as in every prior stage) so that results are
comparable; if Meta's Llama access arrives, a text-on replication is a separate, later run.

**Ten scored clips** (5 cut levels × 2 speech levels), plus the two bases scored as
references. Regress on **measured** cut rate from `cinemetrics.py`, not on the requested
count (stage 01's effective range was 2.1× not 31× because the sources carried their own
cuts; here the bases are single takes, so the range should be close to nominal).

## Pre-registered predictions

**H3a — cutting is causal for the inferior-frontal cluster.** In the S+ arm, at least **2 of
{IFJa, IFJp, IFSp, 8C}** reach |*r*| > 0.9 against log measured cut count across the five
levels, with positive sign. (Stage 01's bar was ≥ 15 of 180 parcels; with *n* = 5 levels
that count is reported too, against chance ≈ 7.)

**H3b — speech does not abolish it.** The same criterion holds in the S− arm. If H3a holds
and H3b fails, the stage-01 effect required speech and the observational auditory signature
is the same effect seen through the audio branch — the disagreement is *explained*.

**Reported, not gating.** Whole-vector correlation cut01 vs cut31 in each arm (stage 01:
+0.893). The auditory parcels A4, A5, MBelt against cut count in each arm — stage 02's
observational signature — to see whether it appears under control at all.

## Verdicts, fixed now

| outcome | reading | consequence |
|---|---|---|
| **PASS** — H3a and H3b | cutting is causal for IFJ, independent of speech; stage 01 replicates on generated footage | cut rate is a *causal* lever; stage 04 may use it |
| **PARTIAL-A** — H3a, not H3b | the frontal cut effect needs speech present | the observational/controlled disagreement is explained by the missing speech descriptor; cut rate is a lever only with dialogue |
| **PARTIAL-B** — neither, but the auditory signature tracks cut count | stage 02's signature is what cutting does on this sensor; stage 01 was scene-specific | stage 01's frontal result is demoted to a property of its two clips |
| **FAIL** — no parcel tracks cut count in either arm | cutting does not move the sensor on generated footage | either 01b's PASS does not extend to the motion/cutting axis, or the effect is live-action-specific; stage 04 must not use cut rate |

## Cost and wall-clock

| | |
|---|---|
| Bases: 2 × 4 × 15 s at 768P | 120 s × $0.02 = **$2.40 until 14 Sep 2026; $9.60 after** |
| Cutting and audio variants | $0 (ffmpeg) |
| Scoring: 12 clips on A10G | ≈ $2.05, ≈ 2 h |
| Regeneration budget | one round per base, ≤ $2.40 |
| **Total** | **≈ $5–15**, against the roadmap's $60 |

Needs: fal balance ≥ $5 (currently ≈ $6.40 after 01b); HF prepaid credit ≥ $3.

## Done when

`03-isolation/` holds this README unchanged from before generation; `CLIPS.md` with base
prompts as sent, cinemetrics on the bases (the single-take precondition), and per-condition
measured cut counts; `RESULT.md` against the verdict table above; `../LOG.md` lines for every
run including failures.
