---
name: auto-message-format
description: "Use for every answer to me, in every session and project (the hook auto-message-format.py reminds you on each prompt), and when my message looks dictated by voice: long, no formatting, spoken style with fillers (donc, en fait, du coup, ok, so, basically). Gives the two answer formats, short and long, how to choose between them, and the recap of a dictated request. Not for the progress lines written while working, nor for the questions lists of the create-slides and create-message skills."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Auto message format: one short and one long
     ┌─┴───┴─┐       format for every answer, read in seconds.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# AUTO MESSAGE FORMAT

What you say is usually right, but I read only part of long answers. Every answer follows one of two formats, on a
computer as on a phone: the message comes first, so that reading the first section is enough, and the details sit
below, numbered, so that I can answer about one of them by its number.

| File                           | Use                                                          | When                                         |
| ------------------------------ | ------------------------------------------------------------ | -------------------------------------------- |
| `hooks/auto-message-format.py` | runs by itself on every message (plugin hook), never by hand | reminds the format; flags a dictated message |

**Contents**

0. In short
1. Short or long
2. The short format
3. The long format
4. A dictated request: the recap
5. Exceptions and order
6. Checklist

---

## 0. IN SHORT

1. **Every answer** is short or long (§ 1): short when I only need an information, long when I must understand or
   decide something.
2. **The first section is enough**: a few words in bold, then " :" and the message in 2 to 3 lines, then the state
   (§ 2, § 3).
3. **Details are numbered** (1., 2., …), what is not checked and your notes are lettered (A., B., …), and every
   question names the number or letter it is about (§ 3).
4. **A dictated request** gets the recap of § 4 first (the long format, without the state), then the work at once.
5. **Not for** the progress lines written while working, nor for the questions lists of `create-slides` and
   `create-message` (§ 5).
6. **In my language**, French unless I write in English; "détaille" from me asks for the full, normal answer.

---

## 1. SHORT OR LONG

The question is not the situation but: **must I understand or decide something?** Yes → long; no → short.

| Situation                                            | Format                                                |
| ---------------------------------------------------- | ----------------------------------------------------- |
| A question before working                            | short: the question, the minimal context, the options |
| After working                                        | long: what changed, what is left or not checked       |
| A simple question ("does X work?")                   | short                                                 |
| An explanation I asked for                           | long: a point may be a short paragraph                |
| Blocked during the work (error, approval needed)     | long: context, cause, options                         |
| Start of a session ("Quoi de neuf" of `auto-update`) | long; short when nothing changed                      |
| Background work back (CI, Slurm job, agent)          | short when it went well, long when it failed          |
| A dictated request                                   | the recap of § 4, then the work                       |

---

## 2. THE SHORT FORMAT

One section between two horizontal rules, then the question, if any.

````markdown
---

**<A few words> :** <1 to 3 lines: the answer, the information or the context of the question.>

**État :** <✅ | ⏳ | ⛔ | 💬>

---

❓ <the question> ? (<answer A> / <answer B>)
````

| State | Meaning                                           |
| ----- | ------------------------------------------------- |
| ✅    | done: nothing waits for me                        |
| ⏳    | in progress: a job, the CI or an agent still runs |
| ⛔    | blocked: nothing moves without my answer          |
| 💬    | an answer or an opinion, no work done             |

- No question → no last rule and no ❓ line.
- Example:

  ```markdown
  ---

  **CI de la PR #41 :** les 3 checks sont verts, rien à corriger.

  **État :** ✅

  ---
  ```

---

## 3. THE LONG FORMAT

````markdown
---

**<A few words> :** <2 to 3 lines: the message to keep. If I read only this, I know the essential.>

**État :** <✅ | ⏳ | ⛔ | 💬>

---

1. **<Keyword>** : <a fact, a change or a cause, in one sentence or a short paragraph>.

2. **<Keyword>** : <…>

   ```bash
   <a command, after the text of its point, when I must run or see it>
   ```

---

**A.** **Pas vérifié** : <what was not run or not checked>.

**B.** **Note** : <a remark of yours: a doubt, a risk, an idea>.

---

❓ **(1)** <the question about point 1> ? (<answer A> / <answer B>)

❓ **(B)** <the question about note B> ? (oui / non)
````

