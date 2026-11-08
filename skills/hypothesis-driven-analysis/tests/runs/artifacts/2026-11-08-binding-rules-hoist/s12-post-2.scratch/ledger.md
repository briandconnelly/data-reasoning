# Investigation: How much did launching /lp/summer-sale improve checkout conversion?

## Problem

- Decision informed: whether to credit/continue/expand the summer-sale campaign on the strength of a conversion lift.
- Falsifiable question: did checkout conversion (sessions with checkout_reached=yes / sessions) rise because of the /lp/summer-sale launch, in sessions 2026-06-01..2026-06-14, and by how much?
- Success criteria: answered means a causal number is reported only if the design identifies it; otherwise report that it is not identifiable and what the data does show (descriptive contrasts with intervals).
- Stop condition: conclude when each hypothesis has a test outcome under the interval check or the data cannot test it; no iteration beyond the budget.
- Effort budget: 12 tool calls.
- Assumptions (headless, cannot ask): assignment of the campaign was not randomized (launched 06-08 to whoever arrived); outcome = checkout_reached per session (orders.csv cannot be joined to sessions; no key). Coverage level 95%.

## Hypotheses

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | The campaign launch (06-08) raised site-wide checkout conversion | site-wide rate in 06-08..06-09 (campaign live, before the 06-10 deploy) exceeds 06-01..06-07 | no rise in that window | site-wide rate 06-08..06-09 must exceed the 06-01..06-07 rate (contrast interval excludes <=0) | T1 | sessions |
| H2 | causal | The 06-10 v3.4.1 checkout form refactor changed conversion | step on non-campaign pages (/home,/product) at 06-10 | no step | non-campaign-page rate 06-10..06-12 must differ from 06-08..06-09 (contrast interval excludes 0) | T2 | sessions, deploys.log |
| H3 | descriptive (estimand: checkout rate of /lp/summer-sale sessions minus checkout rate of /home+/product sessions, 06-08..06-12) | Campaign-page visitors reach checkout more than other visitors | positive difference | zero/negative | difference must be positive (interval excludes <=0) | T3 | sessions |
| H4 | data-artifact | Session export is incomplete on 06-13/06-14 (session volume falls, orders exceed checkout_reached sessions), biasing denominators for those days | orders count > checkout_reached=yes count on 06-13/14 only, with a segment-shaped hole | counts reconcile as on other days | on 06-13/14 orders must exceed checkout_reached=yes sessions, while they equal on 06-01..06-12 | T4 | sessions, orders |
| H5 | descriptive (estimand: device-standardized change in site-wide rate vs raw change, 06-01..07 vs 06-08..09) | Device-mix shift (more mobile after launch) rather than any rate change moves the site-wide number | standardized change differs materially from raw | same | standardized and raw change must differ (interval of the difference excludes 0) | T5 | sessions |

Orientation done before preregistration (inventory/coverage only, no candidate-cause/outcome relationship inspected other than the daily counts of checkout_reached=yes, which appear in the coverage reconciliation for H4).

## Sources

| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 rows, unique ids) | 2026-11-08 | 06-01..06-14; /lp/summer-sale 160/day from 06-08 |
| S2 | data/s1-conversion/orders.csv (268 rows) | 2026-11-08 | client_version 3.4.0 through 06-09, 3.4.1 from 06-10; no session key |
| S3 | data/s1-conversion/deploys.log | 2026-11-08 | v3.4.1 checkout refactor 06-10T14:00Z; v3.4.2 logging only 06-12 |

## Data Validity

