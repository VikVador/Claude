r"""Hook on every prompt: remind Claude of the answer format, and to recap a dictated message first.

Runs with the system python3 of every machine, down to Python 3.6 (Lucia login nodes): standard library only.
"""

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

FORMAT = (
    "Answer in the format of the auto-message-format skill (read it once per session). Short when the user only "
    "needs an information, long when they must understand or decide. Both open with: ---, '**<a few words> :** "
    "<the message in 1 to 3 lines>', then '**État :** <✅ | ⏳ | ⛔ | 💬>' on its own line, then ---. Long adds "
    "numbered points (bold keyword, blank line between them), then ---, lettered 'Pas vérifié' / 'Note' items if "
    "any, then ---, one question per line as '❓ **(n)** ... ? (a / b)'. Not for progress lines while working, nor "
    "for the questions lists of create-slides and create-message."
)

RECAP = (
    " This message looks dictated (long, no formatting, spoken style): before anything else, reply with the recap of "
    "§ 4 of the skill (the long format without the État line: what you understood, one point per thing asked), then "
    "start working at once, without waiting for a confirmation."
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
    context = FORMAT + (RECAP if is_dictated(prompt) else "")
    output = {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": context}}
    print(json.dumps(output))  # ASCII escapes: safe under any locale of a login node


if __name__ == "__main__":
    main()
