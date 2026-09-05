# VoI Record: missing-model

## VoI

- Route: voi
- Pending decision: Choose A or B; they currently tie at the supplied prior and losses.
- Signal model: unavailable
- Value basis: upper-bound
- Value calculation: The source is the correspondingly named request in `/private/tmp/voi-pricing-final/prompts.json`.
All supplied prior, loss, calibration, and cost inputs have provenance `user-elicited`; calibration is reported by the user as applicable, and no calibration observations were independently inspected.
Computed risks, predictive probabilities, posterior probabilities, and values below are derived from those inputs.
The binary descriptive states are H and not-H, with not-H including all situations in which H does not hold.
The supplied loss matrix in dollars is L(A,H)=0, L(A,not-H)=100, L(B,H)=100, L(B,not-H)=0.
The supplied prior is P(H)=0.5.
R0=min(0.5($0)+0.5($100),0.5($100)+0.5($0))=$50.
With the state known, choose A under H and B under not-H, yielding expected loss 0.5($0)+0.5($0)=$0.
Expected value of perfect information is therefore $50-$0=$50, an upper bound on gross report value.
The report's calibration and signal model are missing, so predictive probabilities, post-report probabilities, R1, and actual gross value G cannot be calculated.
Known cost is $10 fee plus $0 delay and $0 other costs, totaling $10.
Allowing the report to be ignored, its gross information value lies between $0 and $50, and its net value after the stated fee lies between -$10 and $40.
The $50 bound is not this report's break-even fee; the $10 price being below that bound does not establish a worthwhile purchase.
Actual break-even fee remains unknown, and the supplied information supports no purchase recommendation.

- Cost: $10
- Verdict: upper-bound-only

Authority: `/private/tmp/voi-pricing-final/SKILL.md`, § The VoI Route and § Numeric Policy.
