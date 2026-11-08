# Investigation: How much did launching /lp/summer-sale improve checkout conversion? (2026-06-01..06-14)

Route: full. Assignment of the campaign = someone launched it (first /lp/summer-sale sessions 06-08); not randomized; v3.4.1 checkout refactor deployed 06-10. Assumption named: nothing identifies the effect.

## Problem
- Decision informed: whether to credit/continue the campaign for conversion gains.
- Falsifiable question: did site checkout conversion (checkout_reached=yes / sessions) rise because of the campaign, and by how much, 06-01..06-14?
- Success criteria: answered means a causal magnitude is either supported by an identified contrast, or shown unavailable with what the data does support.
- Stop condition: conclude after T1-T4; stop with limits if no contrast is identified.
- Effort budget: 12 queries.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | The summer-sale launch raised checkout conversion | overall conversion rises after 06-08 launch, before 06-10 deploy | no rise 06-08..06-09 vs 06-01..07 | overall conversion 06-08..09 must exceed 06-01..07 (95% CI of difference excludes <=0 side) | T1 | sessions |
| H2 | causal | The 06-10 v3.4.1 checkout refactor changed conversion | step at/after 06-10 on all landing pages incl. non-campaign | step precedes 06-10 or only on campaign page | no conversion change on /home,/product after 06-10 would mean refuted: change on non-campaign pages must appear | T2 | sessions |
| H3 | descriptive (estimand: conversion rate by device and landing page, and device mix, per period) | Conversion moved via mix shift (device/page) not component rates | pooled change is reproduced by reweighting fixed-period rates | within-stratum rates move equally | device mix must differ between periods | T3 | sessions |
| H4 | data-artifact | 06-13/14 volume shortfall (sessions ~22% lower on all pages) distorts comparisons | shortfall coincides with conversion shift | no | shortfall must be present in sessions but not orders | T4 | sessions, orders |

## Sources
| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 rows) | 2026-11-08 | landing_page, device, checkout_reached; no user id, no assignment flag |
| S2 | data/s1-conversion/orders.csv (268 rows) | 2026-11-08 | client_version; not joinable to sessions |
| S3 | data/s1-conversion/deploys.log | 2026-11-08 | 3 releases |

## Data Validity
- Collection method: unknown; flat exports.
- Coverage matrix: day x landing page counts: /home and /product 400/200 per day 06-01..12, 311/149 (06-13), 304/154 (06-14); summer-sale 0 before 06-08, 160/day 06-08..12, 127,126 on 06-13/14. Day x device: mobile 330-350 pre; 390-440 06-08..12; ~240 on 06-13/14. Orientation only; no outcome inspected.
- Field population: all fields populated (to be confirmed in T-queries).
- Coverage baseline: none independent; unverifiable.
- Known instrument failures: 06-13/14 mobile session drop of ~100/day (all pages) unexplained.
- Source completeness semantics:
S1: UNKNOWN — no export contract or independent counter; the 06-13/14 shortfall cannot be classed as real traffic vs export loss.
S2: UNKNOWN — same; orders (268) exceed checkout_reached=yes (256) so the sources don't reconcile.
- Sensitivity checks: bootstrap/Newcombe 95% CI on rate differences.

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | overall conversion 06-08..09 > 06-01..07 | two-prop diff, 95% CI | NON_DISCRIMINATING | S1: 2.43% vs 3.12%, diff -0.68pp [-1.62,+0.25]; CI brackets 0 and contrast is unidentified (campaign shipped alongside nothing-randomized); campaign-page sessions convert 0.7% (3/427) pre-deploy vs 3.0%/3.6% on /home,/product; no confound-free comparison exists |
| T2 | H2 | conversion on /home,/product shifts at 06-10 | pre/post 06-10 by page, 95% CI | NON_DISCRIMINATING | S1,S3: non-campaign pages C-B -0.25pp [-1.35,+0.85]; CI includes 0; ~2900 sessions cannot detect shifts under ~1pp |
| T3 | H3 | device mix differs across periods and rates differ by device | strata tables | CONSISTENT | S1: mobile share 56%->53%->50%; lp page share 0%->21%; lp conversion 0.5-0.7% vs 2.7-3.9% elsewhere, so pooled rate is pulled down by mix of the campaign page. Lp is a new stratum, not a counterfactual for it |
| T4 | H4 | shortfall in sessions on 06-13/14 not mirrored in orders | counts | CONSISTENT | S1,S2: sessions -22% on 06-13/14 (mobile ~240 vs ~400), orders 23 and 17/day (normal). Orders=268 vs checkout_reached=yes=256, unreconciled; shortfall's cause unknown |

## Amendments

- 2026-11-08: none; no hypotheses or data requests were added after the plan.

## Conclusion
- Answer: the data does not show any improvement from the campaign, and no causal magnitude is identifiable. Site conversion fell from 3.12% (06-01..07) to 2.43% (06-08..09); that difference is -0.68pp, 95% CI [-1.62,+0.25]. /lp/summer-sale sessions converted at 0.6% (6/1053) versus 2.7-3.9% on /home and /product.
- Best supported: none for a campaign effect. H3 (mix) is descriptively consistent with the pooled dip.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 NON_DISCRIMINATING; unidentified contrast cannot refute; point estimate is negative |
  | H2 | causal | UNRESOLVED | T2 NON_DISCRIMINATING; refactor on 06-10 not separable, CI includes 0 |
  | H3 | descriptive | UNRESOLVED | T3 CONSISTENT as description; not discriminated against H1/H2 as cause |
  | H4 | data-artifact | UNRESOLVED | T4 CONSISTENT for a 06-13/14 session shortfall; cause unknown |
- Limitations: no randomization or holdout; campaign page has no pre-period; v3.4.1 checkout refactor (06-10) co-occurs; 14 days only, no seasonality baseline; S1/S2 completeness UNKNOWN; sessions have no user id so campaign-exposed users cannot be traced to orders. Continuation: causal-identification-review (design e.g. holdout/geo split).
