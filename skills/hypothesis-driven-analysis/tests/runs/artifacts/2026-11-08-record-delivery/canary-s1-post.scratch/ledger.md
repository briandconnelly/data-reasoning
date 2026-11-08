# Investigation: Why did weekly checkout conversion fall from 3.1% (wk 2026-06-01) to 2.5% (wk 2026-06-08)?

## Problem

- Decision informed: whether to roll back / fix a release, or address traffic acquisition/instrumentation.
- Falsifiable question: what explains the change in sessions->order conversion between Mon 06-01..Sun 06-07 and Mon 06-08..Sun 06-14 (UTC, per-session)?
- Success criteria: answered means the gap is decomposed and each live explanation survives or fails a discriminating test.
- Stop condition: conclude when no named unresolved alternative could reverse the answer; otherwise stop with limits.
- Effort budget: 15 queries.

## Hypotheses

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | The v3.4.1 release (06-10, checkout form refactor) caused a step down in conversion | conversion on 06-10..14 below 06-08..09 | conversion already low on 06-08..09 | conversion on 06-10..14 must be lower than on the pre-release days 06-08..09 (a release cannot cause a drop that preceded it) | T1 | orders, sessions, deploys.log |
| H2 | descriptive (estimand: week-2 conversion re-weighted to week-1 landing_page x device mix, minus observed week-2 conversion) | Traffic composition shifted (more low-converting landing page/device sessions) so the aggregate fell without per-segment decline | mix-standardized week-2 rate is close to week-1 rate | standardized rate stays ~2.5% | week-2 mix must differ from week-1 mix toward a lower-converting segment | T2 | sessions, orders |
| H3 | data-artifact | The 06-13/14 mobile session shortfall (or order/session record mismatch) distorts the weekly rate | excluding affected days/segments moves week-2 rate materially | rate unchanged excluding them | week-2 rate computed excluding 06-13..14 must differ from the full-week rate by a material amount (>=0.2pp) | T3 | sessions, orders |

## Sources

| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 rows) | 2026-11-08 | 06-01..06-14; ~600/day wk1, ~760/day 06-08..12, 587/584 on 06-13/14 (mobile 242/238 vs ~400) |
| S2 | data/s1-conversion/orders.csv (268 rows) | 2026-11-08 | 06-01..06-14, 17-23/day; no session_id link; client_version 3.4.0 until 06-09, 3.4.1 from 06-10 |
| S3 | data/s1-conversion/deploys.log | 2026-11-08 | 3 releases: 06-03 v3.3.9, 06-10 v3.4.1, 06-12 v3.4.2 (logging only) |

## Data Validity

- Collection method: unknown beyond file contents; no export contract provided.
- Coverage matrix: sessions day x device inspected (orientation; see Sources S1). Day x landing_page and orders x segment to be tabulated in T2.
- Field population: all session fields populated; orders have no device/landing_page, so order-side segmentation is impossible; conversion by segment must use sessions.checkout_reached (a different quantity: reached checkout, not ordered).
- Coverage baseline: none independent; coverage unverifiable. Notable: S1 checkout_reached=yes count (256) != S2 order count (268) and v3.4.2 appears in log but not in order client_version.
- Known instrument failures: mobile sessions drop ~40% on 06-13/14 with desktop unchanged (unexplained).
- Source completeness semantics: S1: UNKNOWN — no export contract or independent count discriminates dropped from absent sessions. S2: UNKNOWN — no independent order count.
- Sensitivity checks performed: see tests.

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | conv(06-10..14) < conv(06-08..09) | daily and pre/post rates with Wilson/bootstrap CI on the contrast | CONTRADICTED | Conversion (checkout_reached/sessions, the metric matching 3.1%/2.5%) was 2.43% on pre-release 06-08..09 vs 2.55% on 06-10..14; the drop is already present before the release. Orders/sessions: 2.43% vs 2.90%. Release cannot cause a drop that preceded it. Per-day rates are noisy (2.2-3.0%) at ~17-23 events/day; confound check: LP launch coincides with 06-08 (S1). Scope: refutes the release as cause of the week-over-week drop only. adequacy: deterministic ordering prediction, zero rate (variants: any release effect size) |
| T2 | H2 | week-2 mix differs from week-1 toward lower-converting segment; standardized rate near week-1 | landing_page x device mix, segment rates, direct standardization | CONSISTENT | New landing page /lp/summer-sale first appears 06-08T08:00, 1053 sessions (21% of wk2), 6 checkout_reached (0.57%). Wk2 excluding it: 3.04% vs wk1 3.12% (diff -0.08pp, 95% CI -0.83..+0.67). Re-weighted to wk1 home/product x device mix: 3.06%. Aggregate diff incl. LP: -0.60pp, CI -1.29..+0.08 (includes 0). Segment-level: home/product cells show no consistent decline. S1 |
| T3 | H3 | excluding 06-13..14 changes wk2 rate >=0.2pp | recompute rates | CONTRADICTED | Wk2 excluding 06-13..14: 2.55% vs full 2.51% (0.04pp < 0.2pp). Note: mobile sessions fell ~40% on 06-13/14 while 12 more orders than checkout_reached rows exist on those days (orders 40 vs reach 28) — unexplained record inconsistency; S1,S2 |

## Amendments

- 2026-11-08: metric definition clarified from data, not hypothesis change: stated 3.1%/2.5% reproduce as checkout_reached/sessions (3.12%, 2.51%); orders/sessions gives 3.12% and 2.76%.

## Conclusion

- Answer: The drop is a traffic-mix effect: a new landing page /lp/summer-sale began receiving ~21% of week-2 sessions on 06-08 and converts to checkout at ~0.6%. Excluding it (or re-weighting to week-1 mix) the rate is ~3.0-3.1%, same as week 1. The release is not the cause: the drop is already present on 06-08/09 before v3.4.1 (06-10).
- Best supported: H2 (T2 discriminates it from H1 via timing and from H3 via the exclusion check). Associative only: the LP's sessions are additive traffic, not assigned; the 0.6% rate is conversion of that traffic, not a counterfactual effect of the LP on those users.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | REFUTED | necessary timing prediction failed under T1: drop precedes release |
  | H2 | descriptive | UNRESOLVED | best supported (T2 CONSISTENT); week-2 total diff CI includes 0 so the drop itself is statistically soft |
  | H3 | data-artifact | UNRESOLVED | T3 contradicts a material effect on the rate, but the mobile session shortfall on 06-13/14 and 12 orders with no checkout_reached record remain unexplained (no independent baseline) |
- Limitations: orders.csv has no session link, so order-side segmentation is impossible; segment rates use checkout_reached. Event counts are small (~130-250), so CIs are wide: -0.6pp total change is not distinguishable from noise at 95%. Mobile gap on 06-13/14 is unexplained. Source completeness UNKNOWN for S1 and S2. Whether the LP campaign is worth its low conversion (e.g. cost per order, or whether it displaced organic traffic) is outside this data; decision-analysis could take that up.
