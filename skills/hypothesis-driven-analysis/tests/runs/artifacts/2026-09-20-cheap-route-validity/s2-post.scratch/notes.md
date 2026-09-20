# Median June order value (route: direct)
- Source: data/orders.csv, 268 rows, no blanks/dup ids, order_id contiguous o00001-o00268.
- Coverage: timestamps span 2026-06-01 .. 2026-06-14 only; 2026-06-15..30 absent. Completeness semantics for absent days: UNKNOWN (no export contract/sentinel).
- Median amount over all 268 rows (June 1-14): 76.36 (min 18.37, max 139.74). Currency unstated.
- Client version 3.4.0 through Jun 9, 3.4.1 from Jun 10 (nothing further checked).
