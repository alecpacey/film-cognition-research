# Technique, affect, and what is actually established

Scope: film/video datasets annotated with *induced* or *perceived* audience affect, and the empirical
record connecting cinematographic technique to measured viewer response.

Three distinctions govern everything below. Conflating them is the single most common way this
literature gets over-read:

1. **Expected vs. induced emotion.** *Expected* emotion is the normative response a general audience
   is assumed to have — effectively an objective property of the content. *Induced* (experienced,
   felt) emotion is what an individual viewer actually feels. Almost every benchmark that claims to
   predict "emotional impact" is scored against **expected** emotion, because induced emotion does
   not have enough inter-rater agreement to be a usable target. MediaEval's own task definition says
   this outright.
2. **Perceived/attributed vs. felt.** Many of the strongest technique effects in the literature are
   effects on *what emotion the viewer attributes to a character*, not on what the viewer feels. The
   Kuleshov paradigm is entirely of this kind. AFEW/SFEW annotate the *actor's* expression. These
   are not audience affect.
3. **Lab vs. naturalistic.** Effects measured on 8-second clips, with a joystick in hand, in a
   scanner, do not transfer automatically to someone watching on a phone.

**The ceiling result.** COGNIMUSE measured inter-annotator agreement for *experienced* emotion on
continuous movie viewing: Pearson r = 0.293 (valence) / 0.409 (arousal); Krippendorff's α = 0.308 /
0.152; **Cohen's κ = 0.035 (valence) / 0.029 (arousal)**. On the discrete level, seven trained
annotators watching the same films agreed at essentially chance. The authors' own summary is "as
expected, the inter-annotator agreement is low." By contrast, *intended* and *expected* emotion
correlated at r = 0.74 (arousal) / 0.70 (valence).

This is the most important number in this document. It caps every downstream model. Any system
predicting *felt* emotion from film content is fitting a target that humans themselves do not agree
on; reported performance above that ceiling is a sign the target has quietly been swapped for
expected emotion or for something else entirely.

---

## What is reliably established

Ordered by strength of evidence. I have been strict: "reliably established" here means replicated,
with an effect size, on a mechanism that is at least plausibly causal.

### 1. Montage context determines perceived emotional meaning — very large effect

The strongest quantified technique→affect result in the recent literature. Cao et al. (2024,
*Humanities and Social Sciences Communications* 11:1349) crossed film colour (colour / black-and-white)
with editing context (fearful / neutral / happy cut-arounds) on authentic film material, in two
experiments:

| Experiment | N | Effect | Statistic |
|---|---|---|---|
| 1 (behavioural) | 117 | Editing → valence | F(1.6, 182.2) = 288.73, p < .001, **η²p = 0.715** |
| 2 (behavioural + fMRI) | 67 | Editing → valence | F(1.4, 91.2) = 168.00, p < .001, **η²p = 0.721** |
| 2 | 67 | Editing → arousal | F(1.7, 107.5) = 29.90, p < .001, η²p = 0.315 |

η²p ≈ 0.72 replicated across two independent samples is about as solid as this field gets. The fMRI
arm found distinct activation patterns (insula, ACC, IPG) per condition, consistent with the
behavioural data.

**The honest caveat:** this is *perceived* emotion of a neutral face, i.e. a Kuleshov-family
paradigm. It establishes that what you cut *to* dominates how the adjacent shot is emotionally read.
It does *not* establish that it induces a corresponding felt state in the audience.

### 2. Cuts and edits reliably elicit an orienting response — physiological, replicated over decades

Lang's programme (from *Communication Research* 17(3), 1990 onward) established that structural
features — cuts, edits, scene changes — evoke an automatic orienting response: transient cardiac
deceleration over roughly 8–10 beats (~4–6 s) plus a skin-conductance rise. This is one of the most
replicated findings in media psychology, measured physiologically rather than by self-report, and it
is mechanistically clear.

Two constraints that are usually dropped when this gets cited:

- It is an **attention/orienting** effect, not a valence effect. A cut makes you look; it does not
  make you feel good or bad.
- It **habituates**, and the dose–response is an **inverted U**. Lang's own follow-up work ("When an
  edit is an edit, can an edit be too much?") found that increasing edit rate improves recognition
  memory up to a point, then degrades it — and that the turning point depends on how difficult the
  content already is. More cuts is not monotonically more engagement.

