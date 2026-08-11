# Preregistration — description veto fix and its measurement (issue #5)

Written before any arm of any phase ran.
Revised once after the cross-model design review required by `hypothesis-driven-analysis/tests/PROTOCOL.md` step 3 — eleven findings, all applied — still before any arm ran.
This document is the single home for this wave's estimands, designs, gates, and stopping rules; run files and decision records point here and do not restate them.
The gates' computation has exactly one implementation, `analyze_ab.py`, committed before any arm; on any disagreement between prose and that script, the script as committed is authoritative and the disagreement is disclosed.
The Iron Law binds: every result belongs to the exact wording it is measured against.

## Step 0: the premises, re-derived

Verified against the repository before this document was written:

- The compression in PR #4 changed the exclusion's object: `SKILL.md@a772557` read "or for summarizing prose documents"; the shipped text reads "or prose summarizing". The change is real.
- Issue #5's proposed restoration does not fit: the description is 1019/1024 characters, and restoring "for summarizing prose documents" costs +14 ("summarizing prose documents" alone costs +10). The issue's "5 characters with 5 to spare" claim is arithmetically wrong.
- The per-query rates the issue cites match `results-edited.json` exactly, and its statistical figures reproduce (Clopper–Pearson 0/3 two-sided upper 0.708, one-sided 0.632; Fisher 2/3 vs 0/3 p = 0.40).
- The two-skill prompted-dispatch seam check ran first, against the shipped text: T13 5/5 and T14 5/5 to the expected skills (`../runs/2026-08-11-t13-trigger.md`, `-t14-`, merged into this branch at `63df79f`), so no collision problem needs untangling before a description edit.

## The change under test

One word-order swap in the description's final clause: "or prose summarizing" → "or summarizing prose".
It restores a verb-plus-object reading (the thing not to summarize is prose) at zero character cost — both texts are 1019 characters — leaving every other character identical, so the edit is single-variable.
The mechanism hypothesis, from issue #5 item 1: the activity-veto reading conflicts with the description's positive claim of an entity "whose story is wanted", and that conflict suppresses the overview/rundown/context/tell-me-about phrasings that dominate the 0.33 tier.

Frozen texts, committed before any arm:

- Baseline (shipped): `frozen-2026-08-11-baseline.txt` — byte-identical to `frozen-description.txt`, which stays untouched per `README.md`.
- Treatment: `frozen-2026-08-11-treatment.txt`.

