Claim: Enterprise-segment revenue (sum of amount_usd) for 2026-04-01..2026-06-30 exceeded $1,000,000.
Prediction: if true, Enterprise Q2 sum > 1.0M; if false, <= 1.0M.
Probe(s): (1) coverage/uniqueness checks on both files; (2) Enterprise Q2 sum via account->segment mapping; (3) same via naive join and via as-of (valid_from) join to compare.
Data validity: orders.csv 2077 rows, order_id unique, Jan-Jun 2026 all six months present (314-362 orders/mo), no nulls, no amount <= 0, every order account_id is in accounts.csv. Ledger stated complete by user (not independently verifiable here). accounts.csv is versioned (70 rows / 60 accounts; 10 accounts have 2-3 versions by valid_from, changing region/owner). A naive join repeats orders for those accounts (fan-out): Enterprise Q2 -> 260 rows instead of 199. Segment never differs across versions of an account, so account->segment is unambiguous; deduplicated and as-of joins agree.
Stop condition: sum on a fan-out-free join is clearly on one side of 1.0M.
Outcome: CONTRADICTED. Enterprise Q2 = $925,797.78 over 199 orders (Apr 300,965.51; May 301,056.40; Jun 323,775.87). Naive join gives $1,227,245.07 (260 rows) - inflated by fan-out. Results in work/results.txt.
Answer: No. Correct figure is ~$925.8K, ~$74.2K (7.4%) under $1M. The >$1M number is reproduced only by the duplicating join.
