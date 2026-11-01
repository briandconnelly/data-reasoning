#!/usr/bin/env python3
"""Fail when a new run record has no `Scorer:` line.

skills/hypothesis-driven-analysis/tests/PROTOCOL.md § Who scored it owns the
rule; this script only enforces it.

A record passes only when a visible `Scorer:` line (not inside a ``` / ~~~
fence or an HTML comment) appears in its preamble, before the first table
line (one starting with `|`). That is necessary, not sufficient, for
PROTOCOL's "directly under its date line": placement relative to the date
line is not checked.
"""

import re
import sys
from datetime import date
from pathlib import Path

SINCE = date(2026, 11, 1)
DATE_PREFIX = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")
SCORER_LINE = re.compile(r"^Scorer: \S")
ONE_LINE_COMMENT = re.compile(r"^\s*(<!--.*?-->\s*)+$")
REPO = Path(__file__).resolve().parent.parent


def record_date(path: Path) -> date | None:
    m = DATE_PREFIX.match(path.name)
    if not m:
        return None
    try:
        return date(*map(int, m.groups()))
    except ValueError:
        return None


def has_preamble_scorer(text: str) -> bool:
    """A visible `Scorer:` line appears before the first table line."""
    fenced = commented = False
    for line in text.splitlines():
        if commented:
            commented = "-->" not in line
            continue
        if line.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.startswith("|"):
            return False
        if ONE_LINE_COMMENT.match(line):
            continue
        opened = line.rfind("<!--")
        if opened != -1 and "-->" not in line[opened:]:
            commented = True
            continue
        if SCORER_LINE.match(line):
            return True
    return False


def missing_scorer(paths: list[Path], since: date = SINCE) -> list[Path]:
    """Records that must carry a Scorer line and do not.

    An undated record (no leading ``YYYY-MM-DD``) is always an offender: it
    cannot be shown to predate the cutoff, so it is never silently skipped.
    """
    out = []
    for p in paths:
        d = record_date(p)
        if d is None:
            out.append(p)
            continue
        if d < since:
            continue
        if not has_preamble_scorer(p.read_text(encoding="utf-8")):
            out.append(p)
    return out


def default_record_paths() -> list[Path]:
    """Run records in both skill trees: shipped `skills/` and `.agents/skills/`."""
    return sorted(
        {
            *REPO.glob("skills/*/tests/runs/*.md"),
            *REPO.glob(".agents/skills/*/tests/runs/*.md"),
        }
    )


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv] or default_record_paths()
    bad = missing_scorer(paths)
    for p in bad:
        label = "UNDATED RUN RECORD" if record_date(p) is None else "MISSING SCORER"
        print(f"{label}: {p}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
