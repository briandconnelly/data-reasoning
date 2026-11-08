# Investigation: Why did weekly checkout conversion fall from 3.1% (wk 06-01) to 2.5% (wk 06-08)?

## Problem
- Decision informed: whether to roll back v3.4.1 / fix checkout, or treat the drop as traffic-mix.
- Falsifiable question: what explains the fall in orders/sessions between 2026-06-01..07 and 2026-06-08..14 (all sessions, units = fraction)?
- Success criteria: answered means the drop is decomposed into contributing explanations that survive discriminating tests; unattributed residual reported as such.
- Stop condition: conclude when no unresolved alternative could reverse the answer; otherwise stop with limits.
- Effort budget: 12 queries.

## Hypotheses
Orientation (counts only, before any cause-outcome test) found: sessions on /lp/summer-sale appear from 06-08 (~160/day, none before); sessions/day rise 600 -> 760; device mix shifts on 06-13/14. Orientation also displayed daily checkout_reached/order counts (outcome by day, not by cause).

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 (retrospective) | descriptive (estimand: change in overall conversion attributable to adding summer-sale landing sessions, = wk2 rate minus wk2 rate excluding that landing page) | Composition: new low-converting summer-sale traffic dilutes the rate | excluding summer-sale, wk2 rate ~ wk1 rate | wk2 rate excl. summer-sale still well below wk1 | wk2 conversion excluding summer-sale sessions must be within the 95% CI of the wk1 rate | T1 | sessions, orders |
| H2 | causal | v3.4.1 (06-10) checkout form refactor reduced checkout completion | session->order rate among checkout-reached falls after 06-10 vs before | no change | checkout-reached->order rate on 06-10..14 must be lower than 06-08..09 (95% CI of contrast excludes 0) | T2 | orders, sessions, deploys.log |
| H3 | causal | v3.3.9 (06-03) /product copy tweaks hurt | /product conversion in wk2 below wk1 | flat | /product conversion must drop between wk1 and wk2 (95% CI of contrast) | T3 | sessions |
| H4 | descriptive (estimand: device-mix-standardized conversion change) | Device mix shift (mobile/desktop) | standardized change much smaller than raw | same as raw | wk2 desktop/mobile mix must differ from wk1 | T4 | sessions |
| H5 | data-artifact | Orders/sessions logging gap in wk2 | order count per day deviates from checkout_reached count | they reconcile per day | per-day orders must differ from checkout_reached=yes count at some day x device cell | T5 | both |

Conversion definition assumption: conversion = orders / sessions (ties to 3.1%/2.5%; verified in T-def below).

## Sources
| id | Origin | Acquired | Coverage notes |
| S1 | sessions.csv (9171 rows, 06-01..06-14) | local | no blanks, unique ids |
| S2 | orders.csv (268 rows) | local | no blanks, unique ids; no session id link |
| S3 | deploys.log | local | 3 releases |

## Data Validity
- Collection method: unknown export; no contract.
- Coverage matrix: sessions by day x device and day x landing_page tabulated (orient.py). Wk1 600/day flat; wk2 760/day through 06-12, ~585 on 06-13/14 (mobile drops 440->242, desktop flat). Orders 17-23/day, no gaps.
- Field population: all fields 100% populated.
- Coverage baseline: none independent; unverifiable. 06-13/14 mobile drop is a coverage anomaly to flag.
- Source completeness semantics: S1: UNKNOWN — no export contract or independent counter discriminates unrecorded sessions from absent traffic.
S2: UNKNOWN — same.
- Sensitivity checks performed: see tests.

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| T1 | H1 | wk2 excl. summer-sale within wk1 95% CI | Wilson CI | CONSISTENT | wk1 3.12% (2.63-3.69); wk2 excl SS 3.04% (2.54-3.62); SS-only 0.57% (6/1053) (S1, an.py). Same-metric: checkout_reached/sessions |
| T2 | H2 | checkout->order rate lower after 06-10 | contrast CI | NON_DISCRIMINATING | orders have no session link; proxy used: session checkout rate 06-08/09 2.43% vs 06-10..14 2.55%, contrast +0.12pp (-0.82..+1.05); interval wide enough to contain the ~0.6pp effect predicted; orders/day flat after deploy (17-23). Only a proxy of the stated prediction |
| T3 | H3 | /product conv drops wk1->wk2 | contrast CI | CONTRADICTED | /product 3.93% -> 3.76%, contrast -0.17pp (-1.62..+1.28): interval contains 0 and the effect needed to explain the drop would have to be ~0.6pp+, inside it too -> reclassified NON_DISCRIMINATING per interval rule (amendment) |
| T4 | H4 | mix differs and standardization shrinks drop | direct standardization | NON_DISCRIMINATING | device mix differs only on 06-13/14 (artifact, see H5); desktop rate fell 3.36->2.22% but SS traffic is spread across both devices; not pursued further |
| T5 | H5 | per-day orders != checkout_reached | reconcile | CONSISTENT | orders=reached on 06-01..12; 06-13 orders 23 vs reached 17; 06-14 17 vs 11; mobile sessions 06-13/14 ~240 vs ~430 (home -105, product -55, SS -40ish) -> mobile sessions missing on 06-13/14 |

## Amendments
- 2026-11-08: T3 outcome set to NON_DISCRIMINATING (not CONTRADICTED) after reading its interval against the effect size needed; H3 stays UNRESOLVED.
- 2026-11-08: observed during analysis that the stated 2.5% equals checkout_reached/sessions (2.51%), while orders/sessions is 2.76%; the 137 vs 125 gap is the H5 artifact.

## Conclusion
- Answer: the drop is associated with a composition change: from 06-08 a new /lp/summer-sale landing page adds ~160 sessions/day that almost never reach checkout (6 of 1053, 0.57%). Excluding it, wk2 conversion is 3.04% vs 3.12% in wk1, a difference well inside noise. Not a checkout regression as far as this data can show.
- Best supported: H1 (retrospective, framed after the landing-page coverage view, so it needs evidence that didn't inform it; the 06-13/14 days were not separately held out, so this is exploratory support).
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 (retrospective) | descriptive | UNRESOLVED | best supported, T1 CONSISTENT; retrospective and not tested on held-out evidence |
  | H2 | causal | UNRESOLVED | T2 NON_DISCRIMINATING: orders cannot be linked to sessions, interval too wide to exclude a ~0.6pp effect |
  | H3 | causal | UNRESOLVED | T3 NON_DISCRIMINATING |
  | H4 | descriptive | UNRESOLVED | T4 NON_DISCRIMINATING |
  | H5 | data-artifact | UNRESOLVED | T5 CONSISTENT: mobile sessions missing on 06-13/14 (orders exceed checkout-reached by 6/day) |
- Limitations: no independent session denominator (S1/S2 UNKNOWN); week-2 sessions undercounted on 06-13/14, direction on the rate unknown beyond what the order reconciliation shows; causal claims unavailable (the landing page was launched, not randomized, and a v3.4.1 effect cannot be excluded); validator not run (instruments/check_record.py absent).
