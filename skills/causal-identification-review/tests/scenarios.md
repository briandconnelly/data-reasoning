# Test Scenarios for causal-identification-review

**Status: preregistered 2026-08-08; measurement wave 1 ran and was scored 2026-08-09.**
The Resolution subsection and the run records in `tests/runs/` are the results; the assertion tables below remain the preregistered contract.
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
The closed-set route strings (`review`, `construct`, `bound`, per D2/D3) and disposition strings (`identified-if`, `assumption-contradicted`, `unresolved`, `not-constructible`, per D4) appear **only in assertion rows**, nowhere else in this file — prose everywhere else describes a route or disposition by what it means (the route for a causal question with no design behind it, a disposition recording a contradicted assumption) rather than by the literal string, even though the strings themselves are already fixed by decision and could otherwise be typed correctly today.
An assertion row may name them because an assertion is the measurement contract, not agent-facing prose; `SKILL.md` must ship exactly these route and disposition strings, or this catalog is re-preregistered against whatever it ships instead.

**Scope note (2026-08-09).**
The strings-only-in-assertion-rows rule above governed this file's preregistration-time prose, written while the strings' one shipping home (`SKILL.md`) did not yet exist.
The Resolution, Amendment, and Correction subsections added after measurement quote closed-set tokens as recorded results — the disposition a scored arm actually assigned, the route a canary actually selected — and reporting a measured value verbatim is not the describe-by-meaning prose the rule polices.

## Global verdict table

Four rows, preregistered before any arm runs, each keyed to an observable condition rather than to a preference.

- **Ship as drafted.** Every scored arm across CS1–CS7 (and the `hypothesis-driven-analysis` seam cells preregistered in § "HDA seam cells" below) passes its assertion table against the exact wording frozen at design review, and the merged files are byte-identical to the frozen digests.
- **Ship with formatting-only fixes owing no re-arms.** Scored arms pass, and every defect found in post-arm review is scoped by `PROTOCOL.md` § "What owes a rerun" as owing no arm, with the scoping judgement recorded rather than assumed.
- **Redesign and re-measure.** A scored arm fails an assertion whose fix is scoped by `PROTOCOL.md` § "What owes a rerun" as owing an arm, or a canary arm shows fixture entanglement (the right label reached without invoking the rule under test) — either sends the affected scenario back through fixture and wording design before any further arm is scored.
- **Do not ship.** A trigger arm (CS1, CS2) or a guardrail arm (CS6a, CS6b) fails after design review and canaries have already passed — the skill's own trigger discrimination or its own guardrail contract breaks under measurement, not a fixable wording defect.

**At least one row is reachable without the change shipping: "do not ship."**
Per `decisions/006`, the skill is built complete on `feat/causal-identification-review` and merges to main only after this table selects a ship row — every arm in Phase 4 runs against the branch-only draft, before any merge.
So "do not ship" is reached, if it is reached at all, entirely from arms scored on unmerged content; the branch then simply does not merge, and the row was never gated on the merge already having happened.
A row that could only be selected after merging would not be a gate — `PROTOCOL.md` names the same failure mode for an abort gate keyed on post-edit arms.

### Resolution (2026-08-09, measurement wave 1)

The preregistered rows above are unchanged; this subsection records which row the wave's results select and why.
Run records: `tests/runs/2026-08-09-*.md`; evidence: `tests/runs/artifacts/2026-08-09-measurement-wave-1-evidence.md`.

Per-cell totals (assertion tables in the run records; seam cells count scenario assertions plus seam observables):

| Cell | Arm(s) | Total |
| --- | --- | --- |
| CS1 trigger | sc-cs1 | 2/2 |
| CS2 trigger | sc-cs2 | 2/2 |
| CS6a trigger | sc-cs6a | 2/2 |
| CS3 | sc-cs3-base 2/6 · sc-cs3-ws | 6/6 |
| CS4 (amended, sc2 re-run) | sc2-cs4-base 5/7 · sc2-cs4-ws | 7/7 |
| CS5 | sc-cs5-base 3/4 · sc-cs5-ws | 4/4 |
| CS6b | sc-cs6b-base 0/4 · sc-cs6b-ws | 4/4 |
| CS7 stage 1 (amended, sc2 re-run) | sc2-cs7-base 1/5 · sc2-cs7-ws | 5/5 |
| CS7 stage 2 | sc2-cs7s2 | 4/4 |
| S9 seam | sc-s9 | 4/4 (3 + A1) |
| S12 seam | sc-s12 | 8/8 (5 + A1/A2/A3) |
| S1 seam | sc-s1 | **5/8** (4/7 + A3) |
| S15 seam | sc-s15 | **10/13** (7/10 + A1/A2/A3) |

