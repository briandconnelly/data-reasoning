"""The record template's slot labels must equal check_decision.py's, as sets.

`references/decision-record-template.md` is the agent-facing statement of the
record's shape; `check_decision.py` is the operable one. The slot labels live
in both -- a template is read, a checker runs -- so this check keeps the two
sets from diverging silently, in either direction: a template-only label the
checker never enforces, or a checker label the template no longer shows.
The checker-side set is its DECIDE_LABELS/VOI_LABELS constants, which
_require_slots actually iterates, so every label asserted here is enforced.
"""

import re
from pathlib import Path

from check_decision import DECIDE_LABELS, VOI_LABELS

TEMPLATE = Path(__file__).resolve().parents[1] / "references" / "decision-record-template.md"

# A top-level `- <label>:` bullet inside the template's record skeletons;
# the trailing colon is part of the label to match the checker constants.
_TEMPLATE_BULLET = re.compile(r"^- ([^<\n]+?:)")


def checker_labels() -> set[str]:
    labels: set[str] = set()
    for section_labels in (*DECIDE_LABELS.values(), *VOI_LABELS.values()):
        labels.update(section_labels)
    return labels


def template_labels() -> set[str]:
    labels: set[str] = set()
    for line in TEMPLATE.read_text(encoding="utf-8").splitlines():
        m = _TEMPLATE_BULLET.match(line)
        if m:
            labels.add(m.group(1).strip())
    return labels


def test_extractors_surface_known_positives():
    assert "Prior odds:" in checker_labels()
    assert "Prior odds:" in template_labels()
    assert len(template_labels()) > 10  # noqa: PLR2004


def test_label_sets_are_equal():
    assert checker_labels() == template_labels()
