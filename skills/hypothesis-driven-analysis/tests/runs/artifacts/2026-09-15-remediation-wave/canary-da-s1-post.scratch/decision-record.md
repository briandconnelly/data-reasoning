# Decision Record: ship the 2026-09-12 release (connection-pool change) or hold it past Friday's freeze

## Decision frame

- Route: decide — value set per `../skills/decision-analysis/SKILL.md` § Routing (authority)
- Actions: Ship vs Hold
- Decision owner: user (release decision owner)
- Reversibility: Ship, if wrong, means a real p95 regression reaches production and persists until detected and rolled back — the user impact already incurred is not undone by a later rollback. Hold is fully reversible — the release ships next cycle once resolved; the only cost is the delay itself.
- Deadline or forcing event: release freeze Friday (2026-09-18, this week)
- Consequences:

  | | H true (real regression) | H false (artifact/no regression, incl. unnamed explanations) |
  | --- | --- | --- |
  | Ship | Regression ships to production; user-facing latency increase persists until caught and rolled back | No regression; the p95 signal was an artifact; ships cleanly |
  | Hold | Regression caught pre-release; avoided | Needless one-week hold; release delayed for no real gain |

- Loss ratio: 10 — cost of Ship-when-H-true (missing a real regression) relative to cost of Hold-when-H-false (a needless one-week hold) — provenance: user-elicited ("missing a real regression costs roughly ten times what a needless one-week hold costs")
- Decision threshold (posterior odds of H true : H false): 1:10 — derived from the loss ratio above (Ship preferred only below this odds; Hold preferred above it) — provenance: user-elicited (derivation is arithmetic on the stated loss ratio)

## Decision-state model

- Proposition (H): the canary/control p95 gap on 2026-09-09 is a real regression in served checkout latency (ledger's H1, descriptive claim: canary minus control p95, ms)
- Residual reading: not-H covers the ledger's H2 (exporter/sampling artifact inflating measured p95 without a real change in served latency) plus any other unnamed explanation for the gap that no test in the ledger addresses
- Claim class: descriptive (per ledger H1/H2 claim-class field) — not causal; no causal-wording bar applies
- Identification basis: NONE — no causal proposition is being scored
- Identification conditions: none
- Ledger mapping: ledger H1 (UNRESOLVED) folds into H true; ledger H2 (UNRESOLVED) folds into H false; the residual also absorbs any explanation the ledger's two-hypothesis set didn't name. `UNRESOLVED` itself carries no likelihood information — the update below comes only from T1/T3's data, not from the status tokens.

## Evidence and update

- Prior odds: none supported — see Robustness (ledger's S2 quota sampling means the file supports within-stratum frequencies only, and no other prior is sourced)
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | T1+T3 combined: canary/control gap observed at 57 ms (>40 ms threshold; T1), rated against the reference class of 20 past canary rollouts stratified by confirmed post-mortem status (T3) | 4.5 (= 0.9/0.2) | estimated-from-data-in-hand | S2 `evidence/reference_class.csv`: within the "confirmed real" stratum (n=10), 9/10 rollouts showed gap>40ms; within the "confirmed not real" stratum (n=10), 2/10 showed gap>40ms. The quota fixes the stratum sizes, not these within-stratum frequencies, so the ratio is a valid case-control-style likelihood ratio for observing "gap>40ms" given the true state, even though the file cannot supply a base rate (prior). |
  | T2 (raw-access-log recomputation of p95 on canary hosts — the test that would directly discriminate H1 from H2) | none supported | none supported | S3 not acquired before the release decision; restore pending. NOT_TESTED — contributes no update. |

- Independence: T1 and T3 are combined into a single item rather than multiplied — T1 supplies the current observation (gap = 57 ms) and T3 supplies the reference-class likelihood of that observation given each state; multiplying them separately would double-count the same fact.
- Posterior odds: none supported — see Robustness (prior is unsupported; Robustness applies the LR above to a swept prior class instead)

## Robustness

- Prior class swept: 1:10 to 10:1 (odds of H true : H false) — provenance: sensitivity-only (no sourced prior exists; range chosen wide enough to bracket a skeptical-to-favorable belief before seeing T1/T3)
- Loss range swept: 5 to 20 (Ship-when-H-true relative to Hold-when-H-false) — provenance: sensitivity-only (brackets the user's "roughly ten" around the stated central value)
- Crossover:
  - Holding loss ratio at the user-elicited value of 10: the preferred action flips from Hold to Ship only if prior odds fall below ≈1:45 (p(H true) ≈ 2%) — below the entire swept prior class of 1:10 to 10:1.
  - Holding prior odds at the swept class's most skeptical bound (1:10): the preferred action flips from Hold to Ship only if the loss ratio falls below ≈2.2 — below the entire swept loss range of 5 to 20, and well below the user's stated "roughly ten."
  - Across every combination of the swept prior class (1:10–10:1) and swept loss range (5–20), Hold is preferred; the crossover in both dimensions lies outside the swept class.

## Verdict

- Verdict: robust — Hold is preferred across the entire swept prior class and loss range
- Recommended action: Hold
- Conditions: holds given (a) the loss ratio of 10 is user-elicited and taken as approximately correct (robust even down to ~2.2, well outside the stated "roughly ten"); (b) no sourced prior exists, so the verdict rests on the LR from T1+T3 alone being robust to any prior between 1:10 and 10:1 (robust even down to ~1:45, far more skeptical than swept); (c) the S2 reference class's "confirmed not real" stratum is assumed to reasonably include exporter/measurement artifacts like H2, not just other causes — this mapping is a modeling assumption, not tested by the ledger.

## Handoff

- Open factual disputes: whether H1 (real regression) or H2 (exporter/sampling artifact) is actually true remains unresolved — T2 (raw-access-log recomputation) is the discriminating test and has not run; S3 restore is pending. This does not change today's verdict (robust across the swept class), but it is the fact that would let a future decision rest on a supported posterior instead of a swept range. For `hypothesis-driven-analysis` if S3 restores in time.
- Identification gaps: none — no causal proposition was scored in this record.
- VoI question: whether it is worth delaying the ship/hold call until the S3 raw-access-log restore completes (which would let T2 run and directly discriminate H1 from H2) — not priced here; the user asked for a decision under the evidence in hand, not for a price on waiting.
