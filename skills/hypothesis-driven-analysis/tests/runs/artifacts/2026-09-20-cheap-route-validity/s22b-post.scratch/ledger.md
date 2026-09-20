# Mini ledger: "Q2 2026 revenue exceeded $1M"

Route: mini (one stated, non-causal claim, no rival explanation). Collection is a local file, so no costly-collection plan is needed.

Claim: total amount_usd of orders dated 2026-04-01..2026-06-30 exceeds $1,000,000.
Prediction: if the claim holds, the sum over the file exceeds $1M. If the file is complete, a sum below $1M contradicts the claim.
Probe(s): sum, row count and id/timestamp continuity of orders.csv; a day-by-day coverage check (Apr 1 to Jun 30) against the calendar; a bound on what the missing tail would have to contain.
Data validity:
- 10,000 rows. order_id is unique and contiguous (O500001..O510000, step 1, no gaps). Timestamps are monotonic. There are no nulls and no non-positive amounts.
- Coverage: the last row is 2026-06-11T09:55Z. Nothing exists for the rest of Jun 11 or Jun 12-30 (about 19.6 days of the 91-day quarter).
- Row count is exactly 10,000, a round number, which fits an export row cap. The evidence that fits truncation is the round count plus contiguous ids ending mid-day. There is no export contract or sentinel row, so the cause is not confirmed.
- Days Apr 1..Jun 10 are all present and complete. Daily counts run 128-152 and daily revenue runs $10.5k-$14.1k. Jun 11 is partial (65 orders).
- Completeness semantics: the missing tail is "export incomplete", not "no orders". This is unconfirmed, so the quantity is treated as a lower bound.
- No joins. Amount semantics (refunds, cancellations, tax, currency) are unknown. The file has no status column.
Stop condition: settled if the covered rows alone exceed $1M. Otherwise settled only conditionally, by what the missing tail would need to contain.
Outcome: NON_DISCRIMINATING on the file as given. Covered total is $862,691.37, below $1M, but the file is truncated so the sum does not refute the claim. The claim is consistent with the data only under an assumption about the missing tail (see Answer).
Answer:
- Covered total (Apr 1 to Jun 11 09:55Z): $862,691.37. April $365,213.67, May $371,113.73, June 1-11 partial $126,363.97.
- Shortfall to $1M: $137,308.63. That is about 11.4 average days of revenue, or 13.1 days at the lowest full-day revenue seen ($10,515).
- Missing window is about 19.6 days. If it resembles the covered rows (weekly totals steady at $82k-$87k across 10 full weeks), the quarter is about $1.10M. Even at the worst full-day revenue seen it is about $1.07M.
- Conditional verdict: probably true, but not established from this file. It rests on the assumption that Jun 11-30 looks like Apr-early Jun. The covered rows do not bound absent ones.
- To confirm: re-export Q2 without the row cap, or get a finance/DB total for Q2.
