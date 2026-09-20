# Mini ledger: did Q2 2026 revenue exceed $1M?

Route: mini (one stated claim, no rival explanations). Source S1: data/b-truncated/orders.csv (10,000 rows + header).

Claim: Revenue for 2026 Q2 (Apr 1 - Jun 30) exceeded $1,000,000, taking revenue = sum(amount_usd) of orders.
Prediction: If it holds, the covered rows plus a plausible remainder sum above $1M. If it fails, the full quarter sums below $1M.
Probe(s): (1) sum, row count, date range, order_id contiguity; (2) per-month and per-day counts and revenue; (3) shortfall vs $1M against the observed daily-revenue range.
Data validity:
- Coverage: rows run 2026-04-01T00:06Z to 2026-06-11T09:55Z, sorted by time. Nothing from Jun 11 10:00 to Jun 30 (~19.59 days, ~21% of the quarter). Jun 11 is partial (65 orders, $5,515.56).
- Row count is exactly 10,000, and order_ids O500001-O510000 are contiguous with no gaps, so the file is a cut-off prefix (cap or truncation), not a sample with holes. Ending mid-day is consistent with a row limit.
- Integrity: 10,000 unique ids, no blanks, no non-positive amounts, no duplicate (customer, ts, amount).
- Source completeness semantics: S1: UNKNOWN - the file has no export contract or sentinel rows, and its own pattern (a round 10,000 cap) cannot tell "orders stopped on Jun 11" from "export cut off". Nothing here says whether amount_usd is gross or net of refunds/cancellations.
- Coverage baseline: none independent (no expected-order count or ledger total); coverage checked only against the calendar quarter.
Covered total: $862,691.37 (Apr $365,213.67 / May $371,113.73 / Jun 1-11 partial $126,363.97). Shortfall to $1M: $137,308.63.
Crossing requirement: the missing 19.59 days must average >= $7,010/day. Full covered days ($10,515-$14,069, mean $12,073) never fell that low, and no 20-day window sums below $237.6k, vs $137.3k needed.
Stop condition: settled if the covered rows alone cross $1M (they do not) or the shortfall is checkable; otherwise state the conditional verdict with the assumption.
Outcome: NON_DISCRIMINATING on the covered data alone (they total $862.7k < $1M). CONSISTENT with the claim only conditionally, on the assumption that the missing Jun 11-30 orders exist and resemble Apr 1-Jun 11 (S1, probes 1-3).
Answer: Not verifiable from this file. Probably true if the export was just cut off (projected ~$1.10M; even at the lowest observed daily rate ~$1.07M), false if orders really stopped Jun 11 (then $862.7k).
