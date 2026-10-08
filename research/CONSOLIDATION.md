# Consolidation plan — from exploration draft to preprint

Started 20 September 2026. Source: `reviews/REVIEW-2026-09-16-exploration-paper.md` (comments
M1–M9, future work F1–F10). **Scope decision:** this paper is the exploration-phase paper
(stages 00–03, 01b, 02b). Stage 04 and real-fMRI validation are paper two.

Rules: tick a box only when its done-criterion is met and the evidence is committed. Every run
gets a `LOG.md` line. Paid steps get criteria in a README *before* spend. Update the status
line below at the end of each session.

**Status (7 Oct 2026):** **Steps 1, 2a–2d and 3a complete; 4a–4g and 4i complete — 03b is in the paper** (§ 6.9, with abstract, § 6.8, § 8, § 9 aligned). 2e (text branch, ≈ $1.25, capped) awaits the author's decision. **3a complete (7 Oct): the frontal flip is not demonstrated; speech is a missing auditory dial.** 3a is in the paper (§ 5.7.2 after the restructure). **4a–4g and 4i complete (8 Oct).** Left: 4h availability statement and repo visibility, then 4j preprint — both outward-facing, the author's decision.

## Step 1 · Integrity fixes — free

- [x] **1a · Reproduce § 6.7 (review M2).** *Done 20 Sep: 45/45 figures reproduced; reading corrected — the ~3 dimensions are the sensor's response space (shuffled-label fit as concentrated, p 0.42); technique-specific = face area leads axis 1 (p 0.010) and +5 points retained variance over the shuffled floor (p 0.005). Paper abstract, § 2, § 6.7, § 8 corrected.* `experiments/02-index/index_map.py` rebuilds **B** from
      `analysis_result.json`, reproduces every § 6.7 figure, adds a permuted-label baseline, writes
      `index_map.json`. *Done when:* each figure matches the paper to stated precision or the
      paper is corrected; the script is cited from § 6.7.
- [x] **1b · Ladder count null (M1).** *Done 20 Sep: `experiments/ladder_count_null.py`; p = 0.017 (stage 01), 0.025 (stage 03, both arms); no "times chance" left; p-floor limitation added to § 8.* Commit the level-permutation script; replace every
      "× chance" statement (Abstract, § 5.2, § 6.8) with the permutation *p*, the null's 95th
      percentile and the participation ratio. *Done when:* no "times chance" remains in `PAPER.md`.
- [x] **1c · Per-film coefficients (M7).** *Done 20 Sep: `experiments/02-index/per_film.py`; table in § 6.4 — face/place signature same sign in all three films; frontal parcels conflict.* Table of cut-rate and face-area coefficients per film
      for the named parcels. *Done when:* table in § 6.4 or a supplement, from a committed script.
- [x] **1d · OSF amendment posted (M8, m1).** *Done 20 Sep 2026 (submitted and accepted by the author; registration still embargoed to Sep 2027, so not externally verifiable). Eight fields corrected: six for the futility check, two for the never-recorded scene-boundary count. Text in `experiments/02-index/OSF-AMENDMENT.md`; PAPER abstract, § 4.8, § 7 aligned.* **Author action** — `~/Desktop/osf-registration-attachments/15-AMENDMENT.md`.
      *Done when:* posted; § 4.8 / § 7 wording matches the fact and the date.

## Step 2 · One paid session, ≈ $5–8 — criteria first

