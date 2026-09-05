# VoI Record: missing-price

## VoI

- Route: voi — authority: [/private/tmp/data-reasoning-voi/skills/decision-analysis/SKILL.md](/private/tmp/data-reasoning-voi/skills/decision-analysis/SKILL.md), § Routing.
- Pending decision: Choose A versus B under H versus not H.
  A and B currently tie.
- Signal model: Supplied applicable calibration summary: P(plus|H)=0.8, P(plus|not H)=0.2, P(minus|H)=0.2, P(minus|not H)=0.8 (provenance: user-elicited, as user-reported calibration results).
Derived P(plus)=0.5×0.8+0.5×0.2=0.5 and P(minus)=0.5.
Prior odds 1:1 become 4:1 after plus (LR=0.8/0.2=4), so P(H|plus)=0.8; after minus the odds become 1:4 (LR=0.2/0.8=0.25), so P(H|minus)=0.2.
- Value basis: signal-model
- Value calculation:

State H is the descriptive proposition supplied by the owner; not H includes all alternatives, including unnamed explanations.
The owner supplies losses L(A,H)=$0, L(A,not H)=$100, L(B,H)=$100, and L(B,not H)=$0 (provenance: user-elicited).
The owner supplies P(H)=0.5 and P(not H)=0.5 (provenance: user-elicited).
Current risk R0=min(0.5×0+0.5×100, 0.5×100+0.5×0)=$50; A and B tie.
After plus, expected losses are $20 for A and $80 for B, so choose A.
After minus, expected losses are $80 for A and $20 for B, so choose B.
Expected post-report minimum loss R1=0.5×20+0.5×20=$20.
Gross information value G=R0−R1=50−20=$30.
Delay cost is $5 and other costs are $0 (provenance: user-elicited); fee F is unknown.
Total-cost break-even threshold is $30.
The remaining-fee threshold is 30−5=$25; net value is 25−F.
Fees below $25 produce positive net value, $25 breaks even, and fees above $25 produce negative net value.

- Cost: none stated — full cost is unknown because the fee is missing; known components appear above.
- Verdict: break-even-only

Source: `/private/tmp/voi-pricing-control/prompts.json`, case `missing-price`.
All reported numerical inputs are supplied by that request; calculated quantities are derived in the displayed arithmetic.
Verdict semantics and execution authority are governed by [the supplied skill](/private/tmp/data-reasoning-voi/skills/decision-analysis/SKILL.md), § The VoI Route and § Numeric Policy.
