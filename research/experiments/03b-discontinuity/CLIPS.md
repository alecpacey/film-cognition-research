# 03b — Clips

Built 20 September 2026 by `build_03b.py`, measured by `measure_joins.py` (output `joins.json`),
after `README.md` was committed (`221faad`) and before anything was scored. $0.

## Construction

Bases: stage 03's `face_close.mp4` and `landscape.mp4` (1344 × 768, 24 fps, 60.4 s, single takes).

- **B, C** — source B is the base through `trim 30:60 + trim 0:30 → concat → hflip`, i.e.
  out(t) = mirror(base(t + 30 s)). Ladder built by `../01-cutrate/build_conditions.py` **unchanged**
  (base × mirrored-shifted base), then the landscape's audio mapped over the clip with the same
  ffmpeg call `build_stage03.sh` used for stage 03's S− arm.
- **D** — REF's segment layout (face ↔ landscape, 30 / n s segments), every join an ffmpeg
  `xfade` cross-dissolve of **0.5 s**; each segment extended 0.25 s into the join on each interior
  side so the clip is 60.00 s; sources read from +0.25 s so the first join can extend backwards.
  Same audio call.

## Preconditions, measured

| ladder | constructed cuts | detected (total) | joins detected as cuts | peak frame Δ at joins | histogram distance across joins | duration s |
|---|---|---|---|---|---|---|
| REF | 1 | 1 | 1 / 1 | 72.1 | 0.828 | 59.92 |
| REF | 3 | 3 | 3 / 3 | 68.6 | 0.789 | 59.79 |
| REF | 7 | 7 | 7 / 7 | 69.2 | 0.768 | 59.62 |
| REF | 15 | 15 | 15 / 15 | 69.3 | 0.764 | 59.25 |
| REF | 31 | 31 | 24 / 31 | 54.1 | 0.741 | 58.54 |
| B | 1 | 2 | 1 / 1 | 42.1 | 0.084 | 59.92 |
| B | 3 | 4 | 3 / 3 | 42.5 | 0.181 | 59.79 |
| B | 7 | 8 | 7 / 7 | 43.4 | 0.185 | 59.67 |
| B | 15 | 16 | 15 / 15 | 43.7 | 0.188 | 59.38 |
| B | 31 | 32 | 21 / 31 | 30.0 | 0.184 | 58.88 |
| C | 1 | 1 | 1 / 1 | 38.3 | 0.107 | 59.92 |
| C | 3 | 3 | 3 / 3 | 41.1 | 0.247 | 59.79 |
| C | 7 | 7 | 7 / 7 | 43.1 | 0.266 | 59.67 |
| C | 15 | 15 | 15 / 15 | 43.2 | 0.277 | 59.38 |
| C | 31 | 31 | 21 / 31 | 30.1 | 0.269 | 58.88 |
| D | 1 | 1 | 1 / 1 | 20.6 | 0.824 | 59.96 |
| D | 3 | 1 | 1 / 3 | 17.1 | 0.787 | 59.96 |
| D | 7 | 1 | 1 / 7 | 14.7 | 0.767 | 60.00 |
| D | 15 | 1 | 1 / 15 | 13.4 | 0.763 | 60.00 |
| D | 31 | 2 | 2 / 31 | 12.7 | 0.763 | 60.00 |

| ladder | joins detected as hard cuts | mean peak frame Δ | mean histogram distance | what it is |
|---|---|---|---|---|
| REF | 50 / 57 | 66.7 | 0.778 | hard cut + scene change |
| B | 47 / 57 | 40.3 | 0.164 | hard cut, same scene |
| C | 47 / 57 | 39.2 | 0.233 | hard cut, same scene |
| D | 6 / 57 | 15.7 | 0.781 | scene change, no hard cut |

`cinemetrics.cuts()` unchanged; a join counts as detected if a cut falls within 0.35 s of it;
peak frame Δ is the largest adjacent-frame HSV difference within 8 frames of the join; histogram
distance compares the 20 frames ending 10 before the join with the 20 starting 10 after it.

**Rule check (README): D's joins detected as cuts must be ≤ 25%.** Measured 6 / 57 =
11%. **Met; the 0.5 s dissolve stands, no re-build.** (The README's *expectation* was
≤ 10%; 11% is recorded as measured.) D keeps the full scene change — histogram distance
0.78 against REF's 0.78 — with a peak frame Δ of 16 against REF's 67.

**B and C hold the scene and make a hard, large jump**: total detected cuts equal constructed
at every level (B runs one over, see below), histogram distance 0.16 and 0.23 against REF's
0.78, peak frame Δ ≈ 40 against REF's 67. The pixel jump is about 60% of a
scene change's — large, not equal, as README § Limits anticipated. The shortfall in "joins
detected" at 31 cuts is join-timing drift in the measurement, not missing cuts: totals match.

**Audio is identical in all twenty clips**, REF included: one decoded-audio MD5 (`98b8fcf2…`)
across REF, B, C and D at every level.

## Recorded, not corrected

- **B carries one extra discontinuity at every level** (detected totals [2, 4, 8, 16, 32]): the face
  base's own generator seam, which stage 03's `CLIPS.md` already records (`n_cuts` 1). It falls
  in the base's second half, which B uses (mirrored) and REF does not. Constant across levels,
  so it cannot contribute to a slope.
- **Clip duration shrinks with cut count in REF, B and C** (59.92 s at 1 cut to 58.5–58.9 s at
  31): `build_conditions.py` loses part of a frame per segment. This is a property of stages 01
  and 03 as run, found here; it is 2% at most and identical in kind across REF, B and C. D is
  60.00 s at every level.
- Visual check of one join per ladder: B same kitchen, people swap sides; C same valley
  mirrored; D a mid-dissolve blend of both scenes.
