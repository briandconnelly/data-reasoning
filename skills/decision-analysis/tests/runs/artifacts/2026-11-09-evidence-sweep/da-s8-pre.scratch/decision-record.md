# Decision Record: Ship or hold the pool-change release at the Friday freeze

## Decision frame

- Route: decide
- Actions: ship the release with the pool change vs hold the release one week
- Decision owner: the release team (decision owner as named by the requester; not identified in the ledger)
- Reversibility: a hold costs one week and is recoverable; a shipped real regression costs a rollback or hotfix after users are affected
- Deadline or forcing event: Friday release freeze
- Consequences:

  | | canary p95 gap is real served latency | canary p95 gap is not real |
  | --- | --- | --- |
  | ship the release with the pool change | missed regression, loss L (units of one needless hold) | no loss |
  | hold the release one week | no loss | needless one-week hold, loss 1 |

- Loss ratio: 2–20 — provenance: user-elicited
- Decision threshold (posterior odds): 0.05–0.5 — provenance: user-elicited

## Decision-state model

- Proposition: the canary hosts' served checkout p95 is genuinely higher than control on the same traffic (ledger H1 as stated, descriptive)
- Residual reading: false means the gap is not a change in served latency, including the exporter-sampling artifact (H2), noise, and explanations nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into true; H2 UNRESOLVED folds into false; the residual absorbs unnamed non-served-latency explanations; no status token supplies a likelihood ratio

## Evidence and update

- Prior odds: 0.02–0.2 — provenance: user-elicited
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap over the 40 ms band (T1, 57 ms) read against past rollouts (T3) | 4.5 | estimated-from-data-in-hand | S2, 20 past canary rollouts stratified 10 real and 10 not real by post-mortem; P(gap given real)=9/10, P(gap given not real)=2/10, ratio 0.9/0.2; conditioned on the gap appearing in the metrics pipeline |

- Independence: single item
- Posterior odds: 0.09–0.9

## Robustness

- Prior class swept: 0.02–0.2 — provenance: user-elicited
- Loss range swept: 2–20 — provenance: user-elicited
- Crossover: flips at prior odds 0.011–0.111

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: hold when prior odds x 4.5 x loss ratio exceeds 1, ship otherwise; the prior-odds crossover is 0.111 at loss ratio 2, 0.044 at loss ratio 5, 0.022 at loss ratio 10 and 0.011 at loss ratio 20, so ship wins only in the low-prior, low-loss corner and hold wins at every prior once the loss ratio reaches 11.1 at the lowest prior; the loss-ratio crossover is 11.1 at prior odds 0.02 and 1.11 at prior odds 0.2, below the swept range, so at the highest prior hold wins at every loss; both prior and loss flip the action; the single LR rests on 10 rollouts per stratum, treats the T1 gap as the same event S2 tabulates, and comes from the same metrics pipeline H2 questions; the proposition is descriptive and does not attribute any gap to the pool change

## Handoff

- Open factual disputes: whether the 57 ms canary gap is served latency or an exporter sampling artifact (H1 vs H2); T2 on restored raw access logs (S3) would discriminate and could move the posterior well outside 0.09–0.9
- Identification gaps: none
- VoI question: is restoring and recomputing p95 from the S3 raw access logs before the Friday freeze worth its restore time against a one-week hold

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
