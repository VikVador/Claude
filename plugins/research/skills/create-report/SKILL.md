---
name: create-report
description: "Use before writing an analysis report or a study summary to publish as an HTML artifact (results of an analysis, a diagnostic, a comparison of runs or designs, a summary of past work), in any project. Gives the fixed structure, the way of writing (the message first, details only when they serve), the look (the reef palette of my slides) and build.py, which turns the body into one bilingual page. Use it instead of a generic document or page. Not for a chat answer, a status update or a subagent report."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Create report: one structure and one look for every
     ┌─┴───┴─┐       report, readable in a minute, also on a phone.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# CREATE REPORT

Every report has the same structure, the same way of writing and the same look, in every project, so that I get the
message in a minute, on a computer as on a phone. Each idea comes as its message first, then what makes it
understood, then what proves it; a detail stays only if the rest needs it. For my reports, this skill replaces the
generic document and artifact design guidance: publish the page `build.py` makes as it is (no dark mode, no
restyling).

| File                 | Use                                                                    | When              |
| -------------------- | ---------------------------------------------------------------------- | ----------------- |
| `body-template.html` | **Copy** next to the analysis and fill: every element below, bilingual | start of a report |
| `style.css`          | the look of every report, inlined by `build.py`: never restyle by hand | never edited      |
| `build.py`           | **Run** `python <skill folder>/build.py body.html report.html`          | § 5               |

Related: the `create-figure` skill for every figure, the `create-diagram` skill for every diagram of a mechanism: read them before
drawing the first one.

**Contents**

0. In short
1. Structure
2. Writing
3. Look
4. Figures
5. Work order

---

## 0. IN SHORT

1. **Always the same order**: title and two sentences, one section per question, Conclusion then Pour aller plus
   loin, Sources, Versions (§ 1).
2. **The message first**: in each section, and for each idea, the message in plain words, then the intuition, then
   the proof (a number, a figure), then the detail, only if what follows needs it (§ 2).
3. **Every section ends with a figure and its caption**; remarks sit beside what they concern, never at the end.
4. **Mathematics only when it helps**, always in LaTeX, never Unicode maths; numbers rather than adjectives (§ 2).
5. **Nothing said twice**: the results are in the Conclusion only, what remains to do in Pour aller plus loin only.
6. **French first, English last**: write the whole report in French, translate it when the French is final (§ 5).
7. **Never invent a reference**: cite only sources that were found and read.
8. **Build, look, publish**: `build.py`, check at phone and computer width, publish as an artifact, give me the link
   (§ 5).

---

## 1. STRUCTURE

| Part                             | Element                                 | Content                                               |
| -------------------------------- | --------------------------------------- | ----------------------------------------------------- |
| Header                           | `<header>`                              | project and date, the title, two sentences            |
| Sections                         | `<section>`                             | one per question studied, ending with a figure        |
| Conclusion, Pour aller plus loin | `<div class="closing">`, two boxes      | what each section found; what to check or do next     |
| Sources                          | `<section class="sources">`             | numbered references, when any is cited                |
| Versions                         | `<p class="versions">`                  | commits of the libraries the results were made with   |

### Header

- First line, small and grey: `Projet : <name>` on the left, the date and the FR / EN toggle on the right. The name
  links to the GitHub repository of the project when it is known, otherwise plain text.
- **The title says what the report studies**, clearly and with a little character, not only its topic:
  "Neptune : deux architectures pour le processeur latent", not "Processeur latent".
- **Two sentences** under it (`<p class="lede">`) recall the goal of the report and its content (what the sections
  are about), with the key words in bold. **No result here**, and no box: the results are in the Conclusion.

### Sections

One section per question studied:

1. **A title that carries the message** of the section, short and expressive: "Attention jointe : tout lit tout",
   "À coût presque égal", rather than "Comment fonctionne la variante attention jointe" or "Comparaison des coûts".
2. **The text, written as in § 2**: the message, the intuition, the proof citing the figure "(Fig. A)" and the
   sources, then the details that the rest needs, in an "En pratique" paragraph.
3. The figure, then its caption. **A section always ends with a figure and its caption.** When a second experiment
   is needed to answer the question, its paragraphs, figure and caption follow, in the same order.

