# A technique→response index for cinematography, measured through a brain encoding model

**Working paper · consolidated draft of 8 October 2026**
**Status: stages 00, 01, 02, 03 and 03b complete and reported, with the 01b transfer gate
and an exploratory 02b generalisation check. Stage 02's analysis plan was registered at
`osf.io/dg7fe` before the analysis was run; it returned PARTIAL. Stage 03, criteria fixed
before generation, returned PARTIAL-A and reconciles stages 01 and 02; stage 03b returned
GRADED. Exploratory analyses are labelled as such wherever they appear.**

---

## Abstract

Can cinematographic technique move a brain encoding model's predicted cortical response
systematically enough to be mapped, and the map inverted? We use TRIBE, a trimodal fMRI
encoding model, as the sensor, read at 180 cortical parcels with its text branch off.
Every result is therefore a statement about the model: its published out-of-distribution
accuracy against real cortex is *r* = 0.2146, which we propagate into a smallest effect
worth reporting (*r* ≥ 0.5) as a justified heuristic, not a bound.

Each stage was judged against criteria fixed before it ran. A probe
separated content along a reciprocal face/place axis (PASS). Varying only cut count on
identical footage moved inferior-frontal cortex at the design's permutation floor (PASS).
A registered observational index — 14 measured dials, 70 segments of three 1937–1951
Technicolor features — associated every dial with surviving parcels but placed cut rate in
auditory, not frontal, cortex (PARTIAL). Generated footage moved the same face/place
axis (PASS). Cutting alone on generated footage, content fixed by construction,
raised inferior-frontal and lowered auditory response with and without speech
(PARTIAL-A, by 0.001 on one parcel); separating a cut's parts showed the frontal response
close to additive in hard cut and scene change, and the auditory one following the hard
cut (GRADED).

Two structural results follow. The index is broad but weak: face area dominates, and in
exploratory analysis only 6 of 2,520 dial–parcel correlations reach the threshold on the
statistic it was derived for, none securely. And the two tracks disagreed without either
being wrong: cutting has a frontal and an auditory signature, and real cinema shows only
the auditory one at a detectable size. Exploratory follow-ups find the frontal miss needs
no film-specific explanation, and that speech, absent from the dials, explains much of the
auditory variance the visual dials leave.

Exploratory analysis of the index bounds inversion. The model's responses to these films
vary along about three dimensions, and an index fitted to shuffled labels is as
concentrated, so the reachable set is limited by the sensor before technique; what is
specific to technique is narrow, chiefly that face area leads the dominant axis. Inversion
is projection, many-to-one, and a controller on this index would move towards faces.

We also report method failure as evidence: silent pipeline failures, an analysis whose
numbers reproduced while its reading did not, and a registration that misstated its own
compliance and was corrected by formal amendment.

---

## 1 · Introduction

### 1.1 The question

A director changes the cut rate and something changes in the audience. That much is
uncontroversial and is the working assumption of every editing manual written. What
is missing is a *map*: which techniques move which parts of cortex, by how much, and
with enough structure that the relation can be run backwards.

Backwards is the point. An index from technique to response is descriptive; the
thesis this programme is built toward is **inversion** — specify a target response
profile, and derive the technique that reaches it. That is a control problem, and it
requires three things the current literature does not supply together: many dials
measured on the same material, a response measure dense enough to distinguish
cortical regions, and enough samples to fit a model rather than compare two
conditions.

### 1.2 Why an encoding model, and what that costs

