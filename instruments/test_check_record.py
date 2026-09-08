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


def test_voi_upper_bound_only_verdict_is_accepted():
    record = "# VoI Record: price unknown\n\n## VoI\n\n- Verdict: upper-bound-only\n"
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
        "- Prior odds: 1:1 — provenance: sensitivity-only",
        "- Prior odds: 1:1 — provenance: sensitivity-only\n\n```\n- Verdict: optimal\n```",
    )
    assert cr.check(good) == []


def test_tilde_fenced_quote_is_ignored_too():
    good = GOOD_DECISION.replace(
        "- Prior odds: 1:1 — provenance: sensitivity-only",
        "- Prior odds: 1:1 — provenance: sensitivity-only\n\n~~~\n- Verdict: optimal\n~~~",
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
    assert any("'- Verdict:' slot is missing" in f for f in findings)


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
    rec = "# VoI Record: x\n\n```\n<!--\n```\n\n## VoI\n\n- Verdict: worth-it\n"
    assert cr.check(rec) == []


def test_fence_closer_with_info_string_does_not_close():
    rec = "# VoI Record: x\n\n```\ntext\n```python\n\n## VoI\n\n- Verdict: worth-it\n"
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
    assert cr.check("# VoI Record: x\n\n## VoI \n\n- Verdict: worth-it\n") == []


def test_bold_verdict_label_is_still_the_slot():
    assert cr.check("# VoI Record: x\n\n## VoI\n\n- **Verdict:** worth-it\n") == []
    assert cr.check("# VoI Record: x\n\n## VoI\n\n- **Verdict**: worth-it\n") == []


def test_bold_verdict_with_bad_value_is_still_caught():
    findings = cr.check("# VoI Record: x\n\n## VoI\n\n- **Verdict:** optimal\n")
    assert any("verdict 'optimal'" in f for f in findings)


def test_inline_code_pipe_in_method_cell_does_not_shift_outcome():
    ledger = GOOD_LEDGER.replace(
        "| T1 | H1 | step at 09:10 | window compare |", "| T1 | H1 | step at 09:10 | run `a | b` |"
    )
    assert cr.check(ledger) == []


REVIEW_SKELETON = (
    "# Identification Review: q\n\n## Question\n\n- Route: {route}\n\n"
    "## Handoff\n\n- Dispositions: {disp}\n"
)


def test_annotated_none_disposition_is_accepted():
    assert (
        cr.check(REVIEW_SKELETON.format(route="bound", disp="none — bound route assigns none"))
        == []
    )


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
    plan = GOOD_LEDGER.replace(
        "- Answer: unresolved\n- Per-hypothesis summary:\n\n  | id | claim | status | basis |\n  | --- | --- | --- | --- |\n  | H1 | causal | UNRESOLVED | best supported; T1 consistent |\n  | H2 | data-artifact | UNRESOLVED | not tested |\n",
        "(pending — to be completed after Analysis)\n",
    )
    assert "(pending" in plan
    assert cr.check(plan) == []


def test_prose_beginning_with_pending_does_not_suppress_completeness():
    ledger = GOOD_LEDGER.replace(
        "## Data Validity\n\n- Collection method: exporter\n\n", ""
    ).replace(
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
        "- Answer: unresolved\n- Per-hypothesis summary:\n\n"
        "  | id | claim | status | basis |\n  | --- | --- | --- | --- |\n"
        "  | H1 | causal | UNRESOLVED | best supported; T1 consistent |\n"
        "  | H2 | data-artifact | UNRESOLVED | not tested |\n",
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
    f.write_bytes(b"# VoI Record: x\n\n## VoI\n\n- Verdict: worth-it \xff\n")
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
    ledger = GOOD_LEDGER.replace(
        "## Data Validity\n\n- Collection method: exporter\n\n", ""
    ).replace(
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
    findings = cr.check("# VoI Record: x\n\n## VoI\n\n- **Verdict** worth-it\n")
    assert findings, "a label with no colon delimiter must not satisfy the slot check"


def test_disposition_error_lists_none_as_accepted():
    findings = cr.check(REVIEW_SKELETON.format(route="review", disp="certified"))
    msg = next(f for f in findings if "does not begin with a value" in f)
    assert "none" in msg, msg


def test_hyphenated_prose_beginning_with_pending_does_not_suppress():
    """`pending-state` is one hyphenated word, not the marker plus an
    annotation, so it must not suspend the completeness checks."""
    for value in ("pending-state evaluation is complete", "pending-data analysis found no gaps"):
        ledger = GOOD_LEDGER.replace(
            "## Data Validity\n\n- Collection method: exporter\n\n", ""
        ).replace("- Answer: unresolved\n", f"- Answer: {value}\n")
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
        ledger = GOOD_LEDGER.replace(
            "## Data Validity\n\n- Collection method: exporter\n\n", ""
        ).replace("- Answer: unresolved\n", f"- Answer: unresolved {tag} see above\n")
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
    ledger = GOOD_LEDGER.replace(
        "## Data Validity\n\n- Collection method: exporter\n\n", ""
    ).replace("- Answer: unresolved\n", "- Answer: unresolved <selectedcontent> x\n")
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
    findings = cr.check("# VoI Record: x\n\n## VoI\n\n- Verdict: worth-it\n\n```\nopen\n")
    fence = next(f for f in findings if "unterminated code fence" in f)
    assert "re-validate" not in fence, fence
    assert "close the fence" not in fence, fence


def test_uri_autolinks_without_a_double_slash_are_not_placeholders():
    """`<tel:...>` and `<urn:...>` are CommonMark autolinks, i.e. record
    content, so they must not mark the record in progress."""
    for link in ("<tel:+15551212>", "<urn:isbn:0451450523>", "<news:comp.lang.python>"):
        ledger = GOOD_LEDGER.replace(
            "## Data Validity\n\n- Collection method: exporter\n\n", ""
        ).replace("- Answer: unresolved\n", f"- Answer: unresolved, see {link}\n")
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
        ledger = GOOD_LEDGER.replace(
            "## Data Validity\n\n- Collection method: exporter\n\n", ""
        ).replace("- Answer: unresolved\n", f"- Answer: unresolved {tag}\n")
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
