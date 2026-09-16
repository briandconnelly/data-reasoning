# Decision Record: ship the release carrying the connection-pool change, or hold for one week, given the UNRESOLVED p95-regression ledger

## Decision frame

- Route: decide
- Actions: ship vs hold
- Decision owner: release owner (user)
- Reversibility: shipping a real regression reaches all users before it can be rolled back and forces a reactive hotfix under incident conditions; holding one week is fully reversible — the same release ships next window once resolved
- Deadline or forcing event: 2026-09-19 (Friday release freeze, user-stated)
- Consequences:

  | | H true | H false |
  | --- | --- | --- |
  | ship | real regression reaches all users (missed regression) | no regression; ship was correct, no cost |
  | hold | regression correctly kept out; hold was correct, no cost | needless one-week hold |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: the 2026-09-09 checkout p95 rise on canary hosts is a real increase in served latency (ledger H1, descriptive: canary minus control served checkout p95, ms)
- Residual reading: not-H includes H2 as stated (exporter sampling change inflating measured p95 with no served-latency change) and any other unnamed measurement artifact
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into H-true; H2 UNRESOLVED folds into the H-false residual; the residual also absorbs any artifact explanation the ledger never named

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | T1: canary/control p95 gap of 57 ms, exceeding the 40 ms noise band | none supported | none supported | both H1 and H2 predict this same pipeline-measured gap; T1 rules out pure noise (gap exceeds the 5-quiet-day band) but does not discriminate a real latency change from an exporter artifact — the ledger's own conclusion and limitations state no test separates H1 from H2 until S3 is restored |
  | T2: raw access-log p95 on canary hosts | none supported | none supported | NOT_TESTED — S3 not acquired before the decision; would have been the discriminating test |
  | T3: reference-class gap frequency, real vs non-regression rollouts | 4.5 | estimated-from-data-in-hand | S2 `evidence/reference_class.csv`, 20 past canary rollouts; conditioning event is "canary/control gap > 40 ms"; within-stratum frequencies 9/10 (real regressions) vs 2/10 (non-regressions) are usable as a likelihood ratio despite the quota-fixed strata carrying no base rate, per the ledger's own validity note that the split "supports the gap's frequency within each stratum only" |

- Independence: single item (T3 is the only item carrying a supported ratio; T1 and T2 contribute none)
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.25–4 — provenance: sensitivity-only
- Loss range swept: 5–15 — provenance: sensitivity-only
- Crossover: none within swept class

  Worked arithmetic (sensitivity-only prior × supported LR = posterior; hold preferred when posterior odds > 1/loss ratio):

  | prior odds | posterior odds (× LR 4.5) | threshold at loss 5 (0.2) | threshold at loss 10 (0.1) | threshold at loss 15 (0.0667) | preferred |
  | --- | --- | --- | --- | --- | --- |
  | 0.25 (1:4, skeptical) | 1.125 | exceeds | exceeds | exceeds | hold |
  | 1 (1:1, reference) | 4.5 | exceeds | exceeds | exceeds | hold |
  | 4 (4:1, favorable) | 18 | exceeds | exceeds | exceeds | hold |

  General crossover (outside the swept class): prior odds = 1/(4.5 × loss ratio) — 0.0444 at loss 5, 0.0222 at loss 10, 0.0148 at loss 15 (prior probability roughly 1.5%–4.3%). All three fall below the swept floor of 0.25; the swept class does not approach the flip.

## Verdict

- Verdict: robust
- Recommended action: hold
- Conditions: holds for prior odds of H1 (real regression) in 0.25–4 (sensitivity-only, unsupported by the ledger itself — no base rate is available) and loss ratio in 5–15 (sensitivity-only sweep around the user-elicited central value of 10); the only supported update is T3's likelihood ratio of 4.5, which by itself is enough to push hold's expected loss below ship's across this entire prior and loss range; the actual crossover (prior probability ~1.5%–4.3%) sits well outside the swept class, so only a considerably more skeptical prior than the swept floor — disbelieving the already-observed above-noise gap almost entirely before any reference-class evidence — would flip the recommendation

## Handoff

- Open factual disputes: whether the p95 rise is served-latency (H1) or exporter artifact (H2) — T2 against the restored raw access logs (S3) would settle this and is the fact that would most directly confirm or overturn today's recommendation; route to hypothesis-driven-analysis once S3 is available
- Identification gaps: none
- VoI question: whether expediting the pending S3 restore (raw access logs, currently retained 7 days with a restore request pending) before Friday's freeze is worth its delay/effort cost, given it is the one pull that could resolve H1 vs H2 directly
