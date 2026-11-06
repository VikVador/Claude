---
name: cluster-remote
description: "Use to start, check, reattach, stop or repair my Claude Code session kept alive in tmux on a cluster login node and reached through Remote Control (claude.ai/code, the Claude app), also when it is unreachable or says 'not running' because it runs on another login node; for /phone on or off (compact answers for a phone); to install the setup on a new machine. Gives the commands to hand me, the checks and the compact style. Not for git remotes or plain SSH work."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Cluster remote: keep Claude Code running on a
     ┌─┴───┴─┐       remote machine, driven from anywhere.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# CLUSTER REMOTE

Claude Code runs on a distant machine (typically the login node of a cluster) inside tmux, and stays reachable through
its **Remote Control** from https://claude.ai/code or the Claude app, on a computer or a phone. When the client is a
phone, a compact answer mode keeps the answers readable on a small screen. The principle: **one session per project
folder, on one node**, started by me in my own terminal, checked by you.

| File                          | Use                                                                 | When                         |
| ----------------------------- | ------------------------------------------------------------------- | ---------------------------- |
| `scripts/claude-remote`       | installed as `~/bin/claude-remote`: **Run** only `status`, `stop`   | check, stop (§ 1)            |
| `scripts/phone-mode.sh`       | **Run** the copy `~/.claude/hooks/phone-mode.sh`, with `on` or `off` | my answer to the phone question |
| `scripts/phone-prompt.sh`     | hook on every prompt, in `~/.claude/hooks/`: never by hand          | runs by itself               |
| `scripts/phone-start.sh`      | hook at startup, in `~/.claude/hooks/`: never by hand               | runs by itself               |
| `scripts/phone.md`            | the `/phone` command, in `~/.claude/commands/`                      | I type `/phone`              |
| `scripts/settings-hooks.json` | **Copy**, merged into `~/.claude/settings.json`                     | install only                 |
| `references/install.md`       | **Read**                                                            | only to install, or a script changed |

Related: the `cluster-lucia` and `cluster-torch` skills for the rules of their login nodes.

**Contents**

0. In short
1. What you do
2. Commands
3. How it works
4. How long it stays open
5. Compact answer mode
6. Requirements

---

## 0. IN SHORT

1. **Never start it yourself**: `claude-remote` ends with `tmux attach`, which fails in your Bash, and your session
   would share the folder with the remote one. Give me `cd <project folder> && claude-remote` to paste in my own
   terminal on the login node (§ 1).
2. **Check with `claude-remote status`** from the project folder: it changes nothing.
3. **One session per project folder**: run `claude-remote` from each folder to work on several projects at once,
   but never give work to the remote session of a folder and to a local one in the same folder.
4. **tmux is per node**: check, attach or stop a session only on the node where it runs, which `claude-remote status`
   names; starting on another node makes a **second** session.
5. **Ask me before `claude-remote stop`**: it kills Claude and the conversation of that session.
6. **Phone question first**: in a remote session, ask "Es-tu sur ton téléphone ?" when the hook says so, after the
   recap of a dictated request and before the "Quoi de neuf"; yes → the compact style (§ 5).
7. **The phone mode is shared**: `/phone on` in one project turns it on in every remote session (§ 5).

---

## 1. WHAT YOU DO

| Request                   | You                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------- |
| Start a session           | check first, then give me the command for my terminal ("Start" below)                 |
| Is it running?            | run `claude-remote status` from the folder, tell me the node                          |
| Reattach (watch it live)  | give me `cd <project folder> && claude-remote`, on the node of the session            |
| Stop                      | status first, ask me, then `claude-remote stop` on that node ("Stop" below)           |
| Unreachable, broken       | status, then "Repair" below                                                           |
| `/phone on`, `/phone off` | the command runs `phone-mode.sh`: confirm the new state in one short line in French   |

### Start

1. Find the project folder (the one I name, otherwise the current one) and run `claude-remote status` from it.
   Running already: tell me where, nothing to start. Started on another node: see "Repair".
2. Give me, for my own terminal on the login node, `cd <project folder> && claude-remote`, and how to leave it
   running without stopping it: **Ctrl+B**, then **D**.
3. Tell me where to connect: claude.ai/code or the Claude app → **Code** → the session named after the project folder.
4. If your own session works in that folder, tell me to close it once the remote one runs (one session per folder).

### Stop

1. Run `claude-remote status` from the project folder.
2. Running on this node: ask me, then run `claude-remote stop` from the folder. If `CLAUDE_REMOTE` is `1` in your
   environment and the folder is yours, you are that session: give me the command for my terminal instead.
3. Running on another node: give me `ssh <node>`, then `cd <project folder> && claude-remote stop`.

### Repair

| Symptom                               | Cause                                   | Fix                                                    |
| ------------------------------------- | --------------------------------------- | ------------------------------------------------------ |
| "not running", another node named     | the editor reconnected to another node  | me: `ssh <node>`, then status, attach or stop there    |
| gone from the app for a few minutes   | network outage, Claude exited           | wait: the loop reattaches every 30 s                   |
| "gave up after 480 failures"          | outage longer than about 4 h            | ask me, `claude-remote stop`, then me: `claude-remote` |
| "not running", no other node named    | reboot of the node, or processes killed | me: `cd <project folder> && claude-remote`             |
| "Claude Code CLI not found"           | no CLI in `PATH` nor in VSCode          | install the CLI (§ 6)                                  |
| Remote Control refused                | the account blocks it                   | check `~/.claude/policy-limits.json` (§ 6)             |

---

## 2. COMMANDS

