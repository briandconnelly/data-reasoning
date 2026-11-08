# Investigation: why did weekly checkout conversion fall from 3.1% (wk 2026-06-01) to 2.5% (wk 2026-06-08)?

## Problem

- Decision informed: whether to roll back v3.4.1 / pull the summer-sale landing campaign / fix instrumentation.
- Falsifiable question: which of the candidate explanations account for the drop in orders/sessions (all sessions, 06-01..06-07 vs 06-08..06-14, UTC)?
- Success criteria: answered means each hypothesis has a derived status from an adequate discriminating test and the drop is decomposed into attributed vs unattributed parts.
- Stop condition: conclude when no unresolved alternative could reverse the answer; else stop with limits.
- Effort budget: 15 tool calls.
- Assignment note: nothing randomized; deploys/campaign shipped to everyone, so wording is associative.

## Hypotheses

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | descriptive (estimand: order-per-session rate of /lp/summer-sale sessions minus that of other sessions in wk2, and the mix-standardized wk2-wk1 change) | Landing-page mix shift: the new /lp/summer-sale traffic (present from 06-08) converts poorly and dilutes the aggregate | summer-sale sessions convert below others; holding mix at wk1 weights removes most of the drop | summer-sale converts at or above others; standardizing leaves the drop | checkout_reached rate of summer-sale sessions in wk2 is below that of non-summer-sale sessions in wk2 (interval on the contrast excludes 0) | T1 | sessions.csv |
| H2 | causal | v3.4.1 checkout refactor (deployed 2026-06-10 14:00Z) lowered checkout completion | checkout-to-order rate falls after deploy, not before | fall predates deploy or none | the drop in orders per checkout_reached must not begin before 06-10 14:00Z (a deploy cannot cause earlier change) | T2 | orders, sessions, deploys.log |
| H3 | data-artifact | Session logging shortfall on 06-13/14 (mobile sessions ~240 vs ~430 typical) distorts the wk2 rate | excluding 06-13/14 (or recomputing on complete days) removes the drop | drop persists on complete days | wk2 conversion on days 06-08..06-12 only must be materially closer to wk1 rate than the full wk2 | T3 | sessions, orders |
| H4 | descriptive (estimand: device-standardized wk2-wk1 change in orders/session) | Device mix shift (desktop share rose) rather than any within-segment change | conversion differs by device and standardizing by device removes the drop | standardizing leaves the drop | desktop and mobile conversion rates must differ in wk1 | T4 | sessions, orders have no device -> use checkout_reached |

## Sources

| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 rows, 06-01..06-14) | 2026-11-08 | no nulls, unique ids; summer-sale page absent before 06-08; 06-13/14 total sessions 587/day vs ~760 on 06-08..12, mobile 240 vs ~420 |
| S2 | orders.csv (268 rows) | 2026-11-08 | no nulls; no session_id so orders cannot be joined to sessions/device/landing page; client_version 3.4.0 through 06-09, 3.4.1 from 06-10 (whole day, incl. before 14:00 release?) |
| S3 | deploys.log (3 lines: v3.3.9 06-03, v3.4.1 06-10 14:00Z, v3.4.2 06-12) | 2026-11-08 | log has no v3.4.0 entry |

## Data Validity

