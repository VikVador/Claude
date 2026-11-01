---
name: remote
description: Use to deploy, check or stop a remote Claude Code session on a distant machine (for example the login node of a computing cluster), kept alive in tmux and reached from anywhere through Remote Control (claude.ai/code or the Claude app). Also use for the compact answer mode of such sessions (/phone), and to install this setup on a new machine.
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Remote: keep Claude Code running on a distant
     ┌─┴───┴─┐       machine and drive it from anywhere.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# REMOTE

Claude Code runs on a distant machine (typically the login node of a cluster) inside tmux, and stays reachable through
its **Remote Control** from https://claude.ai/code or the Claude app, on a computer or a phone. When the client is a
phone, a compact answer mode keeps the answers readable on a small screen.

**Contents**

0. In short
1. Usage
2. How it works
3. How long it stays open
4. Requirements
5. Compact answer mode
6. Install on a new machine

---

## 0. IN SHORT

1. **Start** in a terminal on the machine, from the project folder: `claude-remote`. **Leave** without stopping it:
   **Ctrl+B**, then **D**.
2. **Connect**: claude.ai/code or the Claude app → **Code** → the session named after the project folder.
3. **One active session at a time**: never give work to the remote session and to a local one simultaneously.
4. **tmux is per node**: check or stop the session from the node where it runs; `claude-remote status` names it.
5. **Compact answers** on a phone: `/phone on`, back to normal with `/phone off` (§ 5).

---

## 1. USAGE

| Command               | Effect                                                                                         |
| --------------------- | ---------------------------------------------------------------------------------------------- |
| `claude-remote`        | Starts the tmux session `claude` if needed, then attaches to it                                |
| `claude-remote stop`   | Kills the tmux session (and Claude with it)                                                    |
| `claude-remote status` | Tells whether the session runs **on the current node**, otherwise on which node it was started |

| Option (environment variable) | Effect                                         | Default       |
| ----------------------------- | ---------------------------------------------- | ------------- |
| `CLAUDE_REMOTE_MODE`           | permission mode (`default`, `plan`, `auto`, …) | `acceptEdits` |
| `CLAUDE_REMOTE_DIR`            | working directory, its name names the session  | the current folder |


---

## 2. HOW IT WORKS

| Piece          | Details                                                                                                  |
| -------------- | -------------------------------------------------------------------------------------------------------- |
| Script         | `~/bin/claude-remote` (in `PATH`, outside any repository)                                                 |
| Claude binary  | `claude` from `PATH` (standalone CLI in `~/.local/bin`), otherwise the latest one bundled with VSCode    |
| Command        | `claude remote-control` in a detached tmux session, from the project folder                              |
| tmux socket    | `~/.tmux/claude-remote-<node>.sock`, not `/tmp`, which some nodes clean (the session became unreachable)  |
| Shared nodes   | `nice -n 10`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS` and `OPENBLAS_NUM_THREADS` set to 4                   |
| Network        | outbound HTTPS to Anthropic only: the client needs neither the VPN nor the 2FA of the cluster            |

**Restart loop**

- The first run creates the named session (`--name`), the next ones reattach to it (`-c`).
- After a failure, it restarts 30 s later.
- It stops on exit code 0 or 130 (Ctrl+C); Ctrl+C during the 30 s wait also stops it.

---

## 3. HOW LONG IT STAYS OPEN

| Event                                       | Consequence                                                     |
| ------------------------------------------- | --------------------------------------------------------------- |
| Network outage of about 10 minutes          | Claude exits, the loop reattaches with `-c` every 30 s          |
| `-c` only reattaches within about **4 h**   | After 480 failed retries the loop gives up: `stop` then `start` |
| Reboot of the node                          | Everything is lost: run `claude-remote` again                    |
| Long processes killed by the cluster admins | Same, run `claude-remote` again                                  |
| `claude-remote stop`, or exit in the session | Ends normally                                                   |

**Good to know**

- **tmux is per node.** An editor can reconnect to another login node: `claude-remote status` then says "not running"
  and names the node where the session was started. Go there with `ssh <node>` before stopping or attaching,
  otherwise you start a **second** session.
- **Login nodes are for light work.** Claude itself is light (~350 MB), but heavy work (training, analysis,
  transfers) goes through the scheduler or the transfer nodes. Check the rules of the cluster (its own skill).

---

## 4. REQUIREMENTS

| Requirement     | Details                                                                        |
| --------------- | ------------------------------------------------------------------------------ |
| Claude Code CLI | ≥ 2.1, installed with `curl -fsSL https://claude.ai/install.sh \| bash`        |
| Login           | a **claude.ai account** (`/login`), API keys are not supported                 |
| Remote Control  | allowed by the account: some managed (institution) accounts block it           |
| Client          | logged in with the **same account** as the CLI                                |
| tmux            | installed on the machine                                                       |
| One session     | **one active session at a time**: never the remote session and a local one     |

