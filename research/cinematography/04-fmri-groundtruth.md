# fMRI film datasets as ground truth

Researched 2026-09-01. Primary sources: arXiv:2605.04326v1 full text (HTML, fetched and parsed
directly), the `facebookresearch/tribev2` repo tree via the GitHub API, OpenNeuro's GraphQL API,
CNeuroMod's own docs, and OpenAlex/Semantic Scholar for the literature.

**Headline:** the technique → brain-region literature is much further along than assumed. A
2026 review (Cao et al., *Behavioral Sciences*) already synthesises it into an explicit
"Film Cognition Matrix". Several specific mappings are established with named regions. And
StudyForrest — which TRIBE never touched — already ships 870 human-coded shot boundaries
alongside its fMRI. The validation study the lead is contemplating is substantially cheaper
than expected, but it is also **not** a TRIBE study: the cinema-annotatable ground truth sits
mostly outside TRIBE's training set.

---

## What TRIBE actually saw

Verified against Table 1 and §5.7 of arXiv:2605.04326v1 ("A foundation model of vision,
audition, and language for in-silico neuroscience", d'Ascoli, Rapin, Benchetrit, Brooks,
Begany, Raugel, Banville, King — FAIR at Meta; v1 dated 5 May 2026, paper date 24 Aug 2026).

### Corrections to the brief's premises

1. **"Courtois NeuroMod (Friends, movie10), Algonauts 2025" are not two datasets — they are
   one.** The paper cites the training set as `Gifford et al., 2024` (the Algonauts 2025
   challenge paper) precisely because TRIBE used the *4-subject Algonauts curation of
   CNeuroMod*, not the full 6-subject databank. §5.7: "we focus on a subset of four subjects
   curated for the Algonauts 2025 competition (the other two subjects are not publicly
   available at the time of writing)." The repo confirms this — the loader is literally
   `tribev2/studies/algonauts2025.py`.
2. **"~1,000+ hours across 720 subjects" is correct and slightly understated.** Table 1 totals:
   **1,117.7 h fMRI, 720 subjects, 5,094 sessions, 121.1 h video, 142.4 h audio, 71k sentences.**
3. **StudyForrest and Cam-CAN are NOT in TRIBE.** Zero mentions in the full text. Confirmed by grep.

### The eight datasets

**Training — 4 "deep" datasets, 25 subjects, 451.6 h**

| Dataset | Modalities | Subj | fMRI h | Stimuli |
|---|---|---|---|---|
| CNeuroMod (`St-Laurent 2023` / `Gifford 2024`) | A+V+T | 4 | 268.7 | *Friends* S1–S6, plus *The Bourne Supremacy*, *Hidden Figures*, *The Wolf of Wall Street*, *Life* (BBC nature doc) |
| BoldMoments (`Lahner 2024`) | A+V | 10 | 61.9 | 1,102 × **3-second** clips from Memento10k |
| Lebel2023 (`LeBel 2023`) | A+T | 8 | 85.8 | 27 (+57 for 3 subj) *Moth* podcast stories — **audio only** |
| Wen2017 (`Wen 2018`) | V | 3 | 35.2 | YouTube/VideoBlocks clips in 8-min streams — **silent, no audio** |

**Testing — 4 "wide" datasets, 695 subjects, 666.1 h** (all held out, never trained on)

| Dataset | Modalities | Subj | fMRI h | Stimuli |
|---|---|---|---|---|
| NNDb (`Aliko 2020`) | A+V+T | 86 | 160.6 | 10 full-length feature films |
| LPP (`Li 2022`) | A+T | 112 | 180.2 | *Le Petit Prince* audiobook — **audio only** |
| Narratives (`Nastase 2021`) | A+T | 321 | 146.6 | Spoken stories — **audio only** |
| HCP 7T (`Van Essen 2013`) | A+V+T | 176 | 178.7 | Movie clips, 7T |

Plus **IBC** (`Pinho 2018`) — controlled localisers, used only for the in-silico experiments,
not in Table 1's hour counts.

### The thing that matters most for this project

**Only three of the eight datasets contain real cinema: CNeuroMod, NNDb, and HCP 7T.**

