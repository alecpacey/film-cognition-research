# A technique→response index for cinematography, measured through a brain encoding model

**Working paper · draft of 15 September 2026**
**Status: stages 00, 01, 02 and 03 complete and reported, with the 01b transfer gate and
an exploratory 02b generalisation check. Stage 02's analysis plan was registered at
`osf.io/dg7fe` before the analysis was run; it returned PARTIAL. Stage 03, criteria fixed
before generation, returned PARTIAL-A and reconciles stages 01 and 02.**

---

## Abstract

Film craft is taught as a set of dials — cut rate, shot scale, lighting key, camera
movement, colour — but the relation between those dials and a viewer's neural
response is documented only piecemeal, one dial at a time, in studies that rarely
share a stimulus set or an analysis. We ask whether that relation can be measured
systematically enough to be **inverted**: given a target cortical response profile,
choose the technique that reaches it.

The instrument is TRIBE (Meta AI, winner of the Algonauts 2025 challenge), a
trimodal encoding model that predicts whole-cortex fMRI response from video, audio
and text. Using an encoding model as a *measurement device* rather than as a
prediction target is the methodological move this programme rests on, and it
carries a scope condition we state at the outset and never relax: **the dependent
variable is a model's prediction of cortex, not cortex.** Every claim inherits
TRIBE's accuracy against real brains — mean Pearson *r* = 0.3195 in-distribution and
**0.2146 out-of-distribution** — and our corpus is further out of distribution than
that figure was measured on.

We report four completed stages. **Stage 00** establishes that the sensor
discriminates content: mean pairwise top-10 Jaccard overlap 0.15 against a
pre-registered threshold of 0.60, with a reciprocal double dissociation between the
voice chain (A5, STSdp) and the place chain (VMV2, PHA1/2) and a graded intermediate
condition. **Stage 01** establishes that *technique* moves the sensor with content
held constant: intercutting two fixed 60-second scenes at five rates moved 51 of 180
parcels to |*r*| > 0.9 against log cut count, against a pre-registered bar of 15; against
the correct null, a permutation of the five level labels, that count has *p* = 0.017, the
floor of a five-level design. The strongest responders were inferior-frontal (IFJa
*r* = +0.996) rather than the dorsal-attention network the literature predicted —
coherent, since every cut is a task switch, but post-hoc and treated as a hypothesis
rather than a finding.

**Stage 02**, the observational index, was pre-registered at `osf.io/dg7fe` before
its analysis was run, and returned **PARTIAL** — the outcome the pre-registration
named in advance as the most important one available. Three public-domain live-action
Technicolor features were cut into 244 fixed 60-second segments, normalised to a
common encode, and measured on 14 cinematographic dials; 70 segments were selected by
stratified maximin sampling across dial ranges and scored. We derive a smallest effect
size of interest of *r* ≥ 0.5 from TRIBE's published out-of-distribution accuracy
rather than asserting a convention, and set *n* = 70 from that.

The first pass criterion was met and the second was not. All 14 dials carry weight in
at least one of 101 parcels surviving a 1,000-permutation null under FDR correction —
but **cut rate does not replicate where stage 01 put it.** IFJa, stage 01's strongest
responder at *r* = +0.996 on identical footage, is indistinguishable from its null
here; the one cluster parcel that survives does so with *exactly zero* weight on both
cut-rate dials. Observationally, cut rate loads on auditory and early visual cortex,
never frontal. We read this as the difference between varying cutting with nothing
else changing and measuring it where it co-occurs with dialogue, close-ups and
interiors — but which track is wrong is not decidable from this data, and that it must
be resolved before anything is built on cut rate is the finding.

**Stage 03** resolves it under control. Two generated single-take scenes (0 cuts measured)
were intercut at exactly 1, 3, 7, 15 and 31 cuts per minute — a 31× range against stage
01's effective 2.1× — in two arms, with the face scene's dialogue present (S+) or replaced
by continuous ambient sound (S−), criteria fixed before generation. **Cutting alone drives
inferior-frontal cortex up and auditory cortex down, in both arms**: 58 and 54 of 180
parcels reach |*r*| > 0.9 against log cut count (level-permutation *p* = 0.025 in each
arm); IFJa, IFSp and 8C reach
+0.91 to +0.93 with speech and +0.89 to +0.90 without; A4, A1 and MBelt fall to −0.92 to
−0.97 in both. The pre-fixed verdict is **PARTIAL-A**, because the no-speech arm puts one
rather than two cluster parcels over the 0.9 bar — three miss it by 0.001 to 0.03 at
*n* = 5 levels — and we report that verdict as fixed while stating plainly that the
mechanistic reading the verdict table attached to it, that the frontal effect *requires*
speech, is not supported by these numbers. **Stages 01 and 02 were each right about half
of one effect.** The observational index recovered the auditory half and missed the frontal
half; an exploratory follow-up on the frozen stage-02 data shows why: the elastic net zeroed
frontal cut-rate weights that are indistinguishable from zero unpenalised (|*t*| < 1), the
raw within-film correlation of IFJa with cut rate is −0.005 and flips sign between films,
and transplanting stage 03's causal slopes into the corpus's variance predicts *r* ≈ +0.3
to +0.45 for the frontal parcels where the auditory parcels come in at their predicted
size. The frontal response to cutting is absent from these three films at that size.
The one hypothesis that survived was that inferior-frontal cortex responds to *scene
switches*, which in the intercut ladders are identical to cuts and in cinema mostly are
not; a between-scene cut count built to test it finds no frontal association at any
threshold, with the same film-flipping sign, while auditory cortex follows cuts of every
kind. The frontal miss is a property of this corpus and remains unexplained.

