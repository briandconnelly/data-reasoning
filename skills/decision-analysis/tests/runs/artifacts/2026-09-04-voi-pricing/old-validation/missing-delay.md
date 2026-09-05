# VoI Record: missing-delay

## VoI

- Route: voi
- Pending decision: Choose A or B; their current expected losses are tied at $50.
- Signal model: Use the supplied calibrated plus/minus model detailed below; provenance: user-elicited.
- Value calculation: Conditional on delay cost d, the break-even fee is $25−d; no single exact fee can be established while d is unknown.
- Cost: Fee unspecified; opportunity cost $5, provenance: user-elicited; delay cost unknown.
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
Write the unknown delay cost as d, without assigning it a numeric estimate.
Net value at fee f is $30−$5−d−f=$25−d−f.
A nonnegative fee is weakly justified by this calculation only if f+d≤$25; strict benefit requires f+d<$25.
If d=$25, only a zero fee is break-even; if d exceeds $25, even a free report has negative net value.
Those delay values are sensitivity-only crossovers.
For nonnegative delay cost, $25 is an upper bound on the fee ceiling, not an established ceiling for the actual delay.
A positive fee cannot be certified across unbounded nonnegative delay costs.

No purchase is made.
