# Preregistration: 2026-09-15 remediation wave

Written before any arm ran; revised once, before the canaries, on the cross-model design review recorded in `2026-09-15-remediation-wave/design-review.md`.
This wave measures the agent-read wording that the 2026-09-15 external-review remediation changed, on the cells whose decision points traverse it, per `../../PROTOCOL.md` § What owes a rerun.
It is the PROTOCOL step 1 artifact for every cell below; the step 2 entanglement pass, the step 3 review pointer, and the step 4 canary rule are recorded here too, so the scored runs can point at one document.

## What changed, and which cells reach it

| Change | File and section | Cells that reach it | Cells that do not |
| --- | --- | --- | --- |
| Estimation route inherits the coverage matrix (§ Plan) and completeness semantics and confound check (§ Analysis); randomization identifies assignment, not the analysis population | `hypothesis-driven-analysis/SKILL.md` § Estimation Route | S9 | every `full`, `mini`, `direct` scenario |
| Degraded mode for no defensible prior or likelihood ratio, with worked example | `decision-analysis/SKILL.md` § Degraded Modes | DA-S1 | DA-S4..S7 (no update sequence, or a different route); DA-S8 (its inputs are supported) |
| Precedence when both sensitivities fire: `prior-sensitive`, loss crossover in Conditions | `decision-analysis/SKILL.md` § Verdict | DA-S8 (new; see the catalog) | DA-S1 (losses elicited, so only the prior flips); DA-S3 (no supported inputs, so the degraded mode and the loss rule decide without the paragraph) |
| Profile route separates dated sequence (recorded) from attribution (unresolved, handed off) | `exploratory-data-analysis/SKILL.md` § Profile Route | B10 | B1..B9 (explore route) |
| No-file-tools degraded mode names Frame-lite on the profile route | `exploratory-data-analysis/SKILL.md` § Degraded Modes | B10-nofile (skill arms given Read, Glob, Grep only) | every arm with file tools |
| Data rules as four bullets; authorization-gate rationale relabelled | EDA § Data Rules; the shared gate in all four skills | none — same obligations, same words | all |

The scorer for the decision-analysis cells, `decision-analysis/tests/check_decision.py`, licensed only `none needed` in the belief slots before this wave.
It now licenses the degraded mode's `none supported — see Robustness` sentinel, coupled to a `prior-sensitive` verdict and a `sensitivity-only` sweep, and a `none supported` evidence row, with positive and negative tests; without that, an arm following the skill would fail the skill's own checker, and the cell would score the checker rather than the wording.

## Arms

Every cell runs three arms, so the comparison matches the claim:

- **baseline** — no skill. Answers whether the skill is needed on this cell at all.
- **pre** — the skill as it stood on `main` before this branch (`--skill-ref main`). The control for the changed sentence.
- **post** — the skill in this working tree.

The attribution question — does the changed sentence reach behavior — is **pre versus post** on the added assertion.
Baseline versus either skill arm answers a different question and is recorded separately; it decides nothing about the sentence.
B10-nofile has no baseline arm: a no-skill agent has no degraded mode to follow.

## Harness and isolation

Every arm is one `claude -p` subprocess run by `../../run_arm.py`, model `sonnet` (the resolved model is recorded per arm).
The fixture and, for a skill arm, a standalone copy of the skill directory without its `tests/` tree are staged into a fresh directory outside the repository; that directory is the arm's cwd and its only `--add-dir`, and the prompt names only staged paths.
`--tools` sets the built-in tools the arm is actually given (Read, Write, Edit, Bash, Glob, Grep; B10-nofile: Read, Glob, Grep) and `--allowedTools` pre-approves the same set; `--setting-sources project` keeps user-level settings and plugins — including the installed release of this plugin and its hook — out of the arm.
Bash is not a filesystem sandbox, so after each run every tool call is scanned for the repository path, any `SKILL.md` other than the staged one, and any `tests/` path; a hit is recorded in the manifest as contamination and voids the arm.

Isolation was probed before the wave with two arms that were asked, with no tool calls, to list their tools, their loaded instruction files, and their skills (`2026-09-15-remediation-wave/isolation/`).
The file-tools arm reported Bash, Edit, Glob, Grep, Read, Write; the no-file arm reported Glob, Grep, Read; both reported no instruction or memory file loaded and no skills; both manifests' `tools_at_startup` from the `system` init event match.
That is an arm's self-report plus the harness's own record of what it was given, not a proof about the model's weights or training; it is the isolation this wave claims and no more.

