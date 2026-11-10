# Decision Record: Release 6.0 after canary error-rate spike — ship now or hold one week

## Decision frame

- Route: decide
- Actions: ship now vs hold one week
- Decision owner: release owner (the user's team)
- Reversibility: not stated; losses already price the outcomes in engineer-days
- Deadline or forcing event: Release 6.0 canary spike; hold would last one week
- Consequences:

  | | real regression | not a real regression |
  | --- | --- | --- |
  | ship now | 10 engineer-days | 0 engineer-days |
  | hold one week | 1 engineer-day | 1 engineer-day |

- Favored if true: hold one week
- Loss ratio: 9 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1111 — provenance: user-elicited

## Decision-state model

- Proposition: Release 6.0 contains a real regression (as confirmed by a post-release review)
- Residual reading: false includes any release where the spike is benign or caused by canary artifacts, load, or other explanations nobody named
- Claim class: predictive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.035 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | first-hour canary error-rate spike | 3 | externally-sourced | spike_reference.csv, consortium census of comparable first-hour canaries across member companies; P(spike given real)=18000/20000=0.9, P(spike given not real)=6000/20000=0.3; quota-drawn so the split carries no base rate; conditioned on the same first-hour spike |

- Independence: single item
- Posterior odds: 0.105

## Robustness

- Prior class swept: 0.035–0.035 — provenance: estimated-from-data-in-hand
- Loss range swept: 9–9 — provenance: user-elicited
- Crossover: flips at likelihood ratio 3.175

## Verdict

- Verdict: robust
- Recommended action: ship now
- Conditions: prior is the complete-census rate 7 of 207 releases (odds 7/200 = 0.035) held fixed at the user's instruction; losses are the user's stated point values; spike LR 3 is a point from counts (sampling 95% interval about 2.94–3.07, below the 3.175 crossover). Margin is thin: posterior odds 0.105 against threshold 0.111. Release 6.0 is assumed exchangeable with the census releases and with the consortium's canaries. Recommendation only; it authorizes nothing.

## Handoff

- Open factual disputes: none
- Identification gaps: none
- VoI question: none
