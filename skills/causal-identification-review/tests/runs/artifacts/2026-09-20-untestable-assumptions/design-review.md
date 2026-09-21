# Cross-model design review: untestable-assumptions wave (issue #40)

Reviewer: Codex, through amicus, read-only on this repository.
The dispatching session (Fable) wrote the draft, verified each finding before acting on it, and records here what it did with each.
Three paid calls were budgeted for the whole task: issue selection, this review, and one repeat.

## Issue selection (call 1, before any design)

Codex was given the eleven open issue titles and asked which fix most improves the correctness of conclusions a data agent hands to a person.
It ranked #40 first, #39 second, #41 third, and named the strongest argument against its own pick: the skill is already non-certifying, so the harm needs a downstream over-read, while #39 sits on a busier path.
The session had independently ranked #39 first, on traffic.
It adopted #40 after checking Codex's citations against the text: the defect is a contradiction a faithful arm cannot escape and not an omission, one horn of it is in the archive (the prereg's step 0), and the favorable disposition gates causal wording in two other skills.
The disagreement on traffic was not resolved and is not claimed to be; #39 stays the close second.

## Pass 1 — on commit `b0ec13b`, before any arm

Verdict: do not run the arms yet.
Shipped-skill diff against `main` at that commit: `SKILL.md` +16 −5, `references/identification-review-template.md` +8 −6, nothing else outside `tests/`.

| # | Finding | Class | Verified how | Disposition |
| --- | --- | --- | --- | --- |
| 1.1 | Exclusion is not untestable in the fixture: with a randomized binary invitation, binary enrollment, and a count outcome, the instrument's inequality restrictions are observable, and the shipped data satisfies them, so the honest record is a clean joint probe, not an absent one | blocking | The session had computed the same restrictions on `customers.csv` while the review ran, and found every retained cell non-negative | Taken. The ground truth now allows two sound records for exclusion; `SKILL.md` says a check that tests several assumptions jointly is a probe of each, and lists an instrument's inequality restrictions among the examples; validator trap 8 requires the restrictions to hold and was seen to fire on a planted direct effect of the email. The cell no longer claims a strictly untestable assumption — almost nothing is — and measures the two failures the issue names instead |
| 1.2 | Enrollment "as of day 90" overlaps the outcome window, so treatment timing is undefined to an arm and the design could fairly end before its assumptions are reached | blocking | Read `data_notes.md` against the generator: the generator orders them, the notes did not | Taken. Enrollment is fixed on 2026-03-16 and the outcome window opens that day; the validator requires both sentences |
| 1.3 | The assertions let a post arm call a testable assumption untestable and still land the favorable row; monotonicity is in the ground truth and in no assertion | blocking | Read against the prereg's own at-risk line, which conceded it | Taken. CS8.3 requires the feedable probes run with results; CS8.2 takes monotonicity on the CS4 precedent (or the alternative restriction); a wave-level rule says the favorable row is earned on the whole cell |
| 1.4 | The checker accepts `not run` in the probe cell under a favorable assessment | blocking | Reproduced: no findings on that record | Fixed test-first (`test_a_probe_cell_saying_not_run_cannot_carry_a_run_assessment`) |
| 1.5 | Duplicate ids collapse; inline assumptions without ids pass; bold ids are rejected; an alternate header is rejected | should-fix | Reproduced the first and third; read the code for the second | First three fixed test-first. The header is schema, not formatting: `assumption` and `assessment` are the template's column names, and a table without them does not bind the gates, which the favorable disposition then fails on |
| 1.6 | The checker's one-directional disposition gate has no home in `SKILL.md`, whose precedence list is keyed on assessments alone | should-fix | Read both | Taken, against the session's first instinct. Its first fix — a threat-register clause under the could-not-discriminate value — was traced through CS8 before shipping and would have stranded the design again, since a direct effect of the email is a registered threat with no discriminating probe. `SKILL.md` now says a threat bears on the disposition through the assumption it threatens, and the checker's gate is bidirectional |
| 1.7 | "Every probe the data in hand can feed is run" is unbounded, invites specification search, and reads past the gates; the forward reference to a family of checks narrows the search to the examples | should-fix | Read | Taken. A probe is a check of something the assumption implies about data the gates already permit; probes are named before any is run and a later one says so; the list of examples says it is not a census; the untestable value owes the checks considered and why each is silent, which is what a reader contests |
| 1.8 | The template line "One row per assumption id" paraphrases a rule; the prereg paraphrases others; HDA lines 45 and 319 still say "with its probes run" | should-fix | Read | Template line made pointer-only. The prereg describes a diff for a reader deciding which cells reach it, which is not a second home for a rule an agent follows. The HDA lines are left under the catalog's standing ruling, and the reviewer's position — that the branch should not ship until they are pointer-ized and their seam arms run — is recorded as an open disagreement for the owner, not settled here |
| 1.9 | CS8.3 as drafted would fail an arm that runs the inequality check, and a keyword scorer could fail "consistent with randomization" | should-fix | Read | Taken: CS8.4 names the three silent checks, carries the safe-harbor sentence, and passes the inequality check by name |
| 1.10 | "What would the number be conditional on?" half-asks for the number | should-fix | Read | Taken: the prompt asks on what assumptions a downstream estimate would be conditional and says not to estimate |
| 1.11 | The new clause under the could-not-discriminate value does not move CS3, because the contradicted value precedes it | note | Read the precedence list and the CS3 ground truth | Agreed; CS3 and CS6b stay as regression cells |

