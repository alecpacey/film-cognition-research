# Vocabularies for the cognitive layer

*Research date: 2026-09-02. All counts below were pulled directly from the live APIs and data files, not from secondary descriptions — commands and URLs are in Sources.*

## Recommendation

**Adopt a two-layer vocabulary: NeuroQuery's curated psychology term set as the decoding target, and a hand-authored ~30-term "directorial construct" layer sitting on top of it, with an explicit many-to-many crosswalk that you write yourself.**

Do not adopt a single existing ontology. None of them will carry the chain on its own.

Specifically:

1. **Decoding layer — NeuroQuery `neuroquery6308` vocabulary, filtered to its `psychology` category.** That is **1,604 terms** (I computed the intersection: 6,308 model-vocabulary terms ∩ 4,809 psychology-categorised normalised terms). This is the only vocabulary that is simultaneously (a) large enough to be expressive, (b) curated so that anatomy/disease/method noise is separable, (c) backed by a continuous predictive model over 13,459 studies rather than a per-term binary map, and (d) still maintained (`neuroquery` package 1.1.0, Aug 2025). It contains `surprise`, `narrative`, `threat`, `empathy`, `mentalizing`, `agency`, `trust`, `curiosity`, `vigilance`, `startle`, `salience`, `anticipation`, `memory encoding`, `story comprehension`, `aesthetics`, `beauty`, `naturalistic`, and `film` — none of which survive in Neurosynth's term list.

2. **Structure layer — Cognitive Atlas concepts (918) for the is-a / part-of relations**, used only to organise and disambiguate, never as the decoding target. Its definitions are human-written and its relationships are asserted, which is exactly what you want for building a defensible crosswalk document; but it is not itself linked to images.

3. **Fallback / sanity layer — BrainMap behavioural domains (~70 categories, 5 top-level).** Coarse, but it is the one taxonomy that is *hand-coded by experts* onto every experiment in the database. Use it as a coarse-grained check that a fine-grained NeuroQuery decode is not hallucinating: if the fine decode says "threat" but the coarse domain profile says `Cognition.Language`, the decode is wrong.

4. **The directorial layer you must author yourself.** Roughly thirty constructs — tension, suspense, dread, immersion, spatial presence, social presence, threat proximity, familiarity, orientation/disorientation, surprise, subjective time dilation, character alignment, dramatic irony, and so on. **Twelve of the most important of these do not exist in any vocabulary I checked** (see The gap). This layer is a deliverable of your project, not something you can download.

Why not Neurosynth as the decoding layer: its vocabulary is 3,228 raw abstract tokens, of which 60 begin with a digit and which include `12 healthy`, `2014`, `voxel`, `roi`, `bold`, `groups`, `gyrus`, `anterior`, `task`, `effects`, `signal`. Every filmmaker-facing term I searched for is either absent (`suspense`, `narrative`, `surprise`, `agency`, `startle`, `vigilance`, `trust`, `film`, `movie`, `aesthetic`, `curiosity`, `awe`, `immersion`) or present as a *homograph of a methods word*: `presence` is in the list, but in a neuroimaging abstract "presence" means "the presence of a lesion"; `engagement` means "task engagement"; `flow` resolves to `blood flow`; `character` resolves to letters on a screen; `identification` means "identification of ROIs". Decoding to that vocabulary would produce a readout that *looks* like it says something about presence and engagement and is in fact measuring English prose habits. That is the single most dangerous failure mode available to this project, and Neurosynth walks straight into it.

If you want richer semantics than 1,604 terms allows, the 2025 direction is **NiCLIP** (Peraza, Kent, Nichols, Poline, de la Vega, Laird) — a CLIP-style contrastive model trained on 23,000+ full-text neuroscience articles that predicts *free text* from activation maps rather than scoring a fixed term list. Its own finding is relevant to your decision: performance was best "when using full-text articles instead of abstracts, as well as a **curated cognitive ontology with precise task-concept-domain mappings**" — i.e. even the model designed to escape fixed vocabularies did better with a curated ontology attached. It is a bioRxiv preprint, not a shipping tool, and it degrades on subject-level maps. Treat it as the v2 path, not v1.

---

## Ontology comparison

