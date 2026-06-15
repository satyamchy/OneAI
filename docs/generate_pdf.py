#!/usr/bin/env python3
"""Convert PAIOS-Architecture.md to a styled PDF via Chrome headless."""

import re
import subprocess
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).parent
MD_FILE = DOCS_DIR / "PAIOS-Architecture.md"
HTML_FILE = DOCS_DIR / "PAIOS-Architecture.html"
PDF_FILE = DOCS_DIR / "PAIOS-Architecture.pdf"

CSS = """
@page {
  size: A4;
  margin: 18mm 16mm 20mm 16mm;
}
* { box-sizing: border-box; }
body {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  font-size: 10.5pt;
  line-height: 1.55;
  color: #1a1a2e;
  max-width: 100%;
  margin: 0;
  padding: 0;
}
.cover {
  page-break-after: always;
  text-align: center;
  padding-top: 80px;
  min-height: 90vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.cover h1 {
  font-size: 28pt;
  color: #0f3460;
  margin-bottom: 8px;
  border: none;
}
.cover .subtitle {
  font-size: 14pt;
  color: #533483;
  margin-bottom: 40px;
}
.cover .meta {
  font-size: 11pt;
  color: #666;
  line-height: 2;
}
.cover .use-cases {
  margin-top: 50px;
  text-align: left;
  max-width: 480px;
  background: #f0f4f8;
  padding: 24px 32px;
  border-radius: 8px;
  border-left: 4px solid #0f3460;
}
.cover .use-cases h3 { margin-top: 0; color: #0f3460; font-size: 12pt; }
.cover .use-cases ul { margin: 0; padding-left: 20px; }
h1 {
  font-size: 20pt;
  color: #0f3460;
  border-bottom: 2px solid #0f3460;
  padding-bottom: 6px;
  margin-top: 28px;
  page-break-after: avoid;
}
h2 {
  font-size: 14pt;
  color: #16213e;
  margin-top: 22px;
  page-break-after: avoid;
}
h3 {
  font-size: 12pt;
  color: #533483;
  margin-top: 16px;
  page-break-after: avoid;
}
h4 { font-size: 11pt; color: #444; margin-top: 12px; }
p { margin: 8px 0; }
ul, ol { margin: 8px 0; padding-left: 24px; }
li { margin: 4px 0; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
  font-size: 9.5pt;
  page-break-inside: avoid;
}
th {
  background: #0f3460;
  color: white;
  padding: 8px 10px;
  text-align: left;
  font-weight: 600;
}
td {
  padding: 7px 10px;
  border-bottom: 1px solid #dde3ea;
  vertical-align: top;
}
tr:nth-child(even) td { background: #f8fafc; }
pre {
  background: #1a1a2e;
  color: #e8e8e8;
  padding: 14px 16px;
  border-radius: 6px;
  font-size: 8.5pt;
  line-height: 1.45;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  page-break-inside: avoid;
  margin: 12px 0;
}
code {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 9pt;
  background: #eef2f7;
  padding: 1px 5px;
  border-radius: 3px;
}
pre code { background: none; padding: 0; color: inherit; }
hr {
  border: none;
  border-top: 1px solid #dde3ea;
  margin: 20px 0;
}
.toc {
  page-break-after: always;
  padding: 20px 0;
}
.toc h2 { border-bottom: 2px solid #0f3460; }
.toc ol { line-height: 1.8; }
.toc a { color: #0f3460; text-decoration: none; }
.section { page-break-inside: avoid; }
footer {
  display: none;
}
@media print {
  h1, h2, h3 { page-break-after: avoid; }
  pre, table { page-break-inside: avoid; }
}
"""


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_]+", "-", text).strip("-")


