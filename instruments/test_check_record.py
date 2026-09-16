# ruff: noqa: E501 -- the ledger fixture's table rows are literal record data
# whose column widths and content are the thing under test; wrapping them
# would change what a matching real ledger row looks like.
"""The structural validator must catch closed-vocabulary and completeness
violations, must pass every shipped template skeleton (the write-then-fill
workflow is correct work), and must be able to fail."""

import importlib.util
import re
from pathlib import Path

import pytest

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
- Coverage matrix: hour x route, 3.9k-4.4k rows per cell
- Coverage baseline: deploy schedule
- Source completeness semantics: S1 — event unrecorded; export manifest

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | step at 09:10 | window compare | CONSISTENT | S1 rows 1-9 |
| T2 | H2 | coverage hole | coverage matrix | NOT_TESTED | pending |

## Amendments

- none

## Conclusion

- Answer: unresolved
- Best supported: H1, on T1
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | best supported; T1 consistent |
  | H2 | data-artifact | UNRESOLVED | not tested |

- Limitations: T2 not run
"""


DATA_VALIDITY = (
    "## Data Validity\n\n- Collection method: exporter\n"
    "- Coverage matrix: hour x route, 3.9k-4.4k rows per cell\n"
    "- Coverage baseline: deploy schedule\n"
    "- Source completeness semantics: S1 — event unrecorded; export manifest\n\n"
)
CONCLUSION_BODY = (
    "- Answer: unresolved\n- Best supported: H1, on T1\n- Per-hypothesis summary:\n\n"
    "  | id | claim | status | basis |\n  | --- | --- | --- | --- |\n"
    "  | H1 | causal | UNRESOLVED | best supported; T1 consistent |\n"
    "  | H2 | data-artifact | UNRESOLVED | not tested |\n\n- Limitations: T2 not run\n"
)
VOI_SLOTS = (
    "- Route: voi\n- Pending decision: ship vs wait\n- Signal model: a 2-week holdout\n"
    "- Value basis: expected loss avoided\n- Value calculation: 0.4 x 3 = 1.2\n"
    "- Upper bound: 1.5\n- Cost: 1.0\n"
)


def test_good_ledger_passes():
    assert cr.detect(GOOD_LEDGER) == "ledger"
    assert cr.check(GOOD_LEDGER) == []


def test_voi_upper_bound_only_verdict_is_accepted():
    record = (
        "# VoI Record: price unknown\n\n## VoI\n\n" + VOI_SLOTS + "- Verdict: upper-bound-only\n"
    )
    assert cr.check(record) == []


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

- Causal question, restated as a counterfactual contrast: would depot throughput differ had the pilot not run
- Estimand: ATT on weekly throughput
- Assignment mechanism as stated: "the three largest depots were chosen" — ops memo
- Route: review

## Design: pilot-vs-rest difference-in-differences

- Design: difference-in-differences, pilot depots vs the rest
- Identifying assumptions:
  - throughput at pilot and non-pilot depots would have moved in parallel absent the pilot
- Assumption probes:

  | assumption | probe | result |
  | --- | --- | --- |
  | parallel trends | pre-period slope comparison | slopes within 0.2 |

- Data requirements: weekly throughput per depot, 12 pre-weeks
- Threat register:

  | threat | probe | result |
  | --- | --- | --- |
  | concurrent staffing change | staffing log review | none in window |

- Disposition: identified-if — parallel pre-trends; probe attached

## Handoff

- Facts: pre-trend probe run, slopes within 0.2
- Assumptions: parallel trends absent the pilot
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

- Route: decide
- Actions: ship vs wait
- Decision owner: the release manager
- Reversibility: a shipped build can be rolled back in an hour
- Deadline or forcing event: Friday release train
- Consequences:

  | | p true | p false |
  | --- | --- | --- |
  | ship | regression ships | on time |
  | wait | caught | a week lost |

- Loss ratio: 3 — provenance: user-elicited
- Decision threshold (posterior odds): 3:1 — provenance: user-elicited

## Decision-state model

- Proposition: p
- Residual reading: not-p, including causes nobody named
- Claim class: descriptive (estimand: p95 latency)
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 1:1 — provenance: user-elicited
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | T1 consistent | 2 | estimated-from-data-in-hand | ledger T1; checkout p95; US |

- Independence: single item
- Posterior odds: 2:1

## Robustness

- Prior class swept: 1:3 to 3:1
- Loss range swept: 1 to 5
- Crossover: none within swept class

## Verdict

- Verdict: prior-sensitive — crossover at 3:1
- Recommended action: returned to owner
- Conditions: prior class 1:3 to 3:1; losses user-elicited

## Handoff

- Open factual disputes: none
- Identification gaps: none
- VoI question: none
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


def test_escaped_pipe_in_method_cell_is_not_an_outcome():
    """Codex finding: an escaped pipe in a Tests Method cell shifted the
    columns, so a correct ledger was flagged on outcome 'wc -l'."""
    good = GOOD_LEDGER.replace(
        "| T1 | H1 | step at 09:10 | window compare | CONSISTENT | S1 rows 1-9 |",
        "| T1 | H1 | step at 09:10 | grep -c err log \\| wc -l | CONSISTENT | S1 rows 1-9 |",
    )
    assert cr.check(good) == []


def test_fenced_quoted_record_does_not_reject_a_valid_verdict():
    """Codex finding: a fenced excerpt quoting '- Verdict: optimal' inside
    Evidence rejected a decision record whose actual verdict is valid."""
    good = GOOD_DECISION.replace(
        "- Prior odds: 1:1 — provenance: user-elicited",
        "- Prior odds: 1:1 — provenance: user-elicited\n\n```\n- Verdict: optimal\n```",
    )
    assert cr.check(good) == []


def test_tilde_fenced_quote_is_ignored_too():
    good = GOOD_DECISION.replace(
        "- Prior odds: 1:1 — provenance: user-elicited",
        "- Prior odds: 1:1 — provenance: user-elicited\n\n~~~\n- Verdict: optimal\n~~~",
    )
    assert cr.check(good) == []


def test_longer_fence_is_not_closed_by_a_shorter_run():
    """Copilot finding: the closer check ignored fence length, so a ````
    block quoting a ``` fence closed early and its content was scanned."""
    good = GOOD_DECISION.replace(
        "- Verdict: prior-sensitive — crossover at 3:1",
        "- Verdict: prior-sensitive — crossover at 3:1\n\n````\n```\n- Verdict: optimal\n```\n````",
    )
    assert cr.check(good) == []


def test_html_tag_in_prose_does_not_suspend_completeness():
    """Codex finding: any <...> span anywhere marked the record in-progress
    and suppressed every completeness finding."""
    skel = "# Investigation: q?\n\n## Problem\n\nSee <details> below.\n"
    assert any("required section missing" in f for f in cr.check(skel))


def test_decision_record_without_a_verdict_line_is_caught():
    """Codex finding: a decision record with all six headings empty and no
    Verdict line validated clean."""
    empty = (
        "# Decision Record: d?\n\n## Decision frame\n\n## Decision-state model\n\n"
        "## Evidence and update\n\n## Robustness\n\n## Verdict\n\n## Handoff\n"
    )
    assert any("Verdict" in f for f in cr.check(empty))


def test_ledger_table_missing_its_claim_column_is_caught():
    """Codex finding: tables whose headers omit the checked columns passed
    silently because _column returned [] without complaint."""
    bad = (
        GOOD_LEDGER.replace(
            "| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |",
            "| id | note |",
        )
        .replace("| --- | --- | --- | --- | --- | --- | --- | --- |", "| --- | --- |", 1)
        .replace(
            "| H1 | causal | deploy caused step | latency steps at 09:10 | no step at 09:10 | step aligns with deploy window | T1 | logs |",
            "| H1 | banana |",
        )
        .replace(
            "| H2 | data-artifact | exporter gap | gap in coverage | no gap | coverage hole spans the step | T2 | export manifest |",
            "| H2 | banana |",
        )
    )
    assert any("claim" in f and "column" in f for f in cr.check(bad))


def test_review_handoff_without_dispositions_line_is_caught():
    bad = GOOD_REVIEW.replace("- Dispositions: identified-if", "- Notes: none")
    assert any("Dispositions" in f for f in cr.check(bad))


def test_unclosed_fence_suppresses_completeness_not_correctness():
    """An unterminated fence blanks the tail; completeness findings on the
    swallowed sections would fail a correct record, so they are suspended."""
    good = GOOD_DECISION.replace(
        "- Crossover: none within swept class",
        "- Crossover: none within swept class\n\n```\npasted log excerpt",
    )
    findings = cr.check(good)
    assert not any("required section missing" in f for f in findings)
    assert any("unterminated code fence" in f for f in findings)


