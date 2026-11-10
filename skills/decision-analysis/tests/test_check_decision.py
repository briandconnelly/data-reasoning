"""Unit suite for check_decision.py's structural gates.

Every negative test mutates VALID_DECIDE or VALID_VOI through replace_once,
which asserts the target occurs exactly once -- a mutation that silently
misses its target would otherwise turn a negative test into a no-op. Each
gate is demonstrated against a known positive that passes clean: a checker
that rejects everything and a checker that accepts everything both fail here.

The fixture records below use the en dash the template itself uses for
numeric ranges (e.g. ``0.25`` to ``1.0``); replace_once matches these fixtures
character-for-character against what check_decision.py parses, so the en
dashes and the resulting long lines are measured text, not style choices --
reflowing or ASCII-fying them would silently stop testing what the template
actually contains.
"""
# ruff: noqa: E501, RUF001

import importlib.util
from fractions import Fraction
from pathlib import Path

from base_check_decision_cac2464 import check as base_check
from check_decision import (
    DECIDE_VERDICTS,
    EXIT_UNVERIFIABLE,
    PROVENANCE,
    check,
    main,
    orient,
    parse_quantity,
    parse_range,
    parse_sections,
    preferred_action,
)

FIXTURES = Path(__file__).parent

VALID_DECIDE = """# Decision Record: hold the release or ship

## Decision frame

- Route: decide
- Actions: ship now vs hold one week
- Decision owner: release manager
- Reversibility: shipping is hard to undo; holding costs a week
- Deadline or forcing event: freeze on Friday
- Consequences:

  | | regression is real true | regression is real false |
  | --- | --- | --- |
  | ship now | incident | on-time release |
  | hold one week | delay, no incident | needless delay |

- Favored if true: hold one week
- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: the p95 regression is a real regression
- Residual reading: false includes measurement noise and any cause nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.25–1.0 — provenance: externally-sourced
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | repro on staging | 3–5 | estimated-from-data-in-hand | staging run 2026-08-08, same build |

- Independence: single item
- Posterior odds: 0.75–5.0

## Robustness

- Prior class swept: 0.25–1.0 — provenance: sensitivity-only
- Loss range swept: 5–20 — provenance: user-elicited
- Crossover: none within swept class

## Verdict

- Verdict: robust
- Recommended action: hold one week
- Conditions: prior odds within 0.25–1.0; loss ratio within 5–20

## Handoff

- Open factual disputes: none
- Identification gaps: none
- VoI question: none
"""

VALID_VOI = """# VoI Record: rerun the load test before deciding

## VoI

- Route: voi
- Pending decision: ship now vs hold one week, leaning hold
- Signal model: a clean rerun halves the odds; a dirty rerun triples them — provenance: estimated-from-data-in-hand
- Value basis: signal-model
- Value calculation: net expected improvement 0.4 incident-equivalents after subtracting one day's delay, positive across the swept class
- Upper bound: not applicable
- Cost: 1 day
- Verdict: worth-it
"""


def replace_once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f"target occurs {text.count(old)} times: {old!r}"
    return text.replace(old, new)


def test_known_positive_decide_passes():
    assert check(VALID_DECIDE) == []


def test_known_positive_voi_passes():
    assert check(VALID_VOI) == []


def _upper_bound_voi() -> str:
    text = replace_once(VALID_VOI, "- Value basis: signal-model", "- Value basis: upper-bound")
    text = replace_once(text, "- Verdict: worth-it", "- Verdict: upper-bound-only")
    text = replace_once(
        text,
        "- Signal model: a clean rerun halves the odds; a dirty rerun triples them "
        "— provenance: estimated-from-data-in-hand",
        "- Signal model: unavailable",
    )
    return replace_once(
        text, "- Upper bound: not applicable", "- Upper bound: 50 incident-equivalents"
    )


def test_unknown_signal_model_with_stated_cost_accepts_bound_or_nonpositive_verdict():
    assert check(_upper_bound_voi()) == []
    for verdict in ("worth-it", "sensitive", "break-even-only"):
        bad = replace_once(
            _upper_bound_voi(), "- Verdict: upper-bound-only", f"- Verdict: {verdict}"
        )
        assert any("upper-bound" in msg for msg in check(bad)), verdict


def test_upper_bound_schema_permits_bound_determined_not_worth_it():
    text = replace_once(
        _upper_bound_voi(),
        "- Value calculation: net expected improvement 0.4 incident-equivalents after "
        "subtracting one day's delay, positive across the swept class",
        "- Value calculation: finite perfect-information bound: 50; full cost: 200; "
        "therefore net value is nonpositive",
    )
    text = replace_once(text, "- Cost: 1 day", "- Cost: 200 incident-equivalents")
    text = replace_once(text, "- Verdict: upper-bound-only", "- Verdict: not-worth-it")
    assert check(text) == []


def test_unknown_signal_model_without_full_cost_cannot_be_not_worth_it():
    text = replace_once(_upper_bound_voi(), "- Cost: 1 day", "- Cost: none stated")
    text = replace_once(text, "- Verdict: upper-bound-only", "- Verdict: not-worth-it")
    assert any("stated full Cost" in msg for msg in check(text))


def test_upper_bound_not_worth_it_requires_cost_at_least_bound():
    text = replace_once(_upper_bound_voi(), "- Cost: 1 day", "- Cost: 10 incident-equivalents")
    text = replace_once(text, "- Verdict: upper-bound-only", "- Verdict: not-worth-it")
    assert any("Cost at least Upper bound" in msg for msg in check(text))


def test_upper_bound_not_worth_it_requires_matching_units():
    text = replace_once(_upper_bound_voi(), "- Cost: 1 day", "- Cost: 200 days")
    text = replace_once(text, "- Verdict: upper-bound-only", "- Verdict: not-worth-it")
    assert any("Upper bound's unit" in msg for msg in check(text))


def test_upper_bound_not_worth_it_requires_finite_bound():
    text = replace_once(
        _upper_bound_voi(), "- Upper bound: 50 incident-equivalents", "- Upper bound: unavailable"
    )
    text = replace_once(text, "- Cost: 1 day", "- Cost: 200 incident-equivalents")
    text = replace_once(text, "- Verdict: upper-bound-only", "- Verdict: not-worth-it")
    assert any("finite Upper bound" in msg for msg in check(text))


def test_unknown_signal_model_and_cost_still_accepts_bound_verdict():
    text = replace_once(_upper_bound_voi(), "- Cost: 1 day", "- Cost: none stated")
    assert check(text) == []


def test_hypothetical_signal_model_accepts_bound_basis():
    text = replace_once(
        _upper_bound_voi(),
        "- Signal model: unavailable",
        "- Signal model: perfect classification — provenance: sensitivity-only",
    )
    assert check(text) == []


def test_unknown_model_cannot_claim_signal_specific_break_even():
    text = replace_once(
        _upper_bound_voi(), "- Value basis: upper-bound", "- Value basis: signal-model"
    )
    text = replace_once(text, "- Verdict: upper-bound-only", "- Verdict: break-even-only")
    text = replace_once(text, "- Cost: 1 day", "- Cost: none stated")
    assert any("requires upper-bound" in msg for msg in check(text))


def test_signal_model_cannot_claim_upper_bound_verdict():
    text = replace_once(VALID_VOI, "- Verdict: worth-it", "- Verdict: upper-bound-only")
    assert any("cannot carry" in msg for msg in check(text))


def test_signal_model_requires_not_applicable_upper_bound():
    text = replace_once(VALID_VOI, "- Upper bound: not applicable", "- Upper bound: unavailable")
    assert any("not applicable" in msg for msg in check(text))


def test_stated_full_cost_requires_net_value_verdict():
    text = replace_once(VALID_VOI, "- Verdict: worth-it", "- Verdict: break-even-only")
    assert any("net-value verdict" in msg for msg in check(text))


def test_value_basis_is_required_and_closed():
    for replacement in ("", "- Value basis: price-bound\n"):
        text = replace_once(VALID_VOI, "- Value basis: signal-model\n", replacement)
        assert any("Value basis" in msg for msg in check(text))


def test_unavailable_model_sentinel_must_be_bare():
    text = replace_once(
        _upper_bound_voi(),
        "- Signal model: unavailable",
        "- Signal model: unavailable — provenance: sensitivity-only",
    )
    assert any("bare" in msg for msg in check(text))


def test_voi_prose_slots_accept_continuation_paragraphs():
    text = replace_once(
        VALID_VOI,
        "- Signal model: a clean rerun halves the odds; a dirty rerun triples them "
        "— provenance: estimated-from-data-in-hand",
        "- Signal model:\nA clean rerun halves the odds — provenance: externally-sourced.\n"
        "The owner-supplied prior has provenance: `user-elicited`.",
    )
    text = replace_once(
        text, "- Value calculation: net expected", "- Value calculation:\n\nnet expected"
    )
    assert check(text) == []


def test_voi_signal_model_requires_at_least_one_provenance_class():
    text = replace_once(VALID_VOI, "— provenance: estimated-from-data-in-hand", "")
    assert any("one or more provenance" in msg for msg in check(text))


