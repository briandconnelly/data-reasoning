#!/bin/sh
# PostToolUse entry point. With python3 available, defer to the Python hook.
# Without it, do the same record sniff in shell so a record write is reported
# as not validated (never silently passed) and every other write stays silent.
# Claude Code sets CLAUDE_PLUGIN_ROOT; Codex sets PLUGIN_ROOT.
# Failure semantics: skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md
root="${CLAUDE_PLUGIN_ROOT:-${PLUGIN_ROOT:-}}"
# Mirrors FRONTMATTER_SCAN_BYTES in hooks/check_record_hook.py.
FRONTMATTER_SCAN_BYTES=65536
if command -v python3 >/dev/null 2>&1; then
  exec python3 "${root}/hooks/check_record_hook.py"
fi
# Print a file's document title: the first non-blank line after an optional
# frontmatter block, which is the only line `looks_like_record` in the Python
# hook classifies. Scanning every heading instead would call an ordinary
# document that quotes or embeds `# Decision Record: ...` a record write, and
# the two paths must agree. Exit 3 when frontmatter is still open at the end
# of the budget: like the Python hook, an indeterminate title fails closed.
record_title() {
  head -c "$FRONTMATTER_SCAN_BYTES" "$1" | awk '
    NR == 1 && $0 == "---" { fm = 1; next }
    fm { if ($0 == "---") fm = 0; next }
    /^[[:space:]]*$/ { next }
    { print; exit }
    END { if (fm) exit 3 }
  '
}

# True when $1 is a record: its title carries a signature, or its title could
# not be determined.
has_record_title() {
  title=$(record_title "$1") || return 0
  printf '%s\n' "$title" | grep -q -E '^# (Investigation|Exploration|Identification Review|Decision Record|VoI Record): '
}

# Print the first readable .md path on stdin (one per line, relative ones
# resolved against $1) whose head carries a record title; print nothing else.
first_record_path() {
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    case "$p" in
      (*.md) ;;
      (*) continue ;;
    esac
    case "$p" in
      (/*) full="$p" ;;
      (*) full="${1:-.}/$p" ;;
    esac
    [ -r "$full" ] || continue
    if has_record_title "$full"; then
      printf '%s\n' "$full"
      return 0
    fi
  done
  return 0
}
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
  paths=$(printf '%s' "$payload" | grep -o -E '\*\*\* (Add File|Update File|Move to): [^"\\]*' | sed 's/^\*\*\* [A-Za-z ]*: //')
  # One path per line, read through a pipe: a name with spaces must stay one
  # candidate, and a here-document would need writable temporary storage,
  # which a locked-down host may not have. The reader runs in a subshell, so
  # the first record it finds comes back through the substitution.
  hit=$(printf '%s\n' "$paths" | first_record_path "$cwd")
  if [ -n "$hit" ]; then
    printf 'data-reasoning: the record at %s was not validated (python3 is not on PATH).\nNot validated is not a clean pass. Validator terms: skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md\n' "$hit" >&2
    exit 2
  fi
  # A record title inside the patch text counts only as an added line
  # (`\n+# Title: `, JSON-escaped) belonging to a Markdown file's own
  # operation. The command string is extracted with grep -E (alternation is
  # portable there, not in sed's basic regex); each `*** ` marker is then
  # moved to its own line, so one line is one file operation with its hunk
  # still JSON-escaped, and the title is looked for only on lines whose
  # operation names a .md file. A title added to a Python file, or quoted in
  # source, is not a record, whatever else the patch touches.
  command=$(printf '%s' "$payload" | grep -o -E '"command"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"' | head -n 1 | sed 's/^"command"[[:space:]]*:[[:space:]]*"//; s/"$//')
  if printf '%s' "$command" | sed 's/\\n\*\*\* /\
*** /g' | grep -E '^\*\*\* (Add File|Update File|Move to): [^\\]*\.md\\n' | grep -q -E '\\n\+# (Investigation|Exploration|Identification Review|Decision Record|VoI Record): '; then
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
if has_record_title "$file_path"; then
  printf 'data-reasoning: the record at %s was not validated (python3 is not on PATH).\nNot validated is not a clean pass. Validator terms: skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md\n' "$file_path" >&2
  exit 2
fi
exit 0
