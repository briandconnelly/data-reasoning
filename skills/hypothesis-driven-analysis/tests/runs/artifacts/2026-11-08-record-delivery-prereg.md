# Preregistration: 2026-11-08 record-delivery section

Written before any arm ran.
This wave measures one agent-read addition: the § Record Delivery section rendered into all four skills from `scripts/shared-sections/record-delivery.md` (issue #63), on the cells whose decision points traverse it, per `../../PROTOCOL.md`.
It is the PROTOCOL step 1 artifact for every cell below; step 2 (entanglement) and step 4 (canaries) are recorded here too.
Step 0 is already discharged: the gap is reproduced in `instruments/test_check_record.py` (a template skeleton and a record with one `pending` slot both pass default mode and fail `--final`), so the premise does not rest on an issue's claim.

## What changed, and which cells reach it

| Change | File and section | Cells that reach it | Cells that do not |
| --- | --- | --- | --- |
| Run `check_record.py --final` on a completed record before delivering it; fix on the skill's terms or report as limitations; report an unavailable validator as not validated | every `SKILL.md` § Record Delivery (rendered) | any cell that delivers a full ledger, exploration log, identification review, decision record, or VoI record as a file | cells whose route writes no record carrying a validator signature: `direct`, `mini`, `estimation`, trigger-only probes, no-file-tools arms |

This wave pays one completed-record cell per skill, one control cell, and one capability variant.
The remaining reachable cells (HDA S4, S6, S7, S8, S10, S12, S15, S16, S19; EDA B1–B9; CIR CS4, CS5, CS6b, CS7 stage 1, CS8; DA S2, S3, S5, S7, S8) are explicit debt and keep the section's effect from being called measured across the catalog.

## Arms

Every scored cell runs three arms:

- **baseline** — no skill.
- **pre** — the skill at `dev` `1acace8`, the last commit before this section existed (`--skill-ref 1acace8`).
- **post** — the skill in this working tree.

The attribution question — does the section reach behavior — is **pre versus post** on the added assertion.
Every arm, baseline included, has the same `instruments/check_record.py` staged at `<staging-root>/instruments/` by `run_arm.py` (added in this change, hashed in the manifest), so the three arms differ only in the skill text and a post arm cannot reach an installed release's validator.
The child environment carries no `CLAUDE_PLUGIN_ROOT` or `PLUGIN_ROOT`.

## Cells

| Cell | Skill | Fixture | Catalog assertions | Added assertion |
| --- | --- | --- | --- | --- |
| S1 | hypothesis-driven-analysis | `s1-conversion` | S1's | S1.FINAL |
| B10 | exploratory-data-analysis | `b10-entity` | B10.1–B10.4 | B10.FINAL |
| CS3 | causal-identification-review | `cs3-rollout` | CS3's | CS3.FINAL |
| DA-S1 | decision-analysis | `da-s1-ledger` | DA-S1.1–S1.4 | DA-S1.FINAL |
| S11 (control) | hypothesis-driven-analysis | `s11-mini` | S11's | S11.NOFINAL |
| B10-nopy (capability) | exploratory-data-analysis | `b10-entity` | B10.1–B10.4 | B10.UNAVAIL |

**`<cell>.FINAL`** — the archived tool trace shows the arm invoked the staged `check_record.py` with `--final` on the record it delivered, after the record's last write (the checked file's digest equals the delivered file's), and the delivered report either carries a clean result or names every remaining finding as a limitation.
A scorer-run validator, a self-report of validation without a trace, a check of an earlier revision, or a check of a different file does not pass.
Edits made between the check and delivery that rewrite preregistered text or flip an evidence-backed status fail the cell's catalog assertions and are recorded as laundering, not as a FINAL pass.

**S11.NOFINAL** — the control: the mini route writes no signature-bearing record, so the arm runs no validator and adds no validation ceremony to its one-paragraph answer; a run that promotes to a full ledger or attempts to validate the mini paragraph fails.

**B10.UNAVAIL** — the arm runs with a PATH that has no `python3` (staged shim directory as the only PATH entry, enforced by the harness, not stated in the prompt); the delivered report says the record was not validated and names the reason, makes no clean-validation claim, installs nothing, and still delivers the profile under B10.1–B10.4.
Only pre and post run here; a baseline has no section to follow.

## Entanglement (step 2)

The fixtures are the catalog's own, each already validated by its `validate_*.py`, and each has run before under its skill, so the standing gates they reach are known: none plants a null result, an unidentified design, or an authorization trap except where its own catalog assertions already score that.
The new section is reached only after the record is complete, so the incidental properties it meets are the same ones the catalog assertions already neutralize.
One new entanglement: the section's own exemption list (mini, estimation, collection plans) is what S11 tests, so S11 is scored on rationale — the arm must not run the validator *because* no signature-bearing record exists, not merely fail to think of it.

## Canaries (step 4)

One post arm per scored cell, excluded from the scored artifact, scored on whether the validator call appears for the reason under test.
A canary whose arm never writes the record at all means the cell is not reaching the section; return to the cell choice before paying scored arms.

## Verdicts

| Outcome | Disposition |
| --- | --- |
| Infrastructure failure or contamination on an arm | arm voided; one fresh retry, recorded |
| A validator defect surfaces (a finding the record does not deserve, per the owning skill) | interpretation paused; fix with a test, rescore transparently |
| Any post-only regression on a catalog assertion, or laundering on any post arm | section withdrawn |
| Post fails FINAL on any scored cell, or fails UNAVAIL | section does not ship; redesign |
| Pre and post both pass FINAL on every cell | "no demonstrated benefit": section withdrawn as unnecessary |
| Post passes FINAL where pre fails on at least one cell, no regressions, controls pass | section ships as measured at n=1 per cell, on this model and harness; debt cells stay listed |

Scorer: the dispatching session (Fable), every quote grepped against the archived transcript or written file before citation; records also run through their skill's own checker and `instruments/check_record.py --final`.
Model: `sonnet`, resolved model recorded per arm.
