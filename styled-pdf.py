import subprocess
import tempfile
import os
import sys
import shutil
import datetime

# === 1. Paths & Config ===
markdown_files = [
    os.path.join(os.path.dirname(__file__), "README.md"),
    # Add more markdown files here if needed
]
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_pdf = f"vnc_tutorial_{timestamp}.pdf"

# === 2. Your CSS styling ===
css_content = """
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

# === 3. Check dependencies ===
def check_dependencies():
    for tool in ["pandoc", "wkhtmltopdf"]:
        if not shutil.which(tool):
            print(f"Error: {tool} is not installed or not in PATH.")
            sys.exit(1)

# === 4. Convert ===
def generate_pdf_from_md(md_paths, css, output_pdf):
    valid_md_files = [f for f in md_paths if os.path.isfile(f)]

    if not valid_md_files:
        print("Error: No valid Markdown files found.")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        combined_md_path = os.path.join(tmpdir, "combined.md")
        css_file = os.path.join(tmpdir, "style.css")
        html_file = os.path.join(tmpdir, "output.html")

        # Merge all markdown files
        with open(combined_md_path, "w", encoding="utf-8") as outfile:
            for md_file in valid_md_files:
                with open(md_file, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n\n")

        with open(css_file, "w", encoding="utf-8") as f:
            f.write(css)

        subprocess.run([
            "pandoc", combined_md_path,
            "-s", "--css", css_file,
            "-o", html_file
        ], check=True)

        subprocess.run([
            "wkhtmltopdf", html_file, output_pdf
        ], check=True)

        print(f"\n✅ PDF generated: {output_pdf}")

# === 5. Run ===
if __name__ == "__main__":
    check_dependencies()
    generate_pdf_from_md(markdown_files, css_content, output_pdf)
