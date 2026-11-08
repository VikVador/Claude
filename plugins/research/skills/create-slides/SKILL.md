---
name: create-slides
description: "Use when I ask for slides, a deck, a talk or a presentation (diapos, présentation, slides pour la réunion), for a progress meeting or a talk to people who do not know my work, built from the session or a project; also to change, rebuild or publish one of my talks. Opens with a fixed list of questions, builds the deck from the template branch of my Marp repository, drafts it as a private artifact and publishes it on GitHub Pages only if asked. Use it instead of PowerPoint or generic slide tools unless a .pptx file is asked for."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Create slides: a talk from my template,
     ┌─┴───┴─┐       so that I think and discuss instead of formatting.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# CREATE SLIDES

This skill is the **procedure**: the questions, the draft, the checks, the publication. The **slide rules** are in
`template.md` of the template, one per slide in a yellow box: they win over anything you remember, and never change
the design or the rules without asking me. The same steps make a progress-meeting deck or a talk to people who do not
know my work: every part of the deck is an option, chosen in a fixed list of questions before any slide.

| Branch of [VikVador/Talks](https://github.com/VikVador/Talks) | Holds |
| -------- | ----- |
| `template` | everything to make a talk: `template.md`, the theme, `projects/` (recap videos and `project.yaml`), `media/` (title animation), `logos/`, `team/` (faces and `people.yaml`), `animations/`, the scripts; the local drafts in `talks/`, ignored by git |
| `main` | only the published talks, `talks/YYYY-MM-DD-name/` (`talk.md` and `figures/`), the shared files they use (title animation, recap videos, logos, faces) at the same paths, and the README list; GitHub Pages builds them with the theme of `template` |

Related: the `create-figure` skill for what goes in a figure and its size on a slide, the `create-diagram` skill for a
diagram of a mechanism.

**Contents**

0. In short
1. Get the template
2. Ask first: the questions list
3. Write the deck
4. Check the figures
5. Draft as an artifact, iterate
6. Publish (only if asked)
7. Checklist

---

## 0. IN SHORT

1. **The template branch**: pull it, read `template.md` in full before any slide (§ 1).
2. **First reply = the questions list**, in its fixed format, then stop and wait; after my answer, send the updated
   list and draft only on my go (§ 2).
3. **Never invent** a result, a number or a citation: a visible placeholder instead, and say so.
4. **One experiment = an analysis slide, then a result slide** (figure as large as possible, caption, one box) (§ 3).
5. **Figures drawn for the slide** (about 1080 × 350 px), then **one agent reviews only the figures** (§ 4).
6. **Draft as a private artifact**, iterate at the same link (§ 5); **publish only if question 10 says yes**, with
   `scripts/publish.sh` (§ 6). Not published → the talk stays an artifact, nothing goes to GitHub.

---

## 1. GET THE TEMPLATE

1. Find a clone of `VikVador/Talks` on the branch `template`: on my Mac `~/Desktop/victor-slides`; elsewhere, a
   folder whose remote is `VikVador/Talks`. None → `gh repo clone VikVador/Talks ~/talks -- -b template`.
2. `git switch template && git pull`, then `npm install` if `node_modules/` is missing.
3. **Read `template.md` in full** before writing a single slide, every time: its slides are the rules, its last slide
   draws the structure of a deck.
4. List the projects: one folder per project in `projects/`, each with a `project.yaml` (`title`, `university`,
   `logo`, `paper`, `videos` in order with their `stills`). Question 4 offers exactly these, nothing hard-coded.

---

## 2. ASK FIRST: THE QUESTIONS LIST

Your first reply, before writing anything, is this list, in French, in exactly this format; then **stop and wait**.
Read my request first: what it already answers gets its `[x]`; everything else gets its default.

- Options are written `` `[x]` `` (chosen) or `` `[ ]` `` in inline code: never Markdown task lists (`- [x]`),
  which render the checked text struck through.
- Every point you propose (Progress, experiments, What's next) starts with a **bold keyword**, so I can cite it.
- The points of questions 5, 6 and 7 come from the session: figures made, numbers, problems met, open choices.
- Question 4 lists one line per folder of `projects/` (its `title`, `university`); question 9 has one line
  "Pour le projet …" per project selected in question 4, and none if no project is selected.

````markdown
```text
──────────────────────────────────────────────────────────
                   GÉNÉRATION DU TALK
──────────────────────────────────────────────────────────
```

Réponds seulement sur ce que tu veux changer : sans réponse, je garde les cases cochées.

**1. Titre**
- `[x]` Le titre de ma thèse
- `[ ]` Nouveau titre à proposer

**2. Slide d'introduction**
- `[x]` Avec tout le monde
- `[ ]` Moi seul

**3. Palette**
- `[x]` reef
- `[ ]` slate
- `[ ]` liege
- `[ ]` violet

**4. Récap de projet**
- `[ ]` <title of a project of projects/> (<university>)
- `[ ]` Nouvelle slide de projet (préciser le nom et l'université)
- `[x]` Aucun projet (seulement Progress s'il existe, ou directement les expériences)

**5. Progress**
- `[x]` Faire une slide Progress, avec ces points :
  - `[x]` **<Keyword>** : <what we worked on, in a few words>.
- `[ ]` Pas de slide Progress

**6. Expériences**
- `[x]` **<Idea>** : montrer que <the result>. Figure : <what it shows>. Boîte : <Key result | Problem | Choice>.

**7. What's next**
- `[x]` Utiliser une slide What's next, avec ces points :
  - `[x]` **<Keyword>** : <a direction of the work>.
- `[ ]` Pas de What's next

**8. Sources**
- `[x]` Utiliser une slide Sources
- `[ ]` Pas de Sources

**9. Visages des collègues**
- `[x]` Ne citer personne
- `[ ]` Citer des collègues :
  - Pour le projet <project selected in 4> : …

**10. Rendre cette présentation publique ?**
- `[ ]` Oui (préciser le nom du talk)
- `[x]` Non
````

Then:

1. An unanswered question keeps its `[x]`. Apply my answers, send the **whole updated list**, and ask
   "Es-tu d'accord avec l'ensemble des choix ?".
2. Draft only after my yes. A new title or a new project without its name or university: ask, never guess.
3. Faces only of the people I name. The talk folder is `talks/YYYY-MM-DD-<short name>/`, from today's date and
   the title or project.

---

## 3. WRITE THE DECK

- Copy `template.md` into `talks/YYYY-MM-DD-<name>/talk.md`, keep its front matter (set `theme` and `title`) and
  the title slide chosen in question 2, exactly, with the credit of the animation (only the title text changes, if
  question 1 says so). Delete every other slide you do not use.
- **Remove every yellow `rule` box, every `guides` div and every `<!-- RULE … -->` comment**: Marp would turn the
  comments into speaker notes, and `publish.sh` refuses a deck that still has them.
- Paths from a talk: shared files as `../../media/…`, `../../projects/…`, `../../logos/…`, `../../team/…`; the talk's
  own figures in `talks/…/figures/`, linked as `figures/…`. These paths are the same on `main`.
- Structure (the last slide of the template draws it): title → for each project, its project slide and, for a
  project of `projects/`, all its recap videos in the order of `videos` → Progress → the experiments → Summary →
  What's next; then Sources. No project: no project slide.
- **Each experiment**: an **analysis** slide (`## name of the experiment`, then what we did: question, setup, the
  numbers that define it, no box), then a **result** slide (class `result`: the figure, the caption starting with
  **Figure A.**, **B.**, … in slide order, exactly one one-line box). Add an explanation slide only when the result
  needs a why that is not a figure.
- **Boxes** say what the figure means for us: check each one against its figure, never claim more than it shows.
- **Summary**: every Key result, every Problem, every Choice, one line each, in three columns (the third only if
  there is a choice). **Sources**: every library used (name, use, GitHub link), then the sources not credited in a
  footnote; a project paper from its `project.yaml`.
- Every slide follows its rule in the template: one idea, *we* not *I*, text always justified (the theme does it),
  colours with one job each, maths in LaTeX with the notation slides, credits in one footnote, no speaker notes,
  English only.

---

## 4. CHECK THE FIGURES

1. **Draw every result figure for its room on the slide**: about **1080 × 350 px** under a one-line caption and a
   one-line box, so `figsize` about 9.8 × 3.2 in, PNG at dpi 256 (the `create-figure` skill, § 2). One figure per message:
   never a multi-row figure shrunk to fit, never "top row / bottom row" in the text.
2. `bash scripts/build.sh talks/<talk>/talk.md`, serve the repository root (`python3 -m http.server 8765`), open
   `http://127.0.0.1:8765/talks/<talk>/talk.html` and look at every slide: nothing overflows, every box ends at the
   same height, the videos play, the maths renders.
3. **Then launch one agent for the figures only**: give it the PNGs of `figures/` and a screenshot of each result
   slide, and ask it to list, per figure, legends or labels drawn over the data, overlapping or cut text, ticks
   unreadable at the size shown, and a figure that leaves the slide half empty. Nothing else.
4. Fix what it finds (redraw with the `create-figure` skill), rebuild, and only then show me the draft.

---

## 5. DRAFT AS AN ARTIFACT, ITERATE

1. Stage it: `bash scripts/artifact.sh talks/<talk>/talk.md OUTDIR`, with `OUTDIR` an **absolute** folder of your
   scratchpad, e.g. `<scratchpad>/talk-<talk>` (the script empties it first).
2. **Publish it as an artifact** (private): `OUTDIR/index.html` as the page, every other file of `OUTDIR` in `files`
   under its path inside `OUTDIR`. Give me the link.
3. **Iterate with me on that artifact**: after each change, rebuild, stage into the same `OUTDIR` and publish the same
   file path, so the link stays the same.
4. **Never commit a talk on `template`**: git ignores `talks/` there. A private talk lives as its artifact only; a PDF
   (`bash scripts/build.sh talks/<talk>/talk.md --pdf`, each recap video becomes its stills) only if I ask for one.

---

## 6. PUBLISH (ONLY IF ASKED)

Only if question 10 says yes (or I ask later), once the deck is approved:

1. From the clone on `template`: `bash scripts/publish.sh talks/<talk> "<Talk name>"`, with the name I gave. It
   copies `talk.md`, `figures/` and every shared file the talk uses to `main` at the same paths, adds
   `- YYYY-MM-DD: [<Talk name>](<page>)` at the top of the README list, commits and pushes `main`: no branch, no pull
   request.
2. The workflow `Pages` of `main` builds the talk with the theme of `template` (about a minute): check it with
   `gh run list -R VikVador/Talks -L 1`, open the page and look at it.
3. Give me the link of the page: `https://vikvador.github.io/Talks/talks/<talk>/talk.html`.

To change the template, the theme, the projects or the scripts: ask me first, then commit on `template`. Every
published talk is rebuilt with the new theme at the next push on `main`: look at them after a change of the theme.

---

## 7. CHECKLIST

- [ ] Did the first reply send the questions list in its fixed format, and did I say yes to the updated list?
- [ ] Is every result, number and citation from the session or from me, with placeholders for the rest?
- [ ] Is every experiment an analysis slide then a result slide, with one box checked against its figure?
- [ ] Do the figures fill their room, with captions labelled Figure A, B, … and boxes ending at the same height?
- [ ] Did one agent review the figures only, and were its findings fixed?
- [ ] Are the rule boxes, guides and RULE comments gone, and do the Summary and Sources collect what they should?
- [ ] Is the draft a private artifact, and did anything go to `main` only if question 10 said yes?
