# Exploration: tell me about the Northgate Clinic account (entity profile)

## Frame-lite

- Goal: profile — orientation and descriptive facts about the "Northgate Clinic" account, not lead-seeking.
- Scope: entity = "Northgate Clinic". Identifier resolution (see Orientation): accounts.csv shows this name attached to ACC-1042 (valid 2025-01-01..2026-03-31) and to ACC-1077, named "Northgate Health Partners (formerly Northgate Clinic)" (valid 2026-04-01..open). The two validity windows are contiguous with no gap/overlap, and the rename is stated in-source (accounts.csv's own name field), so this profile treats ACC-1042 + ACC-1077 as one continuous entity across the window. Recorded here as a scope decision, not silently assumed.
- Sources: data/b10-entity/{accounts,billing,tickets,contract_status,plan_changes}.csv, README.md — all under the named data directory, nothing else read.
- Timeframe: 2026-01 through 2026-06 (per README and per user).
- Effort budget: one read of each of the 5 CSVs + README (6 file reads total); no re-reads, no filtering pulls beyond what's needed to isolate ACC-1042/ACC-1077 rows.
- Stop rule: stop once the orientation record and entity record are filled from that single pass.
- Note on sequencing: SKILL.md was read first to determine method; accounts.csv was read before the rest to resolve the entity's identifier(s), which is what let this Frame-lite state the ID-continuity decision explicitly rather than after the fact. Profile route has no Explore phase, so no looks register/leads table applies here — this is Frame-lite + Orient only.

## Orientation record

| id | Origin (file, query, system) | Acquired | Notes |
| --- | --- | --- | --- |
| S1 | data/b10-entity/README.md | 2026-09-15 | extract description: Jan-Jun 2026, 4 tables |
| S2 | data/b10-entity/accounts.csv | 2026-09-15 | 5 rows: account_id, account_name, valid_from, valid_to |
| S3 | data/b10-entity/billing.csv | 2026-09-15 | 23 rows: account_id, month, plan, billed_volume, amount_usd |
| S4 | data/b10-entity/tickets.csv | 2026-09-15 | 39 rows: ticket_id, account_id, opened, category |
| S5 | data/b10-entity/contract_status.csv | 2026-09-15 | 21 rows: account_id, month, status |
| S6 | data/b10-entity/plan_changes.csv | 2026-09-15 | 2 rows: account_id, effective_date, from_plan, to_plan |

- Schema and grain: accounts.csv = one row per account_id validity window. billing.csv = one row per account per billed month (per README). tickets.csv = one row per ticket. contract_status.csv = one row per account per month. plan_changes.csv = one row per dated plan-change event.
- Quality: no duplicate keys observed in any table. No null/sentinel values observed in the Northgate-relevant rows. billing.csv and contract_status.csv are both month-grain but neither is a full account x month grid — rows are simply absent for some account/months rather than present with a null status.
- Coverage against expected schedule (billing.csv, "one row per account per billed month," Jan-Jun = 6 expected months per account):
  - ACC-1003, ACC-1019: 6/6 months present.
  - ACC-1058: 6/6 months present.
  - ACC-1042/ACC-1077 (Northgate, combined): 4/6 months present (Jan, Mar, Apr, May). Feb and Jun absent.
  - contract_status.csv stops at 2026-05 for every account (ACC-1003, ACC-1019, ACC-1058, ACC-1077 all have no 2026-06 row) — this is a global gap, not Northgate-specific, so June contract status is unverifiable for all accounts, Northgate included.
- Absence semantics:
  - contract_status.csv, 2026-06 (all accounts): export incomplete (evidence: absence is uniform across every account_id, not selective) — not "no status."
  - billing.csv, ACC-1042 2026-02: plausibly explained by contract_status.csv showing status=paused that month — read as "no billing event occurred" (paused account), not export gap, since this absence IS selective to the one account with a paused status that month.
  - billing.csv, Northgate 2026-06: UNKNOWN. Sibling accounts (ACC-1003, ACC-1019, ACC-1058) all have June billing rows, so this isn't the same global gap as contract_status.csv's June gap. No contract_status row exists for June for anyone, so "paused/terminated" cannot be confirmed or ruled out from this data. Recorded as an observation below, not a finding.
  - tickets.csv absences: read as "no ticket opened," since ticket rows are individually keyed events with no evidence of sampling or export truncation.
- Instrument caveats: billing amount_usd is per README's monthly billed extract; no indication of pre/post-refund or proration. plan_changes.csv only logs the one Northgate change (2026-03-01); no plan-change row exists for the ACC-1042 -> ACC-1077 identifier transition itself (only accounts.csv's validity windows mark it).

## Entity record

- Entity and identifier: "Northgate Clinic," resolved to ACC-1042 (2025-01-01..2026-03-31) then ACC-1077 "Northgate Health Partners (formerly Northgate Clinic)" (2026-04-01..open), per accounts.csv's own naming. Treated as one continuous entity for this profile (see Frame-lite).
- Descriptive facts (Jan-Jun 2026):
  - Jan 2026: contract status active (ACC-1042); billing plan standard, 1,840 billed units, $772.80; 1 ticket opened (feature-request, 2026-01-08).
  - Feb 2026: contract status paused (ACC-1042); no billing row; no tickets.
  - Mar 2026: contract status active (ACC-1042); plan_changes.csv records a plan change effective 2026-03-01, standard -> enterprise-annual; billing plan enterprise-annual, 1,910 billed units, $592.10; 2 tickets opened (feature-request 2026-03-11, integration 2026-03-26). accounts.csv validity for ACC-1042 ends 2026-03-31.
  - Apr 2026: account_id ACC-1077 becomes valid 2026-04-01 under the name "Northgate Health Partners (formerly Northgate Clinic)"; contract status active; billing plan enterprise-annual, 1,120 billed units, $347.20; 2 tickets opened (billing-question, 2026-04-01 and 2026-04-04).
  - May 2026: contract status active (ACC-1077); billing plan enterprise-annual, 1,085 billed units, $336.35; 1 ticket opened (outage-report, 2026-05-25).
  - Jun 2026: no billing row, no ticket, and no contract-status row for ACC-1077 (contract_status.csv has no June rows for any account — see Orientation).
  - Across the window: 7 tickets total (4 under ACC-1042, 3 under ACC-1077); categories: feature-request x2, integration x2, billing-question x2, outage-report x1.
- Change over time (dated sequence, associational — no cause asserted):
  - The account was paused for Feb 2026 and active again in Mar 2026.
  - The billing plan changed from standard to enterprise-annual effective 2026-03-01; the per-unit amount dropped from about $0.42/unit (Jan, standard) to about $0.31/unit (Mar, enterprise-annual), a sequence coincident with the plan change, not attributed to it here.
  - The account identifier changed from ACC-1042 to ACC-1077 (and the account name changed to "Northgate Health Partners") at the same point the validity windows meet, 2026-03-31 -> 2026-04-01.
  - Both billing-question tickets in the dataset for this entity landed in the first 4 days after the ACC-1077 identifier took effect (2026-04-01, 2026-04-04); this is a sequence noted, not explained.
  - No billing row and no ticket exist for this entity in Jun 2026, while three other accounts in the same extract do have Jun billing rows. Attribution (paused again, contract ended, export gap, genuinely no activity) is unresolved by this data; flagged as an observation, not chased, per profile route.

## Amendments

- (none)
