# Decision Record: Ship or hold the 2026-09-12 release carrying the pool change, given an unresolved p95 regression

## Decision frame

- Route: decide
- Actions: ship the release at Friday's freeze vs hold the release one week
- Decision owner: the release team (the user's team; owner not named in the ask)
- Reversibility: hold costs one week of delay and is recoverable; ship leaves a real regression in production until it is found and rolled back or fixed (rollback cost not stated)
- Deadline or forcing event: release freeze Friday
- Consequences:

  | | canary served p95 is genuinely higher (real regression) | not real (exporter artifact or unnamed explanation) |
  | --- | --- | --- |
  | ship | missed regression, loss k·c | no loss |
  | hold | no loss (regression kept out) | needless one-week hold, loss c |

- Loss ratio: 2–20 — provenance: user-elicited
- Decision threshold (posterior odds): 0.05–0.5 — provenance: user-elicited

## Decision-state model

- Proposition: the canary hosts' served checkout p95 on 2026-09-09 is genuinely higher than control, i.e. a real change in what users experience (ledger H1 as stated)
- Residual reading: false includes H2 (exporter sampling change inflating measured p95) and any other measurement artifact or explanation nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into true; H2 UNRESOLVED folds into false together with the residual; no likelihood ratio is taken from either status token

## Evidence and update

- Prior odds: 0.02–0.2 — provenance: user-elicited
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap exceeds the 40 ms band (T1 observed 57 ms; T3 tabulates the same event) | 4.5 | estimated-from-data-in-hand | S2, 20 past canary rollouts, within-stratum frequencies: P(gap given real) = 9/10, P(gap given not real) = 2/10, ratio 0.9/0.2; conditioned on a >40 ms gap appearing; strata quota-drawn so no base rate is used |

- Independence: single item
- Posterior odds: 0.09–0.9

## Robustness

- Prior class swept: 0.02–0.2 — provenance: user-elicited
- Loss range swept: 2–20 — provenance: user-elicited
- Crossover: flips at prior odds 0.011–0.111

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: Rule is hold iff posterior odds exceed 1/k, i.e. prior odds exceed 1/(4.5k). Prior-odds crossover is 0.111 at k=2 and 0.0111 at k=20; at k=20 the crossover lies below the swept class floor, so hold wins across the whole class there. At k=2, prior odds below 0.111 (about 1:9) favour ship, above favour hold. Loss-ratio crossover k* = 1/(4.5 × prior): 11.1 at prior 0.02 (1:50), 4.4 at 0.05 (1:20), 2.2 at 0.1 (1:10), 1.1 at 0.2 (1:5, below the swept range, so hold at every k). Ship wins only in the low-prior, low-k corner: prior below 0.111 and k below 1/(4.5 × prior). LR 4.5 comes from 10 vs 10 rollouts (small n), is carried as a point and not swept, and rests on the gap having been measured by the same pipeline H2 questions. The loss ratio is user-elicited, but the team disagrees on it, so the owner must pick it. The posterior is about the descriptive claim only; attribution of any real gap to the pool change is not covered. Dates: the ledger is dated 2026-09 while today is 2026-11-08; whether the Friday freeze and the S3 restore are still live is unverified.

## Handoff

- Open factual disputes: H1 (served latency genuinely higher) vs H2 (exporter sampling artifact) is unadjudicated; T2 (raw access-log p95 on canary hosts, S3, restore pending, 7-day retention) is the discriminating test and would move the posterior far outside 0.09–0.9
- Identification gaps: none for the descriptive claim; whether a real gap was caused by the pool change rather than host-level differences is not addressed, though the canary rotation was fixed independent of traffic and latency
- VoI question: is restoring S3 and running T2 before Friday worth its cost (restore time, effort, delay), given the hold costs one week

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