### 3. Sound carries more affective signal than image

Within LIRIS-ACCEDE / MediaEval 2018, a clean modality ablation (Ou et al., arXiv:1909.01763):

| Modality | Valence MSE / PCC | Arousal MSE / PCC |
|---|---|---|
| **Audio** | 0.098 / **0.264** | 0.140 / 0.172 |
| Scene | 0.103 / 0.192 | 0.152 / 0.140 |
| Facial expression | 0.110 / 0.150 | 0.162 / 0.061 |
| Action | 0.132 / 0.057 | 0.156 / **0.158** |

Audio is the best single modality for valence by a wide margin and competitive for arousal. This is
correlational and within one dataset, but it is consistent with the design choices of the affect
literature: EMDB deliberately *strips* audio precisely because sound otherwise dominates the
elicitation.

### 4. Directed film synchronises viewers' brains; unstructured footage does not

Hasson et al. (2008), "Neurocinematics." Inter-subject correlation of fMRI response, by stimulus:
Hitchcock ~65% of cortex, Leone ~45%, Larry David ~18%, unedited Washington Square Park footage
<5%. The gradient tracks directorial control and has held up well.

**What this does and does not show:** it shows that tight construction produces *consistent* neural
response across viewers. It says nothing about valence, and — directly relevant to this project —
consistency of response is not the same as retention. The published null the project already has
(brain-model engagement curves failing to predict retention) sits comfortably alongside this result
rather than contradicting it; ISC-family measures index *shared processing*, not *willingness to
keep watching*.

### 5. Film clips are effective, reproducible emotion elicitors with stable normative structure

Two well-validated normative sets:

- **FilmStim** (Schaefer et al., *Cognition & Emotion*, 2010): 70 excerpts across 6 emotion
  categories + neutral, selected by 50 film experts, rated by **N = 364**. 24 classification
  criteria published.
- **EMDB** (Carvalho et al., *Applied Psychophysiology and Biofeedback*, 2012): 52 clips, no audio,
  self-report from N = 113 plus psychophysiology. Found the expected dissociation — **skin
  conductance level increase with heart-rate deceleration** in high-arousal (horror, erotic)
  conditions.

The clip→category mapping replicates across labs. This is the solid ground: *content* reliably moves
affect. It is technique-agnostic.

---

## What is claimed but weak

### Close-ups increase emotional engagement — a clean, well-powered null

The most-cited piece of film-school folk wisdom does not survive testing. Bálint et al. (2020),
"Shot scale matters," *Poetics* 82:101480 — **N = 495**, an animated film cut into six versions
varying only close-up frequency (1, 3, 4, 5, 10 CUs):

- Effect of close-up frequency on **affective processing**: Wald χ²(5) = 10.168, **p = .071 —
  not significant.** The authors state this "rejects our hypothesis."
- Effect on **cognitive processing**: Wald χ²(5) = 0.34, **p = .99.**
- Effect on **prompted** mental state attribution: Wald χ²(5) = 6.58, p = .254.
- The *only* significant result was **spontaneous** mental state attribution, χ²(5) = 14.09, p = .015
  — and it was **non-monotonic**: the 3-close-up condition departed from the mean, differing from 1,
  4, 5 *and* 10. A non-monotonic pattern with no dose–response is the signature of noise, not a lever.

Note the title oversells the result; the body of the paper is largely null.

### Colour drives valence — null main effect

From the same Cao et al. (2024) study that produced the large editing effect:

- Main effect of colour on valence: **F(1, 115) = 0.117, p = .733, η²p = 0.001.** A clean null.
- Colour × editing interaction: η²p = 0.048 in Experiment 1 (p = .007) — small — and it **failed to
  replicate** in Experiment 2 (p = .129).

Within a single study, editing gave η²p ≈ 0.72 and colour gave η²p ≈ 0.001. Colour grading may do
other work (period signalling, legibility, style), but as a valence lever the evidence is weak.

### Neural/biometric measures predict box office

Christoforou et al. (2017), *Frontiers in Neuroinformatics* 11:72, headlines "up to 72% of the
variance" of premiere-weekend box office from EEG and eye-gaze. Read the degrees of freedom:
**F(1, 12)** — the regression has roughly **14 films**. The paper fits **seven** models and reports
the best; the top model uses two predictors on ~14 points. That is textbook overfitting, and the
bootstrap SEs on R² (0.07–0.25) are large.

