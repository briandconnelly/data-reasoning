Goal: decide whether to ship B over A on signup conversion.
Estimand: difference in signup rate per visit, B minus A (also relative lift), under stated per-visitor randomization.
Population: visitors to the signup page over the two-week test; generalizes to similar future traffic.
Uncertainty method: 95% CI (committed): Wald and bootstrap over days (paired by day) for the contrast; also check coverage matrix date x variant, sample-ratio.
Practical threshold: not supplied by user; reported against 0 and flagged as an assumption.
Stop condition: one pass of contrast + coverage + day-level consistency check.
Result: A 583/14089 = 4.14%; B 666/13961 = 4.77%; diff +0.63pp, 95% CI Wald [+0.15, +1.12]pp, day-bootstrap [+0.13, +1.12]pp; relative lift +15% (ratio 1.153). B higher on 9/14 days. Coverage: 14 dates x 2 variants complete, no gaps; visit split 50.2/49.8 (SRM z=0.76, fine).
Limitations: user did not give threshold; assignment randomization taken as stated; only signup count, not downstream quality; two weeks only (novelty effects untested); coverage vs independent denominator unverifiable.
