---
name: create-message
description: "Use when I want to write a message to share my progress, ask a question or ask for help with my team or a community (un message, un post, une update, partager mon avancement), usually with figures. Opens with a short list of proposed points and questions taken from the session, then writes one short structured message ready to paste on any chat platform, and a caption for each figure. Not for slides (create-slides skill) or a written report (create-report skill)."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Create message: a short project update to post,
     ┌─┴───┴─┐       with its figures and questions.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# CREATE MESSAGE

I share my progress in short, structured messages on chat platforms (Slack, Discord, …), usually with figures, and use
them to ask questions or for help. This skill proposes what to say from the session, lets me choose and complete, then
writes one message that pastes as is on any of them, and the captions I post under each figure in its thread.

Related: the `create-figure` skill for a figure to draw, the `create-slides` skill for slides.

---

## 0. IN SHORT

1. **First reply = the questions list** of § 1, in its fixed format, then stop and wait; after my answer, send the
   updated list and write only on my go.
2. **Propose, never invent**: the points and questions you propose come from the session (results, figures, problems,
   open choices); I can complete each list with "Autre", and you rewrite what I add as short as your own points.
3. **One message for every platform**, in the format of § 2: in English, clear, simple and concise.
4. **One caption per figure** (§ 3): what the figure shows, then what to read.

---

## 1. ASK FIRST: THE QUESTIONS LIST

Your first reply, before writing anything, is this list, in French, in exactly this format; then **stop and wait**.

- Options are written `` `[x]` `` (proposed) or `` `[ ]` `` in inline code: never Markdown task lists, which render the
  checked text struck through.
- Question 1: one line per project of the template branch of VikVador/Talks (`projects/*/project.yaml`, its
  `title`, with an emoji that fits it); tick the project(s) the session is about, several if needed (one section
  each). "Autre" means we work on something else: I give its name. Read the titles from a clone on `template` if
  there is one (on my Mac `~/Desktop/victor-slides`); otherwise, without cloning:
  `gh api 'repos/VikVador/Talks/contents/projects?ref=template' -q '.[].name'`, then each
  `https://raw.githubusercontent.com/VikVador/Talks/template/projects/<folder>/project.yaml`.
- Questions 2 and 3: propose every point and every question worth sharing that you find in the session, each starting
  with a **bold keyword**, one per project ticked in 1. For each, say its figure: an existing one (its file), one to
  generate (what it would show), or none. Always end with "Autre", for what I want to add.

````markdown
```text
──────────────────────────────────────────────────────────
                  GÉNÉRATION DU MESSAGE
──────────────────────────────────────────────────────────
```

Réponds seulement sur ce que tu veux changer : sans réponse, je garde les cases cochées.

**1. Projet**
- `[ ]` <title of a project of projects/> <emoji>
- `[ ]` Autre (préciser le nom) : …

**2. Points à partager**
- `[x]` **<Keyword>** : <what we share, in one sentence>.
  Figure : <existante, `<file>`> | <à générer : <what it would show>> | aucune.
- `[ ]` Autre (préciser) : …

**3. Questions et demandes d'aide**
- `[x]` **<Keyword>** : <the question, precise and short>.
  Figure : <existante, `<file>`> | <à générer : <what it would show>> | aucune.
- `[ ]` Autre (préciser) : …
````

Then:

1. An unanswered question keeps its `[x]`. Apply my answers (unticked points, my "Autre"), send the **whole updated
   list**, and ask "Es-tu d'accord avec l'ensemble des choix ?". What I add, often explained at length, becomes a point
   like yours: one sentence, its bold keyword, clear, simple and concise; keep its meaning, drop the explanation.
2. Write only after my yes. A figure to generate: draw it with the `create-figure` skill (wide, readable on a phone), save it
   next to the session's figures, and give me its path.

---

## 2. WRITE THE MESSAGE

One message, in a ```` ```text ```` block, in plain Markdown (`**bold**`, `- ` bullets): it renders the same on Slack,
Discord and most chat platforms.

```text
**[ PROJECT UPDATE | #XXX ]**

Hey @everyone 👋

**Project A | <title of the first project> <emoji>**

- <A point>, with the **key information** in bold (Fig. 1).
- <A problem or a choice>, in one sentence: **<the question, in bold>?**

**Project B | <title of the second project> <emoji>**

- …
```

- **Header**: `**[ PROJECT UPDATE | #XXX ]**`, the number left as `#XXX` for me to edit, then a blank line and
  `Hey @everyone 👋`.
- **One section per project**, in the order of question 1, named `**Project A | <title> <emoji>**`, `Project B`, …,
  a blank line after the title and a blank line between sections. No other section: questions are points like the
  others, the question itself in bold.
- **Points**: `- ` bullets, 2 to 4 per section, one sentence each, with the key information in bold (one to four words).
  English, clear, simple, concise; *we*, not *I*; numbers with their unit.
- **Figures**: numbered across the whole message (Fig. 1, Fig. 2, …), cited at the end of their point.
- Under the block, one line in French: where `@everyone` is not the mention for everyone (on Slack, `@canal`), replace it.

---

## 3. WRITE THE CAPTIONS

After the message, one ```` ```text ```` block per figure, in the order of the numbers, plain text (no Markdown), which
I post under the figure in the message's thread:

```text
Fig. 2 | Power spectral density of the temperature at 0.3 m against the wavenumber, for the simulation (grey) and the generated samples (orange), without (left) and with (right) the convolutional head. Without the head, the generated spectrum flattens into a white-noise tail at small scales; with it, it follows the simulation down to the smallest scales.
```

- **First what the figure shows**: the quantity, the axes, each curve or colour, the date or zone, the number of
  samples; **then what to read**: the one thing to notice, in one sentence.
- Then the list of the figure files to attach, in order.

---

## 4. CHECKLIST

- [ ] Did the first reply send the questions list, and did I say yes to the updated list?
- [ ] Is every point and number from the session or from me, nothing invented?
- [ ] One message, header with `#XXX`, `Hey @everyone 👋`, one section per project named Project A, B, …?
- [ ] Are the questions bold inside their points, with no separate section?
- [ ] Is every figure cited (Fig. N) and given a caption that says what it shows and what to read?
- [ ] Under 2 000 characters (the shortest limit, Discord's)?
