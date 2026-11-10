# Decision Record: Restore db-07 from last night's backup now, or keep serving and investigate in the morning

## Decision frame

- Route: decide
- Actions: restore db-07 now vs keep db-07 serving
- Decision owner: the user's team (they act on the recommendation themselves)
- Reversibility: not stated; losses already fold in outage-equivalent hours
- Deadline or forcing event: checksum mismatch alert on db-07 at 02:14, persisted on re-read at 02:31; morning investigation is the alternative
- Consequences:

  | | corruption is real | corruption is not real |
  | --- | --- | --- |
  | restore db-07 now | 1 outage-equivalent hour | 1 outage-equivalent hour |
  | keep db-07 serving | 3 outage-equivalent hours | 0 outage-equivalent hours |

- Favored if true: restore db-07 now
- Loss ratio: 2 — provenance: user-elicited
- Decision threshold (posterior odds): 0.5 — provenance: user-elicited

## Decision-state model

- Proposition: the db-07 checksum mismatch reflects real on-disk corruption
- Residual reading: not-H includes transient faults (controller, bus, read path) and any other explanation nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.25 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | mismatch persisted on immediate re-read | 0.5–4 | externally-sourced | vendor note SV-2291 rev 3: P(persist given real)/P(persist given transient), this controller family, all shipped firmware revisions; db-07 firmware revision not exposed so no narrower figure |

- Independence: single item
- Posterior odds: 0.125–1

## Robustness

- Prior class swept: 0.25 — provenance: estimated-from-data-in-hand
- Loss range swept: 2 — provenance: user-elicited
- Crossover: flips at likelihood ratio 2

## Verdict

- Verdict: evidence-sensitive
- Recommended action: returned to owner
- Conditions: prior odds 0.25 = 40 confirmed of 200 alerts in the census (2024-01-01 onward, fleet-wide), held fixed by the owner; losses are the owner's stated point values (restore 1/1, keep 3/0), loss ratio 2, threshold 0.5; LR range 0.5–4 from the vendor bound; the history has no re-read data so it contributes no LR; assumes db-07's alert is exchangeable with the fleet's alerts.

## Handoff

- Open factual disputes: db-07's controller firmware revision, which sets where in 0.5–4 the persistence LR falls; the product of supported LRs must exceed 2 to favor restore, below 2 to favor keep serving
- Identification gaps: none
- VoI question: whether learning db-07's firmware revision, or the persistence rates for its revision, is worth pricing before the morning

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
