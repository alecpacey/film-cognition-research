# Corpus and segmentation — stage 02

**Written 3 September 2026, as objective O1 of `../OBJECTIVES.md`.**
Answers the four questions left open in `../HANDOFF.md`. Every runtime, resolution
and licence below was read from the Internet Archive metadata API in this session,
not recalled. Anything not verified is labelled as an assumption.

---

## Headline: the premise behind the animation assumption is false

`HANDOFF.md` recorded, explicitly as an assumption pending research:

> prefer animated Technicolor features … public-domain animated colour titles are
> more available than live-action ones

**They are not.** Six public-domain live-action Technicolor features were verified
this session, against two animated colour features, one of which carries French
titling. What is abundant in `collection:animationandcartoons` is colour *shorts* —
the top results by downloads are Popeye one-reelers of 7–9 minutes — not features.

The assumption is dropped. It did not need GPU to test.

---

## Q4 · What exists — verified

Runtime and resolution are from the largest video file in each item;
licence is the item's stated `licenseurl`.

### Live-action colour features

| Title | Year | Archive identifier | Runtime | Resolution | Licence |
|---|---|---|---|---|---|
| **Nothing Sacred** | 1937 | `nothing-sacred-1937-by-william-a.-wellman` | 73.8 min | 1472×1072 | PD Mark 1.0 |
| Nothing Sacred *(alt)* | 1937 | `NothingSacredVideoQualityUpgrade` | 73.9 min | 720×536 | PD Mark 1.0, in `feature_films` |
| **Jungle Book** | 1942 | `ams-junglebook-1080p` | 105.7 min | 1440×1080 | — *(in `feature_films` as `jungle-book-1942_202312`, 640×480, PD Mark)* |
| **Royal Wedding** | 1951 | `royal-wedding-1951_202507` | 93.1 min | 1424×1072 | PD Mark 1.0 |
| Dr. Cyclops | 1940 | `dr..-cyclops.-1940` | 76.8 min | 1480×1080 | PD Mark 1.0 |
| A Star Is Born | 1937 | `AStarIsBorn` | 110.9 min | 640×480 | publicdomain |
| The Little Princess | 1939 | `little_princess` | 92.8 min | 640×480 | publicdomain |
| Becky Sharp | 1935 | `Becky_Sharp_` | 83.4 min | 720×480 | publicdomain |

*Rejected:* **Leave Her to Heaven** (1945, `leave-her-to-heaven-1945_202110`,
110.0 min, 988×720) — no licence stated on the item. Not worth the question.

### Animated colour features

| Title | Year | Archive identifier | Runtime | Resolution | Licence |
|---|---|---|---|---|---|
| The Snow Queen | 1957 | `the-snow-queen-1957_202501` | 60.6 min | 1434×1080 | PD Mark 1.0 |
| The Snow Queen *(dub)* | 1959 | `the-snow-queen-1957-1959-dub-restored` | 66.6 min | 1280×720 | PD Mark 1.0 |
| Gulliver's Travels | 1939 | `LesVoyagesDeGulliver1939` | 76.4 min | 640×480 | PD Mark 1.0 — French titling |

Two titles, one of them a duplicate of the other, and one with French intertitles.
That is not a corpus.

### Colour verification — measured, not assumed

Every title here is a documented Technicolor production, but a documented Technicolor
production can still reach the archive as a black-and-white dupe, and a black-and-white
film in a colour corpus is the exact failure this corpus question exists to avoid. So
each print is checked by measurement before use: twelve frames sampled across the
running time, then mean HSV saturation, Hasler–Süsstrunk colourfulness, and mean
per-pixel channel spread. A greyscale print scores ~0 on the last two whatever its
pixel format says — `yuv420p` proves nothing on its own.

Run by `verify_colour.py`, 12 frames per print, sampled evenly across the middle
90% of the running time so that titles and end credits — often monochrome even in a
colour film — do not dominate. Results land in `colour_check.json`.

| Print | mean sat | colourfulness | chroma | sat range | verdict |
|---|---|---|---|---|---|
| `nothing_sacred_1937.mp4` | **81.9** | 20.5 | 10.5 | 57–133 | ✅ **COLOUR** |
| `royal_wedding_1951.mp4` | **85.5** | 31.0 | 16.3 | 50–150 | ✅ **COLOUR** |
| `jungle_book_1942.mkv` | **115.6** | 27.2 | 14.6 | 21–170 | ✅ **COLOUR** |

Thresholds are `mean saturation > 15` and `chroma > 3`; a true greyscale print sits
at essentially zero on both, so all three clear by a wide margin.

**All three prints verified. No black-and-white dupe in the corpus.**

Streams, by ffprobe — note the audio codecs differ and normalisation must reconcile
them, since TRIBE has an audio branch and both prior runs kept audio:

