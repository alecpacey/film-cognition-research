# Handoff — 15 September 2026

Resume point for a fresh session. Read `ROADMAP.md` first, then this. The write-up is
`../PAPER.md`; every figure below is sourced there or in a stage `RESULT.md`.

**This handoff closes the exploration phase.** Stages 00–03, plus 01b and 02b, are complete
and reported against criteria fixed in advance. The 15 September decisions below have been
executed. Nothing is running. The Space is PAUSED.

## Where we are

| stage | status |
|---|---|
| **00 · Probe** | ✅ PASS — Jaccard 0.15 vs 0.60; voice/place double dissociation |
| **01 · Gate** | ✅ PASS — 51/180 parcels at \|r\|>0.9 on identical footage; strongest responders inferior-frontal (IFJa +0.996), not dorsal attention |
| **02 · Index** | ✅ **PARTIAL** — registered at `osf.io/dg7fe` before the analysis ran. Criterion 1 met (14/14 dials, 101/180 parcels); criterion 2 **not** met (cut rate does not replicate in IFJa/IFJp/IFSp/8C). Only 9/180 parcels reach the derived SESOI of 0.5 |
| **01b · Transfer** | ✅ **PASS** — generated H3 Max clips reproduce the index's face/place axis at r = +0.699 (bar 0.50; live-action reference +0.936); Jaccard 0.083; direction both. **Cutting confounded with content** (generator cuts 7/10/15 per min) |
| 02b · Generalisation | ✅ run (exploratory, n=3) — index predicts generated clips at r 0.41/0.90/0.89; contrast +0.77; landscape weakest; `contrast_p5_p95` extrapolated |
| 03 · Isolation | ✅ **PARTIAL-A** — frontal cut effect in both arms (S+ 3/4, S− 1/4 at r>0.9, all ≥0.87); auditory signature reproduces stage 02; cut rate is a causal lever. See `03-isolation/RESULT.md` |
| 04 · Inversion | not started — **bounded in advance** (§6.7): the reachable set is ~3-dimensional |

## The findings that carry forward

1. **The index exists but is broad and weak.** 101 parcels survive; 9 matter. Through TRIBE's
   0.2146 out-of-distribution accuracy a median survivor implies r ≈ 0.07 against cortex.
2. **The two tracks disagreed on cut rate; stage 03 reconciled them.** Cutting drives
   inferior-frontal cortex up and auditory cortex down, in both speech arms. The corpus carries
   only the auditory half — not the penalty's fault, the frontal signal is absent at the size the
   causal slopes predict (`02-index/frontal_miss.md`). Standing hypothesis: frontal cortex tracks
   *scene switches*, which equal cuts in the intercut ladders and not in cinema. Untested; the
   scene-boundary diagnostic CORPUS.md specified was never implemented.
3. **Fourteen dials move this cortex along ~3 axes**: face/place 69%, motion 14%, colour 6%.
   Axis 1 is run 00's contrast (r = +0.936) and the axis generated imagery reproduces (+0.699).
   **Inversion is projection, not solution; the inverse is many-to-one.**
4. **The film's premise has measured support**: face area is the dominant dial (largest coefficient
   in 65 of 101 survivors). A controller maximising this index goes to faces. Mechanism, not proof
   of the forty-clip drift.

## Do not re-derive