Claims in the review not independently verified: the two Pearl-inequality sums it reports (0.852 and 0.452), and its reading that the single negative cell it found sits at an outcome value of 9, in the tail the validator's 1% mass floor leaves out.
Neither decides anything above.

## Pass 2 — on commit `6e0a9f7`, before any arm

Verdict: no-go for the canary.
This was the third and last budgeted call, so its findings were applied without a further pass; what that leaves unreviewed is stated at the end.

| # | Finding | Class | Verified how | Disposition |
| --- | --- | --- | --- | --- |
| 2.1 | The revised `SKILL.md` says an assumption with an observable implication owes its probe and names an instrument's inequality restrictions as one, so the second record the ground truth allowed for exclusion — untestable, probe absent — is wrong under the post wording, and a post arm could pass CS8.5 while violating its own text | blocking | The session had put this exact question to the reviewer, suspecting it. Read both texts: they disagree | Taken, by redesigning the fixture and not by weakening the wording. Enrollment now reaches the extract only as counts by invitation arm, privacy rules barring a customer-level link. The first stage, the balance checks, and the ratio the analyst proposes are all still computable; the joint distribution the inequality restrictions need is not. Exclusion is untestable in fact, the ground truth is single again, and text and ground truth agree |
| 2.2 | Validator trap 8 dropped outcome values under 1% of customers, hiding one cell (outcome value 9, one customer) where an inequality is negative, while the ground truth said the restrictions hold "for every outcome value" | blocking | Read trap 8 and the ground-truth sentence: the truncation was stated in the file but not arm-visible, and a careful arm on the full support could fairly report a contradiction | Moot after 2.1: no customer-level enrollment, no restrictions to compute, trap 8 removed. Recorded because the session wrote that trap an hour earlier and chose the mass floor to make it pass |
| 2.3 | The assessment gates were skipped for any block without an assessment column unless it ended on the favorable disposition, and for every block ending on the cannot-be-built disposition, an exception the checker had invented | should-fix | Reproduced on an old three-column table under the could-not-discriminate disposition: no findings | Fixed test-first. Every Design block owes the template's four columns in order, except one ending on the cannot-be-built disposition, and that exception now has its home in `SKILL.md`'s data-requirements sentence. Three legacy tests migrated: probes proposed and not run are `not-run` rows, not an inline `none run` |
| 2.4 | An assumption cell with trailing text was read as its id; a table missing the probe column passed | should-fix | Reproduced both | Fixed test-first: the id cell is full-matched, the header is compared to the four column names in order |
| 2.5 | HDA lines 45 and 319 still say "with its probes run", which the new semantics make divergent and not merely duplicated | should-fix | Read | Not taken in this wave, and the reviewer's position is recorded as standing: editing those lines owes HDA seam arms under the catalog's ruling. The session's reading is that the phrase remains true — every probe the review named was run, and an assumption with none is carried as a condition HDA line 319 already says the causal wording carries. The owner settles it; the wave-level rules say this wording does not merge until they have |
| 2.6 | Naming probes before running any is scoreable from the archived tool-call order and is not scored | note | Read | Recorded for the canary's rationale read; decides no row |
| 2.7 | The checker's module docstring still called the disposition gate one-directional | note | Read | Fixed |

