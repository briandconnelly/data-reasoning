# VoI Record: missing-prior

## VoI

- Route: voi — authority: [/private/tmp/data-reasoning-voi/skills/decision-analysis/SKILL.md](/private/tmp/data-reasoning-voi/skills/decision-analysis/SKILL.md), § Routing.
- Pending decision: Choose A versus B under H versus not H.
  Current leaning is undetermined because no state probabilities are supplied.
- Signal model: unavailable — neither state probabilities nor a signal model are supplied.
- Value basis: upper-bound
- Value calculation:

State H is the descriptive proposition supplied by the owner; not H includes all alternatives, including unnamed explanations.
The owner supplies losses L(A,H)=$0, L(A,not H)=$100, L(B,H)=$100, and L(B,not H)=$0 (provenance: user-elicited).
No current expected loss, posterior, or signal-specific expected value can be calculated.
A finite-matrix loose bound over all possible priors and signals is max(loss)−min(loss)=100−0=$100, using the owner’s supplied losses (provenance: user-elicited).
This is an upper bound on gross information value, not a belief, expected value estimate, or report break-even fee.
Delay and other costs are $0 (provenance: user-elicited), while the fee is unknown.
No purchase recommendation or justified report fee follows from this loose bound.
The missing state probabilities and signal model prevent an actual value calculation; the missing fee prevents a net-cost comparison.

- Cost: none stated — full cost is unknown because the fee is missing; known components appear above.
- Verdict: upper-bound-only

Source: `/private/tmp/voi-pricing-control/prompts.json`, case `missing-prior`.
All reported numerical inputs are supplied by that request; calculated quantities are derived in the displayed arithmetic.
Verdict semantics and execution authority are governed by [the supplied skill](/private/tmp/data-reasoning-voi/skills/decision-analysis/SKILL.md), § The VoI Route and § Numeric Policy.