| Name | Size | Derivation | Maintained | Neuroimaging-linked | Usable by a filmmaker? |
|---|---|---|---|---|---|
| **Cognitive Atlas** | 918 concepts, 857 tasks, 221 disorders; 11 concept classes | Expert-curated, community-editable wiki (Poldrack, NIMH-funded) | Partially. Concept `last_updated` stamps exist for 2020–2025 but only 50 of 918 concepts carry one; 868 have never been updated since import. `cogat-python` client last pushed Jul 2024; a `legacy_cogat_linkml` re-modelling repo was pushed Feb 2025. Alive but slow. | **Indirectly.** It defines concepts and asserts concept↔task↔contrast relations, but ships no images. It is the label set NeuroVault/NiMARE point *at*, not a data source. | **Partly.** Has `attention` (25 sub-types), `emotion` (17), `memory` (25+), `surprise`, `empathy`, `familiarity`, `agency`, `theory of mind`, `mentalization`, `narrative`, `narrative comprehension`, `curiosity`, `salience`, `time perception`, `biological motion`. Lacks `tension`, `suspense`, `immersion`, `presence`, `threat`, `engagement`, `absorption`, `awe`, `aesthetic`. |
| **CogPO** (Cognitive Paradigm Ontology) | Small; task/paradigm-level classes (stimulus type, response type, instruction) | Expert-authored by Turner & Laird to annotate the fMRI literature's *experimental design*, not its psychology | **No.** cogpo.org still resolves but the last CogPO paper is Chakrabarti et al. 2014; the ontology is not in the EBI OLS4 index. PIs' contact details on the site are stale (Laird listed at UTHSCSA, Turner at MIND). Effectively dormant. | Yes by construction — it exists to annotate BrainMap experiments. | **No.** CogPO describes *paradigms*: stimulus modality, response modality, instructions. Its vocabulary is `visual stimulus`, `button press`, `attend`, `n-back`. It cannot express what a scene is doing to a viewer; it can only express how an experiment was run. Wrong layer entirely. |
| **BrainMap behavioural domains** | ~70 categories, 5 top-level (Action, Cognition, Emotion, Interoception, Perception) + Pharmacology | Expert-defined taxonomy; every experiment in BrainMap is hand-coded to it by a trained annotator | Yes, but stable/frozen — the taxonomy has not materially changed in years. The database continues to grow. | **Yes, strongly.** ~20–30% of the compliant literature is coded to it; this is the only vocabulary with human-verified per-experiment labels. | **Coarse but honest.** `Emotion.Negative.Fear`, `Emotion.Negative.Anxiety`, `Emotion.Positive.Humor`, `Emotion.Intensity`, `Emotion.Valence`, `Cognition.Attention`, `Cognition.Social Cognition`, `Cognition.Spatial`, `Cognition.Temporal`, `Cognition.Memory.Explicit`, `Perception.Vision.Motion`. A director understands all of those. But there are only ~70, and there is no tension, no suspense, no presence. |
| **Neurosynth v7 terms** | **3,228** raw terms; ~1,300 have enough studies for a usable map | **Word/bigram frequency in abstracts**, tf-idf weighted. No curation. 713 are multi-word, 60 start with a digit. | **No.** `neurosynth-data` last commit Aug 2021; the neurosynth.org `/api/analyses/terms/` endpoint currently returns HTTP 500. Superseded by Neurosynth Compose (compose.neurosynth.org, live) and NiMARE (actively developed, last commit Aug 2026). | Yes — 14,371 studies, per-term association maps, the most-used decoding substrate in the field. | **No, and dangerously so.** See Recommendation. `suspense`, `narrative`, `surprise`, `agency`, `startle`, `vigilance`, `trust`, `immersion`, `aesthetic`, `curiosity`, `awe`, `film`, `movie` are all absent. `presence`, `engagement`, `flow`, `character`, `identification` are present but mean something else. |
| **Neurosynth v7 LDA topics** | 50 / 100 / 200 / 400 topic sets | LDA over the same abstracts; each topic is a *ranked word list*, unnamed | Same freeze (2021), same data repo | Yes — topic-weight maps ship alongside | **Better than the raw terms, but unnamed.** LDA100 topic 26 is unmistakably threat (`fear anxiety ptsd amygdala threat conditioning extinction … anticipation … threatening`); topic 30 is affect (`emotional negative positive amygdala emotion affective neutral valence arousal`); topic 33 is reward anticipation; topic 49 is attention/salience; topic 12 is narrative/discourse (`… narrative … discourse … story … metaphor … irony`). These are coherent and film-relevant. But they arrive as topic *numbers* with 100-word tails, so somebody has to name them — which is the same authoring job as the directorial layer, just with less control. |
| **NeuroQuery** | 6,308-term model vocabulary (full corpus vocab 156,521); **1,604 psychology-category terms in the model vocab**; 13,459 studies | Corpus-derived but **curated and categorised** — a shipped `termcategories.csv` sorts 39,755 terms into `anatomy` (17,461), `disease` (14,124), `psychology` (8,170). Multi-word phrases are first-class. | **Yes** — `neuroquery` 1.1.0, Aug 2025. Data repo is stable at v1 (2021) but the model package is live. | **Yes, and differently.** Rather than one map per term it fits a smoothed regression from text to brain, so it will produce a map for a *query phrase* it has never seen, by decomposing it over the vocabulary. | **Best of the lot.** Has `surprise`, `threat`, `narrative`, `story comprehension`, `agency`, `empathy`, `mentalizing`, `trust`, `vigilance`, `startle`, `curiosity`, `beauty`, `aesthetics`, `salience`, `arousal`, `valence`, `emotional valence`, `anticipation`, `reward anticipation`, `loss anticipation`, `memory encoding`, `emotion regulation`, `naturalistic`, `film`, `music`. Still no `suspense`, `immersion`, `presence`, `familiarity`, `absorption`, `awe`, or `theory of mind` as a phrase. |
| **Emotion Ontology (MFOEM)** | 624 classes | OBO-Foundry, expert-authored, appraisal-theory grounded | Yes — indexed and refreshed in EBI OLS4 (loaded 2026-09-02) | **No.** No image linkage at all. | **As a controlled emotion vocabulary, yes.** `fear`, `terror`, `anxiety`, `surprise`, `disgust` (with `core disgust`, `moral disgust`, `interpersonal disgust`, `animal-nature disgust`), `joy`, `sadness`, `amusement`, `interest`, `arousal`. But no `suspense`, no `dread`, no `tension`. Useful as a naming source for the emotion half of your directorial layer. |
| **Neuro Behavior Ontology (NBO)** | 4,546 classes | OBO-Foundry | Yes (OLS4, 2026) | No | **No.** Heavily animal-behaviour weighted (`galant reflex`, `male courtship behavior`). Wrong domain. |

