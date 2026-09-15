# Exploration: what do we have on the Northgate Clinic account?

## Frame

- Goal: entity profile (profile route). No lead-shaped goal; deliver descriptive facts the records settle about this account, per SKILL.md § Profile Route.
- Scope: entity = "Northgate Clinic". Identifier: ACC-1042 (accounts.csv: valid_from 2025-01-01, valid_to 2026-03-31). NOTE: accounts.csv also lists ACC-1077 "Northgate Health Partners (formerly Northgate Clinic)", valid_from 2026-04-01, valid_to blank. Both IDs are in scope for the framed window since the parenthetical naming and adjacent validity windows (ACC-1042 ends 2026-03-31, ACC-1077 begins 2026-04-01) suggest continuity of the same underlying account across an ID change. Timeframe: 2026-01 through 2026-06 (per user). Sources: accounts.csv, billing.csv, contract_status.csv, plan_changes.csv, tickets.csv (all under data/b10-entity/).
- Effort budget: 15 tool calls.
- Stop rule: stop at budget, or when Orient + entity record are complete, whichever comes first (profile route: budget doubles as stop rule).
- Confirmation reservation: profile route takes no reservation (Frame-lite scope per SKILL.md § Profile Route: "profiling seeks orientation, not leads ... takes no lead-shaped goal and no reservation").

## Orientation record

| id | Origin (file, query, system) | Acquired | Notes |
| --- | --- | --- | --- |
| S1 | accounts.csv | 2026-09-15 | 5 rows total; account ids + validity windows |
| S2 | billing.csv | 2026-09-15 | 23 rows total, 4 accounts × Jan–Jun |
| S3 | contract_status.csv | 2026-09-15 | 20 rows total, monthly status Jan–May only (no account has a June row) |
| S4 | plan_changes.csv | 2026-09-15 | 1 row total, dated plan-change events |
| S5 | tickets.csv | 2026-09-15 | 6 rows for Northgate (3 under ACC-1042, 3 under ACC-1077); event-level, not aggregated |

- Schema and grain: accounts.csv: one row per account_id per validity window (account_id, account_name, valid_from, valid_to). billing.csv: one row per account per billed month (account_id, month, plan, billed_volume, amount_usd). contract_status.csv: one row per account per month (account_id, month, status). plan_changes.csv: one row per dated plan-change event (account_id, effective_date, from_plan, to_plan). tickets.csv: one row per support ticket (ticket_id, account_id, opened, category).
- Quality: no duplicate account_ids within a validity window; no obvious sentinel values (zeros, -1, etc.) in billing amounts/volumes. accounts.csv has an unlabeled identity-continuity signal: ACC-1042 ("Northgate Clinic") has valid_to=2026-03-31, and ACC-1077 ("Northgate Health Partners (formerly Northgate Clinic)") has valid_from=2026-04-01 — adjacent, non-overlapping windows plus the parenthetical name are the only evidence linking them; no explicit "renamed_from" or "successor_id" field exists in any source.
- Coverage: billing.csv — the other 3 accounts (ACC-1003, ACC-1019, ACC-1058) each have exactly 6 rows, one per month Jan–Jun, so the expected schedule is monthly. Against that schedule: ACC-1042 has Jan and Mar only (Feb absent); ACC-1077 has Apr and May only (Jun absent). The Feb gap coincides with contract_status=paused that month (see below). The Jun gap for ACC-1077 has no such explanation — other accounts *do* have Jun billing rows, so this gap looks specific to Northgate rather than an export-wide truncation. contract_status.csv — no account (Northgate or otherwise) has a June row, so that absence is export-wide, not Northgate-specific.
- Absence semantics: billing.csv Feb row for ACC-1042 — read as event absent (no bill generated while paused), supported by the matching paused status in contract_status.csv for that month. billing.csv Jun row for ACC-1077 — UNKNOWN; no other source discriminates "not yet billed"/export lag from "billing stopped"; other accounts have Jun rows, so it is not export-wide. contract_status.csv Jun for all accounts — export incomplete (the whole file stops at May), not evidence about June contract state for anyone. tickets.csv — absence of tickets in a month is read as UNKNOWN (no independent ticket-volume denominator exists to distinguish "no tickets filed" from "not exported").
- Instrument caveats: none stated in README.md beyond the one-line file descriptions; amounts/volumes have no stated currency or unit beyond "_usd" suffix.

## Entity record (entity profile only)