- [x] **2a · README with criteria** *(written 20 Sep, committed before any clip exists; awaiting the author's read before 2b–2d)* for the discontinuity-vs-switch test (M5 / F2), the text-on
      rescoring (M6 / F3) and timeline saving (F8), in `experiments/03b-discontinuity/README.md`.
- [x] **2b · Build clips, $0:** *Done 20 Sep: 15 clips built and measured (`03b-discontinuity/CLIPS.md`). D's joins detected as cuts 11% (rule ≤ 25%); B/C hard cuts with histogram distance 0.16/0.23 vs REF 0.78; audio MD5 identical across all 20 clips.* same-scene self-intercut ladder from `face_close.mp4`; black-frame
      insert ladder; measured with `cinemetrics.py`.
- [x] **2c · Space app saves the 1 Hz timeline** *(done 20 Sep; identity PASS, raw Δ 0.00)* per clip to the results repo; identity-tested
      against an existing result.
- [x] **2d · Score** *Done 25 Sep: 20/20 in three sessions (session 1 overspent, see LOG; sessions 2–3 bounded by a server-side guard). Verdict GRADED; `03b-discontinuity/RESULT.md`.* (HF credit needed), harvest by exact name, evaluate, `RESULT.md`, LOG.
- [ ] **2e · Text branch on:** *(not run; README allows it if ≥ $3 credit remains — author's call after the overspend)* five clips rescored, whole-vector and named-parcel Δ reported, or
      the failure bounded and stated.

## Step 3 · Free analysis alongside

- [x] **3a · Content descriptors (F5):** *Done 7 Oct: plan committed before any descriptor (55a8515), amendment before any parcel data (73cac7e). **Q0 NOT DEMONSTRATED** — the frontal sign flip is not significant (cut × film F 1.38, perm p 0.28; NS − JB +0.53, CI −0.14 to +1.08); speech, semantic change and semantic distance per cut all **DO NOT CARRY**. Post-hoc: speech explains within-film auditory variance (r +0.78; LOO R² dials −0.09 → dials + speech +0.54) and part of the corpus auditory cut-rate signature (−0.27 → −0.19). 8 Oct: folded into PAPER as § 6.10 — the seven 'flips between films' statements re-worded, the abstract's 'co-occurs with dialogue' corrected, speech added to § 8; per-parcel interaction tests added post-hoc (IFJa p 0.19, others 0.44–0.58).* speech proportion and semantic embeddings per segment on
      the 244 segments; test whether they carry the *Nothing Sacred* / *Jungle Book* sign flip.
      Note in `experiments/02-index/content_descriptors.md`.

## Step 4 · Consolidation pass — after steps 1–3

- [x] **4a · Restructure** to the outline in review § 8; results written once, history in § 7. *Done 8 Oct in two commits. Phase 1 (`a079dab`): pure move, 1,486/1,486 body lines preserved. Phase 2: results § 5 = 00, 01, 02, **new 5.4 (01b/02b, previously absent)**, 03, 03b, 5.7 'why the corpus lacks the frontal effect' (placed after 03b, not under 02 as the review proposed, because it uses stage 03's slopes and 03b's re-estimate); index map § 6; § 7 gains the count-null and map-without-a-script lessons and the paid-run missteps; § 8 Limitations and future work; § 9 status table only. Added: H3′ row, contribution 4 (reconciliation; detectability demoted to a method note), § 3.4 (model-based sensor / encoder artefact), § 4.10 (ladder null). § 5.3.6 rewritten once with stage 03 known. Every results subsection opens with what it licenses. 89/89 § refs resolve. **Left to other items:** abstract length (4f), SESOI (4b), stage 03 audio and verdict-table lesson (4c), limitations / future-work text (4e), § 4 narrative trimming and terminology drift (index / crosswalk / map / console) (4f).*
- [x] **4b · SESOI as heuristic (M3); criterion 1 leniency stated.** *Done 8 Oct: § 3.2 a justified heuristic with range ≈ 0.12–0.47 (mediation assumption; parcel-wise accuracy; marginal statistic), 0.5 kept as registered. New exploratory `02-index/sesoi_marginal.py` computes the quantity the SESOI applies to: **6 of 2,520 marginal dial–parcel r reach 0.5, none with its 95% CI clear; semi-partial 0** (max 0.498) — harsher than the registered 9-of-180 on CV r. Criterion 1 stated as unable to produce a null (§ 5.3.5, § 8.1). Abstract, H2 row, contribution 1, § 8.1 aligned.*
- [x] **4c · Stage 03 audio construction stated exactly (M4); verdict-table lesson in § 7.** *Done 8 Oct from `build_stage03.sh` / `build_conditions.py`: S+ cuts the soundtrack with the picture (30 s of dialogue in 1–16 pieces, audio discontinuity at every cut); S− maps the landscape's ambient track over the whole clip. PARTIAL-A's reading stated as untestable by design; A5 arm difference attributed to neither; § 8.1 limitation with the third arm needed; § 7 'a verdict table should carry outcomes, not mechanisms'.*
- [x] **4d · Encoder-artefact alternative named (M5),** with step 2's result. *Done 7 Oct: § 6.9 and § 8 — pure form weakened (half the frontal effect arrives with no discontinuity), broad form ("any large visual change") not excluded. Every 03b figure verified against `evaluation.json` / `cut_locked.json`; two derived figures corrected (LOG).*
- [x] **4e · Limitations and Future Work** from review § 9, edited to the results of steps 1–3. *Done 8 Oct: § 8.1 regrouped (instrument / observational index / controlled designs / reconciliation), every existing limitation kept, plus the review's encoder-artefact, generated-footage and exploratory-map items; § 8.2 is F1–F10 with tiers and falsifiers, each item stating what this paper already ran (F2 = 03b, F5 = 3a, F7 = § 4.10, F8 = timelines, F10 = amendment) and what remains. Old § 8.2 prose folded into F3, F6, F9; every number it held is still stated in its results section.*
- [x] **4f · Abstract ≤ 400 words,** exploratory results flagged (m7); minor comments m2–m13. *Done 8 Oct: abstract 1,705 → 397 words in the review's five-paragraph shape, exploratory results marked; every number the old abstract carried is still stated in a results section. m5 power table marked indicative; m6 determinism established empirically (stage 00 re-run, 03b identity test), subject handling stated as not inspected; m10 the film's drift is a hypothesis tested; m11 § 4.3 correction to two sentences; m12 one spend table in § 4.9 (≈ $40–43 to date; RESULT/log disagreements shown, the 13 Sep text-branch run estimated); m13 § 9 table gains 'what it licenses'; M9 'crosswalk' / 'console' → 'index'. m2–m4, m7, m8 done earlier in 4a–4b; m1 already true; m9 (sources) is 4g.*
- [x] **4g · References** verified and formatted (citation-management skill). *Done 8 Oct: every entry fetched from its primary record (CrossRef, PubMed, arXiv, bioRxiv, DataCite); `references.bib` written and validated (11 entries, 0 errors). **Three source errors corrected:** (1) 'Gruber et al. (2024)' is **Leipold et al.** — same bioRxiv DOI, wrong author in all versions; its quoted figures (112 participants, eight animated movies, 210 parcels, F(7,385) 4.65, one shared parcel, 'treated similarly to a particular task') all verified in the v1 full text. (2) § 3.2's 'best regions, normalised 0.77–0.85' is in neither source; TRIBE says only 'near the noise ceiling' in auditory and language cortex — row replaced, heuristic lower bound 0.12 → 0.10. (3) § 5.2's η²ₚ 0.715 was unsourced and misdescribed: it is Cao et al. (2024)'s editing-*context* effect on valence, not a cut-*rate* effect — cited and reworded. Also: TRIBE figures 0.3195 / 0.2146 / 0.54 verified at source and cited; the parcellation stated exactly (TRIBE evaluated on 1,000 Schaefer parcels; the Space reads fsaverage5 at 180 HCP-MMP1 areas). No preprint has a published version. The Scientific Agent Skills library is credited under Tools, as its licence asks — author's call to keep.*
- [ ] **4h · Availability statement;** decide repo visibility; stage 03 README cited by commit hash.
- [x] **4i · Claim–evidence audit** of the final text, programmatic where possible. *Done 8 Oct: `reviews/AUDIT-2026-10-08-claim-evidence.md`. 777 decimals traced to committed outputs or verified sources (39 first-pass misses, 0 after triage); headline counts and every verdict checked against the result files; 36-claim matrix (`reviews/claim_evidence_2026-10-08.csv`) valid — 29 supported, 7 supported with a qualifier the text states, 0 unsupported. Four introduction overstatements softened. Not covered: paragraph-level interpretation through §§ 5–8; figures (none yet).*
- [ ] **4j · Preprint** on OSF Preprints.

## Paper two — not in this plan

F1 real-fMRI validation of the dials · F4 corpus expansion with film random slopes · F6 face-area
ladder · F9 stage 04 as projection, then as a controller.
