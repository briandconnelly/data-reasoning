"""The record template's slot labels must match check_review.py's.

`references/identification-review-template.md` is the agent-facing statement
of the record's shape; `check_review.py` is the operable one. The slot labels
necessarily live in both -- a template is read, a checker runs -- so this
check keeps the two sets from diverging silently, the same way the gate-parity
tests keep the authorization-gate copies aligned (AGENTS.md: one home per
normative rule; a copy gets an instrument, not trust). Before this test, a
template edit renaming a slot ("Assumption probes" -> "Probes") left every
hook green while every record written from the amended template failed the
checker -- the exact mismatch class measurement wave 1 documented as the
checker's dominant failure mode.

The checker-side set is derived from check_review.py's source (the label
literals its slot lookups pass), not restated here, so this file adds no
third copy that could itself drift.
"""

from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).parent
TEMPLATE = HERE.parent / "references" / "identification-review-template.md"
CHECKER = HERE / "check_review.py"

# A slot lookup in the checker: find_bullet(body, "<label>") or
# has_table_with_data_row(body, "<label>"). find_sublist/_find_paragraph and
# _bullet_pattern calls receive labels that already passed through one of
# these, so the two entry points cover the checker's whole label surface.
_CHECKER_LABEL_CALL = re.compile(r'(?:find_bullet|has_table_with_data_row)\(\s*body,\s*"([^"]+)"')

# A top-level `- <label>:` bullet inside the template's record skeleton;
# indented sub-bullets (assumption placeholders) are not slots.
_TEMPLATE_BULLET = re.compile(r"^- ([^:<]+):")


def checker_labels() -> set[str]:
    return set(_CHECKER_LABEL_CALL.findall(CHECKER.read_text(encoding="utf-8")))


def template_labels() -> set[str]:
    labels: set[str] = set()
    for line in TEMPLATE.read_text(encoding="utf-8").splitlines():
        match = _TEMPLATE_BULLET.match(line)
        if match:
            labels.add(match.group(1).strip())
    return labels


def test_extractors_surface_known_positives() -> None:
    """Both extractors can surface a known label, so an empty set on either
    side cannot silently pass the equality check below."""
    assert "Estimand" in checker_labels()
    assert "Estimand" in template_labels()
    assert "Assumption probes" in checker_labels()
    assert "Assumption probes" in template_labels()


def test_template_slot_labels_match_checker_labels() -> None:
    template, checker = template_labels(), checker_labels()
    assert template == checker, (
        f"template-only labels: {sorted(template - checker)}; "
        f"checker-only labels: {sorted(checker - template)}"
    )
