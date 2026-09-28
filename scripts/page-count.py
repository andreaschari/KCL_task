"""Render a markdown file to PDF and report its page count.

The CSS below sets the assumed submission format: A4, 1.8 cm margins, 10.5 pt
serif, left-aligned text, 8.5 pt tables, 7.6 pt code in a shaded box. The page count is only meaningful relative
to that format; adjust the CSS if the target format differs. Prints a warning
when the count exceeds 2 pages.

Usage:  python3 scripts/page-count.py report.md [out.pdf]
Needs:  markdown (pip), and soffice + pdfinfo on PATH.
"""
import os, subprocess, sys, tempfile
import markdown

CSS = """<style>
@page { size: A4; margin: 1.8cm; }
body { font-family: 'Liberation Serif', serif; font-size: 10.5pt; line-height: 1.22; }
h1 { font-size: 15pt; margin: 0 0 6pt 0; }
h2 { font-size: 11.5pt; margin: 9pt 0 3pt 0; }
p { margin: 0 0 4pt 0; text-align: left; }
li { margin: 0 0 4pt 0; text-align: left; }
table { border-collapse: collapse; font-size: 8.5pt; width: 100%; }
td, th { border: 0.5pt solid #999; padding: 1.5pt 3pt; vertical-align: top; }
pre { font-family: 'Liberation Mono', monospace; font-size: 7.6pt; line-height: 1.1; margin: 3pt 0;
      background: #f3f3f3; border: 0.5pt solid #bbbbbb; padding: 4pt; }
code { font-family: 'Liberation Mono', monospace; font-size: 9pt; }
</style>"""

def pages(src, keep_pdf=None):
    body = markdown.markdown(open(src).read(), extensions=["tables", "fenced_code"])
    with tempfile.TemporaryDirectory() as d:
        html = os.path.join(d, "note.html")
        open(html, "w").write(f"<html><head><meta charset='utf-8'>{CSS}</head>"
                              f"<body>{body}</body></html>")
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", d, html],
                       check=True, capture_output=True)
        pdf = os.path.join(d, "note.pdf")
        info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
        n = int(next(l for l in info.splitlines() if l.startswith("Pages")).split()[-1])
        if keep_pdf:
            os.replace(pdf, keep_pdf)
    return n

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "report.md"
    out = sys.argv[2] if len(sys.argv) > 2 else None
    n = pages(src, out)
    print(f"{src}: {n} page(s)" + (f"  -> {out}" if out else "")
          + ("  ** OVER the 2-page limit **" if n > 2 else "  (within 2 pages)"))
