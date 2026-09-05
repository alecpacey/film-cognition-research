# Automatic cinematography annotation

Scope: models and methods that take a video clip and emit technique labels — shot scale, camera movement, camera angle, lighting key, colour statistics, cut rate, depth of field — so that ~40–200 short generated clips can be annotated without hand-labelling.

Researched 2026-09-01. Every repo and HF id below was fetched and confirmed to exist; anything I could not verify is marked **[unverified]**.

## Recommendation

**Run the no-model baseline on everything, and add exactly one model — `Vchitect/ShotVL-7B` — for the two dials the baseline genuinely cannot measure: camera angle and lighting type.**

The reasoning, in order of how much it should move the decision:

1. **Five of the seven dials are image statistics, not perception.** Cut rate, camera movement, lighting key, colour, and depth of field are all directly measurable. I wrote and validated the code (`cinemetrics.py`, in this directory) against synthetic clips with known ground truth: **16/16 correct**, including all six camera-motion axes (static, pan, tilt, push, pull, roll). It needs no weights, no GPU, and no network. It runs a 1080p 5-second clip in **~2 seconds**, so all 200 clips take **under 7 minutes** on one CPU process. A fine-tuned transformer that predicts "push_in" is not better than measuring that the frame-to-frame affine scale compounded to 1.49.

2. **Shot scale is half-solved by the baseline and needs a fallback.** Face-box area works cleanly from extreme close-up down to full shot, but YuNet stops detecting at a roughly fixed *pixel* size (~30–40px box — measured, see below), so genuine wide shots return `no_face`, indistinguishable from a shot with no person in it. For those clips use the model.

3. **You already know the answer.** These are *your* generated clips — the prompt that produced each one states the intended shot scale, movement and lighting. The task is **verification**, not discovery: flag the clips where the measured label disagrees with the prompt. That reframing matters, because it means a metric with a known bias is still useful (the bias is constant across clips) and you only need human eyes on the disagreements — realistically 10–20% of the set.

**Do not** reach for VideoLLaMA / InternVideo / generic Qwen-VL prompting. ShotBench evaluated 24 VLMs on exactly this task and found GPT-4o at **59.3%** average, with roughly half of all models below 50%, and camera movement, lens size and composition "often approaching random accuracy". Prompting a general VLM would produce labels less reliable than an optical-flow calculation you can debug.

**Concretely:** run `cinemetrics.py` over all clips (~7 min), diff the output against the prompt metadata, then run ShotVL-7B only on the disagreements plus the `no_face` clips for angle/lighting/scale. Budget a few hours end to end, most of it the one-time ShotVL setup.

## Model options