def test_unknown_code_formatted_provenance_still_fails():
    text = replace_once(
        VALID_VOI,
        "provenance: estimated-from-data-in-hand",
        "provenance: `guessed`",
    )
    assert any("closed set" in msg for msg in check(text))


def test_voi_empty_calculation_cannot_borrow_next_slot():
    text = replace_once(
        VALID_VOI,
        "- Value calculation: net expected improvement 0.4 incident-equivalents after "
        "subtracting one day's delay, positive across the swept class",
        "- Value calculation:\n",
    )
    assert any("Value calculation" in msg and "empty" in msg for msg in check(text))


def test_voi_signal_provenance_cannot_be_borrowed_from_calculation():
    text = replace_once(VALID_VOI, "— provenance: estimated-from-data-in-hand", "")
    text = replace_once(
        text,
        "- Value calculation:",
        "- Value calculation: provenance: estimated-from-data-in-hand;",
    )
    assert any("Signal model" in msg and "provenance" in msg for msg in check(text))


def test_voi_prose_stops_at_unrecognized_bullet_or_heading():
    for boundary in ("- Note:", "### Note"):
        text = replace_once(
            VALID_VOI,
            "— provenance: estimated-from-data-in-hand",
            f"\n{boundary}\nprovenance: estimated-from-data-in-hand",
        )
        assert any("Signal model" in msg and "provenance" in msg for msg in check(text))


def test_parse_sections_finds_all_decide_sections():
    sections, _ = parse_sections(VALID_DECIDE)
    for name in (
        "Decision frame",
        "Decision-state model",
        "Evidence and update",
        "Robustness",
        "Verdict",
        "Handoff",
    ):
        assert name in sections


def test_duplicate_section_fails():
    bad = VALID_DECIDE + "\n## Verdict\n\n- Verdict: robust\n- Conditions: duplicate\n"
    assert any("duplicate" in msg.lower() for msg in check(bad))


def test_unknown_route_fails():
    bad = replace_once(VALID_DECIDE, "- Route: decide", "- Route: estimate")
    assert any("Route" in msg for msg in check(bad))


def test_decide_missing_section_fails():
    bad = replace_once(VALID_DECIDE, "## Robustness", "## Extra")
    assert any("Robustness" in msg for msg in check(bad))


def test_missing_slot_fails():
    bad = replace_once(
        VALID_DECIDE,
        "- Proposition: the p95 regression is a real regression\n",
        "",
    )
    assert any("Proposition" in msg for msg in check(bad))


def test_empty_slot_fails():
    bad = replace_once(
        VALID_DECIDE,
        "- Residual reading: false includes measurement noise and any cause nobody named",
        "- Residual reading:",
    )
    assert any("Residual reading" in msg for msg in check(bad))


def test_unknown_verdict_fails():
    bad = replace_once(VALID_DECIDE, "- Verdict: robust", "- Verdict: optimal")
    assert any("Verdict" in msg for msg in check(bad))


def test_voi_verdict_vocabulary_is_disjoint_per_route():
    bad = replace_once(VALID_VOI, "- Verdict: worth-it", "- Verdict: robust")
    assert any("Verdict" in msg for msg in check(bad))


def test_unknown_provenance_fails():
    bad = replace_once(VALID_DECIDE, "provenance: externally-sourced", "provenance: my-best-guess")
    assert any("provenance" in msg for msg in check(bad))


def test_sensitivity_only_in_evidence_block_fails():
    bad = replace_once(
        VALID_DECIDE,
        "- Prior odds: 0.25–1.0 — provenance: externally-sourced",
        "- Prior odds: 0.25–1.0 — provenance: sensitivity-only",
    )
    assert any("sensitivity-only" in msg for msg in check(bad))


def test_causal_claim_without_identification_basis_fails():
    bad = replace_once(VALID_DECIDE, "- Claim class: descriptive", "- Claim class: causal")
    assert any("Identification basis" in msg for msg in check(bad))


def test_causal_claim_with_identification_basis_passes():
    good = replace_once(VALID_DECIDE, "- Claim class: descriptive", "- Claim class: causal")
    good = replace_once(
        good,
        "- Identification basis: NONE",
        "- Identification basis: CIR record cir-2026-08-01, identified-if, assumptions restated above",
    )
    good = replace_once(
        good,
        "- Identification conditions: none",
        "- Identification conditions: staging traffic is representative of production traffic",
    )
    assert not any("Identification basis" in msg for msg in check(good))
    assert not any("Identification conditions" in msg for msg in check(good))


def test_causal_claim_with_basis_but_conditions_none_fails():
    bad = replace_once(VALID_DECIDE, "- Claim class: descriptive", "- Claim class: causal")
    bad = replace_once(
        bad,
        "- Identification basis: NONE",
        "- Identification basis: CIR record cir-2026-08-01, identified-if, assumptions restated above",
    )
    assert any("Identification conditions" in msg for msg in check(bad))


def test_unknown_claim_class_fails():
    bad = replace_once(VALID_DECIDE, "- Claim class: descriptive", "- Claim class: Causal")
    assert any("Claim class" in msg for msg in check(bad))
    bad2 = replace_once(VALID_DECIDE, "- Claim class: descriptive", "- Claim class: statistical")
    assert any("Claim class" in msg for msg in check(bad2))


def test_three_actions_fails_binary_scope():
    bad = replace_once(
        VALID_DECIDE,
        "- Actions: ship now vs hold one week",
        "- Actions: ship now vs hold one week vs roll back",
    )
    assert any("two actions" in msg for msg in check(bad))


def test_three_consequence_rows_fails_binary_scope():
    bad = replace_once(
        VALID_DECIDE,
        "  | hold one week | delay, no incident | needless delay |",
        "  | hold one week | delay, no incident | needless delay |\n  | roll back | churn | churn |",
    )
    assert any("two action rows" in msg for msg in check(bad))


def test_three_state_columns_fails_binary_scope():
    bad = replace_once(
        VALID_DECIDE,
        "| | regression is real true | regression is real false |",
        "| | real | noise | config drift |",
    )
    assert any("two state columns" in msg for msg in check(bad))


def test_loss_ratio_without_provenance_fails_robust():
    bad = replace_once(
        VALID_DECIDE,
        "- Loss ratio: 10 — provenance: user-elicited",
        "- Loss ratio: 10",
    )
    assert any("Loss ratio" in msg for msg in check(bad))


def test_loss_range_without_provenance_fails_robust():
    bad = replace_once(
        VALID_DECIDE,
        "- Loss range swept: 5–20 — provenance: user-elicited",
        "- Loss range swept: 5–20",
    )
    assert any("Loss range swept" in msg for msg in check(bad))


def test_loss_ratio_nonnumeric_fails():
    bad = replace_once(
        VALID_DECIDE,
        "- Loss ratio: 10 — provenance: user-elicited",
        "- Loss ratio: bananas — provenance: user-elicited",
    )
    assert any("Loss ratio" in msg for msg in check(bad))


def test_loss_range_swept_reversed_fails():
    bad = replace_once(
        VALID_DECIDE,
        "- Loss range swept: 5–20 — provenance: user-elicited",
        "- Loss range swept: 20–5 — provenance: user-elicited",
    )
    assert any("Loss range swept" in msg for msg in check(bad))


def test_robust_verdict_with_sensitivity_only_losses_fails():
    bad = replace_once(
        VALID_DECIDE,
        "- Loss ratio: 10 — provenance: user-elicited",
        "- Loss ratio: 10 — provenance: sensitivity-only",
    )
    bad = replace_once(
        bad,
        "- Loss range swept: 5–20 — provenance: user-elicited",
        "- Loss range swept: 5–20 — provenance: sensitivity-only",
    )
    assert any("loss" in msg.lower() for msg in check(bad))


def test_voi_sensitivity_only_signal_model_requires_upper_bound():
    bad = replace_once(
        VALID_VOI, "provenance: estimated-from-data-in-hand", "provenance: sensitivity-only"
    )
    assert any("upper-bound" in msg for msg in check(bad))


def test_voi_missing_slot_fails():
    bad = replace_once(VALID_VOI, "- Cost: 1 day\n", "")
    assert any("Cost" in msg for msg in check(bad))


def test_unreadable_record_is_unverifiable_not_clean(tmp_path):
    missing = tmp_path / "absent.md"
    assert main([str(missing)]) == EXIT_UNVERIFIABLE


def test_provenance_vocabulary_is_the_settled_set():
    assert (
        frozenset(
            {
                "user-elicited",
                "externally-sourced",
                "estimated-from-data-in-hand",
                "sensitivity-only",
            }
        )
        == PROVENANCE
    )


def test_parse_range_single_dashes_and_order():
    assert parse_range("3") == (3.0, 3.0)
    assert parse_range("0.25–1.0") == (0.25, 1.0)
    assert parse_range("0.25-1.0") == (0.25, 1.0)
    assert parse_range("1.0–0.25") is None
    assert parse_range("unknown") is None


def test_parse_quantity_requires_a_nonnegative_decimal_and_unit():
    assert parse_quantity("50 incident-equivalents") == (50.0, "incident-equivalents")
    assert parse_quantity("50") is None
    assert parse_quantity("$50") is None


