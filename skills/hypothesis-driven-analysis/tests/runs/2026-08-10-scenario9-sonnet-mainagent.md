# Scenario 9 — 2026-08-10 (Sonnet as main agent)

Wave: Sonnet-as-main-agent, preregistered in `artifacts/2026-08-10-sonnet-mainagent-wave-prereg.md`.
Model: Sonnet, fresh general-purpose subagent acting as main agent, skill loaded by path, forbidden from `tests/scenarios.md` and `tests/runs/`.
Fixture: `s9-ab/signups.csv`.
Scorer: dispatching session (Fable), against the committed S9 assertions.

| Assertion | Result | Evidence |
| --- | --- | --- |
| Routes estimation: estimand, population, uncertainty statement, practical threshold | PASS | Return states the rate-difference estimand, the two-week population with a generalization caveat, two interval methods (pooled and day-paired), and handles the threshold slot by stating none was given and returning that call to the decision owner |
| No causal "why" hypotheses, no full PPDAC ledger | PASS | Scratch directory empty (scorer-checked); routing paragraph explicitly declines the full loop because "randomization already rules out rival explanations" |
| Estimate with uncertainty, not a bare point | PASS | 0.63pp difference with pooled 95% CI [0.15, 1.12]pp and a wider day-paired interval; scorer recomputed totals (A 583/14,089 = 4.14%, B 666/13,961 = 4.77%) and the pooled CI ([0.15, 1.12]) — exact match |

Total: 3/3.
The predicted at-risk failure for this cell — over-routing to `full` despite stated randomization — did not occur.
Tool calls: 2. Tokens: ~44.3k.

Routing paragraph from the verbatim return:

> **Route used:** this was a randomized experiment with an unambiguous comparison question ("is B better, by how much"), so per the hypothesis-driven-analysis skill I used the **estimation** route (estimand + population + uncertainty method), not the full hypothesis-comparison loop — randomization already rules out rival explanations for the difference.
