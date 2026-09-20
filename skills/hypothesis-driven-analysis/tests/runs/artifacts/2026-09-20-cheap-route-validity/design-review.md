# Cross-model design review — 2026-09-20 cheap-route data-validity wave

PROTOCOL step 3, run before any arm.
Reviewer: Codex (`codex-cli 0.155.1`, reasoning effort high), through `amicus_consult_async`, job `85389b460e1b43aca6c352f314c9de9c`, read-only over the working tree.
Reviewed together: the first draft of `../2026-09-20-cheap-route-validity-prereg.md`, the prompts, `fixtures/generate_s22.py`, `validate_s22.py`, `test_validate_s22.py` and the CSVs, the harness, and the draft wording in `SKILL.md` and `references/ledger-template.md`.
Verdict: **do not run the arms yet.**
Every finding was checked against the files it cites before it was acted on; the dispositions below are the dispatching session's.

## Findings and dispositions

| # | Rank | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | blocking | `b-truncated` was justified by evidence the governing rule rejects: the draft said the row cap and the mid-morning stop are "enough to call the export incomplete", while § Analysis says a source's own missingness pattern can never establish its completeness. The validator's projection was described as a lower bound; it is one compatible completion. | **Accepted.** Verified against § Analysis. The packet's rationale is now two compatible completions under `UNKNOWN` completeness semantics, in the prereg, the generator docstring, the validator docstring and comment, and the catalog entry. The fixture bytes did not change. Not taken: failing an arm for calling the export "apparently truncated" — that is a reason to doubt, honestly stated; S22b.4 fails only a settled claim that the export is complete. |
| 2 | blocking | Verdict precedence could credit a cell that never took the route it measures (rows 4/5 sat above the shared-catalog-failure row and did not require the route assertion), and the wave-level rule allowed shipping with a void or fixture-defect cell outstanding. No row for an added-assertion failure the text does not address. | **Accepted.** The route assertion is now an eligibility condition on pre and post for rows 5–7; added row 4 (off-target) and row 8 (unaddressed failure); nothing ships from a partial wave. |
| 3 | blocking | The join rule was scoped to `mini` and `direct` only, though `full` and `estimation` fan out the same way, and its prescribed check was not generally valid ("a repeated key inflates a total": fact-side repeats are legitimate, negative measures need not inflate, an inner join can drop and repeat rows at once and leave the count unchanged). | **Accepted.** The rule's single home is now § Plan, three sentences after the coverage baseline: declared cardinality at the measure's grain, key uniqueness on every one-row-per-key side, fact-row identities and the measure's total reconciled across the join. The cheap-route subsection points at it. Reachability was redone: S15 is the one `full` cell with a keyed row-level join and joins the wave as a regression cell. § Estimation Route's pointer was first left untouched; the second pass reversed that (2.2). The rule's wording was also generalized there (2.4). |
| 4 | should-fix | Duplicate homes: the template slot restated coverage, join grain, and absence semantics; the subsection paraphrased § Plan's coverage obligation and repeated the `direct`-records-nothing rule from § Routing. | **Accepted.** The subsection now names the inherited obligations by pointer only; the `direct` record sentence is cut; the template slot is a pointer to the subsection. |
| 5 | should-fix | "The number does not stand bare" is unobservable, and "a fault that could carry the quantity across the claim's threshold" leaves "could" and "fault" undefined. | **Accepted, with a different trigger than the one suggested.** The suggested trigger — values on both sides of the threshold "compatible with the evidence" — is satisfied by S11 too (its four absent hours could logically hold anything), which would turn S11's correct FALSE into `NON_DISCRIMINATING`. The rule now asks the arm to state what the unresolved part would have to contain to cross the threshold, and compares that with what the covered rows show: ordinary there means `NON_DISCRIMINATING`; nothing like it means the outcome stands with the condition as a limitation. Computed for both fixtures before any arm: S22b needs $7,226.77 a day against a slowest covered day of $10,514.59; S11 needs more than 24% of absent requests over 500ms against 1.2% covered. The "ordinary / nothing like it" wording was replaced on the second pass (2.1). |
| 6 | should-fix | Assertions were composite (route + form; verdict + figure; verdict + label + bound), and S22b could pass for the wrong reason. | **Accepted.** Split into S22a.2–4 and S22b.2–4; route assertions score the absence of a hypothesis table and nothing about form. |
| 7 | should-fix | The `direct` clause cut `direct` on row 5 (no measured effect) as well as on failure, and gave no path when S2 or S14 regress. | **Accepted.** `direct` stays in scope as a design decision; row 5 leaves it an unmeasured clarification; a `direct`-caused row 3 or 7 on S22c, S2, or S14 cuts or revises that sentence and remeasures every `mini` cell against the narrower text. |
| 8 | note | "Not needed" overstated what one draw establishes. | **Accepted.** Reworded to "no incremental behavior observed on this cell and arm". |

Codex also confirmed, from the files: no sound reading of `a-fanout` carries Enterprise Q2 revenue past $1M ($925,797.78 by unique account; only the duplicating join gives $1,227,245.07); naming `valid_from` in the prompt is a fair schema signal; and under the first draft's placement no `full` or `estimation` cell traversed the subsection, with S11, S13, S2, S14 the complete existing set that did.

## Second pass

Same reviewer, job `feb3a762e1bf44529c33f498b32b7045` (reasoning effort medium), on the rewritten draft.
Verdict: **fix first.**
It confirmed first-pass finding 1 resolved and finding 2 substantially resolved, and raised seven findings.

