# 00 — Discrimination probe · RESULT

**Run 1 September 2026 · HF Space `alecnpacey/tribe-probe` · A10G Small · TRIBE v2, video mode, `audio_only=True`**

## Update — full 180-parcel vectors (2 September)

The first run kept only the top 10 per clip; the rest was lost to the Space's
ephemeral disk. Re-run with all 540 values persisted (`parcel_vectors.json`).
**The full vectors are a substantially stronger result than the top-10 was.**

### Reproducibility

Independent run, same clips, same model: LO2 +2.43 vs +2.43, A5 +2.37 vs +2.38,
STSdp +2.04 vs +2.04. Matching to two decimals; the ±0.01 drift is the `???`
parcel no longer polluting the z-score. TRIBE is deterministic and the reduction
is stable.

### A double dissociation

The bottom of each vector turned out to carry as much information as the top,
and it is reciprocal:

| chain | face | landscape | crowd |
|---|---|---|---|
| A5 (auditory) | **+2.37** | −3.26 | −0.38 |
| STSdp (social/voice) | **+2.04** | −3.99 | −0.74 |
| STSda | +0.06 | −3.33 | −1.15 |
| VMV2 (place) | −2.26 | **+2.83** | −0.17 |
| PHA2 (parahippocampal) | −3.46 | **+1.26** | −2.08 |
| PHA1 | −2.65 | **+1.01** | −1.77 |

Two systems trade places in opposite directions, and **crowd sits between them on
both chains** — a graded middle condition, not a third arbitrary point. That is a
far harder pattern to produce by noise or misalignment than three-way separation.

### The contrast the validity research asked for

`d-validity` recommended decoding *contrasts* rather than single-condition maps.
That contrast is computable from what we already have:

- **face − landscape**: STSdp +6.03, A5 +5.63, STSvp +3.92, TPOJ1 +3.67,
  STSda +3.38, A4 +2.97, STGa +2.53, 55b +2.33, PBelt +2.18
- **landscape − face**: VMV2 −5.09, PHA2 −4.72, PHA1 −3.66, PHA3 −3.64,
  PGp −3.18, DVT −3.02, POS1 −3.00, VMV3 −2.87, VMV1 −2.56

Two complete anatomical chains, cleanly opposed. Whole-vector correlations:
landscape vs face **r = −0.098** (orthogonal), landscape vs crowd +0.455,
crowd vs face +0.453 — crowd is intermediate, as its content implies.

Note this also weakens the 55b concern: 55b appears at +2.33 in the contrast,
well below the superior-temporal parcels around it, so the face-clip signal does
not depend on it.

## Verdict: PASS on both criteria

TRIBE discriminates content, and it does so in the anatomically correct direction.
The sensor works. Everything downstream is unblocked.

## Criterion 1 — separation

Mean pairwise top-10 Jaccard overlap **0.15**, against a threshold of < 0.60 fixed
before the run.

| | overlap |
|---|---|
| crowd vs face | **0.05** |
| crowd vs landscape | 0.33 |
| face vs landscape | **0.05** |

Face and landscape share one parcel out of ten. Crowd and landscape share more,
which is expected — both are visually busy wide shots.

## Criterion 2 — direction

Top-10 HCP-MMP1 (Glasser) parcels, ranked on z-scored values over 181 parcels:

| clip | top 10 |
|---|---|
| **crowd** | LO2, V4t, V7, IPS1, FEF, LIPv, VIP, V6A, V4, V8 |
| **face** | A5, STSdp, 55b, V8, A4, PEF, PBelt, IFSp, IFJa, PIT |
| **landscape** | VMV2, VMV3, V3B, V8, V4, V3CD, IPS1, IP0, V6A, LIPv |

Read anatomically:

- **face → auditory and language.** A4, A5 and PBelt are auditory belt/parabelt;
  STSdp is superior temporal sulcus, which integrates voices, faces and
  biological motion; 55b, IFSp and IFJa are language-network. PIT is posterior
  inferotemporal, object and face processing. This is two people talking in
  close-up, and the model reads it as such.
- **landscape → scene-selective ventromedial visual.** VMV2 and VMV3 top the
  list by a clear margin (+2.84, +2.61), and they sit in the parahippocampal
  place-area neighbourhood. Jungle and water, read as *place*.
