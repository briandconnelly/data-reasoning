# Investigation Ledger — S6 Search Latency Regression Claim

## Problem
- Decision: whether to treat "index rebuild slowed search down" as a confirmed regression worth acting on (rollback/investigate rebuild).
- Falsifiable question: is the post-rebuild median request latency elevated relative to the pre-rebuild 200ms reference by roughly the claimed ~30ms, beyond what sampling noise explains — and, if so, is the rebuild an identifiable cause?
- Answered means: a clear CONSISTENT/REFUTED/NON_DISCRIMINATING read on the median-shift claim, plus an explicit statement of whether causal attribution to the rebuild is possible from this data.
- Stop condition / budget: single pass over the one available CSV (41 rows); no further collection possible (fixture is the only data).
- Population/timeframe/units: individual search requests, 6 hours immediately after the rebuild, 2026-07-15 10:00–15:20 UTC, latency in ms, systematic ~1-in-500 sample (~8-minute spacing).

## Data validity
- Source: `s6-latency/latency_sample.csv`, 41 rows, one row per ~8 minutes — consistent with a systematic 1-in-500 sample, not a random sample; no gaps observed in the timestamp sequence.
- Pre-rebuild reference: a single dashboard "200ms median" figure. No pre-rebuild raw data, percentiles, or distribution survived. Measurement pipeline/definition of that 200ms figure (windowing, rounding, inclusion criteria) is unknown — comparability to the CSV's raw per-request latencies is unverified.
- Coverage: only post-rebuild period is observed; no pre-rebuild window, no unaffected comparison group/system exists in this data. This is a pre/post comparison against a single retained summary statistic, not two comparable samples.

## Hypotheses

| # | Hypothesis | Claim class | Necessary prediction |
|---|---|---|---|
| H1 | Rebuild produced a real, ~30ms sustained median regression | causal (unidentified design — no randomization, no comparison group) | Post-rebuild median sits outside the sampling-uncertainty interval around 200ms, i.e., a ~230ms shift is not attributable to noise |
| H2 | No real median shift; apparent regression is sampling noise from a 41-point, 1-in-500 sample | data-artifact | 200ms (and 230ms) both fall inside the sample's 95% CI for the median |
| H3 | A right-tail latency cluster (a subset of slow requests) is what users perceive as "slower," independent of the median | descriptive (estimand: shape/tail of post-rebuild distribution) | A distinct high-latency cluster is present in the post-rebuild sample; cannot be compared to pre-rebuild tail because none was retained, so this stays an open, untested-against-baseline observation |

## Tests run

1. **Order-statistic 95% CI on post-rebuild median** (rank-based, n=41): [177.6, 249.6] ms. Bootstrap 95% CI (20,000 resamples): [180.7, 249.6] ms. Both the null (200ms) and the claimed value (~230ms) fall inside these intervals.
   - Outcome vs H1: NON_DISCRIMINATING (interval brackets the claimed shift; sample too small/coarse to detect it).
   - Outcome vs H2: CONSISTENT, but only because the same test cannot rule H1 out either — does not by itself establish "no change."
2. **Split-half trend check** (first 20 vs last 21 points): median 241ms (first half) vs 183ms (second half); mean 286ms vs 250ms. Weak downward trend across the window (correlation of latency with time index ≈ −0.21), the opposite of a persisting/worsening regression. n=20/half is too small to treat this as adequate on its own.
   - Outcome vs H1's "sustained" reading: NON_DISCRIMINATING (suggestive but underpowered; consistent with either a transient cache-warm effect or noise).
3. **Tail inspection**: 6/41 (14.6%) of sampled requests are 618–697ms, clearly separated from the rest of the distribution (bulk sits at 69–360ms, sample p95≈662ms). Median (202ms) is close to the reference, but mean (267ms) is pulled well above it by this tail.
   - Outcome vs H3: the tail exists in the post-rebuild sample (observed fact), but whether it's *new* is untestable — no pre-rebuild percentile/tail data exists to compare against. Recorded as an open, unattributable finding, not a tested hypothesis outcome.

## Conclusion
- H1: UNRESOLVED (NON_DISCRIMINATING test; a real ~30ms median regression is neither confirmed nor ruled out by 41 sampled points).
- H2: UNRESOLVED (same reason — inadequate power, not evidence of "no effect").
- H3: not a claim with a testable necessary prediction against baseline (no pre-rebuild tail data) — reported as an open observation, not a status.
- Causal attribution to the rebuild specifically: not identifiable from this data even under an assumed shift, because there is no comparison period/group and no information on other changes co-occurring in the 6-hour window (traffic mix, load, concurrent deploys, cache state).
- Stop rule applied: **Stop with limits.** No further collection is available from this fixture; a specific, available test (retaining/comparing p95/p99 and a larger post-rebuild sample, or a pre-rebuild raw sample) could change the answer, but is not available now.
