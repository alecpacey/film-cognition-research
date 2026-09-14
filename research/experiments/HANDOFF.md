# Handoff — 13 September 2026

Resume point for a fresh session. Read `ROADMAP.md` first, then this. The write-up is
`../PAPER.md`; every figure below is sourced there or in a stage `RESULT.md`.

**This handoff closes the exploration phase.** Four experiments are complete and
reported against criteria fixed in advance. Nothing is running. The Space is PAUSED.

## Where we are

| stage | status |
|---|---|
| **00 · Probe** | ✅ PASS — Jaccard 0.15 vs 0.60; voice/place double dissociation |
| **01 · Gate** | ✅ PASS — 51/180 parcels at \|r\|>0.9 on identical footage; strongest responders inferior-frontal (IFJa +0.996), not dorsal attention |
| **02 · Index** | ✅ **PARTIAL** — registered at `osf.io/dg7fe` before the analysis ran. Criterion 1 met (14/14 dials, 101/180 parcels); criterion 2 **not** met (cut rate does not replicate in IFJa/IFJp/IFSp/8C). Only 9/180 parcels reach the derived SESOI of 0.5 |
| **01b · Transfer** | ✅ **PASS** — generated H3 Max clips reproduce the index's face/place axis at r = +0.699 (bar 0.50; live-action reference +0.936); Jaccard 0.083; direction both. **Cutting confounded with content** (generator cuts 7/10/15 per min) |
| 02b · Generalisation | ✅ run (exploratory, n=3) — index predicts generated clips at r 0.41/0.90/0.89; contrast +0.77; landscape weakest; `contrast_p5_p95` extrapolated |
| 03 · Isolation | not started — gate passed; **first design must control cutting per shot** |
| 04 · Inversion | not started — **bounded in advance** (§6.7): the reachable set is ~3-dimensional |

## The findings that carry forward

1. **The index exists but is broad and weak.** 101 parcels survive; 9 matter. Through TRIBE's
   0.2146 out-of-distribution accuracy a median survivor implies r ≈ 0.07 against cortex.
2. **The two tracks disagree on cut rate, and the measured dials do not explain it.** Cut rate is
   the most nearly independent dial (max |r| 0.194 with any other); the confound, if it is one,
   is unmeasured — speech, semantics, scene type. The text branch was off throughout.
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

## ⚠ Stage 03 scoring was in flight at close (14 Sep 2026, ~16:30)

Ladder built and measured (cuts exactly 1/3/7/15/31, both arms), original scoring app
verified on the Space, 12 clips submitted. **6 of 12 scored** when the local watcher was
lost to the machine sleeping; the Space finishes the remaining six on its own (Sminus
cut03/07/15/31, base_face, base_landscape) and pauses on its inactivity timer.
Two earlier missteps are recorded honestly: a text-branch rescoring run produced 0/12 after
189 min (parked, cause undiagnosed, `02-index/text_branch/`), and a watcher filter matching
`"03_"` anywhere harvested six foreign files — a separate experiment `x1-av-emotion` writes
to the same results repo — and paused the run at 6/12; corrected to exact-name matching.

**Resume, in order (fresh session, from `03-isolation/`):**
1. `python3 -c "from huggingface_hub import HfApi; print(HfApi().space_info('alecnpacey/tribe-probe').runtime.stage)"` — if not PAUSED, pause it.
2. Harvest with the corrected `watch_03.sh` logic (exact names from `names.json`), or run its
   inner Python once by hand → `parcel_vectors.json` must hold exactly the 12 keys
   `Splus_cut01…31`, `Sminus_cut01…31`, `base_face`, `base_landscape`.
3. `../02-index/.venv-analysis/bin/python evaluate_03.py` → verdict per README table.
4. Write `RESULT.md` (verdict, both arms' tables, face base 0.052 limitation, spend ≈ $2.2
   scoring + $3.60 bases, the two missteps), `LOG.md` line, status rows in ROADMAP/PAPER §9/
   this table. Commit and push.

## First actions next session

1. Decide among: free 02b (n=3), stage 03 spec (cut rate first, per-shot cut control, criteria before spend), or the paper's finishing pass (claim–evidence audit, references).
2. Before any stage-03 spend: add HF credit; confirm fal balance; write `03-isolation/README.md` with criteria first.
3. If publishing resumes: post the amendment, then verify references, then OSF Preprints.
