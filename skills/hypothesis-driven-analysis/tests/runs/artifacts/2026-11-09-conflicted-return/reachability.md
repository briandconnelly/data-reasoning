# Reachability: conflicted-return rule for status and "best supported" (issue #86)

Written 2026-11-09, before any arm of this workstream exists.
Scope judgement per `../../../PROTOCOL.md` § What owes a rerun and `../../../../decisions/001-rerun-obligation.md`: a cell owes arms when its decision point traverses an edited sentence.

## Step 0 — the reported failure, re-derived

Re-derived from `../2026-11-08-binding-rules-hoist/` with this directory's `extract.py` (and, independently first, a throwaway script with the same field regex), not taken from issue #86, the wave record, or the brief.

**Reconciliation against a stated total.**
`extract.py census ../2026-11-08-binding-rules-hoist` prints `manifests=81 {'canary': 13, 'scored': 62, 'pretrunc': 6}` and `cost=$25.97`, which are the wave record's stated arm total, split, and cost (`../../2026-11-08-binding-rules-hoist-wave.md`, header and Cost line).
It also lists the two arms the wave record says its scanner flagged (`s1-pretrunc-2`, `s21d6-pretrunc-2`), so the contamination field is read correctly too.
`extract.py fields` finds 45 S21 arms there: 7 canaries plus the 38 non-canary `s21d*` manifests.

**Counts, on the shipped wording (pre arms, `--skill-ref 692fd31`):**

| Cell | Arm | H2 STATUS | BEST SUPPORTED (first clause) | Catalog assertion |
| --- | --- | --- | --- | --- |
| d3 | `s21d3-pre-1` | `UNRESOLVED` | — | pass |
| d3 | `s21d3-pre-2` | `UNRESOLVED (T2 outcome stays CONTRADICTED, …)` | — | pass |
| d3 | `s21d3-pre-3` | `UNRESOLVED` | — | pass |
| d6 | `s21d6-pre-1` | `UNRESOLVED` | "Only as a qualified "best supported" in the basis text" | **miss** |
| d6 | `s21d6-pre-2` | `UNRESOLVED` | "Yes, but only as a qualified report." | **miss** |
| d6 | `s21d6-pre-3` | `UNRESOLVED` | "No, not as an established or action-ready finding." … "It can't be reported as "best supported"." | pass |

d3 pre 3/3 and d6 pre 1/3: the reviewer's claim holds.
Every d3 and d6 pre arm names the command/output day conflict in its reasoning, and none relabels T2's Outcome.
Both d6 misses quote the Analysis sentence that the limitation "bars treating the result as established or action-ready" and still judge the best-supported bar "met" on the ledger's own terms, which is the gap the new sentence closes: nothing in the shipped text says the conflicted `CONSISTENT` fails the bar's second limb.
The post arms of that wave (a verbatim move of § Conclusion, withdrawn) show d6 1/3 and d3 1/3; they ran a different SKILL.md and are not this workstream's pre.
The d5, d7, d1 pre arms are 3/3, 3/3, 3/3 on their catalog assertions, re-read from `answer.md`.

So `decisions/005`'s reopening condition ("an arm reaches the disposition Scenario 21's d3 or d6 cell scores as a miss, under any wording") is met on the shipped wording, twice.

**Digest comparison — can the 15 pre arms be reused?**
For each of the 15 `s21d{1,3,5,6,7}-pre-*` manifests: all 14 entries of `skill_files_sha256` equal the sha256 of the same file in this branch's parent (`dev` at `cac2464`), with no file missing and no non-`tests/` skill file absent from the manifest; `fixture_files_sha256` equals the current packet; `instruments_sha256` equals the current `instruments/check_record.py`.
The S21 fixture directory, `validate_s21.py`, and `generate.py` have identical git blob ids at `692fd31` and `cac2464`, and `run_arm.py` is unchanged since `c733f80`, the commit the pre arms ran under.
`validate_s21.py` passes on the current packets and fails on a scratch copy with d6's planted conflict removed (`FAIL: d6-support-conflict: expected exactly one planted conflict`), so the validator is not a check that cannot fail.
The prompt files are byte-identical copies (`prompts/s21-*.txt`, sha256 in `prereg.md`).
The 15 pre arms therefore ran the same skill tree, packets, validator, instrument, harness and prompt files that a fresh pre arm would run today; what differs is the date and whatever changed in the model service or Claude Code between runs, which no digest can pin.

## The edited sentences

E1 — § Analysis, Conflicting execution records, new bullet after "Record the fault as a limitation …":
"Whether such an outcome can carry a `REFUTED` status or "best supported" is stated in § Conclusion."

E2 — § Conclusion, new paragraph before "`SUPPORTED` is not a status":
"An outcome resting on a return whose execution records conflict (§ Analysis) counts neither as a necessary prediction's failure under an adequate test nor as the `CONSISTENT` outcome from a discriminating test that the "best supported" bar below requires, until evidence from outside that return resolves the conflict."

E3 — § Conclusion, immediately after E2:
"A return the free check cleared that merely could not be re-run is not this case: its outcome refutes and supports like any other."