Collecting fMRI on enough film segments to fit such a model is out of reach for this
project. The substitute is an encoding model that predicts fMRI from stimulus.
TRIBE, the Algonauts 2025 winner (d'Ascoli et al., 2025; Scotti & Tripathy, 2025), predicts
cortical fMRI responses from video, audio and time-aligned text. It was evaluated in the
competition on the 1,000 parcels of the Schaefer atlas; the released model, as run here,
returns 20,484 fsaverage5 vertices, which this paper reads out at the 180 areas of the
HCP-MMP1 (Glasser) parcellation.

Using it as an instrument has one large advantage and one large cost.

The advantage is that **the measurement is deterministic**, and this is established
empirically rather than assumed from the architecture. TRIBE was trained on several
subjects; the Space calls the released checkpoint through the package's default
prediction path, and how that path treats subjects (one, or an average) was not
inspected. What was checked is the output: an independent re-run in stage 00 reproduced
parcel values to two decimal places (LO2 +2.43 vs +2.43, A5 +2.37 vs +2.38, STSdp +2.04 vs
+2.04), and stage 03b's identity test reproduced stage 03's values exactly (maximum
|Δ| 0.0). There is no trial-to-trial noise, no
subject variance, no scanner drift. A correlation computed against these values is
not attenuated by measurement unreliability, which is the dominant limit on effect
sizes in real naturalistic-imaging work.

The cost is **validity**. We are measuring a model's behaviour, and the model's
agreement with real cortex is a published, finite number. Section 3.2 turns that
number into a quantitative scope condition rather than leaving it as a caveat.

### 1.3 Relation to the wider project

This research sits inside a film production — *The Simulated Viewer*, a ten-minute
short in which a machine is instructed to make a simulated cortex respond as strongly
as possible and drifts, over ten minutes, from showing the world to showing faces.
That drift is a hypothesis this research tests, not a result it relies on. The
production brief adopts one rule that this paper inherits: **nothing is claimed
as tested that has not been tested here, and every figure is either sourced to a
primary document or explicitly marked unmeasured.** The subject invites overclaiming
— a system that predicts brain activity is very easy to describe dishonestly — so the
distinction is structural rather than decorative.

### 1.4 Contributions

1. A **justified** rather than conventional effect-size threshold for encoding-model
   studies, obtained by propagating the model's published accuracy through to the
   claim being made — a heuristic with a stated range, not a bound (§3.2).
2. A **two-track design** separating what observational data can establish
   (association across real cinema) from what only controlled generation can
   (isolation of covarying dials), with the boundary stated in advance.
3. A corpus decision made by **overturning our own prior assumption on evidence**
   (§4.1), including the finding that animation — proposed as the corpus on
   availability grounds — is the *minimum*-variance case for the covariance-breaking
   the design requires.
4. A **reconciliation of observational and controlled measurement** of the same dial.
   The registered observational index and a controlled ladder disagreed about where cut
   rate acts; constructed tests then showed neither was wrong — cutting has a frontal and
   an auditory signature that separate under different kinds of join, and real cinema
   shows only the auditory one at a detectable size (§5.5–§5.7).
5. A report of **silent-failure modes** in this class of pipeline, and the practices
   that surfaced them (§7).

A detectability classification (§4.6) separates "this dial did not move the sensor" from
"this dial never varied enough to test"; it is a method note rather than a contribution.

---

## 2 · Hypotheses

The programme is a chain. Each link gates the next and is permitted to break it.

| | Hypothesis | Status |
|---|---|---|
| **H0** | TRIBE discriminates content — different kinds of scene produce different parcel profiles, in anatomically interpretable directions | ✅ **Supported** (stage 00) |
| **H1** | Cinematographic *technique* moves the predicted response with content held constant | ✅ **Supported** (stage 01, cut rate only) |
| **H2** | Across real cinema, measured technique dials predict parcel-level response profiles, recoverably by penalised regression | ✅ **Supported** (stage 02) — 14/14 dials, 101/180 parcels. But only 9 parcels reach the SESOI on the registered statistic, and 6 of 2,520 dial–parcel pairs on the marginal statistic it was derived for (§5.3.5) |
| **H2b** | The controlled cut-rate result of stage 01 reappears observationally | ❌ **Not supported** (stage 02) — IFJa at its null; the one surviving cluster parcel has zero cut-rate weight. **Explained by stage 03 (§5.5)**: the observational index recovered the auditory half of the cut effect; the frontal half is not detected in the corpus, where §5.6–§5.7 put it at a size three films could not detect |
| **H3** | At least some of those associations are causal, demonstrable by holding all dials fixed and moving one | ✅ **Supported** (stage 03, verdict **PARTIAL-A** against the pre-fixed table) — cutting alone, content fixed by construction, drives IFJa / IFSp / 8C up and A4 / A1 / MBelt down on generated footage in both speech arms; the no-speech arm misses the 0.9 bar on three cluster parcels by ≤ 0.03 at *n* = 5 |
| **H3′** | The frontal response to cutting is a response to temporal discontinuity, to a change of scene, or both | **Graded** (stage 03b, verdict **GRADED**) — a hard cut within a scene carries 18–44% of the frontal effect and a change of scene with no hard cut 48%, close to additively; the auditory response follows the hard cut. The pure discontinuity (encoder-artefact) form is weakened; a response to any large visual change is not excluded |
| **H4** | The mapping can be inverted — a target profile selects a technique, and the achieved profile matches | Not started (stage 04). **Bounded in advance by §6**: the reachable set is ~3-dimensional — a property of the sensor's response space, which technique cannot exceed — so inversion is projection onto it, and the inverse is many-to-one |

**H2b deserves emphasis.** It is the only place in the design where the controlled
and observational tracks can contradict each other. If cut rate moves the sensor on
identical footage but shows no association across real cinema, one of the two results
is wrong, and that must be resolved before anything is built on either. The
pre-registration names this outcome **PARTIAL** and calls it the most important
possible finding — which is why §4.5 records that we raised the sample size
specifically so that this check would be able to fail informatively. It did fail, and
stage 03 (§5.5) then showed that neither track was wrong: cutting has a frontal and an
auditory signature, and the observational corpus shows only the second.

---

## 3 · Theoretical framework

### 3.1 The instrument

TRIBE is a trimodal transformer encoder that fuses representations from pretrained
unimodal backbones — V-JEPA 2 for video, Wav2Vec2-BERT for audio, Llama for text —
and predicts fMRI response across cortical parcels. Its training corpus is 121 hours
of video, of which **64.5 hours is the sitcom *Friends***; the remainder is
Memento10k real-world clips, silent YouTube footage and live-action features.

Two consequences follow and are load-bearing throughout.

**The visual diet is narrow.** A model whose training was dominated by a
multi-camera sitcom shot largely in medium two-shots on a fixed set may have poor
sensitivity to exactly the variation this project intends to use. That is not a
rhetorical worry; it is why stage 00 exists as a gate rather than a formality.

**The encoding head is the exposure, not the backbone.** V-JEPA 2 was pretrained
broadly and has almost certainly seen material far outside TRIBE's fMRI-fitting
corpus. The feature→BOLD mapping, however, was fitted only on that corpus. Material
outside it — animation, generated video, and to a lesser extent 1930s Technicolor —
is out-of-distribution for the head specifically, and the head **fails silently**,
returning plausible numbers rather than raising.

Operational facts, established by measurement in stage 00 and recorded so they are
not re-derived:

| | |
|---|---|
| Output rate | exactly **1 Hz** — `timeline (61, 20484)` over a 60.0 s span = 1.000 rows/s |
| Vertices | 20,484 (fsaverage5) |
| Parcels | HCP-MMP1 (Glasser): 181 returned; index 0 is `???` and is dropped, leaving **180 usable** |
| Throughput | ~10 min per 60 s clip on an A10G — roughly **10× slower than real time** |
| Determinism | reproduces to 2 d.p. across independent runs |

### 3.2 The scope condition, stated quantitatively

The dependent variable is TRIBE's prediction, not measured cortex. The link between
the two is published (d'Ascoli et al., 2025: Algonauts 2025 leaderboard, eq. 1 and fig. 3):

| | Pearson *r* |
|---|---|
| In-distribution (Friends season 7) | 0.3195 |
| **Out-of-distribution** | **0.2146** |
| Noise-ceiling-normalised | 0.54 ± 0.1 (54% of explainable variance) |
| Best regions (auditory and language cortex) | "near the noise ceiling"; no figure given |

Our corpus — Technicolor features from 1937–1951 — is out of distribution, and
arguably further out than the challenge's own out-of-distribution films, so 0.2146
should be read as an optimistic upper bound for our case.

This is a bottleneck, and it can be propagated. If a dial *D* correlates with a
TRIBE parcel prediction *P* at *r*<sub>DP</sub>, and *P* tracks real BOLD *Y* at
*r*<sub>PY</sub>, then under a simple mediation reading the dial's implied
association with real cortex is approximately *r*<sub>DP</sub> × *r*<sub>PY</sub>.

To imply even a conventionally small real effect of *r* = 0.10:

| via | *r*<sub>PY</sub> | required *r*<sub>DP</sub> |
|---|---|---|
| raw out-of-distribution accuracy | 0.2146 | 0.10 / 0.2146 = **0.47** |
| noise-ceiling-normalised accuracy | 0.54 | 0.10 / 0.54 = 0.19 |

**We adopt SESOI = *r* ≥ 0.5**, the conservative row rounded up, and it is the value
the registration fixed. The generous row is recorded so the choice is visible rather
than buried: it would put the threshold near 0.19 and demand roughly 200 segments.

**This is a justified heuristic, not a bound, and its range is wide.** It follows
Lakens' requirement (Lakens, 2022) that a smallest effect size of interest be *justified*
rather than asserted, and the justification is the measurement chain itself — better anchored than a
convention or a resource constraint, but looser than the table's two decimal places
suggest, for three reasons. First, *r*<sub>DY</sub> ≈ *r*<sub>DP</sub> × *r*<sub>PY</sub>
holds only if the prediction fully mediates the dial's relation to cortex and TRIBE's
error is uncorrelated with the dial; nothing establishes either, so the true implied
correlation can be larger or smaller than the product. Second, 0.2146 is an average over
parcels. TRIBE predicts some regions far better: its authors report the highest scores in
auditory and language cortex, "near the noise ceiling" (d'Ascoli et al., 2025, fig. 3b),
which includes the auditory parcels this paper's cut-rate results rest on. A parcel-wise
propagation would therefore put the required *r*<sub>DP</sub> anywhere from about 0.10 in
those regions to 0.47 at the raw average; no per-parcel figures are published, and none
were measured here. Third, the
threshold is derived for a *marginal* correlation between one dial and one parcel, so it
applies to that quantity and only approximately to anything else; §5.3.5 reports both.

What the heuristic does support is the direction it pushes: towards a **higher**
threshold and therefore a **cheaper** study. A dial reaching only *r* = 0.3 in a
measurement with no noise in it would be worth little once passed through a 0.21
bottleneck. What it does not support is reading a result just under 0.5 as negligible or
one just over it as meaningful. §4.5 records the sample-size headroom taken against its
looseness.

### 3.3 Prior art, and where this design departs from it

**Kauttonen et al. (2015)**, *Optimizing methods for linking cinematic features to
fMRI data*, NeuroImage 110:136–148, is the closest methodological precedent. They
related 37 cinematic features to free-viewing fMRI of a single 14-minute art film,
combining elastic-net regularisation with ICA and inter-subject correlation, and
found elastic net more sensitive than PLS or unregularised regression precisely
because the feature set was large and heavily intercorrelated.

We take the regularisation choice directly from them. **The null does not
transfer.** Their design regresses feature *timeseries* against a continuous BOLD
timeline within one film; ours regresses aggregate dial values against aggregate
parcel values *across segments*. That difference propagates: it makes segment-label
permutation the correct null (§4.7), and it substantially weakens the objection that
fixed windows straddle scene boundaries (§4.3).

**Aliko et al. (2020)**, the Naturalistic Neuroimaging Database (*Scientific Data*),
scanned 86 participants watching one of **ten full-length feature films** across
diverse genres. It is the strongest precedent that a multi-film, whole-feature corpus
is an ordinary design rather than an invention.

**Leipold et al. (2024)**, *Between-movie variability severely limits generalizability
of "naturalistic" neuroimaging* (bioRxiv 2024.12.03.626542, version 1; retitled in
version 3), is the most consequential
for us. Across 112 participants watching **eight animated movies** over 210
Brainnetome parcels, whole-brain inter-subject correlation differed significantly
between films — *F*(7,385) = 4.65, *p* < 0.001, η²<sub>G</sub> = 0.048 — and the
differences were not driven by one atypical film. Their downstream analysis found
associations in **non-overlapping regions for nearly every movie**: of eight films,
exactly one parcel was shared between two.

Their conclusion — that "using a specific movie in neuroscience should be treated
similarly to using a particular task" — supports two of our decisions and imposes one
limitation. It supports the multi-film corpus and the within-film centring. It
imposes the requirement that **our index be reported as corpus-conditional**: three
films is enough to break dial covariance, not enough to claim film-independence.

The same paper also supplied the argument that removed animation from our corpus
(§4.1), because they chose animated films precisely for being "stylistically and
thematically similar" — a deliberate minimum-variance condition.

**Baldassano et al. (2017)** and **Geerligs et al. (2022)** establish that neural
event timescales form a partially nested cortical hierarchy — short states in early
sensory regions, long states in angular gyrus and posterior medial cortex. This is
the reason no single event-aligned segmentation can be correct for all 180 parcels
(§4.3).

### 3.4 What a model-based sensor can and cannot license

Every result in this paper is a statement about TRIBE's predictions, and TRIBE is a stack
of pretrained encoders — a video encoder, an audio encoder and, when enabled, a language
model — feeding a learned mapping onto cortex. That architecture admits a reading of any
result that cognitive neuroscience would not entertain for a brain: **the response may be
a property of an encoder's representation, passed through the mapping, rather than of
anything cortex would do.** A cut is a large discontinuity in a video encoder's input; if
the mapping happens to route large discontinuities to inferior-frontal parcels, "frontal
cortex responds to cutting" would be true of the sensor and uninformative about cortex.

This alternative cannot be excluded by measuring the sensor alone, but it can be made
specific and tested against variants it predicts differently. Its pure form — the sensor
maps temporal discontinuity to frontal cortex and nothing more — predicts that a change of
scene without a hard cut does nothing, and that a hard cut does the same whatever is
interrupted. Stage 03b tests exactly those predictions (§5.6). Its broad form — a response
to any large change in the encoder's input, gradual or abrupt — is not separable from
"change of scene" by any design in this paper. Results are therefore read as properties of
the sensor first, and as hypotheses about cortex only where a variant has been tested and
the encoder-artefact reading has been made to predict differently; §3.2's threshold
bounds what any of them could imply for real cortex.

---

## 4 · Methods

### 4.1 Corpus, and an assumption overturned

The corpus requirement follows from the covariance problem. Directors covary their
dials deliberately — fast cutting arrives with camera movement and high contrast,
close-ups arrive with shallow focus — so within a single film the dials are
confounded by intent. **Varying the director is the cheapest way to break that
covariance without a lab.**

The corpus went through two rejections, both recorded because the reasoning matters
more than the outcome.

*His Girl Friday* (1940) was proposed as the dialogue picture against a landscape
picture. **Rejected: it is black and white.** In a corpus where every other film is
in colour, saturation becomes a perfect proxy for film identity, and any
colour-correlated parcel association would in fact be a which-film association
carrying era, genre, director and subject matter with it.

Animated Technicolor features were then adopted as a working assumption, recorded
explicitly as an assumption rather than a finding, on the grounds that public-domain
animated colour titles are more available than live-action ones and that animation
offers strong deliberate colour with less confound from lens and stock.
**Both halves of that failed.**

The availability premise is false. A survey of the Internet Archive verified **six
public-domain live-action Technicolor features against two animated colour features**,
one of the latter carrying French intertitles. What is abundant in the animation
collections is colour *shorts* — Popeye one-reelers of 7–9 minutes — not features.

The second failure is more interesting, and comes from Leipold et al. They selected
animated movies *because* animation is stylistically and thematically homogeneous —
an ideal limiting case for measuring between-movie variability. **Animation is
therefore the minimum-variance condition, which is the opposite of what a corpus
assembled to break dial covariance requires.** An all-animated corpus would have been
the worst available instrument for this specific job, independently of whether TRIBE
can see animation at all.

The adopted corpus is three public-domain live-action Technicolor features:

| Film | Year | Contributes |
|---|---|---|
| ***Nothing Sacred*** (Wellman) | 1937 | dense overlapping dialogue, interiors, fast cutting, medium shots |
| ***Jungle Book*** (Korda) | 1942 | landscape, exteriors, slow cutting, wide shots |
| ***Royal Wedding*** (Donen) | 1951 | sustained camera movement, high-key luminance, moving long takes |

***Nothing Sacred* is the direct colour replacement for *His Girl Friday*** — the
same object, a fast-talking 1937 newspaper satire, in three-strip Technicolor. It
fills the role the rejected film was chosen for, with the black-and-white confound
removed.

Three films rather than four: more films break covariance better, but fewer films
leave more segments per film for within-film centring to estimate a stable film mean.
At the planned sample size, three films gives ~23 segments each; four would give ~17.

**Colour was verified by measurement, not by provenance.** A documented Technicolor
production can still reach an archive as a black-and-white dupe, and a pixel format
proves nothing — a greyscale encode is still `yuv420p`, merely with flat chroma
planes. Twelve frames per print were sampled across the middle 90% of running time
(excluding titles and credits, often monochrome even in colour films) and measured on
mean HSV saturation, Hasler–Süsstrunk colourfulness, and mean per-pixel channel
spread:

| Print | mean saturation | colourfulness | chroma | verdict |
|---|---|---|---|---|
| Nothing Sacred | 81.9 | 20.5 | 10.5 | COLOUR |
| Royal Wedding | 85.5 | 31.0 | 16.3 | COLOUR |
| Jungle Book | 115.6 | 27.2 | 14.6 | COLOUR |

Thresholds were saturation > 15 and chroma > 3; a true greyscale print sits at
essentially zero on both.

### 4.2 Encode normalisation

The verified prints spanned 640×480 to 1480×1080 with differing audio codecs (AAC on
two, AC-3 on one). This is a confound, and a subtle one.

`cinemetrics.py` measures depth of field as a **centre-versus-surround sharpness
ratio**, and its colour and contrast statistics move with encode quality. Within-film
centring removes a per-film *mean*; it does **not** remove a resolution-dependent
difference in a dial's *variance*. Left uncorrected, "depth of field" would be partly
a proxy for which print happened to be downloaded.

Every segment is therefore re-encoded identically before any dial is measured: scaled
to a common 720-line height with the same Lanczos scaler, libx264 at CRF 20,
`yuv420p`, and AAC 128 kbps 48 kHz stereo. All three sources are natively 24000/1001
fps, so no frame-rate conversion is applied. Audio is preserved — TRIBE has an audio
branch, and both prior runs kept it.

Segments are re-encoded rather than stream-copied. A stream copy begins at the
nearest keyframe and silently yields a clip that starts late or runs short, and a
short clip is precisely the failure mode that returns confident noise.

### 4.3 Segmentation: fixed 60 s, non-overlapping

Three reasons, in order of weight.

**The unit of analysis is the segment, not the timepoint.** Stage 02 regresses a
segment's aggregate parcel vector on its aggregate dials. A scene change inside a
segment is therefore not a confound — it is *measured*, by the cut-rate dial, and
both sides of the regression see the same 60 seconds. The straddling objection is
serious for a timepoint-level design such as Kauttonen's; it does not transfer to a
cross-segment design.

**No event-aligned segmentation is correct for all 180 parcels.** Given a nested
hierarchy of neural state durations (Baldassano 2017; Geerligs 2022), windows aligned
to boundaries defined at one timescale are misaligned for every parcel operating at
another.

**Variable-length windows fight the sensor.** TRIBE has a ~30 s floor and a 100 s
training window. Fixed 60 s sits comfortably inside that band. Shot-aligned windows
vary in length, and some would land near the floor — where the model returns diffuse
output *without erroring*.

Head and tail of each film are skipped (5% each end). The scene-boundary count the corpus
plan specified as a diagnostic was never implemented — `cinemetrics.py` counts cuts without
classifying them as within- or between-scene (§7). An exploratory between-scene cut count
was added later for all 244 segments (`02-index/scene_switches.py`: the cut detector
unchanged, each cut scored by the HSV-histogram distance between the adjacent shots) and
is used in §5.7.1 as a diagnostic, not a registered dial.

This yields **244 segments**: Jungle Book 95, Nothing Sacred 66, Royal Wedding 83.

### 4.4 Dials

`cinemetrics.py` measures 14 dials per segment using OpenCV and NumPy only — no model
weights, no network:

| family | dials |
|---|---|
| cutting | `cuts_per_min`, `mean_shot_len_s` |
| camera | `camera_jitter`, `camera_zoom`, `camera_pan` |
| lighting | `median_luma`, `contrast_p5_p95`, `shadow_frac` |
| colour | `colourfulness`, `mean_saturation`, `warm_cool` |
| shot scale | `face_area_frac`, `face_hit_rate` |
| focus | `dof_ratio` |

Shot scale uses YuNet face detection rather than a Haar cascade, because Haar fires
on texture *consistently* — a false positive appears on every frame of a static shot,
and no temporal filter removes it — whereas YuNet returns a confidence score that
does. Where no face is detected at all (16 of 244 segments), `face_area_frac` is
encoded as 0.0 and `face_hit_rate` carried alongside, so that "no face present"
remains distinguishable from "a small face" rather than being conflated by a bare
zero.

Measurement cost was **~28 s per 60 s segment at 720p**, measured on the real corpus.
An earlier planning figure of ~2 s per clip, inherited from shorter and smaller test
material, was wrong by roughly 14× and has been corrected in the planning documents.
Frame stride is held at 1: raising it would halve the cost, but cut detection compares
adjacent frames, and cut rate is both the dial stage 01 established and the one stage
02 must replicate.

### 4.5 Sample size

Power for a Pearson *r* at α = .05 two-tailed, with 3 degrees of freedom lost to
within-film centring across three films. The table is indicative: it is computed for a
marginal correlation, while the registered model is a 14-dial elastic net whose
effective degrees of freedom are different and unknown, so "80% power" below is a
planning figure, not an exact property of the test that was run:

| *n* segments | *r*=0.3 | *r*=0.4 | *r*=0.5 | *r*=0.6 | min *r* at 80% power |
|---|---|---|---|---|---|
| 20 | 0.21 | 0.35 | 0.54 | 0.74 | 0.63 |
| 40 | 0.44 | 0.70 | 0.89 | 0.98 | 0.45 |
| 60 | 0.62 | 0.88 | 0.98 | 1.00 | 0.36 |
| **70** | 0.68 | 0.92 | **0.99** | 1.00 | **0.33** |
| 100 | 0.85 | 0.98 | 1.00 | 1.00 | 0.28 |

**Target: *n* = 70** (Jungle Book 24, Nothing Sacred 23, Royal Wedding 23).

The SESOI of 0.5 would be satisfied by *n* = 40, which has 89% power there. The
headroom above that is deliberate, and one component of it was **not** planned but
forced by measurement.

At *n* = 60, the two cut-rate dials came in at **0.79 and 0.80 power — below the 80%
floor** — because roughly a third of cut rate's variance lies *between* films and
within-film centring removes it (§4.6). Cut rate is the dial that pass criterion 2
requires to replicate. At 60 segments a null on cut rate could not have been
distinguished from a failure to detect, so **the replication check would have been
unable to fail informatively**, and the PARTIAL verdict the design calls its most
important possible outcome would have been unearned. Raising *n* to 70 brings both
cut-rate dials to 0.85 and 0.86 and puts all 14 dials over the floor. The fix cost
$1.70.

Two further reasons for headroom, both of which would otherwise bite silently:

1. The mediation estimate in §3.2 is first-order. If the true bottleneck is kinder
   than 0.2146, the SESOI belongs lower, and 70 segments retains 80% power down to
   *r* = 0.33.
2. **The pass criteria's quantity is not a marginal correlation.** It is a
   cross-validated predictive *r* for a parcel from the whole dial set — a
   multivariate quantity whose null is established by permutation, not by the table
   above. The power table is indicative, not exact.

### 4.6 Detectability: no dial is dropped

A conventional pipeline drops predictors with too little variance to test. **That
step was specified, then removed as wrong on its own terms.**

It saves nothing: GPU cost is per *segment*, and `cinemetrics.py` returns every dial
in one pass regardless of intent, so dropping a dial saves neither GPU nor
measurement time. And it would create a reporting error the design explicitly
forbids. A dropped dial and a tested-null dial become indistinguishable in the
write-up, when the pre-registration requires that a dial which does not move the
sensor be reported with equal prominence as a finding. **"Did not move the sensor"
and "never varied enough to test" are different results and must not be merged** —
the first is evidence, the second is absence of evidence.

Every dial is therefore measured, entered, and reported, each carrying a
pre-registered label derived from its realised range. The label is computed, not
chosen by eye. A dial's spread surviving within-film centring is
*s* = within-film SD / total SD; restriction of range then attenuates a true
correlation *r* to

> *r*<sub>obs</sub> = *r·s* / √(1 − *r*² + *r*²*s*²)

| range retained | a true *r* = 0.5 is observed as |
|---|---|
| 100% | 0.50 |
| 70% | 0.37 |
| 50% | 0.28 |
| 30% | 0.17 |

**TESTED** means *r*<sub>obs</sub> at the SESOI still yields ≥ 80% power at the
planned *n*; a null there is a real null. **UNDERPOWERED** means it does not; a null
there is uninformative and must be reported as untested, never as evidence of
absence.

A known limitation of this metric is recorded because it did not bite rather than
because it cannot: *s* is a **ratio**, so a dial with almost no absolute variance
whose remnant survives centring scores *s* ≈ 1.0 and is labelled TESTED. The metric
measures what centring costs, not whether anything was there to begin with.
`camera_pan` presented exactly that appearance — its SD printed as `0.000` — and was
checked directly rather than trusted: values reach 2.9 × 10⁻³ of frame width per
frame, a pan across 421% of the frame over 60 s, with 27 static segments and 48
distinct values. A real dial; the `0.000` was a formatting artefact of `%.3f` applied
to a 2 × 10⁻⁴ number. Future dials should be checked on absolute spread as well as on
*s*.

### 4.7 Model, null, and segment selection

Per parcel, a cross-validated elastic net regresses the parcel's *z* on the dial set.
Elastic net rather than OLS follows Kauttonen: the dial set is multicollinear by
construction (§5.3.3), and unregularised regression is unstable there.

The null is **permutation over segment labels**, 1,000 permutations. This is a
regression across segments, not a map-to-map comparison, so a spin test is the wrong
null; spin tests become appropriate only when comparing resulting technique-maps
against external maps such as Neurosynth terms, which is stage 03 and beyond. (An
earlier version of the roadmap specified a spin test here; that was wrong and has
been corrected.)

Dials and parcels are centred **within film**, always. This removes any per-film
constant, and is what stops saturation — or any other dial with a large between-film
offset — from becoming a proxy for film identity.

**Selection.** All 244 segments are cut and dialled, both free. The 70 scored are
chosen by stratifying on cut rate within each film, then taking, within each stratum,
the segment whose standardised dial vector is farthest from those already selected —
a maximin coverage design that spreads every dial rather than only the stratifying
one. The selection retains 83–100% of each dial's full range.

This is a design choice on **predictors**, made before any parcel value exists.
Selecting on outcomes would be p-hacking; selecting on stimulus properties is
ordinary experimental design. The genuine caveat is different and is recorded in
advance: deliberately spreading a dial inflates its variance relative to a random
sample, so **estimates are design-conditional** and must not be read as "the effect
in typical cinema". Stratifying across quantiles rather than taking extreme groups
keeps that mild.

### 4.8 The no-peeking constraint, and why this paper stops where it does

Collection is complete at **70 of 70 segments** and the registered test has been run
once, on the complete set, after the analysis plan was registered at `osf.io/dg7fe`.
The account below describes the constraint as it was operated, and one place where we
described our own compliance wrongly.

This is not fastidiousness. Peeking at an accumulating dataset and stopping when it
looks good inflates false positives, and a programme whose headline finding turned
out to be an artefact of when its authors chose to stop would be worthless. The
pre-registration therefore states that the statistical test runs **once, on the
complete set**, that interim looks are exploratory, and that anything seen in one may
not be reported as a finding.

Between-batch checks verify **pipeline health only**: 180 parcels per clip, no NaN,
no implausible *z*, filenames aligning between the dial table and the parcel table.
For completeness, the batch-0 health check also inspected pairwise whole-vector
correlations between four clips — to confirm the sensor discriminates at all rather
than returning one vector for everything. None of these is a dial→parcel
relationship, so none is an outcome peek.

**One pre-specified exception** exists, and it is a resource decision rather than a
test. **It was invoked, and the registration said otherwise.** The registration
asserted in three places that the futility script had never been executed. It had —
once, on 6 September 2026 at 30 of 70 segments, returning CONTINUE. The script is
written to print a verdict and nothing else, so no dial, parcel or coefficient was
produced; the study proceeded exactly as it would have, and no threshold or
specification moved. The error was ours and its mechanism is instructive: we checked
the claim by searching the repository and its logs for the script's output, found
nothing, and read absence of a record as absence of execution. The script was
untracked and had printed to a terminal. The registration was amended through OSF's formal update process on 20 September 2026 —
the original remains visible as version 1, and both stay under embargo until September
2027 — and §7 treats this as a method failure rather than a footnote. It was also *restated*, because the original was arithmetically inert. The
original rule — "if after 20 segments no dial reaches |*r*| > 0.3, stop" — fires about
one time in five under pure noise: at *n* = 20 the null probability of a single dial
exceeding |*r*| = 0.3 is 0.247, and across six dials the probability at least one does
so is 0.82. A rule that almost never triggers is not a stopping rule. The restated
version runs the permutation null at 30 segments and stops only if no dial has any
parcel whose cross-validated *r* exceeds the 95th percentile of its own permutation
distribution *uncorrected* — a real threshold with a real false-trigger rate, using
the same machinery as the final test, and deliberately lenient enough to stop only a
study showing nothing at all.

### 4.9 Infrastructure

Scoring runs on a duplicated Hugging Face Space (`alecnpacey/tribe-probe`) on A10G
Small hardware at $1.00/hr, approximately $0.17 per 60-second segment. The Space's
reference environment is used — its `tribev2` fork, pinned transformers, patches and
windowing — but its interactive interface is replaced, so the modules are driven
directly rather than through a UI.

Inference runs in video mode with `audio_only=True`. This skips ASR and the gated
Llama-3.2-3B text branch, which the upstream documentation names as the path for
validating metrics before Meta licence approval; the model tolerates the missing text
modality through modality dropout. **All results are therefore video + audio only,
with no text branch.**

Checkpointing is per clip: the Space prints each segment's 180 parcel values to
stdout the moment it finishes, so a run that dies half-way still banks its completed
clips. Resume is by omission — only segments with no saved vector are uploaded, so
nothing is ever scored twice. The Space's filesystem is wiped on pause, so results
survive only in the log stream until harvested, and harvesting pauses the Space to
stop billing.

**Spend, once.** Scoring ran on an A10G Small at $1.00/hr; generation on fal. Figures are
from each stage's RESULT and the run log; where they disagree, both are given.

| stage | generation | scoring | note |
|---|---|---|---|
| 00 · probe | — | ≈ $2.50 | ~2.5 h, mostly spent on the failures of §7 |
| 01 · gate | — | ≈ $0.85 | five conditions |
| 02 · index | — | ≈ $16 | against an estimate of $11.90; includes the $1.70 of raising *n* to 70 |
| 01b · transfer | $3.60 | ≈ $0.50–0.65 | RESULT and log differ on scoring |
| 02b · generalisation | — | $0 | reuses 01b's vectors |
| 03 · isolation | $3.60 | ≈ $2.20 | generation includes one face-base regeneration |
| 03b · discontinuity | $0 | ≈ $7.60–10.30 | session 1 overspent (≈ $5.50–8.20; exact figure on the billing page only), sessions 2–3 ≈ $2.10 (§7) |
| text-branch rescoring, 13 Sep | — | ≈ $3.15 | 189 min, 0 / 12 results; not separately recorded, estimated at the hourly rate |
| all exploratory analyses | — | $0 | local |
| **total** | **$7.20** | **≈ $32.80–35.65** | **≈ $40–43 for the programme to date** |

### 4.10 Ladder designs and their null

Stages 01, 03 and 03b are *ladders*: one dial set at five levels (1, 3, 7, 15 and 31
cuts) with everything else fixed, each level scored once. Their statistics are computed
across the five levels — Pearson *r* of each parcel against log cut count, the count of
parcels with |*r*| > 0.9, and in 03b a cluster's slope relative to a reference ladder.

**The null permutes the level labels**, not the parcels (`ladder_count_null.py`; 03b's
evaluator uses the same scheme). Five levels have 120 orderings; each is applied to the
whole 180-parcel response and the statistic recomputed, so the parcels' correlation
structure is preserved under the null. Parcels are not independent across a ladder — the
response moves along close to one direction, which we report as the participation ratio
of the five level profiles (1 to 4) — so a null that treats 180 parcels as 180 trials
overstates any count. Two consequences are properties of the design, not of any result.
**There is a *p*-floor**: an ordering and its mirror image give the same |*r*|, so no
count can do better than *p* = 2/120 = 0.017 (one-sided slope statistics, as in 03b, reach
1/120 = 0.008). And a design that reaches the floor cannot distinguish a strong effect
from a very strong one. Stage 01's result used log₂ of cut count and stages 03 and 03b
natural logs; Pearson *r* is invariant to the base, and 03b's slope ratios are ratios of
slopes on the same base.

---

## 5 · Results

### 5.1 Stage 00 · Discrimination probe

*Licenses: TRIBE separates kinds of content along a reciprocal face/place axis. It does
not license attributing the face response to faces rather than to speech.*

**Question.** Does TRIBE distinguish kinds of content at all? Everything downstream
assumes it does; if the top-ranked regions were the same for a landscape, a crowd and
a close-up face, no downstream design could rescue the programme.

**Design.** Three 60-second clips, all drawn from **one film** (*Jungle Book*, 1942) —
deliberately, so that stock, grade, era, grain and encode are held constant and
content is the only variable. Three unrelated stock clips would have confounded
content with everything about how each was shot and digitised.

Timestamps were chosen by measurement, not by eye. An initial visual pass picked
badly: the first face candidate contained *fewer* faces than the crowd clip, which
would have made the test meaningless. The film was then scanned with YuNet at
4-second intervals (1,574 samples) and windows ranked objectively, producing a clean
gradient on face area (24.1% → 1.5% → 0.6%) with face *count* inverted between the
face and crowd clips (1.8 vs 3.3).

**Criteria, fixed before the run.** (1) Separation: mean pairwise top-10 Jaccard
overlap < 0.60. (2) Direction: at least two of three clips rank their expected region
family higher than the others do.

**Result: PASS on both.**

Mean pairwise top-10 Jaccard overlap **0.15**:

| pair | overlap |
|---|---|
| crowd vs face | 0.05 |
| face vs landscape | 0.05 |
| crowd vs landscape | 0.33 |

Direction was correct on **all three** clips, not two:

| clip | top parcels | reading |
|---|---|---|
| face | A5, STSdp, 55b, V8, A4, PEF, PBelt, IFSp, IFJa, PIT | auditory belt/parabelt, superior temporal sulcus, language network |
| landscape | VMV2, VMV3, V3B, V8, V4, V3CD, IPS1, IP0, V6A, LIPv | scene-selective ventromedial visual, parahippocampal neighbourhood |
| crowd | LO2, V4t, V7, IPS1, FEF, LIPv, VIP, V6A, V4, V8 | intraparietal / frontal-eye-field, lateral occipital |

**The stronger result was the full vector, not the top ten.** Retaining all 540 values
revealed a reciprocal **double dissociation**:

| chain | face | landscape | crowd |
|---|---|---|---|
| A5 (auditory) | **+2.37** | −3.26 | −0.38 |
| STSdp (social/voice) | **+2.04** | −3.99 | −0.74 |
| VMV2 (place) | −2.26 | **+2.83** | −0.17 |
| PHA2 (parahippocampal) | −3.46 | **+1.26** | −2.08 |
| PHA1 | −2.65 | **+1.01** | −1.77 |

Two systems trade places in opposite directions, and **crowd sits between them on
both chains** — a graded middle condition rather than an arbitrary third point. That
is a considerably harder pattern to produce by noise or misalignment than three-way
separation alone. Whole-vector correlations: landscape vs face *r* = **−0.098**
(orthogonal), landscape vs crowd +0.455, crowd vs face +0.453.

**Caveats, carried forward.** The face clip is two people *talking* with the audio
branch live, so auditory and language parcels may be responding to speech rather than
to faces — the discrimination result stands, the *attribution* to faces does not. The
landscape clip is environment-dominant, not people-free. The crowd clip drifts in its
second half. All three come from one film at 640×480 in a dim 1942 grade, so
generalisation across stocks and eras is not yet shown. The text branch was skipped.

### 5.2 Stage 01 · Cut rate on identical footage

*Licenses: technique alone — cut count on identical footage — moves the sensor, most
strongly in inferior-frontal cortex. One dial, one scene pair, a 2.1× effective range.*

**Question.** Does cinematographic *technique* move the sensor with content held
constant? This is the first genuine test of the thesis and the first thing capable of
killing it.

**Design.** The two most orthogonal clips from stage 00 (face and landscape,
whole-vector *r* = −0.098) intercut at five rates: 1, 3, 7, 15 and 31 added cuts.
**Every condition contains exactly the same 30 s of each scene.** Colour, luminance,
motion, subject matter and audio are all held; only the number of cuts differs.

Cut rate was chosen as the gate rather than as part of the index because it is the
only dial that can be varied with content perfectly constant, and because editing
carries the largest documented effect of any cinematographic manipulation on viewers:
what a shot is cut together with shifts its rated valence at η²ₚ = 0.715, replicated at
0.721 (Cao et al., 2024). That is an effect of editing *context*, not of cut *rate*; it
made cutting the natural first lever without measuring cut rate itself. If technique
could not move the sensor when varied this cleanly, no subtler dial would.

**Criteria, fixed before the run.** (1) Count: at least 15 of 180 parcels reach
|*r*| > 0.9 against log cut count — with *n* = 5, *r* = 0.9 is *p* ≈ 0.037, so ~7 are
expected by chance, and the bar is twice that. (2) Anatomy: the dorsal-attention
family (IPS1, FEF, LIPv, VIP, V7, PEF, IP0) over-represented relative to its 7/180
base rate.

**Result: PASS on both.**

**51 of 180 parcels** reached |*r*| > 0.9, against a bar of 15. Against the
level-permutation null (§4.10) — median count 3, 95th percentile 28, with 17% of random
orderings clearing the bar of 15 — the observed 51 is matched only by the true ordering
and its mirror image: *p* = 2/120 = 0.017, **the most extreme result a five-level design
can produce, and no stronger than that**. The criterion's own "~7 by chance" treated the
180 parcels as independent; across the five levels cortex moves along roughly one
direction (participation ratio 1.85 of a possible 4), so the bar was weaker than it was
written to be (§7). The pre-fixed verdict stands. Dorsal attention was
over-represented: **3 of 7** parcels survived (LIPv, PEF, VIP) against 1.98 expected.

**The strongest responders were not where the literature pointed:**

| parcel | *r* | cut01 → cut31 |
|---|---|---|
| **IFJa** | +0.996 | +1.36 · +1.75 · +2.02 · +2.17 · +2.39 |
| IFSp | +0.995 | +0.45 → +1.45 |
| 8C | +0.990 | +0.61 → +1.34 |
| IFJp | +0.984 | +0.92 → +1.59 |
| 7AL | −0.990 | +0.66 → +0.25 |
| V3B | −0.978 | +2.70 → +1.88 |

The top responders — IFJa, IFJp, IFSp, 8C, 45, 44, p9-46v — are **inferior frontal
junction and inferior frontal sulcus**: cognitive control and task-switching cortex,
not the dorsal attention network predicted. Read plainly this is coherent — **every
cut is a switch**, and IFJ is the region most associated with updating task set when
input changes. The monotonicity is near-perfect: IFJa rises across all five conditions
without a reversal. Meanwhile V3B *falls*, consistent with shorter shots giving less
sustained visual processing per shot.

Hitting a different coherent signature is a better outcome than hitting the predicted
one by luck. **But it is a post-hoc reading of an unpredicted result, and is treated
as a hypothesis for stage 02 rather than as a finding.**

Whole-vector correlation cut01 vs cut31 = **+0.8934** — well below the 0.99 that
would have meant the manipulation did nothing, while remaining high, as it should
since the content is identical by design.

**Caveats, carried forward.** The effective range was **2.1×, not 31×**: the source
scenes carry ~22–24 cuts of their own, so detected totals ran 25 → 53 rather than
1 → 31. This makes the pass *conservative* — the effect appeared despite a compressed
manipulation — but it also means a null here would have meant "cutting did not move
the sensor over a 2.1× range". One dial, one film, one pair of scenes: a passing gate
says technique *can* move the sensor, not that lighting or shot scale do. And *n* = 5
conditions is few; the defence is the count at the design's *p*-floor and the anatomical
coherence, not any single parcel.

### 5.3 Stage 02 · The observational index — PARTIAL

*Licenses: across 70 segments of three 1937–1951 films, all fourteen measured dials carry
a surviving association with this sensor's response, dominated by face area. Most
associations fall below the smallest effect worth calling a finding, and cut rate's is
auditory, not frontal.*

**The analysis plan was registered at `osf.io/dg7fe` on 8 September 2026, before the
analysis was run.** It was filed after collection and declares itself as such: OSF's
foreknowledge field is set to *"Authors' limited observation of the data could not
influence their analysis decisions"*, and the complete 70-segment response dataset is
attached to the registration, frozen, with SHA-256 checksums. The test ran once, on
the complete set, against the frozen copy, with the checksum verified in-script.

Two things about that registration are verifiable rather than asserted. The four
documents fixing the criteria are byte-identical between the repository commit made
when 13 of 70 segments had been scored and the commit at registration — 57 further
segments were scored across that span and no threshold, pass criterion, sample size or
model specification moved. And the registered test was run exactly once; the only
earlier dial→parcel computation was the pre-registered futility check described in
§4.8, whose output is a single binary verdict by construction.

#### 5.3.1 Verdict

| criterion | required | found | |
|---|---|---|---|
| 1 · dials with ≥ 1 surviving parcel | ≥ 3 of 14 | **14 of 14** | met |
| 2 · cut rate replicates in {IFJa, IFJp, IFSp, 8C} | yes | **no** | not met |

**PARTIAL.** The pre-registration names this outcome, in advance, as the most
important one available: it means the observational and controlled tracks disagree,
and one of them is wrong. §4.5 records that the sample size was raised from 60 to 70
specifically so that this check could fail informatively. It has.

#### 5.3.2 Pass criteria, as fixed

For each dial, a cross-validated elastic net predicts each parcel's *z* from the dial
set, compared against 1,000 label permutations.

**PASS** requires both:

1. **At least 3 of the measured dials** have ≥ 1 parcel whose cross-validated
   predictive *r* exceeds the 95th percentile of its permutation null, after FDR
   correction across 180 parcels.
2. **Cut rate replicates** — the inferior-frontal cluster from stage 01 (IFJa, IFJp,
   IFSp, 8C) associates with cut rate observationally as well.

**FAIL** if fewer than 3 dials survive, or if cut rate fails to replicate.

**PARTIAL** — dials survive but cut rate does not replicate — means the observational
and controlled tracks disagree. The pre-registration names this the most important
possible finding, and one that would redirect the programme.

**Nulls are reported with equal prominence.** A dial that does not move the sensor is
a dial you cannot direct with, and knowing that is worth more than a plausible story.

#### 5.3.3 Stimulus-side diagnostic: dial interdependence

Reported as a pre-registered diagnostic, computed on centred dials across all 244
segments, and **not modelled**.

**Condition number of the dial correlation matrix: 58.8** — meaningful collinearity
(> 30), short of severe (> 100).

| pair | *r* |
|---|---|
| median_luma ~ shadow_frac | **−0.90** |
| contrast_p5_p95 ~ shadow_frac | −0.71 |
| median_luma ~ mean_saturation | −0.68 |
| median_luma ~ contrast_p5_p95 | +0.68 |
| shadow_frac ~ mean_saturation | +0.68 |

Highest VIF: `shadow_frac` **9.5**, `median_luma` 6.1, `mean_saturation` 5.9,
`colourfulness` 5.0. Conventionally VIF > 5 warrants comment, > 10 is serious.

**The structure is one tight cluster, and it is lighting-and-colour.** Luminance,
shadow fraction, contrast and saturation move together and are close to redundant;
`shadow_frac` at *r* = −0.90 with `median_luma` is nearly a deterministic function of
it. The camera dials, the face and shot-scale dials, and depth of field are
comparatively independent (VIF < 2.3), as is cut rate.

This is the elastic net earning its place — precisely the multicollinearity Kauttonen
(2015) encountered with 37 features. It carries a consequence that must be stated
before any result is read: **any association found inside the lighting/colour cluster
will attribute poorly.** The model may establish that the cluster matters without
being able to say which member drives it. Observational data structurally cannot
resolve that; it needs a constructed ladder of the kind stage 03 ran for cut rate, which
has not been run for lighting or colour (§8).

#### 5.3.4 Detectability at *n* = 70

All 14 dials clear the 80% power floor at the SESOI. The two cut-rate dials are the
weakest (*s* = 0.66 and 0.67; power 0.85 and 0.86), for the reason given in §4.5 —
their variance is disproportionately *between* films, and within-film centring removes
it. The remaining twelve sit at *s* = 0.87–1.00 with power 0.94–0.99.

**The cause is a genuine design tension, not an error.** Cut rate loses a third of its
variance to centring *because the corpus was chosen for director contrast* — Wellman,
Korda and Donen cut at different rates, which is exactly the between-film spread the
corpus was built to have. Within-film centring, adopted to stop any dial becoming a
proxy for film identity, removes exactly that. The two decisions oppose each other,
and only on the dials where between-film contrast is the point.

Stratified selection does not rescue it: recomputing detectability on the selected
subset rather than all 244 leaves *s* essentially unchanged and **no dial changes
label**. Stratifying *within* film cannot recover variance that lives *between* films.

#### 5.3.5 Criterion 1 — technique predicts the sensor, broadly but weakly

**101 of 180 parcels survive** a 1,000-permutation segment-label null under
Benjamini–Hochberg FDR at *q* < 0.05, and **every one of the 14 dials** carries a
non-zero coefficient in at least one survivor. All 14 were classified TESTED at
*n* = 70 before the run, so every result below is a real result and not an untested
one.

**Criterion 1 could not have produced a null.** With 101 survivors and an L1 penalty that
leaves several non-zero coefficients per parcel, every dial was all but certain to be
attributed to some survivor. "At least 3 of 14 dials with at least one surviving parcel"
was met as registered, but once any broad fit exists it is too lenient to be informative;
a future registration should set a per-dial bar, for instance on the marginal effect size
reported below.

| dial | surviving parcels attributed | dial | surviving parcels attributed |
|---|---|---|---|
| face_area_frac | 85 | face_hit_rate | 39 |
| mean_shot_len_s | 72 | cuts_per_min | 35 |
| mean_saturation | 59 | dof_ratio | 35 |
| camera_zoom | 58 | contrast_p5_p95 | 32 |
| camera_pan | 53 | warm_cool | 31 |
| camera_jitter | 46 | colourfulness | 25 |
| median_luma | 43 | shadow_frac | 11 |

**Statistical survival is not the same as reaching the smallest effect worth calling a
finding, and almost none of this result reaches it.** The registered comparison is
approximate: the SESOI was derived for a marginal dial→parcel correlation (§3.2), while
the survival test uses each parcel's cross-validated *r* from all fourteen dials. On that
statistic, survivors have median 0.35 (IQR 0.28–0.44, max 0.61) and **nine parcels exceed
0.5** — PCV 0.61, POS2 0.55, DVT 0.55, 7Pm 0.55, 31a 0.54, 6v 0.53, POS1 0.53, 7Am 0.52,
V3 0.50.

**On the quantity the threshold does apply to, the picture is harsher** (exploratory,
`02-index/sesoi_marginal.py`, registered preprocessing). Of 2,520 marginal dial–parcel
correlations, **6 reach |*r*| ≥ 0.5** — face area with PCV −0.56, 7Am −0.55, DVT −0.54,
7Pm −0.53 and POS2 −0.51, and contrast with V3 +0.54 — against a median of 0.12, and
**none** does so with the lower bound of its 95% interval above 0.5. Each dial's unique
share, the semi-partial *r* given the other thirteen, reaches 0.5 nowhere (largest 0.498,
contrast with V3). The six pairs lie among the nine parcels above, so the two statistics
agree on *where* the largest effects are and both put them at or just over the line.
Passed through TRIBE's out-of-distribution accuracy of 0.2146, a survivor at the median
cross-validated *r* implies roughly *r* ≈ 0.07 against real cortex, with §3.2's caveat
that the propagation is a heuristic. Making this distinction visible rather than burying
it under a count of significant parcels is what the threshold is for.

**The dominant dial is face area**, holding the largest coefficient in 65 of the 101
survivors. Its signature is stage 00's double dissociation reappearing as a
continuously measured dial rather than a three-way contrast: the voice chain up
(STSdp +0.84, A5 +0.69, STSvp +0.58) and the place chain down (VMV2 −0.66,
PHA2 −0.62, MT −0.54). A controlled probe and an observational index, sharing no
segments and no analysis, agree on this axis to the parcel.

**The face-area signature holds in each film separately; the frontal parcels do not**
(exploratory, `02-index/per_film.py`). Within-film centring removes film means, not film
slopes, so the pooled fit could average slopes of opposite sign. For face area it does not:

| parcel | *Jungle Book* (n 24) | *Nothing Sacred* (n 23) | *Royal Wedding* (n 23) | pooled |
|---|---|---|---|---|
| STSdp | +0.49 | +0.37 | +0.89 | +0.40 |
| A5 | +0.44 | +0.36 | +0.90 | +0.37 |
| STSvp | +0.43 | +0.35 | +0.88 | +0.37 |
| VMV2 | −0.48 | −0.49 | −0.66 | −0.45 |
| PHA2 | −0.54 | −0.45 | −0.80 | −0.46 |
| MT | −0.42 | −0.49 | −0.70 | −0.43 |
| IFJp | +0.39 | −0.42 | −0.59 | −0.04 |

Within-film Pearson *r* of each parcel with `face_area_frac`. The voice chain is positive and
the place chain negative in all three films, strongest in *Royal Wedding*. The exception is
inferior-frontal: IFJp's relation to face area is +0.39 in one film and −0.42 and −0.59 in
the others, and pools to nothing. The same split appears for cut rate (§5.7): auditory
parcels negative in every film, frontal parcels of opposite sign in two — a difference
§5.7.2 finds not significant. **The index's
dominant axis is a property of all three films; its frontal entries are not a property of
any pooled fit.**

**The lighting/colour cluster** is dominant in 25 survivors and, per the
pre-registration, is reported as an association with the *cluster*. §5.3.3 fixed that
consequence before any result existed: with condition number 58.8 and
`median_luma`~`shadow_frac` at −0.90, this design can establish that the cluster
matters without saying which member drives it.

#### 5.3.6 Criterion 2 — cut rate does not replicate where stage 01 put it

| parcel | CV *r* | null 95th pct | *q* | survives | coef cuts_per_min | coef mean_shot_len_s |
|---|---|---|---|---|---|---|
| IFJa | +0.044 | 0.178 | 0.191 | no | 0 | 0 |
| IFJp | −0.204 | 0.126 | 0.567 | no | 0 | 0 |
| IFSp | +0.346 | 0.221 | 0.015 | **yes** | **0** | **0** |
| 8C | +0.075 | 0.176 | 0.158 | no | 0 | 0 |

IFSp survives, and it survives with zero weight on both cut-rate dials — its model is
carried by face area (+0.23) and camera zoom (−0.12). Under an L1 penalty an exact zero is
expected output rather than a striking finding; the informative figure is the
unpenalised refit (§5.7.1), whose cut-rate weights on the four cluster parcels are +0.04
to +0.07 with |*t*| < 1. Stage 01's strongest
responder, **IFJa at *r* = +0.996 on identical footage, is indistinguishable from its
null here**. IFJp's point estimate is negative. The criterion required that the cluster
associate *with cut rate*; nothing in it does.

**Where cut rate goes instead.** Among survivors its largest weights are auditory and
negative — A4 −0.23, A1 −0.17, MBelt −0.16, A5 −0.13 — and early visual and positive —
PIT +0.17, MST +0.17, FFC +0.16, V8 +0.14. Mean shot length, its inverse, loads on the
place chain (PHA2 −0.22, VMV2 −0.17) and on motion-sensitive cortex (MT −0.17,
V3A −0.21). Neither dial reaches frontal cortex at all.

**The disagreement is not a confound among the measured dials.** The natural explanation
would be that stage 01 varied cut count on identical footage, where nothing else changed,
while stage 02 measures cut rate where fast cutting co-occurs with other technique.
**Among the measured dials, it does not.** After within-film centring, `cuts_per_min`
correlates with every other dial except its own definitional inverse at |*r*| ≤ 0.194 —
with `face_area_frac` at −0.194 (faster cutting goes with *smaller* faces, not close-ups),
`camera_zoom` +0.163, `face_hit_rate` +0.145, and nothing else above 0.12. Cut rate is the
most nearly independent dial we measure (VIF < 2.3, §5.3.3). Controlling the fourteen
measured dials is therefore not sufficient to isolate cutting, which is why stage 03
isolates it by construction instead.

**How the disagreement resolves — stated here once, argued in §5.5–§5.7.** Neither track
was wrong. Cutting has two signatures on this sensor: inferior-frontal up and auditory
down. Stage 03 shows both causally, with content fixed, and shows the auditory one is a
property of cutting rather than of speech or of the disabled text branch, because it
appears with no speech present and a continuous ambient track (§5.5). The observational
index recovered that half. The frontal half is not detected in the corpus, and §5.7 shows
why that need not be surprising: the penalty did not hide it, cinema's mostly within-scene
cuts should produce only a fraction of it (§5.6), and the per-film differences that seemed
to call for a film-specific explanation are not significant. Of the content the dial set
does not measure, speech accounts for part of the corpus's auditory signature — faster
cutting carries less dialogue, and auditory cortex follows dialogue — and neither speech
nor semantic content accounts for the frontal miss (§5.7.2).

#### 5.3.7 Declared choices, and one exploratory check

**Declared before the run, where the registration was silent.** Elastic net α = 0.1,
l1_ratio = 0.5, 5-fold shuffled cross-validation — the values already present in the
pre-registered futility script, adopted as the only available anchor rather than
tuned. Dials standardised after within-film centring, which is a penalty necessity
rather than a data transformation: dials span 10⁻⁴ to 10², and an unscaled L1/L2
penalty would zero the small-unit ones by units alone. Parcels are not rescaled.
Permutation *p* = (1 + #{*r*_perm ≥ *r*_obs}) / 1001, one-sided; one shared label
permutation across all 180 parcels per iteration, preserving their correlation
structure under the null. Attribution of a survivor to a dial is a non-zero
coefficient in the full-data fit. Seed 20260908. **That the registration did not fix
these hyperparameters is a residual degree of freedom, and it is disclosed rather than
presented as fully specified.**

**Exploratory sensitivity check — not the registered test, which was not re-run.** The
registered null permuted labels across all 70 segments as literally registered, and we
flagged the restricted alternative as a limitation: the three films differ in dial
distribution and response variance, and within-film centring removes each film's mean
but not its variance, so an unrestricted permutation breaks structure the design never
claimed to break. Re-running with permutation restricted **within film**, identical in
every other respect, gives:

| | registered | restricted (exploratory) |
|---|---|---|
| surviving parcels | 101 / 180 | 99 / 180 |
| dials with ≥ 1 survivor | 14 / 14 | 14 / 14 |
| cut rate replicates | no | no |
| median 95th-pct null *r* | +0.192 | +0.182 |

94 parcels are retained, 7 lost and 5 gained; no dial moves by more than 4 parcels.
The restricted null is marginally *narrower*, not wider, so the film-blocking
structure the unrestricted permutation was breaking is negligible and the headline
count is not an artefact of a lenient test. Observed *r* is unchanged by construction
and matched the registered run to 0.00 × 10⁰, which is the correctness check on the
script. **This does not address within-film temporal adjacency**, which shuffling
inside a film does not preserve; the check is one step more conservative than
registered, not the conservative limit.

### 5.4 Stages 01b and 02b · Transfer to generated imagery

*Licenses: generated imagery from one generator moves this sensor along the same
face/place axis live action does, which is the precondition for running stages 03 and 03b
on generated footage. It licenses nothing about other generators, about live action, or
about dials other than face/place; 02b's prediction result is exploratory at n = 3.*

**Question.** Stages 03 and 03b need content held fixed while one dial moves, and only
generation can do that. That is worth nothing unless the sensor reads generated imagery
along the axis it reads real film. 01b asks this as a gate; 02b asks, exploratorily,
whether the fitted index transfers.

**Design (01b).** Three 60 s clips from `minimax/h3-max/text-to-video` — 768P, four 15 s
generations chained on their last frames, native audio — a face, a landscape and a crowd,
the three kinds of content stage 00 used, scored on the unchanged stage-02 Space path
(`audio_only=True`). Criteria were fixed in `01b-transfer/README.md` before generation, and
the evaluator was self-tested on stage 00's vectors (PASS, axis *r* +0.936):
(1) separation, mean top-10 Jaccard < 0.60; (2) direction, the place chain highest on the
landscape and the voice chain on the face; (3) axis, the generated face − landscape
contrast correlating with the index's dominant axis (§6) at *r* ≥ +0.50, against live
action's +0.936.

**Result (01b): PASS on all three.** Jaccard **0.083**, tighter than stage 00's; direction
met on both; axis ***r* = +0.699**. Reported, not gating: the generated contrast correlates
with stage 00's live-action contrast at +0.831, and clip by clip the face at +0.885, the
landscape at +0.412 and the crowd at +0.347. The sensor reads the generated face almost as
it reads the real one and the wide shots less faithfully.

**The confound 01b carried, and why stage 03's design follows from it.** The generator
cuts inside its own 15 s outputs — 7.0, 9.9 and 14.9 cuts per minute for landscape, crowd
and face — so 01b's pass was earned with cutting confounded with content. Stage 03 therefore
required single-take bases and measured them (0 cuts) before intercutting them. Three
further deviations were disclosed before the result was seen: the face-area pre-check
failed as literally written, because the crowd's faces fall below the detector's size
floor; the audio is generated rather than matched to stage 00's, with synthetic speech on
the face clip; and the silent diagnostic arm was dropped on cost.

**02b · Does the fitted index predict generated clips? (exploratory, n = 3).** The
fourteen dials, measured on the three 01b clips and preprocessed as in stage 02, were
passed through the already-fitted 180 × 14 coefficient matrix with no refitting. Predicted
against actual profile *r*: landscape 0.41, crowd **0.90**, face **0.89** (0.48 / 0.92 / 0.92
on the 101 surviving parcels); face − landscape contrast +0.77 against a parcel-permutation
95th percentile of 0.15. Of the six ways to assign the three dial vectors to the three
responses, the true assignment gives the highest mean profile *r* (0.73) and the runner-up
swaps the two wide shots (0.62). One dial, `contrast_p5_p95`, lies outside stage 02's
range, so the prediction extrapolates on it.

**What 02b can carry.** An index fitted on 1937–1951 Technicolor predicting a 2026
generator's output at *r* ≈ 0.9 looks like strong transfer, but §6 shows that the index's
dominant axis is largely the sensor's own response space, so part of any prediction along
it would come from any fit to these responses. With three clips, and 01b's confound
inherited — part of what is predicted is the generator's own cutting — 02b is a reason to
expect generated footage to work, not a finding. Landscapes are the weak case in both
checks.

### 5.5 Stage 03 · Isolation — PARTIAL-A, and the two tracks reconciled

*Licenses: cutting alone, with content fixed by construction, raises inferior-frontal and
lowers auditory response on generated footage, with and without speech. It does not
license the reading the verdict table attached to PARTIAL-A, that the frontal effect needs
speech.*

**Criteria were fixed in `03-isolation/README.md` on 13 September 2026, before any
generation, and were not softened.** Run 14–15 September. Data `parcel_vectors.json` (12
clips × 180 parcels), script `evaluate_03.py`, full output `evaluation.json`; every figure
below is taken from that file.

**Question.** Stage 01 varied cut count on identical live-action footage and the sensor
answered in inferior-frontal cortex. Stage 02 measured cut rate across real cinema and found
no frontal association; cut rate loaded on auditory cortex, negatively. The measured dials do
not explain the disagreement (§5.3.6). Two candidates remained: stage 01's result was specific
to its two scenes, or the observational signature was confounded by something unmeasured,
speech above all. Stage 03 tests both with one design.

**Design — 2 × 5, content held fixed by construction.** Two scenes were generated with the
01b route (`minimax/h3-max`, 768P, 4 × 15 s chained), each a single continuous take: a face
scene (two people in conversation at a table) and a landscape. The single-take precondition
was measured, not assumed — 01b had shown the generator cuts within its own outputs at 7–15
per minute — and both bases returned **0 cuts** on `cinemetrics.py`. The two were then
intercut with stage 01's `build_conditions.py` unchanged at 1, 3, 7, 15 and 31 added cuts;
measured cut counts were **exactly 1 / 3 / 7 / 15 / 31**, a 31× range against stage 01's
effective 2.1×. Every level contains the same 30 s of each scene.

**The two audio arms, exactly as built** (`03-isolation/build_stage03.sh`). **S+** is the
ladder as `build_conditions.py` makes it: each segment is cut from its source *with that
source's audio*, so the soundtrack switches between the face scene's dialogue and the
landscape's ambient sound at every cut. Every level carries the same 30 s of dialogue, in
1 to 16 pieces, and an audio discontinuity at every visual cut. **S−** keeps the same video
and maps the landscape's own ambient track over the whole clip, so it has no speech, no
audio discontinuity at any cut, and the same sound at every level. The arms therefore
differ in three things at once — speech, audio discontinuity at cuts, and loudness and
spectrum — and "speech" names the arm factor only loosely. Video is byte-identical across
arms. Scored on the unchanged stage-02 Space path,
`audio_only=True`; the two bases were scored as references.

**Pre-registered predictions.** H3a: in S+, at least 2 of {IFJa, IFJp, IFSp, 8C} reach
*r* > +0.9 against log measured cut count. H3b: the same in S−. PASS requires both;
**PARTIAL-A** (H3a, not H3b) was fixed in advance with the reading "the frontal cut effect
needs speech present"; PARTIAL-B (neither, but auditory tracks) would demote stage 01 to a
property of its two clips; FAIL if nothing tracks. Reported, not gating: the |*r*| > 0.9
count (scored against the level-permutation null of §4.10), whole-vector *r* cut01
vs cut31, and A4 / A5 / MBelt / A1
against cut count — stage 02's observational signature, to see whether it appears under
control at all.

**Result.**

| | required | S+ (speech) | S− (no speech) |
|---|---|---|---|
| cluster parcels at *r* > +0.9 | ≥ 2 of 4 | **3 of 4** — met | **1 of 4** — not met |
| IFJa · IFJp · IFSp · 8C | | +0.907 · +0.863 · **+0.932** · **+0.930** | +0.899 · +0.871 · **+0.902** · +0.889 |
| parcels at \|*r*\| > 0.9 | reported | **58 / 180** | **54 / 180** |
| that count against 120 level permutations | — | *p* = 0.025 (null 95th pct 32, max 79) | *p* = 0.025 (null 95th pct 32, max 90) |
| A4 · A1 · MBelt · A5 | reported | **−0.969 · −0.959 · −0.951** · +0.152 | **−0.939 · −0.931 · −0.924 · −0.949** |
| whole-vector *r*, cut01 vs cut31 | reported | +0.743 | +0.822 |

H3a met, H3b not met: **PARTIAL-A**, by the table as fixed. The strongest single parcels
were 7PL −0.996, STSva +0.981, 9a +0.980 with speech and 23d −0.990, VVC +0.981, PFcm −0.979
without.

**The verdict is reported as fixed; the reading the table attached to it is not supported.**
In the no-speech arm all four cluster parcels sit at +0.87 to +0.90, and the three that
miss the bar do so by 0.001 (IFJa), 0.011 (8C) and 0.029 (IFJp). At *n* = 5 levels that gap
is inside noise. The data show **the inferior-frontal cut effect present in both arms at
near-identical magnitude**, with 58 and 54 parcels at |*r*| > 0.9, replicating stage 01's
51 / 180 on generated footage with content fixed by construction and the cut range
genuinely 31×. Against the level-permutation null (§4.10) each count has *p* = 3/120 =
0.025 — the true ordering, its mirror image and one other — and some random orderings put
79 or 90 parcels over the bar, because the response across the ladder is close to
one-dimensional (participation ratio 1.25 and 1.20 of a possible 4). Two consequences. The
counts are near the strongest evidence five levels can give. And
within this ladder "frontal up, auditory down" is the sign pattern of one response mode,
not two independent findings — a statement that holds within a ladder and, as §5.6 shows by
varying the kind of join, fails across ladders, where the two signatures separate.
PARTIAL-A stands because the criteria were
fixed and are not softened afterwards; the claim that speech is *required* for the frontal
effect must not be carried forward as a finding, and this paper does not carry it. That
reading could not have been supported by this design in any case: S+ never isolates speech
from audio discontinuity, so a PARTIAL-A could not have said which one the frontal effect
needed (§7).

**Stage 02's observational signature reproduces under control.** In both arms cut rate is
strongly negative in auditory cortex — A4 −0.97 / −0.94, A1 −0.96 / −0.93, MBelt −0.95 /
−0.92 (S+ / S−) — and A5 joins them without speech (−0.95) while sitting at +0.15 with it.
That arm difference is unexplained, and because the arms differ in audio discontinuity as
well as in speech, it is at least as likely to be about the one as the other.
This is what the index found in §5.3.6 and what stage 01 did not report. **Both earlier tracks
were right about different parts of one effect**: cutting drives inferior-frontal cortex up
and auditory cortex down, with or without speech, and — since S− has a continuous ambient
track with no discontinuity at any cut — the auditory decrease follows *visual* cut count,
not an interrupted sound stream. The alternative §5.3.6 raised, that the auditory signature
was an artefact of the missing text modality, does not survive an arm with no speech in it.

**Cut rate is therefore a causal lever on this sensor**, with the frontal and auditory
signatures both available as targets for stage 04 — on the material where it has been
shown, which is intercut generated footage (§5.6 grades it by the kind of join).

**Limitations.** The regenerated face base reached `face_area_frac` 0.052 against a 0.10
target (a wide first attempt measured 0.035; no third attempt at the post-promotional
generation rate), so the face/place contrast between the bases is weaker than stage 01's;
the cut manipulation is unaffected. *n* = 5 levels per arm: |*r*| > 0.9 is a coarse
instrument and the arm difference is not resolvable at this *n*. Generated footage, one
scene pair, one generator — the scope 01b licensed. Text branch off, as in every prior
stage; a text-on replication is unrun.

### 5.6 Stage 03b · Which part of a cut — GRADED

*Licenses: on constructed ladders, a hard cut within a scene and a change of scene without
a hard cut each carry part of the frontal effect, close to additively, while the auditory
effect follows the hard cut. The verdict is GRADED, so no categorical claim is made.*

Stage 03 varied cutting on a ladder where every cut alternated two maximally different
scenes, so a cut and a change of scene were the same event. Stage 03b separates them.
Four ladders, each 1 / 3 / 7 / 15 / 31 constructed joins per minute as in stage 03:
**REF**, stage 03's no-speech arm rescored, where each join is both a hard cut and a scene
change; **B** and **C**, hard cuts with no change of scene, made by self-intercutting a
single base — the two-person face scene and a landscape respectively; and **D**, changes of
scene with no hard cut, the REF material joined by 0.5 s dissolves. Criteria, the four
verdict classes and the frontal cluster were fixed in `03b-discontinuity/README.md` at
commit `221faad` before any clip was built, and the evaluator was committed and self-tested
on frozen calibration data before any result existed. Twenty clips, 180 parcels, plus a
saved 1 Hz × 180 timeline per clip. The audio track is byte-identical across all twenty
clips (one decoded MD5), so nothing here can be an auditory artefact of the construction.

**Identity test: PASS.** The timeline-saving app reproduced stage 03's S− parcel values
exactly (max raw |Δ| 0.0e+00), and each parcel's 60-point timeline averages to its raw value
to 4.3e-08. Every figure below therefore sits on the same footing as stages 01–03.

The frontal ratio ρ_F is a ladder's mean frontal-cluster slope (IFJa · IFJp · IFSp · 8C
against log constructed cuts) divided by REF's +0.251; *p* is one-sided over the 120 level
orderings, floor 0.008. As fixed: **REPRODUCES** at ρ_F ≥ 0.50 with *p* ≤ 0.05, **ABSENT**
at ρ_F ≤ 0.25, **PARTIAL** otherwise.

| ladder | ρ_F | *p* | class | ρ_A (*p*) | whole-map gain (*p*) | *r* with REF mode | PR |
|---|---|---|---|---|---|---|---|
| **REF** · hard cut + scene change | +1.00 | 0.017 | **REPRODUCES** | +1.00 (0.008) | +1.00 (0.008) | +1.00 | 1.20 |
| **B** · hard cut, same scene — face | +0.44 | 0.008 | **PARTIAL** | +0.62 (0.008) | +0.67 (0.008) | +0.86 | 1.05 |
| **C** · hard cut, same scene — landscape | +0.18 | 0.017 | **ABSENT** | +0.38 (0.008) | +0.47 (0.008) | +0.73 | 1.03 |
| **D** · scene change, 0.5 s dissolves | +0.48 | 0.042 | **PARTIAL** | +0.17 (0.075) | +0.50 (0.008) | +0.62 | 1.25 |

The same-scene arm returns one PARTIAL and one ABSENT, the dissolve arm PARTIAL. By the
table as fixed that is **GRADED — no categorical claim; the ratios are reported as
measured.**

**The sensor is neither a pure cut detector nor a pure switch detector.** A hard cut with no
change of scene carries 44% of the frontal effect in the face scene and 18% in the
landscape; a change of scene with no hard cut carries 48%. The two contributions are close
to additive — B + D ≈ 0.92 of REF, C + D ≈ 0.67 — and every ladder's whole-map response
pattern resembles REF's (*r* +0.62 to +0.86, all *p* = 0.008), so what varies across the
ladders is the size of one response and not its shape.

**The two signatures of cutting come apart, which qualifies §5.5.** The auditory decrease
follows the hard discontinuity: 62% and 38% for same-scene cuts, and only 17% under
dissolves, where it is the one figure in the table that does not clear its null
(*p* = 0.075). The frontal increase does not need the discontinuity at all: dissolves carry
48% of it. §5.5 read "frontal up, auditory down" as the sign pattern of a single response
mode, on the evidence of a participation ratio of 1.25 and 1.20 within one ladder. That
reading holds within a ladder and fails across them. **The auditory signature is a
discontinuity response; the frontal one is partly that and partly a response to the scene
changing.** Two signs of one mode in stage 03, two separable effects here.

**The same-scene result depends on the scene, and not on the size of the jump.** B and C
have near-identical discontinuity magnitudes — peak frame Δ 40 against 39, histogram
distance 0.16 against 0.23 — and ρ_F of 0.44 against 0.18. Cutting inside a scene of two
people at a table moves the frontal cluster more than cutting inside a landscape. What is
interrupted matters, not only that something is.

**On the encoder-artefact alternative.** Its pure form — the model maps temporal
discontinuity to frontal cortex and nothing more — is weakened: half the frontal effect
arrives with no discontinuity, while the auditory half is the part that tracks
discontinuity. A broader form, a response to any large visual change whether gradual or
abrupt, is **not** excluded, because this design cannot separate it from "change of scene"
(`03b-discontinuity/README.md` § Limits).

**The frontal miss is smaller than it looked, and is still not resolved.** Most cuts in
cinema are continuity cuts inside a scene, which by B and C produce 0.18 to 0.44 of REF's
frontal slope per unit log cuts. `frontal_miss.md` put the corpus *r* expected from REF's
*full* slope at ≈ +0.30 to +0.45; at 0.18–0.44 of it the expected corpus *r* is ≈ +0.05 to
+0.20. That is small enough to go undetected in three films of 23–24 segments, and §5.7
finds the per-film sign differences within noise, so the miss needs no film-specific
explanation. It is still not *shown* to be small rather than absent, and the observational
scene-switch test of §5.7 and the constructed test here disagree in a way *n* = 3 films
cannot settle: scene change alone carries half the frontal effect on
constructed material, and no frontal association with between-scene cuts appears in the
corpus at any threshold.

**Reported, not gating: no join-locked transient (exploratory, `cut_locked.py`).** Timelines
projected on the unit REF mode and epoched −3 to +12 s around the joins of levels 1, 3 and 7
show no clean transient. All four ladders give a small rise into the join, a dip near +3 s
and a larger one at +10 to +11 s (REF −1.56, B −4.40, C −3.00, D −2.10), of similar shape
whatever the join type. A shape recurring at fixed lags across ladders with different joins
is more likely a property of the model's windowing than of the join, and with ten epochs per
ladder this is descriptive only. The effect the slopes measure is in the **sustained level**:
mean projection per level rises with cut count in REF (−1.84 → −1.34 → −0.76 → +0.88 →
+4.07) and B (+0.95 → +1.28 → +2.09 → +4.23 → +4.66), weakly in C (−2.45 → −2.41 → −1.50 →
−0.42 → +0.36) and D (−1.70 → −1.26 → −0.59 → +0.02 → +0.22). The timelines are saved for a
better-designed analysis; this one licenses no claim.

**Limitations.** Five levels and a *p*-floor of 0.008; one generator; two scenes; text branch
off; everything here is about TRIBE. Scene change and large gradual visual change are not
separated, and a dissolve is also 0.5 s of blended imagery — 26% of the clip at 31 joins. B
and C are single-scene clips where REF and D are two-scene, so slopes are within-ladder and
the baselines differ. Clip length shrinks slightly with cut count in REF, B and C (59.9 →
58.5–58.9 s), a property of `build_conditions.py` inherited from stages 01 and 03; D is
60.00 s throughout. B carries the face base's one generator seam at every level, which is
constant and cannot affect a slope. All three whole-map gain *p*-values sit at the floor, so
the gain ordering (B 0.67 > D 0.50 > C 0.47) is not statistically resolved.

### 5.7 Why the corpus lacks the frontal effect

*Licenses: the frontal miss in the corpus is not an artefact of the regression and needs no
film-specific explanation. It does not license saying the frontal effect is absent from
cinema.*

Stage 03 showed cutting raises inferior-frontal response causally, and stage 02's corpus
shows no trace of it. Everything in this section is exploratory and was run on the frozen
stage-02 data after the registered test; the PARTIAL verdict of §5.3.1 is unchanged. It
proceeds by exclusion (§5.7.1) and then by measuring what the dial set lacks (§5.7.2).

#### 5.7.1 Exclusions on the frozen stage-02 data

Full note in `02-index/frontal_miss.md` and `02-index/scene_switches.md`. *The penalty is not the cause*: refitting the four cluster parcels on
the registered design matrix without regularisation gives cut-rate weights of +0.04 to +0.07
with the stage-03 sign and |*t*| < 1 (*p* 0.35–0.53); the elastic net zeroed coefficients
indistinguishable from zero, and kept the auditory quartet's (OLS −0.15 to −0.26, MBelt
*t* = −2.37). *The raw signal is absent*: IFJa's within-film correlation with cut rate is
−0.005, and the per-film frontal estimates differ in sign (negative in *Jungle Book*,
positive in *Nothing Sacred*) while the auditory sign is negative in all three — though
the frontal difference is not significant (§5.7.2). *Range is not the
explanation*: the two wide-range films each span a 7–8× range of cut rate and show the
auditory effect inside each film and the frontal effect in neither. *Nor is swamping*:
transplanting each parcel's stage-03 slope into the corpus's within-film variance predicts
*r* ≈ +0.30 to +0.45 for the frontal parcels — *larger* than for auditory, whose corpus
variance is greater — and the auditory parcels arrive at or above their predicted size
(−0.27 to −0.31) while the frontal ones show nothing (−0.12 to +0.06). *Everywhere else the
index is right*: across 180 parcels the observational cut-rate map correlates with the
stage-03 no-speech causal map at *r* = +0.52, and of the 23 parcels stage 03 moves the same
way in both arms at |*r*| > 0.9, stage 02 has the sign of 22. The corpus, not the regression,
lacks the frontal effect. The hypothesis left standing is that inferior-frontal cortex
responds to **scene switches**: in the stage 01 and 03 ladders every cut alternates two
maximally different scenes, so cuts and scene switches are the same count, whereas most cuts
in cinema are continuity cuts inside one scene. **Tested, and not supported**
(`02-index/scene_switches.md`). A between-scene cut count — cinemetrics' detector unchanged,
each cut scored by the histogram distance between the shots either side — separates stage
03's ladder perfectly (all 57 imposed cuts at 0.73–0.84, the single-take bases at 0.20 or
nothing) and stage 01's live-action ladder only partially (it recovers about half the imposed
cuts, because *Jungle Book*'s own internal cuts reach 0.6–0.8). On the 70 scored segments no
frontal parcel tracks between-scene cuts at any of three thresholds (|*r*| ≤ 0.16, every
*p* ≥ 0.19); IFJa's per-film estimates still differ in sign (+0.40 in *Nothing Sacred*,
−0.25 in *Jungle Book*); and the auditory decrease follows within- and between-scene cuts alike
(A1 and MBelt with within-scene cuts at −0.27 and −0.30, A4 and A5 with between-scene at
−0.22 and −0.25), which is stage 03's no-speech result seen in real cinema across cut types.
Because the proxy is partial on live action the hypothesis is weakened rather than excluded,
but a surviving effect would have to be small where the transplanted slopes say it should be
large. What stands: the frontal miss is not the penalty, not the range, not content variance
and not, by this measure, the composition of the cuts. The frontal parcels' relation to
cutting differs in sign between films, which pointed at film-specific content the dial set
does not measure; §5.7.2 measured two candidates and found the sign difference itself not
significant. The index's cut-rate column should be read as the auditory half of the effect
only, and that half as partly cutting, partly speech (§5.7.2). §5.6 put the same question to
a constructed test, and its answer lowers the corpus effect the frontal parcels should have
shown to *r* ≈ +0.05 to +0.20.

