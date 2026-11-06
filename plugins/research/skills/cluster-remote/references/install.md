# Install on a new machine

Read only when installing the `claude-remote` setup on a machine, or when a script changed. `<skill folder>` is the "Base
directory for this skill" shown when the skill loads; the scripts are in `<skill folder>/scripts/`.

## Pieces

Everything lives outside any repository and serves every project of the machine.

| From `<skill folder>/scripts/` | To                            | Role                                                                     |
| ------------------------------ | ----------------------------- | ------------------------------------------------------------------------ |
| `claude-remote`                | `~/bin/claude-remote`         | the script (in `PATH`); sets `CLAUDE_REMOTE=1` in the tmux session       |
| `phone-prompt.sh`              | `~/.claude/hooks/`            | hook on every prompt: 2 h check, reminder when the mode is on            |
| `phone-start.sh`               | `~/.claude/hooks/`            | hook at startup: the first prompt of a new session always asks           |
| `phone-mode.sh`                | `~/.claude/hooks/`            | turns the mode on / off (state file `~/.claude/phone/mode`)              |
| `phone.md`                     | `~/.claude/commands/phone.md` | the `/phone` command                                                     |
| `settings-hooks.json`          | merged into `~/.claude/settings.json` | declares the two hooks (keep what is there)                      |

The hooks act only where `CLAUDE_REMOTE=1`, so they change nothing in the other sessions.

## Steps

1. Check the requirements of the skill (§ 6): `claude --version` (≥ 2.1, standalone), `command -v tmux`.
2. Copy the scripts (replace `<skill folder>` with the real path):

   ```bash
   mkdir -p ~/bin ~/.claude/hooks ~/.claude/commands
   cp <skill folder>/scripts/claude-remote ~/bin/ && cp <skill folder>/scripts/phone-*.sh ~/.claude/hooks/
   cp <skill folder>/scripts/phone.md ~/.claude/commands/ && chmod +x ~/bin/claude-remote ~/.claude/hooks/phone-*.sh
   ```

3. Check that `~/bin` is in `PATH` (`command -v claude-remote`). If not, **ask me** before adding
   `export PATH="$HOME/bin:$PATH"` to `~/.bashrc`: it is persistent configuration.
4. **Merge the hooks, after asking me** (`~/.claude/settings.json` is persistent configuration of every session):
   1. read `~/.claude/settings.json` (it may not exist) and `<skill folder>/scripts/settings-hooks.json`;
   2. add the `SessionStart` entry (matcher `startup`, `~/.claude/hooks/phone-start.sh`) and the `UserPromptSubmit`
      entry (`~/.claude/hooks/phone-prompt.sh`) to the lists already there, unless they are already in it; change
      nothing else;
   3. show me the resulting `hooks` block, write it only after my yes, then check that the file parses:
      `python3 -m json.tool ~/.claude/settings.json > /dev/null`.
5. Test: `claude-remote status` from a project folder says "not running"; then I start it in my own terminal
   (§ 1 of the skill).

## After a change of a script

- The copies in `~/bin` and `~/.claude/` are not updated by a plugin update: copy the changed scripts again (step 2).
- A change made on a machine goes back into a clone of VikVador/Claude, at `plugins/research/skills/cluster-remote/scripts/`,
  on a branch, through a pull request, so that every machine and the skill stay identical. Never edit
  `~/.claude/plugins/`: that copy is overwritten at the next update.
