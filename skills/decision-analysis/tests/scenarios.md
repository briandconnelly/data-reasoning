# Test Scenarios for decision-analysis

Behavioral test scenarios for this skill, following the repo's baseline/with-skill methodology: run each scenario with a fresh subagent that does NOT have the skill loaded (baseline), then with the skill loaded (treatment), and compare against the assertions.
**Status (2026-11-17, except where a clause is dated):** DA-S1, DA-S1x, DA-S3, DA-S6, DA-S8, DA-S9, and DA-S10 have scored arms, recorded under `runs/` and summarized per cell in `docs/evidence-status.md`, which is the authority on what each measured and which wording ships; DA-S2, DA-S4, DA-S5, DA-S7, and DA-S11 have no arm; DA-S12 and DA-S13 (added 2026-11-24) are unrun.
Separate, focused VoI wording checks are recorded in `runs/2026-09-04-voi-pricing.md`; they do not complete this scenario suite.
Generated fixtures: `da-s1-ledger` (DA-S1, DA-S1x, DA-S3, DA-S8) and `da-sweep` (DA-S9, DA-S10), each with a validator in the house pattern and a prek hook; the fixtures DA-S2, DA-S4, DA-S12, and DA-S13 name are still to be generated.
A fixture must be validated to still encode its stated properties before any run scored against it is trusted.
A baseline run that already satisfies every assertion means the scenario is too easy; tighten it.
Trigger scenarios load a catalog containing this skill's description AND the three siblings', because the failure under test is collision; record which skill activated and, if this one, which route it took.
Give each agent only the scenario prompt and any skill access required; do not reveal assertions, expected routes, or prior outputs.
With-skill subagents may read the skill files and the one fixture directory named in their prompt, but not this file and not `tests/runs/`.
Store each scored output as `tests/runs/YYYY-MM-DD-<id>-<variant>.md` (`baseline`, `with-skill`, `trigger`); on re-runs append `-rerun` and say which earlier run it supersedes and why.
Score record shape with `check_decision.py`; anything asserting an action did NOT happen needs harness transcript evidence archived under `tests/runs/artifacts/`.

## Owed measurements (opened 2026-08-09; entries dated)

- As of 2026-08-09 every scenario below had 0 arms run; the 2026-09-15 and 2026-11-08 entries below record the arms since.
- The SKILL.md description's routing behavior: unmeasured.
- The two HDA seam sentences: recorded as HDA's own debt in `skills/hypothesis-driven-analysis/tests/scenarios.md` § Owed measurements.
- The 2026-11-17 signal-coherence change (#94) reaches DA-S5, DA-S7, and DA-S11; all are unmeasured.
  The attached decision context in DA-S5 and DA-S7 must supply a priceable signal model to exercise their expected pricing outcomes.
- The post-2026-09-04 VoI wording that permits a bound-determined `not-worth-it` verdict, accepts mixed signal-model provenance, and requires the tight binary loss-matrix bound: unmeasured.
- The 2026-09-15 wording: § Verdict's precedence rule when both sensitivities fire (`prior-sensitive`, loss crossover in Conditions), and § Degraded Modes' no-defensible-prior procedure with its worked example: unmeasured.
  Reachability: DA-S1 (an `UNRESOLVED` ledger with one sourced LR and no elicited prior) traverses the degraded mode's no-supported-prior branch and must keep that LR in the sweep; a scenario whose sweep flips on both axes traverses the precedence rule.
  **Paid 2026-09-15** for DA-S1 and DA-S8 (three arms each: baseline, `main` wording, this wording), preregistered in `../../hypothesis-driven-analysis/tests/runs/artifacts/2026-09-15-remediation-wave-prereg.md` and recorded in `runs/2026-09-15-da-s1-da-s8-degraded-mode-and-precedence.md`.
  The degraded mode changed the record's content (the post arm used the `none supported — see Robustness` sentinel where the pre arm put an invented `sensitivity-only` prior in Evidence and update) but the sentinel was annotated, not bare; on the precedence paragraph every skill arm chose `prior-sensitive`, and only the wave-1 post arm stated the loss crossover in Conditions as the paragraph then required (this summary first said the pre arm did; the run record's corrected table is the authority).
  Neither arm's record passed `check_decision.py`; most failures were form, one was substantive (a `sensitivity-only` loss sweep under a `robust` verdict), and one was the checker's (escaped pipes); see the debts below.
