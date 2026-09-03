- When writing markdown, use one sentence per line for easy diffs
- Commit messages follow conventional commits
- A normative rule has exactly one home.
  Every other file points at it and does not paraphrase it — two statements of one rule diverge silently, and nothing fails when they do (see `skills/hypothesis-driven-analysis/decisions/004-single-authority-for-normative-rules.md`)
- Text that must ship inside more than one standalone skill is rendered from one source file under `scripts/shared-sections/` and never hand-copied (see `skills/hypothesis-driven-analysis/decisions/007-shared-text-is-rendered-not-copied.md`)
