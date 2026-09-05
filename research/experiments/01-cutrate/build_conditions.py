#!/usr/bin/env python3
"""
Build the cut-rate conditions.

Two 60 s source scenes, intercut at five rates. Every output is 60 s and contains
exactly 30 s of each source, in order — so total content is identical and the only
variable is how many times it cuts.

Segments are re-encoded, not stream-copied: a stream copy snaps to the nearest
keyframe, which would make the actual cut points drift from the intended ones and
silently vary content across conditions.

    python build_conditions.py ../00-probe/clips/face.mp4 ../00-probe/clips/landscape.mp4
"""
import argparse, subprocess, tempfile
from pathlib import Path

ALTERNATIONS = [1, 2, 4, 8, 16]      # -> 1, 3, 7, 15, 31 cuts
TOTAL = 60.0
PER_SOURCE = TOTAL / 2               # 30 s of each


def seg(src, start, dur, out):
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-ss", f"{start:.4f}", "-i", str(src),
        "-t", f"{dur:.4f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
        "-avoid_negative_ts", "make_zero", str(out)], check=True)


def build(a, b, n_alt, outdir):
    """n_alt alternations of each source -> 2*n_alt segments, 2*n_alt-1 cuts."""
    dur = PER_SOURCE / n_alt
    with tempfile.TemporaryDirectory() as td:
        td = Path(td); parts = []
        for i in range(n_alt):
            for src, tag in ((a, "a"), (b, "b")):
                p = td / f"{i}_{tag}.mp4"
                seg(src, i * dur, dur, p)      # walk forward through each source
                parts.append(p)
        lst = td / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts))
        cuts = 2 * n_alt - 1
        out = outdir / f"cut{cuts:02d}.mp4"
        # Trim to exactly TOTAL. Per-segment encoding rounds up to whole frames and
        # the error accumulates with segment count — without this, cut31 runs ~1.5 s
        # longer than cut01, so "more cuts" would also mean "more content".
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                        "-i", str(lst), "-t", f"{TOTAL:.3f}",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
                        str(out)], check=True)
        return out, cuts, dur


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source_a"); ap.add_argument("source_b")
    ap.add_argument("--outdir", default="clips")
    args = ap.parse_args()
    out = Path(args.outdir); out.mkdir(parents=True, exist_ok=True)
    print(f"{'condition':10} {'cuts':>5} {'seg len':>9} {'duration':>9}")
    for n in ALTERNATIONS:
        f, cuts, dur = build(Path(args.source_a), Path(args.source_b), n, out)
        d = probe(f)
        flag = "" if abs(d - TOTAL) < 1.0 else "  <-- LENGTH DRIFT"
        print(f"{f.name:10} {cuts:>5} {dur:>8.3f}s {d:>8.2f}s{flag}")
