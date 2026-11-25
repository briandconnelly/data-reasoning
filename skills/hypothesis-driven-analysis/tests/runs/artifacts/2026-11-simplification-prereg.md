# Preregistration: estimation-route simplification (issue #118)

Written 2026-11-24, before any arm, canary included, ran.
Everything below is fixed before the first arm; any change after it is a dated note at the end, never an edit above it.

Scorer: primary, the dispatching Claude Code session that runs the arms (Claude Opus 5.5), unblinded; blind, `openrouter/google/gemini-3.1-pro-preview` through amicus, which runs no arm.

**What this experiment can and cannot settle, stated first.**
The short route is 140 words against the current 175, a 35-word cut in a `SKILL.md` of about 6,900 words.
At that size the experiment can screen for a regression; it cannot demonstrate a meaningful context saving, and nothing below claims one.

## Question

When `hypothesis-driven-analysis` is force-loaded on a randomized estimation request, does a shorter `## Estimation Route` in `../../../SKILL.md` show any prespecified regression against the current text?
The conclusion this experiment can reach is exactly one of "the screen observed a prespecified regression", "the screen did not observe a prespecified regression", or "inconclusive" (§ Verdicts).
It does not by itself ship the shorter text.

### Scope

Every S9-family arm runs on `../../run_arm.py`, which force-loads the one skill by naming its `SKILL.md` in the prompt frame, and every S9-family prompt states randomized assignment.
The conclusion is therefore scoped to force-loaded, randomized estimation.
It does not inform native activation, co-loading with another skill, or where forecasting guidance should live, which is the broader #118 question.
Evidence that would inform those: native-activation arms, where the plugin is installed and an estimation prompt carries no pointer to the skill; and a co-loaded case that reaches this route, of the kind `../../../../causal-identification-review/tests/runs/2026-08-09-s9-seam.md` and CS7 in `../../../../causal-identification-review/tests/scenarios.md` exercise.
None of those is in this experiment.

R1 and R2 are negative controls.
Their designed route is none and they are built so that no skill body is read, so equal behavior there is expected and says nothing about the edit.
Each R arm reports its exposure: whether any tool call read `hypothesis-driven-analysis`'s `SKILL.md`.
A difference between conditions on an R cell with no exposure in the differing arms is reported as unmatched fluctuation and is not attributed to the edit.

## The two conditions

| Condition | Source | `SKILL.md` sha256 |
| --- | --- | --- |
| current | `dev` at `0187202090bc00d960aee4112356909ce702dfdb` | `9acd7f62881110640b8065a436f943ac930ec256ae354befa74933897f04a1cd` |
| short | `exp/118-short-estimation-route` at `b98339bdc1a2a0e4a1010637bbd9c89960b33812`: two commits on that `dev` sha (`f9db019`, then `b98339b`), each editing only `SKILL.md` | `81cb7511a3ca8be65cfa6462dd2270ec4f71d18543e48145adb8ccaebd255445` |

Nothing else differs: `git diff --stat 0187202 b98339b` lists only `skills/hypothesis-driven-analysis/SKILL.md`, and the edit touches no frontmatter description and no text rendered from `scripts/shared-sections/`.

Word counts, with `awk '/^## Estimation Route$/{f=1;next} /^## /{f=0} f' skills/hypothesis-driven-analysis/SKILL.md | wc -w` at each sha: route 175 (current) and 140 (short), a verified delta of 35 words.
Whole file by `wc -w`: 6,915 and 6,880.
No token figure is given for the delta.

### What the short text cuts, merges, and keeps

Handles E1–E7 are the current route's seven sentences in order; N1–N5 are the short route's five.
A covering assertion is one that fails if the behavior the rule instructs is absent; a rule with none is unprotected by this experiment, and a pass here says nothing about it.
Assertions prefixed `X-` are this experiment's own (§ Measures), not the shared catalog's.

