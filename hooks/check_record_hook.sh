#!/bin/sh
# PostToolUse entry point. With python3 available, defer to the Python hook.
# Without it, do the same record sniff in shell so a record write is reported
# as not validated (never silently passed) and every other write stays silent.
# Failure semantics: skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md
if command -v python3 >/dev/null 2>&1; then
  exec python3 "${CLAUDE_PLUGIN_ROOT}/hooks/check_record_hook.py"
fi
payload=$(cat)
file_path=$(printf '%s' "$payload" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"\\]*\)".*/\1/p' | head -n 1)
case "$file_path" in
  *.md) ;;
  *) exit 0 ;;
esac
[ -r "$file_path" ] || exit 0
if head -c 4096 "$file_path" | grep -q -E '^# (Investigation|Exploration|Identification Review|Decision Record|VoI Record): '; then
  printf 'data-reasoning: the record at %s was not validated (python3 is not on PATH).\nNot validated is not a clean pass. Validator terms: skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md\n' "$file_path" >&2
  exit 2
fi
exit 0
