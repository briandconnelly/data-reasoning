# Investigation: How much did launching /lp/summer-sale improve checkout conversion?

## Problem
- Decision informed: whether to credit/continue the campaign for a conversion gain.
- Falsifiable question: did site-wide session->checkout_reached rate rise because of the campaign launch (first seen 2026-06-08) in sessions 2026-06-01..06-14? Unit: session.
- Assumption (headless, cannot ask): launch was not randomized; nothing identifies the effect, so a causal number is not expected. "Checkout conversion" = checkout_reached=yes / sessions (orders.csv has no session key; used only as secondary).
- Success criteria: answered means either an identified, interval-bounded effect, or a demonstration that it is not identifiable plus the descriptive quantities that are available.
- Stop condition: conclude after T1-T5 run; iterate only if a specific test could change the answer.
- Effort budget: 12 tool calls.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | The campaign launch caused higher checkout rate among sessions | non-lp (home/product) rate or overall rate rises after 06-08 and/or lp sessions convert above pre-period baseline | no rise | overall checkout rate in 06-08..06-09 (before any other release) must be above 06-01..06-07 rate | T1 | sessions |
| H2 | causal | The v3.4.1 checkout-form refactor (06-10) changed checkout rate on all pages | step in /home and /product rate at 06-10 | no step at 06-10 | /home+/product rate must differ between 06-08..09 and 06-10..12 | T2 | sessions, deploys |
| H3 | descriptive (estimand: checkout rate of lp sessions minus non-lp sessions, 06-08..06-12, standardized by device) | Campaign traffic is simply a different mix (landing page/device) so aggregate change is composition, not effect | lp sessions' rate differs from non-lp; device mix explains aggregate | lp rate equals non-lp | lp-vs-non-lp rate difference must be nonzero after device standardization | T3 | sessions |
| H4 | data-artifact | Mobile session logging is incomplete on 06-13/14 (mobile sessions down ~45% on every page), distorting late-period rates | mobile checkout rate/composition shift on 06-13/14 is not mirrored in desktop | desktop and mobile move together | rate in 06-13/14 must differ from 06-08..12 for mobile only if rows were dropped selectively | T4 | sessions |

Sensitivity: 95% bootstrap/Wilson intervals around each contrast, committed now. Null counts as evidence only if the interval excludes the predicted value.

## Sources
| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 rows) | 2026-11-08 | 06-01..06-14, no nulls, unique ids |
| S2 | data/s1-conversion/orders.csv (268 rows) | 2026-11-08 | no session key; client_version field |
| S3 | data/s1-conversion/deploys.log | 2026-11-08 | 3 releases; no campaign entry |

## Data Validity
- Collection method: unknown beyond file contents.
- Coverage matrix: (day x page x device counts, inspected) lp absent before 06-08 (160/day after). Mobile sessions fall from ~90-110 to ~55-65 per page on 06-13 and 06-14 on every page, hourly 08-16 on 06-13 about 20% below 06-12 total; desktop stable. Pre-period is only 7 days, no prior-year seasonality.
- Field population: all fields 100% populated.
- Coverage baseline: none independent (no traffic counter) -> coverage unverifiable, not clean.
- Known instrument failures: none documented; 06-13/14 mobile drop unexplained.
- Source completeness semantics:
S1: UNKNOWN — no export contract or independent counter distinguishes a real mobile traffic drop from missing rows; the file's own pattern cannot.
S2: UNKNOWN — no key to sessions, so absent orders cannot be reconciled to sessions.
- Sensitivity checks performed: see Tests.

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | overall rate 06-08..09 > 06-01..07 | rate and diff CI | CONTRADICTED | overall 3.12% -> 2.43%, diff -0.68pp, 95% bootstrap CI [-1.60,+0.22]; non-lp 3.12% -> 3.00% CI [-1.23,+1.01]; 06-08..12 diff -0.57pp CI [-1.33,+0.16] (S1, analysis.py). Contrast is unidentified (launch not randomized, no concurrent control), so it cannot refute a causal claim |
| T2 | H2 | /home+/product rate differs 06-08..09 vs 06-10..12 | diff CI | NON_DISCRIMINATING | 3.00% -> 3.17%, diff +0.17pp CI [-1.11,+1.47] contains 0 and effects up to ~1.3pp; pre vs post-refactor +0.05pp CI [-0.88,+1.05] (S1,S3). Detection limit ~1pp on a ~3% base |
| T3 | H3 | lp minus non-lp differs from 0, device-standardized | diff CI, stratified by device | CONSISTENT | lp 0.50% (n=800) vs non-lp 3.10% (n=3000), diff -2.60pp CI [-3.37,-1.72]; desktop -2.84pp CI [-3.78,-2.04], mobile -2.40pp CI [-3.58,-1.08] (S1). Descriptive, not causal |
| T4 | H4 | mobile and desktop rates diverge on 06-13/14 vs 06-08..12 | diff-in-diff CI | NON_DISCRIMINATING | desktop -0.07pp CI [-1.31,+1.26]; mobile -0.10pp CI [-1.61,+1.55] (S1). Rates unchanged but a selective-drop artifact of ~1.5pp is undetectable; no independent counter to confirm coverage |

## Amendments
(none)

## Conclusion
- Answer: the data cannot tell us how much the campaign improved checkout conversion; no causal number is available (launch not randomized, no concurrent control, 06-10 checkout release and only 7 pre-days). What is observable: overall session->checkout rate was 3.12% before launch and 2.55% over 06-08..12 (diff -0.57pp, 95% CI [-1.33,+0.16]), i.e. no evidence of improvement. Non-campaign pages stayed at ~3.1%. Campaign-page sessions converted at 0.50% (4 of 800) vs 3.10% on other pages (diff -2.6pp, CI [-3.4,-1.7]), so the campaign added low-converting traffic and, if anything, diluted the aggregate rate. Associated, not caused.
- Best supported: H3 (descriptive), via T3.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 went against it but the contrast is unidentified, so cannot refute; no sign of lift |
  | H2 | causal | UNRESOLVED | T2 NON_DISCRIMINATING, cannot detect shifts below ~1pp |
  | H3 | descriptive | UNRESOLVED | best supported (T3 CONSISTENT) |
  | H4 | data-artifact | UNRESOLVED | T4 NON_DISCRIMINATING; coverage unverifiable |
- Limitations: orders.csv cannot be joined to sessions (orders 268 vs 256 checkout sessions, unreconciled), so order conversion and revenue are unassessed; 7 pre-days only; mobile session drop on 06-13/14 unexplained; lp sessions may be incremental traffic with no counterfactual on lp visitors' alternative behavior (displacement from /home unseen: /home and /product volumes were flat). Continuation: causal-identification-review (if installed) for a design (e.g. holdout or staggered launch) that would identify the effect.

