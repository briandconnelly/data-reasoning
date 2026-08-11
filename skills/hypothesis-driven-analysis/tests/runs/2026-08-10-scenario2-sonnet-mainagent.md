# Scenario 2 — 2026-08-10 (Sonnet as main agent)

Wave: Sonnet-as-main-agent, preregistered in `artifacts/2026-08-10-sonnet-mainagent-wave-prereg.md`.
Model: Sonnet, fresh general-purpose subagent acting as main agent, skill loaded by path, forbidden from `tests/scenarios.md` and `tests/runs/`.
Fixture: `s1-conversion/orders.csv`.
Scorer: dispatching session (Fable), against the committed S2 assertions.

| Assertion | Result | Evidence |
| --- | --- | --- |
| Routes direct: computes the median and answers | PASS | Final answer is two sentences: "Median order value in June: $76.36 (268 orders)"; value and count independently recomputed by scorer and exact |
| No ledger, no hypothesis language, no PPDAC ceremony | PASS | Per-arm scratch directory empty (checked by scorer: `ls` shows no files); no route/hypothesis vocabulary in the return |

Total: 2/2.
Tool calls: 3. Tokens: ~45.1k (harness-reported subagent total, includes reading the 315-line SKILL.md).

Verbatim final answer:

> All 268 orders in the file fall in June 2026, so the median is over the full dataset.
> **Median order value in June: $76.36** (268 orders, ranging from $18.37 to $139.74).
