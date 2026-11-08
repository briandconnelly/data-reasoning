# Decision Record: ship or hold the 2026-09-12 release carrying the pool change

## Decision frame

- Route: decide
- Actions: ship the 2026-09-12 release vs hold the release one week
- Decision owner: release owner (user's team)
- Reversibility: hold costs one week of delay; cost of rolling back a shipped regression not stated
- Deadline or forcing event: release freeze Friday (2026-09-12)
- Consequences:

  | | real served-latency regression true | real served-latency regression false |
  | --- | --- | --- |
  | ship the 2026-09-12 release | regression missed: loss 10 units | no loss: 0 |
  | hold the release one week | regression caught: 0 | needless hold: loss 1 unit |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: H1 as stated — canary checkout p95 is genuinely higher than control in served latency (gap >40 ms)
- Residual reading: false = H2 (exporter sampling artifact) plus any unnamed explanation that leaves served latency unchanged
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED -> true; H2 UNRESOLVED -> false; residual -> false. Status tokens supply no LR.

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap >40 ms observed (T1 gap 57 ms; T3 is the same observation, counted once) | 4.5 | estimated-from-data-in-hand | S2: 20 past canary rollouts, 9/10 real regressions showed gap vs 2/10 non-regressions (0.9/0.2); quota-drawn strata so valid for LR only, no base rate; n=10 per stratum so imprecise; assumes non-regression stratum includes exporter artifacts like H2 |
  | raw-log p95 recompute (T2) | none supported | none supported | S3 not acquired; NOT_TESTED, no ratio |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.01–1 — provenance: sensitivity-only
- Loss range swept: 10–10 — provenance: user-elicited
- Crossover: flips at prior odds 0.0222

Arithmetic: posterior = prior x 4.5. Hold iff posterior > 0.1, i.e. prior odds > 0.0222 (prior probability ~2.2%). Swept: prior 0.01 -> posterior 0.045 -> ship; prior 0.0222 -> tie (counts as flip); prior 1 -> posterior 4.5 -> hold.
Side check (not swept, single-point loss): at prior odds 0.1 loss ratio flips at ~2.2; at prior odds 1 at ~0.22.

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: no supported prior exists (no base rate: S2 is quota-drawn); swept prior class is analyst-chosen sensitivity-only; loss 10 is a rounded elicited value taken nominally, no range endpoints supplied; LR 4.5 is from n=20 and assumes the reference class resembles this rollout; LR is a point, its uncertainty not swept; H2 untested.

## Handoff

- Open factual disputes: H1 vs H2 (exporter artifact) is undecided until S3 raw access logs are restored; a flat raw-log p95 would refute H1 and a matching gap would confirm it
- Identification gaps: none
- VoI question: is waiting for/pulling the pending S3 restore (retained 7 days, from 2026-09-09) worth it before Friday's freeze
