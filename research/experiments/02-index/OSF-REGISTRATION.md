# OSF registration draft — stage 02, the observational index

**Prepared 5 September 2026, before any stage-02 analysis.**
Template: **OSF Preregistration** (form v1). Field numbers match the form's items.

Paste each block into the matching field. Nothing here is new: every figure is
carried from `README.md`, `DIALS.md`, `CORPUS.md` or `../../PAPER.md`, all of which
were written before the run they describe. **Do not soften anything below after
submission** — an OSF registration is immutable, and changes go through the formal
Update process with a documented justification.

---

## 1 · Study Information

### item_1 · Title

> A technique→response index for cinematography, measured through a brain encoding
> model — Stage 02: the observational index

### item_2 · Authors

> Alec Pacey (independent researcher).
>
> Sole author. No funder. No institutional affiliation. Analysis and writing were
> assisted by a large language model acting under instruction; all design decisions,
> pre-registered criteria and interpretations are the author's.

### item_3 · Description

> Film craft is taught as a set of dials — cut rate, shot scale, lighting key, camera
> movement, colour — but the relation between those dials and a viewer's neural
> response is documented only piecemeal, one dial at a time, in studies that rarely
> share a stimulus set or an analysis. This programme asks whether that relation can
> be measured systematically enough to be inverted: given a target cortical response
> profile, choose the technique that reaches it.
>
> The instrument is TRIBE (Meta AI, winner of the Algonauts 2025 challenge), a
> trimodal encoding model predicting whole-cortex fMRI response from video, audio and
> text. **The dependent variable is a model's prediction of cortex, not cortex.**
> This scope condition is stated at the outset and never relaxed; it is quantified in
> item_14 and item_25.
>
> Two stages are complete and reported against criteria fixed in advance. Stage 00
> established that the sensor discriminates content (mean pairwise top-10 Jaccard
> overlap 0.15 against a pre-registered threshold of 0.60, with a reciprocal double
> dissociation between the voice and place chains). Stage 01 established that
> technique moves the sensor with content held constant (intercutting two fixed 60 s
> scenes at five rates moved 51 of 180 parcels to |r| > 0.9 against log cut count,
> against a pre-registered bar of 15 and a chance expectation of ~7).
>
> **This registration covers Stage 02 only:** the observational index, which
> regresses parcel-level response on measured cinematographic dials across segments
> of real cinema. Its analysis has not been run.

### item_4 · Hypotheses

> **H2.** Across real cinema, measured technique dials predict parcel-level response
> profiles, recoverably by penalised regression.
>
> **H2b.** The controlled cut-rate result of stage 01 reappears observationally — the
> inferior-frontal cluster (IFJa, IFJp, IFSp, 8C) associates with cut rate here too.
>
> H2b is the only place in the design where the controlled and observational tracks
> can contradict each other. If cut rate moves the sensor on identical footage but
> shows no association across real cinema, one of the two results is wrong and must
> be resolved before anything is built on either. That outcome is named PARTIAL in
> item_21 and is treated as the most important possible finding, not as a failure.
>
> **Directional predictions are deliberately absent for the other twelve dials.**
> Stage 01's strongest responders were inferior-frontal rather than the
> dorsal-attention network the literature predicted; that reading is coherent (every
> cut is a task switch) but post-hoc, and is carried into stage 02 as a hypothesis to
> be tested, not as a finding to be confirmed.

---

## 2 · Design Plan

### item_5 · Study type

> Observational. A cross-sectional regression across film segments, with no
> manipulation and no human participants. No experimental intervention is applied to
> any organism; the "response" is a deterministic model prediction.

### item_6 · Blinding

> No human or animal participants, so participant blinding does not apply.
>
> **Analyst blinding does apply and is the central procedural control of this study.**
> At the time of this registration the analysis team has not inspected any
> dial→parcel relationship, and the file holding the response data
> (`parcel_vectors.json`) has not been opened for analysis. See item_7 and item_11.

### item_7 · Additional blinding details