Two results qualify the first criterion and are reported with equal prominence. The
dominant dial is **face area**, largest coefficient in 65 of the 101 survivors, whose
signature reproduces stage 00's double dissociation to the parcel; a controller
maximising predicted response would find faces the lever with the most reach, which
is a measured claim where it was previously a predicted one. And **only 9 of 180
parcels exceed the derived SESOI**, median survivor *r* = 0.35 implying roughly
*r* ≈ 0.07 against real cortex — so surviving a permutation null and reaching the
smallest effect worth calling a finding are not the same thing, and most of this
result falls on the wrong side of that line. A declared exploratory sensitivity check
using a restricted within-film permutation returns 99 of 180 with a marginally
*narrower* null, so the headline count is not an artefact of a lenient test.

Characterising the fitted crosswalk as a map — exploratory, and the artefact the
programme was built to produce — gives a structural result, and a correction to our own
first reading of it. Three components carry 90% of the index's variance, interpretable as
a face/place axis (69%), a motion axis (14%) and a colour axis (6%). **That
low-dimensionality belongs to the sensor's response space, not to technique**: refitting
the same model to label-shuffled responses gives an index just as concentrated (three
components 89%, *p* = 0.42), whose first axis aligns with the first principal component of
cortical variation almost as well. What is specific to technique is narrower and survives
the shuffled null: **face area is the dial that leads the dominant axis** (loading 0.80
against a null 95th percentile of 0.57, *p* = 0.010), and the index's subspace retains
90.8% of observed profile variance against a shuffled-label floor of 85.5% (*p* = 0.005) —
not against the 7.8% of a random subspace, which was the wrong comparison. The bound on the
programme's endpoint stands and is if anything tighter: **inversion is projection, not
solution** — an arbitrary target profile is not reachable, because this sensor's responses
to cinema occupy about three dimensions and technique can command no more than that — and
the direction technique commands most strongly is the face/place axis.

We also report method failure as evidence. Six of seven failures in stage 00 were
assumed API shapes rather than model or data problems; clip uploads were silently
dropped by a `.gitignore` rule while reporting success; and a "fact" recorded in the
project handoff — that background log pollers had been *killed* — was a wrong
diagnosis of a blocking read on a stream that never closes. The registration itself
carried an error of the same kind: it stated three times that a pre-registered interim
check had never been executed, inferred from the absence of any record of it on disk.
The check had in fact been run, and the registration was corrected through OSF's formal
update process on 20 September 2026. **When
an instrument returns plausible numbers whatever you feed it, silent failure is the
central methodological hazard**, and the discipline that catches it — including when
it catches the authors — is worth reporting alongside the results it protects.

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
TRIBE, the Algonauts 2025 winner, predicts responses across 1,000 cortical parcels
from video, audio and time-aligned text.

Using it as an instrument has one large advantage and one large cost.

The advantage is that **the measurement is deterministic**. TRIBE's released
checkpoint has no subject-specific parameters, so predictions are identical whoever
is nominally watching, and identical on repeated runs — verified in stage 00, where
an independent re-run reproduced parcel values to two decimal places (LO2 +2.43 vs
+2.43, A5 +2.37 vs +2.38, STSdp +2.04 vs +2.04). There is no trial-to-trial noise, no
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
The production brief adopts one rule that this paper inherits: **nothing is claimed
as tested that has not been tested here, and every figure is either sourced to a
primary document or explicitly marked unmeasured.** The subject invites overclaiming
— a system that predicts brain activity is very easy to describe dishonestly — so the
distinction is structural rather than decorative.

### 1.4 Contributions

1. A **derived** rather than conventional effect-size threshold for encoding-model
   studies, obtained by propagating the model's published accuracy through to the
   claim being made (§3.2).
2. A **two-track design** separating what observational data can establish
   (association across real cinema) from what only controlled generation can
   (isolation of covarying dials), with the boundary stated in advance.
3. A corpus decision made by **overturning our own prior assumption on evidence**
   (§4.1), including the finding that animation — proposed as the corpus on
   availability grounds — is the *minimum*-variance case for the covariance-breaking
   the design requires.
4. A **detectability classification** that distinguishes "this dial did not move the
   sensor" from "this dial never varied enough to test", two results that a
   conventional drop-low-variance-predictors step would have merged (§4.6).
5. A report of **silent-failure modes** in this class of pipeline, and the practices
   that surfaced them (§7).

---

## 2 · Hypotheses

The programme is a chain. Each link gates the next and is permitted to break it.