def test_unclosed_fence_does_not_suppress_prefence_vocab():
    bad = GOOD_DECISION.replace(
        "- Verdict: prior-sensitive — crossover at 3:1", "- Verdict: optimal"
    ).replace(
        "- Open factual disputes: none",
        "- Open factual disputes: none\n\n```\npasted log excerpt",
    )
    assert any("verdict" in f.lower() for f in cr.check(bad))


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


def test_html_commented_structure_is_not_record_content():
    """A record whose headings and verdict sit only inside <!-- --> has none of
    them: commented text is never loaded as content."""
    hidden = (
        "# Decision Record: d\n\n<!--\n## Decision frame\n\n## Decision-state model\n\n"
        "## Evidence and update\n\n## Robustness\n\n## Verdict\n\n- Verdict: robust\n\n"
        "## Handoff\n-->\n"
    )
    findings = cr.check(hidden)
    assert any("required section missing: ## Verdict" in f for f in findings)
    assert any("required section missing: ## Decision frame" in f for f in findings)
    assert not any("verdict 'robust'" in f for f in findings)


def test_comment_stripping_preserves_line_count():
    text = "a\n<!-- one\ntwo\nthree -->\nb\n"
    assert cr._strip_hidden(text)[0].count("\n") == text.count("\n")


def test_unclosed_html_comment_hides_everything_after_it():
    rec = (
        "# Decision Record: d\n\n<!--\n## Decision frame\n\nx\n\n## Decision-state model\n\nx\n\n"
        "## Evidence and update\n\nx\n\n## Robustness\n\nx\n\n## Verdict\n\n- Verdict: robust\n\n"
        "## Handoff\n\nx\n"
    )
    findings = cr.check(rec)
    assert any("required section missing: ## Verdict" in f for f in findings)


def test_comment_opener_inside_a_fence_is_code_not_a_comment():
    rec = "# VoI Record: x\n\n```\n<!--\n```\n\n## VoI\n\n" + VOI_SLOTS + "- Verdict: worth-it\n"
    assert cr.check(rec) == []


def test_fence_closer_with_info_string_does_not_close():
    rec = (
        "# VoI Record: x\n\n```\ntext\n```python\n\n## VoI\n\n"
        + VOI_SLOTS
        + "- Verdict: worth-it\n"
    )
    findings = cr.check(rec)
    assert any("unterminated code fence" in f for f in findings)


def test_double_backtick_code_span_pipe_does_not_shift_cells():
    ledger = GOOD_LEDGER.replace(
        "| T1 | H1 | step at 09:10 | window compare |",
        "| T1 | H1 | step at 09:10 | run ``a | b`` |",
    )
    assert cr.check(ledger) == []


INEQUALITY_DECISION = (
    "# Decision Record: d\n\n## Decision frame\n\n"
    "- Crossover: flips where prior odds < 1.5 or loss ratio > 2\n"
)

BR_LEDGER = GOOD_LEDGER.replace(
    "| H1 | causal | deploy caused step |", "| H1 | causal | deploy<br>caused step |"
).replace(
    "## Sources\n\n| id | Origin (file, query, system) | Acquired | Coverage notes |\n| --- | --- | --- | --- |\n| S1 | logs.csv | 2026-08-18 | full day |\n\n",
    "",
)


def test_inequality_in_a_slot_is_not_a_placeholder():
    findings = cr.check(INEQUALITY_DECISION)
    assert any("required section missing: ## Verdict" in f for f in findings)


def test_br_tag_in_a_cell_is_not_a_placeholder():
    assert "## Sources" not in BR_LEDGER  # the fixture really removed the section
    findings = cr.check(BR_LEDGER)
    assert any("required section missing: ## Sources" in f for f in findings)