---

## The terms that matter

Sorted by the intent a director would actually express. **Bold = present in NeuroQuery's psychology-categorised model vocabulary and therefore directly decodable today.**

**Attention and where the eye goes**
- **`attention`**, **`attention biased`**, **`salience`**, **`salience network`**, **`vigilance`**, **`hypervigilance`**, **`gaze`**
- Cognitive Atlas adds the fine grain a cinematographer would recognise: `covert attention` vs `overt attention`, `exogenous attention` (the cut that grabs you) vs `voluntary/endogenous`, `divided attention`, `spatial selective attention`, `attentional blink`, `inattentional blindness`, `attention shift`, `attentional resources`, `attentional effort`.
- BrainMap: `Cognition.Attention`.
- This is your strongest category. Directorial intent about *where the audience is looking and how hard they are working to look* maps cleanly.

**Threat, dread, and the body braced**
- **`threat`**, **`threatening`**, **`fear`**, **`fearful`**, **`fearful faces`**, **`anxiety`**, **`startle`**, **`startle response`**, **`acoustic startle reflex`**, **`anticipation`**
- Neurosynth LDA100 topic 26 is a ready-made composite: fear + anxiety + threat + conditioning + extinction + anticipation + threatening + aversive + sustained + unpredictable.
- Cognitive Atlas: `fear`, `anxiety`, `aversive salience`, `anticipation`.
- BrainMap: `Emotion.Negative.Fear`, `Emotion.Negative.Anxiety`.
- **Note what is missing: `suspense` and `dread` exist nowhere.** `anticipation` + `threat` + `uncertainty` is the closest available triple, and it is a real neural signature (Bezdek 2015/2017), just not a lexicalised one.

**Emotional temperature**
- **`arousal`**, **`valence`**, **`emotional valence`**, **`emotion`**, **`emotion perception`**, **`emotion recognition`**, **`emotion regulation`**, **`mood`**, **`disgust`**
- BrainMap has the two dimensions a colourist thinks in explicitly: `Emotion.Intensity` and `Emotion.Valence`, with `Emotion.Positive.Humor` as a bonus.
- MFOEM supplies named discrete emotions if you want them: `terror`, `amusement`, `interest`, `sadness`, `joy`, plus four flavours of disgust.

