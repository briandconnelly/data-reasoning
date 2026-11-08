# Mini ledger
Claim: checkout p95 latency > 500ms on 2026-07-15 (non-causal, single claim; route: mini).
Prediction: if true, p95 (nearest-rank) of that day's latency_ms > 500.
Probes: overall p95; bootstrap 95% CI (5000 resamples, seed 1, level committed before reading); hourly p95 for sanity; coverage check.
Outcome: p95 = 392.2ms; CI [374.7, 409.4]; 500 outside the interval -> CONTRADICTED on covered data. 14/1200 requests >500, max 708.7.
Data validity: 1200 rows, one per minute, 00:00-19:59Z only; 20:00-23:59Z absent (unverified whether unrecorded or no traffic); 1 row/min suggests a sample, not all requests.