- Debt surfaced 2026-09-15: every decision record in that wave, under either wording, failed `check_decision.py` on annotated slots, `1:49`-style odds, relabelled slots, and six-cell evidence rows, with correct arithmetic underneath.
  The template's slot text invites the annotations the checker forbids; the two need reconciling before DA-S1.1's "passes `check_decision.py`" can be a fair bar.
  **Reconciled 2026-09-15 (wave 2):** the template's skeletons now show bare values and exact labels with the guidance in § Slot notes; under it the DA-S1 and DA-S8 post arms wrote bare sentinels, decimal odds, exact labels, and four-cell rows, and each failed `check_decision.py` on exactly one gate (`runs/2026-09-15-da-s1-da-s8-degraded-mode-and-precedence.md` § Wave 2).
- Debt surfaced 2026-09-15 (wave 2): given a rounded loss ("roughly ten"), three of four skill arms swept a range around it, labelled the sweep `sensitivity-only`, and still called the verdict `robust`, which § Numeric Policy caps at `loss-sensitive`; the one arm that read "roughly ten" as `8–12 — user-elicited` passed both checkers.
  A worked example or slot note for a rounded elicited loss is a wording change owing its own arm.
- **Withdrawn 2026-09-15:** the § Verdict precedence paragraph for a double flip landed on row 3 at wave 3 (the post arm read the elicited prior as probabilities and failed DA-S8.2, which the pre arm passes) and was dropped per the preregistration; the external review's A2 — one verdict slot, two applicable sensitivity labels — is owed.
  Every skill arm, pre and post, chose `prior-sensitive` in that case, so the remedy may be a clarification whose measurement needs an assertion that settles how "odds … 1 in N" is read.
  **Attempt 2, 2026-11-08:** the precedence lives in § Numeric Policy's ordered rule (a prior flip at the stated losses gives `prior-sensitive` whether or not the losses flip too) and is measured as a clarification with no lift: under a DA-S8 prompt that now states odds explicitly, pre and post both chose `prior-sensitive` and both pass every DA-S8 assertion under the final wording (`runs/2026-11-08-no-supported-prior.md`). Sentences prescribing which slot carries which crossover were tried, failed the checker on the first post arm, and were withdrawn; where the second crossover goes is the remaining debt.
- **Withdrawn 2026-09-15:** the no-defensible-prior degraded mode measured in DA-S1 landed on the preregistration's row 6 (its own condition that `robust` needs belief-grade losses was not met by any skill arm) and was dropped from the branch per that preregistration's amendment 2; the external review's finding 7 — a record form for missing quantitative evidence — is owed.
  A future attempt owes a `loss-sensitive` path for a no-prior record with `sensitivity-only` losses, which the withdrawn checker branch lacked, and its own preregistered arms.
  **Attempt 2, 2026-11-08:** § Numeric Policy now carries the no-supported-prior form, the rounded-loss rule, and one ordered verdict rule with the loss cap; both checkers carry the paired sentinels and the per-axis flip tests; preregistered in `runs/artifacts/2026-11-08-no-supported-prior-prereg.md` (DA-S1, DA-S1x exact-loss control, DA-S3, DA-S8).
- Debt surfaced 2026-09-15 (wave 2): a `prior-sensitive` record must state two crossovers and the template's Crossover slot has one line; the DA-S8 post arm wrote both as prose and the checker read the wrong number.
- The 2026-11-09 wording (`decisions/007`): the likelihood-ratio clause, the `evidence-sensitive` verdict, the tie and point rulings, and the Favored if true orientation slot.
  **Measured 2026-11-10** (`runs/2026-11-10-evidence-sweep.md`): no behavioral lift on DA-S9 or DA-S10 at n=3 (pre already reasoned and acted correctly; preregistration row 7), no regression on the DA-S1 and DA-S8 controls at n=1; under the pre text all three DA-S9 arms chose `prior-sensitive`, which failed the base checker 3/3.
  Preregistered in `runs/artifacts/2026-11-09-evidence-sweep/prereg.md` (new cells DA-S9 and DA-S10); the cells that already exist and reach the edited text are listed, with the debt left unpaid, in `runs/artifacts/2026-11-09-evidence-sweep/reachability.md`.

## Scenarios

### DA-S1 — clean decide

**Prompt:** "Here's our investigation ledger (`tests/fixtures/da-s1-ledger/ledger.md`) — it ended with two UNRESOLVED explanations for the p95 regression. Release freeze is Friday. Missing a real regression costs us roughly ten times what a needless one-week hold costs. Should we ship or hold?"
**Fixture:** `da-s1-ledger` — an HDA-format ledger with two UNRESOLVED rows and one evidence pointer usable as a sourced LR; generated by `fixtures/generate_da_s1.py` and validated by `fixtures/validate_da_s1.py`.
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