**Social presence and character**
- **`empathy`**, **`mentalizing`**, **`social cognition`**, **`trust`**, **`trustworthiness`**, **`face`**, **`face perception`**, **`face recognition`**, **`emotional faces`**, **`fusiform face`**, **`agency`**
- Cognitive Atlas: `theory of mind`, `mentalization`, `joint attention`, `emotional mimicry`, `facial trustworthiness recognition`, `social inference`, `social context`, `emotional bonding`.
- BrainMap: `Cognition.Social Cognition`.
- Strong coverage. "Do we trust this character," "does the audience read his mind," "are we with him or watching him" are all expressible.

**Spatial and where the viewer feels they are**
- **`spatial navigation`**, **`ability spatial`**, **`scene`**, **`place`**, **`motion`**
- Cognitive Atlas: `spatial cognition`, `spatial attention`, `spatial localization`, `near spatial distance` / `far spatial distance`, `body orientation`, `visuospatial sketch pad`, `biological motion`, `Naturalistic Biological Motion`.
- BrainMap: `Cognition.Spatial`, `Perception.Vision.Motion`.
- **`presence` and `immersion` are absent from every vocabulary** — see The gap and the crosswalk section, because these *do* have established neural correlates, just under a different name.

**Memory and what the audience will retain**
- **`memory encoding`**, **`encoding`**, **`encoding retrieval`**, **`autobiographical memory`**, **`autobiographical recall`**
- Cognitive Atlas: `memory acquisition`, `memory consolidation`, `emotional memory`, `episodic memory`, `context memory`, `self-reference effect`, `memory trace`.
- BrainMap: `Cognition.Memory.Explicit`, `.Implicit`, `.Working`.
- Directly usable: "will they remember this shot" is a real, decodable question (Bezdek 2017 and Song 2021 both tie narrative attentional state to subsequent memory).

**Surprise, prediction and the cut**
- **`surprise`**, **`prediction`**, **`expectation`**, **`uncertainty`**, **`novelty`** (Neurosynth has `novelty`; NeuroQuery has the prediction-error family)
- Cognitive Atlas: `expectancy`, `episodic prediction`, `novelty detection`, `conflict detection`, `monetary reward prediction error`.
- Neurosynth LDA100 topic 25 is the prediction-error topic (`feedback error learning prediction outcome … unexpected … predictability`).
- This matters for editing specifically: Drew et al. 2024 ("Perceptual oddities: assessing the relationship between film editing and prediction processes") makes the cut a prediction-violation event.

**Narrative and story**
- **`narrative`**, **`story`**, **`story comprehension`**, **`naturalistic`**, **`film`**
- Cognitive Atlas: `narrative`, `narrative comprehension`.
- Neurosynth LDA100 topic 12 is the discourse topic and it contains `narrative`, `story`, `stories`, `discourse`, `metaphor`, `irony`, `figurative`, `pragmatic`.
- Thin but real. Note `film` is in NeuroQuery's vocabulary at all, which is worth something.

**Aesthetic response**
- **`beauty`**, **`aesthetics`**, **`curiosity`**, **`music`**, **`musical`**
- Weakly grounded but present, and Hartung 2021 shows aesthetic appraisal and emotional intensity are neurally dissociable during narrative — so this is not vapour.

---

## The gap

Being blunt about it: **the vocabularies can express roughly two-thirds of what a director means, and the missing third is disproportionately the part directors care most about.**

**1. The core suspense vocabulary does not exist.** `tension`, `suspense`, `dread`, `anticipatory unease`, `mounting`, `release`. I checked all of them across Cognitive Atlas (918), Neurosynth (3,228), NeuroQuery (6,308), MFOEM (624), NBO (4,546), and BrainMap (~70). `suspense` appears in **none**. `tension` appears only in NeuroQuery, where it resolves to `hypotension` / `orthostatic hypotension` — cardiovascular, not dramatic. This is the exact word a director uses in a note ("the tension drops in the middle of the scene") and it is unavailable at every layer of the stack.

**2. Presence and immersion are absent as terms despite existing as science.** There is a twenty-year EEG/fMRI literature on spatial presence (Baumgartner 2006, Kober 2012, Havranek 2012 — see crosswalk) and the constructs have validated questionnaires. But they were developed by *communication scholars*, and the neuroimaging ontologies were built by *cognitive neuroscientists* annotating cognitive-psychology paradigms. The two literatures do not share a vocabulary, so presence never entered the ontologies. This is a sociological gap, not a scientific one — which means it is closable by you, by hand, rather than blocked.

