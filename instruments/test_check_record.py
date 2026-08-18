# ruff: noqa: E501 -- the ledger fixture's table rows are literal record data
# whose column widths and content are the thing under test; wrapping them
# would change what a matching real ledger row looks like.
"""The structural validator must catch closed-vocabulary and completeness
violations, must pass every shipped template skeleton (the write-then-fill
workflow is correct work), and must be able to fail."""

import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("check_record", HERE / "check_record.py")
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

REPO = HERE.parent

TEMPLATE_FILES = [
    REPO / "skills/hypothesis-driven-analysis/references/ledger-template.md",
    REPO / "skills/exploratory-data-analysis/references/exploration-log-template.md",
    REPO / "skills/causal-identification-review/references/identification-review-template.md",
    REPO / "skills/decision-analysis/references/decision-record-template.md",
]

GOOD_LEDGER = """\
# Investigation: did the deploy cause the 09:10 step?

## Problem

- Decision informed: rollback or keep
- Falsifiable question: q
- Success criteria: answered means x
- Stop condition: s
- Effort budget: 20 tool calls

## Hypotheses

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | deploy caused step | latency steps at 09:10 | no step at 09:10 | step aligns with deploy window | T1 | logs |
| H2 | data-artifact | exporter gap | gap in coverage | no gap | coverage hole spans the step | T2 | export manifest |

## Sources

| id | Origin (file, query, system) | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | logs.csv | 2026-08-18 | full day |

## Data Validity

- Collection method: exporter

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | step at 09:10 | window compare | CONSISTENT | S1 rows 1-9 |
| T2 | H2 | coverage hole | coverage matrix | NOT_TESTED | pending |

## Amendments

- none

## Conclusion

- Answer: unresolved
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | best supported; T1 consistent |
  | H2 | data-artifact | UNRESOLVED | not tested |
"""


def test_good_ledger_passes():
    assert cr.detect(GOOD_LEDGER) == "ledger"
    assert cr.check(GOOD_LEDGER) == []


def test_shipped_templates_validate_clean():
    """The skills mandate write-template-then-fill; a validator that flags a
    fresh skeleton fails correct work. Every record-shaped fenced block in the
    shipped templates must validate clean."""
    found = 0
    for path in TEMPLATE_FILES:
        text = path.read_text(encoding="utf-8")
        for block in re.findall(r"```markdown\n(.*?)```", text, re.S):
            if cr.detect(block) is None:
                continue
            found += 1
            assert cr.check(block) == [], (path.name, cr.check(block))
    assert found >= 4  # ledger, exploration, review, decision/voi at minimum  # noqa: PLR2004


def test_supported_status_is_caught():
    bad = GOOD_LEDGER.replace("| H1 | causal | UNRESOLVED |", "| H1 | causal | SUPPORTED |")
    assert any("status" in f for f in cr.check(bad))


def test_invented_claim_class_is_caught():
    bad = GOOD_LEDGER.replace("| H1 | causal |", "| H1 | associative |", 1)
    assert any("claim" in f for f in cr.check(bad))


def test_empty_necessary_prediction_is_caught():
    bad = GOOD_LEDGER.replace("step aligns with deploy window", "")
    assert any("necessary" in f.lower() for f in cr.check(bad))


def test_bad_outcome_is_caught():
    bad = GOOD_LEDGER.replace("| CONSISTENT |", "| SUPPORTED |")
    assert any("outcome" in f.lower() for f in cr.check(bad))


def test_prefix_smuggling_is_caught():
    """Substring matching would accept INCONSISTENT; token matching must not."""
    bad = GOOD_LEDGER.replace("| CONSISTENT |", "| INCONSISTENT |")
    assert any("outcome" in f.lower() for f in cr.check(bad))


def test_annotated_outcome_is_accepted():
    good = GOOD_LEDGER.replace(
        "| CONSISTENT |", "| CONSISTENT — adequacy: 0.02 ± 0.01 (variants: all) |"
    )
    assert cr.check(good) == []


def test_code_span_value_is_accepted():
    good = GOOD_LEDGER.replace("| H1 | causal | UNRESOLVED |", "| H1 | causal | `UNRESOLVED` |")
    assert cr.check(good) == []