| | Hypothesis | Status |
|---|---|---|
| **H0** | TRIBE discriminates content — different kinds of scene produce different parcel profiles, in anatomically interpretable directions | ✅ **Supported** (stage 00) |
| **H1** | Cinematographic *technique* moves the predicted response with content held constant | ✅ **Supported** (stage 01, cut rate only) |
| **H2** | Across real cinema, measured technique dials predict parcel-level response profiles, recoverably by penalised regression | ✅ **Supported** (stage 02) — 14/14 dials, 101/180 parcels. But only 9 parcels reach the SESOI |
| **H2b** | The controlled cut-rate result of stage 01 reappears observationally | ❌ **Not supported** (stage 02) — IFJa at its null; the one surviving cluster parcel has zero cut-rate weight. **Explained by stage 03 (§6.8)**: the observational index recovered the auditory half of the cut effect and the corpus does not carry the frontal half |
| **H3** | At least some of those associations are causal, demonstrable by holding all dials fixed and moving one | ✅ **Supported** (stage 03, verdict **PARTIAL-A** against the pre-fixed table) — cutting alone, content fixed by construction, drives IFJa / IFSp / 8C up and A4 / A1 / MBelt down on generated footage in both speech arms; the no-speech arm misses the 0.9 bar on three cluster parcels by ≤ 0.03 at *n* = 5 |
| **H4** | The mapping can be inverted — a target profile selects a technique, and the achieved profile matches | Not started (stage 04). **Bounded in advance by §6.7**: the reachable set is ~3-dimensional — a property of the sensor's response space, which technique cannot exceed — so inversion is projection onto it, and the inverse is many-to-one |

**H2b deserves emphasis.** It is the only place in the design where the controlled
and observational tracks can contradict each other. If cut rate moves the sensor on
identical footage but shows no association across real cinema, one of the two results
is wrong, and that must be resolved before anything is built on either. The
pre-registration names this outcome **PARTIAL** and calls it the most important
possible finding — which is why §4.5 records that we raised the sample size
specifically so that this check would be able to fail informatively. It did fail, and
stage 03 (§6.8) then showed that neither track was wrong: cutting has a frontal and an
auditory signature, and the observational corpus carries only the second.

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
| Parcels | 181 returned; index 0 is `???` and is dropped, leaving **180 usable** |
| Throughput | ~10 min per 60 s clip on an A10G — roughly **10× slower than real time** |
| Determinism | reproduces to 2 d.p. across independent runs |

### 3.2 The scope condition, stated quantitatively

The dependent variable is TRIBE's prediction, not measured cortex. The link between
the two is published:

| | Pearson *r* |
|---|---|
| In-distribution (Friends season 7) | 0.3195 |
| **Out-of-distribution** | **0.2146** |
| Noise-ceiling-normalised | 0.54 ± 0.1 (54% of explainable variance) |
| Best individual regions, normalised | 0.77 – 0.85 |

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

**We adopt SESOI = *r* ≥ 0.5**, the conservative row rounded up. The generous row is
recorded so the choice is visible rather than buried: it would put the threshold near
0.19 and demand roughly 200 segments.

Two things about this derivation are worth stating plainly. First, it follows
Lakens' requirement that a smallest effect size of interest be *justified* rather
than asserted, and the justification used here is the measurement chain itself — a
theoretical/practical anchor rather than a convention or a resource constraint.
Second, it argues for a **higher** threshold and therefore a **cheaper** study. A
dial reaching only *r* = 0.3 in a measurement with no noise in it would be worth
almost nothing once passed through a 0.21 bottleneck. The mediation reading is
first-order and approximate; §4.5 records the sample-size headroom taken to absorb
that.

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

**Gruber et al. (2024)**, *Between-movie variability severely limits generalizability
of "naturalistic" neuroimaging* (bioRxiv 2024.12.03.626542), is the most consequential
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

---

## 4 · Methodology

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

The second failure is more interesting, and comes from Gruber et al. They selected
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

Head and tail of each film are skipped (5% each end). The corpus plan specified
recording scene-boundary counts per segment as a diagnostic, not a covariate. **That count
was never implemented**: no scene-boundary field exists in the dial table or in any
per-segment measurement file, and `cinemetrics.py` counts cuts without classifying them
as within- or between-scene. An earlier draft of this paragraph stated the count was
recorded; it was not, and the omission matters — §6.8 ends on a hypothesis that turns on
exactly that distinction. An exploratory between-scene cut count now exists for all 244
segments (`02-index/scene_switches.py`, 16 September: cinemetrics' cut detector unchanged,
each cut scored by the HSV-histogram distance between the adjacent shots); it is a measured
diagnostic, not a registered dial.

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
within-film centring across three films:

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
construction (§6.2), and unregularised regression is unstable there.

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

---

## 5 · Results — completed stages

### 5.1 Stage 00 · Discrimination probe

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

**Question.** Does cinematographic *technique* move the sensor with content held
constant? This is the first genuine test of the thesis and the first thing capable of
killing it.

**Design.** The two most orthogonal clips from stage 00 (face and landscape,
whole-vector *r* = −0.098) intercut at five rates: 1, 3, 7, 15 and 31 added cuts.
**Every condition contains exactly the same 30 s of each scene.** Colour, luminance,
motion, subject matter and audio are all held; only the number of cuts differs.

Cut rate was chosen as the gate rather than as part of the index because it is the
only dial that can be varied with content perfectly constant, and it carries the
largest documented effect in the literature (montage context, η²ₚ 0.715). If
technique could not move the sensor when varied this cleanly and this strongly, no
subtler dial would.

**Criteria, fixed before the run.** (1) Count: at least 15 of 180 parcels reach
|*r*| > 0.9 against log cut count — with *n* = 5, *r* = 0.9 is *p* ≈ 0.037, so ~7 are
expected by chance, and the bar is twice that. (2) Anatomy: the dorsal-attention
family (IPS1, FEF, LIPv, VIP, V7, PEF, IP0) over-represented relative to its 7/180
base rate.

**Result: PASS on both.**