| Model / tool | What it labels | Accuracy if reported | Licence | HF id or repo | Setup cost |
|---|---|---|---|---|---|
| **`cinemetrics.py`** (this dir) | cut rate, camera movement (6 axes), lighting key, colour stats, DoF proxy, shot-scale proxy | 16/16 on synthetic ground truth (my tests, below) | yours | — | **None.** opencv-python + numpy |
| **ShotVL-7B** ⭐ | 8 dimensions: shot size, framing, **camera angle**, lens size, **lighting type**, **lighting conditions**, composition, camera movement | 70.1 avg on ShotBench. Per-dim: size 81.2, framing 90.1, angle 78.0, lens 68.5, lighting type 70.1, lighting cond. 64.3, composition 45.7, movement 62.9 | **Apache 2.0** | `Vchitect/ShotVL-7B` | Qwen2.5-VL-7B fine-tune; ~16GB GPU. Takes images *or* video. vLLM/SGLang/transformers |
| ShotVL-3B | same 8 dims | lower than 7B **[unverified per-dim]** | Apache 2.0 **[unverified]** | `Vchitect/ShotVL-3B` | smaller GPU |
| **VideoMAE MovieShots (multitask)** | shot scale (ECS/CS/MS/FS/LS) + movement (Static/Motion/Pull/Push) | scale 88.32% acc / 88.57 macro-F1; movement 91.45% acc / 80.8 macro-F1 | **MIT** | `gullalc/videomae-base-finetuned-kinetics-movieshots-multitask` | 86M params, runs on CPU. One-line `pipeline()` |
| VideoMAE MovieShots (scale only) | shot scale, 5 classes | 88.93% acc / 89.19 macro-F1 | MIT | `gullalc/videomae-base-finetuned-kinetics-movieshots-scale` | as above |
| VideoMAE MovieShots (movement only) | movement, 4 classes | 91.35% acc — but **Pull only 51.25%**, Static 92.94% | MIT | `gullalc/videomae-base-finetuned-kinetics-movieshots-movement` | as above |
| **CameraBench / cam-motion** | camera motion primitives (taxonomy built with cinematographers), motion captioning, video-text retrieval | "SOTA for classifying camera motion"; ~doubled AP over base after SFT on ~1,400 clips. No per-class table on the card | **"other"** — check before shipping | `chancharikm/qwen2.5-vl-7b-cam-motion` (also `-32b`, `-72b`) | Qwen2.5-VL fine-tune, **8.0 fps input**. NeurIPS 2025 Spotlight |
| CineScale | shot scale, 9 classes (ECU→ELS + FS, IS) | VGG-16: 94% precision / 94% recall | **[unverified]** | github.com/CineScale | **Weights not clearly released** — dataset (792k frames, 124 films) on Mendeley. Frame-level, not clip-level |
| MovieNet / movienet-tools | shot scale (5) + movement (4); source of the MovieShots benchmark | — | **[unverified]** | github.com/movienet/movienet-tools | Use the VideoMAE models above instead — same labels, packaged |
| AVE (ECCV 2022) | shot-size, **shot-angle**, shot-type, shot-motion, subject, location, #people, sound-source — 1.5M tags / 196k shots | — | **not specified in repo** | github.com/dawitmureja/AVE | **Dataset only, no checkpoint.** Clips must be re-scraped from YouTube. Training cost, not a runnable model |
| PySceneDetect | cuts / shot boundaries | — | BSD-3 | github.com/Breakthrough/PySceneDetect | `pip install scenedetect`. v0.7.1 |

Notes that matter when choosing:

- **ShotVL is the only option covering camera angle and lighting.** Nothing else in the table labels high/low angle or lighting type. That is why it is the one model I recommend.
- **The VideoMAE MovieShots models are the cheapest real model** (86M params, MIT, CPU-viable) and their headline numbers are the best in the table — but they only re-measure scale and movement, which the baseline already does. Their `Pull` class at 51.25% is barely better than a coin flip, whereas the baseline measures net zoom directly and got push/pull exactly right (1.488 and 0.674 against ground truths of 1.5 and 0.667). Worth using only as a cross-check on shot scale for `no_face` clips.
- **PySceneDetect is not needed as a dependency** — the 30 lines in `cinemetrics.py` do the same job and let you use the adaptive rule that these clips actually require (see below). Install it if you want a maintained implementation.

## The no-model baseline

Measurable with plain OpenCV/numpy, no ML: **cut rate, camera movement, lighting key, colour statistics, depth of field**, and **shot scale down to a full shot**. Not measurable this way: **camera angle** and **lighting type/direction** (key vs fill vs practical) — those need ShotVL.

Full runnable script: **`research/cinematography/cinemetrics.py`** (450 lines, compiles clean, validated).

```bash
pip install opencv-python numpy
# 233KB face model, once — note the media. host, raw.githubusercontent returns an LFS pointer
curl -L -o yunet.onnx "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"

python cinemetrics.py 'shots/*.mp4' --json labels.json --stride 2
```

### Camera movement — the one that needed real care

Fit a partial affine transform between adjacent frames (Shi-Tomasi corners + Lucas-Kanade + RANSAC). It decomposes into translation, scale and rotation, which map straight onto pan / tilt / push / pull / roll.

The subtlety that makes or breaks this: **read the translation at the frame centre, not at the origin.** `M[:,2]` is the shift of the top-left corner, so a pure zoom or roll about the centre shows up there as a large fake pan. Before fixing this my push-in clip reported `pan_right+tilt_down+push_in`; after, the spurious translation dropped from ~3e-3 to ~1e-5 and all six axes came out clean.

```python
scale = math.hypot(M[0, 0], M[1, 0])
rot   = math.degrees(math.atan2(M[1, 0], M[0, 0]))
cx, cy = W / 2.0, H / 2.0
dx = M[0, 0] * cx + M[0, 1] * cy + M[0, 2] - cx   # centre-referenced
dy = M[1, 0] * cx + M[1, 1] * cy + M[1, 2] - cy
```

