# Mini ledger (written before probing relationships)
Claim: checkout p95 latency exceeded 500ms on 2026-07-15 (primary estimand: p95 of latency_ms over all requests in the UTC day; hourly p95 as secondary reading, since the claim doesn't say which grain).
Prediction: holds -> daily p95 > 500 (95% order-statistic CI entirely above 500). Fails -> daily p95 CI entirely below 500. CI straddling 500 -> NON_DISCRIMINATING.
Probes: (1) orientation: row count, time range, minute coverage by hour vs expected 1/min schedule, dup request_ids, nulls/non-numeric; (2) p95 + CI overall; (3) hourly p95.
Data validity: TBD
Stop condition: interval read against 500 at precommitted 95%; or coverage gap that could flip the answer -> conditional/NON_DISCRIMINATING.

## Results
Data validity: 1200 rows, 1/min, no gaps, no dup request_ids, no nulls, timestamps monotonic, all 2026-07-15 UTC. Coverage matrix (hour x count): hours 00-19 each 60 rows; hours 20-23 ABSENT (export ends 19:59Z). No independent denominator -> whether 20-23 had no traffic, was unrecorded, or export truncated is UNKNOWN. Exactly 1 row/min also suggests a sample, not all requests (unverified). No joins. Timezone of "yesterday" unstated (UTC assumed).
Probe results: covered-rows p95 = 392.2ms; 95% order-statistic CI [378.1, 410.4]; 14/1200 (1.2%) >500ms; max 708.7. Hourly p95 range 320.8-460.1 (n=60/hr, coarse); no hour >500.
Crossing requirement: for a 1440-row day to have p95>500, need >72 rows >500; covered has 14, so >=59 of the 240 missing rows (~25%) would have to exceed 500 vs 1.2% observed (max 3.3%/hr).
Outcome: CONTRADICTED on covered 20h (CI entirely below 500), conditional on missing 20:00-23:59Z resembling covered hours.
