# Decision Record: ship the 2026-09-12 release (pool change) or hold it a week, given the UNRESOLVED p95-regression ledger

## Decision frame

- Route: decide — value set per `../skills/decision-analysis/SKILL.md` § Routing (authority)
- Actions: Ship (proceed with the 2026-09-12 release carrying the connection-pool change) vs Hold (delay the release at least one week, pending discrimination between H1 and H2)
- Decision owner: the release-owning team (not individually named in the prompt or ledger)
- Reversibility: Ship exposes users to any real regression for the exposure window before a rollback/hotfix could land — that exposure cost is not undone by a later fix. Hold is fully reversible: ship next cycle once T2 runs or the deadline forces a call.
- Deadline or forcing event: release freeze Friday (2026-09-18)
- Consequences:

  | | H1 true (real regression) | H1 false (residual: artifact / noise / unnamed) |
  | --- | --- | --- |
  | Ship | regression reaches users — cost = miss cost, `k` units | no regression shipped — cost ≈ 0 |
  | Hold | regression avoided — cost ≈ 0 | needless one-week hold — cost = 1 unit (baseline) |

- Loss ratio: `k` = cost of missing a real regression, in units of one needless one-week hold — range 2–20 — provenance: user-elicited ("the team can't agree on the number")
- Decision threshold (posterior odds): Ship preferred when posterior odds of H1 < `1/k`; Hold preferred when posterior odds > `1/k` — provenance: derived from the user-elicited loss ratio (not a separately-elicited number)

## Decision-state model

- Proposition (H1, as stated): the canary hosts' served checkout latency on 2026-09-09 is genuinely higher than control — a real regression in what users experience, whatever its cause (ledger's own wording; descriptive, not causal — no claim about what caused it)
- Residual reading (not-H1): the observed gap is not a genuine change in served latency. This absorbs H2 (exporter/pipeline sampling artifact inflating the measured p95 without any real latency change) and any other explanation nobody named. It does **not** claim H2 specifically is true — only that H1 is false.
- Claim class: descriptive (ledger's own label for H1's row)
- Identification basis: NONE — no causal claim is being scored; H1 is an estimand claim (canary minus control served p95 on 2026-09-09), not a "the pool change caused X" claim
- Identification conditions: none
- Ledger mapping: H1 (UNRESOLVED) → proposition true. H2 (UNRESOLVED) → folds into the residual, alongside noise/other. The residual is exactly what T2 (NOT_TESTED, S3 not acquired) would have separated from H1 — the ledger's stop condition ("remaining tests cannot run before the release decision") is the reason this decision runs on UNRESOLVED evidence rather than a settled ledger.

## Evidence and update

- Prior odds: 0.02–0.2 (1 in 50 to 1 in 5, as stated by the user "going in") — provenance: user-elicited
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | Observed canary/control p95 gap of 57 ms, which exceeds the pre-established 40 ms noise band (T1/S1), calibrated against how often such a gap appears when a past rollout's regression was later settled real vs. not (T3/S2) | 4.5 (= 0.9 / 0.2) | estimated-from-data-in-hand | S2: 20 past canary rollouts, quota-drawn 10 settled-real / 10 settled-not-real by post-mortem status; P(gap>40ms \| real)=9/10, P(gap>40ms \| not real)=2/10. Conditioning: applies given a >40ms gap is observed, which T1/S1 established for the current case. The quota-drawn sampling caps a base rate (why the prior above is user-elicited, not read off S2) but does not bias these within-stratum conditional frequencies. |

- Independence: single combined item, not two multiplied items. T1 establishes the observation (a >40ms gap exists); T3 is the calibration of what that same observation implies (how often such a gap accompanies a real vs. not-real regression). Multiplying them as if independent would double-count the same fact.
- Note on what this LR does *not* do: it does not discriminate H1 from H2 specifically — S2's "not real" post-mortems are a mixed bag of causes (of which an exporter-style artifact is one plausible member), and the ledger's own Limitations state no test in hand separates H1 from H2 (T2 NOT_TESTED, S3 not acquired). The LR moves belief away from "the gap is nothing" toward "the gap reflects *some* real phenomenon (real regression or a systematic artifact)" without saying which.
- Posterior odds: 0.09–0.9 (= prior odds × 4.5)

## Robustness

- Prior class swept: 0.02–0.2 (as user-elicited) — provenance: user-elicited
- Loss range swept: 2–20 (as user-elicited) — provenance: user-elicited
- Crossover: Ship is preferred iff posterior odds < `1/k`, i.e. iff prior odds × 4.5 < `1/k`.
  - At the low end of the loss range (`k`=2, threshold odds=0.5): crossover prior odds ≈ 0.111 — Ship favored below that, Hold favored above it. This crossover point sits *inside* the swept prior range [0.02, 0.2].
  - At the high end of the loss range (`k`=20, threshold odds=0.05): crossover prior odds ≈ 0.0111 — below the entire swept prior range, so Hold is favored for every prior in [0.02, 0.2] once `k` reaches 20.
  - At the low end of the prior range (prior=0.02, posterior=0.09): crossover loss ratio ≈ 11.1 — Ship favored for `k` below that, Hold above. This sits inside the swept loss range [2, 20].
  - At the high end of the prior range (prior=0.2, posterior=0.9): crossover loss ratio ≈ 1.11 — below the entire swept loss range's floor of 2, so Hold is favored for every `k` in [2, 20] once the prior reaches 0.2.
  - Net shape: Ship only wins in the low-prior / low-loss-ratio corner of the swept box (roughly prior < 0.111 combined with `k` below ~1/(4.5×prior)); Hold wins everywhere else, including the entire upper half of the prior range regardless of `k`, and the entire upper half of the loss range regardless of prior.

## Verdict

- Verdict: prior-sensitive (the preferred action flips within the stated prior class for part of the stated loss range; the loss ratio is independently outcome-determining across most of that same prior range — see Conditions)
- Recommended action: returned to owner
- Conditions: the flip depends jointly on where the true prior sits in [0.02, 0.2] (user-elicited "going-in odds") and where the true loss ratio sits in [2, 20] (user-elicited, and explicitly disputed within the team). Ship is defensible only if both the team's going-in skepticism is near the low end of its stated range *and* the loss ratio is agreed to be near the low end of its stated range. Anywhere the prior sits above ≈0.111 (posterior above ≈0.5), Hold is preferred regardless of which loss ratio (2–20) is chosen. The evidence's own limitation caps how much weight the LR can bear: it moves odds off the "nothing's there" hypothesis but does not distinguish a real regression from an exporter artifact.

## Handoff

- Open factual disputes: whether T2 (recomputing p95 from raw access logs on the canary hosts) would show the same elevation as the metrics pipeline, or show it flat — this is the test that would separate H1 from H2 and is currently NOT_TESTED because S3 (raw access logs) was not acquired before this decision. Route to `hypothesis-driven-analysis` once S3 restores.
- Identification gaps: none — H1 is descriptive, not causal; no causal posterior was computed here.
- VoI question: whether restoring S3 and running T2 before Friday's freeze is worth doing, given that the current posterior (0.09–0.9 odds) straddles the decision threshold (0.05–0.5 odds) for a substantial part of the stated prior and loss ranges — meaning T2's result could plausibly flip the recommended action. The restore's cost and timing are not stated in the ledger ("restore request pending"), so this question is named here but not priced.