def test_unparseable_prior_odds_fails_closed():
    bad = replace_once(VALID_DECIDE, "- Prior odds: 0.25–1.0", "- Prior odds: unknown")
    assert any("Prior odds" in msg for msg in check(bad))


def test_zero_likelihood_ratio_fails_domain():
    bad = replace_once(
        VALID_DECIDE,
        "| repro on staging | 3–5 |",
        "| repro on staging | 0 |",
    )
    assert any("LR" in msg for msg in check(bad))


def test_missing_evidence_data_row_fails_closed():
    bad = replace_once(
        VALID_DECIDE,
        "  | repro on staging | 3–5 | estimated-from-data-in-hand | staging run 2026-08-08, same build |\n",
        "",
    )
    assert any("Evidence" in msg for msg in check(bad))


def test_posterior_odds_recomputation_catches_bad_arithmetic():
    bad = replace_once(VALID_DECIDE, "- Posterior odds: 0.75–5.0", "- Posterior odds: 2.0–9.0")
    assert any("Posterior odds" in msg for msg in check(bad))


def test_posterior_odds_tolerates_one_percent_rounding():
    rounded = replace_once(
        VALID_DECIDE, "- Posterior odds: 0.75–5.0", "- Posterior odds: 0.75–5.04"
    )
    assert not any("Posterior odds" in msg for msg in check(rounded))


def test_robust_crossover_inside_swept_class_fails():
    # threshold 0.1, LR 3-5 -> crossover prior odds [0.02, 0.0333];
    # widening the swept class to include it makes 'robust' inconsistent.
    bad = replace_once(
        VALID_DECIDE,
        "- Prior class swept: 0.25–1.0 — provenance: sensitivity-only",
        "- Prior class swept: 0.01–1.0 — provenance: sensitivity-only",
    )
    assert any("crossover" in msg.lower() for msg in check(bad))


def test_prior_sensitive_requires_crossover_number_in_computed_interval():
    bad = replace_once(VALID_DECIDE, "- Verdict: robust", "- Verdict: prior-sensitive")
    bad = replace_once(
        bad,
        "- Prior class swept: 0.25–1.0 — provenance: sensitivity-only",
        "- Prior class swept: 0.01–1.0 — provenance: sensitivity-only",
    )
    bad = replace_once(
        bad,
        "- Crossover: none within swept class",
        "- Crossover: flips at prior odds 0.5",
    )
    assert any("crossover" in msg.lower() for msg in check(bad))


def test_prior_sensitive_with_correct_crossover_passes():
    good = replace_once(VALID_DECIDE, "- Verdict: robust", "- Verdict: prior-sensitive")
    good = replace_once(
        good,
        "- Prior class swept: 0.25–1.0 — provenance: sensitivity-only",
        "- Prior class swept: 0.01–1.0 — provenance: sensitivity-only",
    )
    good = replace_once(
        good,
        "- Crossover: none within swept class",
        "- Crossover: flips at prior odds 0.02–0.033",
    )
    good = replace_once(
        good, "- Recommended action: hold one week", "- Recommended action: returned to owner"
    )
    assert check(good) == []


def _dominated_decide() -> str:
    """VALID_DECIDE with a dominated verdict and its belief slots sentineled."""
    text = replace_once(VALID_DECIDE, "- Verdict: robust", "- Verdict: dominated")
    text = replace_once(
        text,
        "- Prior odds: 0.25–1.0 — provenance: externally-sourced",
        "- Prior odds: none needed",
    )
    text = replace_once(text, "- Posterior odds: 0.75–5.0", "- Posterior odds: none needed")
    text = replace_once(
        text,
        "- Prior class swept: 0.25–1.0 — provenance: sensitivity-only",
        "- Prior class swept: none needed",
    )
    text = replace_once(text, "- Crossover: none within swept class", "- Crossover: none needed")
    return replace_once(text, "- Favored if true: hold one week", "- Favored if true: none needed")


def test_dominated_verdict_with_none_needed_slots_passes():
    assert check(_dominated_decide()) == []


def test_dominated_verdict_with_real_numbers_fails():
    # A dominated verdict's belief slots must read exactly 'none needed';
    # a real number in any of them is a gate failure, not a tolerated extra.
    bad = replace_once(
        _dominated_decide(), "- Crossover: none needed", "- Crossover: flips at prior odds 0.5"
    )
    assert any("Crossover" in msg for msg in check(bad))
    bad2 = replace_once(_dominated_decide(), "- Prior odds: none needed", "- Prior odds: bananas")
    assert any("Prior odds" in msg for msg in check(bad2))


def test_threshold_range_uses_both_endpoints_to_fail_robust():
    # threshold 0.1-2, LR 3-5 -> crossover [0.1/5, 2/3] = [0.02, 0.667],
    # which intersects the swept class 0.25-1.0: 'robust' is inconsistent.
    bad = replace_once(
        VALID_DECIDE,
        "- Decision threshold (posterior odds): 0.1 — provenance: user-elicited",
        "- Decision threshold (posterior odds): 0.1–2 — provenance: user-elicited",
    )
    assert any("crossover" in msg.lower() for msg in check(bad))


def test_prior_odds_without_provenance_fails():
    bad = replace_once(
        VALID_DECIDE,
        "- Prior odds: 0.25–1.0 — provenance: externally-sourced",
        "- Prior odds: 0.25–1.0",
    )
    assert any("Prior odds" in msg for msg in check(bad))


def test_prior_class_swept_without_provenance_fails():
    bad = replace_once(
        VALID_DECIDE,
        "- Prior class swept: 0.25–1.0 — provenance: sensitivity-only",
        "- Prior class swept: 0.25–1.0",
    )
    assert any("Prior class swept" in msg for msg in check(bad))


def test_prior_odds_with_two_provenance_mentions_fails():
    bad = replace_once(
        VALID_DECIDE,
        "- Prior odds: 0.25–1.0 — provenance: externally-sourced",
        "- Prior odds: 0.25–1.0 — provenance: externally-sourced, provenance: user-elicited",
    )
    assert any("Prior odds" in msg for msg in check(bad))


def test_evidence_row_sourced_with_empty_source_cell_fails():
    bad = replace_once(
        VALID_DECIDE,
        "  | repro on staging | 3–5 | estimated-from-data-in-hand | staging run 2026-08-08, same build |",
        "  | repro on staging | 3–5 | estimated-from-data-in-hand | |",
    )
    assert any("repro on staging" in msg for msg in check(bad))


def test_voi_no_cost_with_worth_it_fails():
    bad = replace_once(VALID_VOI, "- Cost: 1 day", "- Cost: none stated")
    assert any("break-even-only" in msg for msg in check(bad))


def test_voi_no_cost_with_break_even_only_passes():
    good = replace_once(VALID_VOI, "- Cost: 1 day", "- Cost: none stated")
    good = replace_once(good, "- Verdict: worth-it", "- Verdict: break-even-only")
    assert check(good) == []


def test_voi_signal_model_without_provenance_fails():
    bad = replace_once(
        VALID_VOI,
        "- Signal model: a clean rerun halves the odds; a dirty rerun triples them "
        "— provenance: estimated-from-data-in-hand",
        "- Signal model: a clean rerun halves the odds; a dirty rerun triples them",
    )
    assert any("Signal model" in msg for msg in check(bad))


def test_no_threshold_falls_back_to_structural_crossover_check():
    good = replace_once(
        VALID_DECIDE,
        "- Decision threshold (posterior odds): 0.1 — provenance: user-elicited",
        "- Decision threshold (posterior odds): none stated",
    )
    assert check(good) == []
    bad = replace_once(
        good, "- Crossover: none within swept class", "- Crossover: flips at prior odds 0.5"
    )
    assert any("crossover" in msg.lower() for msg in check(bad))


def test_duplicate_slot_label_in_section_fails():
    bad = replace_once(
        VALID_DECIDE,
        "- Verdict: robust\n",
        "- Verdict: robust\n- Verdict: optimal\n",
    )
    assert any("exactly once" in msg for msg in check(bad))


def test_zero_decision_threshold_fails_domain():
    bad = replace_once(
        VALID_DECIDE,
        "- Decision threshold (posterior odds): 0.1 — provenance: user-elicited",
        "- Decision threshold (posterior odds): 0 — provenance: user-elicited",
    )
    assert any("strictly positive" in msg for msg in check(bad))


def test_structural_crossover_rejects_none_prose_with_incidental_digits():
    # No numeric threshold -> the structural branch runs; a Crossover that
    # starts with 'none' must not pass on a digit that is not a flip point.
    bad = replace_once(
        VALID_DECIDE,
        "- Decision threshold (posterior odds): 0.1 — provenance: user-elicited",
        "- Decision threshold (posterior odds): none stated",
    )
    # With no threshold the stated loss supplies one (SKILL.md § Numeric
    # Policy), so the loss slot is blanked too to reach the structural branch.
    bad = replace_once(
        bad, "- Loss ratio: 10 — provenance: user-elicited", "- Loss ratio: none stated"
    )
    bad = replace_once(bad, "- Verdict: robust", "- Verdict: loss-sensitive")
    bad = replace_once(
        bad, "- Recommended action: hold one week", "- Recommended action: returned to owner"
    )
    bad = replace_once(
        bad, "- Crossover: none within swept class", "- Crossover: none known in 2026"
    )
    assert any("positive flip" in msg for msg in check(bad))


