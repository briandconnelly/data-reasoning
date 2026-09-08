#!/usr/bin/env python3
"""Render the shared authorization gate; freeze the reworded shared sections.

Two mechanisms live here, because the two kinds of shared text differ.

The authorization gate is byte-identical in all four skills, so it has one
home -- scripts/shared-sections/authorization-gate.md -- and each SKILL.md
carries a rendered copy between marker comments. --render writes the
authority into every carrier; the default run checks that each rendered copy
still matches it and is still visible to a reader (not fenced, not commented
out). Skills install standalone, so a carrier cannot point at another file at
read time; rendering is what keeps the shipped copies from being hand-edited.

The costly-collection and data-rules sections are deliberately reworded per
skill, so they cannot be compared to one authority;
skills/exploratory-data-analysis/decisions/001-shared-gate-authority.md
instead enumerates the invariants each copy must preserve. For those, this
checker is a change detector: each copy is frozen against a golden file, so
any edit fails here and the failure message routes the editor to the
invariant list. Refreshing a golden (--update <slug>) is an explicit,
diff-visible act; whether the invariant re-check happened stays a review
question, per the decision.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

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

# The rendered authorization gate: one authority file, one marker pair per
# carrier. skills/hypothesis-driven-analysis/decisions/
# 007-shared-text-is-rendered-not-copied.md records why.
GATE_NAME = "authorization-gate"
GATE_AUTHORITY = "scripts/shared-sections/authorization-gate.md"
GATE_CARRIERS = [
    "hypothesis-driven-analysis",
    "exploratory-data-analysis",
    "causal-identification-review",
    "decision-analysis",
]
GATE_DECISION = (
    "skills/hypothesis-driven-analysis/decisions/007-shared-text-is-rendered-not-copied.md"
)

# Exit codes: 1 is drift a maintainer resolves by editing; 2 is a fault the
# checker cannot act on at all (a bad argument, an unreadable file, a marker
# pair that is missing, duplicated, or hidden).
DRIFT_CODE = 1
FAULT_CODE = 2

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


def visible_indices(lines: list[str]) -> Iterator[int]:
    """Indices of the lines an agent reads as instruction: everything not
    inside a fenced block and not inside an HTML comment.

    One pass tracks both hidden-text states so neither can hide the other's
    delimiters. Per CommonMark a fence closes only on a run of the same
    character at least as long as the opener with nothing but whitespace after
    it, `<!--` inside a fence is code, and a comment opened and never closed
    runs to the end of the document. A line that opens either state is itself
    withheld, so a one-line comment such as a marker stays visible while a
    `<!--` that opens a block does not.
    """
    fence: tuple[str, int] | None = None
    commented = False
    for i, line in enumerate(lines):
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
        yield i


def extract_section(text: str, heading: str) -> str:
    """Return the exact byte slice from `heading` to the next same-or-higher
    heading outside code fences (boundary blank lines included)."""
    lines = text.split("\n")
    level = len(heading) - len(heading.lstrip("#"))
    boundary = re.compile(rf"^#{{1,{level}}} ")
    start = None
    for i in visible_indices(lines):
        line = lines[i]
        if start is None:
            if line == heading:
                start = i
            continue
        if boundary.match(line):
            return "\n".join(lines[start:i]) + "\n"
    if start is None:
        raise ValueError(f"heading not found: {heading!r}")
    return "\n".join(lines[start:]) + "\n"


def marker_bounds(text: str, name: str) -> tuple[int, int]:
    """Line indices of the one visible `<!-- shared: name -->` marker pair.

    Markers hidden inside a fence or an HTML comment are not found, so a gate
    that a reader never sees is an error rather than a silent pass.
    """
    lines = text.split("\n")
    opener = f"<!-- shared: {name} -->"
    closer = f"<!-- /shared: {name} -->"
    opens = [i for i in visible_indices(lines) if lines[i].strip() == opener]
    closes = [i for i in visible_indices(lines) if lines[i].strip() == closer]
    if len(opens) != 1 or len(closes) != 1:
        raise ValueError(
            f"expected exactly one visible {opener} ... {closer} pair, "
            f"found {len(opens)} opener(s) and {len(closes)} closer(s)"
        )
    if closes[0] <= opens[0]:
        raise ValueError(f"{closer} precedes {opener}")
    return opens[0], closes[0]


def extract_marked(text: str, name: str) -> str:
    """Return the exact byte slice between the one visible marker pair."""
    start, end = marker_bounds(text, name)
    return "\n".join(text.split("\n")[start + 1 : end]) + "\n"


def replace_marked(text: str, name: str, body: str) -> str:
    """Return `text` with the slice between the marker pair replaced by `body`."""
    lines = text.split("\n")
    start, end = marker_bounds(text, name)
    return "\n".join(lines[: start + 1] + body.split("\n")[:-1] + lines[end:])


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


def run_gate(repo: Path, render: bool) -> int:
    """Check (or, with `render`, rewrite) every carrier's authorization gate.

    Returns 0 when every carrier matches the authority, 1 on drift, and 2 when
    the authority itself is unreadable or hidden, or a carrier's marker pair is
    missing, duplicated, or hidden -- structural faults the checker cannot
    resolve on its own.
    """
    authority_path = repo / GATE_AUTHORITY
    try:
        authority = authority_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: {authority_path}: {exc}", file=sys.stderr)
        return FAULT_CODE
    if not authority.endswith("\n"):
        print(f"ERROR: {authority_path}: must end with a newline", file=sys.stderr)
        return FAULT_CODE
    # The carriers' markers are checked for visibility, but a hidden authority
    # defeats that: fence its body and every carrier still matches it byte for
    # byte, with all four gates rendered as sample text. Check before either
    # comparing or rendering, so neither path can accept it.
    authority_lines = authority.split("\n")
    visible = set(visible_indices(authority_lines))
    hidden = [i for i, line in enumerate(authority_lines) if i not in visible and line.strip()]
    if hidden:
        print(
            f"ERROR: {authority_path}: line {hidden[0] + 1} is hidden from a reader "
            f"(inside a code fence or an HTML comment); the gate must be instruction, "
            f"not sample text.",
            file=sys.stderr,
        )
        return FAULT_CODE
    # Read and locate every marker pair before writing any of them, so a fault
    # in the last carrier cannot leave the first three rendered and the run
    # failed -- a half-applied render is worse than no render.
    carriers = []
    for skill in GATE_CARRIERS:
        skill_md = repo / "skills" / skill / "SKILL.md"
        try:
            text = skill_md.read_text(encoding="utf-8")
            block = extract_marked(text, GATE_NAME)
        except (OSError, ValueError) as exc:
            print(f"ERROR: {skill_md}: {exc}", file=sys.stderr)
            return FAULT_CODE
        carriers.append((skill, skill_md, text, block))
    failures = 0
    for skill, skill_md, text, block in carriers:
        if block == authority:
            continue
        if render:
            skill_md.write_text(replace_marked(text, GATE_NAME, authority), encoding="utf-8")
            continue
        failures += 1
        print(
            f"DRIFT: {skill}/SKILL.md authorization gate differs from {GATE_AUTHORITY}.\n"
            f"  The gate text has one home; edit that file, then run "
            f"scripts/check-shared-sections.py --render.\n"
            f"  See {GATE_DECISION}.",
            file=sys.stderr,
        )
    return DRIFT_CODE if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # --update refreshes a reworded section's golden; --render rewrites the
    # gate from its authority. They act on different mechanisms, and asking
    # for both in one run would leave which one ran to argument order.
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--update",
        nargs="+",
        default=[],
        metavar="SLUG",
        help="refresh the named golden(s), or 'all'",
    )
    mode.add_argument(
        "--render",
        action="store_true",
        help="write the authorization-gate authority into every carrier's SKILL.md",
    )
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    if args.render:
        return run_gate(repo_root, render=True)
    sections = run(repo_root, update=frozenset(args.update))
    if sections == FAULT_CODE:  # a usage or I/O error; the gate pass adds nothing
        return sections
    return max(sections, run_gate(repo_root, render=False))


if __name__ == "__main__":
    sys.exit(main())
