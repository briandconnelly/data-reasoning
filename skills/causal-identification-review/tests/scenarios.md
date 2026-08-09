# Test Scenarios for causal-identification-review

**Status: preregistered only — no arm has run, and nothing below is a result.**
This catalog is written before `SKILL.md` exists, per `decisions/006` and the Iron Law, whose single home is `skills/hypothesis-driven-analysis/tests/PROTOCOL.md`.
`../decisions/` records the calls settled by argument (naming, authority map with `hypothesis-driven-analysis`, scope, dispositions, numeric policy, branch discipline); this file records the calls settled by a run.

## Methodology

This catalog follows the baseline/with-skill methodology defined in `skills/hypothesis-driven-analysis/tests/scenarios.md` (header) and ordered by `skills/hypothesis-driven-analysis/tests/PROTOCOL.md`, which is the Iron Law's single home and is not restated here.
What follows states only what differs for this skill; everything else (scoring as pass/fail with an evidence pointer, evidence-archiving under `tests/runs/artifacts/`, the rule that an assertion the with-skill run misses is a finding against the skill and not the agent, the rule that a baseline already satisfying every assertion means the scenario is too easy except where noted otherwise) carries over from that header unchanged.

**Three-skill catalog.**
Every trigger and guardrail scenario (CS1, CS2, CS6a) loads all three skills' descriptions — `hypothesis-driven-analysis`, `exploratory-data-analysis`, and `causal-identification-review` — because the failure under test is collision between all three, and a catalog missing one of them cannot show it.

**Which scenarios have a baseline.**
CS1, CS2, and CS6a are trigger scenarios: one run each, scored on which skill and route activates and on the stated reason, with no baseline/treatment split, per HDA's "Trigger" step.
A passing baseline is not a defect for these three (CS6a in particular expects the passing baseline as its result) — this mirrors HDA's S2/S3 convention, not this skill's route-selection convention, because CS1/CS2/CS6a test selection among skills, not among this skill's own routes.
CS3, CS4, CS5, and CS6b are ordinary baseline/with-skill pairs.
CS7 is two-stage: stage 1 gets a baseline (an agent without the skill, scored against the stage-1 assertions, expected to fail to produce a template-shaped record with a run disposition) and a with-skill arm; stage 2 has no baseline, because a baseline stage 1 produces no record shaped well enough to hand to anything, and stage 2 exists to test whether a downstream consumer reads a real record, not to test what happens with none.

**Run-record naming.**
Store each scored output as `tests/runs/YYYY-MM-DD-csN-<variant>.md`, where `<variant>` is `baseline`, `with-skill`, or `trigger`.
CS7's with-skill arm produces two files, `...-with-skill-stage1.md` and `...-with-skill-stage2.md`; its baseline arm produces one, `...-baseline-stage1.md`.
Re-runs append a second suffix (`-rerun`, `-corrected`, `-hardened`) and say in the file which earlier run it supersedes and why, per HDA's convention.
Create `tests/runs/` and `tests/runs/artifacts/` if a fresh checkout of this skill lacks them; git does not track empty directories.

**Contamination rule.**
With-skill and baseline subagents alike may read the skill files (once written) and the one fixture directory named in their scenario prompt.
They may never read this file (`tests/scenarios.md`) or anything under `tests/runs/` — the assertions, dispositions, and prior scored outputs would contaminate the run.

**Unwritten skill content.**
`SKILL.md` does not exist yet.
Where a scenario below references routing precedence, non-goal wording, or per-route procedure beyond the values fixed by decision, the value is marked `per SKILL.md (to be written)` and cites the decision record that fixed its existence — `002` for the HDA seam, `003` for scope, `004` for dispositions, `005` for numeric policy.
Assertion rows are the one exception: they may name the closed-set values the plan already fixed — routes `review`, `construct`, `bound` (D2/D3) and per-design dispositions `identified-if`, `assumption-contradicted`, `unresolved`, `not-constructible` (D4) — because an assertion is the measurement contract, not agent-facing prose.
`SKILL.md` must ship exactly these route and disposition strings, or this catalog is re-preregistered against whatever it ships instead.

## Global verdict table

Four rows, preregistered before any arm runs, each keyed to an observable condition rather than to a preference.

