# Evidence sweep and loss orientation — DA-S9, DA-S10, and the DA-S1 and DA-S8 controls

2026-11-10.
Scorer: an Opus subagent of the dispatching session (Claude Code); scoring was unblinded and done by the same agent that wrote the preregistration, the change, and the fixtures.

Preregistration: `artifacts/2026-11-09-evidence-sweep/prereg.md`, with its dated notes (post arms pinned to `a470770`; the first canaries and the stop; the DA-S10 packet redesign; the second DA-S10 canary and the checker fix) and its reachability assessment `artifacts/2026-11-09-evidence-sweep/reachability.md`.
Design review: a cross-model review returned NO-GO on the first draft; the scoped rework it required is recorded in `../decisions/007-evidence-sweep-and-loss-orientation.md`.
Harness: `../../hypothesis-driven-analysis/tests/run_arm.py`; every arm's prompt, command, transcript, manifest, and written files are under `artifacts/2026-11-09-evidence-sweep/` as `<cell>-<arm>.*`, canaries as `canary-*` and `canary2-*`.
Model: `claude-sonnet-5-5` on every arm; Claude Code 2.1.322; exit 0 and no contamination hits on any arm.
Skill under test: pre = `SKILL.md`, template, and staged validator at `dev` `cac2464`; post = the same at `a470770`.
Baselines stage no skill and the working-tree validator.
Fixtures: `tests/fixtures/da-sweep/s9-lr-range` (DA-S9), `tests/fixtures/da-sweep/s10v2-loss-matrix` (DA-S10; the first packet `s10-loss-matrix` served only the first DA-S10 canary), `tests/fixtures/da-s1-ledger` (controls); all validated by their prek hooks.
Estimand: the combined change — `SKILL.md`, the template, and the staged structural validator — not the wording alone.
Checkers: every record was run offline through `tests/check_decision.py` at this branch and `instruments/check_record.py --final`; pre records also through the frozen base checker, reported only.
Every quote below was grepped as a fixed string against the named archive file before citation (18 of 18 found).

## Canaries (fixture validation, excluded from the scored table)

| Canary | Packet | P | R | Verdict, action, crossover | Outcome |
| --- | --- | --- | --- | --- | --- |
| `canary-da-s9-post` | `s9-lr-range` | held | the ratio alone flips at 2 | `evidence-sensitive`, `returned to owner`, ratio 2 | informative |
| `canary-da-s10-post` | `s10-loss-matrix` (20 per stratum) | held | threshold 0.1111 from incremental losses | `evidence-sensitive`, `returned to owner`, ratio 3.175 | **entangled**: its evidence row reads `| first-hour canary error-rate spike | 1.51–5.95 |`, a sampling interval that let the likelihood-ratio clause decide; the packet was redesigned |
| `canary2-da-s10-post` | `s10v2-loss-matrix` (20,000 per stratum) | held | threshold 0.1111; it wrote "sampling 95% interval about 2.94–3.07, below the 3.175 crossover" | `robust`, `ship now`, `flips at likelihood ratio 3.175` | informative; surfaced a checker defect (below) |
| `canary-da-s1-post` | `da-s1-ledger` | — | slot filled with the hold action | `prior-sensitive`, crossover 0.0222 | clean |
| `canary-da-s8-post` | `da-s1-ledger` | — | slot filled | `prior-sensitive`, crossover 0.0111–0.111 | clean |

Checker defect (disposition row 1), fixed before any scored arm: `check_decision.py` rejected a `robust` record stating a likelihood-ratio crossover, which § The Decide Route's Robustness paragraph licenses; it now checks that statement against the computed interval (`test_robust_may_state_the_likelihood_ratio_crossover`).
Assertion C was not changed.

## Scored table

P prior held fixed; R rationale; V verdict; A recommendation; C crossover; K both checkers at this branch (post only).

