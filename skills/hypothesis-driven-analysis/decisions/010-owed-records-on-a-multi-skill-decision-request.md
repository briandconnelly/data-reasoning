# 010 — Which records a multi-skill decision request owes

Status: proposed, 2026-11-24; awaiting an owner decision (issue #119).

## Question

On a decision request whose designed route crosses several skills, some runs deliver only the final memo and none of the intermediate records the earlier skills require.
The answers can still be acceptable.
Are those records part of what the user is owed, or is a memo enough for some asks — and how is a run that skips them scored?

## Evidence

All counts below are copied from `docs/evidence/integration/2026-11-17-full-catalog/results.md` (at `807838a`), n=3 per cell; they are counts, not rates.

- I4 (designed route HDA → (CIR) → DA), Codex plugin arms: "1/3 with ledger, review, and memo; 2/3 read all three skills, wrote a memo only" (Route table, line 18).
- I4, Codex: E plugin 3, E none 3, C plugin 3, C none 3 (E/C table, line 33).
- I2 (designed route EDA → HDA), Codex plugin arms: "2/3 with both records; 1/3 read both, wrote the exploration log only" (Route table, line 16).
- I2, Codex: E plugin 3, E none 0, C plugin 3, C none 3 (E/C table, line 29).
- Across I2–I4, Codex "read every skill of the designed route in 9 of 9 I2–I4 plugin arms, usually several `SKILL.md` files in one shell `cat`, and wrote each skill's record in 6" (line 21).

On I4 the no-plugin Codex arms already passed E and C 3/3, so on that cell the records are most of what the plugin adds.

`docs/evidence/integration/2026-11-18-handoff-fix/results.md` reran Claude Code only; its I4 arms took the designed route 0/3 and loaded no skill in 3/3 (Route table, line 16), so it says nothing about records on I4 and is cited only to rule it out as evidence here.

Measurement limit, from the full-catalog results file's own Limits (line 55): a batched `cat` of several `SKILL.md` files shows that the skill text entered context, not that each skill was followed.
A Codex route read from file reads is therefore an upper bound on what was followed, which is why the records each arm wrote are the stronger evidence.

## Where each route requires a record

Pointers only; the requirement and its conditions live at these lines (as of this record's commit), not here.

- `skills/exploratory-data-analysis/SKILL.md` line 73 (exploration log).
- `skills/hypothesis-driven-analysis/SKILL.md` line 180 (investigation ledger).
- `skills/causal-identification-review/SKILL.md` line 43 (identification review).
- `skills/decision-analysis/SKILL.md` line 128 (decision record).
- Each of the four files' § Record Delivery, rendered from `scripts/shared-sections/record-delivery.md`, for what happens to a record before delivery.

## Positions

*Proposed: the records stay owed wherever a skill's route already requires them.*
A plan written before the results is the point of those skills; a memo assembled afterwards cannot show that the plan preceded the results, however good the memo is.
A memo-only answer on a route that requires records is scored as a record failure, separately from answer quality, and is not grounds for relaxing the rule.
What the user is shown of a record — all of it, a summary, or only a path — is a separate choice this record leaves unconstrained.

*Alternative: relax the records for some asks.*
The strongest form of it: on I4 the memo-only arms passed E and C 3/3, the same as arms with every record, so for a user who asked "should we expand?" the extra files bought nothing visible.
Records cost tokens, time, and file writes; a user who wants a recommendation may reasonably not want a ledger directory.
If the skills named a class of ask — for example, a decision request whose upstream question is already settled in the prompt — where the memo alone suffices, the I4 memo-only arms would become passes and the skills would stop asking for work some users never read.
This position is coherent, and it would need the skills to say so in one place, per decision 004.

## What settles it, if adopted

E and C are scored on the final message, so they cannot see ordering; that they passed in memo-only arms shows the scoring was blind to the records, not that the records were worthless.
On I2 the same host's plugin arms held E 3/3 against 0/3 without the plugin, so where the precommitment can change the answer it did, and a rule that keeps it only when the answer turns out not to need it has to know the answer first.
No relaxed class has been proposed that can be recognised before the results, which is when the record must already exist.
The cost objection is answered by the third clause: the user need not be shown the record.

## Scoring columns

The columns are first activation, handoff taken, record written, record written before results, evidence boundary, and task.
Record columns and answer columns are reported side by side and never combined into one score; an arm can pass evidence boundary and task and fail every record column, which is the I4 memo-only case.
Their definitions have one home, the representative-suite preregistration at `docs/evidence/integration/representative-v1/prereg.md`, which the #115 work creates and which does not exist yet.

## Reopening condition

A proposed class of ask, recognisable from the prompt alone before any results, on which memo-only arms and full-record arms score the same on evidence boundary and task across a measured suite, and on which a record written after the results changes no answer.
Separately, a scoring method that can show ordering from the memo alone would remove the main argument.

## Where the rule lives

The record requirements live at the skill lines listed in § Where each route requires a record.
The scoring-column definitions live in the preregistration named in § Scoring columns.
If this proposal is adopted unchanged, no skill text changes; if the alternative is adopted, the exemption gets one home in the skills, and this section points at it.
