# Scenario 12 — 2026-08-11 (Sonnet as main agent, summary-table replication, issue #8)

Wave: issue #8 replication, preregistered in `artifacts/2026-08-11-issue8-s12-table-replication-prereg.md`.
Model: Sonnet, three fresh general-purpose subagents each acting as main agent, skill loaded by path, forbidden from `tests/scenarios.md` and `tests/runs/`.
Fixture: `s1-conversion/`.
Scorer: dispatching session (Fable), against the single preregistered assertion (per-hypothesis summary table present with closed-set `status` column); status decisions and the other committed S12 assertions were deliberately not re-scored this wave.
Arm ledgers archived at `artifacts/2026-08-11-issue8-s12-rep{1,2,3}-ledger.md`.
Dispatch prompts, input digests, ledger digests, and the manifest-availability statement are in `artifacts/2026-08-11-issue8-s12-harness-evidence.md`.
Skill wording identical to the 2026-08-10 wave (`git diff 79248f5..HEAD` on `SKILL.md` and `references/ledger-template.md` is empty).

| Arm | Table present, closed-set `status` | Read `references/ledger-template.md` (self-report) | Evidence |
| --- | --- | --- | --- |
| rep1 | PASS | yes | ledger line 68 table header; statuses REFUTED/UNRESOLVED/REFUTED/UNRESOLVED; claim-class tokens carried from Plan rows |
| rep2 | PASS | yes | ledger line 68 table header; statuses UNRESOLVED/UNRESOLVED/REFUTED/REFUTED; claim-class tokens carried from Plan rows |
| rep3 | PASS | yes | ledger line 63 table header; statuses REFUTED/UNRESOLVED/UNRESOLVED/UNRESOLVED; claim-class tokens carried from Plan rows |

"Claim-class tokens carried" means exactly that: every summary `claim` cell holds its Plan row's class token (`causal`/`descriptive`/`data-artifact`), none relabelled or invented.
Some summary cells shorten their Plan cell's annotations — rep1 drops H3's "(rival)" tag, rep1 abbreviates and rep2/rep3 drop descriptive rows' estimand parentheticals (rep2 H2/H4, rep3 H4) — which matches the ledger template's own worked example (bare class in the summary `claim` cell, estimand discussed in `basis`) and was not scored either way.

Total: 3/3 on the scored assertion.
Instrument check: the header grep used for scoring returns 0 matches on the archived 2026-08-10 S12 ledger (the known negative), so a hit is discriminating.
Template-read status is post-hoc self-report by each arm to a neutral query sent after its report was final; it is labelled self-report and was not scored.

Verdict: preregistered row 1 — the 2026-08-10 table miss does not recur at n=3 with identical wording; issue #8 closes with the n=1 note the issue itself proposed.
All three arms also read the ledger template, which weakens the under-signposting reading further: the template is being found, and when found, its table stub is being followed.
No wording change ships from this wave, per every reachable prereg row.

Unpreregistered observation, recorded as such and not scored: reps 1 and 3 marked the causal H1 `REFUTED` from a pre/post aggregate contrast (rep1 T1 weekday-matched site rate, rep3 T1 raw aggregate rate), reasoning that "caused an increase" requires an increase to have occurred at all.
That necessary prediction is not in fact necessary under confounding — a concurrent negative factor can mask a true lift — and the committed S12 assertion 5 ("the observational contrast does not mark it `REFUTED`") would have failed on both arms.
Rep2, whose T1 came back `NON_DISCRIMINATING` on the same contrast, left H1 `UNRESOLVED` and would have passed.
The 2026-08-10 arm also passed assertion 5.
This is a status-decision observation outside this wave's scored question; it is filed separately rather than adjudicated here.

Per-run metadata (`scenarios.md` requires conclusion correctness, premature-conclusion, tool calls, tokens for every run):

- Conclusion correctness: all three arms correct — causal effect declared not identifiable, no improvement claimed, blended dip explained as composition, page-level underperformance reported.
  Every figure the conclusions rest on was scorer-recomputed from the fixture and reproduces exactly, including rep1's weekday-matched variant and its weekend `orders.csv` mismatch; figures in the harness-evidence artifact.
- Premature-conclusion: not verifiable in this dispatch mode — no transcript manifest exists to order ledger writes against analysis queries (see the harness-evidence artifact); recorded as unverifiable rather than asserted, the same scope limit the 2026-08-10 wave preregistered.
- Tool calls: 13/13/11. Tokens: ~66.6k/64.1k/68.8k (harness-reported subagent totals, minus the post-hoc bookkeeping exchange where separable; reported totals include it).