**51 of 180 parcels** reached |*r*| > 0.9, against a bar of 15. **The criterion's "~7 by
chance" was wrong, and an earlier draft's "seven times chance" with it.** That figure treats
180 parcels as independent; across the five levels the cortex moves along roughly one
direction (participation ratio 1.85 of a possible 4), so the count behaves like a single
event. The correct null permutes the five level labels (`ladder_count_null.py`, 120
orderings): median count 3, 95th percentile 28, and 17% of random orderings clear the bar of
15. The observed 51 is matched only by the true ordering and its mirror image — *p* = 2/120
= 0.017, **the most extreme result a five-level design can produce, and no stronger than
that**. The pre-fixed verdict stands; the bar was weaker than we believed. Dorsal attention was
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
conditions is few; the defence is the count (51 ≫ 7) and the anatomical coherence, not
any single parcel.

---

## 6 · Stage 02 · The observational index — PARTIAL

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

### 6.0 Verdict

| criterion | required | found | |
|---|---|---|---|
| 1 · dials with ≥ 1 surviving parcel | ≥ 3 of 14 | **14 of 14** | met |
| 2 · cut rate replicates in {IFJa, IFJp, IFSp, 8C} | yes | **no** | not met |

**PARTIAL.** The pre-registration names this outcome, in advance, as the most
important one available: it means the observational and controlled tracks disagree,
and one of them is wrong. §4.5 records that the sample size was raised from 60 to 70
specifically so that this check could fail informatively. It has.

### 6.1 Pass criteria, as fixed

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

### 6.2 Stimulus-side diagnostic: dial interdependence

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
resolve that; it is a stage-03 question and will be written up as one rather than
argued away.

### 6.3 Detectability at *n* = 70

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

### 6.4 Criterion 1 — technique predicts the sensor, broadly but weakly

**101 of 180 parcels survive** a 1,000-permutation segment-label null under
Benjamini–Hochberg FDR at *q* < 0.05, and **every one of the 14 dials** carries a
non-zero coefficient in at least one survivor. All 14 were classified TESTED at
*n* = 70 before the run, so every result below is a real result and not an untested
one. There are no nulls to report.

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
finding, and most of this result falls on the wrong side of that line.** Among
survivors, cross-validated *r* has median 0.35 (IQR 0.28–0.44, max 0.61). **Only nine
parcels exceed the pre-registered SESOI of 0.5** — PCV 0.61, POS2 0.55, DVT 0.55,
7Pm 0.55, 31a 0.54, 6v 0.53, POS1 0.53, 7Am 0.52, V3 0.50. Passed through TRIBE's
out-of-distribution accuracy of 0.2146, a survivor at the median implies roughly
*r* ≈ 0.07 against real cortex. §3.2 derived that threshold precisely so this
distinction would be visible rather than buried under a count of significant parcels.

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
the others, and pools to nothing. The same split appears for cut rate (§6.8): auditory
parcels negative in every film, frontal parcels of opposite sign in two. **The index's
dominant axis is a property of all three films; its frontal entries are not a property of
any pooled fit.**

**The lighting/colour cluster** is dominant in 25 survivors and, per the
pre-registration, is reported as an association with the *cluster*. §6.2 fixed that
consequence before any result existed: with condition number 58.8 and
`median_luma`~`shadow_frac` at −0.90, this design can establish that the cluster
matters without saying which member drives it.

### 6.5 Criterion 2 — cut rate does not replicate where stage 01 put it

| parcel | CV *r* | null 95th pct | *q* | survives | coef cuts_per_min | coef mean_shot_len_s |
|---|---|---|---|---|---|---|
| IFJa | +0.044 | 0.178 | 0.191 | no | 0 | 0 |
| IFJp | −0.204 | 0.126 | 0.567 | no | 0 | 0 |
| IFSp | +0.346 | 0.221 | 0.015 | **yes** | **0** | **0** |
| 8C | +0.075 | 0.176 | 0.158 | no | 0 | 0 |

IFSp survives, and it survives with *exactly zero* weight on both cut-rate dials — its
model is carried by face area (+0.23) and camera zoom (−0.12). Stage 01's strongest
responder, **IFJa at *r* = +0.996 on identical footage, is indistinguishable from its
null here**. IFJp's point estimate is negative. The criterion required that the cluster
associate *with cut rate*; nothing in it does.

**Where cut rate goes instead.** Among survivors its largest weights are auditory and
negative — A4 −0.23, A1 −0.17, MBelt −0.16, A5 −0.13 — and early visual and positive —
PIT +0.17, MST +0.17, FFC +0.16, V8 +0.14. Mean shot length, its inverse, loads on the
place chain (PHA2 −0.22, VMV2 −0.17) and on motion-sensitive cortex (MT −0.17,
V3A −0.21). Neither dial reaches frontal cortex at all.

**A reading, stated as a reading — and one obvious version of it is ruled out by our
own data.** The natural explanation is confounding: stage 01 varied cut count on
identical footage, so every cut was a switch and nothing else changed, whereas stage 02
measures cut rate where fast cutting co-occurs with other technique. **Among the
measured dials, it does not.** After within-film centring, `cuts_per_min` correlates
with every other dial except its own definitional inverse at |*r*| ≤ 0.194 — with
`face_area_frac` at −0.194 (faster cutting goes with *smaller* faces, not close-ups),
`camera_zoom` +0.163, `face_hit_rate` +0.145, and nothing else above 0.12. Cut rate is
the most nearly independent dial we measure, which §6.2 already recorded as VIF < 2.3.