- Collection method: unknown beyond file contents; no export contract.
- Coverage matrix: /home 400/day, /product 200/day, /lp/summer-sale 160/day (06-08..12) constant through 06-12; on 06-13/14 all three drop ~22-25% (311/127/149; 304/126/154). Date x device: mobile falls from ~330-440 to ~240 on 06-13/14 while desktop stays ~345 — a mobile-shaped hole. No hole before 06-13. Also the device mix shifts toward mobile 06-08..12.
- Field population: no nulls in any field (S1, S2).
- Coverage baseline: orders (S2) as independent denominator for checkout sessions: orders/day equal checkout_reached=yes per day 06-01..06-12; 06-13: 23 vs 17; 06-14: 17 vs 11.
- Known instrument failures: v3.4.2 "logging only" 06-12.
- Source completeness semantics: S1: UNKNOWN — no export contract; its own missingness pattern cannot establish completeness; 06-13/14 rows are selection-sensitive with direction unknown (orders reconcile only partially).
S2: UNKNOWN — no export contract or independent baseline.
- Sensitivity checks performed: bootstrap intervals (95%) on contrasts; see Tests.

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | site-wide rate 06-08..09 > 06-01..07 | difference of proportions, bootstrap 95% CI | NON_DISCRIMINATING | S1: 2.43% (n=1520) vs 3.12% (n=4200), diff -0.68pp, CI95 [-1.60,+0.30]pp; the CI includes the predicted positive direction, and the contrast is unidentified (campaign adds a new page population; non-campaign pages alone: -0.12pp, CI [-1.17,+1.06]). Confound/composition check: device mix irrelevant (T5). work/analysis_output.txt |
| T2 | H2 | non-campaign rate 06-10..12 differs from 06-08..09 | difference of proportions, bootstrap 95% CI | NON_DISCRIMINATING | S1: 3.17% vs 3.00%, diff +0.17pp, CI95 [-1.14,+1.39]pp; detection limit ~1.3pp (~40% relative), so a refactor effect of ordinary size is not excluded. Also no pre-deploy/post-deploy comparison is free of the campaign overlapping. work/analysis_output.txt |
| T3 | H3 | campaign-page rate > other pages, 06-08..12 | difference, bootstrap 95% CI | CONTRADICTED | S1: 0.50% (n=800) vs 3.10% (n=3000), diff -2.60pp, CI95 [-3.36,-1.80]pp; interval around the same estimand, same scope, excludes >=0. Daily campaign rate 0.0-1.3% every day. Device mix of campaign page is balanced (550 mobile/503 desktop), no reversal check available by page-level confounds beyond device. adequacy: deterministic descriptive contrast on the full census of the stated scope, interval above (variants: none) |
| T4 | H4 | orders > checkout yes on 06-13/14 only | daily reconciliation | CONSISTENT | S1,S2: orders equal checkout_reached=yes on every day 06-01..06-12 (e.g. 17/17..20/20); 06-13: 23 orders vs 17 yes; 06-14: 17 vs 11. Mobile sessions fall 06-13/14 (~240 vs 330-440) while desktop is stable. Days 06-13/14 excluded from all other tests. work/analysis_output.txt |
| T5 | H5 | standardized vs raw change differ | direct standardization by device | CONTRADICTED | S1: pre-period device weights give a 06-08..09 rate of 2.43% vs raw 2.43%; device rates are nearly equal (desktop 2.45%, mobile 2.42%), so mix cannot move the number. adequacy: deterministic arithmetic identity on the observed rows (variants: none) |

## Amendments

- 2026-11-08: T1 outcome noted NON_DISCRIMINATING rather than CONTRADICTED because the 95% CI reaches +0.30pp. No hypotheses added.

## Conclusion

- Answer: the data does not show any improvement from the launch, and no causal number is available. Checkout conversion (sessions reaching checkout) was 3.12% in 06-01..06-07 and 2.43% in 06-08..06-09 with the campaign live and before the 06-10 deploy (difference -0.68pp, 95% CI -1.60 to +0.30pp). /lp/summer-sale sessions themselves reach checkout at 0.50% vs 3.10% for other pages (06-08..06-12; difference -2.60pp, CI -3.36 to -1.80pp), and daily orders did not rise after launch. Associative only: the launch was not randomized and the 06-10 checkout refactor overlaps.
- Best supported: H4 (data-artifact, T4 CONSISTENT) for the 06-13/14 gap; nothing is best supported as a cause of any conversion change (H1, H2 non-discriminated).
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 NON_DISCRIMINATING; contrast is unidentified (new page population, concurrent deploy), CI [-1.60,+0.30]pp |
  | H2 | causal | UNRESOLVED | T2 NON_DISCRIMINATING; detection limit ~1.3pp |
  | H3 | descriptive | REFUTED | necessary prediction (campaign-page rate higher) failed under T3; interval excludes zero on the same estimand |
  | H4 | data-artifact | UNRESOLVED | best supported for the 06-13/14 hole (T4 CONSISTENT); direction of bias unknown (S1 completeness UNKNOWN) |
  | H5 | descriptive | REFUTED | necessary prediction (standardized differs from raw) failed under T5; device rates nearly equal |
- Limitations: no randomization or holdout, so the lift is not identifiable; the 06-10 v3.4.1 checkout refactor overlaps the campaign (06-10 onward) and cannot be separated from it, and before 06-08 there is no comparison group; only 2 pre-refactor campaign days; outcome is checkout_reached, not purchases (orders cannot be joined to sessions); 06-13/14 session export is incomplete (mobile-shaped) and excluded; S1/S2 completeness UNKNOWN. Constructive continuation: causal-identification-review (design with a holdout or staggered rollout), if installed.