The same paper's own literature review is more informative than its result: it notes that Boksem &
Smidts (2015), testing EEG prediction of box office, found **explained variance < 2%** despite
statistical significance. And in Christoforou et al.'s own data, the *behavioural* self-report
predictors were flatly non-significant (liking R² = 0.02, p > .54; willingness-to-watch R² = 0.11,
p > .20).

Combined with the project's existing null on retention, the fair summary is: **no
neural or biometric measure has a credible, replicated record of predicting audience-level commercial
or retention outcomes.**

### The Kuleshov effect as a large, general phenomenon

Frequently invoked as settled; it is not. The original footage is lost. Barratt et al. (2016),
*Perception* 45(8):847–874 (N = 36) found *some* effect — participants chose the context-congruent
category above chance, with valence and arousal moving in the expected direction — so the 2016 study
is a qualified positive, not the null it is sometimes cited as. Subsequent work (Cao et al. 2024;
"Reexamining the Kuleshov effect," *PLOS ONE* 2024, doi:10.1371/journal.pone.0308295) finds the
effect is real but **depends heavily on using authentic film material rather than static images**,
and interacts with editing style. Treat it as a genuine but paradigm-sensitive effect about
*attributed* emotion, not a general-purpose affect lever.

### "Arousal is easier to predict than valence"

Commonly asserted; the data are mixed and dataset-dependent.

- COGNIMUSE inter-annotator: arousal higher on Pearson (0.409 vs 0.293) but **lower** on
  Krippendorff's α (0.152 vs 0.308).
- MediaEval 2018 leaderboard: most teams scored *higher* on valence than arousal; the best arousal
  score came from a team mid-table on valence.

There is no stable ordering. Do not design around one.

### That induced emotion is predictable at any useful level

The MediaEval 2018 official leaderboard, on 12 held-out movies, predicting **expected** (not felt)
valence/arousal per second:

| Team | Valence MSE / PCC | Arousal MSE / PCC |
|---|---|---|
| CERTH-ITI | 0.117 / 0.098 | 0.138 / 0.054 |
| THUHCSI | 0.092 / 0.305 | 0.140 / 0.087 |
| Quan et al. | 0.115 / 0.146 | 0.171 / 0.091 |
| Yi, Wang & Li | 0.090 / 0.301 | 0.136 / 0.175 |
| GLA | 0.084 / 0.278 | 0.133 / **0.351** |
| Ko et al. | 0.102 / 0.114 | 0.149 / 0.083 |
| *Ou et al. (post-hoc, 2019)* | *0.071 / 0.444* | *0.137 / 0.419* |

**Best in-task PCC ≈ 0.31 (valence), 0.35 (arousal); median around 0.15.** The MediaEval 2015
discrete task was worse: 3-class valence accuracy 0.33–0.43, arousal 0.45–0.56, against an
imbalanced 3-class baseline.

Post-hoc numbers published after the test labels were available (the italicised row) should be
discounted; they were not produced under held-out conditions.

---

## Dataset table

