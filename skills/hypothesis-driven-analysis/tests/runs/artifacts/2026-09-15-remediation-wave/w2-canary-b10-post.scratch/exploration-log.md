# Exploration: profile the Northgate Clinic account

## Frame-lite (entity profile — scope pin + budget only)

- Entity and identifier: "Northgate Clinic" resolves in accounts.csv to account_id `ACC-1042` (valid_from 2025-01-01, valid_to 2026-03-31). accounts.csv also lists `ACC-1077`, "Northgate Health Partners (formerly Northgate Clinic)" (valid_from 2026-04-01, no valid_to), immediately following ACC-1042's valid_to. Read as the same underlying entity continuing under a new account_id and name, not a coincidence — both are in scope.
- Sources: accounts.csv, billing.csv, contract_status.csv, plan_changes.csv, tickets.csv (all under data/b10-entity/, per README.md).
- Timeframe: 2026-01 through 2026-06, per user statement and README.md.
- Effort budget: 10 file reads (the whole dataset is 5 files / ~92 lines total).
- Stop rule: stop once all 5 sources have been read in full and cross-checked for the entity's two account_ids — reached below, dataset fully read.

## Orientation record

| id | Origin (file, query, system) | Acquired | Notes |
| --- | --- | --- | --- |
| S1 | data/b10-entity/accounts.csv | 2026-09-15 | 5 accounts, validity windows |
| S2 | data/b10-entity/billing.csv | 2026-09-15 | 22 rows, one per account per billed month |
| S3 | data/b10-entity/contract_status.csv | 2026-09-15 | 20 rows, monthly status |
| S4 | data/b10-entity/plan_changes.csv | 2026-09-15 | 2 rows, dated plan-change events |
| S5 | data/b10-entity/tickets.csv | 2026-09-15 | 38 rows, support tickets |

- Schema and grain: accounts.csv — one row per account_id validity window (account_id, account_name, valid_from, valid_to). billing.csv — one row per account per billed calendar month (account_id, month, plan, billed_volume, amount_usd). contract_status.csv — one row per account per month (account_id, month, status). plan_changes.csv — one row per dated plan-change event (account_id, effective_date, from_plan, to_plan). tickets.csv — one row per support ticket (ticket_id, account_id, opened date, category).
- Quality: no duplicate keys observed in any file at stated grain. Billing amounts check out arithmetically against a flat per-unit rate by plan (standard ≈ $0.42/unit, enterprise-annual ≈ $0.31/unit) across every row for every account — no calculation anomalies found. No null/sentinel values observed in populated cells.
- Coverage: billing.csv has 6 monthly rows (Jan–Jun) for ACC-1003, ACC-1019, ACC-1058, but only 4 combined for the Northgate entity: ACC-1042 Jan, Mar; ACC-1077 Apr, May — Feb and Jun are absent for the Northgate entity specifically. contract_status.csv has no rows at all for June for *any* account (dataset-wide), so June contract status is unverifiable for every entity, not just this one. No independent volume/revenue denominator exists outside these files, so coverage against a ground truth is unverifiable beyond internal cross-checks.
- Absence semantics: billing.csv Feb gap for ACC-1042 — event absent, corroborated by contract_status.csv showing ACC-1042 `paused` that month (S3 agrees with S2: no billing during a paused month is a consistent, explained absence). billing.csv Jun gap for ACC-1077 — UNKNOWN: contract_status.csv has no June rows for any account, so it cannot confirm or rule out a Northgate-specific pause/cancellation; other accounts (ACC-1003, ACC-1019, ACC-1058) do have June billing rows, so this is not a dataset-wide June cutoff in billing.csv, meaning the absence is specific to ACC-1077 and no source here discriminates "account inactive in June" from "billing record for June not yet exported for this account." tickets.csv has no June ticket for ACC-1077, but ticket counts are low and sparse for every account in every month, so a single month's absence carries little weight and is also UNKNOWN in cause.
- Instrument caveats: none stated in README.md beyond the file descriptions; amounts appear to be billed amounts (no explicit refund/adjustment field).

## Entity record

- Entity and identifier: Northgate Clinic = `ACC-1042` (2025-01-01 through 2026-03-31), continued as `ACC-1077`, renamed "Northgate Health Partners (formerly Northgate Clinic)," from 2026-04-01 onward. The account_id change and rename both land on the same date boundary (2026-03-31 → 2026-04-01) with no gap in the accounts.csv validity windows.
- Descriptive facts (Jan–Jun 2026, ACC-1042 then ACC-1077):
  - Jan 2026: plan `standard`, billed_volume 1840, amount $772.80. Contract status `active`. 1 ticket (feature-request, 01-08).
  - Feb 2026: contract status `paused`; no billing row this month. No tickets.
  - Mar 2026: contract status `active`. Plan changed `standard` → `enterprise-annual`, effective 2026-03-01 (plan_changes.csv). Billed volume 1910, amount $592.10 under the new plan. 2 tickets (feature-request 03-11, integration 03-26).
  - Apr 2026: account_id/name changed to ACC-1077 "Northgate Health Partners." Contract status `active`. Plan `enterprise-annual`, billed_volume 1120, amount $347.20. 2 tickets (both billing-question, 04-01 and 04-04).
  - May 2026: contract status `active`. Plan `enterprise-annual`, billed_volume 1085, amount $336.35. 1 ticket (outage-report, 05-25).
  - Jun 2026: no billing row, no contract-status row (no account has one this month), no ticket. Absence cause is UNKNOWN per Orientation.
- Change over time (stated as sequence, not cause):
  - Contract status changed from `active` to `paused` between Jan and Feb 2026, then back to `active` by Mar 2026.
  - Plan changed from `standard` to `enterprise-annual` effective 2026-03-01.
  - Billed volume and amount fell from $772.80/1840 units (Jan, standard) to $592.10/1910 units (Mar, enterprise-annual) to $347.20/1120 units (Apr) to $336.35/1085 units (May) — volume and spend decline overlaps with, but is not shown by these records to be caused by, the plan change or the account rename.
  - The account_id and account name changed from ACC-1042/"Northgate Clinic" to ACC-1077/"Northgate Health Partners" effective 2026-04-01, immediately following the plan change.
  - Ticket category mix shifted from feature-request/integration (Jan–Mar, under ACC-1042) to billing-question/outage-report (Apr–May, under ACC-1077); this is a small-sample (6 tickets total) observation, not a trend claim.

## Looks register

(Profile route: no leads chased; the reads above are Orient examinations, not Explore looks. No separate looks register entries beyond Orient.)

## Leads

| id | Statement (associational) | Class | Evidence | Search context | Alternatives noted | Cheapest confirming test | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | ACC-1077 (Northgate's successor account) has no billing.csv row for June 2026, unlike the other three ongoing accounts, which all have June rows | data-quality | Orientation, S2 | found during Orient, cross-checking 5 sources for 1 entity | account churned/canceled in June; account paused in June; billing export missed this one account; account still active with a late/missing export | ask the billing-export owner whether ACC-1077 had a June invoice, or check contract_status.csv once June rows are backfilled | reported |
| D2 | contract_status.csv has no rows for June 2026 for any account in the dataset | data-quality | Orientation, S3 | found during Orient, cross-checking 5 sources for 1 entity | export cutoff at May; contracts system genuinely has nothing to report; extract truncated | ask the contract_status export owner why June is absent workspace-wide | reported |

## Amendments

- (none)