| Command                | Effect                                                                                         |
| ---------------------- | ---------------------------------------------------------------------------------------------- |
| `claude-remote`        | Starts the tmux session `claude-<folder>` if needed, then attaches to it (same as `start`)     |
| `claude-remote stop`   | Kills the tmux session of the current folder (and Claude with it)                              |
| `claude-remote status` | Tells whether the session of the folder runs **on the current node**, or names the other nodes |

| Option (environment variable) | Effect                                         | Default            |
| ----------------------------- | ---------------------------------------------- | ------------------ |
| `CLAUDE_REMOTE_MODE`          | permission mode (`default`, `plan`, `auto`, …) | `acceptEdits`      |
| `CLAUDE_REMOTE_DIR`           | working directory, its name names the session  | the current folder |

- **The folder is the one the command runs from.** `CLAUDE_REMOTE_DIR` is for one call only
  (`CLAUDE_REMOTE_DIR=<project folder> claude-remote status`): never export it nor edit its default in the script,
  otherwise every project would share one session.
- Every session of the node: `tmux -S ~/.tmux/claude-remote-$(hostname -s).sock ls`.

---

## 3. HOW IT WORKS

| Piece          | Details                                                                                                  |
| -------------- | -------------------------------------------------------------------------------------------------------- |
| Script         | `~/bin/claude-remote` (in `PATH`, outside any repository)                                                |
| Claude binary  | `claude` from `PATH` (standalone CLI in `~/.local/bin`), otherwise the latest one bundled with VSCode    |
| Command        | `claude remote-control` in a detached tmux session, from the project folder                              |
| tmux socket    | `~/.tmux/claude-remote-<node>.sock`, not `/tmp`, which some nodes clean (the session became unreachable) |
| Shared nodes   | `nice -n 10`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS` and `OPENBLAS_NUM_THREADS` set to 4                   |
| Environment    | `CLAUDE_REMOTE=1` in the tmux session: the phone hooks act only there                                    |
| Network        | outbound HTTPS to Anthropic only: the client needs neither the VPN nor the 2FA of the cluster            |

**Restart loop**

- The first run creates the named session (`--name`), the next ones reattach to it (`-c`).
- After a failure, it restarts 30 s later.
- It stops on exit code 0 or 130 (Ctrl+C); Ctrl+C during the 30 s wait also stops it.

---

## 4. HOW LONG IT STAYS OPEN

| Event                                        | Consequence                                                     |
| -------------------------------------------- | --------------------------------------------------------------- |
| Network outage of about 10 minutes           | Claude exits, the loop reattaches with `-c` every 30 s          |
| `-c` only reattaches within about **4 h**    | After 480 failed retries the loop gives up: `stop` then `start` |
| Reboot of the node                           | Everything is lost: run `claude-remote` again                   |
| Long processes killed by the cluster admins  | Same, run `claude-remote` again                                 |
| `claude-remote stop`, or exit in the session | Ends normally                                                   |

**Good to know**

- **tmux is per node.** An editor can reconnect to another login node: `claude-remote status` then says "not running"
  and names the node where the session was started. Go there with `ssh <node>` before stopping or attaching,
  otherwise you start a **second** session.
- **Login nodes are for light work.** Claude itself is light (~350 MB), but heavy work (training, analysis,
  transfers) goes through the scheduler or the transfer nodes. Check the rules of the cluster (its own skill).

---

## 5. COMPACT ANSWER MODE

In a session started by `claude-remote`, answers can switch to the **compact style**, short enough for a phone.

| When                                        | What happens                                                              |
| ------------------------------------------- | ------------------------------------------------------------------------- |
| First prompt of the session                 | You first ask: "Es-tu sur ton téléphone ?"                                |
| More than **2 h** since the previous prompt | Same question                                                             |
| My answer yes / no                          | You run `~/.claude/hooks/phone-mode.sh on` / `off` and answer accordingly |
| `/phone on`, `/phone off`, `/phone`         | Turns it on, off, or toggles it, at any time                              |
| Mode on                                     | Every prompt reminds you to use the compact style                         |

### The compact style

Every answer has three parts, separated by a horizontal rule (a `---` line between blank lines).

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

### One state for every session

The state lives in `~/.claude/phone/`: `mode` (present while the mode is on) and `last-prompt` (time of the last
prompt). It is **one state for every remote session** of the machine, and for every login node when `$HOME` is shared
(as on a cluster):

- `/phone on` in one project turns the mode on in every remote session, on every node; `/phone off` turns it off
  everywhere.
- The 2 h clock is shared too: a prompt in one project counts for all. A new session clears `last-prompt`, so the next
  prompt of any remote session asks the question again.

Two hooks run the mode (`phone-start.sh` at startup, `phone-prompt.sh` on every prompt), declared in
`~/.claude/settings.json`; `references/install.md` lists every piece.

---

## 6. REQUIREMENTS

| Requirement     | Details                                                                        |
| --------------- | ------------------------------------------------------------------------------ |
| Claude Code CLI | ≥ 2.1, standalone install (command below the table)                            |
| Login           | a **claude.ai account** (`/login`), API keys are not supported                 |
| Remote Control  | allowed by the account: some managed (institution) accounts block it           |
| Client          | logged in with the **same account** as the CLI                                 |
| tmux            | installed on the machine                                                       |
| One session     | **one active session per folder**: never the remote session and a local one    |

Install the CLI: `curl -fsSL https://claude.ai/install.sh | bash`.

A blocked account shows it in `~/.claude/policy-limits.json` (`allow_remote_control: false`).

Prefer the **standalone CLI** to the binary bundled with an editor (VSCode): an editor update removes the old binary,
which breaks a running session at its next restart.