| fact | |
|---|---|
| Output | 1 Hz, 180 usable parcels (index 0 `???` dropped), ~10 min/clip on A10G ≈ $0.17 |
| Scoring path | **manifest-driven**: clips → dataset `alecnpacey/tribe-probe-clips`, `batch.json`, restart; results as files in `alecnpacey/tribe-probe-results`; log is fallback only (bounded window). `02-index/run_batch.py`, `auto_batch.py`; `01b-transfer/score_01b.py` for named clips |
| Space billing | needs **HF prepaid credit** — `restart_space` 402s when empty. Idle gap is the leak; `auto_batch.py` pauses on every exit path |
| Generator | `minimax/h3-max/text-to-video` on fal (no `fal-ai/` prefix); 5–15 s/gen, 480P/768P/1080P, **native audio**, no audio input; `…/director` is a WebRTC session, not a job. Introspect schema with the key; public OpenAPI URLs 404. **The generator cuts within a 15 s output** |
| fal key | `01b-transfer/.env` (gitignored) |
| Analysis env | `02-index/.venv-analysis` (sklearn, scipy, no statsmodels — use `scipy.stats.false_discovery_control`); HF tooling in system `python3` |
| cinemetrics | `cinemetrics.py CLIP --json OUT`, run from `02-index/` (needs `yunet.onnx`); nested keys (`cuts.cuts_per_min`, `shot_scale.face_area_frac`); largest-face nulls on tiny faces |
| Registration | `osf.io/dg7fe`, embargoed to 7 Sep 2027. **Amendment drafted, not posted**: `~/Desktop/osf-registration-attachments/15-AMENDMENT.md` — the futility check *was* run on 6 Sep (CONTINUE); three registration sentences say otherwise |
| Frozen data | `02-index/parcel_vectors.json` sha `93807b80…`; four criteria docs byte-identical to `89d01a1` |

## Deviations and unfinished business, honestly

- OSF amendment unposted (user deferred all registration work). Paper §7 already describes it.
- Elastic-net hyperparameters (α 0.1, l1 0.5, 5-fold) were not pre-registered; disclosed.
- Within-film adjacency never tested (restricted permutation held: 99 vs 101).
- Two accidental empty fal requests on 11 Sep, expected $0, **unverified** on the dashboard.
- `arXiv 2607.01400` (README, engagement null) never resolved anywhere in this repo.
- `LOG.md` gap 4–7 Sep partly reconstructed only.
- No publication: user chose to hold. arXiv needs an endorser; OSF Preprints does not.

## Spend

Stage 02 ≈ $16 · 01b $3.60 generation + ≈ $0.65 scoring · earlier stages $4.35. **≈ $25 total.**

## Pending, outside the repo

- **Meta gated access to `meta-llama/Llama-3.2-3B`**: **granted 13 Sep 2026**, verified readable with the account token. Unlocks the text-branch rescoring (~20 segments at the extremes of cut rate,
  ≈ $3.40, `audio_only=False`) — the cheapest experiment left that could resolve the H2b
  disagreement. Needs HF prepaid credit at run time.

## Stage 03 scoring — closed 15 Sep 2026 (was in flight at the 14 Sep close)

Ladder built and measured (cuts exactly 1/3/7/15/31, both arms), original scoring app
verified on the Space, 12 clips submitted. **6 of 12 scored** when the local watcher was
lost to the machine sleeping; the Space finishes the remaining six on its own (Sminus
cut03/07/15/31, base_face, base_landscape) and pauses on its inactivity timer.
Two earlier missteps are recorded honestly: a text-branch rescoring run produced 0/12 after
189 min (parked, cause undiagnosed, `02-index/text_branch/`), and a watcher filter matching
`"03_"` anywhere harvested six foreign files — a separate experiment `x1-av-emotion` writes
to the same results repo — and paused the run at 6/12; corrected to exact-name matching.

**Closed 15 Sep:** harvested 12/12, `evaluate_03.py` → PARTIAL-A, `RESULT.md`, LOG line and
status rows written (commits `cdbb07b`, `53cbee8`). Space PAUSED.

## Decisions taken 15 September 2026 — executed 15 September, in order

