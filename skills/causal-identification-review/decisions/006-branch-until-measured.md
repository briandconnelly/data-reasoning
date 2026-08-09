# 006 — Development happens outside the shipped surface until measured

Status: accepted, 2026-08-08.

## Question

This skill is being built from scratch, with none of its agent-facing prose measured yet.
Where should that construction happen — directly on the shipped surface behind some kind of placeholder, or somewhere the shipped surface never sees until there is evidence to justify shipping?

## Positions

*Develop on main with a placeholder stub (rejected).*
The convenient path: land a minimal `SKILL.md` early with a stub or placeholder description, then fill it in as the design settles, so the skill directory exists on main throughout.

*Build complete on a feature branch, merge only after measurement selects a ship row (adopted).*
The skill is built out in full on `feat/causal-identification-review` — a complete `SKILL.md` with its real draft description from the start — and merges to main only once the plan's Phase 4 verdict table selects a ship row.
No stub, placeholder, or partial `SKILL.md` ever lands on main.

## What settled it

Two independent reasons converged on the same answer, not one.
First, mechanically: the repo's frontmatter validator requires every `SKILL.md`'s `description` field to be a non-empty string, so a placeholder-stub description would fail the check that already gates every commit touching a `SKILL.md` — the stub path was not actually available as a middle ground.
Second, on the merits: even a stub that somehow passed validation would put agent-facing wording on the shipped surface before any run had measured it, which the repo's Iron Law — measure before trusting a procedure's wording — forbids regardless of whether the wording is meant as final.
Either reason alone would have settled this; both applying together left no version of the stub path worth arguing for.

## Reopening condition

The frontmatter validator's contract changes to permit an empty or placeholder description, or the repo adopts a different pattern for staged rollout that does not require a skill to be fully built before any of its surface lands on main.
Neither is anticipated.

## Where the rule lives

`skills/causal-identification-review/SKILL.md` (to be written, branch-only until the plan's Phase 4 verdict) and `scripts/check-skill-frontmatter.py` for the mechanical gate.
