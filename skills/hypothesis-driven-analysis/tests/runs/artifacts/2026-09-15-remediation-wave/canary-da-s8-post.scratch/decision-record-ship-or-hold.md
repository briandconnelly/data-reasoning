# Decision Record: ship the 2026-09-12 release (pool change) or hold it past Friday's freeze

## Decision frame

- Route: decide — per SKILL.md § Routing ("the investigation came back UNRESOLVED — act or wait" trigger)
- Actions: Ship (release the connection-pool change on schedule) vs Hold (delay past Friday's freeze)
- Decision owner: release owner / team making the ship-or-hold call
- Reversibility: Ship is the harder-to-undo action if wrong — a real regression reaches users and must be caught and rolled back/hotfixed after the fact. Hold is cheaply reversible — the change ships next cycle at the cost of the week's delay.
- Deadline or forcing event: Friday release freeze (as stated by the user)
- Consequences:

  | | H1 true (real regression) | H1 false (artifact or other unnamed cause) |
  | --- | --- | --- |
  | Ship | Ships a real p95 regression to users — loss = L (loss-ratio units) | Ships correctly — no loss |
  | Hold | Holds correctly — no loss | Needlessly holds a fine release for one week — loss = 1 (baseline unit) |

- Loss ratio: cost of shipping a real regression, as a multiple of the cost of a needless one-week hold — 2–20 — provenance: user-elicited ("the team can't agree on the number," but agrees on this range)
- Decision threshold (posterior odds of H1 at which Ship and Hold are equally bad): 1/L → 0.05–0.5 (odds 1:20 to 1:2) — provenance: derived from the user-elicited loss ratio above

## Decision-state model

- Proposition (H1): the canary hosts' served checkout latency on 2026-09-09 is genuinely higher than control — a real regression in what users experience, whatever its cause (descriptive claim, per ledger)
- Residual reading (not-H1): the observed canary/control gap is not a real elevation in served latency — includes the ledger's H2 (exporter sampling change inflating measured p95 without a real latency change) and any other unnamed explanation for the metric-level gap (e.g., a different measurement or environmental artifact nobody in the ledger named). Residual does NOT include "no gap was observed" — a gap was observed (T1); the residual is about what the gap means.
- Claim class: descriptive (ledger's own classification for H1) — no causal wording is used or needed for this decision
- Identification basis: NONE — not applicable to a descriptive claim
- Identification conditions: none
- Ledger mapping: H1 (UNRESOLVED) folds into the "H1 true" state. H2 (UNRESOLVED) folds into "not-H1," alongside the residual's unnamed explanations. T2, the one test that could have separated H1 from H2, is NOT_TESTED — raw access logs were never restored before this decision. That gap is carried into this record's evidence as "none supported," not silently dropped.

## Evidence and update

- Prior odds: 1:49 – 1:4 (0.0204 – 0.25) — provenance: user-elicited ("odds that it's a real regression somewhere between 1 in 50 and 1 in 5," converted from probability to odds)
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | Observed canary/control p95 gap of 57 ms (T1), read against the reference class of past rollouts (T3/S2) | 4.5 | estimated-from-data-in-hand | S2: 20 past canary rollouts with settled post-mortems, quota-drawn 10 real-regression / 10 not-real. A >40 ms gap appeared in 9/10 real-regression rollouts and 2/10 not-real rollouts. LR = (9/10) / (2/10) = 4.5. T1 is the fact this LR is applied to (a >40 ms gap was in fact observed here); T3 supplies the ratio. They are combined into one item, not multiplied separately, because T3's frequencies are the interpretation of T1's observation, not an independent fact. |
  | Raw access-log check for exporter-artifact vs real latency (T2) | none supported | none | T2 was the ledger's designated discriminating test between H1 (real) and H2 (exporter artifact) and it is NOT_TESTED — raw logs were never acquired (S3 restore pending). No likelihood ratio can be read off a test that did not run. |

- Independence: the T1+T3 item is treated as a single combined item (see above, to avoid double-counting the same observed gap). The T2 row contributes no update.
- Posterior odds: 0.092 – 1.125 (≈1:10.9 to ≈1.13:1) — computed as prior odds × 4.5 across the stated prior range. In probability terms, this is roughly 8% to 53% — a wide spread driven by the width of the stated prior, not by new precision from the evidence.

## Robustness

- Prior class swept: 1:49 – 1:4 (0.0204 – 0.25 odds) — provenance: user-elicited, same as Evidence and update
- Loss range swept: 2 – 20 — provenance: user-elicited
- Crossover:
  - Holding the prior at its low end (1:49, p≈2%): the preferred action flips from Ship to Hold at loss ratio L ≈ 10.9. Ship is preferred for L < 10.9, Hold for L > 10.9 — this crossover falls **inside** the stated loss range [2, 20].
  - Holding the prior at its high end (1:4, p≈20%): the flip point is L ≈ 0.89, which is **below** the stated loss floor of 2 — so Hold is preferred across the *entire* stated loss range at this end of the prior.
  - Holding the loss ratio at its low end (L=2): the preferred action flips from Ship to Hold at prior odds ≈ 1:9 (p≈10%) — this crossover falls **inside** the stated prior range.
  - Holding the loss ratio at its high end (L=20): the flip point is prior odds ≈ 1:90 (p≈1.1%), which is **below** the stated prior floor of 1:49 — so Hold is preferred across the *entire* stated prior range at this end of the loss ratio.
  - Net picture: Ship is preferred only in the corner of the swept box where the prior is near its low end (real regressions this rare going in) *and* the loss ratio is near its low end (missing a real one isn't much worse than a needless hold). Everywhere else in the stated ranges, Hold is preferred.

## Verdict

- Verdict: prior-sensitive — the preferred action flips within both the stated prior class and the stated loss range (per SKILL.md's rule for this combined case, the verdict slot is prior-sensitive and its Conditions state the loss crossover too)
- Recommended action: returned to owner
- Conditions: Ship is defensible only if you believe (a) the "going in" odds of a real regression sit toward the low end of the stated range (nearer 1-in-50 than 1-in-5), and (b) the cost of missing a real regression sits toward the low end of the stated multiple (nearer 2x than 20x a needless hold). If either belief shifts toward the range's high end, Hold is preferred. Given the team already disagrees on the loss number, and the evidence in hand (T1+T3) only pulls the odds up by a factor of 4.5 — not enough to dominate a wide prior range — this is not a case where the record can settle it without the owner picking a number on one or both scales.

## Handoff

- Open factual disputes: whether the observed gap is a real served-latency regression (H1) or an exporter/measurement artifact (H2) is still unresolved — T2, the discriminating test, never ran because S3 (raw access logs) was not restored in time. Restoring S3 and running T2 would supply the LR this record currently lacks for separating H1 from H2 specifically. Route to `hypothesis-driven-analysis` if that test can still be completed before Friday.
- Identification gaps: none — H1 is a descriptive claim, no causal identification is at stake in this decision.
- VoI question: whether restoring S3 and running T2 before Friday is worth the delay it would itself cost, given the freeze deadline — this is a candidate for the voi route if the team wants that pull priced out, but pricing it was not asked here and is not done in this record.
