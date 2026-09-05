# Dial table and detectability — stage 02

**244 segments, 14 dials, measured 4 September 2026.** Diagnostics and thresholds
were pre-registered in `README.md` § *Effect size, sample size, and what counts as
testable* before any dial was measured. No parcel had been scored when this was
written, and nothing here touches an outcome — every figure below is stimulus-side.

Corpus: jungle_book 95 · nothing_sacred 66 · royal_wedding 83.

**Current state, added 5 September 2026:** *n* = 70 was adopted on 4 September and
**all 14 dials are TESTED at that sample size** — see § 1 *Fix*. § 1's table and
heading record the detectability finding **at n = 60**, which is what forced the
change, and are kept as the record of why. § 3 has been recomputed against the
70-segment selection actually in `selection.json`.

---

## 1 · Detectability — 12 of 14 dials testable, and the two that are not are the wrong two

A dial is scored on how much of its spread survives **within-film centring**:
`s = within-film SD / total SD`. A dial that varies mostly *between* films loses
that variance to centring, and only what remains can carry a correlation.
Restriction of range then gives the observed correlation at the pre-registered
SESOI of r = 0.5, and the power that implies at n = 60.

| dial | s | r_obs at SESOI | power | label |
|---|---|---|---|---|
| **cuts_per_min** | 0.66 | 0.36 | **0.79** | ⚠ **UNDERPOWERED** |
| **mean_shot_len_s** | 0.67 | 0.36 | **0.80** | ⚠ **UNDERPOWERED** |
| camera_jitter | 0.99 | 0.50 | 0.98 | TESTED |
| camera_zoom | 0.97 | 0.49 | 0.98 | TESTED |
| camera_pan | 1.00 | 0.50 | 0.98 | TESTED |
| median_luma | 0.93 | 0.47 | 0.96 | TESTED |
| contrast_p5_p95 | 0.87 | 0.45 | 0.94 | TESTED |
| shadow_frac | 0.93 | 0.47 | 0.96 | TESTED |
| colourfulness | 0.87 | 0.45 | 0.95 | TESTED |
| mean_saturation | 0.87 | 0.45 | 0.94 | TESTED |
| warm_cool | 0.87 | 0.45 | 0.94 | TESTED |
| face_area_frac | 0.97 | 0.49 | 0.98 | TESTED |
| face_hit_rate | 0.99 | 0.49 | 0.98 | TESTED |
| dof_ratio | 0.94 | 0.48 | 0.97 | TESTED |

### Why this is the worst possible pair to lose

Cut rate is not one dial among fourteen. It is **the dial stage 01 established** —
51 of 180 parcels at |r| > 0.9 on identical footage — and **pass criterion 2
requires it to replicate here**. The criteria say a failure to replicate is the
most important possible finding, one that would redirect the project.

At 79% power that inference is not available. A null on cut rate could not be
distinguished from a failure to detect, so the PARTIAL verdict the README calls
"the most important possible finding" would be unearned. **The replication check
is currently unable to fail informatively.**

### The cause is a genuine design tension, not a mistake

Cut rate loses a third of its variance to centring precisely *because the corpus
was chosen for director contrast* — Wellman, Korda and Donen cut at different
rates, which is exactly the between-film spread the corpus was built to have. And
within-film centring, the decision taken to stop saturation becoming a proxy for
film identity, removes exactly that. **The two decisions work against each other on
this dial**, and only on the dials where between-film contrast is the point.

### Stratified selection does not rescue it

Detectability was recomputed on the selected 60 rather than all 244, since the
selection deliberately widens each dial's spread and could have lifted the power.
It does not: `s` stays at 0.67 and 0.66, and **no dial changes label**. Stratifying
*within* film cannot recover variance that lives *between* films.

### Fix

| n | power on cut rate | GPU | wall-clock |
|---|---|---|---|
| 60 | 0.79 | $10.20 | ~10 h |
| 65 | 0.83 | $11.05 | ~10.8 h |
| **70** | **0.85** | **$11.90** | ~11.7 h |
| 80 | 0.90 | $13.60 | ~13.3 h |

