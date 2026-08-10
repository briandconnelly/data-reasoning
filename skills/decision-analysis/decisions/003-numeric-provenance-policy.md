# 003 — Numeric provenance policy

Status: accepted, 2026-08-09.

## Question

How does a skill built on numbers coexist with `hypothesis-driven-analysis`'s rule "Do not invent numeric confidence values"?

## Decision

Four rules were decided here — provenance classing, the hypothetical-number quarantine, robustness-first priors, and the missing-loss gate; their operative statements live only in `../SKILL.md` § Numeric Policy, which is their single home.
What this record preserves is why the asymmetry between priors and losses exists: the 2026-08-09 Codex design review showed that an agent can pick a wide-looking likelihood-ratio range that still favors its preferred action, and that robustness across priors alone would launder invented stakeholder preferences into an action-ready verdict.
Provenance classing exists to make "defended" observable; the loss gate exists so that a recommendation cannot rest on stakes nobody stated.
`tests/check_decision.py` encodes the placement and coupling rules; calibration and honesty of ranges remain prose-governed.

## Reopening condition

Measured arms show the provenance ceremony failing to prevent manufactured-number verdicts, or blocking legitimate ones.