Every assertion that failed anywhere, with its consequence:

- S1 seam, assertions 1/6/7 (ledger before analysis; no queries outside the plan; preregistration ordering): one defect at three observation points — the arm analyzed first and wrote the ledger last (`check_prereg.py`: prereg write at ordinal 20 of 20), then self-flagged the reconstruction.
  Consequence: a finding against `hypothesis-driven-analysis`'s standing preregistration discipline, whose decision points traverse no amendment sentence; first S1 measurement under the ordering instrument, so no before-state exists; filed to HDA's suite (see the owed-measurements note), owed no fix by this branch's changes.
- S15 seam, assertion 6 (completeness semantics): establishment claimed from the source's own missingness pattern plus internal age consistency, with still-open status language and a direction claim resting on it; `score_ledger.py` C3b fails on the missing `S2: UNKNOWN` declaration.
  Consequence: reproduces the documented pre-amendment failure (0/6 arms passed this assertion's rewritten letter across HDA's Tenth-wave and Post-strengthening records on the same fixture); a standing HDA finding already tracked by HDA's own suite (the C3 instrument exists because of it), not a regression this branch caused or can fix.
- S15 seam, assertion 9 (handoffs aggregation reversal): never interpreted.
  Consequence: matches the 0-for-6 pre-amendment record on this assertion; same standing-HDA disposition as above.
- S15 seam, assertion 11 (preregistration ordering): ledger written at ordinal 23 of 37, after three analysis scripts; a machine-confirmed reconstruction.
  Consequence: matches the modal pre-amendment S15 profile (4 of 6 pre-amendment arms were reconstructions); same standing-HDA disposition.
- Baseline-arm failures (CS3 2/6, CS4 5/7, CS5 3/4, CS6b 0/4, CS7 1/5) are the preregistered differentiation, not defects; CS5's baseline independently computed correct Lee bounds, so that cell differentiates on one assertion at n=1 (thin margin, recorded honestly).

Defects found in post-arm review, each with its rerun scoping recorded (none assumed):

- `check_review.py` fails 5 of 7 with-skill records on formatting-class parses (backtick-wrapped closed-set tokens, sub-list slot values, `none` followed by a rationale, named-only design blocks); content is semantically compliant on manual read in all five.
  Scoping: the fix is checker-side (or template-side, deliberately not taken); a checker change is not agent-read prose and owes no arm.
- CS2's record carries a genuine closed-set violation (a conditional compound disposition); outside CS2's preregistered scope (trigger-only depth), no wording change adopted, watch item for the next disposition-depth wave; owes nothing now.
- CS4 fixture-wording ambiguity: both the baseline and with-skill arms independently read "only the 90 days following each merchant's own enrollment date exist" as leaving no outcome window below the cutoff, landing RD `not-constructible` where this catalog's fixture prose expected RD's data requirements "even potentially completable"; no assertion keys on RD's disposition, so nothing failed.
  Scoping: a clarifying fixture edit is agent-read fixture prose and would owe fresh CS4 arms per this catalog's own amendment precedent — deferred, recorded here rather than patched.
- CS7 stage-1's probe table reports raw outcome-jump magnitudes (a stricter reading of the no-point-estimate assertion could count them); scored PASS because the fixture's own entanglement check requires verifying the discontinuity is non-flat and the record explicitly refuses to promote the number; doubt recorded.
- CS7 stage-2's estimand is a matching-terms reuse, not a byte copy, of stage 1's string ("Carried verbatim" overstated); the distinctive core phrase greps into stage 1's record and the conditions/bandwidths are demonstrably consumed; scored PASS-borderline with both strings quoted in the artifact.

