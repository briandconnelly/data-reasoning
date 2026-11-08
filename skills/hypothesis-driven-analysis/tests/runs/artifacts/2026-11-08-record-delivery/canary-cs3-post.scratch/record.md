# Identification Review: Effect of the new checkout flow on West checkout completion time

## Question

- Causal question, restated as a counterfactual contrast: how would West's median checkout completion time over the two weeks from 2026-03-15 differ had West stayed on the old flow?
- Estimand: effect of the new flow on completion time for West checkouts, 2026-03-15 to 2026-03-28.
- Assignment mechanism as stated: "West was selected for the checkout-flow rollout because it had the highest cart-abandonment complaint volume of any region in the quarter before rollout." (data/cs3-rollout/targeting_note.md; West 184 vs East 97 complaints, 2025-11-01 to 2026-01-31)
- Route: review
- Provenance: daily.csv (140 rows, one per region-day, 2026-02-01..2026-04-11, complete per data_notes.md), promotions.log, ux_cleanup_note.md, targeting_note.md, all under data/cs3-rollout/. Probe script: work/probe.py. The `completion_time_seconds` column is assumed to be the daily median; the extract does not say.

## Design: West before/after (implicit in the claim)

- Design: West pre-rollout weeks vs two post-rollout weeks, no comparison region
- Identifying assumptions:
  - A1: Absent the new flow, West completion time would have stayed at its pre-period level (no pre-existing trend).
  - A2: Nothing else that moves completion time changed in West at or near 2026-03-15.
- Assumption probes:

  | assumption | probe | assessment | evidence or reason |
  | --- | --- | --- | --- |
  | A1 | Slope of West daily completion time over 2026-02-01..03-14 | contradicted | West falls about 0.53 s/day across the pre-period (weekly means 206.6, 201.7, 198.2, 195.1, 191.2, 187.2). ux_cleanup_note.md states the cleanup improved West "through the whole pre-period". |
  | A2 | Read promotions.log and ux_cleanup_note.md; West avg_order_value pre vs post | contradicted | A West-wide price promotion launched 2026-03-15, the same day as the rollout. West avg_order_value rose from 44.94 to 53.62 while East stayed at 44.96 / 45.01. Volume is unchanged (590 / 591). |

- Data requirements: West pre/post daily series. Present.
- Threat register:

  | threat | probe | result |
  | --- | --- | --- |
  | Pre-existing downward trend (UX cleanup) | pre-period slope | present in West; trend-extrapolation baseline is itself unidentified |
  | Concurrent promotion | promotions.log, AOV | same-day launch, so confounded |
  | Selection of West on complaint volume | targeting note; pre-period level comparison | West was selected because it was worst; regression-to-the-mean or targeting-driven differences cannot be probed with this data |

- Disposition: assumption-contradicted — A1 (pre-trend slope) and A2 (promotion launched the same day)

## Design: Difference-in-differences, West vs East

- Design: DiD with East as the untreated comparison
- Identifying assumptions:
  - A1: Absent the new flow, West and East would have had parallel completion-time trends (a pre-period trend gap must be absent).
  - A2: No West-only shock coincides with rollout.
  - A3: East's completion time is unaffected by the West rollout (no spillover), and East is a valid counterfactual despite West being chosen for its complaint volume.
- Assumption probes:

  | assumption | probe | assessment | evidence or reason |
  | --- | --- | --- | --- |
  | A1 | Pre-period slope, West vs East | contradicted | West -0.53 s/day, East -0.02 s/day over the same 42 days. The East control is flat while West was already improving. West level is also different (about 197 vs 180 s). |
  | A2 | promotions.log; AOV West vs East pre/post | contradicted | West-only promotion from 2026-03-15. East has no promotion activity. Whether a discount changes completion time is not testable here, but the timing makes the two inseparable. |
  | A3 | East post-period completion time and volume vs pre | not-contradicted | East stayed at 180.0 pre / 179.9 post and volume 543 / 542, so no sign of spillover. The probe could not see spillover that leaves East's aggregate unchanged, and says nothing about whether East is a valid counterfactual for a region selected on complaints. |

- Data requirements: both regions, pre and post. Present.
- Threat register:

  | threat | probe | result |
  | --- | --- | --- |
  | Differential pre-trend | pre-period slopes | contradicted for A1 |
  | Concurrent West promotion | log, AOV | confounded in time with rollout |
  | Selection on complaints | targeting note | no probe available; differences in West customer mix or friction cannot be checked with this data |
  | Persistence of the post-period drop | West means for 2026-03-29..04-11 (about 146 s) vs the first post weeks (about 145-147 s) | step then flat. This is a descriptive fact; it does not separate flow from promotion, since both persist |

- Disposition: assumption-contradicted — A1 (differential pre-trend) and A2 (concurrent promotion)

## Other designs considered (no Design block)

- Synthetic control and regression discontinuity are not constructible here: the data holds two regions only (no donor pool) and there is no eligibility cutoff.
- A prospective randomized experiment (randomize sessions or users within West, or randomize rollout timing across regions, with promotion exposure equal across arms) is the identifying option. Naming it is the whole of this skill's permission; its mechanics are out of scope.

## Handoff

- Facts: (1) West pre-period completion time was already falling about 0.53 s/day while East was flat (-0.02 s/day), because of a separate UX cleanup. (2) A West-only price promotion launched 2026-03-15, the same day as the flow, and West avg_order_value rose from 44.94 to 53.62 while East stayed flat. (3) West was chosen for the rollout because of its complaint volume ("highest cart-abandonment complaint volume"). (4) West's weekly mean fell from 187.2 (last pre week) to 144.5 (first post week), then stayed near 146-147 through 2026-04-11; East stayed near 180 throughout. (5) The data holds two regions only.
- Assumptions: any downstream estimate would be conditional on a way to remove the West-specific pre-trend, on the promotion having no effect on completion time (or on its effect being separable), and on no selection-driven difference between West and East.
- Dispositions: assumption-contradicted (West before/after); assumption-contradicted (DiD West vs East); not-constructible (synthetic control / RD, noted outside the Design blocks)

This block states facts, assumptions, and dispositions only.
