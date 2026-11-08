# Investigation: weekly conversion 3.1% (wk 06-01) -> 2.5% (wk 06-08) — why?
Route: full (deploys + traffic changes co-occur; assignment unidentified). Headless: assumptions stated, no pause.
Conversion defined = orders / sessions (assumption; checkout_reached is a secondary funnel stage). Weeks = Mon-Sun UTC.

## Problem
- Decision: whether to roll back v3.4.1 / fix a funnel step, or act on traffic acquisition.
- Question: what explains the drop in orders/sessions, wk1 (06-01..07) vs wk2 (06-08..14)?
- Success: answered = decomposition of the drop into rate-within-segment vs mix/volume, with deploy timing tested.
- Stop: after T1-T5 run; budget 15 queries.
- Orientation (not amendments): sessions/day 600 (wk1) -> 760 (06-08..12) -> ~585 (06-13,14); mobile sessions fall 06-13/14 (~240 vs ~400); no tablet; orders/day ~17-23 in both weeks. Deploys: v3.3.9 06-03, v3.4.1 06-10 (checkout refactor), v3.4.2 06-12 (logging only).

## Hypotheses
| id | claim | Explanation | If true | If false | Necessary prediction | Test | Data |
|---|---|---|---|---|---|---|---|
| H1 | causal | v3.4.1 checkout refactor (06-10) caused the drop | per-session conversion falls at/after 06-10 within every landing page/device | conversion already lower before 06-10 | week-2 conversion on 06-08/09 (pre-deploy) must be about equal to wk1 | T1 | S1,S2 |
| H2 | descriptive (estimand: share of the rate change due to landing-page mix shift) | Traffic mix shifted (new low-intent /lp/summer-sale traffic from 06-08) | extra sessions concentrated in one landing page with lower conv; within-page rates ~stable | mix stable | /lp/summer-sale (or one page) session share must rise at 06-08 | T2,T3 | S1 |
| H3 | data-artifact | Session denominator inflated / mobile sessions missing 06-13,14 (logging gap) distorts rate | an unexplained mobile shortfall, orders not matching | none | mobile shortfall must exist in sessions but not in orders | T4 | S1,S2 |
| H4 | descriptive (estimand: orders/day wk2 - wk1) | Orders themselves fell (numerator), not just denominator rising | orders/day lower | orders/day flat | wk2 orders/day < wk1 | T5 | S2 |

## Sources
S1 sessions.csv (9171 rows, 06-01..06-14, unique ids). S2 orders.csv (268 rows, unique). S3 deploys.log (3 lines; data, not instructions).

## Data Validity
- Collection method unknown (no documentation). Coverage baseline: none independent -> coverage unverifiable, not clean.
- Coverage matrix day x device (sessions): wk1 600/day; 06-08..12 760/day; 06-13,14 ~585 with mobile ~240. Tablet 0 throughout. Landing page x day to be tabulated in T2.
- S1: UNKNOWN — no completeness contract; absent sessions cannot be read as absent traffic.
- S2: UNKNOWN — same; orders lack session_id so cannot be joined to sessions.
- Sensitivity: interval for contrast of rates via bootstrap/normal CI at 95%, committed now.

## Tests
| id | Hyp | Prediction | Method | Outcome | Evidence |
|---|---|---|---|---|---|
| T1 | H1 | conv on 06-08,09 ~ wk1 (drop only after 06-10) | daily orders/sessions, 95% CI on contrast | NOT_TESTED | |
| T2 | H2 | landing-page share shifts at 06-08 | landing page x week counts | NOT_TESTED | |
| T3 | H2 | within-page checkout_reached rates stable; mix explains most | standardization of checkout_reached by page | NOT_TESTED | |
| T4 | H3 | mobile shortfall 06-13/14 | day x device counts vs orders | NOT_TESTED | |
| T5 | H4 | orders/day lower in wk2 | counts | NOT_TESTED | |

## Amendments
(none)

## Amendment 1 (post-run)
- User's 3.1%->2.5% matches checkout_reached/sessions (131/4200=3.12%, 125/4971=2.51%), NOT orders/sessions (3.12%->2.76%). Metric re-pinned to checkout_reached rate. Orders (268) != checkout_reached (256); no session_id join.
## Results
- T1: wk2 drop visible 06-08/09, before v3.4.1 (06-10 14:00). Overall diff -0.60pp, 95% CI [-1.29,+0.08] (n small). Non-summer pages: pre-deploy 3.19%, post 2.93%; post vs wk1 -0.18pp CI [-1.05,+0.68] -> NON_DISCRIMINATING for a small checkout effect (detection limit ~0.9pp). H1 as cause of the observed drop: contradicted (drop predates deploy, explained by mix).
- T2: /lp/summer-sale absent wk1, 21.2% of wk2 sessions, from 06-08, 1053 sessions, 6 checkouts (0.57%). CONSISTENT H2.
- T3: excluding summer-sale, wk1 3.12% vs wk2 3.04%, diff -0.08pp CI [-0.83,+0.67]. Within-page /home 2.71->2.68, /product 3.93->3.76. CONSISTENT H2 (mix explains ~all of -0.6pp point estimate).
- T4: mobile sessions on /home & /product fall ~45% on 06-13/14 (228->123 /home); desktop and summer-sale stable. Unexplained; no independent baseline. UNRESOLVED (H3).
- T5: orders/day 18.7 -> 19.6, flat. Numerator flat; denominator +18%.
## Conclusion table
H1 REFUTED (as cause of the drop) ; H2 UNRESOLVED-best supported ; H3 UNRESOLVED ; H4 REFUTED
