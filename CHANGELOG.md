# Changelog

All notable changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
The version is the `version` field of the plugin manifests; installs track the `main` branch, which is rebuilt from `dev` on every push, so a version bump marks a notable change rather than a separate publish.

## [Unreleased]

### Fixed

- Decision analysis: the record validator now enforces the Numeric Policy's provenance rules — every provenance mention comes from the closed class set, `sensitivity-only` may not appear in Evidence and update, a `robust` verdict's losses must be `user-elicited` or `externally-sourced`, and a `dominated` verdict's belief slots read `none needed` (#60).

### Changed

- The README is a short introduction; install verification, record validation, the output style, and evidence status moved to pages under `docs/`, which ship with the plugin.

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
