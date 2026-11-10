# Decision Record: Release 6.0 after canary error-rate spike, ship now or hold one week

## Decision frame

- Route: decide
- Actions: ship now vs hold one week
- Decision owner: the release team
- Reversibility: holding costs one week of delay in either state; shipping a real regression costs 10 engineer-days of remediation
- Deadline or forcing event: Release 6.0 canary first-hour spike
- Consequences:

  | | real regression | not a real regression |
  | --- | --- | --- |
  | ship now | 10 engineer-days | 0 engineer-days |
  | hold one week | 1 engineer-day | 1 engineer-day |

- Favored if true: hold one week
- Loss ratio: 9 — provenance: user-elicited
- Decision threshold (posterior odds): 0.111 — provenance: user-elicited

## Decision-state model

- Proposition: Release 6.0 contains a real regression, as post-release review would confirm
- Residual reading: false includes a benign cause of the spike, noise, and explanations nobody named
- Claim class: predictive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.035 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | first-hour canary error-rate spike observed | 3.0 | externally-sourced | spike_reference.csv, consortium census of comparable first-hour canaries, 20,000 confirmed-regression and 20,000 confirmed-not drawn to fixed quotas; P(spike given regression)=18000/20000=0.9, P(spike given not)=6000/20000=0.3 |

- Independence: single item
- Posterior odds: 0.105

## Robustness

- Prior class swept: 0.035–0.035 — provenance: estimated-from-data-in-hand
- Loss range swept: 9–9 — provenance: user-elicited
- Crossover: flips at likelihood ratio 3.175

## Verdict

- Verdict: robust
- Recommended action: ship now
- Conditions: prior is the 7-of-207 census regression rate (odds 7/200), held fixed as the user directs; losses are the user's stated point values; sampling error on the reference counts gives an approximate 95 percent LR interval of 2.93–3.07, below the 3.175 flip point; the margin is thin (posterior odds 0.105 against threshold 0.111, posterior probability about 9.5 percent), so any input change such as a canary less comparable to the reference class than assumed can reverse the action

## Handoff

- Open factual disputes: whether Release 6.0's canary spike is comparable to the consortium's first-hour spike definition, which would move the LR
- Identification gaps: none
- VoI question: none