| Print | video | resolution | fps | audio |
|---|---|---|---|---|
| `nothing_sacred_1937.mp4` | h264 yuv420p | 1472×1072 | 24000/1001 | AAC 48 kHz stereo |
| `royal_wedding_1951.mp4` | h264 yuv420p | 1424×1072 | 24000/1001 | AAC 48 kHz stereo |
| `jungle_book_1942.mkv` | h264 yuv420p | 1440×1080 | 24000/1001 | **AC-3** 48 kHz stereo |

Noted in passing, and useful on two counts.

**Within film**, saturation ranges 57–133 (Nothing Sacred), 50–150 (Royal Wedding)
and 21–170 (Jungle Book). Saturation is one of the dials and it moves substantially
inside every film — early evidence it will survive the O3 variance check rather than
being dropped as static.

**Between films**, the mean saturations are 81.9 / 85.5 / 115.6. Jungle Book is
markedly more saturated than the other two, which is the between-film spread the
corpus was chosen for — and precisely why dials are centred within film before any
regression, so that "saturation" cannot become a proxy for "which film".

Stream, verified by ffprobe: h264, 1472×1072, yuv420p, 24000/1001 fps, 4426.80 s,
AAC stereo. Audio is present and must be preserved through normalisation — TRIBE has
an audio branch and runs 00 and 01 both kept it.

---

## Q2 · Corpus composition — and why animation is now out

Beyond mere availability, there is a positive reason not to build stage 02 on
animation, and it is about what the corpus is *for*.

Gruber et al. (2024), *Between-movie variability severely limits generalizability of
"naturalistic" neuroimaging* — 112 participants, eight animated movies, 210
Brainnetome parcels — chose animation deliberately, and said why:

> Animated movies are an ideal limiting case for assessing movie-related variability
> in ISC, as they are **stylistically and thematically similar**.

Animation is their **minimum-variance** condition. Stage 02 needs the opposite:
maximum style variance, because breaking dial covariance is the entire reason for
using more than one film. An all-animated corpus is the worst available instrument
for that specific job — independently of whether TRIBE can see animation at all.

Two further findings from the same paper bear directly on our design:

- Whole-brain ISC differed significantly across movies — *F*(7,385) = 4.65,
  *p* < 0.001, η²G = 0.048 — and **the differences were not driven by one odd film**;
  ISC values differed consistently across all eight.
- Their downstream analysis found associations in **non-overlapping brain regions
  for every movie** — of eight films, exactly one parcel was shared between two.

Their conclusion — *"using a specific movie in neuroscience should be treated
similarly to using a particular task"* — is the strongest external support we have
for both the multi-film design and the decision to centre within film. It also
warns that our index will be corpus-conditional, and that must be said plainly in
the stage-02 RESULT rather than discovered by someone else later.

### How many films

**Three**, with segments split evenly. The tension is that more films break
covariance better, while fewer films leave more segments per film for the
within-film centring to estimate a stable film mean. At the planned 40-segment
start, three films gives ~14 segments each; four gives 10, which is thin for a
per-film mean.

**Recommended triad** — chosen to differ on opposite ends of as many dials as possible:

| Film | Buys us |
|---|---|
| **Nothing Sacred** (1937) | dense overlapping dialogue, interiors, fast cutting, medium shots |
| **Jungle Book** (1942) | landscape, exteriors, slow cutting, wide shots — *already characterised by runs 00 and 01* |
| **Royal Wedding** (1951) | musical: sustained camera movement, high-key luminance, long takes that still move |

Fourth if budget allows, or a substitute if Royal Wedding's dials disappoint:
**Dr. Cyclops** (1940), for low-key lighting at the dark end of a range where
Royal Wedding sits bright.

**Nothing Sacred is the direct replacement for *His Girl Friday*.** It is the same
thing — a fast-talking 1937 newspaper satire — in three-strip Technicolor. It fills
the role that picture was chosen for, with the black-and-white confound removed.
This is the single most useful thing O1 produced.

### Does animation pool with live action

Not in this corpus, because animation is not in this corpus. Recorded for whenever
it returns: it should **not** be pooled naively. Existing fMRI work reports
systematic live-action/animation differences — greater lateral occipital and
inferior frontal response to animated sequences, and weaker agency-related response
to animated than to real agents performing identical biological motion. Within-film
centring removes a per-film *offset*; it does not remove an *interaction*, and a
dial→parcel mapping that differs by medium is exactly an interaction. Pooling would
need to be tested, not assumed.

---

## Q1 · Segmentation — fixed 60 s windows, non-overlapping

**Decision: fixed 60 s, non-overlapping, sampled across each film. Not shot-aligned.**

Three reasons, in order of weight:

1. **Our unit of analysis is the segment, not the timepoint.** Stage 02 regresses a
   segment's aggregate parcel vector on its aggregate dials. A scene change inside a
   segment is therefore not a confound — it is *measured*, by the cut-rate dial,
   and both sides of the regression see the same 60 s. This is what makes the
   straddling objection in `HANDOFF.md` much weaker than it looks: it would matter
   for a timepoint-level model such as Kauttonen's, which regressed 37 feature
   timeseries against a continuous BOLD timeline within a single 14-minute film. It
   does not transfer to a cross-segment design.
