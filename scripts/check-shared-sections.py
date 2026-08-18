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


def extract_section(text: str, heading: str) -> str:
    """Return the exact byte slice from `heading` to the next same-or-higher
    heading outside code fences (boundary blank lines included)."""
    lines = text.split("\n")
    level = len(heading) - len(heading.lstrip("#"))
    boundary = re.compile(rf"^#{{1,{level}}} ")
    start = None
    fenced = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
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
            golden.write_text(block.rstrip("\n") + "\n", encoding="utf-8")
            continue
        if not golden.exists():
            print(f"ERROR: missing golden {golden}; run --update {slug} once", file=sys.stderr)
            return 2
        golden_content = golden.read_text(encoding="utf-8")
        normalized_block = block.rstrip("\n") + "\n"
        if golden_content != normalized_block:
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
