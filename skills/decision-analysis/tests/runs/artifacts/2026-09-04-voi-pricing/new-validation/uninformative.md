# VoI Record: uninformative

## VoI

- Route: voi
- Pending decision: Choose A or B; the supplied prior and losses make them tied before the report.
- Signal model: Returns are plus and minus, with P(plus|H)=P(plus|not-H)=P(minus|H)=P(minus|not-H)=0.5; provenance: `user-elicited`.
The reference class is the applicable report calibration population stated by the user, conditioned on H or not-H.
At the supplied prior P(H)=0.5, both returns have predictive probability 0.5.
Prior odds 1:1 multiplied by either LR=0.5/0.5=1 remain 1:1, so P(H|plus)=P(H|minus)=0.5.
Likelihood ratios derive from the `user-elicited` calibration inputs, and only one prospective signal is modeled.

- Value basis: signal-model
- Value calculation: The source is the correspondingly named request in `/private/tmp/voi-pricing-final/prompts.json`.
All supplied prior, loss, calibration, and cost inputs have provenance `user-elicited`; calibration is reported by the user as applicable, and no calibration observations were independently inspected.
Computed risks, predictive probabilities, posterior probabilities, and values below are derived from those inputs.
The binary descriptive states are H and not-H, with not-H including all situations in which H does not hold.
The supplied loss matrix in dollars is L(A,H)=0, L(A,not-H)=100, L(B,H)=100, L(B,not-H)=0.
R0=min(0.5($0)+0.5($100),0.5($100)+0.5($0))=$50.
Either return leaves both actions at $50 expected loss, so R1=0.5($50)+0.5($50)=$50.
Gross information value G=R0-R1=$0.
Known delay and opportunity costs are both $0, while fee F is unspecified.
Total cost C=F, net value is -F, and the total-cost break-even threshold is $0.
The remaining-fee threshold is also $0, derived from `user-elicited` inputs.
A free report only ties acting now; no positive fee is justified by its information value.
The robustness class is the supplied singleton prior, loss matrix, and signal model; the unknown fee remains symbolic.

- Cost: none stated
- Verdict: break-even-only

Authority: `/private/tmp/voi-pricing-final/SKILL.md`, § The VoI Route and § Numeric Policy.
