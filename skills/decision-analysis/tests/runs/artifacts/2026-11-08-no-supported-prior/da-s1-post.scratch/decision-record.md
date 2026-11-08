# Decision Record: ship or hold the 2026-09-12 release carrying the pool change, given an unresolved checkout p95 gap

## Decision frame

- Route: decide
- Actions: ship the release vs hold the release one week
- Decision owner: release owner for the 2026-09-12 release (the user's team)
- Reversibility: hold costs one week of delay and can be lifted; ship cannot be un-shipped cheaply if the regression is real (rollback cost not stated in the ledger)
- Deadline or forcing event: release freeze Friday
- Consequences:

  | | canary served p95 genuinely higher | canary served p95 not genuinely higher |
  | --- | --- | --- |
  | ship the release | missed real regression: loss 10 units | no loss: 0 units |
  | hold the release one week | no regression shipped: 0 units | needless one-week hold: loss 1 unit |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: H1 as stated: the canary hosts' served checkout p95 on 2026-09-09 is genuinely higher than control's (gap above the 40 ms noise band), in what users experience
- Residual reading: not-H1, including H2 (exporter sampling artifact) and any explanation nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the true state; H2 UNRESOLVED folds into the false state; the residual absorbs unnamed explanations of the gap; the UNRESOLVED status tokens carry no likelihood information and no ratio is derived from them

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap above 40 ms observed (T1, 57 ms; T3 reference class) | 4.5 | estimated-from-data-in-hand | S2, 20 past canary rollouts from the incident tracker, quota-drawn strata of 10 real and 10 not-real by post-mortem; P(gap given real) 9/10 over P(gap given not real) 2/10 = 4.5; conditioning is the gap exceeding 40 ms, which is the T1 observation |
  | raw access-log p95 on canary hosts (T2) | none supported | none supported | S3 not acquired, restore pending; an untested item supplies no ratio and is not given 1 |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.01–1 — provenance: sensitivity-only
- Loss range swept: 10–10 — provenance: user-elicited
- Crossover: flips at prior odds 0.0222

Arithmetic (posterior odds = prior odds x 4.5; hold preferred when posterior odds exceed the threshold 0.1, since 10 x P(H1) > 1 x P(not H1)):

- prior odds 0.01 gives posterior 0.045, below 0.1: ship preferred
- prior odds 0.0222 gives posterior 0.1: tie, counts as a flip
- prior odds 0.05 gives posterior 0.225: hold preferred
- prior odds 1 gives posterior 4.5: hold preferred
- Swept posterior range 0.045–4.5; the threshold 0.1 lies inside it.
- Prior odds 0.0222 is about a 2.2% prior probability that the canary gap reflects a genuine served-latency increase, before seeing the gap.
- Loss crossover at a given prior (not swept; the elicited 10 is a rounded figure with no elicited endpoints): ship is preferred when loss ratio < 1/(4.5 x prior odds). At prior odds 0.01 that is 22.2; at 0.05 it is 4.44; at 0.1 it is 2.22; at 1 it is 0.222.

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: prior class 0.01–1 is sensitivity-only, my declared class, not a belief; the single likelihood ratio 4.5 comes from n=10 per stratum, so it is imprecise, and I carried it as a point and did not sweep it; the strata are quota-drawn, so S2 supports the ratio but carries no base rate and cannot supply a prior; the loss ratio 10 is "roughly ten" recorded at its nominal value with the rounding stated, and its endpoints are not supplied; loss of 1 unit is the one-week hold, and the cost of shipping a regression is set at 10 units with no further components; the proposition is descriptive (canary served latency higher), not a claim that the pool change caused it; gap measured by the same metrics pipeline H2 questions, so T1 cannot rule out H2, and the S2 ratio already averages over artifact cases inside the not-real stratum

## Handoff

- Open factual disputes: whether the canary exporter changed its sampling on 2026-09-09 (H2 against H1), settled only by S3 raw access-log p95 on the canary hosts; S3 has 7-day retention and the restore was pending, so it may no longer be recoverable
- Identification gaps: that the pool change causes any real gap is not established; the contrast is canary versus control on one day with no pre/post comparison and no causal review
- VoI question: is restoring and reading S3 raw logs worth its cost and delay against a one-week hold, given a hold costs 1 unit and the discriminating test would settle H1 versus H2

This block states facts, crossovers, and open questions only.
