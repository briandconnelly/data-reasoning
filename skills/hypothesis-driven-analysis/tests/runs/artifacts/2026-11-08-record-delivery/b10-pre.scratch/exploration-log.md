# Entity profile: Northgate Clinic account

## Frame-lite
- Route: profile (entity). Entity: "Northgate Clinic". Resolver: accounts.csv name -> ACC-1042 (valid 2025-01-01..2026-03-31); ACC-1077 "Northgate Health Partners (formerly Northgate Clinic)" valid from 2026-04-01. Link 1042->1077 rests on the name string only (no id-mapping table). Both ids are in scope; recorded as a decision.
- Sources: accounts, billing, contract_status, plan_changes, tickets (all in data/b10-entity). Window 2026-01..2026-06.
- Budget: 6 tool calls of reads/queries (files tiny; all read once). Stop rule = budget. No chasing.

## Orientation record
S1-S5 = the five csvs, user-provided extract per README.
- Grain: billing = account x month; contract_status = account x month; plan_changes = event; tickets = ticket.
- Quality: no duplicates seen; no nulls except accounts.valid_to (open). 
- Coverage (expected: each account one billing row and one status row per month Jan-Jun):
  - ACC-1042: billing Jan, Mar only (Feb missing); status Jan-Mar (Feb = paused). 
  - ACC-1077: billing Apr, May only (Jun missing); status Apr, May only (Jun missing). 
  - Other accounts: billing Jan-Jun complete; status Jan-May only (Jun missing for ALL accounts).
  - Jun status absent for every account -> export looks truncated for contract_status.
- Absence semantics: billing Feb ACC-1042 absent while status = paused: consistent with "no billing while paused" but nothing outside billing confirms; UNKNOWN. ACC-1077 June billing absent: UNKNOWN (no activity vs unrecorded vs incomplete export) - other accounts have June billing, so billing export is not obviously truncated, but status export is. ACC-1042 after Mar: absent consistent with account closure at valid_to 2026-03-31, but that's the accounts table's own claim.
- Caveats: no plan_changes row for ACC-1077 (it appears on enterprise-annual from its first row). plan_changes ACC-1042 2026-03-01 matches billing plan in Mar.

## Entity record
- Identity: ACC-1042 Northgate Clinic, to 2026-03-31; ACC-1077 Northgate Health Partners (formerly Northgate Clinic) from 2026-04-01.
- Billing: 2026-01 standard 1840 units $772.80 ($0.42/unit); 2026-02 no row; 2026-03 enterprise-annual 1910 $592.10 ($0.31/unit). ACC-1077: 2026-04 enterprise-annual 1120 $347.20 ($0.31); 2026-05 1085 $336.35 ($0.31); 2026-06 no row.
- Status: Jan active; Feb paused; Mar active; (1077) Apr, May active; Jun none.
- Tickets: ACC-1042: T-5033 01-08 feature-request, T-5034 03-11 feature-request, T-5035 03-26 integration. ACC-1077: T-5036 04-01 billing-question, T-5037 04-04 billing-question, T-5038 05-25 outage-report. Total 6.
- Changes over time (named as changes, attribution unresolved): 
  2026-02: status paused, no billing row. 2026-03-01: plan standard->enterprise-annual; per-unit price 0.42->0.31 (Jan->Mar). 2026-04-01: account id changes 1042->1077 with rename; billed volume 1910 (Mar) -> 1120 (Apr), -41%; two billing-question tickets opened 04-01 and 04-04. 
  Attribution of any of these to another is unresolved; hand to hypothesis-driven-analysis if wanted.

## Looks register
(none - profile route; observations noted not chased)

## Leads
(none - observations only)

## Amendments
(none)
