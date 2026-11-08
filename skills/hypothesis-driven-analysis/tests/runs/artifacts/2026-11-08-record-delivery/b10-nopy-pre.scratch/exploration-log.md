# Exploration (profile route, entity): Northgate Clinic account, 2026-01..2026-06

## Frame-lite
- Scope: entity "Northgate Clinic". Identifier resolved via accounts.csv: ACC-1042 "Northgate Clinic" (valid 2025-01-01..2026-03-31) and ACC-1077 "Northgate Health Partners (formerly Northgate Clinic)" (valid from 2026-04-01). Both treated as the entity (recorded decision: name-resolution widened to the successor id; other accounts used only as context).
- Sources: accounts, billing, contract_status, plan_changes, tickets (all in data/b10-entity). Timeframe 2026-01..06.
- Effort budget: 6 tool calls of analysis (files are tiny; read in full). Stop rule: budget or orientation + entity record complete. No chasing; observations only. No reservation (profile route).

## Orientation record
| id | Origin | Notes |
| S1 | accounts.csv | 5 accounts; 1042 closed 03-31, 1077 opens 04-01 |
| S2 | billing.csv | 22 rows; account-month grain |
| S3 | contract_status.csv | 20 rows; months 01-05 only |
| S4 | plan_changes.csv | 2 events |
| S5 | tickets.csv | 38 tickets |
- Quality: no duplicates seen, no nulls except accounts.valid_to (open-ended). No sentinels.
- Coverage: billing 1042: Jan, Mar only (Feb missing); 1077: Apr, May (June missing) while all other accounts have Jan-Jun. contract_status ends 2026-05 for all accounts (June absent everywhere); 1042 has no Apr+ rows (consistent with accounts window). 
- Absence semantics: 1042 Feb billing absent while status = paused (contracts system) -> consistent with no billing during pause, but billing source itself can't prove it; pause is from a different system, so partial evidence. 1077 June billing absent: UNKNOWN (event absent / unrecorded / export incomplete) - other accounts have June, contract_status has no June, no ticket in June. 1042 Apr-Jun absent: explained by account window end in accounts.csv (id change), not by inactivity.
- Caveats: README claims billing is "one row per account per billed month" yet gaps exist. Billing volume units undefined.

## Entity record
- ACC-1042: Jan standard 1840 vol $772.80 (0.42/unit); Feb paused, no bill; Mar enterprise-annual 1910 vol $592.10 (0.31/unit). Plan change standard->enterprise-annual effective 2026-03-01.
- ACC-1077: Apr 1120 vol $347.20; May 1085 vol $336.35 (0.31/unit, enterprise-annual); June no billing row. Status active Apr, May.
- Combined monthly billed: Jan 1840/$772.80; Feb none; Mar 1910/$592.10; Apr 1120/$347.20; May 1085/$336.35; Jun none.
- Tickets: ACC-1042: T-5033 feature-request 01-08, T-5034 feature-request 03-11, T-5035 integration 03-26. ACC-1077: T-5036 billing-question 04-01, T-5037 billing-question 04-04, T-5038 outage-report 05-25. 6 total.
- Change over time (dated): 2026-02 contract status paused; 2026-03-01 plan change to enterprise-annual; 2026-03 status active again; 2026-03-31 ACC-1042 validity ends; 2026-04-01 ACC-1077 begins (renamed); billed volume 1840 (Jan) -> 1910 (Mar) -> 1120 (Apr) -> 1085 (May); per-unit rate fell 0.42->0.31 from March. Two billing-question tickets on 04-01 and 04-04 are the first tickets under the new id. Attribution of any of these to each other: unresolved.
