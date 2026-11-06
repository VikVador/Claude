r"""Hook on every prompt: when a project folder was not brought up to date for a while, remind Claude to do it.

Runs with the system python3 of every machine, down to Python 3.6 (Lucia login nodes): standard library only.
"""

import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

# fmt: off
#
# ----- How often a project folder is brought up to date, and where the time of the last reminder is kept (UTC)
#
HOURS  = 6
STAMPS = Path.home() / ".claude" / "up-to-date"
#
# ----- Only folders of these repositories are brought up to date (git remote, any case)
#
REPOSITORIES = r"github\.com[:/]VikVador/(Heimdall|Neptune|albus|shaggy)(\.git)?/?\s"
FORMAT       = "%Y-%m-%dT%H:%M"
# fmt: on

REMINDER = (
    "This project folder was {last}. Follow the auto-update skill before answering: "
    "check whether albus and shaggy in the project environment are behind GitHub (update them if so), read the "
    "last pull requests of Heimdall and Neptune (python check.py{since}), give a very short 'Quoi de "
    "neuf' first (with a short question for each change of the other project worth reusing here), then "
    "answer the message."
)


def stamp_of(folder: str) -> Path:
    r"""Give the file keeping the date of the last reminder for a project folder.

    Arguments:
        folder : Working directory of the session.

    Returns:
        stamp : Path of the file.
    """
    name = re.sub(r"[^A-Za-z0-9]+", "-", folder).strip("-") or "root"
    return STAMPS / f"{name}.txt"


def is_project(folder: str) -> bool:
    r"""Tell whether a folder belongs to one of the projects or libraries kept up to date.

    Arguments:
        folder : Working directory of the session.

    Returns:
        project : Whether one of its git remotes is in REPOSITORIES.
    """
    try:
        remotes = subprocess.run(
            ["git", "-C", folder, "remote", "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
            timeout=2,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    return re.search(REPOSITORIES, remotes + "\n", re.I) is not None


def main() -> None:
    try:
        data = json.load(sys.stdin)
        folder, prompt = data.get("cwd", ""), data.get("prompt", "")
    except (json.JSONDecodeError, AttributeError):
        return
    if prompt.lstrip().startswith(("/", "<")) or not folder or not is_project(folder):
        return

    stamp = stamp_of(folder)
    now = datetime.datetime.now(datetime.timezone.utc).replace(
        tzinfo=None, second=0, microsecond=0
    )
    try:
        last = datetime.datetime.strptime(stamp.read_text().strip()[:16], FORMAT)
    except (OSError, ValueError):
        last = None
    if last is not None and now - last < datetime.timedelta(hours=HOURS):
        return

    # The time is written when reminding, so that the reminder comes once and not at every message
    stamp.parent.mkdir(parents=True, exist_ok=True)
    stamp.write_text(now.strftime(FORMAT))
    since = last.strftime(FORMAT) if last else ""
    reminder = REMINDER.format(
        last=f"last brought up to date on {since} UTC" if last else "never brought up to date",
        since=f" --since {since}" if last else "",
    )
    output = {"hookEventName": "UserPromptSubmit", "additionalContext": reminder}
    print(json.dumps({"hookSpecificOutput": output}))


if __name__ == "__main__":
    main()