| Dataset | Stimuli | Affect annotation | Technique annotation? | Licence | Access |
|---|---|---|---|---|---|
| **LIRIS-ACCEDE (discrete)** | 9,800 excerpts, 8–12 s, from 160 CC-licensed movies (~73 h) | Induced valence + arousal **rankings**, pairwise crowdsourced (CrowdFlower) | **No** | Videos CC BY / BY-SA / BY-NC | Signed EULA to accede@liris.cnrs.fr, institutional email only. **Not on HF** |
| **LIRIS-ACCEDE (continuous)** | 30 full movies | Continuous V/A self-report at 1 Hz **+ raw and processed GSR**; annotated by **only 10 paid French participants, aged 18–27** | **No** | CC (per source film) | Same EULA |
| **MediaEval EIMT 2018** | 54 dev movies (26.8 h) + 12 test (8.9 h), drawn from the 160 | Per-second **expected** V/A (GTrace + joystick, 28 French annotators, 3–5 per movie); **fear** intervals — *1 annotator per movie*, 2 NICAM staff total | **No** (ships openSMILE audio + LIRE/VGG16 visual features, not technique labels) | CC | Same EULA |
| **MediaEval 2015 (Affective Impact)** | 10,900 excerpts from 199 movies | Discrete valence class, arousal class, binary violence | **No** | CC | Same EULA |
| **COGNIMUSE** | 7 Hollywood half-hour segments (3.5 h) + 5 documentaries + *Gone with the Wind* (104 min) | Continuous V/A ∈ [−1,1] via FEELTRACE, **intended** (1 expert × 3 passes), **experienced** (7 volunteers), **expected** (derived). Agreement reported and low | **Partial — manual shot & scene segmentation** (cuts/fades; mean shot 3.5 s), plus sensory/semantic saliency | Paper CC BY 4.0; **video is DVD-ripped Hollywood — not redistributable** | cognimuse.cs.ntua.gr/database (TLS cert currently misconfigured) |
| **EMDB** | 52 clips, ~40 s, **no audio** | Normative valence/arousal/dominance (N = 113) **+ SCL and HR** | No | Academic, on request | Request from authors |
| **FilmStim** | 70 excerpts, 1–7 min | 24 criteria: discrete emotion, arousal, PANAS, DES (N = 364) | No | Academic, on request | Request from authors |
| **DEAP** | 40 × 1-min **music videos** (not film) | Self-report V/A/dominance/liking + **32-ch EEG** + peripheral physio; face video for 22/32 | No | EULA, academic | Official EULA. Unofficial HF/Kaggle re-uploads exist — **licence-unsafe, do not use** |
| **MAHNOB-HCI** | 20 clips, 35–117 s, from commercial films | Self-report V/A/dominance/predictability + emotion keyword; **EEG, peripheral physio, eye gaze, face video** (N = 27) | No | EULA, academic | mahnob-db.eu |
| **DECAF** | 36 movie clips + the 40 DEAP music videos | Explicit + implicit responses, **MEG**, NIR face, hEOG, ECG, EMG (N = 30) | No | EULA, academic | Request |
| **AFEW / SFEW** | Clips/frames from movies | **The actor's *expressed* emotion.** Not audience affect | No | EULA (EmotiW) | Challenge registration |
| **EMOTIC** | **Still images**, not film | 26 discrete categories + VAD, for people *in the image* | No | Research use | Unofficial HF mirror `chitradrishti/Emotic` |
| **CEAP-360VR** | 8 affective 360° VR clips | Continuous V/A + head/eye/pupil + physio (N = 32) | No | Research | GitHub |
| **studyforrest** | *Forrest Gump* (one film) | **Portrayed** emotions — 12 observers, episodes with arousal/valence + category + perceptual evidence | **Yes — 870 shots**, each with start time, location (3 abstraction levels), setting, locale, interior/exterior, temporal-progression class, time of day. Single annotator, multi-pass | **CC0** | studyforrest.org, F1000Research, OpenNeuro |
| **NNDb** (Aliko et al. 2020) | 10 full-length films, 10 genres, 86 participants, fMRI | **None.** Only automated word/face annotations | No | Open | OpenNeuro `ds002837` |
| **MovieNet** | 1,100 movies | **None** | **Yes — 92K cinematic style tags**, 42K scene boundaries, 1.1M character boxes | Research only, no video redistribution | Request form |
| **AVE** (Adobe/KAIST) | 196,176 shots from 5,591 movie scenes | **None** | **Yes — 8 attributes** (shot size, angle, type, motion, …), >1.5M labels | Annotations on GitHub; **video scraped from MovieClips YouTube** | github.com/dawitmureja/AVE |
| **CineScale** | 792,000 frames @1 fps, 124 full films, 6 directors | **None** | **Yes — 9-category shot scale**, 2 independent coders + adjudicator; ships a trained CNN | **CC BY-NC-ND** (Data in Brief) | Project site |
| **CineTechBench** | 600+ expert-annotated movie images/clips | **None** | **Yes — 7 dimensions** (shot scale, angle, composition, camera movement, lighting, colour, focal length) | Research | arXiv:2505.15145 |

---

## The pairing problem

**There is no dataset that annotates both cinematographic technique and audience affect on the same
material at any useful scale.** This is not a gap in my search; it is a structural feature of how the
two literatures grew. The affect datasets are built by psychologists and multimedia-retrieval groups
who treat the film as an opaque stimulus; the technique datasets are built by vision groups for
editing and style-recognition tasks and have no reason to collect viewer response. Neither cites the
other's annotation as something worth adding.

