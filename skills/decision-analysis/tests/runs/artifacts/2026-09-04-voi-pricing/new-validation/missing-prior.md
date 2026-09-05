# VoI Record: missing-prior

## VoI

- Route: voi
- Pending decision: Choose A or B; no current leaning is justified without a state probability.
- Signal model: unavailable
- Value basis: upper-bound
- Value calculation: The source is the correspondingly named request in `/private/tmp/voi-pricing-final/prompts.json`.
All supplied prior, loss, calibration, and cost inputs have provenance `user-elicited`; calibration is reported by the user as applicable, and no calibration observations were independently inspected.
Computed risks, predictive probabilities, posterior probabilities, and values below are derived from those inputs.
The binary descriptive states are H and not-H, with not-H including all situations in which H does not hold.
The supplied loss matrix in dollars is L(A,H)=0, L(A,not-H)=100, L(B,H)=100, L(B,not-H)=0.
No prior, signal model, or fee is supplied.
Current expected loss R0, post-report expected loss R1, and actual expected information value cannot be calculated.
The finite loss-matrix span supplies a loose upper bound over possible priors and signals: max(L)-min(L)=$100-$0=$100.
This is a loss-span bound, not an expected value calculation or the actual report's break-even fee.
Known delay and other costs are $0; fee F and hence full cost are unknown.
No numeric justified purchase fee or purchase recommendation follows from the bound, and no prior or report accuracy has been invented.

- Cost: none stated
- Verdict: upper-bound-only

Authority: `/private/tmp/voi-pricing-final/SKILL.md`, § The VoI Route and § Numeric Policy.
