# Why the stage-02 index missed the frontal half of the cut effect

**Exploratory, analysis-only, 15 September 2026.** Not the registered test; the PARTIAL
verdict of `RESULT.md` is unchanged. Script `frontal_miss.py`, outputs `frontal_miss.json`
and `frontal_miss_transplant.json`, run on the frozen `parcel_vectors.json` (sha `93807b80…`).

## The question

Stage 03 showed, on generated footage with content fixed by construction, that cutting alone
drives IFJa / IFSp / 8C *up* (r ≈ +0.9 vs log cuts) and A4 / A1 / MBelt *down* (≈ −0.95), in
both speech arms. The stage-02 index recovered the auditory half — negative cut-rate weights
in A4, A1, MBelt, A5 — and nothing frontal (§ 6.5). Is that the regression's fault or the
corpus's? Stage 04 builds on one or the other.

## Verdict: the corpus, not the index

The frontal cut effect is **absent from the corpus at the size the causal slopes predict**;
the regression reported that absence correctly. Four lines of evidence, then the one
hypothesis they leave standing.

### 1 · The penalty did not zero a real weight

Refitting the four cluster parcels on the identical registered design matrix (14 within-film
centred, standardised dials, n = 70) without the penalty:

| parcel | EN coef (registered) | OLS coef | t | p | ridge (α=1) | EN at α=0.001 |
|---|---|---|---|---|---|---|
| IFJa | 0 | +0.051 | +0.84 | 0.40 | +0.048 | +0.049 |
| IFJp | 0 | +0.039 | +0.94 | 0.35 | +0.038 | +0.038 |
| IFSp | 0 | +0.067 | +0.63 | 0.53 | +0.060 | +0.065 |
| 8C | 0 | +0.038 | +0.73 | 0.47 | +0.034 | +0.036 |

Unpenalised, every frontal cut-rate weight has the stage-03 sign and none has |t| > 1. The
elastic net at α = 0.1 zeroed coefficients indistinguishable from zero. For comparison the
auditory quartet's OLS weights are −0.15 to −0.26 (MBelt t = −2.37, p = 0.022; A1 t = −2.00),
and the registered elastic net kept all four.

### 2 · The raw within-film correlation is zero, in every film

| parcel | r with cuts_per_min (n=70) | log cuts | Jungle Book | Nothing Sacred | Royal Wedding |
|---|---|---|---|---|---|
| IFJa | −0.005 | −0.067 | −0.25 | +0.32 | −0.11 |
| IFJp | +0.129 | +0.056 | +0.16 | +0.27 | −0.10 |
| IFSp | −0.078 | −0.115 | −0.35 | +0.12 | −0.03 |
| 8C | −0.031 | −0.061 | −0.27 | +0.15 | +0.06 |
| A4 | **−0.285** (p .017) | −0.268 | −0.46 | −0.28 | −0.09 |
| A1 | **−0.324** (p .006) | −0.306 | −0.50 | −0.30 | −0.15 |
| MBelt | **−0.337** (p .004) | −0.310 | −0.41 | −0.33 | −0.25 |
| A5 | −0.193 | −0.212 | −0.38 | −0.15 | −0.06 |

The auditory sign is negative in all three films. The frontal sign **flips between films**
(negative in *Jungle Book*, positive in *Nothing Sacred*), which is what a parcel tracking
film-specific content that happens to co-vary with cut rate looks like, not a parcel tracking
cutting.

**Range is not the explanation.** After within-film centring cut rate keeps 47% of its
variance (s = 0.69; SD 3.47 cuts/min). *Jungle Book* spans 3–21 cuts/min (n = 24) and
*Nothing Sacred* 2–17 (n = 23), a 7–8× range each; *Royal Wedding* contributes little (0–7,
SD 1.97). The auditory effect is visible inside each of the two wide-range films; the frontal
effect is not visible in either.

### 3 · Transplanting the causal slopes predicts a *larger* frontal signal than auditory — and it is not there

Take each parcel's stage-03 slope (z per unit log cuts), scale it by the corpus's within-film
SD of log cuts (0.50) and divide by the parcel's within-film SD in the corpus. That is the
correlation stage 02 would have seen if the causal effect simply added to whatever else moves
the parcel in real cinema.

| parcel | slope S+ / S− | corpus SD(z) | predicted r (S+ / S−) | observed r (log cuts) |
|---|---|---|---|---|
| IFJa | +0.40 / +0.29 | 0.43 | **+0.42 / +0.32** | −0.07 |
| IFJp | +0.25 / +0.18 | 0.29 | +0.40 / +0.30 | +0.06 |
| IFSp | +0.47 / +0.25 | 0.77 | +0.29 / +0.16 | −0.12 |
| 8C | +0.37 / +0.28 | 0.37 | **+0.45 / +0.36** | −0.06 |
| A4 | −0.33 / −0.53 | 1.26 | −0.13 / −0.21 | **−0.27** |
| A1 | −0.38 / −0.34 | 0.80 | −0.23 / −0.21 | **−0.31** |
| MBelt | −0.52 / −0.40 | 0.74 | −0.33 / −0.26 | **−0.31** |
| A5 | +0.02 / −0.56 | 2.13 | +0.01 / −0.13 | −0.21 |

