# Mini ledger: "checkout p95 > 500ms on 2026-07-15"
Claim: p95 of checkout latency_ms over 2026-07-15 (UTC, per Z timestamps) exceeded 500 ms.
Prediction (precommitted): if true, the day's p95 > 500, i.e. >5% of requests (>=72 of 1440 at 1/min) above 500 ms.
Probes: p95 (linear and nearest-rank) over deduped rows; 95% order-statistic and bootstrap intervals; per-hour p95; coverage by hour.
Data validity: 1200 rows, unique ids, no missing values, all dated 2026-07-15, exactly 1 row/min for 00:00-19:59Z (60/hour). Nothing for 20:00-23:59Z (240 expected minutes absent). Completeness semantics of the absence: UNKNOWN (no export contract/sentinel; file's own pattern cannot settle it).
Outcome (observed window): p95 = 392.2 ms; 95% order-stat CI [378.1, 410.4]; bootstrap [375.0, 407.7]. 14/1200 (1.2%) >500 ms; max 708.7. Highest hourly p95 = 460.2 (15h) on 60 pts; the 19h bucket had p95 437 and a 708.7 max. CONTRADICTED for 00:00-19:59Z (500 far outside CI).
Sensitivity: to push the full-day p95 over 500 the missing 240 requests would need >=58 (24%) above 500 ms, versus 1.2% observed, so the claim is only possible if the missing hours contained a severe incident. Not testable here.
Script: b.py (stdlib only; pandas/numpy not installed).
