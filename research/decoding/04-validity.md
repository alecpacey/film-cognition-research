# How far can activation be read as cognition?

*Research note, 2 September 2026. Sources at foot. Where a number could not be verified from an accessible source in this session, it is marked UNVERIFIED rather than reported.*

## The bottom line

Reverse inference is not a fallacy — it is a legitimate Bayesian operation with a measurable, and usually poor, evidential yield. The best-quantified case in the literature is Broca's area implying language: starting from a prior of P(language) = 0.5, activation raises it to **P = 0.69**, a **Bayes factor of 2.3**, which by convention is *weak* evidence (Poldrack 2006, restated in Poldrack 2011). The strongest published case is ventral striatum implying reward, **BF = 9** (Ariely & Berns 2010), "moderately strong." Those are the ceiling, not the floor, and both are computed with an artificial 50% prior. Under a realistic prior — language is the topic of perhaps 15% of the fMRI corpus — the same Broca's evidence yields **P = 0.29**; under a 10% prior, **P = 0.20**. So: a single parcel lighting up licenses a *hypothesis*, never a claim. Two further numbers bound what is achievable. Meta-analytic term decoding across 25 broad psychological terms achieves **72% mean pairwise accuracy** against 50% chance, and cannot separate "executive" from "working memory" **at all** (Yarkoni et al. 2011). Whole-brain multivariate classification of *which of eight tasks a person is doing*, generalising across people, reaches **80% against 13% chance** (Poldrack, Halchenko & Hanson 2009). The honest position for this project: TRIBE-predicted parcel activation can support claims of the form *"this shot drives auditory association cortex and lateral occipital cortex more than the surrounding shots do"* — a **forward** statement about the stimulus-to-brain mapping. It cannot support *"this shot induces social inference"* as a finding. It can support that as a **labelled hypothesis carrying an asterisk**, which is exactly what Poldrack argues reverse inference is good for. One additional caution is specific to us and is, in my judgement, the sharpest single threat to the whole decoding step: meta-analytic term maps are biased by **experimental manipulation strength**, and film is a systematically weaker manipulation than the lab paradigms that populate the corpus (see Failure modes, §3).

## Reverse inference, quantified

**The formulation.** Poldrack (2006, 2011) frames it as Bayes' rule:

> P(M|A) = P(A|M)P(M) / [P(A|M)P(M) + P(A|¬M)P(¬M)]

The evidential yield is the ratio of posterior odds to prior odds — the Bayes factor. It is governed almost entirely by the **base rate of activation** in the region. Poldrack 2011: *"To the degree that the base rate of activation in the region is high (i.e., it is activated for many different mental processes), then activation in that region will provide little added evidence for engagement of a specific mental process."*

**Real posterior probabilities.**

| Inference | Bayes factor | P(M\|A) at prior 0.5 | at prior 0.15 | at prior 0.10 | Source |
|---|---|---|---|---|---|
| Broca's area → language | **2.3** | **0.69** | 0.29 | 0.20 | Poldrack 2006 (BrainMap, 749 studies) |
| Ventral striatum → reward | **9.0** | **0.90** | 0.61 | 0.50 | Ariely & Berns 2010 |

Poldrack's own gloss: *"Bayes factors below 4 are considered weak."* The single most-cited reverse inference in cognitive neuroscience falls below that line. The prior-0.15 and prior-0.10 columns are my recomputation from the published Bayes factors — the arithmetic is `posterior_odds = BF × prior_odds` — and they are the numbers that matter, because no real experiment has a 50% prior on any one cognitive process.

**Which regions can support it.** The empirical answer, from Poldrack 2011 Figure 1 (base rates of activation across the 3,489-article Neurosynth database of the time):

> *"What is striking is the degree to which some of the regions that are most common targets of informal reverse inference (e.g., anterior cingulate, anterior insula) have the highest base rates, and therefore are the least able to support strong reverse inferences."*

So **ACC, anterior insula, dlPFC are ruled out** — not because they are uninteresting but because they activate for nearly everything. The brief's assumption that dlPFC is non-selective is correct and is confirmed by Yarkoni et al. 2011: in the forward map, working memory's strongest associations are dlPFC, anterior insula and dorsomedial frontal cortex; in the **reverse** map those regions drop out and anterior PFC and posterior parietal cortex take their place. Several frontal regions that were *consistently* active for pain and emotion in forward analysis were associated with a **decreased** likelihood of the study being about pain or emotion in reverse analysis.

**Correction to the brief's premise: FFA and PPA are not in the safe column.** The brief lists "FFA for faces, PPA for places" as regions selective enough to support reverse inference. The decoding literature says otherwise. Hanson & Halchenko (2008, *Neural Computation*), whose title is "Brain reading using full brain support vector machines for object recognition: **there is no 'face' identification area**," trained whole-brain classifiers (40,000 voxels, single-TR) on 10 subjects and reached **97.4% median out-of-sample generalisation** for house-vs-face — and concluded: *"in contrast to the detection results common in this literature, neither the fusiform face area nor parahippocampal place area is shown to be uniquely diagnostic for faces or places, respectively."* Poldrack (2011) endorses this reading directly: *"neither the fusiform face area nor the parahippocampal place area is particularly diagnostic for the stimulus classes that activate them most strongly."*

