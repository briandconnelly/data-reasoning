# CS3 baseline — 2026-08-09

Arm transcript: `sc-cs3-base.jsonl` (sha256 `3bd5bfe8…`, full digest in `artifacts/2026-08-09-measurement-wave-1-evidence.md`).
No skill loaded; prompt plus staged `cs3-rollout` fixture only.
Scored against `tests/scenarios.md` § CS3.

| Assertion (verbatim) | Result | Evidence |
| --- | --- | --- |
| Names {concurrent change, pre-existing trend, selection into exposure} as identifying threats — all three, not a subset. | PASS | Final text numbers them: "1. West wasn't randomly assigned — it was picked because of its outcomes", "2. West already had a declining trend before rollout", "3. A West-only price promotion launched on the exact same day". |
| Proposes ≥1 probe per named threat: a placebo/falsification check on `avg_order_value` … a pre-period slope comparison … a check of whether West's baseline (pre-rollout) completion time was already an outlier relative to East consistent with the stated targeting criterion (selection into exposure). | PASS | Pre-trend: "Run an event-study/pre-trend check (weekly West vs. East gaps …)"; promotion: cites the AOV shift ($44.80 → $53.99) and proposes "order-level data to control for promo-code usage"; selection: "check whether West's complaint/completion-time metrics were already reverting before the rollout". |
| Every design considered ends on a disposition from the closed set `{identified-if, assumption-contradicted, unresolved, not-constructible}` — no unconditional "valid" or "identified" language anywhere. | FAIL | No closed-set disposition vocabulary appears anywhere in the output; it also writes "plain DiD isn't valid as-is", leaving a repaired DiD implicitly on the table with no recorded disposition. |
| Both the before/after and the East-comparison designs are assigned `assumption-contradicted`, matching the fixture's documented ground truth. | FAIL | Neither design is assigned any disposition; the substance matches (both are rejected) but the closed-set assignment the assertion requires does not exist. |
| Does not propose synthetic control; proposing it fails this assertion regardless of whatever else the review gets right (the infeasible-decoy contract). | FAIL | Grep: "additional untreated comparison regions (synthetic control) instead of relying on East alone" — proposed as a remedy despite the two-region fixture having no donor pool. |
| Route recorded is `review` per SKILL.md … | FAIL | No route is recorded; no record artifact exists (answer is inline, 0 writes in the manifest). |

Total: 2/6.

Comparison note (what the baseline did that the with-skill run did differently): the baseline's threat detection and arithmetic are strong (all three planted threats found, pre-trend medians computed), but it proposed the infeasible synthetic-control decoy, produced no record, no route, and no closed-set dispositions, and offered repair paths ("trend-adjusted DiD") without a disposition discipline — precisely the deltas the with-skill arm closed.

Cost: 34,924 tokens (harness-reported, n=1); 3 tool uses (identity).
