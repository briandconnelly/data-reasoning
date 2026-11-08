# Decision Record: ship or hold the release carrying the connection-pool change

## Decision frame

- Route: decide
- Actions: ship vs hold
- Decision owner: the user's release owner (release freeze Friday)
- Reversibility: hold costs one week of delay and is undone by releasing next week; ship with a real regression has an unquantified rollback and user-impact cost, folded into the elicited loss ratio
- Deadline or forcing event: release freeze Friday
- Consequences:

  | | served canary latency genuinely higher | served canary latency not genuinely higher |
  | --- | --- | --- |
  | ship | missed real regression, loss 10 | no loss, 0 |
  | hold | regression caught, loss 0 | needless one-week hold, loss 1 |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: H1 as stated: the canary hosts' served checkout p95 on 2026-09-09 is genuinely higher than control's, a real change in what users experience
- Residual reading: not-H1 includes H2 (exporter sampling artifact) and any explanation nobody named that leaves served latency unchanged
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the true state; H2 UNRESOLVED folds into the false state together with the unnamed residual; no likelihood ratio is taken from either status token

## Evidence and update

- Prior odds: none needed
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control p95 gap above 40 ms observed (T1: 57 ms, every canary host above every control host) | 4.5 | estimated-from-data-in-hand | S2 reference class of 20 past canary rollouts; P(gap given real regression)=9/10 and P(gap given not)=2/10 from within-stratum frequencies, which quota sampling leaves valid for an LR; n=10 per stratum so the ratio is imprecise; conditioning is gap above 40 ms in the same pipeline |

- Independence: single item
- Posterior odds: none needed

## Robustness

- Prior class swept: 0.1–10 — provenance: sensitivity-only
- Loss range swept: 5–20 — provenance: user-elicited
- Crossover: flips at prior odds 0.022

## Verdict

- Verdict: robust
- Recommended action: hold
- Conditions: no prior is held; sweeping posited prior odds 0.1–10 gives posterior odds 0.45–45 against threshold 0.1; hold is preferred when posterior odds exceed 1/L; with LR 4.5 and L=10 the flip is at prior odds 0.022 (about 2% probability), below the whole swept prior class; at prior odds 0.1 the loss ratio flips at L=2.2, below the swept range of 5–20; with LR 1 (S2 ignored) hold still wins for prior odds above 0.1; the verdict fails if one believes H1 is under 2% likely before seeing the gap, or if the loss ratio is under about 2; T1 and S2 both come from the metrics pipeline H2 questions, so the LR assumes S2's gaps were measured the same way; the prior class is a posited range, not a belief

## Handoff

- Open factual disputes: whether the 57 ms gap is real served latency or an exporter sampling artifact (H2, T2 NOT_TESTED because raw logs S3 were not acquired); the ledger gives S3 7-day retention with a restore pending, so check whether the restore is still possible
- Identification gaps: whether the pool change causes any real gap is not established; the canary hosts were chosen independently of traffic and latency but no identification review was done
- VoI question: whether restoring S3 and running T2 before Friday is worth its cost, since a flat raw-log p95 would refute H1 and could flip the decision to ship
