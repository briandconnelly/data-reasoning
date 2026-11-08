# Exploration: profile of the Northgate Clinic account, 2026-01..2026-06

## Frame

- Goal: entity profile (orientation + entity record); no lead-seeking, no reservation (Frame-lite).
- Scope: entity = Northgate Clinic. Resolved via accounts.csv to ACC-1042 (valid 2025-01-01..2026-03-31) and ACC-1077 "Northgate Health Partners (formerly Northgate Clinic)" (valid from 2026-04-01). Treating both ids as one entity rests on the name text alone; recorded as a scoping decision. Sources: accounts, billing, contract_status, plan_changes, tickets. Window 2026-01..2026-06, monthly grain, USD.
- Effort budget: 8 tool calls.
- Stop rule: stop at budget, or when the entity record is written.
- Confirmation reservation: none (profile route; no leads are pursued).

## Orientation record

| id | Origin (file, query, system) | Acquired | Notes |
| --- | --- | --- | --- |
| S1 | accounts.csv (user-provided extract) | 2026-11-08 | 5 accounts, validity windows |
| S2 | billing.csv (extract) | 2026-11-08 | 22 rows, one per account per billed month |
| S3 | contract_status.csv (contracts system) | 2026-11-08 | 20 rows, months 2026-01..2026-05 only |
| S4 | plan_changes.csv (subscriptions system) | 2026-11-08 | 2 events |
| S5 | tickets.csv (support) | 2026-11-08 | 38 tickets |

- Schema and grain: billing/contract_status one row per account-month; plan_changes one row per event; tickets one row per ticket.
- Quality: no duplicate keys seen in the Northgate rows; no blanks or sentinel values in them. valid_to blank on open accounts.
- Coverage: billing has no ACC-1042 row for 2026-02 and none for ACC-1077 in 2026-06 (other accounts have 2026-06 rows). contract_status ends 2026-05 for every account, so June status is not covered. ACC-1042 has no rows after 2026-03, as its validity window implies. No independent denominator for billing or tickets: completeness unverifiable.
- Absence semantics: ACC-1042 2026-02 billing: contract_status says paused that month, consistent with no billing, but this is a second system's record, not proof of completeness. ACC-1077 2026-06 billing: UNKNOWN (no contract status, no plan event, no ticket; cannot distinguish no billing, unrecorded, or export incomplete). Tickets: absence of tickets in a month is UNKNOWN (no ticket-system completeness check).
- Instrument caveats: README gives no export contract; contract_status shorter than billing.

## Entity record

- Entity and identifier: Northgate Clinic = ACC-1042 through 2026-03-31; ACC-1077 (renamed Northgate Health Partners) from 2026-04-01.
- Descriptive facts:
  - ACC-1042 billed 2026-01 standard, 1840 volume, $772.80 ($0.42/unit); 2026-03 enterprise-annual, 1910, $592.10 ($0.31/unit).
  - ACC-1077 billed 2026-04 enterprise-annual 1120, $347.20; 2026-05 enterprise-annual 1085, $336.35 (both $0.31/unit). No 2026-06 row.
  - Tickets: ACC-1042 T-5033 01-08 feature-request, T-5034 03-11 feature-request, T-5035 03-26 integration. ACC-1077 T-5036 04-01 billing-question, T-5037 04-04 billing-question, T-5038 05-25 outage-report. None in June.
- Change over time (as changes, attribution unresolved):
  - 2026-02: contract status paused; no billing row.
  - 2026-03-01: plan changed standard -> enterprise-annual (plan_changes); status back to active in March.
  - Billed volume 1840 (Jan) -> 1910 (Mar) -> 1120 (Apr, new id) -> 1085 (May); amount $772.80 -> $592.10 -> $347.20 -> $336.35.
  - 2026-03-31: ACC-1042 validity ends; 2026-04-01: ACC-1077 begins under the new name. The ids' rows are not overlapping.
  - Per-unit rate fell from 0.42 to 0.31 between Jan and Mar.
  - Unresolved: why volume is ~40% lower under ACC-1077 than under ACC-1042 (could be real, or reflect a different scope under the new id); why Feb was paused; June status.

## Looks register

(none; profile route)

## Leads

(none; observations noted in the entity record, not chased. Candidates for handoff to hypothesis-driven-analysis if the user wants them settled: volume step-down at the id change; Feb pause.)

## Amendments

- (none)