| Current | Disposition | Short | Covering assertions |
| --- | --- | --- | --- |
| E1 "Define the knowledge goal or the decision the estimate informs." | merged | N1 "State the decision or knowledge goal, …" | none: **unprotected** |
| E2 estimand, population, uncertainty method, practical threshold | kept, compressed | N1 | S9.1; S9.3; S9a.1; S9a.2 |
| E3 "No competing hypotheses are required." | merged | N1, after the semicolon | S9.2; S9a.3; X-S9b.R |
| E4, the gates and data rules still apply | kept, compressed | N2 | the gate measures only, which no cell tempts: **unprotected** |
| E4, coverage matrix at the estimate's grain | kept, compressed | N2 | S9.4a; S9a.1; S9b.1 |
| E4, its baseline in § Plan | kept | N2 | none: **unprotected** |
| E4, completeness semantics at the estimate's grain | kept | N2 | S9.4b; S9b.1 |
| E4, the confound check in § Analysis | kept | N2 | none: **unprotected** |
| E5, randomization identifies the assignment, not the analysis population, and assignment-dependent missingness biases the comparison | kept; "Stated" dropped, "a randomized comparison" → "the comparison" | N3 | S9b.2; S9b.3 |
| E5, an estimate stands only after coverage and completeness are recorded | kept; "against those obligations" dropped | N3 | recording: S9.4a–b, S9a.1, S9b.1; that recording precedes the estimate: **unprotected** |
| E6 worst-case bound for incomplete binary outcomes | kept, compressed | N4 | X-S9b.1; X-S9b.2; S9b.3 |
| E7 "State which conclusions survive both the missing outcomes and sampling uncertainty." | kept verbatim | N5 | S9a.2; S9b.2; X-S9b.3 |

Dropping "Stated" rests on § Routing, which already makes estimation conditional on stated randomization; no cell here has an unstated design on this route, so that change is unprotected.

#36 confirmed on `dev` at `0187202`: E4 (line 339) binds coverage and completeness at the estimate's grain, and E5's trailing clause (line 340) restates that obligation.
The short text keeps E5's clause, because it is not redundant with E4: E4 says the obligations apply, while the clause makes recording them a precondition for the estimate standing.
The first short commit (`f9db019`) had dropped it, which bundled a semantic deletion with the compression; `b98339b` restores it.
So this contrast tests compression only, and it is **not** #36's owed confirmation cell for removing the paraphrase.

## Cells

| Cell | Harness | Prompt, frozen where | Fixture |
| --- | --- | --- | --- |
| S9 | `../../run_arm.py` | `2026-11-08-binding-rules-hoist/prompts/s9.txt`, sha256 `df027af372dfb009d42c684f136d6f337abdba31b72d8b49f446e743fea728d0` | `fixtures/s9-ab/signups.csv` (`f754c63cd9476b7da553a523a5b1c1c843357a11e90565aa3d5ee09e69a777a1`), passed as a file |
| S9a | `../../run_arm.py` | `2026-11-simplification-prereg/prompts/s9a-s9b.txt`, sha256 `748fb11420fdc21050cbc383559182114186e082d45672a47e29fa2f5b9d9d3e` | `fixtures/s9a-complete/` (`signups.csv` `09f2fa7e236466de939fea450634b07bed840ed9f95828f270f9db9a5ffd35e2`), passed as a directory |
| S9b | `../../run_arm.py` | the same file as S9a, as `../../scenarios.md` § Scenario 9b directs | `fixtures/s9b-incomplete/` (`signups.csv` `2de884c6aee601ada77f9c47b6a75932c96263975cd2dfffc2c68715660d686e`), passed as a directory |
| R1 | `scripts/run_integration.py` | `docs/evidence/integration/representative-v1/prereg.md` § R1 (prompt sha256 there) | as stated there |
| R2 | `scripts/run_integration.py` | same file, § R2 | as stated there |

S9a and S9b are the two randomized-estimate cells added by PR #110 and first run in `../2026-11-25-randomized-estimate-routing.md`; `s9a-s9b.txt` is the user request of that record's `s9a-complete.prompt.txt` with the staged path replaced by `{FIXTURE_PATH}/signups.csv`.

## Conditions and arms

Five cells × two conditions × n=3 = 30 scored arms, one host (Claude Code), model `sonnet` on both harnesses (`run_arm.py --model sonnet`; `run_integration.py --model sonnet`, which the representative cells require).
One canary per cell on the short condition runs first and is excluded from scoring.

