# Mini ledger (route: mini — one stated claim, no rival)
Claim: checkout p95 latency_ms exceeded 500ms on 2026-07-15 (UTC day; timezone unstated in claim, timestamps are Z).
Prediction: if true, day-level p95 of latency_ms > 500; if false, <= 500. Interval: 95% order-statistic CI on the day p95 (committed before reading). Claim's estimand = whole-day p95 (not hourly).
Probe(s): (1) coverage check by hour (rows/hour, nulls, dupes, date range); (2) day p95 + order-statistic CI; (3) hourly p95 as context only.
Stop condition: CI entirely above or below 500 => settled; CI straddles 500 or coverage hole could move it => NON_DISCRIMINATING.
Source S1: data/s11-mini/checkout_latency.csv (1200 rows).

## Results (probe.py, S1)
Coverage: all 1200 rows are 2026-07-15 00:00–19:59Z, exactly 1/min, 60 rows every hour 00–19, no dupes/blanks. NO rows for 20:00–23:59Z (240 expected at this cadence). Completeness semantics S1: UNKNOWN — no export contract/independent counter; the file's own pattern cannot say whether 20–23h were unrecorded, unexported, or the file was cut before the day ended.
Covered-window p95 = 392.2ms; 95% order-statistic CI [378.1, 410.4] (n=1200). Max 708.7; 14 rows >500 (1.2%). Hourly p95 max 460.1 (hour 15); no hour's p95 >500.
Sensitivity: for the full-day (1440-row) p95 to exceed 500, >=72 rows must be >500; 14 present, so the missing 4 hours would need >=58/240 (24%) above 500 vs 1.2% observed elsewhere.
Outcome: CONTRADICTED for 00:00–19:59Z (CI entirely below 500). Full-day claim: not settled for 20–24h; selection-sensitive, direction unknown.
