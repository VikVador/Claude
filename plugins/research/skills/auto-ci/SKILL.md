---
name: auto-ci
description: "Use as soon as a pull request is opened, or new commits are pushed to one, in a repository with GitHub Actions (a .github/workflows folder: Heimdall, Neptune, Poseidon, Shaggy, Albus, ...), whether you opened it or I did; also when I say a PR is up or ask whether the CI passed. Watches the checks in the background, and when one fails, reads the failing log on GitHub, finds the cause, reproduces it locally, pushes the fix to the same branch and watches again. Not for merging, reviewing or changing the CI itself."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Auto CI: after a pull request, check that the
     ┌─┴───┴─┐       CI passes online, and fix it when it does not.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# AUTO CI

Tests pass locally, yet the CI on GitHub can still fail: another Python, another version of a tool, a dependency
missing from `pyproject.toml`, a file that was never committed. Every pull request is watched until its checks end,
and a failure is understood and fixed before I have to look at it.

**Last checked: 2026-11-06** (the `ci.yml` and `pre-commit.yml` of Heimdall, Neptune, Poseidon, Shaggy and Albus;
`gh pr checks` exit codes on a green and a red pull request).

Related: the `auto-update` skill (pull requests of the projects); the cluster skills for where tests can run.

**Contents**

0. In short
1. Watch
2. Diagnose
3. Fix
4. Report

---

## 0. IN SHORT

1. **Right after a PR is opened or pushed to**, start a watcher in the background (§ 1); keep working meanwhile.
2. **A check fails** → read its log on GitHub, find the first real error, reproduce it locally (§ 2).
3. **Fix it on the PR's branch**, one commit, push, watch again; at most 3 rounds, then stop and tell me (§ 3).
4. **Never** weaken a test, skip it, add an ignore rule, change the workflow or the pre-commit config, force-push,
   merge, or touch `main` without asking me first.
5. **Tell me** in a few lines, in French: passed, or what failed, why, and the fix pushed (§ 4).
6. **Already watched by the app** (Claude desktop app with Auto-fix or a CI monitor on the PR): let it do the work,
   do not start a second watcher.

---

## 1. WATCH

1. Get the number of the pull request (`gh pr view --json number -q .number` on its branch, or from `gh pr create`).
2. Start the watcher **in the background** (the Bash tool's background mode; you are notified when it exits). The
   first wait lets GitHub register the checks:

   ```bash
   sleep 60; gh pr checks <number> -R <owner>/<repo> --watch --interval 30 --fail-fast
   ```

   Exit code 0: every check passed. Any other code: a check failed or was cancelled (also when no check started
   after the wait: then look with `gh run list -R <owner>/<repo> -L 3` before concluding).
3. Do not poll by hand and do not wait idle: the notification brings you back. If the main conversation is busy,
   a background agent can do the watch and the diagnosis of § 2, and report back.
4. No `.github/workflows` in the repository → nothing to watch; say so once.

---

## 2. DIAGNOSE

1. Find the failed run and job: `gh pr checks <number> -R <owner>/<repo>` (the link names the run), or
   `gh run list -R <owner>/<repo> --branch <branch> -L 3`.
2. Read the failing log, **from the first error**, not its end: the last lines are the runner cleaning up.

   ```bash
   gh run view <run-id> -R <owner>/<repo> --log-failed | grep -nE "##\[error\]|Error|error:|FAILED|Failed|would reformat" | head -40
   gh run view <run-id> -R <owner>/<repo> --log-failed | sed -n '<first line - 20>,<first line + 40>p'
   ```

3. Decide which kind of failure it is:

| Kind                      | Signs                                                         | What to do                          |
| ------------------------- | ------------------------------------------------------------- | ----------------------------------- |
| Caused by the PR          | the failing test or file is one the PR changed or uses        | fix it (§ 3)                        |
| Already failing on `main` | the same job fails on the last run of `main`                  | tell me, do not fix it in this PR   |
| Flaky or infrastructure   | network, download, runner, timeout, nothing about the code    | `gh run rerun <run-id> --failed` once |

4. Reproduce it locally before changing anything, in the conditions of the CI (read `.github/workflows/ci.yml`).
   In my projects the CI runs pre-commit on every file, then pytest on Python 3.11 with the CPU build of PyTorch:

| Job        | Reproduce with                                                                                |
| ---------- | --------------------------------------------------------------------------------------------- |
| pre-commit | `pre-commit run --all-files --config pre-commit.yml` (pinned tool versions, as in the CI)     |
| pytest     | `pytest tests` in a fresh Python 3.11 environment with `pip install .` (not an editable install) |

**Good to know**: why it passes locally and fails online

- A different version of `ruff` than the one pinned in `pre-commit.yml` (formatting or rules differ).
- A dependency installed in my environment but missing from `pyproject.toml`; a CUDA-only path on a CPU runner.
- A new file not committed, or a path that only works on macOS (case of file names).
- Another Python than 3.11, a test that needs data, a GPU, a secret or the network.

---

## 3. FIX

- Work on the PR's branch, in its folder; pull first if I may have pushed.
- The smallest change that fixes the cause; run the same reproduction again, it must pass locally.
- One commit per round, message `🐛 CI - <what was wrong>`, then push (never `--force`) and start the watcher again.
- **At most 3 rounds**: if the CI still fails, stop, say what you tried and what you think is wrong.
- Ask me first before any of: deleting, skipping or loosening a test; an ignore rule (`# noqa`, a ruff exclusion);
  changing the workflow, the pre-commit config or a pinned version; adding a dependency.

---

## 4. REPORT

A few lines, in French, when the watch ends:

- **Passed**: "CI verte sur #<n>." and nothing more.
- **Fixed**: what failed (job, test), the cause in one sentence, the fix and its commit, "CI relancée" then the
  result.
- **Not fixed**: what failed, the cause if known, what was tried, and the one decision I need to take.
