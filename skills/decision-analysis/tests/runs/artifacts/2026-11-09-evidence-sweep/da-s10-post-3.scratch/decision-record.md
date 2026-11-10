# Decision Record: Release 6.0 after canary error-rate spike: ship now or hold one week

## Decision frame

- Route: decide
- Actions: ship now vs hold one week
- Decision owner: release owner (the user's team)
- Reversibility: not stated; holding costs 1 engineer-day either way, shipping a real regression costs 10
- Deadline or forcing event: Release 6.0 canary spike; the hold option is one week
- Consequences:

  | | real regression | not a real regression |
  | --- | --- | --- |
  | ship now | 10 engineer-days | 0 engineer-days |
  | hold one week | 1 engineer-day | 1 engineer-day |

- Favored if true: hold one week
- Loss ratio: 9 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1111 — provenance: user-elicited

## Decision-state model

- Proposition: Release 6.0 has a real regression, as the post-release review would confirm it
- Residual reading: false includes a benign canary spike from any cause nobody named (noise, canary-environment artifact, traffic mix)
- Claim class: predictive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.035 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | Release 6.0 first-hour canary showed an error-rate spike | 3.0 | externally-sourced | spike_reference.csv, consortium census of comparable first-hour canaries across member companies; P(spike given regression) = 18000/20000 = 0.9, P(spike given no regression) = 6000/20000 = 0.3, LR = 0.9/0.3; fixed 20,000/20,000 quotas so only the ratio is used, never the split |

- Independence: single item
- Posterior odds: 0.105

## Robustness

- Prior class swept: 0.035 — provenance: estimated-from-data-in-hand
- Loss range swept: 9 — provenance: user-elicited
- Crossover: none within swept class

## Verdict

- Verdict: robust
- Recommended action: ship now
- Conditions: Prior odds 7/200 = 0.035 from the complete release census (7 real regressions in 207 releases, 3.0 through 5.6), held fixed at the user's instruction as the settled base rate; losses are the user's stated point values and are belief-grade; the LR is a point from the consortium reference class and assumes 6.0's canary is exchangeable with it. Margin is thin: posterior odds 0.105 vs threshold 0.1111 (P(regression) about 0.095; expected loss ship about 0.95 vs hold 1.00 engineer-days). Outside the swept class, the action flips to hold one week if the LR product exceeds 0.1111/0.035 = 3.175 (stated LR 3.0), if the prior odds exceed 0.1111/3.0 = 0.0370 (stated 0.035), or if the loss ratio exceeds 1/0.105 = 9.52 (stated 9). Sampling noise in the quota-drawn reference counts is about 0.04 on the LR (rough binomial estimate), well inside the 0.175 gap but not a formal range.

## Handoff

- Open factual disputes: none
- Identification gaps: none
- VoI question: none
