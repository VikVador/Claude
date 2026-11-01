---
name: report
description: Use before writing any report, analysis page, study summary or figure for Victor (Heimdall, Neptune or any other project), whether published as an HTML artifact or saved as matplotlib figures. Gives the fixed report structure, the writing rules, the figure rules from Gilles Louppe's visualisation course, and the shared page style.
---

# Reports and figures for Victor

Every report has the same structure and the same look, in every project, so that Victor can read it quickly,
also on his phone. Read this file fully, then `figures.md` before drawing any figure.

## Files of this skill

| File                 | What                                                                       |
| -------------------- | -------------------------------------------------------------------------- |
| `figures.md`         | figure rules: plots, colours, scales, captions, maps, checklist (§ 9)      |
| `body-template.html` | skeleton of a report, in French, to copy and fill                          |
| `style.css`          | shared page style (light and dark themes, phone width)                     |
| `build.py`           | `python build.py body.html report.html`: adds style, title, fonts, images  |
| `plot_style.py`      | matplotlib style and colours, to import or copy in the analysis script     |

## Structure (always this order)

1. **Header**: eyebrow `Projet · sujet`, a short name as title (2 to 4 words), the question in one sentence,
   then date, data used, and whether the numbers are measured or estimated.
2. **En bref**: 3 or 4 bullets, each a result in bold followed by the number that shows it.
3. **One section per message**: the title states the finding, then its figure, its caption, and 2 to 3 lines.
4. **Mes conclusions et la suite**: my own recommendations, numbered, with why.
5. **Ce qui n'est pas vérifié**: assumptions, estimates, open questions.
6. **Sources**: only when literature or external pages were used.

## Writing

- French by default (English only if Victor asks, e.g. for a paper), simple words, short sentences.
- Figures first: the text explains the figure, not the other way around. Few words.
- Numbers rather than adjectives; always say what was measured and what was estimated.
- Small tables only for exact numbers (4 to 5 columns, short cells); never a table where a figure works.
- Give my own conclusions, not only the results.
- Never mix a sweep dump into a report: one question, one figure.

## Figures (details in `figures.md`)

- One figure, one message, stated in its title. Linear scale by default; a logarithmic scale only across
  several orders of magnitude, and said in the caption. Memory is always on a linear scale, with a line per GPU size.
- Axes with quantity and unit in `[]`; maps with longitude, latitude, coastlines, a colorbar of the axis size,
  2 % and 98 % limits; colourblind-safe colours; uncertainty shown.
- Matplotlib with `plot_style.py`; save PNG at `dpi=110` or more; wide figures go in `<figure class="wide">`.
- Diagrams are hand-written inline SVG using `currentColor`, inside `<div class="plate svg">`.
- Run the checklist of `figures.md` § 9 before publishing.

## Building and publishing

1. Write the analysis script and the figures in the project's analysis folder (not in the repository).
2. Copy `body-template.html` next to them, fill it, then `python build.py body.html report.html`.
3. Look at the page at phone width (about 400 px) if a browser is available, then publish it as an artifact.
4. Keep the same file path to update the same artifact; give Victor the link.