> The no-peeking protocol was written into `02-index/README.md` before collection
> began, and is reproduced here in full force:
>
> 1. The statistical test in item_21 is run **once, on the complete set of 70
>    segments.**
> 2. Between-batch checks verify **pipeline health only**: 180 parcels per clip, no
>    NaN, no |z| > 8, and filenames aligning between the dial table and the parcel
>    table. For completeness, the batch-0 check also computed pairwise whole-vector
>    correlations between four clips, to confirm the sensor discriminates at all
>    rather than returning one vector for everything. **None of these quantities is a
>    dial→parcel relationship**, so none is an outcome peek.
> 3. Interim looks are exploratory by construction, and anything seen in one may not
>    be reported as a finding.
> 4. One pre-specified exception exists and is a resource decision rather than a
>    test: see item_15.

### item_8 · Study design

> Three public-domain live-action Technicolor features were cut into fixed,
> non-overlapping 60-second segments, yielding **244 segments** (Jungle Book 95,
> Nothing Sacred 66, Royal Wedding 83). Head and tail of each film are skipped, 5%
> each end.
>
> **Corpus:** *Nothing Sacred* (Wellman, 1937), *Jungle Book* (Korda, 1942), *Royal
> Wedding* (Donen, 1951). Different directors on purpose. Directors covary their
> dials deliberately — fast cutting arrives with camera movement and high contrast,
> close-ups with shallow focus — so within a single film the dials are confounded by
> intent. Varying the director is the cheapest way to break that covariance without a
> lab.
>
> Two earlier corpus choices were rejected on evidence and both rejections are part
> of the record. *His Girl Friday* (1940) was rejected for being black and white,
> which would have made saturation a perfect proxy for film identity. An
> animated-Technicolor corpus was then adopted as an explicit working assumption and
> subsequently dropped: its availability premise proved false (six public-domain
> live-action Technicolor features verified against two animated colour features),
> and, more importantly, Gruber et al. (2024) selected animated films *because* they
> are "stylistically and thematically similar" — a deliberate minimum-variance
> condition, which is the opposite of what a corpus assembled to break dial
> covariance requires.
>
> **Colour was verified by measurement, not provenance.** A documented Technicolor
> production can reach an archive as a black-and-white dupe, and a pixel format proves
> nothing. Twelve frames per print across the middle 90% of running time gave mean HSV
> saturation 81.9 / 85.5 / 115.6 against a threshold of 15, and chroma 10.5 / 16.3 /
> 14.6 against a threshold of 3. All three prints clear by a wide margin.
>
> **Encode normalisation.** The verified prints spanned 640×480 to 1480×1080 with
> differing audio codecs. The depth-of-field dial is a centre-versus-surround
> sharpness ratio, and colour and contrast statistics move with encode quality;
> within-film centring removes a per-film mean but not a resolution-dependent
> difference in a dial's *variance*. Every segment is therefore re-encoded identically
> before any dial is measured — 720-line height, Lanczos, libx264 CRF 20, `yuv420p`,
> AAC 128 kbps 48 kHz stereo. Segments are re-encoded rather than stream-copied,
> because a stream copy begins at the nearest keyframe and silently yields a short
> clip, which is the failure mode that returns confident noise.
>
> **Segmentation is fixed 60 s rather than shot-aligned**, for three reasons in order
> of weight. (a) The unit of analysis is the segment, not the timepoint: a scene
> change inside a segment is measured by the cut-rate dial, and both sides of the
> regression see the same 60 seconds. (b) Given a nested cortical hierarchy of neural
> state durations (Baldassano 2017; Geerligs 2022), no event-aligned segmentation is
> correct for all 180 parcels. (c) TRIBE has a ~30 s floor and a 100 s training
> window; fixed 60 s sits inside that band, whereas shot-aligned windows vary and some
> would land near the floor, where the model returns diffuse output without erroring.

### item_9 · Randomization

