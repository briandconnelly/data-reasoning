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

## What no cross-model pass has read

The fixture redesign in 2.1, the assertions as they stand after it (CS8.4, CS8.5, CS8.8), and the checker changes in 2.3 and 2.4.
PROTOCOL step 3 asks for the design review before any arm; two passes ran and each ended no-go, so by the protocol's own reading no arm should run until a pass reads the redesign and says go.
No arm has run.
