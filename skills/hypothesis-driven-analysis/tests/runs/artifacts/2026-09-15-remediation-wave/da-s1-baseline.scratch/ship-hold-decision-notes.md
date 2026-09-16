# Ship/hold decision notes — checkout p95 regression (2026-09-12 release)

Source: ledger.md (unresolved investigation, H1 real-regression vs H2 data-artifact)

## What the ledger actually supports

- T1 (H1, CONSISTENT): canary mean 468ms vs control 411ms, gap 57ms > 40ms noise
  band. Every single canary host beats every single control host — full
  separation, not just a mean difference inside overlapping distributions.
  Strong direct evidence of a canary/control difference in the metrics
  pipeline's numbers.
- T3 (H1, CONSISTENT): reference class of 20 past rollouts (quota-drawn 10/10
  real vs not-real, so no base rate). Within strata: gap>40ms appeared in 9/10
  real regressions, 2/10 non-regressions. That's a likelihood ratio of ~4.5:1
  for "gap implies real" — meaningful Bayesian evidence even without a prior/
  base rate, since it only requires the within-stratum frequencies, not the
  stratum sizes.
- T2 (H2, NOT_TESTED): the one test that could isolate "real served-latency
  change" from "exporter artifact on canary hosts" never ran — raw access
  logs (S3) aren't restored yet. H2 is UNTESTED, not weakened and not
  supported. Zero evidence either way.

Net: both direct evidence (T1) and analogous evidence (T3) point toward H1
(real regression). Nothing in the ledger points toward H2 (artifact) — it's
just an open possibility that hasn't been checked.

## Decision framing: asymmetric cost

Given: cost(miss real regression) = 10 x cost(needless one-week hold).

Let p = P(H1 true | evidence) = probability the regression is real.

- Expected cost of shipping = p * 10
- Expected cost of holding  = (1-p) * 1

Ship is only the better expected-cost choice when p*10 < (1-p)*1, i.e.
p < 1/11 ≈ 9%.

So shipping is only justified if we're >91% confident this is a measurement
artifact, not a real regression.

## Does the evidence support p < 9%?

No. If anything it points the opposite direction:
- T1 shows full host-level separation well past the pre-established noise
  band — hard to explain away without an artifact mechanism, and no artifact
  mechanism has been demonstrated (S3/T2 never ran).
- T3's likelihood ratio (~4.5:1 favoring "real" given the gap is observed)
  would need a very strong prior toward "artifact" to pull posterior p below
  9%, and no such prior is documented in the ledger.
- The one test that could have raised confidence in H2 (T2) simply didn't
  run — its absence is not evidence for H2, it's an information gap.

Under the stated cost ratio, this evidence does not clear the bar needed to
ship. The rational move is to hold pending the missing test, not to treat
"H2 is merely untested" as license to ship.

## Caveats carried forward from the ledger

- T3's 9/10 vs 2/10 comes from quota-drawn strata (10 real / 10 not, fixed by
  the analyst) — it licenses within-stratum frequencies and a likelihood
  ratio, not a base rate or a direct posterior probability for this incident.
- The canary/control contrast (T1) comes from the same metrics pipeline that
  H2 questions — it's evidence of *a* gap, not yet proof the gap reflects
  what users experienced.
- S3 restore is pending (7-day retention, request in flight) — if it lands
  before Friday, T2 should be run immediately; it's the only test that can
  actually resolve H1 vs H2 rather than argue about priors.

## Recommendation

HOLD the 2026-09-12 release pending T2. Push to expedite the S3 restore;
if raw logs land before the freeze, run T2 and re-decide with a real
discriminating result instead of a cost-ratio argument.