def test_consequence_row_with_wrong_cell_count_fails():
    bad = replace_once(
        VALID_DECIDE,
        "  | ship now | incident | on-time release |",
        "  | ship now | incident |",
    )
    assert any("state columns" in msg for msg in check(bad))


def test_evidence_row_with_extra_cells_fails():
    bad = replace_once(
        VALID_DECIDE,
        "  | repro on staging | 3–5 | estimated-from-data-in-hand | staging run 2026-08-08, same build |",
        "  | repro on staging | 3–5 | estimated-from-data-in-hand | staging run 2026-08-08, same build | extra |",
    )
    assert any("exactly 4" in msg for msg in check(bad))


def test_voi_unclassifiable_cost_fails_closed():
    for value in ("unknown", "TBD", "none"):
        bad = replace_once(VALID_VOI, "- Cost: 1 day", f"- Cost: {value}")
        assert any("Cost" in msg for msg in check(bad)), value


def test_annotated_sentinel_on_threshold_fails():
    bad = replace_once(
        VALID_DECIDE,
        "- Decision threshold (posterior odds): 0.1 — provenance: user-elicited",
        "- Decision threshold (posterior odds): none stated — provenance: user-elicited",
    )
    assert any("bare" in msg for msg in check(bad))


def test_annotated_sentinel_on_dominated_slot_fails():
    bad = replace_once(
        _dominated_decide(),
        "- Prior odds: none needed",
        "- Prior odds: none needed — provenance: user-elicited",
    )
    assert any("Prior odds" in msg for msg in check(bad))


def test_robust_recommended_action_must_name_a_framed_action():
    bad = replace_once(
        VALID_DECIDE,
        "- Recommended action: hold one week",
        "- Recommended action: proceed",
    )
    assert any("Recommended action" in msg for msg in check(bad))


def test_sensitive_recommended_action_must_return_to_owner():
    bad = replace_once(VALID_DECIDE, "- Verdict: robust", "- Verdict: loss-sensitive")
    bad = replace_once(
        bad,
        "- Crossover: none within swept class",
        "- Crossover: flips at loss ratio 12",
    )
    assert any("returned to owner" in msg for msg in check(bad))


# Remediation wave 2026-09-15, row 2: three archived records carried `\|`
# inside an evidence source cell and parsed as six-cell rows.


def test_escaped_pipe_inside_an_evidence_cell_is_content():
    text = replace_once(
        VALID_DECIDE,
        "  | repro on staging | 3–5 | estimated-from-data-in-hand | staging run 2026-08-08, same build |",
        "  | repro on staging | 3–5 | estimated-from-data-in-hand | P(gap \\| real)=9/10, "
        "P(gap \\| not)=2/10 |",
    )
    assert check(text) == []


def test_unescaped_extra_pipe_is_still_an_extra_cell():
    text = replace_once(
        VALID_DECIDE,
        "  | repro on staging | 3–5 | estimated-from-data-in-hand | staging run 2026-08-08, same build |",
        "  | repro on staging | 3–5 | estimated-from-data-in-hand | P(gap | real) | extra |",
    )
    assert any("cells; the template requires exactly 4" in f for f in check(text))


# Wave-2 canary 2026-09-15: a robust record named the flip point outside the
# swept class, which § Robustness asks for; the checker demanded the sentinel.


def test_robust_may_name_the_flip_point_outside_the_swept_class():
    # VALID_DECIDE: threshold 0.1, LR 3-5 -> flip interval [0.02, 0.0333]; swept 0.25-1.0
    ok = replace_once(
        VALID_DECIDE,
        "- Crossover: none within swept class",
        "- Crossover: flips at prior odds 0.025",
    )
    assert check(ok) == []


def test_robust_with_a_flip_point_not_matching_the_arithmetic_fails():
    bad = replace_once(
        VALID_DECIDE, "- Crossover: none within swept class", "- Crossover: flips at prior odds 0.5"
    )
    assert any("robust verdict requires Crossover" in f for f in check(bad))


def test_robust_may_name_the_prior_flip_point_outside_the_class():
    # Threshold 0.1 and swept losses 5-20 (thresholds 0.05-0.2) with LR 3-5 put the
    # prior-odds flip at [0.01, 0.0667], outside the swept class 0.25-1.0; a robust
    # record may name a point in that interval.
    ok = replace_once(
        VALID_DECIDE,
        "- Crossover: none within swept class",
        "- Crossover: flips at prior odds 0.06",
    )
    assert check(ok) == []


def test_robust_with_a_sweep_that_reaches_the_flip_fails():
    # Prior class 0.05-1.0 reaches the flip interval [0.01, 0.0667]: somewhere in
    # the class x range the action reverses, which the ordered rule reads as a
    # prior flip.
    bad = replace_once(
        VALID_DECIDE,
        "- Prior class swept: 0.25–1.0 — provenance: sensitivity-only",
        "- Prior class swept: 0.05–1.0 — provenance: sensitivity-only",
    )
    assert any("lies inside the swept prior class" in f for f in check(bad))


def test_robust_with_a_prior_flip_at_the_stated_losses_fails():
    # Threshold 0.1 with LR 3-5 puts the prior-odds flip at [0.02, 0.0333];
    # a swept class reaching down to 0.01 contains it.
    bad = replace_once(
        VALID_DECIDE,
        "- Prior class swept: 0.25–1.0 — provenance: sensitivity-only",
        "- Prior class swept: 0.01–0.25 — provenance: sensitivity-only",
    )
    assert any("lies inside the swept prior class" in f for f in check(bad))


def test_every_number_in_a_stated_crossover_must_be_in_the_interval():
    bad = replace_once(
        VALID_DECIDE,
        "- Crossover: none within swept class",
        "- Crossover: flips at prior odds 0.06–999",
    )
    assert any("robust verdict requires Crossover" in f for f in check(bad))


# Re-review 2026-09-15: digit fragments were accepted wherever they appeared.


def test_crossover_grammar_rejects_signs_reversed_ranges_and_prose():
    for value in ("-0.025", "0.06–0.02", "none known at 0.025", "roughly 0.025 or so"):
        bad = replace_once(
            VALID_DECIDE, "- Crossover: none within swept class", f"- Crossover: {value}"
        )
        assert any("robust verdict requires Crossover" in f for f in check(bad)), value


def test_crossover_grammar_accepts_the_stated_forms():
    for value in ("0.025", "prior odds 0.025", "flips at prior odds 0.02–0.03"):
        ok = replace_once(
            VALID_DECIDE, "- Crossover: none within swept class", f"- Crossover: {value}"
        )
        assert check(ok) == [], value


# --- Issue #41: the no-supported-prior form, the loss cap, and the ordered
# verdict rule (SKILL.md § Numeric Policy, 2026-11-08) -------------------

NO_PRIOR = replace_once(
    replace_once(
        VALID_DECIDE,
        "- Prior odds: 0.25–1.0 — provenance: externally-sourced",
        "- Prior odds: none supported — see Robustness",
    ),
    "- Posterior odds: 0.75–5.0",
    "- Posterior odds: none supported — see Robustness",
)


def test_no_supported_prior_form_with_supported_lr_passes():
    # swept class 0.25-1.0, LR 3-5, threshold 0.1: no prior flip ([0.02, 0.033]);
    # loss flip over the class: [0.2, 1.33] vs 5-20: none -- robust stands.
    assert check(NO_PRIOR) == []


def test_no_prior_sentinel_must_fill_both_slots():
    half = replace_once(
        NO_PRIOR, "- Posterior odds: none supported — see Robustness", "- Posterior odds: 0.75–5.0"
    )
    assert any("must read the same sentinel" in f for f in check(half))


def test_no_prior_sentinel_must_be_bare():
    bad = replace_once(
        NO_PRIOR,
        "- Prior odds: none supported — see Robustness",
        "- Prior odds: none supported — see Robustness (no base rate exists)",
    )
    assert any("must appear bare" in f for f in check(bad))


def test_unquantified_evidence_row_is_a_paired_sentinel_with_a_reason():
    ok = replace_once(
        NO_PRIOR,
        "| repro on staging | 3–5 | estimated-from-data-in-hand | staging run 2026-08-08, same build |",
        "| repro on staging | 3–5 | estimated-from-data-in-hand | staging run 2026-08-08, same build |\n"
        "  | T2 raw logs | none supported | none supported | T2 never ran; logs not restored |",
    )
    assert check(ok) == []
    half = ok.replace("| none supported | none supported |", "| 1 | none supported |")
    assert any("together" in f for f in check(half))
    no_reason = ok.replace(
        "| none supported | none supported | T2 never ran; logs not restored |",
        "| none supported | none supported | |",
    )
    assert any("reason in the source cell" in f for f in check(no_reason))


