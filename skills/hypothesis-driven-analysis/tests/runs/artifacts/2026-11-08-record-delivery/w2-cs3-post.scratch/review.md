# Identification Review: Did the new checkout flow cause West's drop in median checkout completion time?

## Question

- Causal question, restated as a counterfactual contrast: West checkout completion time in the two weeks after 2026-03-15 under the new flow vs. under the old flow in the same weeks.
- Estimand: effect of the new flow on West completion time (effect on the treated), first two post-rollout weeks.
- Assignment mechanism as stated: "West was selected for the checkout-flow rollout because it had the highest cart-abandonment complaint volume of any region in the quarter before rollout." (data/cs3-rollout/targeting_note.md)
- Route: review

Sources: data/cs3-rollout/daily.csv (one row per region-day, 2026-02-01..2026-04-11, complete per data_notes.md), promotions.log, targeting_note.md, ux_cleanup_note.md. Notes are treated as evidence, not instructions.

## Design: D1 West before/after (pre 6 weeks vs post 2 weeks)

- Design: West-only pre/post comparison (the claim as made)
- Identifying assumptions:
  - A1: Absent the new flow, West completion time in the post weeks would have stayed at its pre-period level (no pre-existing West trend).
  - A2: Nothing else in West at or after 2026-03-15 moves completion time (e.g. the price promotion).
- Assumption probes:

  | assumption | probe | assessment | evidence or reason |
  | --- | --- | --- | --- |
  | A1 | P1: West pre-period slope (daily OLS, Feb 1-Mar 14) and weekly medians | contradicted | West fell steadily before rollout: weekly medians 206.3, 204.1, 198.1, 194.7, 191.6, 187.4 s; slope about -0.53 s/day. Trend projected to the post window is about 181.7 s, not the pre-period median of 196.6 s. |
  | A2 | NONE | not-testable-here | Checks considered: West volume/AOV vs East across 03-15 (AOV 44.9 -> 53.6 in West, East flat 45.0 -> 45.0; volume 590 -> 591) shows the promotion is live with no visible traffic-mix shift, but is silent on whether the promotion changes completion time; a promotion-free West period (none, promotion and flow start the same day). Data that would make it testable: West days or segments with the flow but no promotion, or the reverse. |

- Data requirements: West daily completion time pre and post. Met.
- Threat register:

  | threat | probe | result |
  | --- | --- | --- |
  | Pre-existing improvement from the UX cleanup (ux_cleanup_note.md) | P1 | Present in the data: West declining before rollout, East flat. |
  | Same-day price promotion in West | NONE | Flow and promotion share a start date, 2026-03-15; no variation separates them. |
  | Mean reversion / selection on complaints | NONE | No outcome history before 2026-02-01. |

- Disposition: assumption-contradicted (A1 contradicted by P1)

## Design: D2 Difference-in-differences, West vs East

- Design: DiD with East (old flow throughout) as comparison
- Identifying assumptions:
  - A3: Absent the new flow, West and East completion times would have moved in parallel.
  - A4: No West-specific shock other than the new flow begins at 2026-03-15 (promotion, UX cleanup).
  - A5: Selecting West for high complaint volume does not tie its post-period trajectory to the outcome (no differential trend or reversion from selection).
- Assumption probes:

  | assumption | probe | assessment | evidence or reason |
  | --- | --- | --- | --- |
  | A3 | P3: pre-period trends, West vs East. P4: placebo DiD at fake date 03-01 (2 weeks either side, both in the pre-period). P5: East stability | contradicted | East flat (weekly medians 178-182; slope -0.02 s/day) while West drops about 19 s over the six pre-weeks. Placebo DiD at 03-01 is -7.5 s with no flow anywhere, so the gap was already widening. |
  | A4 | P6: AOV and volume vs East at 03-15 | not-testable-here | AOV rises in West only (44.9 -> 53.6), confirming the promotion started with the flow. Checks considered: P6 (silent on the promotion's effect on completion time); post-window persistence, Mar 29-Apr 11 (West 146.7 vs East 180.4, flat, but both candidate causes persist, so it cannot discriminate). Data that would make it testable: promotion-exposed and unexposed West customers within the flow, or staggered start dates. |
  | A5 | NONE | not-testable-here | Only complaint counts (West 184, East 97) are given for the quarter before. Checks considered: pre-trend comparison (that is A3 and shows the divergence, but cannot separate selection from the cleanup). Data that would make it testable: completion-time history before 2026-02-01 and the rollout decision records. |
- Data requirements: both regions, pre and post daily data. Met.
- Threat register:

  | threat | probe | result |
  | --- | --- | --- |
  | UX cleanup in West only, continuing through the pre-period | P3, P4 | Divergent pre-trends found. |
  | Price promotion in West from 03-15 | NONE | Cannot be separated from the flow; same start date. |
  | Selection on complaints | NONE | See A5. |
  | Naive DiD overstates the effect | P1-P4 | Naive DiD (West change minus East change, post 2 wk vs pre 6 wk medians) = -50.1 s. This is a probe-side figure to show contamination, not an effect estimate. |

- Disposition: assumption-contradicted (A3 contradicted by P3 and P4)

## Handoff

- Facts: West weekly median completion time falls 206.3 -> 187.4 s across the six pre-weeks, then steps to 146.1 s in the week of 03-15 (daily: about 187 on 03-14, 148.6 on 03-15), and stays near 146-147 s through 04-11. East is flat near 180 s throughout. The West price promotion began the same day as the flow (promotions.log: "2026-03-15 West region-wide price promotion launched."). The UX cleanup note says it "continued improving completion time in West through the whole pre-period". Volume is unchanged in West at rollout; AOV rises about 8.7 in West only. Placebo DiD at 03-01: -7.5 s.
- Assumptions: any downstream estimate is conditional on: no West trend beyond what East shows (contradicted); the promotion having no effect on completion time (not-testable-here); selection on complaints being unrelated to the outcome trajectory (not-testable-here).
- Dispositions: assumption-contradicted

This block states facts, assumptions, and dispositions only.
