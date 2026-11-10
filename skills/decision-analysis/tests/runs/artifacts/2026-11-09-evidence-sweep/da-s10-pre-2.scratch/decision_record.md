# Decision Record: Ship Release 6.0 now or hold one week after canary error-rate spike

## Decision frame

- Route: decide
- Actions: ship now vs hold one week
- Decision owner: release owner (the user's team)
- Reversibility: not stated; losses are given as engineer-days and treated as complete
- Deadline or forcing event: Release 6.0 canary spike; hold window is one week
- Consequences:

  | | real regression | not a real regression |
  | --- | --- | --- |
  | ship now | 10 engineer-days | 0 engineer-days |
  | hold one week | 1 engineer-day | 1 engineer-day |

- Loss ratio: 9 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1111 — provenance: user-elicited

## Decision-state model

- Proposition: Release 6.0 contains a real regression (as the post-release review would confirm it)
- Residual reading: false includes a benign cause of the spike, noise, and any explanation nobody named
- Claim class: predictive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.035 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | first-hour canary error-rate spike observed | 3 | externally-sourced | spike_reference.csv, consortium census of comparable first-hour canaries, fixed 20,000/20,000 quotas by outcome; P(spike given regression)=18000/20000=0.9, P(spike given no regression)=6000/20000=0.3, LR=0.9/0.3 |

- Independence: single item
- Posterior odds: 0.105

## Robustness

- Prior class swept: 0.035 — provenance: estimated-from-data-in-hand
- Loss range swept: 9 — provenance: user-elicited
- Crossover: none within swept class

## Verdict

- Verdict: robust
- Recommended action: ship now
- Conditions: Prior is the complete-census rate 7 of 207 releases (odds 7/200), held fixed at the user's instruction, so the prior class is a single point and cannot flip. Losses are the stated point values (flip threshold odds 1/9). Posterior odds 0.105 sit just under the 0.1111 threshold, so the margin is thin. Outside the swept point, the action flips at posterior odds above 0.1111, i.e. prior odds above 0.0370 (rate about 3.6 percent versus 3.4 percent) or loss ratio above 9.52 (ship-now regression loss above about 10.5 engineer-days). The LR assumes 6.0's canary is exchangeable with the consortium's comparable canaries and that the spike is conditionally independent of the census base rate.

## Handoff

- Open factual disputes: none
- Identification gaps: none
- VoI question: none
