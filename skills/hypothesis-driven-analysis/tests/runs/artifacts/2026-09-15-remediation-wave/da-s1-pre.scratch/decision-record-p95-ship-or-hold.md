# Decision Record: ship the 2026-09-12-carried release now vs. hold for one week pending p95-regression investigation

## Decision frame

- Route: decide — value set per `../skills/decision-analysis/SKILL.md` § Routing (authority)
- Actions: Ship (proceed with the pending release now) vs Hold (delay ~one week, using the window to restore S3 and run T2)
- Decision owner: the release/on-call decision owner — not named in the request; presumed to be the requester's team
- Reversibility: Ship is hard to reverse once served — if H1 is true, real users already experienced the regression before any rollback lands. Hold is fully reversible — lifting it once T2 resolves the question costs only the elapsed delay.
- Deadline or forcing event: release freeze Friday (2026-09-18, today is 2026-09-15); no default action if undecided is stated in the request.
- Consequences:

  | | H1 true (real regression) | H1 false (not a real regression — includes H2 and unnamed explanations) |
  | --- | --- | --- |
  | Ship | Real p95 regression reaches production users — "missing a real regression" cost | Correctly ship; no cost |
  | Hold | Regression caught before shipping; only the hold's delay cost | Needless one-week hold cost |

- Loss ratio: 10 (cost of shipping a real regression, in units of one needless-hold's cost) — provenance: user-elicited ("roughly ten times", stated in the request)
- Decision threshold (posterior odds): 0.1 — i.e., Hold is preferred once posterior odds of H1 exceed 1:10 (~9.1% probability) — provenance: derived from the user-elicited loss ratio above (threshold odds = 1/loss ratio)

## Decision-state model

- Proposition: H1 as stated in the ledger — the canary/control checkout-p95 gap on 2026-09-09 reflects a real change in served latency (a genuine regression), whatever its cause
- Residual reading: not-H1 includes H2 as named (the exporter/sampling artifact explanation) plus any explanation nobody named (e.g., an unidentified confound not covered by either hypothesis)
- Claim class: descriptive (estimand: canary minus control served checkout p95 on 2026-09-09, ms) — per the ledger's own claim-class field for H1
- Identification basis: NONE — this decision does not require a causal posterior; H1 asks whether the metric reflects real latency, not whether the pool change caused it
- Identification conditions: none
- Ledger mapping: H1 (UNRESOLVED) folds into the "true" state; H2 (UNRESOLVED) folds into the "false" state as the named alternative; the residual absorbs any explanation neither hypothesis named. Per SKILL.md, the UNRESOLVED status tokens themselves carry no likelihood information — the update below is built from the ledger's test outcomes (T1, T3), not from the status column.

## Evidence and update

- Prior odds: 0.1–4 (range swept; no data-based prior is available) — provenance: sensitivity-only. The ledger's only candidate base-rate source, S2, is explicitly quota-drawn (10 real / 10 not-real by construction), so per the ledger's own Data Validity note it "supports within-stratum frequencies... and carries no base rate."
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | Canary/control p95 gap (57 ms) exceeds the pre-registered 40 ms noise band (T1), evaluated against a reference class of 20 past canary rollouts where a >40 ms gap appeared in 9/10 rollouts later settled as real regressions vs. 2/10 settled as not (T3) | 4.5 (0.9/0.2) — treat as approximate given the small quota-drawn strata (10 per stratum) | estimated-from-data-in-hand | S1 `evidence/host_p95.csv` (T1) establishes the gap exceeds the noise band; S2 `evidence/reference_class.csv` (T3) supplies the reference-class detection rate; conditioning: quota-fixed 10/10 split by post-mortem status — this LR carries no base-rate information, only the within-stratum rate at which a qualifying gap appears |

- Independence: single combined item, not two multiplied items. T3's reference-class rate is conditioned on the same qualifying gap that T1 establishes (>40 ms); multiplying T1's and T3's ratios separately would double-count that one underlying observation, per § Numeric Policy.
- Note on discriminating power: per the ledger's own Limitations, "the canary/control contrast... comes from the same pipeline H2 questions" and "no test discriminates H1 from H2 until S3 is restored." T1 alone (gap exceeds noise band) is predicted equally by H1 and H2, so it does not by itself separate the two named hypotheses — it only rules out "nothing happened" (pure noise). The discriminating weight above comes entirely from T3's reference-class comparison, which is why it is reported as one item, not stacked evidence.
- Posterior odds: 0.45–18 (= prior 0.1–4 × LR 4.5) — every value in this range clears the 0.1 decision threshold

## Robustness

- Prior class swept: 0.1–4 (posterior... prior odds; ≈9%–80% probability of a real regression) — provenance: sensitivity-only, spanning a skeptical-to-credulous range since no base rate is available
- Loss range swept: 5–15 (multiple of one needless-hold's cost) — provenance: user-elicited point value 10 ("roughly ten times"), swept ±50% as sensitivity-only to test the "roughly" qualifier
- Crossover: none within swept class — Hold is preferred at every combination of prior odds in [0.1, 4] and loss ratio in [5, 15]. The tightest corner of the swept class (prior odds 0.1, loss ratio 5) still gives posterior odds 0.45 against a threshold of 0.2. Flipping to Ship would require either a prior odds below ≈0.044 (loss ratio 5) to ≈0.022 (loss ratio 10) — i.e., starting out already near-certain (>95%) this is not a real regression — or a loss ratio far below the user's stated "roughly ten times." Both lie outside the swept class as stated.

## Verdict

- Verdict: robust — Hold is preferred across the entire stated prior class and loss range
- Recommended action: Hold
- Conditions: loss ratio ≈10x (user-elicited, swept 5–15 to cover "roughly"); prior probability of a real regression in the 9%–80% range (sensitivity-only, since S2 cannot supply a base rate); evidence likelihood ratio ≈4.5 from the combined T1+T3 observation (estimated-from-data-in-hand, with a small-sample/quota-sampling caveat). The verdict does not depend on resolving H1 vs. H2 — it holds precisely because the evidence in hand cannot yet rule out a real regression, and the stated losses make that residual uncertainty expensive to ship into.

## Handoff

- Open factual disputes: whether H1 or H2 is true remains open — T2 (raw access-log p95 vs. exporter config diff) is the discriminating test and is NOT_TESTED because S3 (raw access logs) was not acquired. Resolving this would change the posterior (and could, if H2 is confirmed and H1 is refuted, move posterior odds below the 0.1 threshold) — routes to `hypothesis-driven-analysis` to continue the ledger once S3 is restored.
- Identification gaps: none — H1 is descriptive, not causal; this decision makes no claim about the pool change causing anything.
- VoI question: whether restoring S3 and running T2 within the hold window is worth its delay/cost, if the user wants that priced formally. Not computed here because the recommended action is already Hold, and the hold period itself provides the natural window to pursue it; a separate VoI record would only be needed if the user is weighing a *faster/costlier* path to restore S3 against extending or shortening the hold.