> **No randomization.** Segments are not assigned to conditions; there are no
> conditions.
>
> The 70 segments scored are chosen from the 244 by **stratified maximin sampling on
> predictors**: stratify on cut rate within each film, then within each stratum take
> the segment whose standardised dial vector is farthest from those already selected.
> This spreads every dial rather than only the stratifying one, and retains 83–100%
> of each dial's full range.
>
> This is a design choice on predictors, made before any response value existed.
> Selecting on outcomes would be p-hacking; selecting on stimulus properties is
> ordinary experimental design. **The genuine caveat is different and is registered
> here in advance:** deliberately spreading a dial inflates its variance relative to a
> random sample, so estimates are **design-conditional** and must not be read as "the
> effect in typical cinema". Stratifying across quantiles rather than taking extreme
> groups keeps that mild.

---

## 3 · Sampling Plan

### item_10 · Existing data

> ☑ **Registration prior to analysis of the data.**

### item_11 · Explanation of existing data

> **This registration is filed after data collection and before any analysis.
> It is declared as such, not presented as prospective.**
>
> **VERIFY THIS COUNT IMMEDIATELY BEFORE SUBMITTING** — run
> `python run_batch.py --plan`, which prints `selected / scored / pending`, and set
> the number below to what it reports. As of 7 September 2026, 11:50, collection
> stood at **66 of 70 scored, 4 in flight**.
>
> All 70 selected segments have been scored by the pipeline in item_12. The response
> data is stored in `research/experiments/02-index/parcel_vectors.json` and, per clip,
> in the Hugging Face dataset `alecnpacey/tribe-probe-results`.
>
> **No analysis of that data has been performed.** Specifically:
>
> - No dial→parcel relationship has been computed, inspected, or estimated, by any
>   means, at any point.
> - **No elastic net has been fitted to the response data. No permutation null has
>   been run.** The pre-registered futility script `futility_check.py` exists in the
>   repository but **has never been executed** — see item_15.
> - The only quantities inspected from the scored clips are pipeline-health checks:
>   parcel count (must be 180), NaN presence, z-magnitude (must be |z| ≤ 8), absence
>   of stray keys, per-film segment counts, and, at batch 0, one between-clip
>   whole-vector correlation confirming the sensor does not return an identical vector
>   for every input. None of these is a dial→parcel relationship.
>
> **The stimulus side was fully measured before any segment was scored.** All 244
> segments were cut, normalised and dialled; the detectability classification and
> collinearity diagnostics were computed; and the 70-segment selection was fixed and
> written to `selection.json`. Those quantities appear in item_14, item_18 and item_25.
>
> **The pre-registered criteria have not changed during collection, and this is
> verifiable.** `02-index/README.md`, `02-index/DIALS.md`, `02-index/CORPUS.md` and
> `selection.json` are byte-identical between commit
> `89d01a1b693154bfd54ac443c70899d8a75b1dea` (5 September 2026, when 13 of 70 had been
> scored) and the commit accompanying this registration. Fifty-three further segments
> were scored between those two commits and not one threshold, pass criterion, sample
> size or model specification moved.
>
> **One mid-collection change to the scoring environment, and the check it triggered.**
> The Space application was patched partway through collection so that each clip's
> result is written to a durable dataset repository rather than recovered from a log
> stream. The pre-registration (item_22) states that clips scored under a different
> configuration must be discarded and rescored, because mixing two scoring
> configurations in one dataset is a silent confound. The patch was therefore tested
> rather than assumed: `royal_wedding_013`, already banked under the unpatched
> application, was rescored under the patched one and compared parcel by parcel.
> Result: same 180 keys, maximum |Δz| = 5.0 × 10⁻⁷, whole-vector correlation
> 0.999999999999961, i.e. identical to floating-point noise. **The scoring path is
> unchanged and the dataset is homogeneous.** Evidence in `identity_test.py` and
> `identity_test_result.json`.
>
> **Why this was not filed before collection began.** Candidly: the author had not
> registered a study before, and the pre-registration existed only as documents in a
> private repository. The criteria themselves were fixed in advance and demonstrably
> have not been altered — the record shows the sample size being *raised* on
> measurement (60 → 70, item_14) rather than a threshold being lowered. Filing after
> collection is a weaker position than a fully prospective registration and is reported
> as such rather than dressed up as one. What it does establish, and what the commit
> history supports, is that **the analysis plan was fixed before the analysis was
> run.**

