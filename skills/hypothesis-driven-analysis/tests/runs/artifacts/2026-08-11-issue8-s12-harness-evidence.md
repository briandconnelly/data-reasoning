# Harness evidence: S12 summary-table replication (issue #8) — 2026-08-11

Companion to `2026-08-11-issue8-s12-table-replication-prereg.md` and `../2026-08-11-scenario12-sonnet-table-replication.md`.
Recorded after PR #10 review noted the run artifacts carried no prompt hashes, input digests, or manifest statement.

## Dispatch prompts

The three arms received identical prompts except for the per-arm scratch directory (`s12-rep1/`, `s12-rep2/`, `s12-rep3/`).
The rep1 prompt, verbatim (reps 2 and 3 substitute their rep number in the scratch path):

```
You are the main agent on a data-analysis task for a user.

You have a skill installed at /Users/bdc/projects/data-reasoning/skills/hypothesis-driven-analysis/SKILL.md. Read it and follow it as your working method for this task.

The user's request:

"How much did launching the /lp/summer-sale campaign improve our checkout conversion? Data: /Users/bdc/projects/data-reasoning/skills/hypothesis-driven-analysis/tests/fixtures/s1-conversion/"

Write any working files you produce (notes, ledgers, scripts, intermediate results) to /private/tmp/claude-501/-Users-bdc-projects-data-reasoning/550cef23-2806-446b-a99d-b6937cb41b7c/scratchpad/s12-rep1/ — do not write anywhere inside /Users/bdc/projects/data-reasoning.

Do not read /Users/bdc/projects/data-reasoning/skills/hypothesis-driven-analysis/tests/scenarios.md or anything under /Users/bdc/projects/data-reasoning/skills/hypothesis-driven-analysis/tests/runs/.

Your final message is your report to the user.
```

SHA-256 of the prompt texts (trailing newline included):

| Arm | Prompt sha256 |
| --- | --- |
| rep1 | `6b615e8729f492571d1bae15043e26c7eae0218edc9975c75c158f8d28382a28` |
| rep2 | `6475fc821de12d85d0d9d3d679639614ebb44a19393b1c6b7c41f3d293675674` |
| rep3 | `ec4fca9e786bb917ba76d5214763aee0e601250160c742a05aed2bac8587e9a4` |

Provenance caveat, stated rather than hidden: these prompt files were reconstructed from the dispatching session's transcript after the arms ran, not captured by an independent harness at dispatch time; the transcript records the dispatch calls verbatim, but a reader is trusting that transcript.

## Input digests (SHA-256)

Skill and fixture state the arms read, hashed from the working tree, which was clean at both dispatch and hashing time (`git status --porcelain` empty for these paths) and identical to the 2026-08-10 wave state (`git diff 79248f5..HEAD` empty for the skill files):

| File | sha256 |
| --- | --- |
| `SKILL.md` | `c88a49c9bedfd0f61f52587828185b4cff0e586530d4a87ca5e8efc8051cceb7` |
| `references/ledger-template.md` | `3ceda09c912b5636bf63f4104a6048abb7b3a22c2a5b4423cfe53a8c7fdb71b5` |
| `tests/fixtures/s1-conversion/sessions.csv` | `77970b8484c3733fd1950fddef83314d9faafe8b564bd719e58c70e5a1faf494` |
| `tests/fixtures/s1-conversion/orders.csv` | `39486b25560ac523af351bf4376d1fe9e4c8d2c267c63b95e7e9fa7b1ada1ddc` |
| `tests/fixtures/s1-conversion/deploys.log` | `9f2a5b80677a1b2bf82b91c21ddc4ad0e5f1ffc9f8e4618cb95de633022451c7` |

Archived arm ledgers, verified byte-identical to the files the arms wrote in their scratch directories:

| File | sha256 |
| --- | --- |
| `2026-08-11-issue8-s12-rep1-ledger.md` | `b6ae2eaabef86086e2c9b7d4822c10ea07de12640892e6644a3e622cc87c2425` |
| `2026-08-11-issue8-s12-rep2-ledger.md` | `28bf7078474cef69d9d7a9f58f238ac36f9b59eb46aac7a6432f9c5e7e19034c` |
| `2026-08-11-issue8-s12-rep3-ledger.md` | `0288c29e9708ced7856923459f53538a1c4d2103ac6e7ce778b2482b48a2c4f8` |

## Tool-call manifest availability

No independent tool-call manifest exists for these arms.
They were dispatched in-session (Agent tool subagents), the same mode the 2026-08-10 wave preregistered with the same limitation ("these arms are dispatched in-session and the harness manifest is not extracted"); the harness reports only aggregate tool-call and token counts, which the run file records.
Consequences, labelled per `scenarios.md`'s transcript-evidence rule (a claim that an action did *not* happen needs harness evidence):

- Forbidden-path compliance (no reads of `tests/scenarios.md` or `tests/runs/`) is **not independently verified** — it rests on the prompt instruction plus each arm's post-hoc self-reported file list, which named only `SKILL.md` and `references/ledger-template.md` beyond the fixture files.
- The template-read observation is self-report, as the prereg declared it would be.
- Preregistration ordering (`check_prereg.py`) is unverifiable in this mode; S1-class ordering assertions were not scored, consistent with the 2026-08-10 wave's identical scope limit.

None of the scored content depends on these unverified negatives: the one scored assertion (summary-table presence) is checked directly against the archived ledgers, which any reader can re-grep.

## Conclusion-correctness verification figures

Scorer-recomputed from `sessions.csv`/`orders.csv` this session (script rerun against the fixture, not read off the ledgers):

- Site-wide pre 131/4200 = 3.12%, post 125/4971 = 2.51% (reps 2, 3).
- Mon–Fri weekday-matched pre 93/3000 = 3.10%, post 97/3800 = 2.55% (rep1's variant).
- `/lp/summer-sale` 6/1053 = 0.57%; `/home` post 70/2615 = 2.68%; `/product` post 49/1303 = 3.76%.
- Per-weekday `/home` and `/product` checkout counts identical across all five matched pairs (rep1's T2 exact-match claim).
- `checkout_reached` vs `orders.csv` daily counts match on 06-01..06-12 and diverge exactly on 06-13 (17 vs 23) and 06-14 (11 vs 17) (rep1's T4).

Every figure each arm's conclusion rests on reproduces exactly.