The reviewer also confirmed, tracing CS3 and CS6b through the revised text, that neither documented ground truth moves: a contradicted assessment takes precedence whatever the selection-into-exposure row says.

## Pass 3 — on commit `9c2a366`, before any arm (a fourth call, approved by the owner)

Verdict: no-go for the canary.

| # | Finding | Class | Verified how | Disposition |
| --- | --- | --- | --- | --- |
| 3.1 | By-arm enrollment still leaves exclusion an observable implication: the arms' outcome distributions can differ by no more than the share whose enrollment the invitation moves, and monotonicity implies the sign of the first stage. So the single untestable ground truth is wrong again, and CS8.4, CS8.5, and CS8.8 would fail a correct arm | blocking | The session computed the same bound while the pass ran: total-variation distance 0.0790 against a first stage of 0.3040, the figure the generator now records | Taken, and not by a fourth fixture. Three designs in a row left the assumption some weak implication, which is the finding: strict untestability almost never survives the presence of outcome data. The wording no longer depends on it — an implication the review can name owes its probe, however weak, and a bound only a large violation would break is a probe assessed with that blind spot named. The ground truth allows two sound records; validator trap 7 keeps the bound clean and was seen to fire on a planted direct effect. The reviewer argued in pass 2 that reading the untestable value as "the review found nothing" lets ignorance pass; the session's answer is that the value's row owes the checks considered and why each is silent, which is what a reader contests, and that a skill cannot demand a partial-identification literature of its reader — it can demand that silence not be filed as evidence |
| 3.2 | CS8.6 and CS8.7 required only exclusion downstream, so an arm could name monotonicity and drop it | blocking | Read against the ground truth, which conditions on both | Taken: both assertions require exclusion and, for an effect among compliers, monotonicity or its named alternative |
| 3.3 | On `main`, a sophisticated arm can satisfy the every-assumption-a-probe sentence with the weak bound and reach the conditional disposition, so the cell may no longer separate the wordings | blocking as part of 3.1 | Reasoned from `main`'s text; no arm has run | Accepted as a reachable row, not designed away. It also narrows issue #40's textual claim: the sentence is escapable by an arm that knows a bound, and the live failures are the two the archive and the issue name — a silent check filed as support, and a design stranded for want of a probe |

The reviewer found no further checker-shape conflict, and confirmed the disposition is unique and the design constructible.

## Pass 4 — on commit `6db1d3c`, before any arm (a fifth call, asked for by the owner)

The first attempt ended in 52 seconds on the reviewer's usage limit and produced nothing; this is the retry.
Verdict: no-go for the canary.
The reviewer accepted the two-record ground truth and the reading of the untestable value as the review's own contestable finding ("this makes ignorance auditable but does not prevent it"); what it blocked on is narrower than in any earlier pass.

