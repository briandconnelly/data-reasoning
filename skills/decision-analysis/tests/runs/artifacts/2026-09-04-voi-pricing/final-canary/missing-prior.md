# VoI Record: missing-prior

## VoI

- Route: voi
- Pending decision: Choose A or B; no current probability-based preference is justified.
- Signal model: unavailable
- Value basis: upper-bound
- Value calculation:

The source for inputs is the named request in `/private/tmp/voi-pricing-final/prompts.json`.
The decision owner's loss matrix is L(A,H)=$0, L(A,not H)=$100, L(B,H)=$100, and L(B,not H)=$0 (provenance: `user-elicited`).
H is the supplied binary descriptive state; not H includes every circumstance in which H does not hold, including unnamed explanations.

No prior probability, signal model, or fee is available.
Therefore R0, R1, an expected value of perfect information at an actual prior, and this report's actual gross value cannot be numerically calculated.
The finite loss matrix supplies the loose uniform bound max(loss)−min(loss)=$100−$0=$100 over possible priors and signals.
This is a loss-range bound, not an expected value estimate or a report-specific break-even fee.
Delay and other costs are $0 (provenance: `user-elicited`), but the fee and therefore total cost remain unknown.
No positive purchase price is established as worthwhile by this upper bound.
No probability or signal model has been invented.

- Cost: none stated
- Verdict: upper-bound-only

Interpretation and execution limits: [/private/tmp/voi-pricing-final/SKILL.md](/private/tmp/voi-pricing-final/SKILL.md), § The VoI Route and § Numeric Policy.
No report was purchased.
