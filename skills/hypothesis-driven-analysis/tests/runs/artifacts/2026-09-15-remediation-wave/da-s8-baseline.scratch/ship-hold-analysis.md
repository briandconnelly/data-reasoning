# Ship/hold decision analysis — checkout p95 regression (2026-09-12 release)

Source: `data/da-s1-ledger/ledger.md`. Both hypotheses (H1: real regression, H2: exporter
artifact) ended UNRESOLVED — T2, the test that would discriminate them, could not run
(S3 raw access logs not restored in time). Decision must be made from T1 + T3 alone.

## Inputs

- Prior P(real regression), p0: team range 1/50 to 1/5 → [0.02, 0.20]
- Cost ratio k = C(miss real regression) / C(needless 1-week hold): team range [2, 20]
- Evidence: T1 CONSISTENT — canary/control gap 57ms, exceeds the 40ms noise band, every
  canary host above every control host.
- Likelihood ratio for that evidence, from T3's reference class (S2):
  LR = P(gap>40ms | real regression) / P(gap>40ms | not real) = 0.9 / 0.2 = 4.5
  Valid despite S2's quota (case-control) sampling: quota sampling distorts the base
  rate but preserves each stratum's conditional frequency, i.e. exactly the two
  numbers a likelihood ratio needs. It does NOT supply a prior — that's why the prior
  comes from the team's stated range instead of from S2.

## Bayesian update

odds1 = odds0 * LR, where odds0 = p0/(1-p0)

| p0 (prior) | posterior p1 = P(real \| gap observed) |
|---|---|
| 0.02 | 0.084 |
| 0.05 | 0.192 |
| 0.10 | 0.333 |
| 0.15 | 0.443 |
| 0.20 | 0.529 |

Geometric-mean prior (0.063) → posterior 0.233.

## Decision rule

E[cost(ship)] = p1 * C_miss
E[cost(hold)] = (1-p1) * C_hold
Hold iff p1 > p* where p* = 1/(1+k)

Equivalently, hold iff k > k*(p0) = (1-p0)/(4.5*p0)

| p0 | k* (hold if k exceeds this) |
|---|---|
| 0.02 | 10.89 |
| 0.05 | 4.22 |
| 0.10 | 2.00 |
| 0.15 | 1.26 |
| 0.20 | 0.89 |

Team's k range is [2,20], entirely above k*(p0) for p0 >= 0.10, and only below k*(p0)
for p0 <= ~0.10 combined with k on the low end.

## Sensitivity across the full stated ranges

- Geometric-mean point estimate (p0=0.063, k=6.32): posterior 0.233 > threshold 0.137
  → HOLD.
- Log-uniform grid over the full stated ranges of p0 x k: HOLD is favored in ~73% of
  the grid; SHIP only wins in the corner where the prior is near its low end (~0.02-0.05)
  AND the cost ratio is near its low end (~2-4).
- The decision is not robust to the full range (both SHIP and HOLD are reachable at the
  ranges' extremes), but it is not a coin flip either — most of the plausible
  combinations, and both central-tendency estimates, favor HOLD.

## Caveat

This whole analysis stands in for the test that never ran (T2/S3). If raw access logs
can be restored before Friday, that result should override this probabilistic estimate.
