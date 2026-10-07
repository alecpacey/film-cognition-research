#!/usr/bin/env python3
"""
EXPLORATORY (7 Oct 2026; consolidation 3a, review F5). Content descriptors per segment, computed
from video and audio only -- this script never reads parcel data. Plan fixed in
content_descriptors.md (commit 55a8515) before anything here ran.

    .venv-content/bin/python content_descriptors.py validate <B_dir> <C_dir>   -> content_validation.json
    .venv-content/bin/python content_descriptors.py av                         -> content_av.jsonl
    .venv-content/bin/python content_descriptors.py words                      -> content_words.jsonl

validate: CLIP distance across 03b joins -- REF (stage 03 S-, scene change) must exceed B and C
          (same scene) at every level, or sem_change_per_min is reported as failed.
av:       speech_prop (Silero VAD bundled with faster-whisper), CLIP ViT-B/32 frames at 0.5 Hz
          (segment mean embedding, sem_dispersion), and CLIP distance across every cut already in
          scene_switches_corpus.jsonl, 12 frames either side (sem_change_per_min).
words:    Whisper small int8 word count (secondary).
Resumable: segments already in the output file are skipped.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

H = Path(__file__).parent
SEG = H / "segments"
FPS, OFFSET, SAMPLE_EVERY_S = 24.0, 12, 2.0
VAD = dict(threshold=0.5, min_silence_duration_ms=500, speech_pad_ms=100)
_clip = None


def clip_model():
    global _clip
    if _clip is None:
        from fastembed import ImageEmbedding
        _clip = ImageEmbedding("Qdrant/clip-ViT-B-32-vision")
    return _clip


def probe_frames(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                        "stream=nb_read_frames,width,height", "-of", "json", str(path)], capture_output=True, check=True)
    s = json.loads(r.stdout)["streams"][0]
    return int(s["nb_read_frames"]), int(s["width"]), int(s["height"])


def frames_at(path, idx, n_frames, w, h):
    """Decode exactly the frames with these indices, in index order. Returns {index: PIL image}."""
    want = sorted({int(min(max(i, 0), n_frames - 1)) for i in idx})
    W = 320; H2 = int(round(h * W / w / 2) * 2)
    expr = "+".join(f"eq(n\\,{i})" for i in want)
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"select='{expr}',scale={W}:{H2}",
                        "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
    arr = np.frombuffer(r.stdout, np.uint8)
    got = arr.size // (W * H2 * 3)
    if got != len(want):
        raise RuntimeError(f"{path.name}: asked for {len(want)} frames, decoded {got}")
    arr = arr.reshape(got, H2, W, 3)
    return {i: Image.fromarray(a) for i, a in zip(want, arr)}


def embed(images):
    E = np.array(list(clip_model().embed(images, batch_size=32)), dtype=np.float64)
    return E / np.linalg.norm(E, axis=1, keepdims=True)


def join_distances(path, cut_frames):
    n, w, h = probe_frames(path)
    pairs = [(max(c - OFFSET, 0), min(c + OFFSET, n - 1)) for c in cut_frames]
    imgs = frames_at(path, [i for p in pairs for i in p], n, w, h)
    keys = sorted(imgs); E = dict(zip(keys, embed([imgs[k] for k in keys])))
    return [float(1 - E[a] @ E[b]) for a, b in pairs], n


def validate(bdir, cdir):
    ladders = {"REF": H.parent / "03-isolation" / "clips" / "Sminus", "B": Path(bdir), "C": Path(cdir)}
    out = {}
    for lad, d in ladders.items():
        for k in (1, 3, 7, 15, 31):
            p = d / f"cut{k:02d}.mp4"; n, _, _ = probe_frames(p)
            joins = np.arange(1, k + 1) * ((n / FPS) / (k + 1))            # as measure_joins.py
            dist, _ = join_distances(p, [int(round(t * FPS)) for t in joins])
            out[f"{lad}_cut{k:02d}"] = {"n_joins": k, "clip_dist_mean": float(np.mean(dist)), "clip_dist_min": float(np.min(dist)),
                                       "clip_dist_max": float(np.max(dist))}
            print(f"{lad:3} cut{k:02d}  CLIP distance across joins  mean {np.mean(dist):.3f}  [{np.min(dist):.3f}, {np.max(dist):.3f}]", flush=True)
    passes = {k: out[f"REF_cut{k:02d}"]["clip_dist_min"] > max(out[f"B_cut{k:02d}"]["clip_dist_max"], out[f"C_cut{k:02d}"]["clip_dist_max"])
              for k in (1, 3, 7, 15, 31)}
    mean_pass = {k: out[f"REF_cut{k:02d}"]["clip_dist_mean"] > max(out[f"B_cut{k:02d}"]["clip_dist_mean"], out[f"C_cut{k:02d}"]["clip_dist_mean"])
                 for k in (1, 3, 7, 15, 31)}
    out["criterion"] = "REF mean CLIP distance across joins > B and C means, at every level (content_descriptors.md)"
    out["pass_by_level_means"] = mean_pass; out["PASS"] = all(mean_pass.values())
    out["stricter_separation_REF_min_gt_BC_max"] = passes
    (H / "content_validation.json").write_text(json.dumps(out, indent=1))
    print("PASS" if out["PASS"] else "FAIL", "| stricter (every REF join > every B/C join):", passes)


def done(path):
    return {json.loads(l)["clip"] for l in open(path)} if path.exists() else set()


def audio16k(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).copy()


def av():
    from faster_whisper.vad import VadOptions, get_speech_timestamps
    rows = {json.loads(l)["clip"]: json.loads(l) for l in open(H / "scene_switches_corpus.jsonl")}
    out = H / "content_av.jsonl"; skip = done(out); clips = sorted(rows)
    print(f"{len(clips)} segments, {len(skip)} already done", flush=True)
    for i, c in enumerate(clips):
        if c in skip: continue
        p = SEG / f"{c}.mp4"; a = audio16k(p)
        spans = get_speech_timestamps(a, VadOptions(**VAD), sampling_rate=16000)
        speech = sum(s["end"] - s["start"] for s in spans) / len(a)
        n, w, h = probe_frames(p); dur = n / FPS
        samp = [int(round(t * FPS)) for t in np.arange(SAMPLE_EVERY_S / 2, dur, SAMPLE_EVERY_S)]
        imgs = frames_at(p, samp, n, w, h); keys = sorted(imgs); E = embed([imgs[k] for k in keys])
        m = E.mean(0); m_unit = m / np.linalg.norm(m)
        disp = float(np.mean(1 - E @ m_unit))
        cut_frames = [int(x["frame"]) for x in rows[c]["cuts"]]
        dist = join_distances(p, cut_frames)[0] if cut_frames else []
        rec = {"clip": c, "duration_s": dur, "speech_prop": float(speech), "n_speech_spans": len(spans),
               "n_cuts": len(cut_frames), "cut_clip_dist": dist, "sem_change_per_min": float(np.sum(dist) / dur * 60),
               "sem_dispersion": disp, "n_sampled_frames": len(keys), "mean_embedding": [round(float(x), 6) for x in m_unit]}
        with open(out, "a") as f: f.write(json.dumps(rec) + "\n")
        print(f"[{i+1:3}/{len(clips)}] {c:20} speech {speech:.2f}  cuts {len(cut_frames):2}  sem_change/min {rec['sem_change_per_min']:.2f}  disp {disp:.3f}", flush=True)


def words():
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8")
    clips = sorted(json.loads(l)["clip"] for l in open(H / "scene_switches_corpus.jsonl"))
    out = H / "content_words.jsonl"; skip = done(out)
    print(f"{len(clips)} segments, {len(skip)} already done", flush=True)
    for i, c in enumerate(clips):
        if c in skip: continue
        a = audio16k(SEG / f"{c}.mp4")
        segs, _ = model.transcribe(a, language="en", vad_filter=True, vad_parameters=VAD)
        text = " ".join(s.text.strip() for s in segs)
        rec = {"clip": c, "duration_s": len(a) / 16000, "n_words": len(text.split()), "words_per_min": len(text.split()) / (len(a) / 16000) * 60, "text": text}
        with open(out, "a") as f: f.write(json.dumps(rec) + "\n")
        print(f"[{i+1:3}/{len(clips)}] {c:20} words/min {rec['words_per_min']:.0f}", flush=True)


if __name__ == "__main__":
    {"validate": lambda: validate(sys.argv[2], sys.argv[3]), "av": av, "words": words}[sys.argv[1]]()
