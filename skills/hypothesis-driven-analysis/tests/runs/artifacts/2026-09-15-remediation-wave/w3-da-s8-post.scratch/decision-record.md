# Decision Record: ship or hold the 2026-09-12 release carrying the connection-pool change, given the UNRESOLVED p95-regression ledger

## Decision frame

- Route: decide
- Actions: ship the release vs hold the release (one week)
- Decision owner: the team calling the ship/hold decision on the pool-change release (not further named by the user)
- Reversibility: shipping is reversible only by a post-hoc rollback/hotfix after users are exposed to whatever the regression turns out to be; holding is fully reversible — the release can still go out next week
- Deadline or forcing event: release freeze Friday (2026-09-18)
- Consequences:

  | | H1 true (real regression) | H1 false (not a real regression) |
  | --- | --- | --- |
  | Ship | misses a real regression — loss L_miss | correct — no loss |
  | Hold | correct — no loss beyond the routine one-week delay | needless one-week hold — loss L_hold |

- Loss ratio: 2–20 — provenance: user-elicited
- Decision threshold (posterior odds): 0.05–0.5 — provenance: user-elicited

## Decision-state model

- Proposition: H1 as stated — the canary hosts' served checkout latency is genuinely higher than control on 2026-09-09, a real regression in what users experience, whatever its cause
- Residual reading: not-H1 covers H2 (exporter-sampling artifact, inflating measured p95 without a served-latency change) plus any other measurement- or artifact-type explanation nobody named; it does not cover a real regression with an unidentified cause, since H1 is stated cause-agnostically ("whatever its cause")
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the "H1 true" state; H2 UNRESOLVED folds into the "H1 false" state; the residual absorbs any unnamed artifact explanation not distinguished from H2 by the tests run

## Evidence and update

- Prior odds: 0.0204–0.25 — provenance: user-elicited
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | Observed 57 ms canary/control gap exceeds the 40 ms discriminating band, calibrated against past rollouts' post-mortem outcomes | 4.5 | estimated-from-data-in-hand | S1 (`host_p95.csv`, 2026-09-09, 6 canary/6 control hosts) for the observed gap; S2 (`reference_class.csv`, 20 past canary rollouts, 10 settled-real/10 settled-not by post-mortem) for the conditional frequencies 9/10 vs 2/10 of the gap exceeding 40 ms within each stratum |

- Independence: single item — T1 (the observed gap) and T3 (the reference-class frequencies) are not independent evidence to multiply; T3 supplies the likelihood ratio for the single fact T1 established (that the observed gap clears the 40 ms band), so they are combined into one item
- Posterior odds: 0.092–1.125

## Robustness

- Prior class swept: 0.0204–0.25 — provenance: user-elicited
- Loss range swept: 2–20 — provenance: user-elicited
- Crossover: Ship is preferred only where prior odds × 4.5 < 1/loss ratio (equivalently, posterior probability of a real regression below the loss-implied threshold probability). Within the swept classes: for prior probability above ≈10% (prior odds above ≈0.111), Hold is preferred at every loss ratio 2–20. For prior probability below ≈1.1% (prior odds below ≈0.0111), Ship would be preferred at every loss ratio 2–20, but this floor sits below the stated prior class's own floor (2%), so it is never reached inside the swept class. Between 2% and 10% prior probability, the flip depends on the loss ratio: Ship needs a loss ratio below 1/(4.5 × prior odds) — about 10.9 at the 2% prior floor, falling to about 2.0 near a 9–10% prior — both values inside the stated 2–20 loss-ratio range.

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: within the stated prior class (2%–20% real-regression probability, user-elicited) and the stated loss range (2–20×, user-elicited), the preferred action flips at the boundary prior odds × 4.5 = 1/loss ratio; Hold dominates the upper half of the stated prior range (above ≈10% probability) regardless of loss ratio, and Ship is reachable only in the lower half of the prior range (2%–10%) and only for loss ratios below roughly 2–11× depending on exactly where the prior sits

## Handoff

- Open factual disputes: whether T2 (raw access-log p95 vs canary exporter config) would refute H2 — it is the one test that discriminates a real regression from an exporter artifact, and it did not run (S3 not acquired); resolving it would sharpen or replace the 4.5 likelihood ratio used here
- Identification gaps: none
- VoI question: whether restoring the retained raw access logs (S3) and running T2 before Friday's freeze is worth its delay cost, given the decision sits inside the prior-sensitive zone identified above
