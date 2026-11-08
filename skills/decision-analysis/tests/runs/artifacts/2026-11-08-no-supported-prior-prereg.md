# Preregistration: 2026-11-08 no-supported-prior form, rounded losses, and the ordered verdict rule (issue #41)

Written before any arm ran.
This wave measures the decision-analysis wording changed for issue #41, per `../../../hypothesis-driven-analysis/tests/PROTOCOL.md`: § Numeric Policy's no-supported-prior form, its rounded-elicited-loss rule, and its ordered verdict rule (which absorbs § The Decide Route's verdict definitions and settles the double-flip precedence), with the template's two new sentinels.
Step 0 is discharged by the archive: the 2026-09-15 run record shows every DA-S1 arm, pre and post, either inventing a `sensitivity-only` prior inside Evidence and update or failing the checker on loss provenance, and today's record-delivery wave reproduced the first failure on a fresh pre arm (`../../../hypothesis-driven-analysis/tests/runs/artifacts/2026-11-08-record-delivery/da-s1-pre.scratch/decision-record.md`).
Design review (PROTOCOL step 3): a Codex consult critiqued the draft before any edit; its table of verdict cases, its objection to analyst-chosen loss endpoints carrying `user-elicited`, and its demand for a `loss-sensitive` path and paired sentinels shaped the wording and both checkers.

## What changed, and which cells reach it

| Change | File and section | Cells that reach it | Cells that do not |
| --- | --- | --- | --- |
| No-supported-prior form: sentinel in Prior odds and Posterior odds, supported LRs kept, unquantified items as paired `none supported`, arithmetic in Robustness | `SKILL.md` § Numeric Policy; template § Slot notes | DA-S1, DA-S1x, DA-S3 (no base rate anywhere in the fixture) | DA-S8 (prior elicited) |
| Rounded elicited loss recorded at its nominal value as `user-elicited`; analyst endpoints are `sensitivity-only` | § Numeric Policy | DA-S1 ("roughly ten") | DA-S1x ("ten times", exact), DA-S3 (no loss), DA-S8 (elicited range) |
| Ordered verdict rule with the loss cap and the double-flip precedence; Crossover slot carries the prior flip, Conditions the loss flip | § Numeric Policy (absorbing § The Decide Route § Verdict) | DA-S3 (cap), DA-S8 (double flip), DA-S1/S1x (robust or prior-sensitive under the rule) | DA-S4, S5, S6, S7 (no decide verdict, or voi route) |

Both checkers changed with the wording and are frozen with it: `check_decision.py` (paired sentinels, loss cap on `prior-sensitive`, per-axis flip tests, loss-ratio crossover validation) and `instruments/check_record.py` (paired sentinels, loss cap).
A checker defect found during scoring pauses interpretation, is fixed with a test, and the archived records are rescored transparently.

## Arms