| # | Rank | Finding | Disposition |
| --- | --- | --- | --- |
| 2.1 | blocking | The "ordinary / nothing like it" trigger conflicts with `UNKNOWN` completeness: covered rows cannot bound absent rows, so S11's 1.2% covered does not rule out more than 24% absent, and only independently established structural bounds can let an outcome stand. Its suggested text makes both S22b and S11 `NON_DISCRIMINATING`. | **Taken in part; open disagreement.** The logical point is right and is now in the rule's own words ("covered rows do not bound absent ones"). What was not taken is the consequence that S11 must become `NON_DISCRIMINATING`: S11's FALSE-with-limitation is a catalog expectation the owner set deliberately (the 20-hour coverage was "retained as a live check"), and a rule under which any claim on incompletely covered data is unadjudicable is a larger behavior change than issue #38 asks for. The rule now lets the outcome stand only as conditional on a named assumption, with the crossing requirement stated beside the verdict, and the comparison is operational: "within what the covered rows show at the same grain" (S22b: needs $7,226.77 a day, every covered day is at least $10,514.59) against "far outside anything they show" (S11: needs over 24%, worst covered hour 3.3%). Whether S11's expectation should change is the owner's decision and is flagged in the PR. |
| 2.2 | blocking | § Estimation Route's pointer enumerates the inherited obligations and omits the relocated join check, silently exempting estimation joins. | **Accepted**, reversing the first-pass disposition. "and the join check" added to the pointer. S9 has one table, so arguably nothing is owed; S9 runs pre and post anyway as one confirmation cell, because that sentence carries a measured claim. |
| 2.3 | blocking | No verdict row for a regression cell where pre fails a catalog assertion and post passes. | **Accepted.** Row 10 added; the partial-wave rule now lists the terminal rows. |
| 2.4 | should-fix | The join check was additive-specific ("summed or counted", "the measure's total"); S15's primary outcome is a median. | **Accepted.** Trigger is any measure computed across a join; reconciliation is of dropped, kept, and repeated fact rows, plus the total for an additive measure. |
| 2.5 | should-fix | S22c.1 did not reject a standalone validity section, which the expected-outcomes text named as the failure. | **Accepted.** |
| 2.6 | should-fix | The wave rule called the whole subsection measured if any one cell reached behavior. | **Accepted.** Shipping claims are per component: S22a, S22b, S22c each measure one. |
| 2.7 | should-fix | S22b.4's "so does `UNKNOWN`" let a bare full-quarter figure pass. | **Accepted.** S22b.4 now scores the label on the figure alone; completeness wording moved to S22b.5. |

## Step 7 — review of the commit

Same reviewer, job `9959fd4ea04a4fc8a78098d7c415ec7c` (reasoning effort high), on the four commits through `526c4cb`, with the archive open to it.
It was told the measurement had reversed the plan — every new cell on row 5, the wording reverted — and asked to attack the run record.
No blocking finding and no scoring error: it recounted 28 manifests, all `claude-sonnet-5`, exit 0, uncontaminated, and reproduced the cost ratios.

| # | Rank | Finding | Disposition |
| --- | --- | --- | --- |
| 7.1 | adjudication | S22d.3 for `s22d-pre` and `s22d-baseline`: both pass. The assertion scores the claim-level verdict, not the first token of the Outcome cell; the pre arm scopes `CONTRADICTED` to "as exported" and concludes it cannot settle the claim. S22d stays on row 5. A future assertion may score the Outcome label, but this one did not. | Recorded in the run record. |
| 7.2 | adjudication | S2 row 3 is right by amendment 1's reading, weak at n=1: `s2-pre` wrote no file, `s2-post` wrote a route-headed note carrying completeness vocabulary. The harness instruction is a disclosed confound, not a reason to rescore. | Stands. The record/working-artifact line is now stated in the run record. |
| 7.3 | should-fix | S15 "not fully scored" leaves the wave partial under the all-cells gate, and the prose implied the complete rule had fired. | **Accepted.** Run record and decision 008 now say the decline is the conservative reading of an unclosed wave. |
| 7.4 | should-fix | The run record described the post snapshot by the patch, which is the post-revert archive, not what the arms staged. | **Accepted.** Run-time and committed states are now separated. |
| 7.5 | should-fix | Decision 008 line 13 overgeneralized an n=1 result. | **Accepted.** |
| 7.6 | should-fix | S22c.1 was abbreviated to "table" where the assertion says hypothesis table; the record/working-file boundary was unstated. | **Accepted.** |
| 7.7 | note | Amendment 2 is adaptive; decision 008 called S22d "preregistered" without the qualifier. | **Accepted.** |
| 7.8 | note | The run record pointed here for an adjudication this file did not yet contain. | **Accepted**; this section is it. |
| 7.9 | note | Decision 008 called twelve arms twelve cells. | **Accepted.** |

It also held that declining is right on this evidence, and that the § Plan join check should not ship as an unmeasured clarification: it is a new normative obligation, showed no incremental behavior on S22a or S22c, and its S15 regression cell is unfinished.

## Attribution check

Recorded before the canaries: the staged post skill differs from `main` only in the edits under test.
At canary time (`6ec2dd6`) `git diff --stat main` over the skill directory outside `tests/` showed `SKILL.md` (+15 −1) and `references/ledger-template.md` (+1) and nothing else (prereg amendment 1); every post manifest's `skill_files_sha256` fixes what was staged.
