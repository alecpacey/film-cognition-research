#!/usr/bin/env python3
"""Build the preprint PDF from research/PAPER.md: Markdown -> HTML with a print stylesheet ->
headless Chrome -> page numbers and document metadata stamped with pypdf/reportlab.
    python build_preprint.py            (needs markdown-it-py, mdit-py-plugins, pypdf, reportlab; Google Chrome)
Writes Pacey-2026-technique-response-index-v1.pdf and the intermediate .html beside this file."""
import io, subprocess, sys
from pathlib import Path
from markdown_it import MarkdownIt
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "PAPER.md"
NAME = "Pacey-2026-technique-response-index-v1"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TITLE = "A technique→response index for cinematography, measured through a brain encoding model"

CSS = """
@page { size: A4; margin: 20mm 19mm 22mm 19mm; }
html { font-family: Charter, "Iowan Old Style", Georgia, serif; font-size: 10.2pt; line-height: 1.42; color: #111; }
body { margin: 0; }
h1 { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 18pt; line-height: 1.2; margin: 0 0 8pt; }
h2 { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 13pt; margin: 18pt 0 6pt; border-bottom: 0.6pt solid #999; padding-bottom: 2pt; break-after: avoid; }
h3 { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 11pt; margin: 13pt 0 4pt; break-after: avoid; }
h4 { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 10pt; margin: 10pt 0 3pt; break-after: avoid; }
p { margin: 0 0 6pt; text-align: justify; hyphens: auto; orphans: 3; widows: 3; }
ul, ol { margin: 0 0 6pt; padding-left: 16pt; } li { margin: 0 0 2pt; hyphens: manual; }
code { font-family: Menlo, "SF Mono", monospace; font-size: 8.4pt; background: #f2f2f2; padding: 0 2pt; border-radius: 2pt; overflow-wrap: anywhere; }
blockquote { margin: 6pt 0 6pt 10pt; padding-left: 8pt; border-left: 2pt solid #bbb; color: #333; }
hr { border: 0; border-top: 0.6pt solid #bbb; margin: 12pt 0; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 8.3pt; line-height: 1.3; break-inside: avoid; }
th, td { border: 0.5pt solid #bbb; padding: 2.5pt 4pt; vertical-align: top; text-align: left; overflow-wrap: normal; word-break: normal; hyphens: manual; }
th { background: #eee; } tr { break-inside: avoid; }
a { color: #1a4f8a; text-decoration: none; }
sub, sup { font-size: 70%; line-height: 0; }
"""


def build():
    md = MarkdownIt("commonmark", {"html": True, "typographer": False}).enable("table")
    body = md.render(SRC.read_text())
    html = (f"<!doctype html><html lang='en-GB'><head><meta charset='utf-8'><title>{TITLE}</title>"
            f"<style>{CSS}</style></head><body>{body}</body></html>")
    h = HERE / f"{NAME}.html"; h.write_text(html, encoding="utf-8")
    raw = HERE / f"{NAME}.raw.pdf"
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={raw}", h.as_uri()], capture_output=True, text=True, timeout=180)
    if not raw.exists() or raw.stat().st_size == 0:
        sys.exit(f"Chrome produced no PDF:\n{r.stderr[-800:]}")
    reader = PdfReader(str(raw)); n = len(reader.pages); writer = PdfWriter()
    for i, page in enumerate(reader.pages, 1):
        buf = io.BytesIO(); w, hgt = float(page.mediabox.width), float(page.mediabox.height)
        c = canvas.Canvas(buf, pagesize=(w, hgt)); c.setFont("Helvetica", 7.5); c.setFillGray(0.35)
        c.drawCentredString(w / 2, 22, f"{i} / {n}")
        c.drawString(54, 22, "Pacey (2026) · preprint v1"); c.drawRightString(w - 54, 22, "github.com/alecpacey/film-cognition-research")
        c.save(); buf.seek(0); page.merge_page(PdfReader(buf).pages[0]); writer.add_page(page)
    writer.add_metadata({"/Title": TITLE, "/Author": "Alec Pacey",
                         "/Subject": "Preprint, version 1, 8 October 2026",
                         "/Keywords": "cinematography; brain encoding model; TRIBE; fMRI; pre-registration; film editing; cut rate"})
    out = HERE / f"{NAME}.pdf"
    with open(out, "wb") as f: writer.write(f)
    raw.unlink()
    print(f"wrote {out.name}: {n} pages, {out.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    build()