Three arms per scored cell: **baseline** (no skill), **pre** (the skill at `dev` `992b866`, `--skill-ref 992b866`), **post** (this working tree).
No arm stages a validator: this branch is cut from `dev`, whose skills carry no section pointing at `instruments/check_record.py`, and `run_arm.py` here has no staging option (that harness change lives on the #74 branch); the three arms differ only in the skill text, and the scorer runs both checkers on every delivered record. (Amended 2026-11-08 before any scored arm was read: the first draft said every arm stages the validator, which this branch's harness cannot do; the four pre arms launched with that flag exited on an argument error and were relaunched without it.)
DA-S1's baseline from today's record-delivery wave (`.../2026-11-08-record-delivery/da-s1-baseline.*`, same prompt, same fixture, same model) is reused rather than rerun; DA-S3 and DA-S8 get fresh baselines; DA-S1x gets pre and post only (its baseline question is DA-S1's).
The attribution question is **pre versus post** on the added assertions; baseline answers whether the skill is needed on the cell.

## Cells and assertions

| Cell | Prompt | Catalog assertions | Added assertions |
| --- | --- | --- | --- |
| DA-S1 | `prompts/da-s1.txt` ("roughly ten") | DA-S1.1–S1.4 | S1.A, S1.B, S1.C |
| DA-S1x | `prompts/da-s1x.txt` ("ten times") | DA-S1.1–S1.4 | S1.A, S1.C |
| DA-S3 | `prompts/da-s3.txt` | DA-S3's two | S3.A |
| DA-S8 | `prompts/da-s8.txt` (explicit odds) | DA-S8.1–S8.4 (revised 2026-11-08) | S8.A |

- **S1.A — the form.** Prior odds and Posterior odds read `none supported — see Robustness`, bare; the 4.5 ratio stays as a supported row naming `reference_class.csv`, the 20-rollout class, and the gap condition; any untested item is a paired `none supported` row with its reason; Robustness carries a `sensitivity-only` prior class, the conditional posterior range, and the crossover. No number appears in Evidence and update carrying `sensitivity-only`.
- **S1.B — the rounded loss.** Loss ratio reads `10 — provenance: user-elicited` with the rounding stated in Conditions; any wider sweep is `sensitivity-only` and sits in Loss range swept, not in Loss ratio. (Reaches DA-S1 only.)
- **S1.C — the verdict follows the rule, and both checkers pass.** With the elicited loss and no prior flip inside the declared class the record is `robust` naming `hold`, or `prior-sensitive` with the prior-odds crossover if the declared class reaches the flip (0.022 at loss 10), or `loss-sensitive` if the analyst's swept loss endpoints are `sensitivity-only`; whichever it is, `check_decision.py` and `check_record.py --final` both pass on the delivered record. A verdict the record's own numbers do not license fails; so does a clean checker run on a record that invented a prior or relabelled a loss.
- **S3.A — the cap.** With no stated loss, Loss ratio carries `sensitivity-only` (or `none stated` with a `sensitivity-only` threshold), the verdict is `loss-sensitive` with the loss-ratio crossover (or `dominated` with the domination shown), Recommended action reads `returned to owner`, no prior is invented in Evidence and update, and both checkers pass.
- **S8.A — the precedence.** Prior odds `0.02–0.2 — provenance: user-elicited`, loss ratio `2–20 — provenance: user-elicited`, posterior `0.09–0.9`; verdict `prior-sensitive`; the Crossover slot carries the prior-odds flip (within 0.011–0.111), Conditions carries the loss-ratio flip with the prior it was computed at; both checkers pass.

Every assertion is scored on the delivered record and the archived transcript; a checker run by the scorer is evidence for S1.C, S3.A, and S8.A only alongside the record's content, never instead of it.

## Entanglement (step 2)

The fixture is DA-S1's (validated by `validate_da_s1.py`); its only sourced number is the 4.5 ratio and it carries no base rate, which is the property under test, not an entanglement.
DA-S1 reaches the record-delivery section only on the `#74` branch; this branch is from `dev` and carries no such section, so no arm here is asked to run `--final`; the scorer runs both checkers.
The rounding rule and the no-prior form are both reached by DA-S1; DA-S1x isolates the form from the rounding, and DA-S8 isolates the precedence from both.

## Canaries (step 4)

One post arm per scored cell, excluded from the scored artifact, scored on rationale: the arm must reach the sentinel, the cap, or the precedence *because* it read the rule, not by accident.

## Verdicts

| Outcome | Disposition |
| --- | --- |
| Infrastructure failure or contamination | arm voided; one fresh retry, recorded |
| Checker defect surfaces | interpretation paused; fix with a test, rescore transparently |
| Post fails a catalog assertion that pre passes, on any cell | the change responsible is withdrawn |
| Post fails an added assertion for a reason the changed wording addresses | that change is revised and remeasured, or dropped, before merge |
| Pre and post both pass every added assertion | "no demonstrated benefit": the wording is withdrawn as unnecessary |
| Post passes every added assertion on every cell where pre fails at least one, no regressions | ships as measured at n=1 per cell, on this model and harness |

Scorer: the dispatching session (Fable), every quote grepped against the archive before citation; every delivered record run through both checkers.
Model: `sonnet`, resolved model recorded per arm.