Of the 121.1 h of video TRIBE ever saw, CNeuroMod contributes 64.5 h and everything else is
3-second Memento10k clips (33.2 h), silent YouTube (3.1 h), NNDb (19.4 h) and HCP (1.0 h).
Three of the four *test* sets are audio-only narratives with no image at all. So TRIBE's
exposure to deliberate cinematography is dominated by a single sitcom shot in a
multi-camera studio style — *Friends* is 64.5 h of the 121.1 h, and its coverage of shot
scale, camera movement and lighting variation is narrow by any film-form standard.

A note on TRIBE's own methods that is directly relevant: §5.9 records that for one in-silico
experiment "since the original movie was not available for download, we simply contrast
segments from the Algonauts dataset which contain speech versus those which do not." Meta hit
the same stimulus-access wall described below.

**Licence:** code and weights are **CC-BY-NC-4.0** (verified in the repo LICENSE and README).
Non-commercial only. That constrains any productised use downstream.

---

## Can we get the stimuli?

Ranked by friction. This is where the project's real cost sits.

### Open, no application (start here)

**NNDb — OpenNeuro `ds002837`, licence CC0, 89 GB, 887 files, 86 subjects.**
Verified via OpenNeuro's GraphQL API: `public: true`, `License: "CC0"`, snapshot 2.0.0,
DOI 10.18112/openneuro.ds002837.v2.0.0. The ten films, from the BIDS task labels:

`500 Days of Summer` · `12 Years a Slave` · `Citizenfour` · `The Usual Suspects` ·
`Pulp Fiction` · `The Shawshank Redemption` · `The Prestige` · `Back to the Future` ·
`Split` · `Little Miss Sunshine`

This is the single best target. Ten commercially-released features spanning wildly different
cinematographic registers (Deakins-adjacent prestige drama, a documentary, a Tarantino
ensemble, an M. Night thriller), 86 subjects, CC0 fMRI, one command to download. The **films
themselves are not in the CC0 release** — they are commercial titles and you source your own
copies. For a private research annotation pass that is a non-issue; for redistributing
annotations it is fine (timecoded labels are not the film).

**StudyForrest — CC BY-SA, openly downloadable, and already annotated.** Not in TRIBE, but
the most valuable dataset in this whole list for this specific project, because the shot-level
annotation work is *already done and public*:

- **870 shot boundaries** with depicted locations and temporal progression
- 2,500+ sentences / 16,000 words / 66,000 phonemes of speech annotation
- portrayed emotions (arousal, valence, category)
- semantic conflict markers (lies, irony, sarcasm), body-contact events
- **low-level perceptual confounds already extracted: volume, brightness, frame differences**
- eye-gaze during scanning, with saccade/fixation/smooth-pursuit classification

fMRI: 7T audio-only movie (n=20, 2 h) and 3T audio-visual movie (n=15, 2 h) plus in-lab
eye-tracking controls. The stimulus is *Forrest Gump*; you source the film yourself.

That the confound regressors are pre-extracted matters more than it sounds — see the
validation section.

### Application required, weeks not days

**Courtois NeuroMod.** Two tiers, confirmed on cneuromod.ca/access/access/ and docs.cneuromod.ca:

- *Partial, unrestricted*: four subjects (sub-01, 02, 03, 05) via the Canadian Open
  Neuroscience Platform, under "a liberal Creative Commons data license, in particular
  authorizing re-sharing of derivatives." **This is the tier TRIBE used.** No application.
- *Full databank*: six subjects. Requires an access form (English or French), project
  approval, then a signed **Data Transfer Agreement**. Contact courtois.neuromod@gmail.com.
  The docs note DTA templates were "available soon", so terms cannot be pre-reviewed.

On stimuli: the docs for **movie10** state segments live at
`movie10/stimuli/<movie>/<movie>_seg<seg>.mkv` — so the four feature films *are* carried
inside the databank as video. **Friends** is different: what is distributed is visual frames,
audio samples and time-stamped English subtitles, not the episodes. Neither page carries an
explicit copyright statement for the underlying commercial content, which is itself a caution
— these are Warner Bros. and Universal titles under a research-use framing.

Friends coverage per the docs: seasons 1–7, ~170 episodes, ~65 h viewing per subject, 61.9 h
fMRI/subject; sub-04 only got through S1–S4. **Season 7 is withheld as the Algonauts held-out
test set.** Episodes are cut into ~12-min runs with deliberate overlap.

