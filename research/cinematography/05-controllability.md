# Can you actually prompt for technique?

**Short answer: partially, and unevenly — and nobody has measured it for the model we plan to use.**

Three things are true at once, and they determine how much of the prompt → technique → brain-response chain survives:

1. **The dimensions are not equally controllable.** Framing and shot scale are broadly obeyed; lighting is obeyed as *look* but is weakly verified; camera movement is the documented weak link, with the best-measured models at 62% on a 9-way movement classification and several near chance.
2. **No published benchmark evaluates MiniMax H3 or fal's H3 Max post-train.** The closest datapoint is Hailuo 2.3 in FilmBench, where it placed **last of nine T2V models (68.94 overall vs. 88.93 for the leader)**. H3 is a later generation, so this is a prior, not a measurement.
3. **fal's endpoint rewrites every prompt before the model sees it, and rewriting cannot be switched off.** `prompt_expansion_mode` is a *required* field with exactly two values, `balanced` and `quality`. There is no `off`. Every technique instruction passes through an LLM first.

Point 3 is the one that most threatens the design, and it is the cheapest to test.

## Verdict per dimension

Two different questions hide inside "controllable": *does the model produce it* (generation adherence) and *can we tell whether it did* (verifiability). A dimension is only usable for this project if both hold. The table separates them.

