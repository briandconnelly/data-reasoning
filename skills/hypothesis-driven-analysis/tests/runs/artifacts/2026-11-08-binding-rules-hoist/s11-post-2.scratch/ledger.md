Claim: checkout p95 latency exceeded 500ms on 2026-07-15 (day-level p95 of per-request latency_ms, S1 checkout_latency.csv).
Prediction: holds if day p95 > 500; fails if <= 500. 95% order-statistic CI on p95 committed in advance; coverage checked (expected 1 row/min, 1440/day).
Probe(s): p95 + CI; coverage by hour; max/outliers; hourly p95; dupes/nulls.
Stop condition: CI entirely on one side of 500 and coverage understood; else say data cannot settle.
Outcome: (pending)
Answer: (pending)

RESULT (appended): 1200 rows, unique ids, no nulls, 1/min 00:00Z-19:59Z; 20:00-23:59Z absent (240 min, completeness semantics UNKNOWN).
p95=392.2ms, 95% CI (rank, normal approx) [378.1, 410.4]; 500 outside. Max hourly p95 = 460.1 (h15); 14/1200 requests >500.
Outcome: CONTRADICTED for covered window (adequate: CI at committed 95%, same estimand). Not for the missing 4h.
Answer: claim not supported; p95 ~392ms over 20h covered; cannot exclude 20:00-24:00 UTC (and timezone of "yesterday" unstated).