**Algonauts 2025.** Four subjects, Friends S1–S6 train (55 h) + S7 test (10 h), plus the four
movie10 films. Distributed via a Google Form, underlying data CC0 through CONP. The challenge
closed July 2025; the page does not state whether downloads remain open, so assume you may
need to ask.

**Cam-CAN.** Application with academic affiliation, a stated hypothesis, and supervisor
sign-off for students. The site is explicit that "requesting ALL the data with vague
hypotheses" gets rejected. 649 participants completed the movie task; TA=7:57, multi-echo,
instruction was simply "enjoy movie". **I could not verify the film's identity from a primary
Cam-CAN source** — the dataset pages do not name it. It is widely reported in the literature
as a condensed ~8-minute cut of Hitchcock's *Bang! You're Dead*; treat that as unconfirmed
until you see it in the Cam-CAN materials or Taylor et al. 2017.

**HCP 7T.** 176 subjects, 7T, four movie runs. Requires HCP data-use terms acceptance
(open-access tier is self-serve; restricted tier is an application). **I could not verify
which clips were used** — the HCP documentation page I fetched did not cover 7T movie
stimuli. It is generally described as a mix of Creative Commons independent/Vimeo shorts and
Hollywood clips, but do not rely on that without checking the 7T release notes. Only 1.0 h of
video, so it is low-value for annotation anyway.

### Tooling that removes most of the annotation labour

You do not have to hand-code shot scale. Two ready datasets plus trained CNNs exist:

- **CineScale** (Savardi, Kovács, Signoroni, Benini, *Data in Brief* 2021): 792,000+ frames
  from 124 complete films by Scorsese, Godard, Béla Tarr, Fellini, Antonioni and Bergman,
  double-coded with adjudication, on nine classes — ECU, CU, MCU, MS, MLS, LS, ELS, FS, IS.
  **Model and code for automated shot-scale recognition are provided.**
- **CineScale2** (same group, 2023): ~25,000 frames annotated for **camera angle** (Overhead,
  High, Neutral, Low, Dutch) and **camera level** (Aerial, Eye, Shoulder, Hip, Knee, Ground),
  again with a CNN.

Frames are shared on request under fair use; the models are the point. Shot-boundary
detection itself is a solved commodity problem (TransNetV2 and equivalents).

**The gap I could not fill:** I found **no published shot-level cinematographic annotation of
the Friends/CNeuroMod stimuli**. Searches for it returned nothing. If that holds, annotating
CNeuroMod is genuinely novel work — but see below for why NNDb is the better first target.

---

## Existing technique → brain findings

This is the section that may change the plan. A great deal is already published, and one 2026
review has already organised it.

### The review that does most of the work

**Cao, Wang, Xiao & Wang (2026), "Rethinking Naturalistic Movie Neuroimaging Through Film
Form", *Behavioral Sciences* 16(5):639, CC BY, PMC13203540, 153 references.**

Its argument is precisely the premise of this project, stated as a methodological warning:
films are "systematically constructed through film forms such as editing, camera movement,
and sound, which diverge from natural perceptual conditions and shape cognitive processing",
and film form should be modelled as an explicit **mediating layer** between stimulus and
cognition. It proposes the **Film Cognition Matrix** — film forms (editing, camera, lighting,
colour, sound, subtitles, narrative, acting, viewer–film interaction) × cognitive domains
(attention, emotion, memory) — with each cell a form–function intersection.

Read this before designing anything. Two of its conclusions are load-bearing:

