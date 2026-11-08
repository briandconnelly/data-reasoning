# Investigation: Weekly checkout conversion fell 3.1% -> 2.5% (wk 2026-06-01 vs wk 2026-06-08) — why?

## Problem
- Decision informed: whether to roll back v3.4.1 (checkout refactor, 06-10) or look elsewhere.
- Falsifiable question: what explains the drop in checkout_reached/sessions, sessions of 06-01..06-07 vs 06-08..06-14 (UTC), all sessions?
- Success criteria: answered means the drop is decomposed and each live explanation survives or fails a discriminating test.
- Stop condition: conclude when no unresolved alternative could reverse the answer; else stop with limits.
- Effort budget: 10 queries.
- Assumption (headless, no assignment mechanism stated): nothing identifies causal effects; wording associative.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | v3.4.1 checkout refactor (06-10) lowered conversion | per-day conversion steps down on/after 06-10 | no step at 06-10 | the conversion drop must not already be present before 06-10 (06-08/09 rate below wk1 range) | T1 | sessions, deploys |
| H2 | descriptive (estimand: conversion of sessions in week 2 excluding /lp/summer-sale minus week-1 conversion, and share of the drop from the new-page denominator) | New landing page /lp/summer-sale (first seen 06-08) adds low-converting sessions, diluting the rate (composition) | non-summer-sale conversion is about unchanged wk1 vs wk2; summer-sale page converts far lower | non-summer-sale conversion itself falls ~0.6pp | non-summer-sale conversion wk2 must be within the 95% interval of wk1 | T2 | sessions |
| H3 | descriptive (estimand: mobile share change and per-device conversion) | Device mix shift to mobile lowers rate | mobile share up and mobile conv < desktop | mix flat | mobile share must rise wk1->wk2 | T3 | sessions |
| H4 | data-artifact | Orders/sessions instrument gap (missing rows) creates apparent drop | orders/checkout counts disagree or coverage holes | coverage complete, counts reconcile | daily checkout_reached=yes must differ from orders count on some day | T4 | both files |

## Sources
| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 rows) | 2026-11-08 | 06-01..06-14, no nulls/dups |
| S2 | data/s1-conversion/orders.csv (268 rows) | 2026-11-08 | 06-01..06-14, no nulls/dups |
| S3 | data/s1-conversion/deploys.log | 2026-11-08 | 3 releases |

## Data Validity
- Collection method: unknown export; no contract.
- Coverage matrix: sessions day x device and day x landing_page counted (orientation). 600/day for 06-01..07; 760/day 06-08..12; 587/584 on 06-13/14 (mobile 242/238, all pages ~22% lower). Orders by day x client_version counted.
- Field population: all fields 100% populated.
- Coverage baseline: no independent denominator or schedule; session volume 06-13/14 differs from 06-08..12 pattern (possible weekend or partial capture) — unverifiable.
- Known instrument failures: none documented.
- Source completeness semantics:
S1: UNKNOWN — no export contract or independent session counter, so absent sessions cannot be read as no traffic.
S2: UNKNOWN — no export contract, so absent orders cannot be read as no purchases.
- Sensitivity checks performed: Wilson/bootstrap intervals in tests (95%).

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | pre-deploy (06-08..06-10T14) all-session rate not below wk1 | pooled pre-deploy vs wk1, bootstrap 95% contrast | NON_DISCRIMINATING | pre-deploy 2.66% (54/2028) vs wk1 3.12% (131/4200); contrast -0.46pp, 95% CI [-1.34,+0.39] includes 0, so no discrimination (S1). Descriptive aside (not preregistered): non-summer-sale daily counts 06-10..12 (21,17,19 of 600) equal 06-03..05 exactly, and non-SS rate pre-deploy 3.19% vs post-deploy 3.00% (51/1601 vs 42/1399), no visible step. Confound check: SS page is a composition shift that explains the pre-deploy dip |
| T2 | H2 | non-summer-sale wk2 rate within 95% Wilson interval of wk1 | stratify by landing page | CONSISTENT | non-SS wk2 3.04% (119/3918) inside wk1 [2.63,3.69]; contrast wk2-wk1 -0.08pp, bootstrap 95% CI [-0.80,+0.69]; SS page 0.57% (6/1053), 21.2% of wk2 sessions; /home and /product session counts unchanged at 400/200 per day through 06-12, so SS traffic is additive (S1). Aggregation check done: Simpson-style standardization: wk2 rate = 0.788*3.04+0.212*0.57=2.51 |
| T3 | H3 | mobile share rises | device share by week | CONTRADICTED | mobile share 56.0% (2354/4200) wk1 -> 51.1% (2542/4971) wk2; deterministic count on the records, no sampling adequacy bound needed (S1) |
| T4 | H4 | yes-count equals orders count each day | reconcile | CONSISTENT | matches 06-01..12; 06-13: 23 orders vs 17 yes; 06-14: 17 vs 11. Sessions on 06-13/14 are ~22% below 06-08..12 (587/584 vs 760), across all pages and hours. Scope: 06-13/14 only (S1,S2) |

## Amendments
- Note: orientation counts of daily yes by day were seen alongside page counts before registering; H2 is therefore treated as potentially retrospective; support would rest on within-page/held-out structure (day-level check T1, device split).

## Conclusion
- Answer: the drop is mostly a denominator effect, not a worse checkout. From 06-08 a new landing page /lp/summer-sale adds ~160 sessions/day that convert at 0.57% (6/1053); the rest of traffic converts at 3.04% in week 2 vs 3.12% in week 1 (contrast -0.08pp, 95% CI -0.80 to +0.69). Mixing in the page gives the 2.51% (about 0.5pp of the 0.6pp drop). The v3.4.1 deploy on 06-10 shows no visible step, but the data cannot rule out a modest checkout effect (within roughly +/-0.7pp).
- Best supported: H2 (composition), via T2. Caveat: I saw daily counts alongside page counts before stratifying, so H2 is partly retrospective; its support is not independent of the records that suggested it.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 NON_DISCRIMINATING (CI includes 0); no step in non-SS conversion at the deploy, but not refuted |
  | H2 | descriptive | UNRESOLVED | best supported (T2 CONSISTENT) |
  | H3 | descriptive | REFUTED | necessary prediction (mobile share rises) failed, T3: share fell |
  | H4 | data-artifact | UNRESOLVED | T4 CONSISTENT for 06-13/14 only: orders and checkout_reached disagree and sessions drop ~22%; cause unknown |

- Limitations: session/order completeness is UNKNOWN (no export contract), so on 06-13/14 the direction of bias in the rate is unknown. Using orders as numerator, week 2 would be 2.76% on observed sessions (or ~2.58% if the missing ~330 sessions are added), so the drop is 0.4-0.5pp rather than 0.6pp but the dilution story survives. Claims are associative: nothing randomized the landing page or deploy. Whether summer-sale traffic is truly additive is inferred from flat /home and /product counts. One week-2 SS page effect on checkout is not tested.

