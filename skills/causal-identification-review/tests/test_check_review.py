"""Executable tests for check_review.py — run with:

    uv run --with pytest pytest skills/causal-identification-review/tests/ -v

check_review.py enforces the identification-review record's schema-scope
contract only: required fields present, route and disposition values drawn
from their closed sets, route-aware block structure (review/construct need
Design blocks and no Bound block; bound needs the Bound block and no Design
blocks), Handoff Dispositions reusing only values assigned above (or the
literal `none` when the route assigns none), and forbidden certification
vocabulary (`valid`, `certified`) absent from disposition slots.
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
- Dispositions: none
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
# Forbidden vocabulary — scoped to the disposition VALUE token, not the whole
# bullet (reviewer finding on an earlier revision: "identified-if -- the
# instrument is valid only if the exclusion restriction holds" is a
# conforming record whose rationale legitimately uses ordinary
# causal-inference vocabulary; decision 004 forbids `valid`/`certified` as an
# unconditional verdict VALUE, not that word anywhere in rationale prose).
# --------------------------------------------------------------------------- #
def test_forbidden_word_valid_as_disposition_value_rejected() -> None:
    record = VALID_RECORD.replace(
        "Disposition: identified-if — parallel trends and no-anticipation both hold",
        "Disposition: valid — the design is sound",
    )
    findings, _ = cr.check_record(record)
    assert any("forbidden" in f.lower() and "valid" in f.lower() for f in findings)


def test_forbidden_word_certified_as_disposition_value_rejected() -> None:
    record = VALID_RECORD.replace(
        "Disposition: identified-if — parallel trends and no-anticipation both hold",
        "Disposition: certified — this design is sound",
    )
    findings, _ = cr.check_record(record)
    assert any("forbidden" in f.lower() and "certified" in f.lower() for f in findings)


def test_forbidden_word_valid_in_rationale_prose_is_not_flagged() -> None:
    """'valid' used in ordinary rationale prose after a real closed-set
    disposition value (e.g. "valid instrument") must NOT trip the gate --
    only the isolated value token is checked, never the rationale."""
    record = VALID_RECORD.replace(
        "Disposition: identified-if — parallel trends and no-anticipation both hold",
        "Disposition: identified-if — the instrument is valid only if the "
        "exclusion restriction holds",
    )
    findings, _ = cr.check_record(record)
    assert findings == []


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
# Route-aware structure — review/construct need >=1 Design block and no Bound
# block; bound needs the Bound block and no Design blocks (a design-review
# finding: `Route: bound` + a Design block passed before this check existed).
# --------------------------------------------------------------------------- #
def test_route_bound_with_design_block_rejected() -> None:
    record = VALID_RECORD.replace("Route: review", "Route: bound")
    findings, _ = cr.check_record(record)
    assert any("route 'bound' must not carry Design blocks" in f for f in findings)
    assert any("route 'bound' requires the Bound block" in f for f in findings)


def test_route_bound_without_bound_block_rejected() -> None:
    lines = VALID_BOUND_RECORD.splitlines()
    out, skipping = [], False
    for line in lines:
        if line.strip() == "## Bound":
            skipping = True
            continue
        if skipping and line.startswith("## "):
            skipping = False
        if not skipping:
            out.append(line)
    record = "\n".join(out) + "\n"
    findings, _ = cr.check_record(record)
    assert any("route 'bound' requires the Bound block" in f for f in findings)


def test_route_review_with_bound_block_and_no_design_rejected() -> None:
    record = VALID_BOUND_RECORD.replace("Route: bound", "Route: review")
    findings, _ = cr.check_record(record)
    assert any("route 'review' requires at least one Design block" in f for f in findings)
    assert any("route 'review' must not carry a Bound block" in f for f in findings)


def test_route_construct_with_bound_block_and_no_design_rejected() -> None:
    record = VALID_BOUND_RECORD.replace("Route: bound", "Route: construct")
    findings, _ = cr.check_record(record)
    assert any("route 'construct' requires at least one Design block" in f for f in findings)
    assert any("route 'construct' must not carry a Bound block" in f for f in findings)


# --------------------------------------------------------------------------- #
# Handoff Dispositions — reuse-only, with `none` for a route assigning none
# --------------------------------------------------------------------------- #
def test_bound_record_handoff_dispositions_none_accepted() -> None:
    """A bound record assigns no disposition above, so its Handoff carries the
    literal `none` -- accepted, not treated as a missing or invalid value."""
    findings, _ = cr.check_record(VALID_BOUND_RECORD)
    assert findings == []


def test_bound_record_fabricated_disposition_rejected() -> None:
    """A closed-set disposition planted in a bound record's Handoff that
    appears nowhere above is a fabrication, not a reuse -- rejected."""
    record = VALID_BOUND_RECORD.replace("- Dispositions: none", "- Dispositions: unresolved")
    findings, _ = cr.check_record(record)
    assert any("appear nowhere above" in f and "unresolved" in f for f in findings)


def test_design_record_fabricated_disposition_rejected() -> None:
    """A Design record whose Handoff names a closed-set value never assigned
    above (assigned: identified-if; handoff: unresolved) is rejected."""
    record = VALID_RECORD.replace("- Dispositions: identified-if", "- Dispositions: unresolved")
    findings, _ = cr.check_record(record)
    assert any("appear nowhere above" in f and "unresolved" in f for f in findings)


def test_design_record_handoff_none_rejected() -> None:
    """`none` is only for a record whose route assigns no disposition; a
    record that assigned one above must reuse it."""
    record = VALID_RECORD.replace("- Dispositions: identified-if", "- Dispositions: none")
    findings, _ = cr.check_record(record)
    assert any("'none' but the record assigns" in f for f in findings)


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
# Formatting tolerance (task-5.2 scoped fix) -- measurement arms produced
# records that are substantively conforming but that the checker rejected on
# parses that only differ in layout, not content: backtick-wrapped closed-set
# tokens, a `none` Handoff Dispositions value carrying a trailing rationale,
# and Design-block presence gates (identifying assumptions, assumption
# probes, threat register) written as inline prose rather than a sublist or
# table. None of the closed sets, the forbidden-vocabulary gate, route-aware
# block structure, or the fabricated-disposition rejection are loosened by
# any of this -- see the "still rejected" tests below, which pin that.
# --------------------------------------------------------------------------- #
def test_backtick_wrapped_route_accepted() -> None:
    record = VALID_RECORD.replace("Route: review", "Route: `review`")
    findings, _ = cr.check_record(record)
    assert findings == []


def test_backtick_wrapped_disposition_accepted() -> None:
    record = VALID_RECORD.replace(
        "Disposition: identified-if — parallel trends and no-anticipation both hold",
        "Disposition: `identified-if` — parallel trends and no-anticipation both hold",
    )
    findings, _ = cr.check_record(record)
    assert findings == []


def test_backtick_wrapped_invalid_route_still_rejected() -> None:
    """Stripping backticks must not turn an invalid token into a valid one."""
    record = VALID_RECORD.replace("Route: review", "Route: `recommend`")
    findings, _ = cr.check_record(record)
    assert any("route" in f.lower() and "recommend" in f for f in findings)


def test_backtick_wrapped_forbidden_disposition_still_rejected() -> None:
    """Stripping backticks must not exempt a certification-vocabulary value."""
    record = VALID_RECORD.replace(
        "Disposition: identified-if — parallel trends and no-anticipation both hold",
        "Disposition: `valid` — the design is sound",
    )
    findings, _ = cr.check_record(record)
    assert any("forbidden" in f.lower() and "valid" in f.lower() for f in findings)


def test_handoff_dispositions_none_with_em_dash_rationale_accepted() -> None:
    record = VALID_BOUND_RECORD.replace(
        "- Dispositions: none",
        "- Dispositions: none — no Design block is carried by this bound-route record",
    )
    findings, _ = cr.check_record(record)
    assert findings == []


def test_handoff_dispositions_none_with_hyphen_dash_rationale_accepted() -> None:
    record = VALID_BOUND_RECORD.replace(
        "- Dispositions: none",
        "- Dispositions: none - no Design block is carried by this bound-route record",
    )
    findings, _ = cr.check_record(record)
    assert findings == []


def test_handoff_dispositions_backtick_none_accepted() -> None:
    record = VALID_BOUND_RECORD.replace("- Dispositions: none", "- Dispositions: `none`")
    findings, _ = cr.check_record(record)
    assert findings == []


def test_handoff_dispositions_none_with_rationale_but_assigned_still_rejected() -> None:
    """`none — <rationale>` tolerance must not excuse a record that actually
    assigned a disposition above from reusing it."""
    record = VALID_RECORD.replace(
        "- Dispositions: identified-if",
        "- Dispositions: none — nothing to report",
    )
    findings, _ = cr.check_record(record)
    assert any("'none' but the record assigns" in f for f in findings)


_ASSUMPTIONS_BLOCK = (
    "- Identifying assumptions:\n"
    "  - parallel trends: absent the tier change, cohorts would trend in retention the same way\n"
    "  - no anticipation: customers did not change behavior ahead of their cohort's switch\n"
)
_PROBES_BLOCK = (
    "- Assumption probes:\n"
    "\n"
    "  | assumption | probe | result |\n"
    "  | --- | --- | --- |\n"
    "  | parallel trends | pre-period retention slope by cohort | slopes match within noise |\n"
    "  | no anticipation | retention in the two weeks before each switch date | "
    "no discontinuity |\n"
)
_THREATS_BLOCK = (
    "- Threat register:\n"
    "\n"
    "  | threat | probe | result |\n"
    "  | --- | --- | --- |\n"
    "  | concurrent promotion | cross-referenced promotions.log against switch dates | "
    "no overlap |\n"
)


def test_identifying_assumptions_inline_prose_accepted() -> None:
    """A single prose sentence in the label's own line satisfies the
    >=1-assumption presence gate just as a sublist does."""
    record = VALID_RECORD.replace(
        _ASSUMPTIONS_BLOCK,
        "- Identifying assumptions: n/a — not evaluated; this design is named only, not probed\n",
    )
    findings, _ = cr.check_record(record)
    assert not any("identifying assumption" in f.lower() for f in findings)


def test_identifying_assumptions_blank_still_rejected() -> None:
    """A genuinely empty slot -- no inline value, no sublist, nothing before
    the next bullet -- must still fail; the tolerance is for format, not for
    absence. (``blank_field`` only clears the label's own line, so a real
    empty-slot record must also drop the sublist items below it.)"""
    record = VALID_RECORD.replace(_ASSUMPTIONS_BLOCK, "- Identifying assumptions:\n")
    findings, _ = cr.check_record(record)
    assert any("identifying assumption" in f.lower() for f in findings)


def test_assumption_probes_inline_prose_accepted() -> None:
    """A named-only design carrying `none run` probes is a formatting-tolerated
    shape — but only under a disposition that does not claim probe support
    (`not-constructible` here); an `identified-if` with none-run probes is a
    contradiction the probes-run gate rejects (see the gate tests below)."""
    record = (
        VALID_RECORD.replace(
            _PROBES_BLOCK,
            "- Assumption probes: none run — this design is named only, not probed\n",
        )
        .replace(
            "Disposition: identified-if — parallel trends and no-anticipation both hold",
            "Disposition: not-constructible — named only; the data cannot feed this design",
        )
        .replace("- Dispositions: identified-if", "- Dispositions: not-constructible")
    )
    findings, _ = cr.check_record(record)
    assert not any("probe" in f.lower() for f in findings)


def test_threat_register_inline_prose_accepted() -> None:
    record = VALID_RECORD.replace(
        _THREATS_BLOCK,
        "- Threat register: none run — this design is named only, not probed\n",
    )
    findings, _ = cr.check_record(record)
    assert not any("threat register" in f.lower() for f in findings)


def test_handoff_facts_nested_list_accepted() -> None:
    record = VALID_RECORD.replace(
        "- Facts: pre-period slopes matched noise; no promotion overlapped a switch window",
        "- Facts:\n"
        "  - pre-period slopes matched noise\n"
        "  - no promotion overlapped a switch window",
    )
    findings, _ = cr.check_record(record)
    assert not any("Facts" in f for f in findings)


def test_handoff_facts_prose_paragraph_accepted() -> None:
    record = VALID_RECORD.replace(
        "- Facts: pre-period slopes matched noise; no promotion overlapped a switch window",
        "- Facts:\n"
        "  pre-period slopes matched noise; no promotion overlapped a switch window,\n"
        "  reported as a paragraph rather than a single line.",
    )
    findings, _ = cr.check_record(record)
    assert not any("Facts" in f for f in findings)


def test_handoff_facts_blank_still_rejected() -> None:
    record = blank_field(VALID_RECORD, "Facts")
    findings, _ = cr.check_record(record)
    assert any("Facts" in f for f in findings)


def test_four_space_indented_sublist_accepted() -> None:
    """Sublist tolerance is not two-space-only (external review finding): a
    4-space-indented item is a valid markdown sublist, and before this fix it
    fell through both the sublist collector and the paragraph fallback (whose
    collection ends at any stripped line starting '- '), reading a populated
    slot as empty."""
    record = VALID_RECORD.replace(
        "- Facts: pre-period slopes matched noise; no promotion overlapped a switch window",
        "- Facts:\n"
        "    - pre-period slopes matched noise\n"
        "    - no promotion overlapped a switch window",
    )
    findings, _ = cr.check_record(record)
    assert findings == []


def test_tab_indented_sublist_accepted() -> None:
    record = VALID_RECORD.replace(
        _ASSUMPTIONS_BLOCK,
        "- Identifying assumptions:\n"
        "\t- parallel trends: absent the tier change, cohorts would trend the same way\n"
        "\t- no anticipation: customers did not change behavior ahead of the switch\n",
    )
    findings, _ = cr.check_record(record)
    assert findings == []


def test_handoff_dispositions_nested_list_reuse_accepted() -> None:
    """A per-design breakdown written as a nested list under Dispositions,
    each entry backtick-wrapped, still counts as reusing the values assigned
    above -- this is the shape sc2-cs7-ws's Handoff block used."""
    record = VALID_RECORD.replace(
        "- Dispositions: identified-if",
        "- Dispositions:\n"
        "  - staggered-rollout difference-in-differences: `identified-if` (conditions above)",
    )
    findings, _ = cr.check_record(record)
    assert findings == []


