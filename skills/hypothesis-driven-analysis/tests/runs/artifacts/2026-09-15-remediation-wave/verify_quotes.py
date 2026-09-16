#!/usr/bin/env python3
"""Grep every quote in a run record against the archive it cites.

A run record cites evidence as `"<quoted text>" (<archive-file>)` or, for a
file an arm wrote, `(<name>.scratch/<file>)`. This script finds each
double-quoted span of 12+ characters that is followed by a parenthesized
archive path and checks the span occurs verbatim in that file (whitespace
normalized). PROTOCOL step 6: quote only from the archived artifact, and grep
each quote against it.

    python3 verify_quotes.py <run-record.md> [<run-record.md> ...]

Exit 1 with one line per quote that does not resolve.
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# A backslash-escaped inner quote belongs to the span, not to its end: without
# `\\.` here, a citation carrying an escaped inner quote matched only the
# suffix after the inner quote, and the material first half went unchecked.
QUOTE = re.compile(
    r"[“\"]((?:\\.|[^”\"\\]){12,}?)[”\"]\s*\(([\w./-]+(?:\.md|\.jsonl|\.json|\.txt))\)"
)
UNESCAPE = re.compile(r"\\(.)")


def text_of(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        raw = json.dumps(json.loads(raw), ensure_ascii=False)
    if path.suffix == ".jsonl":
        parts = []
        for line in raw.splitlines():
            try:
                parts.append(json.dumps(json.loads(line), ensure_ascii=False))
            except json.JSONDecodeError:
                parts.append(line)
        raw = "\n".join(parts)
    return re.sub(r"\s+", " ", raw)


def main() -> int:
    bad = 0
    total = 0
    for rec in sys.argv[1:]:
        for m in QUOTE.finditer(Path(rec).read_text(encoding="utf-8")):
            total += 1
            quote = re.sub(r"\s+", " ", UNESCAPE.sub(r"\1", m.group(1)))
            target = HERE / m.group(2)
            if not target.exists():
                print(f"{rec}: archive not found: {m.group(2)}")
                bad += 1
                continue
            if quote not in text_of(target):
                print(f"{rec}: quote not in {m.group(2)}: {quote[:80]!r}")
                bad += 1
    print(f"{total} quotes checked, {bad} unresolved")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
