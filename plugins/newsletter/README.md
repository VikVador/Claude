# Newsletter

Two newsletters, prepared and sent by Claude from a scheduled task, through the
[Resend](https://resend.com) connector.

| Newsletter         | Skill               | When         | To                         | Language |
| ------------------ | ------------------- | ------------ | -------------------------- | -------- |
| Daily Paper Digest | `newsletter-papers` | every day    | me and the subscribers     | en or fr |
| ULiège weekly      | `newsletter-uliege` | every Monday | me                         | fr       |

## Folders

| Folder       | What                                                                                                | Who edits it          |
| ------------ | --------------------------------------------------------------------------------------------------- | --------------------- |
| `templates/` | The HTML structure of each email, always shown light (no automatic dark mode).                      | me, rarely            |
| `config/`    | Every setting, one YAML per newsletter: sender, recipients, research interests, sources, bounds.    | me, to tune or reuse  |
| `data/`      | The state: `subscribers.yaml`, the papers already sent (`papers/sent.json`) and the ones kept for the next issue (`papers/backup.json`). | Claude, after each issue; me for the subscribers |
| `scripts/`   | `render.py` fills a template from a JSON, checks it and forces the light colours; `state.py` reads and writes the state. | rarely |
| `skills/`    | How to do it: how to search, select, write, send and record. No setting inside.                     | rarely                |

## Run it

- A scheduled task whose prompt is only: `Run the newsletter-papers skill.` (or `newsletter-uliege`).
- The account running it needs the **Resend** connector; `newsletter-uliege` also needs **Microsoft 365** (read
  only), and `newsletter-papers` a way to push to this repository (it records the papers after each issue).

## Change something

- **A subscriber**: add a line to `data/subscribers.yaml` (`email`, `active: true/false`, `language: en/fr`).
- **A theme, a source, a number of papers**: `config/papers.yaml` (themes give the bars of the statistics card).
- **The sender**: `sending.from` in both configs, once the domain is verified in Resend; then
  `sending.subscribers: true` in `config/papers.yaml` to leave test mode.
- **The look**: `templates/*.html`, then check with
  `python3 scripts/render.py papers <content.json> out.html --lang en`.

Test a render without sending: write a small `content.json` (format at the top of `scripts/render.py`) and open the
HTML it gives.
