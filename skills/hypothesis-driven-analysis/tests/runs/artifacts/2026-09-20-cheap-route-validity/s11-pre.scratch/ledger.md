# Mini ledger: "checkout p95 exceeded 500ms on 2026-07-15"

Route: mini (one stated claim, non-causal, no rivals). Source S1: checkout_latency.csv (local file, no collection cost).
Orientation (schema/coverage only, before any latency stats): 1200 data rows, 1 row/min, first 2026-07-15T00:00Z, last 2026-07-15T19:59Z, so 20:00-23:59Z not in file.

Claim: p95 of per-request checkout latency_ms on 2026-07-15 exceeded 500 ms.
Estimand (precommitted): p95 of latency_ms over all requests on 2026-07-15 (UTC, timestamps as given), with 95% interval (order-statistic / bootstrap). Secondary reading if whole-day is not the intended grain: p95 per clock hour.
Prediction: if true, sample p95 > 500 and the 95% interval sits above 500; if false, p95 < 500 and interval sits below 500. Interval straddling 500 => NON_DISCRIMINATING.
Probes: (1) coverage: rows per hour, dupes, nulls, non-numeric; (2) whole-day p95 + CI; (3) hourly p95 + count of hours >500; (4) tail inspection (max, count >500).
Stop condition: probes 1-4 done; settled when interval excludes 500 for the covered window AND the uncovered window (20:00-23:59) cannot plausibly reverse it, else state limit.
Completeness semantics S1: UNKNOWN - no export contract or independent request counter; missing 20:00-23:59Z could be export cutoff, outage, or no traffic; file's own pattern cannot discriminate.
Outcome: NOT_TESTED

## Results (S1, run after the ledger above was written)
Coverage: 1200 rows, all 2026-07-15, 60 rows in each hour 00-19 UTC, 0 rows in hours 20-23. No nulls, no duplicate ids/timestamps, no non-positive latencies.
Whole-covered-window p95 = 392.2 ms (p50 200.0, p90 334.7, p99 505.7, max 708.7). 14/1200 (1.17%) requests >500 ms.
95% CI for p95: order-statistic 378.1-410.4; bootstrap (5000) 374.9-409.4. 500 is outside, ~90 ms above the upper bound.
Hourly p95 (60 req/hour): max 460.2 (hour 15); no hour has p95 > 500. (Hourly p95 on n=60 is noisy; descriptive only.)
Reversal bound: for the 20:00-23:59 gap to lift the full-day p95 over 500, ~58+ of ~240 requests (>=24%) would need to exceed 500 ms, versus 1.2% observed in the covered hours.
Outcome: CONTRADICTED for the covered 00:00-19:59Z window. For the claim as stated (whole day), NON_DISCRIMINATING in the strict sense - the interval covers 20 of 24 hours and S1 completeness for the missing 4 hours is UNKNOWN.
Answer: not supported by the data; p95 ~392 ms, CI 378-410, no covered hour above 500. Cannot exclude the missing 4 hours or a different day-boundary (local tz).
