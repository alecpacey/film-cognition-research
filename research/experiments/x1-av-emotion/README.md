# x1 — Does the face change the emotion signal? (audiovisual pilot)

**Written before the run, 11 September 2026. Do not edit the pass criteria afterwards.**

A side branch, not a stage in the 00→04 chain. Nothing downstream depends on it and it
gates nothing. It exists because a speech-emotion connectome project, which drives
connectome wiring with CREMA-D *audio*, asked where to start on other modalities. CREMA-D was recorded on video, and that project used only the sound.

## The question

Running the same emotional speech through TRIBE with and without the speaker's face, does
the face change the predicted cortical emotion signal, and does that change **replicate
across independent actors**?

Happy vs angry is chosen deliberately. Both are high-arousal, so the voice separates them
less well than it separates, say, angry from sad. Valence is where the face (smile vs
scowl) should carry the most, so if the face adds anything it should show here.

## Design — 8 blocks, one Space run

2 emotions (HAP, ANG) × 2 conditions (face, blank) × 2 disjoint actor sets (A, B).

| | |
|---|---|
| Source | CREMA-D `VideoFlash/` (ODbL 1.0 / DbCL 1.0), 480×360, 29.97 fps, lip-synced audio |
| Actors | 4 per set, 2 female + 2 male, drawn with `random.Random(20260911)` from `VideoDemographics.csv`; A and B disjoint |
| Sentences | the 11 sentences recorded at level `XX` only; `IEO`, the one recorded at graded intensities, is excluded so intensity is constant |
| Block | utterances concatenated sentence-major (all four actors say sentence 1, then sentence 2 …), cut at exactly 60.0 s |
| Matching | within a set, HAP and ANG use the **same actor × sentence list in the same order** — the contrast cancels identity and content |
| Face | the actors' own video with its own audio |
| Blank | a mid-grey (0x808080) frame at the same size and rate, with **byte-identical audio** to the face block (checked by decoded-audio MD5 at build) |
| Loudness | every utterance RMS-normalised to −23 dBFS, peak-limited below 0.99, before concatenation. Anger is louder than happiness, and a pure-loudness contrast would replicate across actors and pass as emotion |
| Encode | libx264 CRF 20 `yuv420p`, AAC 128 kbps |
| Scoring | the unchanged stage-02 Space path: `mode="video"`, `audio_only=True` (video + audio, no text branch), whole-clip mean per parcel, 180 HCP-MMP1 parcels, within-clip z |

Run order puts the four face blocks first, so C1 is decidable even if the run is cut short.

## Quantities

For actor set *S*, emotion *E*, condition *C*, let **z**(*S*,*E*,*C*) be the 180-parcel z vector.

- emotion contrast **c**(*S*,*C*) = **z**(*S*,HAP,*C*) − **z**(*S*,ANG,*C*)
- face interaction **d**(*S*) = **c**(*S*,face) − **c**(*S*,blank)

Replication is the Pearson *r* between set A's vector and set B's, across the 180 parcels.

## Why the bar is 0.78, not 0.50

TRIBE's cortex moves along only a few dominant axes (stage 02 § 6.7: three components
carry 90% of the index). So two *unrelated* contrasts often point the same way by
chance, and a replication *r* has a wide null. It was measured **before this pilot's data
existed**, from the frozen stage-02 vectors (SHA-256 `93807b80…53a3189`, verified): 20,000
draws of disjoint random segments, seed 20260911.

| null | mean *r* | 95th pct | 99th pct |
|---|---|---|---|
| contrast (*a*−*b*) vs (*c*−*e*) | +0.000 | **+0.774** | +0.902 |
| interaction ((*a*−*b*)−(*c*−*e*)) vs ((*f*−*g*)−(*h*−*i*)) | −0.009 | **+0.787** | +0.899 |

The programme's SESOI of 0.50 would be crossed by chance far more often than one time in
twenty here, so each bar is the one-sided 95th percentile, rounded **up**.

## Pass criteria — fixed now

1. **C1 — the emotion signal with the face replicates.** *r*(**c**(A,face), **c**(B,face)) **≥ 0.78**.
2. **C2 — the face's contribution to that signal replicates.** *r*(**d**(A), **d**(B)) **≥ 0.79**.

**PASS**: both. **PARTIAL**: C1 only — TRIBE carries a replicable happy/angry signal with
the face on, but what the face adds beyond the voice cannot be separated at this *n*.
**FAIL**: C1 not met. C2 is then reported but not interpreted.

**Reported, not gating:** *r*(**c**(A,blank), **c**(B,blank)), the voice-only emotion
replication; the top-10 parcels of the set-averaged **c**(face), **c**(blank) and **d**; where
the face and voice parcels (FFC, PIT, V8, STSdp, STSvp, STSda, STSva, A4, A5, TPOJ1) rank.
No direction is predicted for them and none will be claimed as a prediction afterwards.
Pipeline health: 180 parcels per block, no NaN, |z| ≤ 8.

## What this cannot show

- **It is a pilot.** One block per cell and one replicate pair, so each criterion is a
  single correlation. A pass says "worth a proper study", not "established".
- **The dependent variable is TRIBE's prediction, not cortex** (r = 0.21 out of distribution).
- **The null comes from film segments, not emotion blocks.** It measures chance alignment
  under TRIBE's cortical covariance, which is the relevant hazard, but the stimulus family
  differs.
- **A grey frame is out of distribution for TRIBE's head.** It is identical across
  emotions, so it cancels inside **c**(·,blank), but not inside the face − blank main effect,
  which is therefore not reported as a finding.
- **Posed emotion, two emotions, whole-block means.** Timing and dynamics are averaged away.

## Files

`build_blocks.py` builds and verifies the blocks (sources/work/blocks are local only) ·
`blocks_manifest.json` lists every utterance used · `run_x1.py` stages, scores and harvests
without touching stage-02's files · `results/` holds the eight vectors · `analyse_x1.py`
computes the criteria · `RESULT.md` the verdict.

## Results repo — split on 15 September 2026

x1 now writes to its own Hugging Face dataset, **`alecnpacey/x1-av-emotion-results`**
(private, created empty 15 Sep). `run_x1.py --run` sets the Space's `RESULTS_REPO` variable
to it while the Space is paused, verifies the read-back, restarts, and restores the variable
to the programme's `alecnpacey/tribe-probe-results` on every exit path. `--migrate` moves
the 11 Sep pilot's eight result files out of the shared repo (copy, verify, then delete;
refuses unless all eight are banked locally in `results/`). Run 16 Sep 2026: 8 files
moved, 0 left in the shared repo. Reason for the
split: a stage-03 watcher matching `"03_"` anywhere in a filename harvested x1's files from
the shared repo on 14 Sep and paused that run at 6 / 12.
