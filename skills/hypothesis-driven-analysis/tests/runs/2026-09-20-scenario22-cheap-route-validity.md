# Scenario 22 — data validity on `mini` and `direct`, 2026-09-20 wave (issue #38)

Preregistration: `artifacts/2026-09-20-cheap-route-validity-prereg.md` (cells, assertions, verdict rows, amendments 1 and 2).
Design review: `artifacts/2026-09-20-cheap-route-validity/design-review.md` (two Codex passes before any arm).
Harness: `../run_arm.py` through `artifacts/2026-09-20-cheap-route-validity/run_wave.sh`; every arm's prompt, command, transcript, manifest, and written files are under `artifacts/2026-09-20-cheap-route-validity/`.
Model: `claude-sonnet-5` on all 28 arms (manifest `model`); Claude Code 2.1.278; every arm exited 0 with an empty `contaminated` list, so no arm is void.
Skill under test: pre = `main` at `f4c5093`; post = the working tree at `6ec2dd6`, whose staged `SKILL.md` (+15 −1) and `references/ledger-template.md` (+1) carried the draft wording and were the only skill files differing from `main` (each manifest's `skill_files_sha256` is the proof).
That is the run-time state; the branch as committed has both files reverted to `main`, with their diff archived as `artifacts/2026-09-20-cheap-route-validity/draft-wording.patch`.
Scorer: the dispatching session (Fable); every quote below was grepped against the named archive file with `artifacts/2026-09-20-cheap-route-validity/verify_quotes.py`.

## Result in one paragraph

Issue #38's textual finding holds: on `main`, nothing on `mini` or `direct` asks whether the rows are the right rows.
Its behavioral prediction did not reproduce.
On four cells that each plant one fault on which the answer turns — a duplicating join on `mini` and on `direct`, an export that stops on 11 June, and a region-shaped hole inside a whole quarter — all twelve scored arms found the fault and none settled the claim on the wrong rows: the four no-skill baselines, the four arms on `main`'s wording, and the four arms on the draft wording.
Every new cell lands on row 5, which under the rules written before any arm ran means no wording ships as measured.
When this record first shipped the regression wave was partial — S15 had been machine-checked on C1 only — so the decline was the conservative reading of an unclosed wave.
S15 has since been scored in full (issue #43, § Regression cells): it lands on row 9 with no regression, every cell now ends on a terminal row, and the wave-level rule written in advance fires as the decline already read — S22a–c all on row 5, so nothing ships as measured.
The draft wording is declined (`../../decisions/008-cheap-route-data-validity.md`); the fixture, the catalog entry, and this record ship.

## Scored table — new cells

| # | Assertion | baseline | pre | post |
| --- | --- | --- | --- | --- |
| S22a.1 | One claim, no hypothesis table | PASS — no skill, no table | PASS — one ledger, no table | PASS — one ledger, no table |
| S22a.2 | Says the account table repeats keys | PASS — "`accounts.csv` has 70 rows for 60 accounts." (s22a-baseline.manifest.json) | PASS — "Joining orders straight to that file repeats the orders of those accounts." (s22a-pre.manifest.json) | PASS — "A plain join of orders to accounts repeats each order once per row." (s22a-post.manifest.json) |
| S22a.3 | Verdict FALSE | PASS | PASS — "Outcome: CONTRADICTED (deterministic sum over the complete ledger" (s22a-pre.scratch/ledger.md) | PASS — "Outcome: CONTRADICTED. Enterprise Q2 = $925,797.78 over 199 orders" (s22a-post.scratch/ledger.md) |
| S22a.4 | $925,797.78 ± $1,000 | PASS — "| Enterprise | $925,797.78 | 199 |" (s22a-baseline.manifest.json) | PASS | PASS |
| S22b.1 | One claim, no hypothesis table | PASS | PASS | PASS |
| S22b.2 | Says where the rows stop | PASS — "The timestamps stop at 2026-06-11 09:55 UTC." (s22b-baseline.manifest.json) | PASS — "The last order is 2026-06-11 09:55Z." (s22b-pre.manifest.json) | PASS — "orders run from 2026-04-01 to 2026-06-11 09:55 UTC." (s22b-post.manifest.json) |
| S22b.3 | Verdict neither FALSE nor TRUE | PASS — "the claim is plausible but unproven." (s22b-baseline.manifest.json) | PASS — "Outcome: NON_DISCRIMINATING on the file alone" (s22b-pre.scratch/ledger.md) | PASS — "Outcome: NON_DISCRIMINATING on the file as given." (s22b-post.scratch/ledger.md) |
| S22b.4 | $862,691 labelled as the recorded rows' total | PASS — "**Total in file**" (s22b-baseline.manifest.json) | PASS — "**Total in file**" (s22b-pre.manifest.json) | PASS — "the 10,000 rows sum to **$862,691.37**" (s22b-post.manifest.json) |
| S22b.5 | Completeness not asserted as settled | PASS | PASS — "I can't confirm that from the file." (s22b-pre.manifest.json) | PASS — "nothing in the file confirms it." (s22b-post.manifest.json) |
| S22c.1 | `direct`: no ledger, hypothesis table, PPDAC headings, or validity record | PASS | PASS | PASS |
| S22c.2 | $925,797.78 ± $1,000 | PASS | PASS | PASS |
| S22c.3 | Says a plain join overstates | PASS — "**A plain join would have overstated Enterprise revenue.**" (s22c-baseline.manifest.json) | PASS — "A naive join on `account_id` would have counted orders on the duplicated accounts more than once" (s22c-pre.manifest.json) | PASS — "A plain join repeats their orders." (s22c-post.manifest.json) |
| S22d.1 | One claim, no hypothesis table | PASS | PASS | PASS |
| S22d.2 | Locates the hole by region and date | PASS — "**The problem is that EMEA has no orders from June 3 through June 16.**" (s22d-baseline.manifest.json) | PASS — "EMEA has **zero orders from 2026-06-03 through 2026-06-16**" (s22d-pre.manifest.json) | PASS — "EMEA has zero orders on every day from 2026-06-03 to 06-16." (s22d-post.manifest.json) |
| S22d.3 | Verdict neither FALSE nor TRUE | PASS — "I'd hold off on calling the claim false" (s22d-baseline.manifest.json) | PASS on the report — "so I can't say the claim is false." (s22d-pre.manifest.json); see the note below on its Outcome cell | PASS — "Outcome: NON_DISCRIMINATING. Recorded total ($972.5k) is below $1M" (s22d-post.scratch/ledger.md) |
| S22d.4 | $972,510 labelled as the recorded rows' total | PASS — "Not on this export: it totals $972,510.46" (s22d-baseline.manifest.json) | PASS — "the 11,971 orders sum to **$972,510.46**" (s22d-pre.manifest.json) | PASS — "The export sums to $972,510.46" (s22d-post.manifest.json) |

Totals: every arm passes every assertion on every new cell.

## Verdict rows

| Cell | Component | Row | Skill needed vs baseline |
| --- | --- | --- | --- |
| S22a | join handling on `mini` | **5 — not needed** | no |
| S22b | unresolved-completeness disposition on `mini` | **5 — not needed** | no |
| S22c | join handling and reporting on `direct` | **5 — not needed** | no |
| S22d | segment-shaped coverage hole on `mini` | **5 — not needed** | no |

Row 5 means what it said before any arm ran: no incremental behavior observed on this cell and arm, and the text carries no measured behavioral claim there.
The wave-level rule for this case was also written in advance: nothing ships as measured, and the text is the owner's call.
By the catalog's own standard the scenario is still too easy — every baseline passes — after the one tightening round amendment 2 allowed itself.
S22d is adaptive evidence: it was specified after S22a–c's results were read and before any S22d arm ran, which prevents choosing among packets but is not the same as belonging to the original preregistration.

## The one scoring call that was not mechanical

S22d.3 scores "the verdict on the claim".
The pre arm's report to the user is unambiguous — "Can't settle from this data alone." (s22d-pre.scratch/ledger_mini.md) — and it passes on that.
Its ledger's Outcome cell, though, reads "Outcome: as exported, CONTRADICTED ($972.5k < $1M). But the export fails the coverage precondition" (s22d-pre.scratch/ledger_mini.md), where the post arm's reads `NON_DISCRIMINATING`.
The same shape shows on S11: pre records "Outcome: CONTRADICTED for the covered 00:00-19:59Z window. For the claim as stated (whole day), NON_DISCRIMINATING in the strict sense" (s11-pre.scratch/ledger.md), while post records "Outcome: CONTRADICTED on covered 20h (CI entirely below 500), conditional on missing 20:00-23:59Z resembling covered hours." (s11-post.scratch/ledger.md) with a line headed "Crossing requirement" above it.
So the draft's disposition sentence appears to tidy what goes in the Outcome cell on `mini` when coverage is unresolved: one label, with its condition, instead of two labels and a hedge.
That is an observation at n=1 on two cells, made after the arms returned, against no preregistered assertion, and it is claimed as nothing.
It is recorded because it is the most specific thing a future wave could preregister: score the Outcome cell's single label, not the report's verdict.
If S22d.3 were rescored on the Outcome cell alone, S22d would land on row 6 for that component; the preregistered assertion says "verdict".
The step-7 review was asked to adjudicate the reading without tilting either way and held that both arms pass: the assertion scores the claim-level verdict, the pre arm scopes `CONTRADICTED` to "as exported" and then withdraws it, and S22d stays on row 5 (`artifacts/2026-09-20-cheap-route-validity/design-review.md` § Step 7).

## Regression cells

| Cell | pre | post | Row |
| --- | --- | --- | --- |
| S11 (mini) | S11.1–3 pass; answers the claim is not supported at p95 392ms, with the 20-of-24-hour coverage as a limitation | S11.1–3 pass; same answer, as conditional on the absent hours, with the crossing requirement computed (25% needed against 1.2% covered, 3.3% worst hour). S11.4: the ledger carries a `Data validity` entry | **10 — no regression** |
| S13 (mini) | S13.1–3 pass — "**The claim doesn't hold.**" (s13-pre.manifest.json), returning slice 438.6ms, new-user slice 804ms | S13.1–3 pass — "The claim doesn't hold as stated." (s13-post.manifest.json) | **10** |
| S2 (direct) | S2.1–2 pass; median 76.36 over 1–14 June, coverage gap stated in the answer; no file written | S2.1 passes, same figure and the same coverage statement; **S2.2 fails on the amendment-1 reading**: the arm wrote `notes.md`, a record headed "(route: direct)" with the line "Completeness semantics for absent days: UNKNOWN (no export contract/sentinel)." (s2-post.scratch/notes.md) | **3 — regression**, with a confound named below |
| S14 (direct) | S14.1–4 pass; collection plan written in the same command as, and ahead of, the first metered query; 30 queries, no re-pull | the same, and it reuses the 06-01 orientation call as that day's data | **10** |
| S9 (estimation) | S9.1–3, S9.4a–b pass | S9.1–3, S9.4a–b pass — "S1: UNKNOWN — no export contract or independent count" (s9-post.scratch/estimation_record.md) | **10** |
| S15 (full) | scored in `artifacts/2026-09-20-cheap-route-validity/s15-scoring/scoring.md` | the same; the ledger applies the new § Plan sentence — "reconcile 420 = 409 matched + 11 unmatched." (s15-post.scratch/ledger.md) | **9 — shared catalog failure**; post fails nothing pre passes |

The S2 row is a regression by the letter of the clarification this wave wrote for itself, and it is reported as one.
The confound: the harness frame tells every arm to "Write any working files you produce (notes, logs, records, intermediate results)" to scratch, the S22c pre arm also wrote a results file on `direct`, and S2's answer to the user is the same in both arms.
What differs is that the post arm's notes carry the full route's completeness vocabulary on a bounded descriptive query, which is the ceremony creep the `direct` guardrail exists to catch.
The observable line drawn here, and applied to S22c as well: raw calculation output an arm saves (`result.txt`, `enterprise_q2_2026.txt`, `notes.txt` on the S22c arms) is a working artifact; a structured analysis note naming its route and carrying completeness-semantics vocabulary is a record.
At n=1 it is one draw; it points the same way as the rows 5.

S15 shipped in this record machine-checked on C1 only, and was scored in full afterwards under issue #43: `artifacts/2026-09-20-cheap-route-validity/s15-scoring/scoring.md` holds the recovered Plan-time ledgers, every instrument's output, the per-assertion table with quotes, and the two places where its two scorers (this session and Codex, working separately) differ.
Both arms fail the same catalog assertion and post fails none that pre passes, so the cell is row 9; the assertions, the quotes, and the scorers' differences are in that file and are not repeated here.
On the join sentence the cell reads as S22a and S22c do: the reconciliation post's ledger names was run, in part, before the plan was written, and the pre arm ran the same counts unasked, so the sentence changed the ledger's text and not the arm's behavior.
This closes the wave and does not reopen the decline; what a join rule proposed again would owe is `../PROTOCOL.md`'s to say (§ What owes a rerun), not this record's.

## Correctness and cost

Every new-cell arm reports the ground-truth figure to the cent: $925,797.78 (S22a, S22c), $862,691.37 (S22b), $972,510.46 (S22d).

| cell | arm | tool calls | output tokens | wall clock |
| --- | --- | --- | --- | --- |
| S22a | baseline / pre / post | 4 / 6 / 6 | 1,986 / 3,449 / 3,556 | 22 / 40 / 40 s |
| S22b | baseline / pre / post | 4 / 5 / 6 | 2,463 / 3,742 / 4,475 | 29 / 44 / 51 s |
| S22c | baseline / pre / post | 4 / 4 / 4 | 1,853 / 2,453 / 2,805 | 22 / 27 / 32 s |
| S22d | baseline / pre / post | 5 / 6 / 7 | 3,305 / 5,157 / 5,854 | 37 / 58 / 68 s |

The skill costs 32–74% more output tokens than no skill on these cells for the same answer, and the draft wording a further 3–20% over `main`'s.

## What this does not show

n=1 per arm, one model, one day.
It does not show that `mini` and `direct` are safe on the wrong rows in general: it shows that `claude-sonnet-5` profiles keys, date ranges, and day-by-region coverage unprompted on small local CSVs, with or without the skill.
A weaker model, a fault that needs domain knowledge to see (the wrong revenue definition, which issue #38 also names and no packet here plants), or data behind a query interface where profiling is not free are all unmeasured.
The pre arms on S22d and S11 built a coverage view that nothing on `mini` asks for, so the premise that "every obligation the skill states" can be satisfied on the wrong rows stays true on the page and unobserved in behavior.