The auditory parcels come in **at or above** the transplanted prediction. The frontal parcels
should have shown r ≈ +0.3 to +0.45 — larger than auditory, because their corpus variance is
small — and show nothing. This rules out "swamped by content variance": the prediction already
divides by the corpus variance. The frontal response to cutting that stage 03 measures does
not occur, at that size, when cameras cut in these three films.

### 4 · Everywhere else, the observational map recovers the causal one

Across all 180 parcels, the within-film marginal cut-rate map of stage 02 correlates with the
stage-03 causal map at **r = +0.52** (S− arm; Spearman 0.58), +0.21 with the S+ arm, and
−0.03 with stage 01's live-action map. Excluding 30 auditory / insular parcels the S− figure
is still +0.41. Of the 23 parcels stage 03 moves the same way in both arms at |r| > 0.9, stage
02 gets the sign right in **22** — all 16 that go down (mean marginal r −0.28; the registered
elastic net kept 14 of them, all with the causal sign) and 6 of the 7 that go up (mean +0.17;
5 kept, all concordant). The one miss is IFSp. The index is not blind to cutting; it is blind
to what cutting does in inferior-frontal cortex specifically.

### 5 · The auditory signature does not carry the frontal variance — it covaries the wrong way

In the corpus the frontal and auditory parcels move *together*: IFSp correlates with A5 at
+0.83 and with A4 at +0.74 (R² 0.75 on the auditory quartet), 8C at R² 0.54, the cluster
means at +0.49. Cutting drives them *apart* (stage 03). So the corpus's dominant shared
variance — the face / voice / speech axis of § 6.7 — is orthogonal to the cut contrast, and
removing it exposes only a small frontal residual: partial r of IFSp with cuts given the
auditory mean is +0.22 (p 0.069), IFJa +0.07, 8C +0.11. The frontal − auditory contrast
correlates with cuts at +0.30 (p 0.012), but that is the auditory half doing the work
(auditory mean alone −0.27, frontal mean alone −0.03). Suggestive of a small frontal effect
under the shared variance; not a recovery of it.

## The hypothesis left standing

In stages 01 and 03 **every cut is a scene switch**: the ladder alternates two maximally
different scenes, so cut count and scene-switch count are the same number. In cinema most cuts
are continuity cuts inside one scene — a 15-cut dialogue exchange has zero scene switches. If
the inferior-frontal response is to *updating the scene*, not to *the cut*, it would appear in
the ladder and vanish in the corpus exactly as observed, while the auditory decrease — which
follows visual cut count even in the S− arm, where the audio track is continuous ambient with
no discontinuity at any cut — tracks cuts as such, and does so in every film.

This is testable for free. `CORPUS.md` specified counting scene boundaries per segment as a
diagnostic ("record, do not correct"). **It was never implemented**: no scene-boundary field
exists in `dial_table.json` or in any `dials/*.json`, and `cinemetrics.py` counts cuts without
classifying them. Paper § 4.3's statement that the count was recorded is corrected. Adding a
between-scene cut count (a cut whose neighbouring shots do not share a colour / layout
signature) and regressing IFJa on it is the next analysis, before any stage-04 spend.

## Consequences

- **The index is sound where it can be checked.** Its cut-rate column is the auditory half of
  a two-part effect; the other columns are untouched by this finding.
- **Cut rate is a causal lever on frontal cortex only in the regime where it was shown:**
  intercut, scene-alternating generated footage. The observational index must not be used to
  steer frontal cortex via cut rate in real cinema; it has no such weight to steer with.
- **For stage 04**, cut rate is admissible with both signatures as targets on generated
  intercut material (stage 03's regime), and inadmissible as a frontal lever anywhere else
  until the scene-switch hypothesis is tested.

## Addendum, 16 September — the hypothesis tested

The between-scene cut count was implemented (`scene_switches.py`) and run on all 244 segments.
**Not supported**: no frontal parcel correlates with between-scene cuts at any threshold
(|r| ≤ 0.16, p ≥ 0.19), the film-flipping sign persists (IFJa +0.40 in *Nothing Sacred*, −0.25 in
*Jungle Book*), and auditory cortex follows cuts of every kind. The proxy separates scene
switches only partially on live action, so the hypothesis is weakened rather than excluded. See
`scene_switches.md`. The consequences above stand.
