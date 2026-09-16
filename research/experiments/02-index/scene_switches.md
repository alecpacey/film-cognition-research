# Does inferior-frontal cortex track scene switches rather than cuts? — No, not by this proxy

**Exploratory, analysis-only, 16 September 2026.** Follows `frontal_miss.md`, which left one
hypothesis standing: the frontal cut effect of stages 01 and 03 is a response to *scene
switches* (every cut in those ladders alternates two unrelated scenes), and cinema's cuts are
mostly within-scene. `CORPUS.md` specified a per-segment scene-boundary count that was never
implemented; `scene_switches.py` implements one and this note reports the test. Registered
verdict unchanged. Scripts `scene_switches.py`, `scene_switches_analysis.py`; data
`scene_switches_corpus.jsonl` (all 244 segments, every cut scored), `scene_switches_validation.json`,
`scene_switches_result.json`.

## Measurement

Cuts are detected with `cinemetrics.cuts()` unchanged; on the 70 scored segments the cut dial
is reproduced exactly (max |Δ cuts/min| 0.00, r = 1.0000). Each cut is then
scored by the distance between the shot before and the shot after it — 0.5 × L1 between their
mean HSV histograms (16 × 4 × 4), frames within 2 of a cut excluded — and called *between-scene*
above a threshold. Three thresholds are carried (0.5, 0.6, 0.7) plus two threshold-free
quantities (sum and mean of distances at cuts).

**Validation.** Stage 03's ladder, where every cut is a face ↔ landscape switch by construction:
all 57 cuts score 0.73–0.84; the single-take bases score 0.20 (one cut) and nothing. Stage 01's
live-action ladder, where the 1 / 3 / 7 / 15 / 31 imposed cuts are between-scene and the *Jungle
Book* sources' own ~22 cuts are within-scene: detected totals 25 / 27 / 31 / 36 / 53; cuts ≥ 0.7:
2 / 4 / 6 / 10 / 18; ≥ 0.6: 6 / 8 / 12 / 15 / 23. The count rises with the manipulation but recovers roughly half
of it, because the sources' internal cuts (wide valley → animal close-up, inside one scene)
reach 0.6–0.8 too. **The proxy is clean on generated footage and partial on this live action.**
That bounds what a null here can mean.

**Corpus.** 1670 cuts over 244 segments; median distance 0.50; 51% ≥ 0.5, 25% ≥ 0.6,
9% ≥ 0.7. Per segment: *Jungle Book* 10.2 cuts, 2.8 ≥ 0.6; *Nothing Sacred* 8.5 / 2.0;
*Royal Wedding* 1.7 / 0.3. Within-film centred, between-scene count correlates with total cuts
at 0.70 (≥ 0.5), 0.41 (≥ 0.6), 0.43 (≥ 0.7): the split is real, not a relabelling.

## Result — the 70 scored segments, within-film centred

| parcel | cuts | between ≥ 0.5 | between ≥ 0.6 | between ≥ 0.7 | within < 0.6 | sum of distances |
|---|---|---|---|---|---|---|
| IFJa | -0.01 (0.97) | +0.13 (0.28) | +0.00 (0.99) | -0.03 (0.78) | -0.01 (0.95) | +0.05 (0.68) |
| IFJp | +0.13 (0.29) | +0.09 (0.47) | +0.15 (0.22) | +0.13 (0.29) | +0.02 (0.86) | +0.14 (0.24) |
| IFSp | -0.08 (0.52) | +0.05 (0.71) | -0.16 (0.19) | -0.16 (0.20) | +0.04 (0.76) | -0.05 (0.67) |
| 8C | -0.03 (0.80) | +0.09 (0.44) | -0.13 (0.28) | -0.13 (0.29) | +0.06 (0.59) | -0.01 (0.94) |
| A4 | -0.29 (0.02) | -0.15 (0.21) | -0.22 (0.07) | -0.19 (0.11) | -0.13 (0.27) | -0.25 (0.04) |
| A1 | -0.32 (0.01) | -0.17 (0.16) | -0.18 (0.15) | -0.17 (0.16) | -0.20 (0.09) | -0.26 (0.03) |
| MBelt | -0.34 (0.00) | -0.17 (0.16) | -0.12 (0.32) | -0.13 (0.29) | -0.26 (0.03) | -0.25 (0.03) |
| A5 | -0.19 (0.11) | -0.12 (0.32) | -0.25 (0.04) | -0.21 (0.08) | -0.01 (0.93) | -0.19 (0.12) |

Pearson *r* (*p*), *n* = 70.

**No frontal parcel tracks between-scene cuts at any threshold** (|*r*| ≤ 0.16, every
*p* ≥ 0.19), and partialling out within-scene cuts changes nothing (between | within: IFJa
-0.00, IFSp -0.15, 8C -0.12 at 0.6). The frontal cluster mean correlates with between-scene count at
+0.10 / -0.09 / -0.10 across the three thresholds. The film-flipping sign of `frontal_miss.md` is still there
and is, if anything, sharper: IFJa vs between-scene count is +0.40 in *Nothing Sacred* and -0.25 in
*Jungle Book* (≥ 0.6; ≥ 0.7: +0.41 and -0.30). Whatever frontal cortex is doing in these films, it
is not a monotone function of how many times the scene changes.

**The auditory decrease follows cuts of every kind.** A1 and MBelt correlate with *within*-scene
cuts (< 0.7) at -0.27 and -0.30, A4 and A5 with between-scene cuts (≥ 0.6) at -0.22 and -0.25;
the total-cut correlation (-0.29 to -0.34) is the strongest of all because it pools both. This is the
stage-03 S− result again — the auditory signature is a response to the visual discontinuity
as such — now seen in real cinema across cut types.

**Whole-map.** The marginal map of between-scene cuts at 0.5 correlates with stage 03's S− causal
map at *r* = +0.66 over 180 parcels (total cuts: +0.52), with S+ at +0.37 and stage 01 at +0.17; the
higher thresholds (sparser counts) do *worse* against stage 01 (-0.31, -0.27). None of these improvements
comes from the frontal cluster.

## Reading

The hypothesis is **not supported**. It is *weakened*, not excluded: the proxy is a colour
histogram, which separates a generated face scene from a generated valley perfectly and a
1942 conversation from a 1942 animal close-up only partly, so a real scene-switch effect could
survive at the ~50% recovery rate the stage-01 validation shows — but it would then have to be
small, and the transplanted slopes of `frontal_miss.md` said it should be large (predicted
*r* +0.3 to +0.45). A semantic scene-change detector (shot embeddings rather than histograms)
is the next-cheaper proxy; it is not built.

What is now established about the frontal miss, taken together with `frontal_miss.md`:

- not the penalty, not the range, not swamping by content variance, and not — by this proxy —
  the within/between-scene composition of the cuts;
- the frontal parcels' relation to cutting **differs in sign between films**, which no
  cut-classification can produce and which points at film-specific content the dial set does
  not measure;
- the auditory half of the effect is robust to all of this and appears in every film and for
  every kind of cut.

**Consequence for stage 04 is unchanged from `frontal_miss.md`**: cut rate is a demonstrated
frontal lever only on intercut, scene-alternating generated material; the index's cut-rate
column is the auditory half only. The between-scene count is now available as a measured
diagnostic for the 244 segments, as `CORPUS.md` asked, and is not a registered dial.
