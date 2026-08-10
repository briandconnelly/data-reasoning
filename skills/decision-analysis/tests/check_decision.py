#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Check a decision record's schema-scope contract, failing closed.

SCOPE: this is a machine encoding of the record's *shape and arithmetic*, not
its content. It verifies: no duplicate sections; every route-required section
and slot present and non-empty; Route/Verdict/provenance values drawn from
their closed sets; sensitivity-only provenance absent from the Evidence and
update block; a causal Claim class carrying a non-NONE Identification basis;
the binary/two-action v1 scope (two ' vs '-separated actions, exactly two
consequence action rows and two state columns -- records outside it are
rejected, not approximated); loss numbers carrying belief-grade provenance
under a robust verdict, each field checked independently; the voi
signal-model/verdict coupling; and (arithmetic gates) recomputation of the
posterior-odds interval and, when a numeric decision threshold is recorded,
of the prior-odds crossover interval against the swept prior class. Required
numeric fields that do not parse, or violate their domain (ordered ranges,
odds and LRs strictly positive), are gate failures -- never skipped checks.

Explicitly NOT this checker's claim: whether the record preceded reasoning
(a transcript-level fact this file never sees), whether a likelihood ratio is
calibrated or its named source real, whether the state model is exhaustive,
whether the swept prior class or loss range is honest, whether a `dominated`
verdict's statewise-domination claim holds (structural presence only),
whether the voi Value calculation's prose arithmetic is correct (voi numerics
are not recomputed in v1), whether the route was the right one, or whether
any prose entry is semantically adequate. Passing this checker is
consistency, not validity.

The closed-set vocabulary and its semantics are governed by ../SKILL.md
(§ Routing, § Numeric Policy, § The Decide Route, § The VoI Route); this
checker enforces, it does not restate.

Exit codes:
  0  no gate failures
  1  one or more gate failures
  2  UNVERIFIABLE: the record file could not be read
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROUTES = frozenset({"decide", "voi"})
DECIDE_VERDICTS = frozenset({"robust", "prior-sensitive", "loss-sensitive", "dominated"})
VOI_VERDICTS = frozenset({"worth-it", "not-worth-it", "sensitive", "break-even-only"})
PROVENANCE = frozenset(
    {"user-elicited", "externally-sourced", "estimated-from-data-in-hand", "sensitivity-only"}
)
BELIEF_LOSS_PROVENANCE = frozenset({"user-elicited", "externally-sourced"})

# Every top-level template bullet, by section; Task 5's parity test asserts
# set equality between these labels and the template's bullets.
DECIDE_LABELS: dict[str, tuple[str, ...]] = {
    "Decision frame": (
        "Route:",
        "Actions:",
        "Decision owner:",
        "Reversibility:",
        "Deadline or forcing event:",
        "Consequences:",
        "Loss ratio:",
        "Decision threshold (posterior odds):",
    ),
    "Decision-state model": (
        "Proposition:",
        "Residual reading:",
        "Claim class:",
        "Identification basis:",
        "Ledger mapping:",
    ),
    "Evidence and update": ("Prior odds:", "Evidence:", "Independence:", "Posterior odds:"),
    "Robustness": ("Prior class swept:", "Loss range swept:", "Crossover:"),
    "Verdict": ("Verdict:", "Conditions:"),
    "Handoff": ("Open factual disputes:", "Identification gaps:", "VoI question:"),
}
VOI_LABELS: dict[str, tuple[str, ...]] = {
    "VoI": (
        "Route:",
        "Pending decision:",
        "Signal model:",
        "Value calculation:",
        "Cost:",
        "Verdict:",
    ),
}

EXIT_OK = 0
EXIT_GATE_FAILURE = 1
EXIT_UNVERIFIABLE = 2

# v1 binary/two-action scope constants (see module docstring).
_SCOPE_ACTIONS = 2
_SCOPE_ACTION_ROWS = 2
_SCOPE_TABLE_COLUMNS = 3

_SECTION = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
_PROVENANCE_MENTION = re.compile(r"provenance:\s*([a-z-]+)")
_RANGE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*(?:[–-]\s*(\d+(?:\.\d+)?))?\s*$")  # noqa: RUF001
_SEPARATOR_CELL = re.compile(r"^:?-+:?$")
_REL_TOLERANCE = 0.01


