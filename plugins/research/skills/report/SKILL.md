---
name: report
description: Use before writing any report, analysis page or study summary meant to be read by the user or shared (published as an HTML artifact), in any project. Gives the fixed structure of a report, the writing rules, the shared page style and a builder that turns the content into one self-contained page. For each figure of the report, also read the figure skill.
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Report: one structure and one look for every
     ┌─┴───┴─┐       report, readable in a minute, also on a phone.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# REPORT

Every report has the same structure and the same look, in every project, so that it reads quickly, also on a phone.
**Every figure follows the `figure` skill**: read it before drawing the first one.

| File                 | What                                                                       |
| -------------------- | -------------------------------------------------------------------------- |
| `body-template.html` | skeleton of a report, in French, to copy and fill                          |
| `style.css`          | shared page style (light and dark themes, phone width)                     |
| `build.py`           | `python build.py body.html report.html`: adds style, title, fonts, images  |

---

## 1. STRUCTURE (ALWAYS THIS ORDER)

1. **Header**: on the first line, `Projet : <name>` on the left, the date and the FR / EN toggle on the right, small
   and grey; the name links to the GitHub repository of the project when it is known (otherwise plain text); then
   the title (a short name, 2 to 4 words); then one or two sentences saying what the report studies and why.
2. **Résumé**: a violet box (thin border, very light inside, "Résumé" set in a gap of its top border:
   `<fieldset class="box summary">` and `<legend>`), holding 3 or 4 bullets; each opens with its topic in semibold, then the
   result and the number that shows it.
3. **Sections**, one per question studied. Each follows the same pattern:
   - a **generic title** naming what is analysed ("Analyse des pics de loss"), not the finding;
   - a paragraph: the **goal** of the analysis, the experiment done to reach it, then what the figure shows and what
     we observe and conclude, citing the figure (Fig. A); the key words (goal, main observation) in semibold, so
     the main information can be picked up at a glance;
   - the figure, then its caption.
   A section always ends with a figure and its caption: nothing comes after them. When a second experiment is needed
   to answer the question, its paragraph, figure and caption follow, in the same order.
   For a report that **summarises past work** (a cleaning of the data, a set of fixes), open each section with three
   columns, `<div class="trio">`: the problem met, the solution put in place, and what we observe since (is it
   solved?); then the figure that shows it, and its caption.
   Captions start with "Fig. A.", "Fig. B.", … (added by the style, in order).
   A caption then has two parts: **what the figure shows, in a few words, in semibold** (it plays the role of the
   figure title, so the PNG has no title of its own); then how to read it: the x axis, the y axis, and what each
   curve is, the word naming a curve in semibold and in the colour of that curve, e.g.
   `<span class="blue">entraînement</span>` (classes `blue`, `amber`, `green`, `vermilion`, `grey`, matching
   `plot_style.py`).
   **Remarks** (a caution, an assumption, an estimate, something not verified) are not gathered at the end: each is a
   short `<aside class="remark">` placed just before the paragraph, figure or box it concerns. On a wide screen it
   sits in the right margin at that level, in thin dark red; on a narrow one, just above.
4. **Conclusion**: the same kind of box in orange (`<fieldset class="box conclusion">`), always after the last
   section: my own conclusions and recommendations, numbered, with why. The orange box is always the conclusion.
5. **Sources**: only when literature or external pages were used.

## 2. TYPOGRAPHY (FIXED, IN `style.css`)

- **One typeface everywhere: Inter**, for titles, text, tables and captions; a monospace only for code and file names.
- **Two weights**: regular (400) and semibold (600, for titles and the opening words of a key point). No italic,
  no capitals for emphasis, no letter-spacing.
- **Four sizes**: title 34 px, section 20 px, text 16 px, captions, tables and header details 14 px.
- **Off-white page (`#f7f7f5`), black text**, in every theme of the viewer (no dark mode): near the most contrast,
  without the glare of pure white. Figures keep a white background; the page blends it into its own colour. No frame or background around the figures. Colour only where it carries information.
- **Text colours**: ink for the text, grey for captions, the subtitle and the header details, dark red for remarks.
- Figures follow the same rule: Inter (or the default sans-serif of matplotlib) in every figure and diagram.

## 3. WRITING

- **Two languages, French by default**: every text I write exists in French and in English, as sibling elements
  marked `lang="fr"` and `lang="en"` (a whole block, or a `<span>` inside a caption or a title); the toggle in the
  header switches between them. The English version is written last (§ 5). Figures are made once, in English. Simple words, short sentences.
- Figures first: the text explains the figure, not the other way around. Few words.
- Numbers rather than adjectives; always say what was measured and what was estimated.
- Small tables only for exact numbers (4 to 5 columns, short cells); never a table where a figure works.
- Give my own conclusions, not only the results.
- One question, one figure: an exploratory sweep stays out of the report.
- **Spell out every variable and acronym** whose meaning is known, at least at its first use: "la température
  de surface de la mer (SST)", so that a reader from outside the project understands. Same in the figures.

## 4. FIGURES AND DIAGRAMS

- Results: matplotlib figures following the `figure` skill, saved as PNG (`dpi=110` or more). Every figure takes the
  width of the text column: `<figure>`, inside it `<div class="plate">`, then a `<figcaption>`.
- Diagrams (an architecture, a pipeline): hand-written inline SVG using `currentColor`, inside
  `<div class="plate svg">`, so that they follow the light and dark themes.

## 5. BUILD AND PUBLISH

1. Write the analysis script and the figures in the analysis folder of the project (never in the repository).
2. Copy `body-template.html` next to them and write the whole report **in French only** (figures stay in English):
   gather the data, run the analysis, draw the figures, write the text. Leave the `lang="en"` elements empty for now.
3. When the French draft is final, the one I would hand over, **translate it into English as the last step**: fill
   every `lang="en"` element next to its French one, nothing else changes.
4. `python build.py body.html report.html`, look at the page at phone width (about 400 px) when a browser is
   available, in both languages, then publish it as an artifact.
5. Keep the same file path to update the same artifact, and give the link.
