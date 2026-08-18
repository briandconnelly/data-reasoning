#!/usr/bin/env python3
# hooks/check_record_hook.py
"""PostToolUse hook: structurally validate any record file the agent writes.

Runs instruments/check_record.py on the written file and feeds findings back
via exit 2 + stderr (PostToolUse cannot block — the file is already written;
after-the-fact feedback is the design).

This is harness-level enforcement, not agent-read prose: no SKILL.md sentence
points at the instrument, so no measured arms are owed for it.

Exit codes: 0 non-record file or clean record; 2 record with findings
(printed to stderr), validator missing/broken/timed-out, or file
unreadable/unclassifiable.

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


def looks_like_record(path: str) -> bool:
    try:
        with Path(path).open(encoding="utf-8", errors="replace") as f:
            head = f.read(4096)
    except OSError:
        return False
    first = head.lstrip().split("\n", 1)[0]
    return first.startswith(SIGNATURES)


def unavailable(file_path: str, why: str) -> int:
    print(
        f"data-reasoning: the record at {file_path} was not validated ({why}).\n"
        f"Not validated is not a clean pass; validate structure against the owning "
        f"template yourself. Validator terms: {DECISION}",
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
    if not looks_like_record(str(file_path)):
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
            f"Fix the record; closed vocabularies live in the owning SKILL.md, "
            f"and the check's scope is {DECISION}",
            file=sys.stderr,
        )
        return 2
    # exit 2 from the validator on a file the signature sniff matched:
    # it could not be read or classified, which is still not a clean pass.
    return unavailable(file_path, "validator could not read or classify the file")


if __name__ == "__main__":
    sys.exit(main())