Second subtlety: **aggregate with the median, not the sum or product.** A 0.5% per-frame scale error compounds to 40% over 72 frames. Take the median per-frame log-scale and extrapolate: `zoom = exp(median(log(scales)) * n)`.

Validated against ffmpeg-synthesised clips with known moves — **6/6 exact label matches**:

| clip | ground truth | measured |
|---|---|---|
| static | no motion | `static`, pan/tilt ≈ 0.00000 |
| pan | window slides right | `pan_right` |
| tilt | window slides down | `tilt_down` |
| push | zoom 1.0 → 1.5 | `push_in`, net_zoom **1.488** |
| pull | zoom 1.5 → 1.0 | `pull_out`, net_zoom **0.674** (truth 0.667) |
| roll | rotate 0.15 rad/s × 3s = 25.8° | `roll_ccw`, **24.4°** |

### Cut rate — use the adaptive rule, not a fixed threshold

**This is the single most important correction in the baseline.** The textbook approach (mean absolute HSV delta vs a fixed threshold of 27, PySceneDetect's `ContentDetector` default) is *unusable on camera-moving clips*: a smooth pan pushes every frame over the threshold. On my pan clip, fixed-threshold detection reported **71 cuts in a 72-frame single take**. Generated clips are frequently one continuous move, so this would have corrupted the whole dataset.

Compare each frame's delta against a **rolling median** of its neighbours instead, and require both a relative and an absolute condition:

```python
s = np.asarray(scores)          # mean abs HSV delta per adjacent pair
for i, v in enumerate(s):
    lo, hi = max(0, i - 9), min(len(s), i + 10)
    ctx = np.concatenate([s[lo:i], s[i + 1:hi]])
    med = float(np.median(ctx))
    if v >= 18.0 and v >= 3.0 * max(med, 1.0):
        cut_idx.append(idxs[i])
```

After the fix: **5/5** — 2 cuts found in the 3-segment clip (frames 24 and 48, exactly right), and 0 cuts on the static, pan, push and roll single-takes.

### Lighting key — histogram shape, not mean brightness

Low-key puts most pixels in shadow with a small highlight tail; high-key fills the top and empties the shadows. So discriminate on the *shape*: median plus the mass in the bottom and top deciles.

```python
p   = hist / hist.sum()
cdf = np.cumsum(p)
median         = int(np.searchsorted(cdf, 0.5))
shadow_frac    = float(p[:26].sum())     # bottom 10% of range
highlight_frac = float(p[230:].sum())    # top 10%
if   shadow_frac    > 0.35 and median <  80: key = "low_key"
elif highlight_frac > 0.20 and median > 150: key = "high_key"
else:                                        key = "mid_key"
```

**3/3** on a properly textured test scene (low 13 median / 0.71 shadow, high 246 / 0.86 highlight, mid 126 / 0.0 / 0.0).

### Colour statistics — Hasler & Süsstrunk (2003)

```python
b, g, r = cv2.split(bgr.astype(np.float32))
rg = r - g
yb = 0.5 * (r + g) - b
colourfulness = math.hypot(rg.std(), yb.std()) + 0.3 * math.hypot(rg.mean(), yb.mean())
warm_cool = (rg.mean() + yb.mean()) / 2.0    # +ve warm, -ve cool
```

Rough scale from that paper: <15 not colourful, ~33 average, >65 extremely colourful. Measured: greyscale **0.0**, saturated **106.65**, warm **+3.87**, cool **−5.29** — correct ordering and correct signs.

### Depth of field — centre-vs-surround sharpness

Variance of Laplacian in the centre third against the border. Shallow focus = sharp subject, soft background = high ratio.

Measured **13.04** for a synthetic shallow-focus frame vs **0.679** for a uniformly sharp one. Clean separation. Caveat: the deep-focus case landed at 0.68, not 1.0, because the centre third happened to be less textured — **the ratio is not centred on 1.0, it depends on content**, so treat it as a relative ranking across your clips rather than an absolute threshold.

### Shot scale — face-box area, with a hard floor

Use **YuNet** (`cv2.FaceDetectorYN`, ships with OpenCV ≥4.5.4), not a Haar cascade. Haar fires on texture *consistently*, so a false positive appears on every frame of a static shot and no temporal filtering removes it — my texture-only test clip reported a confident "full shot" from 45 detections across 48 frames. YuNet returns a confidence score and gave **zero** false positives on the same clips.

Then band the median face-box area fraction: >0.25 ECU, >0.10 CU, >0.03 MS, >0.008 FS, else wide.

**The floor is the thing to know.** I swept face size against detection at several resolutions:

| analysis resolution | score thr | smallest detected face box | as frame-area fraction |
|---|---|---|---|
| 640×360 | 0.85 | 41×60 px | 0.0109 |
| 1280×720 | 0.85 | 30×41 px | 0.0014 |
| 1920×1080 | 0.85 | 39×53 px | 0.0010 |
| 1920×1080 | 0.60 | 21×27 px | 0.00028 |

The floor is a roughly **fixed pixel size**, so the *fractional* floor falls ~10× by analysing at 720p instead of 360p. At 640×360 the floor (0.011) sits above the full-shot band (0.008) — every wide shot would return `no_face`. `cinemetrics.py` therefore runs face detection at native resolution while the other metrics use downscaled frames.

### Throughput

Measured on a 1080p 5-second clip: **2.28s** at stride 1, **2.07s** at stride 2. So 40 clips ≈ **1.4 min**, 200 clips ≈ **6.9 min**, single process. Parallelise across cores if it ever matters; it won't.

## Reliability caveats

**On AI-generated video specifically:**

- **Generated clips break the rigid-scene assumption behind optical flow.** The affine fit assumes the frame moves as one rigid background. Diffusion video frequently has non-rigid drift, objects that morph rather than translate, and background texture that boils between frames. RANSAC will find *a* dominant transform, and it may be the average of an incoherent field rather than a camera move. **Mitigation:** the script reports `jitter` (spread of per-frame deltas) and `n_pairs` alongside every label — high jitter with a confident label is the signature of this failure, so treat those clips as needing review. I have not measured this failure rate on real generated footage; validation was on synthetic clips. **[unverified on generated video]**
- **Temporal flicker inflates cut counts.** Frame-to-frame luminance and colour instability is common in generated video and is exactly what a content-based cut detector keys on. The adaptive rule helps (flicker raises the *local median* too, so it partly cancels), but a clip with a sudden coherence break may register a real-looking cut. Sanity-check any clip reporting cuts you did not prompt for.
- **Lighting-key thresholds are calibrated on nothing.** My values came from synthetic fixtures. Generated video often has flatter, more diffuse lighting than film stock, so the low/high-key bands may need re-cutting. Run the metric over your set first, look at the distribution, then set thresholds at its natural breaks rather than trusting my constants.
- **Face detectors are trained on real faces.** YuNet on AI-generated faces — especially stylised or non-photoreal characters — will have a different (probably worse) detection rate than the numbers above, which were measured on a photograph. For a stylised character the shot-scale proxy may fail wholesale. **[unverified]**

**On the models:**

- **General VLMs are not reliable annotators here.** ShotBench: GPT-4o **59.3%** average across the 8 dimensions, ~half of 24 tested models below 50%, and models "frequently confuse semantically adjacent categories (e.g. medium shots vs. medium close-ups)". Scaling does not rescue it — 72B models plateau well below expert accuracy. Even ShotVL, the purpose-built SOTA, gets **45.7% on composition** and **62.9% on camera movement** — i.e. *worse at camera movement than the optical-flow baseline*, which is the clearest argument for using the baseline as primary.
- **CameraBench found VLMs and geometry fail in opposite directions**: SfM/SLAM "struggle to capture semantic primitives that depend on scene content" (e.g. *following* a subject), while VLMs "struggle to capture geometric primitives that require precise estimation of trajectories". The baseline here is the geometric kind, so its blind spot is semantic: it cannot tell a tracking shot that follows a character from a pan across a static scene. If tracking-vs-pan is a dial you care about, that specific distinction needs a model.
- **Zoom vs dolly is genuinely ambiguous from pixels alone.** The CameraBench authors note even human novices "confuse zoom-in (a change of intrinsics) with translating forward (a change of extrinsics)". My baseline reports both as `push_in` and cannot separate them. Neither can any 2D-flow method, in principle — it needs parallax analysis.
- **The MovieShots `Pull` class is unreliable** at 51.25% despite the 91.35% headline. Macro-F1 (80.8%) is the honest number for that model, not accuracy.
- **Training-domain mismatch throughout.** Every model in the table was trained on film and trailer footage (MovieNet, MovieShots, internet video). Short generated clips are a different distribution and reported accuracies should be treated as upper bounds.
- **Licence gaps:** CameraBench models are `other` and AVE specifies no licence. Check both before anything ships. ShotVL (Apache 2.0) and the VideoMAE models (MIT) are clean.

**Method caveat on my own numbers:** the 16/16 is against *synthetic* clips with programmatic ground truth, which validates that the maths is correct and the thresholds separate clean cases. It is not evidence about real generated footage. Two of my first-pass fixtures were themselves invalid (an animated `testsrc2` source, and a mostly-black scene) and produced misleading failures until replaced — worth remembering if you re-tune the thresholds.

## Sources

1. [gullalc/videomae-base-finetuned-kinetics-movieshots-multitask](https://huggingface.co/gullalc/videomae-base-finetuned-kinetics-movieshots-multitask) — MIT, scale 88.32% / movement 91.45%
2. [gullalc/…-movieshots-scale](https://huggingface.co/gullalc/videomae-base-finetuned-kinetics-movieshots-scale) — 88.93% acc
3. [gullalc/…-movieshots-movement](https://huggingface.co/gullalc/videomae-base-finetuned-kinetics-movieshots-movement) — 91.35% acc, Pull 51.25%
4. [Vchitect/ShotVL-7B](https://huggingface.co/Vchitect/ShotVL-7B) — Apache 2.0, Qwen2.5-VL-7B fine-tune, 70.1 avg
5. [ShotBench GitHub](https://github.com/Vchitect/ShotBench) — 8 dimensions, per-dimension accuracy table
6. [ShotBench project page](https://vchitect.github.io/ShotBench-project/) / [alphaXiv 2506.21356](https://www.alphaxiv.org/overview/2506.21356) — GPT-4o 59.3%, 24 VLMs evaluated
7. [CameraBench GitHub](https://github.com/sy77777en/CameraBench) — NeurIPS 2025 Spotlight; model ids
8. [chancharikm/qwen2.5-vl-7b-cam-motion](https://huggingface.co/chancharikm/qwen2.5-vl-7b-cam-motion) — licence "other", 8.0 fps
9. [Towards Understanding Camera Motions in Any Video (arXiv 2504.15376)](https://arxiv.org/abs/2504.15376) — SfM vs VLM failure modes, zoom/dolly ambiguity
10. [MovieNet](https://movienet.github.io/) and [Shot Type ECCV 2020](https://movienet.github.io/projects/eccv20shot.html) — shot scale/movement taxonomy
11. [movienet/movienet-tools](https://github.com/movienet/movienet-tools)
12. [AVE — dawitmureja/AVE](https://github.com/dawitmureja/AVE) — dataset only, no checkpoint, no licence stated
13. [AVE paper (ECCV 2022, arXiv 2207.09812)](https://arxiv.org/pdf/2207.09812) — 196k shots, 1.5M tags
14. [CineScale](https://cinescale.github.io/shotscale/) and [CineScale GitHub](https://github.com/CineScale) — VGG-16 94%; [Mendeley dataset](https://data.mendeley.com/datasets/th46h4vdwd/1)
15. [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) / [v0.7.1 API](https://www.scenedetect.com/docs/latest/api.html) — ContentDetector vs AdaptiveDetector
16. [Computing image colorfulness — PyImageSearch](https://pyimagesearch.com/2017/06/05/computing-image-colorfulness-with-opencv-and-python/) — Hasler & Süsstrunk implementation
17. [Measuring colourfulness in natural images (Hasler & Süsstrunk 2003)](http://infoscience.epfl.ch/record/33994/files/HaslerS03.pdf)
18. [OpenCV optical flow tutorial](https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html) — Lucas-Kanade, Farnebäck
19. [OpenCV Zoo — YuNet face detector](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet)
20. [szymonrucinski/types-of-film-shots](https://huggingface.co/datasets/szymonrucinski/types-of-film-shots) — 2,919 frames, 8 shot-scale classes (dataset, if you ever want to fine-tune)

All measurements attributed to "my tests" were produced by `cinemetrics.py` in this directory against ffmpeg- and OpenCV-generated fixtures on 2026-09-01; the fixtures are reproducible from the commands recorded in the script's docstrings.
