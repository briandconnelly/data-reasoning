# Exploration: entity profile of Northgate Clinic (ACC-1042 -> ACC-1077), 2026-01..2026-06

## Frame

- Goal: profile route (entity). Descriptive story of the account; no lead-seeking, no causes.
- Scope: Entity = Northgate Clinic. Resolving identifier: ACC-1042 (accounts.csv, valid 2025-01-01..2026-03-31) and ACC-1077 "Northgate Health Partners (formerly Northgate Clinic)" (valid from 2026-04-01). Sources: accounts, billing, contract_status, plan_changes, tickets. Window 2026-01..2026-06. Other accounts used only as a coverage denominator, not profiled. Widening to both ids is a recorded scope decision: the accounts table itself says ACC-1077 is the former ACC-1042.
- Effort budget: 6 tool calls of analysis (data already read in 1 call).
- Stop rule: stop at budget or once the entity record is written.
- Confirmation reservation: not applicable on profile route (no leads sought).

## Orientation record

| id | Origin (file, query, system) | Acquired | Notes |
| --- | --- | --- | --- |
| S1 | data/b10-entity/accounts.csv (user-provided extract) | 2026-11-08 | 5 accounts; validity windows |
| S2 | billing.csv | 2026-11-08 | 22 rows, one per account-month |
| S3 | contract_status.csv | 2026-11-08 | 20 rows; contracts system |
| S4 | plan_changes.csv | 2026-11-08 | 2 events; subscriptions system |
| S5 | tickets.csv | 2026-11-08 | 38 tickets |

- Schema and grain: billing/contract_status one row per account_id x month; tickets one row per ticket; plan_changes one row per event; accounts one row per account id. Entity is split across two account ids; no common key other than the name string in S1.
- Quality: no duplicate keys seen; no blanks except open-ended valid_to (expected). Identity link 1042->1077 rests on the "formerly" text in S1 only.
- Coverage: billing months present for ACC-1042/1077: 2026-01, 03, 04, 05 (missing 02 and 06). The other three accounts have all six billing months, so both gaps are specific to this entity. contract_status has no 2026-06 rows for any account. Tickets: no independent denominator, unverifiable.
- Absence semantics: S2 Feb 1042 missing: contract_status (S3, independent system) says paused for 2026-02, so no-billing is consistent with a pause, but pause cause/definition is not documented. S2 June 1077 missing: no evidence discriminates no-activity vs unrecorded vs export incomplete -> UNKNOWN (S3 has no June at all for anyone, so cannot corroborate). S3 June: export incomplete for all accounts (all absent). S2/S3 April+ for 1042: absent because id ended 03-31 (S1). S5 months with no tickets: UNKNOWN (no ticket-volume denominator).
- Instrument caveats: unit rate implied by amount/volume is 0.42 for standard and 0.31 for enterprise-annual across accounts (derived, consistent in this extract).

## Entity record (entity profile only)

- Entity and identifier: Northgate Clinic = ACC-1042 (to 2026-03-31); renamed/re-keyed as ACC-1077 Northgate Health Partners from 2026-04-01 (per S1).
- Descriptive facts:
  - Billing: 2026-01 standard, 1840 units, $772.80; 2026-02 no row; 2026-03 enterprise-annual, 1910, $592.10; 2026-04 (ACC-1077) enterprise-annual, 1120, $347.20; 2026-05 enterprise-annual, 1085, $336.35; 2026-06 no row. Total billed in extract $2,048.45.
  - Contract status: active Jan; paused Feb; active Mar; (1077) active Apr, May; no June record.
  - Tickets: 6 total. ACC-1042: T-5033 2026-01-08 feature-request, T-5034 2026-03-11 feature-request, T-5035 2026-03-26 integration. ACC-1077: T-5036 2026-04-01 billing-question, T-5037 2026-04-04 billing-question, T-5038 2026-05-25 outage-report. None in Feb or June.
- Change over time (each a change, dated):
  - 2026-02: contract status changed active -> paused; no billing row for the month.
  - 2026-03: status back to active; 2026-03-01 plan change standard -> enterprise-annual (S4); March billed on enterprise-annual; amount fell $772.80 -> $592.10 while volume rose 1840 -> 1910.
  - 2026-04-01: account id/name changed ACC-1042 -> ACC-1077 (S1); billed volume fell 1910 -> 1120 (-41%) in April and 1085 in May. Two billing-question tickets were opened 04-01 and 04-04.
  - 2026-06: no billing row and no contract-status row for the entity.
  - Sequence only; attribution of the volume/amount changes to the plan change, the pause, or the id change is unresolved and would go to hypothesis-driven-analysis.

## Looks register

(Profile route: no Explore looks.)

| id | Family | Examined | Comparisons exposed | Note |
| --- | --- | --- | --- | --- |

## Leads

(None sought. Observations only, recorded above.)

| id | Statement (associational) | Class | Evidence | Search context | Alternatives noted | Cheapest confirming test | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Amendments

- 2026-11-08: scope widened from ACC-1042 to ACC-1042+ACC-1077 because accounts.csv states the latter was formerly Northgate Clinic.