def test_template_placeholders_still_count():
    assert cr._has_placeholder("<one-line question>")
    assert cr._has_placeholder(
        "<CONSISTENT / CONTRADICTED / NON_DISCRIMINATING, with evidence pointer>"
    )
    assert cr._has_placeholder("<date>")
    assert not cr._has_placeholder("<br>")
    assert not cr._has_placeholder("<br/>")
    assert not cr._has_placeholder("a < 1.5 or b > 2")
    assert not cr._has_placeholder("<5% and >2%")
    assert not cr._has_placeholder('<a href="x">')
    assert not cr._has_placeholder("<https://dash.internal/funnel>")
    assert not cr._has_placeholder("<name@example.com>")
    assert not cr._has_placeholder("<mailto:ops@example.com>")


def test_autolink_in_a_slot_does_not_suspend_completeness():
    rec = "# Exploration: e\n\n## Frame\n\n- Source: <https://dash.internal/funnel>\n"
    findings = cr.check(rec)
    assert any("required section missing: ## Orientation record" in f for f in findings)


def test_lone_unterminated_fence_is_a_finding_not_a_pass():
    findings = cr.check("# Decision Record: d\n\n## Decision frame\n\n```\n")
    assert findings, "an unterminated fence must not produce a clean pass"
    assert any("unterminated code fence" in f for f in findings)


def test_trailing_whitespace_on_a_heading_is_still_the_heading():
    assert cr.check("# VoI Record: x\n\n## VoI \n\n" + VOI_SLOTS + "- Verdict: worth-it\n") == []


def test_bold_verdict_label_is_still_the_slot():
    assert cr.check("# VoI Record: x\n\n## VoI\n\n" + VOI_SLOTS + "- **Verdict:** worth-it\n") == []
    assert cr.check("# VoI Record: x\n\n## VoI\n\n" + VOI_SLOTS + "- **Verdict**: worth-it\n") == []


def test_bold_verdict_with_bad_value_is_still_caught():
    findings = cr.check("# VoI Record: x\n\n## VoI\n\n" + VOI_SLOTS + "- **Verdict:** optimal\n")
    assert any("verdict 'optimal'" in f for f in findings)


def test_inline_code_pipe_in_method_cell_does_not_shift_outcome():
    ledger = GOOD_LEDGER.replace(
        "| T1 | H1 | step at 09:10 | window compare |", "| T1 | H1 | step at 09:10 | run `a | b` |"
    )
    assert cr.check(ledger) == []


REVIEW_SKELETON = (
    "# Identification Review: q\n\n## Question\n\n"
    "- Causal question, restated as a counterfactual contrast: c\n- Estimand: e\n"
    "- Assignment mechanism as stated: UNSTATED\n- Route: {route}\n\n"
    "## Design: d\n\n- Design: d\n- Identifying assumptions:\n  - a\n- Assumption probes:\n\n"
    "  | assumption | probe | result |\n  | --- | --- | --- |\n  | a | p | r |\n\n"
    "- Data requirements: dr\n- Threat register:\n\n"
    "  | threat | probe | result |\n  | --- | --- | --- |\n  | t | p | r |\n\n"
    "- Disposition: {disp}\n\n"
    "## Handoff\n\n- Facts: f\n- Assumptions: a\n- Dispositions: {disp}\n"
)
BOUND_BLOCK = (
    "## Bound\n\n- Assumption ledger: monotone selection\n- Bound logic: Lee bounds\n"
    "- Computed endpoints: -0.4, 0.9\n\n"
)


def test_annotated_none_disposition_is_accepted():
    rec = REVIEW_SKELETON.format(route="bound", disp="none — bound route assigns none").replace(
        "## Handoff", BOUND_BLOCK + "## Handoff"
    )
    assert cr.check(rec) == []


def test_route_outside_closed_set_is_caught():
    findings = cr.check(REVIEW_SKELETON.format(route="banana", disp="none"))
    assert any("route 'banana'" in f for f in findings)


def test_annotated_route_is_accepted():
    assert cr.check(REVIEW_SKELETON.format(route="construct — no design stated", disp="none")) == []


def test_empty_required_section_is_a_finding():
    findings = cr.check("# Exploration: e\n\n## Frame\n\n## Orientation record\n")
    assert any("required section empty: ## Frame" in f for f in findings)
    assert any("required section empty: ## Orientation record" in f for f in findings)


def test_pending_prose_marks_a_plan_stage_record_in_progress():
    plan = GOOD_LEDGER.replace(CONCLUSION_BODY, "(pending — to be completed after Analysis)\n")
    assert "(pending" in plan
    assert cr.check(plan) == []


def test_prose_beginning_with_pending_does_not_suppress_completeness():
    ledger = GOOD_LEDGER.replace(DATA_VALIDITY, "").replace(
        "- none\n", "Pending replication by the data team, we still report the finding below.\n"
    )
    assert "## Data Validity" not in ledger
    findings = cr.check(ledger)
    assert any("required section missing: ## Data Validity" in f for f in findings)


def test_pending_record_still_reports_bad_vocab():
    plan = GOOD_LEDGER.replace(
        "| T1 | H1 | step at 09:10 | window compare | CONSISTENT |",
        "| T1 | H1 | step at 09:10 | window compare | SUPPORTED |",
    )
    plan = plan.replace(
        CONCLUSION_BODY,
        "(pending — to be completed after Analysis)\n",
    )
    # the section-level pending marker marks it in progress
    assert cr._in_progress(cr._strip_hidden(plan)[0])
    findings = cr.check(plan)
    assert any("outcome 'SUPPORTED'" in f for f in findings)


def test_signature_without_any_required_heading_is_not_a_record():
    note = "# Investigation: prod outage 2026-08-20\n\nTimeline...\n"
    assert cr.detect(note) is None


def test_signature_with_one_required_heading_is_a_record():
    assert cr.detect("# Investigation: x\n\n## Problem\n") == "ledger"


def test_invalid_utf8_is_unreadable_not_a_crash(tmp_path, capsys):
    f = tmp_path / "bad.md"
    f.write_bytes(
        b"# VoI Record: x\n\n## VoI\n\n" + VOI_SLOTS.encode() + b"- Verdict: worth-it \xff\n"
    )
    rc = cr.main([str(f)])
    assert rc == 2  # noqa: PLR2004 -- 2 is the validator's documented exit code
    assert capsys.readouterr().err.startswith("unreadable")


def test_unreadable_file_reports_with_the_prefix_the_hook_keys_on(tmp_path, capsys):
    rc = cr.main([str(tmp_path / "missing.md")])
    assert rc == 2  # noqa: PLR2004 -- 2 is the validator's documented exit code
    assert capsys.readouterr().err.startswith("unreadable")


