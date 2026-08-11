# Investigation: How much did launching /lp/summer-sale improve checkout conversion?

## Problem

- Decision informed: whether to credit the summer-sale campaign launch with a conversion lift, and whether to expand/renew it on that basis.
- Falsifiable question: what is the effect of launching the `/lp/summer-sale` landing page (2026-06-08) on site-wide checkout conversion (share of sessions with `checkout_reached = yes`), 2026-06-01 to 2026-06-14?
- Success criteria: answered means either (a) a defensible causal magnitude is produced, or (b) the loop establishes the magnitude is not identifiable from this data and reports what the data does show instead.
- Stop condition: conclude when no named unresolved alternative could reverse the answer, given the effort budget below.
- Effort budget: ~20 shell/python probes over the 3 fixture files (no external or metered sources involved).

## Assignment check (before routing)

No randomization or A/B assignment is stated anywhere in the fixtures (sessions.csv, orders.csv, deploys.log). `/lp/summer-sale` is a new landing page that started receiving traffic on 2026-06-08 — consistent with an ad/marketing push that recruits its own traffic, not with random assignment of existing visitors to "see campaign" vs "not see campaign". No user is available to ask (headless). Per SKILL.md: assume nothing identifies the causal effect, take the `full` route, and name this assumption explicitly. This also matches the skill's own worked example of an unidentified-assignment question wearing a causal-magnitude wording.

## Hypotheses

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | Launching the campaign page caused an increase in site-wide checkout conversion | aggregate post-launch conversion rate exceeds pre-launch rate | aggregate post-launch rate is flat or lower | aggregate conversion (all sessions) after 2026-06-08 must exceed the pre-06-08 rate — an "improvement" claim requires the aggregate to have risen at all, independent of whether a rise could be attributed causally | T1 | sessions.csv, all rows, checkout_reached by day |
| H2 | data-artifact | The campaign page itself converts to checkout at a much lower rate than existing traffic, so adding it to the mix mechanically drags down the site-wide blended rate even with no change in visitor behavior on existing pages | per-page (`/home`, `/product`) conversion rates are unchanged pre vs post; a composition-adjusted post rate (post per-page rates, pre-period page mix) reproduces the pre-launch aggregate rate | per-page rates shift materially pre vs post, or composition adjustment does not close the gap | `/home` and `/product` conversion rates pre vs post must not differ by more than sampling noise (95% CI on the difference must bracket 0) | T2 | sessions.csv stratified by landing_page x period |
| H3 | data-artifact / confound | The 2026-06-10 "checkout form refactor, cart service bump" deploy (deploys.log), not the campaign, is what moved conversion in the post-launch window | a detectable break in `/home` and `/product` conversion appears at 06-10, distinct from the pre-existing day-of-cycle pattern | conversion continues the same cyclical pattern straight through 06-10 with no detectable break | `/home`+`/product` conversion in the 3 days after the 06-10 deploy must differ from the 2 days between campaign launch (06-08) and the deploy (06-09) by more than sampling noise | T3 | sessions.csv by day, deploys.log |
| H4 | descriptive (estimand: checkout_reached rate on `/lp/summer-sale` sessions minus checkout_reached rate on `/home` and on `/product` sessions, post-launch period) | The campaign page's own visitors convert to checkout at a different rate than visitors landing elsewhere | `/lp/summer-sale` rate differs from `/home` and `/product` rates by more than sampling noise | rates statistically indistinguishable | the 95% CI on (`/lp/summer-sale` rate − `/home` rate) and on (`/lp/summer-sale` rate − `/product` rate) must exclude 0 for this to register as a real difference | T4 | sessions.csv, post-launch, by landing_page |

## Sources

| id | Origin (file, query, system) | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | `tests/fixtures/s1-conversion/sessions.csv` (local fixture, 9,171 rows) | read directly, this session | fields: session_id, timestamp, landing_page, device, checkout_reached; no nulls in any field |
| S2 | `tests/fixtures/s1-conversion/orders.csv` (local fixture, 268 rows) | read directly, this session | fields: order_id, timestamp, amount, client_version; used only as a cross-check on order volume/version, not joinable to sessions (no shared key) |
| S3 | `tests/fixtures/s1-conversion/deploys.log` (local fixture, 3 lines) | read directly, this session | full text read; 3 releases: 06-03 copy tweak, 06-10 checkout form refactor + cart service bump, 06-12 logging-only |

Local, already-provided, non-costly, non-sensitive files; no collection plan or authorization gate applies beyond reading files already handed to this task.

## Data Validity

