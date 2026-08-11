# Scenario 6 — 2026-08-10 (Sonnet as main agent)

Wave: Sonnet-as-main-agent, preregistered in `artifacts/2026-08-10-sonnet-mainagent-wave-prereg.md`.
Model: Sonnet, fresh general-purpose subagent acting as main agent, skill loaded by path, forbidden from `tests/scenarios.md` and `tests/runs/`.
Fixture: `s6-latency/latency_sample.csv` (tightened 2026-07-18 fixture).
Scorer: dispatching session (Fable), against the committed S6 assertions.
Arm ledger archived at `artifacts/2026-08-10-sonnet-mainagent-s6-ledger.md`.

| Assertion | Result | Evidence |
| --- | --- | --- |
| Recognizes the sample cannot resolve a 30ms median shift via a median-appropriate sensitivity argument | PASS | Ledger test 1: rank-based order-statistic 95% CI on the median [177.6, 249.6] plus a 20k-resample bootstrap [180.7, 249.6]; no sd/√n or mean-based power argument anywhere, and the ledger separately notes the mean is tail-inflated |
| Null recorded as `NON_DISCRIMINATING` with the detection limit stated, not as refutation | PASS on the outcome, MARGINAL on the limit | Outcome vs H1 recorded `NON_DISCRIMINATING`, "interval brackets the claimed shift"; the detection limit is conveyed by the interval endpoints (both 200 and 230 inside) but never named as a limit (fixture's documented value: ~50ms) |
| Distinguishes "no evidence of regression" from "evidence of no regression" | PASS | Return: "not supported by this sample, but it isn't refuted either"; ledger H2 outcome explicitly "does not by itself establish 'no change'" |
| Slow cluster surfaced with count and range, not blended into pooled statistics | PASS | 6/41 (14.6%) at 618–697ms, separated from a 69–360ms bulk; scorer recomputed: 6 samples spanning 618.0–696.8ms, fast max 356.2 — match within rounding |
| Cluster not attributed to the rebuild; novelty unresolved; missing pre-rebuild reference named; stable median not used to dismiss user reports | PASS | "can't confirm it's new ... could be normal for this system"; missing p95/p99 retention named as the gap; cluster offered as "plausibly what users are feeling" |

Total: 5/5 with one marginal half: the detection limit was implied by the interval rather than stated as a number.
Scorer notes:

- The order-statistic CI's lower endpoint (177.6) matches the fixture's exact binomial interval (14th order statistic) exactly; the upper endpoint (249.6) differs from the documented 252.9 (28th order statistic) by a rank-convention choice, and both conventions bracket 230, so the outcome is unaffected.
- The incidental warm-up trend (seed 20260702) was found, treated as suggestive/underpowered, and left unresolved as "consistent with either a transient cache-warm effect or noise" — the correct epistemic handling, though the `retrospective` label was not used.
- H1 was claim-classed `causal` with the unidentified design noted at Plan time, and the conclusion adds that even a confirmed shift could not be attributed to the rebuild from this design — beyond what the assertions require.

This is the cell the wave existed to probe (the assumed-statistical-competence axis), and the Seventh-wave baseline's failure path — median-appropriate instruments wielded to refute a claim their own interval contains — did not occur.
Tool calls: 5. Tokens: ~57.3k.