The committed files are authoritative; every instrument records the sha256 of the description string it actually served, and the analysis rejects any row whose digest matches neither frozen file (after stripping the file's single trailing newline).

## Estimands

- **Primary: isolated triggerability** — the probability the description triggers on a query with no competitor present. Chosen primary because it attributes change to the edit alone.
- **Secondary: prompted-dispatch seam** — which skill a fresh arm selects with both descriptions stated, measured by `../run_trigger.py` as in the 2026-08-11 T13/T14 wave (this branch, merged at `63df79f`). A routing check, not an attribution instrument.

Historical results (`results-baseline.json`, `results-edited.json`) are reference only: they carry no run metadata and were produced by an instrument that scores invalid executions as non-triggers, so treatment-versus-history differences cannot be attributed to wording.
Every comparison below is between arms run contemporaneously by the same operator on the same model with the instruments below.

## Instruments, frozen before any arm

- `run_desc_eval.py` (this directory, this branch): single-description trigger harness that mirrors `skill-creator` `run_eval.py`'s detection signal but (a) passes the frozen rendered text directly, recording its sha256 in every result row; (b) archives every invocation's stream-JSON transcript and stderr; (c) classifies timeout, nonzero exit, unparseable stream, or missing result event as **void**, never as non-trigger; (d) retries a void invocation at most twice, immediately, archiving all attempts; (e) interleaves the two descriptions at matched-pair query level — for each query in a seeded pseudo-random order, both arms run back-to-back, alternating which goes first by (query index + run) parity — recording ordinal, timestamp, and which-first per invocation.

  **Termination semantics.** Detection is decisive: the reference implementation stops the session the moment the first tool-use decides the outcome, and this harness does the same. An invocation is therefore `valid` when either the session completes normally with a result event, or detection reached a decisive verdict and the harness terminated the session itself; `void` covers only timeout, nonzero exit, or unparseable stream *before* a decisive verdict. Every transcript records which of the two valid endings occurred.

  Waiting for full completion instead was considered and rejected before any arm ran: these queries name data that does not exist, so a triggered session can flail searching for it (one arm of the 2026-08-11 seam wave spent its entire 600 s that way). Because triggering sessions run longest, a completion-wait design would void preferentially in the arm the wave is about, converting a measurement into an expensive completeness failure. Early termination removes that differential hazard and matches the semantics under which every historical number was produced.
- `analyze_ab.py` (this directory, this branch): the single computational home for completeness checks, arm means, gates, verdict, paired per-query differences, order diagnostics, mechanism mean, and tag breakdowns. It fails loudly (exit 2) if any (query, arm) has fewer than 3 valid invocations or any duplicate rows.
- Arm membership is read from the fixture's own `arm` field (P1 = 20, N1 = 10, P0 = 8, N2 = 6, F = 6); no reconstruction is performed and no separate arms file is authoritative.

The known parser defect in `skill-creator`'s harness (single-quoted YAML descriptions are not unescaped) is avoided entirely: no instrument in this wave parses the description out of YAML.

## Phase A — fixture A/B (development-set screen, primary estimand)

- Fixture: the frozen 50-query `entity-profiling-eval.json`, unchanged. It is outcome-inspected, so Phase A is a **screen and regression suite**, not confirmatory evidence, and its ship verdict is a **provisional engineering acceptance**, not a measured no-harm finding — Phase C is the post-ship check with a preregistered reopen rule.
- Arms: baseline and treatment frozen texts, both served by `run_desc_eval.py` in one invocation (matched-pair interleaving as specified under Instruments), model `claude-opus-5`, `--runs 3`, `--timeout 390`, fixed `--seed 20260811`, strictly sequential.
- Canary invocations, excluded from scoring, run first and gate the phase: the four 0.33-tier queries, plus two canary-only probes of the clause under test, authored here and deliberately absent from the fixture, which contains no prose-summarization query (its only summarization query, `Summarize the dataset in ./circulation.csv.`, is a dataset summary the description explicitly claims):
  - prose probe — "Summarize this staff report on branch renovations for me."
  - dataset probe — "Summarize what's in the circulation export."

  One invocation per description for each of the six, archived. The operator reads the canary transcripts and records whether any visible routing rationale engages the summarizing clause, and whether the detector's trigger signal matches a manual reading. If canary transcripts contain no rationale text (plausible for `-p` runs), that is recorded and the canaries still serve as live instrument checks; a detector/manual disagreement voids the phase before scored arms. The probes are never scored and never enter any arm mean: under both descriptions the prose probe is expected not to trigger and the dataset probe to trigger, and a reversal is recorded as an observation about the clause, not as a gate.
- Stopping rules: the scored batch is exactly 50 queries × 2 arms × 3 valid runs. Voids surviving 3 attempts leave the batch incomplete; `analyze_ab.py`'s completeness gate then blocks any result inspection, and the operator runs one disclosed top-up pass covering only the incomplete (query, arm) cells. At most one top-up; further incompleteness voids the phase. No result is inspected before completeness passes.

Gates, evaluated strictly top-down by `analyze_ab.py`; the first failure determines the verdict and nothing below it is evaluated:

1. **Instrument** — baseline P0 mean ≥ 0.8, else verdict VOID (fix instrument, rerun phase).
2. **No harm** — treatment P0 ≥ 0.8; treatment N1 ≤ 0.2 and ΔN1 ≤ +0.10; treatment N2 ≤ 0.2 (bounds inherited from `decisions/003` Gate 3), else verdict NO_SHIP_HARM.
3. **Ship** — ΔP1 ≥ 0, else verdict NO_SHIP_REGRESSION; otherwise verdict SHIP.

Shipping therefore requires gates 1 and 2 to pass and ΔP1 ≥ 0.
Gate arms are the fixture's preregistered arms at their existing sizes (P0 = 8, P1 = 20, N1 = 10, N2 = 6); the small control arms are inherited from `decisions/003` and their width is a disclosed limitation, not a gate.
The sign rule at ΔP1 = 0 ships the swap on the conflict-removal argument alone; that is a policy choice recorded here, and the paired per-query interval reported by `analyze_ab.py` is disclosure, not a gate.

Recorded, not gating: the four-query 0.33-tier mechanism mean per description; order and drift diagnostics (rate by which-first and by run); fresh-baseline-vs-historical-0.517 drift.
Reachable verdicts: SHIP, NO_SHIP_REGRESSION, NO_SHIP_HARM, VOID; every row except SHIP leaves the repository's description untouched.
`SKILL.md` is edited only after a SHIP verdict, and the edit must byte-match the frozen treatment text.

## Phase B — orthogonal annotation of the P1 arm (consistency-checked, not independent)

Replaces issue #5's three-subclass split, which is not mutually exclusive.
Three orthogonal fields, defined once in the annotation packet:

- `scope`: `whole` | `facet`.
- `temporality`: `snapshot` | `longitudinal`.
- `boundary`: `clean` | `named-effect` (asserts a directional change) | `frontier` (correct route genuinely unsettled).

Procedure: a standalone blinded packet (`annotation-packet-2026-08-11.md`) contains only randomized query IDs, query text, and the field definitions — no rates, no expectations, no pointer to this document.
The ID-to-fixture-index mapping lives in `annotation-key-2026-08-11.json` (seed 20260811) and is withheld from annotators; it is used only to join labels back onto queries after both label sets are committed.
Two fresh sessions of the same model each label all 20 P1 queries from the packet alone; their raw labels are written to separate files and committed before reconciliation; reconciliation notes are a third file.
This is a **consistency check** (same model, same operator, same definitions), not independent annotation, and is labelled as such; per-field agreement is reported.
Query text never changes; arm membership never changes in this phase; whether any `named-effect` query moves arms is a fixture-revision decision deferred to Phase C authorship and disclosed there.

## Phase C — crossed speech-act pairs (narrow confirmation, primary estimand)

- Design: description (baseline B, treatment T) × speech act (`profile`, `overview`, `rundown`, `tell-me-about`), entity and facet held constant within each of 10 independently authored bases → 40 queries; all bases snapshot-temporality, no directional effects, no claims.
- The fixture is authored and committed **before any Phase A result is inspected**, and receives its own design review before its canary; both facts are recorded in its file.
- Runs: `run_desc_eval.py`, both descriptions × 3 runs per query, same interleaving, seed `20260812` (~240 scored invocations plus canaries).
- **Preregistered estimand**: per base i and description D, gap_i(D) = rate(profile) − mean(rate over the three generic acts). θ_i = gap_i(B) − gap_i(T); positive θ means the treatment narrowed the profile-vs-generic gap. Estimator: θ̄ = mean over the 10 bases; uncertainty: exact paired sign-flip permutation of θ_i (all 2^10 enumerations, deterministic), two-sided 95%.
- Support levels, fixed here: **confirmed** if θ̄ > 0 and the permutation interval excludes 0; **directional** if θ̄ > 0 otherwise; **not supported** if θ̄ ≤ 0.
- Precision, honestly stated for the estimand: with 10 bases and rates in [0,1], the worst-case 95% half-width for θ̄ is on the order of ±0.3–0.4; this phase is a **narrow confirmation** over ten authored library-system bases, not a general claim about entity-profiling speech acts.
- **Reopen rule**: if Phase A shipped and Phase C lands **not supported** with θ̄ < 0 and the interval excluding 0 (the treatment measurably worsened the gap), the ship decision reopens: the swap reverts pending redesign, and the reversal owes its own Phase-A-style screen. Any other Phase C outcome records evidence without reopening.
- Phase C runs with both descriptions regardless of Phase A's verdict; under a no-ship verdict its treatment arm is evidence about the declined text.

## Phase D — seam repeats (secondary estimand)

If Phase A ships: repeat T13/T14 under the repaired text with `../run_trigger.py` exactly as the 2026-08-11 wave (same gates, canaries, and rep counts), plus one dual-install pass over one speech-act rendering per Phase C base (10 queries × 1 rep per catalog order) as a routing spot check.
If Phase A declines: Phase D is not owed; the 2026-08-11 seam result stands for the unchanged text.

## Statistical limits, stated once

Three valid runs per query is screening precision: a per-query 0/3 has a two-sided 95% Clopper–Pearson upper bound of 0.708.
Repetition of a fixed query is not replication of the query class; queries and bases are the sampling units for any generalization claim, which is why Phase C spends its budget on breadth.
Gates read arm-level means only; per-query and per-base numbers are exploratory disclosure.

## Contamination controls

- Both frozen texts, both instruments, this document, and the Phase C fixture are committed before the arms they govern run; `frozen-description.txt` is never modified.
- Every result row carries the served description's sha256; `analyze_ab.py` rejects foreign digests.
- No arm of any phase is shown this document, the fixture's expectations, or any prior result; Phase B annotators see only the packet.
- The operator's user-global configuration is present identically in every arm and disclosed, as in all prior waves.
- The `claude` CLI version, model id, git SHA, seeds, and per-invocation timestamps are recorded in each instrument's manifest.

## Results

Appended per phase after its arms run; nothing below this line existed before the wave.
