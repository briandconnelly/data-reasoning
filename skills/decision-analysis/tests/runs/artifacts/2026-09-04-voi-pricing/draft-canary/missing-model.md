# VoI Record: missing-model

## VoI

- Route: voi — authority: [/private/tmp/data-reasoning-voi/skills/decision-analysis/SKILL.md](/private/tmp/data-reasoning-voi/skills/decision-analysis/SKILL.md), § Routing.
- Pending decision: Choose A versus B under H versus not H.
  A and B currently tie.
- Signal model: unavailable — no calibration information or defensible signal model is supplied.
- Value basis: upper-bound
- Value calculation:

State H is the descriptive proposition supplied by the owner; not H includes all alternatives, including unnamed explanations.
The owner supplies losses L(A,H)=$0, L(A,not H)=$100, L(B,H)=$100, and L(B,not H)=$0 (provenance: user-elicited).
The owner supplies P(H)=0.5 and P(not H)=0.5 (provenance: user-elicited).
Current risk R0=min(0.5×0+0.5×100, 0.5×100+0.5×0)=$50; A and B tie.
Perfect knowledge permits zero loss in either state: expected perfect-information loss=0.5×0+0.5×0=$0.
Expected value of perfect information is 50−0=$50, an upper bound on gross value of this report.
The stated fee is $10, delay and other costs are $0 (provenance: user-elicited), so full cost C=$10.
The report’s gross value cannot be calculated from these inputs; its net value is bounded above by 50−10=$40.
In this optional-use decision model its gross value can range from $0 to $50, so net value may range from −$10 to $40.
The $50 upper bound is not this report’s break-even price; $10 being below it does not justify purchase.

- Cost: $10 total, consisting of $10 fee plus $0 delay and $0 other costs (provenance: user-elicited).
- Verdict: upper-bound-only

Source: `/private/tmp/voi-pricing-control/prompts.json`, case `missing-model`.
All reported numerical inputs are supplied by that request; calculated quantities are derived in the displayed arithmetic.
Verdict semantics and execution authority are governed by [the supplied skill](/private/tmp/data-reasoning-voi/skills/decision-analysis/SKILL.md), § The VoI Route and § Numeric Policy.