- Entity and identifier: "Northgate Clinic" resolves to ACC-1042 in accounts.csv (valid_from 2025-01-01, valid_to 2026-03-31). accounts.csv also carries ACC-1077, "Northgate Health Partners (formerly Northgate Clinic)" (valid_from 2026-04-01, valid_to blank/open). The adjacent validity windows and the parenthetical name are consistent with the same underlying account continuing under a new ID and a new legal/trade name effective 2026-04-01 — but this is an inference from two rows, not a stated linkage in the data, so it is carried as an identity observation rather than a settled fact. Both IDs are covered below since the user's Jan–Jun window spans the transition.
- Descriptive facts (associational, dated):
  - Jan 2026 (ACC-1042): contract active; billed on the "standard" plan, 1,840 units, $772.80; 1 support ticket opened (feature-request, Jan 8).
  - Feb 2026 (ACC-1042): contract status = paused; no billing row this month; no tickets.
  - Mar 2026 (ACC-1042): contract active again; billed on "enterprise-annual" plan, 1,910 units, $592.10; a plan-change event is recorded effective 2026-03-01 (standard → enterprise-annual), consistent with the Jan-vs-Mar plan values in billing.csv; 2 tickets opened (feature-request Mar 11, integration Mar 26). accounts.csv shows this account's validity ends 2026-03-31.
  - Apr 2026 (ACC-1077, "Northgate Health Partners"): accounts.csv validity for this ID begins 2026-04-01; contract active; billed on "enterprise-annual," 1,120 units, $347.20 (down from 1,910 units / $592.10 in March, same plan tier); 2 tickets opened, both "billing-question" (Apr 1, Apr 4).
  - May 2026 (ACC-1077): contract active; billed on "enterprise-annual," 1,085 units, $336.35; 1 ticket opened ("outage-report," May 25).
  - Jun 2026: no billing row for ACC-1077 in billing.csv (gap — see Coverage above); no contract_status row for ACC-1077 or any account (export-wide gap); no tickets recorded for Northgate in June.
- Change over time (dated sequence, no cause assigned):
  - The account paused in Feb 2026 and resumed active in Mar 2026.
  - The plan changed from "standard" to "enterprise-annual" effective 2026-03-01; billed amount per unit is higher on the new plan ($0.31/unit in Jan vs. ~$0.31/unit in Mar — comparable rate, higher plan tier).
  - The account_id/name changed from ACC-1042 "Northgate Clinic" to ACC-1077 "Northgate Health Partners" at the Mar/Apr 2026 boundary.
  - Billed volume and amount dropped from Mar (1,910 units / $592.10) to Apr (1,120 units / $347.20) — a ~41% drop — coinciding with the account/name change; both are stated as a sequence, not as one causing the other.
  - Ticket category shifted from feature-request/integration (Jan, Mar) to billing-question (both Apr tickets, immediately after the account/ID change) to outage-report (May); this is a dated sequence, not an attributed cause.

## Looks register

| id | Family | Examined | Comparisons exposed | Note |
| --- | --- | --- | --- | --- |
| L1 | identity | accounts.csv rows for name match "Northgate" | 1 (2 matching rows) | found the ACC-1042 → ACC-1077 adjacency |
| L2 | coverage | billing.csv monthly row presence, Northgate vs. other 3 accounts, Jan–Jun | ~4 accounts × 6 months = 24 cells | found Feb and Jun gaps specific to Northgate |
| L3 | coverage | contract_status.csv monthly row presence, all accounts, Jan–Jun | ~4-5 accounts × 6 months | found Jun absent for every account (export-wide) |
| L4 | cross-source | billing.csv plan values vs. plan_changes.csv effective date, Northgate only | 1 comparison | plan-change date matches the Jan→Mar plan shift |
| L5 | segment | tickets.csv category by month, Northgate only | 6 rows, 3 categories | noted category shift across the account-ID transition (not chased) |

## Leads

| id | Statement (associational) | Class | Evidence | Search context | Alternatives noted | Cheapest confirming test | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | ACC-1042 and ACC-1077 likely represent the same underlying account across an ID/name change, based on adjacent validity windows and the parenthetical former-name text | data-quality (identity) | L1 | 1 look, 1 family, 1 comparison | coincidental timing; two genuinely distinct accounts that happen to reference each other in name | ask the source system (subscriptions/contracts) for an explicit successor-account mapping | reported |
| D2 | ACC-1077 has no June 2026 billing row while every other account in the extract does | data-quality | L2 | 1 look, 1 family, ~24 cells | billing lag/late invoice not yet exported; genuine service pause not captured elsewhere | check the billing system directly for a Jun invoice on ACC-1077 | reported |
| D3 | Billed volume/amount fell ~41% from March (ACC-1042) to April (ACC-1077) on the same plan tier, coinciding with the account-ID change | descriptive | L4, entity record | 1 look, 1 family, 1 comparison | partial-month billing at the ID cutover; usage change unrelated to the ID change | reconcile against raw usage logs for Mar 15–Apr 15 if available | reported |
| D4 | Both Apr 2026 tickets (immediately after the ACC-1042→ACC-1077 change) are billing-question, versus feature-request/integration/outage in other months | descriptive | L5 | 1 look, 1 family, 6 rows / 3 categories | small n (2 of 6 tickets); routine billing questions unrelated to the ID change | none — small-n observation, not worth a dedicated confirming test | reported |

## Amendments

- (none)