### item_12 · Data collection procedures

> Each selected segment is uploaded to a duplicated Hugging Face Space
> (`alecnpacey/tribe-probe`) running on A10G Small hardware at $1.00/hr, roughly
> $0.17 per 60-second segment.
>
> The Space's reference environment is used — its `tribev2` fork, pinned transformers,
> patches and windowing — but its interactive interface is replaced, so the modules
> are driven directly rather than through a UI. Inference runs in video mode with
> `audio_only=True`, which skips ASR and the gated Llama-3.2-3B text branch; the model
> tolerates the missing text modality through modality dropout. **All results are
> therefore video + audio only, with no text branch.**
>
> Output is exactly 1 Hz (61 rows per 60 s clip) across 20,484 fsaverage5 vertices,
> reduced to 181 HCP parcels of which index 0 is `???` and is dropped, leaving **180
> usable parcels** per segment. Throughput is ~10 minutes per 60-second clip.
>
> The model is deterministic: the released checkpoint has no subject-specific
> parameters, predictions are identical whoever is nominally watching, and an
> independent re-run in stage 00 reproduced parcel values to two decimal places.
>
> Collection runs in resumable batches. Each clip is a checkpoint — the Space prints
> its 180 parcel values to stdout on completion — so a batch that dies half-way still
> banks its completed clips. Resume is by omission: only segments with no saved vector
> are uploaded, so nothing is scored twice. Candidates are drawn from `selection.json`
> and the runner refuses to start without it, so the pre-registered stratified design
> cannot be bypassed by convenience sampling.

### item_13 · Sample size

> **70 segments**: Jungle Book 24, Nothing Sacred 23, Royal Wedding 23.
>
> Drawn from 244 available segments, all of which are cut and dialled.

### item_14 · Sample size rationale

> **The smallest effect size of interest is derived, not asserted**, following Lakens'
> requirement that a SESOI be justified. The justification is the measurement chain.
>
> Parcel values are not brain data; they are TRIBE's predictions of brain data, and
> the link from those predictions to real cortex is published: mean Pearson
> **r = 0.3195 in-distribution** (Friends s7) and **r = 0.2146 out-of-distribution**,
> or 0.54 normalised against the noise ceiling. **This corpus is out of distribution**
> — 1937–1951 Technicolor features are not *Friends*, and are arguably further out
> than the challenge's own OOD films — so 0.2146 is an optimistic upper bound.
>
> If a dial correlates with a parcel prediction at r_DP, and that parcel tracks real
> BOLD at r_PY, the dial's implied association with real cortex is approximately
> r_DP × r_PY. To imply even a conventionally small real effect of r = 0.10:
>
> | via | r_PY | required r_DP |
> |---|---|---|
> | raw out-of-distribution accuracy | 0.2146 | **0.47** |
> | noise-ceiling-normalised accuracy | 0.54 | 0.19 |
>
> **SESOI is set at r ≥ 0.5**, the conservative row rounded up. The generous row is
> recorded so the choice is visible rather than buried: it would put the threshold near
> 0.19 and demand roughly 200 segments. The conservative reading is taken because the
> raw figure is what governs a claim about actual cortex. Note the direction of the
> argument: it demands a *higher* threshold and therefore a *cheaper* study.
>
> Power for a Pearson r at α = .05 two-tailed, with 3 df lost to within-film centring:
>
> | n | r=0.3 | r=0.4 | r=0.5 | r=0.6 | min r at 80% power |
> |---|---|---|---|---|---|
> | 20 | 0.21 | 0.35 | 0.54 | 0.74 | 0.63 |
> | 40 | 0.44 | 0.70 | 0.89 | 0.98 | 0.45 |
> | 60 | 0.62 | 0.88 | 0.98 | 1.00 | 0.36 |
> | **70** | 0.68 | 0.92 | **0.99** | 1.00 | **0.33** |
> | 100 | 0.85 | 0.98 | 1.00 | 1.00 | 0.28 |
>
> **n was raised from 60 to 70 on measurement, before scoring began.** At n = 60 the
> two cut-rate dials came in at 0.79 and 0.80 power — below the 80% floor — because
> roughly a third of cut rate's variance lies *between* films and within-film centring
> removes it. Cut rate is the dial H2b requires to replicate, so at 60 a null on cut
> rate could not have been distinguished from a failure to detect, and the PARTIAL
> verdict this design calls its most important possible outcome would have been
> unearned. **The replication check would have been unable to fail informatively.** At
> 70 both cut-rate dials reach 0.85 and 0.86 and all 14 dials clear the floor. The fix
> cost $1.70 of GPU.
>
> Two further reasons for headroom above the n = 40 that SESOI alone would require:
> the mediation estimate above is first-order, and 70 retains 80% power down to
> r = 0.33 if the true bottleneck is kinder than 0.2146; and the pass criterion's
> quantity is a cross-validated predictive r from the whole dial set, a multivariate
> quantity whose null is established by permutation, so the power table is indicative
> rather than exact.

