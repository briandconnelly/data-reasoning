# Issue #41, attempt 2 — no-supported-prior form, rounded losses, ordered verdict rule, 2026-11-08

Preregistration: `artifacts/2026-11-08-no-supported-prior-prereg.md` (cells DA-S1, DA-S1x, DA-S3, DA-S8; added assertions S1.A–C, S3.A, S8.A; verdict table; one amendment on validator staging, made before any scored arm was read).
Design review (PROTOCOL step 3): a Codex consult critiqued the draft before any edit; it supplied the verdict-case table, rejected analyst-chosen loss endpoints carrying `user-elicited`, and required a `loss-sensitive` path and paired sentinels. Each shaped the wording and both checkers.
Harness: `../../hypothesis-driven-analysis/tests/run_arm.py`; every arm's prompt, command, transcript, manifest, and written files are under `artifacts/2026-11-08-no-supported-prior/` as `<cell>-<arm>.*`; canaries as `canary-<cell>-post.*`.
Model: `claude-sonnet-5-5` on every arm; Claude Code 2.1.319 (Claude Code); no contamination hits on any arm.
Fixture: `tests/fixtures/da-s1-ledger/` on every cell (validated by `validate_da_s1.py`).
Skill under test: pre = `SKILL.md` and template at `dev` 992b866; post = this branch's working tree before the DA-S8 withdrawal below (the withdrawn clause is reached by DA-S8 only, so the other cells' arms stand under PROTOCOL § What owes a rerun).
Checkers: both frozen with the wording; one defect surfaced at the canaries (a stated crossover rounded to three figures sat exactly on the 1% tolerance edge and was rejected) and was fixed with a test before any scored arm was read (`check_decision.py` `_rounding_tolerance`).
Scorer: the dispatching session (Fable); every quote below was grepped against the named archive file before citation; every delivered record was run through `check_decision.py` and `instruments/check_record.py --final`.

## Canaries (fixture validation, excluded from the scored artifact)

All three post canaries reached the rule for the reason under test: DA-S1 wrote the paired sentinels, kept the 4.5 ratio, recorded `Loss ratio: 10 — provenance: user-elicited` and returned `prior-sensitive` at 0.022; DA-S3 wrote the sentinels, a paired `none supported` row for the untested T2, `sensitivity-only` losses, `loss-sensitive`, and said of its sweeps "Both ranges are my own placeholders, not your numbers"; DA-S8 read the explicit odds as 0.02–0.2, returned `prior-sensitive` with the prior flip in Crossover and the loss flips in Conditions.

## Scored table

| Cell | Arm | Prior odds slot | Loss ratio | Verdict | `check_decision` | `check_record --final` | Added assertions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DA-S1 | baseline (reused from the record-delivery wave, same prompt and fixture) | no record | — | — | — | — | — |
| DA-S1 | pre | `0.1–10 — sensitivity-only` in Evidence and update; the 4.5 ratio swept to `1.2–20` | `10 — user-elicited`, swept `5–20 — user-elicited` | `loss-sensitive` | fail | fail | S1.A fail, S1.B fail, S1.C fail |
| DA-S1 | post | `none supported — see Robustness` (paired) | `10 — user-elicited`, swept `10–10 — user-elicited`, rounding in Conditions | `prior-sensitive`, flips at 0.0222 | pass | pass | **S1.A, S1.B, S1.C pass** |
| DA-S1x | pre | `0.05–2 — sensitivity-only` in Evidence and update; ratio swept `1.2–17` | `10 — user-elicited` | `prior-sensitive` | fail | fail | S1.A fail, S1.C fail |
| DA-S1x | post | paired sentinels | `10 — user-elicited` | `prior-sensitive`, flips at 0.022 | pass | pass | **S1.A, S1.C pass** |
| DA-S3 | baseline | no record; a recommendation from the ledger's lean | — | — | — | — | — |
| DA-S3 | pre | `0.1–10 — sensitivity-only` in Evidence and update | `0.1–10 — sensitivity-only` | `loss-sensitive` | fail | fail | S3.A fail (cap and handback right; invented prior) |
| DA-S3 | post | paired sentinels; untested T2 as a paired `none supported` row with its reason | `1 — sensitivity-only` | `loss-sensitive`, flips at loss ratio 0.22 | pass | pass | **S3.A pass** |
| DA-S8 | baseline | no record; a table of flip points | — | — | — | — | — |
| DA-S8 | pre | `0.02–0.2 — user-elicited` | `2–20 — user-elicited` | `prior-sensitive`, Crossover `0.0111–0.111`, loss flips in Conditions | pass | pass | **S8.A pass** |
| DA-S8 | post | `0.02–0.2 — user-elicited` | `2–20 — user-elicited` | `prior-sensitive`; Crossover is prose: "flips at prior odds 0.111 at loss ratio 2; 0.0444 at 5; 0.0222 at 10; 0.0111 (below class) at 20. Hold if prior odds × 4.5 × L > 1." | fail (form) | pass | S8.A fail on form |

Post DA-S1's report: "I used your \"roughly ten\" at its nominal value of 10."
Pre DA-S8's report: "The verdict is `prior-sensitive`, and it is also loss-sensitive."

## Catalog regression check

- DA-S1.1–S1.4, DA-S1x: post passes all four where pre fails S1.1 (checker) on both; no post-only loss.
- DA-S3: post passes both catalog assertions; pre passes the first on substance and fails the second's "handback explicit" only in that it also invents a prior; no post-only loss.
- DA-S8: **pre passes DA-S8.1 (checker) and post fails it** — a post-only regression on a catalog assertion, on the cell that alone reaches the double-flip clause.

## Verdict, per the preregistered table

- **No-supported-prior form and rounded-loss rule (DA-S1, DA-S1x, DA-S3): ship as measured at n=1 per cell.** Pre fails at least one added assertion on every cell and post passes every added assertion; no post-only regression on those cells; both checkers accept every post record.
- **Double-flip precedence clause (DA-S8): withdrawn.** The regression row fires: pre passes the checker, post fails it on form, and the pre arm already produced the intended behavior under the explicit-odds prompt, so the clause also had no demonstrated benefit. The clause and the slot-placement sentences were removed from § Numeric Policy before merge; the ordered rule keeps `dominated`, the loss cap, `prior-sensitive` on a prior flip, `loss-sensitive` on a loss flip, and `robust` otherwise, and says that a record where both flip reports both crossovers. `check_decision.py` accepts either sensitive label with the crossover of its own axis. The precedence stays owed in the catalog; DA-S8.3 is restated in a one-value form.
- DA-S8's prompt reword (explicit odds) stays: it is a catalog change, and the pre arm under it read the odds as 0.02–0.2 where the 2026-09-15 arms split.

Removing the clause changes the shipped text after DA-S1, DA-S1x and DA-S3 were measured; none of those cells reaches a double flip (DA-S1 and DA-S1x have one elicited loss, DA-S3 is capped), so under PROTOCOL § What owes a rerun they owe none.

## Debt this wave leaves

- The precedence between `prior-sensitive` and `loss-sensitive` when both flip (issue #41, item 2).
- Which quantity the single Crossover slot carries when both flip: the template's one-value form was violated by the only post arm asked to carry two.
- Every figure is n=1 per cell on one model; Codex is unmeasured.
