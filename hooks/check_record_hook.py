#!/usr/bin/env python3
# hooks/check_record_hook.py
"""PostToolUse hook: structurally validate a record file the agent writes.

Runs instruments/check_record.py on each written file and feeds findings back
via exit 2 + stderr (PostToolUse cannot block — the file is already written;
after-the-fact feedback is the design).

Two hosts, two payload shapes. Claude Code's Write and Edit tools name the
file in `tool_input.file_path`. Codex routes file edits through `apply_patch`
and hands the hook the patch text in `tool_input.command`, so the paths are
read off its `*** Add File:` / `*** Update File:` / `*** Move to:` lines and
resolved against the payload's `cwd`. A record created by a shell command is
covered by neither shape and is not validated; README § Live record validation
says so.

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

PATCH_PATH = re.compile(r"^\*\*\* (?:Add File|Update File|Move to): (.+?)\s*$", re.M)

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


def candidate_paths(payload: dict) -> list[str]:
    """The files this tool call wrote, from whichever payload shape the host
    sent. Relative paths in a patch are relative to the payload's `cwd`."""
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return []
    file_path = tool_input.get("file_path")
    if file_path:
        return [str(file_path)]
    command = tool_input.get("command")
    if not isinstance(command, str) or not command.lstrip().startswith("*** Begin Patch"):
        return []
    base = Path(str(payload.get("cwd") or Path.cwd()))
    seen: list[str] = []
    for raw in PATCH_PATH.findall(command):
        path = os.path.normpath(base / raw)
        if path not in seen:
            seen.append(path)
    return seen


def plugin_root() -> str | None:
    """Claude Code sets CLAUDE_PLUGIN_ROOT; Codex sets PLUGIN_ROOT."""
    return os.environ.get("CLAUDE_PLUGIN_ROOT") or os.environ.get("PLUGIN_ROOT")


def unavailable(file_path: str, why: str) -> int:
    print(
        f"data-reasoning: the record at {file_path} was not validated ({why}).\n"
        f"Not validated is not a clean pass. Validator terms: {DECISION}",
        file=sys.stderr,
    )
    return 2


def check_one(file_path: str) -> int:  # noqa: PLR0911
    if not file_path.endswith(".md"):
        return 0
    sniff = looks_like_record(file_path)
    if sniff is None:
        return unavailable(file_path, "the file could not be read")
    if not sniff:
        return 0
    root = plugin_root()
    if not root:
        return unavailable(file_path, "CLAUDE_PLUGIN_ROOT and PLUGIN_ROOT are unset")
    validator = Path(root) / "instruments" / "check_record.py"
    if not validator.is_file():
        return unavailable(file_path, "validator missing from the plugin install")
    try:
        result = subprocess.run(
            [sys.executable, str(validator), file_path],
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


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return 0
    if not isinstance(payload, dict):
        return 0
    # One patch can write several files; every record among them is reported,
    # and one finding anywhere is the hook's exit code.
    return max((check_one(path) for path in candidate_paths(payload)), default=0)


if __name__ == "__main__":
    sys.exit(main())
