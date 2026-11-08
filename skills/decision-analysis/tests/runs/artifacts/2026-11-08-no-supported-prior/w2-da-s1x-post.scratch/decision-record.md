# Decision Record: ship or hold the 2026-09-12 release carrying the pool change

## Decision frame

- Route: decide
- Actions: ship vs hold
- Decision owner: release owner (the user's team)
- Reversibility: hold costs a one-week delay; ship with a real regression costs ten times that
- Deadline or forcing event: Friday release freeze
- Consequences:

  | | H1 true | H1 false |
  | --- | --- | --- |
  | ship | missed real regression, loss 10 | ships, loss 0 |
  | hold | caught regression, loss 0 | needless one-week hold, loss 1 |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: H1 — canary served checkout p95 on 2026-09-09 is genuinely higher than control (real change in what users experience)
- Residual reading: not-H1 includes H2 (exporter sampling artifact) and any explanation nobody named that leaves served latency unchanged
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the true state; H2 UNRESOLVED folds into the false state; the residual absorbs unnamed non-served-latency explanations; no likelihood ratio is taken from either UNRESOLVED token

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap over 40 ms observed (T1 and T3 are one observation: T1 shows it, T3 calibrates it) | 4.5 | estimated-from-data-in-hand | S2 evidence/reference_class.csv, 20 past canary rollouts, conditioned on post-mortem status; P(gap given real)=9/10, P(gap given not real)=2/10; quota-drawn strata so the likelihoods are valid but no base rate is implied; n=10 per stratum so the ratio is imprecise |
  | raw access-log p95 on canary hosts (T2) | none supported | none supported | S3 not acquired, restore pending; NOT_TESTED supplies no likelihood information |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.01–1 — provenance: sensitivity-only
- Loss range swept: 10–10 — provenance: user-elicited
- Crossover: flips at prior odds 0.0222

Arithmetic (conditional, not a belief): posterior odds = prior odds x 4.5. Hold iff posterior odds > 0.1, i.e. prior odds > 0.1/4.5 = 0.0222 (P(H1) about 2.2%). Prior 0.01 gives posterior 0.045, ship. Prior 0.0222 gives 0.1, tie counts as a flip. Prior 0.05 gives 0.225, hold. Prior 1 gives 4.5, hold. At prior odds 0.1 or above, hold holds with LR as low as 1.0. Loss ratio is a single point (rounded "ten", nominal) so it cannot flip; for reference at prior odds p, hold iff loss ratio > 1/(4.5p).

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: no supported prior exists, so the verdict rests on the sensitivity-only class 0.01–1; losses are user-elicited, "ten times" recorded at nominal value with the rounding unconfirmed; LR 4.5 is a point from 9/10 vs 2/10 and is not swept; the LR assumes the 20 past rollouts resemble this one and that the gap itself (which both H1 and H2 predict in the pipeline) is the only evidence; T2 would change this

## Handoff

- Open factual disputes: whether the canary gap survives in raw access logs (H1 vs H2); S3 is retained 7 days and a restore is pending
- Identification gaps: none
- VoI question: is restoring and recomputing p95 from S3 raw logs before Friday worth its cost, given it separates H1 from H2
