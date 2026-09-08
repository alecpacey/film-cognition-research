# 02 — Result

**Run once, 8 September 2026, against the pre-registration at osf.io/dg7fe.**
Data: `parcel_vectors.json`, SHA-256 `93807b80…b053a3189`, verified by the script
before use. n = 70 (jungle_book 24, nothing_sacred 23, royal_wedding 23). Script:
`analyse.py`. Full output: `analysis_result.json`. Runtime 47 s.

## Verdict: PARTIAL

| criterion | required | found | |
|---|---|---|---|
| 1 · dials with ≥1 surviving parcel | ≥ 3 of 14 | **14 of 14** | met |
| 2 · cut rate replicates in {IFJa, IFJp, IFSp, 8C} | yes | **no** | not met |

PARTIAL was registered in advance as the most important possible outcome: the
observational and controlled tracks disagree, and one of them is wrong. Sample size
was raised 60→70 so that this check could fail informatively. It has.

## Criterion 1 — technique predicts the sensor, broadly

101 of 180 parcels survive (permutation p, BH-FDR q < 0.05). Every one of the 14
dials carries a non-zero weight in at least one surviving parcel. All 14 were
TESTED at n = 70; none is underpowered, so every null below is a real null.

| dial | surviving parcels attributed | label |
|---|---|---|
| face_area_frac | 85 | TESTED |
| mean_shot_len_s | 72 | TESTED |
| mean_saturation | 59 | TESTED |
| camera_zoom | 58 | TESTED |
| camera_pan | 53 | TESTED |
| camera_jitter | 46 | TESTED |
| median_luma | 43 | TESTED |
| face_hit_rate | 39 | TESTED |
| cuts_per_min | 35 | TESTED |
| dof_ratio | 35 | TESTED |
| contrast_p5_p95 | 32 | TESTED |
| warm_cool | 31 | TESTED |
| colourfulness | 25 | TESTED |
| shadow_frac | 11 | TESTED |

**No dial is a null.** The registration required nulls be reported with equal
prominence; there are none to report. The weakest dial, shadow_frac, still reaches
11 parcels — though it sits inside the lighting/colour cluster (see below) and its
individual count attributes poorly.

**Effect sizes.** Among survivors, cross-validated r has median 0.35 (IQR 0.28–0.44,
max 0.61). Only nine parcels exceed the pre-registered SESOI of r ≥ 0.5 — PCV 0.61,
POS2 0.55, DVT 0.55, 7Pm 0.55, 31a 0.54, 6v 0.53, POS1 0.53, 7Am 0.52, V3 0.50.
**Statistically surviving is not the same as reaching the smallest effect of
interest.** Through TRIBE's out-of-distribution accuracy of 0.2146, a survivor at
the median r = 0.35 implies roughly r ≈ 0.07 against real cortex.

**The dominant dial is face area.** 65 of the 101 survivors have face_area_frac as
their largest coefficient. Its signature is the run-00 double dissociation
reappearing as a dial: STSdp +0.85, A5 +0.69, STSvp +0.58 (the voice chain, up) and
VMV2 −0.67, PHA2 −0.62, MT −0.55 (the place chain, down). The controlled probe and
the observational index agree on this axis to the parcel.

**The lighting/colour cluster** is dominant in 25 of 101 survivors. Per the
registration these are reported as associations with the *cluster*: condition
number 58.8, shadow_frac VIF 9.5, median_luma 6.1, mean_saturation 5.9,
median_luma~shadow_frac r = −0.90. This design cannot say which member drives them.

## Criterion 2 — cut rate does not replicate where stage 01 put it

| parcel | CV r | null 95th | q | survives | coef cuts_per_min | coef mean_shot_len_s |
|---|---|---|---|---|---|---|
| IFJa | +0.044 | 0.178 | 0.191 | no | 0 | 0 |
| IFJp | −0.204 | 0.126 | 0.567 | no | 0 | 0 |
| IFSp | +0.346 | 0.221 | 0.015 | **yes** | **0** | **0** |
| 8C | +0.075 | 0.176 | 0.158 | no | 0 | 0 |

IFSp survives — but with *exactly zero* weight on both cut-rate dials. Its model is
carried by face_area_frac (+0.23) and camera_zoom (−0.12). Stage 01's strongest
responder, IFJa (r = +0.996 on identical footage), is indistinguishable from its
null here. IFJp's point estimate is negative.

**Where cut rate goes instead.** Among survivors, its largest weights are auditory
and negative — A4 −0.23, A1 −0.17, MBelt −0.16, A5 −0.13 — and early visual and
positive — PIT +0.17, MST +0.17, FFC +0.16, V8 +0.14. Shot length (its inverse)
loads on the place chain: PHA2 −0.22, VMV2 −0.17, and on MT −0.17, V3A −0.21.
Neither dial reaches frontal cortex.

**Reading, stated as a reading.** Stage 01 varied cut count on *identical footage*:
every cut was a switch and nothing else changed, and the sensor answered in
cognitive-control cortex. Stage 02 measures cut rate as it occurs in cinema, where
fast cutting co-occurs with dialogue, close-ups and interiors, and within-film
centring removes only each film's mean of that. The observational cut-rate
signature looks like *the content that fast cutting accompanies*, not *the act of
cutting*. That is exactly the covariance the corpus was built to break and could
only partly break — and exactly the separation stage 03 exists to make. Which
track is "wrong" is not decidable from this data; that it must be resolved before
anything is built on cut rate is the finding.

## Declared choices (registration silent; fixed before the run)

Elastic net α = 0.1, l1_ratio = 0.5, 5-fold shuffled CV — the values of the
pre-registered 30-segment check, so the machinery is the same. Dials standardised
after within-film centring: required so that "no dial is dropped" holds, since an
unscaled penalty would zero the small-unit dials by units alone; parcels not
rescaled. Permutation p = (1 + #{r_perm ≥ r_obs})/1001, one-sided; BH q = 0.05;
one shared label permutation across all 180 parcels per iteration. A surviving
parcel attributes to a dial if that dial's full-data coefficient is non-zero.
"Replicates" = ≥1 cluster parcel survives with coef(cuts_per_min) > 0 or
coef(mean_shot_len_s) < 0. Seed 20260908. Listed in full in `analyse.py`.

## Limitations

- **Unrestricted permutation.** Labels were permuted across all 70 segments, as
  registered. With three films, any within-film structure not removed by centring —
  segments from one scene are not independent — makes this null lenient, and 101
  of 180 is a large fraction. A within-film (restricted) permutation would be the
  conservative test. It was not registered and was not run.
- **Corpus-conditional** (three films) and **design-conditional** (segments chosen
  to spread dial ranges; not "the effect in typical cinema").
- **A model, not a brain.** Every association here is between technique and
  TRIBE's prediction. TRIBE agrees with real cortex at r = 0.2146 out of
  distribution, and this corpus is further out than that figure was measured on.
- **Attribution inside the lighting/colour cluster** is not available from this
  design.

## Disclosure

The pre-registered 30-segment futility check (`futility_check.py`) **was executed**,
on 6 September 2026 at 30/70, and returned CONTINUE. Only that verdict was recorded;
no dial, parcel or effect size was inspected. The OSF registration text states the
script had never been executed; that statement is incorrect and is corrected here.
