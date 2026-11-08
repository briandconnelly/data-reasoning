# Decision Record: Ship or hold the 2026-09-12 release carrying the pool change

## Decision frame

- Route: decide
- Actions: ship the release vs hold the release one week
- Decision owner: release owner (user's team)
- Reversibility: hold costs one week and can be undone by shipping later; shipping a real regression reaches users before it can be rolled back
- Deadline or forcing event: release freeze Friday
- Consequences:

  | | canary p95 gap is a real served-latency regression | gap is not real (artifact, noise, or unnamed cause) |
  | --- | --- | --- |
  | ship | missed regression, loss 10 units | no loss |
  | hold | no loss (regression caught) | needless one-week hold, loss 1 unit |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: canary served checkout p95 on 2026-09-09 is genuinely higher than control (ledger H1, descriptive)
- Residual reading: false includes H2 (exporter sampling artifact), noise, and explanations nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into true; H2 UNRESOLVED folds into false; the residual absorbs unnamed non-real explanations; no LR is taken from the UNRESOLVED tokens

## Evidence and update

- Prior odds: 0.05–1 — provenance: sensitivity-only
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | observed canary/control gap of 57 ms, above the 40 ms band (T1) | 4.5 | estimated-from-data-in-hand | S2 within-stratum frequencies: 9/10 real regressions showed the gap vs 2/10 non-regressions, 0.9/0.2; stratified quotas preserve these likelihoods though not the base rate; reference class is 20 settled past canary rollouts |

- Independence: single item
- Posterior odds: 0.225–4.5

## Robustness

- Prior class swept: 0.05–1 — provenance: sensitivity-only
- Loss range swept: 5–20 — provenance: user-elicited
- Crossover: flips at prior odds 0.022

## Verdict

- Verdict: robust
- Recommended action: hold the release one week
- Conditions: holds for prior odds of a real regression of at least 0.05 (about 4.8%) up to even odds, and loss ratios 5–20 (loss crossover 4.4 at the lowest prior); at loss ratio 10 the flip is at prior odds 0.022 (about 2.2%), so ship is preferred only if the owner holds a prior below that; assumes the 57 ms gap is exchangeable with S2's past gaps and that the 0.9/0.2 frequencies transfer; the recommendation does not authorize execution

## Handoff

- Open factual disputes: H1 vs H2 is untested (T2 NOT_TESTED, S3 raw access logs not restored); a flat raw-log p95 would refute the real-regression reading and change the verdict
- Identification gaps: none
- VoI question: whether restoring S3 (retention 7 days, restore pending) and running T2 before Friday is worth its cost against holding a week
