# Decision Record: ship or hold the 2026-09-12 release carrying the connection-pool change

## Decision frame

- Route: decide
- Actions: ship vs hold
- Decision owner: the release owner for the 2026-09-12 release (the user's team)
- Reversibility: hold costs a one-week delay and is undone by shipping next week; ship exposes users to the regression until it is detected and rolled back
- Deadline or forcing event: release freeze Friday
- Consequences:

  | | canary checkout p95 is genuinely higher | canary checkout p95 is not genuinely higher |
  | --- | --- | --- |
  | ship | missed real regression, loss 10 units | no loss, 0 units |
  | hold | regression caught, 0 units | needless one-week hold, loss 1 unit |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: the canary hosts' served checkout p95 on 2026-09-09 is genuinely higher than control (H1 as stated in the ledger)
- Residual reading: false includes H2 (exporter sampling artifact) and any unnamed explanation under which served latency did not rise
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into true; H2 UNRESOLVED folds into false and the residual absorbs unnamed non-regression explanations; no likelihood derived from either status token

## Evidence and update

- Prior odds: 0.01–1 — provenance: sensitivity-only
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap over 40 ms observed (57 ms, T1), scored against past rollouts (T3) | 4.5 | estimated-from-data-in-hand | S2, 20 past canary rollouts, quota-drawn strata of 10 real and 10 not-real by post-mortem; P(gap given real)=9/10 over P(gap given not real)=2/10, conditioned on stratum; 10 per stratum so the ratio is imprecise |

- Independence: single item
- Posterior odds: 0.045–4.5

## Robustness

- Prior class swept: 0.01–1 — provenance: sensitivity-only
- Loss range swept: 5–20 — provenance: user-elicited
- Crossover: flips at prior odds 0.011–0.044

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: posterior odds are compared with threshold 1/loss ratio (0.05–0.2, point 0.1); hold wins whenever prior odds exceed 0.0222 at loss ratio 10 (prior probability above about 2.2% before seeing the gap), the range 0.011–0.044 covering loss ratios 20 to 5; the LR of 4.5 is one imprecise stratified estimate, and if the true LR were near 2 or lower the crossover prior odds would rise to 0.05 or above; losses are the user's rough figure of ten times, with hold costing 1 unit only when no regression is real; the prior class is a stated sweep and not a belief; nothing here adjudicates H1 against H2

## Handoff

- Open factual disputes: whether raw access logs (S3) show the same canary gap, which separates H1 from H2 and would move the posterior far beyond the LR above
- Identification gaps: none
- VoI question: whether restoring the S3 raw access logs before the freeze is worth its restore cost and delay, priced in units of the loss ratio
