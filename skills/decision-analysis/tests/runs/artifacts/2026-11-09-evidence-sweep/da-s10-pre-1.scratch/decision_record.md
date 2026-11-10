# Decision Record: Release 6.0 after canary error-rate spike — ship now or hold one week

## Decision frame

- Route: decide
- Actions: ship now vs hold one week
- Decision owner: release owner (the user's team)
- Reversibility: not stated; losses are given in engineer-days and already price the outcomes
- Deadline or forcing event: none
- Consequences:

  | | real regression | not a real regression |
  | --- | --- | --- |
  | ship now | 10 engineer-days | 0 engineer-days |
  | hold one week | 1 engineer-day | 1 engineer-day |

- Loss ratio: 9 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1111 — provenance: user-elicited

## Decision-state model

- Proposition: Release 6.0 contains a real regression (as the post-release review would confirm)
- Residual reading: false includes every non-regression explanation of the canary spike, named or not (noisy canary, load, infra, instrumentation)
- Claim class: predictive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.035 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | first-hour canary error-rate spike | 3 | externally-sourced | spike_reference.csv, consortium census of comparable first-hour canaries; P(spike\|real)=18000/20000=0.9, P(spike\|not real)=6000/20000=0.3; quotas fixed so split is not a base rate |

- Independence: single item
- Posterior odds: 0.105

## Robustness

- Prior class swept: 0.035–0.035 — provenance: estimated-from-data-in-hand
- Loss range swept: 9–9 — provenance: user-elicited
- Crossover: flips at prior odds 0.037

## Verdict

- Verdict: robust
- Recommended action: ship now
- Conditions: prior is the census rate 7/207 (odds 7/200) taken as settled by the user, so the class is a single point; losses are the stated point values; Release 6.0's spike is assumed comparable to the reference class's first-hour spike; the margin is thin (posterior odds 0.105 vs threshold 0.1111, posterior probability about 9.5% vs 10% break-even), so any prior odds above 0.037 (rate above about 3.6%) or loss ratio above 9.5 would flip to hold one week, but neither is within the stated class.

## Handoff

- Open factual disputes: whether Release 6.0's spike matches the reference class's spike definition (magnitude and timing), which is not checkable from the files
- Identification gaps: none
- VoI question: none

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