The three nearest misses, and why each falls short:

- **COGNIMUSE** is the only dataset that genuinely has both. It has continuous intended/experienced
  V/A *and* manual shot and scene segmentation. But the technique layer is only **cut boundaries** —
  it gives you shot length and editing pace, nothing about scale, angle, movement, or lighting — and
  the corpus is **3.5 hours across 7 films** with 7 emotion annotators. Underpowered, and the video
  cannot be redistributed.
- **studyforrest** has 870 richly attributed shots, portrayed-emotion episodes, fMRI, eye-tracking,
  and a **CC0** licence. But it is **one film**, the emotion layer is *portrayed* (what the
  characters feel) rather than induced, and the shot annotation is location/time-oriented rather than
  cinematographic — no shot scale or camera movement.
- **Canini, Benini & Leonardi (2012)**, "Affective Recommendation of Movies Based on Selected
  Connotative Features" (*IEEE TCSVT*) is the closest thing to a deliberate attempt at the pairing:
  it extracts shooting and editing descriptors, has users rate *connotative* properties, and predicts
  affective response through that intermediate layer. The idea is right and directly relevant. But no
  reusable dataset was released, and the evaluation is a user-satisfaction study rather than a held-out
  benchmark.

Notably, the CineScale authors explicitly name "the unfolding of the relationship between shot scale
and the viewers' emotional experience" as a motivation for their dataset — and then do not collect
any affect labels. The gap is recognised and unfilled.

### Cheapest way to construct one

The construction is genuinely cheap, because one side already exists in redistributable form.

**Base material: Continuous LIRIS-ACCEDE / MediaEval 2018.** 54 movies, ~27 hours, per-second
valence and arousal already annotated, GSR available for the 30-movie continuous subset, and — the
decisive property — **the films are Creative Commons**, so you may redistribute the derived
annotations alongside pointers to freely obtainable video. No other affect corpus has this. You need
the EULA and an institutional email address.

Then add the technique layer to exactly that material:

1. **Automated pass (GPU-hours, no annotation labour).** PySceneDetect for cut boundaries → shot
   length, ASL, cutting-rate time series. The **CineScale** released CNN for shot scale (note its
   CC BY-NC-ND licence: fine for internal research, restricts redistribution of derivatives). Optical
   flow or a camera-motion estimator for movement magnitude and type. This alone yields
   pace + scale + motion aligned to the existing 1 Hz affect signal, across all 54 films.
2. **VLM pass, validated (cheap at scale, measurable error).** Prompt or fine-tune a VLM on the
   **AVE** 8-attribute taxonomy, calibrate it against AVE and CineScale held-out splits so you have a
   published per-attribute error rate, then run it over the 54 films. Using an existing taxonomy is
   what makes the result comparable to other work rather than bespoke.
3. **Human calibration subsample (low thousands of dollars).** Hand-annotate ~3,000–5,000 shots,
   stratified to cover the valence–arousal plane rather than sampled uniformly (the corpus is
   heavily neutral). Two independent coders plus an adjudicator — the protocol both AVE and CineScale
   used. This exists to *measure* the error in steps 1–2, not to replace them.

Do 1 and 2 for coverage; do 3 to know what your labels are worth. Budget the whole thing in
GPU-hours plus a few thousand dollars of annotation.

**Set expectations before building it.** Three constraints are properties of the labels, not of any
model you fit:

- The affect target is **expected**, not felt, emotion. On induced emotion, humans agree at
  κ ≈ 0.03.
- The continuous LIRIS-ACCEDE annotations come from **10 French participants aged 18–27**. Whatever
  you learn is that cohort's expected response.
- Given the MediaEval ceiling, a well-built model on this pairing should be expected to land around
  **PCC 0.2–0.35**. If it scores much higher, suspect leakage or a swapped target.

**For the project's actual purpose — steering a generator — the defensible read of the evidence is
narrow:** the levers with real measured support are **montage context** (what you cut to, η²p ≈ 0.72
on perceived valence), **cut rate** (orienting response, inverted-U dose–response), and **sound**
(the strongest single modality for affect prediction). Shot scale and colour, the two levers most
often assumed, have well-powered nulls against them. And no measured-affect signal — self-report,
physiological, or neural — currently has a credible record of predicting retention, which is
consistent with the null result the project already holds.

