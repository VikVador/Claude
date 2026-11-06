# Claude skills

- Every `plugins/research/skills/*/SKILL.md` follows `SKILL-TEMPLATE.md`: read it before creating or editing a skill.
- After an edit, check the sizes (`wc -lc plugins/research/skills/*/SKILL.md`: at most 400 lines and 20 000
  characters) and that every front matter parses as YAML; then bump `plugins/research/.claude-plugin/plugin.json`
  and open a pull request.
