# Preregistration: 2026-09-20 cheap-route data-validity wave (issue #38)

Written before any arm ran; revised twice, before the canaries, on the two passes of the cross-model design review recorded in `2026-09-20-cheap-route-validity/design-review.md`.
This is the `../../PROTOCOL.md` step 1 artifact for every cell below; the step 0 check, the step 2 entanglement pass, the step 3 review pointer, and the step 4 canary rule are recorded here too, so the scored runs can point at one document.
Harness, isolation, archive layout, and scorer are those of `2026-09-15-remediation-wave-prereg.md` § Harness and isolation, unchanged; this wave's archive is `2026-09-20-cheap-route-validity/`, and its prompts are under `prompts/` there.

## Step 0 — does the reported failure exist?

Issue #38 makes two claims.
The first is textual and was re-derived from `main` at `f4c5093`, not taken from the issue: a search of `SKILL.md` for the words that carry the full route's data-validity obligations (`coverage matrix`, `completeness semantics`, `confound`) finds them in § Plan (line 170), § Analysis (217, 220–224), and § Estimation Route (330), plus `confounders` once in § Conclusion's causal-wording bar (318), which is a different rule; nothing in § Routing, where `mini` and `direct` are defined; the Mini Route Template has no slot for population, grain, or absence; § Data Rules is four bullets, none about which rows.
The instrument was checked against a known positive: the same search finds the estimation route's inheritance sentence, which is the thing `mini` and `direct` lack.
The second claim is behavioral — that an arm on `mini` or `direct` settles a claim on the wrong rows — and the archive cannot settle it, because no committed `mini` or `direct` fixture can fail that way: S11 and S13 are one clean table each, S2 is one table, S14 is one dataset.
So the behavioral claim is what this wave measures, and the pre arms measure it without the change existing: if pre already finds the planted fault, the verdict is row 5: no incremental behavior observed on that cell and arm, which is a statement about one draw on one fixture and not about the premise in general.

## What changes, and which cells reach it

| Change | File and section | Cells that reach it | Cells that do not |
| --- | --- | --- | --- |
| Join check: declared cardinality at the measure's grain, key uniqueness on every one-row-per-key side, fact rows and the measure's total reconciled across the join | `SKILL.md` § Plan, three sentences after the coverage-baseline sentence — the rule's single home | S15, the only `full` cell whose analysis joins row-level tables on a key (`incidents.csv` ⋈ `activity.csv` on `incident_id`); S22a and S22c through the pointer below | S1, S5, S7, S12: `sessions.csv` and `orders.csv` share no key and are compared as daily aggregates. S4, S6, S8, S10: one table, or sources never joined. S16, S19, S20, S21: resumed at a reconciliation or status decision, with no collection. S9 is one table, so the rule itself reaches no S9 decision point; S9 runs anyway, for the pointer in the next row |
| `mini` and `direct` inherit § Plan's coverage matrix, baseline, and join check and § Analysis's completeness semantics, by pointer; what an unresolved validity condition does to a `mini` outcome and a `direct` figure | `SKILL.md` § Routing, new subsection "`mini` and `direct` still owe the right rows" | S22a, S22b (mini, new); S22c (direct, new); S11, S13 (mini); S2, S14 (direct) | every `full` scenario and S9: the subsection addresses `mini` and `direct` by name. S17 and S18 are trigger cells scored on activation, which the description decides and this change does not touch |
| § Estimation Route's pointer gains "and the join check", so the route's enumerated inheritance does not silently exempt estimation joins | `SKILL.md` § Estimation Route, the sentence S9 measured on 2026-09-15 | S9. A pointer-only addition on a one-table fixture arguably reaches no decision point and owes nothing; it is run as one confirmation cell because that sentence carries a measured claim and a measured result belongs to the exact wording | everything else |
| `Data validity:` slot in the Mini Route Template, a pointer to that subsection | `references/ledger-template.md` | S22a, S22b, S11, S13 | everything else |

The post arm stages the whole working-tree skill, so attribution needs the skill directory to differ from `main` in these edits and no others; `git diff --stat main -- skills/hypothesis-driven-analysis ':!skills/hypothesis-driven-analysis/tests'` is recorded in the design-review file before the canaries and again in the run record.

## Arms

- **baseline** — no skill. Run on S22a–c only: whether the skill is needed on the cell at all.
- **pre** — the skill at `main` (`--skill-ref main`, `f4c5093`). The control for the changed text.
- **post** — the skill in this working tree.

