# Handoff — 5 September 2026

Resume point for a fresh session. Read `ROADMAP.md` first, then this. The
technical write-up of everything below is `../PAPER.md`.

**This file replaces the 3 September handoff**, which was written when stage 02 was
blocked on a corpus question. That question is resolved and stage 02 is running.

## Where we are

| stage | status |
|---|---|
| **00 · Probe** — does the sensor work? | ✅ **PASS** — mean top-10 Jaccard 0.15 vs a 0.60 bar; double dissociation between the voice and place chains, with a graded middle condition; reproducible to 2 d.p. |
| **01 · Gate** — does technique move it? | ✅ **PASS** — 51/180 parcels at \|r\|>0.9 against log cut count, vs a bar of 15 and chance ~7. Identical footage; only the cutting varied |
| **02 · Index** — the crosswalk | 🔄 **Collection running.** 13 of 70 segments banked, a batch of 20 in flight. Analysis pre-registered and **unrun** |
| 01b · Synthetic-imagery transfer | Specified, unrun. **Reclassified** from a stage-02 animation gate to a **stage-03 prerequisite** |
| 02b · Generalisation test | Specified. Pulls only after stage 02 has a written RESULT |
| 03 · Isolation · 04 · Inversion | Specified in `ROADMAP.md`, not started |

## ⚠ A collection job is live — do not disturb it

At the time of writing, `auto_batch.py --batch 20 --loop` is running locally
(PID recorded in `02-index/auto_batch.pid`), driving the Space
`alecnpacey/tribe-probe`. It uploads a batch, restarts the Space, polls until every
clip has reported, harvests, and pauses — then starts the next batch. It stops on
its own at 70.

| | |
|---|---|
| Started | 5 Sep 2026, ~12:33 |
| Batch in flight | 20 segments, round-robin across the three films, ETA ~205 min from start |
| Banked before it started | **13** of 70 (`selected: 70   scored: 13   pending: 57`) |
| On a clean finish | 33 of 70; two further batches (20, then 17) complete the set |
| Remaining spend as the runner printed it | ~9.5 h GPU, **$9.69** for the 57 |

**Before doing anything with the Space, check whether that process is still alive.**
If it is, leave it. If it is not:

```sh
cd research/experiments/02-index
python auto_batch.py --status      # no cost, no side effects — prints scored/pending
tail -40 auto_batch.log            # progress lines are `clip N/M: <name> -> 180 parcels`
python run_batch.py --harvest      # idempotent: merges the log into the saved set, then pauses
```

`--harvest` is safe at any time and always pauses the Space. If the runner died
between "done" and "pause", the Space may be billing — confirm the stage is
`PAUSED`.

**No `LOG.md` line has been written for this batch yet.** One is owed when it
finishes, crash included, per the standing rule.

## What changed since the 3 September handoff

The old handoff described stage 02 as blocked on which films to use, and carried a
research assumption — *prefer animated Technicolor features* — recorded explicitly
as an assumption. **Both the block and the assumption are gone.**

1. **The animated-Technicolor assumption is dropped, on evidence.** Its availability
   premise is false: six public-domain live-action Technicolor features were verified
   against two animated colour features, one of those a duplicate of the other and one
   carrying French titling. What is abundant in the animation collections is colour
   *shorts*, not features. Evidence and archive identifiers in `02-index/CORPUS.md`.
2. **There is a second, better reason animation is out.** Gruber et al. (2024) chose
   animated films precisely because they are "stylistically and thematically similar"
   — a deliberate *minimum*-variance condition. Stage 02 exists to break dial
   covariance, so animation is the worst available instrument for this specific job,
   independently of whether TRIBE can see it.
3. **Corpus:** *Nothing Sacred* (1937) · *Jungle Book* (1942) · *Royal Wedding* (1951)
   — three public-domain live-action Technicolor features, different directors on
   purpose. *Nothing Sacred* is the direct colour replacement for *His Girl Friday*,
   which was rejected for being black and white.
