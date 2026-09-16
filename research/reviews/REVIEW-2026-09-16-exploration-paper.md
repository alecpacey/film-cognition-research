# Review — *A technique→response index for cinematography, measured through a brain encoding model*

**Working draft of a review, 16 September 2026.** Prepared for the author on the author's own
manuscript (`research/PAPER.md`, draft of 15 September 2026, ~15,000 words), locally, with no
manuscript text sent to any external service. Materials available: the manuscript, every stage
`README` / `RESULT` / `CLIPS`, the analysis scripts and their JSON outputs, the build scripts,
the OSF registration text and the drafted amendment, `LOG.md`, `HANDOFF.md`. Not available:
the OSF registration as filed (embargoed), the fal and Hugging Face billing records, real fMRI
data of any kind. Reviewer competence: computational methods, statistics, study design,
reproducibility. Outside competence: the neuroanatomical readings (IFJ as task-switching cortex,
the auditory belt hierarchy); those are assessed only for internal consistency and for whether
the paper treats them as hypotheses. Two small analyses were run by the reviewer on the
repository's own data to check specific concerns; they are reported as such, with their
commands, and nothing else in this review is a reanalysis.

The three questions asked: **is the paper complete, is it theoretically grounded, and do its
conclusions hold** — as a consolidated report of an exploration that began with one hypothesis
and grew through observational and controlled stages — and **what should its limitations and
future work say** so that the next explorations follow from it.

---

## 1 · What the paper is, stated neutrally

| | |
|---|---|
| Research question | Can the relation between cinematographic technique and cortical response be measured systematically enough to be inverted — target profile → technique? |
| System under study | TRIBE (Meta AI), a trimodal fMRI encoding model, used as a deterministic *sensor*; 180 HCP-MMP1 parcels; text branch disabled throughout |
| Unit of inference | A 60 s clip's mean predicted response per parcel (stages 00, 01, 03, 01b, 02b); a 60 s film segment (stage 02, n = 70 from 244) |
| Designs | Three-clip content contrast (00); 5-level intercut ladder on identical footage (01); observational elastic net of 14 dials on 70 segments across 3 films, pre-registered (02); generated-imagery transfer gate (01b); 2 × 5 intercut ladder on generated single-take scenes, criteria fixed before generation (03); exploratory map characterisation (§6.7) and two exploratory follow-ups (§6.8) |
| Principal claims | H0 supported; H1 supported for cut rate; H2 supported broadly and weakly (101/180 survive, 9 reach SESOI); H2b not supported, then explained; H3 supported (PARTIAL-A); technique spans ~3 effective cortical directions, dominated by a face/place axis; inversion is projection; face area is the largest lever; the frontal miss in real cinema is a corpus property, unexplained |

---

## 2 · Summary assessment

**Completeness.** As a report of the exploration phase the paper is complete in *content*: every
stage that was run is reported against criteria fixed in advance, every verdict is the fixed one,
and the deviations are disclosed. It is not complete as a *document*: it was written by accretion
over ten days and carries the seams (§2.3 below), the abstract now runs to nine paragraphs, one
headline result has no script behind it (M2), and the statistical framing of the two controlled
stages needs correcting (M1). None of that is content missing; it is consolidation not yet done.

**Theoretical grounding.** The grounding is strongest where it is operational — the sensor as
instrument, the scope condition, the derived SESOI, the two-track design, the corpus argument
from Gruber et al. — and weakest where it is neuroscientific. The paper is careful to call the
IFJ reading a hypothesis, but it does not yet consider the most economical alternative for a
model-based sensor: that the "frontal response to cutting" is the video encoder's response to
temporal discontinuity, propagated through an encoding head that was never fitted to distinguish
the two (M5). The film-flipping sign found this week is the first evidence that bears on that,
and it should be treated as such rather than as a loose end.

**Conclusions.** The conclusions the paper actually draws are supportable, and several are
stated more carefully than most work in this area. Two need weakening. "Seven / eight times
chance" for the ladder counts is not a defensible statement (M1); the correct statement is that
each ladder's count is as extreme as, or one step from, the most extreme configuration a
5-level design can produce, at permutation *p* = 0.017–0.025. And the three-axis / 90.8%
retained-variance result must either be reproduced from a committed script or demoted (M2).
With those two changes the paper's final position — a broad, weak, low-dimensional index on a
model; a causal cut effect with two signatures, only one of which real cinema carries; face area
as the dominant reachable direction; inversion as projection — is an honest and useful endpoint
for an exploration paper.

**Is it a robust exploration paper?** Yes, in the sense that matters: the chain of stages is
explicit, each stage's ability to break the chain was fixed before it ran, and the two places
where results contradicted the plan (PARTIAL, PARTIAL-A) are reported as the plan said they would
be and then resolved by further work rather than reinterpreted. The robustness is procedural. The
statistical robustness of the controlled stages is thinner than the text says, for the reason in
M1, and the paper is better served by saying so than by the "×chance" framing.

