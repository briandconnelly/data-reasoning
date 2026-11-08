# Investigation: Why did weekly checkout conversion fall from 3.1% (wk 2026-06-01) to 2.5% (wk 2026-06-08)?

Route: full (causal question, no identifying design: v3.4.1 shipped to everyone; several co-occurring changes). Assumption named: nothing identifies a causal effect, so conclusions are associative.

## Problem

- Decision informed: roll back v3.4.1 (checkout form refactor), or look at traffic mix / data instead.
- Falsifiable question: what accounts for the fall in orders/sessions between Mon 06-01..Sun 06-07 and Mon 06-08..Sun 06-14 (UTC, per session)?
- Success criteria: answered means one or more explanations account for most of the ~0.6pp drop and survive a discriminating test, or the data is shown unable to say.
- Stop condition: conclude when no unresolved alternative could reverse the rollback decision; else stop with limits.
- Effort budget: 12 tool calls of analysis.
- Definition (orientation): conversion = orders / sessions (orders has no session id, so it cannot be joined to sessions); checkout_reached/sessions is a secondary metric.

## Hypotheses

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | The v3.4.1 release (2026-06-10 14:00Z, checkout form refactor) caused the drop | Daily conversion falls after the deploy, orders shift to 3.4.1 clients | Conversion already low before deploy | Conversion on 06-08..06-09 (pre-deploy) must be near week-1 level (not already at the week-2 level); a deploy cannot cause a drop that precedes it | T1 | orders, sessions, deploys.log |
| H2 | descriptive (estimand: change in aggregate rate attributable to device x landing-page mix, by standardizing wk2 rates to wk1 mix) | The drop is a composition shift (more desktop / different landing mix) not a change in within-segment rates | Standardized wk2 rate ~ wk1 rate | Within-segment rates themselves fall | Mix-standardized wk2 conversion must recover most (>50%) of the drop | T2 | sessions device x landing; orders cannot be segmented (no join) -> use checkout_reached rate per segment as proxy |
| H3 | data-artifact | Partial coverage on 06-13/06-14 (mobile sessions 242/238 vs ~330-440, /home capped at 400/day) or a denominator/numerator mismatch creates the apparent drop | Drop vanishes when 06-13/14 excluded or orders vs sessions counts reconcile | Drop persists on full-coverage days | Drop must shrink to ~0 when comparing full-coverage days only (06-01..06-05 vs 06-08..06-12) | T3 | sessions, orders by day |
| H4 | causal | A step change at the 06-08 boundary (not the deploy): week-2 traffic from a different source (e.g. /lp/summer-sale) lower intent | Landing-page rate for summer-sale much lower and share up | summer-sale share flat | /lp/summer-sale session share must rise in wk2 | T4 | sessions landing_page |

## Sources

| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 rows) | 2026-11-08 | 06-01..06-14; 400 sessions/day capped on /home-ish days 06-01..06-12; 06-13/14 ~ 311/304 on /home |
| S2 | data/s1-conversion/orders.csv (268 rows) | 2026-11-08 | 06-01..06-14, 17-23/day; client_version 3.4.0/3.4.1 |
| S3 | data/s1-conversion/deploys.log | 2026-11-08 | 3 releases: 06-03 v3.3.9, 06-10 v3.4.1, 06-12 v3.4.2 |

## Data Validity

