---
name: presentation
description: Use when the user asks for slides, a deck or a presentation, typically for a meeting with a supervisor or a team, made from the results of the current session or project. Builds a Marp Markdown deck in the user's private repository VikVador/slide-template, following its template and its brief, builds it to HTML and PDF, and once approved publishes the PDF in the public repository VikVador/Talks. For figures in the deck, also read the figure skill; for diagrams and animations of a mechanism, the animation skill.
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Presentation: a meeting deck from my template,
     ┌─┴───┴─┐       so that I think and discuss instead of formatting.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# PRESENTATION

This skill is the **procedure**. The details live in the repository
[VikVador/slide-template](https://github.com/VikVador/slide-template) (private: it holds a licensed font): `template.md` shows every rule on its own slide,
in a yellow box; `docs/skill-brief.md` holds the workflow and the decisions behind it. **Those two files win** over
anything you remember: never change the design or the rules without asking me. Only the PDFs go public, in
[VikVador/Talks](https://github.com/VikVador/Talks).

**Contents**

1. Get the repository
2. Ask first
3. Write the deck
4. Build and check
5. Finish and publish

---

## 1. GET THE REPOSITORY

1. Find a clone: on my Mac it is `~/Desktop/victor-slides`; elsewhere, look for a folder whose remote is
   `VikVador/slide-template`. None → `gh repo clone VikVador/slide-template ~/slide-template`.
2. `git pull` on `main`, then `npm install` if `node_modules/` is missing.
3. **Read `template.md` and `docs/skill-brief.md` in full** before writing a single slide, every time.

---

## 2. ASK FIRST

One message, before writing anything, with the questions still open and a proposed outline:

| Ask                                  | Rule                                                                                    |
| ------------------------------------ | --------------------------------------------------------------------------------------- |
| Which project recaps                 | **Always ask**: NYU (its 3 videos), ULiège (its 2 videos), both or none. Never a subset. |
| Meeting name and date                | Gives the folder `talks/YYYY-MM-DD-meeting/` (e.g. `2026-11-12-weekly-gilles`).          |
| Palette                              | Do not ask. `theme: reef`, unless I name `slate`, `liege` or `violet`.                   |
| Content                              | What to show, if not given: results, problems, choices to make together.                |
| Faces of colleagues                  | Never add any unless I ask, and then only the people I name.                            |

**The outline**: from the results of the session (figures made, numbers, problems met, open choices), one line per
slide, grouped by project, each result slide with its box (`key` result, `alert` problem, `question` choice).
**Never invent a result, a number or a citation**: what I did not give becomes a visible placeholder, and you say so.

---

## 3. WRITE THE DECK

- Copy `template.md` into `talks/YYYY-MM-DD-meeting/talk.md`, keep its front matter (change `theme` and `title`)
  and its **title slide exactly**, then delete every other slide you do not use.
- **Remove every yellow `rule` box and every `guides` div**: they exist only in the template.
- Paths from a talk: shared assets are `../../media/…` and `../../team/…`; the deck's own figures go in
  `talks/YYYY-MM-DD-meeting/figures/` and are linked as `figures/…`.
- Structure, once per project: recap videos (if asked) → `## Progress` → one slide per result, each with exactly
  one box → `## Summary` (every `key` left, every `alert` and open `question` right) → dark `## What's next`.
  No separate issues slide, no final discussion slide. About 6 to 12 slides per project.
- Every slide follows its rule in the template: one idea, text on the text line, colours with one job each,
  maths in LaTeX with the notation slides, one centred figure with a caption, credits in one footnote.
  No speaker notes, no logos, English only.
- **Figures**: what goes *in* a figure follows the `figure` skill; a diagram or an animation of a mechanism, the
  `animation` skill. Read them before making the first one. The template only says where it goes.

---

## 4. BUILD AND CHECK

1. `bash scripts/build.sh talks/YYYY-MM-DD-meeting/talk.md` (add `--pdf` for a PDF).
2. Look at it: serve the repository root (`python3 -m http.server 8765`) and open
   `http://127.0.0.1:8765/talks/YYYY-MM-DD-meeting/talk.html`. A snapshot of the file cannot load relative media.
   Check that the videos play, the figures and faces load, the maths renders, and no text overflows a slide.
3. Show me the deck (a few slides) and fix what I ask.

---

## 5. FINISH AND PUBLISH

1. Add one row to the *Talks* table of `README.md`, newest first:
   `| 2026-11-12 | Weekly, Gilles Louppe | NYU, ULiège | [talk](talks/2026-11-12-weekly-gilles/) |`.
2. Commit on `main` (no branch per talk) with the deck, its figures and the README; built HTML and PDF are ignored.
   Push when I approve the deck.
3. **Publish, only when I approve**: `bash scripts/build.sh talks/YYYY-MM-DD-meeting/talk.md --pdf`, check that the
   PDF uses Arial Nova (`pdffonts`), then in a clone of `VikVador/Talks` (on my Mac `~/Desktop/talks`)
   copy it to `talks/YYYY-MM-DD-meeting.pdf`, add one row to its README table, newest first
   (`| 2026-11-12 | Weekly meeting with Gilles Louppe | [PDF](talks/2026-11-12-weekly-gilles.pdf) |`),
   commit and push. **Only the PDF goes public**: never the Markdown, the fonts, the media or the figures' sources.
4. If the theme or the template had to change, ask me first, then tag the repository `theme-vN`.
