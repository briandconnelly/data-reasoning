# Changelog

All notable changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
The version is the `version` field of the plugin manifests; installs track the `main` branch, which is rebuilt from `dev` on every push, so a version bump marks a notable change rather than a separate publish.

## [Unreleased]

### Added

- Decision analysis: a record form for a decision with no supported prior — Prior odds and Posterior odds read `none supported — see Robustness`, supported likelihood ratios stay in the Evidence table, an unquantified item is a paired `none supported` row with its reason, and the sweep in Robustness does the arithmetic (#41). Measured on DA-S1, DA-S1x and DA-S3 at n=1 per cell.
- Every skill carries a § Record Delivery section telling the agent to run `check_record.py --final` on a completed record before delivering it, fix findings on the skill's own terms or report them as limitations, and report an unavailable validator as not validated (#63). Rendered from `scripts/shared-sections/record-delivery.md`; measured 2026-11-08 at n=1 per cell on one model (four completed-record cells, a control, and a no-`python3` variant).

### Changed

- Decision analysis: § Numeric Policy now carries one ordered verdict rule (`dominated`, then the loss cap, then `prior-sensitive`, then `loss-sensitive`, then `robust`), treats only `user-elicited` and `externally-sourced` losses as belief-grade, and records a rounded elicited loss at its nominal value with analyst-chosen endpoints as `sensitivity-only`; § The Decide Route's verdict bullets point there. Both checkers enforce the paired sentinels, the loss cap, and per-axis flip tests.
- The evidence-status page reports per-scenario measurement status: one table per skill covering every catalog scenario, with the wording each was measured against, whether that wording ships, and the result; it no longer calls the exploration and decision-analysis catalogs unrun, records the 2026-11-08 settlement of the missing-prior and verdict-precedence debts, and refreshes the context-cost word counts (#68).
- The output style page names both ways to select `Data Answer` — `/output-style data-reasoning:Data Answer` and `/config` → Output style — and records that output styles are supported, not deprecated, in current Claude Code (#70).
- The README is a short introduction; install verification, record validation, the output style, and evidence status moved to pages under `docs/`, which ship with the plugin.
- [Installing](docs/installing.md) now explains how to invoke a skill explicitly in Claude Code and Codex, and reports that automatic routing for `exploratory-data-analysis` was measured only against a reduced catalog, where "Tell me about ..." asks loaded it 8/30 times; explicit invocation itself is unmeasured (#65).

### Fixed

- Decision analysis: a belief slot reading `none needed` under any verdict but `dominated` is a validator finding, so the sentinel cannot be used to clear a provenance finding on a `robust` record (seen in the 2026-11-08 DA-S1 probe).
- The hook's shell wrapper derives the plugin root from its own location when neither `CLAUDE_PLUGIN_ROOT` nor `PLUGIN_ROOT` is set, instead of failing on every write, and a not-validated report names the actual reason: no `python3`, or no Python hook at the resolved root (#64).
- Decision analysis: the record validator now enforces the Numeric Policy's provenance rules — every provenance mention comes from the closed class set, `sensitivity-only` may not appear in Evidence and update, a `robust` verdict's losses must be `user-elicited` or `externally-sourced`, and a `dominated` verdict's belief slots read `none needed` (#60).
- The record validator accepts the identification-review template's probes table (`assessment` and `evidence or reason` columns, not `result`), checks the assessment vocabulary as a closed set, and asks no probe rows of a `not-constructible` design (#61).
- The record validator accepts an exploration log headed `## Frame-lite` for the profile route and asks it for scope and budget only, as SKILL.md § Profile Route prescribes (#62).
- The scenario-catalog link in each skill's introduction resolves: it pointed at `main`, which carries no `tests/` paths, and now pins a `dev` commit that holds the catalog (#67).

## [0.3.0] - 2026-11-01

### Added

- A PostToolUse hook that structurally validates a written record for all four skills, with a fixture-neutral validator and a shell fallback for hosts without `python3`.
- An install checker that verifies an installed plugin root and its hook command.
- Codex install verification: the install checker exercises the manifest hook path, and the README documents recovering an install that carries test skills.
- A runtime-only release tree built by CI onto `main`, so an install never downloads the evidence archive.
- The `data-answer` output style, installed without being forced active.
- Hypothesis-driven analysis: a preregistration checker that recovers the ledger-writing call from shell redirects and heredocs.
- Decision analysis: value-of-information prices are separated from bounds, and bound verdicts are validated.
- Exploratory data analysis: the description claims generic entity-profiling speech acts, with the gain and cost measured.

### Changed

- The hook and validator fail closed on an unreadable candidate, a crashed validator, an unrecognized exit code, invalid UTF-8, and an unterminated fence.
- Records are parsed fence- and escape-aware, HTML comments are stripped before validation, and placeholders are scoped to template slots.
- Causal identification review: an identified-if verdict requires a probe row for every named assumption, and per-assumption assessments ship as an unmeasured clarification.
- Skills cite the scenario catalogs by URL rather than by a path an install does not carry.
- The shared authorization gate is rendered into every skill from one source file instead of being copied.

### Removed

- Decision analysis: the degraded mode for a missing prior and the verdict-precedence paragraph, each withdrawn after failing its preregistered condition.

## [0.2.0] - 2026-08-09

### Added

- The `decision-analysis` skill, with a record template, a fail-closed record checker, and decision records 001 through 006.
- Entity profiling in `exploratory-data-analysis`.
- This repository serves as its own Claude Code plugin marketplace.

## [0.1.0] - 2026-08-08

### Added

- The `exploratory-data-analysis`, `hypothesis-driven-analysis`, and `causal-identification-review` skills.
- The plugin manifest, README, and repository conventions.

[Unreleased]: https://github.com/briandconnelly/data-reasoning/compare/v0.3.0...dev
[0.3.0]: https://github.com/briandconnelly/data-reasoning/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/briandconnelly/data-reasoning/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/briandconnelly/data-reasoning/releases/tag/v0.1.0
