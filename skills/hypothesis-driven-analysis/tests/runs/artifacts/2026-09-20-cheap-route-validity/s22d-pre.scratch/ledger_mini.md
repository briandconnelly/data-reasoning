# Mini ledger: "Q2 2026 revenue exceeded $1M"

Route: mini (one stated claim, no rival explanations). Non-costly collection (local 11,971-row CSV); no authorization issues.
Source: data/c-hole/orders.csv, export of Q2 orders (provenance as stated by user; no export contract available).

Claim: total revenue for orders 2026-04-01..2026-06-30 exceeds $1,000,000.
Prediction: sum(amount_usd) > 1,000,000 if it holds; <= 1,000,000 if it fails. Also precommitted: the file must have no region x day holes, else the sum is a lower bound of unknown completeness.
Probes: (1) row/dup/null/sign/range checks; (2) sum in total and by month; (3) coverage matrix day x region across all 91 days x 3 regions; (4) order_id contiguity; (5) size of any hole, using the region's own daily rate outside the hole.
Stop condition: sum computed and coverage matrix checked; if a hole exists, bound its size.

Results
- 11,971 rows, no nulls, no duplicate ids/rows, all amounts positive ($12.83-$420.46), all timestamps 2026-04-01..2026-06-30 UTC.
- Sum = $972,510.46 (Apr 337,536; May 350,915; Jun 284,060). Shortfall vs $1M: $27,490.
- Coverage: every day has orders, but EMEA has ZERO orders on 2026-06-03..2026-06-16 (14 consecutive days). AMER/APAC normal in the same days (AMER 4,935/day, APAC 2,497/day vs 5,066/2,582 elsewhere). June total is low (3,471 orders vs 4,146/4,354).
- EMEA elsewhere: 44.8 orders, $3,631/day (daily range $2,625-$5,080).
- order_id is contiguous (700001..711971, no gaps) and monotone in time -> no id gap marks the hole; ids may be assigned/renumbered at export, so this does not show that no orders occurred. Completeness semantics of an absent record: UNKNOWN (event absent, unrecorded, or export incomplete not separable with this file).
- Gap fill estimate (if EMEA orders occurred at normal rate): 14 x $3,631 = ~$50.8k; using EMEA's lowest observed day, $36.7k; highest, $71.1k. Implied total ~ $1.009M-$1.044M (point ~$1.023M). Any fill above $27.5k crosses $1M.

Outcome: as exported, CONTRADICTED ($972.5k < $1M). But the export fails the coverage precondition, so this is a lower bound with unknown completeness, not a settled Q2 total.
Answer: Not on this file; the file is likely incomplete, and if the missing EMEA days are real orders the claim is probably true. Can't settle from this data alone.
