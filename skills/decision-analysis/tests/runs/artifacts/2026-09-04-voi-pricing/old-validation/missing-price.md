# VoI Record: missing-price

## VoI

- Route: voi
- Pending decision: Choose A or B; their current expected losses are tied at $50.
- Signal model: Use the supplied calibrated plus/minus model detailed below; provenance: user-elicited.
- Value calculation: The break-even fee is $25; a fee below $25 yields positive net value, and a fee above $25 yields negative net value.
- Cost: Fee f unspecified; delay $5 and other costs $0, provenance: user-elicited.
- Verdict: break-even-only

## Calculation and conditions

The decision owner supplies all losses: L(A,H)=$0, L(A,not-H)=$100, L(B,H)=$100, and L(B,not-H)=$0; provenance: user-elicited.
The state is descriptive H versus not-H, including unnamed alternatives.
The supplied prior P(H)=0.5 has provenance user-elicited, giving prior odds 1.
The prior and loss robustness class consists exactly of the supplied values.
Without a report, A and B each have expected loss $50 and are tied.
The report has plus and minus outcomes with P(plus|H)=0.8, P(plus|not-H)=0.2, P(minus|H)=0.2, and P(minus|not-H)=0.8; provenance: user-elicited, from the applicable calibration described in the request.
There is one prospective evidence item, so no multiplication of dependent items is involved.
For plus, LR=0.8/0.2=4 and posterior odds=1×4=4, hence P(H|plus)=0.8.
For minus, LR=0.2/0.8=0.25 and posterior odds=1×0.25=0.25, hence P(H|minus)=0.2.
These LR inputs inherit user-elicited provenance from the supplied calibration, with the report population as the reference class and H or not-H as the conditioning state.
Both report outcomes have marginal probability 0.5.
Choose A after plus and B after minus; each conditional expected loss is $20, so expected loss after the report is $20 and gross expected improvement is $50−$20=$30.
All computed quantities are derived from the stated inputs.
Net value is $30−$5−f=$25−f.
At a fee of $25 the report is exactly break-even.
The ceiling uses this specified report’s attainable improvement, and is not a claim that a different or perfect report is available.

No purchase is made.