#### 5.7.2 Content descriptors · the sign flip not demonstrated, and speech the missing dial

The exclusions of §5.7.1 end on a pointer: the frontal parcels' relation to cutting differs in sign between films, so perhaps
film-specific content the dial set lacks carries it. Two candidates were measured on all 244
segments without reading any parcel data: **speech proportion** (Silero VAD; Whisper word
counts agree at *r* 0.96), and **semantic change at cuts** (CLIP ViT-B/32 distance between
frames either side of each detected cut). The plan, the class rules and the order of
questions were committed before any descriptor existed, and an amendment before any parcel
value was read (`02-index/content_descriptors.md`). The CLIP measure was validated on 03b's
ladders — scene-change joins 0.42–0.49 against same-scene joins 0.02–0.07 — and the analysis
on synthetic data where a carrier was planted.

**The first question answered the rest: the flip is not demonstrated.** Within film, the
frontal cluster's correlation with cut rate is −0.27 in *Jungle Book*, +0.26 in *Nothing
Sacred* and −0.05 in *Royal Wedding*. Testing whether those slopes differ (cut × film, 10,000
within-film permutations) gives *F* 1.38, *p* 0.28; the *Nothing Sacred* − *Jungle Book*
difference is +0.53 with a 95% bootstrap interval of −0.14 to +1.08. Per parcel, IFJa —
the parcel the earlier sections name — reaches *p* 0.19, and IFJp, IFSp and 8C 0.44–0.58.
The auditory cluster, as a control, is homogeneous (*p* 0.97). By the class rules fixed in
advance, speech proportion, semantic change per minute and semantic distance per cut **do
not carry** the difference (shrinkage −0.09, +0.13 and −0.06) — and none could, because none
correlates with cut rate in opposite directions in the two films. Faster cutting goes with
*less* speech in both, and with cuts that change the picture's meaning *more* in all three.

