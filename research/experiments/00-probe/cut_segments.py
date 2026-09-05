#!/usr/bin/env python3
"""
Cut probe segments from a source film.

The probe needs three clips of at least 30 s that differ in content but not in
anything else. Taking all three from one film is deliberate: same stock, same
grade, same era, same grain — so content is the only thing that varies. Three
unrelated clips would confound content with everything else about how they were
shot and encoded.

    python cut_segments.py FILM.mp4 --landscape 1420 --crowd 2610 --face 3180

Each timestamp is the START of a 60 s segment, in seconds. 60 rather than the
30 s minimum because TRIBE was trained on 100 s windows and degrades toward the
floor — more context is strictly better and costs nothing here.

Audio is kept. TRIBE has an audio branch and dropping it would waste a modality.
"""

import argparse
import subprocess
import sys
from pathlib import Path

SEG_SECONDS = 60


def cut(src, start, out, seconds=SEG_SECONDS):
    """Re-encode rather than stream-copy, so the segment starts on a keyframe
    and the duration is exact. Stream copy would silently give you a clip that
    starts late or runs short, and short clips are the failure mode we care about."""
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-ss", str(start), "-i", str(src), "-t", str(seconds),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        str(out),
    ]
    subprocess.run(cmd, check=True)


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--landscape", type=float, required=True, help="start second")
    ap.add_argument("--crowd", type=float, required=True)
    ap.add_argument("--face", type=float, required=True)
    ap.add_argument("--seconds", type=float, default=SEG_SECONDS)
    ap.add_argument("--outdir", default="clips")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for label in ("landscape", "crowd", "face"):
        start = getattr(args, label)
        dest = outdir / f"{label}.mp4"
        print(f"cutting {label:<10} from {start:7.1f}s -> {dest}")
        cut(args.source, start, dest, args.seconds)
        got = probe_duration(dest)
        if got < args.seconds - 1.0:
            print(f"  WARNING: {dest.name} is only {got:.1f}s — the source may be "
                  f"shorter than {start + args.seconds:.0f}s", file=sys.stderr)
        else:
            print(f"  ok, {got:.1f}s")

    print("\nNow run:")
    print(f"  python probe.py {outdir}/landscape.mp4 {outdir}/crowd.mp4 {outdir}/face.mp4")


if __name__ == "__main__":
    main()
