# Install on a new machine

Read only when installing the `claude-remote` setup on a machine, or when a script changed. `<skill folder>` is the "Base
directory for this skill" shown when the skill loads; the scripts are in `<skill folder>/scripts/`.

## Pieces

Everything lives outside any repository and serves every project of the machine.

| From `<skill folder>/scripts/` | To                            | Role                                                                     |
| ------------------------------ | ----------------------------- | ------------------------------------------------------------------------ |
| `claude-remote`                | `~/bin/claude-remote`         | the script (in `PATH`); sets `CLAUDE_REMOTE=1` in the tmux session       |

The answer format of every session (also the remote one) comes from the plugin itself: the `auto-message-format`
skill and its hook, nothing to install.

## Steps

1. Check the requirements of the skill (§ 5): `claude --version` (≥ 2.1, standalone), `command -v tmux`.
2. Copy the scripts (replace `<skill folder>` with the real path):

   ```bash
   mkdir -p ~/bin
   cp <skill folder>/scripts/claude-remote ~/bin/ && chmod +x ~/bin/claude-remote
   ```

3. Check that `~/bin` is in `PATH` (`command -v claude-remote`). If not, **ask me** before adding
   `export PATH="$HOME/bin:$PATH"` to `~/.bashrc`: it is persistent configuration.
4. Test: `claude-remote status` from a project folder says "not running"; then I start it in my own terminal
   (§ 1 of the skill).

## Remove the old phone mode

The phone mode (`/phone`, "Es-tu sur ton téléphone ?") was removed on 2026-11-06: the format of `auto-message-format`
now applies to every answer. On a machine where it was installed, **after asking me** (persistent configuration):

1. remove the files: `rm -f ~/.claude/hooks/phone-*.sh ~/.claude/commands/phone.md && rm -rf ~/.claude/phone`;
2. in `~/.claude/settings.json`, remove the `SessionStart` and `UserPromptSubmit` entries whose command is
   `~/.claude/hooks/phone-start.sh` or `~/.claude/hooks/phone-prompt.sh` (and a list left empty), change nothing
   else, show me the result, write it after my yes, then check: `python3 -m json.tool ~/.claude/settings.json > /dev/null`.

## After a change of a script

- The copies in `~/bin` and `~/.claude/` are not updated by a plugin update: copy the changed scripts again (step 2).
- A change made on a machine goes back into a clone of VikVador/Claude, at `plugins/research/skills/cluster-remote/scripts/`,
  on a branch, through a pull request, so that every machine and the skill stay identical. Never edit
  `~/.claude/plugins/`: that copy is overwritten at the next update.
