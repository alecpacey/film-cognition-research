# 03 — Result

**Verdict: PARTIAL-A**, against `README.md` as fixed before generation. Run 14–15 September
2026. Data `parcel_vectors.json` (12 clips, 180 parcels each), script `evaluate_03.py`,
full output `evaluation.json`. Generated bases (single take, 0 cuts), stage 01's own
`build_conditions.py` intercut ladder, measured cuts **exactly 1 / 3 / 7 / 15 / 31** in
both arms (31× range; stage 01 achieved 2.1×). Scored on `alecnpacey/tribe-probe`, original
app verified byte-identical, `audio_only=True`.

## Against the criteria

| | required | S+ (speech) | S− (no speech) |
|---|---|---|---|
| H3a / H3b: ≥ 2 of {IFJa, IFJp, IFSp, 8C} with *r* > +0.9 vs log cuts | ≥ 2 | **3 of 4** — met | **1 of 4** — not met |
| IFJa · IFJp · IFSp · 8C | | +0.907 · +0.863 · **+0.932** · **+0.930** | +0.899 · +0.871 · +0.902 · +0.889 |
| parcels with \|*r*\| > 0.9 (chance ≈ 7) | reported | **58 / 180** | **54 / 180** |
| whole-vector *r*, cut01 vs cut31 | reported | +0.743 | +0.822 |

H3a met, H3b not met → **PARTIAL-A** by the table: "the frontal cut effect needs speech
present".

## Reading — stated against the verdict, not instead of it

**The label overstates the difference between arms.** In the no-speech arm all four
cluster parcels sit at +0.87 to +0.90; three of them miss the pre-fixed bar by 0.001–0.03.
At *n* = 5 levels that gap is inside noise. The data show the inferior-frontal cut effect
**present in both arms at near-identical magnitude**, with 58 and 54 parcels at |*r*| > 0.9
— eight times chance, replicating stage 01's 51 / 180 on generated footage with content
fixed by construction. The verdict is PARTIAL-A because the criteria were fixed and are not
softened; the mechanistic reading the table attaches to it — that speech is *required* — is
**not supported** by these numbers and should not be carried into the paper as a finding.

**Stage 02's observational signature reproduces under control.** In both arms cut rate is
strongly *negative* in auditory cortex: A4 −0.97 / −0.94, A1 −0.96 / −0.93, MBelt −0.95 /
−0.92 (S+ / S−), and A5 −0.95 without speech. This is exactly what the observational index
found (§ 6.5) and what stage 01 did not report. **Both earlier tracks were right about
different parts of the same effect:** cutting drives inferior-frontal cortex *up* and
auditory cortex *down*, and it does so with or without speech. Why the observational index
recovered the auditory half but not the frontal half is now the open question, and it is a
question about the corpus and the regression — not about the sensor.

**Cut rate is a causal lever on this sensor.** For stage 04 it is admissible, with the
frontal and auditory signatures both available as targets.

## Limitations

- **Face base short of spec:** `face_close` has `face_area_frac` 0.052 against a 0.10
  target (wide first attempt 0.035; no third at the post-promo rate). The face/place contrast
  between bases is weaker than stage 01's; the cut manipulation is unaffected.
- **n = 5 levels per arm.** Correlations at |*r*| > 0.9 are the design's coarse instrument;
  the arm difference is not resolvable at this *n*.
- **Generated footage, one scene pair, one generator.** The scope is what 01b licensed.
- **Text branch off**, as in every prior stage. A text-on replication is unrun.

## Spend and missteps, recorded

Bases $3.60 (fal, incl. one regeneration). Scoring ≈ $2.2 (HF): 12 clips plus one wasted
restart after a watcher of mine matched result files containing `"03_"` anywhere — which
also matched stage-02 ordinals and files from a separate experiment (`x1-av-emotion`)
writing to the same results repo — and paused the run at 6 / 12. Corrected to exact-name
matching. The local machine killed background tasks for memory twice; the Space finished
the batch unattended and paused on its inactivity timer.
