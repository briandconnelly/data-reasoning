# Investigation: why did weekly conversion fall from 3.1% (wk 2026-06-01) to 2.5% (wk 2026-06-08)?

## Problem
- Decision informed: whether to roll back the v3.4.1 checkout refactor, or look at the new traffic source instead.
- Falsifiable question: which of (traffic-mix change, deploy regression, device mix, data artifact) account for the change in orders/sessions between 06-01..06-07 and 06-08..06-14 (UTC, per-session)?
- Success criteria: answered means the drop is decomposed into parts attributable to tested explanations, with a residual reported as unattributed if untested.
- Stop condition: conclude when the decomposition and the deploy-timing test are done; stop with limits otherwise.
- Effort budget: 12 queries.
- Assumption (headless, not asked): conversion = orders / sessions (orders have no session id, so no session-level join). Expected to reproduce 3.1% / 2.5%; check first.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | descriptive (estimand: change in overall checkout-reach rate explained by landing-page mix shift, mix-standardized to week-1 shares) | New landing page /lp/summer-sale (first appears 06-08) brings traffic that converts below the others, diluting the rate | /lp/summer-sale reach rate is below the rate of other pages; standardizing to week-1 mix removes a material share of the drop | summer-sale rate >= other pages, standardized drop ~ raw drop | summer-sale checkout-reach rate must be below week-1 overall rate | T1 | sessions |
| H2 | causal | v3.4.1 deploy (06-10 14:00) broke checkout, lowering conversion | within wk2, conversion on non-summer-sale pages falls after the deploy vs before it | no step at deploy | non-summer-sale conversion after 06-10 14:00 must be lower than non-summer-sale conversion 06-08 to 06-10 14:00 (a deploy cannot cause a drop that precedes it) | T2 | sessions, orders, deploys.log |
| H3 | descriptive (estimand: change in overall rate explained by device mix, standardized to week-1 device shares) | Mobile/desktop mix shifted toward lower-converting device | device-standardized drop much smaller than raw | standardized ~ raw | device-specific rates must differ between devices in week 1 | T3 | sessions |
| H4 | data-artifact | Week-2 records are incomplete or mis-tagged (sessions or orders under-recorded, e.g. 06-13/14 mobile session counts dip) so the ratio is distorted | an hour x device x page cell is missing or orders/day dips against sessions | uniform coverage | per-day orders must not be proportionally lower than checkout_reached sessions; the 06-13/14 dip is real in a coverage matrix | T4 | sessions, orders |

## Sources
| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 rows) | 2026-11-08 | 06-01 08:00Z to 06-14 16:56Z; 08:00-16:59 each day |
| S2 | data/s1-conversion/orders.csv (268 rows) | 2026-11-08 | order_id unique; client_version 3.4.0 through 06-09, 3.4.1 from 06-10; no session id |
| S3 | data/s1-conversion/deploys.log (3 lines) | 2026-11-08 | v3.3.9 06-03, v3.4.1 06-10 14:00, v3.4.2 06-12 logging only |

