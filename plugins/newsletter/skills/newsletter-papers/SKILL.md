---
name: newsletter-papers
description: "Use when a scheduled task or I ask to prepare and send the daily paper digest (Daily Paper Digest, newsletter de papiers, veille scientifique du jour). Collects recent papers from arXiv, journals and labs with subagents, selects and orders them by research interest, renders the light HTML email in English and French, sends it with the Resend connector to me and the subscribers, and records the papers on GitHub. Not for the weekly university newsletter (newsletter-university skill)."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Newsletter papers: the daily digest of new
     ┌─┴───┴─┐       papers, collected, written, sent, recorded.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# NEWSLETTER PAPERS

Every day, the Daily Paper Digest brings me and its subscribers recent papers that matter for my research, each with
a short summary. You do everything in one run: collect, select, write, send, record. You usually run alone, at night,
from a scheduled task: never ask a question, decide with these rules and go to the end. This file says **how**; every
setting (interests, sources, bounds) is in `config/papers.yaml`, and every recipient in `data/subscribers.yaml`.

Everything lives in `VikVador/Claude`, folder `plugins/newsletter/` (called `NL` below), always used from a fresh
clone: the installed plugin copy is stale.

| File in `NL`               | Use                                                                         | When        |
| -------------------------- | --------------------------------------------------------------------------- | ----------- |
| `config/papers.yaml`       | **Read**: sending, bounds, research group, projects, themes, sources        | § 1         |
| `scripts/state.py`         | **Run**: next issue, exclusion list, sending plan, record                   | § 1, 6      |
| `scripts/render.py`        | **Run** `python3 scripts/render.py papers content.json <out> --lang <en/fr>`| § 4         |
| `templates/papers.html`    | the structure of the email, filled by `render.py`: never edited by hand     | never       |
| `data/papers/*.json`, `data/subscribers.yaml` | the state, read and written by `state.py`                | never by hand |

Related: the `newsletter-university` skill for the weekly university newsletter.

**Contents**

0. In short
1. Read the state
2. Collect
3. Select and order
4. Write and render
5. Send
6. Record
7. When something fails
8. Checklist

---

## 0. IN SHORT

1. **Fresh clone first**, settings from `config/papers.yaml`, never values remembered from an earlier run (§ 1).
2. **Send once**: if `state.py status` says `already_sent_today`, stop without sending (§ 1).
3. **Never a paper twice**: every id of `state.py exclude` is out (§ 3).
4. **Only verified papers**: existence checked by DOI, arXiv id or OpenReview id; never an invented metadata, write
   `non disponible` instead (§ 3).
5. **Between `papers.min` and `papers.max`**, never filler to reach a number (§ 3).
6. **Recipients from `state.py plan` only**, never an address you make up or remember (§ 1, § 5).
7. **Record after sending**, in one commit pushed to `main` (§ 6).

---

## 1. READ THE STATE

```bash
git clone --depth 1 https://github.com/VikVador/Claude.git /tmp/newsletter-repo
cd /tmp/newsletter-repo/plugins/newsletter
python3 scripts/state.py status
```

1. Read `config/papers.yaml` in full.
2. From `status`: `next_issue` is today's number; `already_sent_today: true` means **stop**, send nothing;
   `last_two_dominant_labels` must differ from today's dominant label; `backup` counts the already-checked candidates
   of `data/papers/backup.json`: take them first if they still fit.
3. `python3 scripts/state.py exclude > /tmp/exclude.txt`: the strict exclusion list.
4. `python3 scripts/state.py plan config/papers.yaml > /tmp/plan.json`: the `owner` (gets every issue and the
   reports) and one email per language to send, each with its `to` and `bcc` (only the owner in test mode). Its
   languages are the ones to write (§ 4).

If the clone fails, go on without exclusion and add ` | no history check` to the subject (§ 5).

---

## 2. COLLECT

1. Launch one subagent per group of `sources`, **in parallel**; the `Labs` groups only on the days of
   `subagents.labs_on`. Give each one: its sources, the windows (`windows_days`), its bounds (`subagents`), the
   `themes`, the `keywords`, the exclusion list, the reading rules below and the return format. Without a subagent
   tool, do the groups one after the other with the same bounds.
2. Under `papers.min` relevant candidates after this first wave: `papers.extra_waves` targeted wave(s), then accept.

**Reading rules** (give them to every subagent, word for word)

- **arXiv**: read the listing pages, filter on titles first. `monthly` categories: the pages of the current and the
  previous month, `https://arxiv.org/list/<category>/<YYYY-MM>?skip=0&show=2000`; `recent` categories:
  `https://arxiv.org/list/<category>/recent?show=2000`. **Never** `export.arxiv.org` nor `arxiv.org/search`: both
  are closed to robots.
- **Journals**: one Crossref request with all the group's ISSNs, the date and the keywords, titles only:
  `https://api.crossref.org/works?filter=issn:<ISSN1>,issn:<ISSN2>,...,from-pub-date:<YYYY-MM-DD>&query.bibliographic=<keywords>&select=DOI,title,container-title,published&rows=<crossref_rows>&mailto=<crossref_mailto decoded by state.py decode>`;
  sort on titles, then read the abstract of the kept papers only, through their DOI.
