# Decision Record: ship or hold the 2026-09-12 release carrying the pool change, given two UNRESOLVED explanations for the checkout p95 rise

## Decision frame

- Route: decide
- Actions: ship the release vs hold the release one week
- Decision owner: the release owner for the Friday freeze (the user's team)
- Reversibility: a hold costs one week of delay and can be lifted next week; a shipped real regression costs about ten holds (user-stated) and needs a rollback or fix
- Deadline or forcing event: release freeze on Friday
- Consequences:

  | | real served-latency regression | no real regression (artifact or other) |
  | --- | --- | --- |
  | ship the release | loss 10 hold-equivalents | loss 0 |
  | hold the release one week | loss 0 | loss 1 hold-equivalent |

- Favored if true: hold the release one week
- Loss ratio: 10 — provenance: user-elicited
- Decision threshold (posterior odds): 0.1 — provenance: user-elicited

## Decision-state model

- Proposition: H1 as stated: canary checkout p95 on 2026-09-09 was genuinely higher than control in served latency (a real regression in what users experience)
- Residual reading: not-H1 includes H2 (exporter sampling artifact) and any explanation nobody named that leaves served latency unchanged
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: H1 UNRESOLVED maps to the proposition; H2 UNRESOLVED maps to not-H1 together with the residual; no likelihood information is taken from the UNRESOLVED status tokens

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | observed canary-minus-control gap above the 40 ms band (T1: 57 ms) scored against past rollouts (T3) | 4.5 | estimated-from-data-in-hand | S2, 20 past canary rollouts; P(gap given real regression) = 9/10, P(gap given no regression) = 2/10, so 0.9/0.2; the strata were quota-drawn so this ratio is valid but the file carries no base rate; n = 10 per stratum so the ratio is imprecise; assumes the current pipeline and gap definition match those of the past rollouts |
  | raw access-log p95 on canary hosts (T2) | none supported | none supported | S3 not acquired, T2 NOT_TESTED; an untested item carries no likelihood information |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.01–1 — provenance: sensitivity-only
- Loss range swept: 10–10 — provenance: user-elicited
- Crossover: flips at prior odds 0.0222

## Verdict

- Verdict: prior-sensitive
- Recommended action: returned to owner
- Conditions: no supported prior exists (S2 is quota-stratified and has no base rate), so prior odds 0.01–1 (probability about 1% to 50%) is a sensitivity-only class; the posterior odds under it are 0.045–4.5 using the supported LR of 4.5 (a point; its sampling imprecision is not swept); the threshold is 0.1 from the user's rounded "roughly ten" loss ratio recorded at its nominal value, with no range endpoints supplied so the loss range is a point that cannot flip the action on its own; hold is preferred when prior odds exceed 0.0222 (prior probability above about 2.2%), ship only below that; at the loss-ratio level, with prior odds 0.01 the loss ratio would need to exceed about 22 for hold to win, and with prior odds 1 hold wins for any loss ratio above about 0.22; the LR is from past rollouts and assumes the same pipeline behavior; H2 is untested, so the LR 4.5 does not separate a real regression from an exporter artifact beyond the base rate in S2's within-stratum frequencies

## Handoff

- Open factual disputes: whether the exporter sampling changed on the canary hosts and whether raw access-log p95 shows the same gap (T2 with S3, restore pending), which would discriminate H1 from H2 and move the posterior far past the threshold in either direction
- Identification gaps: none
- VoI question: whether restoring the raw access logs (S3) and running T2 before the freeze is worth its cost against a one-week hold; the ledger says logs are retained 7 days, so the restore may no longer be possible