4. **Colour was verified by measurement, not provenance** — 12 frames per print,
   mean saturation 81.9 / 85.5 / 115.6 against a threshold of 15. A greyscale dupe
   sits at essentially zero. All three prints clear by a wide margin.
5. **A new confound was found and handled:** the prints span 640×480 to 1480×1080,
   and the depth-of-field dial is a centre-versus-surround sharpness ratio, so
   resolution would have leaked into it. Every segment is re-encoded identically —
   720 lines, libx264 CRF 20, `yuv420p`, AAC 128 kbps — before any dial is measured.
6. **01b is no longer a stage-02 gate.** It is reclassified as a **stage-03
   prerequisite**: stage 03 generates clips, and generated video is out of
   distribution for an encoding head fitted on live action in the same ways animation
   is. Its criteria are held unmodified in `OBJECTIVES.md` § O2. **The
   reclassification is an argument, not a finding** — whether generated and
   hand-animated footage are out-of-distribution in the same way is untested.
7. **Stage 02 is built and measured.** 244 segments cut at fixed 60 s and normalised;
   14 dials measured by `cinemetrics.py`, 0 failures; 70 segments selected by
   stratified maximin sampling into `selection.json`.
8. **n was raised 60 → 70 on measurement.** At 60 the two cut-rate dials came in at
   0.79 and 0.80 power, below the floor, because roughly a third of cut rate's
   variance is *between* films and within-film centring removes it. Cut rate is the
   dial pass criterion 2 requires to replicate, so at 60 that check could not have
   failed informatively. At 70 all 14 dials clear the floor. The fix cost $1.70.
   See `02-index/DIALS.md`.
9. **`run_batch.py` was fixed before it could bias the sample.** It had drawn
   candidates alphabetically from `segments/`, which would have scored four
   consecutive segments from the opening of one film — convenience sampling
   silently substituted for the design. It now draws from `selection.json` and
   refuses to run without it.

## The no-peeking constraint — the single most important rule here

**Do not open `02-index/parcel_vectors.json`, and do not compute any dial→parcel
relationship.** The statistical test in `02-index/README.md` runs **once**, on all 70
segments. Reading those numbers early destroys the study's value, and nothing in the
output would show that it had happened.

Between-batch checks verify **pipeline health only**: 180 parcels per clip, no NaN,
no \|z\| > 8, filenames aligning between the dial table and the parcel table.

**One pre-specified exception**, and it is a resource decision rather than a test.
At 30 segments, run the permutation null on the dials measured so far; if no dial
has any parcel whose cross-validated `r` exceeds the 95th percentile of its own
permutation distribution *uncorrected*, stop for futility. This **replaces** the
older rule — *"if after 20 segments no dial reaches \|r\|>0.3, stop"* — which was
arithmetically inert: at n=20 the null probability of one dial exceeding \|r\|=0.3 is
0.247, so across six dials it fires about four times in five under pure noise.

Batch-0 segments **count toward the 70**, because batch 0 required no change to the
scoring path. Had it required one, its clips would have come from a different
pipeline and would have to be discarded and rescored.

## Do not re-derive these

| fact | |
|---|---|
| Output rate | **exactly 1 Hz** — 61 rows per 60 s clip |
| Parcels | **180** usable; `get_hcp_labels()` returns `{name: vertex_indices}`, and index 0 is `???` — drop it |
| Speed | **~10 min per 60 s clip** on A10G, ~10× slower than real time; ~$0.17 per segment at $1.00/hr |
| Gated Llama | avoid with `audio_only=True` — upstream docs call it the path for exactly this. All results are **video + audio only, no text branch** |
| `run_inference` | returns `(preds, abs_times)`, not an array |
| `load_fsaverage5_atlas()` | raises NotImplementedError — superseded by `build_roi_masks`, which returns the app's 5 **composites**, not parcels |
| Space `.gitignore` | contains `*.mp4`; clip uploads report success and are silently dropped unless allow-listed. `!probe_clips/*.mp4` is present and confirmed |
| Persistence | Space filesystem is **wiped on pause**. Results survive only in the log stream until harvested |
| Log fetch | `/logs/run` is a **live SSE stream that never closes while the Space is RUNNING**, so any reader blocks — foreground or background alike. This, not "pollers being killed", is why run 00 produced no log output. Readers now use a wall-clock deadline plus a socket idle timeout. Corrected 4 Sep 2026 |
| Idle billing | The gap between "done" and "paused" is the only real money leak. Batch 0 lost ~$0.60 to it; `auto_batch.py` now closes it in code and pauses on every exit path, failures included |
| `cinemetrics.py` | writes a **list** of per-clip records, not a dict keyed by path; and encodes no-face segments as `face_area_frac` 0.0 with `face_hit_rate` alongside, so "no face" stays distinct from "small face" |
| Dial measurement cost | **~28 s per 60 s segment at 720p**, measured on the real corpus. The ~2 s planning figure was wrong by ~14× |

