# Mini ledger (preregistered before computing p95)
Claim: checkout p95 latency exceeded 500ms on 2026-07-15 (p95 of per-request latency_ms, whole day, UTC timestamps).
Prediction: holds -> p95 > 500; fails -> p95 <= 500. Interval: 95% order-statistic/bootstrap CI around p95 committed in advance.
Probes: (1) coverage by hour (expected 60 rows/hr, 24 hr); (2) p95 + CI; (3) max, count >500, hourly p95.
Stop condition: CI entirely on one side of 500 over covered period AND coverage gap can't reverse it; else report limit.
Source S1: checkout_latency.csv. Completeness semantics: S1: UNKNOWN (no export contract/independent counter).

## Results
Coverage: 1200 rows, 1200 unique ids, exactly 60/hr for hours 00-19 UTC; hours 20-23 have ZERO rows (4h absent, unexplained). One row/min -> likely a sample, not all requests.
Covered period p95 = 392.2ms (95% bootstrap CI 374.9-409.4); median 200; max 708.7; 14/1200 (1.2%) >500ms. Hourly p95 max 460.2 (hr 15) - never >500.
Outcome: CONTRADICTED for 00:00-19:59 UTC (500 is far outside CI). Not adequate for hours 20-23.
Sensitivity: for full-day p95 >500 with 1440 rows, need >=72 rows >500; 14 exist, so the missing ~240 would need >=58 (~24%) above 500 - far from the 1.2% observed, but cannot be excluded (source completeness UNKNOWN).
Answer: claim not supported by this data; cannot be ruled out for 20:00-23:59.
