"""Executable tests for check_review.py — run with:

    uv run --with pytest pytest skills/causal-identification-review/tests/ -v

check_review.py enforces the identification-review record's schema-scope
contract only: required fields present, route and disposition values drawn
from their closed sets, and forbidden certification vocabulary (`valid`,
`certified`) absent from disposition slots.
It deliberately does not judge whether the record preceded reasoning (scored
from transcripts, per the catalog) or the semantic quality of any assumption
or probe -- both out of scope per the task-3.2 brief.

We load the module by path with importlib (as check_prereg's own test does)
so no sys.path mutation is needed; check_review imports only the standard
library.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).parent
_spec = importlib.util.spec_from_file_location("check_review", HERE / "check_review.py")
assert _spec is not None
assert _spec.loader is not None
cr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cr)


# --------------------------------------------------------------------------- #
# Fixture records, built as strings so the test file is self-contained and
# does not touch skills/causal-identification-review/tests/fixtures/ (that
# tree belongs to the fixture-generation tasks, per the brief's "do not
# modify fixtures dirs" rule).
# --------------------------------------------------------------------------- #
VALID_RECORD = """\
# Identification Review: does the loyalty-tier change raise 90-day retention?

## Question

- Causal question, restated as a counterfactual contrast: retention differ absent the tier change
- Estimand: the average effect of tier-change exposure on 90-day retention
- Assignment mechanism as stated: "customers moved oldest cohorts first" (rollout_notes.md)
- Route: review

## Design: staggered-rollout difference-in-differences

- Design: staggered-rollout difference-in-differences across cohorts
- Identifying assumptions:
  - parallel trends: absent the tier change, cohorts would trend in retention the same way
  - no anticipation: customers did not change behavior ahead of their cohort's switch
- Assumption probes:

  | assumption | probe | result |
  | --- | --- | --- |
  | parallel trends | pre-period retention slope by cohort | slopes match within noise |
  | no anticipation | retention in the two weeks before each switch date | no discontinuity |

- Data requirements: per-customer enrollment date, cohort, switch date, retention status
- Threat register:

  | threat | probe | result |
  | --- | --- | --- |
  | concurrent promotion | cross-referenced promotions.log against switch dates | no overlap |

- Disposition: identified-if — parallel trends and no-anticipation both hold

## Handoff

- Facts: pre-period slopes matched noise; no promotion overlapped a switch window
- Assumptions: parallel trends and no anticipation, conditional on the probes above holding
- Dispositions: identified-if
"""

VALID_BOUND_RECORD = """\
# Identification Review: does removing the waitlist raise signup completion?

## Question

- Causal question, restated as a counterfactual contrast: completion differ had waitlist remained
- Estimand: the average effect of waitlist removal on signup completion
- Assignment mechanism as stated: UNSTATED
- Route: bound

## Bound

- Assumption ledger: waitlist completers are a subset of no-waitlist completers (monotonicity)
- Bound logic: Manski-style worst-case bounds from observed completion rates under monotonicity
- Computed endpoints: 0.04, 0.31

## Handoff

- Facts: observed completion rate rose from 0.41 to 0.52 across the waitlist-removal boundary
- Assumptions: monotonicity of completion under waitlist removal
- Dispositions: unresolved
"""


def strip_line(text: str, needle: str) -> str:
    """Remove the line containing ``needle`` entirely (simulates a missing field)."""
    lines = [line for line in text.splitlines() if needle not in line]
    return "\n".join(lines) + "\n"


def blank_field(text: str, label: str) -> str:
    """Blank out a ``- <label>: <value>`` field's value (simulates an empty field)."""
    return re.sub(rf"(- {re.escape(label)}:).*", r"\1", text)


# --------------------------------------------------------------------------- #
# Happy path
# --------------------------------------------------------------------------- #
def test_conforming_record_accepted() -> None:
    findings, _warnings = cr.check_record(VALID_RECORD)
    assert findings == []


def test_conforming_bound_record_accepted() -> None:
    findings, _warnings = cr.check_record(VALID_BOUND_RECORD)
    assert findings == []


# --------------------------------------------------------------------------- #
# Missing required fields — Question block
# --------------------------------------------------------------------------- #
def test_missing_counterfactual_contrast_rejected() -> None:
    record = strip_line(VALID_RECORD, "Causal question, restated as a counterfactual contrast")
    findings, _ = cr.check_record(record)
    assert any("counterfactual contrast" in f for f in findings)


def test_missing_estimand_rejected() -> None:
    record = blank_field(VALID_RECORD, "Estimand")
    findings, _ = cr.check_record(record)
    assert any("Estimand" in f for f in findings)


