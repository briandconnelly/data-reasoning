# Decision Record: ship or hold the pool-change release at the Friday freeze

## Decision frame

- Route: decide
- Actions: ship the release vs hold the release one week
- Decision owner: the release owner / team that sets the Friday freeze
- Reversibility: a hold costs one week of delay and can be lifted next week; a shipped real regression costs user-facing latency until it is detected and rolled back
- Deadline or forcing event: release freeze Friday (ledger: 2026-09-12 release)
- Consequences:

  | | checkout p95 regression is real | checkout p95 regression is not real |
  | --- | --- | --- |
  | ship the release | real regression reaches users (miss cost, 2-20 times the hold cost) | release goes out on time, no loss |
  | hold the release one week | regression caught, one-week hold cost paid | needless one-week hold cost paid |

- Favored if true: hold the release one week
- Loss ratio: 2–20 — provenance: user-elicited
- Decision threshold (posterior odds): 0.05–0.5 — provenance: user-elicited

## Decision-state model

- Proposition: the canary hosts' served checkout p95 on 2026-09-09 is genuinely higher than control (ledger H1 as stated, a real regression in served latency)
- Residual reading: not-H1 includes the exporter-sampling artifact (ledger H2) and any other explanation nobody named that leaves served latency unchanged
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the true state; H2 UNRESOLVED folds into the false state; the residual absorbs unnamed non-real explanations; no likelihood ratio is taken from either UNRESOLVED token

## Evidence and update

- Prior odds: 0.02–0.2 — provenance: user-elicited
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary minus control p95 gap above 40 ms observed (57 ms, every canary host above every control host) | 4.5 | estimated-from-data-in-hand | S2 / ledger T3: 20 past canary rollouts, 9 of 10 post-mortem-real showed the gap and 2 of 10 not-real did, so 0.9 / 0.2; conditioning is the gap exceeding 40 ms; the ratio compares within strata so the analyst-fixed 10/10 quotas do not bias it |

- Independence: single item
- Posterior odds: 0.09–0.9

## Robustness

- Prior class swept: 0.02–0.2 — provenance: user-elicited
- Loss range swept: 2–20 — provenance: user-elicited
- Crossover: flips at prior odds 0.111

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: the prior is the user's stated 1:50 to 1:5 and the losses the stated 2 to 20 times, both user-elicited; the one likelihood ratio of 4.5 comes from 10 and 10 past rollouts, so sampling error is large and is not swept; prior-odds crossover is 1/(4.5 r): 0.111 at r=2, 0.044 at r=5, 0.022 at r=10, and 0.011 at r=20, which is below the swept prior class so at r of about 11.1 or more hold is preferred across the whole prior class; at the lowest prior 0.02 the loss-ratio crossover is 11.1, and at prior 0.2 hold is preferred at every r in the range; the evidence is the same metrics pipeline that H2 questions, and the only discriminating test (T2, raw logs) did not run

## Handoff

- Open factual disputes: whether the exporter sampling changed on the canary hosts on 2026-09-09 (H2), decided by recomputing p95 from the raw access logs (S3, restore pending); a flat raw-log p95 would leave H1 refuted on its necessary prediction
- Identification gaps: none
- VoI question: whether waiting on the S3 raw-log restore, which could settle H1 vs H2 before the freeze, is worth its delay compared with the one-week hold
