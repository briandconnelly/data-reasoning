# Mini-route ledger — checkout p95 claim (written BEFORE any latency-by-segment read)

Route: mini. One stated claim, no rival explanation asked to be told apart, non-causal. Not full: nothing causal is asked.

Claim: On 2026-07-15, checkout p95 latency_ms exceeded 500 ms, and did so only for mobile x evening-peak x returning requests
(i.e. the exceedance is confined to that conjunction; every other slice is <=500).

Orientation (counts/coverage only, no latency looked at): 1400 rows, 1400 unique request_id, no nulls, 2026-07-15T00:00Z..23:19Z,
exactly 1 row/min (60/hour, hour 23 has 20 -> last 40 min of the day absent; completeness of export UNKNOWN, tail hours only).
Volume is flat by hour, so no "peak" is visible in the data; evening peak is not defined by the claimant, and timestamps are UTC (site timezone unknown).
Assumptions pinned before probing: evening peak = 18:00-21:59 UTC (primary); sensitivity windows 17-20, 19-22, 17:00-23:19. p95 = order-statistic p95 (linear-interp) of latency_ms.
Cells n (mobile,returning,18-21): from crosstab ~ 70 rows -> p95 rests on ~4 tail points; interval will be wide.

Prediction (necessary parts, all must hold for the claim as stated):
 P1 p95(mobile & returning & evening) > 500.
 P2 "only": p95 of each complementary slice <= 500 — mobile-returning off-evening, mobile-new evening, desktop-returning evening, and whole-day overall.
If the claim is false: P1 fails (cell p95 <=500), or some other slice also exceeds 500 (the "only" fails).
Interval: 95% (committed now), bootstrap (10k resamples, seed 0) around each p95, and around the contrast (cell p95 minus rest-of-day p95).
Reading rule: 500 inside the interval -> NON_DISCRIMINATING for that part; outside -> discriminates.
Stop: after the probes below (2 scripts). Budget: 3 tool calls.
Probes: (a) p95 + CI per slice above and window sensitivity; (b) look at distribution/outliers in the cell.

## Outcome (probes in work/probe_a.txt, work/probe_b.txt)
P1 CONTRADICTED, discriminating: mobile&returning&18-21 UTC p95 = 438.6 ms, 95% bootstrap CI (397, 468), n=71; 500 lies outside the CI. Robust to windows 17-21, 19-23, 17-24, 20-24 (p95 408-434, CI upper bounds <=468). Only 1 of 71 requests >500 (598 ms).
P2 ("only") also fails independently: mobile&NEW&evening p95 = 804 ms, CI (510, 867), n=63 (9 >500) — exceedance sits in the new-user slice. Whole-day p95 453 (CI 433-472), no exceedance overall; all-evening p95 497 (CI 468-633).
Post-hoc (retrospective, exploratory): mobile-new is high off-evening too (p95 552, CI 479-626), so the evening effect for new users is not separated from a general mobile-new slowness. Not a finding.
Limits: last 40 min of the day missing (23:20-23:59), completeness UNKNOWN; evening window/timezone assumed; per-cell p95 rests on few tail points.
