# Decision Record: ship or hold the 2026-09-12 release carrying the pool change

## Decision frame

- Route: decide
- Actions: ship the 2026-09-12 release vs hold the release one week
- Decision owner: release owner (the user's team)
- Reversibility: hold costs one week of delay; ship with an undetected real regression costs about ten times that
- Deadline or forcing event: release freeze, Friday 2026-09-12
- Consequences:

  | | real served-latency regression true | real served-latency regression false |
  | --- | --- | --- |
  | ship the 2026-09-12 release | undetected regression reaches production (loss 10 units) | clean ship (loss 0) |
  | hold the release one week | regression caught (loss 0) | needless one-week hold (loss 1 unit) |

- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: canary hosts' served checkout p95 on 2026-09-09 is genuinely higher than control (H1 as stated)
- Residual reading: false includes H2 (exporter sampling artifact) and any unnamed explanation under which served latency is not higher
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED folds into true; H2 UNRESOLVED folds into false; the residual absorbs unnamed non-regression explanations; no LR derived from the UNRESOLVED tokens

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | 40 ms canary/control gap appears (T3 on S2) | 4.5 | estimated-from-data-in-hand | S2, 20 past canary rollouts: gap in 9/10 settled-real vs 2/10 settled-not-real = 0.9/0.2; within-stratum frequencies only, valid for LR, no base rate; n=10 per stratum |
  | T1 observed gap 57 ms, all canary hosts above all control | none supported | none supported | T1 is the observation that the T3 ratio conditions on; counted once through the T3 ratio, not multiplied again |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.01–1 — provenance: sensitivity-only
- Loss range swept: 10–10 — provenance: user-elicited
- Crossover: flips at prior odds 0.022

Arithmetic: posterior odds = prior odds x 4.5, so over the class 0.045–4.5 (conditional range). Hold wins when posterior odds > 0.1, i.e. prior odds > 0.1/4.5 = 0.0222 (prior probability about 2.2%). At prior odds 0.01 posterior is 0.045 < 0.1: ship. At 0.0222: tie (counts as flip). At 0.1 posterior 0.45: hold. At 1: 4.5: hold.
Informational only (not swept, analyst-chosen): if the LR were as low as 1.5, crossover prior odds = 0.067 (about 6%); if 4.5 holds, a team would need to put under ~2% on a real regression before shipping.

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: prior class is hypothetical (sensitivity-only, 1%-50%); loss ratio 10 is a rounded elicited value at nominal, no range endpoints supplied so loss is a single point; single LR 4.5 from small quota-drawn strata (n=10 each), carried as a point and not swept; S3 (raw logs) not acquired so the artifact hypothesis is untested; T1 evidence and H2 share the same pipeline.

## Handoff

- Open factual disputes: H1 vs H2 (served latency vs exporter artifact); T2 on raw access logs (S3, restore pending) would discriminate and could move the verdict
- Identification gaps: none
- VoI question: is the S3 restore plus T2 recompute achievable before Friday's freeze, and at what delay cost relative to the one-week hold?