def test_no_supported_lr_cannot_reach_robust():
    bad = replace_once(
        NO_PRIOR,
        "| repro on staging | 3–5 | estimated-from-data-in-hand | staging run 2026-08-08, same build |",
        "| repro on staging | none supported | none supported | no reproducible source for a ratio |",
    )
    assert any("hypothetical inputs alone cannot reach robust" in f for f in check(bad))
    ok = replace_once(bad, "- Verdict: robust", "- Verdict: prior-sensitive")
    ok = replace_once(
        ok, "- Recommended action: hold one week", "- Recommended action: returned to owner"
    )
    ok = replace_once(
        ok, "- Crossover: none within swept class", "- Crossover: flips at prior odds 0.1"
    )
    assert not any("robust" in f for f in check(ok)), check(ok)


def test_sensitivity_only_losses_cap_prior_sensitive():
    bad = replace_once(
        VALID_DECIDE,
        "- Loss ratio: 10 — provenance: user-elicited",
        "- Loss ratio: 10 — provenance: sensitivity-only",
    )
    bad = replace_once(bad, "- Verdict: robust", "- Verdict: prior-sensitive")
    bad = replace_once(
        bad, "- Recommended action: hold one week", "- Recommended action: returned to owner"
    )
    bad = replace_once(
        bad, "- Crossover: none within swept class", "- Crossover: flips at prior odds 0.03"
    )
    assert any("caps the verdict at loss-sensitive" in f for f in check(bad))


def test_estimated_losses_are_not_belief_grade():
    bad = replace_once(
        VALID_DECIDE,
        "- Loss ratio: 10 — provenance: user-elicited",
        "- Loss ratio: 10 — provenance: estimated-from-data-in-hand",
    )
    assert any("caps the verdict at loss-sensitive" in f for f in check(bad))


def _loss_only_flip(verdict: str, crossover: str, action: str) -> str:
    # Prior 0.25-1.0, LR 3-5: loss flip at [0.2, 1.33]; swept losses 1-20 meet it;
    # the prior flip [0.02, 0.033] does not meet the class 0.25-1.0.
    rec = replace_once(
        VALID_DECIDE,
        "- Loss range swept: 5–20 — provenance: user-elicited",
        "- Loss range swept: 1–20 — provenance: user-elicited",
    )
    rec = replace_once(rec, "- Verdict: robust", f"- Verdict: {verdict}")
    rec = replace_once(
        rec, "- Recommended action: hold one week", f"- Recommended action: {action}"
    )
    return replace_once(rec, "- Crossover: none within swept class", f"- Crossover: {crossover}")


def test_a_flip_reachable_through_the_prior_class_is_prior_sensitive():
    # Losses 1-20 with prior class 0.25-1.0: the prior flip read over the loss
    # range is [0.01, 0.667], which meets the class, so the ordered rule gives
    # prior-sensitive; loss-sensitive and robust are rejected.
    assert any(
        "the ordered rule gives prior-sensitive" in f
        for f in check(
            _loss_only_flip("loss-sensitive", "flips at loss ratio 1", "returned to owner")
        )
    )
    assert any(
        "lies inside the swept prior class" in f
        for f in check(_loss_only_flip("robust", "none within swept class", "hold one week"))
    )
    ok = _loss_only_flip("prior-sensitive", "flips at prior odds 0.03", "returned to owner")
    assert check(ok) == [], check(ok)


def test_loss_only_flip_with_a_point_prior_class_is_loss_sensitive():
    # A single-point prior class cannot flip; the losses 1-20 flip at the stated
    # prior 0.25-1.0 (loss flip [0.2, 1.33]).
    rec = replace_once(
        _loss_only_flip("loss-sensitive", "flips at loss ratio 1", "returned to owner"),
        "- Prior class swept: 0.25–1.0 — provenance: sensitivity-only",
        "- Prior class swept: 0.5–0.5 — provenance: sensitivity-only",
    )
    assert check(rec) == [], check(rec)
    bad = replace_once(
        rec, "- Crossover: flips at loss ratio 1", "- Crossover: flips at loss ratio 999"
    )
    assert any("does not fall in the computed loss-ratio interval" in f for f in check(bad))


def test_tie_at_a_sweep_boundary_counts_as_a_flip():
    """Codex review of #77: prior 0.5, LR 1, loss 40, threshold 0.025, class
    0.05-0.5, losses 20-40 put the product exactly at 1 on one corner."""
    rec = replace_once(VALID_DECIDE, "| repro on staging | 3–5 |", "| repro on staging | 1 |")
    rec = replace_once(
        rec,
        "- Loss ratio: 10 — provenance: user-elicited",
        "- Loss ratio: 40 — provenance: user-elicited",
    )
    rec = replace_once(
        rec,
        "- Decision threshold (posterior odds): 0.1 — provenance: user-elicited",
        "- Decision threshold (posterior odds): 0.025 — provenance: user-elicited",
    )
    rec = _sweep(
        rec,
        "- Prior odds: 0.5 — provenance: externally-sourced",
        "- Posterior odds: 0.5",
        "- Prior class swept: 0.05–0.5 — provenance: sensitivity-only",
        "- Loss range swept: 20–40 — provenance: user-elicited",
    )
    assert any("lies inside the swept prior class" in f for f in check(rec)), check(rec)


def test_unstated_threshold_is_supplied_by_the_stated_loss():
    """Codex review of #77: 'none stated' must not switch the sweep checks off."""
    rec = replace_once(NO_PRIOR, "| repro on staging | 3–5 |", "| repro on staging | 4.5 |")
    rec = replace_once(
        rec,
        "- Decision threshold (posterior odds): 0.1 — provenance: user-elicited",
        "- Decision threshold (posterior odds): none stated",
    )
    rec = replace_once(
        rec,
        "- Prior class swept: 0.25–1.0 — provenance: sensitivity-only",
        "- Prior class swept: 0.01–1 — provenance: sensitivity-only",
    )
    rec = replace_once(
        rec,
        "- Loss range swept: 5–20 — provenance: user-elicited",
        "- Loss range swept: 10–10 — provenance: user-elicited",
    )
    assert any("lies inside the swept prior class" in f for f in check(rec)), check(rec)


def test_axis_is_checked_on_robust_and_capped_records():
    bad = replace_once(
        VALID_DECIDE,
        "- Crossover: none within swept class",
        "- Crossover: flips at loss ratio 0.03",
    )
    assert any("names prior odds" in f for f in check(bad))
    capped = replace_once(
        VALID_DECIDE,
        "- Loss ratio: 10 — provenance: user-elicited",
        "- Loss ratio: 10 — provenance: sensitivity-only",
    )
    capped = replace_once(capped, "- Verdict: robust", "- Verdict: loss-sensitive")
    capped = replace_once(
        capped, "- Recommended action: hold one week", "- Recommended action: returned to owner"
    )
    capped = replace_once(
        capped, "- Crossover: none within swept class", "- Crossover: flips at prior odds 999"
    )
    assert any("names a loss ratio" in f for f in check(capped))


def test_double_flip_is_prior_sensitive_not_loss_sensitive():
    # class 0.01-1.0 meets the prior flip [0.02, 0.033]; losses 1-20 meet the loss flip.
    # The ordered rule gives prior-sensitive (both DA-S8 arms chose it; measured
    # 2026-11-08 as a clarification with no lift).
    rec = replace_once(
        _loss_only_flip("prior-sensitive", "flips at prior odds 0.03", "returned to owner"),
        "- Prior class swept: 0.25–1.0 — provenance: sensitivity-only",
        "- Prior class swept: 0.01–1.0 — provenance: sensitivity-only",
    )
    assert check(rec) == []
    bad = replace_once(rec, "- Verdict: prior-sensitive", "- Verdict: loss-sensitive")
    bad = replace_once(
        bad, "- Crossover: flips at prior odds 0.03", "- Crossover: flips at loss ratio 1"
    )
    assert any("the ordered rule gives prior-sensitive" in f for f in check(bad))


def _sweep(rec: str, prior: str, posterior: str, cls: str, losses: str) -> str:
    rec = replace_once(rec, "- Prior odds: 0.25–1.0 — provenance: externally-sourced", prior)
    rec = replace_once(rec, "- Posterior odds: 0.75–5.0", posterior)
    rec = replace_once(rec, "- Prior class swept: 0.25–1.0 — provenance: sensitivity-only", cls)
    return replace_once(rec, "- Loss range swept: 5–20 — provenance: user-elicited", losses)


def test_robust_rejects_a_reversal_between_sweep_corners():
    """Codex review of #77: supported prior 1, LR 4.5, swept priors 0.05-1 and
    losses 2-20: prior * LR * loss runs from 0.45 to 90 across the corners.
    Read over the swept loss range, the prior flip [0.0111, 0.111] meets the class."""
    rec = replace_once(VALID_DECIDE, "| repro on staging | 3–5 |", "| repro on staging | 4.5 |")
    rec = _sweep(
        rec,
        "- Prior odds: 1 — provenance: externally-sourced",
        "- Posterior odds: 4.5",
        "- Prior class swept: 0.05–1 — provenance: sensitivity-only",
        "- Loss range swept: 2–20 — provenance: user-elicited",
    )
    findings = check(rec)
    assert any("lies inside the swept prior class" in f for f in findings), findings
    ok = replace_once(rec, "- Verdict: robust", "- Verdict: prior-sensitive")
    ok = replace_once(
        ok, "- Recommended action: hold one week", "- Recommended action: returned to owner"
    )
    ok = replace_once(
        ok, "- Crossover: none within swept class", "- Crossover: flips at prior odds 0.011–0.111"
    )
    assert check(ok) == [], check(ok)


