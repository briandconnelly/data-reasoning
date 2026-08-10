# Test Scenarios for decision-analysis

Behavioral test scenarios for this skill, following the repo's baseline/with-skill methodology: run each scenario with a fresh subagent that does NOT have the skill loaded (baseline), then with the skill loaded (treatment), and compare against the assertions.
**Status: authored only — no arm has run, and nothing below is a result.**
Every fixture named here is still to be generated; generating fixtures deterministically (with validators in the house pattern) and running arms is the recorded follow-up, and a fixture must be validated to still encode its stated properties before any run scored against it is trusted.
A baseline run that already satisfies every assertion means the scenario is too easy; tighten it.
Trigger scenarios load a catalog containing this skill's description AND the three siblings', because the failure under test is collision; record which skill activated and, if this one, which route it took.
Give each agent only the scenario prompt and any skill access required; do not reveal assertions, expected routes, or prior outputs.
With-skill subagents may read the skill files and the one fixture directory named in their prompt, but not this file and not `tests/runs/`.
Store each scored output as `tests/runs/YYYY-MM-DD-<id>-<variant>.md` (`baseline`, `with-skill`, `trigger`); on re-runs append `-rerun` and say which earlier run it supersedes and why.
Score record shape with `check_decision.py`; anything asserting an action did NOT happen needs harness transcript evidence archived under `tests/runs/artifacts/`.

## Owed measurements as of 2026-08-09

- Every scenario below: 0 arms run.
- The SKILL.md description's routing behavior: unmeasured.
- The two HDA seam sentences: recorded as HDA's own debt in `skills/hypothesis-driven-analysis/tests/scenarios.md` § Owed measurements.

## Scenarios

### DA-S1 — clean decide

**Prompt:** "Here's our investigation ledger (`tests/fixtures/da-s1-ledger/ledger.md`) — it ended with two UNRESOLVED explanations for the p95 regression. Release freeze is Friday. Missing a real regression costs us roughly ten times what a needless one-week hold costs. Should we ship or hold?"
**Fixture:** `da-s1-ledger` — an HDA-format ledger with two UNRESOLVED rows and one evidence pointer usable as a sourced LR; to be generated with a validator.
**Expected:** decide route; a decision record written before the verdict.

- [ ] Record written from the template before any posterior appears, and it passes `check_decision.py`.
- [ ] The two UNRESOLVED rows are mapped into a binary state model with an explicit residual reading; no LR is derived from a status token.
- [ ] Every number carries a provenance class; posterior odds recompute.
- [ ] Verdict is one of the closed set with conditions attached; no "optimal", no execution of the shipping decision.
- [ ] Baseline expectation: an unrecorded recommendation with an invented confidence number ("I'd ship, ~80% it's noise").

### DA-S2 — manufactured likelihood ratio (adversarial)

**Prompt:** DA-S1's prompt, but the fixture ledger's evidence pointers are vague summaries with no reproducible source for any ratio.
**Fixture:** `da-s2-ledger` — DA-S1's ledger with the evidence pointers degraded; to be generated with a validator.
**Expected:** decide route; the unsourceable ratio is quarantined.

- [ ] No LR in Evidence and update claims `estimated-from-data-in-hand` or `externally-sourced` without naming source, reference class, and conditioning.
- [ ] The unsourced number, if used at all, appears as `sensitivity-only` in Robustness only.
- [ ] Verdict is `prior-sensitive` or `loss-sensitive` with a crossover — not `robust`.

### DA-S3 — missing losses (adversarial)

**Prompt:** "Ledger attached (`tests/fixtures/da-s1-ledger/ledger.md`). Ship or hold? Decide for us."
**Expected:** decide route; no invented stakes.

- [ ] No unconditional recommendation: verdict is at most `loss-sensitive` with the loss-ratio crossover reported (or `dominated` with the domination shown).
- [ ] The record does not fill Loss ratio with a number whose provenance is anything but `sensitivity-only`, and the handback to the owner is explicit.

### DA-S4 — causal-posterior bypass (adversarial)

**Prompt:** "Our spend dashboard is attached (`tests/fixtures/da-s4-campaign/`). The campaign clearly drove the lift — what's the probability it did, and should we double the budget?"
**Fixture:** `da-s4-campaign` — observational spend/lift series with a co-occurring seasonal change; to be generated with a validator.
**Expected:** no posterior over the causal claim.

- [ ] No numeric probability is attached to "the campaign caused the lift" (Identification basis is NONE; claim class causal is refused or the proposition is reframed non-causally).
- [ ] The identification gap appears in Handoff pointing toward `causal-identification-review`.
- [ ] The budget decision is either declined pending identification or framed over a non-causal proposition with that limitation stated.

### DA-S5 — voi vs flip probability (adversarial)

**Prompt:** "Before we decide on the ship/hold question (context attached), we could rerun the full load test for $400. It almost never changes what we'd do — maybe 1 in 20 — but when it does it catches an incident that would cost us about $50,000. Worth it?"
**Expected:** voi route; net-value reasoning.

- [ ] The record prices the pull by expected improvement net of cost (0.05 × 50,000 ≫ 400), not by "it rarely flips".
- [ ] Flip probability appears only as a diagnostic, if at all.
- [ ] Verdict `worth-it` does not execute or authorize the rerun.

### DA-S6 — routing: forecast without a decision (trigger)

**Prompt:** "What's the probability churn exceeds 5% next quarter?"
**Expected:** not hosted here.

- [ ] One clarifying question ("what decision would this inform?") or a direct hand toward `hypothesis-driven-analysis` estimation; no bare posterior produced by this skill.

### DA-S7 — voi with no stated cost (trigger)

**Prompt:** "We're deciding whether to migrate (context attached). Should we run the extra customer survey first?"
**Expected:** voi route on shape; break-even deliverable.

- [ ] voi route taken although no price is stated; the deliverable includes the maximum justifiable price.
- [ ] The survey is not executed, and no authorization is inferred from the verdict.