- Collection method: unknown (flat files, no export contract).
- Coverage matrix: sessions by day x device counted at orientation (see transcript): week1 desktop 247-273, mobile 327-353; wk2 desktop 320-370, mobile 390-440 on 06-08..06-12, then mobile 242/238 on 06-13/14 and desktop 345/346. Orders 17-23/day every day. No orders by device/landing possible.
- Field population: no empty cells in either file; session_id and order_id unique. Device has only desktop/mobile.
- Coverage baseline: none independent -> coverage unverifiable. Note version labels: orders on 06-01 already show client_version 3.4.0 though deploy log lists v3.3.9 (06-03) and v3.4.1 (06-10); client_version is not the same namespace as release versions (UNKNOWN mapping).
- Known instrument failures: none documented. Orders (268) vs checkout_reached=yes (256) differ, so orders are not a subset of sessions' checkouts.
- Source completeness semantics:
S1: UNKNOWN — no export contract; the 06-13/14 mobile dip cannot be told apart from real traffic or dropped rows by the file itself.
S2: UNKNOWN — no export contract or independent order counter.
- Sensitivity checks performed: bootstrap interval around the drop contrast (95%) in T1.

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | wk2 sessions before the deploy (06-08 to 06-10T14:00Z) have checkout rate at the wk1 level (contrast 0) | session-level bootstrap 95% CI of pre-deploy minus wk1 | NON_DISCRIMINATING | pre-deploy 2.66% (n=2029) vs wk1 3.12% (n=4200); contrast -0.46pp, 95% CI (-1.33, +0.47)pp contains 0, so the predicted value sits inside the interval (an_2.py). Post-deploy 2.41%; post minus pre -0.25pp, CI (-1.13,+0.64). Detection limit ~ +/-0.9pp (S1,S3) |
| T2 | H2 | mix-standardized wk2 checkout_reached rate recovers >50% of the observed drop | direct standardization on device x landing | CONSISTENT | wk1 3.12%, wk2 2.51%, wk2 standardized to wk1 mix 3.06%: recovers ~91% of the 0.61pp drop. Standardization only removes the summer-sale segment, absent in wk1 (no overlap), so it is a segment-exclusion not a reweighting. Ex-summer-sale wk2 3.04% vs wk1 3.12%, contrast CI (-0.81,+0.71)pp (S1) |
| T3 | H3 | the drop shrinks to ~0 on full-coverage days only (06-01..05 vs 06-08..12) | session-level bootstrap 95% CI | NON_DISCRIMINATING | full-coverage days 3.10% vs 2.55%, contrast -0.55pp, CI (-1.33,+0.27) contains 0 so the predicted value is inside the interval; point estimate nearly unchanged from -0.61pp (S1). Orders (S2) cannot reconcile with checkout_reached on 06-13/14 (23 and 17 orders vs 17 and 11 checkouts) |
| T4 | H4 | summer-sale share rises wk1->wk2 | share by week; rate of the segment vs the rest, bootstrap CI | CONSISTENT | share 0% (0/4200) to 21.2% (1053/4971), first session 06-08T08:00Z, 126-160/day thereafter; its checkout rate 0.57% vs 3.04% for other wk2 traffic, contrast CI (-3.14,-1.72)pp (S1). Adequacy not required (positive, deterministic share) |
| T5 | H1 | non-summer-sale wk2 traffic falls after the deploy | ex-summer-sale pre vs post deploy, bootstrap | NON_DISCRIMINATING | 3.18% (n=1602) pre vs 2.94% (n=2316) post, -0.24pp, CI (-1.39,+0.83)pp contains 0 and the deploy-effect size cannot be excluded within ~+/-1pp (S1,S3) |

## Amendments

- 2026-11-08: Definition amended before any test ran. The user's 3.1% and 2.5% match checkout_reached/sessions (3.12% and 2.51%), not orders/sessions (3.12% and 2.76%), so checkout_reached/sessions is the primary metric. Orders cannot be joined to sessions and do not reconcile with checkout_reached on 06-13/14. Reason: the stated numbers are the spec.
- 2026-11-08: T5 added (H1, ex-summer-sale pre/post deploy) because the aggregate T1 could not separate the deploy from the new traffic. Not a new hypothesis.
- 2026-11-08: orientation also found that orders carry client_version 3.4.1 from 06-10T08:32Z, ~5.5 h before the 14:00:07Z deploy log entry, and 3.4.0 orders stop on 06-09. client_version is not the same namespace as release tags, deploy timing in S3 is therefore uncertain.

## Conclusion

- Answer: the drop is associated with a new traffic segment, /lp/summer-sale, that appears at 2026-06-08T08:00Z and is about 21% of week-2 sessions. It converts to checkout at 0.57% against 3.04% for everything else. Without it, week-2 conversion is 3.04% against 3.12% in week 1, so the segment accounts for about 90% of the 0.61pp drop. The v3.4.1 checkout refactor on 06-10 is not shown to be the cause, but a small deploy effect (up to about 1pp) cannot be ruled out.
- Best supported: H2 and H4, together (T2 and T4 CONSISTENT, T4 discriminating from the deploy because the segment's start precedes the deploy by two days).
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 and T5 NON_DISCRIMINATING: pre-deploy contrast CI (-1.33,+0.47)pp contains 0, so the timing prediction could not refute it; the post-deploy change in non-summer-sale traffic is -0.24pp with CI (-1.39,+0.83)pp. Not best supported: the 06-08 and 06-09 pre-deploy drop point estimate and the segment account for the change without it |
  | H2 | descriptive | UNRESOLVED | best supported (T2 CONSISTENT; recovers ~91% of the drop; standardization is a segment exclusion, not a reweighting) |
  | H3 | data-artifact | UNRESOLVED | T3 NON_DISCRIMINATING: CI contains 0, but the point estimate on full-coverage days is -0.55pp, nearly unchanged; coverage unverifiable (S1, S2 UNKNOWN) |
  | H4 | causal | UNRESOLVED | best supported (T4 CONSISTENT; the segment appears before the deploy and converts far below the rest) |
- Limitations: associative only, because nothing assigned the summer-sale traffic or the deploy independently of the outcome. The whole week-over-week contrast has a 95% session-bootstrap CI (-1.28,+0.12)pp that touches 0, so the size of the drop is itself uncertain at this volume. Sessions that reached checkout but did not order are not separable; orders are unjoinable to sessions and unreconcilable with checkout_reached on 06-13/14. Completeness of both files is UNKNOWN, including the 06-13/14 mobile dip. Deploy time is uncertain (3.4.1 orders predate the log entry). The 4.07% to 2.84% desktop /product change and similar within-segment moves were not tested. Continuation: `decision-analysis` if a rollback decision hangs on the unresolved H1; `causal-identification-review` for a design that would isolate the deploy effect (for example a staged rollout by client version).