### item_15 · Stopping rule

> Collection stops at 70 segments. There is no optional stopping on the basis of
> results, and no interim test.
>
> **One pre-specified futility stop exists, and it is a resource decision rather than
> a test.** At 30 segments, run the permutation null on the dials measured so far. If
> no dial has any parcel whose cross-validated r exceeds the 95th percentile of its own
> permutation distribution *uncorrected*, stop for futility. Being uncorrected it is
> deliberately lenient: it stops only a study showing nothing at all. The full
> FDR-corrected test still runs once, on the complete set.
>
> **The futility check was never executed, and the study did not rely on it.** The
> script implementing it (`futility_check.py`) was written and is in the repository,
> but its banner appears in no log and no verdict string exists anywhere on disk.
> Collection ran to completion without it. A separate script, `gate_and_continue.sh`,
> was run partway through and is sometimes mistaken for it: that one gates on
> **pipeline health only** — banked count, stray keys, 180 parcels, NaN, |z| ≤ 8, and
> a per-film minimum for stable within-film centring — and computes no relationship
> between any dial and any parcel. It returned FAIL on a banked-count precondition
> (30 of an expected 35) and the collection was continued by hand.
>
> **This rule replaces an earlier one, and the replacement is disclosed.** The original
> read "if after 20 segments no dial reaches |r| > 0.3, stop", and was arithmetically
> inert: at n = 20 the null probability of a single dial exceeding |r| = 0.3 is 0.247,
> so across six dials the probability at least one does so is 0.82 — the rule would
> almost never have triggered. It was restated before collection began and before any
> response value was inspected.

---

## 4 · Variables

### item_16 · Manipulated variables

> **None.** Stage 02 is observational; nothing is manipulated.
>
> For context: stage 01 (complete, reported) manipulated cut rate on identical
> footage, and stage 03 (specified, not started) will manipulate individual dials in
> generated clips. Neither is covered by this registration.

### item_17 · Measured variables

> **Predictors — 14 cinematographic dials**, measured per segment by `cinemetrics.py`
> using OpenCV and NumPy only, with no model weights and no network:
>
> | family | dials |
> |---|---|
> | cutting | `cuts_per_min`, `mean_shot_len_s` |
> | camera | `camera_jitter`, `camera_zoom`, `camera_pan` |
> | lighting | `median_luma`, `contrast_p5_p95`, `shadow_frac` |
> | colour | `colourfulness`, `mean_saturation`, `warm_cool` |
> | shot scale | `face_area_frac`, `face_hit_rate` |
> | focus | `dof_ratio` |
>
> Shot scale uses YuNet face detection rather than a Haar cascade: Haar fires on
> texture consistently, so a false positive appears on every frame of a static shot and
> no temporal filter removes it, whereas YuNet returns a confidence score that does.
> Frame stride is held at 1 — raising it would halve measurement cost, but cut
> detection compares adjacent frames, and cut rate is both the dial stage 01
> established and the one H2b must replicate.
>
> Scene-boundary counts per segment are recorded as a diagnostic and are **not**
> entered as a covariate.
>
> **Outcome — 180 HCP parcel values per segment**, as described in item_12.