# --------------------------------------------------------------------------- #
# Copilot review 2026-08-23: the slot-level pending marker matched any value
# merely *starting* with the word, so ordinary prose in a filled slot
# suppressed every completeness finding for the record.
# --------------------------------------------------------------------------- #
def test_prose_in_a_bullet_slot_beginning_with_pending_does_not_suppress():
    ledger = GOOD_LEDGER.replace(DATA_VALIDITY, "").replace(
        "- Answer: unresolved\n",
        "- Answer: Pending replication by another team, the result remains valid\n",
    )
    assert "## Data Validity" not in ledger
    findings = cr.check(ledger)
    assert any("required section missing: ## Data Validity" in f for f in findings), findings


def test_a_bullet_slot_that_says_only_pending_is_still_in_progress():
    ledger = GOOD_LEDGER.replace("- Answer: unresolved\n", "- Answer: pending\n")
    assert cr._in_progress(cr._strip_hidden(ledger)[0])


def test_emphasized_label_without_a_colon_is_not_a_slot():
    findings = cr.check("# VoI Record: x\n\n## VoI\n\n" + VOI_SLOTS + "- **Verdict** worth-it\n")
    assert findings, "a label with no colon delimiter must not satisfy the slot check"


def test_disposition_error_lists_none_as_accepted():
    findings = cr.check(REVIEW_SKELETON.format(route="review", disp="certified"))
    msg = next(f for f in findings if "does not begin with a value" in f)
    assert "none" in msg, msg


def test_hyphenated_prose_beginning_with_pending_does_not_suppress():
    """`pending-state` is one hyphenated word, not the marker plus an
    annotation, so it must not suspend the completeness checks."""
    for value in ("pending-state evaluation is complete", "pending-data analysis found no gaps"):
        ledger = GOOD_LEDGER.replace(DATA_VALIDITY, "").replace(
            "- Answer: unresolved\n", f"- Answer: {value}\n"
        )
        findings = cr.check(ledger)
        assert any("required section missing: ## Data Validity" in f for f in findings), value


def test_spaced_hyphen_annotation_is_still_in_progress():
    ledger = GOOD_LEDGER.replace(
        "- Answer: unresolved\n", "- Answer: pending - waiting on export\n"
    )
    assert cr._in_progress(cr._strip_hidden(ledger)[0])


def test_html_block_tags_are_not_template_placeholders():
    """An HTML tag outside the allowlist read as a placeholder marks the whole
    record in progress and suppresses every completeness finding."""
    for tag in ("<section>", "<blockquote>", "<h1>", "<figure>", "<aside>"):
        ledger = GOOD_LEDGER.replace(DATA_VALIDITY, "").replace(
            "- Answer: unresolved\n", f"- Answer: unresolved {tag} see above\n"
        )
        findings = cr.check(ledger)
        assert any("required section missing: ## Data Validity" in f for f in findings), tag


def test_a_real_template_placeholder_is_still_in_progress():
    ledger = GOOD_LEDGER.replace("- Answer: unresolved\n", "- Answer: <the answer>\n")
    assert cr._in_progress(cr._strip_hidden(ledger)[0])


def test_code_span_runs_pair_only_at_equal_length():
    """Per CommonMark a code span closes on a run of exactly the opener's
    length, so a longer run inside a span is content, not a delimiter."""
    # the span is "x ``` y | z": its pipe is hidden, the three real cell
    # separators outside it are untouched.
    masked = cr._mask_code_pipes("| a `x ``` y | z` b | c |")
    assert masked == "| a `x ``` y \x00 z` b | c |", masked


def test_unpaired_backtick_runs_do_not_hide_a_cell_separator():
    """A 1-backtick opener closes only on a 1-backtick run, so the trailing
    2-run below opens nothing and the pipe is a real cell separator. The
    previous regex paired the runs anyway and masked it, shifting every
    column after it -- the validator then read the wrong cell for Outcome."""
    row = "| T1 | H1 | pattern `a|b`` c | window compare | CONSISTENT | S1 |"
    assert cr._mask_code_pipes(row) == row


def test_escaped_backticks_do_not_hide_a_cell_separator():
    """CommonMark treats a backslash-escaped backtick outside a code span as
    literal text, so it opens nothing and the pipe stays a real separator."""
    row = "| a \\` literal | b \\` c | d |"
    assert cr._mask_code_pipes(row) == row


def test_selectedcontent_is_not_a_template_placeholder():
    ledger = GOOD_LEDGER.replace(DATA_VALIDITY, "").replace(
        "- Answer: unresolved\n", "- Answer: unresolved <selectedcontent> x\n"
    )
    findings = cr.check(ledger)
    assert any("required section missing: ## Data Validity" in f for f in findings), findings


def test_comment_delimiter_inside_inline_code_is_visible_text():
    """CommonMark renders `<!--` in a code span as code, so a record that
    documents the token must not have everything after it blanked."""
    doc = (
        "# Investigation: x\n\n## Problem\n\n"
        "- The token `<!--` opens a comment.\n\n"
        "## Hypotheses\n\n| id |\n| --- |\n| H1 |\n"
    )
    visible, _ = cr._strip_hidden(doc)
    assert "## Hypotheses" in visible, visible


def test_a_real_comment_after_inline_code_still_hides_the_rest():
    doc = "# Investigation: x\n\n- token `<!--` here\n<!--\n## Hypotheses\n"
    visible, _ = cr._strip_hidden(doc)
    assert "## Hypotheses" not in visible, visible


def test_unterminated_fence_finding_carries_no_procedural_instruction():
    """decisions/006: a hook message states structural facts and a pointer to
    the owning authority; the hook forwards these findings verbatim."""
    findings = cr.check(
        "# VoI Record: x\n\n## VoI\n\n" + VOI_SLOTS + "- Verdict: worth-it\n\n```\nopen\n"
    )
    fence = next(f for f in findings if "unterminated code fence" in f)
    assert "re-validate" not in fence, fence
    assert "close the fence" not in fence, fence


def test_uri_autolinks_without_a_double_slash_are_not_placeholders():
    """`<tel:...>` and `<urn:...>` are CommonMark autolinks, i.e. record
    content, so they must not mark the record in progress."""
    for link in ("<tel:+15551212>", "<urn:isbn:0451450523>", "<news:comp.lang.python>"):
        ledger = GOOD_LEDGER.replace(DATA_VALIDITY, "").replace(
            "- Answer: unresolved\n", f"- Answer: unresolved, see {link}\n"
        )
        findings = cr.check(ledger)
        assert any("required section missing: ## Data Validity" in f for f in findings), link