def test_a_point_loss_range_cannot_flip():
    # Archived DA-S1 post shape (Codex review of #77): a swept loss range of
    # 10-10 must not read as a loss flip, so the record cannot be loss-sensitive.
    rec = _sweep(
        VALID_DECIDE,
        "- Prior odds: 0.01–1.0 — provenance: externally-sourced",
        "- Posterior odds: 0.03–5.0",
        "- Prior class swept: 0.01–1.0 — provenance: sensitivity-only",
        "- Loss range swept: 10–10 — provenance: user-elicited",
    )
    rec = replace_once(rec, "- Verdict: robust", "- Verdict: loss-sensitive")
    rec = replace_once(
        rec, "- Recommended action: hold one week", "- Recommended action: returned to owner"
    )
    rec = replace_once(
        rec, "- Crossover: none within swept class", "- Crossover: flips at loss ratio 10"
    )
    assert any("the ordered rule gives prior-sensitive" in f for f in check(rec)), check(rec)


def test_crossover_axis_must_match_the_verdict():
    rec = replace_once(
        _loss_only_flip("loss-sensitive", "flips at prior odds 1", "returned to owner"),
        "- Prior class swept: 0.25–1.0 — provenance: sensitivity-only",
        "- Prior class swept: 0.5–0.5 — provenance: sensitivity-only",
    )
    assert any("names a loss ratio" in f for f in check(rec))


def test_rounding_tolerance_is_per_endpoint():
    """Codex review of #77: a coarse endpoint's tolerance must not cover a finely
    stated endpoint on either side of the computed flip 0.0222."""
    rec = replace_once(VALID_DECIDE, "| repro on staging | 3–5 |", "| repro on staging | 4.5 |")
    rec = _sweep(
        rec,
        "- Prior odds: 0.25–1.0 — provenance: externally-sourced",
        "- Posterior odds: 1.125–4.5",
        "- Prior class swept: 0.01–1.0 — provenance: sensitivity-only",
        "- Loss range swept: 10–10 — provenance: user-elicited",
    )
    rec = replace_once(rec, "- Verdict: robust", "- Verdict: prior-sensitive")
    rec = replace_once(
        rec, "- Recommended action: hold one week", "- Recommended action: returned to owner"
    )
    for stated in ("0.02–0.027000", "0.02–0.021000"):
        bad = replace_once(
            rec,
            "- Crossover: none within swept class",
            f"- Crossover: flips at prior odds {stated}",
        )
        assert any("does not fall in the computed prior-odds interval" in f for f in check(bad)), (
            stated
        )
    ok = replace_once(
        rec, "- Crossover: none within swept class", "- Crossover: flips at prior odds 0.02"
    )
    assert check(ok) == [], check(ok)  # a two-decimal rounding of 0.0222


def test_rounded_crossover_at_the_tolerance_edge_is_accepted():
    """2026-11-08 canaries: 0.022 stated for a computed 0.02222 sat exactly on
    the 1% edge and was rejected; a stated figure is a rounded one."""
    rec = replace_once(
        VALID_DECIDE,
        "- Prior class swept: 0.25–1.0 — provenance: sensitivity-only",
        "- Prior class swept: 0.01–1.0 — provenance: sensitivity-only",
    )
    rec = replace_once(
        rec,
        "- Loss range swept: 5–20 — provenance: user-elicited",
        "- Loss range swept: 10–10 — provenance: user-elicited",
    )
    rec = replace_once(rec, "| repro on staging | 3–5 |", "| repro on staging | 4.5 |")
    rec = replace_once(rec, "- Posterior odds: 0.75–5.0", "- Posterior odds: 1.125–4.5")
    rec = replace_once(rec, "- Verdict: robust", "- Verdict: prior-sensitive")
    rec = replace_once(
        rec, "- Recommended action: hold one week", "- Recommended action: returned to owner"
    )
    ok = replace_once(
        rec, "- Crossover: none within swept class", "- Crossover: flips at prior odds 0.022"
    )
    assert check(ok) == [], check(ok)
    bad = replace_once(
        rec, "- Crossover: none within swept class", "- Crossover: flips at prior odds 0.03"
    )
    assert any("does not fall in the computed prior-odds interval" in f for f in check(bad))


# --- The evidence sweep and loss orientation (decisions/007, 2026-11-09) ---
#
# D1: a likelihood ratio stated as a range was carried through the posterior
# and never swept, so `robust` survived a supported LR range that alone
# reversed the action. D2: the threshold rule named an undefined "hold" and
# never said which losses form the ratio. The arithmetic lives here, in the
# dev checker only; the shipped validator gained the verdict and the slot
# structurally and nothing else. Records are built from parameters so each
# case states only the numbers it is about.

_CR_SPEC = importlib.util.spec_from_file_location(
    "check_record", Path(__file__).resolve().parents[3] / "instruments" / "check_record.py"
)
cr = importlib.util.module_from_spec(_CR_SPEC)
_CR_SPEC.loader.exec_module(cr)

SHIP, HOLD = "ship now", "hold one week"
OWNER = "returned to owner"


def _fmt_range(r: tuple[Fraction, Fraction]) -> str:
    lo, hi = (f"{float(x):.6g}" for x in r)
    return lo if lo == hi else f"{lo}–{hi}"


def _rng(text: str) -> tuple[Fraction, Fraction]:
    parts = [Fraction(p) for p in text.split("–")]
    return (parts[0], parts[-1])


def build(  # noqa: PLR0913 -- one keyword per slot the ordered rule reads
    *,
    prior: str | None = "1",
    cls: str | None = None,
    lrs: tuple[str, ...] = ("1",),
    loss: str = "1",
    losses: str | None = None,
    loss_prov: str = "user-elicited",
    threshold: str = "none stated",
    verdict: str = "robust",
    rec: str = HOLD,
    crossover: str = "none within swept class",
    favored: str = HOLD,
    actions: tuple[str, str] = (SHIP, HOLD),
) -> str:
    """A complete decide record; prior=None writes the no-supported-prior form.
    The prior class defaults to the prior and the loss range to the loss.
    Posterior odds are computed exactly from the prior and the LR rows."""
    cls = cls or prior or "1"
    losses = losses or loss
    lr = (Fraction(1), Fraction(1))
    for r in lrs:
        lo, hi = _rng(r)
        lr = (lr[0] * lo, lr[1] * hi)
    if prior is None:
        prior_line = posterior_line = "none supported — see Robustness"
    else:
        p = _rng(prior)
        prior_line = f"{prior} — provenance: externally-sourced"
        posterior_line = _fmt_range((p[0] * lr[0], p[1] * lr[1]))
    rows = "\n".join(
        f"  | item {i} | {r} | externally-sourced | vendor note {i}, alert class X, this host |"
        for i, r in enumerate(lrs, 1)
    )
    threshold_line = (
        threshold if threshold == "none stated" else f"{threshold} — provenance: user-elicited"
    )
    independence = "single item" if len(lrs) == 1 else "independent given each state"
    a, b = actions
    return f"""# Decision Record: ship or hold

## Decision frame

- Route: decide
- Actions: {a} vs {b}
- Decision owner: release manager
- Reversibility: shipping is hard to undo; holding costs a week
- Deadline or forcing event: freeze on Friday
- Consequences:

  | | regression is real true | regression is real false |
  | --- | --- | --- |
  | {a} | outcome | outcome |
  | {b} | outcome | outcome |

- Favored if true: {favored}
- Loss ratio: {loss} — provenance: {loss_prov}
- Decision threshold (posterior odds): {threshold_line}

## Decision-state model

- Proposition: the regression is real
- Residual reading: false includes noise and any cause nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: {prior_line}
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
{rows}

- Independence: {independence}
- Posterior odds: {posterior_line}

## Robustness

- Prior class swept: {cls} — provenance: sensitivity-only
- Loss range swept: {losses} — provenance: {loss_prov}
- Crossover: {crossover}

## Verdict

- Verdict: {verdict}
- Recommended action: {rec}
- Conditions: as swept

## Handoff

- Open factual disputes: none
- Identification gaps: none
- VoI question: none
"""


def _clean(text: str) -> bool:
    """The dev checker passes it, and the shipped validator finds nothing
    structural in it."""
    return check(text) == [] and cr.check(text, final=True) == []


def _says(text: str, fragment: str) -> bool:
    return any(fragment in f for f in check(text))


def test_builder_known_positive_passes_both_checkers():
    assert _clean(build(prior="2", rec=HOLD))  # posterior 2 above threshold 1


def test_point_prior_lr_range_straddle_is_evidence_sensitive():
    """The D1 reproduction: prior 1, class 1-1, losses 1, LR 0.1-10."""
    assert _says(build(lrs=("0.1–10",)), "the ordered rule gives evidence-sensitive")
    ok = build(
        lrs=("0.1–10",),
        verdict="evidence-sensitive",
        rec=OWNER,
        crossover="flips at likelihood ratio 1",
    )
    assert _clean(ok), check(ok)
    assert _says(
        ok.replace("flips at likelihood ratio 1", "flips at likelihood ratio 5"),
        "computed likelihood-ratio interval",
    )
    assert _says(
        ok.replace("flips at likelihood ratio 1", "flips at prior odds 1"),
        "names a likelihood ratio",
    )


