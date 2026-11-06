#!/bin/bash
# In the claude-remote session, asks about the phone after a 2 h break and recalls the phone style when it is on.
# CLAUDE_REMOTE is set by claude-remote; CLAUDE_PHONE by its former name, claude-phone
[ "${CLAUDE_REMOTE:-${CLAUDE_PHONE:-}}" = "1" ] || exit 0
dir="$HOME/.claude/phone"
mkdir -p "$dir"
now=$(date +%s)
previous=$(cat "$dir/last-prompt" 2>/dev/null || echo 0)
echo "$now" > "$dir/last-prompt"
if [ $((now - previous)) -gt 7200 ]; then
    echo "PHONE CHECK (remote session, first prompt or more than 2 h since the last one): before anything else (after the recap of a dictated request, if any), ask the user exactly this, on its own line: \"Es-tu sur ton téléphone ?\". Yes: run ~/.claude/hooks/phone-mode.sh on and answer in the compact style (remote skill, section 5). No: run ~/.claude/hooks/phone-mode.sh off and answer normally."
elif [ -f "$dir/mode" ]; then
    echo "PHONE MODE ON: answer in the compact style of the cluster-remote skill, section 5: bold concise title, ---, a 2-4 line plain summary, ---, one bullet per change (what changed, then why in one simple sentence); no wide tables or code blocks."
fi