- Collection method: unknown export; sessions flagged checkout_reached; orders separate with no join key.
- Coverage matrix: day x device and day x landing_page counted (orientation). Hole: 06-13/14 mobile ~-43%, with every landing page ~-22%; summer-sale appears 06-08 at 160/day. Orders by day x client_version counted.
- Field population: all fields 100% populated.
- Coverage baseline: none independent (no traffic counter) -> expected schedule is a constant ~600 sessions/day wk1; wk2 baseline unverifiable.
- Known instrument failures: none documented.
- Source completeness semantics:
S1: UNKNOWN — no export contract or independent counter distinguishes unrecorded sessions from fewer sessions on 06-13/14.
S2: UNKNOWN — no independent order count; orders cannot be reconciled to checkout_reached (256 yes vs 268 orders).
- Sensitivity checks performed: bootstrap 95% intervals (committed 95%) on contrasts, below.

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | summer-sale checkout_reached rate < non-summer-sale rate in wk2 | 2-prop contrast, bootstrap 95% CI on the contrast | CONSISTENT | S1: summer-sale 0.57% (n=1053) vs /home 2.68%, /product 3.76%; contrast vs other pages -2.47pp, 95% CI [-3.16,-1.74]. Mix check: wk1 page weights applied to wk2 within-page rates give 3.04% vs wk1 3.12% (residual -0.08pp, CI [-0.85,0.69]), so mix accounts for ~87% of the -0.60pp point change. Aggregation check: /home and /product are individually flat (2.71->2.68, 3.93->3.76); summer-sale is additive traffic (/home and /product daily counts unchanged), no reversal |
| T2 | H2 | aggregate drop must not begin before 06-10 14:00Z | non-summer sessions wk2 pre- vs post-deploy; aggregate daily rates | NON_DISCRIMINATING | S1,S3: non-summer pre 3.19% (n=1601) vs post 2.93% (n=2317), contrast -0.26pp CI [-1.33,0.87]; post-deploy minus wk1 CI [-1.0,0.73]. A deploy effect of the size of the whole drop (-0.6pp) lies inside the interval; detection limit ~+/-1pp. Side observation (not preregistered): orders == checkout_reached per day through 06-12 (ratio 1.0), orders cannot be joined to sessions (S2) |
| T3 | H3 | wk2 rate on 06-08..06-12 closer to wk1 than full wk2 | recompute on complete days, CI on contrast to wk1 | NON_DISCRIMINATING | S1: complete days 2.55% vs full wk2 2.51% (moves 0.04pp) vs wk1 3.12%; (complete - wk1) CI [-1.30,0.17] includes 0. 06-13/14 show orders (40) > checkout_reached (28): checkout_reached is inconsistent with orders on those days; orders-based wk2 rate would be 2.76% (S2). Upper bound the hole could matter ~0.25pp |
| T4 | H4 | desktop and mobile conversion differ in wk1 | wk1 device contrast, bootstrap CI | NON_DISCRIMINATING | S1: wk1 desktop 3.36% vs mobile 2.93%, diff +0.43pp CI [-0.64,1.53]; device-standardized wk2 = 2.54% (residual -0.58pp), i.e. device mix explains ~3% of point change. Device is confounded with landing page (summer-sale 48% desktop / 52% mobile) |

## Amendments

- 2026-11-08: the user's 3.1%->2.5% reproduces as the checkout_reached rate (3.12% -> 2.51%), not orders/sessions (3.12% -> 2.76%); analysis uses checkout_reached as the primary conversion, and orders-based figure is reported as a sensitivity. Orientation finding, not a hypothesis change.

## Conclusion

- Answer: the drop is associated with a new low-converting landing page, /lp/summer-sale, that starts sending ~160 sessions/day on 2026-06-08; its sessions reach checkout at 0.57% vs ~3% elsewhere, and re-weighting to wk1 page mix recovers 3.04% of the 3.12%. Page-mix is a composition effect, not evidence that anything broke. The headline -0.60pp itself has a 95% CI of [-1.29,+0.11], so it is borderline distinguishable from noise.
- Best supported: H1 (T1 CONSISTENT, discriminating against the device-mix rival H4 whose standardization leaves the drop, and unrefuted rivals H2/H3 remain unresolved but have small or untested contributions).
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | descriptive | UNRESOLVED | best supported: T1 CONSISTENT with an interval excluding 0 and mix standardization reproducing ~87% of the change; descriptive only, not a causal claim about the campaign |
  | H2 | causal | UNRESOLVED | T2 NON_DISCRIMINATING: interval [-1.33,0.87] cannot exclude a deploy effect; non-summer traffic shows no significant change after the deploy |
  | H3 | data-artifact | UNRESOLVED | T3 NON_DISCRIMINATING; 06-13/14 orders exceed checkout_reached so the artifact is real but bounded to ~0.25pp |
  | H4 | descriptive | UNRESOLVED | T4 NON_DISCRIMINATING; standardization leaves the drop, so device mix is not a leading explanation |

- Limitations: associative only: nothing randomized, campaign and deploy shipped to all; S1/S2 completeness UNKNOWN (no independent traffic counter; the 06-13/14 session shortfall, esp. mobile, cannot be classified as real traffic drop or lost logging, direction unknown); orders have no session key so order-level analysis by page is impossible; v3.4.1 orders appear from 06-10 08:40, before the 14:00 deploy log time, an unexplained discrepancy; ~13% of the change is unattributed; a small deploy effect (<~1pp) cannot be excluded. Whether to keep summer-sale traffic is a decision on cost per order, not on the conversion rate.
