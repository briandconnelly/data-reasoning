# Scenario 11 — 2026-08-10 (Sonnet as main agent)

Wave: Sonnet-as-main-agent, preregistered in `artifacts/2026-08-10-sonnet-mainagent-wave-prereg.md`.
Model: Sonnet, fresh general-purpose subagent acting as main agent, skill loaded by path, forbidden from `tests/scenarios.md` and `tests/runs/`.
Fixture: `s11-mini/checkout_latency.csv`.
Scorer: dispatching session (Fable), against the committed S11 assertions.
Arm ledger archived at `artifacts/2026-08-10-sonnet-mainagent-s11-ledger.md`.

| Assertion | Result | Evidence |
| --- | --- | --- |
| Routes mini: one-paragraph ledger (claim, prediction, probe, outcome), not the full loop | PASS | Archived ledger has exactly the mini form: Claim / Prediction / Probe / Result / Outcome |
| No hypothesis table, no Sources/Tests/Amendments sections | PASS | Archived ledger contains none of those sections |
| Answers correctly that the claim is false, reporting the measured p95 | PASS | p95 = 392.2ms reported; scorer recomputed n=1200, p95=392.2, p50=200.0, 14 requests >500ms — exact match |

Total: 3/3.
Score-the-reasoning check (the S11 history's wrong-reason trap): the arm routed mini because "someone asserted something ... a truth-value claim someone will act on needs a prediction, a probe, and a recorded outcome", explicitly contrasting with a bare direct lookup — the claim/question distinction, not the effort distinction.
Unprompted extra: the arm found that the file covers only 00:00–19:59 (scorer-verified: timestamps span exactly that window, 1,200 rows) and scoped its refutation to the observed 20-hour window; this coverage property is not in the scenario's documented ground truth.
Tool calls: 5. Tokens: ~49.9k.
