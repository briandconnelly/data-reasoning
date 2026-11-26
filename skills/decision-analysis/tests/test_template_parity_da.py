"""The record template's slot labels must equal check_decision.py's, as sets.

`references/decision-record-template.md` is the agent-facing statement of the
record's shape; `check_decision.py` is the operable one. The slot labels live
in both -- a template is read, a checker runs -- so this check keeps the two
sets from diverging silently, in either direction: a template-only label the
checker never enforces, or a checker label the template no longer shows.
The checker-side set is the union of its DECIDE_LABELS, RESOLVED_LABELS, and
VOI_LABELS constants, which _require_slots actually iterates, so every label
asserted here is enforced; RESOLVED_LABELS is the resolved skeleton's set
(decisions/008).
"""

import re
from pathlib import Path

from check_decision import DECIDE_LABELS, RESOLVED_LABELS, VOI_LABELS

TEMPLATE = Path(__file__).resolve().parents[1] / "references" / "decision-record-template.md"

# A top-level `- <label>:` bullet inside the template's record skeletons;
# the trailing colon is part of the label to match the checker constants.
_TEMPLATE_BULLET = re.compile(r"^- ([^<\n]+?:)")


def checker_labels() -> set[str]:
    labels: set[str] = set()
    for section_labels in (
        *DECIDE_LABELS.values(),
        *RESOLVED_LABELS.values(),
        *VOI_LABELS.values(),
    ):
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


def test_resolved_labels_are_in_the_template():
    assert "Surviving-state loss difference:" in template_labels()
    assert set(RESOLVED_LABELS["Resolution"]) <= template_labels()


def skeleton_sections(block: str) -> dict[str, tuple[str, ...]]:
    """Each `## Section` of one template block mapped to its `- Label:` bullets."""
    out: dict[str, list[str]] = {}
    current = None
    for line in block.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            out[current] = []
        elif current is not None and (m := _TEMPLATE_BULLET.match(line)):
            out[current].append(m.group(1).strip())
    return {k: tuple(v) for k, v in out.items()}


def test_each_skeleton_matches_its_own_label_set():
    """Per skeleton, per section, in order: a label dropped from one skeleton
    fails here even when another skeleton still carries it."""
    text = TEMPLATE.read_text(encoding="utf-8")
    blocks = re.findall(r"```markdown\n(.*?)```", text, re.S)
    by_title = {"Decision Record": [], "VoI Record": []}
    for block in blocks:
        by_title[block.split(":", 1)[0].removeprefix("# ")].append(block)
    ordinary, resolved = sorted(by_title["Decision Record"], key=lambda b: "## Resolution" in b)
    assert skeleton_sections(ordinary) == DECIDE_LABELS
    assert skeleton_sections(resolved) == RESOLVED_LABELS
    assert skeleton_sections(by_title["VoI Record"][0]) == VOI_LABELS
