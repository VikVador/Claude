r"""Hook on every prompt: when a project folder was not brought up to date for a while, remind Claude to do it."""

import datetime
import json
import re
import sys
from pathlib import Path

# fmt: off
#
# ----- How often a project folder is brought up to date, and where the time of the last reminder is kept (UTC)
#
HOURS  = 6
STAMPS = Path.home() / ".claude" / "up-to-date"
# fmt: on

REMINDER = (
    "This project folder was {last}. Follow the up-to-date skill before answering: "
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


def main() -> None:
    try:
        data = json.load(sys.stdin)
        folder, prompt = data.get("cwd", ""), data.get("prompt", "")
    except (json.JSONDecodeError, AttributeError):
        return
    if prompt.lstrip().startswith("/"):
        return

    stamp = stamp_of(folder)
    now = datetime.datetime.now(datetime.timezone.utc).replace(
        tzinfo=None, second=0, microsecond=0
    )
    try:
        last = datetime.datetime.fromisoformat(stamp.read_text().strip())
    except (OSError, ValueError):
        last = None
    if last is not None and now - last < datetime.timedelta(hours=HOURS):
        return

    # The time is written when reminding, so that the reminder comes once and not at every message
    stamp.parent.mkdir(parents=True, exist_ok=True)
    stamp.write_text(now.isoformat(timespec="minutes"))
    since = last.isoformat(timespec="minutes") if last else ""
    reminder = REMINDER.format(
        last=f"last brought up to date on {since} UTC" if last else "never brought up to date",
        since=f" --since {since}" if last else "",
    )
    output = {"hookEventName": "UserPromptSubmit", "additionalContext": reminder}
    print(json.dumps({"hookSpecificOutput": output}))


if __name__ == "__main__":
    main()
