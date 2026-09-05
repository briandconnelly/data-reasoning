# VoI Record: missing-price

## VoI

- Route: voi — authority: `/private/tmp/voi-pricing-control/SKILL.md` § Routing.
- Pending decision: Choose A or B; currently tied at expected loss $50.
- Signal model: The applicable calibration data supplied in the request gives P(plus|H)=0.8 and P(plus|not H)=0.2, with complementary minus probabilities (provenance: estimated-from-data-in-hand; reference class: the stated applicable calibration cases; conditioning: H or not H).
For plus, LR=0.8/0.2=4, so posterior odds are 1×4=4 and P(H|plus)=0.8; choose A with conditional expected loss $20.
For minus, LR=0.2/0.8=0.25, so posterior odds are 1×0.25=0.25 and P(H|minus)=0.2; choose B with conditional expected loss $20.
There is one signal, so no multiplication of separate evidence items or independence assumption is needed.
P(plus)=P(minus)=0.5, and expected decision loss after observing the report is 0.5×$20+0.5×$20=$20.
Gross expected information value is $50−$20=$30.
- Value calculation: The maximum fee is gross value $30 minus delay cost $5, or $25.
At fee f, net value is $25−f: positive below $25, zero at $25, and negative above $25.
- Cost: Fee unspecified; delay $5 and other costs $0 (provenance: user-elicited).
- Verdict: break-even-only — authority: `/private/tmp/voi-pricing-control/SKILL.md` § The VoI Route.

## Inputs and scope

The binary state is H versus not H, including any unnamed explanations consistent with not H.
The decision owner supplies the losses: A has loss $0 under H and $100 under not H; B has loss $100 under H and $0 under not H (provenance: user-elicited).

The supplied prior P(H)=0.5 is user-elicited, giving prior odds 1:1 and expected loss $50 for either action before the report.

All arithmetic results are derived from the stated inputs or explicitly identified bounds.
No report was purchased.
