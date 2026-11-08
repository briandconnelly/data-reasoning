# Decision Record: ship or hold the pool-change release at Friday's freeze

## Decision frame

- Route: decide
- Actions: ship vs hold
- Decision owner: release owner (team currently disagrees on the loss ratio)
- Reversibility: hold costs a one-week delay and is recoverable by shipping next week; shipping a real regression costs the user-facing p95 harm plus rollback effort
- Deadline or forcing event: release freeze, Friday
- Consequences:

  | | real served-latency regression true | real served-latency regression false |
  | --- | --- | --- |
  | ship | missed regression, loss L (2 to 20 times one hold-week) | no loss |
  | hold | regression caught, no loss | needless one-week hold, loss 1 |

- Loss ratio: 2–20 — provenance: user-elicited
- Decision threshold (posterior odds): 0.05–0.5 — provenance: user-elicited

## Decision-state model

- Proposition: the canary hosts' served checkout p95 on 2026-09-09 is genuinely higher than control (H1 as stated)
- Residual reading: false includes H2 (exporter sampling artifact) and any other explanation nobody named that leaves served latency unchanged
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into true; H2 UNRESOLVED folds into false; the residual absorbs unnamed non-real explanations; no likelihood ratio is taken from either UNRESOLVED token

## Evidence and update

- Prior odds: 0.02–0.2 — provenance: user-elicited
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap over 40 ms (T1 observed 57 ms, T3 reference class) | 4.5 | estimated-from-data-in-hand | S2, 20 past canary rollouts stratified by post-mortem status; P(gap given real) = 9/10, P(gap given not real) = 2/10, so 0.9/0.2; conditioned on a gap over 40 ms |

- Independence: single item
- Posterior odds: 0.09–0.9

## Robustness

- Prior class swept: 0.02–0.2 — provenance: user-elicited
- Loss range swept: 2–20 — provenance: user-elicited
- Crossover: flips at prior odds 0.111

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: rule is hold iff prior odds x 4.5 x L > 1 (prior x L > 0.222). At L=2 the action flips at prior odds 0.111 (about 1:9); below it ship, above it hold. Loss-ratio crossover at prior 0.02 is L=11.1, at prior 0.1 is L=2.22, at prior 0.2 is L=1.11. At L=20 hold wins across the whole prior class (prior crossover 0.0111, below the class). Ship is preferred only in the corner of low prior (below about 1:9) and L below 0.222/prior. LR 4.5 rests on 10 rollouts per stratum (small n, point value used) and on S2 strata being quota-drawn, which supports the within-stratum frequencies but no base rate; post-mortem labels in S2 are taken as correct. T1's 57 ms gap exceeds the 40 ms threshold used to build the LR, so the LR does not credit the extra margin. The gap comes from the same pipeline H2 questions; the LR does not separate H1 from H2 beyond what S2 shows.

## Handoff

- Open factual disputes: H1 vs H2 is unadjudicated; the discriminating test T2 (raw canary access-log p95) needs S3, whose restore is pending (7-day retention); a result would replace the reference-class LR and could move the verdict to robust
- Identification gaps: none
- VoI question: is restoring and recomputing p95 from S3 raw logs before Friday worth its cost and delay in hold-week-equivalents; cost not stated

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
