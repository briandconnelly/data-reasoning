# Preregistration: 2026-09-20 untestable-assumptions wave (issue #40)

Written before any arm ran, and revised three times before any arm ran, on the three passes of the cross-model design review recorded in `2026-09-20-untestable-assumptions/design-review.md`; the first draft is commit `b0ec13b`.
This is the `skills/hypothesis-driven-analysis/tests/PROTOCOL.md` step 1 artifact for every cell below; the step 0 check, the step 2 entanglement pass, the step 3 review pointer, and the step 4 canary rule are recorded here too, so the scored runs can point at one document.
Harness, isolation, archive layout, and the per-cell verdict rows are those of `skills/hypothesis-driven-analysis/tests/runs/artifacts/2026-09-20-cheap-route-validity-prereg.md` (§ Arms, § Per-cell verdict table), reused by pointer and not restated; this wave's archive is `2026-09-20-untestable-assumptions/`, its prompts are under `prompts/` there, and `run_wave.sh` there runs one arm.

## Step 0 — does the reported failure exist?

Issue #40 makes a textual claim and a behavioral one.

The textual claim was re-derived from `main` at `5f4bf69`, not taken from the issue.
`SKILL.md` § Per-route procedure says every named assumption gets a probe that could come back against it, defines the one favorable disposition as carrying "the probes supporting each", and says that disposition "is earned by probes run and reported".
The remaining three dispositions are a broken assumption, probes that "could not discriminate", and unmet data requirements.
An assumption no obtainable result could come back against therefore has no record that is both faithful to the text and favorable: the design is stranded on the could-not-discriminate value, or some check is filed beside the assumption to fill its row.
The instrument was checked against a known positive: the same read finds the could-not-discriminate value's definition, which is the nearest thing the text has to the missing state, and it speaks of "the probes run", not of an assumption no probe exists for.

The behavioral claim has two horns, and the archive settles one of them once.
Stranding is observed: `../../scenarios.md` § CS7, Amendment 2026-08-09, records that a scored arm "correctly refused" the favorable disposition and landed on the could-not-discriminate value "because no arm-visible file stated the no-bundled-policy fact", the no-coincident-confound assumption having "no discriminating evidence available in the data".
The remedy then was a fact added to the fixture, not a state added to the skill, so the path is still open on `main`.
That is one arm on one fixture, an existence result.
The second horn — a diagnostic that is silent on an assumption recorded as evidence for it — is not in the archive: the tracked run records were searched for `placebo`, `negative control`, and `support` beside an untestable assumption and show no instance, and the transcripts themselves are untracked (`../../scenarios.md` § "What this repository cannot re-score"), so the archive cannot rule it in or out.
The issue says as much: "inferred from the text, not observed in an arm."
So the pre arms measure both horns without the change existing, and row 5 is the verdict if they show neither.

## What changes, and which cells reach it

| Change | File and section | Cells that reach it | Cells that do not |
| --- | --- | --- | --- |
| Every assumption carries an id and one probes-table row with a closed-set assessment; the five assessment values and their meanings; a check silent on an assumption is not a probe of it; the untestable value is a finding to defend | `SKILL.md` § Per-route procedure, replacing the every-assumption-gets-a-probe sentence — the rule's single home | CS8 (new); CS3 and CS6b (`review`, Design blocks over `cs3-rollout`); CS4 and CS7 stage 1 (`construct`, Design blocks) | CS1, CS2, CS6a: trigger cells scored on activation, which the description decides and this change does not touch. CS5: `bound` carries no Design block and no probes table. CS7 stage 2 and the four HDA seam cells: they run `hypothesis-driven-analysis`, whose text this wave does not edit |
| The disposition list states its precedence, keys each value on the assessments, and drops "with the probes supporting each"; an untestable assumption neither blocks nor counts toward the favorable value and is carried by name | `SKILL.md` § Per-route procedure, the disposition list and the paragraph after it | the same cells | the same cells |
| `A<n>:` assumption placeholders; the probes table gains an `assessment` column and an `evidence or reason` column; a pointer line to `SKILL.md` for the value set | `references/identification-review-template.md` | the same cells | the same cells |
| Assessment gates | `tests/check_review.py`, with `tests/test_check_review.py` | none: an instrument no arm reads, covered by its unit suite and owing no arm | — |

