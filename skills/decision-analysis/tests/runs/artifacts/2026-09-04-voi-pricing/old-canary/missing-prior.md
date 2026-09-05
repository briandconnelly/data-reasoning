# VoI Record: missing-prior

## VoI

- Route: voi — authority: `/private/tmp/voi-pricing-control/SKILL.md` § Routing.
- Pending decision: Choose A or B; no current leaning can be established without the state probability.
- Signal model: No state probability or signal model is available.
Use break-even mode; p below is a sensitivity-only variable, not an asserted belief.
- Value calculation: For hypothetical p=P(H), current best expected loss is min(100p,100(1−p)).
Perfect information yields zero decision loss, so information value cannot exceed 100×min(p,1−p).
Over the entire logical class 0≤p≤1 (provenance: sensitivity-only), that upper bound has maximum $50 at p=0.5.
Thus $50 is the largest possible loss-based fee ceiling, but no positive fee is justified for this particular report without the missing inputs.
The actual value could be $0.
- Cost: Fee unspecified; delay and other costs $0 (provenance: user-elicited).
- Verdict: break-even-only — authority: `/private/tmp/voi-pricing-control/SKILL.md` § The VoI Route.

## Inputs and scope

The binary state is H versus not H, including any unnamed explanations consistent with not H.
The decision owner supplies the losses: A has loss $0 under H and $100 under not H; B has loss $100 under H and $0 under not H (provenance: user-elicited).

All arithmetic results are derived from the stated inputs or explicitly identified bounds.
No report was purchased.