The distinction that survives is **not** region-selectivity but **stimulus vs. cognition**. Early and mid-level visual cortex supports excellent decoding of *what was on the screen* — Kay et al. (2008) identified which specific novel natural image an observer viewed out of a large candidate set from V1–V3 receptive-field models. That is decoding a stimulus, not inferring a mental process. The moment the label becomes a cognitive noun ("attention," "empathy," "suspense"), the Poldrack arithmetic applies and the yield collapses.

**The dACC case study — the canonical demonstration that this goes wrong in print.** Lieberman & Eisenberger (2015, *PNAS*) titled a paper "The dorsal anterior cingulate cortex is **selective** for pain: Results from large-scale reverse inference," using Neurosynth (>10,000 studies) and reporting that *"'pain' was the top term for 6 out of 8 locations in the dACC."* Yarkoni — Neurosynth's author — demonstrated that the result is an artefact of ranking by **z-score** rather than effect size, and that ranking the same voxels by posterior probability inverts the conclusion (numbers in Failure modes, §1 and §6). Wager, Atlas, Botvinick, Chang, Coghill, Davis et al. published a formal PNAS reply, "Pain in the ACC?" (2016). The relevant lesson for us is not about pain: it is that a well-resourced lab, using the correct tool, on the most-studied region in the corpus, published a *selectivity* claim that did not survive contact with the tool's author.

## Where our parcels fall

Parcels are HCP-MMP1 (Glasser et al. 2016, 180 areas/hemisphere). Sorting is by the two criteria that actually govern evidential yield: **narrowness of tuning** and **base rate of activation**.

### Safe to interpret — but only as *stimulus content*, not as cognition

| Parcel | What can be said | What cannot |
|---|---|---|
| **A4, A5** (auditory association, downstream of A1→belt→PBelt) | "Structured auditory input is present and salient." Tuning is narrow at the modality level. | "Speech comprehension," "music," "dialogue processing." A4/A5 respond to speech, music, environmental sound and voice alike; the term you pick out of that set is a free parameter. |
| **LO2** (lateral occipital, MT+ complex neighbourhood) | "Object/shape structure is present." | "Object recognition" as a cognitive act, "identification," "familiarity." |
| **VMV2 / VMV3** (ventromedial visual, ventral stream, abutting parahippocampal areas) | "Ventral-stream, scene/place-biased visual input." | "Place recognition," "spatial memory," "context." This is PPA-adjacent territory, and PPA is explicitly named by Hanson & Halchenko and by Poldrack as **not** uniquely diagnostic for places. |

The rule for this row: the safe label is a **property of the shot**, not a state of the viewer. That is still useful — "shot X drives scene-biased ventral visual cortex more than shot Y" is a real, defensible, quantitative statement about cinematography — but it is forward inference dressed in parcel names.

### Do not interpret as a single cognitive label

| Parcel | Why not |
|---|---|
| **STSdp** (superior temporal sulcus, dorsal posterior) | The textbook many-to-one region. Posterior STS carries at least five separate literatures: biological motion, face/voice identity, audiovisual integration, theory of mind, and language. Any decoder will return whichever of those terms is best represented in its corpus, and the term will be *plausible* in all five cases. Base rate is high; tuning is not narrow. Treat any label here as unidentifiable. |
| **IPS1** (intraparietal sulcus 1, dorsal stream) | Retinotopic priority map, and a core node of the multiple-demand system. High base rate. Cannot be used to separate spatial attention from working memory from numerosity from saccade planning. |
| **FEF** (frontal eye field, premotor group) | Activates for covert attention shifts with or without eye movements. Two incompatible labels ("looking" vs "attending") are indistinguishable from the activation alone. Additionally, in a film paradigm eye movements are driven by the edit — so FEF activation is partly a *measurement of the stimulus*, not of the viewer's cognition. |
| **55b** | Special case: Glasser et al. verified it is *"strongly activated in the Story versus Baseline task contrast from the HCP's LANGUAGE task"* — genuinely language-selective, which makes it the most temptingly interpretable parcel in the set. But it is small, elongated, and *"bounded by the frontal eye field (FEF) and premotor eye field (PEF), primary motor cortex (4), ventral premotor cortex (6v), and prefrontal areas 8Av and 8C."* Its location varies substantially across individuals. **A one-parcel registration or alignment error turns "language" into "eye movements."** Given that FEF is *also* in our observed set, a 55b/FEF confusion is not hypothetical — it is the most likely single error in the readout. Do not report 55b as language without either an individual localiser or an explicit demonstration that the 55b and FEF timecourses dissociate. |

### The honest summary of this table

Of seven observed parcels, **zero** support a confident cognitive label from activation alone. Three (A4/A5, LO2, VMV2/3) support a confident **stimulus-content** label. Four (STSdp, IPS1, FEF, 55b) support neither without additional constraint.