---

## 3 · Strengths (these should survive consolidation intact)

1. **The scope condition is quantitative and never relaxed.** "The dependent variable is a
   model's prediction of cortex, not cortex" is stated in the abstract, propagated through the
   SESOI, and repeated at every claim. This is the single most important sentence in the paper
   and it is in the right place.
2. **Criteria before data, verdicts as fixed.** Stage 02 registered before analysis with frozen
   checksummed data; stage 03 criteria fixed before generation; verdict tables written in advance;
   PARTIAL and PARTIAL-A reported as such and *not softened*. The handling of the PARTIAL-A
   near-miss — keep the verdict, withdraw the mechanistic reading with the numbers that withdraw
   it — is the correct move and is well written.
3. **Nulls and weak results have equal prominence.** "Only 9 of 180 reach the SESOI" sits beside
   "101 survive"; the futility-check disclosure sits in §4.8 and §7 rather than a footnote.
4. **The design arguments are real arguments.** The rejection of animation as the minimum-variance
   case (from Gruber et al.), the black-and-white rejection, colour verified by measurement,
   encode normalisation as a variance confound, the detectability label — each is a decision with
   its reasoning exposed and, where the reasoning was wrong, the correction recorded.
5. **The two follow-ups on the frontal miss are a model of how to close a loose end**: rule out
   the analysis, rule out the range, rule out swamping by transplanting the causal slope, then
   build the missing diagnostic and test the remaining hypothesis. The result is a null, and it
   is reported as one.
6. **Method failure as evidence (§7)** is unusual, well argued, and — given the sensor's
   silent-failure property — belongs in the paper rather than an appendix.

---

## 4 · Evidence quality by stage

Grading scale, adapted for a computational exploration on a deterministic sensor (GRADE is
built for clinical evidence and does not transfer directly): **Strong** — pre-specified, replicated
or permutation-tested against the right null, effect large relative to the design's resolution;
**Moderate** — pre-specified and passed, but one identified threat to inference remains; **Weak**
— exploratory, or *n* too small to separate the claim from alternatives; **Very weak** —
descriptive only. Every grade inherits the model-not-brain ceiling and is *about TRIBE*.

| stage | design / n | what the evidence supports | principal threat | grade |
|---|---|---|---|---|
| 00 Probe | 3 clips, one film | The sensor separates three contents and does so along interpretable chains (double dissociation, graded middle) | Face clip carries speech; attribution to faces vs voices not separable; one film, one grade | **Moderate** for discrimination; **Weak** for attribution |
| 01 Gate | 5 levels, one scene pair, live action, effective range 2.1× | Cut count moves the sensor monotonically on identical footage; the response is whole-cortex and essentially one-dimensional (M1) | Count null mis-specified; permutation *p* = 0.017 is the design's floor; one scene pair; ~22 native cuts | **Moderate** (would be Strong with a second scene pair) |
| 02 Index | n = 70 / 244, 3 films, pre-registered, 1,000-perm null, FDR, restricted-perm sensitivity | Dials predict parcels broadly and weakly; face area dominant; cut rate loads auditory, not frontal | Criterion 1 lenient (14/14 nearly guaranteed once 101 survive); SESOI applies to a marginal *r* but the statistic is a multivariate CV *r*; hyperparameters not registered; temporal adjacency untested; corpus-conditional with film-by-dial sign flips now demonstrated | **Moderate** for "predicts"; **Weak** for any per-dial effect size |
| 01b Transfer | 3 generated clips, criteria pre-fixed | Generated imagery reproduces the face/place axis (+0.699 vs bar 0.50) | Cutting confounded with content; one generator; three clips | **Moderate** for the axis; nothing else |
| 02b Generalisation | n = 3, exploratory | The fitted index predicts generated clips' profiles | Exploratory; one dial extrapolated; inherits 01b's confound | **Weak** |
| 03 Isolation | 2 × 5, generated single-take bases, criteria pre-fixed, range 31× | Cutting alone drives the sensor: frontal up, auditory down, in both arms | Count null mis-specified (M1); S+ vs S− confounds speech with audio discontinuity (M4); one scene pair; face base 0.052; verdict table pre-attached a reading | **Moderate** (Strong on "cutting moves the sensor"; Moderate on anatomy; the arm comparison is Weak) |
| §6.7 Map | exploratory, no script on disk | 14 dials → ~3 effective directions; axis 1 = face/place; 90.8% retained | Not reproducible from the repository as it stands (M2); baseline weak; column space fitted to Y | **Very weak** until reproduced; then **Weak–Moderate** |
| §6.8 follow-ups | exploratory, scripts + JSON committed | The frontal miss is not the penalty, range, swamping or cut composition; sign flips between films | Histogram proxy partial on live action; many comparisons, disclosed | **Moderate** as a set of exclusions; the positive lead (film-specific) is **Weak** |

---

## 5 · Claim–evidence audit