---

## Sources

**Datasets**

1. [LIRIS-ACCEDE — InterDigital dataset page](https://www.interdigital.com/data_sets/liris-accede) — all collections, EULA access terms.
2. Baveye, Dellandréa, Chamaret & Chen (2015), "LIRIS-ACCEDE: A Video Database for Affective Content Analysis," *IEEE Trans. Affective Computing* 6(1):43–55. [DOI](https://doi.org/10.1109/TAFFC.2015.2396531) · [PDF](https://liris.cnrs.fr/Documents/Liris-7059.pdf)
3. Dellandréa, Huigsloot, Chen, Baveye, Xiao & Sjöberg (2018), "The MediaEval 2018 Emotional Impact of Movies Task." [CEUR-WS PDF](https://ceur-ws.org/Vol-2283/MediaEval_18_paper_4.pdf) — dataset composition, annotation protocol, metrics.
4. Zlatintsi et al. (2017), "COGNIMUSE: a multimodal video database annotated with saliency, events, semantics and emotion," *EURASIP J. Image and Video Processing* 2017:54. [Open access](https://doi.org/10.1186/s13640-017-0194-1) — **Table 11 carries the inter-annotator agreement figures.**
5. Häusler & Hanke (2016), "An annotation of cuts, depicted locations, and temporal progression in the motion picture 'Forrest Gump'," *F1000Research*. [PMC5034791](https://pmc.ncbi.nlm.nih.gov/articles/PMC5034791/) — 870 shots, CC0.
6. Labs et al. (2015), "Portrayed emotions in the movie 'Forrest Gump'," *F1000Research*. [PMC4416536](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4416536/)
7. Aliko et al. (2020), "A naturalistic neuroimaging database for understanding the brain using ecological stimuli," *Scientific Data* 7:347. [DOI](https://doi.org/10.1038/s41597-020-00680-2) · OpenNeuro `ds002837`. No affect annotations.
8. Carvalho et al. (2012), "The Emotional Movie Database (EMDB)," *Applied Psychophysiology and Biofeedback*. [DOI](https://doi.org/10.1007/s10484-012-9201-6) · [PubMed](https://pubmed.ncbi.nlm.nih.gov/22767079/)
9. Schaefer et al. (2010), "Assessing the effectiveness of a large database of emotion-eliciting films," *Cognition & Emotion*. [DOI](https://doi.org/10.1080/02699930903274322)
10. Koelstra et al. (2011), "DEAP: A Database for Emotion Analysis Using Physiological Signals," *IEEE Trans. Affective Computing*. [DOI](https://doi.org/10.1109/T-AFFC.2011.15)
11. Soleymani et al. (2011), "A Multimodal Database for Affect Recognition and Implicit Tagging" (MAHNOB-HCI). [DOI](https://doi.org/10.1109/T-AFFC.2011.25)
12. Abadi et al. (2015), "DECAF: MEG-Based Multimodal Database for Decoding Affective Physiological Responses." [DOI](https://doi.org/10.1109/TAFFC.2015.2392932)
13. Kosti et al. (2019), "Context Based Emotion Recognition using EMOTIC Dataset," *IEEE TPAMI*. [DOI](https://doi.org/10.1109/TPAMI.2019.2916866)
14. Xue et al. (2021), "CEAP-360VR: A Continuous Physiological and Behavioral Emotion Annotation Dataset for 360° VR Videos." [DOI](https://doi.org/10.1109/TMM.2021.3124080)

**Technique-annotation datasets (no affect labels)**

15. Argaw, Caba Heilbron, Lee, Woodson & Kweon (2022), "The Anatomy of Video Editing: A Dataset and Benchmark Suite for AI-Assisted Video Editing," [arXiv:2207.09812](https://arxiv.org/abs/2207.09812) · [GitHub](https://github.com/dawitmureja/AVE)
16. Huang et al. (2020), "MovieNet: A Holistic Dataset for Movie Understanding," [arXiv:2007.10937](https://arxiv.org/abs/2007.10937)
17. Benini et al. (2021), "CineScale: A dataset of cinematic shot scale in movies," *Data in Brief*. [DOI](https://doi.org/10.1016/j.dib.2021.107002) — CC BY-NC-ND.
18. "CineTechBench: A Benchmark for Cinematographic Technique Understanding and Generation" (2025), [arXiv:2505.15145](https://arxiv.org/abs/2505.15145)
19. Svanera et al. (2018), "Who is the director of this movie? Automatic style recognition based on shot features," [arXiv:1807.09560](https://arxiv.org/abs/1807.09560)

**Established effects**

20. Cao, Wang, Li, Xiao, Xie, Bi, Wu, Zhu & Wang (2024), "Exploring the combined impact of color and editing on emotional perception in authentic films," *Humanities and Social Sciences Communications* 11:1349. [Open access](https://doi.org/10.1057/s41599-024-03874-w) — **the η²p = 0.715/0.721 editing effect and the colour null.**
21. Lang (1990), "Involuntary Attention and Physiological Arousal Evoked by Structural Features and Emotional Content in TV Commercials," *Communication Research* 17(3). [DOI](https://doi.org/10.1177/009365090017003001)
22. Lang et al., "The Effects of Edits on Arousal, Attention, and Memory for Television Messages: When an Edit Is an Edit Can an Edit Be Too Much?" — the inverted-U result.
23. Hasson et al. (2008), "Neurocinematics: The Neuroscience of Film," *Projections* 2(1). [PDF](https://www.motionpictures.org/wp-content/uploads/2013/01/Hasson-etal_NeuroCinematics2008.pdf) — the 65% / 45% / 18% / <5% ISC gradient.
24. Ou et al. (2019), "Video Affective Effects Prediction with Multi-modal Fusion and Shot-Long Temporal Context," [arXiv:1909.01763](https://arxiv.org/abs/1909.01763) — **the modality ablation and the MediaEval 2018 leaderboard table.**
25. Nummenmaa & Lahnakoski (2021), "Naturalistic Stimuli in Affective Neuroimaging: A Review," *Front. Hum. Neurosci.* 15:675068. [Open access](https://doi.org/10.3389/fnhum.2021.675068)

**Failures and weak claims**

26. Bálint, Blessing & Rooney (2020), "Shot scale matters: The effect of close-up frequency on mental state attribution in film viewers," *Poetics* 82:101480. [DOI](https://doi.org/10.1016/j.poetic.2020.101480) · [OA PDF](https://opus.bibliothek.uni-augsburg.de/opus4/files/83435/1-s2.0-S0304422X20302175-main.pdf) — **the N = 495 affective-processing null.**
27. Christoforou, Papadopoulos, Constantinidou & Theodorou (2017), "Your Brain on the Movies," *Front. Neuroinformatics* 11:72. [Open access](https://doi.org/10.3389/fninf.2017.00072) — the R² = 0.72 claim, and its F(1,12).
28. Boksem & Smidts (2015), EEG prediction of movie preference and box office — explained variance < 2%, as reported in [27].
29. Barratt, Cabak Rédei, Innes-Ker & van de Weijer (2016), "Does the Kuleshov Effect Really Exist?", *Perception* 45(8):847–874. [DOI](https://doi.org/10.1177/0301006616638595)
30. "Reexamining the Kuleshov effect: Behavioral and neural evidence from authentic film experiments" (2024), *PLOS ONE*. [DOI](https://doi.org/10.1371/journal.pone.0308295)

**The near-miss pairing**

31. Canini, Benini & Leonardi (2012), "Affective Recommendation of Movies Based on Selected Connotative Features," *IEEE Trans. Circuits and Systems for Video Technology* 23(4):636–647. [DOI](https://doi.org/10.1109/TCSVT.2012.2211935)

---

### Verification notes

Figures in the tables above were read directly from the source PDFs (MediaEval 2018 overview,
COGNIMUSE Table 11, Cao et al. results section, Bálint et al. results section, Ou et al. Tables 1
and 5, Christoforou et al. Table 2), not from search snippets or abstracts.

Two things I could not verify and have not asserted: exact effect sizes from Tarvainen et al.'s film-mood
work (*The way films feel*, 2015, and *IEEE TAFFC* 11(2):313–326, 2020 — both paywalled, no OA copy
found), and the precise wording of Lang's inverted-U edit-rate thresholds (secondary sources only).
Neither changes any conclusion here. The session's web-search quota was exhausted partway through, so
the later half of this research ran on direct PDF retrieval, the arXiv API, and OpenAlex rather than
on search.