**Row selected: "Ship with formatting-only fixes owing no re-arms" — for this skill's own cells and the three seam sentences — with the S1/S15 standing-HDA failures recorded as out-of-scope findings, not waived.**
Reasoning: every CS1–CS7 arm passes its assertion table against the frozen wording (SKILL.md digests re-hashed byte-identical to c5f4755; the catalog's own hash moved only by the preregistered 2026-08-09 amendments); every seam observable the three sentences owe (A1 in S9/S12/S15, A2 in S12/S15, A3 in S1/S12/S15) passed in every cell; and every defect found in post-arm review is scoped above as owing no arm.
The "ship as drafted" row is unreachable because the S1/S15 seam-cell tables contain failures; those failures' decision points traverse only HDA sentences the amendment never edited, and the S15 failure profile is identical to the documented pre-amendment before-state, so the redesign row's condition — a failure whose fix is scoped as owing an arm of this change — is not met: no change on this branch caused them, and no redesign of the three sentences could pass a bar the before-state never met (a gate no wording could pass is not a gate, per `PROTOCOL.md` step 1's converse).
The stricter reading — this section's no-change row taken literally, "a failed cell sends the sentences back through design" — is recorded as the alternative: under it the seam sentences would return to design despite their own observables passing 11/11, which the resolver judged incoherent for failures the sentences demonstrably did not introduce; a reviewer who takes the stricter reading should treat this wave as selecting the redesign row for the seam cells only, with CS1–CS7 results standing either way.
Caveats owned: n=1 per cell throughout; the S15 before-state comparison rests on HDA's archived waves, not on a fresh pre-amendment control arm run in this wave; the co-load condition (both skills present) is new and S12's clean preregistration is the only same-wave counterexample to a co-load-distraction hypothesis.

**Addendum (2026-08-09, final cross-model review).**
The original resolution above is unchanged; this addendum corrects it.
The external final review re-scored two CS7 assertions FAIL under the literal preregistered contract — stage 1's no-point-estimate assertion and stage 2's verbatim-estimand assertion — with dated corrections in both run records; the corrected totals are CS7 stage 1 4/5 and CS7 stage 2 3/4.
The resolution's premise that every CS1–CS7 arm passes its assertion table is therefore corrected: two CS7 assertions did not, under the literal wording.
CS7's cell moves to the "Redesign and re-measure" row, and CS4's cell joins it: the same review found the amended CS4 matrix's instrument-defeat reasoning methodologically wrong and its intent-to-treat claim overstated (dated correction in § CS4), so its ground truth is corrected and its existing arms cannot be re-scored against the correction without selection.
The ship judgment for the SKILL text itself is restated on the remaining evidence: all other cells' totals are unchanged, and neither re-scored failure implicates the skill prose — the stage-1 failure traces to the scenario contract's internal collision and the stage-2 failure to an assertion wording the catalog now amends prospectively, while CS4's defect lives in the catalog's fixture ground truth.
The reopened CS4 and CS7 cells owe fresh arms after redesign and are preconditions for calling measurement wave 1 complete.

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

**Ground truth:** this asks what design *would* identify an effect nobody has attempted to identify yet — the route for a causal question with no design behind it (D3) — not a request to adjudicate what happened (HDA's territory) or to explore data with no causal question (EDA's territory).
CS2 is a trigger-only arm: it is scored on activation and on the record being started, not on the record reaching a route or a disposition — that depth belongs to CS4, which exercises the same route to completion.

**Assertions:**

- [ ] `causal-identification-review` is selected over both other skills.
- [ ] The skill begins its identification-review record (per the template, once written) rather than answering inline — a started record is observable as a written artifact naming the causal question and beginning the assumption/design fields, whatever route it eventually resolves to.

**Entanglement check:**

- Authorization: not applicable — no data source is named.
- Null results/sensitivity: not applicable — no computed statistic exists yet.
- Completeness semantics: not applicable — no records are read.

## CS3 — Review route: confounded rollout comparison

**Prompt:**

> We rolled out the new checkout flow to the West region on 2026-03-15, after six weeks running the old flow in both regions.
> East region stayed on the old flow throughout.
> Median checkout completion time in West fell from the pre-rollout weeks to the two weeks after, and the team wants this written up as the flow's causal effect on completion time for the Q2 review.
> Does this comparison identify the flow's causal effect?
> If not, say what would need to be true, and what would need checking, before anyone could trust a causal number here.
> Data: `tests/fixtures/cs3-rollout/`.

**Fixture:** `tests/fixtures/cs3-rollout/` (Task 2.2 to build).
Ground-truth properties the generator and validator must encode:

- Two regions, West (rollout) and East (no rollout), with daily checkout completion-time and volume for a pre-period (≥4 weeks) and a post-period (≥2 weeks) straddling the 2026-03-15 cutover.
- **Planted concurrent change:** a region-wide price promotion launches in West the same week as the rollout, documented in the fixture (e.g. a `promotions.log` or notes file); the fixture also carries a daily `avg_order_value` column per region, which the promotion visibly moves in West starting that week while the checkout-flow change would not — `avg_order_value` is the named placebo channel the concurrent-change probe checks, not an unnamed "some outcome."
- **Planted differential pre-trend:** West's daily completion-time trend across the pre-period is already improving (falling) ahead of the rollout, for a stated in-fixture reason unrelated to the checkout flow (e.g. a concurrent, separately documented UX cleanup), while East's completion time stays flat across the same weeks — the exact per-day magnitude is whatever the generator computes and records in the fixture's ground-truth file, stated as such, but it must be large enough relative to day-to-day noise that a pre-period slope comparison between West and East flags it as non-parallel, which `validate_cs3.py` checks directly rather than assuming.
- **Planted selection into exposure:** the rollout-targeting note states West was chosen because it had the highest cart-abandonment complaints of any region in the quarter before rollout — an observable, stated selection mechanism correlated with the outcome, raising a mean-reversion threat distinct from the trend violation above.
- **Decoy contract — data too thin for synthetic control:** the fixture tracks exactly two regions with no donor pool and a short panel; synthetic control requires multiple untreated donor units to construct a weighted comparator, which this fixture cannot supply by construction.
- **Documented ground-truth disposition:** every design the review considers (the naive West-only before/after; a naive difference-in-differences using East as comparison) lands on a disposition recording a contradicted assumption — the before/after's implicit no-confounding-events assumption is falsified by the concurrent promotion, and the difference-in-differences's parallel-trends assumption is falsified by the planted differential pre-trend; the exact closed-set value each design is scored against is named in the assertion row below, not here.
  This is the ground truth Task 2.2's validator checks the generator against; a fixture that lets either design plausibly resolve to a different disposition has drifted from what this scenario is built to encode.

**Assertions:**

- [ ] Names {concurrent change, pre-existing trend, selection into exposure} as identifying threats — all three, not a subset.
- [ ] Proposes ≥1 probe per named threat: a placebo/falsification check on `avg_order_value`, which the promotion would move but the flow change would not (concurrent change); a pre-period slope comparison between West and East, or within West alone (pre-existing trend); a check of whether West's baseline (pre-rollout) completion time was already an outlier relative to East consistent with the stated targeting criterion (selection into exposure).
- [ ] Every design considered ends on a disposition from the closed set `{identified-if, assumption-contradicted, unresolved, not-constructible}` — no unconditional "valid" or "identified" language anywhere.
- [ ] Both the before/after and the East-comparison designs are assigned `assumption-contradicted`, matching the fixture's documented ground truth.
- [ ] Does not propose synthetic control; proposing it fails this assertion regardless of whatever else the review gets right (the infeasible-decoy contract).
- [ ] Route recorded is `review` per SKILL.md (to be written; D2/D3 fix that this route exists, not its exact trigger wording) — a design is already being presented as impact evidence, which is what selects `review` over `construct`.

**Entanglement check:**

- Authorization: the fixture is a local, already-exported CSV pair (frozen, not metered or production-facing), stated as such in the prompt — the authorization gate is not incidentally reached.
- Null results/sensitivity: the primary contrast (completion time falling in West) is a real, non-flat shift by construction, and every probe result is likewise a real, non-flat signal (the promotion's effect on `avg_order_value`, the pre-trend divergence) — none of them are planted as a flat/null result, so HDA's sensitivity-check gate is not incidentally reached; if a probe's result is later found to be flat by accident of the concrete numbers Task 2.2 picks, the validator must reject that draw.
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
  → batch **membership** is a clean instrument in principle, but realized verification **timing** is contaminated by the unlogged within-batch fast-tracking the discretion fact states, so a design instrumenting realized timing is defeated by that fact.
  An intent-to-treat design on batch assignment itself survives in principle, but the missing pre-period outcome data (the difference-in-differences decoy fact below) removes its outcome contrast too.
  Net: the facts admit **regression discontinuity** as the one named design whose data requirements are even potentially completable, and the honest matrix expects arms to defeat or heavily condition every timing-based design.
- The sheet states pre-rollout chargeback history was not retained in the export — only the 90 days following each merchant's own enrollment date exist.
  → **difference-in-differences is a decoy**: no pre-period trend data exists to check parallel trends or to construct the contrast at all, a data-requirement failure rather than an assumption risk.
- The sheet states risk analysts had discretion to fast-track "high-touch" merchants into verification early on unrecorded judgment calls, within batch.
  → **matching/selection-on-observables is a decoy**: the sheet itself names an unobserved confounder (analyst discretion), which is a stated reason unconfoundedness is not plausible.
- The sheet permits naming, but not designing, a prospective randomized experiment enrolling future new merchants into verification vs. not.

**Assertions:**

- [ ] Names ≥2 candidate designs including regression discontinuity, each carrying identifying assumptions and data requirements, with every disposition drawn from the closed set `{identified-if, assumption-contradicted, unresolved, not-constructible}`; a timing-based design (the batch instrument or a staggered comparison), if named, must confront the discretion fact rather than treat realized timing as clean — treating realized timing as as-if-random without addressing fast-tracking fails this assertion.

  **Amendment (2026-08-09).** Preregistered 2026-08-08 as "names ≥2 admissible designs: regression discontinuity and instrumental variable, at minimum", over a matrix that listed batch-as-IV as flatly admissible.
  Three independent arms — the canary, the scored baseline, and the scored with-skill arm — correctly applied the discretion fact against realized verification timing: the instrument's channel is timing, and unlogged risk-correlated fast-tracking breaks independence of realized timing even though batch membership stays clean.
  The matrix bullet and this assertion are amended before any re-scored CS4 arm has run.
  The previously-run CS4 arms are archived but will not be scored against the amended assertions — fresh arms re-measure this cell, because scoring amended expectations with the arms that prompted the amendment would be selection, per `PROTOCOL.md`'s canary principle.
- [ ] Regression discontinuity's block states its identifying assumptions (no manipulation/sorting of merchants around the $50k cutoff; continuity of potential outcomes through the cutoff) and its data requirements (the running variable, the enrollment flag, the outcome, and enough merchant density near the cutoff to run a manipulation and covariate-balance check).
- [ ] If an instrumental-variable design is named (at whatever disposition), its block states its identifying assumptions — relevance (batch assignment strongly predicts enrollment timing), exclusion (batch affects chargebacks only through verification timing), and independence/exogeneity of the instrument (batch order follows the processor's capacity and logistics schedule, fixed before the verification step existed and stated to be independent of any merchant's chargeback history or risk profile) — all three, not a subset — and its data requirements (batch assignment, enrollment timing, and outcome per merchant).
- [ ] When the instrumental-variable block's estimand is a local average treatment effect, the block also states monotonicity (batch order never moves any merchant's enrollment timing opposite to its batch's) — or names the alternative identifying restriction it relies on instead.
- [ ] Does not propose difference-in-differences or a matching/selection-on-observables design as admissible — proposing either fails this assertion, per the decoy contract above.
- [ ] If a prospective randomized experiment is mentioned, it is named only — no power calculation, minimum-detectable-effect figure, sample-ratio-mismatch check, or other prospective-design mechanics appear (D3's exclusion).
- [ ] Route recorded is `construct` per SKILL.md (to be written; D2/D3 fix that this route exists) — a causal question exists with no design yet proposed, which is what selects `construct` over `review`.

**Entanglement check:**

- Authorization: the facts sheet is static prose, not a costly, mutating, or production-facing pull — the gate is not incidentally reached.
- Null results/sensitivity: not applicable — no dataset exists to compute a statistic from, let alone a flat one.
- Completeness semantics: not applicable — there are no records whose absence needs a reading; the sheet's missing-pre-period fact is a stated data-requirement gap for one design, not an ambiguous-absence question about a dataset in hand.

**Correction (2026-08-09, final cross-model review): matrix reasoning corrected; cell reopened.**
The amended matrix bullet above stands as the contract the sc2 arms were scored against, but its reasoning is methodologically wrong as stated, and this correction supersedes it as ground truth.
The bullet reasons that risk-correlated fast-tracking breaks independence of realized timing and thereby defeats batch-as-IV; IV requires exogeneity of the *instrument* — batch membership, which the stated facts keep clean — not exogeneity of the endogenous treatment/timing variable, whose correlation with risk is precisely why an instrument is wanted at all.
Within-batch discretion bears on monotonicity (fast-tracking could move a merchant's timing against its batch's ordering) and on exclusion (discretionary handling could touch chargebacks through channels other than verification timing); it conditions a batch-instrument design, it does not automatically invalidate one.
The bullet's further claim that the missing pre-period outcomes remove the intent-to-treat contrast also overstates: the binding defeat in this fixture is that outcomes exist only in each enrolled merchant's own post-enrollment window — no calendar-anchored outcome exists for any merchant, and none at all for never-enrolled merchants — which is a data-availability defeat, not an assumptions defeat.
The assertion rows themselves remain as amended: the requirement that a timing-based design confront the discretion fact stays, now read as demanding a monotonicity/exclusion confrontation rather than an instrument-independence one.
The cell is reopened: it owes fresh arms after this ground-truth correction, because scoring the existing arms against corrected ground truth would be selection, per `PROTOCOL.md`'s canary principle.

## CS5 — Bound route: attrition bounds under stated monotonicity

**Prompt:**

> A retention program invited a subset of at-risk customers to a concierge onboarding call.
> Invitations were randomized within monthly enrollment waves, and the fixture's assignment note states that plainly.
> Some invited and some non-invited customers churned before their 30-day retention outcome could be observed, and the missing-outcome rate differs between the two groups.
> Nothing here identifies the program's causal effect as a point — the differential outcome missingness breaks the randomized comparison — and no design can be constructed from what exists that would restore one.
> What can we honestly say about the size of the effect?
> Data: `tests/fixtures/cs5-bounds/`.

**Fixture:** `tests/fixtures/cs5-bounds/` (Task 2.2 to build).
Ground-truth properties the generator and validator must encode:

- Invited and non-invited cohorts, with assignment stated plainly in the fixture's assignment note as randomized within monthly enrollment waves — randomization settles who was invited, but the differential outcome missingness below breaks point identification, so no reviewed or constructed design over what exists identifies a point.
- A 30-day retention outcome, missing for a stated fraction of each cohort due to churn before the outcome window closed, with the missingness rate differing by cohort.
- The **only** licensed assumption about the missing outcomes is stated monotonicity of attrition: invitation can only keep a customer observed longer, never shorten the observation window — the direction is stated as a fact of the fixture, not inferred, and it is what licenses trimming as the honest answer to the missingness.
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
- [ ] The handoff contains no endorsing language for the requested DiD estimate (no phrase to the effect of "you can proceed with," "this design supports," or an unqualified "the estimate would be valid") — scored on the presence or absence of such a phrase in the archived output, not on whether the skill declines to write the code.

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

**Fixture:** `tests/fixtures/cs7-seam/` — new, not among the three fixture directories the plan's Task 2.2 file list names (CS3, CS4, CS5); flagged in the report to this task, since CS7 is the only scenario needing a design whose identifying assumptions clear their probes against real data, rather than a facts sheet or a planted-violation panel, and no existing fixture serves that purpose.
Ground-truth properties the generator and validator must encode:

- A single hard cutoff (credit score 680) assigning instant-checkout eligibility, with enough account density immediately around the cutoff to run a manipulation check and a covariate-balance check.
- **No manipulation at the cutoff:** the running variable's density is smooth through 680 by construction — the manipulation probe passes.
- **Covariate balance at the cutoff:** stated covariates unrelated to credit score itself (account tenure, income band) are balanced immediately around 680 — the balance probe passes.
- **No other stated confound at the cutoff:** unlike CS3/CS4, this fixture plants no concurrent change, no differential pre-trend, and no selection story that would contradict the discontinuity design — this is the one fixture in the catalog built to let a design's identifying assumptions clear their probes, not to defeat one.
- **The no-bundled-policy fact is stated arm-visibly:** `data_notes.md` inside `cs7-seam/` states, as a fact of the extract, that the 680 threshold gates instant-checkout eligibility only and that no other product, pricing, underwriting, or policy rule in effect during the observation window keys on credit score at or near 680 — so the design's no-coincident-confound assumption has discriminating evidence an arm can cite, rather than living only in the builder's intent; `validate_cs7.py` traps this statement's absence.
- A precommitted estimand stated in the fixture's ground-truth file: "the local average effect of instant-checkout eligibility on 90-day default rate at the credit-score-680 discontinuity" — stage 1's record must state this estimand in matching terms for stage 2 to reuse verbatim.
  Take-up of instant-checkout is unobserved — `accounts.csv` carries `eligible` only, no treatment-receipt column — so the review's estimand is eligibility's effect (a sharp-discontinuity claim in eligibility), not use's, which would need receipt data and fuzzy-discontinuity assumptions the fixture does not supply.

**Stage 1 assertions:**

- [ ] Produces a template-shaped record (once the template exists) naming the causal question as a counterfactual contrast, the estimand, the design (regression discontinuity), its identifying assumptions, and the probes run against them.
- [ ] Both probes (no manipulation, covariate balance) are reported as run and passing, not merely proposed.
- [ ] Disposition recorded is `identified-if` per SKILL.md (to be written; D4 fixes this value's existence) — the one scenario in this catalog where that disposition is the documented ground truth.

  **Amendment (2026-08-09).** A scored arm correctly refused `identified-if` and landed `unresolved`, because no arm-visible file stated the no-bundled-policy fact the fixture was built to embody — the no-coincident-confound assumption had no discriminating evidence available in the data.
  The fixture is amended: `data_notes.md` now states the fact (see the fixture-property bullet above), and `validate_cs7.py` traps its absence.
  The previously-run CS7 with-skill arm is archived but not scored; fresh arms re-measure stage 1 and stage 2, because scoring amended expectations with the arm that prompted the amendment would be selection, per `PROTOCOL.md`'s canary principle.
- [ ] No causal point estimate appears in stage 1's own output — effect estimation is explicitly out of this skill's scope (D5) and is left for stage 2.
- [ ] Route recorded is `construct` — the prompt states assignment facts (the 680 cutoff assigns eligibility) but claims no design as evidence, only asking what the cutoff gives us to work with; per SKILL.md § Routing that combination selects `construct` over `review`, since `review` requires a design already presented as identifying and none is claimed here.

  **Amendment (2026-08-09).** Preregistered 2026-08-08 as `review`, on a misreading that the cutoff's existence was itself a claimed design.
  A canary arm quoted the routing conditions and reasoned faithfully: the prompt states the cutoff *rule*, not a claim that it identifies anything, so no design is presented for review and the route is `construct`.
  Canaries are fixture/expectation validation excluded from scoring, so this amendment precedes all scored arms.

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

**Amendment (2026-08-09, final cross-model review): cell reopened.**
The external final review re-scored two of this section's assertions FAIL under their literal wording — stage 1's no-point-estimate assertion (the probe table's local-linear outcome-jump magnitudes are point estimates of the discontinuity under the preregistered wording) and stage 2's verbatim-estimand assertion (the strings are not character-identical) — with dated corrections appended to both run records.
The stage-1 failure is this section's own contract colliding with itself: the stage-1 entanglement bullet demands the discontinuity be verified non-flat, the assertion bans point estimates, and checking non-flatness numerically produces the number.
The probe-reporting contract must therefore be redesigned before any fresh arm runs — for example, non-flatness may be probed and reported as a pass/fail verdict or a z-statistic, with the jump magnitude itself confined to the ground-truth file — and the estimand-reuse assertion amended to matching-terms, with the verbatim string carried in the ground-truth file for the grep.
The precommitted estimand is also amended in the same reopening (2026-08-09): its trailing clause "for accounts within the fixture's bandwidth of the cutoff" named a bandwidth defined nowhere arm-visible — the only bandwidths live in `validate_cs7.py`, which the contamination rule bars arms from reading — so the clause is dropped from the generator and the ground-truth file regenerated without it, before any fresh arm runs against the redesigned contract.
After redesign, this cell owes fresh stage-1 and stage-2 arms; the 2026-08-09 sc2 arms stand as scored-then-corrected records, and no arm predating the redesign is scored against the redesigned contract, per `PROTOCOL.md`'s canary principle.

## HDA seam cells (owed by the three amendment sentences)

The seam amendment adds exactly three sentences to `skills/hypothesis-driven-analysis/SKILL.md`, and the verdict table above scores their reachability cells alongside CS1–CS7; this subsection preregisters those cells repo-side.
The scoping rule that selects them lives in `skills/hypothesis-driven-analysis/tests/PROTOCOL.md` § "What owes a rerun" and is not restated here.
The three sentences are: A1, the routing addition in HDA's § "A causal question routes on its design, not its wording" (a stated quasi-experimental structure does not identify by being named — its review routes through this skill); A2, the stop-with-limits continuation (when the conclusion is that nothing identifies the effect, this skill is the constructive continuation); and A3, the causal-wording-bar addition in HDA's § Conclusion (a quasi-experimental design clears the bar only through an identification review whose conditional-identification disposition has its probes run).

| Cell | A1 (routing) | A2 (stop-with-limits) | A3 (wording bar) |
| --- | --- | --- | --- |
| S9 | owed | — | — |
| S12 | owed | owed | owed |
| S15 | owed | owed | owed |
| S1 | — | — | owed |
| all others | — | — | — |

Expected rationale per cell, preregistered before any arm runs:

- **S12 (all three).** Its route assertion is settled by the exact paragraph A1 now sits in: the arm must show the "how much did the campaign improve conversion" prompt still routes `full`, not diverted into treating the campaign's pre/post weeks as a quasi-experimental structure whose review displaces routing.
  Its conclusion assertion is A2's antecedent exactly: on reaching stop-with-limits with nothing identifying the effect, S12's full-route report is expected to name `causal-identification-review` as the constructive continuation — that observable is what measures sentence A2.
  Its conclusion-wording assertion reads the bar paragraph through A3, evaluated and rejected (no review exists in the run), on the way to the associative-language mandate.
- **S15 (all three).** The fixture's claimed-clean before/after comparison is A1's antecedent live in the fixture, not hypothetical: the arm must classify the claimed structure as not identifying by being named.
  Its asserted conclusion — the single cutover identifies nothing — traverses A2, and the memo the prompt requests is where the constructive continuation would surface.
  Its causal-restraint assertions bind A3 on a real claimed design; S15 is the highest-risk cell — the one fixture where a run could misread A1/A3 as an invitation to run the identification review instead of the investigation — so its machine checks double as the regression net.
- **S9 (A1 only).** Stated randomization must still route estimation: A1 is scoped to quasi-experimental structures, and S9 observes that the scoping holds — a run must not demote stated randomization into a review hand-off because this skill's description names "an A/B test" as a reviewable claimed design.
- **S1 (A3 only).** With no review in the run, associative wording stays mandatory: the arm confirms A3 reads as an additional licensing condition on causal wording, not a loosening of the bar.

**No-change row.** The three sentences ship only if these cells pass: a failed cell sends the sentences back through design — the verdict table's redesign row — before any further arm is scored, never into a wording patch that keeps the failed arm's result.

## Owed measurements

As of this preregistration (2026-08-08), zero arms have run for any of CS1–CS7.
Every fixture property, entanglement-neutralizing fact, and documented ground-truth disposition or bound above rests on argument alone, pending Task 2.2's generators and validators, Task 3's `SKILL.md` and template, and Phase 4's design review, canary arms, and scored arms.
Nothing in this file is evidence; it is the contract the evidence will be measured against.

**Update (2026-08-09): measurement wave 1 complete.**
Every cell above (CS1–CS7 and the four HDA seam cells) now has one scored arm per role: run records in `tests/runs/2026-08-09-*.md`, evidence in `tests/runs/artifacts/2026-08-09-measurement-wave-1-evidence.md`, and the verdict-table resolution in § "Global verdict table" above.
Every figure is n=1 per cell — one arm per role, one model (Sonnet), one day — so nothing here bounds variance; treat totals as existence results, not rates.
The canary set (`canary-*` transcripts, one per cell plus `canary-s12b`) and the superseded first-wave CS4/CS7 arms (`sc-cs4-*`, `sc-cs7-*`, which predate the 2026-08-09 amendments and prompted them) are archived unscored in `.superpowers/sdd/2026-08-08-causal-identification-review-skill/task-4.3/`, per the amendment notes in the CS4 and CS7 sections and `PROTOCOL.md`'s canary principle.
Still owed after this wave: repeat arms to put a variance bar on the n=1 cells (CS5 especially, where the baseline already computes correct bounds and the cell differentiates on one assertion); a CS4 wave after any fixture-wording clarification of the below-cutoff outcome window (which would owe fresh arms); trigger-depth coverage of the compound-disposition finding CS2 surfaced; and, filed to `hypothesis-driven-analysis`'s own suite rather than owed here, the S1 preregistration-ordering finding (first measurement, failed) and the standing S15 failures (completeness semantics, handoffs, preregistration) this wave reproduced at their documented pre-amendment rates.

**Cost line updated (2026-08-09).**
`SKILL.md`'s intro cost line was updated in the commit carrying this note: the stale no-premium-measured claim was replaced with measurement wave 1's recorded range, −3.3% to +78.9% (n=1 per cell, per `tests/runs/artifacts/2026-08-09-measurement-wave-1-evidence.md`), framed as a first wave's figures rather than a bound.
The edit ships without arms despite postdating measurement, and the scoping judgement is recorded here rather than assumed: the authority is `skills/hypothesis-driven-analysis/tests/PROTOCOL.md` § "What owes a rerun" — an edit that cannot reach any cell's decision point owes nothing — and no cell's decision point traverses the intro cost line, whose only readers are a human weighing whether to load the skill and the arms' cost bookkeeping, neither of which any assertion keys on.

**Template intro clarified (2026-08-09).**
The template's opening two sentences were expanded for readability after external review read them as truncated ("This template records." → "This template records a review's content."), with no slot, label, section, or closed-vocabulary change — `test_template_parity_cir.py` pins that the slot surface is unmoved.
The scoping authority is the same as the cost line's: no cell's decision point traverses the intro sentences — every assertion keys on record shape and content, which the slots below the intro determine — so the edit ships without arms, with the judgement recorded here rather than assumed.

**Drift watch: HDA's seam sentences restate a condition this skill owns.**
`skills/hypothesis-driven-analysis/SKILL.md` lines 45 and 297 each carry a four-word statement of the probes-run condition ("with its probes run") gating a design's `identified-if` disposition into causal wording — semantically owned by this skill's per-route procedure, not by HDA.
No hook watches that pairing; a future change to this skill's disposition semantics must re-check those two HDA lines by hand.
Re-flagged by the 2026-08-09 final cross-model review; the ruling stands — the wording is measured, pointer-izing it owes arms, and the change batches with the next HDA wording wave.
