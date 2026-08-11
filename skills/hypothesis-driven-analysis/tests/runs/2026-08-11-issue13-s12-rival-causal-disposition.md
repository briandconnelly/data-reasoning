# Issue #13 disposition — S12 rival causal row refuted from a pre/post-deploy contrast

Scope: issue #13, filed from the out-of-scope observation recorded in the issue-#11 disposition note (`2026-08-11-issue11-s12-causal-status-disposition.md`).
This note records the `PROTOCOL.md` step-0 re-derivation and the step-2 decision the issue calls for.
The only prose change shipped alongside it is a new committed S12 assertion in `tests/scenarios.md`, which is scorer-read (arms are forbidden from that file), so no measurement arms are owed per `tests/PROTOCOL.md` ("What owes a rerun").

## Step 0: the reported behavior exists

The issue claims rep1 claim-classed the deploy rival `causal (rival)` and marked it `REFUTED` on a pre/post-deploy contrast alone, while the other arms classed the same hypothesis outside the causal class.
Re-derived fresh from the archived ledgers:

| Arm | Deploy-rival claim class | Status | Rests on | Evidence |
| --- | --- | --- | --- | --- |
| rep1 | `causal (rival)` (Plan line 24) | `REFUTED` (line 72) | T3 only (line 52) — weekday-paired /home and /product counts before vs after 06-10 | basis: "necessary prediction (a level shift at 06-10 distinguishable from 06-08) failed under T3" |
| rep2 | `data-artifact` (line 24) | `REFUTED` (line 72) | T3 (line 53) — daily-rate series inspected around 06-10, no step found | line 257 does not bind non-causal rows |
| rep3 | `data-artifact / confound` (line 21) | `UNRESOLVED` (line 67) | T3 `NON_DISCRIMINATING` (line 50) — underpowered below ~1pp | rule not reached; the contrast was not treated as refuting anyway |
| 2026-08-10 arm | probed as its H2 | `NON_DISCRIMINATING` (ledger line 75) | no discontinuity visible at 06-10, deploy recorded as a live alternative | complied |

Rep1's `REFUTED` rests on T3 and nothing else, and T3 is an exposure–outcome contrast around the deploy's own date: the deploy is the exposure, nothing identifies its assignment (every user is exposed at once), and a co-exposure — the campaign launch two days earlier, or anything unobserved — could in principle mask a real deploy effect.
That is the structure `SKILL.md@faf98cd` line 257 forbids as the sole basis for a causal `REFUTED`, the same rule adjudicated for H1 in the issue-#11 disposition.
Rep1's line 65 ("That refutation does not depend on the unidentified before/after contrast itself") claims line 258's independence carve-out, but the H3 basis at line 72 cites T3, which is that contrast for H3 — the carve-out does not apply to a refutation resting on the exposure's own pre/post split.
Reconciliation against a total the archive states: these are the same four Sonnet-as-main-agent S12 arms the issue-#11 disposition reconciled against the replication wave file, and every class and status above matches the replication wave file's summary of the three rep arms.

## Step 2 decision: fold into #11's caveat, and commit an assertion

Of the issue's three paths, this disposition takes (a) and (b) together and declines (c).

(a) Rep1's H3 row is a further observed application miss of line 257 by a Sonnet main-agent arm, on a rival row rather than the campaign row.
It extends the issue-#11 deployment-advice caveat without changing it: a Sonnet-produced `REFUTED` on any causal-classed row under an unidentified design needs review against line 257 before it is acted on — "any causal-classed row" was already the caveat's substance, and this observation shows the rival rows are a live site for the same miss.

(b) S12 now commits a sixth assertion covering rival causal rows, added to `tests/scenarios.md` in this change.
It is scorer-read, binds only rows an arm claim-classes `causal`, and is vacuously satisfied when no rival row carries that class.
It postdates every archived S12 arm, so it scores future waves only; re-scoring the archived arms against it would be post-hoc and is not done here.
Against it, rep1's archived ledger would have failed and rep2/rep3/the 2026-08-10 arm would have passed vacuously or directly.

(c) is declined: line 257 already binds "that causal hypothesis" by claim class, rival or primary, so there is no reach gap in the wording, and a restatement or example would be a second home for the rule (decision 004) owing arms with no identified defect.

## Recorded limitation

Whether `data-artifact` is the right claim class for a deploy-caused-the-change hypothesis is not settled here.
Rep2 reached the same contested `REFUTED` as rep1 on the same evidence, escaping line 257 only by classing the row outside the causal class, and the new assertion inherits that escape: an arm that classes every rival non-causally passes it vacuously.
Adjudicating classing adequacy would be a wording question about the claim-class definitions, which no observed assertion failure currently motivates; it is recorded here so a future wave that sees the vacuous-pass pattern has the thread.

## What would reopen this

- A scored miss of the new assertion in a future wave.
- The vacuous-pass pattern above appearing in scored arms, which would reopen the classing question as a wording candidate owing arms.
