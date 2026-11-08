# Investigation: why did weekly checkout conversion fall from 3.1% (wk 06-01) to 2.5% (wk 06-08)?

## Problem
- Decision informed: whether to roll back v3.4.1 or act on traffic/acquisition instead.
- Falsifiable question: what explains the drop in orders/sessions between 2026-06-01..07 and 2026-06-08..14 (UTC, per session)?
- Success criteria: answered means one or more explanations account for the drop and survive a discriminating test.
- Stop condition: conclude when no named unresolved alternative could reverse the rollback decision; else stop with limits.
- Effort budget: 12 tool calls.
Headless: no consultation pause. Only read-only local files; no gate issue. Assumption: no assignment mechanism is known, so nothing identifies a causal effect -> associative wording.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | The v3.4.1 checkout refactor (2026-06-10 14:00) caused the drop in conversion | per-day conversion falls at/after the deploy; within-segment rate falls | conversion already lower before the deploy | the lower conversion must not already be present before the 06-10 14:00 deploy (06-08..06-09 at the week-2 level) | T1 | sessions, orders, deploys |
| H2 | descriptive (estimand: week-2 conversion minus week-1 conversion attributable to landing-page x device mix, by reweighting week-1 segment rates to week-2 mix) | Traffic mix shifted toward lower-converting segments (e.g. /lp/summer-sale, new volume from 06-08) | reweighted week-1 rates at week-2 mix reproduce a large share of the drop | reweighting reproduces little | reweighting must reproduce at least ~50% of the 0.6pp drop | T2 | sessions by landing_page x device |
| H3 | data-artifact | Session/order records are mismatched (orders 268 vs 256 checkout sessions; mobile session counts drop 06-13/14) so the rate is mis-measured | mismatch/hole is large enough to move the weekly rate by ~0.6pp | drop robust to reconciliation | the weekly drop must vanish (<0.1pp) when holes/mismatch are corrected or excluded | T3 | sessions, orders |

## Sources
| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 sessions, 06-01..06-14) | 2026-11-08 | see matrix |
| S2 | orders.csv (268 orders, no session_id) | 2026-11-08 | cannot be joined to sessions |
| S3 | deploys.log (3 releases) | 2026-11-08 | v3.3.9 06-03, v3.4.1 06-10 14:00, v3.4.2 06-12 logging only |

## Data Validity
- Collection method: unknown; flat exports.
- Coverage matrix: (day x device sessions) wk1 ~262-273 desktop / 327-353 mobile per day; 06-08..06-12 desktop 320-370, mobile 390-440; 06-13/14 desktop ~345, mobile ~240 (drop ~45%). Orders/day ~17-23 every day, all days present. Orders carry client_version 3.4.0 through 06-09, 3.4.1 from 06-10.
- Field population: all fields populated (no blanks seen in the head; to be confirmed in T3).
- Coverage baseline: no schedule or independent denominator -> coverage unverifiable, not clean.
- Known instrument failures: none documented; v3.4.2 "logging only" release on 06-12.
- Source completeness semantics: S1: UNKNOWN — no export contract or independent counter discriminates unrecorded sessions from absent traffic. S2: UNKNOWN — same; no session key to reconcile.
- Sensitivity checks: bootstrap 95% CI around the weekly contrast, committed in advance.

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | week-2 conversion for 06-08..09 (pre-deploy) is not already at the lowered level | daily orders/sessions, pre vs post deploy | NON_DISCRIMINATING | S1,S2: orders/sessions 06-08 2.24%, 06-09 2.63% (wk1 days 2.83-3.50%) so the lowered level predates the deploy, but 06-08..09 is 1520 sessions / 37 orders and the 95% bootstrap interval around the weekly contrast (orders basis) is -1.06..+0.31pp, which includes both 0 and the predicted value; non-LP traffic pre-deploy 3.19% (51/1601) vs post-deploy 2.93% (68/2317), contrast CI -1.36..+0.86pp. Cannot refute or support. No confound/aggregation check across landing page beyond T2 |
| T2 | H2 | mix/new-segment accounting reproduces >=50% of drop | split by landing page (checkout_reached basis) | CONSISTENT | S1: wk1 3.12% (131/4200); wk2 non-LP traffic 3.04% (119/3918); /lp/summer-sale (new from 06-08, no wk1 counterpart) 0.57% (6/1053) = 26% of wk2 sessions; wk2 total 2.51% (125/4971). Adding LP sessions accounts for ~0.53 of the 0.61pp drop. Within existing pages the contrast is -0.08pp (CI -0.84..+0.68). Within-LP rate unchanged pre/post deploy (3/427 vs 3/626). Aggregation check: Simpson-type reversal not seen by page or device within existing pages except /product desktop 4.07%->2.84% (n small) |
| T3 | H3 | drop persists after excluding 06-13/14 and using checkout_reached | alt numerators/windows | NON_DISCRIMINATING | S1,S2: excluding 06-13/14 wk2 = 97/3800 = 2.55% (vs 3.12%), so the drop persists; but 06-13/14 is itself anomalous (sessions 760->587, mobile 440->242, orders 23/17 exceed checkout_reached 17/11; 12 more orders than checkout sessions in wk2, 0 in wk1) so the orders-based wk2 rate (2.76%) differs from the checkout-based 2.51%; coverage unverifiable (no baseline). The interval around the contrast (-1.06..+0.31pp orders basis) includes 0 |

## Amendments
(none)

## Conclusion
- Answer: associated with a new traffic source: `/lp/summer-sale` appears on 06-08 (1053 sessions, 26% of wk2 traffic) and converts at 0.57% (checkout_reached). Existing pages (/home, /product) converted 3.12% -> 3.04%, essentially flat. Arithmetically the new low-converting landing page accounts for ~0.5 of the 0.6pp fall. The drop starts 06-08, two days before the v3.4.1 deploy (06-10), and LP conversion didn't change across the deploy. The user's 3.1%/2.5% matches checkout_reached/sessions (3.12%/2.51%); orders/sessions gives 3.12%/2.76%.
- Best supported: H2 (T2 CONSISTENT, discriminating against H1: the shift appears before the deploy and in a segment that did not exist the week before). Associative: nothing assigned the landing page independently of visitors, and whether summer-sale visitors would have converted elsewhere is not identified.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 NON_DISCRIMINATING: the drop is already visible 06-08..09 pre-deploy, but with ~1500 sessions the interval includes zero and the predicted value; non-LP post-deploy 2.93% vs pre 3.19% is within noise. A modest checkout regression is not excluded (-0.26pp point estimate, CI -1.36..+0.86) |
  | H2 | descriptive | UNRESOLVED | best supported (T2 CONSISTENT: new /lp/summer-sale at 0.57% on 26% of sessions; existing pages flat) |
  | H3 | data-artifact | UNRESOLVED | T3 NON_DISCRIMINATING: drop persists excluding 06-13/14, but that period has a real session-logging anomaly and the orders/checkout counts disagree; coverage unverifiable |
- Limitations: week-over-week differences are statistically weak (orders-basis contrast CI -1.06..+0.31pp, ~130 orders/week); the 06-13/14 mobile session drop (-45%) and 12 orders with no checkout session are unexplained; orders cannot be joined to sessions; no assignment mechanism for the landing page; LP campaign details (spend, audience) unknown. Not causal. If a decision hangs on the unresolved set (rollback vs. not), `decision-analysis`/a longer window would be the continuation.
