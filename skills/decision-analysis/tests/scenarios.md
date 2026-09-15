# Test Scenarios for decision-analysis

Behavioral test scenarios for this skill, following the repo's baseline/with-skill methodology: run each scenario with a fresh subagent that does NOT have the skill loaded (baseline), then with the skill loaded (treatment), and compare against the assertions.
**Status: the original scenarios below are authored only — no arm of those fixtures has run, and nothing below is a result.**
Separate, focused VoI wording checks are recorded in `runs/2026-09-04-voi-pricing.md`; they do not complete this scenario suite.
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
- The post-2026-09-04 VoI wording that permits a bound-determined `not-worth-it` verdict, accepts mixed signal-model provenance, and requires the tight binary loss-matrix bound: unmeasured.
- The 2026-09-15 wording: § Verdict's precedence rule when both sensitivities fire (`prior-sensitive`, loss crossover in Conditions), and § Degraded Modes' no-defensible-prior procedure with its worked example: unmeasured.
  Reachability: DA-S1 (an `UNRESOLVED` ledger with one sourced LR and no elicited prior) traverses the degraded mode's no-supported-prior branch and must keep that LR in the sweep; a scenario whose sweep flips on both axes traverses the precedence rule.
  **Paid 2026-09-15** for DA-S1 and DA-S8 (three arms each: baseline, `main` wording, this wording), preregistered in `../../hypothesis-driven-analysis/tests/runs/artifacts/2026-09-15-remediation-wave-prereg.md` and recorded in `runs/2026-09-15-da-s1-da-s8-degraded-mode-and-precedence.md`.
  The degraded mode changed the record's content (the post arm used the `none supported — see Robustness` sentinel where the pre arm put an invented `sensitivity-only` prior in Evidence and update) but the sentinel was annotated, not bare; the precedence paragraph was not needed — the pre arm already chose `prior-sensitive` with the loss crossover in Conditions.
  Neither arm's record passed `check_decision.py`, every failure on form; see the debt below.
- Debt surfaced 2026-09-15: every decision record in that wave, under either wording, failed `check_decision.py` on annotated slots, `1:49`-style odds, relabelled slots, and six-cell evidence rows, with correct arithmetic underneath.
  The template's slot text invites the annotations the checker forbids; the two need reconciling before DA-S1.1's "passes `check_decision.py`" can be a fair bar.
  **Reconciled 2026-09-15 (wave 2):** the template's skeletons now show bare values and exact labels with the guidance in § Slot notes; under it the DA-S1 and DA-S8 post arms wrote bare sentinels, decimal odds, exact labels, and four-cell rows, and each failed `check_decision.py` on exactly one gate (`runs/2026-09-15-da-s1-da-s8-degraded-mode-and-precedence.md` § Wave 2).
- Debt surfaced 2026-09-15 (wave 2): given a rounded loss ("roughly ten"), three of four skill arms swept a range around it, labelled the sweep `sensitivity-only`, and still called the verdict `robust`, which § Numeric Policy caps at `loss-sensitive`; the one arm that read "roughly ten" as `8–12 — user-elicited` passed both checkers.
  A worked example or slot note for a rounded elicited loss is a wording change owing its own arm.
- **Withdrawn 2026-09-15:** the no-defensible-prior degraded mode measured in DA-S1 landed on the preregistration's row 6 (its own condition that `robust` needs belief-grade losses was not met by any skill arm) and was dropped from the branch per that preregistration's amendment 2; the external review's finding 7 — a record form for missing quantitative evidence — is owed.
  A future attempt owes a `loss-sensitive` path for a no-prior record with `sensitivity-only` losses, which the withdrawn checker branch lacked, and its own preregistered arms.
- Debt surfaced 2026-09-15 (wave 2): a `prior-sensitive` record must state two crossovers and the template's Crossover slot has one line; the DA-S8 post arm wrote both as prose and the checker read the wrong number.

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


### DA-S8 — both sensitivities fire (precedence)

**Prompt:** "Here's our investigation ledger (`tests/fixtures/da-s1-ledger/ledger.md`) — it ended with two UNRESOLVED explanations for the p95 regression. Going in, we'd put the odds that it's a real regression somewhere between 1 in 50 and 1 in 5. Missing a real regression costs us somewhere between 2 and 20 times what a needless one-week hold costs — the team can't agree on the number. Release freeze is Friday. Should we ship or hold?"
**Fixture:** `da-s1-ledger` — DA-S1's ledger; its reference class supplies one sourced LR (4.5).
**Expected:** decide route; with prior odds 0.02–0.2 and LR 4.5 the posterior spans 0.09–0.9, and with a loss ratio of 2–20 the threshold spans 0.05–0.5, so the preferred action flips inside the prior class and inside the loss range at once.
Added 2026-09-15 for the § Verdict precedence rule (both sensitivities fire → `prior-sensitive`, loss crossover in Conditions); DA-S3 cannot measure it, because a record with no supported inputs reaches a sensitive verdict through the degraded mode and the loss rule without touching the precedence paragraph.

- [ ] Record written from the template before any posterior appears, and it passes `check_decision.py`.
- [ ] Prior odds and loss ratio carry the user-elicited ranges; the LR 4.5 row names `reference_class.csv`, the 20-rollout stratified class, and the 40 ms gap condition; posterior odds recompute (0.09–0.9).
- [ ] Robustness reports both crossovers: the prior odds at which the action flips for a given loss ratio, and the loss ratio at which it flips for a given prior.
- [ ] Verdict is `prior-sensitive`, not `loss-sensitive`; Robustness states both the prior and the loss crossover; Recommended action reads `returned to owner`.
  (Revised 2026-09-15 with § Verdict: the first form also required the loss crossover in Conditions, which one of two post arms and the pre arm did not do; see `runs/2026-09-15-da-s1-da-s8-degraded-mode-and-precedence.md` § Wave 3.)
- [ ] Baseline expectation: picks a point estimate from each range and recommends unconditionally.
