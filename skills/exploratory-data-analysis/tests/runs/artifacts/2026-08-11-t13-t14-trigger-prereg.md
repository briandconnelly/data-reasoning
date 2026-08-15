# Preregistration — T13/T14 two-skill prompted-dispatch seam check

Written before any arm ran.
Revised once, also before any arm ran, after the cross-model design review required by `hypothesis-driven-analysis/tests/PROTOCOL.md` step 3; the review's findings and their dispositions are archived in this wave's harness-evidence artifact.
This wave runs the entity minimal pair T13/T14 from `tests/scenarios.md` with a catalog carrying both this skill's description and `hypothesis-driven-analysis`'s.
It is the first measurement of these scenarios and the first trigger measurement of any kind with a competitor description present.

## What this wave measures, and what it does not

This wave measures **prompted dispatch**: which skill a fresh arm declares and consults when a stated two-entry catalog is placed in its first message and it is required to announce a route.
It does not measure deployment activation (no real skill installation, no plugin catalog), and it does not measure route behavior (the prompts carry no data, so no fixture-backed exploration or investigation can occur).
Behavior assertions are deferred to a fixture-backed wave; `tests/fixtures/` does not exist yet for this skill.

## Step 0: the owed measurement exists and is unrun

- `decisions/003-entity-profiling-in-scope.md` names the debt: "The post-deployment spot check — corpus-shaped queries with all four skills installed, the only test where inter-skill competition is real — is owed and not done", and names T13/T14 as the preregistered entity minimal pair that narrows it.
- `tests/scenarios.md` opens "Status: authored only — no arm has run, and nothing below is a result."
- `tests/runs/` did not exist in this skill before this wave (`ls skills/exploratory-data-analysis/tests/runs` → no such directory, checked 2026-08-11 at `4efdeec`).

This wave carries two descriptions, not four, and its queries are synthetic, so it **narrows the debt rather than discharging it**.
Issue #5 records the debt as still owed; the plan agreed there runs this wave against the current shipped description, before any description edit.

## Question under measurement

When both descriptions are presented, which route does a fresh arm declare for an entity-profile ask (T13) and for a named-effect ask on the same entity (T14)?
Every prior number for this skill was measured with no competitor present, so `N1 = 0.000` in `tests/eval/` says nothing about collision.
The competing readings this wave discriminates:

- The descriptions partition the pair cleanly (each scenario routes to its expected skill).
- EDA's entity clause leaks into named-effect territory (T14 misses toward EDA).
- HDA captures entity-story asks (T13 misses toward HDA) — its description carries an explicit collision clause ("Use it even when an analytics or data-access skill is also loaded and claims the ask").
- The pair confuses both ways, or arms decline both.

## Cells

Two scored cells of five reps, two excluded rationale canaries, three excluded instrument smoke tests.

| Cell | Prompt (verbatim) | Reps | Scored |
| --- | --- | --- | --- |
| T13 | "Tell me about the Northgate Clinic account." | 5 | yes |
| T14 | "Why did the Northgate Clinic account's spend drop last quarter?" | 5 | yes |
| T13-canary | same prompt as T13 | 1 | no — rationale canary |
| T14-canary | same prompt as T14 | 1 | no — rationale canary |
| c-eda / c-hda / c-none | planted EDA positive, planted HDA positive, known negative | 1 each | no — detector smoke tests |

