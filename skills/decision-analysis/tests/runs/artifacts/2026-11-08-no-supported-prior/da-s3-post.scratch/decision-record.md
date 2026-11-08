# Decision Record: ship or hold the 2026-09-12 release carrying the connection-pool change

## Decision frame

- Route: decide
- Actions: ship the 2026-09-12 release vs hold the 2026-09-12 release
- Decision owner: not stated in the ledger (the release owner)
- Reversibility: not stated in the ledger; rollback cost of a shipped regression and delay cost of a hold are both unknown
- Deadline or forcing event: 2026-09-12 release
- Consequences:

  | | checkout served-latency regression is real | checkout served-latency regression is not real |
  | --- | --- | --- |
  | ship the 2026-09-12 release | users get ~57 ms slower checkout p95 until fixed or rolled back (loss Ls) | no loss |
  | hold the 2026-09-12 release | no loss | release delayed for nothing (loss Lh) |

- Loss ratio: 1 — provenance: sensitivity-only
- Decision threshold (posterior odds): none stated

## Decision-state model

- Proposition: the canary hosts' served checkout p95 on 2026-09-09 was genuinely higher than control's (H1 as stated)
- Residual reading: not-H1 includes the exporter-sampling artifact (H2) and any other measurement or non-served-latency explanation nobody named
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into the true state; H2 UNRESOLVED folds into the false state; the residual absorbs unnamed artifacts. No likelihood ratio is taken from the UNRESOLVED tokens.

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | canary/control gap over 40 ms observed (T1 observation, valued through T3) | 4.5 | estimated-from-data-in-hand | S2: 20 past canary rollouts, quota-drawn strata of 10 real and 10 not-real regressions; P(gap given real) = 9/10, P(gap given not real) = 2/10, ratio 4.5; conditioned on the post-mortem state; small n, so the ratio is a point from 10 per stratum |
  | raw access-log p95 on canary hosts (T2) | none supported | none supported | S3 not acquired; no result exists, and NOT_TESTED carries no likelihood information |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.1–1 — provenance: sensitivity-only
- Loss range swept: 0.1–10 — provenance: sensitivity-only
- Crossover: flips at loss ratio 0.22

Working. Loss ratio R = Ls/Lh. Hold when posterior odds exceed 1/R. Posterior odds = prior odds × 4.5, conditional on the single supported LR.
Prior odds 0.1 gives posterior 0.45, and 1 gives 4.5. Loss-ratio crossover R* = 1/posterior: 2.22 at prior 0.1, 0.22 at prior 1. The slot value 0.22 is computed at prior odds 1.
Prior crossover at fixed R: R=1 gives prior 0.22 (1/4.5); R=10 gives prior 0.022; R=0.5 gives prior 0.44. At R=1 the preferred action flips inside the swept prior class (hold above prior odds 0.22, ship below).
T1 and T3 are not multiplied: T3 only values the T1 observation.

## Verdict

- Verdict: loss-sensitive
- Recommended action: returned to owner
- Conditions: the loss ratio and its sweep are analyst-chosen and sensitivity-only, so the verdict is capped at loss-sensitive; no supported prior exists (S2's 10/10 split is quota-drawn and carries no base rate); the only supported LR is 4.5 from S2 and rests on the gap being measured by the same pipeline H2 questions; the loss crossover 0.22 is at prior odds 1; the prior crossover is 0.22 at loss ratio 1, 0.022 at loss ratio 10, and 0.44 at loss ratio 0.5. Direction: unless a wrong ship costs under about 0.22 of a wrong hold (at an even prior), the evidence leans hold; if the owner rates a wrong hold as cheap, the lean strengthens.

## Handoff

- Open factual disputes: whether the 57 ms canary/control gap is served latency or an exporter artifact (H1 vs H2); T2 on raw access logs (S3) would separate them, but S3 was retained 7 days with a restore pending, so its availability is itself unknown
- Identification gaps: none
- VoI question: whether restoring the S3 raw access logs and running T2 before the release is worth its cost against Ls and Lh
