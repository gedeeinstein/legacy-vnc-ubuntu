import os
import sys
import datetime
import tempfile
import markdown
from pathlib import Path
from playwright.sync_api import sync_playwright

# === 1. Paths & Config ===
def get_markdown_files():
    return [
        os.path.join(os.path.dirname(__file__), "README.md"),
        # Add more markdown files here if needed
    ]

def get_output_pdf_name():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"vnc_tutorial_{timestamp}.pdf"

CSS_CONTENT = """
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 30px;
  line-height: 1.6;
  color: #222;
  background: white;
}
h1, h2, h3, h4, h5 {
  font-weight: bold;
  margin-top: 1em;
  color: #2c3e50;
}
code {
  background: #f4f4f4;
  padding: 2px 4px;
  border-radius: 4px;
  font-family: monospace;
}
pre {
  background: #2d2d2d;
  color: #f8f8f2;
  padding: 1em;
  border-radius: 6px;
  overflow-x: auto;
}
blockquote {
  border-left: 4px solid #ccc;
  padding-left: 1em;
  color: #555;
  font-style: italic;
}
details summary {
  cursor: pointer;
  font-weight: 600;
}
"""

def merge_markdown_files(md_paths):
    content = ""
    for md_file in md_paths:
        if os.path.isfile(md_file):
            with open(md_file, "r", encoding="utf-8") as infile:
                content += infile.read() + "\n\n"
    return content

def markdown_to_html(md_text, css):
    html_body = markdown.markdown(md_text, extensions=['extra', 'codehilite', 'toc'])
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>"""

def html_to_pdf(html_content, output_pdf):
    with tempfile.TemporaryDirectory() as tmpdir:
        html_path = os.path.join(tmpdir, "temp.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file:///{html_path}")
            # Wait for content to load
            page.wait_for_timeout(1000)
            page.pdf(path=output_pdf, format="A4")
            browser.close()
    print(f"\n✅ PDF generated: {output_pdf}")

def main():
    md_files = get_markdown_files()
    output_pdf = get_output_pdf_name()
    combined_md = merge_markdown_files(md_files)
    if not combined_md.strip():
        print("Error: No valid Markdown files found.")
        sys.exit(1)
    html_content = markdown_to_html(combined_md, CSS_CONTENT)
    html_to_pdf(html_content, output_pdf)

if __name__ == "__main__":
    main()
