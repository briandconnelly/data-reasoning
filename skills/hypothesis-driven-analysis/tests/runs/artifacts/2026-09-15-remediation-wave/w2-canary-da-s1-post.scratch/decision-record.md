# Decision Record: ship the 2026-09-12 release (connection-pool change) or hold for the p95 regression investigation

## Decision frame

- Route: decide
- Actions: Ship vs Hold
- Decision owner: release owner (user)
- Reversibility: Ship is not cheaply undone — once live, backing out needs a fresh rollback decision under production exposure; Hold is cheaply reversible — the release ships later once the block is lifted, at the cost of the delay itself
- Deadline or forcing event: 2026-09-19 (Friday) — release freeze
- Consequences:

  | | H true (real regression) | H false (artifact / residual) |
  | --- | --- | --- |
  | Ship | ships a live, unaddressed checkout-latency regression — the named "missing a real regression" cost | ships cleanly — no cost |
  | Hold | correctly caught, held for a real problem — no incremental cost beyond the hold itself | needless one-week hold — the named baseline cost |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: the canary/control checkout p95 gap observed on 2026-09-09 is a real regression in served latency (H1 as stated)
- Residual reading: not-H1 — the gap is not a real change in served latency; includes H2 (exporter/measurement artifact) and any other explanation nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the true state; H2 UNRESOLVED folds into the false/residual state; the residual also absorbs any explanation the ledger did not name

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | T1 — per-host metrics p95 gap >40 ms, CONSISTENT | none supported | none supported | same metrics pipeline that H2 questions; both H1 and H2 predict this pipeline-level gap, so the result does not discriminate between them — the qualifying-gap fact it establishes is the conditioning event T3 uses below, so it is not counted a second time |
  | T2 — raw access-log p95, NOT\_TESTED | none supported | none supported | S3 (raw access logs) not acquired before the release decision — restore pending; this is the one test that would separate H1 from H2 |
  | T3 — reference-class gap frequency by post-mortem status, CONSISTENT | 4.5 | estimated-from-data-in-hand | S2 `evidence/reference_class.csv`; 20 past canary rollouts, quota-sampled 10 settled-real / 10 settled-not-real; within-stratum frequency of the qualifying >40 ms gap is 9/10 given real, 2/10 given not-real; conditioning: same 40 ms threshold, same canary/control host-level p95 comparison, assumes this rollout is exchangeable with the reference class; the fixed quota removes any base-rate information from the 10/10 split, but outcome-based sampling like this preserves the within-stratum conditional frequencies, which is what the LR uses |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.25–4 — provenance: sensitivity-only
- Loss range swept: 8–12 — provenance: user-elicited
- Crossover: preferred action flips to Ship only below prior odds ≈0.0185–0.0278 (~1:54 to ~1:36, depending on where the loss ratio sits in 8–12) — below the entire swept prior class of 0.25–4; within the swept prior class and loss range, Hold is preferred at every point (posterior odds range 1.125–18 against thresholds 0.083–0.125)

## Verdict

- Verdict: robust
- Recommended action: Hold
- Conditions: robust across prior odds 0.25–4 (sensitivity-only — the ledger's reference class cannot supply a base rate, so no belief-grade prior is supported) and loss ratio 8–12 (user-elicited reading of "roughly ten times"); flipping to Ship would require a starting belief below roughly 1:40 that the gap is real, which the swept class does not reach and which the evidence in hand (a uniform 57 ms gap on every canary host, and T3's 4.5x likelihood ratio toward "real") does not support as a defensible starting point

## Handoff

- Open factual disputes: whether the canary/control gap is real served-latency change (H1) or an exporter/measurement artifact (H2) — unresolved because T2 could not run; for `hypothesis-driven-analysis` once S3 (raw access logs, restore pending) is available
- Identification gaps: none
- VoI question: whether expediting the S3 restore before the Friday freeze is worth the delay, given T2 is the one test that would discriminate H1 from H2 directly
