# Probe clips — provenance

The clips themselves are gitignored. This file is what makes them reproducible.

## Source

**Jungle Book (1942)**, public domain, Internet Archive.

```sh
curl -L "https://archive.org/download/JungleBook/Jungle_Book.mp4" -o junglebook.mp4
# 656 MB · 6294.7 s · 640x480 · h264 29.97 fps · aac
```

All three clips come from **one film on purpose.** Same stock, same Technicolor
grade, same era, same grain, same encode — so content is the only thing that
varies between them. Three unrelated stock clips would confound content with
everything about how each was shot and digitised, and the probe would not be
able to tell the difference.

## Cutting

```sh
python cut_segments.py junglebook.mp4 --landscape 6005 --crowd 824 --face 4364 --seconds 60
```

60 seconds rather than the 30 s floor: TRIBE was trained on 100 s windows and
degrades as you approach the floor, so more context is strictly better and costs
nothing here. Segments are re-encoded rather than stream-copied, because a
stream copy starts on the nearest keyframe and would silently give a clip that
begins late or runs short — and a short clip is precisely the failure that
returns confident noise.

Audio is preserved. TRIBE has an audio branch and discarding it would waste a
modality for no reason.

## How the timestamps were chosen

Not by eye. An initial visual pass picked badly — the first face candidate
(1215 s) turned out to contain **fewer faces than the crowd clip**, which would
have made the test meaningless. So the film was scanned with YuNet at 4-second
intervals (1,574 samples) and windows ranked objectively.

Measured over each chosen 60 s window:

| Clip | start | mean faces | max faces | mean largest-face area | frames with a big face |
|---|---|---|---|---|---|
| `face.mp4` | 4364 s | 1.8 | 2 | **24.1%** | **100%** |
| `crowd.mp4` | 824 s | **3.3** | 9 | 1.5% | 40% |
| `landscape.mp4` | 6005 s | 0.3 | 2 | 0.6% | 13% |

That is the contrast the probe needs: a clean gradient on face area
(24.1% → 1.5% → 0.6%) with face *count* inverted between the face and crowd
clips (1.8 vs 3.3). A single dominant face, many small faces, and near-empty.

Rejected: `crowd @600 s` (visually denser throngs, but mean largest-face area
2.7% — a weaker contrast against the face clip) and `face @1215 s` (0.4 mean
faces; broken).

## Known limitations — state these in RESULT.md

- **The landscape clip is not people-free.** Roughly two frames in eight contain
  figures. This film is people-dense throughout and a clean 60 s empty landscape
  does not exist in it. It is environment-*dominant*, not environment-only.
- **The crowd clip drifts.** Its first half is a clear gathering; the second half
  moves to a child and then a panther. Sustained 60 s crowd scenes are rare in a
  1942 adventure feature.
- **640×480, and dark.** A 1942 Technicolor transfer with a dim grade. TRIBE's
  visual backbone downscales anyway, but low luminance may compress the range the
  low-level visual regions respond over.
- **YuNet's detection floor is a ~30–40 px face box**, so distant crowd faces go
  uncounted. The crowd clip's true head count is higher than the table suggests.

None of these invalidate the probe — it asks whether TRIBE separates these three
at all, and the contrast is wide. They do mean a *negative* result would need
re-testing on cleaner material before concluding the sensor does not work.
