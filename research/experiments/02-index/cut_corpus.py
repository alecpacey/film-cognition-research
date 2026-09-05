#!/usr/bin/env python3
"""
Cut the stage-02 corpus into fixed, non-overlapping, normalised 60 s segments.

Two jobs, and the second is the one that matters:

1. SEGMENT. Fixed 60 s windows, non-overlapping, across the middle of each film.
   Fixed rather than shot-aligned for the reasons in CORPUS.md: our unit of
   analysis is the segment, so a scene change inside one is *measured* by the
   cut-rate dial rather than confounding it; and variable-length windows would
   put some near TRIBE's ~30 s floor, where it returns diffuse output without
   erroring.

2. NORMALISE. The three prints arrive at 1472x1072, 1424x1072 and 1440x1080,
   with AC-3 audio on one and AAC on the others. `cinemetrics.py` measures depth
   of field as a centre-versus-surround sharpness ratio and its colour and
   contrast statistics move with encode quality, so an un-normalised corpus would
   let "depth of field" become partly a proxy for which print we downloaded.
   Within-film centring removes a per-film mean; it does NOT remove a
   resolution-dependent difference in a dial's variance. So every segment is
   re-encoded identically: same height, same scaler, same codec, same CRF, same
   audio. All three sources are already 24000/1001 fps and yuv420p, so no frame
   rate conversion is needed and none is applied.

Re-encoded, never stream-copied: a stream copy starts at the nearest keyframe and
silently yields a clip that begins late or runs short, and a short clip is exactly
the failure that returns confident noise.

Head and tail are skipped so titles and end credits — often monochrome even in a
colour film, and never representative of the picture's technique — stay out.

    python cut_corpus.py --plan        # what would be cut, no work
    python cut_corpus.py               # cut everything not already present
"""
import argparse, json, subprocess, sys
from pathlib import Path

SEG = 60.0
SKIP = 0.05                    # fraction of runtime dropped at each end
HEIGHT = 720                   # common target; all sources are 1072-1080 tall
CRF = "20"

FILMS = {
    "nothing_sacred": "sources/nothing_sacred_1937.mp4",
    "royal_wedding":  "sources/royal_wedding_1951.mp4",
    "jungle_book":    "sources/jungle_book_1942.mkv",
}


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", str(path)],
                         capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def plan(films):
    jobs = []
    for slug, src in films.items():
        d = duration(src)
        lo, hi = d * SKIP, d * (1 - SKIP)
        n = int((hi - lo) // SEG)
        for i in range(n):
            jobs.append({"film": slug, "src": src, "index": i,
                         "start": round(lo + i * SEG, 3),
                         "name": f"{slug}_{i:03d}.mp4"})
    return jobs


def cut(job, outdir):
    dest = outdir / job["name"]
    subprocess.run([
        "ffmpeg", "-v", "error", "-y",
        "-ss", f"{job['start']:.3f}", "-i", job["src"], "-t", str(SEG),
        "-vf", f"scale=-2:{HEIGHT}:flags=lanczos",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", CRF, "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2",
        str(dest)], check=True)
    got = duration(dest)
    if got < SEG - 1.0:
        print(f"  WARNING {dest.name}: {got:.1f}s, short", file=sys.stderr)
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="segments")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--manifest", default="segments_manifest.json")
    a = ap.parse_args()

    missing = [s for s in FILMS.values() if not Path(s).exists()]
    if missing:
        print("STOP: missing sources:\n  " + "\n  ".join(missing), file=sys.stderr)
        sys.exit(1)

    jobs = plan(FILMS)
    outdir = Path(a.outdir); outdir.mkdir(parents=True, exist_ok=True)
    todo = [j for j in jobs if not (outdir / j["name"]).exists()]

    per = {}
    for j in jobs:
        per[j["film"]] = per.get(j["film"], 0) + 1
    print(f"{len(jobs)} segments planned  ({', '.join(f'{k} {v}' for k, v in per.items())})")
    print(f"{len(todo)} to cut, {len(jobs)-len(todo)} already present")
    if a.plan:
        for j in todo[:10]:
            print(f"  {j['name']:26} @ {j['start']:8.1f}s")
        return

    for n, j in enumerate(todo, 1):
        j["duration_s"] = cut(j, outdir)
        if n % 20 == 0 or n == len(todo):
            print(f"  {n}/{len(todo)}", flush=True)

    Path(a.manifest).write_text(json.dumps(
        {"segment_seconds": SEG, "height": HEIGHT, "crf": CRF, "skip_fraction": SKIP,
         "segments": jobs}, indent=1))
    print(f"wrote {a.manifest}")


if __name__ == "__main__":
    main()
