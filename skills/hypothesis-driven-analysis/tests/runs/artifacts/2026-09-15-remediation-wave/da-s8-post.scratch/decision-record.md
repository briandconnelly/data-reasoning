# Decision Record: ship or hold the 2026-09-12 release (connection-pool change) given the checkout p95 investigation

## Decision frame

- Route: decide — value set per `../skills/decision-analysis/SKILL.md` § Routing (authority)
- Actions: Ship (proceed with / release the connection-pool change) vs Hold (extend a one-week hold past the Friday freeze)
- Decision owner: the team that owns the release/freeze call (user's team)
- Reversibility: Hold is cheaply reversible — ship next week if the remaining test (T2, raw access logs) clears H2, or once due diligence is judged sufficient; costs one week of delay. Ship's reversibility is not established in the evidence in hand — no rollback-cost or detection-latency data is in the ledger, so a real regression that ships is assumed to run in production until separately caught.
- Deadline or forcing event: release freeze Friday (stated by user)
- Consequences:

  | | H1 true (real regression) | H1 false (artifact or other unnamed cause) |
  | --- | --- | --- |
  | Ship | Users experience the elevated p95 in production; cost = L_miss | No real regression; release proceeds; cost ≈ 0 |
  | Hold | Regression avoided pre-release; cost ≈ 0 | Needless one-week hold; cost = L_hold (reference unit) |

- Loss ratio (L_miss / L_hold): 2–20 — provenance: user-elicited (team gave this range; could not agree on a single point)
- Decision threshold (posterior odds, Ship preferred below it): 1/loss ratio → range 0.05–0.5 (odds 1:20 to 1:2) — provenance: derived from the user-elicited loss ratio above

## Decision-state model

- Proposition: H1 as stated in the ledger — the canary hosts' served checkout latency is genuinely higher than control on 2026-09-09 (a real regression in what users experience), whatever its cause
- Residual reading: not-H1 includes H2 as named (exporter/sampling artifact inflating measured p95 without a real change) plus any other explanation nobody named (e.g., an unmodeled host-level confound) — the ledger identifies no other candidate but does not rule one out
- Claim class: descriptive (per ledger H1 row: estimand = canary minus control served checkout p95 on 2026-09-09, ms) — not causal, so no causal-wording bar or identification review applies
- Identification basis: NONE (not needed — descriptive claim class)
- Identification conditions: none
- Ledger mapping: H1 (UNRESOLVED) maps to "proposition true"; H2 (UNRESOLVED) folds into the residual "proposition false." The residual absorbs H2 plus any other explanation the ledger's tests did not target. `UNRESOLVED` itself carries no likelihood information per the ledger's own ambiguity token — only the individual test outcomes below are used for the update.

## Evidence and update

- Prior odds: 1:49 to 1:4 (from stated probability 1/50 to 1/5 that it's a real regression) — provenance: user-elicited
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | T1 (canary/control gap, S1) | none supported | none supported | reason: non-discriminating between H1 and H2 — T1's data (S1, the metrics pipeline's per-host p95) is exactly the channel H2 questions; H1 predicts the >40 ms gap here, but so does H2 (an inflated exporter would show the identical gap in this same pipeline). The ledger's own Limitations section says this contrast "comes from the same pipeline H2 questions." T1 rules out pure noise but does not move the odds between H1 and the residual. |
  | T3 (reference-class gap frequency, S2) | 4.5 | estimated-from-data-in-hand | source: `evidence/reference_class.csv` (S2); reference class: 20 past canary rollouts with settled post-mortems, quota-drawn 10 real-regression-settled / 10 not-real-settled; conditioning: whether the canary/control p95 gap exceeded 40 ms, given post-mortem status. LR = P(gap>40ms \| real) / P(gap>40ms \| not real) = (9/10)/(2/10) = 4.5. Quota sampling makes the 10/10 split uninformative as a base rate, but the within-stratum frequencies it does support are exactly what a likelihood ratio needs. |

- Independence: single item — T1 contributes no update (none supported); T2 (the test that would discriminate H1 from H2 directly) did not run, so it contributes nothing. Only T3 updates the odds.
- Posterior odds: 1:10.9 to 1.13:1 (prior odds × 4.5) — i.e., roughly 8% to 53% probability of a real regression, recomputable as [1/49 × 4.5, 1/4 × 4.5] = [0.0918, 1.125]

## Robustness

- Prior class swept: 1:49 to 1:4 (posterior probability 2%–20%) — provenance: user-elicited
- Loss range swept: loss ratio 2–20 (threshold odds 0.05–0.5) — provenance: user-elicited
- Crossover: Ship is preferred only where posterior odds < threshold odds, i.e., where (prior odds × 4.5) < (1 / loss ratio), i.e., prior odds × loss ratio < 0.222.
  - At loss ratio = 2 (threshold odds 0.5): prior crossover at odds 0.111 (≈10% prior probability). Below ~10% prior, Ship; above, Hold. The stated prior range (2%–20%) straddles this — **flips within the prior class** at this loss ratio.
  - At loss ratio = 20 (threshold odds 0.05): prior crossover at odds 0.0111 (≈1.1% prior probability), below the entire stated prior range (min 2%) → **Hold is preferred across the full prior range** at this loss ratio.
  - At prior = 1/50 (2%, odds 0.0204): loss-ratio crossover ≈ 10.9. Below it, Ship; above it, Hold. The stated loss range (2–20) straddles this — **flips within the loss range** at this prior.
  - At prior = 1/5 (20%, odds 0.25): loss-ratio crossover ≈ 0.89, below the entire stated loss range (min 2) → **Hold is preferred across the full loss range** at this prior.
  - Net: only the low-prior/low-loss-ratio corner (roughly prior ≤ ~10% combined with loss ratio below its own prior-specific crossover, e.g. prior=2% with loss ratio ≲ 10.9) favors Ship; every other combination in the stated ranges favors Hold, including the entire high-prior end regardless of loss ratio and the entire high-loss-ratio end regardless of prior.

## Verdict

- Verdict: prior-sensitive (the preferred action flips within the stated prior class, and separately within the stated loss range — both crossovers are reported above per the rule for a double flip)
- Recommended action: returned to owner
- Conditions: Ship is defensible only if the team's honest prior on a real regression is at the low end (≈2%, i.e., odds ≈1:49) **and** the loss ratio is judged well below ~11× (i.e., missing a real regression is not much worse than ~10x a needless hold). If the prior is anywhere above ≈10%, or the loss ratio is judged at or above ~11x, Hold is preferred regardless of the other parameter's value within its stated range. The T3 likelihood ratio (4.5) rests on a small reference class (9/10 vs 2/10, n=10 per stratum); its own sampling fragility is not swept here but bears on how much weight the posterior should carry (see Handoff).

## Handoff

- Open factual disputes: (1) the team disagrees on the exact loss ratio (2–20×) — this is a preference/values question, not a factual one, so it belongs with the decision owner, not `hypothesis-driven-analysis`. (2) T3's LR of 4.5 comes from a 20-rollout reference class with only 10 in each stratum (9/10 vs 2/10); a materially different split (e.g., 8/10 vs 3/10 → LR 2.67, or one more/fewer past rollout in either stratum) would shift the posterior and could move it across the robustness boundary above — worth checking whether the incident tracker has more than 20 settled rollouts to shrink this uncertainty, for `hypothesis-driven-analysis` to adjudicate if pursued.
- Identification gaps: none — H1 is a descriptive claim (canary minus control p95), not a causal one, so no identification review is needed for the posterior itself; a causal claim about *why* the pool change caused a regression would need one, but that question is not what's being decided here.
- VoI question: whether restoring S3 (raw access logs, 7-day retention, restore already pending) before Friday would resolve T2 and directly discriminate H1 from H2 is a live collect-more option — worth pricing against the Friday deadline if the restore can plausibly land in time. Not priced here (out of scope for this record — this ask is a decide, not a voi, and no restore ETA or cost was supplied).
