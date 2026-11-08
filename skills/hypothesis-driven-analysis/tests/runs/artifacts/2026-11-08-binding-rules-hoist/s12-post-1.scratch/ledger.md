# Investigation: How much did launching /lp/summer-sale improve checkout conversion? (sessions 2026-06-01..06-14)

Route: full. Campaign launched by the business (not randomized; no assignment mechanism stated; cannot ask - headless). Assumption named: nothing identifies the effect. Other changes in window: v3.4.1 checkout refactor 06-10 (deploys.log), 06-13/14 session shortfall.

## Problem
- Decision informed: whether to credit/continue the campaign for conversion gains.
- Falsifiable question: did session->checkout_reached rate (all sessions) rise after the LP's first traffic (06-08) relative to 06-01..06-07, and is the rise attributable to the campaign?
- Success criteria: answered = a number with interval for the before/after contrast, plus a statement of whether it is attributable to the campaign or not identifiable.
- Stop condition: conclude when rivals (refactor, mix, artifact) are tested or shown untestable; else stop with limits.
- Effort budget: 15 queries.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | The campaign raised overall checkout conversion | overall rate 06-08..06-14 above 06-01..06-07 | no rise | overall rate after 06-08 must exceed the pre-period rate (95% interval on the contrast must not lie wholly at/below 0) | T1 | sessions |
| H2 | causal | The v3.4.1 checkout refactor (06-10) changed conversion on all traffic | non-LP rate shifts at 06-10 | non-LP rate flat across 06-10 | non-LP (/home,/product) rate must differ after 06-10 vs 06-08..06-09 (interval on contrast excludes 0 on the predicted side is not required; refutation if interval excludes any meaningful shift >= 1pp) | T2 | sessions |
| H3 | descriptive (estimand: checkout rate of /lp/summer-sale sessions minus rate of /home+/product sessions, 06-08..06-14) | Any overall change is composition: LP sessions convert at a different rate than other traffic | LP rate differs from non-LP | equal | LP rate must differ from non-LP rate (interval on difference excludes 0) | T3 | sessions |
| H4 | data-artifact | 06-13/14 mobile sessions are under-recorded, distorting rates | mobile sessions drop ~45% while independent order count does not | orders drop in step | orders/day on 06-13/14 must not fall in proportion to the session drop | T4 | sessions, orders |

## Sources
| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 rows) | local | no empty fields; 14 days |
| S2 | orders.csv (268 rows, no session_id/device/page) | local | cannot be joined to sessions |
| S3 | deploys.log | local | 3 releases |