def test_handoff_dispositions_nested_list_fabricated_still_rejected() -> None:
    """The nested-list tolerance must not let a fabricated disposition (one
    never assigned by any Design block above) slip past the reuse check."""
    record = VALID_RECORD.replace(
        "- Dispositions: identified-if",
        "- Dispositions:\n"
        "  - staggered-rollout difference-in-differences: `unresolved` (never assigned above)",
    )
    findings, _ = cr.check_record(record)
    assert any("appear nowhere above" in f and "unresolved" in f for f in findings)


def test_compound_conditional_disposition_still_rejected() -> None:
    """A disposition written as a compound conditional sentence rather than a
    closed-set token (no em-dash separating value from rationale) is not a
    formatting variant of a real token -- it is a different, non-conforming
    value, and must still be rejected. Mirrors the real measurement failure
    in phase4-arms/sc-cs2/price-increase-churn-identification-review.md."""
    record = VALID_RECORD.replace(
        "Disposition: identified-if — parallel trends and no-anticipation both hold",
        "Disposition: not-constructible if fewer than a handful of comparators exist; "
        "otherwise unresolved pending further probes",
    )
    findings, _ = cr.check_record(record)
    assert any(
        "disposition" in f.lower() and "not-constructible if fewer than a handful" in f
        for f in findings
    )


