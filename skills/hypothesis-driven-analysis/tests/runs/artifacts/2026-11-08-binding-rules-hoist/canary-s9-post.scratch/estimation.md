# Estimation record (route: estimation; randomization stated by user)
Goal: decide whether to ship B over A.
Estimand: difference in signup rate per visit, B minus A (pooled sum signups / sum visits), also relative lift.
Population: visitors to the signup page 2026-07-01..07-14, randomized to A/B.
Uncertainty method: 95% (committed in advance) Wald/Newcombe interval on rate difference; cross-check with day-level bootstrap (resample days) given daily grain.
Practical threshold: none supplied; report effect so reader can compare to their own (assumption: any positive lift whose interval excludes 0 matters).
Stop condition: one pooled estimate + interval + coverage check (14 days x 2 variants, no gaps, visits balanced).
Coverage matrix plan: date x variant row counts, visits balance, signups<=visits.
Result/Limitations: appended below after analysis.

## Result (script: an.py)
Coverage: 28 rows = 14 dates x {A,B}, no gaps, signups<=visits everywhere. Visits A 14,089 / B 13,961 (SRM chi2=0.58, no imbalance). Completeness vs. an independent denominator: unverifiable (no external count).
A: 583/14,089 = 4.14%. B: 666/13,961 = 4.77%.
Diff (B-A) = +0.63 pp; 95% Wald CI [+0.15, +1.12] pp; day-bootstrap 95% [+0.13, +1.12] pp.
Relative lift = +15.3%; 95% CI [+3.4%, +28.5%] (delta method); bootstrap [+3.1%, +28.2%]. z=2.57. B beat A on 9 of 14 days.
Limitations: unit of randomization is visitor but data is daily aggregates (repeat visitors counted per visit, so intervals may be slightly narrow); signups per visit, not per unique visitor; no downstream quality (activation/retention) data; two weeks only; no practical threshold supplied; randomization taken from user's statement, not verifiable from file.