**So the frontal miss needs no film-specific explanation.** Pooled within film, the frontal
cluster's correlation with cut rate is −0.02, and the per-film estimates scatter around zero
by about as much as samples of 23–24 would. With §5.6's estimate of the effect cinema's
within-scene cuts should produce (*r* ≈ +0.05 to +0.20), the simplest reading is a small
expected effect that three films could not detect. Not detecting it is not showing it
absent: the interaction test has little power at this *n*.

**Speech is the content dial the index lacks, on the auditory side** (post-hoc, labelled
as such in the note). Within film, the auditory cluster follows speech proportion at
*r* +0.78, with the same sign and size in every film. In leave-one-out prediction within
film, the fourteen visual dials alone reach *R*² −0.09 in ordinary least squares (which
overfits at *n* = 70; the registered model was an elastic net, so this is not a re-run of
§5.3.5), the dials plus speech **+0.54**. Because faster cutting carries less dialogue, some
of the corpus's negative auditory–cut relation is speech: the pooled within-film *r* moves
from −0.27 to −0.19 when speech is partialled out. Most of it survives, as stage 03 implies
it should — cutting lowered auditory response there with no speech present. **The index's
auditory cut-rate coefficient is therefore partly a speech coefficient; stage 03's causal
result is unaffected.**

