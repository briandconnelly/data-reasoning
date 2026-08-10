# Transcript evidence — 2026-08-08 rerun of owed trigger arms S2/S3/S17/S18

Four Sonnet trigger-discrimination arms dispatched 2026-08-08 (2026-08-09T03:41Z), scored in `tests/runs/2026-08-08-scenario{2,3,17,18}-trigger-rerun.md`, paying Owed-measurements debt 1 (the 2026-07-20 ungated description edit superseded every prior S2/S3/S17/S18 run).
Transcripts, manifests, and text streams live in `.superpowers/sdd/2026-08-08-causal-identification-review-skill/task-0.1/`; controller-recorded dispatch facts are in that directory's `dispatch-facts.md`, treated here as claims re-run independently, not results copied.
Manifests and text streams were regenerated from the committed transcripts with `tests/extract_evidence.py` (`identity`, `manifest --normalize-root`, `text` subcommands) in this scoring session and diffed byte-for-byte against the committed `s{2,3,17,18}-manifest.tsv`/`s{2,3,17,18}-text.txt`: all four pairs matched exactly, confirming the committed files were not hand-edited after generation.

## Transcript digests (sha256)

Piped through `shasum -a 256` in this scoring session (never hand-copied); the `identity` subcommand's own digests of the same files agree byte-for-byte on all four:

```text
902badc84e88ba198dc959cb58b49af9327af435fb7194db209a26c51877b1b7  s2-trigger.jsonl
1eafa9164ac4db9adbdaa19da8e6de1c6fe7eacde7b4b308eb7f3e4d07bd50d2  s3-trigger.jsonl
e78b96554d7fdd40d32f5c0a358eb34ef98b29d8834aabcf079d2272765289e1  s17-trigger.jsonl
34778413d223d57d4da2804a1cfae5c39b683ee175892ef148f802211195bb73  s18-trigger.jsonl
```

These also match the digests `dispatch-facts.md` recorded at dispatch time.

## Identity counts vs harness-reported

| Transcript | tool_use (identity) | breakdown | paired results | harness-reported tool calls | match |
| --- | --- | --- | --- | --- | --- |
| s2-trigger | 3 | Bash: 2, Read: 1 | ok: 3 | 3 | yes |
| s3-trigger | 9 | Bash: 5, Edit: 1, Read: 3 | error: 1, ok: 8 | 9 | yes |
| s17-trigger | 7 | Bash: 4, Read: 2, Skill: 1 | error: 1, ok: 6 | 7 | yes |
| s18-trigger | 18 | Bash: 11, Read: 2, Write: 5 | error: 2, ok: 16 | 18 | yes |

Harness-reported tool-call counts are from `dispatch-facts.md` (9 / 7 / 18 for S3/S17/S18; 3 for S2, alongside its token figure).
Token total for S2 (33,154) is harness-reported, per `dispatch-facts.md`; S3/S17/S18 token figures did not reach the controller (retrieved without usage blocks), so none is recorded for them rather than reconstructed.

## Machine checks: zero git commands, zero repo-directed writes, zero absolute-path repo redirects