**3. Neurosynth's homographs will silently produce false confidence.** `presence`, `engagement`, `flow`, `character`, `identification` are all in the term list and all mean methods-prose things. If your pipeline decodes to Neurosynth terms and reports "high presence," it will be reporting on how often the phrase "the presence of" appears in abstracts about a region. **Do not use Neurosynth's term vocabulary for this project.** This is the finding I would most want to survive summarisation.

**4. Ontology terms are states, not verbs; directorial intent is a verb with an object.** "Attention" is decodable. "Pull the audience's attention to the left third of the frame at 00:04, then release it" is not — it has a spatial target, a time course, and a direction of change. The ontologies give you a scalar per label per volume. Everything that makes a note *directorial* — where, when, how fast, toward what, followed by what — lives in the temporal derivative and the spatial argument, and no vocabulary encodes those. You will have to model timing and direction yourself, on top of whatever labels you decode.

**5. Nothing in any of these vocabularies is relational to the story.** `Dramatic irony` — the audience knows what the character does not — is a first-class directorial construct with no ontology entry at any granularity. The nearest available handle is `theory of mind` / `mentalizing`, and there is one paper that makes exactly this move (Cabañas et al. 2023, "The audience who knew too much: investigating the role of spontaneous theory of mind on the processing of dramatic events"). Similarly `character alignment`, `sympathy vs. empathy for a character`, `rooting interest`, `suspension of disbelief` (which finally got a validated *scale* in 2026, Loureiro et al., but has no imaging term). These have to be constructed as composites.

**6. Coarse ontologies are too coarse; fine ontologies are unreliable.** BrainMap's ~70 hand-coded domains are trustworthy but cannot distinguish "the shot makes you afraid" from "the shot makes you tense" — both are `Emotion.Negative`. NeuroQuery's 1,604 psychology terms can name the distinction but the underlying maps for rare terms rest on few studies. There is no tier that is both fine and solid. Plan for the readout to be a *distribution over ~20 reliable constructs*, not a single confident label.

**What would be needed instead — and it is buildable.** A **film-intent ontology**: ~30 constructs, each defined operationally, each mapped to (a) a weighted combination of NeuroQuery psychology terms, (b) a BrainMap domain for coarse sanity-checking, (c) a validated behavioural scale where one exists, and (d) at least one published naturalistic-viewing study establishing the neural signature. For example:

> **suspense** := 0.4·`anticipation` + 0.3·`threat` + 0.2·`uncertainty` + 0.1·`vigilance`; coarse domain `Emotion.Negative`; behavioural anchor = continuous suspense ratings (Bezdek 2015); neural anchor = Bezdek et al. 2015, *Neuroscience* (PMID 26143014), suspense narrows attentional focus and suppresses peripheral visual processing; secondary anchor = Lehne et al. 2014 (PMID 23974947), tension tracks OFC and amygdala.

Twelve to fifteen entries of that shape, written once and validated against a handful of naturalistic-viewing datasets, is the actual bridge. It is a week of careful work, not a research programme — but it is *your* work, and no download substitutes for it.

---

## Media-psychology crosswalk

Good news for the project: the media-psychology constructs a director recognises **do have neuroimaging correlates**, established over the last twenty years. They are simply not in the ontologies. This is the corpus your hand-authored layer should be built from.