# --------------------------------------------------------------------------- #
# identified-if requires probes run (2026-08-09 post-review gate) -- SKILL.md's
# disposition semantics say `identified-if` is earned by probes run and
# reported, not merely proposed, yet the checker passed a Design block pairing
# `Disposition: identified-if` with `Assumption probes: none run` (reproduced
# by the final cross-model review). The gate: an identified-if Design block
# must carry at least one probe entry with an actual result; probes that are
# empty, `none`, `none run`, or `not run` reject. Other dispositions may still
# carry none-run probes -- a named-only design legitimately ends
# `not-constructible`.
# --------------------------------------------------------------------------- #
def test_identified_if_with_none_run_probes_rejected() -> None:
    record = VALID_RECORD.replace(
        _PROBES_BLOCK,
        "- Assumption probes: none run — this design is named only, not probed\n",
    )
    findings, _ = cr.check_record(record)
    assert any("identified-if" in f and "probe" in f.lower() for f in findings)


def test_identified_if_with_bare_none_probes_rejected() -> None:
    record = VALID_RECORD.replace(_PROBES_BLOCK, "- Assumption probes: none\n")
    findings, _ = cr.check_record(record)
    assert any("identified-if" in f and "probe" in f.lower() for f in findings)


def test_identified_if_with_backtick_none_run_probes_rejected() -> None:
    """Backtick tolerance must not launder a none-run probes slot."""
    record = VALID_RECORD.replace(
        _PROBES_BLOCK,
        "- Assumption probes: `none run` — proposed but not executed\n",
    )
    findings, _ = cr.check_record(record)
    assert any("identified-if" in f and "probe" in f.lower() for f in findings)


