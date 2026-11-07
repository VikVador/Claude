# Claude skills

- Two plugins: `plugins/research` and `plugins/newsletter`. Every `plugins/*/skills/*/SKILL.md` follows
  `SKILL-TEMPLATE.md`: read it before creating or editing a skill.
- After an edit, check the sizes (`wc -lc plugins/*/skills/*/SKILL.md`: at most 400 lines and 20 000 characters) and
  that every front matter parses as YAML; then bump the `.claude-plugin/plugin.json` of the plugin changed and open a
  pull request.
- One exception: the newsletter skills commit their state (`plugins/newsletter/data/`) straight to `main` after each
  issue. Settings live in `plugins/newsletter/config/`, never in the skills.
