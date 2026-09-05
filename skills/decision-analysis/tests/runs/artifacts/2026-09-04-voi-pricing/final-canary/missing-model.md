# VoI Record: missing-model

## VoI

- Route: voi
- Pending decision: Choose A or B; their current expected losses tie at $50.
- Signal model: unavailable
- Value basis: upper-bound
- Value calculation:

The source for inputs is the named request in `/private/tmp/voi-pricing-final/prompts.json`.
The decision owner's loss matrix is L(A,H)=$0, L(A,not H)=$100, L(B,H)=$100, and L(B,not H)=$0 (provenance: `user-elicited`).
H is the supplied binary descriptive state; not H includes every circumstance in which H does not hold, including unnamed explanations.

The prior P(H)=0.5 has provenance `user-elicited`.
Current expected losses are R(A)=0.5×$0+0.5×$100=$50 and R(B)=0.5×$100+0.5×$0=$50, so R0=$50.
No calibration or defensible signal model is available, so predictive and conditional signal probabilities and actual report value cannot be calculated.
With perfect information, choose A under H and B under not H, incurring expected loss 0.5×$0+0.5×$0=$0.
The expected value of perfect information is $50−$0=$50, an upper bound on this report's gross information value.
The report's actual gross value is between $0 and $50 because information can be ignored, but its position in that interval is unknown.
At the stated full cost of $10, net value is bounded between −$10 and $40.
The $50 bound is not this report's break-even price, and $10 being below the bound does not establish that purchase is worthwhile.
A signal model is needed to decide whether the report's actual gross value exceeds $10.

- Cost: $10 fee + $0 delay + $0 other costs = $10 (provenance: `user-elicited`)
- Verdict: upper-bound-only

Interpretation and execution limits: [/private/tmp/voi-pricing-final/SKILL.md](/private/tmp/voi-pricing-final/SKILL.md), § The VoI Route and § Numeric Policy.
No report was purchased.
