# 00 — Discrimination probe

**Written before the run. Do not edit the pass criteria afterwards.**

## The question

Does TRIBE distinguish between kinds of content at all?

Everything downstream assumes it does. If the top-ranked cortical regions are
the same whether the model is shown a landscape, a crowd or a face in close-up,
then TRIBE is not a usable sensor for this project and no amount of experimental
design further down will rescue it.

This costs nothing and takes an afternoon, so it runs first.

## Why it might fail

Not a formality. There is a specific reason to doubt it: of the 121 hours of
video TRIBE ever saw during training, **64.5 hours is *Friends*** — a
multi-camera sitcom shot almost entirely in medium two-shots on a fixed set.
Only three of its eight training datasets contain real cinema. A model whose
visual diet was mostly a sitcom may have poor sensitivity to exactly the
variation we intend to use.

## Method

Three clips, each **at least 30 seconds**, sourced yourself:

| Clip | Should preferentially drive |
|---|---|
| `landscape.mp4` — wide terrain, no people | scene / place regions (parahippocampal) |
| `crowd.mp4` — many people, mid-distance | body and biological-motion regions |
| `face.mp4` — a single face, close-up, talking | face regions (fusiform) |

Run `probe.py`. It scores each clip, z-scores the predictions over the timeline,
reduces to HCP parcels, and reports the top-ranked regions per clip plus the
differences between clips.

## Pass criteria

The probe **passes** if both hold:

1. **Separation.** The top-10 parcel sets for the three clips are not
   substantially the same. Concretely: mean pairwise Jaccard overlap of the
   top-10 sets **< 0.6**.
2. **Direction.** At least two of the three clips rank their expected region
   family higher than the other two clips do. A face close-up should drive
   fusiform parcels harder than a landscape does.

The probe **fails** if the top regions are near-identical across all three, or
if the expected directions are absent or reversed.

A **partial pass** — separation without correct direction — is still
informative. It would mean TRIBE responds to *something* about the clips but
not the semantic categories we assumed, and the next step would be to find out
what it is responding to before assuming it is content.

## Traps this script guards against

| Trap | Guard |
|---|---|
| Clips under 30 s return diffuse noise and **do not error** | Hard refusal below 30 s, warning below 100 s |
| Absolute activation values are meaningless — the training target was per-sample z-scored and detrended | All ranking is done on z-scored values |
| Activations are ~50× smaller than intuition (a real face drives fusiform to ~+0.080 z) | No absolute thresholds anywhere; ranking only |
| The prediction rate is disputed — config says 1 Hz, a 1.49 s TR would imply ~0.67 Hz | `preds.shape` is printed and recorded rather than assumed |
| `neuroscore`'s region accessors cannot ever have run | Uses `tribev2.utils` directly |

## Recording

`probe.py` writes `out/probe_results.json` (raw, gitignored) and prints a table.
Findings go in `RESULT.md` alongside this file — including a failure, which is
a result and should be written up as one.

Add a line to `../LOG.md` for every run, including runs that crashed.
