# Exploration: entity profile — Northgate Clinic account

## Frame (Frame-lite: scope + budget only; entity profile, no lead-shaped goal, no reservation)

- Entity and identifier: "Northgate Clinic" resolves via accounts.csv to ACC-1042 (valid 2025-01-01..2026-03-31), which accounts.csv records as succeeded by ACC-1077, "Northgate Health Partners (formerly Northgate Clinic)" (valid from 2026-04-01, open-ended). Both account_ids are treated as the same underlying entity for this profile, since accounts.csv itself asserts the succession.
- Sources: accounts.csv, billing.csv, tickets.csv, contract_status.csv, plan_changes.csv — all under data/b10-entity/.
- Timeframe: 2026-01 through 2026-06, per README and user request.
- Effort budget: 15 file reads/tool calls.
- Stop rule: stop once all 5 sources have been read once and cross-checked for the entity's rows; this is Profile route (orientation + entity record), not lead-chasing.
- Confirmation reservation: not applicable — Profile route takes no reservation (per SKILL.md § Profile Route).

## Orientation record

| id | Origin (file, query, system) | Acquired | Notes |
| --- | --- | --- | --- |
| S1 | data/b10-entity/accounts.csv | 2026-09-15 | 4 data rows; account id/name validity windows |
| S2 | data/b10-entity/billing.csv | 2026-09-15 | 22 data rows; one row per account per billed month |
| S3 | data/b10-entity/tickets.csv | 2026-09-15 | 38 data rows; support tickets |
| S4 | data/b10-entity/contract_status.csv | 2026-09-15 | 20 data rows; monthly contract status |
| S5 | data/b10-entity/plan_changes.csv | 2026-09-15 | 2 data rows; dated plan-change events |

- Schema and grain:
  - accounts.csv: account_id, account_name, valid_from, valid_to — one row per account_id validity window (SCD-style; open valid_to = still current).
  - billing.csv: account_id, month, plan, billed_volume, amount_usd — one row per account per billed month.
  - tickets.csv: ticket_id, account_id, opened, category — one row per support ticket.
  - contract_status.csv: account_id, month, status — one row per account per month.
  - plan_changes.csv: account_id, effective_date, from_plan, to_plan — one row per plan-change event.
- Quality:
  - No duplicate keys observed in any of the 5 files (small extract, checked by inspection).
  - No sentinel values (e.g., -1, 9999) observed; all gaps below are row absences, not flagged values.
  - accounts.csv encodes an account_id succession: ACC-1042 -> ACC-1077 at the 2026-03-31/2026-04-01 boundary, with the name change annotated directly in account_name. This is a structural fact to carry into every per-ID join for this entity, not a data error.
- Coverage:
  - contract_status.csv has rows for Jan-May 2026 only, for every account_id in the file (ACC-1003, ACC-1019, ACC-1058 included) — zero June rows for anyone. Against the Jan-June window the request names, this is a dataset-wide gap, not specific to Northgate.
  - billing.csv has rows for all 6 months for ACC-1003, ACC-1019, ACC-1058. For the Northgate lineage specifically: ACC-1042 is missing its Feb row; ACC-1077 is missing its Jun row. Both are entity-specific gaps against peer coverage.
  - tickets.csv has rows across all 6 months, including June rows for other accounts, so ticket coverage does not show the same systemic June gap that contract_status.csv does.
- Absence semantics:
  - billing.csv, ACC-1042, Feb 2026: contract_status.csv independently records ACC-1042 as "paused" that month (billing and contracts are described in the README as separate systems, so this is a real cross-source corroboration, not circular). Read as event absent (no billable usage while paused), not export failure.
  - billing.csv, ACC-1077, Jun 2026: UNKNOWN. No independent June denominator exists in this dataset — contract_status.csv has no June rows for any account — so there is no evidence to discriminate "no usage" from "export incomplete" for this one row.
  - contract_status.csv, all accounts, Jun 2026: UNKNOWN. The file's own missingness cannot establish its own completeness (per skill rule); nothing else in the dataset dates a June contract-status figure to compare against.
- Instrument caveats: none stated in README beyond the system-of-origin notes already used above (billing system vs. contracts system vs. subscriptions system).

## Entity record

- Entity and identifier: Northgate Clinic = ACC-1042 (2025-01-01..2026-03-31) succeeded by ACC-1077 "Northgate Health Partners (formerly Northgate Clinic)" (2026-04-01..open), per accounts.csv.
- Descriptive facts (associational, Jan-Jun 2026):
  - Jan: contract status active (ACC-1042); billed standard plan, 1840 units, $772.80; 1 ticket opened (feature-request, 01-08).
  - Feb: contract status paused (ACC-1042); no billing row present; 0 tickets.
  - Mar: contract status active (ACC-1042); plan_changes.csv records an effective 2026-03-01 change from standard to enterprise-annual; billed enterprise-annual, 1910 units, $592.10; 2 tickets opened (feature-request 03-11, integration 03-26).
  - Apr: account_id transitions to ACC-1077, renamed Northgate Health Partners; contract status active; billed enterprise-annual, 1120 units, $347.20; 2 tickets opened, both billing-question (04-01, 04-04).
  - May: contract status active (ACC-1077); billed enterprise-annual, 1085 units, $336.35; 1 ticket opened (outage-report, 05-25).
  - Jun: no contract_status row for any account this month (dataset-wide gap); no billing row for ACC-1077 (absence semantics UNKNOWN, see above); 0 tickets recorded against ACC-1077.
  - Ticket total across the window, combining both account_ids: 6 tickets — 1 feature-request (Jan), 1 feature-request + 1 integration (Mar), 2 billing-question (Apr), 1 outage-report (May). No outage-report or integration ticket predates March.
- Change over time (reported as change, not cause):
  - Plan changed from standard to enterprise-annual effective 2026-03-01, coinciding with the March billing row's plan field and preceding the April account-id/name change by about a month.
  - The two billing-question tickets (Apr 1 and Apr 4) both fall within the first week after the ACC-1077 rename took effect.
  - The enterprise-annual amount billed in March ($592.10 for 1910 units) is lower than January's standard-plan amount ($772.80 for 1840 units) despite comparable volume. Noted as an observation only; not chased under the Profile route.

## Looks register

| id | Family | Examined | Comparisons exposed | Note |
| --- | --- | --- | --- | --- |
| L1 | source read | accounts.csv, full file | 1 | surfaced ACC-1042 -> ACC-1077 succession |
| L2 | source read | billing.csv, rows for ACC-1042 and ACC-1077 vs. peer accounts | 1 | surfaced Feb (ACC-1042) and Jun (ACC-1077) gaps |
| L3 | source read | tickets.csv, rows for ACC-1042 and ACC-1077 | 1 | 6 tickets total, categories vary by period |
| L4 | source read | contract_status.csv, all accounts by month | 1 | surfaced dataset-wide June gap and Feb pause |
| L5 | source read | plan_changes.csv, full file | 1 | one dated plan change for this entity, 2026-03-01 |

## Amendments

- (none)