**What the frontal cluster does track is the picture's content** (post-hoc). Given cut
rate, it follows the second semantic component of the segment's CLIP embedding at +0.55,
+0.55 and +0.34 by film and falls with semantic dispersion at −0.43, −0.35 and −0.24 — the
same sign in every film; the component is partly faces (*r* +0.40 with face area) but is
not a dial under another name. This marks where a frontal dial would have to come from,
not what it is.

**Limitations.** Three films of 23–24 segments; one VAD and one CLIP model, the latter
trained on photographs and captions rather than cinema; the semantic measure validated on
generated footage, between whose two calibration groups live-action cuts fall (median
0.23). The planned semantic-change rate turned out nearly collinear with cut rate
(*r* 0.94) by construction and was supplemented, before any parcel data was read, with the
per-cut distance. The text branch was off, so the sensor heard speech and never read it.

---

## 6 · The index as a map, and what it implies for inversion

**Exploratory. Not pre-registered, and none of it counts toward the pass criteria.**
The registered test asks whether dials predict parcels. It does not ask what the
resulting index *looks like* — and that index is the artefact the whole
programme was built to produce. This section characterises it. The object is the
180 × 14 matrix **B** of full-data elastic-net coefficients: column *k* is the
cortical pattern associated with dial *k*, and the set of response profiles technique
can reach is the span of those columns.

