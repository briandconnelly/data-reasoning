# Decision Record: Ship or hold the release carrying the connection-pool change

## Decision frame

- Route: decide
- Actions: Ship the release Friday vs Hold the release one week
- Decision owner: the user's release owner (the user's team)
- Reversibility: Hold costs one week of delay and can be lifted next week; Ship with a real regression exposes users to the p95 rise until a rollback or fix lands
- Deadline or forcing event: release freeze Friday (ledger: 2026-09-12 release)
- Consequences:

  | | real regression (H1 as stated) | no real regression (artifact or unnamed) |
  | --- | --- | --- |
  | Ship the release Friday | missed real regression, loss 10 | nothing lost, loss 0 |
  | Hold the release one week | regression caught, loss 0 | needless one-week hold, loss 1 |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: Canary hosts' served checkout p95 on 2026-09-09 is genuinely higher than control by more than the 40 ms noise band (ledger H1, a real regression in what users experience)
- Residual reading: "false" is not-H1: the exporter-sampling artifact (ledger H2) plus any explanation nobody named that leaves served latency unchanged
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED maps to the true state; H2 UNRESOLVED maps to the false state; the false state's residual absorbs unnamed non-regression explanations. The UNRESOLVED tokens supply no likelihood information and are not used as evidence.

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | Observed canary-minus-control gap of 57 ms (>40 ms band) in S1, calibrated by T3 on S2 | 4.5 | estimated-from-data-in-hand | S2 (20 past canary rollouts, quota-drawn 10 real / 10 not real): P(gap>40 ms given real)=9/10, P(gap>40 ms given not real)=2/10, LR=0.9/0.2; within-stratum frequencies only, so valid as an LR, not as a base rate; n=10 per stratum, so imprecise |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.01–1 — provenance: sensitivity-only
- Loss range swept: 10–10 — provenance: user-elicited
- Crossover: flips at prior odds 0.022

Arithmetic (posterior odds = prior odds x 4.5; hold when posterior odds > 0.1, tie counts as a flip):
- prior odds 0.01 (p about 1%) -> posterior 0.045 -> Ship
- prior odds 0.022 -> posterior 0.1 -> tie (flip point; 0.1/4.5 = 0.0222)
- prior odds 0.1 (p about 9%) -> posterior 0.45 -> Hold
- prior odds 1 (p 50%) -> posterior 4.5 -> Hold
Ship is preferred only if the pre-evidence chance of a real regression is below about 2.2% (odds 0.022). Hold is preferred over the rest of the swept class.
Loss-ratio crossover (computed at fixed prior, outside the verdict rule): hold iff L x posterior odds > 1. At prior odds 1 (posterior 4.5) it flips to Ship below L = 0.22; at prior odds 0.1 (posterior 0.45) below L = 2.2. Both are far below the stated 10.
LR sensitivity (carried, not swept): a Laplace-smoothed reading (10/12 vs 3/12 = 3.3) moves the prior crossover to 0.03 (p about 2.9%). The conclusion is unchanged.

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: No supported prior exists (S2 is quota-drawn and gives no base rate), so the swept prior class 0.01–1 is sensitivity-only and its low end was chosen by the analyst. The loss ratio 10 is the elicited "roughly ten", recorded at nominal value with no range endpoints supplied. The LR 4.5 rests on 10 rollouts per stratum, and the "not real" stratum's 2/10 gap rate is the only measure of how often an artifact or noise produces the gap. T1's gap comes from the same pipeline that H2 questions, so the record cannot separate real from artifact. Directional reading: Ship requires being more than about 97% sure, before seeing the gap, that the pool change did not regress latency. The record holds no belief of that kind; the owner decides whether they do. Not an authorization to execute either action.

## Handoff

- Open factual disputes: H1 vs H2 (served latency vs exporter artifact) is unadjudicated because T2 did not run; raw canary access logs (S3) restore is pending. A flat raw-log p95 would settle toward Ship and a matching rise toward Hold. Retention is 7 days, so confirm the restore is still possible.
- Identification gaps: none
- VoI question: Is the S3 restore (or an exporter config diff) obtainable before the Friday freeze, and is its cost below the expected cost of a wrong call? Unpriced here; needs cost in the same loss units.

This block states facts, crossovers, and open questions only.
