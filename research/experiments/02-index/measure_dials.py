#!/usr/bin/env python3
"""
Run cinemetrics over every stage-02 segment and build the dial table.

Resumable and parallel. Each segment is written to its own JSON under dials/, so
a run that dies half-way keeps everything it finished — the same checkpoint
discipline run_batch.py uses for GPU work, for the same reason.

Timing, measured rather than assumed: ~28 s per 60 s segment at 720p, not the
"~2 s per clip" the stage README inherited. That figure came from shorter,
smaller clips; at 1439 frames of 988x720 with stride 1, YuNet and dense optical
flow dominate. 244 segments is ~2 h serial, ~30 min at 4 workers on this machine.

Stride stays at 1 deliberately. Raising it would halve the cost, but cut
detection compares adjacent frames — skipping frames risks missing cuts, and cut
rate is the dial stage 01 established and the one stage 02 must replicate.

    python measure_dials.py --workers 4
    python measure_dials.py --collect      # merge the per-segment JSON into one table
"""
import argparse, json, subprocess, sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

CINEMETRICS = Path(__file__).resolve().parents[2] / "cinematography" / "cinemetrics.py"
SEGMENTS = Path("segments")
DIALS = Path("dials")


def measure(seg: Path):
    out = DIALS / f"{seg.stem}.json"
    if out.exists():
        return seg.stem, "cached"
    r = subprocess.run([sys.executable, str(CINEMETRICS), str(seg), "--json", str(out)],
                       capture_output=True, text=True, cwd=str(Path.cwd()))
    if r.returncode != 0 or not out.exists():
        return seg.stem, f"FAILED rc={r.returncode} {r.stderr.strip()[:160]}"
    return seg.stem, "ok"


def collect():
    """Flatten the per-segment JSON into one row per segment.

    cinemetrics --json writes a LIST of per-clip records, one element even for a
    single clip — introspected, not assumed, after an earlier version guessed a
    dict keyed by clip path and died on it.

    shot_scale.face_area_frac is null on the 16 segments where YuNet found no face
    at all. Those are encoded as 0.0: for a shot-scale proxy, "no face in frame"
    genuinely means the shot is not scaled to a face. cinemetrics' own docstring
    declines to make that call, so `face_hit_rate` is carried alongside as a
    separate dial — it keeps "no face present" distinguishable from "a tiny face",
    which a bare 0.0 would conflate.
    """
    rows = {}
    for p in sorted(DIALS.glob("*.json")):
        d = json.loads(p.read_text())
        if isinstance(d, list):
            d = d[0]
        film = p.stem.rsplit("_", 1)[0]
        rows[p.stem] = {
            "film": film,
            "cuts_per_min":     d["cuts"]["cuts_per_min"],
            "mean_shot_len_s":  d["cuts"]["mean_shot_len_s"],
            "camera_jitter":    d["camera"]["jitter"],
            "camera_zoom":      d["camera"]["net_zoom"],
            "camera_pan":       d["camera"]["pan_per_frame_frac"],
            "median_luma":      d["lighting"]["median_luma"],
            "contrast_p5_p95":  d["lighting"]["contrast_p5_p95"],
            "shadow_frac":      d["lighting"]["shadow_frac"],
            "colourfulness":    d["colour"]["colourfulness"],
            "mean_saturation":  d["colour"]["mean_saturation"],
            "warm_cool":        d["colour"]["warm_cool"],
            "face_area_frac":   d["shot_scale"].get("face_area_frac") or 0.0,
            "face_hit_rate":    d["shot_scale"].get("hit_rate", 0.0),
            "shot_scale_label": d["shot_scale"].get("scale"),
            "dof_ratio":        d["dof"]["centre_surround_sharpness"],
        }
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--out", default="dial_table.json")
    a = ap.parse_args()

    DIALS.mkdir(exist_ok=True)

    if a.collect:
        rows = collect()
        Path(a.out).write_text(json.dumps(rows, indent=1))
        print(f"{len(rows)} segments -> {a.out}")
        raise SystemExit

    segs = sorted(SEGMENTS.glob("*.mp4"))
    todo = [s for s in segs if not (DIALS / f"{s.stem}.json").exists()]
    print(f"{len(segs)} segments, {len(todo)} to measure, {a.workers} workers", flush=True)

    done = fails = 0
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(measure, s): s for s in todo}
        for f in as_completed(futs):
            name, status = f.result()
            done += 1
            if status.startswith("FAILED"):
                fails += 1
                print(f"  {name}: {status}", flush=True)
            if done % 20 == 0 or done == len(todo):
                print(f"  {done}/{len(todo)}  ({fails} failed)", flush=True)
    print("measurement finished")