**Provenance.** Every figure in this section is reproduced by `02-index/index_map.py`, which
rebuilds **B** from `analysis_result.json` (output `index_map.json`), with the
technique-specificity tests in `index_map_followup.py`. The comparison that governs what
the section may claim is the same elastic net refitted to **label-shuffled** responses,
200 times: where the real index and the shuffled ones agree, the property belongs to the
sensor's responses and not to technique. (How this section's first draft went wrong without
that comparison is recorded in §7.)

**The index is concentrated in about three dimensions — and so is an index fitted to
noise.** The singular values of **B** fall away sharply — 3.34, 1.52, 1.01, then nothing
above 0.75. Three components carry 90.1% of the index's variance and five carry 95.9%.
Restricted to the 101 surviving parcels, three components carry 92.7%. (Participation
ratios, on variances: 1.97 for **B**, 1.65 for the survivors and 2.41 for **Y**.) Under
label shuffling the index is just as concentrated: three
components carry 89.1% on average (5th–95th percentile 82.5–93.9%; observed 90.1%,
*p* = 0.42) and the first axis 66% (observed 69%, *p* = 0.39). **The index's three
dimensions are a property of the sensor's response space across these segments, which itself
varies along two to three dimensions; they are not evidence that technique is
low-dimensional.** Any 14-predictor fit to these responses, signal or none, collapses the
same way.

| axis | share | dominant dials | cortex |
|---|---|---|---|
| 1 | 69.4% | face area +0.80, saturation −0.43, zoom −0.27 | STSdp +0.35, A5 +0.30, VMV2 −0.25, PHA2 −0.22 |
| 2 | 14.3% | camera pan −0.65, luminance +0.51, cut rate +0.35 | V4t +0.30, MST +0.30, MT +0.29, FST +0.28 |
| 3 | 6.4% | saturation +0.58, face area +0.46, zoom +0.32 | PCV −0.31, PIT +0.24, A5 −0.23, V8 +0.23 |

The axes are interpretable without being told what to look for. **Axis 1 is the
face/place axis** — stage 00's double dissociation, recovered as the dominant direction
of a continuous 14-dial model that was never shown stage 00's clips. That is not a
resemblance but a measurement: run 00's face − landscape contrast vector correlates with
axis 1 at ***r* = +0.936** (face alone +0.704, landscape alone −0.684, crowd −0.135 —
the graded middle again), against a 180-parcel permutation 95th percentile of 0.144.
Two measurements sharing no segments, no films and no analysis agree on the dominant
direction to 0.94 — **but most of that agreement is about the sensor, not about technique.**
Run 00's contrast correlates with the first principal component of the 70 response profiles
at |*r*| = 0.90 with no dial involved, and with the first axis of *label-shuffled* indices at
0.84 on average (5th–95th percentile 0.68–0.93); the observed +0.936 sits at *p* = 0.045
against that null, not at the 0.144 of a parcel permutation, which tested the wrong thing.
What the agreement establishes is that the dominant axis of this sensor's response to real
cinema *is* the face/place axis of stage 00. What is specific to technique is which dial
leads it: face area loads on axis 1 at 0.80, against a shuffled-label mean of 0.22 and 95th
percentile of 0.57 (*p* = 0.010), and leads axis 1 in 10% of shuffles. **Axis 2 is
motion** — camera movement and cutting loading on MT, MST, FST, V4t, the motion-
sensitive complex. **Axis 3 is colour**, and it is small. Note where cut rate lands: on
the motion axis, at a third the weight of camera pan, and nowhere near frontal cortex —
the same story §5.3.6 tells, arrived at without reference to stage 01.

**Technique is aligned with how this cortex varies, by a modest margin over a fit to
noise.** Projecting the observed 70 × 180 profile matrix onto the reachable subspace
retains **90.8%** of its variance. The comparison that makes that number meaningful is the
third row:

| 14-dimensional subspace | variance of observed profiles retained |
|---|---|
| random | 7.8% (sd 1.8, max 13.5 over 200 draws, seed in script) |
| **index fitted to label-shuffled responses** | **85.5%** (5th–95th pct 81.8–88.5, max 89.6 over 200) |
| **technique** | **90.8%** (*p* = 0.005 against the shuffled fits) |
| top-14 principal components (ceiling) | 99.4% |