def test_identified_if_with_not_run_probes_rejected() -> None:
    """`not run` is the same no-result content as `none run` (the shape the
    sc2-cs4-ws record used for a named-only block) and rejects the same way."""
    record = VALID_RECORD.replace(
        _PROBES_BLOCK,
        "- Assumption probes: not run — no outcome data exists to probe against\n",
    )
    findings, _ = cr.check_record(record)
    assert any("identified-if" in f and "probe" in f.lower() for f in findings)


def test_identified_if_with_probe_table_accepted() -> None:
    """The known negative: identified-if with a real probe table (results in
    the rows) stays accepted -- the gate keys on run results, not on layout."""
    findings, _ = cr.check_record(VALID_RECORD)
    assert findings == []


def test_not_constructible_with_none_run_probes_accepted() -> None:
    """A named-only design ending not-constructible legitimately carries
    none-run probes; the gate binds identified-if only."""
    record = (
        VALID_RECORD.replace(
            _PROBES_BLOCK,
            "- Assumption probes: none run — this design is named only, not probed\n",
        )
        .replace(
            "Disposition: identified-if — parallel trends and no-anticipation both hold",
            "Disposition: not-constructible — the data cannot feed this design",
        )
        .replace("- Dispositions: identified-if", "- Dispositions: not-constructible")
    )
    findings, _ = cr.check_record(record)
    assert findings == []


