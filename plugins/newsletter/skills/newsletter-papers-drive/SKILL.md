---
name: newsletter-papers-drive
description: "Use when a scheduled task of claude.ai (a chat account without Claude Code: no shell, no Python) or I ask to prepare and send the daily paper digest with Google Drive (Daily Paper Digest, newsletter de papiers, veille du jour). The same digest as newsletter-papers, but the state lives in a Google Drive folder, the sources are read with web fetch, and the HTML is written from templates/papers-drive.html; connectors Google Drive and Resend. Not for a Claude Code session, which uses the newsletter-papers skill and GitHub."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Newsletter papers (Drive): the daily digest,
     ┌─┴───┴─┐       without a shell, with Google Drive as memory.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# NEWSLETTER PAPERS (DRIVE)

The Daily Paper Digest, made from a claude.ai account that has no Claude Code: no shell, no script, only web fetch,
the Google Drive connector and the Resend connector. You collect, select, write, send and record in one run, alone,
usually at night from a scheduled task: never ask a question, decide with these rules and go to the end. The
settings are the same as the Claude Code digest, read from GitHub; the memory is a Google Drive folder.

| Where                                                | What                                                                 | Use        |
| ---------------------------------------------------- | -------------------------------------------------------------------- | ---------- |
| `RAW/config/papers.yaml`                             | every setting: sending, bounds, projects, themes, keywords, sources | **Fetch**  |
| `RAW/templates/papers-drive.html`                    | the HTML of the email, filled by you                                 | **Fetch**  |
| Drive `Claude/Daily Paper Digest/subscribers`        | Google Sheet: `email`, `nom`, `statut`, `langue`, `rôle`             | **Read**   |
| Drive `Claude/Daily Paper Digest/state.json`         | `nextIssue`, `lastSent`, `exclude`, `recent`, `backup`               | **Read**, then replace |
| Drive `Claude/Daily Paper Digest/history/`           | one HTML per issue sent                                              | **Create** |

`RAW` = `https://raw.githubusercontent.com/VikVador/Claude/main/plugins/newsletter`. The Drive connector creates
files and trashes them, but never rewrites one: a file is replaced by creating the new one, then trashing the old.

Related: the `newsletter-papers` skill (the same digest from Claude Code, state on GitHub): never run both.

**Contents**

0. In short
1. Read the state
2. Collect
3. Select and order
4. Write
5. Send
6. Record
7. When something fails
8. Checklist

---

## 0. IN SHORT

1. **Settings from GitHub, memory from Drive**: fetch `papers.yaml`, read `state.json` and `subscribers` (§ 1).
2. **Send once**: `lastSent` equal to today's date (in `sending.timezone`) means **stop**, send nothing.
3. **Never a paper twice**: every id of `exclude` is out, case-insensitive (§ 3).
4. **Only verified papers**: a title and an abstract read on arXiv, the publisher or OpenReview; never invented
   metadata, write `not available` instead (§ 3).
5. **Between `papers.min` and `papers.max`**, never filler to reach a number (§ 3).
6. **Recipients from the sheet only** (§ 1, § 5); **the HTML from the template only**, filled, never redesigned (§ 4).
7. **Record after sending**: new `state.json`, old one trashed, the HTML in `history/` (§ 6).

---

## 1. READ THE STATE

1. Fetch `RAW/config/papers.yaml` and read it in full: `sending`, `papers`, `windows_days`, `subagents` (bounds you
   apply to yourself), `look.abstract_sentences`, `collect`, `group`, `projects`, `themes`, `keywords`, `sources`.
2. Find the Drive folder: search `title = 'Daily Paper Digest' and mimeType = 'application/vnd.google-apps.folder'`
   (its parent is the folder `Claude`); then its children `state.json`, `subscribers` and the folder `history`.
