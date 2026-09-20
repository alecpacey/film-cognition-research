#!/usr/bin/env python3
"""
Build the three 03b ladders per README.md. $0, local ffmpeg. Bases are stage 03's single takes.

  B  face_close  x  face_close mirrored + shifted 30 s      (hard cuts, same scene)
  C  landscape   x  landscape  mirrored + shifted 30 s      (hard cuts, same scene)
  D  face_close  x  landscape, every join a cross-dissolve  (scene switches, no hard cut)

B and C use ../01-cutrate/build_conditions.py UNCHANGED. Every clip then gets the landscape
base's continuous ambient audio with the same ffmpeg call stage 03 used for its S- arm.
    python3 build_03b.py [--dissolve 0.5]
"""
import argparse, subprocess, sys, tempfile
from pathlib import Path
H = Path(__file__).parent; BASES = H.parent / "03-isolation" / "clips"
FACE, LAND = BASES / "face_close.mp4", BASES / "landscape.mp4"
ALT = [1, 2, 4, 8, 16]; TOTAL = 60.0; LEAD = 0.25       # LEAD: D reads sources from +0.25 s so a join can extend 0.25 s before a segment start

def run(cmd): subprocess.run(cmd, check=True)
def ff(*a): run(["ffmpeg", "-v", "error", "-y", *map(str, a)])
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p"]

def mirrored_shifted(src, out):
    """out(t) = hflip(src(t + 30 s)), wrapping: [30,60) then [0,30)."""
    ff("-i", src, "-filter_complex",
       "[0:v]trim=30:60,setpts=PTS-STARTPTS[a];[0:v]trim=0:30,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0,hflip[v]",
       "-map", "[v]", "-map", "0:a", *ENC, "-c:a", "aac", "-b:a", "128k", "-t", "60", out)

def ambient(src, out):                                   # identical to build_stage03.sh's S- line
    ff("-i", src, "-i", LAND, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out)

def dissolve_ladder(outdir, T):
    outdir.mkdir(parents=True, exist_ok=True)
    for n in ALT:
        dur, N = (TOTAL / 2) / n, 2 * n
        with tempfile.TemporaryDirectory() as td:
            td = Path(td); parts, lens = [], []
            for i in range(n):
                for src in (FACE, LAND):
                    k = len(parts); pre = T / 2 if k > 0 else 0.0; post = T / 2 if k < N - 1 else 0.0
                    p = td / f"{k:02d}.mp4"; L = dur + pre + post
                    ff("-ss", f"{LEAD + i * dur - pre:.4f}", "-i", src, "-t", f"{L:.4f}", "-an", "-vf", "fps=24,settb=AVTB", *ENC, p)
                    parts.append(p); lens.append(L)
            ins = [x for p in parts for x in ("-i", str(p))]
            fc, prev, acc = [], "[0:v]", lens[0]
            for k in range(1, N):
                lab = f"[x{k}]"; fc.append(f"{prev}[{k}:v]xfade=transition=fade:duration={T}:offset={acc - T:.4f}{lab}"); prev = lab; acc += lens[k] - T
            tmp = td / "v.mp4"
            if N == 1: raise SystemExit("N==1 unreachable")
            ff(*ins, "-filter_complex", ";".join(fc), "-map", prev, "-t", f"{TOTAL:.3f}", *ENC, tmp)
            ambient(tmp, outdir / f"cut{N - 1:02d}.mp4")
        print(f"D cut{N-1:02d}  seg {dur:.3f}s  dissolve {T}s  blend fraction {(N-1)*T/TOTAL:.2f}", flush=True)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--dissolve", type=float, default=0.5); ap.add_argument("--only", default="BCD"); a = ap.parse_args()
    work = H / "clips"; work.mkdir(exist_ok=True)
    for tag, base in (("B", FACE), ("C", LAND)):
        if tag not in a.only: continue
        ms = work / f"{base.stem}_mirrored_shifted.mp4"; mirrored_shifted(base, ms)
        raw = work / f"{tag}_raw"; run([sys.executable, str(H.parent / "01-cutrate" / "build_conditions.py"), str(base), str(ms), "--outdir", str(raw)])
        (work / tag).mkdir(exist_ok=True)
        for f in sorted(raw.glob("cut*.mp4")): ambient(f, work / tag / f.name)
    if "D" in a.only: dissolve_ladder(work / "D", a.dissolve)
    print("built:", {t: len(list((work / t).glob("cut*.mp4"))) for t in "BCD"})