def test_unresolved_with_none_run_probes_accepted() -> None:
    record = (
        VALID_RECORD.replace(
            _PROBES_BLOCK,
            "- Assumption probes: none run — proposed, not yet executed\n",
        )
        .replace(
            "Disposition: identified-if — parallel trends and no-anticipation both hold",
            "Disposition: unresolved — the probes are proposed but not run",
        )
        .replace("- Dispositions: identified-if", "- Dispositions: unresolved")
    )
    findings, _ = cr.check_record(record)
    assert findings == []


# --------------------------------------------------------------------------- #
# Handoff Dispositions set-equality (2026-08-09 post-review gate) -- the reuse
# check rejected fabricated tokens but let assigned dispositions be silently
# OMITTED (one-directional). The mentioned set must equal the assigned set, or
# be `none` only when nothing was assigned.
# --------------------------------------------------------------------------- #
_SECOND_DESIGN_BLOCK = """\
## Design: event-study around each cohort's switch date

- Design: event-study around each cohort's switch date
- Identifying assumptions:
  - no anticipation: behavior does not shift ahead of the switch
- Assumption probes:

  | assumption | probe | result |
  | --- | --- | --- |
  | no anticipation | pre-switch window inspection | could not discriminate from noise |

- Data requirements: per-customer switch date and daily retention status
- Threat register:

  | threat | probe | result |
  | --- | --- | --- |
  | seasonality | month-of-year comparison | inconclusive |

- Disposition: unresolved — the probes run could not discriminate

"""

TWO_DESIGN_RECORD = VALID_RECORD.replace("## Handoff", _SECOND_DESIGN_BLOCK + "## Handoff")


def test_handoff_omitting_an_assigned_disposition_rejected() -> None:
    """A two-design record assigning identified-if + unresolved whose Handoff
    hand-carries only identified-if silently drops an assigned disposition --
    rejected: the mentioned set must equal the assigned set."""
    findings, _ = cr.check_record(TWO_DESIGN_RECORD)
    assert any("unresolved" in f and "not carried" in f for f in findings)


def test_handoff_carrying_every_assigned_disposition_accepted() -> None:
    """The known negative: the same two-design record carrying both assigned
    values passes -- set equality, not merely non-fabrication."""
    record = TWO_DESIGN_RECORD.replace(
        "- Dispositions: identified-if",
        "- Dispositions: identified-if, unresolved",
    )
    findings, _ = cr.check_record(record)
    assert findings == []


