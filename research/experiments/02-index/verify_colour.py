#!/usr/bin/env python3
"""
Is this print actually in colour?

Every title in the stage-02 corpus is a documented Technicolor production, but a
documented Technicolor production can still reach the archive as a black-and-white
dupe — and a black-and-white film in this corpus is the exact failure the corpus
question exists to avoid (saturation becomes a perfect proxy for film identity).

The pixel format proves nothing: a greyscale encode is still yuv420p, just with
flat chroma planes. So this measures actual chroma:

  mean saturation  HSV S channel, 0-255
  colourfulness    Hasler-Susstrunk, on the rg / yb opponent axes
  chroma           mean |R-G|, |G-B|, |R-B| per pixel — exactly 0 for true greyscale

Sampling is spread across the running time and skips the head and tail, so titles
and end credits (often monochrome even in a colour film) do not dominate.

    python verify_colour.py sources/nothing_sacred_1937.mp4
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path
import cv2, numpy as np

SAT_FLOOR, CHROMA_FLOOR = 15.0, 3.0     # a greyscale print sits near zero on both


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", str(path)],
                         capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def measure(frame, max_side=480):
    h, w = frame.shape[:2]
    s = max_side / max(h, w)
    if s < 1.0:
        frame = cv2.resize(frame, (int(w*s), int(h*s)), interpolation=cv2.INTER_AREA)
    sat = float(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[:, :, 1].mean())
    B, G, R = [frame[:, :, i].astype("float32") for i in range(3)]
    rg, yb = R - G, 0.5*(R + G) - B
    colourful = float(np.hypot(rg.std(), yb.std()) + 0.3*np.hypot(rg.mean(), yb.mean()))
    chroma = float(np.abs(np.stack([R - G, G - B, R - B])).mean())
    return sat, colourful, chroma


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--n", type=int, default=12, help="frames to sample")
    ap.add_argument("--skip", type=float, default=0.05,
                    help="fraction of runtime to skip at each end (titles, credits)")
    ap.add_argument("--json", help="append the result to this file")
    a = ap.parse_args()

    dur = duration(a.video)
    lo, hi = dur * a.skip, dur * (1 - a.skip)
    times = np.linspace(lo, hi, a.n)

    rows = []
    with tempfile.TemporaryDirectory() as td:
        for t in times:
            png = Path(td) / f"f{int(t)}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", a.video,
                            "-frames:v", "1", "-y", str(png)], check=True)
            img = cv2.imread(str(png))
            if img is None:
                print(f"  ! could not decode a frame at {t:.0f}s", file=sys.stderr); continue
            rows.append((t,) + measure(img))

    if not rows:
        print("STOP: no frames decoded", file=sys.stderr); sys.exit(1)

    print(f"{Path(a.video).name}   {dur:.1f}s   {len(rows)} frames "
          f"({lo:.0f}-{hi:.0f}s)\n")
    print(f"{'t (s)':>8} {'mean sat':>9} {'colourful':>10} {'chroma':>8}")
    for t, s, c, ch in rows:
        print(f"{t:8.0f} {s:9.2f} {c:10.2f} {ch:8.2f}")

    sat = float(np.mean([r[1] for r in rows]))
    col = float(np.mean([r[2] for r in rows]))
    chr_ = float(np.mean([r[3] for r in rows]))
    sat_rng = (min(r[1] for r in rows), max(r[1] for r in rows))
    ok = sat > SAT_FLOOR and chr_ > CHROMA_FLOOR
    print(f"\n{'MEAN':>8} {sat:9.2f} {col:10.2f} {chr_:8.2f}")
    print(f"saturation range across sample: {sat_rng[0]:.1f} - {sat_rng[1]:.1f}")
    print(f"\nVERDICT: {'COLOUR' if ok else 'GREYSCALE / SUSPECT — do not use before inspecting'}")

    if a.json:
        p = Path(a.json)
        data = json.loads(p.read_text()) if p.exists() else {}
        data[Path(a.video).name] = {"duration_s": dur, "n_frames": len(rows),
                                    "mean_saturation": sat, "colourfulness": col,
                                    "chroma": chr_, "saturation_range": list(sat_rng),
                                    "verdict": "COLOUR" if ok else "SUSPECT"}
        p.write_text(json.dumps(data, indent=1))
        print(f"wrote {p}")


if __name__ == "__main__":
    main()
