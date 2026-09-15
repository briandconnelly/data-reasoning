#!/bin/sh
# PostToolUse entry point. With python3 available, defer to the Python hook.
# Without it, do the same record sniff in shell so a record write is reported
# as not validated (never silently passed) and every other write stays silent.
# Claude Code sets CLAUDE_PLUGIN_ROOT; Codex sets PLUGIN_ROOT.
# Failure semantics: skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md
root="${CLAUDE_PLUGIN_ROOT:-${PLUGIN_ROOT:-}}"
if command -v python3 >/dev/null 2>&1; then
  exec python3 "${root}/hooks/check_record_hook.py"
fi
payload=$(cat)
file_path=$(printf '%s' "$payload" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"\\]*\)".*/\1/p' | head -n 1)
if [ -z "$file_path" ]; then
  # A Codex apply_patch payload carries the patch text, JSON-escaped, in
  # "command". Without Python the patch is not parsed; instead every .md path
  # it names is resolved against "cwd" and sniffed on disk, and a patch whose
  # own text carries a record title is caught even before the file exists.
  # Either way a record is reported as not validated, never passed.
  if ! printf '%s' "$payload" | grep -q 'Begin Patch'; then
    exit 0
  fi
  cwd=$(printf '%s' "$payload" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"\\]*\)".*/\1/p' | head -n 1)
  for p in $(printf '%s' "$payload" | grep -o -E '\*\*\* (Add File|Update File|Move to): [^"\\]*' | sed 's/^\*\*\* [A-Za-z ]*: //'); do
    case "$p" in
      *.md) ;;
      *) continue ;;
    esac
    case "$p" in
      /*) full="$p" ;;
      *) full="${cwd:-.}/$p" ;;
    esac
    [ -r "$full" ] || continue
    if head -c 4096 "$full" | grep -q -E '^# (Investigation|Exploration|Identification Review|Decision Record|VoI Record): '; then
      printf 'data-reasoning: the record at %s was not validated (python3 is not on PATH).\nNot validated is not a clean pass. Validator terms: skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md\n' "$full" >&2
      exit 2
    fi
  done
  if printf '%s' "$payload" | grep -q -E '# (Investigation|Exploration|Identification Review|Decision Record|VoI Record): '; then
    printf 'data-reasoning: a record written by apply_patch was not validated (python3 is not on PATH).\nNot validated is not a clean pass. Validator terms: skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md\n' >&2
    exit 2
  fi
  exit 0
fi
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
