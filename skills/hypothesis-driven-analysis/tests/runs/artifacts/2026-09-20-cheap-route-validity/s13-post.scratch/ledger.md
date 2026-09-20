# Mini ledger — "checkout p95 > 500ms on 2026-07-15, only mobile, only evening peak, only returning users"

Route: mini (one stated non-causal claim, no rival explanations asked for). Headless: no consultation pause; assumptions stated.

Claim: on 2026-07-15, p95 latency_ms of checkout requests exceeded 500ms in the cell mobile × returning × evening peak, and did not exceed 500ms when any one of the three conditions is relaxed ("only").

Assumptions (fixed BEFORE reading any latency-by-segment result):
- "Evening peak" is undefined by the requester and volume is flat by hour (orientation), so it cannot be derived from traffic. Primary definition: 18:00-22:00 (hours 18-21) in the timestamps as given (UTC 'Z'; user timezone unknown). Alternate windows (17-21, 19-23) are robustness checks only, reported as such, not used to pick the answer.
- "Returning" = user_type == returning; "mobile" = device == mobile.
- p95 = empirical 95th percentile of latency_ms over requests in the cell.

Prediction: if claim holds -> slice p95 > 500 with 95% order-statistic CI lower bound > 500, AND each relaxed slice (mobile evening new; desktop evening returning; mobile off-peak returning) has p95 <= 500 (CI not entirely above 500). If fails -> slice p95 <= 500 (CI upper bound < 500 = CONTRADICTED; CI containing 500 = NON_DISCRIMINATING).
Interval: distribution-free order-statistic (binomial) 95% CI for the p95 at each cell; coverage committed now at 95%.
Probes: (1) slice p95 + CI; (2) three relaxed slices + CIs; (3) whole-day p95 for context; (4) alternate evening windows as robustness.
Data validity (orientation, no latency-by-segment inspected): see below.
Stop condition: settled once the slice interval and the three relaxed-slice intervals are computed; if any bearing interval contains 500, outcome is NON_DISCRIMINATING for that part.

## Source
S1: data/s13-conjunctive/checkout_latency.csv (1400 rows; timestamp, request_id, latency_ms, device, user_type). Provenance/collection method not documented.

## Data validity (orientation)
- request_id unique (1400/1400); no nulls; all rows dated 2026-07-15; timestamps sorted, 1 row/minute (a row per minute, 00:00-23:19). Latency range 49.9-897.2.
- Coverage: last row 23:19Z; hour 23 has 40 rows vs ~57-60 for other hours -> 23:20-23:59 absent (export ends early, or day cut). Hour 23 is outside primary window; matters only for the 19-23 robustness window.
- Rows are ~1/min flat, which implies a sample/regular export, not full traffic (real peak traffic would show volume swings). Coverage baseline: none independent -> completeness UNVERIFIABLE; source completeness: S1: UNKNOWN — no export contract or independent counter to tell whether absent requests are absent, unrecorded, or unexported, and flat volume cannot discriminate. So p95 is over the rows in this file only; whether it is the true population p95 is not established.
- Crossed coverage (hour x device x user_type) counted: every hour has all four cells populated, 5-24 rows per cell-hour. No hole in the primary window. No joins.

## Probes and outcome (primary window 18:00-22:00 as given; order-statistic 95% CI for p95; script inline, S1)
| slice | n | p95 | n>500 | 95% CI for p95 |
| --- | --- | --- | --- | --- |
| mobile, returning, evening (claimed) | 71 | 438.6 | 1 | (404.2, >= sample max 597.9) — upper limit not bounded by n=71 |
| mobile, NEW, evening | 63 | 804.1 | 9 | (574.6, >= sample max) |
| desktop, returning, evening | 65 | 374.8 | 0 | (303.7, >= sample max 487.3) |
| mobile, returning, off-peak | 382 | 349.8 | 1 | (330.3, 405.0) |
Robustness windows: 17-21 slice p95 433.8 / mobile-new 824.0 (CI lower 608.0); 19-23 slice 430.7 / mobile-new 698.0 (CI lower 490.9, contains 500). Same qualitative picture.

T1 (claimed slice p95 > 500): NON_DISCRIMINATING by the preregistered CI rule — point estimate 438.6 < 500 but CI upper limit reaches the sample max (597.9) so 500 is inside it; n=71 cannot bound p95 from above. Detection limit: cannot separate p95 in ~404-598 range.
T2 ("only returning": new-user mobile evening p95 must not exceed 500): CONTRADICTED on primary window and 17-21 (CI lower bound 574.6 / 608.0 > 500); 19-23 window inconclusive (lower 490.9). Deterministic threshold comparison against the claim's own estimand at the same scope; conjunctive claim fails if this conjunct fails.
T3 (desktop evening returning, mobile off-peak returning <= 500): CONSISTENT (no CI lower bound above 500).
Data validity caveat unchanged: S1 completeness UNKNOWN; 23:20-23:59 absent.
