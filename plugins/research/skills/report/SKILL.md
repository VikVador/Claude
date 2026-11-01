---
name: report
description: Use before writing any report, analysis page or study summary meant to be read by the user or shared (published as an HTML artifact), in any project. Gives the fixed structure of a report, its look, the writing rules, and a builder that turns the content into one self-contained bilingual page. For each figure of the report, also read the figure skill.
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

Every report has the same structure and the same look, in every project, so that it reads quickly, on a computer as
on a phone. **Every figure follows the `figure` skill**: read it before drawing the first one.

| File                 | What                                                                                         |
| -------------------- | -------------------------------------------------------------------------------------------- |
| `body-template.html` | skeleton of a report, bilingual, with every element below: copy it and fill                  |
| `style.css`          | the look of every report: never restyle a report by hand                                     |
| `build.py`           | `python build.py body.html report.html`: adds style, title, fonts, FR / EN toggle, images    |

**Contents**

1. Structure
2. Look
3. Writing
4. Figures
5. Work order: build and publish

---

## 1. STRUCTURE (ALWAYS THIS ORDER)

| Part                             | Element                                 | Content                                           |
| -------------------------------- | --------------------------------------- | ------------------------------------------------- |
| Header                           | `<header>`                              | project and date, title, one or two sentences     |
| Résumé                           | `<fieldset class="box summary">`        | the whole report in 3 or 4 bullets                |
| Sections                         | `<section>`                             | one per question studied                          |
| Conclusion, Pour aller plus loin | `<div class="closing">`, two boxes      | the conclusion of each section; notes, next steps |
| Sources                          | `<section class="sources">`             | numbered references, when any is cited            |

### Header

- First line, small and grey: `Projet : <name>` on the left, the date and the FR / EN toggle on the right. The name
  links to the GitHub repository of the project when it is known, otherwise plain text.
- Then the title: a short name, 2 to 4 words.
- Then one or two sentences: what the report studies, and why.

### Résumé (violet box)

The whole report in 3 or 4 bullets. Each opens with its topic in semibold ("Pics de loss."), then the result and the
number that shows it. The title "Résumé" sits in a gap of the top border (`<legend>`).

### Sections

One section per question studied, always in this order:

1. A **generic title** naming what is analysed ("Analyse des pics de loss"), not the finding.
2. **Plain, natural text**, in one or several short paragraphs, one idea each: why this analysis, what was done, what
   the figure shows, what we observe and conclude, citing the figure "(Fig. A)" and the sources. No labels such as
   "But :". The key observations in semibold, with their number, so that the main information is picked up at a
   glance.
3. The figure, then its caption. **A section always ends with a figure and its caption.** When a second experiment
   is needed to answer the question, its paragraphs, figure and caption follow, in the same order.

For a report that **summarises past work** (a cleaning of the data, a set of fixes), each section opens instead with
three columns, `<div class="trio">`: the problem met, the solution put in place, and what we observe since (solved
or not, in semibold); then the figure that shows it, and its caption.

**Remarks**: a caution, an assumption, an estimate, something not verified. Never gathered at the end: each is a
short `<aside class="remark">` placed just before the paragraph, the three columns or the figure it concerns. On a
computer it sits in the right margin at that level, in thin dark red; on a phone, just above, with a red line.

### Conclusion and Pour aller plus loin (orange and teal boxes, side by side)

- **Conclusion** (orange, `box conclusion`): the conclusion of each section in one sentence, numbered, each opening
  with the name of the section in semibold. The violet summary covers the whole report; the orange conclusion
  gathers what each section found. The orange box is always the conclusion.
- **Pour aller plus loin** (teal, `box next`): my notes and remarks for the reader, opening with "À vérifier." (the
  remarks of the margin may come back here), then "Ensuite." with what comes next, when it was already discussed.
- Side by side on a computer, stacked on a phone.

### Sources

Whenever results rely on literature or external pages, look for sources and cite them.

