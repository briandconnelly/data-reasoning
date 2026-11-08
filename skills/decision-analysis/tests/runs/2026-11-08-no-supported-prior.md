# Issue #41, attempt 2 — no-supported-prior form, rounded losses, ordered verdict rule, 2026-11-08

Preregistration: `artifacts/2026-11-08-no-supported-prior-prereg.md` (cells DA-S1, DA-S1x, DA-S3, DA-S8; added assertions S1.A–C, S3.A, S8.A; verdict table; one amendment on validator staging, made before any scored arm was read).
Design review (PROTOCOL step 3): a Codex consult critiqued the draft before any edit; it supplied the verdict-case table, rejected analyst-chosen loss endpoints carrying `user-elicited`, and required a `loss-sensitive` path and paired sentinels. Each shaped the wording and both checkers.
Harness: `../../hypothesis-driven-analysis/tests/run_arm.py`; every arm's prompt, command, transcript, manifest, and written files are under `artifacts/2026-11-08-no-supported-prior/` as `<cell>-<arm>.*`; canaries as `canary-<cell>-post.*`.
Model: `claude-sonnet-5-5` on every arm; Claude Code 2.1.319 (Claude Code); no contamination hits on any arm.
Fixture: `tests/fixtures/da-s1-ledger/` on every cell (validated by `validate_da_s1.py`).
Skill under test: pre = `SKILL.md` and template at `dev` 992b866; post = this branch's working tree at the first scored run, then — after the Codex review below changed § Numeric Policy — rerun for every post arm whose record traversed the edited sentences (DA-S1, DA-S1x, DA-S8; DA-S3 is capped before it reaches them), recorded under § Final wording.
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

## Codex review of PR #77 (amicus, read-only)

Six findings, each checked against the archive or reproduced against the checker before acting:

1. *Per-axis checks miss a reversal inside the joint sweep* — **upheld**: a record with prior 1, LR 4.5, class 0.05–1 and losses 2–20 passed as `robust` though prior × LR × loss runs 0.45–90 across the corners. The checker now also requires one action across the corners of the class and the range taken together; § Numeric Policy's `robust` clause says "at every point of the stated prior class and loss range taken together".
2. *The withdrawn precedence still lived in the ordered rule's first-match order* — **upheld, and it changed the disposition**: the archive shows both DA-S8 arms chose `prior-sensitive`, so the label precedence was followed by pre and post alike and only the slot-placement instruction had failed. The precedence stays in the ordered rule as a clarification with no measured lift (DA-S8 pre and post both pass); the placement sentences are the part withdrawn; the checker enforces `prior-sensitive` on a double flip again; the catalog's DA-S8.4 stands.
3. *One endpoint's precision widened the other's tolerance* — **upheld**: tolerance is now per endpoint.
4. *The no-rerun exemption did not cover the edited sentence* — **upheld**: DA-S1 and DA-S1x post arms traversed the `prior-sensitive` sentence; both were rerun under the final wording (§ Final wording). Also upheld: a point loss range read as a loss flip; a single-point range can no longer flip, in the checker and in § Numeric Policy.
5. *The crossover parser discarded the axis the slot named* — **upheld**: a Crossover that names an axis must name the verdict's axis.
6. *Recommendation coupling stated in two homes* — **upheld**: the duplicate sentence left § Numeric Policy; § The Decide Route keeps it.

## Final wording — post arms rerun

Working tree at the rerun: `7b8005f`. Pre arms are unchanged (no changed sentence at 992b866) and stand.

| Cell | w2 post record | `check_decision` | `check_record --final` | Added assertions |
| --- | --- | --- | --- | --- |
| DA-S1 | paired sentinels; `10 — user-elicited`, Conditions: "loss 10 is a rounded elicited value taken nominally, no range endpoints supplied"; untested T2 as a paired `none supported` row; `prior-sensitive`, flips at 0.0222 | pass | pass | **S1.A, S1.B, S1.C pass** |
| DA-S1x | paired sentinels; `10 — user-elicited`; paired `none supported` row; `prior-sensitive`, flips at 0.0222 | pass | pass | **S1.A, S1.C pass** |
| DA-S8 | `0.02–0.2 — user-elicited`, `2–20 — user-elicited`, posterior `0.09–0.9`; Crossover `flips at prior odds 0.111`, bare; Conditions: "At L=2 the action flips at prior odds 0.111 … Loss-ratio crossover at prior 0.02 is L=11.1"; `prior-sensitive` | pass | pass | **S8.A pass** |

## Verdict, per the preregistered table

- **No-supported-prior form and rounded-loss rule (DA-S1, DA-S1x, DA-S3): ship as measured at n=1 per cell.** Pre fails at least one added assertion on every cell; post passes every added assertion under the final wording; no post-only regression on a catalog assertion; both checkers accept every post record.
- **Ordered verdict rule with the double-flip precedence (DA-S8): a clarification carrying no measured lift.** Pre passes S8.A under the explicit-odds prompt; the first post arm failed the checker on form (both crossovers as prose in the one Crossover slot) and the slot-placement sentences it followed were withdrawn; under the final wording the post arm passes. Both arms chose `prior-sensitive`, which is what the rule says; the "unnecessary" row describes this cell, and the rule stays as the one home of verdict selection rather than being removed, because the alternative is the two-homes state the review found. Issue #41's second item is settled by this rule at the clarification grade, not as a measured improvement.
- DA-S8's prompt reword (explicit odds) stays: the pre arm under it read 1:50–1:5 as 0.02–0.2 where the 2026-09-15 arms split.

## Debt this wave leaves

- Where the second crossover goes when both axes flip: the first DA-S8 post arm wrote both into the one Crossover slot; the final-wording arm put one bare value there and the other in Conditions without being told to. A placement sentence owes its own arm if anyone writes one.
- Every figure is n=1 per cell on one model; Codex is unmeasured.
