# Investigation: why did weekly checkout conversion fall 3.1% -> 2.5% (wk 2026-06-01 vs wk 2026-06-08)?

## Problem
- Decision informed: whether to roll back v3.4.1 / change the summer-sale campaign, or neither.
- Falsifiable question: what accounts for the drop in orders/sessions between 06-01..06-07 and 06-08..06-14 (UTC, all sessions)?
- Success criteria: answered = drop decomposed among live explanations, each tested on a preregistered discriminating prediction.
- Stop condition: conclude when no unresolved alternative could reverse the answer; else stop with limits.
- Effort budget: 12 tool calls.
- Assumption (headless): conversion = orders / sessions (week 1 check must give ~3.1%). Nothing assigned the exposure (no randomization) -> associative wording only.

## Orientation findings (coverage/inventory only, no cause-outcome relationship inspected)
- sessions 9171, orders 268, no nulls/dups. New landing page /lp/summer-sale appears from 06-08 (160/day) — not present in wk1.
- Session rows drop on 06-13/14 (~587/day vs ~760 on 06-08..12) with /home,/product,/lp all down; per-day orders do not drop correspondingly. Candidate logging gap.
- Orders client_version 3.4.0 through 06-09, 3.4.1 from 06-10 (deploys.log: v3.4.1 06-10 14:00 checkout refactor; v3.3.9 06-03 copy tweak; v3.4.2 06-12 logging only — no orders show 3.4.2).

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Test | Data |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | descriptive (estimand: wk2-minus-wk1 conversion explained by session mix shift toward /lp/summer-sale) | New low-converting landing page diluted the blended rate | /lp/summer-sale conv well below others; conversion on pre-existing pages ~unchanged | lp conv similar to others, or old pages dropped too | /lp/summer-sale conversion must be lower than conversion on other pages in wk2 | T1 | S1,S2 |
| H2 | causal | v3.4.1 checkout refactor (06-10) reduced conversion | conversion on the same pages falls from 06-10 onward vs 06-08/09 and wk1 | no step at 06-10 within existing pages | conversion on /home+/product sessions after 06-10 must be lower than before 06-10 | T2 | S1,S2,S3 |
| H3 | data-artifact | 06-13/14 session under-logging distorts the denominator | sessions drop on 06-13/14 without matching drop in orders; excluding days changes wk2 rate materially | no session/order mismatch | session-count drop on 06-13/14 must not be matched by an order drop | T3 | S1,S2 |
| H4 | descriptive (estimand: conversion by device, wk2 vs wk1) | Device mix shift (mobile/desktop) | device conv differs and mix changed | mix stable | desktop share must change between weeks | T4 | S1 |

## Sources
| S1 | sessions.csv | 9171 rows 06-01..06-14 | no independent denominator |
| S2 | orders.csv | 268 rows | |
| S3 | deploys.log | 3 lines | |

## Data Validity
- Coverage matrix: day x device and day x landing_page tabulated (work/cov.py). Anomaly: 06-13/14 volume dip across all pages; no expected schedule or independent denominator -> coverage unverifiable, not clean.
- Source completeness: S1: UNKNOWN — no independent session counter, so absent sessions cannot be read as no-traffic vs unlogged.
- S2: UNKNOWN — no independent order ledger.
- Sensitivity: results to be shown with and without 06-13/14, bootstrap intervals on rates.

## Tests
| T1 | H1 | lp conv < other pages conv in wk2 | | NOT_TESTED | |
| T2 | H2 | /home+/product conv after 06-10 < before | | NOT_TESTED | |
| T3 | H3 | session drop 06-13/14 unmatched by order drop | | NOT_TESTED | |
| T4 | H4 | desktop share changes | | NOT_TESTED | |

## Amendments
(none)

## RESULTS (append; scripts t.py, t2.py)
- Metric reconciliation: user's 3.1%/2.5% = checkout_reached/sessions (3.12% -> 2.51%); orders/sessions is 3.12% -> 2.76%, so orders is not the metric.
- T1 H1: CONSISTENT. /lp/summer-sale 6/1053 = 0.57% (boot 95% 0.19-1.04) vs /home 2.68%, /product 3.76%; lp = 21% of wk2 sessions. Non-lp wk2 119/3918 vs wk1 131/4200: diff -0.86..+0.67pp CI (includes 0). Daily lp: 0-2 conversions/160 sessions every day incl. before 06-10 deploy.
- T2 H2: CONTRADICTED on necessary prediction. non-lp 06-08/09 = 3.00%, 06-10..14 = 3.05%; diff post-pre 95% CI -1.16..+1.12pp. adequacy: detects drops >~1.1pp (variants: 0.5-3pp drop; a 0.6pp drop, which is what the whole wk drop needs on non-lp traffic, is NOT reliably detected). LP rate before deploy already ~0.6%, so no step at 06-10. Status REFUTED as cause of a sizeable drop, with detection limit noted.
- T3 H3: CONSISTENT (artifact real, small). 06-13/14 sessions 587/584 vs 760; orders 23/17 exceed checkout_reached 17/11 by 6 each -> session rows missing (~350 sessions, ~12 checkout-reached). Adjusted wk2 ≈ 137/5320 = 2.58%; artifact explains ~0.07pp of the 0.6pp drop. Cause of missing rows UNKNOWN.
- T4 H4: NON_DISCRIMINATING/CONTRADICTED: desktop share 44%->49% but driven by lp traffic; desktop non-lp not tested separately.
