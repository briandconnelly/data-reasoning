# VoI Record: missing-prior

## VoI

- Route: voi
- Pending decision: Choose A or B; a current preference cannot be established without a state probability.
- Signal model: No state probability or signal model is supplied, so there is no evidential posterior or report-specific value estimate.
- Value calculation: For hypothetical prior p, the maximum possible break-even fee is bounded by $100 min(p,1−p); across all priors this bound cannot exceed $50.
- Cost: No fee supplied; delay and other costs $0, provenance: user-elicited.
- Verdict: break-even-only

## Calculation and conditions

The decision owner supplies all losses: L(A,H)=$0, L(A,not-H)=$100, L(B,H)=$100, and L(B,not-H)=$0; provenance: user-elicited.
The state is descriptive H versus not-H, including unnamed alternatives.
Use p only as a sensitivity-only parameter over 0≤p≤1; this range makes no claim about the actual state probability.
Expected losses are $100(1−p) for A and $100p for B.
The preferred action changes at p=0.5: choose B below and A above, with a tie at equality.
The best current loss is $100 min(p,1−p), while perfect information could reduce it to $0.
The universal $50 ceiling follows because min(p,1−p)≤0.5, with equality only at the sensitivity-only crossover.
This ceiling is not a justifiable fee for the unspecified report, whose value might be zero.
Without the missing inputs, neither an actual current expected loss nor a positive report-specific price can be established.

No purchase is made.
