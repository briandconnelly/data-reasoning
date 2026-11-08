# Decision Record: ship or hold the pool-change release given an unresolved canary p95 gap

## Decision frame

- Route: decide
- Actions: ship the release on schedule vs hold the release one week
- Decision owner: the user's release owner (freeze Friday)
- Reversibility: a hold costs one week and is recoverable; shipping a real regression costs about ten holds, rollback cost not stated
- Deadline or forcing event: release freeze Friday
- Consequences:

  | | real served-latency regression true | real served-latency regression false |
  | --- | --- | --- |
  | ship | missed regression, loss 10 hold-equivalents | no loss |
  | hold | regression caught, loss 1 hold-equivalent | needless hold, loss 1 hold-equivalent |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: the canary hosts' served checkout p95 is genuinely higher than control's (ledger H1 as stated, descriptive)
- Residual reading: false includes H2 (exporter sampling artifact) and any other measurement artifact nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into true; H2 UNRESOLVED folds into false together with unnamed artifacts; no likelihood taken from the UNRESOLVED tokens

## Evidence and update

- Prior odds: 0.1–10 — provenance: sensitivity-only
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | pipeline gap above 40 ms (T1 observation, scored with T3) | 1.2–20 | estimated-from-data-in-hand | S2, 20 past canary rollouts, within-stratum frequencies 9/10 real vs 2/10 not real (point 4.5), range from small-n intervals; conditioned on a gap appearing in the metrics pipeline |

- Independence: single item
- Posterior odds: 0.12–200

## Robustness

- Prior class swept: 0.1–10 — provenance: sensitivity-only
- Loss range swept: 5–20 — provenance: user-elicited
- Crossover: flips at prior odds 0.17

## Verdict

- Verdict: loss-sensitive
- Recommended action: returned to owner
- Conditions: the flip appears only at the corner of loss ratio 5, LR 1.2 and prior odds below 0.17; at the point LR 4.5 and loss ratio 10 hold wins for any prior odds above 0.022; the prior class is sensitivity-only because S2 is quota-drawn and gives no base rate; T1 and T3 are one observation, counted once; the LR is conditioned on a pipeline-observed gap, and S2 does not say whether its past gaps passed through an exporter that could have changed

## Handoff

- Open factual disputes: whether the exporter sampling changed on 2026-09-09 and whether raw access-log p95 shows the gap (T2, S3 not acquired); this would move the posterior to near 0 or near certainty
- Identification gaps: none
- VoI question: is restoring the S3 raw logs before Friday worth its cost; cost and restore ETA not stated
