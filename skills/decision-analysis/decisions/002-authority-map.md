# 002 — Authority map with the sibling skills

Status: accepted, 2026-08-09.

## Question

Four skills now touch the same investigations; who owns which verdict, so no two skills can hold incompatible ones?

## Decision

- `hypothesis-driven-analysis` keeps factual status, the causal-wording bar, and final routing authority over its own asks.
- `causal-identification-review` keeps identification dispositions; how a decision record may consume them is `../SKILL.md` § The Decide Route's to state.
- This skill owns decision-state construction, the provenance-classed update, and the verdict.
- Execution authority belongs to none of them (`../SKILL.md` § Numeric Policy).

A consume-only integration with no HDA edits was considered and rejected on the precedent of `skills/causal-identification-review/decisions/002-authority-map-with-hda.md`: that record documents the same untouched-HDA strategy being checked against HDA's shipped text and found false, because the continuation was unreachable from HDA's side.
v1 therefore includes two measured HDA amendment sentences (stop-with-limits naming this skill; a numeric-policy non-conflict sentence), recorded as their own measurement debt in `skills/hypothesis-driven-analysis/tests/scenarios.md` § Owed measurements.

## Reopening condition

HDA's conclusion or numeric-confidence rules change in a way the amendment sentences no longer track, or measurement shows the seam unreachable.