- Collection method: flat CSV exports of session and order events; deploy log is a plaintext release log.
- Coverage matrix (day x landing_page, session counts): `/home` and `/product` present every day 06-01..06-14 at a stable ~400/200-per-day rate (dropping proportionally on 06-13/06-14, the partial-day tail of the export). `/lp/summer-sale` is present only from 06-08 onward (160/day, dropping same tail pattern) — expected, since the page did not exist before launch, not a coverage gap.
- Field population: `checkout_reached`, `landing_page`, `timestamp` are 100% populated across all 9,171 session rows (checked directly, 0 nulls per field).
- Coverage baseline: orders.csv daily counts (17-23/day) track checkout_reached=yes daily counts (11-23/day) closely enough to corroborate that checkout_reached is capturing real conversions and not obviously miscounted; exact per-day equality is not expected since orders.csv is not keyed to sessions.csv.
- Known instrument failures: none found; no gaps, no duplicate ids checked but row counts match expectations (9,171 sessions header-excluded, 268 orders).
- Source completeness semantics: S1 — absent rows would mean an event never reached the export; no independent denominator exists to confirm total traffic volume, so this is UNKNOWN — no evidence discriminates "no session occurred" from "session occurred but was not exported." This does not bear on the within-dataset comparisons used below (all rates are computed on the same export), so it does not block those comparisons, but it does mean absolute traffic-volume claims are not supported.
- Sensitivity checks performed: every pre/post and cross-page comparison below is accompanied by a 95% Wilson-style normal-approximation CI on the difference in proportions, computed before reading the result as discriminating or not, per SKILL.md's interval-check requirement.

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | aggregate post-launch (06-08..06-14) conversion rate > pre-launch (06-01..06-07) rate | proportion test, all sessions, checkout_reached=yes, pre vs post 06-08, 95% CI on the difference | CONTRADICTED | pre 131/4200 = 3.12%, post 125/4971 = 2.51%; diff = -0.60pp, 95% CI (-1.29pp, +0.08pp) (S1). The predicted direction (positive) sits outside the bulk of the interval and the point estimate is negative; the aggregate did not rise |
| T2 | H2 | `/home`, `/product` per-page rates unchanged pre vs post; composition-adjusted post rate ≈ pre rate | proportion test per page pre vs post, 95% CI; reweight post per-page rates by pre-period page-mix weights | CONSISTENT | `/home`: 2.71%→2.68%, diff -0.04pp, CI (-0.90pp, +0.83pp); `/product`: 3.93%→3.76%, diff -0.17pp, CI (-1.62pp, +1.28pp) — both CIs comfortably bracket 0. Composition-adjusted post rate (pre-period page mix applied to post per-page rates) = 3.04%, versus actual pre rate 3.12% and actual post rate 2.51% — adjustment closes nearly all of the aggregate gap (S1) |
| T3 | H3 | `/home`+`/product` conversion after 06-10 deploy differs from the 06-08–06-09 window by more than noise | proportion test, `/home`+`/product` combined, 06-08–06-09 vs 06-10–06-12, 95% CI | NON_DISCRIMINATING | diff = +0.17pp, CI (-1.09pp, +1.43pp) — interval brackets 0, and with ~3,000 sessions across the split this cannot detect an effect smaller than roughly 1pp; day-level rates also continue the same pre-existing 3-day cyclical pattern (2.50%/2.75%/3.00% repeating) uninterrupted through 06-10, with no visible break, but the formal test lacks power to rule out a small deploy effect (S1, S3) |
| T4 | H4 | `/lp/summer-sale` post-launch rate differs from `/home` and `/product` post-launch rates | proportion test, post-launch only, 95% CI on each pairwise difference | CONSISTENT | `/lp/summer-sale` 0.57% vs `/home` 2.68%: diff -2.11pp, CI (-2.87pp, -1.34pp) — excludes 0. `/lp/summer-sale` 0.57% vs `/product` 3.76%: diff -3.19pp, CI (-4.32pp, -2.06pp) — excludes 0. The campaign page converts to checkout at a materially and statistically lower rate than existing traffic sources (S1) |

## Amendments

None. All four hypotheses and their tests were specified before any pre/post or cross-page comparison was computed; only inventory (row counts, field lists, date range, distinct landing pages, null counts) was inspected during orientation.

## Conclusion

- Answer: this data cannot identify a causal lift from launching `/lp/summer-sale`, because no assignment mechanism (randomization or an independent comparison group) is stated or discoverable — visitors were not randomized to see the campaign page. What the data does show: site-wide checkout conversion did not rise after the launch (it fell, 3.12% → 2.51%, T1), and that fall is fully explained by composition — the new campaign page itself converts to checkout at under a quarter the rate of existing pages (0.57% vs 2.68–3.76%, T4), while `/home` and `/product` conversion is unchanged pre vs post at their own rates (T2). Reweighting post-period per-page rates by the pre-period page mix reproduces the pre-launch aggregate almost exactly (3.04% vs 3.12% actual pre). There is no evidence in this window that launching the page improved conversion for anyone; if anything, the plain "did conversion go up" reading is false.
- Best supported: H2 (composition/data-artifact explanation for the aggregate drop), via T2 and T4 — discriminating because it isolates the effect to the new page's own low rate rather than any change in behavior on existing pages, and the composition-adjustment arithmetic reproduces the pre-period aggregate.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | REFUTED | necessary prediction (aggregate conversion rose post-launch) failed under an adequate test, T1 — this refutation does not rely on the unidentified campaign/no-campaign contrast, only on whether the claimed outcome (a rise) occurred at all in the raw aggregate |
  | H2 | data-artifact | UNRESOLVED | best supported (T2, T4 CONSISTENT): per-page rates flat pre/post, composition adjustment closes the gap |
  | H3 | data-artifact / confound | UNRESOLVED | T3 NON_DISCRIMINATING — underpowered to detect an effect smaller than ~1pp from the 06-10 deploy; the unbroken cyclical pattern through 06-10 is suggestive but not a formal refutation |
  | H4 | descriptive | UNRESOLVED | best supported (T4 CONSISTENT, discriminates against H1 by locating the drop in page composition rather than in any causal campaign effect) |
- Limitations: the causal question as posed ("how much did launching it improve conversion") is not answerable from this data — no design identifies the counterfactual (what conversion would have been without the campaign). The observed aggregate change is associative only. Whether the 06-10 checkout-form-refactor deploy had any small effect on conversion is unresolved (T3 underpowered); it does not change the answer either way since the aggregate drop is already fully accounted for by composition. Absolute traffic-volume claims are not supported (S1 completeness semantics are UNKNOWN), though this does not affect the within-export rate comparisons used here. A constructive next step, if a causal answer is wanted, is `causal-identification-review` (when installed) to assess whether a quasi-experimental design (e.g., a pre-registered holdout, geo/channel split, or staggered rollout) could identify the effect going forward.