def test_the_base_threshold_contract_is_unchanged():
    """Review 2026-11-10: prior = class = 0.5, LR 1, loss = range = 1, stated
    threshold 0.1. The base checker accepts robust; widening the stated
    threshold by 1 / L must not newly demand prior-sensitive."""
    rec = build(prior="0.5", threshold="0.1", rec=HOLD)
    assert _clean(rec), check(rec)
    assert base_check(rec) == []


def test_a_stated_threshold_range_alone_is_not_a_new_flip():
    """Point inputs inside a stated threshold range: unsettled contract
    (decisions/007's open question), so robust stays as the base accepted it."""
    rec = build(prior="1", threshold="0.5–2", rec=HOLD)
    assert check(rec) == []
    assert base_check(rec) == []


def test_lr_flip_is_read_against_the_stated_threshold():
    # Stated threshold 0.1, losses 1 (1 / L = 1): the LR range 0.5-2 at prior 0.5
    # gives 0.25-1, which meets 1 / L but not the stated threshold, so no LR flip.
    assert _clean(build(prior="0.5", lrs=("0.5–2",), threshold="0.1", rec=HOLD))
    rec = build(prior="0.5", lrs=("0.1–2",), threshold="0.1")
    assert _says(rec, "the ordered rule gives evidence-sensitive")


def test_narrow_genuine_prior_straddle_is_not_a_point():
    """0.999-1.001 straddles threshold 1; the base's 1% tolerance read it as a
    point and accepted robust -- an exact comparison that now differs."""
    bad = build(prior="1", cls="0.999–1.001")
    assert base_check(bad) == []
    assert _says(bad, "lies inside the swept prior class")
    ok = build(
        prior="1",
        cls="0.999–1.001",
        verdict="prior-sensitive",
        rec=OWNER,
        crossover="flips at prior odds 1",
    )
    assert _clean(ok)


def test_narrow_genuine_loss_straddle_is_not_a_point():
    bad = build(losses="0.999–1.001")
    assert _says(bad, "lies inside the swept loss range")
    ok = build(
        losses="0.999–1.001", verdict="loss-sensitive", rec=OWNER, crossover="flips at loss ratio 1"
    )
    assert _clean(ok)


def test_close_non_straddles_stay_robust_on_the_right_side():
    assert _clean(build(prior="1.001", cls="1.001–1.002", rec=HOLD))
    assert _clean(build(prior="0.998", cls="0.998–0.999", rec=SHIP))
    assert _says(build(prior="0.998", cls="0.998–0.999", rec=HOLD), "lie below the threshold")


def test_a_range_touching_the_threshold_at_an_endpoint_flips():
    assert _says(build(prior="1", cls="1–2"), "lies inside the swept prior class")
    assert _says(build(lrs=("1–2",)), "the ordered rule gives evidence-sensitive")
    ok = build(
        lrs=("1–2",),
        verdict="evidence-sensitive",
        rec=OWNER,
        crossover="flips at likelihood ratio 1",
    )
    assert _clean(ok)


def test_exact_tie_at_points_is_prior_sensitive_never_robust():
    """Every input a point and posterior odds equal to the threshold: no
    action is preferred, so not robust; decisions/007's tie ruling (an owner
    judgement call) gives prior-sensitive."""
    assert _says(build(), "equal the threshold exactly")
    assert _clean(build(verdict="prior-sensitive", rec=OWNER, crossover="flips at prior odds 1"))
    for verdict, axis in (
        ("evidence-sensitive", "likelihood ratio"),
        ("loss-sensitive", "loss ratio"),
    ):
        bad = build(verdict=verdict, rec=OWNER, crossover=f"flips at {axis} 1")
        assert _says(bad, "the ordered rule gives prior-sensitive"), verdict


def test_prior_range_with_lr_range_straddle_keeps_prior_precedence():
    bad = build(
        prior="2",
        cls="2–3",
        lrs=("0.1–10",),
        verdict="evidence-sensitive",
        rec=OWNER,
        crossover="flips at likelihood ratio 0.4",
    )
    assert _says(bad, "the ordered rule gives prior-sensitive")
    ok = build(
        prior="2",
        cls="2–3",
        lrs=("0.1–10",),
        verdict="prior-sensitive",
        rec=OWNER,
        crossover="flips at prior odds 0.1–10",
    )
    assert _clean(ok)


def test_loss_range_with_lr_range_straddle_keeps_loss_precedence():
    # Point prior 1, LR 0.5-2, losses 0.25-4: the losses flip at the stated
    # prior, so loss-sensitive governs before evidence-sensitive.
    bad = build(
        lrs=("0.5–2",),
        losses="0.25–4",
        verdict="evidence-sensitive",
        rec=OWNER,
        crossover="flips at likelihood ratio 1",
    )
    assert _says(bad, "the ordered rule gives loss-sensitive")
    ok = build(
        lrs=("0.5–2",),
        losses="0.25–4",
        verdict="loss-sensitive",
        rec=OWNER,
        crossover="flips at loss ratio 1",
    )
    assert _clean(ok)


def test_lr_range_that_cannot_reach_the_threshold_stays_robust():
    assert _clean(build(prior="2", lrs=("1.1–3",), rec=HOLD))
    bad = build(
        prior="2",
        lrs=("1.1–3",),
        verdict="evidence-sensitive",
        rec=OWNER,
        crossover="flips at likelihood ratio 0.5",
    )
    assert _says(bad, "no supported likelihood-ratio range flips")


def test_several_lr_factors_are_swept_as_their_product():
    """Each factor 1-1.5 alone keeps prior 0.5 below threshold 1 (0.5-0.75);
    their product 1-2.25 reaches it (0.5-1.125)."""
    assert _says(
        build(prior="0.5", lrs=("1–1.5", "1–1.5"), rec=SHIP),
        "the ordered rule gives evidence-sensitive",
    )
    ok = build(
        prior="0.5",
        lrs=("1–1.5", "1–1.5"),
        verdict="evidence-sensitive",
        rec=OWNER,
        crossover="flips at likelihood ratio 2",
    )
    assert _clean(ok)


def test_no_supported_prior_form_reaches_evidence_sensitive():
    assert _says(build(prior=None, lrs=("0.1–10",)), "the ordered rule gives evidence-sensitive")
    ok = build(
        prior=None,
        lrs=("0.1–10",),
        verdict="evidence-sensitive",
        rec=OWNER,
        crossover="flips at likelihood ratio 1",
    )
    assert _clean(ok)


def test_evidence_sensitive_with_sensitivity_only_losses_is_capped():
    bad = build(
        lrs=("0.1–10",),
        loss_prov="sensitivity-only",
        verdict="evidence-sensitive",
        rec=OWNER,
        crossover="flips at likelihood ratio 1",
    )
    assert _says(bad, "caps the verdict at loss-sensitive")
    assert any("evidence-sensitive" in f and "Loss ratio" in f for f in cr.check(bad, final=True))


def test_evidence_sensitive_needs_a_supported_lr_range():
    bad = build(
        lrs=("2",),
        verdict="evidence-sensitive",
        rec=OWNER,
        crossover="flips at likelihood ratio 0.5",
    )
    assert _says(bad, "requires a supported likelihood ratio stated as a range")
    unsupported = replace_once(
        build(
            lrs=("0.1–10",),
            verdict="evidence-sensitive",
            rec=OWNER,
            crossover="flips at likelihood ratio 1",
        ),
        "| item 1 | 0.1–10 | externally-sourced | vendor note 1, alert class X, this host |",
        "| item 1 | none supported | none supported | no reproducible source |",
    )
    assert _says(unsupported, "requires a supported likelihood ratio stated as a range")


def test_evidence_sensitive_must_return_to_owner():
    bad = build(
        lrs=("0.1–10",),
        verdict="evidence-sensitive",
        rec=HOLD,
        crossover="flips at likelihood ratio 1",
    )
    assert _says(bad, "returned to owner")


def test_recommendation_contradicting_orientation_fails():
    # VALID_DECIDE: posterior 0.75-5 lies above the threshold, so the favored action wins.
    flipped = replace_once(
        VALID_DECIDE, "- Favored if true: hold one week", "- Favored if true: ship now"
    )
    assert _says(flipped, "lie above the threshold")
    wrong_rec = replace_once(
        VALID_DECIDE, "- Recommended action: hold one week", "- Recommended action: ship now"
    )
    assert _says(wrong_rec, "lie above the threshold")


