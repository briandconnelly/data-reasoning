# VoI Record: equality

## VoI

- Route: voi
- Pending decision: Choose A or B; they currently tie at the supplied prior and losses.
- Signal model: Returns are plus and minus.
The supplied likelihoods are P(plus|H)=0.8, P(plus|not-H)=0.2, P(minus|H)=0.2, and P(minus|not-H)=0.8; provenance: `user-elicited`.
The reference class is the report's applicable calibration population specified in the request, conditioned on H or not-H; no additional population details are supplied.
At the supplied prior P(H)=0.5, P(plus)=0.5(0.8)+0.5(0.2)=0.5 and P(minus)=0.5.
Prior odds are 1:1; a plus has LR=0.8/0.2=4, yielding posterior odds 4:1 and P(H|plus)=0.8; a minus has LR=0.2/0.8=0.25, yielding posterior odds 1:4 and P(H|minus)=0.2.
The likelihood ratios derive from `user-elicited` calibration inputs; there is one prospective signal, and no multiplication of separate evidence items.

- Value basis: signal-model
- Value calculation: The source is the correspondingly named request in `/private/tmp/voi-pricing-final/prompts.json`.
All supplied prior, loss, calibration, and cost inputs have provenance `user-elicited`; calibration is reported by the user as applicable, and no calibration observations were independently inspected.
Computed risks, predictive probabilities, posterior probabilities, and values below are derived from those inputs.
The binary descriptive states are H and not-H, with not-H including all situations in which H does not hold.
The supplied loss matrix in dollars is L(A,H)=0, L(A,not-H)=100, L(B,H)=100, L(B,not-H)=0.
At P(H)=0.5, each action's current expected loss is $50, so R0=$50.
After plus, A has expected loss $20 and B $80, so choose A.
After minus, A has expected loss $80 and B $20, so choose B.
R1=0.5($20)+0.5($20)=$20, and gross information value G=R0-R1=$30.
The robustness class is the supplied singleton prior P(H)=0.5 and singleton loss matrix and signal model; no unsupported uncertainty range is introduced.
Full cost is $30 fee plus $0 delay and $0 other costs, totaling $30.
Net information value is $30-$30=$0 throughout the stated singleton robustness class.
The fee equals the $30 break-even threshold derived from `user-elicited` inputs.
The report and acting now have equal total expected loss of $50, so buying yields no strictly positive expected benefit.
At equality the applicable verdict is not-worth-it; this records a tie rather than a strict disadvantage.

- Cost: $30
- Verdict: not-worth-it

Authority: `/private/tmp/voi-pricing-final/SKILL.md`, § The VoI Route and § Numeric Policy.
