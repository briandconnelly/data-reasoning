# Decision Record: ship or hold the 2026-09-12 release given the UNRESOLVED p95-regression investigation

## Decision frame

- Route: decide
- Actions: Ship (release 2026-09-12 with the connection-pool change) vs Hold (delay past the Friday freeze)
- Decision owner: the release owner for the 2026-09-12 release
- Reversibility: Ship is not reversible for the exposure window — any real regression is served to users before a rollback lands; Hold is reversible at the cost of a one-week delay
- Deadline or forcing event: Friday release freeze (2026-09-18)
- Consequences:

  | | H1 true (real regression) | H1 false (artifact/other, not-H1) |
  | --- | --- | --- |
  | Ship | real regression reaches users — cost = "missing a real regression" | no real regression — no cost |
  | Hold | regression avoided — no needless-hold cost charged | needless one-week hold — cost = "needless hold" |

- Loss ratio: 2–20 — provenance: user-elicited
- Decision threshold (posterior odds): 0.05–0.5 — provenance: user-elicited

## Decision-state model

- Proposition: H1 — the checkout p95 rise on the canary hosts on 2026-09-09 reflects a real regression in served latency (descriptive: canary minus control served checkout p95, ms)
- Residual reading: not-H1 covers H2 (exporter/measurement artifact) and any other unnamed explanation for the canary/control gap that isn't a real change in served latency
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: ledger H1 (UNRESOLVED) folds into "H1 true"; ledger H2 (UNRESOLVED, data-artifact) folds into "not-H1"; the residual also absorbs any other artifact or confound the ledger did not name

## Evidence and update

- Prior odds: 0.0204–0.25 — provenance: user-elicited
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap (57 ms) falls in the >40 ms band, calibrated against 20 past rollouts' post-mortem outcomes | 4.5 | estimated-from-data-in-hand | `evidence/reference_class.csv` (S2), 20 past canary rollouts stratified 10 real-regression / 10 not by post-mortem status, gap>40ms rate 9/10 vs 2/10 within each stratum, conditioned on the same 40 ms band T1 used |

- Independence: single item — T1's result (gap exceeds the 40 ms band) is the observation that S2's stratified rate is conditioned on, not a second independent test; multiplying T1 and T3 as separate factors would double-count the same 40 ms-band observation
- Posterior odds: 0.092–1.125

## Robustness

- Prior class swept: 0.0204–0.25 — provenance: user-elicited
- Loss range swept: 2–20 — provenance: user-elicited
- Crossover: two crossovers, since the preferred action flips on both axes —
  - holding loss ratio at 2 (threshold 0.5): flips at prior odds ≈0.111 (p≈0.10); below that, Ship, above it, Hold
  - holding prior odds at 0.0204 (p=0.02, low end): flips at loss ratio ≈10.9; below that, Ship, above it, Hold
  - the joint indifference curve is prior_odds × loss_ratio ≈ 0.222; inside the swept box, Ship survives only in the corner where prior_odds < ~0.111 AND loss_ratio < ~10.9 simultaneously (roughly the low-prior, low-loss-ratio quarter of the box); every other combination in the stated ranges prefers Hold, including both single-axis extremes (prior odds 0.25 at any swept loss ratio, and loss ratio 20 at any swept prior)

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: the flip depends on where the true prior and loss ratio sit inside the stated ranges (p(H1) 0.02–0.2, loss ratio 2–20); Hold is preferred across most of that joint range — Ship is preferred only if both the prior is near the low end (p(H1) ≲0.10, i.e., closer to 1-in-50–1-in-10 than 1-in-5) and the loss ratio is near the low end (≲11, i.e., closer to 2–10x than 10–20x) at the same time. The LR of 4.5 itself is a point estimate from a 10-per-stratum reference class (S2) and carries real sampling uncertainty that this record does not further quantify.

## Handoff

- Open factual disputes: whether the gap is a real served-latency regression (H1) or an exporter/measurement artifact (H2) is still unadjudicated — T2, the one test that could discriminate them, is NOT_TESTED because S3 (raw access logs) was not acquired before this decision; this is `hypothesis-driven-analysis` work if S3 becomes available
- Identification gaps: none — H1 is descriptive, no causal proposition is being scored here
- VoI question: whether restoring S3 (raw access logs, 7-day retention, restore request pending) before Friday is worth pursuing, given it is the only evidence that could move this out of prior-sensitive territory before the freeze

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