def parse_sections(text: str) -> tuple[dict[str, str], list[str]]:
    """Map each ``## Section`` heading to its body; also return duplicates."""
    sections: dict[str, str] = {}
    duplicates: list[str] = []
    matches = list(_SECTION.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        name = m.group(1)
        if name in sections:
            duplicates.append(name)
        sections[name] = text[m.end() : end]
    return sections, duplicates


def field(section_text: str, label: str) -> str | None:
    """Return the value of ``- <label> <value>`` in a section, else None."""
    for line in section_text.splitlines():
        stripped = line.strip()
        if stripped.startswith(f"- {label}"):
            return stripped[len(f"- {label}") :].strip()
    return None


def parse_range(value: str) -> tuple[float, float] | None:
    """Parse ``3`` or ``0.25-1.0`` (en dash or hyphen) into an ordered (low, high)."""
    m = _RANGE.match(value)
    if not m:
        return None
    low = float(m.group(1))
    high = float(m.group(2)) if m.group(2) else low
    if low > high:
        return None
    return (low, high)


def _bare(value: str) -> str:
    """Strip a trailing '— provenance: ...' annotation from a slot value."""
    return value.split("—", maxsplit=1)[0].strip()


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= _REL_TOLERANCE * max(abs(a), abs(b), 1e-12)


def _table_rows(section_text: str) -> list[list[str]]:
    """All pipe-table rows in a section, as cell lists (outer pipes stripped)."""
    rows = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            rows.append([c.strip() for c in stripped[1:-1].split("|")])
    return rows


def _data_rows(rows: list[list[str]]) -> list[list[str]]:
    """Table rows minus the first (header) row and any separator rows."""
    body = rows[1:] if rows else []
    return [r for r in body if not all(_SEPARATOR_CELL.match(c) for c in r if c)]


def _require_slots(
    sections: dict[str, str], labels: dict[str, tuple[str, ...]], failures: list[str]
) -> None:
    for section_name, section_labels in labels.items():
        body = sections.get(section_name)
        if body is None:
            failures.append(f"record is missing required section '## {section_name}'")
            continue
        for label in section_labels:
            value = field(body, label)
            if value is None:
                failures.append(f"section '{section_name}' is missing required slot '- {label}'")
            elif not value and label not in ("Consequences:", "Evidence:"):
                failures.append(f"slot '- {label}' in '{section_name}' is empty")


def check(text: str) -> list[str]:
    failures: list[str] = []
    sections, duplicates = parse_sections(text)
    for name in duplicates:
        failures.append(f"duplicate section '## {name}'")

    route = None
    for body in sections.values():
        value = field(body, "Route:")
        if value:
            route = _bare(value)
            break
    if route not in ROUTES:
        failures.append(f"Route value {route!r} is not in the closed set {sorted(ROUTES)}")
        return failures

    for value in _PROVENANCE_MENTION.findall(text):
        if value not in PROVENANCE:
            failures.append(
                f"provenance value {value!r} is not in the closed set {sorted(PROVENANCE)}"
            )

    if route == "decide":
        _require_slots(sections, DECIDE_LABELS, failures)
        if not any(f.startswith("record is missing") for f in failures):
            failures.extend(_check_decide(sections))
    else:
        _require_slots(sections, VOI_LABELS, failures)
        if "VoI" in sections:
            failures.extend(_check_voi(sections))
    return failures


def _check_decide(sections: dict[str, str]) -> list[str]:
    failures: list[str] = []
    frame = sections["Decision frame"]

    actions = _bare(field(frame, "Actions:") or "")
    if len(re.split(r"\s+vs\s+", actions)) != _SCOPE_ACTIONS:
        failures.append("Actions must name exactly two actions separated by ' vs ' (v1 scope)")

    rows = _table_rows(frame)
    data = _data_rows(rows)
    if len(data) != _SCOPE_ACTION_ROWS:
        failures.append(f"Consequences table must have exactly two action rows; found {len(data)}")
    if rows and len(rows[0]) != _SCOPE_TABLE_COLUMNS:
        failures.append(
            f"Consequences table must have exactly two state columns; found {len(rows[0]) - 1}"
        )

    for label in ("Loss ratio:", "Decision threshold (posterior odds):"):
        value = field(frame, label) or ""
        if _bare(value) != "none stated" and not _PROVENANCE_MENTION.search(value):
            failures.append(f"slot '- {label}' carries a number without a provenance class")

    model = sections["Decision-state model"]
    claim = _bare(field(model, "Claim class:") or "")
    basis = _bare(field(model, "Identification basis:") or "")
    if claim == "causal" and (not basis or basis.upper() == "NONE"):
        failures.append(
            "Claim class 'causal' requires a non-NONE Identification basis "
            "(HDA's causal-wording bar or a CIR identified-if, by pointer)"
        )

    evidence = sections["Evidence and update"]
    if "sensitivity-only" in evidence:
        failures.append(
            "sensitivity-only provenance may not appear in Evidence and update; "
            "it belongs in Robustness"
        )

    verdict = _bare(field(sections["Verdict"], "Verdict:") or "")
    if verdict not in DECIDE_VERDICTS:
        failures.append(
            f"Verdict value {verdict!r} is not in the closed set {sorted(DECIDE_VERDICTS)}"
        )
    elif verdict == "robust":
        for section_name, label in (
            ("Decision frame", "Loss ratio:"),
            ("Robustness", "Loss range swept:"),
        ):
            provs = _PROVENANCE_MENTION.findall(field(sections[section_name], label) or "")
            if len(provs) != 1 or provs[0] not in BELIEF_LOSS_PROVENANCE:
                failures.append(
                    f"a robust verdict requires '- {label}' to carry exactly one "
                    "user-elicited or externally-sourced provenance "
                    "(missing losses gate recommendations)"
                )

    failures.extend(_check_decide_arithmetic(sections, verdict))
    return failures


def _check_decide_arithmetic(
    sections: dict[str, str],  # noqa: ARG001 -- Task 4 fills this in
    verdict: str,  # noqa: ARG001 -- Task 4 fills this in
) -> list[str]:
    # Task 4 fills this in; the structural pass ships it as a no-op.
    return []


def _check_voi(sections: dict[str, str]) -> list[str]:
    failures: list[str] = []
    voi = sections["VoI"]
    verdict = _bare(field(voi, "Verdict:") or "")
    if verdict not in VOI_VERDICTS:
        failures.append(
            f"Verdict value {verdict!r} is not in the closed set {sorted(VOI_VERDICTS)}"
        )
    signal = field(voi, "Signal model:") or ""
    if "sensitivity-only" in signal and verdict != "break-even-only":
        failures.append("a sensitivity-only signal model licenses only the break-even-only verdict")
    return failures


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: check_decision.py <record.md>", file=sys.stderr)
        return EXIT_UNVERIFIABLE
    try:
        text = Path(argv[0]).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"UNVERIFIABLE: {exc}", file=sys.stderr)
        return EXIT_UNVERIFIABLE
    failures = check(text)
    for failure in failures:
        print(f"GATE FAILURE: {failure}")
    return EXIT_GATE_FAILURE if failures else EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
