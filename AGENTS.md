- When writing markdown, use one sentence per line for easy diffs
- Commit messages follow conventional commits
- A normative rule has exactly one home.
  Every other file points at it and does not paraphrase it — two statements of one rule diverge silently, and nothing fails when they do (see `skills/hypothesis-driven-analysis/decisions/004-single-authority-for-normative-rules.md`)
- Text that must ship inside more than one standalone skill is rendered from one source file and never hand-copied.
  Those sources are `scripts/shared-sections/authorization-gate.md` and `scripts/shared-sections/record-delivery.md` (the `RENDERED` list in `scripts/check-shared-sections.py` is the inventory), not the directory around them: the other files there are frozen goldens that a checker snapshots *to*, and `skills/hypothesis-driven-analysis/decisions/007-shared-text-is-rendered-not-copied.md` settles which file is which
- Branch from `dev` and open pull requests against `dev` (`gh pr create --base dev`).
  `main` is the runtime tree that `.github/workflows/publish-runtime.yml` builds from `dev`; never commit to it or target it.
  GitHub closes issues from `Fixes #N` only on merges into the default branch, which is `main`, so close an issue by hand once its fix merges into `dev`
- `CHANGELOG.md` records every user-visible change under `## [Unreleased]`, in the pull request that makes it; dev-only changes (tests, scripts, evidence) stay out of it.
  A release moves that section under a new version heading, bumps `version` in both plugin manifests, and tags `v<version>` on `dev`