1. **Investigate why the stage-02 index missed the frontal half of the cut effect.** Free,
   analysis-only. Stage 03 showed cutting drives IFJa/IFSp/8C *up* (r ≈ +0.9) and A4/A1/MBelt
   *down* (≈ −0.95) in both speech arms; the index (§ 6.5) recovered the auditory half and not
   the frontal one. Examine: those four parcels' full elastic-net fits and permutation p in
   `analysis_result.json`; within-film variance of cuts_per_min per film; whether the penalty
   zeroed a real cut-rate weight (refit those parcels OLS/ridge as an exploratory check,
   labelled); whether the auditory signature carries the frontal one's variance. Output: a
   short note in `02-index/frontal_miss.md`. This decides whether the index or the corpus is
   at fault before stage 04 builds on either.
   → **Done.** `02-index/frontal_miss.{py,md,json}`, `frontal_miss_transplant.json`. Verdict:
   **the corpus, not the index.** OLS/ridge refits of the four parcels give cut weights
   +0.04–0.07, |t| < 1 — the penalty zeroed nothing real. Within-film r(IFJa, cuts) −0.005,
   sign flips between films; auditory quartet −0.29 to −0.34 in every film. Transplanting the
   stage-03 slopes into the corpus's variance predicts frontal r +0.30–0.45 (observed ≈ 0)
   while auditory arrives at prediction. Stage-02 cut map vs stage-03 S− map r +0.52 over 180
   parcels; sign right in 22/23 both-arm parcels. Hypothesis left: frontal cortex tracks
   *scene switches*. **Found:** the scene-boundary diagnostic specified in CORPUS.md was never
   implemented (no field anywhere); PAPER § 4.3 corrected.
2. **Full paper update with stage 03** — abstract, § 2 H3 row → supported, a stage-03
   results section (verdict table, both arms, the reconciliation of stages 01 and 02, the
   PARTIAL-A near-miss stated as such), § 8, § 9. Source: `03-isolation/RESULT.md` only;
   verify every figure against `03-isolation/evaluation.json`.
   → **Done.** Header/status, abstract (stage-03 paragraph), § 2 (H2b note, H3 supported),
   § 4.3 correction, § 6.5 pointer, new § 6.8 (stage 03 + labelled exploratory follow-up),
   § 8 (two paragraphs replace the "untested alternative" one), § 9 prose (five points; the
   stale "01b remains a prerequisite" paragraph replaced), internal-documents list. Every
   stage-03 figure read from `evaluation.json`; A5's S+ value (+0.152) added, which RESULT.md
   did not state.
3. **Text-branch failure: parked.** Do not diagnose unless a text-on replication is later chosen.
   → Parked as decided; `02-index/text_branch/` untouched.
4. **Results repo split:** `alecnpacey/x1-av-emotion-results` has been created (private, empty).
   Whoever runs `x1-av-emotion` must repoint its writer there; this programme's scorers keep
   using `alecnpacey/tribe-probe-results` with exact-name matching.
   → **Done in code; nothing run against HF.** `x1-av-emotion/run_x1.py` now targets
   `alecnpacey/x1-av-emotion-results`: `--run` sets the Space variable `RESULTS_REPO` while
   the Space is paused, verifies the read-back, and restores the shared repo on every exit
   path; `--migrate` (replaces `--cleanup`) copies the 8 pilot files into the new repo,
   verifies, then deletes them from the shared repo, refusing unless all 8 are banked locally
   (they are). Verified 15 Sep: new repo private and empty; the 8 `x1_*` files are still in
   the shared repo; Space PAUSED with `RESULTS_REPO=alecnpacey/tribe-probe-results`;
   `score_03.py` / `watch_03.sh` match exact names. **`--migrate` has not been run** — run it
   before any stage-02 harvest touches the shared repo. `x1-av-emotion/README.md` documents
   the split.

Not chosen yet: stage 04 spec; text-on stage-03b. Machine note: background jobs were killed
twice for memory on 14 Sep — keep long watchers light or off-laptop.

## First actions next session

1. Free: implement a between-scene cut count in `cinemetrics.py`, run it on the 244 segments,
   regress IFJa/IFSp/8C on it — the test of the scene-switch hypothesis in `frontal_miss.md`.
   Decide the stage 04 spec after that result.
2. `python3 x1-av-emotion/run_x1.py --migrate` — moves the 8 pilot files out of the shared
   results repo. Do before any stage-02 harvest.
3. If publishing resumes: post the amendment, then the paper's finishing pass (claim–evidence
   audit, references), then OSF Preprints.