So the confound, if that is what this is, lies in what we did **not** measure. The dial
set has no descriptor of speech, semantic content, narrative structure or scene type,
and the text branch was disabled throughout, so dialogue reached the instrument only as
audio. That the observational cut-rate signature is strongest in auditory cortex — and
*negative* there — while stage 01's was frontal, is consistent with the two designs
loading different unmeasured things, but we cannot show which. **We report the
disagreement and decline to explain it.** What this does establish is a requirement on
stage 03 that was not previously visible: controlling the fourteen measured dials is
not sufficient to isolate cutting, because they were never what cut rate was confounded
with.

**We do not claim which track is wrong.** Observational and controlled measurements of
the same dial disagree; that is the finding, and resolving it is a precondition for
building anything on cut rate. One candidate artefact deserves ruling out first: the
text branch was disabled throughout (§4.9), so dialogue reached the model only as
sound. In a corpus containing *Nothing Sacred*, a fast-talking dialogue picture, an
auditory cut-rate signature may be partly an artefact of the missing modality rather
than a property of cutting.

**Written before stage 03; left as written.** Stage 03 (§6.8) has since made the
separation this section asks for. Both halves of the reading above survive in modified
form: the frontal and auditory signatures are two parts of one causal effect, the
auditory part is a property of cutting and not of the missing text modality (it appears
with speech absent and the audio track continuous), and the reason the index missed the
frontal part is a property of the corpus, not of the regression.

### 6.6 Declared choices, and one exploratory check

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


### 6.7 The index as a map, and what it implies for inversion

**Exploratory. Not pre-registered, and none of it counts toward the pass criteria.**
The registered test asks whether dials predict parcels. It does not ask what the
resulting crosswalk *looks like* — and that crosswalk is the artefact the whole
programme was built to produce. This section characterises it. The object is the
180 × 14 matrix **B** of full-data elastic-net coefficients: column *k* is the
cortical pattern associated with dial *k*, and the set of response profiles technique
can reach is the span of those columns.

**Provenance and a correction.** This section was first written with no script committed
behind it. `02-index/index_map.py` (20 September) now rebuilds **B** from
`analysis_result.json` and reproduces all 45 figures below; its output is `index_map.json`,
with `index_map_followup.py` for the technique-specificity tests. The reproduction added the
comparison the first draft lacked — the same elastic net refitted to **label-shuffled**
responses, 200 times — and that comparison changes what the section may claim. Where the
first draft's reading does not survive it, the text below says so.

**The index is concentrated in about three dimensions — and so is an index fitted to
noise.** The singular values of **B** fall away sharply — 3.34, 1.52, 1.01, then nothing
above 0.75. Three components carry 90.1% of the index's variance and five carry 95.9%.
Restricted to the 101 surviving parcels, three components carry 92.7%. (The first draft
quoted participation ratios of 5.56 for **B**, 4.76 for the survivors and 8.35 for **Y**;
those were computed on singular values. On variances, the conventional definition, they are
1.97, 1.65 and 2.41.) Under label shuffling the index is just as concentrated: three
components carry 89.1% on average (5th–95th percentile 82.5–93.9%; observed 90.1%,
*p* = 0.42) and the first axis 66% (observed 69%, *p* = 0.39). **The console's three
outputs are a property of the sensor's response space across these segments, which itself
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
the same story §6.5 tells, arrived at without reference to stage 01.

**Technique is aligned with how this cortex varies, by a modest margin over a fit to
noise.** Projecting the observed 70 × 180 profile matrix onto the reachable subspace
retains **90.8%** of its variance. The comparison that makes that number meaningful is the
third row, which the first draft did not have:

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

**The first draft tempered this with a caveat and then claimed the wrong exception.** It
noted that **B** is fitted to **Y** and so aligned by construction, and said that what
fitting does *not* guarantee is the concentration and the coincidence of the first axis
with the dominant direction of variation. The shuffled-label fits show fitting guarantees
both: their first axis correlates with **Y**'s first principal component at 0.92 on average
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

### 6.8 Stage 03 · Isolation — PARTIAL-A, and the two tracks reconciled

**Criteria were fixed in `03-isolation/README.md` on 13 September 2026, before any
generation, and were not softened.** Run 14–15 September. Data `parcel_vectors.json` (12
clips × 180 parcels), script `evaluate_03.py`, full output `evaluation.json`; every figure
below is taken from that file.

**Question.** Stage 01 varied cut count on identical live-action footage and the sensor
answered in inferior-frontal cortex. Stage 02 measured cut rate across real cinema and found
no frontal association; cut rate loaded on auditory cortex, negatively. The measured dials do
not explain the disagreement (§6.5). Two candidates remained: stage 01's result was specific
to its two scenes, or the observational signature was confounded by something unmeasured,
speech above all. Stage 03 tests both with one design.

**Design — 2 × 5, content held fixed by construction.** Two scenes were generated with the
01b route (`minimax/h3-max`, 768P, 4 × 15 s chained), each a single continuous take: a face
scene (two people in conversation at a table) and a landscape. The single-take precondition
was measured, not assumed — 01b had shown the generator cuts within its own outputs at 7–15
per minute — and both bases returned **0 cuts** on `cinemetrics.py`. The two were then
intercut with stage 01's `build_conditions.py` unchanged at 1, 3, 7, 15 and 31 added cuts;
measured cut counts were **exactly 1 / 3 / 7 / 15 / 31**, a 31× range against stage 01's
effective 2.1×. Every level contains the same 30 s of each scene. The speech factor: **S+**
keeps the face scene's native dialogue; **S−** replaces all audio with the landscape's
continuous ambient track, so no speech is present and the sound has no discontinuity at any
cut. Video is byte-identical across arms. Scored on the unchanged stage-02 Space path,
`audio_only=True`; the two bases were scored as references.