Each scan below was run by the scoring session (not copied from `dispatch-facts.md`'s claims) over the four regenerated manifests, and each pattern was validated against a planted positive written in this session before its zero was trusted.

**git commands** — `grep -E '(^|[^a-zA-Z])git[[:space:]]'`:
Planted positive (a one-line file containing `git status` as a manifest row) fires.
Run over `s2-manifest.tsv s3-manifest.tsv s17-manifest.tsv s18-manifest.tsv`: 0 matches (exit 1).

**write-tool rows** — `awk -F'\t' '$3=="Write"||$3=="Edit"||$3=="NotebookEdit"'`:
Planted positive (a one-line Write row) fires.
Run per manifest: S2 none, S17 none, S3 one `Edit` (ordinal 7, `arm-s3/s3-bug/dateutils.py` — the fix the prompt asked for), S18 five `Write`s (ordinals 10/12/14/16, `analyze.py`..`analyze4.py`, plus ordinal 18 `ledger.md`) — all under each arm's own `<SCRATCH>/trigger-arms/arm-*/` directory.
These counts match `dispatch-facts.md`'s claims exactly.

**repo-directed redirects** — `grep -E '(>|>>|tee)[[:space:]]*"?/Users/bdc/projects/data-reasoning/.claude/worktrees/causal-identification-review'` (the literal worktree root, since `--normalize-root` rewrites any real occurrence of it in emitted manifest text to `<REPO_ROOT>` — see below):
Planted positive (a manifest row with `echo hi > "<worktree-root>/x.md"`) fires.
Run over all four manifests: 0 matches (exit 1).

**Corroborating checks, run in this scoring session:**
`git status --porcelain skills/` after generating all four manifests: empty output — no tracked-or-untracked change under `skills/` from any arm.
`grep -c REPO_ROOT` over all four manifests: 0 in every file — since `extract_evidence.py manifest --normalize-root` rewrites any occurrence of the worktree's absolute path to the literal string `<REPO_ROOT>`, a zero count means no manifest row's target or command text ever referenced the repository path at all, not merely that it was never redirected into — a stronger statement than the redirect-only scan above, and consistent with the arms being confined to `<SCRATCH>/trigger-arms/`.

Scope, as in the 2026-07-18 corpus: these scans establish only that the manifests contain no Write/Edit/NotebookEdit rows outside per-arm scratch and no Bash command text redirecting to an absolute repository path; they do not cover relative redirects after a `cd`, non-redirect file utilities (`touch`, `cp`, `sed -i`), or in-interpreter writes inside a heredoc/`-c` script.
The heredoc/`-c` bodies visible in all four manifests were read in this session and contain only reads, computation, and prints against fixture/scratch paths; every observed Write/Edit target above is under `<SCRATCH>/trigger-arms/arm-*/`.

## Fixture digests (sha256)

Recomputed independently in this scoring session against both the staged scratch copy the arms actually saw (`<SCRATCH>/trigger-arms/data/...` and `<SCRATCH>/trigger-arms/arm-s3/s3-bug/...`, still present on disk) and the repository fixtures — all three match each other and the values `dispatch-facts.md` and the 2026-07-18 evidence artifact recorded:

```text
39486b25560ac523af351bf4376d1fe9e4c8d2c267c63b95e7e9fa7b1ada1ddc  s1-conversion/orders.csv
eea96d9793a56153d23f7412a1cebbba2ac0fb2eadd0acb4f1b9a41650a8523c  s11-mini/checkout_latency.csv
47279ba7b5d49cc6523c692a77d90bbdbe9e8881d08cdb51216050fe7a9b28b9  s3-bug/test_dateutils.py
```

## Verbatim skill-selection sentences

Each arm was instructed: "Before your first tool call, state in one or two sentences which skill (or none) you are using and why."
These are the transcripts' text blocks, quoted exactly, via `tests/extract_evidence.py text`.

**s2** (text block 1, before any tool call): "No skill needed — this is a bounded descriptive query (compute a median from given data), not a hypothesis to test or open-ended exploration."

**s3** (text block 1, before any tool call): "I'll use the **systematic-debugging** skill since this is a reproducible test failure that needs root-cause diagnosis before a fix."

**s17** (text block 1, before any tool call): "This is a stated claim needing adjudication (\"p95 exceeded 500ms yesterday\") — the exact example in hypothesis-driven-analysis's trigger description. I'll load that skill."
(Text block 2, after the errored `Skill` tool call: "The Skill tool doesn't recognize that name (it's a path-based catalog, not a registered skill). I'll read the SKILL.md directly to follow its procedure.")

**s18** (text block 1, before any tool call): "I'm using the hypothesis-driven-analysis skill: this is a diagnostic \"what's driving the drop\" question about a metric change with multiple plausible explanations, which is exactly its trigger case (not a bounded lookup)."

All four placed the choice statement before their first tool call, as instructed — no placement-drift fidelity note is owed for any of the four this wave, unlike several 2026-07-18 probes.

## First-user-message description verification

Each transcript's first user message embeds a stated skill catalog with one `Description:` paragraph per skill.
This section checks, programmatically, that the `hypothesis-driven-analysis` and `exploratory-data-analysis` entries in each transcript's catalog carry the SKILL.md descriptions committed at HEAD, not stale text.

Method: for each of the two `SKILL.md` files, the frontmatter `description:` YAML scalar was parsed from line 3 (single-quote unescaping, fold whitespace); for each transcript, the first `user`-type JSONL record's `message.content` was searched for the named skill's catalog entry and its `Description:` paragraph extracted up to the next blank line.
The two strings were then compared for exact equality.
Script: `check_descriptions.py` (run via `python3`, not committed — a one-off verification script; reproduced here in full for auditability).

```python
import json, re

def skillmd_description(path):
    with open(path) as f:
        text = f.read()
    frontmatter = text.split("---", 2)[1]
    m = re.search(r"description:\s*'((?:[^']|'')*)'", frontmatter, re.DOTALL)
    raw = m.group(1).replace("''", "'")
    return re.sub(r"\s+", " ", " ".join(l.strip() for l in raw.split("\n"))).strip()

def transcript_first_user_message(jsonl_path):
    with open(jsonl_path) as f:
        for line in f:
            obj = json.loads(line)
            if obj.get("type") == "user":
                return obj["message"]["content"]

def extract_catalog_description(message_text, skill_name):
    pattern = r"\*\*" + re.escape(skill_name) + r"\*\*.*?Description:\s*(.*?)\n\n"
    m = re.search(pattern, message_text, re.DOTALL)
    if not m:
        return None
    return re.sub(r"\s+", " ", " ".join(l.strip() for l in m.group(1).split("\n"))).strip()
```

Result, run against all four transcripts in this scoring session:

| Transcript | hypothesis-driven-analysis description | exploratory-data-analysis description |
| --- | --- | --- |
| s2-trigger | MATCH | MATCH |
| s3-trigger | MATCH | MATCH |
| s17-trigger | MATCH | MATCH |
| s18-trigger | MATCH | MATCH |

All eight comparisons matched exactly (`ALL MATCH`, script exit 0).
The parsed `hypothesis-driven-analysis` description is 1020 characters, confirming `tests/scenarios.md`'s "1020 of 1024 characters" note independently.
This establishes that all four arms were dispatched against the descriptions committed at HEAD (the 2026-07-20 edit), not a stale copy — the machine basis for calling this wave a rerun *against the current description*, not merely *a* rerun.

## Preregistration ordering — S18 (fidelity note, not a scored assertion)

S18's assertion table has no preregistration-ordering assertion, so this does not affect either assertion's score; it is recorded because `dispatch-facts.md` flagged S18's ledger-write ordinal for scoring attention.

```text
$ check_prereg.py s18-manifest.tsv --ledger-pattern 'ledger' --data-pattern 's1-conversion'
PREREG_WRITE: ordinal 18 (Write -> <SCRATCH>/trigger-arms/arm-s18/ledger.md)
CLASSIFY: 11 tool_use(s) precede the ledger write; classify each as orientation or analysis...
exit=1
```

The 11 pre-write rows include four `python3 <SCRATCH>/trigger-arms/arm-s18/analyze*.py` executions (ordinals 11, 13, 15, 17) — these are analysis (cause-outcome relationships computed and printed), not orientation, by the same standard `tests/scenarios.md` line 17 uses for the full-route ordering check.
Reading the ordinal-18 `Write` event's content confirms the ledger is a complete hypothesis table (Problem, Orientation, Hypotheses, Tests) written in one shot after `analyze4.py`'s output was already in hand — matching `SKILL.md` line 170's description of what a ledger appearing "first in the final report" looks like.
So this run's ledger documents the investigation retrospectively rather than committing to it beforehand; it does not change either S18 assertion's PASS, since neither assertion tests preregistration ordering, but it is a genuine fidelity gap relative to `SKILL.md`'s own preregistration rule, distinct from S18's scored behavior (activation and composition).

## Catalog-composition deviation (scope note)

`dispatch-facts.md` states this wave's catalogs are the **current two-skill shipped surface** (hypothesis-driven-analysis + exploratory-data-analysis) plus each scenario's required stand-in (`systematic-debugging` for S2/S3/S17, the `s18-analytics` stand-in plus both shipped skills for S18) — not the catalogs earlier waves used.
Two concrete differences, both confirmed against prior evidence in this repository rather than asserted from `dispatch-facts.md` alone:

- **S2/S3/S17 no longer include a visualization skill.** The 2026-07-18 evidence artifact's `pre`-arm skill-choice quote ("not... a visualization request — the three candidate skills' own scope notes rule them out") shows a visualization skill was one of that wave's three catalog entries; this wave's three-entry catalog is hypothesis-driven-analysis + exploratory-data-analysis + systematic-debugging instead.
- **S17/S18 (and now S2/S3) catalogs include `exploratory-data-analysis`,** which did not exist as a shipped skill at the time of the Ninth wave (2026-07-18) or the Thirteenth wave (2026-07-20, S18); `exploratory-data-analysis/SKILL.md` postdates both.

This is a deliberate scope choice, not a defect: the debt being paid is "the current trigger surface has no valid runs behind it," and the current surface is the two shipped skills, so testing against that surface (plus the scenario's required stand-in) is what makes this rerun responsive to the debt.
It does mean this wave's S2/S3/S17 results are not a like-for-like replication of the Ninth wave's catalog, only of its scenario prompts and fixtures.