### item_18 · Indices

> **Within-film centring.** Dials and parcels are both centred within film, always.
> This removes any per-film constant and is what stops any dial with a large
> between-film offset from becoming a proxy for film identity. It costs 3 degrees of
> freedom, accounted for in item_14.
>
> **Detectability label, computed not chosen.** A dial's spread surviving centring is
> `s = within-film SD / total SD`. Restriction of range attenuates a true correlation
> r to r_obs = r·s / √(1 − r² + r²s²). A dial is labelled **TESTED** when r_obs at the
> SESOI still yields ≥ 80% power at n = 70, and **UNDERPOWERED** when it does not.
> **All 14 dials are TESTED at n = 70**, the weakest being the two cut-rate dials at
> s = 0.66 and 0.67 (power 0.85 and 0.86); the remaining twelve sit at s = 0.87–1.00
> with power 0.94–0.99.
>
> A known limitation of this metric is registered because it did not bite rather than
> because it cannot: `s` is a ratio, so a dial with almost no absolute variance whose
> remnant survives centring scores s ≈ 1.0 and is labelled TESTED. `camera_pan`
> presented exactly that appearance — SD printed as `0.000` — and was checked directly:
> values reach 2.9 × 10⁻³ of frame width per frame, a pan across 421% of the frame over
> 60 s, with 27 static segments and 48 distinct values. A real dial; the `0.000` was a
> formatting artefact. **Future dials must be checked on absolute spread as well as on
> `s`.**

---

## 5 · Analysis Plan

### item_19 · Statistical models

> Per parcel, a **cross-validated elastic net** regresses that parcel's centred z on
> the full 14-dial set. Elastic net rather than OLS follows Kauttonen et al. (2015),
> who related 37 cinematic features to free-viewing fMRI and found elastic net more
> sensitive than PLS or unregularised regression precisely because the feature set was
> large and heavily intercorrelated. Our dial set is multicollinear by construction —
> see item_25 — and unregularised regression is unstable there.
>
> **Interaction terms are excluded from the primary model.** With 14 dials, all
> pairwise interactions is 91 additional terms at n = 70, the interactions
> are more collinear than the main effects, and adding them after seeing data is the
> forking-paths problem this registration exists to prevent. Separating covarying dials
> is what stage 03 is for; observational data structurally cannot do it.

### item_20 · Transformations

> Dials and parcels are centred within film (item_18). Parcel values are used as z.
> Cut count enters as measured; no log transform is applied at this stage — stage 01's
> log transform applied to a designed five-level manipulation, not to observational
> spread. No winsorising, no trimming, no outlier removal.

### item_21 · Inference criteria

> The null is **permutation over segment labels, 1,000 permutations.** This is a
> regression across segments, not a map-to-map comparison, so a spin test is the wrong
> null; spin tests become appropriate only when comparing resulting technique-maps
> against external maps such as Neurosynth terms, which is stage 03 and beyond. An
> earlier version of the roadmap specified a spin test here; that was identified as
> wrong and corrected before collection.
>
> **PASS requires both:**
>
> 1. **At least 3 of the 14 measured dials** have ≥ 1 parcel whose cross-validated
>    predictive r exceeds the 95th percentile of its permutation null, after FDR
>    correction across 180 parcels.
> 2. **Cut rate replicates** — the inferior-frontal cluster from stage 01 (IFJa, IFJp,
>    IFSp, 8C) associates with cut rate observationally as well.
>
> **FAIL** if fewer than 3 dials survive, or if cut rate fails to replicate.
>
> **PARTIAL** — dials survive but cut rate does not replicate — means the
> observational and controlled tracks disagree. This is registered in advance as the
> most important possible finding and one that would redirect the programme. It is not
> a failure and will not be reported as one.
>
> **Nulls are reported with equal prominence to positives.** A dial that does not move
> the sensor is a dial you cannot direct with, and knowing that is worth more than a
> plausible story about it. Every dial is reported with its TESTED or UNDERPOWERED
> label, so that "did not move the sensor" is never confused with "never varied enough
> to test" — the first is evidence, the second is absence of evidence.