| Technique dimension | Controllable by prompt? | Evidence | Notes |
|---|---|---|---|
| **Shot framing** (single / two-shot / OTS / group) | **Yes — best-supported** | ShotBench: highest recognition of all eight dimensions — ShotVL 85.6%, GPT-4o 83.1%, Qwen2.5-VL-72B 82.9% ([2506.21356](https://arxiv.org/html/2506.21356v2)) | Recognition evidence only; strongly implies verifiability. Generation adherence not separately measured. |
| **Shot scale** (ECU → wide) | **Yes, model-dependent** | FilmBench shot-scale leader 79.8 (Seedance 2.0), but cross-model variance 209.0 — a wide spread ([2607.24241](https://arxiv.org/html/2607.24241v1)). ShotBench recognition: ShotVL 77.9%, Qwen-72B 75.1% | The safest *semantic* dimension. Verify objectively via subject bounding-box height as a fraction of frame height — do not need a VLM. |
| **Lighting** (low-key / high-key, lighting type) | **Probably yes for look; verification is the weak point** | FilmBench: "static image-quality sub-metrics (sharpness, **lighting**) score markedly higher" than dynamic ones. ShotBench recognition: lighting *type* 65.7%, lighting *condition* only 53.1% | Note the asymmetry: models render lighting well but VLMs classify it poorly. **Verify with luminance histogram statistics** (mean luma, dark-pixel fraction, contrast ratio), not a VLM judge. |
| **Camera angle** (high / low / eye-level / Dutch) | **Untested for generation; moderately verifiable** | ShotBench recognition: ShotVL 68.8%. FilmBench has a viewing-angle sub-metric with high cross-model variance (200.5) | No direct generation-adherence number found. Treat as a "test before relying on it" dimension. |
| **Camera movement** (dolly, pan, tilt, orbit, crane) | **No — this is the weak link** | VBench-2.0, 9-way movement set: **Kling 1.6 61.73%, HunyuanVideo 33.95%, CogVideoX-1.5 33.33%, Sora 27.16%** ([2503.21755](https://arxiv.org/html/2503.21755v1)). FilmBench: camera movement has the **highest cross-model variance of any sub-metric (357.6)**, leader 86.5 falling "toward the low 50s" | Several models sit at or below chance. This is the single most-documented failure. |
| **Camera movement — rotational** (orbit, arc, whip pan) | **No — worst case** | CineTechBench: best models show **RotError 21.68° (Kling 1.6) to 27.80° (Wan2.1)**; "camera rotation remains a particularly challenging dimension, with consistently low accuracy." Error rises with angular velocity ([2505.15145](https://arxiv.org/html/2505.15145v1)) | Translation (push/pull/truck) degrades more gracefully than rotation. If you need movement at all, prefer translational. |
| **Focal length / lens character** (wide vs. long lens compression) | **No — and barely verifiable** | ShotBench lens size is joint-worst: ShotVL 59.3%, GPT-4o 48.9%, **Qwen-72B 46.8%** | Both the model and the judge are unreliable here. Recommend dropping this dimension from the index. |
| **Composition** (symmetry, rule of thirds, centre-framing) | **Weak** | ShotBench recognition: ShotVL 57.4% | Low verifiability. |
| **Multi-shot sequences** | **Degrades measurably** | FilmBench: single-shot → multi-shot average drop of **7.9 points**; "every model scores lower on multi-shot prompts" | Design around single-shot clips. One technique per clip. |

**The pattern:** static, framing-level properties of the image are controllable and (mostly) checkable. Anything defined by *change over time* — camera movement above all — is where both the generators and the automated judges fall apart. This is the same bottleneck FilmBench names field-wide: "the lowest-scoring sub-metrics are action performance, **camera-work appeal**, character-motion realism and emotional performance."

There is an architectural corroboration of this. The entire CameraCtrl / MotionCtrl / Direct-a-Video line of work exists *because* text conditioning does not deliver camera control — CameraCtrl's framing is that existing models "lack control of camera pose that serves as a cinematic language to express deeper narrative nuances," which is why they bolt on explicit pose conditioning. Nobody builds a pose-injection architecture for a problem that prompting already solves.

## MiniMax / Hailuo specifics

**There is a documented bracket vocabulary, and it very likely does not apply to our model.**

MiniMax officially documents 15 camera commands in `[command]` syntax:

```
[Truck left] [Truck right]      [Pan left] [Pan right]
[Push in]    [Pull out]         [Pedestal up] [Pedestal down]
[Tilt up]    [Tilt down]        [Zoom in] [Zoom out]
[Shake]      [Tracking shot]    [Static shot]
```

Syntax rules, from the official docs:
- **Simultaneous:** multiple commands in one bracket fire together — `[Pan left,Pedestal up]`. Recommended maximum 3.
- **Sequential:** `"...[Push in], then ...[Push out]"`.
- **Natural language also works,** but the docs state explicit commands "yield more accurate results."

**The critical caveat — supported models.** MiniMax lists camera-command support for exactly these:

- T2V: `MiniMax-Hailuo-2.3`, `MiniMax-Hailuo-02`, `T2V-01-Director`
- I2V: `MiniMax-Hailuo-2.3`, `MiniMax-Hailuo-2.3-Fast`, `MiniMax-Hailuo-02`, `I2V-01-Director`

**H3 does not appear in MiniMax's model list at all**, let alone in the camera-command support list. Neither does fal's `h3-max`. The bracket vocabulary is documented for the Hailuo 2.x / Director generation — a *previous* generation from the one we would be calling.

fal's own documentation for `minimax/h3-max` contains **no mention of camera control, bracket syntax, or any cinematography vocabulary**. It describes the model only as "a post-trained variant of MiniMax H3, tuned for stronger prompt adherence and better aesthetics." Its single example prompt does use natural-language cinematographic direction ("wide shot", "sweeping crane tracking motion, rising vertically") — which is suggestive of intent, but is marketing copy, not a measurement.

**Community guides claiming bracket syntax works on H3 are folklore, and the better ones admit it.** The most careful one I found states plainly: the 20 templates "were not run as new H3 tests for this article. No success rate is claimed," and advises treating the commands "as instructions to test, not buttons with deterministic outcomes." Its reliability tiering — static/pan/tilt safer, orbit/crane/tracking riskier — is reasoned from geometry (moves that reveal unseen scene content are harder), not measured, and it says so.

**The only published Hailuo-family adherence number:** FilmBench evaluated Hailuo 2.3 against eight other T2V models and scored it **68.94 overall, last place**, against Seedance 2.0 at 88.93, HappyHorse 1.1 at 87.42, Kling 3.0 at ~86, and Veo 3.1 / Grok / Vidu Q3 Pro at ~81. FilmBench's scores were validated against 90 professional raters from the Beijing Film Academy, with model-level Spearman ρ = 0.95. If technique fidelity is the load-bearing requirement, this is a reason to benchmark H3 Max against an alternative rather than assume it.

## The prompt-expansion risk

**This is the sharpest risk in the chain, and the answer is: expansion cannot be disabled on fal's H3 Max.**

From the fal API schema for both `h3-max/text-to-video` and `h3-max/image-to-video`:

- `prompt_expansion_mode` — **string, required**, default `"balanced"`
- Allowed values: **`"balanced"` and `"quality"` only**
- Documented as: *"How much effort to spend rewriting the prompt before generation. 'balanced' returns in about a second. 'quality' spends up to ~30s on a richer prompt."*
- **No `off`, `none`, or `disabled` value is documented.**

So every prompt is rewritten by an LLM before the video model sees it. `balanced` is the minimum-intervention setting, not a bypass.

**Why this endangers technique control specifically.** The research on T2V prompt rewriting is explicit that its *purpose* is distribution-matching, not intent-preservation: rewriters exist "to align diverse user inputs with captions used during model training." A precise, unusual technique instruction — "extreme close-up, low-key, single hard key from frame left, camera static" — is exactly the kind of out-of-distribution input a rewriter is built to normalise toward typical training captions. Prompt-A-Video ([2412.15156](https://arxiv.org/html/2412.15156v1)) and RAPO ([2504.11739](https://arxiv.org/html/2504.11739v1)) both note the need for reward terms enforcing "fidelity to original user intentions" — a constraint you only add because rewriters otherwise drift. The general finding in the rewriting literature is the one you'd expect: encouraging expansion raises drift; constraining terminology reduces it.

For an experimental design where the *independent variable is the technique*, an uncontrolled rewriting stage between your manipulation and the output is a confound, not just noise. If the expander adds "cinematic lighting, dramatic atmosphere, sweeping camera" to *every* prompt, your low-key and high-key conditions converge and your effect vanishes.

**The one piece of good news:** the API returns `expanded_prompt` — *"The prompt after expansion, as sent to the model."* This makes the confound **observable and auditable**. You can measure drift directly, cheaply, and without human judgment. That turns an unknown risk into a measured one.

**Mitigations, in order of preference:**

1. **Audit every generation.** Log `expanded_prompt` alongside every clip. Never analyse a clip whose expansion dropped or contradicted the technique instruction — this is an exclusion criterion, decided in advance.
2. **Write prompts that survive normalisation.** State the technique redundantly, in both technical and descriptive registers ("extreme close-up — the face fills the frame, edges cropped"), so a rewriter must delete two things to destroy the manipulation.
3. **Always use `balanced`.** It is the shallower rewrite and it is 30× faster. `quality` spends ~30s constructing a "richer" prompt, which is precisely more opportunity for drift.
4. **Check whether expansion is deterministic** under a fixed seed. If not, the expander adds per-trial variance that a fixed seed will not control — which changes how many clips per cell you need.
5. **Keep an escape hatch.** MiniMax's own API (`platform.minimax.io`) exposes Hailuo 2.3 directly, which *does* document bracket camera commands and has a `prompt_optimizer` toggle. If fal's forced expansion proves destructive, calling MiniMax directly on Hailuo 2.3 trades model quality for control integrity. That trade may be the right one for this project.

## How to verify cheaply

Nobody has measured this model, so measure it. The protocol below costs roughly **$10–20** and answers the question properly.

### Stage 0 — Expansion audit (do this first; ~$4, ~30 min)

Before spending anything on adherence, find out what the rewriter does to your instructions. `expanded_prompt` only comes back with a generation, so generate at the cheapest possible setting: **480P, 5s** ($0.125/clip at promo rate, $0.25 regular).

Send **30 prompts** covering every technique you intend to index, and analyse only the returned text:

- **Token survival:** does the technique phrase appear in `expanded_prompt`? Score verbatim / paraphrased / dropped / **contradicted** (the failure that matters most).
- **Bracket survival:** send `[Push in]` and `[Static shot]` verbatim. Does the bracket text reach the model, or does the expander eat it? This single test settles whether MiniMax's documented vocabulary is even reachable through fal.
- **Boilerplate injection:** diff expansions across conditions. If the expander injects the same cinematographic clichés everywhere, your conditions are being homogenised.
- **Determinism:** same prompt, same seed, twice. Identical `expanded_prompt`? Two clips, $0.25, and it tells you whether seed-fixing actually controls anything.

**Gate:** if technique-phrase survival is below ~80%, stop and fix prompting (or switch to MiniMax direct) before Stage 1. There is no point measuring adherence to instructions the model never received.

### Stage 1 — Adherence test (~$9–18)

**Design.** One fixed base scene, described identically across all conditions. Vary **one** technique dimension at a time (single-shot only — FilmBench's 7.9-point multi-shot penalty means never confound this with editing).

| Cell group | Levels | Cells |
|---|---|---|
| Shot scale | ECU / MS / WS | 3 |
| Lighting | low-key / high-key | 2 |
| Camera movement | static / push in / pan left / orbit | 4 |

**9 cells × 8 seeds = 72 clips**, 5s at 480P. ~$9 promo, ~$18 regular. Add a second arm at `quality` expansion for the 9 cells × 3 seeds (27 clips, ~$3.40) to test whether expansion mode changes adherence.

Eight seeds per cell distinguishes "reliable" (≥7/8) from "coin-flip" (~4/8) well enough to make a go/no-go decision. It will not give you a tight confidence interval — if a dimension lands ambiguously in the middle, extend that cell to 20 rather than extending everything.

**Measurement — and this is the part most people get wrong.**

> **Do not use a VLM to judge camera movement.** ShotBench measures the best camera-movement classifier at **51.7%**, with "over half of the evaluated models below 40% accuracy." A judge that unreliable cannot certify a generator. Use geometry instead.

| Dimension | Measure with | Why |
|---|---|---|
| **Camera movement** | Point tracking (CoTracker) → sign of net displacement of tracked points, exactly VBench-2.0's published method. Or camera-trajectory estimation (MonST3R) as CineTechBench does, if you want rotation/translation error in degrees | Objective, open-source, reproducible, and far more accurate than any VLM |
| **Shot scale** | Subject bounding-box height ÷ frame height, from any face/person detector. Set thresholds once, apply mechanically | Objective; sidesteps the VLM entirely |
| **Lighting** | Luminance histogram: mean luma, fraction of pixels below a dark threshold, contrast ratio. Low-key and high-key separate cleanly on these | Objective; ShotBench shows VLMs manage only 53.1% on lighting condition, so a histogram beats a judge |
| **Framing / angle / composition** | VLM judge acceptable here — ShotVL reaches 85.6% on framing, 68.8% on angle — but report the judge's own error rate alongside | These are the only dimensions where a VLM is trustworthy enough |

**Analysis.** Per cell, report the proportion of clips where the requested technique was produced. Then classify each dimension:

- **≥ 90%** — usable as a manipulation. Prompt for it.
- **60–90%** — usable only with per-clip verification and rejection of failures. Budget for over-generation.
- **< 60%** — not controllable by prompt. Either drop the technique from the index, or obtain it another way (explicit camera-conditioning model, i2v with a constructed first frame that already encodes the framing and lighting, or post-hoc selection from a larger pool).

**Expected outcome, stated in advance so the test can falsify it:** shot scale and lighting pass; camera movement lands in the 40–70% band with translational moves (push in) clearing static and orbit failing. If that is what you get, the honest design is to **prompt for framing and lighting, and stop treating camera movement as a controllable variable** — or move movement onto an image-to-video pipeline where the first frame fixes the geometry.

### What this buys you

Roughly $20 and an afternoon converts the weakest link in the chain from an assumption into a measured per-dimension reliability figure — which is exactly what a technique index needs to be honest about. Without it, any brain-response result is confounded by unknown adherence, and a null result is uninterpretable: you will not know whether the technique had no effect or was simply never rendered.

## Sources

**Benchmarks — generation adherence**
1. [FilmBench: A Film-Grade Benchmark for Cinematic Video Generation](https://arxiv.org/html/2607.24241v1) (arXiv 2607.24241) — the most directly relevant. 35 T2V sub-metrics under Instruction Following / Temporal Continuity / Aesthetic Quality; evaluates Hailuo 2.3 (68.94, last of nine); validated against 90 Beijing Film Academy raters, ρ = 0.95.
2. [VBench-2.0: Advancing Video Generation Benchmark Suite for Intrinsic Faithfulness](https://arxiv.org/html/2503.21755v1) (arXiv 2503.21755) — nine-movement camera-motion dimension with a published CoTracker2-based evaluation method. Kling 1.6 61.73%, HunyuanVideo 33.95%, CogVideoX-1.5 33.33%, Sora 27.16%.
3. [CineTechBench: A Benchmark for Cinematographic Technique Understanding and Generation](https://arxiv.org/html/2505.15145v1) (arXiv 2505.15145, NeurIPS 2025) — expert-annotated across seven dimensions; generation task measures camera-trajectory error. [GitHub](https://github.com/PRIS-CV/CineTechBench) · [NeurIPS poster](https://neurips.cc/virtual/2025/poster/121706)

**Benchmarks — verification instruments**
4. [ShotBench: Expert-Level Cinematic Understanding in Vision-Language Models](https://arxiv.org/html/2506.21356v2) (arXiv 2506.21356) — 3,572 QA pairs across eight dimensions. The source for per-dimension judge reliability; the reason not to use a VLM for camera movement.
5. [CameraBench — Towards Understanding Camera Motions in Any Video](https://github.com/sy77777en/CameraBench) (NeurIPS 2025 Spotlight) — fine-grained camera-motion annotation; compares SfM against VLMs.

**Architectural corroboration**
6. [CameraCtrl: Enabling Camera Control for Text-to-Video Generation](https://arxiv.org/abs/2404.02101) — explicit pose conditioning, motivated by models lacking "control of camera pose that serves as a cinematic language."

**Prompt rewriting**
7. [Prompt-A-Video: Prompt Your Video Diffusion Model via Preference-Aligned LLM](https://arxiv.org/html/2412.15156v1) (arXiv 2412.15156, ICCV 2025)
8. [The Devil is in the Prompts: Retrieval-Augmented Prompt Optimization for Text-to-Video Generation](https://arxiv.org/html/2504.11739v1) (arXiv 2504.11739)

**Vendor documentation (primary, but not evidence of performance)**
9. [MiniMax Text-to-Video API reference](https://platform.minimax.io/docs/api-reference/video-generation-t2v) — bracket commands for `MiniMax-Hailuo-2.3`, `MiniMax-Hailuo-02`, `T2V-01-Director`. No H3.
10. [MiniMax Image-to-Video API reference](https://platform.minimax.io/docs/api-reference/video-generation-i2v) — full 15-command list and syntax rules.
11. [fal — MiniMax H3 Max Text-to-Video API docs](https://fal.ai/models/minimax/h3-max/text-to-video/api) — `prompt_expansion_mode` required, `balanced` | `quality`, no off; returns `expanded_prompt`.
12. [fal — MiniMax H3 Max Image-to-Video API docs](https://fal.ai/models/minimax/h3-max/image-to-video/api)
13. [fal — MiniMax H3 Max model page](https://fal.ai/models/minimax/h3-max/text-to-video) — pricing and model description.

**Community folklore (flagged as such)**
14. [AI Video Camera Movement Prompts for MiniMax H3](https://minimaxh3.tv/blog/ai-video-camera-movement-prompts) — self-declares that no H3 tests were run and no success rate is claimed. Reliability tiering is geometric reasoning, not measurement. The most honest of the guides found; others assert bracket support on H3 without evidence.

---

## Caveats on this research

- **No published benchmark covers MiniMax H3 or fal's H3 Max.** Every generation-adherence number here is from a different model. They establish the *shape* of the problem (which dimensions are hard), not this model's performance.
- **Hailuo 2.3's FilmBench result is a prior, not a measurement of H3.** H3 is a later generation and fal's variant is explicitly post-trained "for stronger prompt adherence."
- **Cross-benchmark numbers are not comparable.** VBench-2.0's 61.73% (classification accuracy) and FilmBench's 86.5 (0–100 rating) measure different things on different scales. Compare within a benchmark, never across.
- **Recognition accuracy is not generation adherence.** ShotBench measures whether a VLM can *see* a technique. I have used it for judge reliability and as weak evidence about which dimensions are well-defined. It is not evidence that a generator produces them.
- **Some numbers were extracted from paper HTML via an automated reader** rather than read in full. The headline figures (VBench-2.0 camera motion, ShotBench per-dimension, CineTechBench rotation error, Hailuo 2.3's 68.94) should be re-checked against the source before being quoted externally.
- Web-search budget for this session was exhausted mid-research; the lighting-specific and shot-scale-specific generation-adherence searches did not run. If a dedicated lighting-controllability benchmark exists, I have not seen it — which is itself part of why Stage 1 above measures lighting directly.