- Model: `claude-opus-5`, fresh `claude -p` process per rep — processes, not forks, no shared context.
- Harness: `tests/run_trigger.py` on this branch; full `stream-json` transcript archived per rep as JSONL; scratch directories outside the repository, enforced by the harness before launch.
- Catalog: both descriptions stated in the arm's first user message as `**<skill-name>**` + `Description:` entries, parsed live from each `SKILL.md` frontmatter at dispatch.
- Catalog order is counterbalanced within each scored cell: odd reps EDA-first, even reps HDA-first; order is recorded per rep and reported alongside every count.
- Each arm is required to emit a machine-readable first line — `ROUTE: exploratory-data-analysis`, `ROUTE: hypothesis-driven-analysis`, or `ROUTE: none` — before its first tool call, followed by one or two sentences of rationale.
- Neither prompt names a fixture; arms are expected to declare a route and ask for data. Dispatch, not task completion, is what is scored.
- Reps per cell: five, because the description eval surfaced intermediate per-query rates (0.33) that three runs cannot distinguish from noise. Five reps is **screening precision**: 0/5 has a two-sided 95% Clopper–Pearson upper bound of 0.522, and 4/5 spans roughly 0.28–0.99. No outcome of this wave supports a reliability claim about a stable pass rate.

## Dispatch constructs

Three separate signals per rep, never combined with OR:

- **selected** — the route named by the parsed `ROUTE:` token. The primary construct; every scored count is over this signal. A missing or malformed token is `unclear`, classified manually from the archived JSONL with the manual call quoted in the run file.
- **consulted** — which `SKILL.md` files the arm read. Process evidence only: reading a candidate to decide against it is legitimate dispatch, so consultation never counts for or against activation.
- **executed** — Write events and route ceremony in the transcript. Recorded, not scored, because no data exists for any route to execute on.

## Scored assertions

- T13-A1: selected = exploratory-data-analysis, and selected ≠ hypothesis-driven-analysis. Per rep; cell result is the clean count out of 5.
- T14-A1: selected = hypothesis-driven-analysis, and selected ≠ exploratory-data-analysis. Per rep; cell result is the clean count out of 5. (Symmetric by design: an arm declining both skills does not satisfy T14.)

Recorded, not scored: consulted and executed evidence per rep, including the `scenarios.md` observations "no leads chased" (T13) and "no exploration log is created" (T14) — with no data present these are expected to hold trivially, so they are reported as observations and carry no evidential weight for route behavior.
Not re-scored this wave: every number in `tests/eval/` (single-description, different instrument), and every behavior assertion (B1–B10).

## Gates, in precedence order

Evaluated top-down; the first gate that fails determines the wave's disposition and nothing below it is interpreted.

1. **Harness validity.** Every scored rep must have a valid transcript (parseable JSONL, model and session recorded, ≥1 assistant event, a result event, exit 0). An invalid rep is void: excluded and rerun once with a disclosed rerun suffix; two invalid attempts for the same rep void the cell.
2. **Instrument smoke tests.** c-eda must parse to `eda`, c-hda to `hda`, c-none to `none`. A detector that cannot surface a planted positive for each skill, and a clean negative, voids every zero in the scored cells; fix and rerun the wave in full.
3. **Rationale canaries.** One excluded rep of each scored cell runs first and is scored by hand on rationale and on detector agreement: the stated reasons must engage the descriptions (not merely echo the prompt), and the manual reading of the transcript must match the detector's `selected`. Disagreement or degenerate rationale returns the wave to design; scored reps do not run.
4. **Wording fixed.** `git diff` over both `SKILL.md` files must be empty across the whole wave, and each invocation manifest must show both parsed descriptions byte-identical to the frontmatter at the recorded git SHA.
5. **Ambiguity.** If ≥2 scored reps in a cell are `unclear` after manual classification, that cell's count is not computed; both signals are reported per rep and the cell is disposed as "instrument insufficient", feeding a harness revision, not a routing conclusion.

## Outcome classification

Applied only when every gate passes.
Each scored rep is classified on `selected` into: expected-skill, competitor, none, unclear.
Each cell then lands in exactly one row:

| # | Cell outcome (per cell) | Disposition |
| --- | --- | --- |
| 1 | ≥4/5 expected | No collision detected at screening precision in this cell. |
| 2 | ≤3/5 expected, misses predominantly competitor | Collision toward the competitor; see cross-cell table. |
| 3 | ≤3/5 expected, misses predominantly none | The pair under-claims: arms decline both skills; feeds description work, not boundary work. |
| 4 | Misses split between competitor and none with no predominant direction | Mixed failure; report per-rep table, no single mechanism claimed. |

