Goal: decide whether to ship signup-page variant B in place of A.
Estimand: difference in signup conversion rate (signups/visits), B minus A, pooled over the two-week test window; also reported as relative lift over A's rate.
Population: all visitors to the signup page during 2026-07-01 to 2026-07-14 (the randomized experiment population); random per-visitor assignment stated by the user, so the pooled contrast is treated as identifying the causal effect of variant on signup rate for this traffic and period.
Uncertainty method: (1) pooled two-proportion Wald 95% CI on the rate difference; (2) day-level bootstrap (20,000 resamples of the 14 days, recomputing pooled rates each draw) as a check that is robust to day-to-day heterogeneity, since both variants share each day's conditions.
Practical threshold: not stated by user; treated as "is the interval bounded away from 0" (i.e., does the sign of the effect hold under uncertainty) since no minimum-detectable-effect or business threshold was given.
Stop condition: estimate is good enough once both interval methods agree in sign and rough magnitude; full daily visitor-level microdata is not available (only daily aggregate counts), so finer-grained methods (e.g. visitor-level regression with covariates) cannot tighten this further from this file.

## Data
- Source: /var/folders/q1/yy47kpf51gb44d8wg1ywz4p80000gq/T/arm-s9-pre-le1bak1n/data/signups.csv
- 28 rows = 14 days x 2 variants (2026-07-01 .. 2026-07-14), no missing variant-days (checked).
- Totals: A = 583/14089 = 4.138%; B = 666/13961 = 4.770%.

## Result
- Pooled diff (B - A) = +0.632 percentage points (95% Wald CI: +0.15pp to +1.12pp).
- Day-level bootstrap 95% CI: +0.14pp to +1.13pp (mean +0.63pp) -- agrees with the pooled estimate.
- Relative lift of B over A: +15.3% (0.632 / 4.138).
- B's daily rate exceeded A's on 9 of 14 days.
- Both interval methods exclude 0 and agree on sign and magnitude -> B's higher conversion rate is not attributable to sampling noise at the 95% level.

## Limitations
- Only daily aggregate visit/signup counts are available, not visitor-level data, so no covariate adjustment (e.g. traffic source, device) or per-visitor variance structure is possible; the binomial/day-bootstrap approach here is the best available in aggregate.
- Randomization is stated by the user, not independently verified from the data (e.g. no allocation-ratio or SRM check possible without visitor-level assignment logs); taken as given per the request.
- No business threshold (minimum detectable/meaningful lift) was supplied, so "better" is reported as a signed, bounded interval rather than judged against a specific bar. If the user has a required minimum lift (e.g. must exceed 0.5pp to justify migration cost), compare it against the CI above.
