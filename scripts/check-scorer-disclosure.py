#!/usr/bin/env python3
"""Fail when a new run record has no `Scorer:` line.

skills/hypothesis-driven-analysis/tests/PROTOCOL.md § Who scored it owns the
rule; this script only enforces it.
"""

import re
import sys
from datetime import date
from pathlib import Path

SINCE = date(2026, 11, 1)
DATE_PREFIX = re.compile(r"^(\d{4})-(\d{2})-(\d{2})")
SCORER_LINE = re.compile(r"^Scorer: \S", re.MULTILINE)
REPO = Path(__file__).resolve().parent.parent


def record_date(path: Path) -> date | None:
    m = DATE_PREFIX.match(path.name)
    if not m:
        return None
    try:
        return date(*map(int, m.groups()))
    except ValueError:
        return None


def missing_scorer(paths: list[Path], since: date = SINCE) -> list[Path]:
    out = []
    for p in paths:
        d = record_date(p)
        if d is None or d < since:
            continue
        if not SCORER_LINE.search(p.read_text(encoding="utf-8")):
            out.append(p)
    return out


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv] or sorted(REPO.glob("skills/*/tests/runs/*.md"))
    bad = missing_scorer(paths)
    for p in bad:
        print(f"MISSING SCORER: {p}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