def test_favored_if_true_names_a_framed_action_or_dominated_sentinel():
    bad = replace_once(VALID_DECIDE, "- Favored if true: hold one week", "- Favored if true: hold")
    assert _says(bad, "must name one of the framed actions")
    sentinel = replace_once(
        VALID_DECIDE, "- Favored if true: hold one week", "- Favored if true: none needed"
    )
    assert _says(sentinel, "Favored if true")
    assert any("Favored if true" in f and "none needed" in f for f in cr.check(sentinel))
    missing = replace_once(VALID_DECIDE, "- Favored if true: hold one week\n", "")
    assert _says(missing, "Favored if true")
    assert any("Favored if true" in f for f in cr.check(missing, final=True))
    dominated = replace_once(
        _dominated_decide(), "- Favored if true: none needed", "- Favored if true: hold one week"
    )
    assert _says(dominated, "dominated verdict requires '- Favored if true:'")


def test_duplicate_action_names_are_a_finding_not_a_crash():
    """Review 2026-11-10: `hold one week vs hold one week` raised StopIteration
    in the direction check."""
    for actions in ((HOLD, HOLD), (HOLD, "Hold  one week")):
        for verdict, rec in (("robust", HOLD), ("evidence-sensitive", OWNER)):
            text = build(prior="2", actions=actions, verdict=verdict, rec=rec)
            assert _says(text, "two distinct actions"), (actions, verdict)


def test_action_order_carries_no_meaning():
    for actions in ((SHIP, HOLD), (HOLD, SHIP)):
        assert _clean(build(prior="2", rec=HOLD, actions=actions)), actions
        assert _clean(build(prior="0.5", rec=SHIP, actions=actions)), actions
    swapped = replace_once(
        replace_once(
            VALID_DECIDE,
            "- Actions: ship now vs hold one week",
            "- Actions: hold one week vs ship now",
        ),
        "  | ship now | incident | on-time release |\n"
        "  | hold one week | delay, no incident | needless delay |\n",
        "  | hold one week | delay, no incident | needless delay |\n"
        "  | ship now | incident | on-time release |\n",
    )
    assert _clean(swapped)


def test_negating_the_proposition_keeps_the_recommendation():
    """VALID_DECIDE restated over not-H: odds and ratios invert, the favored
    action becomes ship now, and hold one week stays the recommendation."""
    neg = build(
        prior="1–4",
        lrs=("0.2–0.333333",),
        loss="0.1",
        losses="0.05–0.2",
        threshold="10",
        favored=SHIP,
        rec=HOLD,
    )
    assert _clean(neg), check(neg)
    assert _says(
        neg.replace("- Recommended action: hold one week", "- Recommended action: ship now"),
        "lie below the threshold",
    )


def test_orientation_is_the_incremental_loss_ratio():
    """D2: ship=(10, 0), hold=(1, 1) over (H, not-H): r = 9, not the raw 10."""
    losses = {SHIP: (Fraction(10), Fraction(0)), HOLD: (Fraction(1), Fraction(1))}
    assert orient(losses) == (HOLD, SHIP, Fraction(9))
    assert preferred_action(losses, Fraction("0.105")) == SHIP  # between 1/10 and 1/9
    assert preferred_action(losses, Fraction(1, 9)) is None  # an exact tie
    assert preferred_action(losses, Fraction("0.12")) == HOLD


def test_orientation_is_invariant_to_listing_order_state_order_and_shifts():
    losses = {SHIP: (Fraction(10), Fraction(0)), HOLD: (Fraction(1), Fraction(1))}
    for odds in (Fraction("0.05"), Fraction("0.105"), Fraction("0.2"), Fraction(3)):
        base = preferred_action(losses, odds)
        assert preferred_action(dict(reversed(list(losses.items()))), odds) == base
        # Swap the states: losses become (not-H, H), and the odds are of not-H.
        swapped = {a: (n, h) for a, (h, n) in losses.items()}
        assert preferred_action(swapped, 1 / odds) == base
        for k in (Fraction(-1), Fraction(5)):
            assert preferred_action({a: (h + k, n) for a, (h, n) in losses.items()}, odds) == base
            assert preferred_action({a: (h, n + k) for a, (h, n) in losses.items()}, odds) == base


def test_dominance_and_statewise_ties_never_divide():
    strict = {SHIP: (Fraction(1), Fraction(0)), HOLD: (Fraction(2), Fraction(3))}
    assert orient(strict) == ("dominated", SHIP, None)
    # A statewise tie under H leaves no positive difference: dominated, no division.
    tied = {SHIP: (Fraction(1), Fraction(0)), HOLD: (Fraction(1), Fraction(3))}
    assert orient(tied)[0] == "dominated"


def test_decide_verdict_sets_are_equal_across_checkers():
    assert frozenset(cr.DECIDE_VERDICTS) == DECIDE_VERDICTS
    assert "evidence-sensitive" in DECIDE_VERDICTS


def _near(a: Fraction, b: Fraction) -> bool:
    """Within the base checker's 1% padding, where exact comparison may differ."""
    return abs(a - b) <= Fraction(1, 100) * max(abs(a), abs(b))


def test_lr_point_records_keep_the_base_verdicts():
    """Differential against the frozen base checker: on records with no
    likelihood-ratio range, the reworked checker accepts exactly the verdicts
    the base accepted, except where an exact comparison differs (a boundary
    within the base's 1% padding, or an all-point exact tie)."""
    compared = 0
    for prior in ("0.2", "0.9", "2.5"):
        p = Fraction(prior)
        for cls in (prior, f"{p / 2:g}–{p * 2:g}"):
            sw = _rng(cls)
            for lr_text in ("0.5", "1.7", "3"):
                lr = Fraction(lr_text)
                for loss in ("3", "7"):
                    ell = Fraction(loss)
                    for losses in (loss, f"{ell / 2:g}–{ell * 2:g}"):
                        rr = _rng(losses)
                        for threshold in ("none stated", "0.3"):
                            t = (
                                (1 / ell,) * 2
                                if threshold == "none stated"
                                else (Fraction("0.3"),) * 2
                            )
                            thr = (min(t[0], 1 / rr[1]), max(t[1], 1 / rr[0]))
                            pf = (thr[0] / lr, thr[1] / lr)
                            lf = (1 / (p * lr), 1 / (p * lr))
                            if (
                                _near(pf[0], sw[1])
                                or _near(pf[1], sw[0])
                                or _near(lf[0], rr[1])
                                or _near(lf[1], rr[0])
                                or _near(p * lr, t[0])
                            ):
                                continue
                            above = p * lr > t[0]
                            for verdict in ("robust", "prior-sensitive", "loss-sensitive"):
                                if verdict == "robust":
                                    rec_action, crossover = (
                                        (HOLD if above else SHIP),
                                        ("none within swept class"),
                                    )
                                elif verdict == "prior-sensitive":
                                    mid = (pf[0] + pf[1]) / 2
                                    rec_action, crossover = (
                                        OWNER,
                                        f"flips at prior odds {float(mid):.6g}",
                                    )
                                else:
                                    rec_action, crossover = (
                                        OWNER,
                                        (f"flips at loss ratio {float(lf[0]):.6g}"),
                                    )
                                text = build(
                                    prior=prior,
                                    cls=cls,
                                    lrs=(lr_text,),
                                    loss=loss,
                                    losses=losses,
                                    threshold=threshold,
                                    verdict=verdict,
                                    rec=rec_action,
                                    crossover=crossover,
                                )
                                new_ok, base_ok = check(text) == [], base_check(text) == []
                                assert new_ok == base_ok, (prior, cls, lr_text, loss, losses,
                                                           threshold, verdict, check(text),
                                                           base_check(text))  # fmt: skip
                                compared += 1
    assert compared > 200  # noqa: PLR2004 -- the grid must not be skipped into vacuity


def test_preregistered_expected_records_pass():
    """The answers prereg.md scores DA-S9 and DA-S10 against are records this
    checker accepts, and the wrong readings are rejected."""
    restore, serve = "restore now", "keep serving"
    s9 = build(
        prior="0.25",
        lrs=("0.5–4",),
        loss="2",
        actions=(restore, serve),
        favored=restore,
        verdict="evidence-sensitive",
        rec=OWNER,
        crossover="flips at likelihood ratio 2",
    )
    assert _clean(s9), check(s9)
    raw = s9.replace("flips at likelihood ratio 2", "flips at likelihood ratio 1.33")
    assert _says(raw, "computed likelihood-ratio interval")
    s10 = build(prior="0.035", lrs=("3",), loss="9", rec=SHIP)
    assert _clean(s10), check(s10)
    assert _says(s10.replace("- Recommended action: ship now", "- Recommended action: hold one week"),
                 "lie below the threshold")  # fmt: skip


def test_robust_may_state_the_likelihood_ratio_crossover():
    """2026-11-10 DA-S10 canary: a robust record stated `flips at likelihood
    ratio 3.175` ((1/9) / 0.035), which § Robustness licenses; the checker
    accepted only a prior-odds statement."""
    ok = build(
        prior="0.035", lrs=("3",), loss="9", rec=SHIP, crossover="flips at likelihood ratio 3.175"
    )
    assert _clean(ok), check(ok)
    bad = ok.replace("flips at likelihood ratio 3.175", "flips at likelihood ratio 5")
    assert _says(bad, "likelihood-ratio Crossover must lie in the computed interval")
    loss_axis = ok.replace("flips at likelihood ratio 3.175", "flips at loss ratio 9.5")
    assert _says(loss_axis, "names prior odds or a likelihood ratio")
