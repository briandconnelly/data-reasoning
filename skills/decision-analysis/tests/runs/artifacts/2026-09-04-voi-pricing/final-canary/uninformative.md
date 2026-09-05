# VoI Record: uninformative

## VoI

- Route: voi
- Pending decision: Choose A or B; their current expected losses tie at $50.
- Signal model: Plus and minus each have probability 0.5 under H and under not H, according to the supplied applicable calibration (provenance: `user-elicited`).
Predictive probabilities are P(plus)=P(minus)=0.5, and P(H|plus)=P(H|minus)=0.5, derived from those inputs and the supplied prior.
- Value basis: signal-model
- Value calculation:

The source for inputs is the named request in `/private/tmp/voi-pricing-final/prompts.json`.
The decision owner's loss matrix is L(A,H)=$0, L(A,not H)=$100, L(B,H)=$100, and L(B,not H)=$0 (provenance: `user-elicited`).
H is the supplied binary descriptive state; not H includes every circumstance in which H does not hold, including unnamed explanations.

The prior P(H)=0.5 has provenance `user-elicited`.
Current expected losses are R(A)=0.5×$0+0.5×$100=$50 and R(B)=0.5×$100+0.5×$0=$50, so R0=$50.
Prior odds are 1 and either return's likelihood ratio is 0.5/0.5=1, so posterior odds remain 1.
After either return, A and B still tie at $50.
R1=0.5×$50+0.5×$50=$50, so G=$50−$50=$0.
The fee f is unknown; delay and opportunity costs are both $0 (provenance: `user-elicited`).
Total cost is C=f, net value is −f, and both total-cost and remaining-fee break-even thresholds are $0.
No positive fee is justified by this information value; at a zero fee the report is value-neutral.
The robustness class consists of the supplied fixed prior, calibration, and losses.

- Cost: none stated
- Verdict: break-even-only

Interpretation and execution limits: [/private/tmp/voi-pricing-final/SKILL.md](/private/tmp/voi-pricing-final/SKILL.md), § The VoI Route and § Numeric Policy.
No report was purchased.
