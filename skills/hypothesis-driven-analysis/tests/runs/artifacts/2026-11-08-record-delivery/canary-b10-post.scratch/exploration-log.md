# Exploration: profile of the Northgate Clinic account (entity profile, Jan-Jun 2026)

## Frame

- Goal: descriptive entity profile; no lead-seeking (profile route, Frame-lite).
- Scope: entity "Northgate Clinic". Resolves to ACC-1042 (accounts.csv, valid 2025-01-01..2026-03-31) and ACC-1077 ("Northgate Health Partners (formerly Northgate Clinic)", valid from 2026-04-01). Sources: billing, contract_status, plan_changes, tickets, accounts. Window 2026-01..2026-06. Other accounts used only as a coverage denominator.
- Effort budget: 6 tool calls (reads/queries).
- Stop rule: stop at budget or once all five sources are read.
- Confirmation reservation: none (profile route takes none).

## Orientation record

| id | Origin | Acquired | Notes |
| --- | --- | --- | --- |
| S1 | data/b10-entity/accounts.csv | 2026-11-08 | 5 rows |
| S2 | billing.csv | 2026-11-08 | 22 rows, one per account-month |
| S3 | contract_status.csv | 2026-11-08 | 20 rows, Jan-May only |
| S4 | plan_changes.csv | 2026-11-08 | 2 rows |
| S5 | tickets.csv | 2026-11-08 | 38 rows |
| S6 | README.md | 2026-11-08 | extract description |

- Schema and grain: billing/contract = account-month; tickets = ticket; plan_changes = event; accounts = id with validity window.
- Quality: no duplicate keys seen; no sentinels; no nulls except valid_to (open-ended).
- Coverage: billing for the three never-changed accounts is complete Jan-Jun (6 each). ACC-1042 billing present Jan, Mar only (no Feb, no Apr-Jun). ACC-1077 billing present Apr, May only (no Jun). contract_status has no June rows for any account (source ends May). 
- Absence semantics: ACC-1042 Feb billing missing: contract_status shows "paused" for Feb (independent system) - consistent with no bill, but does not settle it (event absent vs unrecorded). ACC-1042 Apr+ rows absent: coincides with valid_to 2026-03-31 and successor ACC-1077. ACC-1077 June billing absent: UNKNOWN (no-bill vs export gap; other accounts have June billing, contract status has no June at all). 
- Instrument caveats: README gives no export contract; identity link rests on one account name string.

## Entity record

- Entity and identifier: ACC-1042 Northgate Clinic to 2026-03-31; ACC-1077 Northgate Health Partners (formerly Northgate Clinic) from 2026-04-01. Link = name text in S1 only; no id-to-id mapping field.
- Descriptive facts: ACC-1042 billed 1840 units/$772.80 in Jan (standard), none in Feb, 1910/$592.10 in Mar (enterprise-annual). ACC-1077 billed 1120/$347.20 Apr, 1085/$336.35 May, enterprise-annual; no Jun row. Implied rate $0.42/unit standard, $0.31/unit enterprise-annual (all rows). Tickets: ACC-1042 3 (feature-request 01-08, feature-request 03-11, integration 03-26); ACC-1077 3 (billing-question 04-01, billing-question 04-04, outage-report 05-25); none in Jun.
- Change over time: 2026-02 contract status paused (ACC-1042); 2026-03 contract active again; plan_changes: standard -> enterprise-annual effective 2026-03-01 (ACC-1042); 2026-03-31 ACC-1042 validity ends; 2026-04-01 ACC-1077 begins; 2026-04 and 2026-05 contract active for ACC-1077; billed volume 1910 (Mar) -> 1120 (Apr) -> 1085 (May). No plan_changes row for ACC-1077. Attribution of any of these to one another: unresolved.

## Looks register

(profile route: none; observations only)

## Leads

(none; observations: Mar->Apr volume drop coincides with the account-id change; two billing-question tickets on ACC-1077 in its first 4 days. Not chased.)

## Amendments

- (none)
