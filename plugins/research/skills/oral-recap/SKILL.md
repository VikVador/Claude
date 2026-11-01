---
name: oral-recap
description: Use when the user's message looks dictated - long, plain sentences with no formatting at all (no bullets, no headings, no code), spoken style with filler words ("donc", "en fait", "bah", "ok", "so", "basically"). Before doing anything, reply with a very short recap of what you understood of the request, then start working at once.
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Oral recap: say back in a few lines what was
     ┌─┴───┴─┐       understood of a dictated request, then work.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# ORAL RECAP

The user often dictates long requests by voice. Before working on one, show what you understood, so that they can
read it while you work and correct you at once if needed.

## When

The message is **long** (a paragraph or more) and **has no formatting**: no bullets, no headings, no numbered list,
no code block; at most a line break or two (around a pasted link). The sentences read as spoken: filler words,
repetitions, corrections on the way ("donc", "en fait", "bah", "ben", "genre", "voilà", "ok", "so", "basically").
The hook `oral-recap.py` of this plugin detects it and reminds you; the rule holds even without the hook.

Not for short messages, formatted ones, or scheduled and automatic messages.

## What

1. **First, a recap of what you understood** of the request, never of what you plan to do, in the compact style:
   - a title in bold, a few words;
   - a line `---`, then 2 to 4 lines of plain text: what is asked, and why if it was said;
   - a line `---`, then one short bullet per distinct thing asked or constraint given (what to keep, what not to do);
   - the heading "Ce que j'ai compris" (or "What I understood" in English) as the title is fine.
   Same language as the message. Very short, very simple: it is read in a few seconds.
2. **Then start working at once**, in the same turn: the recap never waits for a confirmation. Ask a question only if
   the request cannot be started without the answer.
3. The final answer follows the usual rules (compact style too when the compact answer mode is on).
