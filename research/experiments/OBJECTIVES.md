# Session objectives — 3 September 2026

Ordered. Each objective has a written definition of done, and objectives 2 and 3
are gates: they are allowed to stop the ones after them. Derived from
`HANDOFF.md` § *First actions next session* and `02-index/README.md`
§ *Prerequisites*.

**Budget for the whole session: ~$1.20 GPU** on top of the $4.35 spent to date.
Wall-clock is the binding constraint, not money — roughly 5 h, of which ~1.5 h is
GPU that runs unattended.

---

## Sequencing, and why it is this order

**This section was rewritten after O1 ran.** It originally said O2 was the
evaluation whose outcome defined O3's inputs — 01b deciding whether animated
material merged into the stage-02 corpus. O1 settled that question on cheaper
evidence than a GPU run, so O2 no longer gates anything in this session and the
dependency is now simply **O1 → O3 → O4**.

O1 was free and chose the corpus. O3 is free and can kill dials before they are
paid for. O4 is the first spend against the actual dataset.

**Where animation went** — the reasoning is in `02-index/CORPUS.md` and the
reclassification in `ROADMAP.md`. In short: animation is not a deferred second
corpus arm. Pooling an animated arm into the same elastic net would add little
covariance-breaking (animated films are the *minimum*-variance case) while risking
an interaction that within-film centring cannot remove. Its two real jobs are a
**stage-03 prerequisite** and a **post-index generalisation test**, both of which
come after stage 02 has a written RESULT.

---

## O1 · Corpus and segmentation methodology — *research, free* — ✅ **DONE**

Written up in `02-index/CORPUS.md`. The animated-Technicolor assumption is
**dropped**: six public-domain live-action Technicolor features verified against
two animated ones, so the availability premise behind it is false. Corpus is
*Nothing Sacred* (1937) · *Jungle Book* (1942) · *Royal Wedding* (1951).
Segmentation is fixed 60 s, non-overlapping. A new confound — encode/resolution
heterogeneity across prints — was found and handled there.

All four questions from `HANDOFF.md` are answered in `CORPUS.md`: segmentation
unit, corpus composition, prior art, and availability in two lists. The two-list
requirement earned its keep — the live-action list is what made an 01b failure
cost nothing instead of a session.

**Done when:** written to `02-index/CORPUS.md` — segmentation rule chosen with
its reason, primary corpus (2–3 titles, named, with archive IDs and runtimes),
fallback corpus if animation is out, and the pooling decision. Assumptions
labelled as assumptions, per the standing rule that produced this session.

**Branch to check first:** if the live-action list can supply 2–3 public-domain
**colour** features that differ enough in style, animation is not needed for
stage 02 at all, and **O2 defers** — it becomes a gate to run only when
animation is actually proposed. Check this before sourcing animated clips.

---

## O2 · 01b — ⏸ **NOT RUN THIS SESSION · reclassified**

> The branch written below fired on O1's evidence: animation does not enter the
> stage-02 corpus, so the gate has nothing to decide here.
>
> **It is no longer a stage-02 gate at all.** 01b has been reclassified in
> `ROADMAP.md` as a **stage-03 prerequisite** — stage 03 generates clips, and
> generated video is out-of-distribution for an encoding head fitted on live
> action in the same ways animation is: non-physical motion, flat fields,
> synthetic faces. The question 01b asks is therefore not "can we film a cartoon"
> but "does the sensor survive synthetic imagery", which stage 03 needs answered
> whether or not animation is ever in a corpus.
>
> **That reclassification is an argument, not a finding.** Whether generated and
> hand-animated footage are out-of-distribution in the same way is untested, and
> may be false. Which is why the roadmap entry says the clips should probably be
> *generated* rather than animated — testing the case stage 03 actually faces.
>
> Everything below is the pre-registered design, held. Criteria were fixed before
> O1 ran and are not to be softened when it is eventually pulled.

### (held) 01b — animation transfer gate — *~30 min GPU, ~$0.50*

**The question.** TRIBE's encoding head was fitted on 121 h of live action, 64.5 h
of it *Friends*. Animation appears nowhere. The V-JEPA-2 backbone has almost
certainly seen animation; the feature→BOLD head has not, and it fails silently,
returning plausible numbers. Does the sensor transfer?

**Method.** Run 00's three-way content probe, on animated material. Same
harness — `space_app.py`, `mode="video"`, `audio_only=True`, three 60 s clips
from **one** animated feature so that content is the only thing varying, exactly
as `00-probe/CLIPS.md` argues.

Clip selection is objective, not by eye: run 00's first face candidate was picked
visually and contained fewer faces than its crowd clip. Scan the feature with
YuNet at 4 s intervals and rank windows on mean largest-face area, as before.
Animation is the harder case here — YuNet is trained on photographic faces and
may under-detect drawn ones. If detection collapses, fall back to hand-selection
and **say so in RESULT.md** rather than reporting a rank as if measured.

### Pass criteria — fixed now, before the run, not softened after

1. **Separation.** Mean pairwise top-10 Jaccard overlap across the three animated
   clips **< 0.60**. Same bar as run 00, which scored 0.15.
2. **Direction.** Animated scenery ranks the place chain — VMV1–3, PHA1–3 —
   above the other two clips; animated dialogue ranks the voice chain — A4, A5,
   STSdp, STSvp — above the other two. Both must hold.

**PASS** on both: animated material **merges** into the stage-02 corpus and O3
segments it alongside the live-action titles.

**FAIL** on either: animation does not merge, the animated-Technicolor assumption
is dropped on evidence, and the corpus is O1's live-action list alone.

**PARTIAL** — separation without direction — means TRIBE responds to something
about animation but not the semantics assumed. Treat as fail for corpus purposes
and write up what it does respond to.