**Pre-registered predictions.** H3a: in S+, at least 2 of {IFJa, IFJp, IFSp, 8C} reach
*r* > +0.9 against log measured cut count. H3b: the same in S−. PASS requires both;
**PARTIAL-A** (H3a, not H3b) was fixed in advance with the reading "the frontal cut effect
needs speech present"; PARTIAL-B (neither, but auditory tracks) would demote stage 01 to a
property of its two clips; FAIL if nothing tracks. Reported, not gating: the |*r*| > 0.9
count (the README took chance as ≈ 7 at *n* = 5; corrected below), whole-vector *r* cut01
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
genuinely 31×. Against the level-permutation null (§5.2) each count has *p* = 3/120 =
0.025 — the true ordering, its mirror image and one other — and some random orderings put
79 or 90 parcels over the bar, because the response across the ladder is close to
one-dimensional (participation ratio 1.25 and 1.20 of a possible 4). Two consequences. The
counts are near the strongest evidence five levels can give, not "eight times chance". And
"frontal up, auditory down" is the sign pattern of one response mode, not two independent
findings. PARTIAL-A stands because the criteria were
fixed and are not softened afterwards; the claim that speech is *required* for the frontal
effect must not be carried forward as a finding, and this paper does not carry it.

**Stage 02's observational signature reproduces under control.** In both arms cut rate is
strongly negative in auditory cortex — A4 −0.97 / −0.94, A1 −0.96 / −0.93, MBelt −0.95 /
−0.92 (S+ / S−) — and A5 joins them without speech (−0.95) while sitting at +0.15 with it.
This is what the index found in §6.5 and what stage 01 did not report. **Both earlier tracks
were right about different parts of one effect**: cutting drives inferior-frontal cortex up
and auditory cortex down, with or without speech, and — since S− has a continuous ambient
track with no discontinuity at any cut — the auditory decrease follows *visual* cut count,
not an interrupted sound stream. The alternative §6.5 raised, that the auditory signature
was an artefact of the missing text modality, does not survive an arm with no speech in it.

**Cut rate is therefore a causal lever on this sensor**, with the frontal and auditory
signatures both available as targets for stage 04 — on the material where it has been
shown, which is intercut generated footage (see the follow-up below).

**Limitations.** The regenerated face base reached `face_area_frac` 0.052 against a 0.10
target (a wide first attempt measured 0.035; no third attempt at the post-promotional
generation rate), so the face/place contrast between the bases is weaker than stage 01's;
the cut manipulation is unaffected. *n* = 5 levels per arm: |*r*| > 0.9 is a coarse
instrument and the arm difference is not resolvable at this *n*. Generated footage, one
scene pair, one generator — the scope 01b licensed. Text branch off, as in every prior
stage; a text-on replication is unrun.

**Spend and missteps, recorded.** Bases $3.60 on fal including one regeneration; scoring
≈ $2.2 on the Space for 12 clips plus one wasted restart. That restart was caused by a
watcher of ours that matched result files containing `"03_"` anywhere — which also matched
stage-02 ordinals and files from a separate experiment writing to the same results
repository — and paused the run at 6 / 12; corrected to exact-name matching, and the other
experiment has since been given its own results repository. The local machine killed
background tasks for memory twice; the Space finished the batch unattended and paused on
its inactivity timer. A text-branch rescoring attempted on 13 September produced 0 / 12
results after 189 minutes and is parked undiagnosed.

**Exploratory follow-up: why the index missed the frontal half.** Not registered; the
PARTIAL verdict of §6.0 is unchanged. Full note in `02-index/frontal_miss.md`, run on the
frozen stage-02 data. *The penalty is not the cause*: refitting the four cluster parcels on
the registered design matrix without regularisation gives cut-rate weights of +0.04 to +0.07
with the stage-03 sign and |*t*| < 1 (*p* 0.35–0.53); the elastic net zeroed coefficients
indistinguishable from zero, and kept the auditory quartet's (OLS −0.15 to −0.26, MBelt
*t* = −2.37). *The raw signal is absent*: IFJa's within-film correlation with cut rate is
−0.005, and the frontal sign flips between films (negative in *Jungle Book*, positive in
*Nothing Sacred*) while the auditory sign is negative in all three. *Range is not the
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
*p* ≥ 0.19); IFJa's sign still flips between films (+0.40 in *Nothing Sacred*, −0.25 in
*Jungle Book*); and the auditory decrease follows within- and between-scene cuts alike
(A1 and MBelt with within-scene cuts at −0.27 and −0.30, A4 and A5 with between-scene at
−0.22 and −0.25), which is stage 03's no-speech result seen in real cinema across cut types.
Because the proxy is partial on live action the hypothesis is weakened rather than excluded,
but a surviving effect would have to be small where the transplanted slopes say it should be
large. What stands: the frontal miss is not the penalty, not the range, not content variance
and not, by this measure, the composition of the cuts; the frontal parcels' relation to
cutting differs in sign between films, which points at film-specific content the dial set does
not measure. The index's cut-rate column should be read as the auditory half of the effect
only, and cut rate treated as a frontal lever solely on intercut material.

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

Three practices follow, and are now standing rules:

1. **Criteria are written in the stage README before the run and are never softened
   afterwards.** Every result in §5 is reported against a threshold fixed in advance.