- **Labs**: read the publication page, then check each kept paper on arXiv or by its DOI.
- **Light reading**: no PDF; open a detail page only to settle a real doubt.
- **Stop** at the first bound reached, never past it, and return what you have. A source failing
  `attempts_per_source` times is dropped for the rest of the run.
- **Return**, per candidate: title, URL, DOI or arXiv id, publication date, all authors (or the first 3 and whether
  there are more), abstract, source, one label of `themes`, one sentence on why it is relevant.

---

## 3. SELECT AND ORDER

- **Reliable**: keep a paper only if its DOI, arXiv id or OpenReview id was checked; a preprint without DOI is fine.
- **New**: drop every id of the exclusion list (case-insensitive); one entry when a preprint and its published
  version both exist.
- **Relevant**: it clearly matches one of `themes`; exactly one label.
- **Varied**: today's dominant label differs from `last_two_dominant_labels`; relax only to reach `papers.min`.
- **Ordered**: closest to the first of `projects` first, then the next projects in order, then the papers that only
  match a theme; numbered #1 to #N in that order.
- **Over `papers.max`**: keep the best; the next ones (at most `papers.backup`) go to the `backup` list of
  `content.json`.

---

## 4. WRITE AND RENDER

1. Write `/tmp/content.json`, format at the top of `scripts/render.py`: `model` (your name, `Opus 5.5`), `issue`,
   `date` (ISO), `papers`, `backup`. Per paper: `url`, `title`, `authors`, `et_al`, `doi` (bare; arXiv:
   `10.48550/arXiv.<id>`; the OpenReview id if no DOI), `doi_url`, `published` (ISO), `label`, `summary`.
2. **summary**: your own paragraph in English, `summary.characters` long, problem, then proposed solution, then
   conclusion, with `summary.bold_key_phrases` short key phrases in `**bold**`. Plain text (`render.py` escapes
   `& < >`). No em dash (—) nor en dash (–): commas, colons or parentheses.
3. **summary_fr**: the same summary in French, same rules, if `plan.json` has a `fr` email.
4. Render each needed language: `python3 scripts/render.py papers /tmp/content.json /tmp/digest-<lang>.html --lang <lang>`.
   It checks the labels, summaries, dashes, placeholders and size, and forces the light colours. On an error, fix
   `content.json` and run again: never edit the HTML.

---

## 5. SEND

1. **Recipients**: the emails of `/tmp/plan.json`, as they are: one per language, its `to` and its `bcc`. The owner
   is in `to` of each one (with French subscribers, I get both copies). `cut` lists the subscribers over
   `max_bcc`: say it in the report.
2. **Subject**: `Newsletter | Papers | #XXX`, plus ` | no history check` if § 1 failed, plus ` | N papers` if under
   `papers.min`.
3. **Send** each email once with the Resend connector, `send-email`: `from` = `sending.from`; `to`, `bcc`, `subject`
   as above; `html` = the **whole** `digest-<lang>.html`, never cut; `text` = `Daily Paper Digest #XXX` then one line
   per paper, `N. Title: link`; `idempotencyKey` = `papers-<issue>-<lang>`.
4. Check that an email id came back. On an error without id, fix and retry **once** with the same key.

---

## 6. RECORD

```bash
cd /tmp/newsletter-repo/plugins/newsletter
python3 scripts/state.py record /tmp/content.json
git add data && git commit -m "📰 Papers #<issue>" && git push
```

`record` appends the issue to `data/papers/sent.json` and replaces `data/papers/backup.json` by the `backup` list.
If the push is rejected, `git pull --rebase` and push once more. If you cannot push (no GitHub credentials), send
the owner a text email, subject `Newsletter | Papers | #XXX | not recorded`, with the content of the two
files, so that I commit them by hand.

---

## 7. WHEN SOMETHING FAILS

- **No relevant paper at all**: no email to the subscribers; send the owner a text email, subject
  `Newsletter | Papers | DD-MM-YYYY | not generated`, one sentence on why.
- **Resend connector missing or refusing**: do not work around it (no other mail tool); stop, give the error in the
  report.
- **`onboarding@resend.dev` refused for a recipient**: the sending domain is not verified yet; say so in the report.
- **A source keeps failing**: drop it (§ 2), go on with the others.

Never write to anyone else, never ask a question.

---

## 8. CHECKLIST

- [ ] Fresh clone, `config/papers.yaml` read, not already sent today?
- [ ] Between `papers.min` and `papers.max` (or the subject says how many), none excluded, each checked by its id?
- [ ] Dominant label different from the last two (or relaxed to reach the minimum)?
- [ ] Ordered by the projects, numbered #1 to #N, every needed language rendered `OK`?
- [ ] Each email of the plan sent once with an id back, to its `to` and `bcc` only?
- [ ] `state.py record` run and pushed, or the "not recorded" email sent?