## Standing rules

- Criteria written **before** the run, in the stage README, never softened after
- Introspect an API before writing against it — six of seven failures in run 00 were
  assumed shapes; seconds to check, ~35 min each to get wrong
- **A wrong entry in a "do not re-derive" table is worse than no entry**, because it
  is trusted exactly where it will not be re-checked. The log-fetch row above was one
- Persist to disk, not to the Space — its filesystem is wiped on pause
- Batch into one run; each Space restart is ~7 min
- Pause the Space when done; sleep timer is 7200 s so it will not nap mid-run
- Dropped, null and untested dials are **three different results** and are reported as
  such. No dial is dropped

## Spend

| | |
|---|---|
| Through stage 01 and the corpus research, recorded 3 Sep | **$4.35** |
| Stage 02 scoring, 13 segments at $0.17 | ~$2.21 |
| Batch-0 idle overrun | ~$0.60 |
| **To date** *(derived from those three lines, not read from a bill)* | **~$7.2** |
| Remaining for the 57 unscored, as `run_batch.py` printed it | **$9.69** |

## Files

```
research/
  PAPER.md                the technical paper, sections 1–9
  cinematography/         cinemetrics.py and the dial literature
  decoding/               parcel annotation and validity notes
  experiments/
    ROADMAP.md            four stages, costs, pull conditions
    OBJECTIVES.md         the 3–4 Sep session's objectives and outcomes
    LOG.md                every run, newest first, failures included
    HANDOFF.md            this file
    00-probe/    README · RESULT · CLIPS · probe.py · space_app.py
    01-cutrate/  README · RESULT · build_conditions.py
    02-index/    README (criteria pre-registered) · CORPUS · DIALS
                 cut_corpus.py · verify_colour.py · measure_dials.py ·
                 analyse_dials.py · run_batch.py · auto_batch.py · watch_run.py
                 segments/ (244) · dials/ (244) · dial_table.json ·
                 selection.json (70) · parcel_vectors.json ⛔ do not open
```

The repo root also holds the production brief for *The Simulated Viewer* —
`index.html` and `styles.css`. See the top-level `README.md`.

## First actions next session

1. **Check whether the collection job is still running** before anything else.
   `python auto_batch.py --status` costs nothing. If it died, `--harvest` first,
   confirm the Space is `PAUSED`, then relaunch `auto_batch.py --batch 20 --loop`.
2. **Write the `LOG.md` lines** for every batch that has completed, crashes included.
3. At 30 banked segments, the **futility check** above becomes available. It is
   optional and it is not the test.
4. When all 70 are banked: run the pre-registered analysis **once**, and write
   `02-index/RESULT.md` against the criteria exactly as fixed — both pass criteria,
   the permutation null, and every null dial reported with equal prominence, labelled
   TESTED or UNDERPOWERED so a null is never confused with an absence of test.
5. The result must be reported as **corpus-conditional**. Three films is enough to
   break dial covariance, not enough to claim film-independence.
6. Then, and only then, 02b and 01b — in that order of dependency: 01b runs
   immediately before 02b so that a failure can be attributed.