Archived per arm under `2026-09-15-remediation-wave/`: the exact prompt, the exact command, the stream-json transcript, stderr, a manifest (resolved model, tools at startup, tool-call manifest with ordinals, files written and their sha256, sha256 of prompt, transcript, every staged skill file, and every fixture file), and a copy of everything the arm wrote.
The catalog prompts are used verbatim with the fixture path substituted (`prompts/`).
Scorer: the dispatching session (Fable), against the assertions below, with every quote grepped against the archived transcript or written file before it is cited; the decision-analysis records are also run through `check_decision.py` and `instruments/check_record.py --final`.

## Cells

| Cell | Skill | Fixture | Catalog assertions | Added assertions |
| --- | --- | --- | --- | --- |
| S9 | hypothesis-driven-analysis | `s9-ab/signups.csv` (existing) | S9.1–S9.3 | S9.4a, S9.4b |
| DA-S1 | decision-analysis | `da-s1-ledger/` (new, validated) | DA-S1.1–S1.4 | DA-S1.5a–e |
| DA-S8 | decision-analysis | `da-s1-ledger/` | DA-S8.1–S8.4 (new catalog entry) | DA-S8.4 is the precedence assertion |
| B10 | exploratory-data-analysis | `b10-entity/` (new, validated; five CSVs and a README) | B10.1–B10.4 | B10.5a–c |
| B10-nofile | exploratory-data-analysis | `b10-entity/` | B10.1, B10.4 | B10.6a–c |

Added assertions, each a single check on archived output:

- **S9.4a** — the report records the analysis population's coverage: both variants present on each of the 14 days, `visits` and `signups` populated throughout.
- **S9.4b** — the report says what an absent day or an unrecorded visitor would mean for the estimate; `UNKNOWN` or "cannot be verified from daily aggregates" is an accepted answer, silence is not.
- **DA-S1.5a** — Prior odds and Posterior odds read `none supported — see Robustness`, bare.
- **DA-S1.5b** — the Evidence table keeps the reference-class ratio as LR 4.5 (or 9/10 ÷ 2/10) with provenance `estimated-from-data-in-hand`, naming `reference_class.csv`, the 20-rollout quota-drawn class, and the 40 ms gap condition; no row invents a ratio and no row is dropped for want of a prior.
- **DA-S1.5c** — Robustness sweeps a `sensitivity-only` prior class, applies the LR, and reports the prior-odds crossover within the checker's tolerance of 0.1 ÷ 4.5 ≈ 0.022.
- **DA-S1.5d** — Verdict `prior-sensitive`; Recommended action `returned to owner`; Conditions may say the evidence does not quantify the prior.
- **DA-S1.5e** — the written record passes `check_decision.py` and `instruments/check_record.py --final`.
- **DA-S8.4** — Verdict `prior-sensitive`, not `loss-sensitive`; Conditions states the loss-ratio crossover as well as the prior one; Robustness reports both; Recommended action `returned to owner`.
- **B10.5a** — the entity record states the plan change to `enterprise-annual` with its date, 2026-03-01, from `plan_changes.csv`.
- **B10.5b** — the entity record states that billed volume fell from 2026-04 (1,910 in March to 1,120 in April, or the equivalent in words).
- **B10.5c** — the record names the attribution of one to the other as unresolved, or hands it to `hypothesis-driven-analysis`, rather than omitting the sequence or asserting the link.
- **B10.6a** — Frame-lite (entity, identifier, sources, timeframe, budget) appears in the assistant's response text before the first tool call that reads a fixture data file (`billing.csv`, `tickets.csv`, `accounts.csv`, `contract_status.csv`, `plan_changes.csv`); reading the skill, its references, the fixture `README.md`, and listing the fixture directory are exempt; the identifier may be provisional ("to be resolved from `accounts.csv`").
- **B10.6b** — no reservation is emitted or demanded (the profile route has none).
- **B10.6c** — the response says the precommitment is only as strong as the visible message order.

## Expected outcomes

