"""Helpers the representative-v1 validators share: regenerate and byte-compare."""

from __future__ import annotations

import filecmp
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def regenerated_matches(fixture: Path, builder: Callable[[Path], None]) -> list[str]:
    """Rebuild with the committed seed into a tempdir; name any file that differs."""
    problems = []
    with tempfile.TemporaryDirectory() as tmp:
        fresh = Path(tmp) / fixture.name
        builder(fresh)
        names = sorted({p.name for p in fresh.iterdir()} | {p.name for p in fixture.iterdir()})
        for name in names:
            a, b = fixture / name, fresh / name
            if not (a.exists() and b.exists() and filecmp.cmp(a, b, shallow=False)):
                problems.append(
                    f"{name}: committed bytes differ from a fresh build with the committed seed"
                )
    return problems


def report(name: str, problems: list[str], facts: dict[str, object]) -> int:
    for k, v in facts.items():
        print(f"{name}: {k} = {v}")
    for p in problems:
        print(f"{name}: FAIL {p}")
    if not problems:
        print(f"{name}: ok")
    return 1 if problems else 0
