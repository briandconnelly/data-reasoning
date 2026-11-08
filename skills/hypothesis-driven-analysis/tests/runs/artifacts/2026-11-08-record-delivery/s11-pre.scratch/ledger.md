# Mini ledger: checkout p95 > 500ms on 2026-07-15?
Claim: checkout p95 latency exceeded 500ms on 2026-07-15 (per-request latency_ms, UTC day, all rows in S1).
Prediction: holds -> day-level p95 > 500 (95% order-statistic CI lower bound > 500 ideally); fails -> p95 <= 500 with the claim value outside the CI. Also checked: hourly p95 (if claim means any window), coverage.
Probes: (1) orientation: row count, time span, hourly coverage, nulls/dups; (2) day p95 + 95% order-statistic CI; (3) hourly p95 and max; (4) share of requests >500.
Stop condition: day p95 and CI computed and coverage assessed; done.
Source S1: data/s11-mini/checkout_latency.csv (read-only local). Completeness semantics: UNKNOWN - no export contract or independent counter to tell absent minutes from unrecorded.
Outcome: (filled below)
Probe results (S1): 1200 rows, 1200 unique ids, no missing, all dated 2026-07-15, exactly 60 rows/hour for hours 00-19 (one per minute); NO rows for 20:00-23:59 (4h absent).
Day p95 = 392.2ms; 95% order-statistic CI [378.1, 410.4] (ranks 1125-1154 of 1200); 500 is outside CI. p99 = 505.7; max 708.7; 14/1200 (1.2%) >500. Max hourly p95 = 460.2 (hour 15); no hour >500.
Outcome: CONTRADICTED for hours 00:00-19:59 UTC. Coverage caveat: 20:00-23:59 absent (completeness UNKNOWN).
Answer: claim not supported by the data present; cannot cover the missing 4h.
