# Identification Review: Did the new checkout flow (West, 2026-03-15) cause the fall in West median completion time?

## Question

- Causal question, restated as a counterfactual contrast: West median checkout completion time in the two weeks from 2026-03-15 under the new flow, versus what it would have been in West over the same two weeks under the old flow.
- Estimand: effect of the new flow on West median completion time (seconds), 2026-03-15 to 2026-03-28.
- Assignment mechanism as stated: "West was selected for the checkout-flow rollout because it had the highest cart-abandonment complaint volume of any region in the quarter before rollout." (data/cs3-rollout/targeting_note.md). Also, from the request: East stayed on the old flow throughout.
- Route: review

## Design: D1 West before/after (implicit in the claim)

- Design: compare West median completion time in the pre-rollout weeks with the two post weeks.
- Identifying assumptions:
  - A1: Absent the new flow, West completion time would have stayed at its pre-period level (no pre-existing trend).
  - A2: No other change at West around 2026-03-15 moves completion time or the mix of checkouts.
  - A3: No region-wide shock in the window would have moved completion time absent the flow (common shocks).
- Assumption probes:

  | assumption | probe | assessment | evidence or reason |
  | --- | --- | --- | --- |
  | A1 | P1: West weekly median completion time across the six pre-rollout weeks | contradicted | West weekly medians, weeks of 02-01..03-08: 206.3, 204.1, 198.1, 194.7, 191.6, 187.4 s: monotone decline of about 19 s before rollout. ux_cleanup_note.md says a UX cleanup shipped to West gradually across the pre-weeks and kept improving completion time. |
  | A2 | P4: West vs East weekly mean avg_order_value; P5: weekly volume; read of promotions.log | contradicted | West AOV ~44.6-45.3 in all pre-weeks, then 53.3, 53.9, 55.0, 54.2 from the week of 03-15; East flat (43.9-45.5). promotions.log: West price promotion launched 2026-03-15, same day. Volume shows no visible West step (572-609 pre, 591-622 post), so P5 did not contradict a mix shift but is coarse. The promotion is a confirmed concurrent West-only change; whether it moves completion time is not separable here. |
  | A3 | P6: East pre vs post change | not-contradicted | East medians flat (178.3-182.3 all ten weeks; post-minus-pre change -0.14 s). It could not see a shock that hit West only. |

- Data requirements: West daily completion time over pre and post windows (present: 70 days, one row per day, data_notes.md confirms completeness).
- Threat register:

  | threat | probe | result |
  | --- | --- | --- |
  | Pre-existing improving trend (UX cleanup) | P1 | present; see A1 |
  | Concurrent price promotion, West only | P4, promotions.log | present; see A2 |
  | Selection of West for high complaints (regression to the mean, different responsiveness) | NONE | Complaint counts exist only as quarterly totals (West 184, East 97), not as a daily series; no probe on completion time. Would need the complaint series by week through the pre-period. |

- Disposition: assumption-contradicted (A1 and A2 contradicted)

## Design: D2 West-vs-East difference-in-differences

- Design: West-minus-East change in median completion time, pre-period 2026-02-01..03-14 to post 2026-03-15..03-28; East as the untreated comparison.
- Identifying assumptions:
  - A1: Parallel trends: absent the new flow, West and East completion times would have moved in parallel.
  - A2: No West-only change at 2026-03-15 other than the flow moves completion time.
  - A3: The new flow's effect on West is not confounded with West's selection for high complaints (West would not have been on a different trajectory because of why it was chosen).
  - A4: East is unaffected by the West rollout (no spillover).
- Assumption probes:

  | assumption | probe | assessment | evidence or reason |
  | --- | --- | --- | --- |
  | A1 | P3: pre-period gap trend; P7: placebo "rollout" dates inside the pre-period | contradicted | East flat, West falling, so the gap narrowed over the pre-period. Placebo West-minus-East differences (median, two-week windows, no rollout occurred): 02-01..02-14 vs 02-15..02-28 = -8.14 s; 02-15..02-28 vs 03-01..03-14 = -7.55 s. A design with parallel trends should give about 0. Placebo values are evidence about the assumption, not effect estimates. |
  | A2 | P4, promotions.log | contradicted | Same evidence as D1 A2: West-only promotion launched 03-15; East none. |
  | A3 | NONE | not-testable-here | Considered: pre-trend placebo (P7), which is silent on why West was chosen; complaint counts are quarterly only. Would need weekly complaint volume and completion time by region before 02-01 to see whether West was already on a different path. |
  | A4 | P6: East post vs pre | not-contradicted | East change -0.14 s; the probe could not see small or delayed spillover, nor a spillover that moves East in the same direction as a coincidental East shock. |

- Data requirements: both regions, pre and post, daily (met). A longer pre-period would help trend modelling (only six weeks exist for West's trend).
- Threat register:

  | threat | probe | result |
  | --- | --- | --- |
  | Non-parallel pre-trend (UX cleanup in West only) | P3, P7 | contradicted; see A1 |
  | Concurrent West promotion | P4 | present; see A2 |
  | Selection on complaint volume | NONE | see A3 |
  | Only two post weeks | NONE | Persistence or novelty effects cannot be checked from 14 post days used here; later data to 04-11 exists in the extract but the request fixed the two-week comparison. |

- Disposition: assumption-contradicted (A1 and A2 contradicted)

## Handoff

- Facts: West weekly median completion time fell steadily before rollout (206.3 to 187.4 s) and then dropped to about 146-147 s in the four weeks from 03-15; East stayed 178-182 s throughout. A West-only price promotion launched 03-15, same day as the flow (West AOV rose from about 45 to about 54). A separate West-only UX cleanup was shipping through the pre-weeks. West was chosen for having the most complaints (184 vs 97 for East in the prior quarter). Placebo difference-in-differences with no rollout gives about -8 s per two weeks, not 0. Naive pre/post West difference (-50.3 s on window medians) and the DiD difference (-50.1 s) both include the trend and the promotion and are not effect estimates.
- Assumptions: any downstream estimate would be conditional on: West's counterfactual trend being modelled correctly despite the cleanup; the promotion having no effect on completion time (or being separable); no selection-driven differential trajectory; no spillover to East.
- Dispositions: assumption-contradicted (D1 West before/after); assumption-contradicted (D2 West-vs-East DiD)
