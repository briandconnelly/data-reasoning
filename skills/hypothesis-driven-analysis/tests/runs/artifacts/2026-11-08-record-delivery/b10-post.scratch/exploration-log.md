# Exploration: profile of the Northgate Clinic account, Jan–Jun 2026

## Frame

- Goal: orientation and entity record for Northgate Clinic (profile route; no lead-seeking, no reservation).
- Scope: entity = Northgate Clinic. Identifier: accounts.csv resolves it to ACC-1042 (2025-01-01..2026-03-31) and ACC-1077 "Northgate Health Partners (formerly Northgate Clinic)" (from 2026-04-01). Both ids are in scope. Sources: accounts, billing, contract_status, plan_changes, tickets in data/b10-entity/. Window 2026-01..2026-06. Units USD, billed_volume.
- Effort budget: 6 tool calls of analysis (data is 5 tiny files read in full).
- Stop rule: stop at budget or when the entity record is written; anything interesting is noted, not chased.
- Confirmation reservation: none (profile route takes none).

## Orientation record

| id | Origin (file, query, system) | Acquired | Notes |
| --- | --- | --- | --- |
| S1 | accounts.csv (user-provided extract) | 2026-11-08 | 5 accounts, validity windows |
| S2 | billing.csv | 2026-11-08 | 22 rows, account x month |
| S3 | contract_status.csv | 2026-11-08 | 20 rows, ends 2026-05 for all accounts |
| S4 | plan_changes.csv | 2026-11-08 | 2 events |
| S5 | tickets.csv | 2026-11-08 | 38 tickets |

- Schema and grain: billing one row per account-month; contract_status one row per account-month; tickets one row per ticket; plan_changes one row per event.
- Quality: no duplicate keys seen; no nulls beyond accounts.valid_to (open-ended). No sentinels seen. Entity split across two ids by a rename; a filter on the name or on ACC-1042 alone silently drops April onward.
- Coverage: billing for the entity: 1042 has Jan, Mar; 1077 has Apr, May. Missing entity-months: Feb (1042 has contract status paused, no billing row) and Jun (no billing, no status, no tickets under either id). Other three accounts have billing in all six months, so June absence is specific to this entity. contract_status has no June row for any account (source ends May). Tickets have no independent denominator: unverifiable.
- Absence semantics: billing Feb: UNKNOWN (paused status co-occurs, but whether a paused month is unbilled or the row was dropped is not settled by these files). Billing Jun for 1077: UNKNOWN (no status for June to compare; other accounts present, so not a general export gap, but no evidence discriminates no-billing from unrecorded). Tickets: UNKNOWN (absence of tickets is not shown as no support activity). The link ACC-1042 -> ACC-1077 rests on the name text in accounts.csv alone.
- Instrument caveats: README gives no export contract; contract_status is from a different system than billing.

## Entity record (entity profile only)

- Entity and identifier: Northgate Clinic = ACC-1042 through 2026-03-31; renamed Northgate Health Partners = ACC-1077 from 2026-04-01.
- Descriptive facts: billing 2026-01 standard 1840 units $772.80; 2026-03 enterprise-annual 1910 units $592.10; 2026-04 enterprise-annual 1120 units $347.20 (1077); 2026-05 1085 units $336.35 (1077). Implied $/unit: 0.42 (Jan), 0.31 (Mar, Apr, May). Total billed in window $2,048.45 across 4 months. Tickets 6: ACC-1042 on 01-08 feature-request, 03-11 feature-request, 03-26 integration; ACC-1077 on 04-01 billing-question, 04-04 billing-question, 05-25 outage-report.
- Change over time: (1) contract status paused in 2026-02, active 2026-03. (2) plan changed standard -> enterprise-annual effective 2026-03-01 (plan_changes). (3) account renamed/re-keyed to ACC-1077 effective 2026-04-01. (4) billed volume 1910 in March, 1120 in April (a fall coinciding with the re-key; reading it as a real fall vs a partial carry-over is unresolved). (5) per-unit rate fell from 0.42 to 0.31 from March. (6) no records of any kind in June. Attribution of any of these to another is unresolved.

## Looks register

| id | Family | Examined | Comparisons exposed | Note |
| --- | --- | --- | --- | --- |
| (none) | profile route: no Explore looks | | | |

## Leads

| id | Statement (associational) | Class | Evidence | Search context | Alternatives noted | Cheapest confirming test | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | Entity split across ACC-1042 and ACC-1077; single-id views understate it | data-quality | Orientation | n/a — found in Orient | none | confirm mapping with account owner | reported |
| D2 | No Feb billing row and no June records for the entity | data-quality | Orientation | n/a — found in Orient | paused contract; churn; export gap | ask billing owner for Feb and Jun runs | reported |

## Amendments

- (none)
