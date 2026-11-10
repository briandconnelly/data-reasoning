# Decision Record: Ship release 6.0 now or hold one week after the canary error-rate spike

## Decision frame

- Route: decide
- Actions: ship now vs hold one week
- Decision owner: release owner (the requesting team)
- Reversibility: not stated by the owner; the loss matrix already prices the outcomes in engineer-days
- Deadline or forcing event: Release 6.0 canary spike; one-week hold is the alternative
- Consequences:

  | | real regression | not a real regression |
  | --- | --- | --- |
  | ship now | 10 engineer-days | 0 engineer-days |
  | hold one week | 1 engineer-day | 1 engineer-day |

- Loss ratio: 9 — provenance: user-elicited
- Decision threshold (posterior odds): 0.111 — provenance: user-elicited

## Decision-state model

- Proposition: Release 6.0 contains a real regression as the post-release review would confirm it
- Residual reading: false includes any cause of the canary spike that review would not confirm as a regression, including causes nobody named
- Claim class: predictive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.035 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | first-hour canary error-rate spike observed | 3 | externally-sourced | spike_reference.csv, consortium census of comparable first-hour canaries, quota-drawn 20000 real and 20000 not-real; P(spike given real)=18000/20000=0.9, P(spike given not real)=6000/20000=0.3, LR=0.9/0.3 |

- Independence: single item
- Posterior odds: 0.105

## Robustness

- Prior class swept: 0.035 — provenance: estimated-from-data-in-hand
- Loss range swept: 9 — provenance: user-elicited
- Crossover: none within swept class

## Verdict

- Verdict: robust
- Recommended action: ship now
- Conditions: Prior is the release_history.csv census rate 7 of 207 (odds 7/200), held fixed by the owner as the settled base rate, not varied. Losses are the owner's point values; regret ratio (10-1)/(1-0)=9, threshold 1/9=0.111. Posterior 0.035*3=0.105 sits just under the threshold. Not swept but reported as facts: the prior-odds flip is 0.037 at LR 3 (about 6% higher than the census); the LR flip is 3.18 at the census prior; sampling error on the LR (about 2.92 to 3.08) stays below that. Release 6.0 is assumed exchangeable with past releases and with the consortium canaries. The consortium reference class, not the company's own canaries, supplies the LR.

## Handoff

- Open factual disputes: whether 6.0 is exchangeable with the census releases and the consortium canaries, and whether the spike has a cause identified in the write-up; neither is adjudicated here
- Identification gaps: none
- VoI question: whether one more signal, such as a longer canary window, is worth its cost against a margin this thin

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
