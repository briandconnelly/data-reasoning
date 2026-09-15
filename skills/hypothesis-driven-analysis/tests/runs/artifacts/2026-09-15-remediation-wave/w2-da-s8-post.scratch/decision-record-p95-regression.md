# Decision Record: ship or hold the 2026-09-12 release given the UNRESOLVED checkout p95 regression investigation

## Decision frame

- Route: decide
- Actions: Ship the 2026-09-12 release vs Hold the release past Friday's freeze
- Decision owner: release/investigation team
- Reversibility: shipping exposes users to any real regression before it can be rolled back, and served latency already experienced cannot be undone; holding is reversible at the fixed cost of a one-week delay
- Deadline or forcing event: Friday release freeze
- Consequences:

  | | real regression true | real regression false |
  | --- | --- | --- |
  | Ship | users are served degraded checkout latency — the missed-regression loss | ships correctly, no loss |
  | Hold | correctly avoids exposing users to the regression, at the cost of the week's delay | needless one-week hold — the hold loss |

- Loss ratio: 2–20 — provenance: user-elicited
- Decision threshold (posterior odds): 0.05–0.5 — provenance: user-elicited

## Decision-state model

- Proposition: H1 as stated — the canary hosts' served checkout latency is genuinely higher than control on 2026-09-09, a real regression in what users experience
- Residual reading: not-H1 — includes H2 (the canary exporter inflated measured p95 without a served-latency change) and any other explanation for the canary/control gap that the ledger does not name
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 (UNRESOLVED) folds into the proposition being true; H2 (UNRESOLVED) folds into the residual; the residual also absorbs any untested explanation the ledger does not name

## Evidence and update

- Prior odds: 0.02–0.2 — provenance: user-elicited
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | T1's observed canary/control gap (57 ms) crosses the 40 ms noise-band threshold; T3's reference class gives the crossing's reliability as a signal of real-vs-not status | 4.5 | estimated-from-data-in-hand | S2 `evidence/reference_class.csv`, 20 past canary rollouts (10 settled-real, 10 settled-not, quota-drawn strata); within-stratum frequencies P(gap>40ms\|real)=9/10, P(gap>40ms\|not real)=2/10 — the quota draw biases the file's base rate, not these within-stratum conditionals, so the ratio is usable as an LR; T1 (S1 `evidence/host_p95.csv`) supplies this case's gap (57 ms) crossing that same 40 ms line |
  | T2 — the raw-access-log recompute that would separate H1 from H2 directly | none supported | none supported | S3 not acquired before the release decision; 7-day raw access logs retained, restore request pending |

- Independence: single item
- Posterior odds: 0.09–0.9

## Robustness

- Prior class swept: 0.02–0.2 — provenance: user-elicited
- Loss range swept: 2–20 — provenance: user-elicited
- Crossover: Ship is preferred where prior_odds × 4.5 < 1/loss_ratio. At the low end of the swept prior (0.02), the flip is at loss ratio ≈11.1 — inside the swept loss range, so Ship is preferred below ≈11.1 and Hold above it. At the high end of the swept prior (0.2), the flip is at loss ratio ≈1.1 — below the swept loss floor of 2, so Hold is preferred across the entire swept loss range at that prior. Equivalently: at the low end of the swept loss range (2), the flip is at prior odds ≈0.111 — inside the swept prior class, so Ship is preferred below it and Hold above. At the high end of the swept loss range (20), the flip is at prior odds ≈0.011 — below the swept prior floor of 0.02, so Hold is preferred across the entire swept prior class at that loss.

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: holds over prior odds 0.02–0.2 (user-elicited, read as "1 in N" ≈ odds 1/N) and loss ratio 2–20 (user-elicited); the only supported likelihood ratio (4.5) is a reference-class proxy for "gap crosses 40 ms," not a direct test separating H1 from H2 — T2, the test that would do that, did not run. The crossover falls inside both the stated prior class and the stated loss range, so the flip point is where the owner's actual prior (within 1-in-50 to 1-in-5) and actual loss disagreement (within 2x to 20x) land relative to it, not something this record can resolve further from the evidence in hand.

## Handoff

- Open factual disputes: whether raw access logs (S3) would show the same p95 gap on the canary hosts — the one test (T2) that would discriminate a real served-latency regression (H1) from an exporter/measurement artifact (H2); restore is pending and did not complete before this decision
- Identification gaps: none
- VoI question: whether restoring S3 and running T2 before Friday's freeze is worth pricing, given it could collapse the H1/H2 ambiguity that the 4.5 LR only proxies; also worth pricing informally: whether the team's loss-ratio disagreement (2x vs 20x) can be narrowed before Friday, since the crossover is as sensitive to that disagreement as it is to the prior