`hypothesis-driven-analysis/SKILL.md` lines 45 and 319 gate causal wording on a review ending on the favorable disposition "with its probes run".
They are not edited.
The phrase stays true of the new semantics — every probe the review named was run, and an assumption with none is carried as a condition — and the catalog's standing ruling (`../../scenarios.md` § Owed measurements, Drift watch) is that pointer-izing those lines owes HDA seam arms and batches with the next HDA wording wave.
The hand re-check that ruling asks for was done for this change and is recorded here: an untestable assumption reaches HDA through the Handoff block's Assumptions slot, which HDA line 319 already says "the causal wording then carries as conditions".

CS4 and CS7 stage 1 reach the edited text and cannot run in this wave.
Both are reopened cells whose contracts the catalog says must be redesigned before any fresh arm (`../../scenarios.md` § CS4 Correction, § CS7 Amendment of the final cross-model review).
They are recorded as owed against this wording, not waived: a measured result belongs to the exact wording it was measured against, so their redesign wave measures them against whatever text stands then.

The post arm stages the whole working-tree skill, so attribution needs the shipped skill directory to differ from `main` in these edits and no others; `git diff --stat main -- skills/causal-identification-review ':!skills/causal-identification-review/tests'` is recorded in the design-review file before the canary and again in the run record.

## Arms

- **baseline** — no skill. CS8 only: whether the skill is needed on the cell at all.
- **pre** — the skill at `main` (`--skill-ref main`, `5f4bf69`). The control for the changed text.
- **post** — the skill in this working tree.

Attribution is pre versus post on the added assertions.
CS3 and CS6b run pre and post only: they exist here to detect a regression.
Model `sonnet` on every arm, resolved model recorded per arm.

## Cells

| Cell | Route | Fixture | Eligibility | Added assertions |
| --- | --- | --- | --- | --- |
| CS8 | review | `cs8-encouragement/` (new, validated by `fixtures/validate_cs8.py`) | CS8.1 | CS8.2–CS8.7; CS8.8 recorded for post only |
| CS3 | review | `cs3-rollout/` | the catalog's CS3 assertions | — |
| CS6b | review | `cs3-rollout/` | the catalog's CS6b assertions | — |

Ground truth for CS8 is `fixtures/cs8-encouragement-ground-truth.md`, generated from the realized data at seed `20260802`, the first seed counting up from `20260801` to clear every validator trap after the placebo and reduced-form floors were tightened; the floors were fixed before the search.
An invitation assigned at random to 3000 of 6000 customers moves enrollment by 0.304 (z = 27.2); prior-period late payments, tenure, and plan are balanced across it (prior-period difference −0.023, 95% interval −0.085 to +0.038); the reduced form is not flat (z = −6.6).
So relevance and independence each have a probe the extract can feed, and each comes back clean.
Enrollment is fixed on 2026-03-16 and the outcome window opens that day, so treatment precedes outcome and the design is constructible.
Exclusion has one weak bound and nothing else.
Enrollment is held in the billing system and reaches the extract only as counts by invitation arm (`enrollment_by_arm.csv`), privacy rules barring a customer-level link to payment history; so the joint distribution of invitation, enrollment, and outcome, which an instrument's inequality restrictions need, cannot be formed, while the first stage and the ratio the analyst proposes still can.
What the extract does leave is a bound: if the invitation reaches late payments only through enrollment, the two arms' outcome distributions differ by no more than the share whose enrollment it moves. The distance is 0.079 against a first stage of 0.304 (validator trap 7, seen to fire on a planted direct effect), so the bound holds with room and only a very large violation could break it.
Every customer was eligible, so no subgroup exists in which the invitation cannot move enrollment; who opened the email is unrecorded; and the prior-period placebo is balanced by randomization alone whatever the email does after it is sent, so it is silent on exclusion.
Monotonicity's only observable implication is the sign of the first stage.
The ground-truth file therefore allows two sound records for each of the two assumptions — not contradicted by the bound with its blind spot named, or not testable here with the checks considered and why each is silent — and one disposition.
A review is not required to know the bound; it is required not to mistake the placebo for a probe.
Three fixtures in a row were found, in design review, to leave exclusion some weak observable implication; the wording was changed to stop depending on strict untestability, which almost nothing has, and the history is in the design-review file.
The analyst's note plants the overread: the placebo "confirms the instrument is clean, so the IV estimate is the causal effect of autopay".

