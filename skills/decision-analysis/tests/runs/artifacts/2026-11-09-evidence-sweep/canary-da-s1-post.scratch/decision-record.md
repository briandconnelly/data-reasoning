# Decision Record: ship or hold the pool-change release at Friday's freeze

## Decision frame

- Route: decide
- Actions: ship the release now vs hold the release one week
- Decision owner: the release owner for the 2026-09-12 release (user's team)
- Reversibility: holding costs one week of delay and can be undone by shipping next week; shipping a real regression exposes users until it is found and rolled back
- Deadline or forcing event: release freeze, Friday
- Consequences:

  | | canary p95 regression is real | canary p95 regression is not real |
  | --- | --- | --- |
  | ship the release now | real regression reaches all users (loss 10 units) | release goes out as planned (loss 0) |
  | hold the release one week | regression caught before release (loss 0) | needless one-week hold (loss 1 unit) |

- Favored if true: hold the release one week
- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: the canary hosts' served checkout p95 is genuinely higher than control's (ledger H1 as stated, canary minus control gap above the 40 ms noise band)
- Residual reading: not-H1 includes the exporter-sampling artifact (ledger H2) and any explanation nobody named that leaves served latency unchanged
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the proposition true; H2 UNRESOLVED folds into false together with the unnamed residual; UNRESOLVED status carries no likelihood information and supplies no ratio

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | 57 ms canary-over-control gap observed (ledger T1, T3) | 4.5 | estimated-from-data-in-hand | S2, 20 past canary rollouts, 10 settled-real and 10 settled-not-real strata; P(gap over 40 ms given real) = 9/10 against P(gap given not real) = 2/10; stratified quotas so valid only as within-stratum frequencies, not as a base rate |
  | raw access-log p95 on canary hosts (ledger T2) | none supported | none supported | T2 NOT_TESTED because S3 raw logs were not acquired; no outcome exists to rate |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.01–1 — provenance: sensitivity-only
- Loss range swept: 10–10 — provenance: user-elicited
- Crossover: flips at prior odds 0.0222

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: the loss ratio of 10 is the user's rounded figure ("roughly ten") held at its nominal value with no elicited range; the prior class 0.01–1 is analyst-chosen and sensitivity-only; the single ratio 4.5 rests on 10 rollouts per stratum and is a point estimate with wide sampling uncertainty; at the stated losses the threshold is 0.1, so hold is preferred where prior odds exceed 0.1 divided by 4.5 and ship only below it; the proposition is descriptive and does not by itself attribute any real gap to the pool change

## Handoff

- Open factual disputes: whether raw access-log p95 on the canary hosts shows the same gap (ledger T2, S3 restore pending), which would separate real served latency from an exporter artifact; the ledger is dated September and today is 2026-11-10, so whether S3 is still restorable and the freeze facts still hold needs confirming
- Identification gaps: attribution of any real gap to the pool change is a causal claim with no identification review; the canary rotation is described as chosen independent of traffic and latency but no review covers it
- VoI question: whether restoring S3 and running T2 before the freeze is worth its cost against holding a week
