r"""Turn a report written as plain HTML into a single self-contained page.

Usage: python build.py body.html report.html

The body holds the content of <main> only (header, sections). This script adds the title, the fonts and the
shared style and the French / English toggle, and embeds every image referenced as src="figure.png" (path relative to the body) as base64.
"""

import base64
import re
import sys

from pathlib import Path

HERE = Path(__file__).parent
FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600'
    '&family=JetBrains+Mono:wght@400&display=swap">'
)


# French by default; the choice of a reader is remembered in their own browser only
SCRIPT = """<script>
(() => {
  const buttons = document.querySelectorAll(".langs button");
  const set = (lang) => {
    document.body.classList.toggle("en", lang === "en");
    document.documentElement.lang = lang;
    buttons.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.lang === lang)));
    try { localStorage.setItem("lang", lang); } catch (e) {}
  };
  buttons.forEach((b) => b.addEventListener("click", () => set(b.dataset.lang)));
  let saved = "fr";
  try { saved = localStorage.getItem("lang") || "fr"; } catch (e) {}
  set(saved);
})();
</script>"""


def embed(match: re.Match, folder: Path) -> str:
    path = folder / match.group(1)
    kind = "svg+xml" if path.suffix == ".svg" else path.suffix.lstrip(".")
    return f'src="data:image/{kind};base64,{base64.b64encode(path.read_bytes()).decode()}"'


def build(body: Path, output: Path) -> None:
    content = body.read_text()
    # The first title is the French one
    title = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.S).group(1).strip()
    content = re.sub(r'src="(?!data:|https?:)([^"]+)"', lambda m: embed(m, body.parent), content)
    css = (HERE / "style.css").read_text()
    page = (
        f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{FONTS}\n'
        f"<style>\n{css}</style>\n<main>\n{content}\n</main>\n{SCRIPT}\n"
    )
    output.write_text(page)
    print(f"{output} ({len(page) / 1e6:.2f} MB)")


if __name__ == "__main__":
    build(Path(sys.argv[1]), Path(sys.argv[2]))
