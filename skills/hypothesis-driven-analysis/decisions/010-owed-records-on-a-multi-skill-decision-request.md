# 010 — Which records a multi-skill decision request owes

Status: proposed, 2026-11-24; awaiting an owner decision (issue #119).

## Question

On a decision request whose designed route crosses several skills, some runs leave the user only the final memo, without the intermediate records the earlier skills require.
The answers can still be acceptable.
Three things can differ for each record: whether it was created at all, whether it was retained where the user can retrieve it, and whether it was delivered or pointed to.
Which of those does a multi-skill decision request owe, and is a memo enough for some asks?

## Evidence

Counts are of 3 Codex plugin arms per cell, from the 2026-11-17 full-catalog suite; they are counts, not rates.
Arm transcripts are under `docs/evidence/integration/2026-11-17-full-catalog/arms/`, cited as `<arm>.jsonl:<line>`.

### What the results file reports

`docs/evidence/integration/2026-11-17-full-catalog/results.md` (at `807838a`):

- I4 (designed route HDA → (CIR) → DA): "1/3 with ledger, review, and memo; 2/3 read all three skills, wrote a memo only" (line 18).
- I4: evidence boundary (E) and task (C) 3/3 in the plugin condition and 3/3 without the plugin (line 33).
- I2 (designed route EDA → HDA): "2/3 with both records; 1/3 read both, wrote the exploration log only" (line 16).
- I2: E 3/3 with the plugin and 0/3 without; C 3/3 in both (line 29).
- Codex "read every skill of the designed route in 9 of 9 I2–I4 plugin arms ... and wrote each skill's record in 6" (line 21).

`docs/evidence/integration/2026-11-17-full-catalog/scores-primary.md` gives the per-arm labels behind those rows (I2 lines 22–24, I4 lines 41–43).

### What the transcripts show

The transcripts separate the three things the results file's labels combine.
"Created" means a file whose headings follow the owning skill's template was written anywhere during the arm.
"Retained" means that file sits in the arm's workspace at the end.
"Pointed" means the final message names the file's path.

| Cell | Record | Created | Retained in workspace | Pointed to in final message |
|---|---|---|---|---|
| I4 | HDA investigation ledger | 2/3: plugin-2:17 (/tmp/assist-review/ledger.md), plugin-3:15 (mktemp dir, ledger.md) | 0/3 | 0/3 |
| I4 | CIR identification review | 2/3: plugin-2:26 (/tmp/assist-review/identification.md), plugin-3:15 (same dir, review.md) | 0/3 | 0/3 |
| I4 | DA decision record | 0/3 in template form; a memo in 3/3: plugin-1:24, plugin-2:28, plugin-3:22 | memo 3/3 | memo 3/3: plugin-1:25, plugin-2:29, plugin-3:25 |
| I2 | EDA exploration log | 3/3: plugin-1:13, plugin-2:11, plugin-3:11, all under /tmp | 0/3 | 1/3: plugin-2:21 |
| I2 | HDA investigation ledger | 2/3: plugin-1:20, plugin-3:18, both ledger.md under /tmp | 0/3 | 0/3 |

Where results.md is coarser than the transcripts:

- I4-codex-plugin-3 is labelled "memo only" (scores-primary.md line 43), but it created both the ledger and the review in a scratch directory before the memo (`I4-codex-plugin-3.jsonl:15`, appended at `:20`); only the memo was left in the workspace.
- I4-codex-plugin-2, the arm labelled "ledger + review + memo" (scores-primary.md line 42), kept its ledger and review under /tmp/assist-review/, not in the workspace, and its final message points only at the memo.
- I4-codex-plugin-1 wrote /tmp/assist-plan.md, headed "Assist review preanalysis plan" (`I4-codex-plugin-1.jsonl:15`), which does not follow the ledger template and is not counted above.
- I2-codex-plugin-2 wrote /tmp/api-confirmation.md (`I2-codex-plugin-2.jsonl:16`, `:20`) and pointed to it (`:21`); scores-primary.md line 23 scores that arm "log only", and this record does not reclassify it.
- No memo in I4 uses the decision-record template's blocks, so the "memo" results.md counts as the DA record is not one in template form.

Nothing in these arms was retained in the workspace except the memos, so on this evidence "retained" and "pointed" are almost empty columns and "created" is where the arms actually differ.
The arms that wrote under /tmp were following the shipped default: the ledger and exploration-log templates name scratch space as the default location (`skills/hypothesis-driven-analysis/references/ledger-template.md` and `skills/exploratory-data-analysis/references/exploration-log-template.md`, each in its opening lines).
The empty "retained" column is therefore not evidence of an arm disobeying the skills.

`docs/evidence/integration/2026-11-18-handoff-fix/results.md` reran Claude Code only; its I4 arms took the designed route 0/3 and loaded no skill in 3/3 (line 16), so it is no evidence about records on I4.

Measurement limit, from the full-catalog results file's own Limits (line 55): a batched `cat` of several `SKILL.md` files shows that the skill text entered context, not that each skill was followed.
A Codex route read from file reads is therefore an upper bound on what was followed, which is why the records each arm created are the stronger evidence.

## Where each route requires a record

Pointers only, by section; the requirement and its conditions live there, not here.

- `exploratory-data-analysis`: § The Lifecycle (explore route), the exploration log; § Profile Route, the log's Frame-lite and Orientation sections, which are the profile's deliverable.
- `hypothesis-driven-analysis`: § The Loop (full route) § Plan, the investigation ledger on `full`; § Routing's table and § The Loop (full route) § Conclusion, the one-paragraph ledger on `mini` and the estimation route's record; § Costly collection is a modifier, not a route, the collection plan, including on `direct` when collection is costly.
- `causal-identification-review`: § Routing and § Per-route procedure, the identification review on `review`, `construct`, and `bound`.
- `decision-analysis`: § The Decide Route, the full decision record; § The VoI Route, the one-block VoI record.
- Each of the four files' § Record Delivery, rendered from `scripts/shared-sections/record-delivery.md`, for what happens to a record before delivery.

### Reporting and handoff obligations that already bind

These stay in force under either position below, and this record does not restate them:

- `hypothesis-driven-analysis` § The Loop (full route) § Conclusion, the report order ending in a pointer to the ledger when a durable artifact exists.
- `causal-identification-review` § Routing, the bundled review-and-estimation split and the Handoff block it attaches.
- `exploratory-data-analysis` § Profile Route, the orientation and entity records as the profile's deliverable, and § Degraded Modes, precommitment emitted as response text without file tools.
- `decision-analysis` § Degraded Modes, the same for the decision frame without file tools.

## Positions

*Proposed: on a route that already requires a record, the record is owed in the form and at the time its owning route sets, and a record that is file-based under its route is also owed retrievable afterwards.*
The form and timing stay with the owning route, including the forms that are not files: the mini route's inline one-paragraph ledger (`skills/hypothesis-driven-analysis/references/ledger-template.md` § Mini Route Template) and the response-text precommitments the EDA and DA § Degraded Modes allow without file tools.
A plan written before the results is the point of those skills; a memo assembled afterwards cannot show that the plan preceded the results, however good the memo is.
The new part is retrievability, and only for file-based records: a file written to a temporary directory, never retained in the workspace and never pointed to, would not meet it, because nobody but the run can check its ordering.
This goes beyond the shipped instructions, which make scratch the default location and whose § Record Delivery requires validation, not retention; an agent following them today can fail this proposal.
A memo-only answer on such a route is scored as a record miss, separately from answer quality, and is not grounds for relaxing the rule.
Beyond the obligations listed above, how much of a retained record the user is shown is left open.

*Alternative: let some asks bypass upstream work.*
Two different things go by "relax the records" and they need keeping apart.
One is bypassing upstream work whose evidence the user supplies: a decision request whose factual question is already settled, with the evidence in hand, needs no upstream investigation, and so no upstream record.
`decision-analysis` § Routing already draws that line between an unresolved adjudication, which hands off, and a choice with evidence in hand, which it decides.
The other is waiving the record for upstream work that still runs; this is what the I4 arms did, and it is the real alternative.
Its strongest form: every I4 plugin arm passed E and C, as did every arm without the plugin, so the extra files bought nothing the final-message scores could see, while costing tokens, time, and file writes for a user who may never open them.
If the skills named a class of ask where the upstream work runs but its record is waived, that exemption would need one home in the skills, per decision 004.
The I4 prompt is not such a class: it asks the agent to determine causation and do the analysis rather than accept either team's interpretation (`skills/hypothesis-driven-analysis/tests/scenarios.md`, Scenario 15), which is unresolved adjudication, not evidence in hand.

## What settles it, if adopted

E and C are scored on the final message, so they cannot see ordering; that they passed whatever records an arm created shows the scoring was blind to the records, not that the records were worthless.
On I2, the plugin condition, with its reserved holdout, held E 3/3 against 0/3 without the plugin; that varies the whole plugin, and the arm without a ledger file also passed E (scores-primary.md line 23), so these runs do not show that the ledger changed the answer.
The case for the record is separate from these runs: a precommitment that a reader can inspect afterwards is the only evidence that the plan came first, and a memo cannot supply it.
No waiver class has been proposed that can be recognised before the results, which is when the record must already exist.

## Scoring columns

The columns are first activation, handoff taken, record written, record written before results, evidence boundary, and task.
Their definitions have one home, the representative-suite preregistration at `docs/evidence/integration/representative-v1/prereg.md`.
That file lands with PR #125 (the #115 work), so this record must not merge before it.

## Open questions for the owner

- The timing boundary for "record written before results" has to be set per owning route: an upstream skill's computed results legitimately precede a downstream skill's record on a correct handoff (EDA results in `I2-codex-plugin-1.jsonl` around line 15 precede the HDA ledger at line 20).
  Its definition belongs in the preregistration, not here.
- When first activation or a handoff is missed, is a record column not applicable under the observed route, or is there a separate measure of records owed under the designed route?
- If the proposal is accepted, reconciling the owning instructions is outstanding work: the scratch-space default in `skills/hypothesis-driven-analysis/references/ledger-template.md` and `skills/exploratory-data-analysis/references/exploration-log-template.md`, and `scripts/shared-sections/record-delivery.md` (rendered into each SKILL.md's § Record Delivery), would need to say where a file-based record is kept or pointed to, in one home per decision 004.
  That change is agent-read prose and owes measured arms under decision 001.
- Is "retrievable" satisfied by a path reported in the final message to a file outside the workspace, or only by a file in the workspace?

## Reopening condition

A proposed class of ask, recognisable from the prompt alone before any results, in which the upstream work runs, memo-only arms and full-record arms score the same on evidence boundary and task across a measured suite, and a record written after the results changes no answer.
Separately, a scoring method that can show ordering from the memo alone would remove the main argument.

## Where the rule lives

The record requirements and the reporting obligations live at the skill sections listed above.
The scoring-column definitions live in the preregistration named in § Scoring columns.
If this proposal is adopted, its retrievability part needs skill-text changes that are not made here (see § Open questions for the owner), and this section then points at their home.
If the alternative is adopted, the exemption gets one home in the skills, and this section points at it.