def test_a_template_blank_is_still_a_placeholder():
    ledger = GOOD_LEDGER.replace("- Answer: unresolved\n", "- Answer: <the answer>\n")
    assert cr._in_progress(cr._strip_hidden(ledger)[0])


def test_an_emphasized_pending_slot_is_in_progress():
    """Emphasis on a slot label is presentation, so the emphasized and plain
    forms must reach the same verdict."""
    assert cr._in_progress("## Conclusion\n- **Answer:** pending\n- Notes: x\n")
    assert cr._in_progress("## Conclusion\n- *Answer*: pending\n- Notes: x\n")


def test_a_backtick_fence_info_string_may_not_contain_a_backtick():
    """CommonMark forbids a backtick in a backtick fence's info string, so
    the line is ordinary text and the content after it stays visible."""
    doc = "# Investigation: x\n\n## Problem\n\n```bad`info\n\n## Hypotheses\n\n- a\n"
    visible, _ = cr._strip_hidden(doc)
    assert "## Hypotheses" in visible, visible


def test_a_well_formed_unclosed_fence_still_hides_what_follows():
    doc = "# Investigation: x\n\n## Problem\n\n```python\n\n## Hypotheses\n\n- a\n"
    visible, _ = cr._strip_hidden(doc)
    assert "## Hypotheses" not in visible, visible


def test_html_tags_with_boolean_attributes_are_not_placeholders():
    """`<details open>` is a real tag; a boolean attribute carries no `=`."""
    for tag in ("<details open>", "<td colspan>", "<input disabled>"):
        ledger = GOOD_LEDGER.replace(DATA_VALIDITY, "").replace(
            "- Answer: unresolved\n", f"- Answer: unresolved {tag}\n"
        )
        findings = cr.check(ledger)
        assert any("required section missing: ## Data Validity" in f for f in findings), tag


def test_two_verdicts_joined_by_comma_is_a_finding():
    rec = GOOD_DECISION.replace(
        "- Verdict: prior-sensitive", "- Verdict: prior-sensitive, dominated"
    )
    assert rec != GOOD_DECISION
    findings = cr.check(rec)
    assert any("verdict 'prior-sensitive, dominated" in f for f in findings)


def test_two_routes_joined_by_comma_is_a_finding():
    rec = GOOD_REVIEW.replace("- Route: review", "- Route: review, construct")
    assert rec != GOOD_REVIEW
    findings = cr.check(rec)
    assert any("route 'review, construct' does not begin with" in f for f in findings)


def test_two_dispositions_joined_by_comma_is_a_finding():
    rec = GOOD_REVIEW.replace(
        "- Dispositions: identified-if", "- Dispositions: identified-if, assumption-contradicted"
    )
    assert rec != GOOD_REVIEW
    findings = cr.check(rec)
    assert any("disposition 'identified-if, assumption-contradicted'" in f for f in findings)
    assert not any("slot is missing" in f for f in findings)


@pytest.mark.parametrize(
    ("value", "allowed", "expect"),
    [
        ("REFUTED — see H2 (UNRESOLVED rival)", cr.STATUSES, "REFUTED"),
        ("robust (across the swept class)", cr.DECIDE_VERDICTS, "robust"),
        ("CONSISTENT; rerun pending", cr.OUTCOMES, "CONSISTENT"),
        ("worth-it: at 3x", cr.VOI_VERDICTS, "worth-it"),
        ("review - claimed A/B", cr.ROUTES, "review"),
    ],
)
def test_annotation_after_a_delimiter_is_still_accepted(value, allowed, expect):
    assert cr._leading_token(value, allowed) == expect


def test_unnecessary_prediction_does_not_satisfy_necessary_prediction():
    rec = GOOD_LEDGER.replace("Necessary prediction (failure refutes)", "Unnecessary prediction")
    assert rec != GOOD_LEDGER
    findings = cr.check(rec)
    assert any("lacks a 'necessary prediction' column" in f for f in findings)


def test_outcome_rationale_does_not_satisfy_outcome():
    rec = GOOD_LEDGER.replace("| Outcome |", "| Outcome rationale |")
    assert rec != GOOD_LEDGER
    assert any("lacks a 'outcome' column" in f for f in cr.check(rec))


def test_outcome_with_a_parenthetical_does_not_satisfy_outcome():
    rec = GOOD_LEDGER.replace("| Outcome |", "| Outcome (rationale) |")
    assert rec != GOOD_LEDGER
    assert any("lacks a 'outcome' column" in f for f in cr.check(rec))


def test_the_template_header_alias_still_matches():
    assert cr._header_key("Necessary prediction (failure refutes)") == "necessary prediction"
    assert cr._header_key("  Outcome ") == "outcome"
    assert cr._header_key("Outcome (rationale)") == "outcome (rationale)"


def test_frontmatter_does_not_hide_a_record():
    rec = "---\ntags: [analysis]\n---\n" + GOOD_LEDGER.replace("CONSISTENT", "SUPPORTED")
    assert any("outcome" in f.lower() for f in cr.check(rec))


def test_crlf_frontmatter_does_not_hide_a_record():
    rec = "---\r\ntags: [analysis]\r\n---\r\n" + GOOD_LEDGER.replace("CONSISTENT", "SUPPORTED")
    assert any("outcome" in f.lower() for f in cr.check(rec))


def test_frontmatter_alone_is_not_a_record():
    assert cr.detect("---\ntitle: x\n---\n# Notes\n") is None


def test_unterminated_frontmatter_is_left_alone():
    assert cr.strip_frontmatter("---\ntitle: x\n# Investigation: y\n") == (
        "---\ntitle: x\n# Investigation: y\n"
    )


# 2026-09-15 Codex review: four records missing most of their required
# fields validated clean, because only headings and closed vocabularies were
# checked. Each probe below is one of the review's reproductions.


def test_decision_record_of_done_sections_is_incomplete():
    rec = (
        "# Decision Record: probe\n\n"
        + "".join(
            f"{h}\n\nDone.\n\n" for h in cr.REQUIRED_SECTIONS["decision"] if h != "## Verdict"
        )
        + "## Verdict\n\n- Verdict: robust\n"
    )
    findings = cr.check(rec)
    assert any("'- Actions:' slot is missing" in f for f in findings)
    assert any("'- Decision owner:' slot is missing" in f for f in findings)
    assert any("'- Recommended action:' slot is missing" in f for f in findings)