A random subspace is the wrong floor: the columns of any **B** fitted to **Y** are built
from **Y**'s own rows, so they lie in its dominant directions whether or not the dial labels
mean anything. The honest statement is a gain of about five points over that floor, real
(*p* = 0.005) and small. The total coefficient mass tells the same story from the other
side: ‖**B**‖ = 4.01 against a shuffled mean of 2.67 (*p* = 0.015).

Technique reaches 91.3% of what the *best possible* 14-dimensional subspace could. With
a single axis it retains 57.7% against a best-possible 61.8% — **the first technique
axis is very nearly the first principal component of cortical variation across these
segments.**

**Fitting guarantees the alignment, the concentration and the coincidence of axes.**
Because **B** is fitted to **Y**, its columns are aligned with **Y** by construction, and
the shuffled-label fits show that concentration and the first axis's coincidence with the
dominant direction of variation come with fitting too: their first axis correlates with **Y**'s first principal component at 0.92 on average
(observed 0.96, *p* = 0.095) and retains 52.7% of profile variance alone (observed 57.7%,
*p* = 0.075). The single-axis figures in the paragraph above are therefore descriptive of
the response space, not findings about technique.

**What this says about inversion, which is the programme's endpoint.** H4 proposes
specifying a target cortical profile and deriving the technique that reaches it. The
geometry above says what that can and cannot mean.

*A target profile is not freely specifiable.* Response profiles live in 180 dimensions;
this sensor's responses to cinema occupy about three, and technique can reach no more than
the sensor varies over. The bound is on the instrument first and on technique second. Any target decomposes into a reachable component and a
residual that no combination of these fourteen dials can produce, and the residual is
not small in general — it is only small for targets that resemble the profiles real
film already produces. **Inversion is projection, not solution.**

*The inverse is many-to-one, which cuts both ways.* Fourteen dials mapping onto three
effective directions means a reachable target is reachable by a whole family of dial
settings. For a director that is permissive: several technical routes reach the same
predicted response. For identifiability it is fatal: one cannot infer the technique from
the response, and stage 04 must therefore verify an *achieved profile* rather than a
recovered technique.

*And the axis that dominates is the face axis.* If a controller maximises predicted
response along the direction technique most strongly commands, it moves along axis 1,
whose positive pole is the voice/face chain and whose negative pole is the place chain.
**A machine hill-climbing on this index would go to faces and away from landscapes** —
which is the drift *The Simulated Viewer* depicts, here arrived at from a coefficient
matrix rather than from a generative search. This is an association in a model's
predictions, it inherits every limitation in §8, and it is not evidence that the drift
occurs in forty clips. It is evidence that the lever exists and is the largest one.

---

## 7 · Method failure as evidence

This section is not an appendix. When an instrument returns plausible numbers
whatever you feed it, **silent failure is the central methodological hazard**, and the
practices that surface it are part of the result.

**Six of seven failures in stage 00 were assumed API shapes** — not model failures,
not data failures, and none of them in the science. All sat in the last ten lines that
turn vertices into parcel names:

| failure | cause |
|---|---|
| clips silently absent | the Space's `.gitignore` contains `*.mp4`; uploads **reported success** and were dropped |
| wrong readout, twice | `build_roi_masks` returns 5 composite scores, not parcels — giving Jaccard 1.00 *by construction*; then `get_hcp_labels` returns a dict, not a list, mis-keying every parcel |
| `load_fsaverage5_atlas` | raises `NotImplementedError`; superseded |
| tuple unpack | `run_inference` returns `(preds, abs_times)`, not an array |
| gated model 401 | `mode="video"` pulls the text branch; fixed with `audio_only=True` |
| invalid kwarg | `show_copy_button` removed in gradio 6.11 |

The second row is the instructive one. **A Jaccard overlap of 1.00 by construction is
indistinguishable, without introspection, from a sensor that cannot discriminate.**
Had that run been accepted, stage 00 would have "failed" and the programme would have
stopped on an artefact of the readout code.

Each failure cost ~7 minutes of restart plus ~30 minutes of scoring. Verifying an API
shape by introspection costs seconds. This produced the programme's standing rule —
**introspect before writing against an API** — and the rule has since caught the same
class of error again: a later collection step assumed `cinemetrics.py` wrote a dict
keyed by clip path when it writes a *list*, and null face-area values on 16 no-face
segments would have silently dropped the shot-scale dial from the analysis entirely.

**A recorded fact can itself be a wrong diagnosis.** The project handoff carried, in a
"do not re-derive" table, the statement that background log pollers "were killed
silently with no output", and a standing rule to fetch logs in the foreground. That
diagnosis was wrong. The Hugging Face `/logs/run` endpoint is a **live SSE stream that
does not close while the Space is running**, so any reader iterating it blocks
indefinitely — foreground or background alike. The pollers were not killed; they were
hanging. The corrected implementation reads to a wall-clock deadline with a socket
idle timeout.

The cost of that wrong fact was paid twice: once in stage 00, and again when a
monitoring script written from the same misunderstanding blocked while a run completed
underneath it, leaving GPU hardware idling on billed time until a human noticed. **A
wrong entry in a "do not re-derive" table is worse than no entry**, because it is
trusted precisely where it will not be re-checked.

**The same failure recurred in this paper's own pre-registration, which is why it is
reported here rather than in a footnote.** The registration filed at `osf.io/dg7fe`
stated three times that the pre-registered futility check had never been executed, and
once, more broadly, that no dial→parcel relationship had been computed by any means at
any point. Both were false. The check had run on 6 September at 30 of 70 segments and
returned CONTINUE.

The mechanism is the one this section is about. The claim was checked before filing by
searching the repository and its logs for the script's output banner and verdict
strings, which returned nothing. The script was untracked in version control and had
been run interactively, printing to a terminal rather than to a file. **Absence of a
record was read as absence of execution.** The defensible statement — "no record of
execution exists on disk" — is weaker, and would have prompted the question that was
not asked.

What it did and did not cost is worth separating. Running the check was *permitted*: it
was pre-registered, it returned CONTINUE, its output is a single binary verdict by
construction, and no threshold, sample size or specification moved. The protocol was
not violated. What was damaged was the accuracy of a registered document, and the remedy
was an amendment, filed through OSF's update process on 20 September 2026, recording the
correction and its cause. Filing it taught the lesson a third time. Our own notes placed the
false claim in two fields; reading the registration end to end before submitting found it
stated or implied in six, and found a second, unrelated false statement in two more — that
scene-boundary counts were kept in the dial table (§4.3). Eight fields were corrected in
one update, each marked in the text as corrected, with the original wording quoted. **A registration that
must be amended for a false statement about its own compliance is a worse artefact than
one that never made the claim** — and the general lesson is the one already stated
above, now demonstrated twice: a confidently recorded fact is exactly where verification
stops, which is exactly where it is most needed.

**A null that assumed independence.** Stage 01's criterion took chance as ≈ 7 parcels at
|*r*| > 0.9, reasoning that *r* = 0.9 at *n* = 5 has *p* ≈ 0.037 across 180 parcels, and
stage 03's README inherited the figure; earlier drafts of this paper reported the counts as
seven and eight "times chance". The parcels are not 180 independent trials: across a ladder
the response moves along close to one direction, so a count behaves nearly like a single
event. Permuting the level labels (§4.10) puts the null's 95th percentile at 28–32 and has
8–17% of random orderings clearing the pre-fixed bar of 15. The verdicts stand, because the
criteria were fixed and the observed counts sit at or one ordering above the design's
*p*-floor; the bars were weaker than they were written to be. The lesson is the one this
section keeps returning to: a null written down before the run is still an assumption, and
checking it is part of the result.

**A results section written without a script.** The index-as-map analysis (§6) was first
written from interactive computation with no script committed behind it. Rebuilding it from
the frozen coefficients (`index_map.py`) reproduced all 45 figures — and still changed the
reading. Three participation ratios had been computed on singular values rather than
variances (quoted as 5.56, 4.76 and 8.35; conventionally 1.97, 1.65 and 2.41). The
agreement between stage 00's contrast and the index's first axis had been tested against a
parcel permutation (95th percentile 0.144) rather than against fits to label-shuffled
responses (*p* = 0.045). Retained variance had been compared with a random subspace (7.8%)
rather than with those shuffled fits (85.5%). And the draft had named the concentration of
the index and the coincidence of its first axis with the dominant direction of cortical
variation as what fitting does *not* guarantee, when the shuffled fits show it guarantees
both. **Every number was right and the claim was not**: the draft read properties of the
sensor's response space as properties of technique. A figure with no script behind it is a
claim, and the comparison it most needs is the one the analyst did not think to run.

**A verdict table that named a mechanism.** Stage 03's table fixed four outcomes before
generation and attached a reading to each; PARTIAL-A's was "the frontal cut effect needs
speech present". When PARTIAL-A came out — by 0.001 on one parcel — the outcome had to be
reported as fixed while its reading was disowned, because the data showed the frontal
effect at near-identical size in both arms. The reading was also never testable: S+
carried speech *and* an audio discontinuity at every cut, so no outcome could have
isolated speech. Fixing criteria in advance protects a result only if what is fixed is
the outcome. **A verdict table should carry outcomes, not mechanisms**; the mechanism is
a reading, written after the result and separately from it, as stage 03b's result and
the content-descriptor analysis (§5.7.2) are.

Three practices follow, and are now standing rules:

1. **Criteria are written in the stage README before the run and are never softened
   afterwards.** Every result in §5 is reported against a threshold fixed in advance.
2. **Persist to disk, not to the instrument.** The Space's filesystem is wiped on
   pause; stage 00's first full result set was lost that way and had to be re-run.
3. **Introspect before writing.** Seconds to check, ~35 minutes to get wrong.

**Missteps in the paid runs.** *Stage 03.* Bases $3.60 on fal including one regeneration; scoring
≈ $2.2 on the Space for 12 clips plus one wasted restart. That restart was caused by a
watcher of ours that matched result files containing `"03_"` anywhere — which also matched
stage-02 ordinals and files from a separate experiment writing to the same results
repository — and paused the run at 6 / 12; corrected to exact-name matching, and the other
experiment has since been given its own results repository. The local machine killed
background tasks for memory twice; the Space finished the batch unattended and paused on
its inactivity timer. A text-branch rescoring attempted on 13 September produced 0 / 12
results after 189 minutes and is parked undiagnosed.

*Stage 03b.* Three Space sessions, 20–25 September 2026. **Session 1
overspent.** Twenty clips were staged as a single batch against this project's own
documented safe size of eight; the Space stalled after clip 10 while still billing; and the
budget guard lived in a laptop-side watcher that slept with the machine. Roughly 5.5–8.2
hours ran against a $3.60 estimate, ≈ $5.50–8.20 (the exact figure exists only on the
Hugging Face billing page). The fix was to move the guard **server-side** into the app — a
self-pause on completion and an 80-minute watchdog — with a 30-minute Space sleep timeout,
batches of five, and a stall-detecting watcher. Sessions 2 and 3 then ran 63 and 62 minutes
and the Space paused itself both times, ≈ $2.10 for the pair. The original app was restored
byte-identically on 25 September. The lesson is general and it cost money twice: **a budget
guard that runs on the client cannot bound a server's spend.**

---

## 8 · Limitations and future work

### 8.1 Limitations

Stated plainly and grouped by what they limit. None is resolvable within this design.

#### Of the instrument

**It is a model, not a brain.** Every result concerns TRIBE's predictions. The published
link to real cortex is *r* = 0.2146 out-of-distribution, our material is further out than
that figure was measured on, and parcel-wise accuracy on this material is unknown. §3.2
propagates that number into an effect-size threshold — as a heuristic, not a bound — but no
analysis here can escape it. A finding that technique moves TRIBE is a finding about TRIBE.

**A response can belong to an encoder rather than to anything cortical** (§3.4). Stage 03b
weakens the pure form of that reading for cutting: half the frontal effect arrives with no
discontinuity at all. It cannot separate a change of scene from any large change in the
encoder's input, gradual or abrupt, so the broad form stands.

**The sensor's response space is low-dimensional, which bounds every downstream claim.**
Across 70 segments of real cinema the 180-parcel response varies along two to three
dimensions, and an index fitted to label-shuffled responses is as concentrated as the real
one (§6). Whatever the programme eventually demonstrates about control, it is control over
a roughly three-dimensional subspace of response profiles. Whether that is a fact about
cortex, about TRIBE's encoding head, or about clip-mean readouts that average away
everything faster than a minute, this design cannot say.

**The text branch was never on.** All results are video plus audio; the gated language
model was skipped throughout, and the model's tolerance of the missing modality is taken
from its documentation rather than tested. Stage 03's no-speech arm shows the auditory cut
signature is not an artefact of that omission, but for a corpus with dense dialogue —
*Nothing Sacred* in particular — the sensor heard speech and never read it. A text-branch
rescoring attempted on 13 September produced 0 / 12 results after 189 minutes and was not
diagnosed.

#### Of the observational index

**Three films, one era, three directors: the index is corpus-conditional.** Three films
are enough to break dial covariance and not enough to claim film-independence. Leipold et al.
found associations landing in non-overlapping regions for nearly every one of eight films,
and concluded that a specific movie should be treated like a specific task; our index should
be read the same way. Per film (§5.3.5) its dominant face/place axis holds in all three
films and its frontal entries do not, and the frontal differences between films are not
significant (§5.7.2) — which, at three films, also means a real film-by-dial interaction of
modest size would go undetected. Technicolor features from 1937–1951 share conventions of
lighting, staging and lens that contemporary cinema does not; generalisation beyond them is
untested.

**Effect sizes are design-conditional.** Segments were deliberately selected to spread
each dial's range, which inflates dial variance relative to a random sample of cinema.
Estimates therefore do not describe "the effect in typical film".

**Almost nothing reaches the smallest effect worth calling a finding, and the threshold
itself is a heuristic.** 101 of 180 parcels survive the permutation null, but only 9
exceed the SESOI of 0.5 on the registered statistic, and only 6 of 2,520 dial–parcel
pairs on the marginal statistic it was derived for, none securely. The median survivor
implies *r* ≈ 0.07 against real cortex. The count of surviving parcels is the weaker of
the numbers and should not be quoted without the others. The threshold's own range runs
from about 0.10 to 0.47 depending on how TRIBE's accuracy is propagated (§3.2), so
"below the line" is a judgement anchored in the measurement chain, not a measurement.

**Criterion 1 was too lenient to be informative.** It asked for at least 3 of 14 dials
with one surviving parcel each, and with a broad fit and an L1 penalty it could not have
failed (§5.3.5). It was met; it does not show much. A per-dial bar would.

**The dial set has no audio or content dial, and speech is a large one.** All fourteen
dials describe the picture. Measured afterwards (§5.7.2), speech proportion tracks auditory
cortex within film at *r* +0.78 and, added to the dials, lifts out-of-sample within-film
*R*² for the auditory cluster from −0.09 to +0.54; it also carries part of the auditory
cut-rate signature, because faster cutting goes with less dialogue. The index's auditory
coefficients for any dial correlated with speech are therefore partly speech coefficients.

