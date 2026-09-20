# Mini ledger: Enterprise revenue > $1M in 2026 Q2?
Claim: Enterprise-segment revenue (sum amount_usd, orders dated 2026-04-01..2026-06-30) exceeded $1,000,000.
Prediction: if true, Enterprise Q2 sum > 1.0M; if false, <= 1.0M. Segment attribution must be one segment per order (join fanout guard: accounts has valid_from, so may hold several rows per account_id).
Probes: (1) accounts key uniqueness + segment history; (2) orders coverage by month; order_id uniqueness; orphan accounts; (3) Q2 Enterprise sum under join variants (as-of-order-date, latest, naive join) with reconciliation to Q2 total.
Data validity: (filled after probes)
Stop: claim settled once sum under the defensible segment attribution is computed, with sensitivity to attribution choice.
Outcome / Answer: (below)

## Results (probes run 2026-09-20; sources S1 orders.csv 2077 rows, S2 accounts.csv 70 rows/60 accounts)
Data validity: orders: order_id unique, no null/nonpositive amounts, every calendar day present Apr/May/Jun (30/31/30), all order accounts found in accounts. Ledger stated complete by user (not independently verifiable). accounts is a history table (valid_from): 10 accounts have 2-3 rows, so a naive join repeats orders (fanout). Segment never changes within an account (0 multi-segment accounts; only region/owner change), so segment attribution is unambiguous; dedupe to one row per account. Reconciliation: Q2 total 1,691,758.74 = Ent 925,797.78 + Mid 542,840.57 + SMB 223,120.39 (all 1,050 orders, none dropped or repeated). As-of-order-date join gives identical Enterprise figure.
Outcome: CONTRADICTED. Enterprise Q2 = $925,797.78 (199 orders), below $1M by $74,202. Naive (fanout) join gives $1,227,245.07 (260 rows) -- likely origin of the claim.
