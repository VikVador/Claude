---
name: newsletter-university
description: "Use when a scheduled task or I ask to prepare and send the weekly university newsletter (newsletter de l'université, newsletter hebdomadaire, résumé de la semaine). Reads the week's broadcast emails of a university mailbox and a list of seminar and workshop agendas, keeps what matches my research, renders the light HTML email and sends it with the Resend connector to the subscribers. Not for the daily paper digest (newsletter-papers skill)."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Newsletter university: the week's events,
     ┌─┴───┴─┐       seminars and deadlines, in one short email.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# NEWSLETTER UNIVERSITY

Every week, one email sums up what is coming: deadlines, seminars, workshops, university events and practical news,
from the university broadcast emails of the past week and a few external agendas. You prepare **and** send it in one
run, usually alone from a scheduled task: never ask a question, take the most reasonable reading and go on. This file
says **how**; everything specific to one university (its name, mailbox, agendas, interests, section sizes) is in
`config/university.yaml`, and the recipients in `data/subscribers.yaml`.

Everything lives in `VikVador/Claude`, folder `plugins/newsletter/` (called `NL` below), always used from a fresh
clone: the installed plugin copy is stale.

| File in `NL`                | Use                                                                                    | When  |
| --------------------------- | -------------------------------------------------------------------------------------- | ----- |
| `config/university.yaml`    | **Read**: sending, identity, mailbox, sources, budget, interests, sections, lengths    | start |
| `scripts/state.py`          | **Run** `python3 scripts/state.py plan config/university.yaml`: who gets the email     | § 6   |
| `scripts/render.py`         | **Run** `python3 scripts/render.py university /tmp/contenu.json /tmp/newsletter.html`  | § 5   |
| `templates/university.html` | the structure of the email, filled by `render.py`: never edited by hand                | never |

Related: the `newsletter-papers` skill for the daily paper digest.

**Contents**

0. In short
1. Read the broadcast emails
2. Read the external sources
3. Filter
4. Sort into sections
5. Write and render
6. Send
7. When something fails
8. Checklist

---

## 0. IN SHORT

1. **Fresh clone first**: `git clone --depth 1 https://github.com/VikVador/Claude.git /tmp/newsletter-repo`, then
   read `/tmp/newsletter-repo/plugins/newsletter/config/university.yaml` in full.
2. **Period**: previous Monday 00:00 to Sunday 23:59 in `timezone`; run on another day, the last 7 full days.
3. **Only what is still to come**: a past event or a passed deadline is out.
4. **Read-only mailbox**: never move, flag, mark or delete a message (§ 1).
5. **`page_reads` page reads at most, no web search** (§ 2).
6. **Never edit the HTML by hand**: fix `contenu.json` and render again (§ 5).
7. **Recipients from `state.py plan` only**, each email sent once (§ 6).

---

## 1. READ THE BROADCAST EMAILS

- With the Microsoft 365 connector, list the messages of `mailbox.folder_id` received in the period and read each
  one **in full** (the kind of emails of `mailbox.examples`).
- For each item, note: title, date, place, speaker, registration needed or not, deadline, direct link, and a summary
  of one or two sentences.
- Merge duplicates: the same email sometimes arrives twice (through a second address).

---

## 2. READ THE EXTERNAL SOURCES

- Read `sources` in order with WebFetch until `page_reads` is spent; **no WebSearch**. On the first Monday of the
  month, replace the sources marked `monthly_swap` by `first_monday_of_month`. Follow each `note`.
- A source in error: go to the next one, without retrying.
- Follow a link to a detail page only if budget is left and the item is clearly relevant.
- Pages that give dates without the year (« jeu. 05 nov. »): infer it. Pages with one tab per semester: take the
  current one.

---

## 3. FILTER

For **seminars** and **workshops**, keep only what touches `interests` (`thesis`, `generative_ml`, `earth_science`);
in doubt, apply `when_in_doubt`. Otherwise drop the item.

---

## 4. SORT INTO SECTIONS

At most `sections.<key>` items per section; nearest first in each.

