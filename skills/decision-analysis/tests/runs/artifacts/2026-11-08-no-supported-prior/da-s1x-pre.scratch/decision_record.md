# Decision Record: ship or hold the 2026-09-12 release carrying the pool change

## Decision frame

- Route: decide
- Actions: ship the 2026-09-12 release vs hold the release one week
- Decision owner: the user's release team (release owner)
- Reversibility: hold costs one week and can be lifted next cycle; shipping a real regression costs rollback plus user-facing latency in the meantime
- Deadline or forcing event: release freeze Friday (2026-09-12 release)
- Consequences:

  | | canary served p95 is genuinely higher (H1 as stated) | canary served p95 is not genuinely higher (artifact or other) |
  | --- | --- | --- |
  | ship the 2026-09-12 release | regression reaches production: loss 10 hold-week-equivalents | no loss: 0 |
  | hold the release one week | no regression shipped: 0 (delay is the cost of the plan, counted under the other state) | needless hold: loss 1 hold-week-equivalent |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: the canary hosts' served checkout p95 on 2026-09-09 was genuinely higher than control (ledger H1, descriptive)
- Residual reading: not-H1 includes the exporter-sampling artifact (ledger H2) and any other explanation nobody named, including a gap that is real in the pipeline but not in served latency
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the true state as stated; H2 UNRESOLVED folds into the false state; the residual absorbs all unnamed explanations; no likelihood is derived from either UNRESOLVED token

## Evidence and update

- Prior odds: 0.05–2 — provenance: sensitivity-only
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap over 40 ms observed (ledger T1 and T3 combined: T1 is the observation itself, T3 prices it) | 1.2–17 | estimated-from-data-in-hand | S2, 20 past canary rollouts with settled post-mortems, quota-drawn 10 real and 10 not-real; P(gap given real)=9/10 and P(gap given not real)=2/10, point LR 4.5; range from 95% Wilson intervals 0.60–0.98 over 0.06–0.51; conditioned on gap over 40 ms; strata are quota-drawn so no base rate is used |

- Independence: single item
- Posterior odds: 0.06–34

## Robustness

- Prior class swept: 0.05–2 — provenance: sensitivity-only
- Loss range swept: 10 — provenance: user-elicited
- Crossover: flips at prior odds 0.006–0.083

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: prior class is sensitivity-only because no base rate exists (S2 is quota-drawn); loss ratio 10 is user-elicited and held fixed; the reference-class LR assumes S2 post-mortem status maps onto H1 true or false and that the 40 ms gap in S2 is measured as in S1; the ship side wins only if prior odds times LR falls below 0.1, i.e. prior odds below about 0.022 at the point LR 4.5, below 0.083 at the pessimistic LR 1.2; the Handoff gap on S3 is unresolved

## Handoff

- Open factual disputes: H1 versus H2 is not discriminated until S3 (raw canary access logs, restore pending) is recomputed; this is the one fact that would move the verdict from prior-sensitive to a stable side; whether the gap is caused by the pool change is not adjudicated
- Identification gaps: nothing licenses attributing any real served-latency gap to the pool change specifically; canary host assignment was independent of traffic per S1 but no design review covers cause
- VoI question: is waiting for the S3 raw-log restore (and recomputing canary p95) worth a one-week hold, given the logs' 7-day retention may lapse before restore completes

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
