# Decision Record: Ship or hold the 2026-09-12 release carrying the connection-pool change

## Decision frame

- Route: decide
- Actions: ship the release vs hold the release
- Decision owner: release owner (not named in the ledger or request)
- Reversibility: not stated; ship-side rollback cost and hold-side delay cost both unknown
- Deadline or forcing event: 2026-09-12 release (stated in ledger; already past as of 2026-11-08, so treat as a replay of the decision as framed)
- Consequences:

  | | real served-latency regression | no real regression (artifact or other) |
  | --- | --- | --- |
  | ship the release | users get ~57 ms slower checkout p95 until fixed or rolled back | no harm |
  | hold the release | regression avoided; release delayed | release delayed for nothing |

- Loss ratio: 1–10 — provenance: sensitivity-only
- Decision threshold (posterior odds): none stated

## Decision-state model

- Proposition: the canary hosts' served checkout p95 on 2026-09-09 is genuinely higher than control (H1 as stated)
- Residual reading: not-H1 includes the named exporter-sampling artifact (H2) and any explanation nobody named that leaves served latency unchanged
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the true state; H2 UNRESOLVED folds into the false state together with the residual; the UNRESOLVED tokens carry no likelihood information and no ratio is derived from them

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap over 40 ms observed (T1 gap 57 ms; T3 is the reference class for this same observation, so one item) | 4.5 | estimated-from-data-in-hand | S2: 20 past canary rollouts, strata fixed by analyst at 10 real / 10 not real; P(gap given real)=9/10, P(gap given not real)=2/10, so 0.9/0.2; valid as a likelihood ratio because strata are drawn on the state, carries no base rate; n=10 per stratum so imprecise |
  | raw access-log p95 on canary hosts (T2) | none supported | none supported | S3 not acquired, T2 NOT_TESTED, no outcome to weigh |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.02–1 — provenance: sensitivity-only
- Loss range swept: 1–10 — provenance: sensitivity-only
- Crossover: flips at prior odds 0.22

Working (loss ratio R = loss of shipping a real regression / loss of holding needlessly; hold iff posterior odds > 1/R):
- Conditional posterior odds = 4.5 x prior odds: 0.09 at prior 0.02, 4.5 at prior 1 (posterior probability 0.08 to 0.82).
- Prior-odds crossover = 1/(4.5 R): 0.22 at R=1, 0.044 at R=5, 0.022 at R=10. Inside the swept prior class at every R in the range, so the preferred action changes with the prior.
- Loss-ratio crossover at prior odds 1: R = 1/4.5 = 0.22, below the swept range (hold throughout at that prior). At prior odds 0.02: R = 11.1, above the range (ship throughout). At prior odds 0.1: R = 2.2, inside the range.

## Verdict

- Verdict: loss-sensitive
- Recommended action: returned to owner
- Conditions: losses are sensitivity-only (none supplied by the owner), which caps the verdict at loss-sensitive under the ordered rule; prior-sensitivity also present at the stated losses; the LR 4.5 comes from 20 quota-drawn rollouts and holds only if the 40 ms gap behaves in this rollout as in the reference class, and the reference class's non-regression stratum is assumed to include artifact cases; the S2 sample is small, and a ratio stated as a range would be carried but not swept; the prior class is a posited range, not a belief; the 2026-09-12 date is past.

## Handoff

- Open factual disputes: H1 (real served-latency regression) versus H2 (exporter sampling artifact), undiscriminated because T2 did not run; the raw canary access logs (S3) would adjudicate, and the ledger notes 7-day retention with a restore request pending
- Identification gaps: none
- VoI question: whether restoring the S3 raw logs (cost, delay and availability not stated) is worth it against the ship/hold decision; no pull was made or authorized