A blocked account shows it in `~/.claude/policy-limits.json` (`allow_remote_control: false`).

Prefer the **standalone CLI** to the binary bundled with an editor (VSCode): an editor update removes the old binary,
which breaks a running session at its next restart.

---

## 5. COMPACT ANSWER MODE

In the session started by `claude-remote`, answers can switch to a **compact style**, short enough for a phone.

| When                                        | What happens                                          |
| ------------------------------------------- | ----------------------------------------------------- |
| First prompt of the session                 | Claude first asks: "Es-tu sur ton téléphone ?"        |
| More than **2 h** since the previous prompt | Same question                                         |
| Answer yes / no                             | Claude turns the mode on / off by itself              |
| `/phone on`, `/phone off`, `/phone`         | Turns it on, off, or toggles it, at any time          |
| Mode on                                     | Every prompt reminds Claude to use the compact style  |

**Compact style**: every answer has three parts, separated by a horizontal rule (a `---` line between blank lines).

| Part       | Content                                                                            |
| ---------- | ---------------------------------------------------------------------------------- |
| 1. Title   | the task in a few words, in **bold**                                               |
| 2. Summary | 2 to 4 lines of plain text: what was done or found, and why, very simple and clear |
| 3. Changes | one bullet per change: *what* changed, then *why* in one short, simple sentence    |

- Part 3 is left out when nothing was changed (a simple question, a status check).
- A question to me comes last, on its own line, with the expected answers: `👉 Je relance ? (oui / non)`.
- No wide tables, no code blocks, no long paths: file names only. I can ask "détaille" for the normal answer.

Example:

```markdown
**SSS : valeurs aberrantes retirées**

---

Les pics de la validation venaient de quelques salinités impossibles (> 45 PSU)
en 2019-2021. Je les ai retirées et l'entraînement repart de zéro (≈ 20 h).

---

- `data/__init__.py` : les salinités > 45 PSU deviennent des trous (NaN),
  comme les zones sans mesure.
- `encoder-sss.yml` : relancé de zéro, car les anciens poids avaient appris ces pics.
- Job 21012345 : en attente d'une RTX du labo, démarrage estimé ce soir.

👉 Je pousse la branche ? (oui / non)
```

**How it works** (outside the repository, for all projects)

| Piece                             | Role                                                                |
| --------------------------------- | ------------------------------------------------------------------- |
| `CLAUDE_REMOTE=1`                  | set by `claude-remote` in the tmux session: the hooks act only there |
| `~/.claude/hooks/phone-prompt.sh` | hook on every prompt: 2 h check, reminder when the mode is on       |
| `~/.claude/hooks/phone-start.sh`  | hook at startup: the first prompt of a new session always asks      |
| `~/.claude/hooks/phone-mode.sh`   | turns the mode on / off (state file `~/.claude/phone/mode`)         |
| `~/.claude/commands/phone.md`     | the `/phone` command                                                |
| `~/.claude/settings.json`         | declares the two hooks                                              |

---

## 6. INSTALL ON A NEW MACHINE

The scripts live in `scripts/`, next to this file; copy them to the places Claude Code and the shell expect.

| From `scripts/`                                      | To                                                         |
| ---------------------------------------------------- | ---------------------------------------------------------- |
| `claude-remote`                                       | `~/bin/claude-remote` (in `PATH`)                           |
| `phone-mode.sh`, `phone-prompt.sh`, `phone-start.sh` | `~/.claude/hooks/`                                         |
| `phone.md`                                           | `~/.claude/commands/phone.md`                              |
| `settings-hooks.json`                                | merged into `~/.claude/settings.json` (keep what is there) |

```bash
mkdir -p ~/bin ~/.claude/hooks ~/.claude/commands
cp scripts/claude-remote ~/bin/ && cp scripts/phone-*.sh ~/.claude/hooks/
cp scripts/phone.md ~/.claude/commands/ && chmod +x ~/bin/claude-remote ~/.claude/hooks/phone-*.sh
```

- Set `CLAUDE_REMOTE_DIR` (or edit the default in the script) to the folder of the project.
- After a change of a script, copy it back into `scripts/` of the `claude` repository so that both stay identical.
