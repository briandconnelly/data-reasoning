# Decision Record: ship or hold the 2026-09-12 release carrying the connection-pool change

## Decision frame

- Route: decide
- Actions: ship the release vs hold the release
- Decision owner: release owner (not named in the ledger)
- Reversibility: not stated in the ledger; rollback cost for ship and cost of a delay for hold are both unknown
- Deadline or forcing event: 2026-09-12 release
- Consequences:

  | | served checkout latency is higher on canary (H1 as stated) true | H1 false (artifact or unnamed explanation) |
  | --- | --- | --- |
  | ship | regression reaches all users; loss L_s | no harm; loss 0 |
  | hold | regression withheld; loss taken as 0 (baseline) | unnecessary delay; loss L_h |

- Loss ratio: 0.1–10 — provenance: sensitivity-only
- Decision threshold (posterior odds): 0.1–10 — provenance: sensitivity-only

## Decision-state model

- Proposition: canary-minus-control served checkout p95 on 2026-09-09 is genuinely higher (H1 as stated, a real change in what users experience)
- Residual reading: not-H1 includes H2 (exporter sampling artifact) and any explanation nobody named that leaves served latency unchanged
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the proposition; H2 UNRESOLVED folds into not-H1; the residual absorbs unnamed non-served-latency explanations; no likelihood ratio is taken from either status token

## Evidence and update

- Prior odds: 0.1–10 — provenance: sensitivity-only
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap exceeds 40 ms (T1 observation, 57 ms) | 4.5 | estimated-from-data-in-hand | S2: 20 past canary rollouts, quota-stratified 10 real / 10 not-real by post-mortem; P(gap\|real)=9/10, P(gap\|not real)=2/10; conditioned on a gap over 40 ms; strata quota-drawn so the ratio is a likelihood ratio only, not a base rate; 10 per stratum so imprecise |

- Independence: single item
- Posterior odds: 0.45–45

## Robustness

- Prior class swept: 0.1–10 — provenance: sensitivity-only
- Loss range swept: 0.1–10 — provenance: sensitivity-only
- Crossover: flips at prior odds 0.22

## Verdict

- Verdict: loss-sensitive
- Recommended action: returned to owner
- Conditions: losses are sensitivity-only, so the verdict is capped at loss-sensitive. Hold is preferred when posterior odds exceed 1/r, i.e. 4.5 x prior odds x r > 1. At loss ratio 1 the flip is at prior odds 0.22. At even prior odds (1) the flip is at loss ratio 0.22 (ship only if shipping a regression costs under about a quarter of an unnecessary hold). Across the swept corners the action flips (prior 0.1 with r 0.1 gives posterior odds 0.45 against threshold 10 so ship; prior 10 with r 10 gives 45 against 0.1 so hold). The LR of 4.5 comes from the T3 reference class only: T1's gap is the same observation, not a second item, and T1 comes from the pipeline H2 questions, so it does not separate H1 from H2 by itself. Hold taken as zero loss when H1 is true.

## Handoff

- Open factual disputes: H1 (real served-latency change) vs H2 (exporter artifact) is unadjudicated; T2 on raw access logs S3 could not run, and it is the discriminating test that would change the verdict
- Identification gaps: none
- VoI question: whether restoring S3 raw logs and running T2 is worth its cost and delay against the release deadline
