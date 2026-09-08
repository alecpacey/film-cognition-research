# Run log

Newest first. One line per run: date, experiment, where it ran, outcome.

| Date | Experiment | Ran on | Outcome |
|---|---|---|---|
| 2026-09-08 | 02-index pre-registration | osf.io, no GPU | **REGISTERED** — analysis plan filed at `osf.io/dg7fe` (OSF Preregistration, embargoed to 8 Sep 2027; project `osf.io/qtjwf`). Foreknowledge declared as "limited observation could not influence analysis decisions", not as pre-collection. Six files attached including the frozen 70-segment `parcel_vectors.json` (SHA-256 `93807b80…53a3189`, verified identical to the live repo copy). Criteria docs byte-identical to the 5 Sep baseline `89d01a1` across the full 13→70 span. **Analysis still NOT run** |
| 2026-09-07 | 02-index collection | HF Space `alecnpacey/tribe-probe`, A10G Small | **COMPLETE — 70/70 segments**, 180 parcels each, no NaN, all z standardised, films 24/23/23. Five infrastructure failures en route (log window, sleep timer, upload hang, repo quota, osf.io timeout), none touching the data; identity test proved the channel changes were bit-identical (max Δ 5e-7). ~$16 total vs $11.90 estimated. Analysis NOT yet run |
| 2026-09-04 | 02-index batch 0 | HF Space `alecnpacey/tribe-probe`, A10G Small | **PASS** — 4/4 clips, 180 parcels each, no NaN, |z| max 3.59, pairwise whole-vector r from -0.48 to +0.60 so the clips genuinely separate. Pipeline proven on all three new prints. Found and fixed: the logs endpoint is a live SSE stream that never closes, so `fetch_logs` blocked — the real cause of run 00's "background pollers killed silently" |
| 2026-09-04 | O3 dials | local, no GPU | 244 segments cut, normalised and measured; 0 failures. **12/14 dials TESTED, but both cut-rate dials UNDERPOWERED at n=60 (power 0.79)** — the dial pass criterion 2 requires to replicate. Condition number 58.8; lighting/colour cluster near-redundant (median_luma~shadow_frac r=-0.90, VIF 9.5). See `02-index/DIALS.md` |
| 2026-09-03 | O1 corpus research | local, no GPU | **Animated-Technicolor assumption DROPPED** — its availability premise is false (6 PD live-action Technicolor features verified vs 2 animated). Corpus set to Nothing Sacred 1937 / Jungle Book 1942 / Royal Wedding 1951; fixed 60 s segmentation; encode-normalisation confound found. 01b deferred unrun. See `02-index/CORPUS.md` |
| 2026-09-01 | 00-probe | HF Space `alecnpacey/tribe-probe`, A10G Small | **PASS** — mean top-10 Jaccard 0.15 (threshold <0.60); direction correct on all three clips. Rate confirmed 1.000 Hz. ~10x slower than realtime. See `00-probe/RESULT.md` |
| 2026-09-01 | 00-probe | same | FAIL (instrument) — `get_hcp_labels` returns a dict, not a label list; parcels mis-keyed |
| 2026-09-01 | 00-probe | same | FAIL (instrument) — reduced to the app's 5 composite scores instead of HCP parcels; Jaccard 1.00 by construction |
| 2026-09-01 | 00-probe | same | FAIL — Space killed mid-run (10 min auto-sleep and/or client disconnect cancelling the job) |
| 2026-09-01 | 00-probe | same | FAIL — `run_inference` returns `(preds, abs_times)`, not an array |
| 2026-09-01 | 00-probe | same | FAIL — gated `meta-llama/Llama-3.2-3B` 401; fixed with `audio_only=True` |
| 2026-09-01 | 00-probe | same | FAIL — `load_fsaverage5_atlas()` raises NotImplementedError |
| 2026-09-01 | 00-probe | same | FAIL — clips absent: Space `.gitignore` has `*.mp4`, uploads silently dropped |
| 2026-09-01 | 00-probe | same | FAIL — `show_copy_button` invalid in gradio 6.11 |
| 2026-09-01 | 00-probe | HF Space, L4 requested | FAIL — "Scheduling failure: not enough hardware capacity" (HF-side, no billing) |