def parse_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        if not line.strip().startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return "\n".join(lines)

    html = ["<table>"]
    html.append("<tr>" + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr>")
    for row in rows[2:]:
        html.append("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>")
    html.append("</table>")
    return "\n".join(html)


def md_to_html(md: str) -> str:
    lines = md.split("\n")
    html_parts: list[str] = []
    i = 0
    in_code = False
    code_buf: list[str] = []
    code_lang = ""

    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith("```"):
            if in_code:
                html_parts.append(
                    f'<pre><code class="{code_lang}">'
                    + _escape("\n".join(code_buf))
                    + "</code></pre>"
                )
                code_buf = []
                in_code = False
                code_lang = ""
            else:
                in_code = True
                code_lang = line.strip()[3:].strip()
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # Tables
        if line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            html_parts.append(parse_table(table_lines))
            continue

        # Headers
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            text = m.group(2)
            sid = slugify(text)
            html_parts.append(f'<h{level} id="{sid}">{_inline(text)}</h{level}>')
            i += 1
            continue

        # HR
        if line.strip() == "---":
            html_parts.append("<hr>")
            i += 1
            continue

        # List items
        if re.match(r"^[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                items.append(f"<li>{_inline(lines[i][2:].strip())}</li>")
                i += 1
            html_parts.append("<ul>" + "".join(items) + "</ul>")
            continue

        if re.match(r"^\d+\.\s+", line):
            items = []
            num_pat = re.compile(r"^\d+\.\s+")
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                item_text = num_pat.sub("", lines[i])
                items.append(f"<li>{_inline(item_text)}</li>")
                i += 1
            html_parts.append("<ol>" + "".join(items) + "</ol>")
            continue

        # Empty line
        if not line.strip():
            i += 1
            continue

        # Paragraph
        html_parts.append(f"<p>{_inline(line)}</p>")
        i += 1

    return "\n".join(html_parts)


def _escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline(s: str) -> str:
    s = _escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def build_toc(md: str) -> str:
    items = []
    for line in md.split("\n"):
        m = re.match(r"^(#{1,2})\s+(.+)$", line)
        if m and not line.startswith("# Personal AI"):
            level = len(m.group(1))
            text = m.group(2)
            if text.startswith("Table of Contents"):
                continue
            sid = slugify(text)
            indent = "  " * (level - 1)
            items.append(f'{indent}<li><a href="#{sid}">{text}</a></li>')
    return "<ol>\n" + "\n".join(items) + "\n</ol>"


def main():
    md = MD_FILE.read_text(encoding="utf-8")
    body = md_to_html(md)
    toc = build_toc(md)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PAIOS Architecture & Build Guide</title>
<style>{CSS}</style>
</head>
<body>

<div class="cover">
  <h1>Personal AI Operating System</h1>
  <div class="subtitle">Complete Architecture &amp; Build Guide</div>
  <div class="meta">
    <strong>Version 1.0</strong><br>
    June 9, 2026<br>
    Provider-Agnostic Personal AI Platform
  </div>
  <div class="use-cases">
    <h3>Your Use Cases</h3>
    <ul>
      <li><strong>Study</strong> — flashcards, study guides, revision sheets</li>
      <li><strong>Trading</strong> — research notes, market analysis, insights</li>
      <li><strong>Excel / Data Analytics</strong> — Q&amp;A on uploaded spreadsheets</li>
      <li><strong>Research</strong> — storage systems, technical deep-dives</li>
      <li><strong>General Q&amp;A</strong> — multi-model chat with memory &amp; citations</li>
    </ul>
  </div>
</div>

<div class="toc">
  <h2>Table of Contents</h2>
  {toc}
</div>

{body}

</body>
</html>"""

    HTML_FILE.write_text(html, encoding="utf-8")
    print(f"HTML written: {HTML_FILE}")

    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ]
    chrome = next((p for p in chrome_paths if Path(p).exists()), None)
    if not chrome:
        print("ERROR: Chrome/Chromium not found. Open HTML manually and print to PDF.")
        sys.exit(1)

    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=10000",
        f"--print-to-pdf={PDF_FILE}",
        "--print-to-pdf-no-header",
        f"file://{HTML_FILE.resolve()}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"Chrome stderr: {result.stderr}")
        sys.exit(result.returncode)

    if PDF_FILE.exists():
        size_kb = PDF_FILE.stat().st_size / 1024
        print(f"PDF generated: {PDF_FILE} ({size_kb:.0f} KB)")
    else:
        print("ERROR: PDF was not created.")
        sys.exit(1)


if __name__ == "__main__":
    main()
