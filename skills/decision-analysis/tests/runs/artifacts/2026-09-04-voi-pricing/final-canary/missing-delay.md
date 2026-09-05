# VoI Record: missing-delay

## VoI

- Route: voi
- Pending decision: Choose A or B; their current expected losses tie at $50.
- Signal model: Returns are plus and minus.
P(plus|H)=0.8 and P(plus|not H)=0.2 are supplied applicable calibration inputs (provenance: `user-elicited`); their complementary minus probabilities are 0.2 and 0.8.
Predictive probabilities are P(plus)=0.5×0.8+0.5×0.2=0.5 and P(minus)=0.5.
Prior odds are 0.5/0.5=1; LR(plus)=0.8/0.2=4 and LR(minus)=0.2/0.8=0.25.
Thus posterior odds are 4 after plus and 0.25 after minus, giving P(H|plus)=0.8 and P(H|minus)=0.2.
Derived probabilities and likelihood ratios use only the `user-elicited` prior and calibration inputs; there is a single signal, with no independence multiplication.

- Value basis: signal-model
- Value calculation:

The source for inputs is the named request in `/private/tmp/voi-pricing-final/prompts.json`.
The decision owner's loss matrix is L(A,H)=$0, L(A,not H)=$100, L(B,H)=$100, and L(B,not H)=$0 (provenance: `user-elicited`).
H is the supplied binary descriptive state; not H includes every circumstance in which H does not hold, including unnamed explanations.

The prior P(H)=0.5 has provenance `user-elicited`.
Current expected losses are R(A)=0.5×$0+0.5×$100=$50 and R(B)=0.5×$100+0.5×$0=$50, so R0=$50.
After plus, A has expected loss $20 and B $80, so choose A.
After minus, A has expected loss $80 and B $20, so choose B.
R1=0.5×$20+0.5×$20=$20, and gross information value G=R0−R1=$50−$20=$30.
The robustness class is the supplied point prior and calibration, with the supplied fixed loss matrix; no unsupported uncertainty range is introduced.
The fee f and delay cost d are unknown; opportunity cost is $5 (provenance: `user-elicited`).
Total cost is C=f+d+$5, and the total-cost break-even threshold is $30.
Net value is $25−d−f, so the remaining-fee break-even formula is f=$25−d, conditional on delay expressed in dollars and the supplied opportunity cost being the only other cost.
Positive net value requires f<$25−d; equality breaks even.
No numeric fee threshold can be established until d is known.
If d>$25, no nonnegative fee breaks even; if d=$25, only a zero fee breaks even.

- Cost: none stated
- Verdict: break-even-only

Interpretation and execution limits: [/private/tmp/voi-pricing-final/SKILL.md](/private/tmp/voi-pricing-final/SKILL.md), § The VoI Route and § Numeric Policy.
No report was purchased.