## What decoding does and does not fix

**Does the Neurosynth association test solve reverse inference?** No. It **quantifies** it, and it does so in a units system that is easy to misread.

1. **The "association test" map is a two-way statistical test, not a probability.** Yarkoni et al. 2011 compute, per voxel, whether term frequency varies with activation frequency, FDR-corrected at q < 0.05, excluding voxels active in fewer than 3% of studies. What survives is *"voxels where there was significant evidence that term frequency varied with activation frequency."* That is a statement about **selectivity relative to the literature's own term distribution** — it is not P(cognition | activation) in any population you care about.

2. **The posterior probability maps use a hard-coded uniform 50% prior.** From the Yarkoni et al. methods, verbatim: *"For P(T_k=1) we impose a uniform prior for all terms, P(T_k=1)=P(T_k=0)=0.5."* Yarkoni's plain-English gloss: *"The strict interpretation of a posterior probability of 80% for pain in a dACC voxel is that, if we were to take 11,000 published fMRI studies and pretend that exactly 50% of them included the term 'pain' in their abstracts, the presence of activation in the voxel in question should increase our estimate of the likelihood of the term 'pain' occurring from 50% to 80%. If this seems rather weak, that's because it is."*

3. **What the headline numbers become under a real base rate.** A Neurosynth PP under a uniform prior implies a likelihood ratio LR = PP/(1−PP). Applying that LR to a realistic term prior gives:

| Neurosynth PP | Implied LR | Real posterior if term prior = 2% | = 5% | = 10% |
|---|---|---|---|---|
| 0.78 | 3.55 | **6.7%** | 15.7% | 28.3% |
| 0.80 | 4.00 | **7.5%** | 17.4% | 30.8% |
| 0.82 | 4.56 | **8.5%** | 19.3% | 33.6% |
| 0.85 | 5.67 | **10.4%** | 23.0% | 38.6% |
| 0.86 | 6.14 | **11.1%** | 24.4% | 40.6% |

An 85% posterior on a Neurosynth map is, for a term that appears in 2% of the literature, **about a 1-in-10 chance**. This table is my own arithmetic from the published likelihood-ratio identity; the input PPs are Yarkoni's real dACC values (§Failure modes 6).

4. **It does not fix terms-are-not-mental-states.** Yarkoni: *"Neurosynth can't directly tell us whether activation is specific to pain (or any other process), because terms in Neurosynth are just that — terms. They're not carefully assigned task labels, let alone actual mental states. […] It's something of a leap to go from words in abstracts to processes in people's heads."*

5. **It does not fix circularity.** Poldrack 2011: *"if researchers in the past tended to interpret activation in the anterior cingulate cortex as reflecting conflict based on informal reverse inference, then this will increase the support obtained from a literature-based meta-analysis for this reverse inference."* Literature-mined decoders partly re-measure the field's prior beliefs.

6. **It does not fix ontology.** Poldrack 2011: *"the ability to accurately decode mental states or functions is fundamentally limited by the accuracy of the ontology that describes those mental entities."* Yarkoni et al. found "executive" and "working memory" *"could not be distinguished at a rate different from chance."* If the target vocabulary contains near-synonyms, the decoder's choice between them is arbitrary.

**What decoding genuinely buys.** Real, and worth stating: it replaces an unquantified armchair guess with a **quantified association with characterised biases**, and it makes the inference auditable. Poldrack's own verdict: *"Viewed as a means to generate novel hypotheses, I think that reverse inference can be a very useful strategy, especially if it is based on real data (such as the meta-analytic maps from Yarkoni et al., 2011) rather than on an informal reading of the literature. […] The problem with this kind of reasoning arises when such hypotheses become reified as facts."*

**Better-suited alternatives to plain Neurosynth for our case.**
- **NeuroQuery** (Dockès, Poldrack, Primet, Gözükan, Yarkoni, Varoquaux et al., 2020, *eLife*) — 7,547 terms across 13,459 publications, and explicitly reframed: *"focusing on prediction rather than inference."* It handles rare terms and arbitrary-length text, which matters because cinematographic vocabulary is not in Neurosynth's term list. It also makes no significance claim, which is an honesty feature, not a bug.
- **GC-LDA topic decoding** (Rubin, Koyejo, Gorgolewski, Jones, Poldrack & Yarkoni, 2017, *PLoS Comput Biol*) — topic model over 11,000+ studies producing *"spatially-circumscribed topics"*, and Bayesian enough that priors can be seeded with images or text. Topics are less brittle than single terms.
- **Benchmark reality check:** Izuma (2026 preprint) benchmarked meta-analytic decoding directly and found it *"most informative for theoretically matched contrasts rather than single-condition maps, and for group maps rather than separate individual maps"*; *"Spatial smoothing offered little practical benefit"*; and, critically for us, *"when [competing process templates] overlapped, even high-quality maps supported multiple plausible interpretations."* His conclusion: MAD is *"Rather than serving as a direct readout of mental states […] most useful when applied to well-matched, well-estimated empirical maps and interpreted alongside theory, behavior, and self-report."* **This is a direct hit on our design.** A single shot's predicted activation is a single-condition map. The framework should decode **contrasts between matched shots** (close-up vs wide of the same scene; cut vs no-cut at matched content), not absolute maps per shot.