- S9: baseline fails S9.1 on the threshold (as on 2026-07-16), passes S9.2–S9.3, fails S9.4a–b; pre passes S9.1–S9.3 and fails S9.4a–b (the pre-edit route inherits only the gates and data rules); post passes all.
  At-risk: post records coverage in one line and says nothing about absence, failing S9.4b.
- DA-S1: baseline recommends with an invented confidence and no record; pre invents or elicits-from-nothing a prior, or refuses to run the update, failing S1.5a–c; post passes S1.1–S1.5e.
  At-risk: post puts a `sensitivity-only` prior in Evidence and update (fails S1.5a and the checker), or drops the LR row because the prior is missing (fails S1.5b).
- DA-S8: baseline picks point values and recommends; pre reaches a sensitive verdict but labels it `loss-sensitive` or omits one crossover, failing S8.4; post passes S8.1–S8.4.
  At-risk: post labels `loss-sensitive` because the loss disagreement is the salient gap.
- B10: baseline profiles the file, reads both empty months as inactivity, attributes the drop to the plan change (fails B10.1, B10.2, B10.4); pre records the drop as a change but omits the plan-change event or the sequence (fails B10.5a or B10.5c); post passes B10.1–B10.5c.
  At-risk: post suppresses the sequence to stay clear of attribution, failing B10.5a–b — the failure the changed sentence exists to prevent.
- B10-nofile: pre emits the explore route's Frame with a reservation or nothing before its first data read (fails B10.6a or B10.6b); post passes B10.6a–c.

## Per-cell verdict table (every row written before any arm ran)

Outcomes are decided per cell in this precedence order; the first row that applies governs.

1. **Void** — any arm is contaminated (manifest `contaminated` non-empty), exits non-zero, times out, resolves to a different model, or produces output the assertions cannot be scored against (truncated, no record file where one is required). The arm is rerun once under a fresh name; if it voids again the cell is reported void, not RED. Both runs are archived.
2. **Checker defect** — `check_decision.py` or `check_record.py --final` rejects a record the skill's text licenses, or accepts one the skill's text forbids. The checker is fixed with a test, the fix is recorded here, and the same transcript is rescored. This row exists because the design review found one such case before running.
3. **Regression** — post fails a catalog assertion that pre passes. Recorded against the change; the sentence does not ship as written whatever the added assertion shows.
4. **Reaches behavior** — post passes every added assertion for the cell and pre fails at least one. The sentence is measured as reaching behavior at n=1 on one model; an existence result, not a rate. Ships as measured.
5. **Not needed** — post and pre both pass every added assertion. The sentence adds no measured behavior on this cell. It may stay as a clarification carrying no measured claim, or be dropped; the owner decides, and nothing in this wave calls it an improvement.
6. **Does not reach** — post fails an added assertion for a reason the sentence addresses. The sentence is revised and remeasured, or dropped, before the PR merges.
7. **Shared catalog failure** — pre and post both fail the same catalog assertion. Pre-existing debt: recorded in the catalog, not attributed to the change, and not blocking it.

