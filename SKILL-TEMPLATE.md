# Skill template

Every `plugins/<plugin>/skills/<name>/SKILL.md` follows this file. Copy the skeleton below, keep the sections in this
order and delete the optional ones the skill does not need. This file is not a skill: never name it `SKILL.md`.

## Conventions

| Topic        | Rule                                                                                                       |
| ------------ | ---------------------------------------------------------------------------------------------------------- |
| Front matter | `name` (= the folder name, lowercase, hyphens) and `description` only: other keys break claude.ai uploads. |
| Description  | One line, at most 600 characters, no `<` `>`, in double quotes when it contains `: `. It is the trigger:   |
|              | "Use when / before / as soon as {the situation, with the words a request would contain}", then one        |
|              | sentence on what the skill gives. Say what it is **not** for when another skill is close.                 |
| Banner       | The Claude banner, unchanged; its two text lines say "{Name}: {what it is for}".                          |
| Title        | `# NAME` in capitals, then 2 to 4 lines: what the skill is for and the one principle behind it.            |
| Voice        | English. Claude is **you**, Victor is **I / me / my**, never "the user". French only for the exact words  |
|              | to say to me, in quotes ("Quoi de neuf"). Messages to me are in my language (French unless I write in     |
|              | English).                                                                                                  |
| Style        | Imperative, present tense ("Run", "Ask me first"). The reason in one clause after ":". Bold only for the  |
|              | opening words of a rule and the number that matters. No capitals for emphasis.                            |
| Headings     | `## n. TITLE` in capitals, numbered from 0, a `---` line between them; `###` in sentence case.             |
| Sections     | A procedure skill has one `##` per step, named with a verb (ASK FIRST); a reference skill one `##` per    |
|              | topic (STORAGE).                                                                                           |
| Tables       | For 3 or more parallel items; the key in the first column; at most 5 columns. No row that continues on an |
|              | empty first cell: shorten it, or move the rest to "Good to know".                                         |
| Lists        | Numbered for ordered steps, bullets for rules, `- [ ]` only in the CHECKLIST.                              |
| Commands     | In backticks, ready to paste, placeholders `<name>`, never an escaped pipe `\|` inside a command. More     |
|              | than one line: a fenced `bash` block.                                                                      |
| Own files    | Named from the skill's folder, the "Base directory for this skill" given when the skill loads:            |
|              | `python <skill folder>/check.py`. Listed in the Files table with a verb: **Run** (a script, executed, not |
|              | read), **Read** (a reference, only when its When column says so), **Copy** (a template or an asset).      |
| Dates, facts | ISO `YYYY-MM-DD`. A measured value carries its date. An unverified fact gets **[verify]** and a row in    |
|              | OPEN QUESTIONS.                                                                                            |
| Last checked | `**Last checked: YYYY-MM-DD** (what was checked)` when the facts can change; the "Keep this file up to    |
|              | date" box only when they change within months (clusters, quotas, people).                                |
| References   | "§ 4" inside a skill, "the `create-figure` skill" across skills.                                                  |
| Size         | Target: 250 lines and 12 000 characters. Limit: 400 lines and 20 000 characters (about 5 000 tokens, what |
|              | Claude Code keeps of a skill after a compaction). Above it, move out, in this order: code longer than 20  |
|              | lines (to a script), a section only one sub-task needs (to `references/<topic>.md`), catalogues. Never    |
|              | move out IN SHORT or the rules that prevent damage or ask for my approval.                                 |
| Editing      | Only in a clone of VikVador/Claude, on a branch, through a pull request; bump `plugin.json`. Never in    |
|              | `~/.claude/plugins/`: that copy is overwritten at the next update.                                         |

## Skeleton

````markdown
---
name: <folder-name>
description: "Use when <the situation, the words of a request, hostnames, file types>. Gives <what the skill brings>. Not for <the close case that belongs to another skill>."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       <Name>: <what it is for, on at most two lines
     ┌─┴───┴─┐       of about 45 characters>.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# <NAME>

<2 to 4 lines: what this skill is for, and the one principle behind it. Nothing Claude already knows.>

**Last checked: <YYYY-MM-DD>** (<what was checked against what>).

> **Keep this file up to date.** If the date above is more than one month old, before relying on this file:
> 1. launch an agent to re-read <the sources> and check that nothing changed;
> 2. propose the changes to me, then make them in a clone of VikVador/Claude through a pull request.

| File                     | Use                                               | When                     |
| ------------------------ | ------------------------------------------------- | ------------------------ |
| `<script>.py`            | **Run** `python <skill folder>/<script>.py`       | <when>                   |
| `references/<topic>.md`  | **Read**                                          | only when <sub-task>     |
| `<template>.html`        | **Copy** next to <where>                          | <when>                   |

Related: the `<skill>` skill for <what>.

**Contents**

0. In short
1. <Section>
2. <Section>
3. Checklist

---

## 0. IN SHORT

1. **<Rule in a few words>**: <the instruction, with the number or command that matters> (§ 2).
2. **<Rule>**: <…>.

<3 to 8 items: what must hold even if nothing else in this file is read. Every "ask me first" goes here.>

---

## 1. <SECTION>

<Procedure: numbered steps, one action each, with the exact command. Reference: one table, then "Good to know".>

**Good to know**

- <A fact that is not a rule>, measured on <YYYY-MM-DD>.

---

## <n>. CHECKLIST

- [ ] <A yes / no question about the result>

---

## <n+1>. OPEN QUESTIONS

| #   | Question | Status                    |
| --- | -------- | ------------------------- |
| 1   | <…>      | **open**, <how to check>  |

---

## <n+2>. SOURCES

| Source | Link             |
| ------ | ---------------- |
| <…>    | [<site>](<url>)  |
````

Optional parts: the "Last checked" line and the box (facts that change), the Files table (helper files), the
Related line, Contents (over 100 lines), CHECKLIST (skills that produce something), OPEN QUESTIONS (any [verify]),
SOURCES.

## The first message of a session

Several skills ask to speak first. When more than one applies, in this order, in one message:

1. the recap of a dictated request (`auto-message-format`);
2. the "Quoi de neuf" (`auto-update`);
3. the questions a skill asks before working (e.g. `create-slides`, `create-message`), then the work.
