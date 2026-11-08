# Mini ledger
Claim: checkout p95 latency exceeded 500 ms on 2026-07-15 (day-level p95, all requests).
Prediction (necessary): the day's p95 > 500 ms; refuted if the 95% interval for p95 lies below 500.
Probes: day p95 (nearest-rank) + 95% bootstrap CI (5000 resamples, seed 1); hourly p95; coverage check.
Outcome: p95 = 392.2 ms, 95% CI [374.7, 409.4] -> CONTRADICTED (discriminating: 500 is far outside the CI). Only 14/1200 (1.2%) requests >500 ms; max 708.7.
Hourly p95 max 460.1 (15:00, n=60); none >500.
Limits: file has 1200 rows, exactly 60/hour for 00:00-19:59 UTC; nothing after 20:00 UTC. Completeness semantics UNKNOWN (export may be truncated or the day not finished). Timezone assumed UTC.
