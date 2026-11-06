---
name: presentation
description: "Use when I ask for slides, a deck, a talk or a presentation (diapos, présentation, slides pour la réunion), typically for a meeting with a supervisor or the team, built from the results of the session or a project; also to change, rebuild or publish one of my talks. Builds it from my Marp template in VikVador/Talks-template, drafts it as a private artifact to iterate on, and publishes the PDF to VikVador/Talks only when asked. Use it instead of PowerPoint or generic slide-deck tools unless a .pptx file is asked for."
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

This skill is the **procedure**. Two repositories:

| Repository | Visibility | Holds |
| ---------- | ---------- | ----- |
| [VikVador/Talks-template](https://github.com/VikVador/Talks-template) | private (licensed font) | **every resource to make a deck**: the template, the palettes, the recap videos, the team photos, the build scripts, and the sources of every talk |
| [VikVador/Talks](https://github.com/VikVador/Talks) | public | the published talks: one folder per talk with its PDF and its figures, listed in the README |

In Talks-template, `template.md` shows every rule on its own slide, in a yellow box, and `docs/skill-brief.md` holds
the workflow and the decisions behind it. **Those two files win** over anything you remember: never change the
design or the rules without asking me. For my decks this skill replaces PowerPoint and the generic slide-deck tools
(unless I ask for a `.pptx` file).

Related: the `figure` skill for what goes in a figure, the `diagram` skill for a diagram of a mechanism.

**Contents**

0. In short
1. Get the resources
2. Ask first
3. Write the deck
4. Draft as an artifact, iterate
5. Publish in Talks (only when I ask)

---

## 0. IN SHORT

1. **Resources from Talks-template**: clone or pull it, read `template.md` and `docs/skill-brief.md` in full (§ 1).
2. **Ask first, then wait**: project recap (which one) and palette (`reef`?), every time unless I already said;
   the meeting and the content if missing; an outline (§ 2).
3. **Never invent** a result, a number or a citation: a visible placeholder instead, and say so.
4. **Draft as a private artifact** and iterate on it with me at the same link (§ 4).
5. **Publish in Talks only when I ask**: the PDF and the talk's figures, nothing else (§ 5).

---

## 1. GET THE RESOURCES

1. Find a clone of Talks-template: on my Mac it is `~/Desktop/victor-slides`; elsewhere, look for a folder whose
   remote is `VikVador/Talks-template`. None → `gh repo clone VikVador/Talks-template ~/talks-template`.
2. `git pull` on `main`, then `npm install` if `node_modules/` is missing.
3. **Read `template.md` and `docs/skill-brief.md` in full** before writing a single slide, every time.

| Path                           | What                                                                                  |
| ------------------------------ | ------------------------------------------------------------------------------------- |
| `template.md`                  | The template: each slide shows one rule in its yellow box.                            |
| `palettes.md`                  | The four palettes side by side: `reef` (default), `slate`, `liege`, `violet`.         |
| `docs/skill-brief.md`          | The workflow and the decisions behind this skill.                                     |
| `theme/`                       | `base.css`, one CSS per palette, Arial Nova (licensed: never copy it to Talks), `video-controls.js`. |
| `media/title/`, `media/recap/` | Title-slide video; project recap videos and posters, NYU (3) and ULiège (2).          |
| `animations/`                  | HTML sources of the recap videos and their 4K render script (see its README).         |
| `team/`                        | `people.yaml` (name, university, team, photo) and the photos.                         |
| `talks/YYYY-MM-DD-meeting/`    | One folder per talk: `talk.md` + `figures/` (its figures and animations).             |
| `scripts/build.sh`             | Build a deck to HTML (videos get play/pause and a seek bar) or PDF (`--pdf`).         |
| `scripts/artifact.sh`          | Stage a deck as a self-contained folder to publish as an artifact.                    |

---

## 2. ASK FIRST

One message in French, before writing anything, then **stop and wait for my answers**. **Ask the first two questions
every time, unless my request already answers them**:

1. **Project recap?** Should the deck open with a project recap, and if so which one: NYU (its 3 videos), ULiège
   (its 2 videos) or both. Yes → the recap videos of each chosen project, never a subset. No → no recap slides:
   each project starts directly with `## Progress`, then the results.
2. **Palette?** "Default palette, `reef`?" Yes → `theme: reef`. No → ask which one among `slate`, `liege` and
   `violet` (offer to show `palettes.md`, built to HTML).
3. **Meeting name and date**, if not given: they name the folder `talks/YYYY-MM-DD-meeting/`
   (e.g. `2026-11-12-weekly-gilles`).
4. **Content**, if not given: what to show, results, problems, choices to make together.

Never add colleagues' faces unless I ask, and then only the people I name.

In the same message, **propose the outline**: from the results of the session (figures made, numbers, problems
met, open choices), one line per slide, grouped by project, each result slide with its box (`key` result, `alert`
problem, `question` choice). **Never invent a result, a number or a citation**: what I did not give becomes a visible
placeholder, and you say so.

---

## 3. WRITE THE DECK

- Copy `template.md` into `talks/YYYY-MM-DD-meeting/talk.md`, keep its front matter (set `theme` and `title`)
  and its **title slide exactly** (only its paths change, see below), then delete every other slide you do not use.
- **Remove every yellow `rule` box, every `guides` div and every `<!-- RULE … -->` comment**: they exist only in
  the template, and Marp would turn the comments into speaker notes.
- Paths from a talk: rewrite every `media/…` and `team/…` copied from the template (title video and poster
  included) to `../../media/…` and `../../team/…`; the talk's own figures and animations go
  in `talks/YYYY-MM-DD-meeting/figures/` and are linked as `figures/…`.
- Structure, once per project: recap videos (if asked) → `## Progress` → one slide per result, each with exactly
  one box → `## Summary` (every `key` left, every `alert` and open `question` right) → dark `## What's next`.
  No separate issues slide, no final discussion slide. About 6 to 12 slides per project.
- Every slide follows its rule in the template: one idea, text on the text line, colours with one job each,
  maths in LaTeX with the notation slides, one centred figure with a caption, credits in one footnote.
  No speaker notes, no logos, English only.
- **Figures**: what goes *in* a figure follows the `figure` skill; a diagram or an animation of a mechanism, the
  `diagram` skill. Read them before making the first one. The template only says where it goes.

---

## 4. DRAFT AS AN ARTIFACT, ITERATE

1. Build and check: `bash scripts/build.sh talks/YYYY-MM-DD-meeting/talk.md`, then serve the repository root
   (`python3 -m http.server 8765`) and open `http://127.0.0.1:8765/talks/YYYY-MM-DD-meeting/talk.html`: the videos
   play, the figures and faces load, the maths renders, no text overflows a slide.
2. Stage it: `bash scripts/artifact.sh talks/YYYY-MM-DD-meeting/talk.md OUTDIR`, with `OUTDIR` an **absolute** path
   to a folder of your scratchpad, e.g. `<scratchpad>/talk-2026-11-12-weekly-gilles` (the script empties it first).
3. **Publish it as an artifact** (private): `OUTDIR/index.html` as the page, and every other file of `OUTDIR` in
   `files`, under its path inside `OUTDIR` (`media/…`, `theme/fonts/…`, `figures/…`). Give me the link.
4. **Iterate with me on that artifact**: after each change, rebuild, stage again into the same `OUTDIR` and publish
   the same file path, so the link stays the same. The artifact holds the licensed font: it stays private; to show
   the deck to someone, send the PDF.
5. When I approve the deck, commit it on `main` of Talks-template (the deck and its `figures/`; built HTML and PDF
   are ignored; no branch per talk) and push.

---

## 5. PUBLISH IN TALKS (ONLY WHEN I ASK)

When I ask to publish or deploy the talk publicly:

1. `bash scripts/build.sh talks/YYYY-MM-DD-meeting/talk.md --pdf` and check that the PDF uses Arial Nova
   (`pdffonts`).
2. In a clone of `VikVador/Talks` (on my Mac `~/Desktop/talks`), create the folder `talks/YYYY-MM-DD-meeting/` with
   - the PDF, named `YYYY-MM-DD-meeting.pdf`;
   - `figures/`: the figures and animations made for this talk (a copy of its `figures/` in Talks-template).

   **Nothing else goes public**: never the Markdown, the fonts, the shared media (title and recap videos) or the
   team photos as files.
3. Add one row at the top of the README table (keep the invisible spacer images in its header; the first talk replaces
   the empty row `| | | |`):
   `| 2026-11-12 | [Weekly meeting with Gilles Louppe](talks/2026-11-12-weekly-gilles/) | [PDF](talks/2026-11-12-weekly-gilles/2026-11-12-weekly-gilles.pdf) |`
4. Commit, push, and give me the links to the folder and to the PDF.

If the theme or the template had to change, ask me first, then tag Talks-template `theme-vN`.
