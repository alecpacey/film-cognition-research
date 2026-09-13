# Experiment roadmap

Sequential. Each stage gates the next and is allowed to kill it. Pull the next
stage only when the previous one has a written RESULT.md.

**Thesis:** build an index from cinematographic technique to cortical response
profile, then invert it — specify the profile, choose the technique that reaches it.

---

## 00 · Probe — does the sensor work? ✅ COMPLETE

Does TRIBE discriminate content at all. **PASS.** Mean top-10 overlap 0.15 against
a 0.60 threshold; anatomically correct on all three clips; double dissociation
between the voice chain and the place chain, with a graded middle condition.
Reproducible to 2dp. Output rate confirmed 1 Hz. See `00-probe/RESULT.md`.

---

## 01 · Gate — does *technique* move it? ✅ COMPLETE

The first genuine test of the thesis. Cut rate on **identical footage**: the same
two scenes intercut at 1, 3, 7, 15, 31 cuts. Every condition contains exactly the
same 30 s of each scene; only the cutting differs.

Cut rate is the gate rather than the index because it is the only dial that can be
varied with content perfectly constant, and it carries the largest documented
effect in the literature (montage context, η²p 0.715). If technique cannot move
the sensor when varied this cleanly and this strongly, no subtler dial will.

**PASS.** 51 of 180 parcels at |r| > 0.9 against log cut count, against a bar of 15
and a chance expectation of ~7. Dorsal attention over-represented (3 of 7 vs 1.98
expected). Strongest responders were inferior-frontal — IFJa r = +0.996 — i.e.
cognitive control rather than the predicted attention network: every cut is a
switch. Identical footage throughout. See `01-cutrate/RESULT.md`.

**If it fails:** the control claim is dead and so is the directed film. Fall back
to the collapse film, which needs no control law.

---

## 02 · Index — the observational track ✅ COMPLETE — PARTIAL

The stage that produces the actual crosswalk. Score many real film segments and
correlate parcel response against measured dials.

1. Cut **three** public-domain live-action Technicolor features into fixed,
   non-overlapping 60 s segments — *Nothing Sacred* (1937), *Jungle Book* (1942),
   *Royal Wedding* (1951). **Different directors on purpose** — dialogue pictures
   alongside landscape pictures alongside a musical — because directors covary
   their dials, and varying the director is the cheapest way to break that
   covariance without a lab. Corpus reasoning, archive identifiers and the
   encode-normalisation requirement are in `02-index/CORPUS.md`.
2. `cinemetrics.py` on each → cut rate, camera motion, luminance, contrast,
   colour, depth of field. Free, but **~28 s** per 60 s segment at 720p — measured on the real corpus, not the ~2 s previously assumed.
3. TRIBE on each → 180-parcel vector. ~$0.17 per segment.
4. Penalised regression (elastic net) of parcels on dials. **Elastic net, not OLS**
   — Kauttonen 2015 hit exactly this multicollinearity with 37 cinematic features.
5. Null by **permutation over segment labels** — not a spin test. This is a
   regression across segments, not a map-to-map comparison; spin tests belong at
   stage 03+ when comparing against external maps such as Neurosynth terms.
6. **Replication check:** the inferior-frontal cut-rate cluster from stage 01 must
   reappear. If controlled and observational disagree, resolve that first.

**Cost:** 30 segments ≈ $5 · 100 segments ≈ $17.

**Output:** the technique → parcel profile index. This is the deliverable the
whole thesis is built toward.

**The index will be corpus-conditional, and must be reported as such.** Gruber et
al. (2024) found substantial between-movie variability in ISC — *F*(7,385) = 4.65,
η²G = 0.048 across eight films — with downstream effects landing in non-overlapping
regions for nearly every film. Their conclusion, that a specific movie should be
treated like a specific task, applies directly to us: three films is enough to
break covariance, not enough to claim the index is film-independent.

---

## 01b · Synthetic-imagery transfer — **prerequisite for stage 03** ✅ PASS (11 Sep 2026)