| Key         | What                                                                                                     | Format                                                         |
| ----------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `deadlines` | Anything asking an action (registration, application, submission) with a deadline within `deadline_soon_days`; never repeated elsewhere | deadline, title, 1 sentence, button (`S'inscrire`, `Voir l'appel`, `Soumettre`, …) |
| `seminars`  | Seminars and talks in my fields, from the emails or the sources                                         | date + place, title, « speaker · affiliation », 1 sentence     |
| `workshops` | Workshops, conferences, schools in my fields, with their submission or registration date; may come back every week until the deadline (a wanted reminder) | deadline (or event dates) + place, title, organiser, 2 sentences max |
| `events`    | University trainings, days, webinars, contests useful to a PhD student (career, funding, doctorate), and the campus well-being actions of `university.events_senders` (blood drives, health) | date + place, title, 2 sentences max |
| `brief`     | Culture, city, public lectures, campus life                                                              | date + place, title, 1 sentence                                |
| `infos`     | Routine notices (HPC, maintenance, limits), calls and grants with a later deadline, admin                | category (`HPC`, `Recherche`, `Admin`, …), title, 1 sentence   |

**Form**: in `sending.language`, neutral tone, short sentences, no emoji. Dates `12 nov.`, `26–27 nov.`,
`10 nov. · 18h`; the year only if it differs from the current one (`4 janv. 2027`). The place on the university
campus is written `university.short`. Lengths within `lengths` (title, one-line and two-line descriptions). An empty
section stays an empty list: the template writes a default message.

---

## 5. WRITE AND RENDER

1. Write `/tmp/contenu.json` (UTF-8, plain text: `render.py` escapes `&` itself):

```json
{
  "week": "Résumé de la semaine du 2 au 8 novembre 2026",
  "deadlines": [{"date": "12 nov.", "title": "...", "desc": "Une phrase.", "button": "S'inscrire", "link": "https://..."}],
  "seminars": [{"left": ["16 nov.", "<short>"], "title": "...", "speaker": "Nom · Affiliation", "desc": "Une phrase.", "link": "https://..."}],
  "workshops": [{"left": ["12 janv. 2027", "Vienne"], "title": "...", "speaker": "Organisateur", "desc": "Deux phrases max.", "reg": true, "link": "https://..."}],
  "events": [{"left": ["26–27 nov.", "<short>"], "title": "...", "desc": "Deux phrases max.", "reg": true, "link": "https://..."}],
  "brief": [{"left": ["10 nov.", "Gembloux"], "title": "...", "desc": "Une phrase.", "link": "https://..."}],
  "infos": [{"left": ["HPC"], "title": "...", "desc": "Une phrase.", "link": "https://..."}]
}
```

   `left`: line 1 is the date, line 2 the place, or « Date limite » when the date shown is a deadline.
   `reg: true` adds « Inscription » under the date. The logo (an SVG of `logos/`), the events title and the
   margin decoration come from `university` in the config.
2. In `/tmp/newsletter-repo/plugins/newsletter`, run
   `python3 scripts/render.py university /tmp/contenu.json /tmp/newsletter.html`: it prints `OK`. On an error, fix
   the JSON and run again.

---

## 6. SEND

1. `python3 scripts/state.py plan config/university.yaml` gives the `owner` and one email to send: its `to` (the
   owner) and its `bcc` (the active subscribers, empty in test mode). `cut` lists the subscribers over `max_bcc`:
   say it in the report.
2. Send it once with the Resend connector, `send-email`:
   - `from`: `sending.from`; `to` and `bcc` from the plan, never another address;
   - `subject`: `Newsletter | <university.name> | Semaine du 2 au 8 novembre`, the real dates of the period, no
     year; across two months write both (`Semaine du 26 octobre au 1er novembre`);
   - `html`: the **whole** `/tmp/newsletter.html`; `text`: `Newsletter hebdomadaire – ouvre ce mail en HTML pour
     voir la mise en page.`; no attachment;
   - `idempotencyKey`: `university-<YYYY-MM-DD of the Monday>`.
3. Check that an email id came back. On an error without id, fix and retry **once** with the same key.

---

## 7. WHEN SOMETHING FAILS

- **The folder is empty or unreadable**: build the email from the sources anyway, and add to `infos` the line
  `Admin` · `Dossier Newsletter illisible cette semaine`.
- **`render.py` fails**: fix the JSON and run again; never write the HTML by hand.
- **No newsletter possible**: send the owner a short text email, subject
  `Newsletter | <university.name> | Non générée cette semaine`, with one sentence on what failed.
- **Resend connector missing or refusing**: do not work around it; stop, give the error in the report.

Send no other email, ask no question.

---

## 8. CHECKLIST

- [ ] Fresh clone and `config/university.yaml` read?
- [ ] Period right, only items still to come, mailbox untouched?
- [ ] `page_reads` respected, no web search?
- [ ] Each section within its maximum, nearest first, a `deadlines` item nowhere else?
- [ ] Right language, no emoji, lengths respected, `render.py` printed `OK`?
- [ ] Sent once to the addresses of `state.py plan`, with an email id back?
