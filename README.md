# film-cognition-research — mutuals inc.

Two things live here, and they grew out of each other.

1. **The production brief** for *The Simulated Viewer*, a ten-minute short film.
   A machine is told to make a simulated cortex light up as hard as it can, and given
   a video model to do it with. Over ten minutes it stops showing you the world and
   starts showing you faces. The film is that drift. `index.html`, published at
   **`mutuals.inc/film`**.
2. **An experimental research programme** asking whether the relation between
   cinematographic technique and predicted cortical response can be measured
   systematically enough to be *inverted* — specify a target response profile, derive
   the technique that reaches it. Four staged experiments, two complete, one
   collecting. Written up in **`research/PAPER.md`**.

The brief came first and the programme came out of it: the film's premise only works
if a brain encoding model can actually be driven by technique, and nobody had
measured whether it can. `noindex` is on while this is a brief rather than a finished
piece. It can come off once the film exists — the licence position is clean.

## How the film got here

The research asked whether an endless brain-driven livestream was buildable. It is, and it
would cost $131,000 a month on a model whose licence forbids any way of funding that, and it
would collapse into close-up faces within the hour regardless. **The collapse became the piece.**

That decision deleted most of the engineering: four of the twenty research items are moot and
another five are footnotes, because offline generation has no deadline and there is no live
audience. What survives is a loop script, TRIBE, a cortex render and an ffmpeg assembly.

## The one rule

**Nothing is claimed as tested that has not been tested here.** Every figure is either
sourced to a primary document, measured in this repo against criteria fixed before the
run, or explicitly marked unmeasured. The subject invites overclaiming — a system that
predicts brain activity is very easy to describe dishonestly — so both the brief and the
paper are organised around that distinction.

It has a second edge in the experiments. **TRIBE returns plausible-looking numbers for
inputs it cannot handle**, so "the output looked reasonable" is not evidence of
anything. Pass criteria are therefore written into each stage's README *before* the run
and are never softened afterwards.

## What is verified and what is not

| | |
|---|---|
| **Read from source** | TRIBE's shipped config and model code, fal's live OpenAPI schemas, the reference client's frame path. Secondary write-ups were wrong on VRAM, on the numpy pin, on model licensing, and on whether TRIBE ships parcellation helpers |
| **Measured in this research — film side** | nilearn render latency (71 ms – 3.90 s), the dead-cortex normalisation failure (0.00% of vertices lit at plausible settings), Destrieux contiguity on fsaverage5 (median 1.4%) |
| **Measured in this research — experiments** | **Stage 00:** mean top-10 Jaccard 0.15 against a pre-registered 0.60 bar, with a double dissociation between the voice and place chains. **Stage 01:** 51 of 180 parcels at \|r\|>0.9 against log cut count on identical footage, against a bar of 15 and chance ~7. Both against criteria fixed before the run |
| **Measured, stimulus side only** | 244 segments cut and normalised; 14 dials measured; dial condition number 58.8; detectability of all 14 dials at n=70. These touch no outcome |
| **Pre-registered, then run once** | **Stage 02 — verdict PARTIAL.** Plan registered at `osf.io/dg7fe` before the analysis, which then ran once on all 70 segments. Criterion 1 met: 14/14 dials carry weight in 101 of 180 parcels surviving FDR. Criterion 2 **not** met: cut rate does not replicate. **Only 9 parcels reach the pre-registered effect-size threshold** — the count of survivors is the weaker number |
| **Predicted, not observed** | the film's three-act arc. BrainDiVE's 61–70% face purity came from thousands of gradient steps; this film takes forty discrete ones through a text bottleneck. **Whether the drift happens in forty clips is still the single biggest open question.** What changed: stage 02 independently found **face area is the dominant dial**, largest coefficient in 65 of 101 surviving parcels, so a machine maximising this signal would reach faces first. That is measured support for the *mechanism*, arrived at by a different route than BrainDiVE. It is not evidence that the drift happens in forty clips, and it is an association in a model's predictions |
| **Tested, and not replicated** | stage 01's inferior-frontal cut-rate result (IFJa r = +0.996 on identical footage) was carried into stage 02 as pass criterion 2 — where it **failed**. IFJa is indistinguishable from its null observationally; the one cluster parcel that survives has zero cut-rate weight. The two tracks disagree, which the pre-registration named in advance as the most important possible finding. Which is wrong is not decidable from this data |
| **Reported but unconfirmed** | a separate `tribev2-subcortical` checkpoint; the 8,808 voxel figure |

**The largest standing caveat applies to everything in the experiments:** the dependent
variable is a model's prediction of cortex, not cortex. TRIBE's published agreement with
real brains is *r* = 0.3195 in-distribution and **0.2146 out-of-distribution**, and a
1937–1951 Technicolor corpus is further out than that figure was measured on. The paper
turns this into the effect-size threshold (§3.2) rather than leaving it as a disclaimer.
A finding that technique moves TRIBE is a finding about TRIBE.