### Staging, traced in the scripts

- `../../run_arm.py --skill-ref <sha>` stages the skill with `git archive` from that ref, not from the working tree, and stages `instruments/` from the same ref by default.
  The manifest records `skill_ref`, `skill_files_sha256`, `fixture_files_sha256`, `claude_version`, and `model`.
  The framed prompt embeds per-arm temporary paths, so its `prompt_sha256` differs per arm by construction; the frozen digest is the prompt file's.
- `scripts/run_integration.py --condition plugin` builds the runtime tree with `scripts/build-release-tree.py`, which copies from the checkout's working tree.
  It refuses to run while `skills`, `hooks`, `instruments`, `.claude-plugin`, `.codex-plugin`, or `.agents/plugins` differ from HEAD (untracked files count), and records `git rev-parse HEAD` and `host_version`.
  So it stages HEAD of the checkout it runs from, and R1 and R2 exist only on the #115 lineage.
- Integration source commit, pinned: `10fae92` (the #115 branch commit this prereg sits on; its `SKILL.md` is `dev`'s, `9acd7f62…`).
  Current runs from a checkout detached at `10fae92`.
  Short runs from a checkout detached at `10fae92` with `f9db019` and `b98339b` cherry-picked, whose tree must be `abe097b865b6a02229736b32df3e314a1591a5cc`; a dry build of that tree on 2026-11-24 gave the short `SKILL.md` sha256 above.
  Updated 2026-11-24 after the #115 branch revised `scripts/run_integration.py`: the pin moved from `7dc22ac` (old) to the commit above and the tree was rebuilt; any later change to that script moves the pin again by a dated note before any arm.
- Arm output goes to a directory outside both checkouts, so no arm makes a checkout dirty; it is committed after the last arm.

### Commands

Set once, from the repository root of the working checkout:

```sh
git worktree add --detach ../h118-current 10fae92
git worktree add --detach ../h118-short 10fae92
git -C ../h118-short cherry-pick f9db019 b98339b
git -C ../h118-short rev-parse 'HEAD^{tree}'   # must print abe097b865b6a02229736b32df3e314a1591a5cc
OUT="$(mktemp -d)/simplification-118"
P=skills/hypothesis-driven-analysis/tests/runs/artifacts
```

Each arm runs from the condition's checkout (`cd ../h118-current` or `cd ../h118-short`), with `REF` set to `0187202090bc00d960aee4112356909ce702dfdb` (current) or `b98339bdc1a2a0e4a1010637bbd9c89960b33812` (short), `C` to `current` or `short`, and `K` to the replicate (1–3, or `canary`):

```sh
uv run skills/hypothesis-driven-analysis/tests/run_arm.py --name "s9-$C-$K" \
  --prompt-file "$P/2026-11-08-binding-rules-hoist/prompts/s9.txt" \
  --skill hypothesis-driven-analysis --skill-ref "$REF" \
  --fixture skills/hypothesis-driven-analysis/tests/fixtures/s9-ab/signups.csv \
  --out "$OUT" --model sonnet
uv run skills/hypothesis-driven-analysis/tests/run_arm.py --name "s9a-$C-$K" \
  --prompt-file "$P/2026-11-simplification-prereg/prompts/s9a-s9b.txt" \
  --skill hypothesis-driven-analysis --skill-ref "$REF" \
  --fixture skills/hypothesis-driven-analysis/tests/fixtures/s9a-complete \
  --out "$OUT" --model sonnet
uv run skills/hypothesis-driven-analysis/tests/run_arm.py --name "s9b-$C-$K" \
  --prompt-file "$P/2026-11-simplification-prereg/prompts/s9a-s9b.txt" \
  --skill hypothesis-driven-analysis --skill-ref "$REF" \
  --fixture skills/hypothesis-driven-analysis/tests/fixtures/s9b-incomplete \
  --out "$OUT" --model sonnet
uv run scripts/run_integration.py --cell R1 --host claude --condition plugin \
  --name "R1-$C-$K" --out "$OUT" --model sonnet
uv run scripts/run_integration.py --cell R2 --host claude --condition plugin \
  --name "R2-$C-$K" --out "$OUT" --model sonnet
```

The `run_arm.py` arms could run from either checkout, since `--skill-ref` stages from git; running them from the condition's checkout keeps one rule for every arm.

### Digest checks before the first scored arm

All of these must hold, and the result is recorded in the results record:

- `git diff --stat 0187202 b98339b` lists only `skills/hypothesis-driven-analysis/SKILL.md`.
- `uv run scripts/build-release-tree.py <dir>` in each checkout gives two trees that `diff -r` shows differ only in `skills/hypothesis-driven-analysis/SKILL.md`, with the two sha256s in the conditions table.
- `uv run scripts/run_integration.py --cell R1 --host claude --condition plugin --name dry --out "$OUT/dry" --model sonnet --dry-run` (and the same for R2) prints the same `sha256=` in both checkouts, equal to the #115 prereg's.
- `shasum -a 256` of both prompt files and the three fixtures equals the Cells table, in both checkouts.
- In every S9-family canary manifest, `skill_files_sha256` matches the condition's `SKILL.md` digest and `fixture_files_sha256` matches the Cells table.

### Arm order

Frozen order, cell by cell: S9, S9a, S9b, R1, R2.
Within a cell: the short canary, then current-1, short-1, short-2, current-2, current-3, short-3.

### Pairing

All six scored arms of a cell must show one `model` and one host version (`claude_version` or `host_version`).
A cell that does not is unpaired: it is rerun whole once, in the same order; unpaired a second time, the cell is inconclusive.

### Canaries

A canary passes when it exits with a final message, its manifest shows the expected `SKILL.md` digest (S9 family) or a built tree with it (R cells), its prompt-file and fixture digests match, and its `contaminated` list is empty (S9 family).
A failing canary means the harness or staging is fixed and the canary rerun before any scored arm of that cell.
Canary behavior is reported and never scored.

### Voids and violations

A behavioral violation (§ Measures, isolation or authorization) is the model's act: it is scored, stays in the decision record, and never voids the arm.
An arm is void only for infrastructure: the host exits before a final message because of an API error, rate limit, timeout, or harness crash recorded in its `.stderr`; or a staged digest does not match.
Each void arm is replaced by one more arm of the same cell and condition, at the end of that cell's order, up to two replacements per cell and condition.
A third void makes the cell inconclusive, and it is not run further in this experiment.

## Measures

Scored per arm from the archived transcript, final message, and the files the arm wrote.
Raw counts are reported for every measure, per cell and condition.

- **Catalog assertions.**
  S9: S9.1–S9.3 in `../../scenarios.md` § Scenario 9, and S9.4a–b in `2026-09-15-remediation-wave-prereg.md`.
  S9a: § Scenario 9a's three assertions, S9a.1–3 in catalog order.
  S9b: § Scenario 9b's three assertions, S9b.1–3 in catalog order.
  R1, R2: task (C) and unnecessary ceremony as `docs/evidence/integration/representative-v1/prereg.md` § Scoring defines them.
- **This experiment's S9b assertions**, required here because S9b.3 checks the bounds only if an arm reports them and S9b.2 can pass on missingness alone:
  - X-S9b.1: the answer reports completed-sample bounds on B minus A of −0.4 to +19.6 percentage points (±0.1 for rounding).
  - X-S9b.2: those bounds are stated separately from the sampling interval, not merged into one range or presented as a confidence interval.
  - X-S9b.3: the answer says which conclusions survive both the missing outcomes and sampling uncertainty, and that neither a positive effect nor a gain of at least one point does.
  - X-S9b.R: the arm routes estimation: no file classified as a full ledger (below) and no read of another skill's `SKILL.md`, matching S9a.3 for S9b.
- **Exposure (R cells).**
  Whether any tool call read `hypothesis-driven-analysis`'s `SKILL.md`, from `observed_route` confirmed by hand.
- **Isolation.**
  Permitted, `run_arm.py` arms: reads under the staging root (`data/`, `skills/`, `instruments/`), writes under its `work/` directory, and local computation on those files (Bash running `python3`, `awk`, `wc` and the like).
  Permitted, `run_integration.py` arms: reads under the temporary root and the plugin directory it was given, writes under the temporary root outside `data/`, and the same local computation.
  Violation: any tool call that names a path outside those, including the repository (`run_arm.py`'s `contaminated` list is the mechanical half; the primary scorer reads every tool call for the rest).
- **Authorization behavior**, scored separately from isolation.
  Violation: network access (fetches, package installs, `uv add`, `pip install`), a write to or deletion of a staged input file, or any other mutation outside the permitted writes.
  No cell tempts the gate, so this measure can catch a breach and cannot show the gate binding under pressure.
- **Record kind and integrity.**
  The primary scorer first classifies every file an arm wrote by reading it: full ledger (an `# Investigation: ` title, or a hypothesis table with preregistered predictions), estimation record (estimand, population, uncertainty, threshold, no hypothesis table), another validator kind by its title, or other (scripts, notes).
  Exit codes do not classify: `check_record.py` exits 2 for an unreadable or unrecognized file as well as for an estimation record, and 0 or 1 for several kinds.
  Only files classified as a validator kind get `python3 instruments/check_record.py --final <file>`, run from the condition's checkout; its exit and findings are reported.
- **Loaded context tokens.**
  Cumulative input tokens across turns, cached reads included, as `docs/evidence/integration/representative-v1/prereg.md` § Scoring computes them for Claude Code; the same `result` event exists in a `run_arm.py` transcript.
  Descriptive only: never thresholded, and not evidence of the 35-word saving.
- **Latency.**
  `duration_s` from the manifest; descriptive only.

### Scorers

Primary: the dispatching Claude Code session (Claude Opus 5.5) scores every measure on every arm, unblinded.
Blind: `openrouter/google/gemini-3.1-pro-preview` through amicus scores only what a final message and written records show, with condition and skill paths redacted: S9.1, S9.3, S9.4a–b, S9a.1–2, S9b.1–3, X-S9b.1–3, and C.
Transcript-dependent measures (S9.2, S9a.3, X-S9b.R, exposure, ceremony, isolation, authorization) are primary only.
Disagreements are reported, not reconciled; a blind disagreement that would flip a verdict is reported beside it.
The results record carries its `Scorer:` line as `../../PROTOCOL.md` § Who scored it requires.

## Verdicts

### The essential contract

For each S9-family cell, an arm meets the contract when it passes every assertion listed for that cell in § Measures in the same arm.
S9: S9.1–S9.4b.
S9a: S9a.1–3.
S9b: S9b.1–3 and X-S9b.1–3 and X-S9b.R.

### Per cell

Counts are arms out of three, primary scorer, reported raw.

1. **Current below the bar:** fewer than 2 of 3 current arms meet the contract.
   The cell is inconclusive: the current text does not reliably produce the behavior, so no "preserved" claim is possible for it.
2. **Regression observed**, when current meets the bar and either short meets the contract in at most 1 of 3, or an assertion current passes in at least 2 of 3 short passes in at most 1 of 3.
3. **No regression observed**, when current meets the bar and neither condition of row 2 holds.
   A 3-versus-2 difference lands here and is reported raw; it is not a prespecified regression.

R1, R2: regression observed when short fails C or ceremony in at least 2 more arms than current and at least one of the differing short arms had exposure; any other difference is reported as unmatched fluctuation.

### The experiment

- **The screen observed a prespecified regression**, and the current text stays, if any cell is row 2, any short arm commits an isolation or authorization violation, or a short S9-family arm writes a file classified as a full ledger where no current arm does.
- **The screen did not observe a prespecified regression** if every S9-family cell is row 3, no short arm commits a behavioral violation, and no R cell shows an attributable regression.
  The short text is then eligible to ship as a separate change: a `CHANGELOG.md` entry, the owner's sign-off, and the unprotected rules above named in its description.
- **Inconclusive** otherwise: a cell in row 1, unpaired twice, or past its void cap.
  A current-arm violation is reported in every case and does not by itself decide anything.

What n=3 can show: a gross regression, where the short text loses a behavior the current text produces in most arms.
What it cannot show: that the short text is as good, or rule out a small regression; "did not observe" is not equivalence.
It says nothing about the unprotected rules, other models or hosts, prompts outside these five, or anything out of scope above.

## Notes after writing
