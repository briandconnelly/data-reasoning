# Decision Record: Ship or hold the 2026-09-12 release carrying the connection-pool change

## Decision frame

- Route: decide
- Actions: ship the release on Friday's freeze vs hold the release one week
- Decision owner: the release owner who asked (user)
- Reversibility: ship — a shipped regression is only undone by a later rollback, after users have seen it; hold — fully reversible, costs one week
- Deadline or forcing event: Friday release freeze
- Consequences:

  | | real served-latency regression | no real served-latency regression |
  | --- | --- | --- |
  | ship the release | regression reaches users, loss 10 units | on time, loss 0 |
  | hold the release one week | regression caught, loss 0 | needless one-week hold, loss 1 unit (1 unit = one needless hold) |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: H1 as stated — canary-host served checkout p95 on 2026-09-09 is genuinely higher than control, a real regression in what users experience
- Residual reading: not-H1 includes H2 (exporter sampling artifact) and every explanation nobody named, such as other measurement artifacts or canary/control differences unrelated to served latency
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the true state; H2 UNRESOLVED folds into the false state; the residual absorbs unnamed explanations; no likelihood ratio is taken from either status token

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control p95 gap above 40 ms observed (57 ms, ledger T1) | 4.5 | estimated-from-data-in-hand | S2, 20 past canary rollouts, 9 of 10 post-mortem-settled real regressions showed the gap vs 2 of 10 settled non-regressions, so 0.9/0.2; conditioned on a gap above 40 ms; quota-drawn strata, so the ratio is valid and a base rate is not |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.01–1 — provenance: sensitivity-only
- Loss range swept: 10–10 — provenance: user-elicited
- Crossover: flips at prior odds 0.022

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: posterior odds = prior odds × 4.5, so across the swept prior class they run 0.045–4.5 against the 0.1 threshold; hold is preferred above prior odds 0.022 (prior probability about 2.2%, posterior probability about 9%) and ship below it. Loss crossover at the stated prior ends: flips at loss ratio 22 at prior odds 0.01 and 0.22 at prior odds 1. The prior is sensitivity-only, not a belief. The ratio 4.5 is a point from 20 rollouts with no interval, and it is carried, not swept; the prior crossover generalizes to 0.1 divided by the ratio. T1 supplies the observation only; the gap is the quantity both H1 and H2 explain, so it yields no ratio of its own. Whether the S2 gaps came from the same pipeline as S1 is not stated. The proposition is descriptive: it does not establish that the pool change caused the gap. The loss ratio 10 is the owner's rounded figure, recorded at its nominal value with no swept range.

## Handoff

- Open factual disputes: H1 vs H2 is undecided until the raw access logs (S3, restore pending, 7-day retention) are recomputed; a flat raw-log p95 would refute H1 and a matching gap would refute H2
- Identification gaps: that the pool change, rather than something else on the canary hosts, produced any real gap has no licensing design or review
- VoI question: whether waiting for the pending S3 restore and running T2 before Friday is worth its delay, given a gross value bounded above by 0.91 hold-cost units (loss matrix 10/0/0/1, bound at p = 1/11, a sensitivity-only condition)