For a report that **summarises past work** (a cleaning of the data, a set of fixes), each section opens instead with
three columns, `<div class="trio">`: the problem met, the solution put in place, and what we observe since (solved
or not, in semibold); then the figure that shows it, and its caption.

**Remarks**: a caution, an assumption, an estimate, something not verified. Never gathered at the end: each is a
short `<aside class="remark">` placed just before the paragraph, the three columns or the figure it concerns. On a
computer it sits in the right margin at that level; on a phone, just above.

### Conclusion and Pour aller plus loin

Two boxes, one under the other, each over the full width.

- **Conclusion** (`box conclusion`): what each section found, numbered, one sentence or a short paragraph per
  section. **In bold, the idea to keep**, a few words that give it at once ("le choix se fera sur la qualité des
  prévisions, pas sur le coût"), never a label such as "Coût." at the start.
- **Pour aller plus loin** (`box next`): what remains to check (the remarks of the margin may come back here) and
  the next steps already discussed, each as a sentence or a short paragraph with **the action or the decision** in
  bold.

### Sources

Whenever results rely on literature or external pages, look for sources and cite them.

- A section "Sources" below the two boxes: a numbered list, one entry per source, always in this format, each entry
  with an id (`<li id="src-1">`):
  `Author, A., Author, B., & Author, C. (Year). Title. Journal or publisher, volume(issue), pages. <DOI link>`.
- In the text, cite like Geophysical Research Letters: the first author in semibold (coloured by the style), then
  the year, linked to the entry: `(<a class="cite" href="#src-1"><strong>Hampel</strong>, 1974</a>)`; "et al."
  beyond two authors; without parentheses when the author is the subject of the sentence: "selon **Hampel** (1974)".

### Versions

Last line of the page, small: `<strong>Versions :</strong> albus 32ebf6b, shaggy 6095950`, given by
`python <auto-update skill folder>/check.py --versions` in the environment the results were made with. Two
environments (e.g. a run on another cluster) → one line each, saying which. Not needed when no code was run.

---

## 2. WRITING

**Each idea, in this order:**

| Step         | What                                                                   | Example                                            |
| ------------ | ---------------------------------------------------------------------- | -------------------------------------------------- |
| Message      | what to keep, in one sentence, without any symbol                      | "Le processeur donne un ensemble de prévisions."   |
| Intuition    | why or how, in simple words or an image                                | "Deux bruits, deux prévisions."                    |
| Proof        | the number or the figure that shows it                                 | "1,05 fois plus cher (Fig. C)."                    |
| En pratique  | the mechanism, the maths, the settings: a short paragraph, only if needed | "32 valeurs de bruit modulent chaque normalisation." |

- **Keep only what the reader needs at that point** to understand what follows or to take the decision of the
  report. Anything else goes down into "En pratique", or out.
- **Paragraphs**: one idea each, but one idea may take several sentences: group them rather than stacking
  two-line paragraphs. "En pratique" paragraphs open with these words in bold.
- **Bold**: the idea to keep or a concept named for the first time, a few words, never a whole paragraph.
  **Coral** (`<em>`): the one or two words that carry the message of a section.
- **Mathematics**: only when a formula says something the words do not; the message never needs it. When used,
  always in LaTeX, the same everywhere: `\( … \)` inline and `\[ … \]` apart, rendered by MathJax (`build.py` loads
  it), e.g. `\(\sigma/\tau\)`, `\(D \times N\)`; never Unicode maths (ρ₀, σ/τ typed as characters) and never `<sub>`.
  Follow the notation of my slides (`template.md` on the template branch of VikVador/Talks): plain variables `x, y, c`, time as a subscript
  `x_t`, windows `x_{1:L}`, a learned distribution `p_\theta`, conditioning `\mid`. Plain numbers with their unit
  stay in the text: "2,8 fois", "4 h", "18 432 tokens".
- **Spell out every variable and acronym** at its first use, in the text and in the figures: "la température de
  surface de la mer (SST)", so that a reader from outside the project understands.
- Simple words, numbers rather than adjectives. Say what was measured and what was estimated; give your own
  conclusions, not only the results.
- Small tables only for exact numbers (4 to 5 columns, short cells, inside `<div class="table-wrap">`); never a
  table where a figure works. One question, one figure: an exploratory sweep stays out of the report.
- **Two languages, French by default.** Every text exists in French and in English, as sibling elements marked
  `lang="fr"` and `lang="en"`: a whole block (`<p lang="fr">`, `<ul lang="en">`), or a `<span>` inside a caption,
  a legend or the header. The toggle shows one language at a time. The English version is written last (§ 5), with
  its own number format ("18,432", "2.5 times"). Figures are made once, in English.

---

## 3. LOOK

Fixed by `style.css`, in the reef palette of my slides, one job per colour:

| Colour                        | Job                                                                       |
| ----------------------------- | ------------------------------------------------------------------------- |
| Navy `#1d3557`                | titles, bold, the Fig. letters                                            |
| Coral `#e07a5f`               | the 1 or 2 message words of a section (`<em>`); the Pour aller plus loin box |
| Blue `#457b9d`                | mathematics, links, cited authors, list markers; the Conclusion box; never for emphasis |
| Slate `#2a2f3a`               | the text; grey `#555b66` for captions, the two header sentences, details |
| Slate grey `#5b6472`          | remarks (red is kept for problems)                                        |

- **One typeface everywhere: Inter**; a monospace only for code and file names. **Two weights**: regular and
  semibold. No italic, no capitals for emphasis, no letter-spacing.
- **Four sizes**: title 34 px, section 20 px, text 16 px; captions, tables, remarks and header details 14 px.
- **Off-white page (`#f7f7f5`)** whatever the theme of the reader (no dark mode). Figures keep a white background;
  the page blends it into its own colour. No frame or background around the figures. The curves named in a caption
  keep the colours of `plot_style.py`.
- **Text justified and hyphenated** in its language: paragraphs, bullets, captions, remarks.
- **Boxes**: only the two closing ones, framed, without a tint, one under the other over the full width.
- **Width**: one column of 960 px; every figure takes exactly that width. Space between paragraphs (20 px), above
  each figure (28 px), and between a section title and its first paragraph (22 px).

---

## 4. FIGURES

- Matplotlib figures following the `create-figure` skill (and its `plot_style.py`), saved as PNG at `dpi=110` or more,
  without a title of their own: `<figure><div class="plate"><img …></div><figcaption>…</figcaption></figure>`.
- **Captions**: the style adds "Fig. A.", "Fig. B.", … in order. Then two parts:
  1. what the figure shows, in a few words, in semibold (it plays the role of the figure title);
  2. how to read it: the x axis, the y axis, and what each curve is, the word naming a curve in semibold and in the
     colour of that curve: `<span class="blue">entraînement</span>` (classes `blue`, `amber`, `green`, `vermilion`,
     `grey`, the colours of `plot_style.py`).
- **Diagrams and animations** of a mechanism or an architecture follow the `create-diagram` skill: inline SVG drawn
  with its `diagram.js` (copied next to the body, inlined by `build.py`), inside `<div class="plate">`, with a
  caption like any figure (lettered too).

---

## 5. WORK ORDER

1. Write the analysis script and the figures in the analysis folder of the project, never in the repository (named in
   the `CLAUDE.md` of the project; none named → ask me once where, then reuse it).
2. Copy `body-template.html` next to them and write the whole report **in French only**, as in § 2: gather the
   data, run the analysis, draw the figures (in English), write each section message first. Leave the `lang="en"`
   elements empty for now.
3. Read the French draft once more as the reader: does each section give its message in its first sentences? Is
   every sentence needed at that point? Is anything said twice? Fix it, then **translate into English as the last
   step**: fill every `lang="en"` element next to its French one; nothing else changes.
4. `python <skill folder>/build.py body.html report.html`.
5. When a browser is available, look at the page at phone width (about 400 px) and at computer width (about
   1440 px), in both languages: no horizontal scroll, remarks in place, the two boxes one under the other.
6. Publish it as an artifact (at most 16 MB: `build.py` prints the size; above, lower the dpi of the figures or split
   the report); keep the same file path to update the same artifact.
7. Reply in French with the link and the points of the Conclusion.