Predominant = strictly more misses of that kind than the other kind.
Cross-cell disposition:

| T13 row | T14 row | Wave disposition |
| --- | --- | --- |
| 1 | 1 | **Nothing ships from this wave.** The seam shows no collision at screening precision; the issue-#5 plan proceeds unchanged. |
| 2 | 1 | Entity-profile asks leak to HDA under prompted dispatch. Deployment-relevant datum for issue #5 item 1; the description-fix A/B gains a dual-install repeat obligation on T13. |
| 1 | 2 | EDA overtriggers on named-effect asks. Reopens the boundary in `decisions/003`; the description fix must not widen the trigger surface before this is understood. |
| 2 | 2 | Catalog-level confusion; escalate to protocol design before any description edit ships. |
| any 3 or 4 | any | Report per-rep tables; disposition is written against the observed pattern and labelled post hoc, because these rows carry heterogeneous mechanisms a 5-rep screen cannot separate. |

The first row is reachable with no change existing anywhere; this wave can ship nothing.

## Known non-independence (disclosed, not corrected)

T14's prompt is near-identical to the counter-example phrase the EDA description itself carries ("why did this account's spend drop") and to the N1 eval query built from it.
A T14 pass is therefore weak evidence about the exclusion clause in general — `decisions/003` records the same caveat for N1 — but it is the preregistered pair and is run as written.

## Contamination controls and limitations

- Fresh `claude -p` processes; no arm shares context with this session or with another arm.
- Arms run with cwd outside the repository (harness-enforced), so the repository's `CLAUDE.md`/`AGENTS.md` are not loaded; the operator's user-global configuration is present identically in every arm, as in the `tests/eval/` runs, and is disclosed rather than removed.
- Arms are prohibited from reading anything under either skill's `tests/`; the prohibition is in the dispatch prompt and checked post hoc from each JSONL manifest.
- Assertions, expected routes, and this document are not revealed to any arm.
- The forced route declaration is part of the treatment: it measures prompted dispatch, not spontaneous skill selection, and may suppress or surface `none` differently than deployment would.
- Dispatch prompts, their SHA-256 digests, both `SKILL.md` digests, per-invocation manifests, and all JSONL transcripts are archived under `tests/runs/artifacts/`.

## Results

Appended after all arms ran; nothing below this line existed before the wave.
All arms ran 2026-08-11 (UTC 18:22–18:55); archive: `2026-08-11-t13-t14-trigger/`.

Gates: 1 PASS (one void — t14-rep1 timed out at 600s with no result event, disclosed and rerun once as `t14-rep1-r2`, valid); 2 PASS (c-eda→`eda`, c-hda→`hda`, c-none→`none`); 3 PASS (both rationale canaries engaged the descriptions and matched the detector; hand-scoring quoted in the run files); 4 PASS (`git diff` empty over both `SKILL.md` across the wave; all manifests record `4efdeec`); 5 PASS (zero `unclear` after manual review).

| Cell | selected = expected | Outcome row |
| --- | --- | --- |
| T13 | 5/5 `exploratory-data-analysis` | 1 |
| T14 | 5/5 `hypothesis-driven-analysis` | 1 |

**Verdict: cross-cell row 1/1 — no collision detected at screening precision; nothing ships from this wave.**

Deviations and unpreregistered observations, detailed in the run files: three T13 reps (1, 3, 5 — all eda-first) emitted the ROUTE token only after one to three initial Bash calls, a compliance deviation that does not affect classification (each token is present and unambiguous, verified manually against the transcript); arms used Bash although it was absent from `--allowedTools`, confirming that flag gates approval, not availability; every valid T14 arm wrote an HDA-style ledger and none wrote an exploration log, so the preregistered negative observation holds trivially, as expected with no data present.
