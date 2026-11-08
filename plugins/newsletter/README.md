# Newsletter

Two newsletters, prepared and sent by Claude from a scheduled task, through the
[Resend](https://resend.com) connector.

| Newsletter         | Skill               | When         | To                         | Language |
| ------------------ | ------------------- | ------------ | -------------------------- | -------- |
| Daily Paper Digest | `newsletter-papers`     | every day    | me and the subscribers | en or fr, per subscriber |
| University weekly  | `newsletter-university` | every Monday | me and the subscribers | fr or en, per subscriber |

## Folders

| Folder       | What                                                                                                | Who edits it          |
| ------------ | --------------------------------------------------------------------------------------------------- | --------------------- |
| `templates/` | The HTML structure of each email, always shown light (no automatic dark mode).                      | me, rarely            |
| `logos/`     | The logos drawn in the emails (`papers.svg`: the digest histogram; `uliege.svg`), as SVG inlined by `render.py`: no image to attach.                | me, rarely            |
| `config/`    | Every setting, one YAML per newsletter: sender, test mode, research interests, sources, bounds; for the university one, its name and mailbox. | me, to tune or reuse |
| `data/`      | `subscribers.yaml`: every recipient, me included (address in base64, newsletters with the language of each, active, owner); the papers already sent (`papers/sent.json`) and the ones kept for the next issue (`papers/backup.json`). | Claude, after each issue; me for the subscribers |
| `scripts/`   | `render.py` fills a template from a JSON, checks it and forces the light colours; `decorations.py` draws the margins: shards for the university newsletter, printed-circuit traces for the digest (`decoration` in each config); `state.py` reads and writes the state. | rarely |
| `skills/`    | How to do it: how to search, select, write, send and record. No setting inside.                     | rarely                |

## Run it

- A scheduled task whose prompt is only: `Run the newsletter-papers skill.` (or `newsletter-university`).
- The account running it needs the **Resend** connector; `newsletter-university` also needs **Microsoft 365** (read
  only), and `newsletter-papers` a way to push to this repository (it records the papers after each issue).

## Change something

- **A subscriber**: add an entry to `data/subscribers.yaml`: `email` (from `python3 scripts/state.py encode <address>`),
  `newsletters: {science: en}`, `{university: fr}` or both (`{science: en, university: fr}`), each in its language,
  `active: true/false`.
- **The subjects**: `sending.subject_en` and `subject_fr` in each config; the date of the day it is sent is added
  (`Newsletter | Scientific Papers | 07/11/2026`).
- **The problem notice** (sent instead of a newsletter that could not be made): `NOTICE` in `scripts/render.py`;
  see it with `python3 scripts/render.py papers --notice out.html --lang fr`.
- **A theme, a source, a number of papers**: `config/papers.yaml` (themes give the bars of the statistics card).
- **The sender**: `sending.from` in both configs, once the domain is verified in Resend; then `sending.test: false`
  to send to every subscriber, not only the owner.
- **Another university**: `config/university.yaml` (identity, mailbox, agendas); the skill names none.
- **The look**: `templates/*.html`, then check with
  `python3 scripts/render.py papers <content.json> out.html --lang en`.

Test a render without sending: write a small `content.json` (format at the top of `scripts/render.py`) and open the
HTML it gives.
