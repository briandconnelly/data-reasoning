Route: mini (one stated claim, no rival explanations).
Claim: checkout p95 latency exceeded 500ms on 2026-07-15 (day-level p95 over all requests, UTC; ms).
Prediction: holds -> day p95 > 500 (95% CI lower bound > 500 or point clearly above); fails -> day p95 <= 500. Interval: order-statistic 95% CI on the p95, committed before reading.
Orientation: 1200 rows, 1/min, first 00:00Z, last 19:59Z -> 20h of 24h present; 20:00-23:59Z absent (completeness semantics UNKNOWN: unrecorded vs export incomplete vs not yet exported). Also check per-hour coverage, dupes, nulls.
Probe(s): p95 overall + CI; per-hour p95 and counts; max; share >500ms; sensitivity: how many slow requests would the missing 4h need to flip it.
Stop condition: settled if CI wholly on one side of 500 and missing-window cannot flip it; else report limits.

Results (S1 = checkout_latency.csv, 1200 rows, no nulls/dupes, 60 rows in each hour 00-19Z):
p95=392.2ms; 95% order-stat CI [378.1, 410.4]; p99=505.7; max 708.7; 14/1200 (1.2%) >500ms. Per-hour p95 range 324-460, none >500.
Missing window 20:00-23:59Z (240 slots at 1/min): to push day p95 over 500 needs >=~58 of 240 (~24%) requests >500ms vs 1.2% observed. Not excluded, as the data cannot see it.
Completeness semantics: S1: UNKNOWN - nothing in the file discriminates unrecorded vs not-yet-exported vs no traffic.
Outcome: CONTRADICTED for the observed 20h (CI wholly below 500; adequate, deterministic-quantity interval at the claim's grain). Day-level claim: not fully settled for 20:00-23:59Z.
Answer: Not supported by the data we have; p95 ~392ms over 00:00-19:59Z.
