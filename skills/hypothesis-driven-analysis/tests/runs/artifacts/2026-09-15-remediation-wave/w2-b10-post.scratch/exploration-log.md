# Exploration: tell me about the Northgate Clinic account

## Frame-lite (entity profile)

- Entity and identifier: "Northgate Clinic" — resolves in accounts.csv to ACC-1042 (valid 2025-01-01..2026-03-31), which accounts.csv records as continuing under ACC-1077 "Northgate Health Partners (formerly Northgate Clinic)" (valid_from 2026-04-01, open). Both IDs are treated as one entity's lineage for this profile.
- Sources: accounts.csv, billing.csv, contract_status.csv, plan_changes.csv, tickets.csv, all under data/b10-entity/.
- Timeframe: 2026-01 through 2026-06, per README and user framing.
- Effort budget: full read of all 5 files (small: 92 lines total) — one pass, no sampling needed.
- Stop rule: stop after orientation + entity record; this is a profile ask, not a lead search — no chasing.

## Orientation record

| id | Origin (file, query, system) | Acquired | Notes |
| --- | --- | --- | --- |
| S1 | accounts.csv | read in full | 5 accounts, id/name/validity window |
| S2 | billing.csv | read in full | 22 rows, one row = one account-month bill |
| S3 | contract_status.csv | read in full | 20 rows, one row = one account-month status |
| S4 | plan_changes.csv | read in full | 2 rows, dated plan-change events |
| S5 | tickets.csv | read in full | 38 rows, one row = one support ticket |

- Schema and grain: accounts = one row per account_id with a validity window (valid_to blank = still valid). billing = one row per account per billed month. contract_status = one row per account per month. plan_changes = one row per dated plan-change event. tickets = one row per ticket with open date and category.
- Quality: no duplicate keys observed in any file. No sentinel values (e.g. -1, 9999) observed. accounts.csv shows an explicit account-lineage split: ACC-1042 and ACC-1077 are two ids for one entity, linked by the "(formerly Northgate Clinic)" name and adjacent validity dates (1042 ends 2026-03-31, 1077 starts 2026-04-01).
- Coverage: contract_status.csv has **zero rows for 2026-06 for any account** — a whole-file coverage gap, not specific to Northgate. billing.csv covers Jan-Jun for the three other accounts (ACC-1003, ACC-1019, ACC-1058) but has **no 2026-06 row for ACC-1077** (Northgate's current id), breaking what was a two-month (Apr, May) pattern. tickets.csv coverage is inherently sparse/event-driven for all accounts, so a ticket-free month is not itself a coverage gap.
- Absence semantics: contract_status June gap — export-incomplete (affects every account uniformly, so it reads as an instrument gap, not entity-specific). billing June gap for ACC-1077 — UNKNOWN: no evidence in these files discriminates "not billed because churned/paused" from "export incomplete for this account only," since the other three accounts do have June billing rows.
- Instrument caveats: none stated in README beyond file descriptions; amounts and volumes are as reported, no currency/refund caveats given.

## Entity record

- Entity and identifier: Northgate Clinic = ACC-1042 (2025-01-01 to 2026-03-31), continued as ACC-1077 "Northgate Health Partners (formerly Northgate Clinic)" from 2026-04-01 onward (S1).
- Descriptive facts, Jan-Mar (ACC-1042):
  - Jan: contract active; billed for standard plan, 1840 units, $772.80 (S2, S3).
  - Feb: contract status = paused; no billing row for Feb; no tickets opened in Feb (S2, S3, S5).
  - Mar: contract active again; billed for enterprise-annual plan, 1910 units, $592.10 (S2, S3).
  - Plan change: standard → enterprise-annual effective 2026-03-01 (S4), consistent with the March bill already reflecting enterprise-annual.
  - Tickets: T-5033 feature-request (2026-01-08), T-5034 feature-request (2026-03-11), T-5035 integration (2026-03-26) — 3 tickets total Jan-Mar, none in Feb (S5).
- Descriptive facts, Apr-Jun (ACC-1077, post-rename):
  - Apr: contract active; billed enterprise-annual, 1120 units, $347.20 (S2, S3).
  - May: contract active; billed enterprise-annual, 1085 units, $336.35 (S2, S3).
  - Jun: no contract_status row (file-wide gap) and no billing row (ACC-1077-specific gap, see Orientation) (S2, S3).
  - Tickets: T-5036 billing-question (2026-04-01), T-5037 billing-question (2026-04-04), T-5038 outage-report (2026-05-25) — 3 tickets Apr-May, none recorded in June (S5).
- Change over time (dated, associational — no cause assigned):
  - The account name changed from "Northgate Clinic" to "Northgate Health Partners" with a new account id (ACC-1042 → ACC-1077) effective 2026-04-01 (S1).
  - Contract status changed to "paused" for 2026-02 only, then returned to "active" in 2026-03 (S3).
  - Plan changed from standard to enterprise-annual effective 2026-03-01 (S4); billed volume dropped from 1840-1910 units/month (Jan, Mar under old id) to roughly 1085-1120 units/month (Apr-May under new id) — two different plans and two different account ids span this change, so the volume drop is stated as a sequence, not attributed to the plan change or the rename.
  - No billing or contract-status row exists for ACC-1077 in 2026-06, the last month of the window; whether this reflects the account going inactive again or an export gap is not resolved by these files (see Absence semantics).

## Looks register

(Profile route: full-file reads only, no lead-seeking queries run. Each file was one look.)

| id | Family | Examined | Comparisons exposed | Note |
| --- | --- | --- | --- | --- |
| L1 | schema/identity | accounts.csv full read | 5 rows | found ACC-1042/ACC-1077 lineage |
| L2 | coverage | billing.csv rows per account per month | 4 accounts x 6 months grid | ACC-1042/1077 has 2 gaps (Feb, Jun); others have none |
| L3 | coverage | contract_status.csv rows per month | 6 months | Jun entirely absent, all accounts |
| L4 | event | plan_changes.csv full read | 2 rows | one plan change touches Northgate |
| L5 | event | tickets.csv filtered to ACC-1042/ACC-1077 | 6 of 38 rows | ticket categories and dates for the entity |

## Leads

(Profile route: observations noted, not chased or ranked as leads.)

| id | Statement (associational) | Class | Evidence | Search context | Alternatives noted | Cheapest confirming test | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | ACC-1077 (Northgate, post-rename) has no billing or contract-status row for 2026-06, unlike the three other accounts which are billed through June | data-quality / descriptive | L2, L3 | 2 looks, 1 family (coverage) | account churned or paused in June; June billing/status export incomplete for this account specifically; account merged/re-keyed again after 1077 | check the billing/contracts system directly for ACC-1077's June status | reported |
| D2 | contract_status.csv has no rows at all for 2026-06, for any account | data-quality | L3 | 1 look | export for that file simply stops at May | confirm with export owner whether June contract_status was generated | reported |

## Amendments

- (none)