| Part       | Rule                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------- |
| Title      | a few words in bold, followed by " :" and the summary on the same line; no separate heading       |
| Summary    | 2 to 3 lines, self-sufficient; never repeated by the points                                       |
| État       | on its own line, under the summary, inside the first section: `**État :**` then one emoji         |
| Points     | numbered, a blank line between them, each opening with a **bold keyword** then " :"; any number   |
| Code       | a fenced block inside its point, after the text, when it is the content (a command, a snippet)    |
| A., B., C. | "Pas vérifié" first, then "Note": only those, and only when there is one                          |
| Questions  | one per line, `❓ **(n)**` with the number or letter it is about; about nothing listed → no number |

- **A part with nothing in it is left out, with its rule**: no lettered section without a remark, no question
  section without a question.
- **No tables, no headings, no long paths** (file names only), unless a table of exact numbers is the answer itself.
- **Bold** only for the title, the keywords and the state; never a whole sentence.
- **Never claim more than was checked**: what was not run or not verified goes to "Pas vérifié".
- Example:

  ```markdown
  ---

  **Encodeur SSS, pics de validation corrigés :** les pics de la perte de validation venaient de quelques
  salinités impossibles (> 45 PSU) en 2019–2021. Je les ai retirées, et l'entraînement repart de zéro (≈ 20 h).

  **État :** ✅

  ---

  1. **Données** : les salinités > 45 PSU deviennent des trous (NaN) dans `data/__init__.py`.

  2. **Entraînement** : `encoder-sss.yml` relancé de zéro, car les anciens poids avaient appris ces pics.

  3. **Job** : 21012345, en attente d'une RTX du labo, démarrage prévu ce soir.

  ---

  **A.** **Pas vérifié** : l'effet sur la validation, visible seulement après quelques heures d'entraînement.

  **B.** **Note** : 2023 contient peut-être les mêmes valeurs ; je ne l'ai pas regardé.

  ---

  ❓ **(1)** Je pousse la branche avec ce correctif ? (oui / non)

  ❓ **(B)** Je vérifie aussi 2023 ? (oui / non)
  ```

**Good to know**

- Leave a blank line before and after every `---`: right under a line of text, Markdown turns that line into a
  heading.
- In English, the labels become `**Status:**`, `**Not checked**` and `**Note**`.

---

## 4. A DICTATED REQUEST: THE RECAP

I often dictate long requests by voice. Before working on one, show what you understood, so that I can read it while
you work and correct you at once.

| Sign          | What the hook measures                                                               |
| ------------- | ------------------------------------------------------------------------------------ |
| Long          | 600 characters or more                                                               |
| Not formatted | no bullet, heading, numbered item, quote or code block; at most 3 line breaks        |
| Spoken        | 3 filler words or more (donc, en fait, bah, ben, genre, voilà, du coup, euh, ok, so) |

Not for short messages, formatted ones, pasted documents (an email, an abstract, a log), slash commands, or
scheduled and automatic messages (they start with `<`).

1. **The recap is the long format of § 3 without the state**: its purpose is to say what you understood, never what
   you plan to do.
   - Title and summary: the request in a few words, then what is asked, and why if it was said.
   - Points: one per distinct thing asked or constraint given (what to keep, what not to do).
   - A., B.: only what you are unsure you understood.
   - Questions: only if the request cannot be started without the answer.
2. **Then work at once**, in the same turn: the recap never waits for a confirmation.
3. The answer at the end of the work follows § 2 or § 3, as any other.

---

## 5. EXCEPTIONS AND ORDER

**Not formatted**

- The progress lines written while working ("Je lance les tests."): one plain line, already short.
- The questions lists of `create-slides` and `create-message`, and the message and captions `create-message` writes:
  they keep their own fixed formats.
- A deliverable inside the answer (a drafted text, a file content): its own format, inside one of the points.

**The first message of a session**: when several skills ask to speak first, in this order, in one message: the
recap of a dictated request (§ 4), the "Quoi de neuf" of `auto-update`, the questions a skill asks before working,
then the work.

---

## 6. CHECKLIST

- [ ] Is the answer short or long by the question of § 1?
- [ ] Does the first section give the message alone: bold title, " :", 2 to 3 lines, then `**État :**`?
- [ ] Are the points numbered with a blank line between them, each with a bold keyword?
- [ ] Are the unchecked things and notes lettered A., B., and left out when there are none?
- [ ] Does every question start with ❓ and name the number or letter it is about?
- [ ] Is there a blank line around every `---`, and no empty part left with its rule?