### item_22 · Data exclusion

> **No dial is dropped.** A conventional pipeline drops predictors with too little
> variance to test; that step was specified and then removed as wrong on its own terms.
> It saves nothing — GPU cost is per segment and `cinemetrics.py` returns every dial in
> one pass — and it would create a reporting error this design forbids, by making a
> dropped dial and a tested-null dial indistinguishable in the write-up. Dials are
> classified, not dropped (item_18).
>
> **No segment is excluded on the basis of its values.** A segment is rejected only for
> pipeline failure: fewer than 180 parcels, any NaN, or |z| > 8. A rejected segment is
> rescored, not dropped.
>
> **One conditional exclusion was pre-specified and did not fire.** Batch 0 (4
> segments) counts toward the 70 *provided it required no change to the scoring path*.
> Had it required different flags, a different mode or a patched app, its clips would
> have come from a different pipeline than the rest, and mixing two scoring
> configurations in one dataset is a silent confound; they would then have been
> discarded and rescored. Batch 0 on 4 September 2026 required no such change, so its
> four clips stand.
>
> **The same conditional was tested again, and passed, when the Space application was
> patched mid-collection** to write results to a durable dataset repository. Rescoring
> an already-banked clip under the patched application reproduced its 180-parcel vector
> to within 5.0 × 10⁻⁷ (whole-vector r = 0.999999999999961), so all 70 clips come from
> one scoring configuration. See item_11.

### item_23 · Missing data

> **No-face segments are not missing data and are not imputed.** Where YuNet detects
> no face at all (16 of 244 segments), `face_area_frac` is encoded as 0.0 and
> `face_hit_rate` is carried alongside, so that "no face present" remains
> distinguishable from "a small face" rather than being conflated by a bare zero. This
> was found and fixed before analysis: null face-area values would otherwise have
> silently dropped the shot-scale dial from the model entirely.
>
> **Dial measurement had 0 failures across all 244 segments.**
>
> If a segment cannot be scored after rescoring — persistent Space failure — it is
> replaced by the next segment in the pre-registered stratified order for the same
> film, and the substitution is reported.

### item_24 · Exploratory analysis

> Declared in advance so that nothing exploratory can later be presented as
> confirmatory:
>
> 1. **All interim looks are exploratory and non-reportable.** See item_7.
> 2. **The inferior-frontal reading of stage 01 is exploratory.** Stage 01's strongest
>    responders — IFJa r = +0.996, IFJp, IFSp, 8C, 45, 44, p9-46v — were inferior
>    frontal junction and sulcus, i.e. cognitive control and task-switching cortex,
>    not the dorsal attention network predicted. That every cut is a task switch is a
>    coherent reading, but it is post-hoc. It enters stage 02 as pass criterion 2
>    (item_21), where it can fail.
> 3. **The dial correlation structure will be described but not modelled** (item_25).
> 4. Anything else noticed in the data is exploratory, will be labelled as such, and
>    will not be counted toward the pass criteria.

---

## 6 · Other

### item_25 · Additional information

