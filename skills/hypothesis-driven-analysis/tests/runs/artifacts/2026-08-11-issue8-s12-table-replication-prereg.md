# Preregistration: S12 summary-table replication (issue #8) — 2026-08-11

Written before any arm ran.
This wave replicates the S12 Sonnet-as-main-agent cell from `2026-08-10-sonnet-mainagent-wave-prereg.md` to test one thing: does the missing per-hypothesis summary table recur?
It holds the skill wording fixed (verified: `git diff 79248f5..HEAD` on `SKILL.md` and `references/ledger-template.md` is empty) and ships no edit; the rerun-obligation rules in `PROTOCOL.md` do not apply.
Step 0 verification: the archived arm ledger `2026-08-10-sonnet-mainagent-s12-ledger.md` was re-read this session and contains no per-hypothesis summary table; statuses are carried in Analysis/Conclusion prose.
The issue's premise holds.

## Question under measurement

Issue #8 offers two readings of the 2026-08-10 S12 form miss:

1. The rule (`SKILL.md` Conclusion, the summary-table sentence) is findable and the arm dropped it — replication shows recurrence.
2. The rule is under-signposted (the template's table stub is not prominent enough for an agent composing its own ledger) — the fix is structural.

This wave measures recurrence and, separately, whether arms read `references/ledger-template.md` at all.

## Cells

Three identical arms: S12-sonnet-rep1, rep2, rep3.
Each is a fresh Sonnet general-purpose subagent, no conversation context, given the committed S12 prompt with absolute paths, told the skill file to read and follow, forbidden from reading `tests/scenarios.md` and anything under `tests/runs/`, told to write working files to a per-arm scratch directory outside the repo.
Nothing in any prompt names the summary table, the ledger template, the assertions, issue #8, or this file.

## Scored assertion (one per arm, binary)

- The arm's ledger or final report contains a per-hypothesis summary table whose `status` column holds `REFUTED` or `UNRESOLVED` alone (the `SKILL.md` Conclusion closed-set form).

Status *decisions* (which hypothesis gets which status) are not re-scored this wave; they were scored 2026-08-10 and are not in question.

## Secondary observation (recorded, not scored)

- Whether the arm read `references/ledger-template.md`, established by a post-hoc query to the finished arm ("list every file you read during the task"), sent only after the arm's final report is complete.
- This is self-report and is labelled as such in the run files; the query does not name the template.

## Reachable verdicts (all rows written before any arm ran)

1. **Table present in 3/3.** The 2026-08-10 miss does not recur; close issue #8 with the n=1 note the issue itself proposes. No change ships.
2. **Table absent in ≥2/3, template unread in the missing arms.** The discoverability reading is supported; next step is a structural fix designed under the full protocol (which owes arms if agent-read prose changes). No change ships from this wave.
3. **Table absent in ≥2/3, template read.** Recurrence without a discoverability cause; the rule is findable and still dropped. Record that as the finding — the fix question becomes wording emphasis or model capability, not template structure. No change ships from this wave.
4. **Table absent in exactly 1/3.** Ambiguous at n=3 (with the 2026-08-10 arm, 1–2 misses in 4 total). Record the split; whether more reps are worth the spend is reported to the user as a judgement call with the counts, not decided by this prereg.
5. **An arm voids for a harness or fixture reason** (wrong path, tool denial, budget exhaustion). That arm is void, not a miss; rerun it once.
6. **The wave turns out unnecessary or partial** (user redirects, dispatch fails). Record what ran; partial waves are reported as partial.

Rows 1–4 all end with "no wording change ships from this wave"; this measurement decides what issue #8 becomes, never prose.

## Contamination controls

- Fresh subagents, not forks.
- Each prompt names only: the scenario prompt, the skill path, the fixture path, the scratch dir, and the two forbidden paths.
- The post-hoc file-read query is sent after the arm's report is final, so it cannot shape the arm's ledger.

## Results (appended after all arms ran and were scored)

Run file: `../2026-08-11-scenario12-sonnet-table-replication.md`; arm ledgers archived beside this file as `2026-08-11-issue8-s12-rep{1,2,3}-ledger.md`.

| Arm | Table present | Template read (self-report) |
| --- | --- | --- |
| rep1 | yes | yes |
| rep2 | yes | yes |
| rep3 | yes | yes |

**Verdict: row 1** — the table appears in 3/3 arms; the 2026-08-10 miss does not recur.
Per row 1 as preregistered: issue #8 closes with the n=1 note; no change ships.
The secondary observation (all three arms read the template) additionally undercuts the under-signposting reading: the template is found, and its stub is followed when found.
One unpreregistered observation, recorded in the run file and not scored here: reps 1 and 3 marked the causal H1 `REFUTED` from a pre/post aggregate contrast, which the committed S12 assertion 5 would have failed; that is a status-decision question outside this wave's scope and is filed separately.