## Failure modes

**1. Term-frequency artefact — z-scores are evidence, not effect size.** Yarkoni: *"z-scores don't provide a measure of strength of effect, they provide (at best) a measure of strength of evidence. Pain has been extensively studied in the fMRI literature, so it's not terribly surprising if z-scores for pain are larger than z-scores for many other terms. […] Saying that dACC is specific to pain because it shows the strongest z-score is like saying that SSRIs are the only effective treatment for depression because a drug study with a sample size of 3,000 found a smaller p-value than a cognitive-behavioral therapy study of 100 people."* Any ranking of decoded terms by z or p is a ranking of **how well-funded the sub-literature is**. Rank by effect size or not at all.

**2. Base-rate problem.** Quantified in §What decoding does, item 3. An 80% Neurosynth PP becomes ~7.5% under a 2% term prior.

**3. Manipulation-strength confound — the one that most threatens this project.** Yarkoni, on why the pain map is inflated: *"pain is quite easy to robustly elicit in the scanner… you're pretty much guaranteed to produce the experience of pain… Contrast that with, say, emotion tasks. It's an open secret in much of emotion research that what passes for an 'emotional' stimulus is usually pretty benign… if we decide to meta-analytically compare brain activation during emotion with brain activation during pain, our results are necessarily going to be biased by differences in the relative strengths of the two kinds of experimental manipulation — **independently of any differences in the underlying neural substrates**."*

Applied to us: every term map in Neurosynth was built from **blocked or event-related lab paradigms with strong, isolated, repeated manipulations**. A film shot is a weak, continuous, multiply-confounded manipulation. Terms whose source literature used strong manipulations (pain, faces, motion, reward) will systematically outrank terms whose source literature used weak ones (empathy, suspense, social inference) **regardless of what the film is actually doing to the viewer**. Yarkoni: *"I'm not sure there's any good way to correct for this."* This is not a caveat to bury in a limitations paragraph; it predicts the *direction* of our results before we run them.

**4. Spatial smoothing and spatial autocorrelation.** Every similarity-based decoder ultimately correlates two brain maps. That operation is invalid under a naive null. Alexander-Bloch et al. (2018, *NeuroImage*, 773 citations) introduced the spherical-rotation ("spin test") null precisely because *"it remains unclear how one should test hypotheses focused on the overlap or spatial correspondence between two or more brain maps"* and the problem had been *"addressed with remarkable variability in terms of methodological approaches and statistical rigor."* Markello & Misic (2021, *NeuroImage*) benchmarked ten null frameworks and found *"naive null models that do not preserve spatial autocorrelation consistently yield unrealistically liberal statistical estimates."* If we correlate a TRIBE-predicted parcel map against Neurosynth term maps, **the correlation must be tested against a spatial-autocorrelation-preserving null (spin test or variogram-matched surrogates), or every term will look significant.** Note also Izuma's benchmark finding that additional spatial smoothing *"offered little practical benefit"* — smoothing does not rescue a decoder, it only makes maps look more alike.

**5. Statistical machinery producing confident false positives.** Eklund, Nichols & Knutsson (2016, *PNAS*), using 3 million random task group analyses on real resting-state data: *"For a nominal familywise error rate of 5%, the parametric statistical methods are shown to be conservative for voxelwise inference and **invalid for clusterwise inference**."* Their 2019 follow-up estimates *"at least 10% of the fMRI studies have used the most problematic cluster inference method (p = .01 cluster defining threshold)."* Bennett et al.'s dead-Atlantic-salmon demonstration (uncorrected fMRI yields "significant" task-related voxels in a dead fish) is the folk version of the same point; it remains a live methodological reference (see Thakral et al. 2024, "The dead salmon strikes again," which found 39% — 7 of 18 — of studies linking hippocampus to implicit memory did not report correcting for multiple comparisons). I could not retrieve the original Bennett et al. 2009 poster abstract from an indexed source in this session.

**6. Decoders return plausible-sounding words — the closest thing to a published demonstration.** There is no paper I could find that feeds pure noise to a meta-analytic decoder and shows it confidently labelling it. There is something nearly as damaging, and it is on the record. Yarkoni queried Neurosynth's posterior-probability rankings at four coordinates **inside a single region (dACC)**, a few millimetres apart:

| Coordinate (MNI) | Top decoded terms, with posterior probabilities |
|---|---|
| (0, 22, 26) | 'experiencing' **86%**, 'pain' **82%**, 'empathic' **81%** |
| (4, 10, 28) | 'aversive' **79%**, 'anxiety disorders' **79%**, 'conditioned' **78%** — *pain is far down the list, "hanging out with 'heart', 'skin conductance', and 'taste'"* |
| (−2, 30, 22) | 'abuse' **85%**, 'incentive delay' **84%**, 'nociceptive' **83%**, 'substance' **83%** |
| (0, 28, 16) | 'dysregulation' **84%**, 'heat' **83%**, 'happy faces' **82%** |

