# Issue #11 disposition — S12 causal-status misses in the Sonnet replication arms

Scope: issue #11, filed from an unpreregistered observation in the 2026-08-11 issue-#8 replication wave (`2026-08-11-scenario12-sonnet-table-replication.md`).
This note records the `PROTOCOL.md` step-0 re-derivation and the disposition decision the issue's proposed order calls for.
No agent-read prose changes here, so no measurement arms are owed per `tests/PROTOCOL.md` ("What owes a rerun").

## Step 0: the reported failure exists

The issue claims two of three replication arms marked the causal H1 `REFUTED` on a pre/post aggregate conversion contrast alone.
Re-derived fresh from the archived ledgers, not from the issue or the wave notes:

| Arm | H1 status | Rests on | Evidence |
| --- | --- | --- | --- |
| rep1 | `REFUTED` | T1 only — weekday-matched pre/post site rate (3.10% → 2.55%) | ledger line 70: "necessary prediction (post-launch rate not lower than pre-launch) failed under T1"; T1 defined at line 50 |
| rep2 | `UNRESOLVED` | rule applied — same contrast returned `NON_DISCRIMINATING` and was not treated as refuting | ledger line 27 states the Conclusion rule and line 70 leaves H1 `UNRESOLVED` |
| rep3 | `REFUTED` | T1 only — raw pre/post aggregate rate (3.12% → 2.51%) | ledger line 65: "failed under an adequate test, T1"; T1 defined at line 48 |
| 2026-08-10 arm | `UNRESOLVED` (prose) | rule followed | scored PASS on assertion 5, run file line 15 |

Both `REFUTED` rows cite T1 and nothing else, and in both ledgers T1 is the pre/post exposure–outcome contrast — confirming the issue's premise.
Reconciliation against a total the archive states: the replication wave file reports exactly these four arms with exactly these statuses (rep1/rep3 miss, rep2 and the 2026-08-10 arm comply), and these are all the Sonnet-as-main-agent S12 arms under `runs/`.
Earlier S12 arms predate the main-agent design (2026-07-16/17 subagent runs against superseded skill wording; the causal-routing run states Sonnet at `e55ba78`, the 07-17 rerun ran on Opus) and are outside this population: a measured result belongs to the wording it ran against.
Instrument check: the rep1 basis phrase greps to 0 matches in the rep2 ledger, so a hit is discriminating.

## The rule the misses lose to

`SKILL.md@faf98cd` line 257 (the Conclusion section's status rules; all line numbers below are into this pinned version) states the rule at the decision point where statuses are assigned, with the rationale in the same sentence:

> An exposure–outcome contrast from a design that does not identify the causal contrast cannot by itself mark that causal hypothesis `REFUTED`: that test leaves it `UNRESOLVED`, because a co-exposure pushing the other way could mask a real effect.

Line 258 carves out refutation by independent evidence that does not rely on the unidentified contrast.
Rep3's basis text mirrors that carve-out — "this refutation does not rely on the unidentified campaign/no-campaign contrast, only on whether the claimed outcome (a rise) occurred at all in the raw aggregate" — while resting the refutation on T1, which is that contrast: the pre/post split around the launch date is the exposure split.
Rep1's H1 basis engages only the necessary-prediction machinery, but its ledger reaches the rule's substance elsewhere: line 65 applies the carve-out's logic to T2 ("That refutation does not depend on the unidentified before/after contrast itself"), and line 75 calls the negative result associative — while the H1 row at line 70 still rests on T1.

## Decision: capability finding, not a wording defect

The issue's step 2 offers two paths: a Sonnet capability finding extending the 2026-08-10 deployment-advice verdict, or a wording-discoverability question that could lead to prose and would owe arms.
This disposition takes the first path, on three grounds:

1. The wording exists, is single-homed at the exact decision point, and states the masking rationale in the same sentence — there is no missing sentence to add that line 257 does not already say.
2. Discoverability is demonstrated in the same conditions: rep2 — same model, same wording, same fixture, same prompt — found the rule, restated its substance, and applied it, as did the 2026-08-10 arm.
3. Neither miss is a discovery failure: rep3's basis argues around line 258's carve-out, and rep1's ledger applies the carve-out's logic to T2 (line 65) and calls its own negative result associative (line 75) while resting H1's `REFUTED` on T1 anyway — both arms reached the rule's substance and lost to it in application.

The candidate fix on the wording path — an added example or restatement — would in any case be a second home for the rule (decision 004) and would owe arms to justify prose with no identified defect.

## Extended deployment advice

The 2026-08-10 wave's advice ("which model may run as main agent") gains a caveat — it does not flip:
Sonnet as main agent applies the causal-status rule at `SKILL.md@faf98cd` line 257 inconsistently — observed 2 misses in the 4 archived Sonnet-as-main-agent S12 arms, where the one arm scored on assertion 5 passed.
Investigations where the deliverable is a causal status under an unidentified design should treat a Sonnet-produced `REFUTED` on a causal row as needing review against line 257 before it is acted on.

Caveat carried from the issue: the 2 misses come from arms that were not being scored on assertion 5, so 2/4 is an observed count, not a measured failure rate.

## What would reopen this

- A preregistered wave scoring S12 assertion 5 on Sonnet arms, if a measured rate is wanted; that is the only path to a scored capability claim.
- Recurrence of the miss in any scored arm.
- Anyone proposing prose for the rule, which owes arms for the S12 cell per `tests/PROTOCOL.md` before it ships.

Out of scope, noted without adjudication: rep1 also marks its H3 (the 06-10 deploy), claim-classed `causal (rival)`, `REFUTED` from an observational contrast; rep2 and rep3 classed their deploy hypothesis `data-artifact`, where line 257 does not bind.
Assertion 5 names only the campaign hypothesis, and no issue covers the H3 rows.