def test_voi_record_of_only_a_verdict_is_incomplete():
    findings = cr.check("# VoI Record: probe\n\n## VoI\n\n- Verdict: worth-it\n")
    assert any("'- Pending decision:' slot is missing" in f for f in findings)
    assert any("'- Value calculation:' slot is missing" in f for f in findings)


def test_review_of_question_and_handoff_only_is_incomplete():
    rec = (
        "# Identification Review: probe\n\n## Question\n\nDoes X cause Y?\n\n"
        "## Handoff\n\n- Dispositions: identified-if\n"
    )
    findings = cr.check(rec)
    assert any("'- Route:' slot is missing" in f for f in findings)
    assert any("'- Facts:' slot is missing" in f for f in findings)


def test_one_pending_slot_still_suspends_completeness_by_default():
    """A plan-stage record is legitimately incomplete; the default mode keeps
    the in-progress rule. --final is where completeness is demanded."""
    rec = (
        "# Decision Record: probe\n\n## Decision frame\n\n- Decision owner: pending\n\n"
        "## Verdict\n\n- Verdict: robust\n"
    )
    assert cr.check(rec) == []
    findings = cr.check(rec, final=True)
    assert any("required section missing: ## Robustness" in f for f in findings)
    assert any("'Decision owner' is still unfilled: 'pending'" in f for f in findings)


def test_final_mode_flags_placeholders_and_ellipses():
    rec = GOOD_DECISION.replace("- Proposition: p", "- Proposition: <the claim>").replace(
        "- Crossover: none within swept class", "- Crossover: ..."
    )
    assert cr.check(rec) == []
    findings = cr.check(rec, final=True)
    assert any("'Proposition' is still unfilled" in f for f in findings)
    assert any("'Crossover' is still unfilled" in f for f in findings)


def test_final_mode_passes_a_complete_record():
    for rec in (GOOD_LEDGER, GOOD_REVIEW, GOOD_DECISION):
        assert cr.check(rec, final=True) == []


def test_empty_slot_value_is_a_finding():
    bad = GOOD_DECISION.replace("- Decision owner: the release manager", "- Decision owner:")
    assert any("required slot 'Decision owner' is empty" in f for f in cr.check(bad))


def test_exploration_frame_slots_are_required():
    rec = (
        "# Exploration: e\n\n## Frame\n\n- Scope: orders.csv\n\n"
        "## Orientation record\n\n- Schema and grain: one row per order\n"
    )
    findings = cr.check(rec)
    assert any("'- Effort budget:' slot is missing" in f for f in findings)
    assert any("'- Absence semantics:' slot is missing" in f for f in findings)
    assert not any("Confirmation reservation" in f for f in findings)  # profile route has none


def test_ledger_data_validity_slots_are_required():
    bad = GOOD_LEDGER.replace(
        "- Source completeness semantics: S1 — event unrecorded; export manifest\n", ""
    )
    assert any("'- Source completeness semantics:' slot is missing" in f for f in cr.check(bad))


def test_required_slots_exist_in_shipped_templates():
    """Parity: every slot label this validator requires appears, as a
    `- label:` bullet, in the shipped template of that record kind, so a
    renamed template slot fails here rather than orphaning the check."""
    blocks: dict[str, list[str]] = {}
    for path in TEMPLATE_FILES:
        for block in re.findall(r"```markdown\n(.*?)```", path.read_text(encoding="utf-8"), re.S):
            kind = cr.detect(block)
            if kind is not None:
                blocks.setdefault(kind, []).append(block)
    for kind, sections in cr.REQUIRED_SLOTS.items():
        assert kind in blocks, kind
        for heading, labels in sections.items():
            for label in labels:
                assert any(f"- {label}:" in cr._section(b, heading) for b in blocks[kind]), (
                    kind,
                    heading,
                    label,
                )


def test_final_flag_on_the_cli(tmp_path, capsys):
    f = tmp_path / "r.md"
    f.write_text(GOOD_DECISION.replace("- Proposition: p", "- Proposition: <the claim>"))
    assert cr.main([str(f)]) == 0
    assert cr.main(["--final", str(f)]) == 1
    assert "still unfilled" in capsys.readouterr().out


# Codex review pass 1 (2026-09-15): final mode still accepted an identification
# review with no Design block, a bound record with no Bound block, a decision
# record with no Consequences or Evidence table, and a `<status>` placeholder
# in a Conclusion cell.


def test_review_route_without_a_design_block_is_caught():
    rec = re.sub(r"## Design: .*?\n\n(?=## Handoff)", "", GOOD_REVIEW, flags=re.S)
    assert "## Design" not in rec
    findings = cr.check(rec, final=True)
    assert any("no '## Design: <name>' block" in f for f in findings)


def test_design_block_without_a_disposition_is_caught():
    rec = GOOD_REVIEW.replace(
        "- Disposition: identified-if — parallel pre-trends; probe attached", "- Notes: n"
    )
    assert any(
        "## Design: pilot-vs-rest difference-in-differences: required '- Disposition:'" in f
        for f in cr.check(rec)
    )


def test_bound_route_without_a_bound_block_is_caught():
    rec = REVIEW_SKELETON.format(route="bound", disp="none")
    findings = cr.check(rec, final=True)
    assert any("required section missing: ## Bound" in f for f in findings)
    assert cr.check(rec.replace("## Handoff", BOUND_BLOCK + "## Handoff"), final=True) == []


def test_bound_block_missing_a_slot_is_caught():
    rec = REVIEW_SKELETON.format(route="bound", disp="none").replace(
        "## Handoff", BOUND_BLOCK.replace("- Bound logic: Lee bounds\n", "") + "## Handoff"
    )
    assert any("## Bound: required '- Bound logic:' slot is missing" in f for f in cr.check(rec))


def test_decision_without_consequences_table_is_caught():
    rec = re.sub(r"- Consequences:\n\n(  \|.*\n)+\n", "", GOOD_DECISION)
    assert "Consequences" not in rec
    assert any("'- Consequences:' slot is missing" in f for f in cr.check(rec, final=True))
    rec2 = re.sub(r"(- Consequences:\n)\n(  \|.*\n)+", r"\1", GOOD_DECISION)
    assert any("'- Consequences:' has no table" in f for f in cr.check(rec2, final=True))


