# Decision Record: restore db-07 from last night's backup now, or keep serving and investigate in the morning

## Decision frame

- Route: decide
- Actions: restore db-07 from last night's backup now vs keep db-07 serving and investigate in the morning
- Decision owner: the user's team (they act on the recommendation themselves)
- Reversibility: not stated; losses are given as outage-equivalent hours
- Deadline or forcing event: persistent checksum mismatch on db-07 flagged 02:14, persisted on re-read at 02:31
- Consequences:

  | | real corruption | not real corruption |
  | --- | --- | --- |
  | restore db-07 from last night's backup now | 1 hour outage-equivalent | 1 hour outage-equivalent |
  | keep db-07 serving and investigate in the morning | 3 hours outage-equivalent | 0 hours |

- Loss ratio: 3 — provenance: user-elicited
- Decision threshold (posterior odds): 0.5 — provenance: user-elicited

## Decision-state model

- Proposition: the db-07 mismatch reflects real on-disk corruption
- Residual reading: false includes transient faults and any explanation nobody named (controller, bus, memory, job artifacts)
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.25 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | mismatch persisted across an immediate re-read | 0.5–4 | externally-sourced | vendor note SV-2291 rev 3: persistence rate given real corruption over persistence rate given transient fault, this controller family, all shipped firmware revisions; fleet firmware not exposed so no narrower figure |

- Independence: single item
- Posterior odds: 0.125–1

Prior arithmetic: census of 200 alerts since 2024-01-01 (complete, unsampled), 40 confirmed corruption, so p = 0.2, odds 40/160 = 0.25. Treated as settled by the user, not varied. Caveat: the census does not condition on a persisting re-read, and the LR carries that. Posterior = 0.25 x 0.5 = 0.125 to 0.25 x 4 = 1.0 (probability 0.11 to 0.5).

## Robustness

- Prior class swept: 0.25 — provenance: estimated-from-data-in-hand
- Loss range swept: 3 — provenance: user-elicited
- Crossover: flips at prior odds 0.125–1

Restore costs 1 in both states. Keep costs 3 x P(real). Keep is preferred when posterior odds < 0.5 and restore when above (tie at 0.5). With prior odds fixed at 0.25, the flip occurs at LR = 2: LR below 2 favors keep serving, LR above 2 favors restore. The prior-odds crossover is 0.5/LR: 1 at LR 0.5, 0.125 at LR 4. The vendor range 0.5–4 straddles LR = 2, and the vendor gives no narrower figure per revision. The loss ratio is a single point; losses are not swept.

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: prior fixed at the census rate 0.2 (odds 0.25), settled by the user; losses 1/1/3/0 as stated, user-elicited, single point; likelihood ratio carried as the vendor range 0.5–4 and not swept on its own, so the action flips at LR = 2 inside that range; this verdict label is used because the closed set has no value for a flip driven by an unswept likelihood ratio, and the posterior range straddling the threshold is the finding; the vendor bound covers all firmware revisions and the db-07 revision is unknown

## Handoff

- Open factual disputes: which firmware revision db-07's controller runs, since it fixes the persistence ratio and so whether the LR is above or below 2
- Identification gaps: none
- VoI question: whether determining db-07's firmware revision or running a direct block verification (for example a read from a replica or a scrub) before the morning is worth its outage cost, given an expected value of perfect information of 0.4 outage-hours at probability 0.2 on these losses, before the re-read update
