# VoI Record: uninformative

## VoI

- Route: voi
- Pending decision: Choose A or B; their current expected losses are tied at $50.
- Signal model: Plus and minus each have conditional probability 0.5 under both states; provenance: user-elicited calibration supplied in the request.
- Value calculation: The break-even fee is $0; no positive fee can be justified.
- Cost: Fee unspecified; delay and opportunity costs are $0, provenance: user-elicited.
- Verdict: break-even-only

## Calculation and conditions

The decision owner supplies all losses: L(A,H)=$0, L(A,not-H)=$100, L(B,H)=$100, and L(B,not-H)=$0; provenance: user-elicited.
The state is descriptive H versus not-H, including unnamed alternatives.
The supplied prior P(H)=0.5 has provenance user-elicited, giving prior odds 1.
The prior and loss robustness class consists exactly of the supplied values.
Without a report, A and B each have expected loss $50 and are tied.
Each outcome has LR=0.5/0.5=1, so posterior odds remain 1 and P(H|outcome)=0.5.
The single report cannot improve the action choice: expected loss stays $50.
Gross value is $0 and net value at fee f is −f.
A free report gives exact indifference in expected loss.

No purchase is made.
