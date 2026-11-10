# Decision Record: Restore db-07 from last night's backup now vs keep serving after a persistent checksum mismatch

## Decision frame

- Route: decide
- Actions: restore db-07 from last night's backup now vs keep db-07 serving and investigate in the morning
- Decision owner: the db-07 operations team (they act on the recommendation themselves)
- Reversibility: not stated; losses are given as total outage-equivalent hours per cell
- Deadline or forcing event: mismatch alert at 02:14, persisted on re-read at 02:31; decision tonight
- Consequences:

  | | real corruption | not real corruption |
  | --- | --- | --- |
  | restore now | 1 hour | 1 hour |
  | keep serving | 3 hours | 0 hours |

- Loss ratio: 2 — provenance: user-elicited
- Decision threshold (posterior odds): 0.5 — provenance: user-elicited

## Decision-state model

- Proposition: the db-07 checksum mismatch reflects real on-disk corruption
- Residual reading: false includes transient faults and any other non-corruption explanation nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.25 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | mismatch persisted on immediate re-read | 0.5–4 | externally-sourced | vendor note SV-2291 rev 3: P(persist given real)/P(persist given transient), this controller family, all shipped firmware revisions, no narrower figure; db-07 revision not exposed |

- Independence: single item
- Posterior odds: 0.125–1.0

## Robustness

- Prior class swept: 0.25–0.25 — provenance: estimated-from-data-in-hand
- Loss range swept: 2–2 — provenance: user-elicited
- Crossover: flips at prior odds 0.125–1.0

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: Prior odds 0.25 = 40 confirmed of 200 alerts, a complete census treated by the owner as settled and not varied. The flip comes from the vendor LR range 0.5–4, carried through the posterior and not swept alone. Restore wins when posterior odds exceed 0.5, which needs LR above 2 (equivalently, prior odds above 0.5 divided by LR). LR 2 sits inside 0.5–4. At LR 0.5 keep serving has expected loss 0.75 against 1 for restore. At LR 4 posterior odds are 1.0 (p=0.5), keep serving has expected loss 1.5 against 1 for restore. The history did not record re-read persistence, so no narrower LR is available from data in hand. Firmware revision is not exposed.

## Handoff

- Open factual disputes: which firmware revision db-07 runs, or the persistence rates for real versus transient faults on it; either would place the LR relative to 2
- Identification gaps: none
- VoI question: whether a cheap discriminating check tonight (such as another read path or a scrub of the block) is worth its cost against the stakes

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