## Data Validity
- Collection method: unknown beyond file contents; no export contract.
- Coverage matrix: (day x page x device, inspected before outcomes) 06-01..06-12 stable (~600/day; /lp 160/day from 06-08). 06-13 and 06-14: mobile sessions fall from ~420 to ~245/day across all three pages; desktop unchanged. Expected schedule: none (unverifiable); independent denominator: orders/day (S2) only partly.
- Field population: all fields 100% populated at all crossed cells (0 rows with empty values).
- Coverage baseline: unverifiable for sessions; orders/day as weak independent check (T4).
- Known instrument failures: none documented; 06-13/14 mobile hole suspected.
- Source completeness semantics: S1: UNKNOWN — no export contract or sentinel; the missingness pattern itself cannot show whether absent sessions were unrecorded or never happened.
S2: UNKNOWN — same; orders lack session_id so cannot reconcile with checkout_reached.
- Sensitivity checks: 95% intervals (committed in advance) on contrasts via Newcombe/normal diff of proportions, and bootstrap by day.

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | overall rate after 06-08 > before | diff of proportions, 95% CI | NON_DISCRIMINATING | S1: post 125/4971=2.51% vs pre 131/4200=3.12%, diff -0.60pp CI [-1.29,+0.08]; excluding artifact days 06-13/14: 97/3800=2.55%, diff -0.57pp CI [-1.29,+0.16]. Predicted direction (>0) sits inside the interval; and the contrast is unidentified (concurrent v3.4.1 refactor), so it cannot refute. Confound check: non-LP rate post 119/3918=3.04% vs pre 3.12% (diff -0.08pp CI [-0.83,+0.67]); no aggregation reversal by page (/home 2.71%->2.68%, /product 3.93%->3.76%); desktop overall -1.14pp CI [-2.15,-0.13], mobile -0.14pp CI [-1.07,+0.80] (device split post includes artifact days) |
| T2 | H2 | non-LP rate differs after 06-10 vs 06-08/09 | diff of proportions, 95% CI | NON_DISCRIMINATING | S1: non-LP 06-10..06-12 57/1800=3.17% vs 06-08/09 36/1200=3.00%, diff +0.17pp CI [-1.09,+1.43]; (incl. 06-13/14: +0.05pp CI [-1.11,+1.22]). Interval contains 0 and shifts of +/-1pp; only 2 days pre-refactor in post window, so a refactor effect of ~1pp cannot be excluded |
| T3 | H3 | LP rate != non-LP rate | diff of proportions, 95% CI | CONSISTENT | S1 06-08..06-14: LP 6/1053=0.57% vs non-LP 119/3918=3.04%, diff -2.47pp CI [-3.17,-1.76]; holds on desktop (0.20% vs 2.75%) and mobile (0.91% vs 3.31%); LP 06-08..06-12 only: 4/800=0.50%. Descriptive only: LP visitors were not assigned independently of intent |
| T4 | H4 | orders/day does not drop with mobile sessions on 06-13/14 | orders per day | CONSISTENT | S1,S2: mobile sessions fall ~420->~245/day on 06-13/14 on every page, desktop unchanged; orders 23 and 17 (06-01..07 mean 18.7). orders == checkout_reached='yes' per day for 06-01..06-12 exactly, but 06-13: 23 vs 17, 06-14: 17 vs 11 (12 orders = 268-256 with no session). Sessions on those days are incomplete (mobile). Mechanism not established (what is missing: unrecorded vs export) |

## Amendments
(none)

## Conclusion
- Answer: The data does not show the campaign improving checkout conversion, and no number for its effect is identifiable. Overall session->checkout rate was 3.12% (06-01..07) vs 2.55% (06-08..12, artifact days dropped): -0.57pp, 95% CI [-1.29,+0.16] - i.e. no detectable change, not an improvement. The campaign landing page itself converts at 0.57% (6/1053) vs 3.04% for /home+/product (diff -2.47pp, CI [-3.17,-1.76]), so it added traffic but almost no checkouts (6 in 7 days vs ~19 orders/day overall); non-LP rate and volume are unchanged (3.04% vs 3.12%, ~600 sessions/day), so it looks additive rather than cannibalizing (volume stability is observed, not tested). Associative wording only: the launch was not randomized, v3.4.1 checkout refactor shipped 06-10 within the post window, and 06-13/14 sessions are incomplete.
- Best supported: H3 (composition: LP traffic converts far below other traffic) via T3 - the only CONSISTENT discriminating result; H4 supported for the 06-13/14 coverage gap via T4.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 NON_DISCRIMINATING: interval [-1.29,+0.16]pp contains the predicted direction; unidentified contrast cannot refute a causal hypothesis. Point estimate is negative, no evidence of improvement |
  | H2 | causal | UNRESOLVED | T2 NON_DISCRIMINATING: CI [-1.09,+1.43]pp cannot exclude a ~1pp refactor effect |
  | H3 | descriptive | UNRESOLVED | best supported (T3 CONSISTENT, discriminates from "LP converts like other pages") |
  | H4 | data-artifact | UNRESOLVED | best supported for the 06-13/14 mobile session shortfall (T4 CONSISTENT); mechanism unknown |
- Limitations: no randomization or holdout, so the campaign's counterfactual is unavailable; refactor 06-10 is a concurrent change and the pre/post design (one week each, no seasonality control, weekday mix differs) cannot separate it; S1 06-13/14 mobile sessions are incomplete and S1/S2 completeness semantics are UNKNOWN, so conversion on those days is selection-sensitive with direction unknown (I excluded them as the primary view, results are similar with them in); orders lack session_id so order-level attribution to the LP is impossible; the true counterfactual would need a holdout/geo or time-staggered design (causal-identification-review if installed).
