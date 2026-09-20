Claim: Q2 2026 (Apr 1-Jun 30) revenue exceeded $1M (sum of amount_usd, orders.csv).
Prediction: file total > $1,000,000 if it holds; <= if it fails.
Probe(s): sum amount_usd; dup/null/amount checks; coverage matrix day x region (and week x region); order_id contiguity.
Data validity: 11,971 rows, no dup ids, no nulls, amounts 12.83-420.46, ids contiguous 700001-711971 and ordered by ts, all 91 days present overall. BUT EMEA has zero orders 2026-06-03T00:00 to 2026-06-17T00:39 (~14 days); AMER/APAC steady (~30-60/day) through it, EMEA runs ~45/day otherwise. Completeness semantics of an absent record: UNKNOWN (contiguous ids fit a renumbered export or a true zero; no export contract/sentinel/second source to separate them). No join.
Stop condition: settled if total is clearly on one side of $1M irrespective of the EMEA hole; else data cannot settle it.
Outcome: NON_DISCRIMINATING. File total $972,510.46 (Apr 337,536; May 350,915; Jun 284,060), $27,490 short. EMEA hole would have to hold >= $27.5k to cross; a typical 14-day EMEA window in the covered rows is ~$51k (extrapolated), so crossing is well within what the covered rows show.
Answer: Not confirmed by this file ($972.5k < $1M) but not refuted; needs the EMEA Jun 3-17 gap explained.
