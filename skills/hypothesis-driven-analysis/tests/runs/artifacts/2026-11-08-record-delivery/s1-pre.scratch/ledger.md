# Investigation: why did weekly checkout conversion fall 3.1% -> 2.5% (wk 2026-06-01 vs wk 2026-06-08)?
Route: full (observational, co-occurring changes; nothing identifies assignment). Assumption named: no randomization.

## Problem
- Decision informed: roll back v3.4.1 / change campaign traffic, or neither.
- Question: what explains the week-over-week drop, sessions 06-01..06-07 vs 06-08..06-14, UTC.
- Success: the drop is decomposed into explanations that survive discriminating tests; unattributed residual reported as such.
- Stop: conclude after tests T1-T5 run; budget 12 queries.

## Orientation findings (inventory/coverage only, no cause-outcome contrast inspected)
- sessions 9171 rows (06-01..06-14), orders 268 (order->session link absent), deploys.log 3 lines: v3.3.9 06-03, v3.4.1 06-10 14:00 (checkout refactor), v3.4.2 06-12 (logging only).
- landing_page /lp/summer-sale has 0 sessions 06-01..07, then 160/day from 06-08. Sessions/day 600 -> 760 on 06-08..12.
- 06-13/14 sessions drop to ~585/day; mobile 242/238 vs ~430 earlier (device-shaped dip) -> coverage question.
- Order client_version 3.4.0 through 06-09, 3.4.1 from 06-10.
- Metric definition unstated: candidates orders/sessions vs checkout_reached/sessions; to be reconciled to 3.1% / 2.5%.

## Hypotheses
| id | claim | Candidate | Pred if true | Pred if false | Necessary prediction | Test | Data |
|---|---|---|---|---|---|---|---|
| H1 | causal | New /lp/summer-sale traffic (starting 06-08) with lower checkout rate diluted conversion | summer-sale checkout rate well below other pages; non-summer-sale rate flat across weeks | summer-sale rate ~ others | summer-sale checkout_reached rate must be lower than the rate on other pages in wk2 | T1 | sessions |
| H2 | causal | v3.4.1 checkout refactor (06-10 14:00) broke checkout | rate on pre-existing pages falls after 06-10 14:00 | rate on pre-existing pages flat after deploy | rate on non-summer-sale sessions must be lower after 06-10 14:00 than before it (06-08..06-10 14:00) | T2 | sessions, deploys |
| H3 | data-artifact | 06-13/14 mobile session shortfall (or order logging) distorts wk2 rate | independent baseline shows normal traffic/orders in the gap | gap real | orders-vs-checkout_reached reconciliation / mobile rate must differ when the dip is excluded such that wk2 drop changes materially | T3 | sessions, orders |
| H4 | descriptive (estimand: mobile share of sessions wk2 minus wk1, and rate difference mobile-desktop) | Device mix shift | mobile share rises and mobile rate lower | share flat | mobile share wk2 > wk1 | T4 | sessions |
Rates compared with 95% bootstrap/Wilson intervals (committed before reading). Contrast intervals for differences.

## Tests (outcomes filled after running; see Amendments/Conclusion)
T1 (H1) CONSISTENT: summer-sale checkout rate 0.57% (6/1053) vs 3.04% other pages wk2; contrast -3.17pp, 95% bootstrap CI [-3.17,-1.76]pp wait-see raw log; share of wk2 sessions 21.2%. Mix effect ~ 0.212*(0.57-3.04)= -0.52pp of the -0.61pp total.
T2 (H2) NON_DISCRIMINATING: non-sale rate pre-deploy 3.19% vs post 2.93%, diff CI [-1.3,+0.8]pp (includes 0 and includes a drop of the size H2 would need). Wk2 non-sale vs wk1 -0.08pp, CI [-0.8,+0.7]pp. Not refuted (unidentified contrast; v3.4.1 deploy co-occurs with only 3.5 days). Daily non-sale rate no step at 06-10.
T3 (H3) CONSISTENT for a coverage gap: orders == checkout_reached exactly on every day 06-01..06-12; on 06-13 orders 23 vs 17, 06-14 17 vs 11 -> 12 orders with no session row; sessions 06-13/14 ~585/day vs ~760 (mobile 242 vs ~430). Gap affects wk2 denominator, not the conclusion: adding 12 checkouts and ~350 sessions -> ~2.58%, still below 3.12%. Completeness semantics sessions.csv: UNKNOWN for 06-13/14 (export incomplete vs. traffic fall not discriminated beyond order excess).
T4 (H4) not supported: mobile share wk1 56%, wk2 51%; mobile rate 2.9% -> 2.8%; (shift is mostly artifact gap/ sale page); desktop rate fell 3.36%->2.22% but this is the sale page mix (sale page sessions skew desktop on mix?) - not tested; reported descriptive, UNRESOLVED.

## Amendments
- Correction to T1 line: contrast (sale minus other) bootstrap 95% CI is [-3.17,-1.76]pp (printed as the interval of other-minus-sale); ignore "wait-see raw log" text.
- Data note: orders on 06-10 from 08:32 carry client_version 3.4.1 although deploys.log puts v3.4.1 at 14:00 -> log/orders timestamps disagree; H2's timing test is therefore also weakened.
- Complete-day check (06-08..06-12, no gap): wk2 rate 2.55% total, 3.10% excluding summer-sale vs wk1 3.12%.

## Conclusion
- Answer: the drop is mostly a composition effect: the new /lp/summer-sale landing page (from 06-08, 21% of wk2 sessions) converts to checkout at 0.57% vs ~3.0% elsewhere; that accounts for ~0.5pp of the 0.61pp drop. Rate on pre-existing pages is flat (3.04% vs 3.12%, CI [-0.8,+0.7]pp). v3.4.1 not shown to be a cause, not ruled out.
- Status: H1 UNRESOLVED (best supported, associative); H2 UNRESOLVED; H3 UNRESOLVED (data-artifact present for 06-13/14, does not change direction); H4 UNRESOLVED.
- Limitations: observational; summer-sale page also might be low quality intent traffic (no counterfactual); sessions export incomplete 06-13/14; orders not linkable to sessions.