- [ ] Either `hypothesis-driven-analysis` is activated directly, or, if `decision-analysis` was selected, it hands toward `hypothesis-driven-analysis` in the same response without waiting on a clarifying question; an invitation to name the decision the forecast would inform is allowed alongside the handoff, not instead of it.
- [ ] No probability, posterior, or decision record produced by this skill.

### DA-S7 — voi with no stated cost (trigger)

**Prompt:** "We're deciding whether to migrate (context attached). Should we run the extra customer survey first?"
**Expected:** voi route on shape; break-even deliverable.

- [ ] voi route taken although no price is stated; the deliverable includes the maximum justifiable price.
- [ ] The survey is not executed, and no authorization is inferred from the verdict.


### DA-S8 — both sensitivities fire (precedence)

**Prompt:** "Here's our investigation ledger (`tests/fixtures/da-s1-ledger/ledger.md`) — it ended with two UNRESOLVED explanations for the p95 regression. Going in, we'd put the prior odds that it's a real regression (real : not real) somewhere between 1:50 and 1:5. Missing a real regression costs us somewhere between 2 and 20 times what a needless one-week hold costs — the team can't agree on the number. Release freeze is Friday. Should we ship or hold?"
(Reworded 2026-11-08: the first form said "odds … 1 in 50 and 1 in 5", which reads as probabilities 1/50–1/5, odds 0.0204–0.25, as readily as odds 0.02–0.2; the arms split on it and DA-S8.2 could not be scored. The prompt now states odds explicitly.)
**Fixture:** `da-s1-ledger` — DA-S1's ledger; its reference class supplies one sourced LR (4.5).
**Expected:** decide route; with prior odds 0.02–0.2 and LR 4.5 the posterior spans 0.09–0.9, and with a loss ratio of 2–20 the threshold spans 0.05–0.5, so the preferred action flips inside the prior class and inside the loss range at once.
Added 2026-09-15 for the § Verdict precedence rule (both sensitivities fire → `prior-sensitive`, loss crossover in Conditions); DA-S3 cannot measure it, because a record with no supported inputs reaches a sensitive verdict through the degraded mode and the loss rule without touching the precedence paragraph.

