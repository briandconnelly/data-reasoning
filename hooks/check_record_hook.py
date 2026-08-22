#!/usr/bin/env python3
# hooks/check_record_hook.py
"""PostToolUse hook: structurally validate any record file the agent writes.

Runs instruments/check_record.py on the written file and feeds findings back
via exit 2 + stderr (PostToolUse cannot block — the file is already written;
after-the-fact feedback is the design).

Whether this hook's output is agent-read prose, and what it therefore owes,
is settled by the decision record named below; this file does not restate it.

Exit codes: 0 non-record file or clean record; 2 record with findings
(printed to stderr), validator missing/broken/timed-out, or candidate file
unreadable. Garbled stdin exits 0: there is no file to validate.

Failure semantics are owned by
skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md;
this file enacts them.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SIGNATURES = (
    "# Investigation: ",
    "# Exploration: ",
    "# Identification Review: ",
    "# Decision Record: ",
    "# VoI Record: ",
)

DECISION = (
    "skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md"
)


def looks_like_record(path: str) -> bool | None:
    """True: title signature matches. False: it does not. None: unreadable."""
    try:
        with Path(path).open(encoding="utf-8", errors="replace") as f:
            head = f.read(4096)
    except OSError:
        return None
    first = head.lstrip().split("\n", 1)[0]
    return first.startswith(SIGNATURES)


def unavailable(file_path: str, why: str) -> int:
    print(
        f"data-reasoning: the record at {file_path} was not validated ({why}).\n"
        f"Not validated is not a clean pass. Validator terms: {DECISION}",
        file=sys.stderr,
    )
    return 2


def main() -> int:  # noqa: PLR0911
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return 0
    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path or not str(file_path).endswith(".md"):
        return 0
    sniff = looks_like_record(str(file_path))
    if sniff is None:
        return unavailable(file_path, "the file could not be read")
    if not sniff:
        return 0
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if not plugin_root:
        return unavailable(file_path, "CLAUDE_PLUGIN_ROOT is unset")
    validator = Path(plugin_root) / "instruments" / "check_record.py"
    if not validator.is_file():
        return unavailable(file_path, "validator missing from the plugin install")
    try:
        result = subprocess.run(
            [sys.executable, str(validator), str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (subprocess.SubprocessError, OSError) as exc:
        return unavailable(file_path, f"validator failed to run: {exc}")
    if result.returncode == 0:
        return 0
    if result.returncode == 1:
        print(
            f"data-reasoning: the record at {file_path} has structural findings:\n"
            f"{result.stdout}"
            f"Closed vocabularies live in the owning SKILL.md; the check's scope is {DECISION}",
            file=sys.stderr,
        )
        return 2
    # Validator exit 2: either the file is unreadable (it says so on stderr),
    # which is not a clean pass, or the signature matched but no required
    # heading did — a user's own note, not a record — which is silence.
    if result.stderr.startswith("unreadable"):
        return unavailable(file_path, "validator could not read the file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
