# Estimation: Is variant B better than variant A, and by how much?

Route: **estimation**. The user states visitors were randomly assigned to A or B each day for two weeks;
randomization identifies the causal contrast, so no rival explanations need to be told apart — this is a magnitude/comparison question, not a multi-hypothesis diagnosis.

Goal: decide whether to ship B in place of A, and quantify the expected gain in signup rate.
Estimand: the per-visitor signup-rate difference (B − A) and relative lift, pooled over the two-week experiment window (2026-07-01 to 2026-07-14). Signup rate := signups / visits.
Population: visitors to the signup page during the two-week window in which the experiment ran; the estimate generalizes to traffic with a similar composition to this window (see Limitations for what that excludes).
Uncertainty method: two complementary approaches, since assignment is per-visitor but the file only exports day-level aggregates:
  1. Normal-approximation two-proportion 95% CI on the pooled difference (treats visitors as i.i.d. units, ignores day as a block).
  2. Day-cluster bootstrap (resample the 14 days with replacement, recompute the visit-weighted pooled difference each time, 20,000 reps) — respects the fact that A and B were both exposed to the same day-level shocks (weekday/weekend traffic, promos, etc.), so it is the more defensible interval here.
  Cross-check: paired t-test on the 14 unweighted daily (B−A) rate differences, and a sign test on day-level win count as an additional weak-power/direction check.
Practical threshold: not stated by the user. No business-supplied minimum lift or implementation cost was given, so I report the estimate and interval rather than assuming a threshold; the user can compare the interval against their own bar. As a neutral reference: the interval excluding zero at 95% is used below to say whether the sign of the effect is decided by this data.
Stop condition: two independent interval methods (normal-approx and day-cluster bootstrap) agree in sign and rough magnitude, and the daily-level coverage matrix shows no missing day/variant cells → estimate is good enough; stop.

## Data Validity

- Collection method: one CSV row per (date, variant), with visits and signups per day; presumably an export from the experiment's aggregation pipeline.
- Coverage matrix (date × variant, the grain the estimate uses): 14 dates × 2 variants = 28 cells expected; 28 present. No missing date/variant cell.
- Field population: `visits` and `signups` are populated (non-null, positive integers) in all 28 rows.
- Coverage baseline: no independent traffic denominator (e.g., server access logs) was available to cross-check total visits against; daily total visits (A+B) range 1929–2107 with no day near zero or implausibly large, which is consistent with, but does not prove, complete export. Recorded as **unverifiable-but-not-visibly-broken** rather than clean.
- Known instrument failures: none stated or discovered.
- Source completeness semantics: `data/signups.csv` — UNKNOWN. No export contract, sentinel row, or independent denominator was available to distinguish "every visitor is counted" from "some visitors were dropped before aggregation." The absence of any zero/missing day is consistent with completeness but does not establish it discriminatively (a source's own smooth pattern can't certify its own completeness). This is carried into Limitations rather than assumed away.
- Sensitivity checks performed: day-cluster bootstrap (20,000 fresh resamples of the 14-day blocks, each redrawing which days appear and recomputing the whole pooled statistic — not one fixed shifted copy) computed alongside the normal-approximation interval; both read directly, no threshold search.

## Analysis

Per-day rates and per-day (B−A) differences were computed for all 14 days (see `analysis_log.md`... — inline below since the file is short enough to record directly here).

Pooled totals over the 14 days:
- A: 14,089 visits, 583 signups → rate 4.14%
- B: 13,961 visits, 666 signups → rate 4.77%
- Absolute difference (B−A): **+0.63 percentage points**
- Relative lift: **+15.3%**

Randomization-balance check: each day's A/B visit split is close to even (e.g., 988/974, 1010/977, ..., 987/950), consistent with per-visitor random assignment and no evidence of allocation drift across the two weeks.

Aggregation-reversal / confound check: B's daily rate exceeds A's on 9 of 14 days; the pooled direction (B>A) is not produced by one outlier day reversing a uniformly-opposite daily pattern — it is the majority direction, reinforced when weighted by each day's visit volume (bootstrap, below). No weekday/weekend pattern in total traffic or in the A/B split was found that would selectively inflate one arm.

Interval estimates on the pooled difference:
- Normal-approximation (i.i.d. visitor assumption): 95% CI **[+0.15 pp, +1.12 pp]**.
- Day-cluster bootstrap (block = day, 20,000 resamples): 95% CI on absolute difference **[+0.14 pp, +1.13 pp]**; on relative lift **[+3.3%, +28.3%]**. Only 0.54% of bootstrap draws had B ≤ A.
- Paired t-test on the 14 unweighted daily differences: mean +0.63 pp, t = 2.42 (df = 13), 95% CI **[+0.07 pp, +1.19 pp]** — same sign, wider interval, as expected from unweighted day-level pairing with only 14 blocks.
- Sign test (9/14 days B>A): two-sided p = 0.42 — NON_DISCRIMINATING on its own (low power at n=14 counting only wins, not magnitude), but it is not the primary estimator here; it is a weak secondary check and its lack of significance does not contradict the weighted estimates, which use the actual counts rather than just the win/loss sign.

All three magnitude-based methods (normal-approx, day-cluster bootstrap, paired t) agree in sign and in rough magnitude (~0.6 pp absolute, ~15% relative, with 95% CIs that exclude zero). The sign test is directionally consistent (9 of 14 days favor B) but underpowered to discriminate alone, which is expected and does not weaken the weighted result.

## Result

- Estimate: B's signup rate is **0.63 percentage points higher** than A's (4.77% vs 4.14%), a **relative lift of about +15%**.
- 95% CI on the absolute difference: approximately **+0.1 to +1.1 percentage points** (consistent across normal-approximation and day-cluster bootstrap methods).
- 95% CI on the relative lift: approximately **+3% to +28%** (day-cluster bootstrap).
- The interval excludes zero under both interval methods, so this data decides the sign of the effect (B > A) at the 95% level; it does not by itself tell you whether +0.1pp or +1.1pp (the low vs. high end of a wide interval) is "worth it" — that comparison needs a business-stated threshold, which was not provided.

## Limitations

- Source completeness for `data/signups.csv` is UNKNOWN (no export contract or independent denominator to confirm no visitors were dropped before aggregation); if incompleteness were correlated with variant, it could bias the estimate — no evidence of that was found, but none was ruled out either.
- No practical/business threshold was supplied, so "better by how much" is reported as an interval, not a go/no-go verdict; the user should compare the interval above to their own cost/impact bar.
- Estimate is scoped to this two-week window and this traffic mix; if traffic composition (channel mix, seasonality, marketing pushes) differs materially outside this window, the estimate may not transfer.
- Day-level granularity is the finest available; individual-visitor data was not in the file, so within-day heterogeneity (e.g., time-of-day effects) could not be examined.
- Associative-causal framing is warranted here specifically because assignment is stated to be random per visitor with both arms exposed concurrently each day (a comparison group that would have moved the same way absent the intervention) — this is the one case in the routing rules where a causal read of "B causes X pp more signups than A" is licensed by the design itself.