Assertions, each a single check on archived output, worded so an arm on either wording can pass or fail them:

- **CS8.1** — the record's route is `review`, and it carries a Design block for the invitation-as-instrument design.
- **CS8.2** — that block names relevance, independence of the invitation, and the exclusion restriction, all three, each as a claim evidence could break; and when its estimand is an effect among compliers it also names monotonicity, or the alternative restriction it relies on instead.
- **CS8.3** — the probes the extract plainly feeds were run and reported with results: a first stage for relevance, and a balance or prior-period check for independence. Either assumption recorded as untestable, or its probe proposed and not run, fails.
- **CS8.4** — the prior-period placebo, the balance checks, and the first stage are nowhere given as evidence for the exclusion restriction, in a probes-table row or in a sentence. "The placebo is consistent with randomization and says nothing about exclusion" passes. A bound the exclusion restriction does imply — the two arms' outcome distributions differing by no more than the share whose enrollment the invitation moves — is a probe of it and passes here.
- **CS8.5** — exclusion's evidential state is one of the two the ground-truth file allows: not testable from this extract, with the checks considered and why each is silent; or not contradicted by a bound it implies, with what that bound cannot see named. A statement that any check supports, confirms, or establishes exclusion fails.
- **CS8.6** — the instrument design's disposition is `identified-if`, and the conditions stated with it include exclusion and, when the estimand is an effect among compliers, monotonicity or the alternative restriction named in its place. `unresolved` or `not-constructible` fails; so does `identified-if` with either condition absent.
- **CS8.7** — the Handoff block's Assumptions slot carries the same conditions CS8.6 requires, as conditions on any downstream estimate.
- **CS8.8** — post only, recorded, decides no row: `check_review.py` exits 0 on the record, and the exclusion row reads either probe `NONE` with assessment `not-testable-here`, or a named bound with assessment `not-contradicted`.

The baseline is scored on CS8.3, CS8.4, CS8.5, and the report-level reading of CS8.6 (identification stated as conditional on exclusion, neither refused nor unconditional); it writes no template record, so CS8.1, CS8.2's block, and CS8.7 do not apply to it.

## Expected outcomes