Baseline results are recorded beside each cell as "skill needed on this cell: yes/no" and decide nothing about the sentence.
Wave-level: a sentence ships as measured only if its cell lands on row 4 or row 5 (row 5 with the owner's decision recorded); rows 3 and 6 block that sentence; rows 1, 2, and 7 are reported and do not by themselves settle shipping.
A partial wave is reported as partial.
The release gate, validator, hook, and README changes in the branch are not agent-read prose and are unaffected by any row.

## Entanglement pass (PROTOCOL step 2)

- S9: the effect is present (B − A ≈ +0.63pp, interval excluding zero), so the null-result sensitivity gate is not the deciding rule; randomization is stated, so the causal-wording bar is met and routing cannot fall to `full` on identification grounds; the file is local, so the authorization and costly-collection gates are quiet; the CSV is complete (14 days × 2 variants, all fields populated), so S9.4a tests whether coverage is recorded, not whether a hole is found — a hole would make the coverage rule the incidental decider.
- DA-S1 / DA-S8: the ledger validates clean in `--final` mode, so the decision skill has no structural defect to detour into; H1 is `descriptive` — the regression is real in served latency, whatever caused it — which is what the reference-class labels settle and what ship/hold turns on, so Identification basis `NONE` is correct and no review detour is owed; the reference class states it was drawn to fixed quotas and its split is not a base rate, and `validate_da_s1.py` enforces that statement and the absence of any prior, probability, or loss token, so a prior in a DA-S1 record is invented, not found; the file is local.
- DA-S8 specifically: the user-elicited prior range and loss range are chosen so both straddle the boundary with LR 4.5 (posterior 0.09–0.9 against threshold 0.05–0.5), so a correct record must flip on both axes, and only § Verdict's precedence paragraph says which label the single verdict slot takes.
- B10: the two empty months, the rename, and the dated plan change one month before the drop are B10's own traps and in scope; the change date is independently recorded in `plan_changes.csv`, so B10.5a scores a fact in the extract, not an inference from billing; the extract is local and small; no costly source is offered.
- B10-nofile: Read, Glob, Grep suffice to inspect five small CSVs, so tool poverty cannot void the arm on its own; the startup inventory in the manifest proves which tools the arm had.

## Canary rule (PROTOCOL step 4)

One post arm per cell runs first as a canary and is scored on rationale: did it reach its label because it read and applied the sentence under test?
A canary that passes without traversing the sentence means the fixture is entangled — back to step 2.
Canary arms are archived under `canary-*` names and excluded from the scored table; the scored arms are fresh runs.
Rationale is process evidence; attribution rests on pre versus post.

## Cross-model design review (PROTOCOL step 3)

Codex reviewed the first draft of this document, the fixtures with their generators and validators, the harness, the checker change, and the changed sentences together, before any arm ran, and said not to run them yet.
Its ten findings and their dispositions are in `2026-09-15-remediation-wave/design-review.md`; every blocking item was fixed and this document was rewritten before the canaries.

## Amendment 1 — after the canaries, before any scored arm (2026-09-15)

Five canary post arms ran (`canary-s9-post`, `canary-da-s1-post`, `canary-da-s8-post`, `canary-b10-post`, `canary-b10-nofile-post`).
Each was scored on rationale only, per the canary rule; none enters the scored table.

- **Rationale, every cell: the sentence under test was traversed.** S9 wrote a coverage matrix at the day-by-variant grain, a coverage baseline, completeness semantics, and a confound check on the estimation route; DA-S1 used the `none supported — see Robustness` sentinel, kept the 4.5 ratio, and swept a `sensitivity-only` prior class; DA-S8 wrote "per SKILL.md's rule for this combined case, the verdict slot is prior-sensitive and its Conditions state the loss crossover too"; B10 wrote its Frame-lite before reading billing, cited § Profile Route for taking no reservation, and headed its entity record "dated sequence, no cause assigned"; B10-nofile cited the degraded-mode rule and said its precommitment was only as strong as message order.
  No fixture is entangled; no cell returns to step 2.
- **Design defect found by the DA-S1 canary.** Its sweep found no crossover inside the swept prior class, so it returned `robust`, which § Numeric Policy licenses ("a `robust` verdict requires the same action to be preferred across the entire stated prior class") and which the degraded-mode sentence forbade ("the verdict is `prior-sensitive` with that crossover").
  The two conflicted; the sentence was wrong.
  § Degraded Modes now defers to § Numeric Policy on the swept class — `robust` when the action holds across it with belief-grade losses and Conditions naming the unsupported prior, otherwise `prior-sensitive` — and `check_decision.py` accepts either label with the sentinel (a `robust` record still owes `none within swept class` and belief-grade losses under the existing gates).
  The worked example's odds were also corrected: a loss ratio of 3 flips at prior odds 1:3, not 3:1, and a sourced LR of 2 moves that flip to 1:6, outside the example's swept class, making that variant `robust`.
  **DA-S1.5d is revised accordingly:** Verdict `robust` or `prior-sensitive` as § Numeric Policy decides on the swept class; under `robust`, Conditions names the swept class and says the prior is unsupported and Recommended action names the action; under `prior-sensitive`, Recommended action reads `returned to owner`.
  DA-S1.5c is unchanged: the prior-odds crossover (≈0.022 at loss ratio 10) is reported either way.
  The expected outcome for DA-S1 post is now `robust` (the crossover lies far below any plausible swept class); the pre arm is still expected to fail S1.5a–c.
- **Checker strictness is the catalog's bar, not this wave's.** Both DA canaries failed `check_decision.py` on form — annotated sentinels and labels, `1:49 – 1:4` where the checker parses `0.02–0.25`, a nested Crossover list, `none` for `none supported` in a provenance cell — while their arithmetic and verdict logic were right.
  DA-S1.1 and DA-S8.1 ("passes `check_decision.py`") are scored as written; a shared pre/post failure there lands on row 7 (pre-existing debt) and does not decide the sentence.
- **Scoring clarification for B10.3.** The deliverable is the arm's final message.
  The exploration-log template carries a Leads section, and a profile arm may fill it with unchased observations dispositioned `reported`; that is not "a leads table as the deliverable".
  B10.3 fails when the final message is a leads table, or is the orientation record alone.
- **B10.6a boundary is unchanged**, and the canary shows what it will catch: that arm read every data file, attempted a Write it did not have, and only then emitted Frame-lite.
  Whether the scored post arm does the same decides B10.6a; the canary's result is not carried forward.
- The contamination scan was corrected between the canaries: it had flagged a Write whose *content* mentioned "SKILL.md"; it now reads only path-bearing fields, and every canary manifest was rescanned with the previous value preserved under `rescans`.

## Results (2026-09-15, after all fourteen scored arms)

Run records: `../2026-09-15-scenario9-estimation-route.md`, `../../../decision-analysis/tests/runs/2026-09-15-da-s1-da-s8-degraded-mode-and-precedence.md`, `../../../exploratory-data-analysis/tests/runs/2026-09-15-b10-entity-profile.md`.
Every arm resolved to `claude-sonnet-5`, exited 0, and passed the contamination scan; no arm was void; no checker rejected a record the skill licenses (row 2 did not fire in the scored batch).

| Cell | Sentence | Added-assertion outcome (pre → post) | Row | Regression | Skill needed vs baseline |
| --- | --- | --- | --- | --- | --- |
| S9 | Estimation route inherits coverage and completeness obligations | pre fails S9.4b, post passes S9.4a–b | **4 — reaches behavior** | none | yes (S9.1) |
| DA-S1 | No-supported-prior degraded mode | pre invents a `sensitivity-only` prior in Evidence and update; post uses the sentinel but annotates it (5a fails on form); 5b–5d both pass; 5e both fail on the checker | **6 on form, 5 on substance** | none | yes |
| DA-S8 | Verdict precedence when both sensitivities fire | pre and post both `prior-sensitive` with the loss crossover in Conditions | **5 — not needed** | none | yes |
| B10 | Profile route: dated sequence recorded, attribution unresolved | 5a and 5c both pass; 5b both fail (neither names the volume fall as a change) | **5 on 5a/5c, 6 on 5b** | none | yes (B10.1, B10.3, B10.4) |
| B10-nofile | Degraded mode names Frame-lite | 6b and 6c both pass; 6a both fail (frame emitted after every data read and a failed Write) | **5 on 6b/6c; 6a is shared debt** | none | — |

What ships as measured under the table: the S9 sentence (row 4).
What is a clarification carrying no measured claim, the owner's call to keep or drop: the DA-S8 precedence paragraph, the B10 profile-route sentence's dated-sequence and handoff halves, and the Frame-lite naming (row 5).
What the table blocks as measured: the DA-S1 sentinel on form (annotated, not bare) and B10.5b (neither arm named the volume fall).
Both blocked items are argued in their run records to be shared, pre-existing behavior — the annotation habit every DA arm shows on every slot, and a summarizing choice the changed sentence does not govern — rather than defects of the sentences; that argument is the scorer's and is recorded as such, not as a row of this table.

Debts this wave surfaced, recorded in the catalogs:

- Every decision-analysis record, pre and post, fails `check_decision.py` on form while its arithmetic and verdict logic are right: annotated slots, odds written `1:49` where the checker parses `0.02`, relabelled slots, extra evidence cells.
  The template's slot text invites annotation; the checker forbids it.
  Debt against the template and checker together.
- Without file tools, both skill arms read every data file, attempted a Write they had not been given, and only then fell back to response text.
  The degraded mode's "before any exploration output" is not what an agent does when it discovers tool poverty late; debt against § Degraded Modes as a whole.
- The S9 fixture is complete by construction; the estimation route's data-validity inheritance on a fixture with a hole is unmeasured.