No other sentence changed; the frontmatter, the rendered shared sections, `scripts/shared-sections/`, and `instruments/check_record.py` are untouched.

## Reporting versus endorsing

The rule restricts endorsement, not reporting.
Naming a hypothesis as the only unrefuted candidate, with the conflicted return stated as the reason it is not more, reports the ledger's state and is permitted (the same distinction `scenarios.md` § Scenario 19 already draws for a crashed test).
Calling it "best supported", "the leading explanation", "the most likely cause", or presenting it as the answer endorses it, and that is what E2 bars while the conflict stands.
A "leading" or "best supported" phrase that the arm explicitly negates ("not best supported") is reporting.

## Cells

"Antecedent false" means the cell's arms read E2/E3 on the way to their decision but nothing in the fixture is a conflicted return (E2) or a cleared-but-unrepeatable one (E3), so the rule cannot apply except by misreading.

| Cell | Edited sentences on the decision path | Basis | Owes | Paid here |
| --- | --- | --- | --- | --- |
| S21 d6 | E2 (bar limb), E1 | conflicted `CONSISTENT`, rivals `REFUTED`: the bar is live and E2 decides it | yes — test cell | canary + 3 post |
| S21 d3 | E2 (refute limb), E1 | conflicted `CONTRADICTED`: E2 decides adequacy | yes — test cell | canary + 3 post |
| S21 d5 | E3 directly, E2 | cleared-but-unrepeatable `CONTRADICTED`: the over-correction the carve-out guards | yes — control | canary + 3 post |
| S21 d7 | E3 directly, E2 | cleared-but-unrepeatable `CONSISTENT`: best supported must stand | yes — control | canary + 3 post |
| S21 d1 | E2, antecedent false | `NON_DISCRIMINATING` floor | yes (floor control) | canary + 3 post |
| S21 d4 | E2, antecedent false | `CONTRADICTED` with a disclosed immaterial deviation; neither a conflict nor the "unverified" wording that makes d5 the near miss | reached | **no — debt** |
| S20 c3 | E1 inside the disposition block it is scored on; E2 via its unscored `H2 STATUS` field | the scored Outcome cell (`CONTRADICTED`, not `NON_DISCRIMINATING`) sits beside E1, and E2's "counts neither as … a discriminating test" is the sentence most likely to tempt a downgrade | yes — control on `decisions/003`'s token | canary + 3 post |
| S20 c1, c2, c4 | E1 read in the same subsection, antecedent false | established deviation, derived-value error, immaterial deviation; H2 status unscored | reached | no — debt |
| S16 | E2 (bar limb), E1 | W2's conflicted `CONSISTENT` is H2's only support, H1/H3 refuted: the bar is live in a free full-route conclusion; its catalog text permitted "leading remaining candidate" | yes — the only full-route cell where the antecedent is true | canary + 3 post |
| S19 | E2 read at the bar, antecedent false | no return at all; already barred from "best supported" by having no `CONSISTENT` outcome | reached | no — debt |
| S10 | E1 only if a live return faults, antecedent false on the archived run | honest live workers | reached | no — debt |
| S1, S4, S6, S7, S8, S12, S15, S18 | E2, E3 read in § Conclusion, antecedent false | no conflicted return in any fixture; E3's antecedent arises only with a metered unrepeatable source, which none has | reached | no — debt |
| S2, S3, S9, S11, S13, S14, S17, S22a–d | none | never reach § Conclusion (`direct`, `mini`, `estimation`, or no activation) | no | no |
| CIR, DA, EDA cells | none | each stages its own skill | no | no |

S16 owes arms because it is the cell where the rule changes the expected outcome of a free investigation, not only of a probe.
Its fixture also carries a partial coherence the probes lack: W2's Command 2 and its output agree on 2026-07-15 (`index_used=NONE`, `first_seen=…09:00`), so an arm may argue that half of the return is uncontested.
That half is still inside the return whose records conflict, and the necessary prediction is a two-day contrast whose baseline is the conflicted half; E2's "evidence from outside that return" is not met by it.

S20 c3 is paid although E1 is a cross-reference, which `PROTOCOL.md` exempts: E1 is not a bare pointer inside c3's decision block, because the sentence it points at says the outcome does not count as a discriminating test, and c3 is the cell that scores whether an arm keeps a conflicted return's outcome rather than downgrading it.

d4 is the one requested cell left unpaid.
Its decision point reads E2, but neither of E2's or E3's antecedents is present, and d5 is the stricter refute-side control on the same path (it shares the "unverified" wording that a misapplied E2 would latch onto, which d4 does not).
The 30-arm ceiling with five canaries cannot hold S21 ×5, S16, S20 c3 and d4 at canary + 3 each plus any retry, and S16 and S20 c3 each test something no S21 cell tests.
That is a judgement, and d4 is recorded as debt, not as covered.

## Debt this workstream leaves

S21 d4; S20 c1, c2, c4; S19; S10; S1, S4, S6, S7, S8, S12, S15, S18.
Every one reads E2 or E3 with the antecedent false; none is measured for this change, and the wave record must say so.
Every arm is Sonnet under `run_arm.py`; Codex is unmeasured.
