#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""The binding-rules hoist as a program, so the move is verbatim by construction.

    uv run hoist.py <pre SKILL.md> <out>

Reads the pre-edit SKILL.md, removes the preregistered sentences from
`### Conclusion` by exact line match, inserts them in their original order
under a new `## Binding rules` section placed before `## Routing`, and leaves
the preregistered pointer sentence where each moved group stood. Every moved
line must occur exactly once in the source, or the script exits non-zero; the
only new lines are SCOPE, the heading, the pointers, and blank separators.
`check` mode re-verifies an edited file: every moved line occurs exactly once,
inside § Binding rules, and nowhere in § Conclusion.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

HEADING = "## Binding rules"
SCOPE = "These rules bind every full-route conclusion; § Conclusion applies them."

# Each group: (id, line-prefixes identifying the moved lines in source order, pointer).
# A prefix must match exactly one line of the pre-edit file.
GROUPS: list[tuple[str, list[str], str]] = [
    (
        "G1 status set and derivation",
        [
            "Derive hypothesis status from the latest effective outcome",
            "The status set is closed: `REFUTED` when",
            '"Necessary" is not decided at conclusion time',
        ],
        "Status derivation and the closed status set are stated in § Binding rules.",
    ),
    (
        "G2 precedence",
        [
            "Precedence when tests disagree:",
            "- an adequate test failing the necessary prediction",
            "- a `CONTRADICTED` outcome on any non-necessary prediction",
            "- two adequate tests of the *same* necessary prediction",
        ],
        "Precedence when tests disagree is stated in § Binding rules.",
    ),
    (
        "G3 data-artifact rule",
        ["A data-artifact hypothesis is never `REFUTED` on a validity check"],
        "The rule for refuting a `data-artifact` hypothesis is stated in § Binding rules.",
    ),
    (
        "G4 SUPPORTED bar and summary table",
        [
            "`SUPPORTED` is not a status;",
            "The per-hypothesis summary table repeats",
        ],
        'The "best supported" bar and the summary-table rule are stated in § Binding rules.',
    ),
    (
        "G5 stop rule",
        [
            "Apply the precommitted stop rule:",
            "- **Conclude** when the success criterion is met",
            "- **Iterate** (return to Plan)",
            "- **Stop with limits** otherwise",
            "  When the conclusion is that nothing identifies the effect",
            "  When a decision hangs on an `UNRESOLVED` set",
        ],
        "Apply the precommitted stop rule stated in § Binding rules.",
    ),
    (
        "G6 causal wording",
        [
            "Use causal wording only when the design supports a counterfactual",
            "Controlling the intervention is not identifying its effect",
            "Observational adjustment does not clear the bar either",
            "A quasi-experimental design clears the bar only through",
            "Absent such a design, associative language is mandatory",
        ],
        "Causal wording is governed by the bar stated in § Binding rules.",
    ),
    (
        "G7 numeric confidence",
        [
            "Do not invent numeric confidence values.",
            "A `decision-analysis` record's provenance-classed numbers",
        ],
        "The numeric-confidence rule is stated in § Binding rules.",
    ),
    (
        "G8 report order",
        ["Report the answer first, then the per-hypothesis evidence summary"],
        "Report in the order § Binding rules states.",
    ),
]

# Lines that are list blocks keep their blank-line framing in the new section.
LIST_LEADS = {"Precedence when tests disagree:", "Apply the precommitted stop rule:"}


def find(lines: list[str], prefix: str, lo: int, hi: int) -> int:
    hits = [i for i in range(lo, hi) if lines[i].startswith(prefix)]
    if len(hits) != 1:
        sys.exit(f"prefix {prefix!r}: {len(hits)} matches in Conclusion, need exactly 1")
    return hits[0]


def section_bounds(lines: list[str], heading: str) -> tuple[int, int]:
    start = lines.index(heading)
    level = heading.split(" ")[0]
    end = next(
        (
            i
            for i in range(start + 1, len(lines))
            if lines[i].startswith("#") and len(lines[i].split(" ")[0]) <= len(level)
        ),
        len(lines),
    )
    return start, end


