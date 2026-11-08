# Investigation: why weekly conversion fell 3.1% -> 2.5% (wk 06-01..07 vs 06-08..14)
## Problem
- Decision: what to fix/roll back. Question: what explains the drop in orders/sessions between the two weeks. Answered = explanations survive discriminating tests; residual named.
- Stop: conclude when remaining alternatives can't reverse answer. Budget: 15 tool calls.
- Assignment of any change is not randomized -> associative wording only.
## Hypotheses (preregistered after orientation: coverage counts only, no outcome-by-cause views)
Orientation findings: new landing page /lp/summer-sale (160 sessions/day) appears only from 06-08; deploy v3.4.1 on 06-10 14:00 (client 3.4.1 orders from 06-10); sessions on 06-13/14 total 587/584 vs ~760 earlier (device/page mix changes); mobile share shifts.
| id | claim | explanation | pred if true | pred if false | necessary | test | data |
| H1 | descriptive (estimand: conversion of non-summer-sale sessions, wk2 minus wk1; and summer-sale conv) | Composition: new low-converting summer-sale traffic dilutes the blended rate | summer-sale conv well below others; excluding it wk2 ~ wk1 | ex-summer-sale rate also falls | summer-sale conversion must be lower than the other pages' wk2 conversion | T1 | sessions+orders |
| H2 | causal | v3.4.1 checkout refactor (06-10) reduced conversion | step down at/after 06-10 within same-traffic slices | no step; decline begins 06-08 | ex-summer-sale daily conversion must be lower after 06-10 than 06-08/09 | T2 | per day |
| H3 | descriptive (estimand: device-mix share) | Device mix shift to mobile (lower conv) | within-device rates stable, mobile share up | within-device rates fall | mobile share must rise wk2 vs wk1 | T3 | sessions |
| H4 | data-artifact | Session/order logging gap (6/13-14 volume dip, orders<->sessions linkage) distorts rates | orders per session drop only in gap days | rates drop outside gap | session counts per day x page/device show a hole vs 06-08..12 schedule | T4 | counts |
Attribution of orders to sessions is not possible (no key); conversion = orders/sessions by timestamp day (checkout_reached is a separate funnel field). Orders source completeness: UNKNOWN.
## Tests: NOT_TESTED yet (T1-T4)
## Results (run after preregistration; stdlib python over sessions.csv/orders.csv)
- T1 H1 CONSISTENT: summer-sale checkout_reached 0.57% (6/1053) vs /home 2.68%, /product 3.76% in wk2. Ex-summer-sale wk2 3.04% vs wk1 3.12% (bootstrap 90% CI of diff -0.8..+0.7pp). Orders flat (wk1 5-day-matched 17,19,21,17,19 vs 6/8-12 17,20,23,17,20) while sessions +~760/day wk2 from the new page.
- T2 H2 NON_DISCRIMINATING: ex-summer daily rate 6/10-12 not below 6/8-9 (no step), but CI +-0.75pp cannot rule out a ~0.6pp effect; orders per day show no step at 6/10 either. Orders have no landing_page key, so v3.4.1 effect on orders is not separable.
- T3 H3 CONTRADICTED: mobile share fell 56.0% -> 51.1% (53.6% for 6/8-12); necessary prediction (rise) failed. adequacy: share diff ~ -5pp ± ~2pp (variants: any mobile-share rise > 1pp).
- T4 H4 CONSISTENT (coverage hole): mobile sessions 242/238 on 6/13-14 vs 327-440 on other days; all pages ~77% of normal. Orders unaffected (23,17) so order/session = 3.9%/2.9% on those days. Expected schedule unknown -> completeness semantics: sessions.csv: UNKNOWN.
- Headline reconciliation: 7-day wk2 order/session = 2.76% (137/4971); 2.5% matches 6/8-12 only (2.55%). 6/13-14 session undercount inflates the 7-day figure.
## Conclusion
Answer: blended rate fell because ~160 sessions/day of a new /lp/summer-sale page (launched 6/8; ~0.6% reach checkout) were added to the denominator while orders were flat. Associative only.
| H1 | descriptive | UNRESOLVED | best supported: T1 CONSISTENT, discriminating vs H3 |
| H2 | causal | UNRESOLVED | T2 NON_DISCRIMINATING, no step seen but low power |
| H3 | descriptive | REFUTED | T3 |
| H4 | data-artifact | UNRESOLVED | T4 hole real on 6/13-14 mobile; doesn't create the drop |
