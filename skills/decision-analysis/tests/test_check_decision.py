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

from pathlib import Path

from check_decision import EXIT_UNVERIFIABLE, PROVENANCE, check, main, parse_range, parse_sections

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
- Value calculation: net expected improvement 0.4 incident-equivalents after subtracting one day's delay, positive across the swept class
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


def test_voi_sensitivity_only_signal_model_requires_break_even_only():
    bad = replace_once(
        VALID_VOI, "provenance: estimated-from-data-in-hand", "provenance: sensitivity-only"
    )
    assert any("break-even-only" in msg for msg in check(bad))


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
    return text


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
    bad = replace_once(bad, "- Verdict: robust", "- Verdict: prior-sensitive")
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