**Reported, not gating:** correlation between the animated `face − landscape`
contrast vector and run 00's live-action one (STSdp +6.03, A5 +5.63, STSvp +3.92
… VMV2 −5.09, PHA2 −4.72, PHA1 −3.66). A high correlation is strong evidence of
transfer; a low one with criteria still met is worth knowing and does not change
the verdict. No threshold is set on it because none was set before run 00, and
inventing one now would be a post-hoc criterion.

**Done when:** `01b-animation/` holds `README.md` with these criteria copied in
*before* the run, `CLIPS.md` with provenance and window statistics,
`RESULT.md` with the verdict, and `LOG.md` carries a line — including if it
crashed.

---

## O3 · Segment, measure dials, check variance — *free*

No GPU. This is the objective that decides what the GPU is later spent on.

0. **Verify each print is actually in colour**, and **normalise the encode** —
   same resolution, codec and CRF across all three films — before any dial is
   measured. Both steps are O1 findings; see `02-index/CORPUS.md`.
1. Segment each corpus film into non-overlapping 60 s segments, fixed and
   non-overlapping per O1's rule, into `02-index/segments/`. Re-encode, never stream-copy — a stream copy
   starts on the nearest keyframe and silently yields a short clip, which is the
   exact failure that returns confident noise. Verify every segment's duration
   with ffprobe and that none straddles a reel change.
2. `cinemetrics.py` over all segments → dial table. Free, but ~28 s per 60 s
   segment at 720p (measured), so ~30 min at 4 workers for the full 244.
3. **Check dial variance before paying for GPU.** Centre every dial within film,
   per the decision recorded in `HANDOFF.md`, then for each dial report:
   within-film SD, range, and correlation with film identity. A dial that barely
   varies cannot be tested and must be dropped here, not after it has been paid
   for.

> **NOTE — open decision, deferred to O3.** The drop threshold is not yet set.
> It must be fixed **before** `cinemetrics.py` is run over the corpus and never
> after, per the standing rule, but the number itself is taken when we reach O3
> and can see the corpus it applies to.
>
> Standing proposal to accept or replace at that point: drop a dial whose
> within-film interquartile range spans less than **10%** of the range that dial
> takes across the whole corpus. Separately, flag — without dropping — any dial
> still correlating with film identity at |r| > 0.5 after centring; centring
> should have removed that, and a residual means something is wrong with the
> segmentation.

**Done when:** `02-index/DIALS.md` holds the table, the variance check, and the
list of dropped dials with the number that dropped them. Dropped dials are
reported with equal prominence to retained ones — a dial you cannot direct with
is a finding.

---

## O4 · Batch 0 — pipeline proof — *~40 min GPU, ~$0.70*

4 segments, 2 per film. **Not for analysis** — it proves the pipeline end to end
on new material.

Pre-flight, all of which have bitten before (`LOG.md`). **Checked 4 Sep 2026:**

- [x] Space `.gitignore` allow-lists `probe_clips/*.mp4` — confirmed present as an
      explicit `!probe_clips/*.mp4` override of the `*.mp4` rule, and proven by the
      five stage-01 clips actually sitting in the repo
- [x] Space repo intact after the pause — 48 files, `src/tribescore/` all 11
      modules, and `space_app.py` deployed under its runtime name `app.py`
- [x] Sleep timer 7200 s; stage `PAUSED`, so not billing
- [ ] Log fetch runs in the **foreground**. Both background pollers were killed
      silently with no output

### ⚠ `run_batch.py` does not respect the pre-registered selection

Found during the pre-flight. `pending()` returns *every* unscored `segments/*.mp4`
sorted alphabetically, and `--batch N` takes the first N. With 244 segments on disk
that means batch 0 would score `jungle_book_000..003` — four consecutive segments
from the opening of one film — instead of the stratified sample fixed in
`README.md` § *Segment selection*.

Left as written, this silently substitutes convenience sampling for the design, and
nothing in the output would reveal it.

**Fix before O4:** `run_batch.py` must draw its candidates from `selection.json`
and refuse to run if that file is absent, so the design cannot be bypassed by
accident.

```sh
python run_batch.py --plan       # no cost
python run_batch.py --batch 4
python run_batch.py --harvest    # fetches, verifies, pauses the Space
```

**Done when:** `--harvest` reports 4 clips at 180 parcels each, no NaN, no |z| > 8,
and filenames align between the dial table and the parcel table.

`--harvest` is **pipeline health only**. It is not a look at the result: the
statistical test in `02-index/README.md` runs once, on the complete set. The one
pre-declared exception stays as written — if after 20 segments no dial reaches
|r| > 0.3 with any parcel, stop for futility.

---

## O5 · Close the session — *free*

- [ ] `LOG.md` line per run, crashes included
- [ ] `RESULT.md` for 01b, verdict written against the criteria as fixed
- [ ] `ROADMAP.md` and `02-index/README.md` updated where 01b or O1 changed them —
      the struck-through *His Girl Friday* pairing gets replaced by the chosen corpus
- [ ] `HANDOFF.md` rewritten for the next session
- [ ] **Space paused**, and the pause confirmed — it bills while idle
- [ ] `tribe-minimax-reactive-stream/brief.html` synced if any published claim moved

---

## Running totals

| | GPU | wall-clock |
|---|---|---|
| O1 research | — | done |
| O2 01b gate | ~~$0.50~~ **$0 — deferred** | — |
| O3 fetch, normalise, segment, dials | — | ~1.5 h + download |
| O4 batch 0 | ~$0.70 | ~50 min |
| **Session** | **~$0.70** | **~3 h** |
| **Project to date** | $4.35 → **~$5.05** | |
