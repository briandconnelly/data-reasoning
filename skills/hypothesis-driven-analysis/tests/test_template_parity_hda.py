"""The ledger template's Problem slot labels must match compare_prereg.py's.

Mirrors test_template_parity_cir.py / test_template_parity_da.py: a template
is read, a checker runs, so the labels necessarily live in both; this check
keeps them from diverging silently (AGENTS.md: one home per normative rule;
a copy gets an instrument, not trust).
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).parent
TEMPLATE = HERE.parent / "references" / "ledger-template.md"

_spec = importlib.util.spec_from_file_location("compare_prereg", HERE / "compare_prereg.py")
assert _spec is not None
assert _spec.loader is not None
compare_prereg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(compare_prereg)

_BULLET = re.compile(r"^- ([^:<]+):")


def template_problem_labels() -> set[str]:
    """Lower-cased `- Label:` names under `## Problem` in the Full Route Template."""
    text = TEMPLATE.read_text(encoding="utf-8")
    start = text.index("## Full Route Template")
    problem = text.index("\n## Problem\n", start)
    end = text.index("\n## ", problem + 1)
    labels: set[str] = set()
    for line in text[problem:end].splitlines():
        m = _BULLET.match(line)
        if m:
            labels.add(m.group(1).strip().lower())
    return labels


def test_extractor_surfaces_a_known_positive() -> None:
    assert "stop condition" in template_problem_labels()


def test_template_problem_labels_match_checker() -> None:
    assert set(compare_prereg.PROBLEM_FIELDS) == template_problem_labels()
