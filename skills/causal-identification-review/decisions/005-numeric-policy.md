# 005 — Numeric policy

Status: accepted, 2026-08-08.

## Question

This skill must never produce a causal point estimate or run estimator mechanics — that non-goal is not in dispute.
But does that ban extend to every number the skill might produce, including the bound route's own output, or is there a form of numeric output the ban does not cover?

## Positions

*No numeric output anywhere, including the bound route (as drafted before the critique).*
An early draft of the bound route — the route absorbing the former Candidate 6, partial identification under stated assumptions — produced no computed values, only the plan for how bounds would be computed.
This kept the numeric ban simple and total.

*Numeric bound endpoints allowed when computed under a precommitted assumption ledger (adopted).*
The 2026-08-08 Codex cross-model critique found the numberless bound route self-defeating: it "produces a plan for bounds, not bounds," which meant the former Candidate 6 was not actually being absorbed by the draft, only gestured at.
The settled position narrows the ban rather than dropping it: no causal point estimates, no power numbers, but bound-route endpoints computed under a ledger of assumptions committed before the computation, and probe results (a placebo contrast, a negative-control value) reported as evidence about those assumptions, are in scope.
An identified design's actual effect estimation is explicitly not this skill's job — it routes onward to HDA's estimation route with the review record attached.

## What settled it

The Codex critique's direct argument that a route which never outputs a number cannot be said to deliver bounds at all, which the plan resolved by permitting endpoint computation gated on a precommitted assumption ledger rather than by dropping the numeric ban generally.

## Reopening condition

If measured runs (the bound-route scenario in the skill's own catalog) show computed endpoints drifting from the fixture's documented ground-truth bounds, or show the endpoint-computation allowance being used to smuggle an unjustified causal point estimate past the ban, the numeric policy is worth revisiting.

## Where the rule lives

`skills/causal-identification-review/SKILL.md` § Non-Goals and the bound route's per-route procedure, and the checker that enforces it (to be written; this record predates them).