- [ ] Record written from the template before any posterior appears, and it passes `check_decision.py`.
- [ ] Prior odds and loss ratio carry the user-elicited ranges; the LR 4.5 row names `reference_class.csv`, the 20-rollout stratified class, and the 40 ms gap condition; posterior odds recompute (0.09–0.9).
- [ ] The record reports both crossovers: the prior-odds flip at the stated losses (0.011–0.111 across a loss ratio of 2–20 with LR 4.5) and the loss-ratio flip at the stated prior (11.1 at prior odds 0.02); the Crossover slot takes one bare value or range; where the other is stated is not prescribed.
- [ ] Verdict is `prior-sensitive`, not `loss-sensitive`; Recommended action reads `returned to owner`.
  (Revised 2026-09-15 with § Verdict: the first form also required the loss crossover in Conditions, which one of two post arms and the pre arm did not do; see `runs/2026-09-15-da-s1-da-s8-degraded-mode-and-precedence.md` § Wave 3. Revised 2026-11-08 to the slot's one-value form; see `runs/2026-11-08-no-supported-prior.md`.)
- [ ] Baseline expectation: picks a point estimate from each range and recommends unconditionally.

### DA-S9 — a likelihood-ratio range alone flips the action (evidence sweep)

**Prompt:** `runs/artifacts/2026-11-09-evidence-sweep/prompts/da-s9.txt`, with `{FIXTURE_PATH}` the staged `fixtures/da-sweep/s9-lr-range/` packet: tonight's checksum-mismatch alert on db-07 persisted after a re-read; the alert census's rate is stated as settled; losses over (corrupt, not) are restore now = (1, 1) and keep serving = (3, 0); "should we restore now or keep serving?"
**Fixture:** `da-sweep/s9-lr-range` — a census of 200 alerts (40 confirmed corruption, prior odds 0.25) and a vendor note bounding the re-read ratio to 0.5–4 on every firmware revision; validated by `fixtures/validate_da_sweep.py`.
**Expected:** decide route; restore now is favored if the corruption is real, the incremental loss ratio is (3 − 1) / (1 − 0) = 2, and the threshold is 0.5; posterior odds 0.125–1 straddle it while the prior and the losses are points, so only the ratio range flips the action, at a ratio of 2.
Added 2026-11-09 for § Numeric Policy's likelihood-ratio clause and `evidence-sensitive` verdict (`decisions/007`); the assertions and their scoring are preregistered in `runs/artifacts/2026-11-09-evidence-sweep/prereg.md`.

- [ ] Record written from the template before any posterior appears, and it passes `check_decision.py`.
- [ ] Prior odds `0.25` from the census, held fixed; the ratio row carries `0.5–4`, `externally-sourced`, naming the vendor note, the controller family, and the unknown firmware revision; posterior odds recompute (0.125–1).
- [ ] At the fixed prior, the record shows that varying the ratio alone carries the posterior across the threshold 0.5.
- [ ] Verdict `evidence-sensitive`; Recommended action `returned to owner`; Crossover names the likelihood ratio, 2.
- [ ] Baseline expectation: picks a point inside 0.5–4 or the midpoint and recommends unconditionally.

### DA-S10 — an asymmetric four-cell loss matrix (orientation)

**Prompt:** `runs/artifacts/2026-11-09-evidence-sweep/prompts/da-s10.txt`, with `{FIXTURE_PATH}` the staged `fixtures/da-sweep/s10v2-loss-matrix/` packet: release 6.0's canary spiked; the release census's rate is stated as settled; losses in engineer-days are ship now = (10, 0) and hold one week = (1, 1) over (real, not); "ship now or hold one week?"
**Fixture:** `da-sweep/s10v2-loss-matrix` — a census of releases 3.0–5.6 to a stated cutoff (7 of 207 real regressions, prior odds 0.035) and a quota-drawn reference class of 20,000 canaries per stratum fixing a ratio of 3, narrow enough that its 95% interval keeps the posterior between 0.1 and 1/9; release 6.0 appears in neither; validated by `fixtures/validate_da_sweep.py`.
The first packet, `s10-loss-matrix` (20 per stratum), was retired on 2026-11-10 after its canary stated the ratio as an interval straddling the threshold; it is kept only as that canary's archived input.
**Expected:** decide route; posterior odds 0.105; hold one week is favored if the regression is real, the incremental loss ratio is (10 − 1) / (1 − 0) = 9, so the threshold is 1/9 ≈ 0.111 and ship now is preferred; the raw reading 10:1 gives 0.1 and hold.
Added 2026-11-09 for § Numeric Policy's orientation rule (`decisions/007`); scoring is preregistered beside DA-S9's.

- [ ] Record written from the template before any posterior appears, and it passes `check_decision.py`.
- [ ] Prior odds `0.035` and the ratio `3` carry `estimated-from-data-in-hand`, each naming its file and reference class; posterior odds recompute (0.105).
- [ ] Favored if true reads `hold one week`; Loss ratio reads `9 — provenance: user-elicited`; the threshold stated or implied is 1/9 ≈ 0.111, not 0.1.
- [ ] Verdict `robust`, Recommended action `ship now`.
- [ ] Baseline expectation: reads the matrix as 10:1 and holds, or recommends without a threshold.

### DA-S11 — pricing a signal from reported posteriors

Run each variant as a separate request using the shared prompt and its own vendor figures.

**Prompt:** "I must choose which of two states holds, H or its complement.
My independently established prior for H is [prior].
A wrong choice costs me $100 and a correct choice costs $0.
A vendor offers one report for a total cost of $20 including fees, delay and opportunity cost.
Its only possible returns are red and blue.
The vendor gives the following exact probabilities for this population: [vendor figures].
Should I buy the report?"

**Expected:** voi route for every variant.
Added 2026-11-17 for #94.

| Variant | Prior | Vendor figures (red, blue) | Expected record |
| --- | --- | --- | --- |
| Conflicting prior | 50% | Return probabilities (50%, 50%); P(H given return) (90%, 90%). | Identifies the implied 90% prior versus 50%; uses `unavailable`, `upper-bound`, bound `50 USD`, and `upper-bound-only`. |
| Coherent control | 50% | Return probabilities (50%, 50%); P(H given return) (90%, 10%). | Uses `signal-model`; current expected loss $50, expected loss after the report $10, gross value $40, net value $20, verdict `worth-it`. |
| Incomplete distribution | 50% | Return probabilities (40%, 40%); P(H given return) (75%, 50%). | Identifies total probability 80% even though the weighted sum for H is 50%; same bound and verdict as the conflicting-prior case. |
| Independently established lower prior | 20% | Return probabilities (50%, 50%); P(H given return) (90%, 90%). | Identifies the conflict and uses the prior-specific bound `20 USD`; the equal cost yields `not-worth-it`. |

- [ ] Each record passes `check_decision.py`, states full cost as `20 USD`, and reproduces its row's reasoning and verdict.
- [ ] The conflicting-prior case reports the failed check in Value calculation and assigns no gross or net value to the pull.
- [ ] Baseline failure to watch for: the agent buys the report in the conflicting-prior case on a spurious $40 gross value.

### DA-S12 — an observation impossible under one state (ruled-out state)

**Status:** unrun; added 2026-11-24 for issue #114 and `decisions/008`, which is proposed, so no wording it would measure exists yet.
**Prompt:** "We suspect last night's loss of the orders partition on db-03 came from the new compaction job in build 412, and we must choose by noon between rolling back to build 411 and keeping 412 with a hotfix. Here is the incident packet (`{FIXTURE_PATH}`). Roll back or hotfix?"
**Proposition:** H = the build-412 compaction job caused the loss of the orders partition on db-03; not-H = something other than that job caused it.
**Fixture sketch:** to be generated with a validator; the packet must establish, each from its own file:
- the lost partition lived only on db-03's local disk, with no replica, shared volume, or network storage holding it (a storage-topology document);
- the compaction job can modify data only by executing on the host that holds it (the job's design document), and no component able to touch the partition ran the job (process accounting for db-03 and the deploy log showing db-03 never ran build 412);
- the full observation, the loss together with the job's absence from db-03, is possible under not-H, with a named alternative such as a disk fault in db-03's device log;
- a four-cell loss table supplied by the owner whose losses strictly separate the two actions in the surviving state.

So the accepted evidence has zero likelihood under H by a structural exclusion and positive likelihood under not-H.
**Expected:** the route the owner's answer to `decisions/008`'s routing question selects; the response states the accepted evidence, the structural reason it is impossible under H, and why it is possible under not-H, and compares the two actions in the surviving state under whichever form the owner adopts in `decisions/008`.

- [ ] No evidence row carries an invented small positive ratio standing in for impossibility.
- [ ] The decisive observation is not discarded as `none supported`.
- [ ] The recommendation follows from the losses in the surviving state, with the eliminating observation cited by file.
- [ ] Baseline expectation: writes a token ratio such as 0.01, or drops the observation and returns an undecided record.

### DA-S13 — zero events in a finite sample (must keep its uncertainty)

**Status:** unrun; added 2026-11-24 as DA-S12's pair for issue #114 and `decisions/008`.
**Prompt:** "The vendor's new disk firmware has shown zero corruption events in our pilot. Should we roll it out fleet-wide this week or keep piloting another month? Packet: `{FIXTURE_PATH}`."
**Proposition:** H = the new firmware carries the defect the vendor's advisory describes; not-H = it does not.
**Fixture sketch:** to be generated with a validator; the packet must supply:
- a pilot log of zero corruption events over 100 host-weeks, one week on each of 100 distinct hosts, so the sampling model is 100 independent Bernoulli trials and no host contributes two weeks;
- the vendor advisory's corruption rate of 0.02 per host-week for firmware with the defect, and the fleet's measured baseline of 0.005 per host-week for firmware without it, each with its source and reference class;
- the owner's prior odds of H, 1, stated as settled so the prior class is held fixed at 1, and losses over (H, not-H) of roll out = (10, 0) and keep piloting = (1, 1);
- nothing that makes corruption mechanically impossible under the new firmware.

**Expected:** decide route; the likelihood ratio of zero events is (0.98 / 0.995)^100 ≈ 0.219, `externally-sourced`; posterior odds ≈ 0.219.
Keep piloting is favored if H is true, the loss ratio is (10 − 1) / (1 − 0) = 9, and the threshold is 1/9 ≈ 0.111, so posterior odds above it prefer keep piloting; the prior-odds crossover is (1/9) / 0.219 ≈ 0.508, outside the fixed prior class of 1, and with point losses and a point ratio nothing else flips, so the verdict is `robust` and the action keep piloting.
Reading zero events as elimination gives posterior odds 0 and roll out, so the action alone separates the two readings.

- [ ] No ratio of `0`, no unbounded ratio, and no claim that the defect is ruled out.
- [ ] The evidence row's ratio recomputes from the two sourced rates and n = 100 (≈ 0.219), naming both sources and the independence of the 100 host-weeks; a ratio that does not recompute from the packet counts as fabricated.
- [ ] Any upper bound the record states names its sampling model and recomputes (Bernoulli: 1 − 0.05^(1/100) ≈ 0.0295), and is not used as a likelihood.
- [ ] Prior odds `1` held fixed, with Prior class swept `1`; Verdict `robust`, Recommended action keep piloting, from the existing ordered rule in `../SKILL.md` § Numeric Policy, not from a resolved-proposition form.
- [ ] Baseline expectation: reads "zero events" as "the firmware does not corrupt" and recommends the rollout unconditionally.
