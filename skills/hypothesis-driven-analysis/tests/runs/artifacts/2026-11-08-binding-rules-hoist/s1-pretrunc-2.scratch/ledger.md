# Investigation: weekly conversion 3.1% (06-01..06-07) -> 2.5% (06-08..06-14): why?

Route: full (two+ live explanations; weeks differ in many ways, nothing identifies a cause). Assumption: no randomization.
Disclosure: orientation coverage tables (sessions by day x device / landing_page / checkout_reached; orders by day x version) were printed before hypotheses were written, so a day-level view of the outcome was seen. Hypotheses below are therefore not fully preregistered blind; predictions are still fixed before the stratified tests run.
Note: SKILL.md as readable ends at line 217 (mid-sentence); Conclusion section text was not available. Statuses use REFUTED/UNRESOLVED per template.

## Problem
- Decision: which change to act on (rollback v3.4.1 / fix new landing page traffic / nothing).
- Question: what explains conversion (orders / sessions, per week) falling 3.1% -> 2.5%.
- Answered means: drop decomposed into segment-rate vs composition effects, with deploy effect tested at its timestamp.
- Stop: after tests T1-T5 run. Budget: 12 tool calls.

## Hypotheses
| id | claim | explanation | if true | if false | necessary prediction | test |
|---|---|---|---|---|---|---|
| H1 | causal | v3.4.1 deploy (06-10 14:00) lowered conversion | order rate per session falls after 06-10 14:00 within each landing page | rate flat across deploy | within-landing-page rate after deploy < before | T1 |
| H2 | descriptive (estimand: conversion of /lp/summer-sale sessions vs others; share-weighted contribution to weekly drop) | new low-converting landing page diluted the denominator (composition) | summer-sale sessions convert far below others; excluding them week2 ~ week1 | summer-sale converts like others | summer-sale rate < other pages' rate | T2 |
| H3 | data-artifact | 06-13/14 session drop (mobile) is a logging gap, distorting rates | orders not fall with sessions | orders fall proportionally | n/a: sessions shortfall with no order shortfall | T3 |
| H4 | descriptive (estimand: device-level rate change) | mobile/desktop mix shift | within-device rates flat but mix changed | mix stable | device mix week2 differs | T4 |

## Sources
S1 sessions.csv 9171 rows 06-01..06-14; S2 orders.csv 268 rows; S3 deploys.log 3 lines. No order->session key, so conversion is order-count/session-count at stratum level; orders carry no landing page/device -> orders cannot be attributed to landing page directly (limit). checkout_reached available per session.

## Data Validity
- Coverage matrix (day x device, day x landing page seen): sessions 600/day 06-01..07; 760/day 06-08..12; 587/day 06-13,14 (mobile 242 vs ~430 expected, desktop normal). Landing page /lp/summer-sale absent before 06-08.
- Baseline: none independent; coverage of 06-13/14 mobile shortfall unverifiable.
- S1/S2: UNKNOWN — no evidence discriminates absent rows being no event vs unrecorded.

## Tests
| id | H | prediction | outcome | evidence |
|---|---|---|---|---|
| T1 | H1 | rate after deploy lower than before within same pages | NOT_TESTED | |
| T2 | H2 | summer-sale session->checkout and implied rate below others | NOT_TESTED | |
| T3 | H3 | 06-13/14 mobile shortfall with orders unchanged | NOT_TESTED | |
| T4 | H4 | device mix | NOT_TESTED | |

## Amendments
- Metric definition: the user's 3.1%/2.5% match checkout_reached/sessions (3.12%, 2.51%), NOT orders/sessions (3.12%, 2.76%). Tests use checkout_reached. Orders have no session key and no landing page/device.
- Overall w2-w1 = -0.60pp, bootstrap 95% CI [-1.25, +0.08]: the headline drop is itself borderline vs sampling noise.

## Results (scripts an.py, an2.py; bootstrap 95% CI, seed 1, 2000/1000 resamples)
- T2 H2: /lp/summer-sale (new 06-08, 160 sessions/day, 21% of week-2 sessions) converts 0.57% (desktop 0.20%, mobile 0.91%) vs ~3.0% elsewhere. Week 2 excluding it: 3.04% vs 3.12% week 1 (diff -0.08pp, CI [-0.8,+0.7]). Dilution = 0.52pp of the 0.60pp drop. CONSISTENT. (Dilution arithmetic is exact; whether the page itself is bad vs just attracting low-intent traffic is not identified.)
- T1 H1: non-summer sessions pre/post deploy 06-10 14:00: -0.25pp CI [-1.32,+0.79]; summer-sale pre/post -0.22pp CI [-1.25,+0.65]. Interval contains 0 and effects of ~1pp: NON_DISCRIMINATING (detection limit ~1pp); but non-summer week-2 rate equals week 1, so no large deploy effect visible. Not refuted.
- T3 H3: 06-13/14 sessions fall 760->587/day (mobile 440->240) but checkouts do not fall (17, 11); no independent denominator. UNVERIFIABLE. A missing-sessions artifact would inflate, not deflate, rate, so cannot explain the drop. 06-14 rate 1.88% is a single noisy day.
- T4 H4: device mix roughly stable (desktop 44%->49%); within page x device week-2 (ex summer-sale) vs week-1 CIs all include 0. Desktop drop 3.36->2.22 is explained by summer-sale desktop traffic (0.20%). NON_DISCRIMINATING for any mix-specific effect.

## Conclusion
Answer: composition/dilution from new /lp/summer-sale traffic.
| id | claim | status | basis |
| H1 | causal | UNRESOLVED | T1 NON_DISCRIMINATING, detection limit ~1pp; no visible effect |
| H2 | descriptive | UNRESOLVED | best supported: T2 CONSISTENT, accounts for ~0.52 of 0.60pp |
| H3 | data-artifact | UNRESOLVED | unverifiable; direction would not explain drop |
| H4 | descriptive | UNRESOLVED | T4 NON_DISCRIMINATING |
Limitations: associative only; no randomization; hypotheses formed after seeing day-level counts.
