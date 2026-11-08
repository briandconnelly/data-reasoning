Route: estimation (randomization stated by user; no rival hypotheses needed).
Goal: decide whether to ship B over A on the signup page.
Estimand: difference in signup rate (signups/visits), B minus A, pooled over the 14 days; also relative lift.
Population: visitors to the signup page 2026-07-01..07-14, randomized to A or B.
Uncertainty method: 95% (committed in advance) day-block bootstrap, 10000 resamples, seed 1; Wald CI as cross-check.
Practical threshold: none supplied by user; not invented.
Stop condition: one pass; this data cannot tighten it further.
Coverage: 14 dates x 2 variants, all present, no dups, signups<=visits, visits balanced (A 14089, B 13961). Completeness of the export beyond this: unverifiable (no independent denominator).
Result: A 583/14089=4.14%; B 666/13961=4.77%; diff +0.63 pp (95% boot CI +0.13 to +1.12; Wald +0.15 to +1.12); relative lift +15.3% (boot CI +3.1% to +28.3%).
Limitations: single 2-week window; visits may count repeat visitors (unit not stated); randomization taken from user statement, not verified; no threshold.
