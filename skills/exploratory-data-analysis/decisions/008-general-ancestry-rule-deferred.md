# 008 — The general ancestry rule for measurement claims is deferred

Status: accepted, 2026-08-24.

## Context

Issue #20 sketched a general rule: any claim that a run artifact measured a decision's subject binds the artifact's subject commit, and fails when the decision's adopting commit is not an ancestor of it.
Decision 007 closed #20 with a narrower gate: `scripts/check-measurement-claims.py` binds description-measurement claims only, by content hash against the freeze goldens of decision 006.
Issue #22 asked that the general rule be revisited once the description gate had run for a while, on two questions: whether non-description measurement claims occur often enough to need it, and how a decision record should name its adopting commit.
This record answers the first question with a survey and defers the second.
It lives here for the reason 007 does: it is a cross-skill contract.

### What the survey found, 2026-08-24

Non-description measurement claims are common, not rare.
A grep over the gated prose (the same scope 007's checker reads) for a run record or artifact named beside a measurement verb, without the word "description", returned about 88 lines.
Some have exactly the shape #20 was about, a claim that an artifact measured a specific version of a subject:

- `skills/hypothesis-driven-analysis/tests/scenarios.md` § "Eighth wave, 2026-07-18" — final-wording validation runs against skill text at `a836b23`, then second-refinement runs against skill text at `7c3869f`.
- `skills/hypothesis-driven-analysis/tests/scenarios.md` § "Seventh wave, 2026-07-18" — four runs against the tightened fixtures at `2338f30`.
- `skills/causal-identification-review/tests/scenarios.md` — `SKILL.md`'s cost line replaced with the range measurement wave 1 recorded.

The data the general rule needs exists about half the time, and never in a structured place.
65 of the 120 run records under `skills/*/tests/runs/` contain a commit hash; every one is prose in a bullet, and no field names it as the subject commit.
Decision records name their adopting commit inconsistently: 006 cites `4c72ca2` in prose, 005 is described in this directory's README as shipped in two commits without naming them, and the rest name none.

Decision 007 was accepted on 2026-08-23.
On the day this record was written, its gate had failed on zero real claims in review, so nothing yet shows whether the annotation-and-registry design holds up under use.

## Decision

The general ancestry rule is deferred, not rejected.
Non-description measurement claims stay under `scripts/check-citations.py` alone: the artifact must exist, and an attributed quote must appear in it verbatim.
Whether the artifact measured the version the claim says it did is not checked for them, and this record is the honest statement of that gap.

Two preconditions must hold before the rule is worth building, and neither did on 2026-08-24:

1. Decision 007's gate has caught at least one real unbound or mis-bound claim in review, so its annotation-and-registry design has earned the extension.
2. A run record has a structured place to state its subject commit, adopted for a reason beyond this rule, so the ancestry check reads a field rather than parsing prose.

### Reopening condition

Any one of these reopens the question, with the survey above as its baseline:

- A false non-description measurement claim is found the way #20 was: the citation resolves, the quote is accurate, and the claim is wrong.
- Precondition 1 holds and a run-record convention lands that satisfies precondition 2.
- A decision record needs to state its adopting commit for some other purpose, which settles the second of #22's questions on its own.

## Consequences

- No checker change and no new annotation grammar.
  007's annotation stays description-only; writing one on a non-description claim is an R1 violation, not an extension.
- Anyone writing a claim of the #20 shape about a non-description subject should name the subject commit inline, as the 2026-07-18 validation runs in `skills/hypothesis-driven-analysis/tests/scenarios.md` already do.
  That is a convention a reviewer can check by hand and the survey can count; it is not a gate, and this record does not pretend otherwise.
- The survey is a point measurement.
  Whoever reopens this should re-run the count rather than trust the numbers here.