- **Ship as drafted.** Every scored arm across CS1–CS7 (and the `hypothesis-driven-analysis` reachability cells from the seam amendment) passes its assertion table against the exact wording frozen at design review, and the merged files are byte-identical to the frozen digests.
- **Ship with formatting-only fixes owing no re-arms.** Scored arms pass, and every defect found in post-arm review is scoped by `PROTOCOL.md` § "What owes a rerun" as owing no arm, with the scoping judgement recorded rather than assumed.
- **Redesign and re-measure.** A scored arm fails an assertion whose fix touches a sentence a cell's decision point traverses (owing a rerun by the same rule), or a canary arm shows fixture entanglement (the right label reached without invoking the rule under test) — either sends the affected scenario back through fixture and wording design before any further arm is scored.
- **Do not ship.** A trigger arm (CS1, CS2) or a guardrail arm (CS6a, CS6b) fails after design review and canaries have already passed — the skill's own trigger discrimination or its own guardrail contract breaks under measurement, not a fixable wording defect.

**At least one row is reachable without the change shipping: "do not ship."**
Per `decisions/006`, the skill is built complete on `feat/causal-identification-review` and merges to main only after this table selects a ship row — every arm in Phase 4 runs against the branch-only draft, before any merge.
So "do not ship" is reached, if it is reached at all, entirely from arms scored on unmerged content; the branch then simply does not merge, and the row was never gated on the merge already having happened.
A row that could only be selected after merging would not be a gate — `PROTOCOL.md` names the same failure mode for an abort gate keyed on post-edit arms.

## CS1 — Trigger, negative

**Prompt** (verbatim):

> why did conversion drop after the campaign launch?

**Fixture:** none.
This is a pure routing test, scored on the bare prompt with the three-skill catalog loaded, on the pattern of HDA's own S3 trigger-discrimination scenario, which also carries no fixture directory.

**Ground truth:** this is an explanatory/diagnostic question — no design is proposed or claimed, and rival explanations (campaign composition, a concurrent deploy, a data-validity artifact) have to be told apart — which is squarely `hypothesis-driven-analysis`'s `full` territory per its own routing table (`skills/hypothesis-driven-analysis/SKILL.md` § "A causal question routes on its design"), not this skill's.
`causal-identification-review` enters only once a design is being proposed or reviewed, or once something has already concluded that nothing identifies the effect (D2) — neither is true of this bare prompt.

**Assertions:**

- [ ] `hypothesis-driven-analysis` is selected; `causal-identification-review` does not activate.
- [ ] The stated reason for not selecting `causal-identification-review` names the absence of any proposed or claimed design — not merely "this skill sounds more relevant" — matching the routing distinction above.

**Entanglement check:**

- Authorization: not applicable — the prompt names no data source, so no pull is attempted before routing completes.
- Null results/sensitivity: not applicable — no computed statistic exists yet at the point this scenario is scored.
- Completeness semantics: not applicable — no records are read.

## CS2 — Trigger, positive

**Prompt** (verbatim):

> we can't randomize price changes — how could we ever tell if a price increase causes churn?

**Fixture:** none, for the same reason as CS1.

