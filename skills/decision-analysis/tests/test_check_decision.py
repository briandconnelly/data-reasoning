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

from check_decision import EXIT_UNVERIFIABLE, PROVENANCE, check, main, parse_sections

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
- Cost: one day
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
    assert not any("Identification basis" in msg for msg in check(good))


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
    bad = replace_once(VALID_VOI, "- Cost: one day\n", "")
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