**Observational data cannot separate covarying dials.** With a condition number of
58.8 and a near-redundant lighting/colour cluster, any association inside that cluster
will attribute poorly no matter how the regression is regularised. Elastic net manages
the instability; it does not manufacture identifiability. Separating those dials
requires generated ladders that hold all but one fixed, as stage 03 did for cut rate;
none has been run for lighting or colour.

**Cut rate is the weakest dial in the design, and it is not a frontal lever in the
index.** At *s* ≈ 0.66 it carries the most between-film signal, which within-film
centring removes, and it is the dial the replication check depended on; the sample size
was raised to keep that check informative, but it remained the thinnest margin in the
study. The index has no cut-rate weight on inferior-frontal cortex to steer with, and the
exploratory refits show none is hiding under the penalty. Any control law that reaches
frontal cortex through cutting rests on constructed material: at full strength on
scene-alternating intercuts (stage 03), and at 0.18–0.48 of that on same-scene hard cuts
and scene-changing dissolves (stage 03b).

**The null may still be lenient in a way we have not tested.** A declared exploratory
check with permutation restricted within film returned 99 of 180 against the registered
101, with a marginally narrower null, so film-blocking structure is not inflating the
result. Temporal adjacency between neighbouring segments within a film is a separate
dependence that neither permutation preserves, and it remains untested. Treat 101 as an
upper bound.

**The hyperparameters of the model were not pre-registered.** The registration
specified "a cross-validated elastic net" without fixing α, l1_ratio or fold count.
Those were set before the run to the values already present in the pre-registered
futility script, and are disclosed in §5.3.7, but they were a residual degree of freedom
that a tighter registration would have closed.

**The map is exploratory.** §6 was not registered, and its subspace is fitted to the
responses it is then shown to align with, which is why every claim there is made against
label-shuffled fits. What survives that comparison is narrow: which dial leads the dominant
axis, and a five-point gain in retained variance over a fit to noise.

#### Of the controlled designs

**Five levels, one scene pair, and a *p*-floor.** Five levels allow 120 orderings, of which
the true one and its mirror are indistinguishable, so no count can do better than
*p* = 0.017. Stage 01 reaches that floor and stage 03 sits one ordering above it. The
designs cannot separate a strong effect from a very strong one, and the pre-fixed bar of 15
parcels is cleared by 8–17% of random orderings. Stage 03's verdict is PARTIAL-A by a
margin of 0.001 on one parcel — a near-miss reported as a miss. Seven levels, or two scene
pairs, would have cost little more.

**Generated footage, one generator.** Stages 03 and 03b are licensed only on footage from
`minimax/h3-max`, which 01b showed the sensor reads faithfully for a face and less so for
wide shots (§5.4); that is one axis of transfer measured, not distribution-matching in
general. Stage 03's face base fell short of its shot-scale target (`face_area_frac` 0.052
against 0.10), so its face/place contrast is weaker than stage 01's.

**Stage 03's audio arms are not a clean speech factor.** S+ is speech *with* an audio
discontinuity at every cut; S− is no speech with continuous sound (§5.5). The frontal
conclusion survives this, because the effect is present in both arms, so it needs
neither speech nor an audio discontinuity. The auditory conclusion rests on S−, where
visual cuts alone suffice. But nothing that differs *between* the arms — A5 most
visibly — can be attributed to speech.

#### Of the reconciliation

**The frontal miss is smaller than it looked, and is not shown to be small rather than
absent.** Stage 03 shows that the auditory signature is a property of cutting on this
sensor and that the frontal effect is causal on intercut generated footage. It does not
show why real cinema lacks the frontal effect. The scene-switch hypothesis was tested
observationally with a histogram proxy and not supported (§5.7.1); stage 03b tested it by
construction and found scene change alone carries about half the frontal effect (§5.6). The
two tests disagree, and with three films and a proxy that separates within- from
between-scene cuts only partially on live action, this design cannot say which is wrong.
03b lowers the corpus effect the frontal parcels should have shown to *r* ≈ +0.05 to +0.20,
and §5.7.2 finds the per-film frontal differences within noise; together they make the miss
unsurprising, but an undetected small effect and an absent one are not distinguished at
three films.

### 8.2 Future work — a programme of explorations

Each item is a specifiable next exploration: a design, a cost tier, and the result that
would falsify the current reading. Tiers: **A** free (existing data, local compute); **B**
under $20; **C** $20–200; **D** needs resources this programme does not have. Where this
paper has already run part of an item, the item says what was done and what remains.

**F1 · Close the model–brain gap for the dials that matter (tier C–D; the most important
item).** Real fMRI on feature films exists publicly: the Naturalistic Neuroimaging Database
(Aliko et al.; 86 participants, 10 films) and the movie data TRIBE itself was fitted on.
Measure the 14 dials on those films with `cinemetrics.py` unchanged, add speech and semantic
descriptors (F5), fit the same within-film-centred model to *real* parcel responses, and
compare the coefficient maps with this index parcel by parcel. The films must be sourced;
the dial pipeline runs as is. *Falsifies:* if the face/place axis and the auditory cut
signature do not appear in real BOLD at any size, the index is a property of TRIBE and the
programme's inversion thesis is about a model. *Supports:* an axis-1 correlation above the
permutation null on real data would be the first result in this programme that is about a
brain.

**F2 · Scene change versus large visual change (tier B).** *Done in part: discontinuity
versus switch is stage 03b (§5.6), GRADED.* What remains is the broad encoder-artefact
reading — a response to any large change in the encoder's input. Ladders whose joins are
large visual changes *within* one scene (a dissolve to a reframed or regraded take of the
same scene), scored against 03b's dissolve ladder, separate the two; a second scene pair
tests 03b's scene-dependence (face 0.44, landscape 0.18 of the frontal effect at matched
discontinuity). *Falsifies* the scene-change reading of the frontal effect if within-scene
visual change produces it at the dissolve ladder's size; *supports* it if it does not.

**F3 · Text branch on, and a clean speech arm (tier B).** Rescore the stage-00 clips, the
stage-03 bases and one ladder arm with the language branch enabled, and report the
whole-vector and named-parcel change; diagnose the failed attempt within a bounded effort,
or report the bound. Add stage 03's missing third arm — one continuous dialogue bed under
both scenes — which separates speech from audio discontinuity and decides what A5's arm
difference is about. *Falsifies* the paper's video-and-audio results as representative of
the full model if the named parcels move materially with text on.

**F4 · Corpus expansion with film as a random effect (tier B–C).** Six public-domain
live-action Technicolor features were verified; three were used. Add three, re-run the dial
pipeline (free), score 25 segments per new film (~$13, estimated), fit a mixed model with film random
slopes on the cut-rate and face dials, and report the slope variance. §5.7.2's interaction
test had little power at three films; the slope variance, not a sign test, is the quantity
to estimate. *Falsifies* the index as film-independent if slope variance dominates;
*supports* corpus-conditionality as the correct reading either way and makes it
quantitative.

**F5 · Speech and semantic content as dials (tier A, then with F4).** *Done in part:
§5.7.2 measured speech proportion and semantic change and found that neither carries the
frontal sign difference, which is itself not demonstrated.* What remains follows from what
it found instead: speech proportion explains more within-film auditory variance than the
fourteen visual dials together. The next registered index should include speech and
semantic descriptors as dials from the start, fixed in the registration rather than added
after the result. Free on the 244 segments already cut.

**F6 · Isolate face area, then the lighting cluster, by construction (tier B–C).** Face area
is the strongest lever the index found and the dial the inversion thesis rests on: a
control law built from this index would reach faces first. That is a measured association,
not a causal claim. Stage 03's recipe for it: generated single-take scenes at 3–5 face-area
levels with everything else prompted constant, measured with `cinemetrics.py` before
scoring, criteria first. Then luminance and saturation separately, which observational data
structurally cannot attribute (§5.3.3). Each ladder ~$5–15.

**F7 · Ladder designs with resolution (tier A, method).** *Done in part: the
level-permutation null is now this paper's method for ladders (§4.10), and stages 01, 03 and
03b are reported against it.* What remains: register it, with the whole-vector monotonicity
and the participation ratio, and use at least seven levels or two scene pairs so that the
*p*-floor falls below 0.01.

**F8 · Cut-locked responses inside a clip (tier B).** *Done in part: the Space now saves the
1 Hz timeline, and a first exploratory analysis on 03b found no clean join-locked transient
— only a shape recurring at fixed lags whatever the join type, more likely the model's
windowing than the join (§5.6).* What remains is a design that separates the two: joins at
jittered, non-periodic times, so that a join-locked response and a window-locked artefact
predict different averages. This is the analysis that would distinguish "cuts" from "what
cuts accompany" inside a single clip.

**F9 · Stage 04 as projection, then as a controller (tier C).** Inversion cannot mean
specifying an arbitrary cortical profile (§6). Choose a target *inside* the reachable
subspace, derive a dial setting, generate, measure, and test whether the achieved profile
lands within a pre-fixed distance of the prediction, against a permutation null over dial
settings; targets outside the subspace would fail for geometric reasons that have nothing
to do with whether the index is right. Then the film's premise as an experiment: a
hill-climber on the index with a generator in the loop, run for a fixed budget of clips,
with the pre-registered prediction that its trajectory moves along axis 1 towards faces. If
cut rate is among the dials it moves, the frontal target is reachable at full strength
only on scene-alternating material, at about half strength through dissolves or same-scene
cuts in a face scene, and barely through same-scene cuts in a landscape; the auditory
target needs hard cuts. One generator, and no claim about live action.

**F10 · Registration practice (tier A).** *Done in part: the registration's false statement
about its own futility check was corrected through OSF's update process on 20 September
2026 (§7).* What remains: deposit the stage 03 and 03b criteria at their commit hashes (03b:
`221faad`); register every future stage on OSF before generation; fix hyperparameters and
the count null in the registration; and keep verdict tables to outcomes, not mechanisms
(§7).

---

## 9 · Status

| stage | verdict | what it licenses |
|---|---|---|
| 00 · Probe | **PASS** | TRIBE separates content along a reciprocal face/place axis (§5.1) |
| 01 · Gate | **PASS** | cut count alone, on identical footage, moves the sensor — most strongly in inferior-frontal cortex (§5.2) |
| 02 · Index | **PARTIAL** — registered at `osf.io/dg7fe`; criterion 1 met, criterion 2 not | every dial associates with the sensor across real cinema, weakly; cut rate's association is auditory, not frontal (§5.3) |
| 01b · Transfer | **PASS** | one generator's footage moves the same face/place axis, so ladders may use it (§5.4) |
| 02b · Generalisation | exploratory, *n* = 3 | a reason to expect the index to transfer to generated footage; not a finding (§5.4) |
| 03 · Isolation | **PARTIAL-A** | cutting alone raises inferior-frontal and lowers auditory response, with and without speech; not that the frontal effect needs speech (§5.5) |
| 03b · Discontinuity | **GRADED** | hard cut and scene change each carry part of the frontal effect; the auditory effect follows the hard cut (§5.6) |
| — · Why the corpus lacks the frontal effect | exploratory | the frontal miss needs no film-specific explanation; speech is a missing auditory dial (§5.7) |
| 04 · Inversion | not started | — respecified as projection onto the reachable subspace (§8.2, F9) |

---

## Sources

Each entry verified against its primary record (CrossRef, PubMed, arXiv, bioRxiv or DataCite) on
8 October 2026; preprints checked for published versions, none found.

- Aliko, S., Huang, J., Gheorghiu, F., Meliss, S., & Skipper, J. I. (2020). A naturalistic
  neuroimaging database for understanding the brain using ecological stimuli. *Scientific Data*,
  7, 347. https://doi.org/10.1038/s41597-020-00680-2
- Baldassano, C., Chen, J., Zadbood, A., Pillow, J. W., Hasson, U., & Norman, K. A. (2017).
  Discovering event structure in continuous narrative perception and memory. *Neuron*, 95(3),
  709–721.e5. https://doi.org/10.1016/j.neuron.2017.06.041
- Cao, Z., Wang, Y., Li, R., Xiao, X., Xie, Y., Bi, S., Wu, L., Zhu, Y., & Wang, Y. (2024).
  Exploring the combined impact of color and editing on emotional perception in authentic films:
  Insights from behavioral and neuroimaging experiments. *Humanities and Social Sciences
  Communications*, 11, 1349. https://doi.org/10.1057/s41599-024-03874-w
- d'Ascoli, S., Rapin, J., Benchetrit, Y., Banville, H., & King, J.-R. (2025). TRIBE: TRImodal
  Brain Encoder for whole-brain fMRI response prediction. arXiv:2507.22229.
  https://doi.org/10.48550/arXiv.2507.22229
- Geerligs, L., Gözükara, D., Oetringer, D., Campbell, K. L., van Gerven, M., & Güçlü, U. (2022).
  A partially nested cortical hierarchy of neural states underlies event segmentation in the
  human brain. *eLife*, 11, e77430. https://doi.org/10.7554/eLife.77430
- Kauttonen, J., Hlushchuk, Y., & Tikka, P. (2015). Optimizing methods for linking cinematic
  features to fMRI data. *NeuroImage*, 110, 136–148. https://doi.org/10.1016/j.neuroimage.2015.01.063
- Lakens, D. (2022). Sample size justification. *Collabra: Psychology*, 8(1), 33267.
  https://doi.org/10.1525/collabra.33267
- Lakens, D. (2022). *Improving Your Statistical Inferences* (v1.0.0), ch. 8. Zenodo.
  https://doi.org/10.5281/zenodo.6409077
- Leipold, S., Ravi Rao, R., Schoffelen, J.-M., Bögels, S., & Toni, I. (2024). Between-movie
  variability severely limits generalizability of "naturalistic" neuroimaging (version 1).
  bioRxiv. https://doi.org/10.1101/2024.12.03.626542 — retitled in version 3 (2026),
  *Inter-subject correlations and their behavioral associations vary across movies:
  Implications for generalizability*. Earlier drafts of this paper misattributed it to
  "Gruber et al."
- Scotti, P. S., & Tripathy, M. (2025). Insights from the Algonauts 2025 winners.
  arXiv:2508.10784. https://doi.org/10.48550/arXiv.2508.10784

Data and services, not peer-reviewed:

- Internet Archive metadata API, per identifier, read 3 September 2026.
- Hugging Face Spaces hardware pricing (A10G Small, $1.00/hr).

Tools: analysis and writing used the Scientific Agent Skills library (Kassis, T., Agarwal, V.,
He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent Skills: A Library of Procedural
Knowledge for Research Agents. arXiv:2609.00065. https://doi.org/10.48550/arXiv.2609.00065).

## Internal documents

`experiments/ROADMAP.md` · `experiments/LOG.md` · `experiments/OBJECTIVES.md` ·
`experiments/00-probe/{README,RESULT,CLIPS}.md` ·
`experiments/01-cutrate/{README,RESULT}.md` ·
`experiments/02-index/{README,CORPUS,DIALS,RESULT,frontal_miss,scene_switches,content_descriptors}.md` ·
`experiments/01b-transfer/{README,RESULT,CLIPS}.md` ·
`experiments/02b-generalisation/RESULT.md` ·
`experiments/03-isolation/{README,RESULT,CLIPS}.md` ·
`experiments/03b-discontinuity/{README,RESULT,CLIPS}.md`