Attribution is pre versus post on the added assertions.
S11, S13, S2, S14, S15, and S9 run pre and post only: they exist here to detect a regression, and their baselines decide nothing about that.
Model `sonnet` on every arm, resolved model recorded per arm.

## Cells

| Cell | Route | Fixture | Eligibility (catalog) | Added assertions |
| --- | --- | --- | --- | --- |
| S22a | mini | `s22-cheap-route-validity/a-fanout/` (new, validated) | S22a.1 | S22a.2, S22a.3, S22a.4 |
| S22b | mini | `s22-cheap-route-validity/b-truncated/` (new, validated) | S22b.1 | S22b.2, S22b.3, S22b.4, S22b.5 |
| S22c | direct | `s22-cheap-route-validity/a-fanout/` | S22c.1 | S22c.2, S22c.3 |
| S11 | mini | `s11-mini/` | S11.1–3 | — (S11.4 recorded, decides nothing) |
| S13 | mini | `s13-conjunctive/` | S13.1–3 | — |
| S2 | direct | `s1-conversion/orders.csv` (the file alone) | S2.1–2 | — |
| S14 | direct | `s10-fanout/` | S14.1–4 | — |
| S15 | full | `s15-assist-rollout/` | the catalog's S15 assertions, machine-checked where the catalog says so | — |
| S9 | estimation | `s9-ab/signups.csv` | S9.1–3 and S9.4a–b as scored on 2026-09-15 | — |

Ground truth, pinned to the cent by `fixtures/validate_s22.py`: Enterprise Q2 revenue **$925,797.78** (claim FALSE); the plain join on `account_id` reads **$1,227,245.07** (claim TRUE); the second export's rows sum to **$862,691.37** over 2026-04-01 through 09:55 on 2026-06-11, exactly 10,000 rows.

Why `NON_DISCRIMINATING` is the one correct outcome on S22b, in the skill's own terms: the file says nothing about what an absent record means, and § Analysis rules that a source's own missingness pattern can never establish its completeness, so completeness semantics are `UNKNOWN` — the row cap and the mid-morning stop are reasons to doubt the export, not evidence that settles it either way.
Two completions are compatible with the file: nothing was sold after 09:55 on 11 June, and the quarter stays at $862,691.37, below the claim; or the 19 absent days ran like the covered ones, and the quarter passes $1M even at the slowest covered day's $10,514.59 (needs $7,226.77 a day).
The covered rows show the amount that would reverse the answer as ordinary, so neither TRUE nor FALSE stands.
That continuation is a plausible completion, not a lower bound on revenue that exists; the only bound the file gives is that recorded Q2 revenue is at least $862,691.37.

Assertions, each a single check on archived output:

- **S22a.1 / S22b.1** — the run adjudicates one claim with no hypothesis table (two or more candidate explanations tabulated or enumerated as rivals fails). Form beyond that — paragraph or bullets, inline or file — is not scored.
- **S22a.2** — the report or record says `accounts.csv` holds more than one row for some `account_id`, or that the join repeats orders.
- **S22a.3** — the verdict on the claim is FALSE (or `CONTRADICTED`).
- **S22a.4** — the Enterprise Q2 revenue given as the answer is within $1,000 of $925,797.78.
- **S22b.2** — the report or record says the rows stop on 2026-06-11, or that they do not cover the whole quarter.
- **S22b.3** — the verdict on the claim is neither FALSE nor TRUE: `NON_DISCRIMINATING`, or the same in words ("cannot be settled from this export"). A verdict of FALSE fails even when the end date is mentioned; a verdict of TRUE rests on a projection and fails.
- **S22b.4** — the $862,691 figure is explicitly labelled as the total of the recorded rows, or of the part of the quarter they cover; given as "Q2 revenue" without that label it fails, whatever else the report says about completeness.
- **S22b.5** — completeness is stated as unknown, unverified, or apparently incomplete. Asserting as settled fact that the export is complete fails. Recorded; with b.2 it shows why b.3 was reached.
- **S22c.1** — answers without a ledger file, a hypothesis table, PPDAC section headings, or a standalone data-validity or coverage record or section (S2's guardrail, on this fixture). A sentence or two explaining the account-history duplicates is the answer's content, not ceremony.
- **S22c.2** — the Enterprise Q2 revenue given as the answer is within $1,000 of $925,797.78.
- **S22c.3** — the report says the account table repeats accounts, or that a plain join would overstate the figure.
- **S11.4** — the record carries a `Data validity` entry. Recorded for post only; it decides no row.

## Expected outcomes

- S22a: baseline joins on `account_id` and answers TRUE at about $1.23M (fails a.2–a.4); pre adjudicates the one claim and does the same, because nothing on that route asks about the join; post finds the repeated keys and answers FALSE at $925,797.78.
  At-risk: every arm deduplicates by habit (`drop_duplicates`, or a segment lookup built as a dict), so pre passes and the cell lands on row 5; an arm that builds a dict silently gets the right number and never says why, passing a.3–a.4 and failing a.2.
- S22b: baseline and pre answer FALSE at $862,691; post reports where the rows stop and `NON_DISCRIMINATING`.
  At-risk: post mentions the end date and still answers FALSE (fails b.3, row 6); or pre already notices a quarter that ends on 11 June (row 5).
- S22c: baseline and pre report about $1.23M; post reports $925,797.78 and says why.
  At-risk: post wraps the answer in a ledger or a validity section (fails c.1).
- S11, S13, S2, S14, S15, S9: post passes every catalog assertion pre passes.
  At-risk: S2 or S14 post adds ceremony — a coverage matrix, a record — that `direct` forbids; S11 post promotes the known 20-of-24-hour coverage from a stated limitation to `NON_DISCRIMINATING`.
  That last case is scored as written: S11.3 requires the answer FALSE, and the subsection's own test supports it — 14 of the 1,200 covered requests exceed 500ms (1.2%; the worst covered hour is 3.3%), and the 240 absent minutes would need more than 58 such requests (24%) to move the day's p95 past 500ms, far outside anything the covered rows show.
  A post arm that answers FALSE as conditional on the absent hours resembling the covered ones passes S11.3; the conditional is the rule working.
  The second review pass disputes this expectation — see the design-review file, finding 2.1 — and the dispute is the owner's to settle; the arms are scored against the catalog as it stands.
  A post arm that declines to answer fails S11.3 and lands the change on row 3.

## Per-cell verdict table (every row written before any arm ran)

The first row that applies governs.

1. **Void** — any arm is contaminated, exits non-zero, times out, resolves to a different model, or produces output the assertions cannot be scored against. Rerun once under a fresh name; void twice is reported void. Both runs are archived.
2. **Fixture defect** — an arm shows a sound reading of a packet that the ground truth above does not allow for. The fixture and its validator are fixed with a known-positive test, the fix is recorded here, and the cell is rerun in full.
3. **Regression** — post fails a catalog or eligibility assertion that pre passes, on any cell. Recorded against the change; the text that cell reaches does not ship as written.
4. **Off-target** — on S22a–c, pre or post fails the cell's eligibility assertion (it did not take the route the cell measures), and row 3 does not apply. The added assertions are recorded and decide nothing; the cell is rerun once, and off-target twice is reported as such.
5. **Not needed** — both arms eligible; pre and post both pass every added assertion. No incremental behavior observed on this cell and arm; the text carries no measured behavioral claim here. It may stay as a clarification carrying no measured claim, or be dropped; the owner decides. **This row is reachable without the change existing.**
6. **Reaches behavior** — both arms eligible; post passes every added assertion and pre fails at least one. Measured as reaching behavior at n=1 on one model; an existence result, not a rate.
7. **Does not reach** — both arms eligible; post fails an added assertion for a reason the text addresses. The text is revised and remeasured once, or dropped; a second row 7 drops it.
8. **Unaddressed failure** — both arms eligible; post fails an added assertion for a reason the text does not address (an arithmetic slip, a misread date). Recorded; the cell is rerun once; the same result twice is reported as inconclusive for that cell.
9. **Shared catalog failure** — on a regression cell, pre and post fail the same catalog assertion. Pre-existing debt: recorded in the catalog, not attributed to the change, not blocking it.
10. **No regression** — on a regression cell, post passes every catalog assertion pre passes, including the case where pre fails one that post passes. A pre-only failure is recorded as an unattributed difference at n=1, claimed as nothing.

Wave-level, decided here and not after the arms:

- Nothing ships from a partial wave: every cell must end on row 3, 5, 6, 7, 9, or 10, or on a twice-confirmed 4 or 8 reported as such, before any text ships.
- The § Plan join rule ships as measured if S22a or S22c lands on row 6 and S15 shows no row 3. If S15 lands on row 3, the rule is revised and S15, S22a, and S22c are remeasured once.
- The cheap-route subsection is measured by component, never as a whole: S22a measures join handling on `mini`, S22b measures the unresolved-completeness disposition on `mini`, S22c measures join handling and reporting on `direct`. A component ships as measured only on row 6 for its own cell; on row 5 it is an unmeasured clarification, the owner's call to keep or drop. No component ships if any of S22a–c, S11, S13, S2, S14 lands on row 3, or its own cell on row 7.
- The estimation pointer ships if S9 lands on row 10 (or 9).
- `direct` stays in scope as a design decision: "answer and stop" removes ceremony, not the check that the figure is right. Row 5 on S22c leaves the `direct` sentence as an unmeasured clarification, the owner's call to keep or drop. A row 3 or row 7 on a `direct` cell (S22c, S2, S14) that the `direct` sentence caused means that sentence is revised or cut, and every `mini` cell is remeasured against the exact narrower text, because a measured result belongs to the wording it was measured against.
- If S22a–c all land on row 5, nothing ships as measured; the fixture, the catalog entry, and the finding ship, and the text is the owner's call.

Baseline results are recorded as "skill needed on this cell: yes/no" and decide nothing about the text.

## Entanglement pass (PROTOCOL step 2)

- **Null-result sensitivity gate (§ Data).** S22a's truth is a contradicted claim, which is the shape that gate reads. The quantity is a sum over a ledger the prompt states is complete — a census, not a sample — so there is no sampling interval to compute, exactly as on S11, whose runs were not detoured by it. S22b's correct answer is itself `NON_DISCRIMINATING`, reached through completeness and not through an interval; an arm that reaches it by bootstrapping order amounts has the right label for the wrong reason, and the canary is scored on that.
- **Completeness on S22a.** Closed by the prompt ("the complete order ledger for the first half of 2026") and by the fixture (orders on every day of H1, validator-enforced), so the join is the only live fault on that packet. `accounts.csv` covers every `account_id` in the ledger, so the join drops nothing.
- **Convention invariance on S22a.** `segment` is constant across every account's versions and every account's first version predates H1, so distinct ids, latest version, and an as-of join all reach $925,797.78; the validator computes the as-of total and fails if it moves. There are no orders outside H1 and the quarter's edges are whole days, so boundary handling cannot matter.
- **The `valid_from` column is named in the S22a and S22c prompts.** It is a fair schema signal, reviewed as such: it is what makes row 5 reachable if pre reads the history table unaided, and it removes any ambiguity about how to resolve versions.
- **Join fault on S22b.** None: one table.
- **Causal routing.** Neither claim is causal; nothing can fall to `full` on identification grounds. One stated claim, no rival: `mini`. S22c asserts nothing: `direct`.
- **Authorization and costly collection.** Local files; both gates quiet on S22a–c. S14 is metered by design and unchanged.
- **Date.** Each prompt names the quarter (2026 Q2, April through June), so the arm's clock cannot move "last quarter".
- **S15 and the join rule.** `activity.csv` lacks some `incident_id`s by design — that asymmetry is S15's completeness trap — so a reconciliation across the join surfaces the same fact the coverage matrix is already asked to find. The rule cannot hand S15 a new wrong answer; the risk is cost and displacement of other work, which the regression row reads.

## Canary rule (PROTOCOL step 4)

One post arm per new cell (`canary-s22a-post`, `canary-s22b-post`, `canary-s22c-post`) runs first and is scored on rationale: did it find the fault because it read and applied the changed text?
A canary that reaches the right answer without traversing it means the fixture is too easy or entangled — back to step 2.
Canaries are excluded from the scored table; the scored arms run fresh.

## Cross-model design review (PROTOCOL step 3)

Codex reviewed the first draft of this document, the fixture with its generator and validator, the prompts, and the draft wording together, before any arm ran, and said not to run them yet.
Its eight findings and their dispositions are in `2026-09-20-cheap-route-validity/design-review.md`; every blocking item was fixed and this document was rewritten.
A second pass on the rewrite raised seven more, also recorded there: six were taken, and one — that the unresolved-completeness rule must make S11 `NON_DISCRIMINATING` as well — was taken in part and is recorded as an open disagreement for the owner.
A third pass was not run: the remaining edits apply the reviewer's own suggested text or tighten assertions, PROTOCOL asks that review rounds be batched rather than serialized, and step 7's review of the commit reads whatever these edits got wrong.