Checked by the reviewer against the stage `RESULT` files and JSON outputs on 16 September.

| claim (location) | evidence | status |
|---|---|---|
| Stage 00: Jaccard 0.15; pairs 0.05 / 0.05 / 0.33; A5 +2.37, STSdp +2.04, VMV2 +2.83; whole-vector −0.098 / +0.455 / +0.453 (Abstract, §5.1) | `00-probe/RESULT.md` | **supported** |
| Stage 01: 51/180; IFJa +0.996, 8C +0.990, 7AL −0.990; 3/7 dorsal vs 1.98; whole-vector +0.8934; detected totals 25→53 (§5.2) | `01-cutrate/RESULT.md` | **supported** as numbers; **"chance ≈ 7" not supported** (M1) |
| Stage 02: 101/180, 14/14, 9 ≥ SESOI, median 0.35, 65/101 face-dominant, cluster table, restricted 99/180 (§6.0–6.6) | `analysis_result.json`, `sensitivity_restricted_perm.json`, `RESULT.md` | **supported** |
| 01b: +0.699, Jaccard 0.083, reference +0.936, contrast +0.831 (§9) | `01b-transfer/RESULT.md` | **supported** |
| 02b: 0.41 / 0.90 / 0.89, contrast +0.77 (§9) | `02b-generalisation/RESULT.md` | **supported** |
| Stage 03: all 29 figures in §6.8 | `03-isolation/evaluation.json` (programmatic check, 29/29) | **supported** |
| §6.8 follow-ups | `frontal_miss.json`, `frontal_miss_transplant.json`, `scene_switches_result.json` | **supported** |
| §6.7: singular values 3.34 / 1.52 / 1.01; 69.4 / 14.3 / 6.4%; participation 5.56 and 8.35; 90.8% vs 7.9% vs 99.4%; axis-1 vs run-00 contrast +0.936, null 0.144 | **no script, no output file in the repository**; the introducing commit (`d209602`) changed only `PAPER.md`; `01b-transfer/evaluate_01b.py` recomputes an "axis 1" and reports +0.936 as its self-test, which corroborates one figure | **needs evidence** (M2) |
| §4.9 / §8: "All results are video + audio only" | Space variable `AUDIO_ONLY=1` verified; stage 03 scorer asserts it | **supported** |
| §6.8: "S+ keeps the face scene's native dialogue" | `03-isolation/build_stage03.sh`: S+ is the ladder *as built* by `build_conditions.py`, i.e. the audio is intercut with the picture; S− maps the landscape track over the whole clip | **imprecise** (M4) |
| §4.3 scene-boundary count | corrected this week; exploratory count now on disk | **supported** |
| §7: "The registration was amended publicly" | `HANDOFF.md`: amendment drafted at `~/Desktop/osf-registration-attachments/15-AMENDMENT.md`, **not posted** | **not supported as written** (m1) |

---

## 6 · Major comments

Each: location · observation · evidence · why it matters · requested action.

### M1 · The counting criterion's null is mis-specified, and the "×chance" framing overstates stages 01 and 03

**Location.** Abstract; §5.2 ("chance expectation of ~7 … roughly seven times chance");
§6.8 ("roughly eight times chance"); `01-cutrate/README.md`, `03-isolation/README.md`.

**Observation.** "With *n* = 5, *r* = 0.9 is *p* ≈ 0.037, so ~7 of 180 are expected by chance"
treats the 180 parcels as independent draws. They are not. Across the five ladder levels the
180-parcel response has a participation ratio of **1.25** (stage 03 S+; maximum possible 4):
the whole cortex moves along essentially one direction as cut count changes. When one
direction carries the response, either almost every parcel clears |*r*| > 0.9 or almost none
does; the count is close to a single Bernoulli event, not 180 of them.

