# Northgate Clinic — working notes

Source: data/b10-entity/{accounts,billing,tickets,contract_status,plan_changes}.csv
Coverage per README: 2026-01 through 2026-06.

## Identity
- ACC-1042 "Northgate Clinic" — valid_from 2025-01-01, valid_to 2026-03-31
- ACC-1077 "Northgate Health Partners (formerly Northgate Clinic)" — valid_from 2026-04-01, valid_to (open)
- These are the same underlying customer: ACC-1077's valid_from is exactly the day after ACC-1042's valid_to, and the name explicitly says "formerly Northgate Clinic". Treated as one continuous account relationship across the rename.

## Billing (account_id, month, plan, billed_volume, amount_usd)
- ACC-1042,2026-01,standard,1840,772.80
- ACC-1042,2026-03,enterprise-annual,1910,592.10
- (no 2026-02 row for ACC-1042 — coincides with "paused" contract status that month)
- ACC-1077,2026-04,enterprise-annual,1120,347.20
- ACC-1077,2026-05,enterprise-annual,1085,336.35
- (no 2026-06 row for ACC-1077 — NOTE: other accounts in the dataset DO have 2026-06 billing rows, so this looks like a real gap for Northgate specifically, not a dataset-wide lag)

## Tickets (ticket_id, account_id, opened, category)
- T-5033, ACC-1042, 2026-01-08, feature-request
- T-5034, ACC-1042, 2026-03-11, feature-request
- T-5035, ACC-1042, 2026-03-26, integration
- T-5036, ACC-1077, 2026-04-01, billing-question
- T-5037, ACC-1077, 2026-04-04, billing-question
- T-5038, ACC-1077, 2026-05-25, outage-report

## Contract status (account_id, month, status)
- ACC-1042,2026-01,active
- ACC-1042,2026-02,paused
- ACC-1042,2026-03,active
- ACC-1077,2026-04,active
- ACC-1077,2026-05,active
- No 2026-06 row for ANY account in contract_status.csv — dataset-wide gap, not specific to Northgate.

## Plan changes (account_id, effective_date, from_plan, to_plan)
- ACC-1042, 2026-03-01, standard -> enterprise-annual
- No plan-change row for ACC-1077 (it started on enterprise-annual in April, consistent with the March upgrade carrying over through the rename).

## Narrative reconstruction
1. Jan 2026: active, standard plan, billed $772.80. One feature-request ticket.
2. Feb 2026: contract paused; no billing that month (consistent with pause).
3. Mar 2026: reactivated, upgraded standard -> enterprise-annual effective 2026-03-01, billed $592.10 for the month (lower than Jan despite plan upgrade — volume 1910 vs 1840, so per-unit rate dropped, likely the new plan's pricing). Two tickets (feature-request, integration).
4. 2026-03-31: account ACC-1042 record closes (valid_to).
5. 2026-04-01: entity reappears as ACC-1077 "Northgate Health Partners (formerly Northgate Clinic)", same enterprise-annual plan, billed $347.20. Two billing-question tickets right at the start (Apr 1 and Apr 4) — plausibly related to the rename/re-contracting.
6. May 2026: active, billed $336.35, one outage-report ticket (2026-05-25).
7. June 2026: no billing or contract-status row for ACC-1077 under this data pull — open question, see gaps below.

## Gaps / things to flag to user
- June billing missing for Northgate (ACC-1077) while other accounts have June billing rows — worth checking source system for a missed load or an actual lapse/churn.
- Contract_status.csv has no June data for anyone — dataset-wide, not a Northgate-specific issue.
- No plan-change row logged for the Feb pause -> March reactivation (status field captures it, plan_changes.csv does not track pause/resume, only plan-to-plan changes).