- **crowd → dorsal attention and oculomotor.** IPS1, LIPv, VIP and FEF are the
  intraparietal/frontal-eye-field network; LO2 is lateral occipital, objects and
  bodies. Many people to scan across, read as a scanning problem.

That is the predicted direction on all three, not two.

## Secondary readout — the composite scores

The app's five composites, kept only for continuity. These are the
"engagement score" family carrying a published null against real audience
retention (r = +0.058), so they are **not** the primary readout.

| clip | Attention | Engagement | Language | Self-relevance | Virality |
|---|---|---|---|---|---|
| crowd | **+1.48** | +0.48 | +0.08 | −0.52 | −1.52 |
| face | +0.29 | +0.34 | **+1.52** | −0.82 | −1.34 |
| landscape | +1.03 | +0.42 | −1.90 | +0.36 | +0.09 |

Language swings 3.4 z-units between face and landscape, consistent with the
parcel-level reading.

## Settled facts

- **Output rate is exactly 1 Hz.** `timeline (61, 20484)` over a 60.0 s span =
  `1.000 rows/s`. This had been open since the research phase: the shipped config
  said 1 Hz, the paper did not state the TR, and a typical 1.49 s TR would have
  implied ~0.67 Hz. Closed, by measurement.
- **Vertex count is 20,484**, as documented.
- **`get_hcp_labels()` returns `{parcel_name: vertex_indices}`** — a dict, not a
  label list. Reduce directly from it; `summarize_by_roi` is unnecessary.
- **181 parcels** are returned for fsaverage5.
- **~10 minutes per 60 s clip on an A10G** — roughly **10× slower than real
  time**, not the 2.3–2.9× carried through the research from a ZeroGPU
  extrapolation. 120 encoding steps at ~4.9 s each. **This invalidates the buffer
  and worker arithmetic in the brief and needs propagating.**

## Caveats — do not skip these

1. **The face clip is confounded with speech.** It is two people *talking*, and
   `audio_only=True` keeps the audio branch live. The auditory and language
   parcels may be responding to the speech rather than the faces. A silent face
   clip would separate these. The discrimination result stands; the *attribution*
   to faces specifically does not.
2. **The landscape clip is not people-free** — roughly two frames in eight
   contain figures. It is environment-dominant, not environment-only.
3. **The crowd clip drifts** to a child and then a panther in its second half.
4. **One film, one grade, 640×480, dark 1942 Technicolor.** Same-source was a
   deliberate control, but it also means the result is not yet shown to
   generalise across stocks or eras.
5. **Text branch was skipped** (gated Llama-3.2-3B). Results are video + audio only.

## What this unblocks

The sensor discriminates, so the observational track can proceed. The next
experiment is whether it responds to *technique* on identical content — the
cut-rate test — which is the first thing that would actually support the
hypothesis rather than merely permit it.

## Cost

~2.5 hours of A10G Small at $1.00/hr, of which the great majority was spent on
failed iterations rather than computation. Space paused after the run.

## What went wrong on the way — worth not repeating

Seven failures, six of them mine, all in the last ten lines that turn vertices
into parcel names rather than in the model or the data:

| | failure | cause |
|---|---|---|
| 1 | L4 unavailable | HF capacity, not us. Switched to A10G |
| 2 | `show_copy_button` | invalid kwarg in gradio 6.11 |
| 3 | clips silently absent | the Space's `.gitignore` has `*.mp4`; uploads reported success and were dropped |
| 4 | `load_fsaverage5_atlas` | raises `NotImplementedError`, superseded by `build_roi_masks` |
| 5 | gated Llama 401 | `mode="video"` pulls the text branch; fixed with `audio_only=True` |
| 6 | tuple unpack | `run_inference` returns `(preds, abs_times)` |
| 7 | wrong readout twice | `build_roi_masks` returns 5 composites, not parcels; then `get_hcp_labels` returns a dict, not a list |

**The lesson: each cost ~7 minutes of restart plus ~30 minutes of scoring.**
Verifying an API shape by introspection costs seconds. Assuming it costs half an
hour. For the next experiment, introspect first in a throwaway run, then write
the real script once against known facts.