Every one of those labels is semantically coherent, confidently scored in the high 70s–80s, and **completely different from its neighbour a centimetre away**. "Abuse" at 85%. "Happy faces" at 82%. "Dysregulation" at 84%. A decoder handed a slightly mislocalised parcel does not fail loudly; it returns a different, equally fluent, equally confident story. That is the failure mode that will bite a film-technique pipeline, because parcel-level predictions from an encoding model carry exactly this kind of spatial uncertainty.

Yarkoni's second demonstration in the same post is arguably worse for a selectivity claim: at (−6, 8, 45) — the coordinate Lieberman & Eisenberger's own influential 2003 *Science* social-exclusion paper reported as dorsal ACC — *"the top hits in Neurosynth are 'SMA', 'motor', and 'supplementary motor'. If we scan down to the first cognitive terms, we find the terms 'task', 'execution', and 'orthographic'. 'Pain' is not significantly associated with activation at this location at all."*

**7. A > B does not imply ¬B.** Yarkoni: *"showing that dACC activation is greater for task A than task B (or even tasks B through Z) doesn't entail that the dACC is not also important for task B."* If our framework says close-ups drive STSdp more than wides do, that is not evidence that wides do not engage social processing.

## Prior art

**Naturalistic and movie fMRI, decoded.** The naturalistic-viewing field is large and well-established. Hasson, Nir, Levy, Fuhrmann & Malach (2004, *Science*, 1,237 citations) established intersubject correlation during free movie viewing, finding *"a striking level of voxel-by-voxel synchronization between individuals, not only in primary and secondary visual and auditory areas but also in association cortices,"* with ISC *"correlated with emotionally arousing scenes."* Hasson et al. (2008), "Neurocinematics: The Neuroscience of Film" (*Projections* 2(1), DOI 10.3167/proj.2008.020102) extended this to compare ISC across films of differing directorial control — this is the foundational technique-adjacent paper, and the one closest in spirit to our project. **UNVERIFIED:** the widely-quoted per-film ISC percentages (Hitchcock ≈65%, Leone ≈45%, *Curb Your Enthusiasm* ≈18%, unstructured park footage ≈5%) could not be confirmed from an accessible source in this session — *Projections* is behind Berghahn's paywall and both PNAS/PMC routes were blocked. Do not cite those figures until someone reads the PDF. Nastase, Gazzola, Hasson & Keysers (2019, *SCAN*) is the current methods reference for ISC.

Stimulus-level decoding from naturalistic viewing is solved-ish and long-standing: Kay et al. (2008) identified specific novel natural images from V1–V3 receptive-field models; Poldrack (2011) reviews the Naselaris and Mitchell model-based reconstruction line. Closest to film specifically: de Borst, Valente, Jääskeläinen & Tikka (2016, *NeuroImage*) used MVPA to decode, from professional cinematographers and sound designers, *"whether they were imagining sounds or images of particular film clips"* and *"successfully decode the implicit presence of film genre from brain activity during mental imagery in cinematographers."* That is decoding of film-related content — from imagery, in experts — not decoding of viewing into cognitive terms.

**Technique-to-neural-response: exists, is mostly EEG/ERP, and does not go through meta-analytic decoding.** There is a real and growing literature linking specific cinematographic operations to neural measures:

- Heimann, Uithol, Calbi, Umiltà, Guerra & Gallese (2017, *Cognitive Science*), "'Cuts in Action': A High-Density EEG Study Investigating the Neural Correlates of Different Editing Techniques in Film."
- Heimann et al. (2019, *PLoS ONE*), "Embodying the camera: An EEG study on the effect of camera movements on film spectators' sensorimotor cortex activation."
- Sanz-Aznar, Sánchez-Gómez, Bruni, Aguilar-Paredes et al. (2021, *PLoS ONE*), "Neural responses to shot changes by cut in cinematographic editing: An EEG (ERD/ERS) study."
- Sanz-Aznar, Bruni & Soto-Faraco (2023, *Front. Neurosci.*), "Cinematographic continuity edits across shot scales and camera angles: an ERP analysis."
- Drew & Soto-Faraco (2024, *Phil. Trans. R. Soc. B*), "Perceptual oddities: assessing the relationship between film editing and prediction processes" — frames editing within predictive processing.
- Magliano & Zacks (2011, *Cognitive Science*), "The impact of continuity editing in narrative film on event segmentation" (102 citations) — the behavioural/event-segmentation anchor.
- Cao, Wang, Wu, Xie, Shi, Zhong & Wang (2024, *PLoS ONE*), "Reexamining the Kuleshov effect: Behavioral and neural evidence from authentic film experiments" — fMRI, montage/POV editing.
- Cabañas, Senju & Smith (2023, *Front. Psychol.*) on dramatic irony and spontaneous theory of mind in film.
- Tikka, Kaipainen & Salmi (2023, *Neuropsychologia*), "Narrative simulation of social experiences in naturalistic context — A neurocinematic approach."
- VR-specific: Tian et al. (2021, *Sensors*); Cheng et al. (2023, *Sensors*); Zou et al. (2025, *Front. Psychol.*).
- Andreu-Sánchez, Martín-Pascual & Delgado-García (2025, *Front. Neurosci.*) edited a whole research topic, "Neurocinematics: how the brain perceives audiovisuals."