**Recommended: n = 70. ✅ ADOPTED 4 Sep 2026.** At 70 the cut-rate dials reach
power 0.85 and 0.86 and **all 14 dials clear the floor**. The selection is 70
segments — jungle_book 24, nothing_sacred 23, royal_wedding 23 — retaining 83–100%
of every dial's range. Cost of the fix: $1.70.

### ⚠ Known limitation of this metric — stated because it did not bite, not because it cannot

`s` is a **ratio**. A dial with almost no absolute variance, but whose little
variance happens to survive centring, scores s ≈ 1.0 and is labelled TESTED. The
metric measures what centring costs, not whether there was anything there to begin
with.

`camera_pan` looked like exactly that case — SD printed as `0.000` — and was
checked directly rather than trusted: values run to 2.9×10⁻³ of frame width per
frame, which over a 60 s segment is a pan across 421% of the frame, with 27 static
segments and 48 distinct values. It is a real dial, and the `0.000` was a
formatting artefact of `%.3f` on a 2×10⁻⁴ number.

The gap is real even though this instance was benign. Any future dial should be
checked on absolute spread as well as on `s`.

---

## 2 · Interdependence — the covariance is only partly broken

Measured on centred dials, reported as a diagnostic and **not modelled**;
separating covarying dials is what stage 03 is for.

**Condition number: 58.8** — meaningful collinearity (>30), short of severe (>100).

Strongest pairs:

| | | r |
|---|---|---|
| median_luma | shadow_frac | **−0.90** |
| contrast_p5_p95 | shadow_frac | −0.71 |
| median_luma | mean_saturation | −0.68 |
| median_luma | contrast_p5_p95 | +0.68 |
| shadow_frac | mean_saturation | +0.68 |
| contrast_p5_p95 | mean_saturation | −0.58 |

Highest VIF: shadow_frac **9.5**, median_luma 6.1, mean_saturation 5.9,
colourfulness 5.0. Conventionally VIF > 5 warrants comment and > 10 is serious.

**Reading.** There is one tight cluster and it is *lighting-and-colour*:
luminance, shadow fraction, contrast and saturation move together and are close to
redundant — `shadow_frac` at r = −0.90 with `median_luma` is nearly a deterministic
function of it. The camera dials, the face/shot-scale dials and depth of field are
comparatively independent (VIF < 2.3), as is cut rate.

This is the elastic net earning its place: exactly the multicollinearity Kauttonen
2015 hit with 37 cinematic features. It also means any finding inside the
lighting/colour cluster attributes poorly — the model may identify *that the
cluster matters* without being able to say which member drives it. That is a
stage-03 question and should be written up as one, not resolved by argument here.

---

## 3 · Selection — 70 segments: jungle_book 24 · nothing_sacred 23 · royal_wedding 23

Stratified on cut rate within film, then maximin coverage in standardised dial
space. Range retained against all 244:

| dial | kept | | dial | kept |
|---|---|---|---|---|
| mean_shot_len_s | 1.00 | | median_luma | 0.98 |
| camera_jitter | 1.00 | | shadow_frac | 0.98 |
| camera_zoom | 1.00 | | contrast_p5_p95 | 0.94 |
| camera_pan | 1.00 | | face_hit_rate | 0.94 |
| face_area_frac | 1.00 | | cuts_per_min | 0.91 |
| dof_ratio | 1.00 | | mean_saturation | 0.89 |
| | | | warm_cool | 0.89 |
| | | | colourfulness | 0.83 |

Every dial retains ≥ 83% of its full range; six retain all of it. The selection is
in `selection.json`, and `run_batch.py` refuses to run without it.

**This section previously described a 60-segment selection, 20 per film.** That was
superseded by the n = 70 decision recorded in § 1 above, and the table has been
recomputed against the selection actually in `selection.json`. The only dial to lose
range in the change is `colourfulness`, 0.89 → 0.83; `median_luma` and `shadow_frac`
gained. **No dial changes label**, and all 14 remain TESTED at n = 70.

## Files

`dial_table.json` — 244 × 14 · `dials/*.json` — per-segment cinemetrics output ·
`selection.json` — the chosen 70 · `measure_dials.py` · `analyse_dials.py`
