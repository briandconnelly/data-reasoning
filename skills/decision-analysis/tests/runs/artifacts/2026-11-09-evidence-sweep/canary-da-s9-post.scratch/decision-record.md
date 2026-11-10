# Decision Record: restore db-07 from last night's backup now vs keep serving until morning

## Decision frame

- Route: decide
- Actions: restore db-07 from last night's backup now vs keep db-07 serving and investigate in the morning
- Decision owner: db-07 operations team (acts on the recommendation themselves)
- Reversibility: restore costs 1 outage-equivalent hour either way; keep-serving can be switched to a restore in the morning but corruption in the interim is not undone
- Deadline or forcing event: checksum-mismatch alert 02:14, persisted on re-read 02:31
- Consequences:

  | | real corruption | not real corruption |
  | --- | --- | --- |
  | restore db-07 from last night's backup now | 1 hour | 1 hour |
  | keep db-07 serving and investigate in the morning | 3 hours | 0 hours |

- Favored if true: restore db-07 from last night's backup now
- Loss ratio: 2 — provenance: user-elicited
- Decision threshold (posterior odds): 0.5 — provenance: user-elicited

## Decision-state model

- Proposition: the db-07 checksum mismatch reflects real on-disk corruption
- Residual reading: not-H includes transient faults, controller or read-path glitches, and any explanation nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.25 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | mismatch persisted on immediate re-read | 0.5–4 | externally-sourced | vendor note SV-2291 rev 3: P(persist given real)/P(persist given transient), all firmware revisions of this controller family, no narrower figure; db-07 firmware revision not exposed |

- Independence: single item
- Posterior odds: 0.125–1

## Robustness

- Prior class swept: 0.25–0.25 — provenance: estimated-from-data-in-hand
- Loss range swept: 2–2 — provenance: user-elicited
- Crossover: flips at likelihood ratio 2

## Verdict

- Verdict: evidence-sensitive
- Recommended action: returned to owner
- Conditions: prior is the fleet census rate 40/200 = 0.2 (odds 0.25) held fixed per the owner; losses are the owner's point values; the persistence ratio is the vendor bound 0.5–4 and db-07's firmware is unknown; the census does not record persistence, so the prior is the rate among all alerts, not among persisting ones

## Handoff

- Open factual disputes: db-07's controller firmware revision, which fixes where in 0.5–4 the persistence ratio lies; restore is preferred at a ratio above 2 and keep-serving below 2
- Identification gaps: none
- VoI question: whether learning db-07's firmware revision (or an independent integrity check of the block) is worth its cost before the restore decision

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