| Construct | Origin / instrument | Neuroimaging correlate | Status |
|---|---|---|---|
| **Spatial presence** ("I am there") | Communication science; MEC-SPQ, ITC-SOPI | **Baumgartner et al. 2006** (PMID 16497116) — EEG + psychophysiology correlate of spatial presence in arousing non-interactive VR; **Kober & Neuper 2012** (PMID 22206906) — cortical correlate of spatial presence in 2D vs 3D interactive VR; **Havranek et al. 2012** (PMID 22812540) — perspective and agency during video gaming modulate both spatial-presence experience and activation pattern. Frontal/parietal dorsal-stream involvement, with prefrontal activity *inversely* related to presence (deactivation of self-monitoring). | **Established, replicated, and directly relevant to camera position and POV.** Note Havranek explicitly ties *perspective* — a camera decision — to presence. |
| **Narrative engagement / transportation** | Green & Brock transportation scale; Busselle & Bilandzic narrative engagement scale | **Intersubject correlation (ISC)** is the workhorse. **Schmälzle et al. 2015** (PMID 25653012) — "Engaged listeners: shared neural processing of powerful political speeches"; **Imhof et al. 2017** (PMID 28402568) and **2020** (PMID 31954843) — effective messages increase audience brain coupling; **Chang et al. 2024** (PMID 37873125) — multi-brain neural convergence during naturalistic storytelling; **Song et al. 2021** (PMID 34385312) — neural signatures of attentional engagement during narratives *and its consequences for event memory*; **Dini et al. 2023** (PMID 37460223) — EEG study of narrative engagement. | **Established.** ISC is the closest thing the field has to a direct engagement readout, and it does not require an ontology at all — it is stimulus-locked synchrony. Worth considering as a *parallel* readout alongside term decoding. |
| **Suspense** | Continuous self-report during viewing | **Bezdek et al. 2015** (PMID 26143014) — "Neural evidence that suspense narrows attentional focus": suspense suppresses peripheral visual processing; **Bezdek et al. 2017** (PMID 28764896) — visual and musical suspense, brain activation *and memory* during naturalistic viewing; **Lehne et al. 2014** (PMID 23974947) — musical tension tracks orbitofrontal cortex and amygdala. | **Established as a phenomenon, absent as a term.** The single clearest case where the science exists and the vocabulary does not. |
| **Immersion / flow** | Flow scale, immersive tendencies questionnaire | Sparse and mostly VR-clinical. The 478-hit PubMed set for immersion + neuroimaging is dominated by VR-as-intervention studies, not immersion-as-construct. | **Weak.** Treat `immersion` as a composite of spatial presence + narrative engagement rather than a target in its own right. |
| **Character morality / rooting interest** | Affective disposition theory (media psych) | **Weber et al. 2024** (PMID 38631616) — "Vicarious punishment of moral violations in naturalistic drama narratives predicts cortical synchronization"; **Obando Yar et al. 2025** (PMID 40458235) — "The science of story characters: a neuroimaging perspective on antagonists in narrative engagement". | **Emerging and specifically filmic.** Weber's result is that a *story-level* variable predicts a *neural* one — the exact shape of inference your chain needs. |
| **Dramatic irony** | Narratology | **Cabañas et al. 2023** (PMID 37469900) — "The audience who knew too much: investigating the role of spontaneous theory of mind on the processing of dramatic events". | **One study, but it is the right study.** Handle via `theory of mind` / `mentalizing`. |
| **Aesthetic appraisal** | Empirical aesthetics | **Hartung et al. 2021** (PMID 34916583) — aesthetic appraisals of literary style and emotional intensity in narrative engagement are *neurally dissociable*. | **Established, and the dissociation is useful**: it means "beautiful" and "moving" are separable readouts, which is a distinction directors make constantly. |
| **The cut / editing itself** | Film theory | **Drew et al. 2024** (PMID 38104604) — film editing and prediction processes; **Sanz-Aznar et al. 2023** (PMID 37521689) — ERP analysis of continuity edits across shot scales and camera angles; **Sanz-Aznar et al. 2025** (PMID 40678760) — spectator EEG frequency-domain analysis of the cut; **Zou et al. 2025** (PMID 40949345) — editing and viewer narrative cognition in VR film, eye-tracking. A 2025 *Frontiers* editorial (Andreu-Sánchez, PMID 41235172) collects the field under the name **neurocinematics**. | **This is your prior art for the first link in the chain** (technique → activation), and it is more developed than I expected. Shot scale and camera angle already have measured ERP signatures. |
| **Suspension of disbelief** | Narratology | **Loureiro et al. 2026** (PMID 42673853) — the Sd/B chronicity scale, psychometric development and validation. | **Scale exists as of this year; no imaging correlate yet.** |

The pattern across this table: **media psychology has the constructs and the scales; cognitive neuroscience has the ontologies and the images; neurocinematics is the small, growing field stitching them together.** Your crosswalk document is a contribution to that seam rather than a workaround for a missing tool.

---

## Sources

