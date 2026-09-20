# Mini ledger (preregistered before totals computed)
Claim: Revenue (sum amount_usd) for 2026 Q2 (2026-04-01..2026-06-30 UTC) exceeded $1,000,000.
Prediction: If true, sum of amount_usd over valid, unique Q2 orders > 1,000,000. If false, <= 1,000,000.
Probes: (1) schema/nulls/dupe order_id/negative or zero amounts/out-of-window ts; (2) day x region coverage matrix vs expected schedule (every day of Q2 present, per region); (3) sum, with sensitivity to dupes/refunds; (4) order_id sequence contiguity (independent denominator: O700001..O711971 => 11971 expected).
Data validity: pending.
Stop condition: total computed on validated rows and coverage gaps quantified against $1M threshold; or declared unresolved with what missing rows would need to contain.
Outcome: pending.

## Results (2026-09-20)
Probes run on orders.csv (11,971 rows, single source, provenance: user-supplied Q2 export of orders DB; no export contract/row-count manifest supplied).
- Schema: no blanks, no dup order_id, no nonpositive amounts, all ts within 2026-04-01..06-30 UTC. Sum amount_usd = $972,510.46 (Apr 337,536 / May 350,915 / Jun 284,060).
- order_id contiguous O700001..O711971, 0 gaps (but ids could be assigned/renumbered at export; does not prove no rows were lost upstream).
- Coverage matrix day x region (91 days x 3 regions): 14 empty cells, all EMEA, 2026-06-03..06-16 contiguous. AMER/APAC normal in that window (non-EMEA $7,432/day vs $7,647 elsewhere). EMEA otherwise 44.8 orders/day, $3,631/day (min 2,625, max 5,080), ~32% of revenue.
- Expected EMEA revenue in gap ~ $50.8k (bootstrap 95% of 14-day sum: 47.6k-54.2k). Shortfall to $1M = $27,489.54 (~54% of typical EMEA 14-day revenue).
Source completeness semantics: UNKNOWN. Readings live: (a) EMEA truly had no orders (outage/site down/region paused), (b) EMEA orders unrecorded, (c) export incomplete. Nothing supplied discriminates them; own missingness pattern cannot establish completeness.
Data validity: coverage hole in EMEA 06-03..06-16 unresolved.
Outcome: NON_DISCRIMINATING. Recorded total ($972.5k) is below $1M, but missing EMEA rows needing only $27.5k (well within a normal 14-day EMEA haul of ~$50.8k) would flip it; conditionally, if the gap is lost data of typical size, total ~ $1.023M (range ~$1.020-1.027M).
