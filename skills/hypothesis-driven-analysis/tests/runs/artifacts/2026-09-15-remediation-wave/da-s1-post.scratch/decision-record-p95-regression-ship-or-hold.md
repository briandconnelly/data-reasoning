# Decision Record: ship or hold the release carrying the connection-pool change, given the UNRESOLVED p95-regression ledger

## Decision frame

- Route: decide — value set per `../skills/decision-analysis/SKILL.md` § Routing (authority)
- Actions: Ship (proceed with the release carrying the pool change at Friday's freeze) vs Hold (delay the release past Friday's freeze pending further investigation)
- Decision owner: the user (release owner)
- Reversibility: Ship, if wrong, exposes users to the regression until it is detected post-release and rolled back — cost accrues while live. Hold is fully reversible — ship next week once the open question is resolved; its cost is the delay itself.
- Deadline or forcing event: release freeze Friday (2026-09-18, per user's message; the ledger identifies the affected release as "the 2026-09-12 release" carrying the pool change)
- Consequences (units: hold-cost-equivalents, where 1 = the cost of a needless one-week hold):

  | | H1 true (real regression) | H1 false (not real — artifact or other) |
  | --- | --- | --- |
  | Ship | 10 — a real regression reaches users undetected | 0 — correct call, no cost |
  | Hold | 0 — correct call, no cost beyond the delay itself | 1 — needless one-week hold |

- Loss ratio: 10 (cost of shipping a real regression ÷ cost of a needless hold) — provenance: user-elicited (user's message: "missing a real regression costs us roughly ten times what a needless one-week hold costs")
- Decision threshold (posterior odds): 1:10 (H1-true : H1-false) — provenance: user-elicited (derived algebraically from the loss ratio above; expected loss of Ship = 10p, of Hold = 1-p, equal at p = 1/11, i.e. odds 1/10)

## Decision-state model

- Proposition (H1, as stated in the ledger): the canary hosts' served checkout latency is genuinely higher than control on 2026-09-09 — a real regression in what users experience, whatever its cause.
- Residual reading: not-H1 includes H2 as named in the ledger (the canary exporter's sampling changed, inflating measured p95 without a real latency change) *and* any other unnamed explanation for the observed gap (other instrumentation issues, a transient confound, etc.) that would not represent a real change in served latency.
- Claim class: descriptive (per ledger: H1's claim class is descriptive, estimand = canary minus control served checkout p95 on 2026-09-09, ms) — value set per `../skills/decision-analysis/SKILL.md` § The Decide Route (authority)
- Identification basis: NONE — no causal claim is being scored; H1 is descriptive as stated in the ledger, so no causal-wording bar applies.
- Identification conditions: none
- Ledger mapping: ledger row H1 ("real regression") maps directly to this record's H1-true state. Ledger row H2 ("exporter/sampling artifact") folds into the residual (not-H1), alongside unnamed alternatives. Both ledger rows remain UNRESOLVED as ledger status tokens; per SKILL.md, that status carries no likelihood information on its own — the likelihood ratio below is derived from the ledger's Tests table (T1, T3), not from the UNRESOLVED label.

## Evidence and update

- Prior odds: none supported — see Robustness (per `../skills/decision-analysis/SKILL.md` § Degraded Modes (authority) — S2 is explicitly quota-stratified 10 real/10 not by the analyst, so it "says nothing about how often a gap turns out real" as a base rate; no other source in the ledger supplies a prior; none was user-elicited)
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | Canary/control gap (57 ms) exceeds the 40 ms historical noise band (T1), and in the reference class of past rollouts this gap size is 4.5x more common when the underlying regression was later confirmed real than when it wasn't (T3) | 4.5 | estimated-from-data-in-hand | S1 (`evidence/host_p95.csv`, per-host p95, 2026-09-09, established the 57 ms gap and that it clears the 40 ms noise band) combined with S2 (`evidence/reference_class.csv`, 20 past canary rollouts, quota-stratified 10 settled-real / 10 settled-not-real by the analyst): within that reference class, P(gap > 40 ms \| real) = 9/10, P(gap > 40 ms \| not real) = 2/10, LR = 0.9/0.2 = 4.5. Conditioning: rollouts classified by whether the canary/control gap exceeded the 40 ms threshold, cross-tabulated against post-mortem status. |
  | Exporter-artifact discriminator (T2: raw access-log p95 vs. exporter-reported p95 on canary hosts) | none supported | none supported | S3 not acquired — 7-day retention, restore request pending; T2 is NOT_TESTED in the ledger, so it contributes no update either way |

- Independence: T1 and T3 are combined into one item, not multiplied as two: T1 establishes that this rollout's gap clears the 40 ms threshold that T3's likelihood ratio is conditioned on. Treating them as two independent multiplicative factors would double-count the same threshold-crossing signal.
- Posterior odds: none supported — see Robustness (prior is unsupported per Degraded Modes; robustness below applies the 4.5 LR to a swept prior class instead of a point prior)

## Robustness

- Prior class swept: 1:4 to 4:1 (H1-true : H1-false odds, i.e. 20%–80% probability of a real regression) — provenance: sensitivity-only. (Matches the width of the worked example in SKILL.md § Degraded Modes; chosen as a standard-width, not cherry-picked, uninformative-ish sweep given no sourced prior exists.)
- Loss range swept: 5 to 20 (around the user's "roughly ten," which is not stated as an exact point) — provenance: sensitivity-only around a user-elicited central value of 10
- Crossover: applying the 4.5 LR, posterior odds = prior odds × 4.5. The action flips from Hold to Ship when posterior odds fall below the loss-ratio threshold (1/loss-ratio):
  - At loss ratio 10 (user's stated value): flip at prior odds 1:45 (≈2.2% prior probability of a real regression)
  - At loss ratio 5: flip at prior odds 1:22.5 (≈4.3%)
  - At loss ratio 20: flip at prior odds 1:90 (≈1.1%)
  In all three cases the flip point is far below the swept prior class's floor (1:4 odds ≈ 20%). Across the entire swept prior class (1:4 to 4:1) and the entire swept loss range (5 to 20), Hold is preferred; Ship would only become preferred for a prior probability of a real regression below roughly 1%–4% (depending on the exact loss ratio) — a materially more skeptical prior than the swept class considers.

## Verdict

- Verdict: robust — value set and semantics per `../skills/decision-analysis/SKILL.md` § The Decide Route (authority)
- Recommended action: Hold (delay the release past Friday's freeze, pending further investigation)
- Conditions: holds across prior odds 1:4 to 4:1 (unsupported by data, swept as sensitivity-only per § Degraded Modes) and loss ratio 5–20 (sensitivity range around the user-elicited value of 10); the losses are belief-grade (user-elicited), which is what licenses a `robust` call despite the unsupported prior. The verdict would only reverse to Ship for a prior probability of a real regression below roughly 1%–4% — i.e., a stance more skeptical than "1 in 25" that this is real, held *even after* weighing the reference-class evidence. If the decision owner's actual prior is that skeptical, say so and this call returns to `prior-sensitive`.

## Handoff

- Open factual disputes: whether the gap is a real served-latency regression (H1) or an exporter/sampling artifact (H2) remains unadjudicated — T2, the one test that could discriminate them, did not run (S3 not acquired). This dispute does not change the verdict above, because the decision-state model's residual already absorbs H2 (and unnamed alternatives) into "not-H1," and the verdict is robust to that residual across the swept classes. It does matter for follow-up: if the release is held, resolving H1 vs. H2 via the pending S3 restore and T2 is the natural next step — hand to `hypothesis-driven-analysis`.
- Identification gaps: none — H1 is descriptive, not causal.
- VoI question: whether restoring S3 (raw access logs) and running T2 before the freeze is worth its cost/delay. Given the current verdict is already robust to the H1/H2 ambiguity for the ship/hold call itself, this pull's value is in firming up cause and magnitude for post-hold engineering work, not in flipping this decision — worth pricing separately if the owner wants that certainty regardless.