> **Scope condition, stated quantitatively and never relaxed.** The dependent variable
> is TRIBE's prediction, not measured cortex. The link is r = 0.2146
> out-of-distribution, and this corpus is further out than that figure was measured on.
> A finding that technique moves TRIBE is a finding about TRIBE. This is turned into
> the effect-size threshold in item_14 rather than left as a disclaimer.
>
> **Pre-registered collinearity diagnostic, reported and not modelled.** Computed on
> centred dials across all 244 segments, before any segment was scored:
>
> - **Condition number of the dial correlation matrix: 58.8** — meaningful
>   collinearity (> 30), short of severe (> 100).
> - Strongest pairs: `median_luma`~`shadow_frac` **−0.90**;
>   `contrast_p5_p95`~`shadow_frac` −0.71; `median_luma`~`mean_saturation` −0.68;
>   `median_luma`~`contrast_p5_p95` +0.68; `shadow_frac`~`mean_saturation` +0.68.
> - Highest VIF: `shadow_frac` **9.5**, `median_luma` 6.1, `mean_saturation` 5.9,
>   `colourfulness` 5.0.
>
> The structure is one tight cluster and it is lighting-and-colour. The camera dials,
> the face and shot-scale dials, and depth of field are comparatively independent
> (VIF < 2.3), as is cut rate. **A consequence is registered in advance: any
> association found inside the lighting/colour cluster will attribute poorly.** The
> model may establish that the cluster matters without being able to say which member
> drives it. Observational data structurally cannot resolve that; it is a stage-03
> question and will be written up as one rather than argued away.
>
> **The index will be corpus-conditional and will be reported as such.** Gruber et al.
> (2024) found whole-brain ISC differing significantly across eight films —
> F(7,385) = 4.65, p < 0.001, η²G = 0.048 — with downstream associations landing in
> non-overlapping regions for nearly every film; of eight films, exactly one parcel was
> shared between two. Their conclusion, that a specific movie should be treated like a
> specific task, applies directly. Three films is enough to break dial covariance; it
> is not enough to claim film-independence.
>
> **Further limitations registered in advance.** Estimates are design-conditional
> (item_9). One era, one medium, three directors — Technicolor features from 1937–1951
> share conventions of lighting, staging and lens that contemporary cinema does not.
> No text branch: all results are video + audio only, which for a corpus containing
> dense dialogue omits a modality TRIBE was designed to use. Cut rate is the weakest
> dial in the design at s ≈ 0.66, precisely because it carries the most between-film
> signal, and it is also the dial the replication check depends on.
>
> **Materials and code.** `cinemetrics.py` (dial measurement), `cut_corpus.py`,
> `verify_colour.py`, `measure_dials.py`, `analyse_dials.py` (detectability,
> collinearity, selection), `run_batch.py` and `auto_batch.py` (scoring). Corpus
> provenance is by Internet Archive identifier in `CORPUS.md`; the source prints are
> not redistributed. Repository:
> `github.com/alec-mutuals/film-cognition-research`, commit
> `89d01a1b693154bfd54ac443c70899d8a75b1dea`.
>
> **Known defect in the pre-registration text, disclosed rather than corrected.**
> Three passages in `02-index/README.md` and `PAPER.md` reason over **6 dials** where
> the study measures **14**. The figure is a leftover from an earlier design that
> counted dial *families*. It is disclosed here rather than edited, because silently
> revising the arithmetic of a pre-registered document is exactly the softening this
> registration exists to prevent. Both affected conclusions survive, and both are
> strengthened at the true count:
>
> - *Futility rule (item_15).* "Across 6 dials the chance at least one exceeds
>   |r| = 0.3 at n = 20 is 0.82" is correct for 6 dials (1 − 0.753⁶ = 0.818). At 14
>   dials it is 1 − 0.753¹⁴ = **0.98**. The original rule was therefore even more
>   inert than stated, which reinforces rather than undermines the decision to
>   replace it.
> - *Interactions (item_19).* "With 6 dials, all pairwise interactions is 21 terms"
>   reads as 6 main effects plus 15 pairwise. At 14 dials it is 14 + 91 = **105
>   terms** at n = 70, which strengthens the case for excluding interactions from the
>   primary model.
>
> No pass criterion, threshold, sample size or model specification depends on the
> stale count.

> **Prior stages.** Stages 00 and 01 are complete and were reported against criteria
> fixed before each run. They are not covered by this registration and are described
> here only as context.