## Data Validity
- Collection method: unknown; flat CSV exports, no documentation.
- Coverage matrix: sessions day x device and day x landing page inspected. Wk1: 600/day, 400 /home + 200 /product, 0 summer-sale. 06-08..06-12: 760/day, 400 /home + 160 summer-sale + 200 /product. 06-13/14: 587 and 584 (all pages ~22% lower, mobile 330->~240; desktop flat) - unexplained hole, tested in T4. Hour-of-day coverage is flat (~1000-1040 per hour).
- Field population: all fields populated in the file headers; checkout_reached yes/no only.
- Coverage baseline: no independent denominator -> coverage unverifiable, not clean.
- Known instrument failures: none documented.
- Source completeness semantics:
S1: UNKNOWN - no export contract or independent counter; its own missingness cannot discriminate unrecorded sessions from absent traffic.
S2: UNKNOWN - same; orders have no join key to sessions.
- Sensitivity checks performed: see Tests (bootstrap 95% intervals on the contrast, committed at 95% before reading).

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | summer-sale reach rate < week-1 overall rate; mix-standardized drop smaller than raw | rates by page, standardization, session bootstrap 95% CI | CONSISTENT | S1: summer-sale 0.57% (n=1053) vs wk1 overall 3.12%; wk2 /home 2.68%, /product 3.76% (wk1 2.71%, 3.93%). Standardized to wk1 page mix wk2 = 3.04% vs raw 2.51%: raw drop 0.61pp, standardized drop 0.08pp (~87% of the drop is mix). Wk2 non-summer-sale 3.04% vs wk1 3.12%, 95% CI on contrast (-0.83, +0.72)pp. Same pattern within device (desktop SS 0.2%, mobile SS 0.9%) |
| T2 | H2 | non-summer-sale conversion after 06-10 14:00 < before | split wk2 at deploy; non-summer-sale checkout_reached (orders have no page); 95% bootstrap CI on contrast | NON_DISCRIMINATING | S1,S3: pre 3.19% (n=1601) vs post 3.00% (n=1399), diff -0.18pp, 95% CI (-1.42, +1.09)pp; the interval contains 0 and the whole-week drop size, so detection limit ~1.3pp. Point sign matches the prediction but the data cannot separate it from no effect. Also: daily rate was already 2.24% on 06-08 and 2.63% on 06-09, before the deploy. Orders/session 2.66% pre vs 2.43% post (n=54/43 orders), same limit |
| T3 | H3 | device rates differ in wk1 and standardization shrinks drop | rates by device | CONTRADICTED | S1: wk1 desktop 3.36%, mobile 2.93%; device-standardized wk2 = 2.54% vs raw 2.51%, so device mix explains ~0 of the drop. Necessary prediction (device rates differ in wk1) held; the explanatory prediction (shrinks drop) failed - non-necessary, so no refutation |
| T4 | H4 | order/day vs checkout_reached/day ratio stable; 06-13/14 dip inspected | daily ratios | CONSISTENT | S1,S2: orders = checkout_reached exactly 06-01..06-12 (every day). 06-13: 23 orders vs 17 reached; 06-14: 17 vs 11. Mobile sessions fell from ~440 to 242/238 while desktop stayed flat. Consistent with under-recorded mobile sessions on 06-13/14. Effect on the weekly figure small: wk2 06-08..12 only = 2.55% vs 2.51% full week |

## Amendments
- 2026-11-08: no new hypotheses or data. Noted after T4: the user's 2.5% equals checkout_reached/sessions (2.51%); orders/sessions is 2.76% for wk2 (3.12% wk1, both definitions) because orders on 06-13/14 exceed reached sessions. Both reported.

## Conclusion
- Answer: about 87% of the drop is a landing-page mix change, not a checkout regression. A new /lp/summer-sale page started taking ~21% of sessions on 2026-06-08 and reaches checkout at 0.57% against ~3% elsewhere. Holding the page mix at week-1 shares, week 2 is 3.04% against 3.12%. This is a descriptive decomposition, not a causal effect. The v3.4.1 deploy cannot be excluded as a small contributor (T2 non-discriminating), but the drop started on 06-08, two days before it.
- Best supported: H1, via T1 (discriminating: standardization removes ~87% of the drop, and non-summer-sale rates are flat). H3 does not explain it.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | descriptive | UNRESOLVED | best supported (T1 CONSISTENT); rests on landing page not being downstream of the exposure and on summer-sale sessions being incremental |
  | H2 | causal | UNRESOLVED | T2 NON_DISCRIMINATING: -0.18pp, CI (-1.42,+1.09)pp, cannot separate a ~1pp effect from none; the unidentified pre/post contrast could not refute it anyway; drop onset 06-08 precedes the deploy |
  | H3 | descriptive | UNRESOLVED | T3 CONTRADICTED on a non-necessary prediction: device-standardized drop 0.61pp vs raw 0.61pp; contributes ~nothing |
  | H4 | data-artifact | UNRESOLVED | T4 CONSISTENT for a mobile session under-recording on 06-13/14 (orders exceed reached sessions); no independent denominator, so completeness stays UNKNOWN; excluding those days moves wk2 by 0.04pp |
- Limitations: no session-order join, so orders cannot be attributed to pages or versions; the summer-sale effect on other pages (cannibalization) is not testable here; the quality of summer-sale traffic is not assessed (a campaign-quality question); S1 and S2 completeness is UNKNOWN, direction of any 06-13/14 session loss unknown; the deploy test has a detection limit ~1.3pp; all claims are associative, since nothing independent assigned the landing page or the version. Next step if a decision on rolling back is needed: causal-identification-review (not run here) or a holdout of v3.4.1.
