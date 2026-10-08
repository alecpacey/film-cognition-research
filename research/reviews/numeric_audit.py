#!/usr/bin/env python3
"""4i numeric audit. Every decimal and percentage in PAPER.md is looked for in the evidence corpus:
committed text records written by the analyses (RESULT / notes / LOG), summary JSON outputs (not raw
data), and the three external sources verified in 4g. Planning documents (ROADMAP, CONSOLIDATION,
reviews) are excluded so that a number cannot be 'supported' by a document that merely copied it.
Matching: exact string (sign-insensitive) anywhere in the text records; for >= 3 decimals, also any
float in a summary JSON that rounds to it. Unmatched numbers are listed with their line for manual review."""
import json, re, html, sys
from pathlib import Path

R = Path("/Users/alecpacey/Documents/film/film-cognition-research/research")
S = Path(sys.argv[1])
TEXT_GLOBS = ["experiments/*/RESULT.md", "experiments/*/README.md", "experiments/*/CLIPS.md", "experiments/LOG.md",
              "experiments/02-index/*.md", "experiments/03b-discontinuity/*.md"]
RAW = {"parcel_vectors.json", "timelines.json", "content_av.jsonl", "dial_table.json", "selection.json",
       "segments_manifest.json", "batch_names.json", "names.json", "progress.json", "parcel_vectors_text.json"}
EXCLUDE_TEXT = {"ROADMAP.md", "OBJECTIVES.md", "HANDOFF.md"}

text = []
for g in TEXT_GLOBS:
    for f in R.glob(g):
        if f.name not in EXCLUDE_TEXT: text.append(f.read_text(errors="ignore"))
for f in ["arxiv_2507.22229.html", "leipold_v1.html", "cao2024.html"]:
    t = (S / f).read_text(errors="ignore"); text.append(re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))))
corpus = "\n".join(text).replace("−", "-")

floats = []
def walk(x):
    if isinstance(x, bool): return
    if isinstance(x, (int, float)): floats.append(float(x))
    elif isinstance(x, dict): [walk(v) for v in x.values()]
    elif isinstance(x, list): [walk(v) for v in x]
for f in R.glob("experiments/**/*.json"):
    if f.name in RAW or ".venv" in str(f) or f.stat().st_size > 2_000_000: continue
    try: walk(json.loads(f.read_text()))
    except Exception: pass
absf = sorted({abs(x) for x in floats})
import bisect
def json_match(v, k):
    tol = 0.5 * 10 ** -k + 1e-12; i = bisect.bisect_left(absf, abs(v) - tol)
    return i < len(absf) and absf[i] <= abs(v) + tol

paper = (R / "PAPER.md").read_text()
body = paper[:paper.index("## Sources")]
lines = body.split("\n")
NUM = re.compile(r"(?<![\w.])[+−-]?(\d+\.\d+)(%?)")
unmatched, n_checked = [], 0
for ln, line in enumerate(lines, 1):
    if line.startswith("#"): continue
    for m in NUM.finditer(line):
        s, pct = m.group(1), m.group(2); k = len(s.split(".")[1]); v = float(s)
        n_checked += 1
        found = re.search(r"(?<![\d.])" + re.escape(s) + r"(?!\d)", corpus) is not None
        if not found and k >= 3: found = json_match(v, k)
        if not found and k <= 2: found = json_match(v, k) and False   # 2-dp JSON matches are chance; require text
        if not found: unmatched.append((ln, s + pct, line.strip()[:150]))
print(f"decimals checked: {n_checked}; unmatched: {len(unmatched)}")
for ln, s, ctx in unmatched: print(f"  L{ln:5} {s:>9}  | {ctx}")
