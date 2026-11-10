# Decision Record: Restore db-07 from last night's backup now, or keep serving until morning

## Decision frame

- Route: decide
- Actions: Restore db-07 from last night's backup now vs Keep db-07 serving and investigate in the morning
- Decision owner: db-07 operations team (acts on this recommendation themselves)
- Reversibility: Restore now cannot be undone once started; keep serving can be reversed by restoring later, at the cost of the added outage-equivalent hours if corruption is real
- Deadline or forcing event: Checksum mismatch alert 02:14, persisted on re-read at 02:31; decision needed tonight
- Consequences:

  | | Corruption is real | Corruption is not real |
  | --- | --- | --- |
  | Restore db-07 from last night's backup now | 1 hour outage-equivalent | 1 hour outage-equivalent |
  | Keep db-07 serving and investigate in the morning | 3 hours outage-equivalent | 0 hours outage-equivalent |

- Loss ratio: 3 — provenance: user-elicited
- Decision threshold (posterior odds): 0.5 — provenance: user-elicited

## Decision-state model

- Proposition: The checksum mismatch on db-07 reflects real on-disk corruption
- Residual reading: False includes a transient fault and any other non-corruption explanation nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: 0.25 — provenance: estimated-from-data-in-hand
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | Mismatch persisted across immediate re-read | 0.5–4 | externally-sourced | Vendor note SV-2291 rev 3: P(persists given real corruption) / P(persists given transient fault), bound across all firmware revisions of this controller family; db-07 revision not exposed by the management interface so no narrower figure applies |

- Independence: single item
- Posterior odds: 0.125–1.0

## Robustness

- Prior class swept: 0.25 — provenance: estimated-from-data-in-hand
- Loss range swept: 3 — provenance: user-elicited
- Crossover: flips at prior odds 0.5

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: Prior odds 0.25 = 40 confirmed of 200 alerts (0.2 rate) in the census alert_history.csv, treated by the owner as the settled base rate and not varied; the census predates re-read checks, so it holds no persistence data and the prior is not conditioned on persistence. Losses are the owner's stated figures, not varied. The open quantity is the vendor LR band 0.5–4, carried through the posterior (0.125–1.0) rather than swept on its own. The 0.5 in the Crossover slot is the posterior-odds threshold (restore when posterior odds exceed 1/loss-ratio-equivalent 0.5, i.e. p above 1/3); at prior 0.25 it is reached at LR 2. LR below 2 favors keep serving (expected loss 3p < 1), LR above 2 favors restore now (expected loss 1). The prior-sensitive label is used because the verdict set has no slot for an LR-driven flip; the sensitivity here is in the LR, not in a prior the owner left free. At LR 0.5 posterior p = 0.11 (keep expected loss 0.33); at LR 4 posterior p = 0.5 (keep expected loss 1.5). Nothing here authorizes executing either action.

## Handoff

- Open factual disputes: Which firmware revision db-07 runs, and so the vendor persistence ratio for it (whether above or below 2), would change the verdict
- Identification gaps: none
- VoI question: Is establishing db-07's firmware revision, or the persist-given-transient rate for it, worth its cost before acting
