---
name: auto-update
description: "Use when a session starts or resumes after a while in a Heimdall, Neptune, albus or shaggy folder (the hook auto-update.py reminds you), when asked what changed in the libraries or the projects, before a task that needs the latest albus or shaggy, and to write the library versions next to a result. Checks and updates albus and shaggy, reads the last pull requests of Heimdall and Neptune, and gives a very short Quoi de neuf with a question for each change worth reusing."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Auto update: before working again on a project,
     ┌─┴───┴─┐       check what moved in the libraries and the projects.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# AUTO UPDATE

I work on several projects at once (Heimdall on Torch, Neptune on Lucia), with one Claude session per project. The
libraries they share (`albus`, `shaggy`) change often, and so do the projects. Before
working again after a while, each session catches up, for two goals:

- **Same libraries everywhere**: the project environment always runs the latest `albus` and `shaggy`.
- **The best of both projects**: Heimdall and Neptune share most of their design (encoders, losses, training). Each
  session reads what was done in the other project, and proposes to bring here what would help.

| File                 | Use                                                                    | When                   |
| -------------------- | ---------------------------------------------------------------------- | ---------------------- |
| `check.py`           | **Run** `python <skill folder>/check.py` with the Python of the project environment | § 0 to § 3, § 5 |
| `hooks/auto-update.py`| runs by itself on every message (plugin hook), never by hand           | reminds you every 6 h  |

Related: the `research` skill for what albus and shaggy contain; `cluster-torch` and `cluster-lucia` for where to install.

**Contents**

0. In short
1. When
2. Libraries
3. Pull requests
4. What to tell me
5. Versions next to every result

---

## 0. IN SHORT

1. **Run** `python <skill folder>/check.py --since <time of the last check>` with the Python of the **project
   environment** (standard library only, Python 3.6 or later, 3.8 or later to compare the libraries; it reads the
   public GitHub API without any token). Only in a folder of Heimdall, Neptune, albus or shaggy: anywhere else,
   skip this skill.
2. **A library is behind** → update it in the environment (§ 2), unless a job uses the environment or the project
   pins a commit.
3. **Read** the last 3 pull requests of Heimdall and Neptune, to know what was done on the other side (§ 3).
4. **Tell** me in a very short "Quoi de neuf", with **one short question** per change of the other project that
   could help here (§ 4), then answer my message.
5. **Write the versions** (`python <skill folder>/check.py --versions`) next to every result: report, run, log (§ 5).

---

## 1. WHEN

- The hook `auto-update.py` of this plugin adds a reminder to the first message of a session in a folder of Heimdall,
  Neptune, albus or shaggy (found from its git remote) when it was not brought up to date for **6 hours** or more (time in UTC kept in `~/.claude/up-to-date/<folder>.txt`, written when
  reminding, so the reminder comes only once). It gives the time of the last check, to pass to `--since`.
- The check is quick (a few seconds); I change the libraries often, so do it every time it is asked.
- Also when I ask what changed, or before a task that relies on the latest version of a library.
- Not for scheduled or automatic messages, nor in the middle of a task: do it at the first natural pause.

---

## 2. LIBRARIES

`check.py` compares the commit each library was installed from (`direct_url.json` of pip) with its branch on GitHub
(`albus@main`, `shaggy@master`), and lists the commits and the files changed in between.

**Find the environment** in the `CLAUDE.md` of the project (overlay on Torch, micromamba on Lucia, ...). No
environment in the folder → run `python3 <skill folder>/check.py --no-libraries` and skip this section.

**Updating `albus` and `shaggy` this way is pre-approved** (no need to ask); any other install still needs my
approval. **Update only when all hold**, otherwise say why it was not done:

| Condition                                  | Check                                                                     |
| ------------------------------------------ | ------------------------------------------------------------------------- |
| The library is behind                      | `check.py` says `BEHIND`                                                  |
| The project follows the branch             | the requirements say `@main` / no commit; a pinned commit stays as it is |
| No job of mine uses the environment        | `squeue -u $USER` and the command of the jobs (`scontrol show job <id>`)  |

**How** (`--no-deps` leaves torch and the other packages untouched):

```bash
pip install --no-deps --force-reinstall git+https://github.com/VikVador/<library>@<branch>
pip check                                          # a new dependency? install it, then check again
python -c "import albus, shaggy"                   # the environment still imports
```

| Cluster | Where to run it                                                                                                  |
| ------- | ---------------------------------------------------------------------------------------------------------------- |
| Torch   | in a short CPU job, overlay mounted `:rw` with `--fakeroot` (login nodes: 2 GB), read the `cluster-torch` skill first:   |
|         | `srun --account=torch_pr_347_general -c4 --mem=16G -t0:30:00 apptainer exec --fakeroot --overlay <overlay>:rw <image> bash -c "source /ext3/env.sh; pip ..."` |
| Lucia   | in the micromamba environment of the project, read the `cluster-lucia` skill first                                       |
| Other   | in the environment named by the `CLAUDE.md` of the project                                                       |

Then run `check.py` again with the environment mounted read-only: it must say `up to date`.

**When the public API of a library changed** (new module, function renamed or removed, see the files changed): check
that its description in § 3 of the `research` skill still holds; if not, propose the change to me, then make it in
a clone of VikVador/Claude through a pull request.

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
- Read only: never comment, review, approve or merge, and never port a change without my answer.

---

## 4. WHAT TO TELL THE USER

Before answering my message, a block in my language, in the long format of the `auto-message-format` skill (after
the recap of a dictated message, if any):

- title and summary: e.g. **Quoi de neuf depuis le 1er novembre :**, then 1 to 2 lines: the libraries (updated, or
  why not) and the main news; then `**État :**`;
- one numbered point per thing worth knowing: a library updated (from which commit to which, docs only or code), a
  pull request merged or opened (number, one sentence), and what it changes for the current project, if anything;
- for each change of the other project that could help here, **one question** naming its point: clear, simple,
  concise, saying what changed there and why it would help here, e.g.

  > ❓ **(2)** Neptune #38 retire la mise à l'échelle σ/τ des distances de la GME pour l'océan : l'encodeur océan
  > n'apprenait plus avec. Heimdall l'a encore pour les observations ; on teste sans aussi ? (oui / non)

  At most 3 questions, the most useful first; none when nothing applies.

Nothing changed → the short format ("**Quoi de neuf :** tout est à jour : albus, shaggy, aucune nouvelle PR.").
Then answer the message.
Never present as done an update that was not run and checked.

---

## 5. VERSIONS NEXT TO EVERY RESULT

The libraries now change under the experiments: the same command can give another number after an update. To tell a
change of the code from a change of a library, every result says which commits it was made with.

- `python <skill folder>/check.py --versions` (Python of the project environment, no network) prints e.g.
  `albus 32ebf6b, shaggy 6095950`.
- **Reports**: this line at the bottom of the page (`<p class="versions">`, see the `create-report` skill).
- **Runs**: in the configuration logged with the run (WandB config, saved `config.yml`) and at the top of the log.
- **Comparing two results** made with different versions: say it, and check the commits in between before blaming
  the model.
