# Decision Record: Restore db-07 from last night's backup now vs keep serving after a persistent checksum mismatch

## Decision frame

- Route: decide
- Actions: restore db-07 from last night's backup now vs keep db-07 serving and investigate in the morning
- Decision owner: db-07 operations team (user and on-call)
- Reversibility: a restore is a one-way outage cost already counted in the loss; keeping serving can be switched to a restore in the morning at the stated losses
- Deadline or forcing event: tonight's 02:14 alert; choice needed now
- Consequences:

  | | real corruption | not real corruption |
  | --- | --- | --- |
  | restore db-07 from last night's backup now | 1 outage-hour | 1 outage-hour |
  | keep db-07 serving and investigate in the morning | 3 outage-hours | 0 outage-hours |

- Favored if true: restore db-07 from last night's backup now
- Loss ratio: 2 — provenance: user-elicited
- Decision threshold (posterior odds): 0.5 — provenance: user-elicited

## Decision-state model

- Proposition: the db-07 checksum mismatch reflects real on-disk corruption
- Residual reading: false includes transient faults and any other explanation nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.25 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | mismatch persisted across immediate re-read | 0.5–4 | externally-sourced | vendor note SV-2291 rev 3; this controller family; ratio P(persist given real corruption) over P(persist given transient fault), bound covers all firmware revisions, revision of db-07 not exposed |

- Independence: single item
- Posterior odds: 0.125–1

## Robustness

- Prior class swept: 0.25 — provenance: estimated-from-data-in-hand
- Loss range swept: 2 — provenance: user-elicited
- Crossover: flips at likelihood ratio 2

## Verdict

- Verdict: evidence-sensitive
- Recommended action: returned to owner
- Conditions: prior is the census base rate 40/200 = 0.2 (odds 0.25), held fixed as the user directed; losses are the user's stated point values; the re-read likelihood ratio is only bounded 0.5–4 by the vendor and the firmware revision is unknown; restore is preferred when the ratio exceeds 2, keep serving when below 2, and at exactly 2 neither is preferred

## Handoff

- Open factual disputes: which firmware revision db-07 runs, and so where in 0.5–4 the persistence ratio falls relative to 2
- Identification gaps: none
- VoI question: whether learning db-07's firmware revision or the controller's persistence behavior is worth pricing against the cost of a restore tonight
