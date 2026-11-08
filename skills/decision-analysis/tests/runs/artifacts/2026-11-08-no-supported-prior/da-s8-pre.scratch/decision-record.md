# Decision Record: ship or hold the 2026-09-12 release given an unresolved checkout p95 regression

## Decision frame

- Route: decide
- Actions: ship vs hold
- Decision owner: the release owner (not named in the request or ledger)
- Reversibility: hold costs one week of delay; the cost of undoing a shipped real regression is not stated in the ledger or request
- Deadline or forcing event: release freeze Friday
- Consequences:

  | | real regression true | real regression false |
  | --- | --- | --- |
  | ship | loss L one-week-hold units, L between 2 and 20 | no loss |
  | hold | no loss | loss 1 one-week-hold unit |

- Loss ratio: 2–20 — provenance: user-elicited
- Decision threshold (posterior odds): 0.05–0.5 — provenance: user-elicited

## Decision-state model

- Proposition: H1 as stated — the canary hosts' served checkout p95 is genuinely higher than control on 2026-09-09
- Residual reading: not-H1 includes H2 (exporter sampling artifact) and any explanation nobody named that leaves served latency unchanged
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into true; H2 UNRESOLVED folds into false, and the residual absorbs unnamed non-real explanations; no status token supplies a likelihood ratio

## Evidence and update

- Prior odds: 0.02–0.2 — provenance: user-elicited
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap above 40 ms observed (T1 57 ms) | 4.5 | estimated-from-data-in-hand | S2 within-stratum rates, 20 past canary rollouts: P(gap given real) = 9/10 = 0.9, P(gap given not real) = 2/10 = 0.2; conditioning on gap above 40 ms; strata quota-drawn so rates are valid, base rate is not used; n = 10 per stratum |

- Independence: single item
- Posterior odds: 0.09–0.9

## Robustness

- Prior class swept: 0.02–0.2 — provenance: user-elicited
- Loss range swept: 2–20 — provenance: user-elicited
- Crossover: flips at prior odds 0.0111–0.111

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: Arithmetic: posterior odds = prior odds x 4.5; hold iff posterior odds x L exceeds 1, so hold iff prior odds x L exceeds 0.222. Flip points by loss ratio: L=2 flips at prior odds 0.111 (1:9); L=5 at 0.044; L=10 at 0.022; at L=11.1 or more every prior in the class gives hold; at L=20 flips at 0.0111, below the class. By prior: prior 0.02 (1:50) flips at L=11.1; prior 0.1 flips at L=2.22; prior 0.2 (1:5) gives hold at every L in 2–20. The loss range also flips the action, so the record is loss-sensitive as well; one verdict value is recorded and both crossovers are stated. Ship wins only in the low-prior, low-loss corner (about 28 percent of the log-scaled grid, a sweep geometry and not a belief); hold wins elsewhere. Sample-size sensitivity: Wilson 95 percent intervals on 9/10 and 2/10 give a conservative LR range of about 1.2–17 (estimated-from-data-in-hand); at LR 1.2 the posterior is 0.024–0.24 and ship wins over more of the grid, at LR 17 hold wins nearly everywhere. The LR assumes this rollout is exchangeable with the S2 reference class and that S1 and S2 gaps come from the same pipeline H2 questions. Ledger state as of 2026-09-10; S3 not acquired.

## Handoff

- Open factual disputes: H1 versus H2 — whether the raw access-log p95 on the canary hosts shows the same gap (T2 NOT_TESTED, S3 restore pending); a clean T2 result would move the verdict far beyond any value swept here
- Identification gaps: none
- VoI question: whether restoring S3 and running T2 before the freeze is worth its delay and cost, given a hold costs one unit and the discriminating test could remove most of the prior-sensitivity

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
