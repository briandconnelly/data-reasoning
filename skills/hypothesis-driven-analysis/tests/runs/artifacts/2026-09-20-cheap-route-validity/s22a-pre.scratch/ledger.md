# Mini ledger — Enterprise Q2 2026 revenue > $1M?
Claim: Enterprise-segment revenue for 2026-04-01..2026-06-30 exceeded $1,000,000.
Prediction: Sum of amount_usd over Q2 orders whose account is Enterprise > 1,000,000 if true; <= 1,000,000 if false.
Orientation (structure only): accounts.csv has 70 rows / 60 distinct account_ids (valid_from -> SCD-style history; 10 accounts have >1 row), so a naive orders JOIN accounts fans out orders. Orders: 2077 rows, unique order_id, 2026-01-01..2026-06-30, no nulls/non-positive amounts, every account_id present in accounts. Segment attribute is checked for consistency across versions of an account.
Probes: (1) segment per account is unique across versions? (2) revenue via one-row-per-account join, (3) naive fan-out join to show the size of the trap, (4) bracket: as-of-order-date versioning gives same result if segment never changes; sensitivity if it did.
Stop condition: settled when the deduplicated total is clearly on one side of $1M and segment mapping is unambiguous.

Results:
- Segment is single-valued per account across all versions (0 accounts change segment), so the mapping is unambiguous; versions differ only in region/owner.
- Deduplicated (one row per account): Q2 Enterprise = $925,797.78 over 199 orders (Mid-Market $542,840.57; SMB $223,120.39; total $1,691,758.74 = ledger total, 1050 orders, no loss/duplication).
- Naive join to accounts.csv (fan-out): Enterprise = $1,227,245.07 (inflated $301,447 / 33%) — this is the source of a >$1M figure.
Outcome: CONTRADICTED (deterministic sum over the complete ledger; no sampling uncertainty; shortfall $74,202 = 7.4% below $1M).
Answer: Not true. Enterprise Q2 revenue is $925.8K.
