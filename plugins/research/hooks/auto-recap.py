r"""Hook on every prompt: when the message looks dictated, remind Claude to recap what it understood first."""

import json
import re
import sys

# fmt: off
#
# ----- A dictated message: long, unformatted, with spoken filler words
#
MIN_CHARACTERS = 600
MAX_LINE_BREAKS = 3
MIN_FILLERS = 3
FILLERS = r"\b(donc|en fait|bah|ben|genre|voilà|du coup|euh|ok|okay|enfin|tu vois|so|basically|you know|like i said)\b"
FORMATTING = r"^\s*([-*•>#]|\d+[.)])\s|```"
# fmt: on

REMINDER = (
    "This message looks dictated (long, no formatting, spoken style). Follow the auto-recap skill: before anything "
    "else, reply with a very short recap of what you understood of the request (not of what you plan to do), in the "
    "compact style: bold title, ---, 2 to 4 plain lines, ---, one short bullet per thing asked. Then start working "
    "at once, without waiting for a confirmation."
)


def is_dictated(prompt: str) -> bool:
    r"""Tell whether a message looks dictated rather than typed.

    Arguments:
        prompt : Text of the message.

    Returns:
        dictated : Whether the message is long, unformatted and spoken in style.
    """
    if prompt.lstrip().startswith(("/", "<")) or len(prompt) < MIN_CHARACTERS:
        return False
    if prompt.count("\n") > MAX_LINE_BREAKS or re.search(FORMATTING, prompt, re.M):
        return False
    return len(re.findall(FILLERS, prompt, re.I)) >= MIN_FILLERS


def main() -> None:
    try:
        prompt = json.load(sys.stdin).get("prompt", "")
    except (json.JSONDecodeError, AttributeError):
        return
    if is_dictated(prompt):
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": REMINDER}}))


if __name__ == "__main__":
    main()