**Ground truth:** this asks what design *would* identify an effect nobody has attempted to identify yet — the `construct` route's shape (D3) — not a request to adjudicate what happened (HDA's territory) or to explore data with no causal question (EDA's territory).
CS2 is a trigger-only arm: it is scored on activation and on the record being started, not on the record reaching a route or a disposition — that depth belongs to CS4, which exercises `construct` to completion.

**Assertions:**

- [ ] `causal-identification-review` is selected over both other skills.
- [ ] The skill begins its identification-review record (per the template, once written) rather than answering inline — a started record is observable as a written artifact naming the causal question and beginning the assumption/design fields, whatever route it eventually resolves to.

**Entanglement check:**

- Authorization: not applicable — no data source is named.
- Null results/sensitivity: not applicable — no computed statistic exists yet.
- Completeness semantics: not applicable — no records are read.

## CS3 — Review route: confounded rollout comparison

**Prompt:**

> We rolled out the new checkout flow to the West region on 2026-03-15, after two weeks running the old flow in both regions.
> East region stayed on the old flow throughout.
> Median checkout completion time in West fell from the pre-rollout weeks to the two weeks after, and the team wants this written up as the flow's causal effect on completion time for the Q2 review.
> Does this comparison identify the flow's causal effect?
> If not, say what would need to be true, and what would need checking, before anyone could trust a causal number here.
> Data: `tests/fixtures/cs3-rollout/`.

**Fixture:** `tests/fixtures/cs3-rollout/` (Task 2.2 to build).
Ground-truth properties the generator and validator must encode:

- Two regions, West (rollout) and East (no rollout), with daily checkout completion-time and volume for a pre-period (≥4 weeks) and a post-period (≥2 weeks) straddling the 2026-03-15 cutover.
- **Planted concurrent change:** a region-wide price promotion launches in West the same week as the rollout, documented in the fixture (e.g. a `promotions.log` or notes file) and affecting an outcome the checkout-flow change would not — a placebo channel a probe can check (see below).
- **Planted differential pre-trend:** West's daily completion-time trend across the pre-period is already moving at a materially different rate than East's, checkable by comparing pre-period slopes — this is the parallel-trends violation that would defeat a naive difference-in-differences using East as the comparison, not only the raw before/after in West alone.
- **Planted selection into exposure:** the rollout-targeting note states West was chosen because it had the highest cart-abandonment complaints of any region in the quarter before rollout — an observable, stated selection mechanism correlated with the outcome, raising a mean-reversion threat distinct from the trend violation above.
- **Decoy contract — data too thin for synthetic control:** the fixture tracks exactly two regions with no donor pool and a short panel; synthetic control requires multiple untreated donor units to construct a weighted comparator, which this fixture cannot supply by construction.
- **Documented ground-truth disposition:** every design the review considers (the naive West-only before/after; a naive difference-in-differences using East as comparison) lands on `assumption-contradicted` — the before/after's implicit no-confounding-events assumption is falsified by the concurrent promotion, and the difference-in-differences's parallel-trends assumption is falsified by the planted differential pre-trend.
  This is the number Task 2.2's validator checks the generator against; a fixture that lets either design plausibly resolve to `identified-if` or `unresolved` has drifted from what this scenario is built to encode.

**Assertions:**

- [ ] Names {concurrent change, pre-existing trend, selection into exposure} as identifying threats — all three, not a subset.
- [ ] Proposes ≥1 probe per named threat: a placebo/falsification check on an outcome the promotion would move but the flow change would not (concurrent change); a pre-period slope comparison between West and East, or within West alone (pre-existing trend); a check of whether West's baseline (pre-rollout) level was already an outlier relative to East consistent with the stated targeting criterion (selection into exposure).
- [ ] Every design considered ends on a disposition from the closed set `{identified-if, assumption-contradicted, unresolved, not-constructible}` — no unconditional "valid" or "identified" language anywhere.
- [ ] Both the before/after and the East-comparison designs are assigned `assumption-contradicted`, matching the fixture's documented ground truth.
- [ ] Does not propose synthetic control; proposing it fails this assertion regardless of whatever else the review gets right (the infeasible-decoy contract).
- [ ] Route recorded is `review` per SKILL.md (to be written; D2/D3 fix that this route exists, not its exact trigger wording) — a design is already being presented as impact evidence, which is what selects `review` over `construct`.

**Entanglement check:**

- Authorization: the fixture is a local, already-exported CSV pair (frozen, not metered or production-facing), stated as such in the prompt — the authorization gate is not incidentally reached.
- Null results/sensitivity: the primary contrast (completion time falling in West) is a real, non-flat shift by construction, and every probe result is likewise a real, non-flat signal (the promotion's effect on the placebo outcome, the pre-trend divergence) — none of them are planted as a flat/null result, so HDA's sensitivity-check gate is not incidentally reached; if a probe's result is later found to be flat by accident of the concrete numbers Task 2.2 picks, the validator must reject that draw.
- Completeness semantics: the fixture states its extract is complete for both regions across the full window (no missing daily records) — preregistering completeness closes off any inference about absent vs. unrecorded vs. export-incomplete records, which is HDA's territory and not this scenario's.

## CS4 — Construct route: admissible-design matrix over a facts sheet

**Prompt:**

> Our fraud team wants to know whether the new merchant-verification step actually reduces chargebacks, but nothing about how it rolled out looks like a designed experiment.
> Facts about the rollout are in `tests/fixtures/cs4-facts/facts.md` — there is no transaction-level dataset to query, only these facts.
> What would it take to find out?

**Fixture:** `tests/fixtures/cs4-facts/facts.md` (Task 2.2 to build) — a facts sheet, not a dataset, matching the plan's Task 2.2 file list.
Ground-truth facts the sheet must state:

- A hard numeric eligibility cutoff: merchants with lifetime transaction volume ≥ $50,000 are auto-enrolled in verification.
  → admits **regression discontinuity**.
- Enrollment is staged by which processor onboarding batch a merchant was assigned to; the sheet states batch order follows the processor's onboarding capacity and logistics, stated to be independent of any merchant's chargeback history or risk profile.
  → admits **instrumental variable** (batch as instrument for verification-step timing).
- The sheet states pre-rollout chargeback history was not retained in the export — only the 90 days following each merchant's own enrollment date exist.
  → **difference-in-differences is a decoy**: no pre-period trend data exists to check parallel trends or to construct the contrast at all, a data-requirement failure rather than an assumption risk.
- The sheet states risk analysts had discretion to fast-track "high-touch" merchants into verification early on unrecorded judgment calls, within batch.
  → **matching/selection-on-observables is a decoy**: the sheet itself names an unobserved confounder (analyst discretion), which is a stated reason unconfoundedness is not plausible.
- The sheet permits naming, but not designing, a prospective randomized experiment enrolling future new merchants into verification vs. not.

**Assertions:**

- [ ] Names ≥2 admissible designs: regression discontinuity and instrumental variable, at minimum.
- [ ] Regression discontinuity's block states its identifying assumptions (no manipulation/sorting of merchants around the $50k cutoff; continuity of potential outcomes through the cutoff) and its data requirements (the running variable, the enrollment flag, the outcome, and enough merchant density near the cutoff to run a manipulation and covariate-balance check).
- [ ] Instrumental variable's block states its identifying assumptions (relevance — batch assignment strongly predicts enrollment timing; exclusion — batch affects chargebacks only through verification timing, per the sheet's own statement that batch order tracks logistics, not risk) and its data requirements (batch assignment, enrollment timing, and outcome per merchant).
- [ ] Does not propose difference-in-differences or a matching/selection-on-observables design as admissible — proposing either fails this assertion, per the decoy contract above.
- [ ] If a prospective randomized experiment is mentioned, it is named only — no power calculation, minimum-detectable-effect figure, sample-ratio-mismatch check, or other prospective-design mechanics appear (D3's exclusion).
- [ ] Route recorded is `construct` per SKILL.md (to be written; D2/D3 fix that this route exists) — a causal question exists with no design yet proposed, which is what selects `construct` over `review`.

**Entanglement check:**

- Authorization: the facts sheet is static prose, not a costly, mutating, or production-facing pull — the gate is not incidentally reached.
- Null results/sensitivity: not applicable — no dataset exists to compute a statistic from, let alone a flat one.
- Completeness semantics: not applicable — there are no records whose absence needs a reading; the sheet's missing-pre-period fact is a stated data-requirement gap for one design, not an ambiguous-absence question about a dataset in hand.

## CS5 — Bound route: attrition bounds under stated monotonicity

**Prompt:**

> A retention program invited a subset of at-risk customers to a concierge onboarding call.
> Invitation was targeted by an internal risk score that was never exported, so nothing here supports a claim about who would have been invited under any other rule.
> Some invited and some non-invited customers churned before their 30-day retention outcome could be observed, and the missing-outcome rate differs between the two groups.
> Nothing here identifies the program's causal effect, and no design can be constructed from what exists.
> What can we honestly say about the size of the effect?
> Data: `tests/fixtures/cs5-bounds/`.

**Fixture:** `tests/fixtures/cs5-bounds/` (Task 2.2 to build).
Ground-truth properties the generator and validator must encode:

- Invited and non-invited cohorts, assignment stated as targeted by an unrecorded risk score — no cutoff, no instrument, no comparison group whose assignment is stated to be independent of the outcome, so no design in `review` or `construct`'s repertoire identifies a point.
- A 30-day retention outcome, missing for a stated fraction of each cohort due to churn before the outcome window closed, with the missingness rate differing by cohort.
- The **only** licensed assumption is stated monotonicity of attrition: invitation can only keep a customer observed longer, never shorten the observation window — the direction is stated as a fact of the fixture, not inferred.
- **Documented ground-truth bounds:** the generator computes Lee-style trimming bounds — trimming the lower-attrition cohort's outcome distribution to match the higher-attrition cohort's survival rate, from the top and from the bottom, to produce a best-case and worst-case endpoint — and records the exact `[lower, upper]` pair in the fixture's ground-truth file.
  This pair is what `validate_cs5.py` checks a run's computed endpoints against.

**Assertions:**

- [ ] The assumption ledger — the monotonicity direction and the trimming logic it licenses — is written before any endpoint number appears in the record.
- [ ] The computed lower and upper endpoints match the fixture's documented ground-truth bounds (exact match, or within a stated numeric tolerance the validator sets).
- [ ] No causal point estimate appears anywhere in the output — not a naive difference-in-means reported as "the effect," not a midpoint of the bound presented as a best guess; only the interval, framed as a range under the stated assumption.
- [ ] Route recorded is `bound` per SKILL.md (to be written; D3/D5 fix that this route produces real endpoints, not only a plan for endpoints).

**Entanglement check:**

- Authorization: the fixture is a local frozen export, stated as such — not costly, mutating, or production-facing.
- Null results/sensitivity: the bound endpoints are non-degenerate (lower ≠ upper) by construction — the fixture must not accidentally plant equal attrition rates across cohorts, which would collapse the bound to a point and entangle this scenario with HDA's null-result sensitivity gate instead of testing the bound route on its own terms; the validator checks this.
- Completeness semantics: the fixture states the missingness mechanism (early churn before the observation window closed) and its rate per cohort directly, rather than leaving the reader to infer whether a missing outcome means the event didn't happen, wasn't recorded, or the export is incomplete — preregistering the mechanism closes off HDA's three-way completeness question before this scenario's own review has to touch it.

## CS6a — Guardrail: non-activation

**Prompt** (verbatim):

> teach me difference-in-differences

**Fixture:** none.

**Ground truth:** this is a request to teach estimator mechanics, which is the textbook shape D1's naming argument holds this skill apart from, reinforced by D5's rule that effect estimation is this skill's handoff, not its output — the skill must not activate, and whatever answers instead (the base assistant, or neither of the other two skills, since neither's trigger surface covers a methods-teaching request) doing so plainly is the expected result, not a defect.

**Assertions:**

- [ ] `causal-identification-review` does not activate.
- [ ] A passing baseline (the assistant answers the methods question directly, with no skill ceremony) is scored as a pass, per the trigger-scenario convention CS6a shares with HDA's S2/S3 — this is stated explicitly because CS6a is the one scenario in this catalog where "the baseline already satisfies every assertion" is the intended outcome, not a sign the scenario is too easy.

**Entanglement check:**

- Authorization: not applicable — no data source, no skill activates.
- Null results/sensitivity: not applicable.
- Completeness semantics: not applicable.

## CS6b — Guardrail: mixed ask, review in scope and estimation out of it

**Prompt** (verbatim):

> review whether our rollout comparison identifies the effect, and write the DiD estimation code

**Fixture:** reuses `tests/fixtures/cs3-rollout/` (no new fixture) — the same planted concurrent change, differential pre-trend, and selection-into-exposure facts that CS3 exercises, so the review half of this scenario is scored the same way CS3's is, with the DiD-code request layered on top to probe the boundary rather than to re-plant new threats.

**Assertions:**

- [ ] The review is produced: the same threat-naming and probe-proposing content CS3 requires, ending on a disposition from the closed set (`assumption-contradicted`, matching CS3's documented ground truth, since this is the same fixture).
- [ ] No estimator mechanics appear in the skill's own output: no difference-in-differences code, regression formula, or standard-error calculation is emitted by this skill.
- [ ] The handoff is stated explicitly: the response says plainly that estimation code is out of this skill's scope and names `hypothesis-driven-analysis`'s estimation route (or an explicit successor skill, if one is named) as where that work happens — the handoff carries the review's facts, assumptions, and disposition without this skill prescribing which HDA route to take, per D2's authority map.
- [ ] Because this scenario's disposition is `assumption-contradicted` rather than `identified-if`, the handoff does not imply the requested DiD estimate would be trustworthy if produced — the review is not the thing that blocks the code from being written, but it does not license the code either; this line item is scored on the handoff not overstating the design's status, not on the skill refusing on the user's behalf.

**Entanglement check:** identical to CS3's, since the fixture is shared — authorization, null-results/sensitivity, and completeness semantics are neutralized by the same three preregistered facts CS3 states.

## CS7 — Handoff: stage 1 produces a record, stage 2 proves it was read

**Stage 1 prompt:**

> Accounts with a credit score of 680 or higher are auto-approved for the new instant-checkout feature; accounts below 680 go through manual review and are not offered it.
> We want to know instant-checkout's effect on 90-day default rate, and whether the credit-score cutoff gives us anything to work with.
> Data: `tests/fixtures/cs7-seam/`.

**Stage 2 prompt** (dispatched separately, to a subagent with `hypothesis-driven-analysis` loaded and not this skill, handed stage 1's written record verbatim):

> Here is an identification review record for instant-checkout's effect on 90-day default rate.
> [stage 1's full record content]
> Estimate the effect.

**Fixture:** `tests/fixtures/cs7-seam/` — new, not among the three fixture directories the plan's Task 2.2 file list names (CS3, CS4, CS5); flagged in the report to this task, since CS7 is the only scenario needing a design that clears `identified-if` against real data rather than a facts sheet or a planted-violation panel, and no existing fixture serves that purpose.
Ground-truth properties the generator and validator must encode:

- A single hard cutoff (credit score 680) assigning instant-checkout eligibility, with enough account density immediately around the cutoff to run a manipulation check and a covariate-balance check.
- **No manipulation at the cutoff:** the running variable's density is smooth through 680 by construction — the manipulation probe passes.
- **Covariate balance at the cutoff:** stated covariates unrelated to credit score itself (account tenure, income band) are balanced immediately around 680 — the balance probe passes.
- **No other stated confound at the cutoff:** unlike CS3/CS4, this fixture plants no concurrent change, no differential pre-trend, and no selection story that would contradict the discontinuity design — this is the one fixture in the catalog built to let a design clear `identified-if`, not to defeat one.
- A precommitted estimand stated in the fixture's ground-truth file: "the local average treatment effect of instant-checkout on 90-day default rate at the credit-score-680 discontinuity, for accounts within the fixture's bandwidth of the cutoff" — stage 1's record must state this estimand in matching terms for stage 2 to reuse verbatim.

**Stage 1 assertions:**

- [ ] Produces a template-shaped record (once the template exists) naming the causal question as a counterfactual contrast, the estimand, the design (regression discontinuity), its identifying assumptions, and the probes run against them.
- [ ] Both probes (no manipulation, covariate balance) are reported as run and passing, not merely proposed.
- [ ] Disposition recorded is `identified-if` per SKILL.md (to be written; D4 fixes this value's existence) — the one scenario in this catalog where that disposition is the documented ground truth.
- [ ] No causal point estimate appears in stage 1's own output — effect estimation is explicitly out of this skill's scope (D5) and is left for stage 2.
- [ ] Route recorded is `review` — a claimed design (the credit-score cutoff) already exists to be reviewed.

**Stage 2 assertions** (the observables that prove HDA consumed the record, not merely received it):

- [ ] HDA routes `estimation`, not `full` — reachable only if HDA's own routing rule (per the seam amendment, D2, Task 3.4 — `per SKILL.md (to be written)` on this skill's side, `per hypothesis-driven-analysis/SKILL.md (to be amended)` on HDA's) treats an `identified-if` disposition with its probes run as license to skip the unidentified-causal branch.
- [ ] The estimand HDA states matches stage 1's estimand string, reused verbatim rather than re-derived or restated in different terms — quoted from stage 1's archived record and grepped against it, per the citation discipline `PROTOCOL.md` step 6 describes.
- [ ] The identifying assumptions stage 1 named (no manipulation, covariate balance) appear in HDA's limitations section as the conditions the estimate is conditional on — not silently dropped, not replaced with a weaker set HDA invents on its own.
- [ ] HDA's output reports the estimate with an uncertainty statement, per its own estimation-route contract — this is HDA's existing rule, cited rather than restated here.

**Entanglement check (stage 1):**

- Authorization: the fixture is a local frozen export — not costly, mutating, or production-facing.
- Null results/sensitivity: the discontinuity's effect at the cutoff is a real, non-flat signal by construction, so it does not incidentally reach HDA's sensitivity-check gate; the validator checks this is not accidentally flat.
- Completeness semantics: the fixture states its extract is complete with no missing account records — preregistered, so no absent-record ambiguity reaches this scenario.

**Entanglement check (stage 2):**

This stage is not incidental entanglement — HDA's estimation-route gates (authorization, uncertainty reporting) apply because stage 2 genuinely runs HDA, not because the fixture accidentally tripped them.
The assertions above test that HDA's own machinery engages normally with a handed-in record, not that this skill's fixture avoided a gate that does not belong to it.

## Owed measurements

As of this preregistration (2026-08-08), zero arms have run for any of CS1–CS7.
Every fixture property, entanglement-neutralizing fact, and documented ground-truth disposition or bound above rests on argument alone, pending Task 2.2's generators and validators, Task 3's `SKILL.md` and template, and Phase 4's design review, canary arms, and scored arms.
Nothing in this file is evidence; it is the contract the evidence will be measured against.