def test_missing_section_is_caught():
    bad = GOOD_LEDGER.replace("## Data Validity\n\n- Collection method: exporter\n", "")
    assert any("Data Validity" in f for f in cr.check(bad))


def test_empty_hypotheses_table_is_caught():
    bad = re.sub(r"\| H1 \| causal \|.*\n\| H2 \| data-artifact \|.*\n", "", GOOD_LEDGER)
    assert any("Hypotheses" in f for f in cr.check(bad))


def test_in_progress_record_reports_no_completeness_findings():
    """A skeleton mid-fill (placeholders present, sections not yet written)
    is correct work and must be silent on completeness."""
    skeleton = (
        "# Investigation: <one-line question>\n\n"
        "## Problem\n\n- Decision informed: <what>\n\n"
        "## Hypotheses\n\n"
        "| id | claim | Necessary prediction (failure refutes) |\n"
        "| --- | --- | --- |\n"
        "| H1 | causal | <prediction> |\n"
    )
    assert cr.check(skeleton) == []


def test_in_progress_record_still_reports_filled_bad_vocab():
    skeleton = (
        "# Investigation: <one-line question>\n\n"
        "## Hypotheses\n\n"
        "| id | claim | Necessary prediction (failure refutes) |\n"
        "| --- | --- | --- |\n"
        "| H1 | associative | <prediction> |\n"
    )
    assert any("claim" in f for f in cr.check(skeleton))


GOOD_REVIEW = """\
# Identification Review: does the depot comparison identify the effect?

## Question

- Route: review

## Design: pilot-vs-rest difference-in-differences

- Disposition: identified-if — parallel pre-trends; probe attached

## Handoff

- Dispositions: identified-if
"""


def test_good_review_passes():
    assert cr.detect(GOOD_REVIEW) == "review"
    assert cr.check(GOOD_REVIEW) == []


def test_certifying_disposition_is_caught():
    bad = GOOD_REVIEW.replace("identified-if — parallel pre-trends; probe attached", "valid")
    assert any("disposition" in f.lower() for f in cr.check(bad))


GOOD_DECISION = """\
# Decision Record: ship or wait?

## Decision frame

- Actions: ship vs wait

## Decision-state model

- Proposition: p

## Evidence and update

- Prior odds: 1:1 — provenance: sensitivity-only

## Robustness

- Crossover: none within swept class

## Verdict

- Verdict: prior-sensitive — crossover at 3:1

## Handoff

- Open factual disputes: none
"""


def test_good_decision_passes():
    assert cr.detect(GOOD_DECISION) == "decision"
    assert cr.check(GOOD_DECISION) == []


def test_optimal_verdict_is_caught():
    bad = GOOD_DECISION.replace(
        "- Verdict: prior-sensitive — crossover at 3:1", "- Verdict: optimal"
    )
    assert any("verdict" in f.lower() for f in cr.check(bad))


def test_verdict_prefix_smuggling_is_caught():
    bad = GOOD_DECISION.replace(
        "- Verdict: prior-sensitive — crossover at 3:1", "- Verdict: robustly-optimal"
    )
    assert any("verdict" in f.lower() for f in cr.check(bad))


def test_non_record_detects_none():
    assert cr.detect("# Some Notes\n\nhello\n") is None


def test_required_headings_exist_in_shipped_templates():
    """Parity: every heading this validator requires appears in the template
    that owns that record type, so a template rename must fail here."""
    templates = {
        "ledger": REPO / "skills/hypothesis-driven-analysis/references/ledger-template.md",
        "exploration": REPO
        / "skills/exploratory-data-analysis/references/exploration-log-template.md",
        "review": REPO
        / "skills/causal-identification-review/references/identification-review-template.md",
        "decision": REPO / "skills/decision-analysis/references/decision-record-template.md",
        "voi": REPO / "skills/decision-analysis/references/decision-record-template.md",
    }
    for kind, sections in cr.REQUIRED_SECTIONS.items():
        text = templates[kind].read_text(encoding="utf-8")
        for heading in sections:
            assert heading in text, (kind, heading)