def test_decision_without_evidence_table_is_caught():
    rec = re.sub(r"- Evidence:\n\n(  \|.*\n)+\n", "", GOOD_DECISION)
    assert "- Evidence:" not in rec
    assert any("'- Evidence:' slot is missing" in f for f in cr.check(rec, final=True))


def test_final_mode_rejects_placeholder_table_cells():
    rec = GOOD_LEDGER.replace("| H1 | causal | UNRESOLVED |", "| H1 | causal | <status> |")
    assert cr.check(rec) == []  # default mode: a placeholder marks the record in progress
    findings = cr.check(rec, final=True)
    assert any("Conclusion: cell still unfilled: '<status>'" in f for f in findings)
    rec = GOOD_LEDGER.replace("| CONSISTENT |", "| <outcome> |")
    assert any("Tests: cell still unfilled" in f for f in cr.check(rec, final=True))
    rec = GOOD_LEDGER.replace("step aligns with deploy window", "<prediction>")
    assert any("Hypotheses row 1: cell still unfilled" in f for f in cr.check(rec, final=True))
    rec = GOOD_DECISION.replace(
        "- Verdict: prior-sensitive — crossover at 3:1", "- Verdict: <value>"
    )
    assert any("Verdict: cell still unfilled" in f for f in cr.check(rec, final=True))


# Codex review pass 2: a Design block of one Disposition line, a Bound block of
# empty / placeholder / pending values, a placeholder Evidence row, and a
# `pending` necessary prediction all passed --final.


def test_design_block_of_only_a_disposition_is_incomplete():
    rec = re.sub(
        r"(## Design: pilot-vs-rest difference-in-differences\n\n).*?(- Disposition: [^\n]*\n)",
        r"\1\2",
        GOOD_REVIEW,
        flags=re.S,
    )
    assert "Identifying assumptions" not in rec
    findings = cr.check(rec, final=True)
    h = "## Design: pilot-vs-rest difference-in-differences"
    assert f"{h}: required '- Design:' slot is missing" in findings
    assert f"{h}: required '- Identifying assumptions:' slot is missing" in findings
    assert f"{h}: required '- Assumption probes:' slot is missing" in findings
    assert f"{h}: required '- Data requirements:' slot is missing" in findings
    assert f"{h}: required '- Threat register:' slot is missing" in findings


def test_design_nested_structures_must_have_content():
    rec = GOOD_REVIEW.replace(
        "  - throughput at pilot and non-pilot depots would have moved in parallel absent the pilot\n",
        "",
    ).replace("  | parallel trends | pre-period slope comparison | slopes within 0.2 |\n", "")
    findings = cr.check(rec, final=True)
    assert any("'- Identifying assumptions:' has no items under it" in f for f in findings)
    assert any("'- Assumption probes:' has no table rows under it" in f for f in findings)


def test_bound_block_template_state_is_caught_in_final_mode():
    bound = (
        "## Bound\n\n- Assumption ledger:\n- Bound logic: <logic>\n"
        "- Computed endpoints: pending\n\n"
    )
    rec = REVIEW_SKELETON.format(route="bound", disp="none").replace(
        "## Handoff", bound + "## Handoff"
    )
    findings = cr.check(rec, final=True)
    assert "## Bound: required slot 'Assumption ledger' is empty" in findings
    assert "## Bound: required slot 'Bound logic' is still unfilled: '<logic>'" in findings
    assert "## Bound: required slot 'Computed endpoints' is still unfilled: 'pending'" in findings


def test_placeholder_evidence_row_is_caught_in_final_mode():
    rec = GOOD_DECISION.replace(
        "  | T1 consistent | 2 | estimated-from-data-in-hand | ledger T1; checkout p95; US |",
        "  | <item> | <ratio> | <class> | <source> |",
    )
    assert cr.check(rec) == []
    findings = cr.check(rec, final=True)
    assert any("'- Evidence:' row 1 cell still unfilled: '<item>'" in f for f in findings)


def test_pending_necessary_prediction_is_caught_in_final_mode():
    rec = GOOD_LEDGER.replace("step aligns with deploy window", "pending")
    assert cr.check(rec) == []  # a bare pending cell is ordinary content in default mode
    assert any(
        "Hypotheses row 1: cell still unfilled: 'pending'" in f for f in cr.check(rec, final=True)
    )


# Codex review pass 3: empty cells and `pending` in code spans passed --final;
# a nested table of any shape satisfied the Evidence requirement.


def test_final_mode_rejects_empty_and_formatted_pending_values():
    assert cr._unfilled("")
    assert cr._unfilled("`pending`")
    assert cr._unfilled("**...**")
    assert not cr._unfilled("`UNRESOLVED`")
    rec = GOOD_LEDGER.replace("| H1 | causal | UNRESOLVED |", "| H1 | causal | |")
    assert any("Conclusion: cell still unfilled: ''" in f for f in cr.check(rec, final=True))
    rec = GOOD_LEDGER.replace("| CONSISTENT |", "| |")
    assert any("Tests: cell still unfilled: ''" in f for f in cr.check(rec, final=True))
    rec = GOOD_REVIEW.replace("| slopes within 0.2 |", "| |")
    assert any(
        "'- Assumption probes:' row 1 cell still unfilled: ''" in f
        for f in cr.check(rec, final=True)
    )
    rec = GOOD_DECISION.replace(
        "  | T1 consistent | 2 | estimated-from-data-in-hand | ledger T1; checkout p95; US |",
        "  | T1 consistent | | | |",
    )
    assert any(
        "'- Evidence:' row 1 cell still unfilled: ''" in f for f in cr.check(rec, final=True)
    )
    rec = GOOD_DECISION.replace(
        "- Decision owner: the release manager", "- Decision owner: `pending`"
    )
    assert cr.check(rec) == []  # a formatted pending marker still means in progress
    assert any(
        "'Decision owner' is still unfilled: '`pending`'" in f for f in cr.check(rec, final=True)
    )