2. **Persist to disk, not to the instrument.** The Space's filesystem is wiped on
   pause; stage 00's first full result set was lost that way and had to be re-run.
3. **Introspect before writing.** Seconds to check, ~35 minutes to get wrong.

---

## 8 · Limitations

Stated plainly, and none of them resolvable within this design.

**It is a model, not a brain.** Every result concerns TRIBE's predictions. The link to
real cortex is *r* = 0.2146 out-of-distribution, and our material is further out than
that figure was measured on. §3.2 turns this into the effect-size threshold rather
than leaving it as a disclaimer, but no analysis here can escape it. A finding that
technique moves TRIBE is a finding about TRIBE.

**The index will be corpus-conditional.** Three films is enough to break dial
covariance; it is not enough to claim film-independence. Gruber et al. found
associations landing in non-overlapping regions for nearly every one of eight films,
and concluded that a specific movie should be treated like a specific task. Our index
should be read the same way, and the stage-02 report must say so rather than leave it
to be discovered.

**Effect sizes are design-conditional.** Segments were deliberately selected to spread
each dial's range, which inflates dial variance relative to a random sample of cinema.
Estimates therefore do not describe "the effect in typical film".

**Observational data cannot separate covarying dials.** With a condition number of
58.8 and a near-redundant lighting/colour cluster, any association inside that cluster
will attribute poorly no matter how the regression is regularised. Elastic net manages
the instability; it does not manufacture identifiability. Separating those dials
requires generating clips that hold all but one fixed — stage 03 — and that is a
different kind of evidence.

**One era, one medium, three directors.** Technicolor features from 1937–1951 share
conventions of lighting, staging and lens that contemporary cinema does not.
Generalisation beyond that is untested.

**No text branch.** All results are video + audio only; the gated text model was
skipped throughout. For a corpus containing dense dialogue — *Nothing Sacred* in
particular — this omits a modality TRIBE was designed to use.

**Most survivors do not reach the smallest effect worth calling a finding.** 101 of
180 parcels survive the permutation null, but only 9 exceed the derived SESOI of 0.5,
and the median survivor implies *r* ≈ 0.07 against real cortex. The count of surviving
parcels is the weaker of the two numbers and should not be quoted without the second.

**The null may still be lenient in a way we have not tested.** A declared exploratory
check with permutation restricted within film returned 99 of 180 against the registered
101, with a marginally narrower null, so film-blocking structure is not inflating the
result. Temporal adjacency between neighbouring segments within a film is a separate
dependence that neither permutation preserves, and it remains untested. Treat 101 as an
upper bound.

**The hyperparameters of the model were not pre-registered.** The registration
specified "a cross-validated elastic net" without fixing α, l1_ratio or fold count.
Those were set before the run to the values already present in the pre-registered
futility script, and are disclosed in §6.6, but they were a residual degree of freedom
that a tighter registration would have closed.

**The cut-rate disagreement is resolved only as far as stage 03 reaches.** Stage 03 shows
that the auditory signature is a property of cutting on this sensor — it appears with no
speech present and a continuous ambient track — and that the frontal effect is causal on
intercut generated footage. It does not show why real cinema lacks the frontal effect; the
scene-switch hypothesis of §6.8 was tested with a histogram proxy and not supported, and
the proxy separates within- from between-scene cuts only partially on live action, so the
hypothesis is weakened rather than excluded and the frontal miss stays unexplained. Stage 03
is also *n* = 5 levels per arm, one generated scene pair, one generator,
with a face base short of its shot-scale target (0.052 against 0.10), and its verdict is
PARTIAL-A by a margin of 0.001 on one parcel — a near-miss reported as a miss.

**The ladder designs have a *p*-floor.** Five levels allow 120 orderings, of which the true
one and its mirror are indistinguishable, so no count can do better than *p* = 0.017. Stage
01 reaches that floor and stage 03 sits one ordering above it. The designs cannot separate a
strong effect from a very strong one, and the pre-fixed bar of 15 parcels is cleared by 8–17%
of random orderings. Seven levels, or two scene pairs, would have cost little more.

**Cut rate is not a frontal lever in the observational index.** The index has no cut-rate
weight on inferior-frontal cortex to steer with, and the exploratory refits show none is
hiding under the penalty. Any control law that reaches frontal cortex through cutting rests
on stage 03's regime — scene-alternating intercut material — and nothing else yet.

**The sensor's response space is low-dimensional, which bounds every downstream claim.**
Across 70 segments of real cinema the 180-parcel response varies along two to three
dimensions, and an index fitted to label-shuffled responses is as concentrated as the real
one (§6.7). Whatever the programme eventually demonstrates about control, it is control over
a roughly three-dimensional subspace of response profiles. Whether that is a fact about
cortex, about TRIBE's encoding head, or about clip-mean readouts that average away
everything faster than a minute, this design cannot say. The technique-specific content of
the map is narrower than the first draft claimed: which dial leads the dominant axis, and a
five-point gain in retained variance over a fit to noise.

**Cut rate is the weakest dial in the design**, at *s* ≈ 0.66, precisely because it
carries the most between-film signal. It is also the dial the replication check
depends on. The sample size was raised to keep that check informative, but it remains
the thinnest margin in the study.

---

## 9 · Status and next steps