**Primary data pulled live (2026-09-02):**
1. [Cognitive Atlas API — concepts](https://www.cognitiveatlas.org/api/v-alpha/concept) — 918 concepts; also `/task` (857) and `/disorder` (221). Entity schema includes `concepts`, `contrasts`, `citations`, `conceptclasses`, `relationships`.
2. [Cognitive Atlas API documentation](https://www.cognitiveatlas.org/api) — endpoints, CC-BY-SA licence, NIMH-funded.
3. [CognitiveAtlas GitHub org](https://github.com/orgs/CognitiveAtlas/repositories) — `cogat-python` pushed 2024-07-10; `legacy_cogat_linkml` pushed 2025-02-20; `ontology` last pushed 2017.
4. [BrainMap behavioural domain taxonomy](https://brainmap.org/taxonomy/behaviors/) — full ~70-entry list; 5 top-level domains; site states BrainMap covers "20–30% of the compliant literature," each paper verified by a taxonomy expert.
5. [neurosynth-data repository file listing](https://github.com/neurosynth/neurosynth-data) — versions 3–7 with terms and LDA50/100/200/400 vocabularies. Last commit 2021-08-26.
6. [Neurosynth v7 term vocabulary](https://raw.githubusercontent.com/neurosynth/neurosynth-data/master/data-neurosynth_version-7_vocab-terms_vocabulary.txt) — 3,228 terms; 713 multi-word; 60 digit-initial. Absence of `suspense`/`narrative`/`surprise`/`agency`/`startle`/`vigilance`/`trust`/`film` verified by exact and substring match.
7. [Neurosynth v7 LDA100 topic keys](https://raw.githubusercontent.com/neurosynth/neurosynth-data/master/data-neurosynth_version-7_vocab-LDA100_keys.tsv) — 100 topics; topics 12, 25, 26, 30, 33, 49 identified as narrative, prediction-error, threat, affect, reward-anticipation, attention respectively.
8. [NeuroQuery data repository](https://github.com/neuroquery/neuroquery_data/tree/main/data) — vocab sizes 156,521 / 7,547 / 6,308 in filenames.
9. [NeuroQuery 6,308-term model vocabulary](https://raw.githubusercontent.com/neuroquery/neuroquery_data/main/data/data-neuroquery_version-1_vocab-neuroquery6308_vocabulary.txt).
10. [NeuroQuery term categories](https://raw.githubusercontent.com/neuroquery/neuroquery_data/main/data/data-neuroquery_version-1_termcategories.csv) — 39,755 rows: anatomy 17,461, disease 14,124, psychology 8,170 (4,809 unique normalised psychology terms; 1,604 of them in the 6,308 model vocab).
11. [neuroquery package](https://github.com/neuroquery/neuroquery) — release 1.1.0, 2025-08-23.
12. [NiMARE](https://github.com/neurostuff/NiMARE) — actively developed, last commit 2026-08-31.
13. [Neurosynth Compose](https://compose.neurosynth.org/) — live (HTTP 200); the successor platform.
14. [EBI OLS4 ontology index](https://www.ebi.ac.uk/ols4/api/ontologies) — MFOEM (Emotion Ontology) 624 terms, NBO 4,546 terms, both refreshed 2026-09-02; **CogPO is not indexed**.
15. [cogpo.org](http://www.cogpo.org/) — site live, PIs Laird & Turner, collaborators BrainMap / Cognitive Atlas / NeuroLex / NEMO.

**Literature (PubMed, via E-utilities):**
16. Turner JA, Laird AR (2012). *The Cognitive Paradigm Ontology: design and application.* Neuroinformatics. — CogPO's foundational paper; last substantive CogPO paper is Chakrabarti et al. 2014.
17. Peraza JA, Kent JD, Nichols TE, Poline JB, de la Vega A, Laird AR (2025). *NiCLIP: Neuroimaging contrastive language-image pretraining model for predicting text from brain activation images.* bioRxiv. [PMID 40661603](https://pubmed.ncbi.nlm.nih.gov/40661603/) — 23,000+ articles; best performance with full text **and a curated cognitive ontology**; degrades on subject-level maps.
18. Gillig A et al. (2025). *GINNA, a 33 resting-state networks atlas with meta-analytic decoding-based cognitive characterization.* Commun Biol. [PMID 39966659](https://pubmed.ncbi.nlm.nih.gov/39966659/) — cognitive terms synthesised into processes by expert consensus.
19. Wu G et al. (2024). *Unveiling the core functional networks of cognition: an ontology-guided machine learning approach.* [PMID 39173695](https://pubmed.ncbi.nlm.nih.gov/39173695/).
20. Bezdek MA, Gerrig RJ, Wenzel WG, Shin J, Pirog Revill K, Schumacher EH (2015). *Neural evidence that suspense narrows attentional focus.* Neuroscience. [PMID 26143014](https://pubmed.ncbi.nlm.nih.gov/26143014/).
21. Bezdek MA, Wenzel WG, Schumacher EH (2017). *The effect of visual and musical suspense on brain activation and memory during naturalistic viewing.* Biol Psychol. [PMID 28764896](https://pubmed.ncbi.nlm.nih.gov/28764896/).
22. Lehne M et al. (2014). *Tension-related activity in the orbitofrontal cortex and amygdala: an fMRI study with music.* [PMID 23974947](https://pubmed.ncbi.nlm.nih.gov/23974947/).
23. Baumgartner T et al. (2006). *Neural correlate of spatial presence in an arousing and noninteractive virtual reality: an EEG and psychophysiology study.* [PMID 16497116](https://pubmed.ncbi.nlm.nih.gov/16497116/).
24. Kober SE, Neuper C (2012). *Cortical correlate of spatial presence in 2D and 3D interactive virtual reality: an EEG study.* [PMID 22206906](https://pubmed.ncbi.nlm.nih.gov/22206906/).
25. Havranek M et al. (2012). *Perspective and agency during video gaming influences spatial presence experience and brain activation patterns.* [PMID 22812540](https://pubmed.ncbi.nlm.nih.gov/22812540/).
26. Schmälzle R et al. (2015). *Engaged listeners: shared neural processing of powerful political speeches.* [PMID 25653012](https://pubmed.ncbi.nlm.nih.gov/25653012/).
27. Imhof MA et al. (2017). *How real-life health messages engage our brains: shared processing of effective anti-alcohol videos.* [PMID 28402568](https://pubmed.ncbi.nlm.nih.gov/28402568/); and (2020) *Strong health messages increase audience brain coupling.* [PMID 31954843](https://pubmed.ncbi.nlm.nih.gov/31954843/).
28. Song H et al. (2021). *Neural signatures of attentional engagement during narratives and its consequences for event memory.* [PMID 34385312](https://pubmed.ncbi.nlm.nih.gov/34385312/).
29. Chang CHC et al. (2024). *How a speaker herds the audience: multi-brain neural convergence over time during naturalistic storytelling.* [PMID 37873125](https://pubmed.ncbi.nlm.nih.gov/37873125/).
30. Weber R, Hopp FR, Eden A, Fisher JT, Lee HE (2024). *Vicarious punishment of moral violations in naturalistic drama narratives predicts cortical synchronization.* NeuroImage. [PMID 38631616](https://pubmed.ncbi.nlm.nih.gov/38631616/).
31. Obando Yar A et al. (2025). *The science of story characters: a neuroimaging perspective on antagonists in narrative engagement.* [PMID 40458235](https://pubmed.ncbi.nlm.nih.gov/40458235/).
32. Cabañas C et al. (2023). *The audience who knew too much: investigating the role of spontaneous theory of mind on the processing of dramatic events.* [PMID 37469900](https://pubmed.ncbi.nlm.nih.gov/37469900/).
33. Hartung F et al. (2021). *Aesthetic appraisals of literary style and emotional intensity in narrative engagement are neurally dissociable.* [PMID 34916583](https://pubmed.ncbi.nlm.nih.gov/34916583/).
34. Drew A et al. (2024). *Perceptual oddities: assessing the relationship between film editing and prediction processes.* [PMID 38104604](https://pubmed.ncbi.nlm.nih.gov/38104604/).
35. Sanz-Aznar J et al. (2023). *Cinematographic continuity edits across shot scales and camera angles: an ERP analysis.* [PMID 37521689](https://pubmed.ncbi.nlm.nih.gov/37521689/); and (2025) *An exploration of the editing cut as an articulator in film through frequency domain analysis of spectator EEGs.* [PMID 40678760](https://pubmed.ncbi.nlm.nih.gov/40678760/).
36. Andreu-Sánchez C (2025). *Editorial: Neurocinematics: how the brain perceives audiovisuals.* [PMID 41235172](https://pubmed.ncbi.nlm.nih.gov/41235172/).
37. Zou Q et al. (2025). *The neural impact of editing on viewer narrative cognition in virtual reality films: eye-tracking insights.* [PMID 40949345](https://pubmed.ncbi.nlm.nih.gov/40949345/).
38. Dini H et al. (2023). *Exploring the neural processes behind narrative engagement: an EEG study.* [PMID 37460223](https://pubmed.ncbi.nlm.nih.gov/37460223/).
39. Türker B, Belloli L, Owen AM, Naci L, Sitt JD (2023). *Processing of the same narrative stimuli elicits common functional connectivity dynamics between individuals.* Sci Rep. [PMID 38040845](https://pubmed.ncbi.nlm.nih.gov/38040845/).
40. Loureiro F et al. (2026). *The suspension of dis/belief (Sd/B) chronicity scale: psychometric development and validation.* [PMID 42673853](https://pubmed.ncbi.nlm.nih.gov/42673853/).