2. **There is no event-aligned segmentation that is correct for all 180 parcels.**
   The event-segmentation literature (Baldassano 2017; Geerligs 2022) finds a nested
   cortical hierarchy of neural state durations — short states in early sensory
   regions, long ones in angular gyrus and posterior medial cortex. Aligning windows
   to boundaries defined at one timescale mis-aligns every parcel operating at
   another.
3. **Variable-length windows fight the sensor.** TRIBE has a ~30 s floor and a 100 s
   training window. Fixed 60 s sits comfortably inside that band, as runs 00 and 01
   already established. Shot-aligned windows vary in length and some would land near
   the floor, where the model returns diffuse output *without erroring*.

**Record, do not correct:** count scene boundaries per segment and keep it in the
dial table as a diagnostic. If the eventual result turns on it, that is worth
knowing; it is not a covariate in the pre-registered model.

---

## Q3 · Prior art worth copying

| Source | What it gives us |
|---|---|
| **Kauttonen 2015**, *Optimizing methods for linking cinematic features to fMRI data*, NeuroImage 110:136–148 | The elastic-net choice, already in our design. Note the difference: one 14-min film, continuous timeseries, ICA components and ROIs. Ours is cross-segment across films — the regularisation transfers, the null does not. |
| **NNDb** (Aliko et al. 2020, *Sci Data*) | 86 participants, **ten full-length features across diverse genres**, one film per participant. The strongest precedent that a multi-film, whole-feature corpus is a normal design rather than an invention. |
| **Gruber et al. 2024** (bioRxiv 2024.12.03.626542) | The between-movie variability result above. Treat each film as a task; report the index as corpus-conditional. |

No established sampling design was found that prescribes *where within a film* to
draw segments. Sampling evenly across the running time, avoiding titles and end
credits, is our own choice and is recorded here as such.

---

## New confound found in the process: encode heterogeneity

The verified prints span **640×480 to 1480×1080**. `cinemetrics.py` measures
depth of field as a centre-versus-surround sharpness ratio, and its colour and
contrast statistics are sensitive to encode quality. Within-film centring removes a
per-film mean; it does **not** remove a resolution-dependent difference in a dial's
*variance*, which would make "depth of field" partly a proxy for which print we
happened to download.

**Decision: normalise every source before measuring dials** — same target
resolution, same codec, same CRF for all films. All three recommended titles are
available at approximately 1080 tall, so nothing is thrown away:

| Film | Print to use | Native |
|---|---|---|
| Nothing Sacred | `nothing-sacred-1937-by-william-a.-wellman` | 1472×1072 |
| Jungle Book | `ams-junglebook-1080p` | 1440×1080 |
| Royal Wedding | `royal-wedding-1951_202507` | 1424×1072 |

Note this is **not** the Jungle Book print used in runs 00 and 01 — those used a
640×480 copy, 6294.7 s. Keep that copy. Stage 02's dial table must be internally
consistent; cross-stage comparison against stage 01 runs on parcel z-values, not on
dials, so the different print does not enter the cut-rate replication check.

---

## Consequences for the objectives

1. **O2 · 01b defers.** The branch written into `../OBJECTIVES.md` — *"if the
   live-action list can supply 2–3 public-domain colour features that differ enough
   in style, animation is not needed for stage 02 at all"* — has fired, on evidence.
   Animation does not enter the stage-02 corpus, so there is nothing for the gate to
   decide. 01b stays specified and unrun, to be pulled the moment animation is
   actually proposed — most likely at stage 03, where generated clips may be
   animation-like. The $0.50 and the 45 minutes are not spent this session.
2. **O3 gains a step:** verify each print is actually in colour, and normalise the
   encode, before `cinemetrics.py` runs.
3. **The stage-02 README's struck-through pairing can now be replaced** with the
   triad above.

## Sources

- Gruber et al. (2024), [Between-movie variability severely limits generalizability of "naturalistic" neuroimaging](https://www.biorxiv.org/content/10.1101/2024.12.03.626542v1.full)
- Kauttonen et al. (2015), [Optimizing methods for linking cinematic features to fMRI data](https://pubmed.ncbi.nlm.nih.gov/25662868/)
- Aliko et al. (2020), [A naturalistic neuroimaging database for understanding the brain using ecological stimuli](https://www.nature.com/articles/s41597-020-00680-2)
- Geerligs et al. (2022), [A partially nested cortical hierarchy of neural states underlies event segmentation](https://elifesciences.org/articles/77430)
- [Detecting agency from the biological motion of veridical vs animated agents](https://pubmed.ncbi.nlm.nih.gov/18985141/)
- Internet Archive metadata API, per-identifier, read 3 September 2026
