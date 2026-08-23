#!/usr/bin/env python3
"""Freeze the shared costly-collection and data-rules sections against drift.

The authorization gate's copies are byte-parity-tested against HDA
(test_gate_parity*.py). The costly-collection and data-rules sections are
deliberately reworded per skill, so they cannot be compared to one authority;
skills/exploratory-data-analysis/decisions/001-shared-gate-authority.md
instead enumerates the invariants each copy must preserve.

This checker is a change detector for that decision: each copy is frozen
against a golden file, so any edit fails here and the failure message routes
the editor to the invariant list. Refreshing a golden (--update <slug>) is an
explicit, diff-visible act; whether the invariant re-check happened stays a
review question, per the decision.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# (skill directory, exact heading line, golden-file slug)
TARGETS = [
    (
        "hypothesis-driven-analysis",
        "### Costly collection is a modifier, not a route",
        "hda-costly-collection",
    ),
    (
        "exploratory-data-analysis",
        "### Costly collection (modifier, not a route)",
        "eda-costly-collection",
    ),
    (
        "causal-identification-review",
        "### Costly collection (modifier, not a route)",
        "cir-costly-collection",
    ),
    ("decision-analysis", "### Costly collection (modifier, not a route)", "da-costly-collection"),
    ("hypothesis-driven-analysis", "## Data Rules", "hda-data-rules"),
    ("exploratory-data-analysis", "## Data Rules", "eda-data-rules"),
    ("causal-identification-review", "## Data Rules", "cir-data-rules"),
    ("decision-analysis", "## Data Rules", "da-data-rules"),
]

DECISION = "skills/exploratory-data-analysis/decisions/001-shared-gate-authority.md"

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
BACKTICK_RUN = re.compile(r"`+")


def _opens_fence(line: str, m) -> bool:
    """A fence opener's info string may not contain a backtick when the fence
    is made of backticks (CommonMark): such a line is ordinary text."""
    return not (m.group(1)[0] == "`" and "`" in line[m.end() :])


def _shadow(line: str) -> str:
    """`line` with inline code-span interiors blanked index-for-index, so a
    `<!--` that Markdown renders as code is not read as a comment opener.
    Per CommonMark a span closes on a run of exactly the opener's length."""
    runs = [(m.start(), m.end()) for m in BACKTICK_RUN.finditer(line)]
    out = list(line)
    i = 0
    while i < len(runs):
        start, end = runs[i]
        slashes = 0
        while start - slashes - 1 >= 0 and line[start - slashes - 1] == "\\":
            slashes += 1
        opener = start + 1 if slashes % 2 else start
        width = end - opener
        if width <= 0:
            i += 1
            continue
        for j in range(i + 1, len(runs)):
            nxt_start, nxt_end = runs[j]
            if nxt_end - nxt_start == width:
                for k in range(end, nxt_start):
                    out[k] = "\x01"
                i = j + 1
                break
        else:
            i += 1
    return "".join(out)


def extract_section(text: str, heading: str) -> str:
    """Return the exact byte slice from `heading` to the next same-or-higher
    heading outside code fences (boundary blank lines included)."""
    lines = text.split("\n")
    level = len(heading) - len(heading.lstrip("#"))
    boundary = re.compile(rf"^#{{1,{level}}} ")
    start = None
    fence: tuple[str, int] | None = None
    commented = False
    for i, line in enumerate(lines):
        # One pass tracks both hidden-text states so neither can hide the
        # other's delimiters. Per CommonMark a fence closes only on a run of
        # the same character at least as long as the opener with nothing but
        # whitespace after it, and `<!--` inside a fence is code.
        if fence is not None:
            m = FENCE.match(line)
            if (
                m
                and m.group(1)[0] == fence[0]
                and len(m.group(1)) >= fence[1]
                and not line[m.end() :].strip()
            ):
                fence = None
            continue
        if commented:
            if "-->" in line:
                commented = False
            continue
        m = FENCE.match(line)
        if m and _opens_fence(line, m):
            fence = (m.group(1)[0], len(m.group(1)))
            continue
        masked = _shadow(line)
        if "<!--" in masked and "-->" not in masked:
            commented = True
            continue
        if start is None:
            if line == heading:
                start = i
            continue
        if boundary.match(line):
            return "\n".join(lines[start:i]) + "\n"
    if start is None:
        raise ValueError(f"heading not found: {heading!r}")
    return "\n".join(lines[start:]) + "\n"


def run(repo: Path, update: frozenset[str]) -> int:
    known = {slug for _, _, slug in TARGETS}
    if update and not update <= known and update != {"all"}:
        print(f"ERROR: unknown --update target(s): {sorted(update - known)}", file=sys.stderr)
        return 2
    golden_dir = repo / "scripts" / "shared-sections"
    golden_dir.mkdir(parents=True, exist_ok=True)
    failures = 0
    for skill, heading, slug in TARGETS:
        skill_md = repo / "skills" / skill / "SKILL.md"
        try:
            block = extract_section(skill_md.read_text(encoding="utf-8"), heading)
        except (OSError, ValueError) as exc:
            print(f"ERROR: {skill_md}: {exc}", file=sys.stderr)
            return 2
        golden = golden_dir / f"{slug}.md"
        if slug in update or "all" in update:
            golden.write_text(block, encoding="utf-8")
            continue
        if not golden.exists():
            print(f"ERROR: missing golden {golden}; run --update {slug} once", file=sys.stderr)
            return 2
        if golden.read_text(encoding="utf-8") != block:
            failures += 1
            print(
                f"DRIFT: {skill}/SKILL.md {heading!r} differs from {golden}.\n"
                f"  A reworded copy must preserve the invariants in {DECISION}.\n"
                f"  Re-check that list by hand, then refresh this golden with --update {slug}.",
                file=sys.stderr,
            )
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--update",
        nargs="+",
        default=[],
        metavar="SLUG",
        help="refresh the named golden(s), or 'all'",
    )
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    return run(repo_root, update=frozenset(args.update))


if __name__ == "__main__":
    sys.exit(main())