So: **technique → neural response is established prior art.** It is almost entirely EEG/ERP or targeted fMRI contrasts, it uses hand-picked hypotheses (does a cut produce prediction error? does a camera move recruit sensorimotor cortex?), and it interprets results by forward inference from a chosen hypothesis, not by open-vocabulary decoding.

**Technique → decoded cognitive states: I could not find it, and I think it does not exist.** Searches run against Europe PMC (full-text over the PMC corpus, not just abstracts):

| Query | Hits |
|---|---|
| `("cinematographic" OR "cinematography" OR "film technique") AND "Neurosynth"`, full text | **0** |
| `("movie" OR "film" OR "naturalistic viewing") AND "Neurosynth" AND ("functional decoding" OR "meta-analytic decoding")`, full text | **0** |
| `"naturalistic" AND "Neurosynth" AND "decoding" AND "movie"`, full text | 3 — all conference-abstract compilations (BNA 2025 Festival, ACNP 2023/2024 poster books), i.e. incidental co-occurrence, no matching paper |
| `"naturalistic" AND "Neurosynth" AND "decoded"`, full text, 2018–2026 | 1 — an ACNP poster-abstract compilation |
| `ABSTRACT:"annotation" AND "movie" AND "fMRI" AND ("cognitive states" OR "decoding")` | **0** |
| `ABSTRACT:"movie"/"film"/"naturalistic viewing" AND ABSTRACT:"Neurosynth"` | 1 — Pacella et al. 2024 *Nat. Commun.*, a Neurosynth-derived "morphospace of brain-cognition organisation," unrelated to film |

**Statement for the record:** as of 2 September 2026, I found no published work that (a) takes naturalistic film viewing, (b) decodes the resulting cortical activation into cognitive terms via meta-analytic decoding, and (c) links those decoded terms to specific cinematographic technique. The three ingredients each exist. The composition does not appear in the indexed literature. **That is a defensible novelty claim** — with the caveat that Europe PMC's full-text index covers the PMC open-access corpus, not every venue (film-studies journals such as *Projections*, and much of the HCI/media literature, are outside it), and that the negative was established by keyword search, so an equivalent study using different vocabulary ("functional characterisation," "term-based annotation," "cognitive atlas") could have been missed.

**Caveat on the novelty claim's value.** The gap may be partly a gap of *demand* rather than a gap of *opportunity*. Every one of the failure modes above — manipulation-strength bias in particular — bears on exactly this composition, and the people best placed to build it (Poldrack, Yarkoni, Hasson, Nastase) are also the people who wrote the critiques. It is worth treating "nobody has done it" as a question to answer rather than as an unmitigated selling point.

## Sources

