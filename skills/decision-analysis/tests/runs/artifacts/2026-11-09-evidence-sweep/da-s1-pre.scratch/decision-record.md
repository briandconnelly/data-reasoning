# Decision Record: ship or hold the release carrying the connection-pool change, given an unresolved checkout p95 regression

## Decision frame

- Route: decide
- Actions: ship the release vs hold the release one week
- Decision owner: the release owner (user's team)
- Reversibility: holding costs one week of delay and is recoverable; shipping a real regression reaches users and costs roughly ten times a hold
- Deadline or forcing event: release freeze on Friday
- Consequences:

  | | canary p95 gap is a real served-latency regression | canary p95 gap is not a real regression |
  | --- | --- | --- |
  | ship the release | loss 10 (real regression missed) | loss 0 |
  | hold the release one week | loss 0 | loss 1 (needless hold) |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: canary checkout p95 on 2026-09-09 is genuinely higher than control in served latency (H1 as stated)
- Residual reading: not-H1 includes H2 (exporter sampling artifact) and any explanation nobody named that leaves served latency unchanged
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the true state; H2 UNRESOLVED folds into the false state; the residual absorbs unnamed non-regression explanations; no likelihood ratio is taken from either status token

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | Observed canary/control gap over 40 ms (T1 gap 57 ms and T3 are one item: T3 is the reference class for the T1 observation) | 4.5 | estimated-from-data-in-hand | S2, 20 past canary rollouts, P(gap over 40 ms given real) 9/10 over P(gap given not real) 2/10, within-stratum frequencies only, n=10 per stratum so imprecise, conditioned on a gap over 40 ms |
  | T1 as a discriminator between H1 and H2 | none supported | none supported | both H1 and H2 predict a gap in this pipeline, no reference class gives the ratio; not set to 1 |
  | T2 raw-log p95 | none supported | none supported | NOT_TESTED, S3 not acquired, no result to weigh |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.01–1 — provenance: sensitivity-only
- Loss range swept: 10–10 — provenance: user-elicited
- Crossover: flips at prior odds 0.0222

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: hold wins where prior odds times 4.5 exceeds 0.1, so prior odds above 0.0222 (about 2.2 percent chance the change is a real regression before seeing the gap) favor hold and anything lower favors ship; across the swept 0.01–1 class posterior odds run 0.045–4.5 and the action flips only in the bottom of the class; the loss of 10 is rounded ("roughly ten"), recorded at its nominal value with no range; the LR of 4.5 comes from small quota-drawn strata and is carried as a point, not swept; the stratified S2 gives no base rate; the 0.01–1 class is analyst-chosen

## Handoff

- Open factual disputes: whether the 57 ms gap is served latency or an exporter sampling artifact (H1 vs H2); the discriminating test T2 needs the raw access logs S3, restore pending
- Identification gaps: none
- VoI question: whether restoring S3 and running T2 before Friday is worth its cost against a hold of one week