Originally specified as an *animation* gate, when the stage-02 corpus was assumed
to be animated Technicolor features. O1 removed that assumption, so 01b is no
longer a stage-02 gate. It is reclassified here because it answers something
**stage 03 needs regardless**.

TRIBE's encoding head was fitted on 121 h of live action, 64.5 h of it *Friends*.
Stage 03 does not use live action — it **generates** clips, and generated video is
out-of-distribution for that head in the same ways animation is: non-physical
motion, flat colour fields, hard edges, synthetic faces. The head fails silently,
returning plausible numbers. Running stage 03's ~$60 of generation against a sensor
that cannot see generated imagery would produce a confident, worthless result.

So the question is not "can we film a cartoon" but **"does the sensor survive
synthetic imagery"** — and the clips should therefore probably be *generated*
rather than hand-animated, testing the case stage 03 actually faces.

**This reclassification is an argument, not a finding.** Whether generated and
hand-animated footage are out-of-distribution in the same way is untested and may
be false. If it is false, 01b as written tests the wrong thing and needs
respecifying before it is run.

**Respecified 9 September 2026 in `01b-transfer/README.md`**, criteria fixed there
before generation. Three changes from the held design: generated rather than animated
material, from the stage-03 generator (MiniMax H3 Max via fal); a third criterion
requiring the generated face − landscape contrast to reproduce **axis 1 of the stage-02
index** at *r* ≥ 0.50 (live-action reference +0.936); and two arms, silent and
audio-matched, to settle the audio protocol stage 03 will need. **Cost is ≈ $17–30
generation plus ≈ $1 scoring**, not the ~$0.50 previously stated — that figure covered
scoring only, and 60 s clips are 6–10 stitched generations at fal's per-second pricing.

**Also its second job:** once stage 02 has a written RESULT, 01b is the
disambiguator for the generalisation test below.

---

## 02b · Generalisation test — does the index hold outside live action? ✅ RUN (exploratory, n=3, 13 Sep 2026)

Pull only after stage 02 has a written RESULT. **Not a second corpus arm.**

Pooling animated segments into the stage-02 elastic net was considered and
rejected: animated films are the *minimum*-variance case (Gruber et al. chose them
precisely because they are "stylistically and thematically similar"), so they add
little of the covariance-breaking that a second corpus exists for — while the
live-action/animation difference looks like an **interaction** rather than an
offset, which within-film centring does not remove. Pooling risks corrupting the
deliverable to enlarge it.

Instead: measure dials on out-of-medium segments, predict their parcel vectors from
the **already-fitted** index, and compare predicted against actual. Same GPU cost
per segment, no refitting, and it answers the boundary question — how far the
crosswalk reaches — which is worth more than a slightly larger training set.

**01b runs immediately before.** Without it, a failure cannot be attributed: the
index may have failed, or the sensor may simply not see the medium.

---

## 03 · Isolation — controlled clips (pull when 02 identifies candidates)

Whatever 02 flags as interesting but confounded, isolate it. Generate clips that
hold every dial fixed and move one. This is the only place causal claims are
available; observational data cannot get there.

Regress on **measured** technique, not requested technique — `cinemetrics.py`
tells you what the generator actually produced, so poor prompt adherence becomes
variation rather than error.

**Gated by 01b above.** Do not spend generation budget until the sensor is known
to respond to generated imagery.

**Cost ~$60** generation plus GPU.

---

## 04 · Inversion — the control law

Given a target profile, choose the technique. Verify the achieved profile matches.
This is the thesis realised, and the point at which a directed film becomes possible.

---

## Standing rules

| | |
|---|---|
| **Criteria before the run** | Written in the stage README, never softened afterwards |
| **Persist to disk, not to the Space** | The Space's filesystem is wiped on pause; run 00's raw output was lost that way |
| **Foreground the log fetch** | Both background pollers were killed silently with no output |
| **Introspect before writing** | Six of seven failures in run 00 were assumed API shapes. Seconds to check, ~35 min to get wrong |
| **Batch everything into one run** | Each Space restart is ~7 min |
| **Pause the Space when done** | It bills while idle, and the sleep timer is raised to 7200 s so it cannot nap mid-run |