def hoist(src: str) -> str:
    lines = src.split("\n")
    c_lo, c_hi = section_bounds(lines, "### Conclusion")
    moved_idx: list[list[int]] = []
    for _gid, prefixes, _ptr in GROUPS:
        moved_idx.append([find(lines, p, c_lo, c_hi) for p in prefixes])

    # Build the new section from the moved lines, original order, original bytes.
    block: list[str] = [HEADING, "", SCOPE, ""]
    for idxs in moved_idx:
        para: list[str] = []
        for i in idxs:
            line = lines[i]
            if line in LIST_LEADS:
                if para:
                    block += para + [""]
                    para = []
                block += [line, ""]
            else:
                para.append(line)
        block += para + [""]
    # Merge adjacent prose groups the way the source ran them together:
    # G6, G7, G8 were one paragraph; keep it so.
    text_block = "\n".join(block)
    for a, b in [
        (
            "associative language is mandatory and the limitations name which of those "
            "threats remain open.\n\nDo not invent",
            "associative language is mandatory and the limitations name which of those "
            "threats remain open.\nDo not invent",
        ),
        (
            "not confidence values invented here.\n\nReport the answer first",
            "not confidence values invented here.\nReport the answer first",
        ),
    ]:
        if a not in text_block:
            sys.exit(f"paragraph join anchor missing: {a[:40]!r}")
        text_block = text_block.replace(a, b, 1)

    # Rewrite Conclusion: first moved line of each group becomes its pointer,
    # the rest are dropped; blank lines that only framed a moved list go too.
    first = {idxs[0]: ptr for idxs, (_g, _p, ptr) in zip(moved_idx, GROUPS, strict=True)}
    drop = {i for idxs in moved_idx for i in idxs[1:]}
    out: list[str] = []
    for i, line in enumerate(lines):
        if i in first:
            out.append(first[i])
        elif i in drop:
            continue
        else:
            out.append(line)
    body = "\n".join(out)
    # The precedence list and the stop-rule list each left a blank line that
    # framed them; collapse the blanks those removals orphaned.
    body = body.replace(
        "Precedence when tests disagree is stated in § Binding rules.\n\n\n",
        "Precedence when tests disagree is stated in § Binding rules.\n",
    )
    body = body.replace(
        "Apply the precommitted stop rule stated in § Binding rules.\n\n\n",
        "Apply the precommitted stop rule stated in § Binding rules.\n\n",
    )
    anchor = "\n## Routing\n"
    if body.count(anchor) != 1:
        sys.exit("need exactly one ## Routing heading")
    return body.replace(anchor, "\n" + text_block.rstrip("\n") + "\n" + anchor, 1)


def check(path: Path, pre: Path) -> int:
    pre_lines = pre.read_text(encoding="utf-8").split("\n")
    lines = path.read_text(encoding="utf-8").split("\n")
    b_lo, b_hi = section_bounds(lines, HEADING)
    c_lo, c_hi = section_bounds(lines, "### Conclusion")
    bad = 0
    for gid, prefixes, ptr in GROUPS:
        for p in prefixes:
            src = [x for x in pre_lines if x.startswith(p)]
            hits = [i for i, x in enumerate(lines) if x == src[0]]
            where = "ok" if len(hits) == 1 and b_lo < hits[0] < b_hi else "FAIL"
            bad += where != "ok"
            print(f"{where} {gid}: {p[:50]!r} at {hits}")
        in_conc = [i for i in range(c_lo, c_hi) if lines[i] == ptr]
        bad += len(in_conc) != 1
        print(f"{'ok' if len(in_conc) == 1 else 'FAIL'} {gid}: pointer in § Conclusion")
    return 1 if bad else 0


def main() -> int:
    if sys.argv[1] == "check":
        return check(Path(sys.argv[2]), Path(sys.argv[3]))
    src = Path(sys.argv[1]).read_bytes()
    result = hoist(src.decode("utf-8"))
    Path(sys.argv[2]).write_text(result, encoding="utf-8")
    print(f"pre  sha256={hashlib.sha256(src).hexdigest()}")
    print(f"post sha256={hashlib.sha256(result.encode()).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
