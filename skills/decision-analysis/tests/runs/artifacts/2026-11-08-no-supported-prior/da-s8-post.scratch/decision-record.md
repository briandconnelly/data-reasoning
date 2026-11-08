# Decision Record: ship or hold the pool-change release at Friday's freeze given an unresolved p95 regression

## Decision frame

- Route: decide
- Actions: ship the release vs hold the release one week
- Decision owner: release owner (team; the team disagrees on the loss ratio)
- Reversibility: hold costs one week of delay and can be lifted; shipping a real regression costs user-facing latency until a fix or rollback ships
- Deadline or forcing event: release freeze Friday
- Consequences:

  | | regression real | regression not real |
  | --- | --- | --- |
  | ship | missed real regression, loss L (in units of one needless hold) | correct, 0 |
  | hold | correct, 0 (one week delay, fix first) | needless one-week hold, loss 1 |

- Loss ratio: 2–20 — provenance: user-elicited
- Decision threshold (posterior odds): 0.05–0.5 — provenance: user-elicited

## Decision-state model

- Proposition: the canary checkout p95 rise on 2026-09-09 reflects a real change in served latency (H1 as stated)
- Residual reading: false includes the exporter-sampling artifact (H2) and any explanation nobody named (e.g. sub-window effects, measurement differences between arms)
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into true; H2 UNRESOLVED folds into false; the residual absorbs unnamed non-real explanations; no LR derived from either status token

## Evidence and update

- Prior odds: 0.02–0.2 — provenance: user-elicited
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap over 40 ms observed (57 ms, T1) | 4.5 | estimated-from-data-in-hand | S2 (T3): 20 past canary rollouts; P(gap given real)=9/10=0.9, P(gap given not real)=2/10=0.2; conditioned on gap over 40 ms; strata quota-drawn so valid for LR only, not base rate; n=10 per stratum |

- Independence: single item
- Posterior odds: 0.09–0.9

## Robustness

- Prior class swept: 0.02–0.2 — provenance: user-elicited
- Loss range swept: 2–20 — provenance: user-elicited
- Crossover: flips at prior odds 0.111 at loss ratio 2; 0.0444 at 5; 0.0222 at 10; 0.0111 (below class) at 20. Hold if prior odds × 4.5 × L > 1.

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: LR 4.5 is a point from 9/10 vs 2/10 (small n, not swept; interval would be wide); gap measured via the same pipeline H2 questions, so the LR is only as good as the past rollouts' pipeline; holding wins at every loss in 2–20 if prior odds are at least 1:9 (0.111); shipping is preferred only when prior odds x 4.5 x L < 1, e.g. prior at or below 1:22 with L=10; loss crossover at prior 0.02 is L=11.1, at prior 0.2 holding wins at all L above 1.11 (whole range); sample from 2026-09-09 data, now stale relative to today (2026-11-08) if the ledger is the only evidence.

## Handoff

- Open factual disputes: H2 exporter artifact vs real served latency; T2 (raw access-log p95 on canary hosts, S3 restore pending, 7-day retention) would discriminate and could move the posterior well outside 0.09–0.9
- Identification gaps: none
- VoI question: is the S3 raw-log restore (T2) worth its cost and delay against the decision, before the freeze

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