| # | Finding | Class | Verified how | Disposition |
| --- | --- | --- | --- | --- |
| 4.1 | The text never says which assessment a weak bound gets, and the could-not-have-come-back value is defined by sensitivity, so an arm can defensibly call the 0.079-against-0.304 bound that, which the precedence list turns into the stranded disposition — against the ground truth | blocking | The session had put this exact case to the reviewer. Read the two definitions: the reading is fair | Taken, close to the reviewer's wording: a weak probe some obtainable result would have contradicted is not contradicted when its result is not that one, its reach being the blind spot the row names; the could-not-have-come-back value is for a check the data leave with no contradicting result |
| 4.2 | The threat-register sentence requires every threat to carry a probe run, while the untestable value allows none; CS8's direct-effect threat has no probe | blocking | Read `SKILL.md` and the template's threat row | Taken: the sentence allows `NONE` with why no probe exists, and the template's cells say the same |
| 4.3 | CS8.5 and CS8.8 checked exclusion only, so monotonicity could be marked clean on the placebo; and the untestable value's row owes the data that would make the assumption testable, which no assertion asked for | blocking | Read the assertions against `SKILL.md`'s definition | Taken: both assertions cover exclusion and monotonicity, CS8.5 requires the data that would make it testable, and placebo, balance, or the first stage's size offered for either assumption fails |
| 4.4 | The total-variation bound follows from independence, exclusion, and monotonicity together, not from exclusion alone; the generator's docstring said so and the ground truth, catalog, and prereg did not | blocking | Checked the derivation: without monotonicity the first stage is compliers net of defiers and bounds nothing | Taken in all three, and CS8.5 scores a bound record only when it states what the bound follows from |
| 4.5 | The canary rule still required exclusion assessed as untestable, and an entanglement bullet still said no assertion keys on monotonicity | blocking | Read | Taken: the canary accepts either record and is read for the weak-probe and silent-check distinction; the bullet is rewritten |
| 4.6 | "However weak" needs a floor, or a vacuous bound earns the one clean row the favorable disposition needs | should-fix | Read against the rule that at least one assumption be not contradicted | Taken: a bound no obtainable result could violate is a silent check, not a probe |
| 4.7 | `validate_cs8.py`'s docstrings and one helper name still claimed strict untestability | should-fix | Read | Taken |

## The reviewer's recommendation on the wave itself

Asked whether the wave is still worth running as designed, the reviewer said no: a knowledgeable arm on `main` is now expected to pass, so one pre arm against one post arm on a pass-everything comparison cannot tell the wording change from domain knowledge.
It offered two routes.
Ship the clarification unmeasured, at the owner's call, after the blockers are fixed, and keep CS8 as a regression scenario.
Or, if behavior is to be measured, preregister the primary endpoint as the two errors the issue names — a silent diagnostic credited to exclusion, or the stranded disposition chosen only because no exclusion probe was known — and run repeated independent pre and post arms, not one of each.
The session agrees with the diagnosis and leaves the choice to the owner: the second route is a larger spend than the wave preregistered here, and the prereg's row 5 already says an unmeasured clarification is the owner's call.

## The owner's rulings, 2026-09-20

On the wave: the reviewer's first route.
The wording ships as an unmeasured clarification and CS8 as a regression scenario, with no arm run (`../../../../decisions/007-assessments-ship-unmeasured.md`).

On finding 2.5: `hypothesis-driven-analysis/SKILL.md` lines 45 and 319 stay as they are and the change merges.
The phrase is read as still true — every probe the review named was run, and an assumption with none is carried as a condition — and pointer-izing both lines is filed for the next HDA wording wave, where the seam arms can batch (issue #49).
The reviewer's contrary position stands recorded above; it was not argued away.

## After the PR: monotonicity, settled by a second reviewer and a reversal

Copilot's second review of PR #50 objected that the ground truth named the first-stage sign as something monotonicity implies and still allowed the untestable record for it.
The session defended the two-record rule on the PR, on the ground that the untestable value is the review's own finding, which pass 4 had accepted.
Asked the sharper form of the objection in a sixth, single-question call, the cross-model reviewer reversed its pass-4 recommendation and said what it had missed: CS8.3 already has every passing record run the first stage, and the procedure says a check that bears on several assumptions is a probe of each, so an arm with the first stage in hand cannot fairly record that it found nothing monotonicity implies.
A negative first stage is obtainable and would contradict it, so the sign is a weak probe and not a silent check; its blind spot is any defier share smaller than the complier share.
The session was wrong on the PR and says so there.
CS8.5 and CS8.8 now allow monotonicity one record and exclusion two, and the ground-truth file carries the principle that separates them: a check every passing record must already run is a probe of every assumption an obtainable result of it would contradict, while an implication needing a separate derivation no assertion requires may stay outside a documented untestable finding.
No `SKILL.md` sentence changed; the result follows from the text as it stood.

## What no cross-model pass has read

The pass-4 dispositions above.
PROTOCOL step 3 asks for the design review before any arm; four passes ran and each ended no-go, and the owner then took the reviewer's first route, so none will run under this preregistration.
No arm has run.
