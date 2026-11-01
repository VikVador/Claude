#!/bin/bash
# At the start of the claude-remote session, forgets the last prompt time so the first prompt asks about the phone.
# CLAUDE_REMOTE is set by claude-remote; CLAUDE_PHONE by its former name, claude-phone
[ "${CLAUDE_REMOTE:-${CLAUDE_PHONE:-}}" = "1" ] || exit 0
rm -f "$HOME/.claude/phone/last-prompt"