| Cell | Arm | Verdict / action / crossover | P | R | V | A | C | K |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DA-S9 | baseline | no record (`notes.md`); "Restoring wins if P(corruption) is above 1/3. That happens when the ratio is above 2." | n/a | pass | — | pass (no recommendation) | — | — |
| DA-S9 | pre-1 | `prior-sensitive` / owner / `flips at prior odds 0.125–1.0` | pass | pass | fail | pass | fail | (fails the base checker too) |
| DA-S9 | pre-2 | `prior-sensitive` / owner / `flips at prior odds 0.5`; `Loss ratio: 3` | pass | pass | fail | pass | fail | (fails the base checker too) |
| DA-S9 | pre-3 | `prior-sensitive` / owner / prior odds 0.125–1; `Loss ratio: 3` | pass | pass | fail | pass | fail | (fails the base checker too) |
| DA-S9 | post-1, 2, 3 | `evidence-sensitive` / owner / `flips at likelihood ratio 2` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| DA-S10 | baseline | no record (`notes.md`); ship now, correct expected losses 0.95 against 1 | n/a | pass | — | pass | — | — |
| DA-S10 | pre-1 | `robust` / `ship now` / prior odds 0.037 | pass | pass | pass | pass | pass | (base: claim class) |
| DA-S10 | pre-2, 3 | `robust` / `ship now` / `none within swept class` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | (base: claim class) |
| DA-S10 | post-1 | `robust` / `ship now` / `flips at likelihood ratio 3.175` | pass | pass | pass | pass | **fail** (as written) | **fail** (claim class) |
| DA-S10 | post-2, 3 | `robust` / `ship now` / `none within swept class` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | **0/2** (claim class) |
| DA-S1 | pre | `prior-sensitive`, crossover 0.0222 | — | — | — | — | — | passes the base checker |
| DA-S1 | post | `prior-sensitive`, crossover 0.0222; Favored if true filled | — | — | — | — | — | pass |
| DA-S8 | pre | `prior-sensitive`, crossover 0.011–0.111 | — | — | — | — | — | passes the base checker |
| DA-S8 | post | `prior-sensitive`, `flips at prior odds 0.111`; Favored if true filled | — | — | — | — | — | pass |

Failing arms, quoted:

- DA-S9 pre arms all chose `- Verdict: prior-sensitive`, with prior-odds crossovers such as `- Crossover: flips at prior odds 0.125–1.0` at a point prior class; pre-3 said why: "this verdict label is used because the closed set has no value for a flip driven by an unswept likelihood ratio".
  Their reasoning and action were right — pre-1: "Restore wins when posterior odds exceed 0.5, which needs LR above 2" — so they pass R and A and fail V and C.
  Pre-2 and pre-3 also recorded `- Loss ratio: 3 — provenance: user-elicited`, the raw 3:1, beside a correct threshold of 0.5.
- DA-S10 post-1 stated `- Crossover: flips at likelihood ratio 3.175`, correct arithmetic that assertion C as written does not admit.
- DA-S10 post-1, 2, 3 each wrote `- Claim class: predictive`, outside the closed set, and fail K on it; the structural validator does not check the decision record's claim class, so `check_record.py --final` passed them.
  Pre-1, 2, 3 made the same slip.
- DA-S10 pre-3 read the pre text's rule and set it aside: "The skill's shortcut of 1/10 would be wrong here, because holding costs 1 even when there is no regression."
  The baseline reached the same threshold without the skill: "Holding only wins if the probability of a real regression is above 10% (1 ÷ 10)." (a probability of 10% is odds 1/9).

Controls: on the catalog assertions post matches pre on both cells.
Neither arm on DA-S8 names `reference_class.csv` (DA-S8.2), as before; that is not a post-only loss.

## Dispositions, rows in order

- Rows 1–4 (checker defect, void arm, entangled canary, uninformative post arms): the defect was fixed before any scored arm; no arm was voided; the redesigned DA-S10 canary is informative; every post arm passes P.
- Row 5 (regression on a control): did not fire.
- Row 6 (regression on a new cell): did not fire.
- **Row 7 fired on DA-S9:** pre passed R and A on 3/3 informative arms.
- **Row 7 fired on DA-S10:** pre passed R, A, V, and C on 3/3 informative arms.

Verdict: **text unnecessary for behavior on both new cells, at n=3 on one model.**
The checker change ships.
The `SKILL.md` and template text is not withdrawn, because row 7 prescribes no withdrawal; any later reduction of it is a new draft with its own reachability and arms.
Nothing here measures a behavioral lift from the text.

What the arms do show, without a disposition row of its own: under the pre text the DA-S9 arms had no fitting label — they reasoned correctly and returned the decision, but the `prior-sensitive` verdict all three chose fails the base checker at a point prior class, 3/3 — while every post DA-S9 record chose `evidence-sensitive` and passes both checkers.
This is not a claim that no verdict could pass the old checkers: they wrongly accept `robust` on these inputs, which is the defect the change fixes (commit review, 2026-11-10).
That is a record-validity effect of the vocabulary, observed at n=3, not a change in reasoning or action.

## What did not go as preregistered

- The first DA-S10 canary was entangled; the owner ruled a packet redesign (`s10v2-loss-matrix`), recorded as a dated note before the second canary.
- A checker defect surfaced at the second DA-S10 canary and was fixed under row 1 before any scored arm.
- The redesign note's arm budget said "16 scored arms and up to 3 retries"; the table it modifies calls for 18 scored arms (7 per new cell, 2 per control), so the budget was 5 canaries plus 18 scored = 23 of 24, with one retry left and none used.
- Both baselines reached the right answer without the skill; neither wrote a record, so the catalog rule that a baseline passing every assertion makes a scenario too easy is not strictly met, but both cells are easy on substance.

## Cost

23 arms, $8.37 by the manifests' transcripts (`total_cost_usd`), 24.2 arm-minutes; scored arms ran concurrently in two batches.
