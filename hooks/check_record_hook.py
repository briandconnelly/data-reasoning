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
import re
import subprocess
import sys
from pathlib import Path

FRONTMATTER_SCAN_BYTES = 65536
_FRONTMATTER = re.compile(rb"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)

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
    """True: title signature matches. False: it does not. None: unreadable, or
    a frontmatter block whose end lies past the scan budget -- indeterminate."""
    # Read bytes and strictly decode only the title line. A replacement
    # character could mutate the signature into a non-match, exiting clean
    # without the validator ever running, so invalid UTF-8 *in the title* is
    # unreadable and fails closed. Decoding no more than the title keeps a bad
    # byte further down a non-record file from failing it closed: its title
    # already proves it is not a record.
    try:
        with Path(path).open("rb") as f:
            head = f.read(4096)
        if head.startswith(b"---"):
            # The file can disappear between the two opens, so this read shares
            # the handler above.
            with Path(path).open("rb") as f:
                head = f.read(FRONTMATTER_SCAN_BYTES)
            stripped = _FRONTMATTER.sub(b"", head, count=1)
            # No closing delimiter found. Two cases look alike and are not:
            # a short file simply opening with a horizontal rule has been seen
            # whole and is not a record, while a read that filled the whole
            # budget may hide a closing --- and a title just past it. Only the
            # second is indeterminate, and only it fails closed.
            if stripped == head and len(head) == FRONTMATTER_SCAN_BYTES:
                return None
            head = stripped
    except OSError:
        return None
    try:
        first = head.lstrip().split(b"\n", 1)[0].decode("utf-8")
    except UnicodeDecodeError:
        return None
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
        if not result.stdout.strip():
            return unavailable(file_path, f"validator exited {result.returncode}")
        print(
            f"data-reasoning: the record at {file_path} has structural findings:\n"
            f"{result.stdout}"
            f"Closed vocabularies live in the owning SKILL.md; the check's scope is {DECISION}",
            file=sys.stderr,
        )
        return 2
    if result.returncode == 2:  # noqa: PLR2004 -- 2 is the validator's documented exit code
        # Validator exit 2: unreadable (it says so on stderr) is not a clean
        # pass; a signature match with no required heading is a user's own
        # note, not a record, and is silence.
        if result.stderr.startswith("unreadable"):
            return unavailable(file_path, "validator could not read the file")
        return 0
    return unavailable(file_path, f"validator exited {result.returncode}")


if __name__ == "__main__":
    sys.exit(main())