- **Editing dominates the literature**; colour, camera and sound are comparatively
  under-studied. The matrix has real empty cells (it names "the effects of acting style on
  attentional allocation" as an example gap).
- It explicitly recommends the analysis this project would run: "editing rate, which can be
  convolved with a hemodynamic response function in fMRI analyses… while regressors indexing
  the occurrence of close-up shots can be used to examine modulation in face-processing or
  affective networks."

That is the proposed method, already written down, by people who reviewed 153 papers.

### Specific technique → named-region findings that already exist

**Cuts / event boundaries → hippocampus.** Ben-Yakov & Henson (2018, *J Neurosci*, 277
citations): event boundaries defined by independent observers elicit a strong hippocampal
response, **scaling with boundary salience** (how many observers marked it), and this survives
covarying out a large number of perceptual factors. Two cohorts: n=253 on an 8.5-min film,
n=15 on a 120-min film. Both sensitive *and* specific — data-driven hippocampal peaks
correspond to boundaries. This is about as clean as naturalistic fMRI gets.

**Cuts → early visual, then higher-order associative regions.** Per the review: event
boundaries produce transient early-visual responses, with distinct higher-order engagement
emerging specifically when *narrative* structure rather than low-level visual change is
disrupted (Magliano & Zacks 2011; Zacks et al. 2010, "The brain's cutting-room floor",
*Front Hum Neurosci*, 256 citations).

**Narrative temporal disruption → posterior temporal cortex, mPFC, precuneus, cerebellum.**
Breaking film temporal continuity drops inter-subject synchrony in exactly these
long-timescale-integration regions (Lahnakoski et al. 2017).

**Camera movement → sensorimotor cortex, specifically.** Heimann et al. (2019, *PLoS ONE*, 65
citations) shot the same empty room with a static camera, a zoom, and a Steadicam. Steadicam
produced significantly stronger **beta-band event-related desynchronisation of the rolandic mu
rhythm** than static or zoom. Critically, **no equivalent modulation in attention-related
occipital areas** — so the effect is sensorimotor/embodied, not attentional. This is the
cleanest existing demonstration that a purely formal choice, content held constant, moves a
specific neural signature.

**Shot scale change across a cut → graded N300–N400.** Sanz-Aznar, Bruni & Soto-Faraco (2023,
*Front Neurosci*): 20 viewers, four cinematographic excerpts. **Scale-out cuts amplify** the
N300–N400 deflection relative to scale-preserving cuts; **scale-in cuts attenuate** it.
**Camera-angle changes across the cut produced no robust ERP difference.** The authors tie
this to conscious cut detection and note it matches what editing manuals already prescribe —
cut from wider to tighter for fluidity.

**Cuts generally → syntactic-violation ERP; 180° rule violations dissociate later.** Heimann
et al. (2016, *Cognitive Science*): cuts elicit an early ERP component indexing syntactic
violation, as in language, music and action processing. Continuity edits and cuts-across-the-
line differ at *later* components (spatial remapping, conscious awareness). Occipital alpha
did *not* support an attention account; central mu rhythm ERD did — again pointing to
sensorimotor networks.

**Cuts → theta then delta, time-resolved.** Sanz-Aznar et al. (2021): transient theta-band
synchronisation within ~200 ms (orienting), then delta-band desynchronisation over parietal
regions (perceptual integration / scene updating). An earlier EEG study reports the same
shape: theta synchronisation in the first 188 ms with left lateralisation, delta
desynchronisation 250–750 ms, parietal-dominant.

**POV editing → precuneus, PCC, hippocampus, OFC, fusiform gyrus, insula.** Cao et al.
(2024b) — the Kuleshov effect run on authentic cinematic material with neuroimaging, not just
behavioural ratings. Converging behavioural + neural evidence that contextual editing alters
emotional perception, with that named region set.

**Editing rate / cut density → subjective time, via SMA.** Higher cut density accelerates
information updating; viewers perceive time passing faster while *overestimating* duration.
Cancer et al. (2025) show this is mediated by sensorimotor timing — modulating **supplementary
motor area** activity selectively alters perceived duration, time passage and action speed as
a function of editing style.

**Lighting direction → early occipito-parietal responses.** Huttunen (2025): underlighting,
top-lighting and silhouette configurations amplify early occipito-parietal responses
associated with automatic emotional evaluation, **even absent explicit emotional content**.

**Film music → superior temporal sulcus and precuneus.** Muller-Rodriguez & Daly (2021):
moment-to-moment acoustic features of film music track shared arousal/valence fluctuations
across viewers with convergent activity in STS and precuneus.

**Sound masks cuts.** T. J. Smith & Martin-Portugues Santacreu (2017): presence of sound
substantially reduces awareness of edits by sustaining attentional continuity, especially when
audio aligns with post-cut motion. Directly relevant if you ever model visual technique
without the audio track.

**Close-up frequency → mental-state attribution, with an inverted-U.** Bálint, Blessing &
Rooney (2020, *Poetics*, N=495): close-up frequency significantly influenced *spontaneous*
mental-state attribution but not prompted attribution, and the relationship is non-monotonic —
more close-ups help up to a point, then hurt. Behavioural, not neural, but it is the single
best-powered technique-manipulation study in the set, and the non-monotonicity is a warning
against assuming linear technique→response.

**Directing style → ISC magnitude.** Hasson et al. (2008), "Neurocinematics", *Projections*,
558 citations. Control over viewers' brain activity differs as a function of movie content,
editing and directing style; Hitchcock produced the highest ISC. This is the field's founding
result and it is a *style-level*, not shot-level, claim.

### The one prior attempt at exactly the annotate-and-regress method

**Kauttonen, Hlushchuk & Tikka (2015), "Optimizing methods for linking cinematic features to
fMRI data", *NeuroImage*, 38 citations.** They annotated Maya Deren's *At Land* (1944) with
**36 binary + 1 continuous** content features and regressed them against fMRI, comparing
elastic-net regularised regression against PLS and unregularised OLS, over both ICA components
and grey-matter ROIs, with permutation testing.

Findings: 9 of 40 ICs significantly correlated with the annotation model; activations in
parietal and occipital regions with smaller frontal clusters; **elastic net outperformed both
PLS and unregularised regression** because the cinematic regressors are heavily multicollinear.

This is the methodological precedent and it flags the central statistical hazard: **film
technique regressors are strongly correlated with each other and with low-level image
properties.** Their answer was regularisation. Note the study deliberately used a
*non-narrative* film to decouple technique from story — a design choice worth stealing, and a
reason their parietal/occipital result may not generalise to narrative cinema.

---

## The validation opportunity

**Yes — and it is cheaper and more defensible than a TRIBE-prediction study.**

### The core asymmetry

TRIBE gives you technique → *model prediction*. Annotating an open fMRI film dataset gives you
technique → *measured cortical response* in real people. The second is strictly stronger
evidence, and the datasets to do it are already CC0.

There is a live cautionary result on the first path. **Sahu & Pandey (arXiv:2607.01400, July
2026), "A global predicted-fMRI drive signal from TRIBE does not predict YouTube replay
heatmaps"** ran TRIBE over 48 YouTube videos, pooled its cortical predictions into an
engagement metric, and tested it against YouTube "most replayed" data. Pooled
position-controlled partial correlation **+0.058, 95% CI [−0.04, 0.15], t(47)=1.21, p=0.23**,
and **not above simple loudness/motion baselines**. Null across networks, regions and methods,
with the authors arguing for a true absence rather than a power failure.

That is one preprint, testing a crude global pooling against a noisy behavioural proxy — it is
not a verdict on TRIBE as an encoder. But it is exactly the shape of claim this project would
be tempted to make, and it failed. Design around it.

### Concretely, what I would do

**Target: NNDb (`ds002837`).** CC0, 86 subjects, ten full features, 89 GB, no application, and
the films span enough stylistic range to give real variance in technique — which *Friends*,
64.5 h of TRIBE's 121.1 h of video, does not.

**Pilot first: StudyForrest.** Two hours, n=15 audio-visual at 3T, **870 shot boundaries
already coded**, and volume/brightness/frame-difference confound regressors **already
extracted**. You can have a complete technique→response pipeline running against real measured
BOLD before annotating a single frame yourself. If the pipeline cannot recover Ben-Yakov &
Henson's hippocampal boundary response on StudyForrest, it is broken, and you will know that
in days rather than months.

**The build:**

1. **Shot boundaries** — TransNetV2 or equivalent, then spot-check. Commodity.
2. **Shot scale** — run the CineScale CNN. Nine classes, already trained on 792k frames from
   124 films.
3. **Camera angle and level** — run the CineScale2 CNN. Eleven classes across two axes.
4. **Camera movement** — the weakest automated link; static/pan/tilt/dolly/handheld likely
   needs its own classifier or hand-coding. Heimann et al. (2019) gives you the hypothesis
   (Steadicam-class motion → sensorimotor beta ERD) but that was EEG, so the fMRI prediction
   needs restating in BOLD terms.
5. **Confounds** — luminance, contrast, saturation, optical-flow magnitude, RMS audio, speech
   presence. **Non-negotiable.** Kauttonen et al. found cinematic regressors badly
   multicollinear, and the Sahu & Pandey null was specifically "not above loudness/motion
   baselines". Every technique effect must be shown to survive these.
6. **Model** — convolve each technique regressor with an HRF; elastic-net regularised voxelwise
   or parcelwise encoding, following Kauttonen et al.'s explicit finding that elastic net beat
   PLS and OLS on exactly this multicollinearity problem. Cross-validate across *films*, not
   just across time within a film.
7. **Validate against known results before claiming new ones.** Recover the hippocampal
   event-boundary response (Ben-Yakov & Henson 2018) and the early-visual cut transient. These
   are your positive controls. Only then interpret novel cells of the Film Cognition Matrix.

**Effort, honestly:** the pilot is small — days to a couple of weeks, given the annotations
exist. NNDb is the real work: ~19.4 h of film to annotate (automated, but needing QC), 89 GB
to fetch and preprocess, and the fMRI preprocessing is the long pole unless you take the
authors' preprocessed derivatives. Call it weeks, not months, for a first result. No
applications, no DTAs, no waiting on committees — which is the single biggest argument for
starting with NNDb and StudyForrest rather than CNeuroMod.

**Where genuine novelty is available.** The review is explicit that colour, camera and lighting
are under-studied relative to editing, and that no one has systematically compared *multiple*
film forms within the same cognitive domain, or modelled their interaction. Most existing
neural evidence is EEG/ERP (Heimann, Sanz-Aznar) rather than fMRI, so the **spatial** mapping
of shot scale and camera movement is largely open. A CineScale-annotated NNDb would let you
populate several empty matrix cells at once, with named regions, in the same subjects.

**What is already answered, and should not be re-run.** Cuts → hippocampus. Cuts → early
visual. Scale-out vs scale-in asymmetry at the cut. Camera movement → sensorimotor, not
attentional. Editing → raised ISC. Music → STS/precuneus. Cite these; do not rediscover them.

### The three things most likely to sink it

1. **Multicollinearity.** Close-ups co-occur with faces, with dialogue, with reduced optical
   flow. Cut rate co-occurs with action, loudness and luminance change. Without aggressive
   confound modelling you will "discover" the face area responds to faces.
2. **Technique is confounded with narrative.** Directors cut faster *because* the scene is
   tense. Kauttonen et al. sidestepped this by choosing a non-narrative film; you cannot, on
   NNDb. Partial answer: exploit within-film contrasts where technique varies and narrative
   arousal is matched, and treat cross-film effects as weaker evidence.
3. **Non-monotonic effects.** Bálint et al. found close-up frequency has an inverted-U on
   mental-state attribution. Linear regressors will miss or misreport this. Model non-linearity
   at least for the dose-like features (cut rate, close-up density).

---

## Sources

**Primary — TRIBE v2**
1. [arXiv:2605.04326](https://arxiv.org/abs/2605.04326) — d'Ascoli et al., "A foundation model of vision, audition, and language for in-silico neuroscience", FAIR at Meta. Full HTML text parsed; Table 1 and §5.7 are the dataset ground truth.
2. [github.com/facebookresearch/tribev2](https://github.com/facebookresearch/tribev2) — repo tree via GitHub API; `tribev2/studies/` contains exactly `algonauts2025.py`, `lahner2024bold.py`, `lebel2023bold.py`, `wen2017.py`. Licence CC-BY-NC-4.0.
3. [huggingface.co/facebook/tribev2](https://huggingface.co/facebook/tribev2) — weights.
4. [arXiv:2607.01400](https://arxiv.org/abs/2607.01400) — Sahu & Pandey, TRIBE predicted-fMRI drive signal fails to predict YouTube replay heatmaps. The relevant null result.

**Datasets**
5. [OpenNeuro ds002837](https://openneuro.org/datasets/ds002837) — NNDb. CC0, 89 GB, verified via GraphQL API. DOI 10.18112/openneuro.ds002837.v2.0.0
6. [Aliko et al. 2020, *Sci Data*](https://doi.org/10.1038/s41597-020-00680-2) — the NNDb paper.
7. [studyforrest.org/data.html](https://www.studyforrest.org/data.html) — annotations inventory incl. 870 shot boundaries; CC BY-SA.
8. [Hanke et al. 2014, *Sci Data*](https://doi.org/10.1038/sdata.2014.3) — StudyForrest 7T audio movie.
9. [Hanke et al. 2016, *Sci Data*](https://doi.org/10.1038/sdata.2016.92) — StudyForrest 3T audio-visual + eye gaze.
10. [cneuromod.ca/access/access/](https://www.cneuromod.ca/access/access/) — partial (CONP, unrestricted, 4 subjects) vs full (DTA, 6 subjects).
11. [docs.cneuromod.ca — friends](https://docs.cneuromod.ca/latest/datasets/friends.html) and [movie10](https://docs.cneuromod.ca/latest/datasets/movie10.html) — stimulus distribution details; movie10 ships `.mkv` segments, Friends ships frames/audio/subtitles.
12. [algonautsproject.com/2025/challenge.html](https://algonautsproject.com/2025/challenge.html) — 4 subjects, Friends S1–S6 train / S7 test, four movies, Google Form access, CC0 via CONP.
13. [opendata.mrc-cbu.cam.ac.uk/projects/camcan/](https://opendata.mrc-cbu.cam.ac.uk/projects/camcan/) — application process; 649 subjects, TA=7:57 movie task. Film not named on-site.

**The review that shortcuts the project**
14. [Cao, Wang, Xiao & Wang 2026, *Behavioral Sciences* 16(5):639](https://doi.org/10.3390/bs16050639) — "Rethinking Naturalistic Movie Neuroimaging Through Film Form"; the Film Cognition Matrix. CC BY. Full text: [PMC13203540](https://pmc.ncbi.nlm.nih.gov/articles/PMC13203540). **Read first.**

**Technique → brain**
15. [Ben-Yakov & Henson 2018, *J Neurosci*](https://doi.org/10.1523/jneurosci.0524-18.2018) — event boundaries → hippocampus, salience-scaled, perceptually controlled.
16. [Heimann et al. 2019, *PLoS ONE*](https://doi.org/10.1371/journal.pone.0211026) — camera movement → rolandic mu beta ERD; Steadicam > zoom/static; no occipital/attentional effect.
17. [Heimann et al. 2016, *Cognitive Science*](https://doi.org/10.1111/cogs.12439) — cuts as syntactic violation; 180° rule; central mu rather than occipital alpha.
18. [Sanz-Aznar, Bruni & Soto-Faraco 2023, *Front Neurosci*](https://doi.org/10.3389/fnins.2023.1173704) — scale-out amplifies / scale-in attenuates N300–N400; camera angle does not.
19. [Kauttonen, Hlushchuk & Tikka 2015, *NeuroImage*](https://doi.org/10.1016/j.neuroimage.2015.01.063) — 37 annotated cinematic features → fMRI; elastic net beats PLS/OLS. The methodological precedent.
20. [Hasson et al. 2008, *Projections*](https://doi.org/10.3167/proj.2008.020102) — Neurocinematics; ISC varies with editing and directing style.
21. [Zacks et al. 2010, *Front Hum Neurosci*](https://doi.org/10.3389/fnhum.2010.00168) — "The brain's cutting-room floor".
22. [Bálint, Blessing & Rooney 2020, *Poetics*](https://doi.org/10.1016/j.poetic.2020.101480) — close-up frequency → spontaneous mental-state attribution, inverted-U, N=495.
23. [Sonkusare et al. 2020, *NeuroImage*](https://doi.org/10.1016/j.neuroimage.2020.117445) — "Movies and narratives as naturalistic stimuli in neuroimaging", 192 citations. General background.

**Annotation tooling**
24. [Savardi, Kovács, Signoroni & Benini 2021, *Data in Brief*](https://doi.org/10.1016/j.dib.2021.107002) — CineScale: 792k frames, 124 films, 9 shot-scale classes, CNN + code.
25. [Savardi et al. 2023, *Data in Brief*](https://doi.org/10.1016/j.dib.2023.109627) — CineScale2: camera angle (5) and camera level (6), ~25k frames, CNN + code.

**Caveats on sourcing.** Europe PMC was returning 502/504 throughout this session, and MDPI,
Nature and PubMed all block direct fetches — the Cao et al. full text was retrieved via NCBI
E-utilities against PMC13203540 instead. The session's WebSearch budget (200 calls) was
already exhausted before I started, so the literature sweep ran on OpenAlex, Semantic Scholar
and arXiv APIs rather than general search. Two facts I could **not** verify against a primary
source and have flagged inline: the identity of the Cam-CAN film, and which clips make up the
HCP 7T movie runs.
