# 005 — Value of information is net expected improvement, not flip probability

Status: accepted, 2026-08-09.

## Question

The design draft priced a pull by the probability it flips the pending decision, and routed voi on the presence of a stated cost.

## Decision

Both rejected (2026-08-09 Codex design review); the operative definitions live in `../SKILL.md` § The VoI Route and § Routing.
What this record preserves is the two counterexamples that settled it: a rarely-flipping signal can be extremely valuable when it averts a catastrophic loss, and a frequently-flipping one worthless when consequences are nearly tied; and a cost-selected route would have contradicted every sibling skill's costly-collection rule.
What each counterexample requires operatively is stated only at the pointers above.

## Reopening condition

None foreseen; this is a definition correction, not a trade-off.
