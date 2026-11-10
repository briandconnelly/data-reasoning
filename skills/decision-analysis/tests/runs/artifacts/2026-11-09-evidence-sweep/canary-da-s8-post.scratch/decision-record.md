# Decision Record: ship or hold the pool-change release at Friday's freeze

## Decision frame

- Route: decide
- Actions: ship the release vs hold the release one week
- Decision owner: release team (the team disagrees on the loss multiple)
- Reversibility: a hold costs one week and can be lifted; a shipped real regression costs the user-elicited multiple of that, and rollback cost is inside that multiple
- Deadline or forcing event: release freeze Friday
- Consequences:

  | | checkout p95 regression is real | checkout p95 regression is not real |
  | --- | --- | --- |
  | ship the release | missed real regression: 2–20 hold-costs | no loss: 0 |
  | hold the release one week | hold justified: 0 | needless one-week hold: 1 hold-cost |

- Favored if true: hold the release one week
- Loss ratio: 2–20 — provenance: user-elicited
- Decision threshold (posterior odds): 0.05–0.5 — provenance: user-elicited

## Decision-state model

- Proposition: the canary hosts' served checkout p95 on 2026-09-09 is genuinely higher than control (ledger H1, descriptive, as stated)
- Residual reading: not-H1 includes the exporter-sampling artifact (ledger H2) and any explanation nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 (UNRESOLVED) is the proposition true; H2 (UNRESOLVED) folds into false; the residual absorbs unnamed non-real explanations; UNRESOLVED status supplies no likelihood ratio

## Evidence and update

- Prior odds: 0.02–0.2 — provenance: user-elicited
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control p95 gap above 40 ms observed (57 ms, ledger T1; same observation as T3) | 4.5 | estimated-from-data-in-hand | S2, 20 past canary rollouts, P(gap given real) 9/10 over P(gap given not real) 2/10, within-stratum frequencies only (strata quota-drawn, so no base rate used); small sample, point estimate with no interval supplied |

- Independence: single item
- Posterior odds: 0.09–0.9

## Robustness

- Prior class swept: 0.02–0.2 — provenance: user-elicited
- Loss range swept: 2–20 — provenance: user-elicited
- Crossover: flips at prior odds 0.0111–0.111

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: Hold is preferred when prior odds x 4.5 x loss ratio exceeds 1, so the prior crossover is 1/(4.5 x r): 0.111 at r=2, 0.0444 at r=5, 0.0222 at r=10, 0.0111 at r=20 (below the swept class, so at r=20 hold wins across the whole class). Loss crossover at the prior ends: r=11.1 at prior 0.02; at prior 0.2 hold wins for every r in 2–20 (crossover 1.11). Corners: prior 0.02 with r=2 gives posterior 0.09 against threshold 0.5, ship; prior 0.2 with r=20 gives 0.9 against 0.05, hold. Assumes zero loss for ship-when-not-real and hold-when-real, with one hold-cost as the unit; the LR is a single point from 20 rollouts and its sampling error is not swept; the gap observation comes through the same pipeline H2 questions, and the 2/10 non-regression rate in S2 includes such artifacts only to the extent past rollouts had them; the posterior is conditional on the elicited prior range, not a held belief.

## Handoff

- Open factual disputes: H1 versus H2 is undecided because raw access logs (S3) were not acquired and their restore was pending; a raw-log p95 recompute on the canary hosts (ledger T2) would bear directly on the proposition and could move the posterior well outside the 4.5 reference-class ratio
- Identification gaps: none
- VoI question: whether waiting for the S3 restore and running T2 before Friday is worth it; the restore's cost and timing are unstated, so no pricing here
