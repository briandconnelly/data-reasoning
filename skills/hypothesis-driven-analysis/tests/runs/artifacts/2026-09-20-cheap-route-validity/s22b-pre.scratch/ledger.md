# Mini ledger — "Q2 2026 revenue exceeded $1M"
Claim: revenue (sum of amount_usd) for orders 2026-04-01..2026-06-30 exceeded $1,000,000.
Prediction: if true, the Q2 export sums to > $1M; if false, sums to <= $1M with a complete export.
Probes: read-only local file orders.csv (10,000 rows): sum, row/ID/timestamp coverage, per-day counts.
Data validity: 10,000 unique rows, IDs O500001-O510000 contiguous (no internal gaps), timestamps sorted, no null/<=0 amounts. Export ENDS 2026-06-11T09:55Z mid-day (day has 65 orders vs ~140 typical) and row count is exactly 10,000 -> consistent with a row-cap truncation. Jun 11 09:55 - Jun 30 absent = ~19.6 days. Completeness semantics: export incomplete (tail missing); UNKNOWN whether any cap/contract exists, direction of missing data = additive (more orders, not fewer).
Result: sum in file = $862,691.37 (Apr 365,213.67 / May 371,113.73 / Jun 1-11 partial 126,363.97).
Extrapolation (not evidence, labelled): at Apr/May/Jun-1-10 daily rates (~12.2k/12.0k/12.1k) -> ~$1.10M total. $137.3k more needed = ~11.4 days at recent rate vs 19.6 days missing.
Outcome: NON_DISCRIMINATING on the file alone (lower bound $862.7k < $1M; claim not testable from a truncated export).
Answer: cannot be confirmed from this file; likely true if orders continued at the same rate, needs the full Jun 11-30 data.
