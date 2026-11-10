# Decision Record: Ship release 6.0 now or hold one week after a canary error-rate spike

## Decision frame

- Route: decide
- Actions: ship now vs hold one week
- Decision owner: the release team (the user's team)
- Reversibility: not stated; losses already price a shipped regression at 10 engineer-days and a hold at 1
- Deadline or forcing event: release 6.0 canary spike observed in its first hour; no other date given
- Consequences:

  | | real regression | not a real regression |
  | --- | --- | --- |
  | ship now | 10 engineer-days | 0 engineer-days |
  | hold one week | 1 engineer-day | 1 engineer-day |

- Favored if true: hold one week
- Loss ratio: 9 — provenance: user-elicited
- Decision threshold (posterior odds): 0.111 — provenance: user-elicited

## Decision-state model

- Proposition: release 6.0 contains a real regression, as the post-release review would confirm it
- Residual reading: not-H includes every explanation for the spike other than a confirmed real regression (noise, canary-environment artifacts, benign changes nobody named)
- Claim class: predictive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.035 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | first-hour canary error-rate spike | 3 | externally-sourced | spike_reference.csv, consortium census of comparable first-hour canaries; P(spike given real)=18000/20000=0.9, P(spike given not real)=6000/20000=0.3; quota-drawn 20000/20000 so only the ratio is used, never its split as a base rate |

- Independence: single item
- Posterior odds: 0.105

## Robustness

- Prior class swept: 0.035 — provenance: estimated-from-data-in-hand
- Loss range swept: 9 — provenance: user-elicited
- Crossover: none within swept class

## Verdict

- Verdict: robust
- Recommended action: ship now
- Conditions: Prior odds 7/200 = 0.035 from the complete release census (3.0 to 5.6, 207 releases, 7 confirmed regressions), held fixed by the user as the settled base rate, so no prior class is swept. Losses are the user's stated point values (10, 0, 1, 1), not ranges. The LR of 3 is a point from the consortium counts. Robust holds only at those points and the margin is thin: posterior odds 0.105 against threshold 0.111 (regression probability about 9.5%; expected loss ship 0.95 vs hold 1.00). Outside the swept points the action flips at prior odds 0.037 (vs 0.035 used), at likelihood ratio 3.175 (vs 3 used), or at loss ratio 9.52 (vs 9 used). Assumes releases 3.0 to 5.6 are comparable to 6.0 and that the reference-class spike definition matches this canary's spike. A verdict is a recommendation, not an authorization to ship.

## Handoff

- Open factual disputes: whether the 6.0 spike matches the reference class's spike definition and magnitude, and whether 6.0 is comparable to historical releases; either could move the LR or prior across the 3.175 and 0.037 crossovers
- Identification gaps: none
- VoI question: whether a short additional canary soak, or a larger-sample reading of the 6.0 spike, is worth its cost given a perfect-information bound of about 0.86 engineer-days at this prior
