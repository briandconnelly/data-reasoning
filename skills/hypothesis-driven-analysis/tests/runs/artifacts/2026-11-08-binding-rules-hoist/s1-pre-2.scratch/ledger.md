# Investigation: Why did weekly checkout conversion fall from 3.1% (wk 06-01..06-07) to 2.5% (wk 06-08..06-14)?

## Problem
- Decision informed: whether to roll back v3.4.1 (06-10 14:00Z), change the summer-sale traffic, or fix measurement.
- Falsifiable question: which of deploy / traffic-mix / data artifact accounts for the fall in orders/sessions (weekly, all sessions, UTC days)?
- Success criteria: answered means each hypothesis has a tested necessary prediction and the drop is apportioned or declared unattributed.
- Stop condition: conclude after T1-T4 run; stop with limits if all are NON_DISCRIMINATING.
- Effort budget: 12 tool calls.
- Orientation findings (coverage/schema only, no cause-outcome looked at): conversion = orders/sessions (orders not linked to sessions by id). New landing page /lp/summer-sale appears from 06-08 (160/day). Orders/day ~19 flat; sessions/day 600 -> ~760. Mobile sessions fall 06-13/14 (440 -> 242) and /home,/product fall ~22% those days. Orders client_version flips 3.4.0 -> 3.4.1 on 06-10. Deploy log: 06-03 copy tweaks /product, 06-10 14:00 checkout form refactor + cart bump, 06-12 logging only. No nulls/dups assumed pending check.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | v3.4.1 deploy (06-10 14:00Z) caused the drop in checkout-completion conversion | conversion after deploy lower than before it within wk2 | no step at deploy; wk2 already low before | wk2 conversion (non-summer-sale sessions) after 06-10 14:00Z must be lower than wk2 conversion before it; predicted contrast about -0.6pp | T1 | sessions, orders, deploys.log |
| H2 | descriptive (estimand: share of the wk1->wk2 rate change due to /lp/summer-sale traffic mix, via checkout_reached rate by landing page) | New /lp/summer-sale traffic converts worse and dilutes the rate | summer-sale reach rate far below others; /home,/product rates flat wk1 vs wk2 | summer-sale reach rate similar; other pages fell too | summer-sale checkout_reached rate must be lower than the /home+/product rate in wk2 | T2 | sessions |
| H3 | data-artifact | The mobile session hole on 06-13/14 (or session/order mismatch) produces the apparent drop | wk2 drop vanishes when 06-13/14 excluded | drop persists on 06-08..12 | the drop on 06-08..06-12 only (complete days) must be much smaller than the full-week drop | T3 | sessions, orders |
| H4 | causal | Deploy broke the reach->order step of checkout (form refactor), not upstream traffic | share of reached sessions that become orders falls after deploy | reach rate falls but order/reach stable | orders per checkout_reached session must be lower after deploy than before (wk2 pre vs post) | T4 | sessions, orders |

## Sources
| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 rows) | 2026-11-08 | 06-01..06-14; no linkage to orders |
| S2 | data/s1-conversion/orders.csv (268 rows) | 2026-11-08 | 06-01..06-14 |
| S3 | data/s1-conversion/deploys.log (3 lines) | 2026-11-08 | three releases 06-03, 06-10, 06-12; used only for timing |

## Data Validity
- Collection method: unknown (flat exports). 
- Coverage matrix: day x device and day x landing_page session counts examined; day x client_version for orders. Hole: mobile sessions 06-13/14 ~-40% vs 06-12 with desktop unchanged; no independent denominator.
- Coverage baseline: none exists; coverage recorded as unverifiable.
- Source completeness semantics:
S1: UNKNOWN — no export contract or independent counter; its own pattern cannot say whether mobile sessions 06-13/14 were absent, unrecorded, or truly fewer.
S2: UNKNOWN — same.
- Sensitivity checks performed: see Tests (95% intervals committed in advance, normal approx for difference of proportions).

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | wk2 orders/sessions after deploy < before (non-summer sessions not separable from orders; use all sessions and then a sensitivity version), 95% CI on contrast | difference of proportions | NON_DISCRIMINATING | S1,S2: wk2 pre 2.66% (54/2028) vs post 2.82% (83/2943) orders/sessions, contrast +0.16pp 95% CI (-0.76,+1.08); reach-rate version -0.25pp (-1.14,+0.64), non-summer -0.25pp (-1.35,+0.85). Predicted -0.6pp sits inside every interval; detection limit ~±1pp. Also: wk1 vs wk2-pre already 3.12%->2.66%, i.e. the fall is visible before the deploy (point estimate). |
| T2 | H2 | summer-sale reach rate < /home+/product reach rate in wk2 | 95% CI contrast | CONSISTENT | S1: summer-sale reach 0.57% (6/1053) vs /home+/product 3.04% (119/3918), contrast -2.47pp CI (-3.17,-1.76). Non-summer wk1 3.12% -> wk2 3.04%, -0.08pp CI (-0.83,+0.67). Mix arithmetic: summer-sale was 21.2% of wk2 sessions; wk2 reach 2.51% vs 3.04% without it (~0.53 of the 0.61pp fall). CI on within-page change is wide (cannot exclude a within-page drop of the full size), so 'flat' is not established, but the dilution is exact arithmetic. |
| T3 | H3 | 06-08..12 drop much smaller than full-week | rates excluding 06-13/14 | NON_DISCRIMINATING | S1,S2: complete days 06-08..12 reach 3.12%->2.55%, -0.57pp CI (-1.29,+0.16) vs full week -0.61pp; interval includes 0 so cannot refute; point estimate says the drop persists without 06-13/14. Missing mobile sessions would, if anything, inflate the rate, but source completeness is UNKNOWN so direction is not asserted. |
| T4 | H4 | orders/checkout_reached lower after deploy than before in wk2 | ratio, daily | NON_DISCRIMINATING | Orders (83) exceed checkout_reached sessions (71) post-deploy; orders carry no session id, so the reach->order stage ratio is not measurable (S1,S2). |

## Amendments
(none)

## Conclusion
- Answer: the fall is mostly explained by composition: a new /lp/summer-sale landing page (21% of week-2 sessions, 0.57% reach rate vs 3.04% elsewhere) arrived 06-08, diluting the rate. Excluding it, week-2 reach rate is 3.04% vs 3.12% in week 1. The v3.4.1 deploy is not shown to be responsible but cannot be cleared either.
- Best supported: H2 (T2 CONSISTENT, discriminating: dilution arithmetic plus a non-summer rate near week 1). Association only; traffic mix was not randomized.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 NON_DISCRIMINATING: interval (-1.14,+0.64) contains the predicted -0.6pp; point estimates show no step at the deploy |
  | H2 | descriptive | UNRESOLVED | best supported (T2 CONSISTENT) |
  | H3 | data-artifact | UNRESOLVED | T3 NON_DISCRIMINATING; completeness UNKNOWN |
  | H4 | causal | UNRESOLVED | T4 NON_DISCRIMINATING; orders not linkable to sessions |
- Limitations: the 3.1%/2.5% figures match checkout_reached/sessions (3.12%/2.51%); orders/sessions is 3.12%/2.76%. Sample is small (~130 events/week), CIs ~±1pp. Mobile session drop 06-13/14 unexplained. No pre-period design identifies a deploy effect; causal-identification-review is the continuation. Within-page rates cannot be shown flat, only within about ±0.8pp.