- A section "Sources" below the two boxes: a numbered list, one entry per source, always in this format, each entry
  with an id (`<li id="src-1">`):
  `Author, A., Author, B., & Author, C. (Year). Title. Journal or publisher, volume(issue), pages. <DOI link>`.
- In the text, cite like Geophysical Research Letters: the first author in semibold (coloured by the style), then
  the year, linked to the entry: `(<a class="cite" href="#src-1"><strong>Hampel</strong>, 1974</a>)`; "et al."
  beyond two authors; without parentheses when the author is the subject of the sentence: "selon **Hampel** (1974)".
- Never invent a reference: cite only sources that were found and read.

---

## 2. LOOK (FIXED BY `style.css`)

- **One typeface everywhere: Inter**, for titles, text, tables and captions; a monospace only for code and file
  names. **Two weights**: regular and semibold (titles, opening words of a key point, figure letters). No italic,
  no capitals for emphasis, no letter-spacing.
- **Four sizes**: title 34 px, section 20 px, text 16 px; captions, tables, remarks and header details 14 px.
- **Off-white page (`#f7f7f5`), black text**, whatever the theme of the reader (no dark mode): near the most
  contrast, without the glare of pure white. Figures keep a white background; the page blends it into its own
  colour. No frame or background around the figures.
- **Colour only where it carries information**: grey for captions and details, dark red for remarks, the colour of
  a curve for its name in a caption, teal for links and cited authors, and the three boxes: violet (summary), orange
  (conclusion), teal (next steps).
- **Width**: one column of 960 px; every figure takes exactly that width. Space between paragraphs (20 px) and
  above each figure (28 px).

---

## 3. WRITING

- **Two languages, French by default.** Every text exists in French and in English, as sibling elements marked
  `lang="fr"` and `lang="en"`: a whole block (`<p lang="fr">`, `<ul lang="en">`), or a `<span>` inside a caption,
  a legend or the header. The toggle shows one language at a time. The English version is written last (§ 5).
  Figures are made once, in English.
- Simple words, short sentences, one idea per paragraph. Numbers rather than adjectives.
- Figures first: the text explains the figure, not the other way around.
- **Spell out every variable and acronym** whose meaning is known, at least at its first use, in the text and in
  the figures: "la température de surface de la mer (SST)", so that a reader from outside the project understands.
- Say what was measured and what was estimated; give my own conclusions, not only the results.
- Small tables only for exact numbers (4 to 5 columns, short cells, inside `<div class="table-wrap">`); never a
  table where a figure works. One question, one figure: an exploratory sweep stays out of the report.

---

## 4. FIGURES

- Matplotlib figures following the `figure` skill (and its `plot_style.py`), saved as PNG at `dpi=110` or more,
  without a title of their own: `<figure><div class="plate"><img …></div><figcaption>…</figcaption></figure>`.
- **Captions**: the style adds "Fig. A.", "Fig. B.", … in order. Then two parts:
  1. what the figure shows, in a few words, in semibold (it plays the role of the figure title);
  2. how to read it: the x axis, the y axis, and what each curve is, the word naming a curve in semibold and in the
     colour of that curve: `<span class="blue">entraînement</span>` (classes `blue`, `amber`, `green`, `vermilion`,
     `grey`, the colours of `plot_style.py`).
- Diagrams (an architecture, a pipeline): hand-written inline SVG using `currentColor`, inside
  `<div class="plate svg">`.

---

## 5. WORK ORDER: BUILD AND PUBLISH

1. Write the analysis script and the figures in the analysis folder of the project, never in the repository.
2. Copy `body-template.html` next to them and write the whole report **in French only**: gather the data, run the
   analysis, draw the figures (in English), write the text. Leave the `lang="en"` elements empty for now.
3. When the French draft is final, the one I would hand over, **translate it into English as the last step**: fill
   every `lang="en"` element next to its French one; nothing else changes.
4. `python build.py body.html report.html`.
5. When a browser is available, look at the page at phone width (about 400 px) and at computer width (about
   1440 px), in both languages: no horizontal scroll, remarks in place, boxes side by side or stacked.
6. Publish it as an artifact; keep the same file path to update the same artifact, and give the link.