def test_nested_tables_need_their_template_columns():
    rec = GOOD_DECISION.replace(
        "  | item | LR | provenance | source, reference class, conditioning |",
        "  | anything | whatever | arbitrary | other |",
    )
    findings = cr.check(rec, final=True)
    assert "## Evidence and update: '- Evidence:' table lacks a 'item' column" in findings
    assert "## Evidence and update: '- Evidence:' table lacks a 'lr' column" in findings
    assert "## Evidence and update: '- Evidence:' table lacks a 'provenance' column" in findings
    rec = GOOD_REVIEW.replace("  | threat | probe | result |", "  | a | b | c |")
    assert any("'- Threat register:' table lacks a 'threat' column" in f for f in cr.check(rec))
    rec = GOOD_DECISION.replace(
        "  | ship | regression ships | on time |", "  | ship | regression ships |"
    )
    assert any("'- Consequences:' row 1 has 2 cells, header has 3" in f for f in cr.check(rec))
    assert cr.check(GOOD_DECISION, final=True) == []
    assert cr.check(GOOD_REVIEW, final=True) == []


def test_evidence_table_needs_its_source_column():
    """Final review 2026-09-15: a record could drop the whole source column."""
    rec = GOOD_DECISION.replace(
        "  | item | LR | provenance | source, reference class, conditioning |",
        "  | item | LR | provenance |",
    ).replace(
        "  | --- | --- | --- | --- |\n  | T1 consistent", "  | --- | --- | --- |\n  | T1 consistent"
    )
    rec = rec.replace(
        "  | T1 consistent | 2 | estimated-from-data-in-hand | ledger T1; checkout p95; US |",
        "  | T1 consistent | 2 | estimated-from-data-in-hand |",
    )
    assert any(
        "'- Evidence:' table lacks a 'source, reference class, conditioning' column" in f
        for f in cr.check(rec, final=True)
    )


# Re-review 2026-09-15: the VoI record's prose slots may continue on the
# following paragraph (check_decision.py accepts that form); the structural
# validator read only the label's line and reported the slot empty.


def test_multiline_voi_prose_slot_is_read_as_filled():
    rec = (
        "# VoI Record: x\n\n## VoI\n\n- Route: voi\n- Pending decision: ship vs wait\n"
        "- Signal model:\n\n  a 2-week holdout that reports the p95 gap with a 40 ms band\n\n"
        "- Value basis: expected loss avoided\n- Value calculation:\n\n"
        "  0.4 probability of a flip times a loss of 3 is 1.2\n\n"
        "- Upper bound: 1.5\n- Cost: 1.0\n- Verdict: worth-it\n"
    )
    assert cr.check(rec) == []
    assert cr.check(rec, final=True) == []


def test_multiline_slot_with_no_continuation_is_still_empty():
    rec = (
        "# VoI Record: x\n\n## VoI\n\n- Route: voi\n- Pending decision: ship vs wait\n"
        "- Signal model:\n- Value basis: expected loss avoided\n- Value calculation: 1.2\n"
        "- Upper bound: 1.5\n- Cost: 1.0\n- Verdict: worth-it\n"
    )
    assert any("required slot 'Signal model' is empty" in f for f in cr.check(rec))


# PR #34 review: final mode checked placeholder state only in selected labels
# and columns, so a caller asking for completed-record validation could get a
# clean result without source provenance or a populated test method; and the
# slot reader ended a value at the first nested bullet, reporting filled slots
# empty in default mode, which every record write runs.


def test_final_mode_rejects_a_required_section_left_pending():
    rec = GOOD_LEDGER.replace(
        "| id | Origin (file, query, system) | Acquired | Coverage notes |\n"
        "| --- | --- | --- | --- |\n| S1 | logs.csv | 2026-08-18 | full day |",
        "pending",
    )
    assert any(
        "required section still unfilled: ## Sources" in f for f in cr.check(rec, final=True)
    )
    # Default mode keeps treating it as the sanctioned plan-stage state.
    assert cr.check(rec) == []


def test_final_mode_rejects_an_unfilled_required_table_cell():
    rec = GOOD_LEDGER.replace("window compare", "<method>")
    assert any(
        "## Tests row 1: 'method' cell still unfilled: '<method>'" in f
        for f in cr.check(rec, final=True)
    )


def test_a_row_narrower_than_its_header_is_reported_in_both_modes():
    rec = GOOD_LEDGER.replace(
        "| T1 | H1 | step at 09:10 | window compare | CONSISTENT | S1 rows 1-9 |\n"
        "| T2 | H2 | coverage hole | coverage matrix | NOT_TESTED | pending |",
        "| T1 |\n| T2 |",
    )
    for mode in (cr.check(rec), cr.check(rec, final=True)):
        assert any("## Tests row 1: has 1 cells, header has 6" in f for f in mode)
        assert any("## Tests row 2: has 1 cells, header has 6" in f for f in mode)


def test_final_mode_keeps_pending_evidence_on_a_not_tested_row():
    # GOOD_LEDGER's T2 is NOT_TESTED with `pending` evidence: the row's honest
    # state, not template residue.
    assert cr.check(GOOD_LEDGER, final=True) == []
    rec = GOOD_LEDGER.replace(
        "| T2 | H2 | coverage hole | coverage matrix | NOT_TESTED | pending |",
        "| T2 | H2 | coverage hole | coverage matrix | CONSISTENT | pending |",
    )
    assert any(
        "## Tests row 2: 'evidence' cell still unfilled: 'pending'" in f
        for f in cr.check(rec, final=True)
    )


def test_a_slot_value_written_as_a_nested_list_is_not_empty():
    rec = GOOD_LEDGER.replace(
        "- Coverage matrix: hour x route, 3.9k-4.4k rows per cell",
        "- Coverage matrix:\n  - hour x route: 3.9k-4.4k rows per cell\n"
        "  - weekday x route: 2.1k-2.6k rows per cell",
    )
    assert cr.check(rec) == []
    assert cr.check(rec, final=True) == []


def test_a_nested_list_of_placeholders_is_still_unfilled_in_final_mode():
    rec = GOOD_LEDGER.replace(
        "- Coverage matrix: hour x route, 3.9k-4.4k rows per cell",
        "- Coverage matrix:\n  - <cell>: <count>",
    )
    assert any(
        "required slot 'Coverage matrix' is still unfilled" in f for f in cr.check(rec, final=True)
    )


def test_an_unindented_sibling_bullet_still_ends_a_slot_value():
    rec = GOOD_LEDGER.replace(
        "- Coverage matrix: hour x route, 3.9k-4.4k rows per cell",
        "- Coverage matrix:",
    )
    assert any("required slot 'Coverage matrix' is empty" in f for f in cr.check(rec))