def test_missing_assignment_mechanism_rejected() -> None:
    record = blank_field(VALID_RECORD, "Assignment mechanism as stated")
    findings, _ = cr.check_record(record)
    assert any("Assignment mechanism" in f for f in findings)


def test_missing_route_rejected() -> None:
    record = blank_field(VALID_RECORD, "Route")
    findings, _ = cr.check_record(record)
    assert any("Route" in f for f in findings)


# --------------------------------------------------------------------------- #
# Missing required fields — Design block
# --------------------------------------------------------------------------- #
def test_missing_design_name_rejected() -> None:
    record = blank_field(VALID_RECORD, "Design")
    findings, _ = cr.check_record(record)
    assert any("Design" in f and "name" in f for f in findings)


def test_missing_identifying_assumptions_rejected() -> None:
    lines = VALID_RECORD.splitlines()
    out = []
    skipping = False
    for line in lines:
        if line.strip() == "- Identifying assumptions:":
            skipping = True
            continue
        if skipping and line.startswith("  - "):
            continue
        skipping = False
        out.append(line)
    record = "\n".join(out) + "\n"
    findings, _ = cr.check_record(record)
    assert any("identifying assumption" in f.lower() for f in findings)


def test_missing_assumption_probes_rejected() -> None:
    lines = VALID_RECORD.splitlines()
    out = []
    skipping = False
    for line in lines:
        if line.strip() == "- Assumption probes:":
            skipping = True
            continue
        if skipping and (line.strip() == "" or line.strip().startswith("|")):
            continue
        skipping = False
        out.append(line)
    record = "\n".join(out) + "\n"
    findings, _ = cr.check_record(record)
    assert any("probe" in f.lower() for f in findings)


def test_missing_data_requirements_rejected() -> None:
    record = blank_field(VALID_RECORD, "Data requirements")
    findings, _ = cr.check_record(record)
    assert any("Data requirements" in f for f in findings)


def test_missing_threat_register_rejected() -> None:
    lines = VALID_RECORD.splitlines()
    out = []
    skipping = False
    for line in lines:
        if line.strip() == "- Threat register:":
            skipping = True
            continue
        if skipping and (line.strip() == "" or line.strip().startswith("|")):
            continue
        skipping = False
        out.append(line)
    record = "\n".join(out) + "\n"
    findings, _ = cr.check_record(record)
    assert any("threat register" in f.lower() for f in findings)


def test_missing_disposition_rejected() -> None:
    record = blank_field(VALID_RECORD, "Disposition")
    findings, _ = cr.check_record(record)
    assert any("Disposition" in f for f in findings)


# --------------------------------------------------------------------------- #
# Missing required fields — Bound block (present-when case)
# --------------------------------------------------------------------------- #
def test_missing_assumption_ledger_rejected() -> None:
    record = blank_field(VALID_BOUND_RECORD, "Assumption ledger")
    findings, _ = cr.check_record(record)
    assert any("Assumption ledger" in f for f in findings)


def test_missing_bound_logic_rejected() -> None:
    record = blank_field(VALID_BOUND_RECORD, "Bound logic")
    findings, _ = cr.check_record(record)
    assert any("Bound logic" in f for f in findings)


def test_missing_computed_endpoints_rejected() -> None:
    record = blank_field(VALID_BOUND_RECORD, "Computed endpoints")
    findings, _ = cr.check_record(record)
    assert any("Computed endpoints" in f for f in findings)


# --------------------------------------------------------------------------- #
# Missing required fields — Handoff block
# --------------------------------------------------------------------------- #
def test_missing_handoff_facts_rejected() -> None:
    record = blank_field(VALID_RECORD, "Facts")
    findings, _ = cr.check_record(record)
    assert any("Facts" in f for f in findings)


def test_missing_handoff_assumptions_rejected() -> None:
    record = blank_field(VALID_RECORD, "Assumptions")
    findings, _ = cr.check_record(record)
    assert any("Assumptions" in f for f in findings)


def test_missing_handoff_dispositions_rejected() -> None:
    record = blank_field(VALID_RECORD, "Dispositions")
    findings, _ = cr.check_record(record)
    assert any("Dispositions" in f for f in findings)


# --------------------------------------------------------------------------- #
# Closed-set violations
# --------------------------------------------------------------------------- #
def test_route_outside_closed_set_rejected() -> None:
    record = VALID_RECORD.replace("Route: review", "Route: recommend")
    findings, _ = cr.check_record(record)
    assert any("route" in f.lower() and "recommend" in f for f in findings)