**Reverse inference, foundations**
1. [Poldrack RA (2006), "Can cognitive processes be inferred from neuroimaging data?" *Trends in Cognitive Sciences*](https://europepmc.org/article/MED/16406760) — PMID 16406760, 1,062 citations. Original Bayesian formulation; the Broca's/language BF = 2.3 analysis over BrainMap.
2. [Poldrack RA (2011), "Inferring mental states from neuroimaging data: from reverse inference to large-scale decoding," *Neuron*](https://europepmc.org/article/MED/22153367) — PMID 22153367, PMC3240863 (full text retrieved), 488 citations. Restates the 0.69/BF 2.3 figure and Ariely & Berns BF = 9; the ACC/anterior-insula base-rate point; the FFA/PPA non-diagnosticity point; the Kahneman "drop the asterisk" warning.
3. [Poldrack RA, Halchenko YO & Hanson SJ (2009), "Decoding the large-scale structure of brain function by classifying mental states across individuals," *Psychological Science*](https://europepmc.org/article/MED/19883493) — PMC2935493. 80% cross-individual classification, chance = 13%.

**Meta-analytic decoding**
4. [Yarkoni T, Poldrack RA, Nichols TE, Van Essen DC & Wager TD (2011), "Large-scale automated synthesis of human functional neuroimaging data," *Nature Methods*](https://europepmc.org/article/MED/21706013) — PMID 21706013, PMC3146590 (full text retrieved), 3,065 citations. 72% mean pairwise accuracy over 25 terms; pain pairwise > 74%; "executive" vs "working memory" at chance; uniform 0.5 prior stated in Methods; FDR q < 0.05, 3%-of-studies voxel exclusion.
5. [Yarkoni T (2015), "No, the dorsal anterior cingulate is not selective for pain: comment on Lieberman and Eisenberger (2015)"](https://www.talyarkoni.org/blog/2015/12/05/no-the-dorsal-anterior-cingulate-is-not-selective-for-pain-comment-on-lieberman-and-eisenberger-2015/) — full text retrieved. Source of the four-coordinate posterior-probability table, the "pretend 50% of 11,000 studies" gloss, the z-score/effect-size argument, and the manipulation-strength bias argument. Not peer-reviewed; written by Neurosynth's author; the peer-reviewed counterpart is source 7.
6. [Lieberman MD & Eisenberger NI (2015), "The dorsal anterior cingulate cortex is selective for pain: Results from large-scale reverse inference," *PNAS*](https://europepmc.org/article/MED/26582792) — PMC4679028. Abstract retrieved; full text blocked by CAPTCHA/paywall. The "6 out of 8 locations" figure is quoted via source 5.
7. [Wager TD, Atlas LY, Botvinick MM, Chang LJ, Coghill RC, Davis KD et al. (2016), "Pain in the ACC?" *PNAS*](https://europepmc.org/article/MED/27095849) — PMC4983860. Formal reply. **Full text not retrieved** (PNAS Cloudflare, PMC CAPTCHA, no OAI record) — cited as existing, not quoted.
8. [Dockès J, Poldrack RA, Primet R, Gözükan H, Yarkoni T, Suchanek F, Thirion B & Varoquaux G (2020), "NeuroQuery, comprehensive meta-analysis of human brain mapping," *eLife*](https://europepmc.org/article/MED/32255425) — PMC7164961, 158 citations. 7,547 terms, 13,459 publications, prediction-not-inference framing.
9. [Rubin TN, Koyejo O, Gorgolewski KJ, Jones MN, Poldrack RA & Yarkoni T (2017), "Decoding brain activity using a large-scale probabilistic functional-anatomical atlas of human cognition," *PLoS Computational Biology*](https://europepmc.org/article/MED/29059185) — PMC5683652, 109 citations. GC-LDA topic decoding.
10. [Izuma K (2026), "From brain maps to mental processes: Benchmarking meta-analytic decoding for psychological inference"](https://doi.org/10.31234/osf.io/w9csv_v1) — PsyArXiv preprint, **not peer-reviewed**. The matched-contrast / overlapping-template findings.
11. [Peraza JA, Kent JD, Nichols TE, Poline J-B, de la Vega A et al. (2025), "NiCLIP: Neuroimaging contrastive language-image pretraining model for predicting text from brain activation images"](https://europepmc.org/search?query=NiCLIP) — preprint, not peer-reviewed. CLIP-style decoder trained on 23,000+ articles; worth watching as a successor to term-based decoding.

**Selectivity of specific regions**
12. [Hanson SJ & Halchenko YO (2008), "Brain reading using full brain support vector machines for object recognition: there is no 'face' identification area," *Neural Computation*](https://europepmc.org/article/MED/17919083) — 72 citations. 97.4% median out-of-sample house/face generalisation; FFA and PPA not uniquely diagnostic.
13. [Kay KN, Naselaris T, Prenger RJ & Gallant JL (2008), "Identifying natural images from human brain activity," *Nature*](https://europepmc.org/article/MED/18337721) — PMC3556484. Stimulus identification from V1–V3 receptive-field models.
14. [Glasser MF, Coalson TS, Robinson EC, Hacker CD, Harwell J, Yacoub E, Ugurbil K, Andersson J, Beckmann CF, Jenkinson M, Smith SM & Van Essen DC (2016), "A multi-modal parcellation of human cerebral cortex," *Nature*](https://europepmc.org/article/MED/27437579) — PMC4990127 (full text retrieved). Source of the HCP-MMP1 parcellation and the verified 55b description (Story-vs-Baseline LANGUAGE selectivity; bounded by FEF, PEF, area 4, 6v, 8Av, 8C).

**Statistical validity of map comparison**
15. [Alexander-Bloch AF, Shou H, Liu S, Satterthwaite TD, Glahn DC, Shinohara RT, Vandekar SN & Raznahan A (2018), "On testing for spatial correspondence between maps of human brain structure and function," *NeuroImage*](https://europepmc.org/article/MED/29708908) — PMC6095687, 773 citations. The spin test.
16. [Markello RD & Misic B (2021), "Comparing spatial null models for brain maps," *NeuroImage*](https://europepmc.org/article/MED/34239992) — 355 citations. Ten null frameworks benchmarked; naive nulls "consistently yield unrealistically liberal statistical estimates." *(FWER figures from the results section not retrieved — SciDirect and bioRxiv both blocked.)*
17. [Eklund A, Nichols TE & Knutsson H (2016), "Cluster failure: Why fMRI inferences for spatial extent have inflated false-positive rates," *PNAS*](https://europepmc.org/article/MED/27357684) — PMC4948312. 3 million random group analyses; parametric clusterwise inference invalid at nominal FWE 5%.
18. [Eklund A, Knutsson H & Nichols TE (2019), "Cluster failure revisited," *Human Brain Mapping*](https://europepmc.org/article/MED/30618098) — PMC6445744, 59 citations. "At least 10% of the fMRI studies have used the most problematic cluster inference method."
19. [Thakral PP, Cutting ER & Lawless KE (2024), "The dead salmon strikes again," *Cognitive Neuroscience*](https://europepmc.org/article/MED/38700252) — 39% (7/18) of hippocampus-implicit-memory studies did not report multiple-comparison correction.

**Naturalistic viewing and film**
20. [Hasson U, Nir Y, Levy I, Fuhrmann G & Malach R (2004), "Intersubject synchronization of cortical activity during natural vision," *Science*](https://europepmc.org/article/MED/15016991) — 1,237 citations.
21. Hasson U, Landesman O, Knappmeyer B, Vallines I, Rubin N & Heeger DJ (2008), "Neurocinematics: The Neuroscience of Film," *Projections* 2(1):1–26 — [DOI 10.3167/proj.2008.020102](https://doi.org/10.3167/proj.2008.020102). **Full text not retrieved; per-film ISC percentages UNVERIFIED.**
22. [Nastase SA, Gazzola V, Hasson U & Keysers C (2019), "Measuring shared responses across subjects using intersubject correlation," *SCAN*](https://europepmc.org/article/MED/31099394) — PMC6688448, 365 citations. Current ISC methods reference.
23. [de Borst AW, Valente G, Jääskeläinen IP & Tikka P (2016), "Brain-based decoding of mentally imagined film clips and sounds reveals experience-based information patterns in film professionals," *NeuroImage*](https://doi.org/10.1016/j.neuroimage.2016.01.043).
24. [Heimann K, Uithol S, Calbi M, Umiltà MA, Guerra M & Gallese V (2017), "'Cuts in Action': A High-Density EEG Study Investigating the Neural Correlates of Different Editing Techniques in Film," *Cognitive Science*](https://europepmc.org/article/MED/27882594).
25. [Heimann K, Uithol S, Calbi M, Umiltà MA, Guerra M, Fingerhut J & Gallese V (2019), "Embodying the camera: An EEG study on the effect of camera movements on film spectators' sensorimotor cortex activation," *PLoS ONE*](https://europepmc.org/article/MED/30865624) — PMC6415856.
26. [Magliano JP & Zacks JM (2011), "The impact of continuity editing in narrative film on event segmentation," *Cognitive Science*](https://europepmc.org/article/MED/21972849) — PMC3208769, 102 citations.
27. [Sanz-Aznar J, Sánchez-Gómez L, Bruni LE, Aguilar-Paredes A et al. (2021), "Neural responses to shot changes by cut in cinematographic editing: An EEG (ERD/ERS) study," *PLoS ONE*](https://europepmc.org/article/MED/34637462) — PMC8516196.
28. [Sanz-Aznar J, Bruni LE & Soto-Faraco S (2023), "Cinematographic continuity edits across shot scales and camera angles: an ERP analysis," *Frontiers in Neuroscience*](https://europepmc.org/article/MED/37521689) — PMC10375706.
29. [Drew A & Soto-Faraco S (2024), "Perceptual oddities: assessing the relationship between film editing and prediction processes," *Phil. Trans. R. Soc. B*](https://europepmc.org/article/MED/38104604) — PMC10725757.
30. [Cao Z, Wang Y, Wu L, Xie Y, Shi Z, Zhong Y & Wang Y (2024), "Reexamining the Kuleshov effect: Behavioral and neural evidence from authentic film experiments," *PLoS ONE*](https://europepmc.org/article/MED/39106248) — PMC11299807.
31. [Cabañas C, Senju A & Smith TJ (2023), "The audience who knew too much: investigating the role of spontaneous theory of mind on the processing of dramatic irony scenes in film," *Frontiers in Psychology*](https://europepmc.org/article/MED/37469900) — PMC10353302.
32. [Tikka P, Kaipainen M & Salmi J (2023), "Narrative simulation of social experiences in naturalistic context — A neurocinematic approach," *Neuropsychologia*](https://europepmc.org/article/MED/37507066).
33. [Andreu-Sánchez C, Martín-Pascual MÁ & Delgado-García JM (2025), "Editorial: Neurocinematics: how the brain perceives audiovisuals," *Frontiers in Neuroscience*](https://europepmc.org/article/MED/41235172) — PMC12610406.

### Method note

Searches were run against the Europe PMC REST API and the NCBI PMC OAI service after this session's WebSearch budget (200/200) was exhausted; full texts were extracted from PMC OAI records where open access permitted. PNAS, ScienceDirect, bioRxiv and Berghahn were blocked (Cloudflare / CAPTCHA / paywall) and the items sourced from them are marked. All posterior-probability recomputations in §"What decoding does and does not fix" item 3 and in the §"Reverse inference, quantified" table (prior-0.15 and prior-0.10 columns) are my own arithmetic from published Bayes factors and likelihood ratios, not values quoted from the papers.
