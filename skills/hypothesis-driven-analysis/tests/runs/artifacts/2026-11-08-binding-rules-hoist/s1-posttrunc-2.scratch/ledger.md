# Investigation: weekly checkout conversion 3.1% (wk 06-01) -> 2.5% (wk 06-08): why?
## Problem
- Decision: whether to roll back v3.4.1 / pull the new campaign page / ignore.
- Question: what explains the drop in orders/sessions, wk 06-01..07 vs 06-08..14 (all sessions, per-session units). Conversion = orders / sessions.
- Success: one or more explanations account for the drop and survive a discriminating test; unattributed residual reported as such.
- Stop: conclude when no named unresolved rival could reverse the answer. Budget: 12 queries.
- Assumption (headless): assignment of page/deploy not randomized -> associative wording only.
## Hypotheses
| id | claim | Explanation | If true | If false | Necessary prediction | Test | Data |
| H1 | causal | New /lp/summer-sale traffic (first seen 06-08) converts below the rest and dilutes the blended rate | sale-page rate << other pages; other pages' rate ~unchanged | sale rate similar to others | sale-page conversion must be below week-1 blended rate | T1 | sessions |
| H2 | causal | v3.4.1 (06-10 14:00) checkout refactor lowered conversion | rate falls after deploy within each landing page | rate already lower before 06-10 14:00 | the drop must not precede the deploy (06-08/09 on non-sale pages show no drop vs wk1) -> fail if drop already present pre-deploy on same pages | T2 | sessions, orders, deploys |
| H3 | data-artifact | Session volume/coverage anomaly (e.g. 06-13/14 mobile) inflates denominator | hourly session counts show a hole/spike vs schedule | counts steady | sessions per hour x device must deviate from baseline | T3 | sessions |
| H4 | descriptive (estimand: device mix shift in sessions, wk2-wk1) | Mix shift to lower-converting device | per-device rates differ and mix moved enough | per-device rates equal | mobile/desktop rate differ | T4 | sessions |
## Sources
S1 sessions.csv (9171 rows, 06-01..06-14); S2 orders.csv (268); S3 deploys.log (3 lines)
## Data Validity
Coverage (orientation, counts only): daily sessions by device and landing page examined. Sale page 0 before 06-08, 160/day 06-08..12, 127/126 on 06-13/14; 06-13/14 total ~587/584 vs 760 weekdays, mobile 242/238 vs ~430 (week 1 weekend was 600/day). No independent denominator -> coverage unverifiable. Orders/day equals checkout_reached=yes count per day (consistent). No nulls.
Source completeness: S1: UNKNOWN — no independent session counter to discriminate dropped vs real.
S2: UNKNOWN — orders compared only to S1's own flag.
## Tests
| id | H | prediction | outcome | evidence |
| T1 | H1 | sale-page rate below wk1 blended rate; other pages ~unchanged | CONSISTENT | sale page 6/1053 = 0.57% (approx 95% CI 0.2-1.2%) vs wk1 3.12%; non-sale pages wk2 119/3918 = 3.04% vs 3.12% (diff -0.08pp, SE approx 0.37pp, noise). adequacy: n/a for consistent (S1) |
| T2 | H2 | drop must not precede deploy; within-page rates fall after 06-10 | CONTRADICTED | blended rate already 2.2% (06-08: 17/760) and 2.5% pre-deploy; non-sale rate unchanged before/after 06-10 (3.04% overall wk2). adequacy: non-sale difference 0.08pp +/- 0.37pp (variants: a deploy effect >=0.8pp would be detected) (S1,S3) |
| T3 | H3 | hourly session counts deviate from baseline | CONSISTENT (as a gap) | 06-13/14 mobile ~28/hr vs ~45-55 on weekdays and ~40 prior Sat; coverage unverifiable (no independent counter). Drop persists on 06-08..12 alone: 97/3800 = 2.55%, so gap does not drive it |
| T4 | H4 | device rates differ and mix shifted | NON_DISCRIMINATING for the drop | mobile share fell wk1 56%->wk2 51%; device rates differ little within page; desktop fall (3.36->2.22) is the sale page landing on desktop (0.2%) |
## Conclusion
- Answer: the drop is associated with the new /lp/summer-sale landing traffic (first appears 06-08, ~21% of wk2 sessions) converting at ~0.6%, diluting the blended rate. Excluding it, conversion is flat (3.12% -> 3.04%).
| id | claim | status | basis |
| H1 | causal | UNRESOLVED | best supported (T1); associative only, page was not randomized |
| H2 | causal | REFUTED | necessary timing prediction failed, T2 |
| H3 | data-artifact | UNRESOLVED | gap seen on 06-13/14 but coverage unverifiable; does not drive the drop |
| H4 | descriptive | UNRESOLVED | T4 non-discriminating |
- Limitations: sale page conversion is low in 6 orders; whether the page is low-quality traffic or a broken funnel is untested; 06-13/14 volume gap unexplained; no causal design.
