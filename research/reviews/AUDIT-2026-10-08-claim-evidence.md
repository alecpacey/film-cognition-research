# Claim–evidence audit of `PAPER.md` — consolidation step 4i

8 October 2026, on the text after steps 4a–4g. An internal audit by the author's session, run
locally; no manuscript text was sent to any external service (4g's lookups fetched public source
records only). Programmatic where possible. It checks that the paper says what its evidence says;
it does not re-run the analyses, and it is not peer review.

## 1 · Numbers — every decimal traced to evidence (`numeric_audit.py`)

Every decimal and percentage before the Sources section (**777**) was looked for in an evidence
corpus deliberately limited to records the analyses wrote: RESULT files, analysis notes, `LOG.md`,
summary JSON outputs (raw data excluded — a 2-decimal number will match *something* among 200,000
raw values by chance), and the three external sources verified in 4g. Planning documents
(ROADMAP, CONSOLIDATION, reviews) were excluded so that no number is "supported" by a document
that merely copied it. Three or more decimals: exact string or JSON rounding; two decimals: exact
string in a text record only.

**39 unmatched on first pass, 0 after triage:** 17 were § references caught by the pattern; 7 were
the spend table's derived sums (components sourced, sums recomputed in 4f); 15 were § 6 map
figures stored as fractions in `index_map.json` — each confirmed at its exact key, two of them
only after the first match was rejected as coincidental (13.5% is `retained.random_max` 0.1349,
not stage 00's crowd *r*; 57.7% is `retained.axis1` 0.5768, not a dial loading).

Re-running needs the three source pages saved locally; the script takes their directory as its
argument (`arxiv_2507.22229.html`, `leipold_v1.html`, `cao2024.html`).

## 2 · Counts and verdicts — checked against the result files

All match: 101 / 180 survivors and 14 / 14 dials (`analysis_result.json`); face area holds the
largest coefficient in 65 of the 101 (recomputed); 9 survivors with CV *r* > 0.5; stage 02 PARTIAL
with criterion 2 not met; frozen SHA `93807b80…`; stage 01's 51 / 180 and 3 of 7 dorsal-attention
parcels; stage 03's 58 and 54 (`evaluation.json`, `n_parcels_abs_r_gt_0.9`) and PARTIAL-A; 01b PASS;
03b GRADED; 244 segments (95 / 66 / 83) and 70 selected (24 / 23 / 23).

## 3 · External sources — checked at source in 4g

Three errors found and corrected there, recorded here because they are claim–evidence failures:
the between-movie-variability preprint was attributed to the wrong first author ("Gruber"; it is
Leipold et al.), though every figure quoted from it is correct in its version-1 full text; § 3.2
carried a best-region accuracy (0.77–0.85) that appears in neither source; and § 5.2 cited an
effect size (η²ₚ 0.715) without a source and as a cut-rate effect, when it is Cao et al.'s
editing-context effect on valence.

## 4 · Claims — matrix (`claim_evidence_2026-10-08.csv`)

36 claims: every claim in the abstract and § 1.4, every hypothesis status, three introduction
claims, and the three corrected source claims. Validated with the peer-review skill's
`validate_claim_evidence.py`: **valid, 29 supported, 7 partly supported, 0 unsupported.** The
seven partly supported claims are supported *with a qualifier the text already states* — scope
(01b one generator; stage 03 generated footage and its audio arms; H3 on the sensor only; the
controller-towards-faces prediction), magnitude (H2 below the SESOI), uncertainty (the frontal
miss: not detected is not absent), and causal language (03b's additivity is a reading of measured
ratios under a GRADED verdict). One expected warning: the mechanistic H3′ claim marked supported is
flagged for expert review, which is right — it rests on a model-based sensor (§ 3.4).

**Revised in this step** (each was stronger than its support): "the working assumption of every
editing manual written" → "of editing practice"; an unqualified claim that the literature does
not supply three things together → "in the work we found (§ 3.3)"; measurement unreliability as
"the dominant limit" on naturalistic-imaging effects → that it caps observable effects, which is
why accuracy is reported against a noise ceiling; Baldassano and Geerligs "establish" → "show".

A sweep for strong language (proves, establishes, first, never, causal, guarantee) found the
causal language scoped every time ("a causal lever *on this sensor*", "on intercut generated
footage") and "first" always internal to the programme.

## 5 · Structure

45 numbered headings, all unique; 114 § references, all resolving; every table row's column
count matches its header (escaped `\|` inside cells accounted for); abstract 397 words.

## Not covered

Figures — the paper has none yet. Whether each prose *interpretation* follows from its numbers
was checked for the abstract, contributions and hypotheses, not paragraph by paragraph through
§§ 5–8. Re-running every analysis from raw data (the numbers were traced to committed outputs,
not recomputed, except where noted above).