- CS8 baseline: corrects the analyst, says exclusion is an untestable assumption, and calls the estimate conditional on it. Skill needed on this cell: probably no, on the report-level assertions.
- CS8 pre (the reviewer's pass-3 point, accepted): a sophisticated arm on `main` can meet the every-assumption-a-probe sentence with the weak bound and reach the conditional disposition, passing everything — row 5, reachable without the change.
  The more likely pre arm names all three assumptions, runs the first stage and the balance checks, then either lands `unresolved` because exclusion has no probe (fails CS8.6 — the CS7 stranding), or files the placebo in exclusion's row to complete the table (fails CS8.4).
  At-risk: pre writes "untestable" in the result cell and assigns `identified-if` anyway, passing everything — row 5, and a fair result: the text's literal reading did not bind the arm.
- CS8 post: exclusion and monotonicity either `not-testable-here` with probe `NONE` and the placebo named as a check considered and found silent, or `not-contradicted` by the bound each implies; relevance and independence `not-contradicted`; disposition `identified-if` with both conditions named, carried into Handoff.
  At-risk: post treats the untestable value as an exit and assigns it to independence without running the balance check (fails CS8.3, row 7); post lands `unresolved` out of caution the new precedence does not ask for (fails CS8.6, row 7).
- CS3, CS6b: post passes every catalog assertion pre passes, both designs still ending on the contradicted-assumption value.
  At-risk: the new `unresolved` clause or the restated precedence moves a CS3 design off its documented disposition (row 3); the longer procedure displaces a threat from the register (row 3).

## Wave-level rules, decided here and not after the arms

- Nothing ships from a partial wave: every cell ends on a terminal row of the reused verdict table before any text ships.
- The wording and template ship as measured if CS8 lands on row 6 and neither CS3 nor CS6b lands on row 3.
- If CS8 lands on row 5, nothing ships as measured: the fixture, the catalog entry, the checker, and this finding ship, and the text is the owner's call as an unmeasured clarification of a contradiction the text does contain. **This row is reachable without the change existing.**
- If CS3 or CS6b lands on row 3, the text is revised once and all three cells are remeasured against the exact revised text.
- The favorable row is earned on the whole cell: CS8 lands on row 6 only if post passes CS8.2 through CS8.7, so an arm that reaches the conditional disposition by calling a testable assumption untestable is row 7, not row 6.
- A CS8 row 7 revises the text once and remeasures CS8; a second row 7 drops it.
- The checker's assessment gates are coupled to the template: they ship only with it, because a record written from `main`'s template cannot satisfy them under the favorable disposition.
- No arm runs until a design-review pass has read the wave as it stands and said go; all three passes so far ended no-go (`2026-09-20-untestable-assumptions/design-review.md`).
- The wording does not merge until the owner has settled the open disagreement over `hypothesis-driven-analysis/SKILL.md` lines 45 and 319 recorded there (finding 2.5).
- Whatever ships, CS4 and CS7 stage 1 stay owed against it, and the catalog says so.
- Baseline results are recorded as "skill needed on this cell: yes/no" and decide nothing about the text.

## Entanglement pass (PROTOCOL step 2)

- **Null-result sensitivity (HDA § Data).** The placebo is a null, which is the shape that gate reads, and the cell needs it to be settled ground rather than a contested null. The validator requires its 95% interval to contain 0, to be narrower than ±0.08 late payments on a mean near 1.1, and to sit within one standard error of 0; n = 6000. The reduced form is required non-flat (|z| ≥ 4) so no arm is detoured into arguing whether there is an effect to identify.
- **The CS7 collision.** CS7 stage 1 banned point estimates while requiring a non-flatness check that produces one. CS8 asserts nothing about numbers. `check_review.py`'s advisory numeric scan may warn on them; it is advisory and decides nothing.
- **Completeness semantics.** `data_notes.md` states the extract complete with every field populated, so no absent-record reading is live.
- **Authorization and costly collection.** A frozen local export, stated as such in the prompt; both gates quiet.
- **Route.** The analyst presents a design as identifying, which selects `review`; the question asks what the number would be conditional on, not for the number, so the estimation boundary CS6b probes is not reached.
- **A testable exclusion by accident.** The validator fails the fixture if `customers.csv` gains any column beyond the six named (an enrollment, eligibility, open, or segment column would make exclusion testable), if `data_notes.md` loses the all-eligible or no-open-record sentence, or if either note uses the words `exclusion`, `direct effect`, `reminder`, `due date`, or `late fee`. The email body is quoted in full and speaks only of how to enroll, so an arm can reason about a direct channel and cannot settle one.
- **No customer-level enrollment.** `customers.csv` has no enrollment column and the validator fails the fixture if it gains one, so neither a comparison within the unenrolled nor the inequality restrictions can be computed; `data_notes.md` says the link cannot be requested either, so the costly-collection and authorization gates are not the reason the probe is absent.
- **Treatment timing.** `data_notes.md` fixes enrollment on 2026-03-16 and opens the outcome window that day; the validator requires both sentences. Without them the data-requirements check, which precedes assumptions, could fairly end the design before the cell's question is reached.
- **The estimation boundary.** The prompt asks which assumptions a downstream estimate would be conditional on and says not to estimate. Probe statistics — a first-stage difference, a balance difference — are evidence about assumptions and may appear.
- **Monotonicity.** Untestable here as well. No assertion keys on it, so an arm that omits it, or states the estimand as the intent-to-treat effect of the invitation in a second Design block, loses nothing; the ground-truth file records it so a scorer does not read its appearance as an error.

## Canary rule (PROTOCOL step 4)

One post arm (`canary-cs8-post`) runs first and is scored on rationale: did it assess exclusion as untestable because it read and applied the changed text, and did it run the probes the data could feed rather than reaching for the untestable value?
A canary that reaches the right record without traversing the changed text means the fixture is entangled — back to step 2.
The canary is excluded from the scored table; the scored arms run fresh.

## Cross-model design review (PROTOCOL step 3)

Codex reviews this document, the fixture with its generator and validator, the prompts, the draft wording, and the checker together, before any arm runs.
Its findings and their dispositions go in `2026-09-20-untestable-assumptions/design-review.md`.
Issue selection was itself a cross-model step and is recorded there: Codex ranked #40 first and the dispatching session had ranked #39 first, on traffic; the session adopted #40 because the defect is a contradiction a faithful arm cannot escape, one horn of it is in the archive, and its `identified-if` output gates causal wording in two other skills.
