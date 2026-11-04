---
name: up-to-date
description: Use when a conversation starts or resumes after a while in a project folder (the hook up-to-date.py of this plugin reminds you, at most every 6 hours per folder), or when asked what changed in the libraries or the projects. Checks whether albus and shaggy installed in the project environment are behind GitHub and updates them, then reads the last 3 pull requests of Heimdall and Neptune, to know what the other project did, and gives a very short "Quoi de neuf" before answering, with a short question for each change of the other project worth reusing here.
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Up to date: before working again on a project,
     ┌─┴───┴─┐       check what moved in the libraries and the projects.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# UP TO DATE

The user works on several projects at once (Heimdall on Torch, Neptune on Lucia, the playground), with one Claude
session per project. The libraries they share (`albus`, `shaggy`) change often, and so do the projects. Before
working again after a while, each session catches up, for two goals:

- **Same libraries everywhere**: the project environment always runs the latest `albus` and `shaggy`.
- **The best of both projects**: Heimdall and Neptune share most of their design (encoders, losses, training). Each
  session reads what was done in the other project, and proposes to bring here what would help.

**Contents**

0. In short
1. When
2. Libraries
3. Pull requests
4. What to tell the user
5. Versions next to every result

---

## 0. IN SHORT

1. **Run** `python check.py --since <time of the last check>` with the Python of the **project environment**
   (`check.py` sits next to this file, standard library only, reads the public GitHub API without any token).
2. **A library is behind** → update it in the environment (§ 2), unless a job uses the environment or the project
   pins a commit.
3. **Read** the last 3 pull requests of Heimdall and Neptune, to know what was done on the other side (§ 3).
4. **Tell** the user in a very short "Quoi de neuf", with **one short question** per change of the other project that
   could help here (§ 4), then answer their message.
5. **Write the versions** (`python check.py --versions`) next to every result: report, run, log (§ 5).

---

## 1. WHEN

- The hook `up-to-date.py` of this plugin adds a reminder to the first message of a session when the folder was not
  brought up to date for **6 hours** or more (time in UTC kept in `~/.claude/up-to-date/<folder>.txt`, written when
  reminding, so the reminder comes only once). It gives the time of the last check, to pass to `--since`.
- The check is quick (a few seconds); the user changes the libraries often, so do it every time it is asked.
- Also when the user asks what changed, or before a task that relies on the latest version of a library.
- Not for scheduled or automatic messages, nor in the middle of a task: do it at the first natural pause.

---

## 2. LIBRARIES

`check.py` compares the commit each library was installed from (`direct_url.json` of pip) with its branch on GitHub
(`albus@main`, `shaggy@master`), and lists the commits and the files changed in between.

**Find the environment** in the `CLAUDE.md` of the project (overlay on Torch, micromamba on Lucia, ...). No
environment in the folder → run `python3 check.py --no-libraries` and skip this section.

**Update only when all hold**, otherwise say why it was not done:

| Condition                                  | Check                                                                     |
| ------------------------------------------ | ------------------------------------------------------------------------- |
| The library is behind                      | `check.py` says `BEHIND`                                                  |
| The project follows the branch             | the requirements say `@main` / no commit; a pinned commit stays as it is |
| No job of the user uses the environment    | `squeue -u $USER` and the command of the jobs (`scontrol show job <id>`)  |

**How** (`--no-deps` leaves torch and the other packages untouched):

```bash
pip install --no-deps --force-reinstall git+https://github.com/VikVador/<library>@<branch>
pip check                                          # a new dependency? install it, then check again
python -c "import albus, shaggy"                   # the environment still imports
```

| Cluster | Where to run it                                                                                                  |
| ------- | ---------------------------------------------------------------------------------------------------------------- |
| Torch   | in a short CPU job, overlay mounted `:rw` with `--fakeroot` (login nodes: 2 GB), read the `torch` skill first:   |
|         | `srun --account=torch_pr_347_general -c4 --mem=16G -t0:30:00 apptainer exec --fakeroot --overlay <overlay>:rw <image> bash -c "source /ext3/env.sh; pip ..."` |
| Lucia   | in the micromamba environment of the project, read the `lucia` skill first                                       |
| Other   | in the environment named by the `CLAUDE.md` of the project                                                       |

Then run `check.py` again with the environment mounted read-only: it must say `up to date`.

**When the public API of a library changed** (new module, function renamed or removed, see the files changed): check
that the description of the library in the resources file of the project (e.g. `.claude/claude-ressources.md`)
still holds, and update it; in a repository, propose the change to the user first.

---

## 3. PULL REQUESTS

`check.py` prints the last **3** pull requests of `VikVador/Heimdall` and `VikVador/Neptune` (by creation): number,
state (`open`, `merged`, `closed`), `NEW` when updated since the last check, link and the "Summary" section.

**Why**: so that the session knows what was done on the other side, and both projects take the best of each other.

- Read every summary. When a `NEW` one touches a piece both projects share (encoders, losses, training, tools moved
  to `shaggy`, data), open it (`gh pr view <n> -R VikVador/<project>`, or the link) and read its changes.
- In the pull requests of the **current** project, note what changed (another session may have done it).
- In the pull requests of the **other** project, look for what would help here: a fix, a speed-up, a better setting,
  a lesson from an experiment. Check first whether the current project already has it (same name, same code).
- Read only: never comment, review, approve or merge, and never port a change without the user's answer.

---

## 4. WHAT TO TELL THE USER

Before answering their message, a very short block, in their language, in the compact style:

- a title in bold, e.g. **Quoi de neuf depuis le 1er novembre**;
- `---`, then 1 to 2 plain lines: the libraries (updated, or why not) and the main news;
- `---`, then one bullet per thing worth knowing: a library updated (from which commit to which, docs only or code),
  a pull request merged or opened (number, one sentence), and what it changes for the current project, if anything.
- Then, for each change of the other project that could help here, **one question**: clear, simple, concise, saying
  what changed there and why it would help here, e.g.

  > Neptune #38 retire la mise à l'échelle σ/τ des distances de la GME pour l'océan : l'encodeur océan
  > n'apprenait plus avec. Heimdall l'a encore pour les observations ; on teste sans aussi ?

  At most 3 questions, the most useful first; none when nothing applies.

Nothing changed → a single line ("Tout est à jour : albus, shaggy, aucune nouvelle PR."). Then answer the message.
Never present as done an update that was not run and checked.

---

## 5. VERSIONS NEXT TO EVERY RESULT

The libraries now change under the experiments: the same command can give another number after an update. To tell a
change of the code from a change of a library, every result says which commits it was made with.

- `python check.py --versions` (Python of the project environment, no network) prints e.g.
  `albus 32ebf6b, shaggy 6095950`.
- **Reports**: this line at the bottom of the page (`<p class="versions">`, see the `report` skill).
- **Runs**: in the configuration logged with the run (WandB config, saved `config.yml`) and at the top of the log.
- **Comparing two results** made with different versions: say it, and check the commits in between before blaming
  the model.
