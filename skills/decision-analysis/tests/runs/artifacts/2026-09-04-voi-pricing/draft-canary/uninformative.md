# VoI Record: uninformative

## VoI

- Route: voi — authority: [/private/tmp/data-reasoning-voi/skills/decision-analysis/SKILL.md](/private/tmp/data-reasoning-voi/skills/decision-analysis/SKILL.md), § Routing.
- Pending decision: Choose A versus B under H versus not H.
  A and B currently tie.
- Signal model: Supplied applicable calibration summary: plus and minus each have conditional probability 0.5 under each state (provenance: user-elicited, as user-reported calibration results).
Derived predictive probabilities are P(plus)=P(minus)=0.5.
Both likelihood ratios equal 0.5/0.5=1; prior odds 1:1 remain 1:1 and P(H|plus)=P(H|minus)=0.5.
- Value basis: signal-model
- Value calculation:

State H is the descriptive proposition supplied by the owner; not H includes all alternatives, including unnamed explanations.
The owner supplies losses L(A,H)=$0, L(A,not H)=$100, L(B,H)=$100, and L(B,not H)=$0 (provenance: user-elicited).
The owner supplies P(H)=0.5 and P(not H)=0.5 (provenance: user-elicited).
Current risk R0=min(0.5×0+0.5×100, 0.5×100+0.5×0)=$50; A and B tie.
Each return leaves A and B tied at expected loss $50.
R1=0.5×50+0.5×50=$50; G=50−50=$0.
Delay and opportunity costs are $0 (provenance: user-elicited); fee F is unknown.
Net value is −F; total-cost break-even threshold is $0 and remaining-fee break-even threshold is $0.
No positive fee is justified; a free report merely breaks even.

- Cost: none stated — full cost is unknown because the fee is missing; known components appear above.
- Verdict: break-even-only

Source: `/private/tmp/voi-pricing-control/prompts.json`, case `uninformative`.
All reported numerical inputs are supplied by that request; calculated quantities are derived in the displayed arithmetic.
Verdict semantics and execution authority are governed by [the supplied skill](/private/tmp/data-reasoning-voi/skills/decision-analysis/SKILL.md), § The VoI Route and § Numeric Policy.