**Evidence (reviewer's analysis).** The correct null for a 5-level design is the permutation of
the level labels (5! = 120 orderings). Command, from `02-index/`, on the committed parcel
vectors:

```
for each of the 120 orderings of (1,3,7,15,31): recompute r per parcel vs log cuts, count |r|>0.9
stage 01      observed 51   null median 3, 95th pct 28, max 51   P(count ≥ 51) = 2/120 = 0.017
stage 03 S+   observed 58   null median 2, 95th pct 32, max 79   P(count ≥ 58) = 3/120 = 0.025
stage 03 S−   observed 54   null median 1, 95th pct 32, max 90   P(count ≥ 54) = 3/120 = 0.025
```

The 2/120 for stage 01 is the identity ordering and its reverse (identical |*r*|), i.e. the
observed count is *the* most extreme configuration possible. Stage 03 is one configuration
from that. But the null's upper tail reaches 79 and 90: an ordering that is not the true one
can put more parcels over the bar than the true one does. "Seven times chance" is therefore
not a meaningful description; the bar of ≥ 15 is cleared by 29 of 120 random orderings in
stage 01.

**Why it matters.** The count is the primary pre-registered statistic of both controlled
stages, and the abstract leads with it. The results survive — *p* = 0.017 and 0.025 — but as
"as strong as five levels can show", not as "an order of magnitude above chance". The same
fact reframes the anatomy: with one dominant response direction, "IFJa up, A4 down" is the
sign pattern of that direction, and the cluster and quartet are two ends of one mode rather
than two independent findings.

**Requested action.** (a) Replace every "×chance" statement with the level-permutation *p* and
the null's 95th percentile. (b) Report the participation ratio across levels and say plainly
that the sensor's response to cut count is close to one-dimensional. (c) Note in §8 that the
5-level design has a *p*-floor of 1/60 and cannot separate a strong effect from a very strong
one; 9 levels would give a floor of ~3 × 10⁻⁶. (d) Keep the pre-registered bar as reported —
the point is not that stage 01 or 03 failed, it is that the bar was weaker than believed, and a
paper about silent failure should say so.

### M2 · The three-axis map result (§6.7) is not reproducible from the repository

**Location.** §6.7 in full; Abstract paragraph 6; §9 point four; H4 row of §2.

**Observation.** The singular values, variance shares, participation ratios, the 90.8% /
7.9% / 99.4% comparison and the axis-1 correlation with run 00 are reported with no script and
no output file anywhere under `research/`. The commit that introduced the section changed only
`PAPER.md`. One figure (+0.936) is corroborated by the self-test in `evaluate_01b.py`, which
recomputes an axis from the coefficient matrix; the rest are not.

**Why it matters.** This section carries the paper's most quotable structural claim ("fourteen
knobs, about three outputs"), bounds H4 in advance, and supplies the film's thesis its
mechanism (a hill-climber goes to faces). A claim of that weight with no artefact is exactly
the failure mode §7 is about.

**Requested action.** Commit `02-index/index_map.py` that rebuilds **B** from
`analysis_result.json`, reproduces every number in §6.7 to the stated precision, writes
`index_map.json`, and is cited from the section. If any number does not reproduce, correct
the text. While doing so, strengthen the baseline: the "random 14-dimensional subspace" retains
7.9% because random directions in a 180-space are nearly orthogonal to anything; the relevant
comparator is the column space of **B** fitted to *label-permuted* **Y** (same model, no signal),
which will retain far more than 7.9% and is the honest floor for "technique is aligned with how
this cortex varies".

### M3 · The SESOI derivation is a heuristic presented as a bound, and the statistic it is applied to is not the one it was derived for

**Location.** §3.2, §4.5, §6.4, Abstract.

**Observation.** Three separate issues. (i) *r*<sub>DY</sub> ≈ *r*<sub>DP</sub> × *r*<sub>PY</sub>
holds only if P fully mediates D→Y and TRIBE's error is uncorrelated with D; nothing establishes
either, and the true implied correlation can be larger or smaller. (ii) 0.2146 is a *mean over
parcels*; the paper itself reports 0.77–0.85 for the best regions normalised. A parcel-wise
propagation would move the SESOI by a factor of ~2–4 across cortex, and the parcels this paper
cares most about (auditory belt, STS, IFJ) are among TRIBE's best-predicted regions. (iii) The
SESOI is derived for a *marginal* dial→parcel *r*; the reported statistic is the cross-validated
*r* of a 14-dial elastic net per parcel. §4.5 acknowledges this ("indicative, not exact") but
§6.4 then applies the 0.5 line to the multivariate CV *r* to conclude "only 9 reach the SESOI".
That comparison is not licensed by the derivation.

**Why it matters.** The derived SESOI is listed as contribution 1 and it changes the reading of
the main result. If the derivation is loose in both directions, "most survivors fall on the
wrong side of the line" is a judgement, not a measurement.

**Requested action.** Present §3.2 as a *justified heuristic* with a stated range (the two rows
already give 0.19–0.47; say the parcel-wise range would be wider), keep 0.5 as the
pre-registered choice, and in §6.4 either (a) report a per-dial marginal effect size that the
SESOI *does* apply to — the standardised coefficient or the semi-partial *r* of each dial per
parcel — or (b) state that the SESOI comparison is to a different quantity and is approximate.
Also state that criterion 1 as registered ("≥ 3 dials with ≥ 1 surviving parcel") was too
lenient to be informative once a broad fit exists, and that a future registration should set a
per-dial bar.

### M4 · Stage 03's speech factor is confounded with audio discontinuity, and the design text does not say so

**Location.** §6.8 "Design"; `03-isolation/README.md`; `RESULT.md`.

**Observation.** `build_stage03.sh` makes S+ the ladder *as built* by `build_conditions.py`, so
in S+ the soundtrack alternates dialogue / ambient at every cut; S− carries one continuous
ambient track. The two arms therefore differ in (a) speech presence and (b) whether the audio
has a discontinuity at each cut, and (c) loudness and spectral content. The paper's sentence "S+
keeps the face scene's native dialogue" reads as if dialogue ran continuously.

**Why it matters.** For the frontal conclusion it does not matter, and the paper's own reading
survives: the frontal effect is present in both arms, so neither speech nor audio discontinuity
is required. For the auditory signature the S− arm is the informative one (visual cuts alone
suffice), and that is correctly drawn. But the A5 arm difference (+0.15 with speech, −0.95
without) is currently unexplained and is at least as likely to be about audio discontinuity as
about speech. And the verdict table's PARTIAL-A reading ("needs speech present") was
unfalsifiable as designed, because S+ never isolated speech.

**Requested action.** State the audio construction of each arm exactly. Add to §8 that the arm
factor is "speech-with-discontinuous-audio vs no-speech-with-continuous-audio", and that a
clean speech factor needs a third arm (continuous dialogue bed under both scenes, or the face
audio mapped over the whole clip). Record as a method lesson in §7 that verdict tables should
carry outcomes, not mechanisms.

### M5 · The most economical alternative to "cognitive-control cortex responds to switches" is a video-encoder artefact, and the paper does not consider it

**Location.** §5.2 (the IFJ reading), §6.8, §8.

**Observation.** TRIBE's frontal prediction is a linear head on V-JEPA 2 features. A hard cut
is, to a video encoder, a large temporal discontinuity in feature space regardless of what is on
either side of it. If the encoding head learned, on 121 hours of mostly *Friends*, that feature
discontinuities co-occur with frontal BOLD (plausibly, since sitcom cuts track dialogue turns),
then "IFJa rises with cut count on generated footage" is the head reproducing a training
correlation, not a prediction that a viewer's IFJ would do so. Three facts in the paper bear on
this and are not yet connected: the response to cut count is nearly one-dimensional across
cortex (M1); it is present with content and audio held fixed (stage 03); and it *does not
appear in real cinema*, where cuts sit inside continuous scenes — while its sign flips between
films.

**Why it matters.** It is the difference between "cutting engages control cortex" and "the
sensor has a cut detector". Both are compatible with everything reported. Only the second
predicts the corpus null.

**Requested action.** Add the alternative to §8 explicitly. Propose the discriminating test
(free or near-free, §9 / Future Work F2 below): ladders where the discontinuity is not a scene
change — the same scene intercut with itself from a different take, or a 1-frame black insert,
or temporal jitter — score them, and ask whether the frontal response follows discontinuity
count. If it does, the paper's claim becomes "the sensor responds to discontinuity", which is
still a lever for stage 04 and is more honest.

### M6 · The disabled text branch is a standing threat that is now cheaply testable

**Location.** §4.9, §8 ("No text branch"), §9 point two.

**Observation.** The claim that TRIBE "tolerates the missing text modality through modality
dropout" is asserted from upstream documentation, never measured on this material. The parcels
that carry the paper's face axis (STSdp, A5, STSvp) and the auditory cut signature are exactly
the parcels a language branch would move. Meta access is granted; one rescoring attempt failed
for an undiagnosed reason and is parked.

**Why it matters.** Every result is conditional on a modality being absent. The paper says so,
but a reviewer will ask why a $3–4 check was not run.

**Requested action.** Before any preprint, rescore the three stage-00 clips and the two stage-03
bases with the text branch on and report the whole-vector Δ and the Δ on the named parcels. If
the failure cannot be diagnosed in a bounded effort, say that in §8 with the cost of the attempt.

### M7 · Corpus-conditionality is now demonstrated, not merely disclosed, and the analysis should reflect it

**Location.** §3.3, §6.5, §6.8 follow-ups, §8.

**Observation.** The frontal parcels' correlation with cut rate is +0.32 to +0.45 in *Nothing
Sacred* and −0.25 to −0.35 in *Jungle Book* (§6.8 / `frontal_miss.md`). That is a
film-by-dial interaction, which within-film *centring* cannot remove — it removes film means,
not film slopes. Gruber et al. is cited as the reason to expect this; the paper has now
observed it in its own data.

**Why it matters.** The 101/180 pooled fit averages over slopes that may have opposite signs.
Some survivors may be "survivors" only because one film's slope dominates.

**Requested action.** Report per-film coefficients for the cut-rate dials and the face dial as
standard (a table in §6.4 or the supplement), and note that a mixed model with film random
slopes is the appropriate confirmatory model for the next corpus — with the honest caveat that
three films cannot estimate a slope variance. This becomes Future Work F4.

### M8 · Availability and registration state are not what a preprint requires

**Location.** §6 preamble, §7, Sources, absent data/code statement.

**Observation.** The repository is private. The OSF registration is embargoed to September 2027
and the amendment §7 describes as "made" is drafted and unposted. Stage 03 is not registered
anywhere outside the repository; its "criteria fixed before generation" claim rests on git
history alone. There is no data/code availability statement.

**Requested action.** Post the amendment (it is a correction of a false statement about
compliance; the paper's own §7 argues why that cannot wait). Add an availability statement
naming what is public, what is embargoed and until when, and what is withheld (the fal key,
billing). For stage 03, cite the commit hash of the README as the timestamp and say the
registration is by version control, not by OSF. Decide whether the repository goes public with
the preprint; if not, deposit the frozen data, the scripts and the JSON outputs on OSF alongside
the registration.

### M9 · The manuscript needs one consolidation pass before it can be read as a paper rather than as a log

**Location.** Whole document; Abstract; §1–§3; §6.5; §9.

**Observation.** The abstract is nine paragraphs and reports exploratory follow-ups at the same
level as registered results. §1–§3 predate stages 02–03 and still frame inversion as the
endpoint without the §6.7 bound. §6.5 is preserved "as written" with an addendum — right for a
lab notebook, wrong for a paper. §6.2 still says the lighting cluster "is a stage-03 question
and will be written up as one" after stage 03 has been written up on cut rate only. §9's
five-point list mixes done, undone, and constraints. Terminology drifts ("index", "crosswalk",
"map", "console").

**Requested action.** See §8 of this review for a proposed structure. The principle: the
*narrative of how the plan changed* belongs in §7 and the log; the results sections should read
as if written once, after everything was known.

---

## 7 · Minor comments

- **m1 (§7, §4.8).** "The registration was amended publicly" — it has not been. Change to "an
  amendment has been drafted / posted on [date]" once true.
- **m2 (§5.2).** "log cut count" is `log2(added cuts)` in stage 01's RESULT and natural log in
  stage 03's evaluator; correlation is invariant to the base, but say which and say it once.
- **m3 (§6.4).** "There are no nulls to report" — under a criterion that any survivor with a
  non-zero coefficient counts, no dial *could* be a null with 101 survivors and an L1 penalty
  that leaves several coefficients per parcel. Say the criterion could not produce a null.
- **m4 (§6.5, §6.8).** "IFSp survives with exactly zero weight" — with L1 regularisation
  exact zeros are the expected output, not a striking finding; the OLS refit (+0.067, *t* 0.63)
  is the informative number and is now in §6.8; cross-reference it from §6.5.
- **m5 (§4.5).** The power table uses 3 df lost to centring; the elastic net's effective df
  are different and unknown; the table is fine as indicative but the "80% floor" language reads
  as exact.
- **m6 (§3.1).** "TRIBE's released checkpoint has no subject-specific parameters" — TRIBE was
  trained with subject embeddings; state which subject (or average) the Space uses and that
  determinism was verified empirically rather than assumed from architecture.
- **m7 (§6.7, §6.8, Abstract).** Mark exploratory results as such in the abstract ("In
  exploratory analyses…") so that a reader who reads only the abstract can tell registered from
  post hoc.
- **m8 (§6.8).** "roughly eight times chance" — remove per M1.
- **m9 (Sources).** Ten entries, informally formatted, two incomplete (Baldassano 2017 has no
  venue or volume; Lakens has no year or edition). TRIBE and the Algonauts-winners preprints
  should be checked for published versions. The arXiv null result cited in the repository README
  for the engagement claim is not in the paper's sources; either use it or drop the dependency.
  Run the citation-management skill before circulation.
- **m10 (§1.3).** The film production paragraph is well placed but should state that the film's
  premise is a *hypothesis the research tests*, not a result it relies on — one sentence.
- **m11 (§4.3, new text).** The scene-boundary correction is now three sentences; two will do
  once the final draft no longer needs to explain the change.
- **m12 (throughout).** Money is reported in five places to two decimals. One table in §4.9 or
  an appendix, once.
- **m13 (§9 table).** Add a column "what it licenses" so the table does the work the prose
  currently does.

---

## 8 · A proposed structure for the consolidated final version

The current document is a faithful history. The final version should be a paper whose history
is confined to §7 and the log. Proposed outline, with what moves:

1. **Abstract** — five paragraphs, ≤ 400 words: question and instrument with the scope
   condition; the chain (00→01→02→03) and its verdicts in one paragraph; the two structural
   results (index is broad, weak, ~3-dimensional; cut rate is causal with two signatures and
   real cinema carries one); what this bounds for inversion; method failure in one sentence.
   Exploratory results flagged as such.
2. **Introduction** — as now, but §1.3's contribution list updated: add the reconciliation of
   observational and controlled measurement as a contribution, and demote "detectability
   classification" to a method note.
3. **Hypotheses** — table as now with the H2b explanation and H3 row; add H3′ (discontinuity
   vs switch, M5) as *open*.
4. **Theoretical framework** — §3.2 rewritten as a justified heuristic with a range (M3); add a
   short subsection on what a *model-based* sensor can and cannot license (the encoder-artefact
   argument, M5), placed before any result so the results are read through it.
5. **Methods** — corpus, encode, segmentation, dials, sample size, detectability, model and
   null, infrastructure — as now, trimmed of narrative ("was specified, then removed" → one
   clause). Add the level-permutation null for ladder designs (M1) as the method for stages 01
   and 03. Add the exact audio construction of stage 03's arms (M4).
6. **Results** — one section per stage in order 00, 01, 02, 01b/02b (one subsection), 03, with
   identical internal structure (question · design · criteria · result · what it licenses ·
   caveats). §6.5 rewritten once with stage 03 known; §6.8's follow-ups become a subsection of
   stage 02's results titled "Why the corpus lacks the frontal effect: exclusions".
7. **The index as a map** — §6.7, reproduced from a committed script with the permuted-label
   baseline (M2), and with H4's bound stated as its consequence.
8. **Method failure as evidence** — as now, plus the count-null lesson and the verdict-table
   lesson (M1, M4).
9. **Limitations and future work** — replaced by the section drafted in §9 below.
10. **Status** — the table only; the prose moves into §9 of the paper.

Reverse-outline test to apply after the pass: each results subsection's first sentence should
state what the stage licenses; if a paragraph's topic sentence cannot be mapped to that, it
belongs in §8 or the log.

---

## 9 · Draft: Limitations and Future Work

Written to be dropped into the paper after editing, and written so that each future-work item
is a *specifiable next exploration* — a design, a cost tier, and the result that would falsify
the current reading. Cost tiers: **A** free (existing data, local compute); **B** under $20;
**C** $20–200; **D** requires resources this programme does not have.

### 9.1 Limitations

**A model, not a brain.** Every result is a statement about TRIBE's predictions. The published
link to cortex is *r* = 0.2146 out of distribution, the material here is further out than that
figure was measured on, and the parcel-wise accuracy is unknown for this material. The derived
SESOI propagates that number as a heuristic, not a bound.

**The sensor may have a cut detector rather than a cut response.** The response to cut count on
identical footage is nearly one-dimensional across cortex and absent from real cinema, which is
what a video-encoder response to temporal discontinuity, mapped through a head fitted on sitcom
footage, would produce. The cognitive-control reading is one hypothesis; this is the other, and
nothing here separates them.

**Five levels, one scene pair, per controlled stage.** The count criterion reaches its *p*-floor
(1/60) at the observed effect and cannot distinguish strong from very strong; a second scene pair
would have doubled the design's resolution at a third of the cost of stage 03.

**Three films, and film-by-dial interactions are now observed.** The frontal parcels' relation to
cut rate has opposite signs in two of the three films. Within-film centring removes film means,
not film slopes; the pooled index averages over slopes that may disagree.

**The text branch was never on.** Modality-dropout tolerance is assumed from documentation.

**Generated footage is out of distribution for the encoding head**, and stage 03's causal
result is licensed only on that footage, by one generator, with a face base short of its
shot-scale target.

**Stage 03's speech factor is not a clean speech factor**: it co-varies with audio
discontinuity at cuts and with loudness.

**Effect sizes are design-conditional** (segments selected to spread dials) and the SESOI was
applied to a multivariate statistic it was not derived for.

**The map is exploratory** and its column space is fitted to the response it is then shown to
align with.

**The frontal miss is unexplained.** It is not the regression, the range, content variance or
the within/between-scene composition of cuts. It differs in sign between films.

### 9.2 Future work — as a programme of explorations

**F1 · Close the model–brain gap for the dials that matter (tier C–D; the most important item).**
Real fMRI on feature films exists publicly: the Naturalistic Neuroimaging Database (Aliko et
al., 10 films, 86 participants) and the Algonauts 2025 / CNeuroMod movie data TRIBE itself was
fitted on. Measure the 14 dials on those films with `cinemetrics.py` unchanged, fit the same
within-film-centred model to *real* parcel responses, and compare the dial→parcel coefficient
maps with this index parcel by parcel. The films must be sourced; the dial pipeline runs as is.
*Falsifies:* if the face/place axis and the auditory cut signature do not appear in real BOLD
at any size, the index is a property of TRIBE and the programme's inversion thesis is about a
model. *Supports:* an axis-1 correlation above the permutation null on real data would be the
first result in this programme that is about a brain.

**F2 · Discontinuity versus switch (tier B).** Ladders in which the cut is not a scene change:
one generated scene intercut with a second take of itself; the same scene with 1-frame black
inserts at 1/3/7/15/31 positions; temporal jitter without cuts. Score, and ask whether the
frontal and auditory signatures follow discontinuity count. *Falsifies* the cognitive-control
reading if they do; *supports* it if scene-alternating ladders alone produce the frontal
response. This also resolves the frontal miss if the answer is "discontinuity", because real
cinema's cuts are the same discontinuity and the effect should then have appeared — which would
push the explanation back to the encoder's context window and how the Space windows 60 s.

**F3 · Text branch on (tier B).** Rescore the stage-00 clips, the stage-03 bases and one ladder
arm with the Llama branch enabled; report whole-vector and named-parcel Δ. Diagnose the failed
attempt within a bounded effort or report the bound.

**F4 · Corpus expansion with film as a random effect (tier B–C).** Six public-domain
live-action Technicolor features were verified; three were used. Add three, re-run the dial
pipeline (free), score 25 segments per new film (~$13), fit a mixed model with film random
slopes on the cut-rate and face dials, and report the slope variance. *Falsifies* the index as
film-independent if slope variance dominates; *supports* corpus-conditionality as the correct
reading either way and makes it quantitative.

**F5 · Explain the sign flip with content descriptors the dial set lacks (tier A).** Per
segment: speech presence and proportion (Whisper, local), a semantic embedding of the segment
(CLIP on sampled frames, local), and a scene-change count from embedding distance rather than
colour histograms — the semantic proxy `scene_switches.md` names. Regress the frontal parcels
on these within film and ask whether the *Nothing Sacred* vs *Jungle Book* sign difference is
carried by speech proportion or scene semantics. Free; runs on the 244 segments already cut.

**F6 · Isolate face area, then the lighting cluster, by construction (tier B–C).** Stage 03's
recipe for the dial the index says is largest: generated single-take scenes at 3–5 face-area
levels with everything else prompted constant, measured with `cinemetrics.py` before scoring,
criteria first. Then luminance and saturation separately, which observational data structurally
cannot attribute (§6.2). Each ladder ~$5–15.

**F7 · Replace the count criterion (tier A, method).** For every ladder design, pre-register the
level-permutation *p* of the count and the whole-vector monotonicity, report the participation
ratio, and use ≥ 7 levels or ≥ 2 scene pairs so the *p*-floor is below 0.01. Re-express stages
01 and 03 in these terms in the consolidated paper.

**F8 · Cut-locked responses inside a clip (tier A once timelines are saved).** TRIBE emits a
1 Hz timeline; the Space keeps only the clip mean. Saving the timeline costs nothing and allows
event-locked averaging around each cut — the transient response to a cut separated from the
sustained response to content, within one clip, with the cut positions known exactly from the
ladder. This is the analysis that would distinguish "cuts" from "what cuts accompany" without
any new generation.

**F9 · Stage 04 as projection, then as a controller (tier C).** Respecified per §6.7: choose a
target inside the reachable subspace, derive a dial setting, generate, measure, and test whether
the achieved profile lands within a pre-fixed distance of the prediction, against a permutation
null over dial settings. Then the film's premise as an experiment: a hill-climber on the index
with a generator in the loop, run for a fixed budget of clips, with the pre-registered
prediction that its trajectory moves along axis 1 toward faces. Cut rate is admissible as a
frontal lever only on intercut material; F2 decides whether it is admissible at all.

**F10 · Registration practice (tier A).** Register stage 03 retroactively by depositing its
README at its commit hash; register every future stage on OSF before generation; fix
hyperparameters and the count null in the registration; keep verdict tables free of
mechanistic readings; post the pending amendment.

---

## 10 · Five-dimension self-review (research-paper-writing checklist)

| dimension | answer | unresolved |
|---|---|---|
| Contribution | Clear and honest: a method for using an encoding model as a sensor with a quantitative scope condition; a two-track design that produced and then resolved a disagreement; a low-dimensional map that bounds the endpoint | The map (M2) must be reproducible; the count framing (M1) must be corrected |
| Writing clarity | Sentences are clear; the document is not — it reads as a log | M9; the consolidation pass |
| Experimental strength | Procedurally strong (criteria first, verdicts fixed); statistically thin in the controlled stages (5 levels, one pair, *p*-floor) | M1, F7 |
| Evaluation completeness | Complete for what was run; the text-branch and encoder-artefact checks are the two cheap missing evaluations | M5, M6 |
| Method soundness | Sound where registered; the SESOI is a heuristic mis-applied to the reported statistic; the arm factor is confounded | M3, M4 |

---

## 11 · Overall assessment

The paper is a genuinely careful exploration report whose main risk is not overclaiming — it
under-claims in most places — but *mis-stating the strength of its two controlled results* and
*carrying one headline result without an artefact*. Fix M1 and M2, present the SESOI as the
heuristic it is (M3), state the arm construction (M4), add the encoder-artefact alternative as
a named hypothesis (M5), and consolidate the text (M9), and it is a preprint-ready
exploration-phase paper whose conclusions I would sign. F1 and F2 are the two explorations that
would most change what it can claim; F5, F7 and F8 are free and should be done before either.

*Assistance disclosure.* This draft was prepared with the peer-review, scientific-critical-thinking
and research-paper-writing procedures from Scientific Agent Skills (Kassis, T., Agarwal, V.,
He, Y., Patel, D., & Brueckner, A. M., 2026, arXiv:2609.00065); the level-permutation null and
the §6.7 artefact check were computed by the reviewer on the repository's committed data. Every
statement above should be verified by the author before any of it is acted on or reused.
