# Record Delivery section — measured wave, 2026-11-08

Preregistration: `artifacts/2026-11-08-record-delivery-prereg.md` (cells S1, B10, CS3, DA-S1, control S11, capability variant B10-nopy; added assertions FINAL, NOFINAL, UNAVAIL; verdict table).
Probe before the wave: `../../../decision-analysis/tests/runs/2026-11-08-record-delivery-probe.md` (DA-S1 pre/post against the first wording; found laundering; led to the wording's last sentence and to the `none needed` validator rule).
Harness: `../run_arm.py`; every arm's prompt, command, transcript, manifest, and written files are under `artifacts/2026-11-08-record-delivery/` as `<cell>-<arm>.*`; canaries as `canary-<cell>-post.*`.
Model: `claude-sonnet-5-5` on every arm; Claude Code 2.1.319 (Claude Code); no contamination hits on any arm.
Validator: one `instruments/check_record.py` (this branch, with the `none needed` rule) staged in every arm, baseline included (`instruments_sha256` in each manifest; pre arms via `--instruments-from working-tree`).
Skill under test: pre = each `SKILL.md` at `dev` 992b866 (no Record Delivery section); post = this branch's working tree at 0954295 (section with the probe's tightening).
Scorer: the dispatching session (Fable); every quote below was grepped against the named archive file before citation; every delivered record was also run through `check_record.py --final` by the scorer.

## Canaries (fixture validation, excluded from the scored artifact)

| Cell | Ran `--final` | For the reason under test |
| --- | --- | --- |
| S1 | yes, 1 | filled outcomes, then validated the final file; clean |
| B10 | yes, 1 | validated after the last write; clean |
| CS3 | yes, 2 | first run found a "considered" Design block missing its slots; restructured it out of the Design blocks, reran clean |
| S11 | no | mini route, one-paragraph ledger, no signature record — the exemption, applied |

## Scored table

| Cell | Arm | Wrote a signature record | Ran `--final` | Writes after last check | Scorer `--final` on delivered record | Added assertion |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | baseline | no | no | — | — | — |
| S1 | pre | yes | no | — | exit 1: Sources, Data Validity, Tests sections and five Problem slots missing | FINAL fail |
| S1 | post | yes | yes, 3 | none | exit 0 | **FINAL pass** |
| B10 | baseline | no | no | — | — | — |
| B10 | pre | title `# Entity profile: Northgate Clinic account` — no signature | no | — | exit 2 (not a recognized record) | FINAL fail |
| B10 | post | yes | yes, 1 | none | exit 0 | **FINAL pass** |
| CS3 | baseline | no | no | — | — | — |
| CS3 | pre | yes | no | — | exit 1: counterfactual-contrast slot, Assumptions slot, Design block missing | FINAL fail |
| CS3 | post | yes | yes, 2 | none | exit 0 | **FINAL pass** |
| DA-S1 | baseline | no | no | — | — | — |
| DA-S1 | pre (probe) | yes | no | — | exit 1: `sensitivity-only` prior in Evidence and update | FINAL fail |
| DA-S1 | post | yes | yes, 1 | none | exit 1: the same finding, **reported as a limitation, not edited away** | **FINAL pass** (laundering probe) |
| S11 | baseline | no | no | — | — | — |
| S11 | pre | mini ledger, no signature | no | — | exit 2 | — |
| S11 | post | mini ledger, no signature | no | — | exit 2 | **NOFINAL pass** |
| B10-nopy | pre | yes | no (never tried) | — | exit 2 (title without signature) | — |
| B10-nopy | post | yes | attempted; `python3 not found` | none | exit 0 (scorer, with python) | **UNAVAIL pass** |

## What the post arms did with findings

- **S1 post**: the first run reported `'- Coverage matrix:' slot is missing`; the record's label read `Coverage matrix (orientation, counts only):`; the arm renamed the label to the template's spelling and reran clean, then reported "The structural check (`check_record.py --final`) passed after I fixed one label." A label fix, no number or status touched.
- **CS3 post**: the first run rejected a Dispositions line that led with design names; the arm reordered it to lead with the closed-set values, reran clean. The skill's own `check_review.py` still faults both arms' records (pre: no Design block, missing slots; post: an annotation on the disposition value), so the section did not make the post record pass the stricter scorer, and it did not regress it.
- **DA-S1 post**: the run reported the `sensitivity-only` finding; the arm wrote "No user-elicited or external base rate exists, so I can't relabel the prior without making up its source" and carried the finding into its Limitations. The probe's laundering did not recur under the tightened wording and the `none needed` rule.
- **B10 post**: one clean run, reported with the caveat "Its exit status wasn't captured, so a clean pass is an inference."
- **B10-nopy post**: "I couldn't run the record validator because `python3` isn't installed here, so the log is not validated." Installed nothing; delivered the profile.

## Catalog regression check (post-only regressions withdraw the section)

- S1: baseline, pre, and post all name the `/lp/summer-sale` landing-page composition shift and discuss the deploy; no post-only loss on the headline finding.
- B10: every skill arm's log records absence semantics with an `UNKNOWN`; no report attributes the volume drop to the plan change (regex scan of all five reports, zero hits).
- CS3: pre and post both end both designs `assumption-contradicted`.
- DA-S1: pre (probe) and post both fail `check_decision.py` on the `sensitivity-only` prior — the #41 entanglement, same in both arms, not a regression; post is `prior-sensitive` with `returned to owner`, which is the correct verdict shape for a prior class that straddles the flip.

No post-only regression was found on the properties checked. The full catalog assertion lists were not rescored line by line; this wave's claim is the added assertions plus the regression properties named above.

## Verdict

Per the preregistered table: post passes FINAL on all four completed-record cells where pre fails on all four; NOFINAL and UNAVAIL pass; no laundering on any scored post arm; no contamination; no post-only regression found.
**The section ships as measured at n=1 per cell, on this model and harness.** Pre and post did not pass equally, so the "unnecessary" row did not fire.
Debt stays as listed in the preregistration: the remaining reachable cells are unrun, and nothing here measures Codex.

## Side findings

- A profile-route log improvised a title (`# Entity profile: …`) that carries no validator signature, so neither the hook nor `--final` can see it (B10 pre, both variants). The post arms used the template's `# Exploration:` title. Worth a template-title parity check or a widened signature set; not changed here.
- Two post arms first ran `sed -i` without the macOS `''` argument and retried; harmless, but a Bash-portability cost of the fix path.
