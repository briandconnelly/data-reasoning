# Decision Record: Restore db-07 from last night's backup now, or keep serving and investigate in the morning

## Decision frame

- Route: decide
- Actions: restore db-07 now vs keep db-07 serving
- Decision owner: the db-07 operations team (they act on the recommendation themselves)
- Reversibility: restore now costs 1 hour of outage-equivalent whichever state holds; keeping serving can be switched to a restore in the morning, but the 3-hour loss under real corruption is already incurred
- Deadline or forcing event: mismatch alert at 02:14, persisted on re-read at 02:31; morning investigation
- Consequences:

  | | the mismatch reflects real on-disk corruption | the mismatch does not reflect real on-disk corruption |
  | --- | --- | --- |
  | restore db-07 now | 1 hour outage-equivalent | 1 hour outage-equivalent |
  | keep db-07 serving | 3 hours outage-equivalent | 0 hours outage-equivalent |

- Favored if true: restore db-07 now
- Loss ratio: 2 — provenance: user-elicited
- Decision threshold (posterior odds): 0.5 — provenance: user-elicited

## Decision-state model

- Proposition: the persistent checksum mismatch on db-07 reflects real on-disk corruption
- Residual reading: false includes a transient fault, controller or firmware artifacts, and explanations nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.25 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | mismatch persisted across an immediate re-read | 0.5–4 | externally-sourced | vendor note SV-2291 rev 3, this controller family, all shipped firmware revisions, ratio of P(persists given real corruption) to P(persists given transient fault); firmware revision of db-07 not exposed so no narrower range |

- Independence: single item
- Posterior odds: 0.125–1

## Robustness

- Prior class swept: 0.25 — provenance: estimated-from-data-in-hand
- Loss range swept: 2 — provenance: user-elicited
- Crossover: flips at likelihood ratio 2

## Verdict

- Verdict: evidence-sensitive
- Recommended action: returned to owner
- Conditions: prior odds fixed at 0.25 (40 confirmed of 200 alerts, census 2024-Q1 to 2025-Q4, held as the settled base rate by the owner); losses as stated by the owner; the vendor ratio is the only evidence and spans 0.5–4; restore is preferred when the ratio is above 2 and keep serving when below 2, with a tie at exactly 2

## Handoff

- Open factual disputes: which firmware revision db-07 runs, and so where in 0.5–4 its persistence ratio lies; the vendor says the revision is not exposed by the management interface
- Identification gaps: none
- VoI question: whether determining db-07's firmware revision or its actual persistence ratio is worth its cost before the morning

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