3. Read `state.json`. The reader shows `_` as `\_`: read `\_` as `_`. Keep `nextIssue` (today's number), `lastSent`
   (equal to today → stop), `exclude` (the strict exclusion list), `recent` (the last two issues: their
   `dominantLabel` must differ from today's), `backup` (already checked candidates: take them first if they still fit).
4. Read the sheet `subscribers`: one row per person, `email`, `nom`, `statut` (`actif` or not), `langue` (`en` or
   `fr`, `en` when empty), `rôle` (`owner` for me). The plan:
   - the **owner** is the row with `rôle` = `owner` (none → stop and say so in the report);
   - `sending.test` true → one email in the owner's language, `to` = the owner, no `bcc`;
   - otherwise, one email per language present among the active rows: `to` = the owner if it is their language,
     else the sender address of `sending.from`; `bcc` = the other active addresses of that language, at most
     `sending.max_bcc`; the ones over the cap are `cut`: say it in the report;
   - the subject of each: `sending.subject_en` or `subject_fr` + ` | DD/MM/YYYY`, today in `sending.timezone`.

If the Drive folder or `state.json` cannot be read, go on without exclusion and say it in the report; if the sheet
cannot be read, send to nobody: write the report only.

---

## 2. COLLECT

Read the sources yourself with web fetch, within the bounds of `subagents` (`pages_per_source`, `abstracts_read`,
`candidates_returned` per group, `attempts_per_source`): about 30 fetches in all, never more. Keep a title when it
has a `collect.domain` term **and** a `collect.method` term, or two method terms, each at the start of a word.

- **arXiv**: the listing pages, titles first. `monthly` categories: the current and the previous month,
  `https://arxiv.org/list/<category>/<YYYY-MM>?skip=0&show=2000`; `recent` categories:
  `https://arxiv.org/list/<category>/recent?show=2000`. Then the abstract, date and authors of the kept titles on
  `https://arxiv.org/abs/<id>` (or several at once on `http://export.arxiv.org/api/query?id_list=<id>,<id>` when
  that page can be fetched). Never `arxiv.org/search`.
- **Journals**: one Crossref request per `keywords.domain` word and per group, titles only:
  `https://api.crossref.org/works?filter=issn:<ISSN1>,issn:<ISSN2>,...,from-pub-date:<today - windows_days.journals>&query.bibliographic=<word>&select=DOI,title,container-title,published,abstract,author&rows=40&mailto=<crossref_mailto decoded from base64>`;
  a long query returns nothing: one word per request. Keep the titles by the rule above; the `abstract` field (JATS
  XML, strip its tags) when present, else the abstract on the DOI page.
- **Labs** (groups `labs`, only on the days of `subagents.labs_on`): the publication page, then each kept paper
  checked on arXiv or by its DOI.
- **Light reading**: no PDF; a detail page only to settle a real doubt. A source failing `attempts_per_source` times
  is dropped for the run.
- **Per candidate**: title, URL, DOI or arXiv id, publication date, authors (all, or the first 3 and whether there
  are more), abstract word for word, source (journal name or `arXiv <category>`), one label of `themes`.

Under `papers.min` relevant candidates: `papers.extra_waves` targeted wave(s) (the `keywords.method` words on
Crossref, the `physics.ao-ph` listing read further), then accept.

---

## 3. SELECT AND ORDER

- **Reliable**: keep a paper only if its DOI, arXiv id or OpenReview id was seen on its page; a preprint without DOI
  is fine (id `10.48550/arXiv.<id>`).
- **New**: drop every id of `exclude` (case-insensitive); one entry when a preprint and its published version both
  exist.
- **Relevant**: it clearly matches one of `themes` (their `text` and `examples`); exactly one label.
- **Varied**: today's dominant label differs from the `dominantLabel` of the two `recent` issues; relax only to reach
  `papers.min`.
- **Ordered**: closest to the first of `projects` first, then the next projects in order, then the papers that only
  match a theme; numbered 1 to N.
- **Over `papers.max`**: keep the best; the next ones (at most `papers.backup`) go to `backup`.

---

## 4. WRITE

Fetch `RAW/templates/papers-drive.html` and fill it, once per language of the plan; change nothing else in it: no
new style, no new block, light colours as they are.

- `{{lang}}`, `{{issue}}` (= `nextIssue`), `{{count}}` (number of papers), `{{owner}}` (the owner's address),
  `{{date}}`: `6 November 2026` / `6 novembre 2026`.
- Words: `t_issue` Issue / Numéro, `t_review` Review of / Revue du, `t_new` new papers / nouveaux papiers,
  `t_published` published / publié le, `t_read` Read / Lire, `t_footer` "You receive this digest because you
  subscribed. Questions or unsubscribe:" / "Vous recevez ce digest car vous y êtes inscrit. Questions ou
  désinscription :".
- **One card per paper**, the block between `<!-- CARD -->` and `<!-- END CARD -->` repeated in order, comments
  removed: `{{number}}`, `{{label}}`, `{{url}}`, `{{title}}`, `{{authors}}` (the first three, then "et al."),
  `{{source}}`, `{{published}}` (`5 Nov 2026` / `5 nov. 2026`), `{{abstract}}`: the first `look.abstract_sentences`
  sentences of the abstract, **word for word**, then "…" if it was cut; in French, a faithful translation of those
  sentences. Escape `&`, `<`, `>` in every text.
- Under 100 KB (Gmail clips above): fewer sentences before fewer papers.

---

## 5. SEND

For each email of the plan, once, with the Resend connector (`send-email`): `from` = `sending.from`; `to`, `bcc`,
`subject` from the plan, never changed; `html` = the whole page; `text` = `Daily Paper Digest #<issue>` then one line
per paper, `N. Title: link`; `idempotencyKey` = `papers-<issue>-<lang>`. Check that an email id came back; on an
error without id, retry **once** with the same key.

---

## 6. RECORD

After the emails are sent:

1. **New `state.json`**, created in the folder (`text/plain`, no conversion to a Google Doc), with: `about` as
   before; `nextIssue` + 1 (three digits); `lastSent` = today; `exclude` = the old list + today's ids; `recent` = the
   previous issue and today's (`issue`, `date`, `dominantLabel`, `papers` with `id`, `title`, `label`); `backup` =
   today's back-up candidates (`id`, `title`, `url`, `label`). Keys without `_`.
2. **Read it back**: `nextIssue` must be the new number. Then **trash the old `state.json`**, never before.
3. **Archive**: create `history/YYYY-MM-DD #NNN <lang>.html` (`text/html`, no conversion) with the HTML sent.

---

## 7. WHEN SOMETHING FAILS

- **No digest possible** (no relevant paper, sources down): send the **notice** instead, to the same recipients:
  the template with no card and, in place of the cards, one paragraph: "Hello, There was a problem with today's
  newsletter. For any question, you can contact <owner>. Thank you and have a nice day!" (French: "Bonjour,
  Aujourd'hui, il y a eu un souci avec la newsletter. Pour toute question, vous pouvez contacter <owner>. Merci et
  bonne journée !"). Same subject, same key. Record nothing; say why in the report.
- **Resend connector missing or refusing**: no other mail tool; stop, give the error in the report.
- **`onboarding@resend.dev` refused for a recipient**: the sending domain is not verified yet; say so.
- **Drive unwritable**: send anyway, then put the whole new `state.json` in the report so that I save it by hand.

Never write to anyone else, never ask a question. End with a short report in French: candidates read, papers kept
per label, emails sent (language, subject, Resend id), state recorded or not, what failed.

---

## 8. CHECKLIST

- [ ] `papers.yaml` fetched, `state.json` and `subscribers` read, not already sent today?
- [ ] Between `papers.min` and `papers.max` (or the report says how many), none excluded, each seen on its page?
- [ ] Dominant label different from the two recent issues (or relaxed to reach the minimum)?
- [ ] Template filled only, one card per paper in order, abstracts word for word, under 100 KB?
- [ ] Each email of the plan sent once with its subject and an id back, to its `to` and `bcc` only?
- [ ] New `state.json` created and read back, old one trashed, HTML archived in `history/`?
