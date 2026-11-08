# Decision Record: Ship or hold the 2026-09-12 release carrying the pool change

## Decision frame

- Route: decide
- Actions: ship the release vs hold the release one week
- Decision owner: the user's release owner (release freeze Friday)
- Reversibility: hold costs one week of delay and can be undone by shipping next week; a shipped real regression reaches users and is costly to undo
- Deadline or forcing event: release freeze Friday
- Consequences:

  | | H1 true (served p95 really higher) | H1 false (artifact or unnamed non-regression) |
  | --- | --- | --- |
  | ship the release | missed real regression, loss 10 units | no loss, 0 |
  | hold the release one week | regression caught, loss 0 | needless hold, loss 1 unit |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: H1 as stated: canary hosts' served checkout p95 is genuinely higher than control
- Residual reading: not-H1 includes H2 (exporter sampling artifact) and any unnamed explanation under which served latency is not higher
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the proposition; H2 UNRESOLVED folds into the false state together with the unnamed residual; no likelihood ratio is taken from either status token

## Evidence and update

- Prior odds: 0.1–10 — provenance: sensitivity-only
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap over 40 ms observed (T1 and T3 combined) | 4.5 | estimated-from-data-in-hand | S2 ledger T3: 20 past canary rollouts with post-mortems, P(gap\|real)=9/10, P(gap\|not real)=2/10; within-stratum frequencies only, conditioned on the 40 ms gap appearing |

- Independence: single item
- Posterior odds: 0.45–45

## Robustness

- Prior class swept: 0.1–10 — provenance: sensitivity-only
- Loss range swept: 5–20 — provenance: user-elicited
- Crossover: flips at prior odds 0.022

## Verdict

- Verdict: robust
- Recommended action: hold the release one week
- Conditions: prior odds in 0.1–10; loss ratio 5–20 (reading the user's "roughly ten" as a factor-of-two band); LR 4.5 from n=10 per stratum

## Handoff

- Open factual disputes: H1 vs H2 is not discriminated until S3 raw access logs are restored and T2 runs; a flat raw-log p95 would refute H1
- Identification gaps: none
- VoI question: whether the pending S3 restore (T2) can land before Friday and what it costs

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
