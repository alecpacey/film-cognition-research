# Annotated cinematography datasets

_Researched 2026-09-01. Every Hugging Face id below was verified against `https://huggingface.co/api/datasets/<id>` and, where noted, by downloading the actual annotation file. Anything I could not confirm is marked **unverified**._

## Summary table

| Dataset | Size (clips/shots) | Technique labels present | Licence | Access (HF id / URL) | Usable for this project? |
|---|---|---|---|---|---|
| **ShotBench** (test set) | 3,572 QA pairs = 3,049 images + 464 video clips, from 200+ Oscar-cinematography-nominated films | shot size, shot framing, camera angle, **lens size (focal length)**, **lighting type**, **lighting condition**, **composition**, camera movement — 8 dimensions | **Apache-2.0** (verified in repo card) | `Vchitect/ShotBench` — https://huggingface.co/datasets/Vchitect/ShotBench | **Yes — best single source of a technique taxonomy.** Small, but the only public set that covers lighting, lens and composition together. Permissive. |
| **ShotQA** (train set for the same taxonomy) | ~70k QA pairs (images + video) | same 8 dimensions as ShotBench | **CC BY-NC-ND 4.0** + **gated** (access request form, "non-commercial research only") | `Vchitect/ShotQA` — https://huggingface.co/datasets/Vchitect/ShotQA | Yes for a non-commercial project, but ND blocks redistributing a derived/remixed label set, and it is gated. Use for reading the vocabulary, be careful about shipping derivatives. |
| **CameraBench** (test split) | 1,071 clips (verified by downloading `test.jsonl`); ~3,000 videos in the full collection | camera motion only, but by far the deepest motion taxonomy: 34 primitives incl. tracking modes, steadiness, speed | **CC BY 4.0** (LICENSE file in repo is the full CC BY 4.0 text) | `syCen/CameraBench` — https://huggingface.co/datasets/syCen/CameraBench | **Yes.** The right vocabulary for the camera-movement dial. Train split is gated behind a request form. |
| **AVE (Anatomy of Video Editing)** | 196,176 shots from 5,591 movie scenes; >1.5M labels | shot size, shot angle, shot type/framing, shot motion, shot location, shot subject, number of people, sound source — plus shot boundaries, camera-setup grouping and **editing/transition structure** | **No licence stated** anywhere (GitHub repo has no LICENSE; paper states none) — annotations via a Google Drive link, video via MovieClips YouTube | https://github.com/dawitmureja/AVE | Partly. Biggest human-annotated set by an order of magnitude and the only one giving editing structure, but the licence gap and yt-dlp scraping of MovieClips make it awkward. |
| **MovieShots** (the MovieNet ECCV'20 shot-type set) | 46,857 shots from 7,858 movie trailers | shot scale (5), shot movement (4) | Not stated on the project page; MovieNet as a whole is under a "User Service Agreement", not an open licence | https://movienet.github.io/projects/eccv20shot.html (Google Drive) | Weak. Coarse taxonomy (4 movement classes), unclear licence. Useful only as extra volume for scale/movement. |
| **MovieNet** (parent) | 1,100 movies; 46K shots with scale+movement; 42K scenes; 1.1M character instances; 80 action / 90 place classes | shot scale, shot movement, plus non-cinematography annotations | User Service Agreement, registration via OpenDataLab; **not a permissive licence** | https://movienet.github.io/ | No for label vocabulary; yes as background. |
| **CineScale** | 792,000+ frames (1 fps) from 124 complete films by 6 directors | shot scale only — but a **9-class** scale, the finest public one | **CC BY 4.0** (Mendeley Data) | https://data.mendeley.com/datasets/th46h4vdwd/1 · https://cinescale.github.io/ | Yes for shot scale specifically. Frames themselves must be requested from the authors; the CSV of labels is the open part. |
| **types-of-film-shots** | 54,312 frames (53,400 train / 863 test) | shot scale, 8 classes | **CC BY 4.0** | `szymonrucinski/types-of-film-shots` — https://huggingface.co/datasets/szymonrucinski/types-of-film-shots | Yes, as a cheap ready-to-load shot-scale classifier training set. But mostly **machine-labelled** (see caveats). |
| **storyboard-shot-types-reference** | <1k rows; 4 JSON files (shot_types, camera_movements, aspect_ratios, transitions) | shot type, camera movement, aspect ratio, transition — a *reference vocabulary*, not annotated footage | **CC0-1.0** | `Rattata/storyboard-shot-types-reference` — https://huggingface.co/datasets/Rattata/storyboard-shot-types-reference | Yes as a public-domain controlled vocabulary you can copy wholesale with zero licence risk. No images. |
| **SpatialVID** | 1M+ clips | camera trajectory + discrete motion instructions (Dolly In/Out, Truck L/R, Pedestal U/D, Tilt U/D, Pan L/R, Roll CW/CCW, Stay) | **CC BY-NC-SA 4.0** | `SpatialVID/SpatialVID` | Maybe. Web video, not film; motion labels are geometry-derived, not cinematographic intent. |
| **MultiCamVideo-Dataset** (Kling) | synthetic multi-camera renders | camera trajectory parameters | **Apache-2.0** | `KlingTeam/MultiCamVideo-Dataset` | No — synthetic, geometry only, no technique labels. |
| **Cinemetrics** | thousands of user-submitted films | **editing rate / average shot length** per film — the canonical source | Terms of use page; not an open licence (**unverified** — could not read the ToU page) | https://cinemetrics.uchicago.edu/ | Only source for the editing-rate dial. Treat licence as unresolved. |
| **cinematic-mood-palette** | ~80 mappings | affect (VAD + complexity + coherence) → colour/light parameters. Not film annotation; a hand-authored mapping | **CC BY 4.0** | `danielritchie/cinematic-mood-palette` | Curiosity only. Not a film dataset. |

Explicitly checked and **rejected**: `Alexislhb/shotdeck` (a raw ShotDeck scrape, no README, no licence — do not use), `Codec96/cinematic-video-250h-sample` (commercial, $200/hr licence, no technique labels), `gchen019/CineScale_Training` (unrelated to the real CineScale — it is a folder of scraped 4K trailers, no labels, no licence), `pandaphd/camera_settings` / GenPhoto (synthetic camera-parameter text-to-image, CC BY-NC-ND, no film annotation). The HF ids matching "AVE_Dataset" (`Helios1208/AVE_Dataset` etc.) are the **Audio-Visual Event** dataset — a different AVE, not Anatomy of Video Editing.

Searched and **not found**: there is no HF dataset called "Full Cinematic Shot", no HF mirror of MovieShots, MovieNet's shot annotations, CineScale, or AVE, and no HF dataset carrying `shot-type` / `shot-scale` / `camera-movement` as hub tags beyond `szymonrucinski/types-of-film-shots` (tags: `film`, `cinematography`, `shot-scale`, `active-learning`). Condensed Movies / CMD and LSMDC carry **no** cinematography-technique annotations at all — CMD gives scene-level text descriptions, face tracks and metadata; papers that need shot type on CMD run a classifier over it.

---

## Per-dataset detail

### ShotBench — `Vchitect/ShotBench`

**What is labelled.** Eight dimensions, one per question. I downloaded `test.tsv` and counted the actual distribution:

| Dimension | Questions | Modality |
|---|---|---|
| lens size | 489 | image |
| shot size | 485 | image |
| composition | 479 | image |
| camera movement | 464 | **video** |
| camera angle | 455 | image |
| shot framing | 445 | image |
| lighting type | 405 | image |
| lighting (condition) | 350 | image |
| **total** | **3,572** | |

**Vocabulary, verbatim from the answer keys** (these are the atomic labels; I stripped the multi-label compounds, see caveats):

- **shot size** — `Extreme Close Up`, `Close Up`, `Medium Close Up`, `Medium`, `Medium Wide`, `Wide`, `Extreme Wide`
- **shot framing** — `Single`, `2 shot`, `3 shot`, `Group shot`, `Over the shoulder`, `Insert`, `Establishing shot`
- **camera angle** — `Aerial`, `Overhead`, `High angle`, `Low angle`, `Dutch angle` _(note: no "eye level" — see Gaps)_
- **lens size** — `Ultra Wide / Fisheye`, `Wide`, `Medium`, `Long Lens`
- **lighting type** — `Daylight`, `Sunny`, `Overcast`, `Moonlight`, `Firelight`, `Artificial light`, `Practical light`, `Mixed light`, `Fluorescent`, `Tungsten`, `LED`, `HMI`
- **lighting condition** — `Soft light`, `Hard light`, `High contrast`, `Low contrast`, `Side light`, `Backlight`, `Top light`, `Underlight`, `Edge light`, `Silhouette`
- **composition** — `Center`, `Balanced`, `Symmetrical`, `Left heavy`, `Right heavy`, `Short side`
- **camera movement** — `Static shot`, `Push in`, `Pull out`, `Zoom in`, `Zoom out`, `Pan left`, `Pan right`, `Tilt up`, `Tilt down`, `Boom up`, `Boom down`, `Move to the left`, `Move to the right`, `Trucking left`, `Trucking right`, `Arc`, `Camera roll`, `Dolly zoom`, `Tracking`, `Rack focus`

**Annotation method.** Human. Trained annotators with expert audit; multi-round pilot annotation with daily adjudication. For ShotQA, candidate labels were **pulled from ShotDeck** (the professional cinematography reference library) and then verified/corrected by annotators against the ShotBench guidelines — so the taxonomy is effectively ShotDeck's working vocabulary, cleaned up.

**Quality caveats — these matter.**
1. A follow-up paper, **RefineShot** (arXiv 2510.02423), found ShotBench's multiple-choice options are **not mutually exclusive**: options within one question are drawn from heterogeneous descriptive dimensions. It rewrote **961 of the ~3,500 questions**. The worst offender is lighting condition, where directional terms (`side light`, `backlight`), quality terms (`hard`/`soft`) and contrast terms (`high`/`low contrast`) are all offered as alternatives to each other, so several answers are defensible. It also reports a **16.7% confusion rate between `Artificial light` and `Practical light`** — a practical light *is* an artificial light, so the two are not disjoint.
2. Confirming that from the data myself: some correct answers are **compound strings** (multi-label collapsed into one option). Share of compound answers by dimension: lighting condition **31%**, lighting type **19%**, camera movement **15%**, shot framing **12%**, camera angle **9%**, composition 4%, shot size 3%, lens size 2%. So the higher-level dimensions are genuinely multi-label, not single-choice.
3. Camera-movement strings are **dirty**: `Static`, `Static shot`, `Static shot.` all appear as separate strings, along with typos in the distractors (`Fisrtly`, `Fristly`). Normalise before use.
4. The camera-movement tail is thin — `Rack focus` n=2, `Tracking` n=3, `Arc` n=4, `Zoom in` n=5.

**Load snippet.**
```python
from datasets import load_dataset
ds = load_dataset("Vchitect/ShotBench", split="train")  # single CSV split; test.tsv
# images.tar and videos.tar must be pulled separately:
from huggingface_hub import hf_hub_download
hf_hub_download("Vchitect/ShotBench", "images.tar", repo_type="dataset")
hf_hub_download("Vchitect/ShotBench", "videos.tar", repo_type="dataset")
```
Or just take the labels directly, which is what I did:
```bash
curl -sL https://huggingface.co/datasets/Vchitect/ShotBench/resolve/main/test.tsv -o shotbench.tsv
```

**Related, verified ids:** `Vchitect/ShotQA` (train, CC BY-NC-ND 4.0, gated), `Vchitect/ShotVL-3B`, `Vchitect/ShotVL-7B` (models — useful if you want to *auto-label* your own footage with this taxonomy). `marvex/ShotBench` and `Baggio1012/shotbench-organized` are third-party re-uploads of the same test set.

---

### CameraBench — `syCen/CameraBench`

**What is labelled.** Camera motion only, per clip, as a **multi-label set** plus a natural-language caption. Taxonomy was designed with professional cinematographers and separates three reference frames (object-centric, ground-centric, camera-centric).

**Full vocabulary, extracted from the 1,071-row `test.jsonl` (34 labels, with counts):**

| Group | Labels (count) |
|---|---|
| Steadiness | `no-shaking` (422), `minimal-shaking` (299), `unsteady` (197), `very-unsteady` (56) |
| Motion presence | `complex-motion` (852), `no-motion` (187), `static` (97), `minor-motion` (32) |
| Speed | `regular-speed` (940), `slow-speed` (79), `fast-speed` (52) |
| Translation | `dolly-in` (205), `dolly-out` (71), `truck-left` (67), `truck-right` (96), `pedestal-up` (63), `pedestal-down` (77) |
| Rotation | `pan-left` (105), `pan-right` (93), `tilt-up` (69), `tilt-down` (52), `roll-CW` (42), `roll-CCW` (51) |
| Intrinsics | `zoom-in` (54), `zoom-out` (49) |
| Circular | `arc-CW` (60), `arc-CCW` (62) |
| Tracking | `side-tracking` (68), `pan-tracking` (44), `aerial-tracking` (37), `tail-tracking` (36), `lead-tracking` (26), `arc-tracking` (12), `tilt-tracking` (14) |

Note the clean separation CameraBench gets right and ShotBench does not: **dolly-in is a distinct label from zoom-in**, and **tracking is a separate axis from the translation that implements it** (a clip can be `truck-left` + `side-tracking`).

**Annotation method.** Human experts, "label-then-caption": annotators first decide whether motion is clear and consistent, classify each primitive, and mark anything ambiguous as "I am not sure" rather than guessing; then write a free-text caption. Multi-stage training programme, 100+ participant human study, cinematographer collaboration. NeurIPS 2025 Spotlight.

**Caveats.** Source video is **internet video, not film** — nature, games, GoPro, drone, 2D/3D, real and synthetic. So the motion vocabulary transfers to film but the visual distribution does not. Test split is open; the **training split requires filling in a request form**. The GitHub repo's licence is `NOASSERTION`, but the HF dataset ships an actual CC BY 4.0 LICENSE file, so the annotations are CC BY 4.0.

**Load snippet.**
```python
from datasets import load_dataset
ds = load_dataset("syCen/CameraBench", data_files="test.jsonl", split="train")
# each row: {"Video": <gif url>, "labels": [...], "caption": "...", "path": "videos/....mp4"}
```

---

### AVE — Anatomy of Video Editing (ECCV 2022)

**What is labelled.** 196,176 shots from 5,591 movie scenes, eight attributes, >1.5M labels. Also shot boundaries and camera-setup grouping within a scene, which is what makes it the only public source of **editing structure** (which shots belong to the same setup, how a scene is cut together).

**Full vocabulary, verbatim from the paper:**

- **Shot size (5)** — `Extreme wide (EW)`, `Wide (W)`, `Medium (M)`, `Close-up (CU)`, `Extreme close-up (ECU)`
- **Shot angle (5)** — `Aerial (A)`, `Overhead (O)`, `Eye level (EL)`, `High angle (HA)`, `Low angle (LA)`
- **Shot type (6)** — `Over-the-shoulder (OTS)`, `Single (S)`, `Two (2)`, `Three (3)`, `Insert (I)`, `Group (G)`
- **Shot motion (5)** — `Pan/Truck (P/T)`, `Tilt/Pedestal (T/P)`, `Locked (L)`, `Zoom/Dolly (Z/D)`, `Handheld (H)`
- **Shot location (2)** — `Exterior (Ext)`, `Interior (Int)`
- **Shot subject (7)** — `Animal`, `Location`, `Object`, `Human`, `Limb`, `Face`, `Text`
- **Number of people (6)** — `0`, `1`, `2`, `3`, `4`, `5` (5 = five or more)
- **Sound source (4)** — `On screen (OnS)`, `Off screen (OfS)`, `External narration (EN)`, `External music (EM)`

**Annotation method.** Human — a task force of **15 professional video editors**. Shot boundaries pre-computed by a shot-boundary detector and then verified by the annotators.

**Caveats.**
- **No licence.** The GitHub repo has no LICENSE file and the GitHub API reports `license: None`; the paper states none. The annotations are distributed via a personal Google Drive link. For a non-commercial project this is a grey area, not a permission.
- Video is **not distributed** — you download the MovieClips YouTube channel with `yt-dlp` and cut shots with FFmpeg from the provided start/end times. Region-locked clips will fail. Link rot will make this less reproducible over time.
- `Pan/Truck` and `Tilt/Pedestal` **conflate rotation with translation**, and `Zoom/Dolly` conflates an optical change with a physical one. As controllable dials these three are too coarse — CameraBench separates exactly these.
- Handheld is a motion class here, whereas CameraBench treats steadiness as an orthogonal axis. AVE's version means you cannot say "handheld pan".

**Access.** https://github.com/dawitmureja/AVE — `download.sh`, `scenes_to_shots.py`, and annotations at the Drive link in the README.

---

### CineScale

**What is labelled.** Shot scale only, at 1 fps, over 792,000+ frames from 124 complete films — the entire filmographies of Scorsese, Godard, Béla Tarr, Fellini, Antonioni and Bergman.

**Vocabulary (9 classes), verbatim:** `Extreme Close Up (ECU)`, `Close Up (CU)`, `Medium Close Up (MCU)`, `Medium Shot (MS)`, `Medium Long Shot (MLS)`, `Long Shot (LS)`, `Extreme Long Shot (ELS)`, `Foreground Shot (FS)`, `Insert Shots (IS)`.

`Foreground Shot` and `Insert Shots` are the interesting additions — no other set has them as scale classes.

**Annotation method.** Human. Two independent coders annotated every frame; a third adjudicated disagreements. This is the most rigorously coded shot-scale set in existence.

**Caveats.** Six auteur directors, mostly mid-20th-century European and American art cinema — a strongly non-representative visual distribution. Frame-level at 1 fps, not shot-level, so consecutive rows are highly correlated. The **image frames are not in the CC BY 4.0 release**; you get the labels and must request frames from the authors or go via cinescale.github.io.

**Licence.** CC BY 4.0 (Mendeley Data). Data article: https://www.sciencedirect.com/science/article/pii/S2352340921002869

---

### types-of-film-shots — `szymonrucinski/types-of-film-shots`

**Vocabulary (8 classes), verbatim:** `ambiguous`, `closeUp`, `detail`, `extremeLongShot`, `fullShot`, `longShot`, `mediumCloseUp`, `mediumShot`.

54,312 frames (53,400 train / 863 test), 143 MB, from film-grab.com. **CC BY 4.0.** Hub tags include `shot-scale`.

**Annotation method — read this before trusting it.** Mostly automatic. Only **863 frames were hand-labelled by humans**; ~2,056 were classified by a DINOv2 model, and frames scoring below 0.8 confidence were re-labelled by **Claude Opus** in an active-learning loop. The remaining ~51k train rows are model output. Treat the test split as ground truth and the train split as pseudo-labels.

Also note `ambiguous` is a class, which is honest but means ~1/8 of the vocabulary carries no cinematographic meaning.

```python
from datasets import load_dataset
ds = load_dataset("szymonrucinski/types-of-film-shots")
```

---

### storyboard-shot-types-reference — `Rattata/storyboard-shot-types-reference`

Not annotated footage — four JSON files of **vocabulary**, under **CC0-1.0** (public domain), which makes it the only thing here you can copy into your own schema with zero attribution obligation.

`shot_types.json` entries carry `abbreviation`, `name`, `alt`, `framing`, `uses`, `notes` — e.g.
```json
{"abbreviation":"OTS","name":"Over the Shoulder","alt":["ROTS"],
 "framing":"One character past the shoulder of another",
 "uses":["dialogue scenes","interrogation framing","confrontation"],
 "notes":"Pairs with reverse OTS to cut a conversation."}
```
`camera_movements.json` (8 entries): `PUSH` Push In, `PULL` Pull Out, `PAN`, `TILT`, `DOLLY`, `CRANE`, `HANDHELD`, `STATIC`. Also `aspect_ratios.json` and `transitions.json`.

The `uses` field is the useful bit — it is the only public artefact that maps a technique to *narrative intent*, which is exactly what a "dial" needs a description for.

---

### MovieShots / MovieNet

**MovieShots vocabulary, verbatim:** scale = `Long shot (LS)`, `Full shot (FS)`, `Medium shot (MS)`, `Close-up shot (CS)`, `Extreme close-up shot (ECS)`; movement = `Static shot`, `Motion shot`, `Push shot`, `Pull shot`. 46,857 shots from 7,858 trailers.

MovieNet itself describes its scale slightly differently (extreme close-up, close-up, medium, full, long) and its movement as static / pans-and-tilts / zoom-in / zoom-out, over 46K shots.

**Why I would not build on this.** Four movement classes that collapse all lateral and vertical camera motion into one bucket called "motion" is unusable as a set of dials. And MovieNet is not open-licensed — it is distributed under a User Service Agreement via OpenDataLab registration, with the actual movie files behind an agreement the project page says was still pending university legal approval.

---

## The best taxonomy to adopt

**Adopt ShotBench's eight-dimension schema as the spine, and swap its camera-movement dimension for CameraBench's.**

Why ShotBench:
- It is the **only public schema covering lighting, lens/focal length and composition** alongside scale, angle and framing. AVE, CineScale, MovieShots and MovieNet all stop at scale + angle + framing + coarse motion. If you want lighting key or focal length as dials, ShotBench is the only game in town.
- Its vocabulary is derived from **ShotDeck**, a working professional reference library, so the words are the words cinematographers and DPs actually use — which matters if the labels will ever be surfaced to a person or fed to a text-conditioned generator.
- **Apache-2.0** on the benchmark. The most permissive licence of anything with real coverage.
- There is a trained model (`Vchitect/ShotVL-7B`) that emits this exact vocabulary, so you can auto-label your own footage into the schema rather than hand-annotating.

Why swap camera movement: ShotBench's movement labels conflate optical and physical moves (`Zoom in` vs `Push in` are both present but the taxonomy has no principle separating them), have no steadiness axis, no speed axis, no tracking axis, and the raw strings are dirty. CameraBench's 34 primitives are orthogonal by construction, CC BY 4.0, and cinematographer-designed.

Apply RefineShot's fix as you adopt it: **each dimension must be internally mutually exclusive**, and dimensions that are genuinely multi-label (lighting condition, lighting type, framing) should be modelled as multi-select, not single-choice. Explicitly split `Artificial light` (source is not natural) from `Practical light` (source is visible in frame) rather than offering them as alternatives — they are different questions.

### The full vocabulary to adopt

**1. Shot size** (single-select, 7) — `Extreme Close Up` · `Close Up` · `Medium Close Up` · `Medium` · `Medium Wide` · `Wide` · `Extreme Wide`
_Optional extras from CineScale if you need them: `Foreground Shot`, `Insert`._

**2. Shot framing** (multi-select, 7) — `Single` · `2 shot` · `3 shot` · `Group shot` · `Over the shoulder` · `Insert` · `Establishing shot`
_Add `POV` from the CC0 storyboard reference — no annotated dataset has it and it is a real, common framing._

**3. Camera angle** (single-select, 6) — `Eye level` · `Low angle` · `High angle` · `Overhead` · `Aerial` · `Dutch angle`
_`Eye level` is taken from AVE; ShotBench omits it, which means "no special angle" has no label in ShotBench. Add it. Dutch is arguably orthogonal to the vertical axis — consider making it a separate boolean._

**4. Lens size / focal length** (single-select, 4) — `Ultra Wide / Fisheye` · `Wide` · `Medium` · `Long Lens`

**5. Lighting type / source** (multi-select, 12) — `Daylight` · `Sunny` · `Overcast` · `Moonlight` · `Firelight` · `Artificial light` · `Practical light` · `Mixed light` · `Fluorescent` · `Tungsten` · `LED` · `HMI`
_Three sub-axes hide in here: natural-vs-artificial, weather/time-of-day, and fixture technology. Split them if you want clean dials._

**6. Lighting condition / quality** (multi-select, 10) — `Soft light` · `Hard light` · `High contrast` · `Low contrast` · `Side light` · `Backlight` · `Top light` · `Underlight` · `Edge light` · `Silhouette`
_This is the dimension RefineShot found most broken. Restructure as three orthogonal dials: **quality** {soft, hard}, **contrast/key** {low contrast, high contrast}, **direction** {front, side, back, top, under} — with `Silhouette` and `Edge light` as derived states of extreme backlight._

**7. Composition** (single-select, 6) — `Center` · `Balanced` · `Symmetrical` · `Left heavy` · `Right heavy` · `Short side`

**8. Camera movement** — use CameraBench, as five orthogonal axes:
- **translation** (multi) — `dolly-in` · `dolly-out` · `truck-left` · `truck-right` · `pedestal-up` · `pedestal-down`
- **rotation** (multi) — `pan-left` · `pan-right` · `tilt-up` · `tilt-down` · `roll-CW` · `roll-CCW`
- **intrinsics** (multi) — `zoom-in` · `zoom-out`
- **circular** (multi) — `arc-CW` · `arc-CCW`
- **tracking** (multi) — `side-tracking` · `pan-tracking` · `tail-tracking` · `lead-tracking` · `aerial-tracking` · `arc-tracking` · `tilt-tracking`
- **steadiness** (single) — `no-shaking` · `minimal-shaking` · `unsteady` · `very-unsteady`
- **speed** (single) — `slow-speed` · `regular-speed` · `fast-speed`
- **presence** (single) — `static` · `no-motion` · `minor-motion` · `complex-motion`
_Add `Dolly zoom` and `Rack focus` from ShotBench as named compound moves — CameraBench has neither._

Licence position if you adopt this: the ShotBench half is Apache-2.0 and the CameraBench half is CC BY 4.0, so a combined schema is redistributable with attribution. Avoid deriving the schema from **ShotQA** (CC BY-NC-ND) — ND is the problem, not NC.

---

## Gaps

Dimensions the brief asked about that **no public dataset covers well**:

- **Depth of field / focus.** Nothing labels shallow-vs-deep focus. ShotBench has `Rack focus` as a camera-movement label with **n=2 examples**, and a handful of free-text answers describing focus pulls; that is the entire public coverage. Lens size is a proxy at best. This is the single biggest gap.
- **Colour palette / grade.** No public dataset annotates film colour treatment. There is academic work on movie barcodes and colour-scheme extraction, and the **VIAN** annotation system for film-colour digital humanities, but no released label set. `danielritchie/cinematic-mood-palette` (CC BY 4.0, ~80 rows) is a hand-authored affect→colour mapping, not annotation of real films. A recent benchmark, **LumiGrade**, targets automated grading from log footage — **unverified**, I could not confirm a public release.
- **Editing rate / average shot length.** Only Cinemetrics holds this at scale, and its licence is unresolved. AVE gives shot boundaries within 5,591 scenes, so you could **compute** ASL per scene yourself from AVE — that is probably the cleanest route, licence issues aside.
- **Aspect ratio.** Only in the CC0 storyboard reference as a vocabulary; no dataset labels it.
- **Colour temperature / white balance.** Implied by ShotBench's lighting-type fixture classes (Tungsten, HMI, Fluorescent, LED) but never labelled directly.
- **Eye-level / neutral angle.** Present in AVE, absent from ShotBench — so the "no special angle" case has no ShotBench label. Worth noting because it is the *most common* angle in real footage, meaning ShotBench's angle dimension is implicitly a "notable angle" detector, not an angle classifier.
- **Film stock / grain / format** (35mm, 16mm, digital, anamorphic). Nothing.
- **Transitions.** Only the CC0 storyboard reference lists them as vocabulary; AVE annotates shot *boundaries* but the transition type is not a labelled class in what I could verify.
- **Volume at film quality.** ShotBench is 3,572 items — tiny. ShotQA (70k) is the only large set on this taxonomy and it is gated + NC-ND. The only large open sets (AVE at 196k, CineScale at 792k frames) each cover a narrow slice and carry licence problems.

---

## Sources

1. https://huggingface.co/datasets/Vchitect/ShotBench — ShotBench test set, Apache-2.0 (verified via HF API and by downloading `test.tsv`)
2. https://huggingface.co/datasets/Vchitect/ShotQA — ShotQA training set, CC BY-NC-ND 4.0, gated (verified via HF API + README)
3. https://arxiv.org/abs/2506.21356 · https://arxiv.org/html/2506.21356v1 — ShotBench paper; Table 8 carries the label options
4. https://github.com/Vchitect/ShotBench — code; names the eight dimensions and the HF/model ids
5. https://vchitect.github.io/ShotBench-project/ — project page
6. https://arxiv.org/html/2510.02423v1 — RefineShot: the critique of ShotBench's option design (961 questions rewritten)
7. https://huggingface.co/datasets/syCen/CameraBench — CameraBench, CC BY 4.0 (verified via HF API + LICENSE file + `test.jsonl`)
8. https://github.com/sy77777en/CameraBench — CameraBench code, NeurIPS 2025 Spotlight
9. https://linzhiqiu.github.io/papers/camerabench/ — CameraBench project page and taxonomy description
10. https://arxiv.org/abs/2504.15376 — "Towards Understanding Camera Motions in Any Video"
11. https://github.com/dawitmureja/AVE — AVE code and download instructions (no LICENSE file)
12. https://ar5iv.labs.arxiv.org/html/2207.09812 — AVE paper, full class definitions
13. https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136680195.pdf — AVE, ECCV 2022 official PDF
14. https://data.mendeley.com/datasets/th46h4vdwd/1 — CineScale on Mendeley Data, CC BY 4.0
15. https://www.sciencedirect.com/science/article/pii/S2352340921002869 — CineScale data article
16. https://cinescale.github.io/ — CineScale project page
17. https://huggingface.co/datasets/szymonrucinski/types-of-film-shots — CC BY 4.0, 8-class shot scale
18. https://huggingface.co/datasets/Rattata/storyboard-shot-types-reference — CC0-1.0 vocabulary files
19. https://movienet.github.io/projects/eccv20shot.html — MovieShots dataset page
20. https://movienet.github.io/ — MovieNet, access terms
21. https://arxiv.org/pdf/2007.10937 — MovieNet paper
22. https://arxiv.org/pdf/2008.03548 — SGNet, "A Unified Framework for Shot Type Classification Based on Subject Centric Lens" (the MovieShots paper)
23. https://huggingface.co/datasets/SpatialVID/SpatialVID — CC BY-NC-SA 4.0, motion instructions
24. https://openaccess.thecvf.com/content/ACCV2020/papers/Bain_Condensed_Movies_Story_Based_Retrieval_with_Contextual_Embeddings_ACCV_2020_paper.pdf — Condensed Movies (no technique annotations)
25. https://cinemetrics.uchicago.edu/ — Cinemetrics, average shot length database
26. https://www.digitalhumanities.org/dhq/vol/14/4/000500/000500.html — VIAN and film-colour analysis methods
27. https://huggingface.co/datasets/danielritchie/cinematic-mood-palette — CC BY 4.0 affect→colour mapping