## Where the experiments stand

| stage | status |
|---|---|
| **00 · Probe** — does the sensor discriminate content? | ✅ **PASS** |
| **01 · Gate** — does technique move it, content held constant? | ✅ **PASS** |
| **02 · Index** — the technique→parcel crosswalk | ⚠️ **Complete — PARTIAL.** Registered at `osf.io/dg7fe`, run once on 70/70 |
| 01b · Synthetic-imagery transfer | Specified, unrun — a prerequisite for stage 03 |
| 02b · Generalisation test | Specified; pulls only after stage 02 has a written result |
| 03 · Isolation · 04 · Inversion | Specified, not started |

Corpus: *Nothing Sacred* (1937), *Jungle Book* (1942), *Royal Wedding* (1951) — three
public-domain live-action Technicolor features, different directors on purpose, because
directors covary their dials and varying the director is the cheapest way to break that
covariance without a lab. An earlier animated-Technicolor assumption was **dropped on
evidence**: its availability premise was false, and animation is the *minimum*-variance
case — the opposite of what this corpus is for.

`research/experiments/HANDOFF.md` is the current resume point.
`research/experiments/ROADMAP.md` is the plan and its pull conditions.
`research/experiments/LOG.md` records every run, failures included.

## The control run is not optional

H3 Max may drift toward faces on its own, unprompted. If it does, the film's central claim —
that the *brain model* is doing the narrowing — is unsupported. The second pass with the drive
inverted is what separates a film that illustrates a claim from one that evidences it. Budget
for it: each full run is another $30–48.

## Framing

The released checkpoint has no subject-specific parameters, so predictions are bit-identical
whoever is watching. "Your brain" names a quantity the model does not compute. For a film this
is a gift — *a simulated viewer* is a better character than *you*, and an average of 720
strangers is a more unsettling one.

A published null result (arXiv 2607.01400) separately forecloses any engagement claim: partial
r = +0.058, below loudness and motion baselines. The film cannot claim to find what audiences
want. It can claim that a machine chasing a *model* of attention collapses — whether or not
that model is right about anyone.

**Obligations:** EU AI Act Article 50 synthetic-media disclosure has applied since 2 August 2026
and covers the generated video; one burned-in label discharges it. CC BY attribution for TRIBE
belongs in the credits. Keep it non-commercial and the rest of the licence stays quiet.
Not legal advice.

## Structure

```
film-cognition-research/          repo root — published as /film
  index.html                      the brief
  styles.css                      duotone — indigo for the brain side, ochre for the picture side
  research/
    PAPER.md                      the technical paper, sections 1–9
    report.md                     5,779 lines, the long-form reference
    results/*.json                20 items, each validated at 100% field coverage
    outline.yaml                  items and grounding facts
    fields.yaml                   the 18-field schema every item answers
    generate_report.py            rebuilds report.md from results/
    cinematography/               dial literature, and cinemetrics.py — the 14-dial measurer
    decoding/                     parcel annotations, ontologies, validity
    experiments/                  the staged programme; see experiments/README.md
      ROADMAP.md · OBJECTIVES.md · LOG.md · HANDOFF.md
      00-probe/ · 01-cutrate/ · 02-index/
```

```sh
python3 research/generate_report.py   # rebuild after editing any result
```

**Heavy and generated material is local-only** and is not part of the deployable set:
source prints under `research/experiments/02-index/sources/`, the 244 cut segments under
`02-index/segments/`, clip directories under each experiment, and raw prediction arrays.
Raw predictions for one 30 s clip are ~2.5 MB of float32 and there will be thousands —
keep them local, commit the reductions.

The stage-02 dataset `research/experiments/02-index/parcel_vectors.json` is **frozen**.
Its SHA-256 `93807b80…53a3189` is recorded in the OSF registration, and the registered
test verified it in-script before running. Do not modify it; any reanalysis must be able
to show it is working from the same bytes.

## Do not

Add a viewer-side sensor — EEG, webcam arousal, eye tracking — to make it "really your brain".
The privacy statutes are currently not engaged precisely *because* nothing measures anyone;
California's definition of neural data requires measurement and expressly carves out inference.
That single change makes all of them live at once, and it would weaken the film. The point is
that the viewer is a fiction.

And do not soften a pass criterion after seeing a result. Every threshold in this repo was
written before the run that tested it, and the ones that failed are in `LOG.md` alongside the
ones that passed.

## Licence

Code: MIT (`LICENSE`). Text, documentation and data: CC BY 4.0 (`LICENSE-CC-BY-4.0.md`).
The parcel vectors and timelines are TRIBE's predictions, and TRIBE has its own non-commercial
licence; see `LICENSING.md` for scope and exclusions.