# --------------------------------------------------------------------------- #
# Hyphen-dash rationale tolerance (2026-08-09 post-review fix) -- the checker
# accepted `none - <rationale>` in the Handoff Dispositions slot but split
# Route/Disposition rationales on the em-dash only, so `identified-if - <why>`
# false-failed the closed-set gate AND ran the forbidden-vocabulary scan over
# rationale prose, contradicting _check_forbidden's own value-token-only
# promise. The dash discipline is now uniform: an em-dash splits anywhere, a
# hyphen-dash splits only when whitespace-padded on both sides, so a token's
# own hyphens (not-constructible) never read as value-plus-rationale.
# --------------------------------------------------------------------------- #
def test_route_with_hyphen_dash_rationale_accepted() -> None:
    record = VALID_RECORD.replace(
        "Route: review", "Route: review - a design is already being presented"
    )
    findings, _ = cr.check_record(record)
    assert findings == []


def test_disposition_with_hyphen_dash_rationale_accepted() -> None:
    record = VALID_RECORD.replace(
        "Disposition: identified-if — parallel trends and no-anticipation both hold",
        "Disposition: identified-if - parallel trends and no-anticipation both hold",
    )
    findings, _ = cr.check_record(record)
    assert findings == []


def test_forbidden_word_in_hyphen_dash_rationale_is_not_flagged() -> None:
    """The value-token isolation must hold for hyphen-dash rationales the same
    as for em-dash ones: 'valid' in the rationale is ordinary vocabulary."""
    record = VALID_RECORD.replace(
        "Disposition: identified-if — parallel trends and no-anticipation both hold",
        "Disposition: identified-if - the instrument is valid only if the "
        "exclusion restriction holds",
    )
    findings, _ = cr.check_record(record)
    assert findings == []


def test_hyphenated_token_own_hyphens_do_not_split() -> None:
    """not-constructible's bare hyphens are part of the token, not a rationale
    separator -- only a whitespace-padded hyphen-dash splits."""
    record = VALID_RECORD.replace(
        "Disposition: identified-if — parallel trends and no-anticipation both hold",
        "Disposition: not-constructible",
    ).replace("- Dispositions: identified-if", "- Dispositions: not-constructible")
    findings, _ = cr.check_record(record)
    assert findings == []


def test_hyphen_dash_rationale_invalid_value_still_rejected() -> None:
    """Stripping a hyphen-dash rationale must not turn an invalid token valid."""
    record = VALID_RECORD.replace(
        "Disposition: identified-if — parallel trends and no-anticipation both hold",
        "Disposition: probably-fine - looks okay",
    )
    findings, _ = cr.check_record(record)
    assert any("disposition" in f.lower() and "probably-fine" in f for f in findings)


# --------------------------------------------------------------------------- #
# Advisory masking is slot-regional (2026-08-09 post-review fix) -- the mask
# previously string-replaced the parsed endpoints value, which silently no-ops
# when the slot is a sublist (the parsed form, joined with `; `, never appears
# in the text), flagging the licensed endpoints themselves. The mask now
# removes the Computed endpoints slot's region whatever shape its value takes.
# --------------------------------------------------------------------------- #
_SUBLIST_ENDPOINTS_RECORD = VALID_BOUND_RECORD.replace(
    "- Computed endpoints: 0.04, 0.31",
    "- Computed endpoints:\n  - lower: 4 percentage points\n  - upper: 31 percentage points",
)


def test_advisory_scan_masks_sublist_endpoints_slot() -> None:
    findings, warnings = cr.check_record(_SUBLIST_ENDPOINTS_RECORD)
    assert findings == []
    assert warnings == []


def test_advisory_scan_still_fires_outside_masked_slot() -> None:
    """Known positive for the mask's scope: the same sublist-endpoints record
    with a point estimate planted in Handoff Facts still warns -- the mask
    covers the slot's region, not the rest of the record."""
    record = _SUBLIST_ENDPOINTS_RECORD.replace(
        "- Facts: observed completion rate rose from 0.41 to 0.52 across the "
        "waitlist-removal boundary",
        "- Facts: the program looks like a 9.58 percentage points lift",
    )
    findings, warnings = cr.check_record(record)
    assert findings == []
    assert any("9.58" in w for w in warnings)


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