| stage | status |
|---|---|
| 00 · Probe | ✅ Complete — PASS |
| 01 · Gate | ✅ Complete — PASS |
| **02 · Index** | ✅ **Complete — PARTIAL.** Registered at `osf.io/dg7fe`; criterion 1 met, criterion 2 not met |
| 01b · Synthetic-imagery transfer | ✅ **PASS** — generated H3 Max clips reproduce the face/place axis at *r* = +0.699 (bar 0.50, live-action reference +0.936); cutting confounded with content |
| 02b · Generalisation test | ✅ **Run, exploratory, n = 3** — the fitted index predicts generated clips at profile *r* 0.41 / 0.90 / 0.89; contrast *r* +0.77 |
| 03 · Isolation | ✅ **PARTIAL-A** — cutting drives IFJ up and auditory cortex down in both speech arms on generated footage (58 and 54 of 180 parcels at \|*r*\|>0.9); H3b misses the 0.9 bar by ≤ 0.03 at *n* = 5 |
| 04 · Inversion | Not started |

**Stage 02's PARTIAL verdict set the agenda; stage 03 has now answered the first item on
it.** Five things follow.

First, **cut rate has been isolated, and it is causal** (§6.8). Held content, lighting,
motion and shot scale fixed by construction and varied cutting alone over a 31× range, the
inferior-frontal response returned in both speech arms, and the auditory signature stage 02
found appeared alongside it. Neither earlier track was wrong; each saw half of one effect.
What stage 03 did not do is explain why real cinema carries only the auditory half, and the
exploratory follow-up locates that in the corpus rather than in the regression. A
between-scene cut count over the 244 segments does not support the one hypothesis that
follow-up left standing: frontal cortex shows no association with scene switches at any
threshold and its sign flips between films, while auditory cortex follows cuts of every
kind. The frontal miss is a property of this corpus and remains unexplained. Stage 04
should treat cut rate as a frontal lever only on intercut material.

Second, **the text branch remains open, and is parked.** Stage 03's no-speech arm removes
the specific worry that the auditory cut-rate signature was an artefact of the missing text
modality. A text-on replication of stage 03 has not been chosen; a text-branch rescoring
attempt on 13 September failed (0 / 12 after 189 minutes) and is not being diagnosed
unless that replication is chosen. Meta's gated Llama-3.2-3B access was granted on 13
September, so the path is open when wanted.

Third, **face area is the strongest lever the index found**, and it is the dial that
carries the programme's inversion thesis. Any control law built from this index would
reach faces first. That is a measured association, not a causal claim, and it inherits
every limitation in §8 — but it is the association most worth isolating next.

**Fourth, and changing what stage 04 should attempt: the reachable set is about three
dimensional (§6.7).** Inversion cannot mean specifying an arbitrary cortical profile.
The tractable version — and the one stage 04 should be respecified to test — is: take a
target that lies *within* the reachable subspace, derive a dial setting, generate,
measure the achieved profile, and ask whether it lands where the index said it would.
That is a falsifiable control-law test at a scale the effect sizes in §6.4 can support.
Specifying targets outside the subspace would fail for geometric reasons that have
nothing to do with whether the index is right. Stage 03 adds a constraint: if cut rate
is among the dials the controller moves, the frontal target is reachable only on
intercut, scene-alternating material, because that is the only regime where the effect
has been shown.

Fifth, **the 01b transfer gate passed on the axis that matters** — generated H3 Max clips
reproduce the face/place axis at *r* = +0.699 against a bar of 0.50 (live-action reference
+0.936), which is what §6.7 said the gate had to establish. Its one confound, that the
generator cut within its own outputs at 7–15 per minute, is what stage 03 removed by
demanding single-take bases and measuring them (0 cuts). The exploratory 02b check
(*n* = 3) found the fitted index predicts generated clips at profile *r* 0.41 / 0.90 / 0.89.
Stage 04 rests on those two results and on the scope they carry: one generator, and no
claim about live action.

---

## Sources

- TRIBE: *TRImodal Brain Encoder for whole-brain fMRI response prediction*, arXiv:2507.22229
- *Insights from the Algonauts 2025 Winners*, arXiv:2508.10784
- Kauttonen, J. et al. (2015). Optimizing methods for linking cinematic features to fMRI data. *NeuroImage* 110:136–148. PMID 25662868
- Aliko, S. et al. (2020). A naturalistic neuroimaging database for understanding the brain using ecological stimuli. *Scientific Data* 7:347
- Gruber, M. et al. (2024). Between-movie variability severely limits generalizability of "naturalistic" neuroimaging. bioRxiv 2024.12.03.626542
- Geerligs, L. et al. (2022). A partially nested cortical hierarchy of neural states underlies event segmentation in the human brain. *eLife* 11:e77430
- Baldassano, C. et al. (2017). Discovering event structure in continuous narrative perception and memory
- Lakens, D. *Sample Size Justification* / *Improving Your Statistical Inferences*, ch. 8
- Internet Archive metadata API, per-identifier, read 3 September 2026
- Hugging Face Spaces hardware pricing (A10G Small, $1.00/hr)

## Internal documents

`experiments/ROADMAP.md` · `experiments/LOG.md` · `experiments/OBJECTIVES.md` ·
`experiments/00-probe/{README,RESULT,CLIPS}.md` ·
`experiments/01-cutrate/{README,RESULT}.md` ·
`experiments/02-index/{README,CORPUS,DIALS,RESULT,frontal_miss,scene_switches}.md` ·
`experiments/01b-transfer/{README,RESULT,CLIPS}.md` ·
`experiments/02b-generalisation/RESULT.md` ·
`experiments/03-isolation/{README,RESULT,CLIPS}.md`
