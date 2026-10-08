# Consolidation plan — from exploration draft to preprint

Started 20 September 2026. Source: `reviews/REVIEW-2026-09-16-exploration-paper.md` (comments
M1–M9, future work F1–F10). **Scope decision:** this paper is the exploration-phase paper
(stages 00–03, 01b, 02b). Stage 04 and real-fMRI validation are paper two.

Rules: tick a box only when its done-criterion is met and the evidence is committed. Every run
gets a `LOG.md` line. Paid steps get criteria in a README *before* spend. Update the status
line below at the end of each session.

**Status (7 Oct 2026):** **Steps 1, 2a–2d and 3a complete; 4d complete — 03b is in the paper** (§ 6.9, with abstract, § 6.8, § 8, § 9 aligned). 2e (text branch, ≈ $1.25, capped) awaits the author's decision. **3a complete (7 Oct): the frontal flip is not demonstrated; speech is a missing auditory dial.** 3a is in the paper (§ 6.10, 8 Oct). Next: step 4a, the restructure.

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

- [ ] **4a · Restructure** to the outline in review § 8; results written once, history in § 7.
- [ ] **4b · SESOI as heuristic (M3); criterion 1 leniency stated.**
- [ ] **4c · Stage 03 audio construction stated exactly (M4); verdict-table lesson in § 7.**
- [x] **4d · Encoder-artefact alternative named (M5),** with step 2's result. *Done 7 Oct: § 6.9 and § 8 — pure form weakened (half the frontal effect arrives with no discontinuity), broad form ("any large visual change") not excluded. Every 03b figure verified against `evaluation.json` / `cut_locked.json`; two derived figures corrected (LOG).*
- [ ] **4e · Limitations and Future Work** from review § 9, edited to the results of steps 1–3.
- [ ] **4f · Abstract ≤ 400 words,** exploratory results flagged (m7); minor comments m2–m13.
- [ ] **4g · References** verified and formatted (citation-management skill).
- [ ] **4h · Availability statement;** decide repo visibility; stage 03 README cited by commit hash.
- [ ] **4i · Claim–evidence audit** of the final text, programmatic where possible.
- [ ] **4j · Preprint** on OSF Preprints.

## Paper two — not in this plan

F1 real-fMRI validation of the dials · F4 corpus expansion with film random slopes · F6 face-area
ladder · F9 stage 04 as projection, then as a controller.