def test_bad_disposition_rejected() -> None:
    record = VALID_RECORD.replace(
        "Disposition: identified-if — parallel trends and no-anticipation both hold",
        "Disposition: probably-fine — looks okay",
    )
    findings, _ = cr.check_record(record)
    assert any("disposition" in f.lower() and "probably-fine" in f for f in findings)


# --------------------------------------------------------------------------- #
# Forbidden vocabulary
# --------------------------------------------------------------------------- #
def test_forbidden_word_valid_in_disposition_rejected() -> None:
    record = VALID_RECORD.replace(
        "Disposition: identified-if — parallel trends and no-anticipation both hold",
        "Disposition: identified-if — the design is valid",
    )
    findings, _ = cr.check_record(record)
    assert any("forbidden" in f.lower() and "valid" in f.lower() for f in findings)


def test_forbidden_word_certified_in_disposition_rejected() -> None:
    record = VALID_RECORD.replace(
        "Disposition: identified-if — parallel trends and no-anticipation both hold",
        "Disposition: identified-if — this design is now certified",
    )
    findings, _ = cr.check_record(record)
    assert any("forbidden" in f.lower() and "certified" in f.lower() for f in findings)


def test_forbidden_word_does_not_false_positive_elsewhere() -> None:
    """'valid'/'certified' outside a disposition slot must not trip the gate --
    the forbidden-vocabulary check is scoped to disposition slots only, per the
    brief ('forbidden vocabulary ... absent from disposition slots')."""
    record = VALID_RECORD.replace(
        "Data requirements: per-customer enrollment date, cohort, switch date, retention status",
        "Data requirements: a valid, certified export of per-customer enrollment records",
    )
    findings, _ = cr.check_record(record)
    assert findings == []


# --------------------------------------------------------------------------- #
# Advisory numeric-estimate heuristic — catch and documented miss
# --------------------------------------------------------------------------- #
def test_advisory_numeric_scan_catches_planted_point_estimate() -> None:
    """Catch case: a digit-based point estimate planted outside the Bound
    block's endpoints slot (in Handoff Facts) is flagged as a warning, and the
    run still exits clean (advisory, not a gate)."""
    record = VALID_RECORD.replace(
        "- Facts: pre-period slopes matched noise; no promotion overlapped a switch window",
        "- Facts: pre-period slopes matched noise; the effect looks like a 4.2pp lift",
    )
    findings, warnings = cr.check_record(record)
    assert findings == []
    assert any("4.2" in w for w in warnings)


def test_advisory_numeric_scan_documented_miss_spelled_out_number() -> None:
    """Documented miss: the regex heuristic looks for digit-based patterns, so
    a spelled-out point estimate ("a four percentage point lift") is NOT
    caught -- this is a known, on-file limitation of the heuristic, not a bug.
    The run still exits clean either way (advisory, not a gate)."""
    record = VALID_RECORD.replace(
        "- Facts: pre-period slopes matched noise; no promotion overlapped a switch window",
        "- Facts: pre-period slopes matched noise; the effect looks like four percentage points",
    )
    findings, warnings = cr.check_record(record)
    assert findings == []
    assert warnings == []


def test_advisory_numeric_scan_does_not_flag_bound_endpoints_slot() -> None:
    """The Bound block's own Computed endpoints slot is the licensed home for
    numeric output (decisions/005); the heuristic must not flag it."""
    findings, warnings = cr.check_record(VALID_BOUND_RECORD)
    assert findings == []
    assert not any("0.04" in w or "0.31" in w for w in warnings)


# --------------------------------------------------------------------------- #
# CLI / file-handling behavior
# --------------------------------------------------------------------------- #
def test_main_exits_zero_on_conforming_record(tmp_path: Path) -> None:
    record_path = tmp_path / "record.md"
    record_path.write_text(VALID_RECORD, encoding="utf-8")
    assert cr.main([str(record_path)]) == cr.EXIT_OK


def test_main_exits_nonzero_on_gate_failure(tmp_path: Path) -> None:
    record_path = tmp_path / "record.md"
    bad_record = VALID_RECORD.replace("Route: review", "Route: recommend")
    record_path.write_text(bad_record, encoding="utf-8")
    assert cr.main([str(record_path)]) == cr.EXIT_GATE_FAILURE


def test_main_fails_closed_on_unreadable_file(tmp_path: Path) -> None:
    missing = tmp_path / "does-not-exist.md"
    assert cr.main([str(missing)]) == cr.EXIT_UNVERIFIABLE
