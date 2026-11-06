---
name: auto-recap
description: "Use when my message looks dictated by voice: long (a paragraph or more), no formatting at all (no bullets, headings or code), spoken style with fillers and corrections (donc, en fait, bah, du coup, ok, so, basically). Before anything else, reply with a very short recap of what you understood of the request, then start working at once. Not for short, formatted, pasted (an email, an abstract, a log) or automatic messages."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Auto recap: say back in a few lines what was
     ┌─┴───┴─┐       understood of a dictated request, then work.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# AUTO RECAP

I often dictate long requests by voice. Before working on one, show what you understood, so that I can read it while
you work and correct you at once if needed.

| File                  | Use                                                           | When                                 |
| --------------------- | ------------------------------------------------------------- | ------------------------------------ |
| `hooks/auto-recap.py` | runs by itself on every message (plugin hook), never by hand  | adds a reminder to a dictated message |

---

## 0. IN SHORT

1. **Recap first**: what you understood of the request, never what you plan to do, in the format of § 2.
2. **Then work at once**, in the same turn: the recap never waits for a confirmation. Ask a question only if the
   request cannot be started without the answer.
3. **Same language as my message**, very short: it is read in a few seconds.
4. **First of the first message**: when other skills also ask to speak first (phone question, "Quoi de neuf", the
   questions of a skill), the recap comes before them, in the same message.

---

## 1. WHEN

A dictated message, with or without the hook:

| Sign          | What the hook measures                                                                |
| ------------- | ------------------------------------------------------------------------------------- |
| Long          | 600 characters or more                                                                |
| Not formatted | no bullet, heading, numbered item, quote or code block; at most 3 line breaks         |
| Spoken        | 3 filler words or more (donc, en fait, bah, ben, genre, voilà, du coup, euh, ok, so)  |

Not for short messages, formatted ones, pasted documents (an email, an abstract, a log), slash commands, or
scheduled and automatic messages (they start with `<`).

---

## 2. THE RECAP

```markdown
**<A title, a few words>** (or "Ce que j'ai compris")

---
<2 to 4 plain lines: what is asked, and why if it was said.>

---
- <one short bullet per distinct thing asked or constraint given: what to keep, what not to do>
```

Then the work. The final answer follows the usual rules (the compact style too when the compact answer mode of the
`cluster-remote` skill is on).
