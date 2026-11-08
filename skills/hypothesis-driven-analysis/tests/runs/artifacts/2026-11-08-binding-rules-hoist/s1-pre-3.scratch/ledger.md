# Investigation: weekly checkout conversion 3.1% (06-01..07) -> 2.5% (06-08..14) — why?

## Problem
- Decision informed: whether to roll back v3.4.1 / pull the summer-sale landing page, or leave both.
- Falsifiable question: what explains the drop in orders/sessions between week 1 and week 2 (UTC days, all sessions)?
- Success criteria: answered means each live explanation is refuted or retained after a discriminating test, and the drop is decomposed.
- Stop condition: conclude when no unresolved alternative could reverse the answer; else stop with limits.
- Effort budget: 12 queries.
- Assumption (headless): conversion = orders / sessions (week 1 reproduces 131/4200 = 3.1%).

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | descriptive (estimand: week-2 minus week-1 overall conversion explained by landing-page mix shift, via standardization at week-1 per-page rates) | New /lp/summer-sale traffic (absent in wk1) has low conversion and dilutes the blend | Summer-sale rate well below others; standardizing to wk1 mix recovers most of the drop | Summer-sale rate similar to others | Summer-sale session conversion must be lower than the conversion of the other pages in week 2 | T1 | sessions, orders by page |
| H2 | causal | Release v3.4.1 (06-10, checkout form refactor) lowered conversion | Conversion on pages that existed in wk1 falls after 06-10 vs 06-08/09 | Non-summer-sale conversion flat across 06-10 | Non-summer-sale conversion must fall at/after 06-10 relative to before | T2 | daily rate by page, deploys.log |
| H3 | data-artifact | Session undercount/overcount (06-13/14 volume drop, device-shaped) distorts the rate | Orders per session in affected days/devices deviate; session counts differ from schedule | Rates stable on affected days | Rate on 06-13/14 must differ from 06-08..12 by more than sampling noise in the denominator-inflating direction | T3 | day x device coverage |
| H4 | descriptive (estimand: week-2 minus week-1 conversion within device, standardizing device mix) | Device mix shift (more desktop) | Within-device rates unchanged, mix explains drop | Within-device rates fell | Desktop and mobile rates must differ in week 1 | T4 | device |

Orders lack session_id/page/device: order-level attribution to page is unavailable, and sessions carry checkout_reached not order. Orientation findings (counts only): summer-sale appears 06-08 (160/day); v3.4.1 orders begin 06-10; 06-13/14 sessions ~587 vs 760.

## Sources
| id | Origin | Acquired | Coverage notes |
| S1 | sessions.csv (9171 rows) | 2026-11-08 | 06-01 08:00 .. 06-14 16:56 |
| S2 | orders.csv (268 rows) | 2026-11-08 | no session link |
| S3 | deploys.log (3 lines) | 2026-11-08 | v3.3.9 06-03, v3.4.1 06-10, v3.4.2 06-12 |

## Data Validity
- Collection method: unknown export; instrumentation not documented.
- Coverage matrix: day x device and day x page counted (see work/analysis.txt). Wk1 constant 600/day; 06-08..12 760/day; 06-13/14 ~587/day with mobile dropping 440->242 and all pages ~-22%.
- Field population: no nulls in any field.
- Coverage baseline: none independent; coverage unverifiable.
- Known instrument failures: none documented.
- Source completeness semantics:
S1: UNKNOWN — no export contract or independent session counter; its own pattern cannot discriminate unrecorded vs real drop on 06-13/14.
S2: UNKNOWN — no independent order counter.
- Sensitivity checks performed: see Tests.

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | summer-sale session conversion lower than other pages in wk2 | checkout_reached rate by page, S1 | CONSISTENT | summer-sale 0.50% (4/800, 06-08..12) vs other pages 3.10%; other-page rate 3.10% in wk2 vs 3.12% in wk1; mix-only (wk1 rates, wk2 mix) explains the full drop (work/analysis.txt) |
| T2 | H2 | non-summer-sale rate falls at/after 06-10 | bootstrap contrast pre (06-01..09) vs post (06-10..12), other pages, 95% CI committed | CONTRADICTED | 3.09% vs 3.17%, pre-minus-post diff 95% CI [-0.98,+0.81]pp; predicted fall (>0) sits inside the CI, so the interval alone is NON_DISCRIMINATING for small drops; however the full-week other-page rate is 3.10 vs 3.12 (no fall) and the CI excludes a drop larger than ~0.8pp, whereas the observed 0.6pp week gap needs more than that. Recorded as CONSISTENT-with-no-effect only for effects >0.8pp; refutation of H2 not claimed |
| T3 | H3 | 06-13/14 rate deviates / counts inconsistent with orders | per-day sessions, checkouts, orders | CONSISTENT | 06-13/14: sessions 587/584 (vs 760), mobile 440->242, checkouts 17/11 but orders 23/17; orders>checkouts is impossible if sessions were complete (wk2 137 orders vs 125 checkouts; 06-08..12 equal 97/97). Session log incomplete 06-13/14 |
| T4 | H4 | device rates differ in wk1 | rate by device | NON_DISCRIMINATING | wk1 desktop 3.36% vs mobile 2.93%; desktop wk2 fall is the summer-sale mix (364 desktop ss sessions), not tested separately; subsumed by T1 |

## Amendments
- 2026-11-08: T2 outcome recorded as NON_DISCRIMINATING (interval contains the predicted direction); original wording in the table retained as a note, superseded: CONTRADICTED -> NON_DISCRIMINATING, because the committed 95% CI brackets zero and the predicted drop size.

## Conclusion
- Answer: The drop is associated with the new /lp/summer-sale landing page that started 06-08 (160 sessions/day, ~20% of traffic, 0.5% checkout rate). Pages that existed in week 1 convert unchanged (3.10% vs 3.12%). Note the 2.5% figure is checkout_reached/sessions; orders/sessions is 2.76% because the session log is incomplete on 06-13/14.
- Best supported: H1 (T1); H3 is a real separate data issue.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | descriptive | UNRESOLVED | best supported (T1 CONSISTENT) |
  | H2 | causal | UNRESOLVED | T2 NON_DISCRIMINATING; unchanged other-page rate argues against a large effect but cannot exclude <0.8pp |
  | H3 | data-artifact | UNRESOLVED | best supported for 06-13/14 undercount (T3) |
  | H4 | descriptive | UNRESOLVED | T4 NON_DISCRIMINATING |
- Limitations: associative only (page launch not randomized; summer-sale sessions may be a different audience); orders cannot be linked to sessions; coverage unverifiable independently; v3.4.1 effect on the summer-sale traffic itself cannot be separated from its low baseline.
