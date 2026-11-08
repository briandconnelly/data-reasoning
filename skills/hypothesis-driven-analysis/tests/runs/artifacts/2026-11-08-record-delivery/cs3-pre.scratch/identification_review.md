# Identification Review: Did the new checkout flow cause West's median completion time to fall?

## Question
- Counterfactual: West checkout completion time in the 2 weeks after 2026-03-15 under the new flow vs under the old flow, same weeks, same customers.
- Estimand: effect of new flow on median completion time in West, post-rollout weeks.
- Assignment mechanism as stated: "West was selected for the checkout-flow rollout because it had the highest cart-abandonment complaint volume of any region in the quarter before rollout." (data/cs3-rollout/targeting_note.md; West 184 vs East 97 complaints)
- Route: review

## Design 1: West pre/post (before/after, implicit in the claim)
- Identifying assumptions:
  - A1: Absent the new flow, West's median time would have stayed at its pre-period level.
  - A2: No other change in West at 2026-03-15 moves completion time or the mix of checkouts.
- Probes:
  | assumption | probe | assessment | evidence |
  | A1 | P1 West weekly medians, pre-period | contradicted | West fell every week from 206.3 (wk1) to 187.4 (wk6), slope -0.53 s/day; West was already improving before rollout. |
  | A2 | P3 AOV/volume pre vs post; ux_cleanup_note; promotions.log | contradicted | West AOV 44.94 -> 53.62 at the rollout date from a region-wide price promotion launched 2026-03-15 (promotions.log); a UX cleanup also shipped to West through the pre-period (ux_cleanup_note.md). Volume flat (590 -> 591), so no volume shift visible; probe cannot see mix change in basket type. |
- Data requirements: pre and post daily West data - met.
- Threat register:
  | threat | probe | result |
  | pre-existing trend / UX cleanup | P1 | trend present, see A1 |
  | concurrent promotion | P3 | AOV +8.7 at rollout date; timing coincident |
  | selection on complaints (regression to mean / West worst-off) | NONE | needs pre-assignment complaint series; only a quarter total exists |
- Disposition: assumption-contradicted

## Design 2: Difference-in-differences, West vs East
- Identifying assumptions:
  - A3: Absent the new flow, West and East would have moved in parallel (same trend in time).
  - A4: Nothing else differential hit West at 2026-03-15 (promotion, cleanup).
  - A5: West's selection (highest complaints) is unrelated to how its completion time would have evolved.
  - A6: Completion time is a comparable measure in both regions pre/post (no composition change).
- Probes:
  | assumption | probe | assessment | evidence |
  | A3 | P1 pre-trend comparison | contradicted | East flat (slope -0.02 s/day, weekly medians 178.3-182.3); West slope -0.53 s/day. Not parallel. |
  | A3 | P2 East placebo pre->post | not-contradicted | East median 180.0 -> 179.9; shows no common shock in East; cannot see a West-specific shock or trend. |
  | A4 | P3 + notes | contradicted | Region-wide West-only promotion at 2026-03-15 (AOV 44.94 -> 53.62; East 44.96 -> 45.01); UX cleanup West-only. Both coincide with / precede treatment and are inseparable from it. |
  | A5 | NONE | not-testable-here | Checks considered: pre-period trend (P1) is silent on why West was chosen; needs pre-assignment series of complaints and completion time by region and the selection rule. |
  | A6 | P3 volume | not-contradicted | Volume unchanged in both regions; cannot see changes in who or what is being bought (AOV shift suggests basket mix may differ). |
- Data requirements: both regions, pre and post - met (141 rows, one per region-day, per data_notes.md), but only 6 pre weeks and 2 post weeks.
- Threat register:
  | threat | probe | result |
  | differential pre-trend (UX cleanup) | P1 | present |
  | concurrent promotion | P3 | present, same date |
  | trend-continuation sensitivity (P4) | extrapolating West's pre slope alone | West pre median 196.6, observed post 146.3 (-50.3); East -0.1. The pre-slope alone, if it kept going, would account for roughly 15 of the 50 seconds (arithmetic from -0.53 s/day x ~28 days). This is a sensitivity of the probe, not an effect estimate; it shows the naive drop is not all attributable to the flow, and the promotion's contribution is not separable. |
  | selection | NONE | see A5 |
- Disposition: assumption-contradicted

## Handoff
- Facts: West median 196.6 -> 146.3 (pre -> first 2 weeks); East 180.0 -> 179.9. West already declining ~0.53 s/day before rollout, East flat. West-only region-wide price promotion started 2026-03-15; West-only UX cleanup ran through the pre-period. West chosen for highest complaint volume (184 vs 97). Data complete 2026-02-01..04-11.
- Assumptions any causal number would be conditional on: parallel trends absent treatment (contradicted); no concurrent West-specific change (contradicted); selection on complaints unrelated to counterfactual trend (not-testable-here); comparable measurement.
- Dispositions: Design 1 assumption-contradicted; Design 2 assumption-contradicted.
