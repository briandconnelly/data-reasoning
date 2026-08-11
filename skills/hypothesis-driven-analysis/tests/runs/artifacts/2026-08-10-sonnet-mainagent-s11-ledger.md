# Mini-route ledger — checkout p95 latency claim

**Claim:** Checkout p95 latency exceeded 500ms on 2026-07-15.

**Prediction:** If true, at least 5% of that day's checkout requests would have latency_ms > 500, and the p95 order statistic (with a 95% CI) would sit at or above 500ms.
If false, fewer than 5% of requests exceed 500ms and the p95 estimate (with CI) sits below 500ms.

**Probe:** Loaded all 1200 rows of checkout_latency.csv, confirmed single-source contiguous 1-minute cadence with no timestamp gaps, computed p95 (linear-interpolation order statistic, matches nearest-rank), and ran a nonparametric bootstrap (3000 resamples) for a 95% CI around the p95 estimand.

**Result:**
- Full-file p95 = 392.2 ms; bootstrap 95% CI = [374.9, 409.4] ms — does not bracket 500.
- Only 14 of 1200 requests (1.17%) exceeded 500ms, far short of the 5% needed to push p95 past that mark.
- Every hourly sub-window (00:00–19:59) also has p95 well under 500ms (range ~324–460ms).

**Data coverage caveat:** the file runs 2026-07-15T00:00Z to 19:59Z only — 20 of the day's 24 hours, contiguous with no internal gaps, but missing 20:00–23:59.
Nothing in the available data indicates degraded behavior late in the recorded window (hour 19 p95 ≈ 437ms, still well below 500), so there is no signal pointing to a plausible late-day spike, but the last four hours are formally unverifiable from this dataset.

**Outcome:** CONTRADICTED / claim REFUTED for the observed 20-hour window, with the coverage caveat noted above.
