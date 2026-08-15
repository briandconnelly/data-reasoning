# Harness evidence — T13/T14 two-skill prompted-dispatch wave

Companion to `2026-08-11-t13-t14-trigger-prereg.md`; run files at `../2026-08-11-t13-trigger.md` and `../2026-08-11-t14-trigger.md`; raw archive in `2026-08-11-t13-t14-trigger/`.

## Harness

`tests/run_trigger.py` on this branch is the instrument: it parses both descriptions live from `SKILL.md` frontmatter (900–1024 char gate), builds the stated-catalog dispatch prompt, runs one fresh `claude -p --output-format stream-json --verbose` process per rep with cwd outside the repository (hard-enforced before launch), archives the raw JSONL, and emits per-rep `detect.json` plus a `summary.tsv` row.
Its detector was validated before any arm: synthetic-transcript tests for all three `ROUTE:` values, a backtick-wrapped token, a negation sentence without a token (→ `unclear`, never guessed), and an invalid transcript (→ `valid=False`); live smoke tests c-eda/c-hda/c-none each parsed correctly.
`claude` CLI 2.1.227; repo at `4efdeec` throughout; per-invocation manifests in the archive record both `SKILL.md` SHA-256s, both parsed-description SHA-256s, per-scenario filled-prompt SHA-256s, and the per-rep catalog order.

## Cross-model design review (PROTOCOL step 3)

The wave design was reviewed by GPT-5.6-Sol (Codex) after the first prereg draft and harness build, before any arm ran.
Eleven findings; every one was accepted and applied:

1. Scratch cwd could land inside the repo → `--scratch-root` separated from the archive dir, repo-cwd hard-fail added.
2. Activation OR-conflated selection with consultation → replaced by the three-signal construct (selected / consulted / executed), scored on `selected` only.
3. First-mention stated-choice classifier inverted negations → replaced by the machine-readable `ROUTE:` token, no-match → `unclear`.
4. T14 lacked its positive assertion (a `none` arm would have passed) → T14-A1 made symmetric.
5. Verdict table overlapped and had unreachable/multi-match outcomes → precedence-ordered gates plus an exhaustive per-cell outcome classification.
6. Smoke tests are not rationale canaries → one excluded rationale canary per scored cell, hand-scored before the scored reps ran.
7. Fixed catalog order confounded with the seam → counterbalanced within cell, order recorded per rep; wave reframed as prompted dispatch, not deployment activation.
8. "The seam holds" overclaims at n=5 → screening language and Clopper–Pearson bounds throughout.
9. Manifest overwrites and silent rerun overwrites destroyed provenance → per-invocation manifests, duplicate-rep refusal, disclosed `--rerun-suffix`.
10. Malformed JSONL silently tolerated → transcript validity checks (`valid`/`invalid_reason`), voids enforced.
11. Behavior negatives are trivial without data → demoted to recorded observations; behavior deferred to a fixture-backed wave.

The prereg was revised once to incorporate findings 2, 4, 5, 6, 7, 8, and 11 — before any arm ran.

## Deviations observed in the wave

- Three T13 reps (1, 3, 5; all eda-first) emitted the ROUTE token after one to three initial Bash calls rather than before the first tool call. Tokens present and unambiguous; manual transcript review confirmed every detector classification. Zero `unclear` across the wave.
- Arms invoked Bash despite `--allowedTools Read Write Glob Grep`: the flag controls approval-free tools, not availability. Recorded as an environment property of every arm equally.
- One void: original t14-rep1 timed out at 600s (killed, no result event), preserved in the archive and rerun once as `t14-rep1-r2` per the preregistered gate.

## What this wave narrows, and what remains owed

This wave discharges the T13/T14 entry in the debt `decisions/003` records, in its two-description synthetic form: under prompted dispatch with both descriptions present, the entity minimal pair routed 5/5 and 5/5 to the expected skills.
Still owed and untouched: the four-skill deployment spot check with corpus-shaped queries, real skill installation rather than a stated catalog, and any behavior measurement (no fixture exists; `tests/fixtures/` is still absent for this skill).
