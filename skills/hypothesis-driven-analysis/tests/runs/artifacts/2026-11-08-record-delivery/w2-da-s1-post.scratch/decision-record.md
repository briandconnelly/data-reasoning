# Decision Record: ship or hold the 2026-09-12 release carrying the connection-pool change

## Decision frame

- Route: decide
- Actions: ship the release on Friday vs hold the release one week
- Decision owner: the user's release owner (the user, bdc)
- Reversibility: a hold costs one week and is undone by shipping next week; a shipped real regression reaches users until detected and rolled back, which the user prices at about ten times a needless hold
- Deadline or forcing event: Friday release freeze (ledger: 2026-09-12)
- Consequences:

  | | canary served p95 genuinely higher than control | canary served p95 not genuinely higher (measurement artifact or unnamed cause) |
  | --- | --- | --- |
  | ship the release on Friday | loss 10 hold-weeks (missed real regression) | loss 0 |
  | hold the release one week | loss 0 | loss 1 hold-week (needless hold) |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: the canary hosts' served checkout p95 on 2026-09-09 is genuinely higher than control's (ledger H1, descriptive)
- Residual reading: not-H1 includes H2 (exporter sampling artifact) and any explanation nobody named, including noise; H1 as stated says nothing about cause
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the true state; H2 UNRESOLVED folds into the false state, and the false state also absorbs unnamed explanations; no likelihood ratio is taken from the UNRESOLVED tokens

## Evidence and update

- Prior odds: 0.05–1 — provenance: sensitivity-only
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary-control p95 gap over 40 ms observed (T1 gap 57 ms, T3 reference class) | 1–40 | estimated-from-data-in-hand | S2, 20 past canary rollouts in two quota-drawn strata, conditioning on a gap over 40 ms; point 0.9/0.2 = 4.5; range is the ratio of approximate 95% exact binomial bounds (9 of 10: 0.56–1.0; 2 of 10: 0.03–0.56); lower end 1 because H2 predicts the gap with certainty so the generic not-real stratum overstates its rarity |

- Independence: single item
- Posterior odds: 0.05–40

## Robustness

- Prior class swept: 0.05–1 — provenance: sensitivity-only
- Loss range swept: 5–20 — provenance: sensitivity-only
- Crossover: flips at prior odds 0.022–0.1

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: the loss ratio 10 is the user's own "roughly ten times", so the loss side is user-elicited at its centre; the flip to ship needs posterior odds below 1/loss ratio. At loss ratio 10 that is prior odds below 0.1 if the gap carries no information (LR 1) and below 0.022 at the point LR 4.5; at loss ratio 5 the thresholds double and at loss ratio 20 they halve (0.2 and 0.05 posterior). Hold is preferred over most of the swept space, ship wins only for a prior that the gap is real below about 9% with an uninformative gap, or below about 2% with the point LR. No prior is held: none is elicited or sourced, so the prior odds are a sensitivity-only sweep, not a belief and the ledger gives no base rate (S2 is quota-drawn)

## Handoff

- Open factual disputes: H1 versus H2 (served latency versus exporter artifact); T2 needs S3 raw canary access logs, restore request pending, 7-day retention; a flat raw-log p95 would refute H1 and a matching gap would confirm it, either of which moves the posterior far past the crossover
- Identification gaps: attribution of any real gap to the pool change is not established; canary hosts are a fixed rotation chosen independently of traffic, but no identification review covers causal wording
- VoI question: is waiting for the S3 raw-log restore (a free but slow pull of unknown delay) worth more than the hold-week it would replace

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
