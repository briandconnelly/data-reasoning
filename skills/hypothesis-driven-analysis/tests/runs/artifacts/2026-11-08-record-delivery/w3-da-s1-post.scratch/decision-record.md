# Decision Record: ship or hold the 2026-09-12 release carrying the pool change

## Decision frame

- Route: decide
- Actions: ship the release vs hold the release one week
- Decision owner: release owner for the 2026-09-12 freeze
- Reversibility: a hold costs one week and is recoverable; shipping a real regression costs about ten times a hold
- Deadline or forcing event: release freeze Friday 2026-09-12
- Consequences:

  | | real served-latency regression true | real served-latency regression false |
  | --- | --- | --- |
  | ship the release | missed regression, loss 10 hold-equivalents | no loss |
  | hold the release one week | regression caught, no loss | needless hold, loss 1 hold-equivalent |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: the canary p95 rise on 2026-09-09 is a real increase in served checkout latency (H1 as stated)
- Residual reading: false includes the exporter-sampling artifact (H2) and any explanation nobody named that leaves served latency unchanged
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into true; H2 UNRESOLVED folds into false together with the unnamed residual; no likelihood ratio is taken from either status token

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap above 40 ms observed (57 ms, T1) | 4.5 | estimated-from-data-in-hand | S2 (T3): 20 past canary rollouts, stratified by post-mortem status; P(gap given real)=9/10, P(gap given not real)=2/10; within-stratum frequencies only, small n, no base rate used |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.02–1 — provenance: sensitivity-only
- Loss range swept: 10–10 — provenance: user-elicited
- Crossover: flips at prior odds 0.022

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: prior odds are sensitivity-only (S2 is quota-drawn and carries no base rate); posterior odds range 0.09–4.5 (4.5 times prior) against threshold 0.1, so hold wins for any prior odds above 0.022 (about 2.2% prior probability of a real regression) and ship wins only below it; loss ratio is the rounded elicited "roughly ten" held at 10 with no stated range; the LR of 4.5 rests on 9/10 and 2/10 counts and is uncertain; S1 and the exporter in question share one pipeline, and H2 is untested

## Handoff

- Open factual disputes: whether the exporter changed sampling on 2026-09-09 (H2); raw access-log p95 from S3 (restore pending) would discriminate H1 from H2 and move the LR far from 4.5
- Identification gaps: none
- VoI question: whether restoring the S3 raw access logs before Friday is worth its cost and delay relative to the one-week hold

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
