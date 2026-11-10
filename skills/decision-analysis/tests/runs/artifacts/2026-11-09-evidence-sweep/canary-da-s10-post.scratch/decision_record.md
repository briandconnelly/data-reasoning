# Decision Record: Ship release 6.0 now or hold one week after canary error-rate spike

## Decision frame

- Route: decide
- Actions: ship now vs hold one week
- Decision owner: the requesting release team
- Reversibility: shipping a real regression costs 10 engineer-days; holding costs 1 engineer-day either way
- Deadline or forcing event: release 6.0 canary spike; decision pending
- Consequences:

  | | real regression | not a real regression |
  | --- | --- | --- |
  | ship now | 10 engineer-days | 0 engineer-days |
  | hold one week | 1 engineer-day | 1 engineer-day |

- Favored if true: hold one week
- Loss ratio: 9 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1111 — provenance: user-elicited

## Decision-state model

- Proposition: release 6.0 is a real regression (as the post-release review would confirm)
- Residual reading: false includes a benign spike, noise, and explanations nobody named
- Claim class: predictive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.035 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | first-hour canary error-rate spike | 1.51–5.95 | estimated-from-data-in-hand | spike_reference.csv: P(spike given real)=18/20=0.9, P(spike given not real)=6/20=0.3, point LR 3; range is a 95% log-ratio interval (se 0.350) reflecting n=20 per arm; reference class is quota-sampled 20/20 releases, so only the conditional rates are used, never its split as a base rate |

- Independence: single item
- Posterior odds: 0.0529–0.208

## Robustness

- Prior class swept: 0.035 — provenance: estimated-from-data-in-hand
- Loss range swept: 9 — provenance: user-elicited
- Crossover: flips at likelihood ratio 3.175

## Verdict

- Verdict: evidence-sensitive
- Recommended action: returned to owner
- Conditions: prior is the census rate 7/207 (odds 7/200 = 0.035), held fixed as the user directs; losses are the stated point values (r = 9, threshold 1/9); at the point LR of 3 posterior odds are 0.105, just under the threshold 0.111, which favors ship now, but any LR above 3.175 favors hold and the reference-class interval spans it; assumes release 6.0 resembles the reference-class releases and that the reference class is representative given its analyst-set quotas

## Handoff

- Open factual disputes: none
- Identification gaps: none
- VoI question: whether a longer canary window or a larger spike reference class would narrow the LR interval enough to settle which side of 3.175 it falls on
