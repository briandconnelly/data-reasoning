# 004 — Dispositions are evidence-bounded, never certifications

Status: accepted, 2026-08-08.

## Question

What vocabulary should the skill use to report a per-design review outcome, and should any value in that vocabulary function as an unconditional certification a downstream reader could cite as settled?

## Positions

*A weaker, paperwork-shaped disposition set (rejected).*
An early draft used a two-value set distinguishing only whether the assumption review had been done from whether the design could not be built at all.
The 2026-08-08 Codex cross-model critique found this too weak for any consumer of the review: it reported that the paperwork had been completed, not what the review had concluded, which left a downstream reader — including HDA's own routing — nothing to act on.

*An unconditional verdict value such as `valid` or `certified` (rejected).*
Considered and rejected outright as part of the same critique: an unconditional disposition would turn the review into an authority agents cite instead of a discipline they run, which contradicts the whole premise that identification review is something redone against evidence, not stamped once and trusted forever.

*A closed, evidence-bounded disposition set (adopted).*
Every per-design outcome is drawn from a small closed vocabulary, each value conditional on the assumptions actually named and the probes actually run against them — never an unconditional pass.

## What settled it

The Codex critique's finding that the draft's two-value set reported process completion rather than review result, combined with the independent argument that any unconditional verdict value defeats the discipline's purpose regardless of how many values surround it.

## Reopening condition

If a scenario in the skill's own test catalog (in particular the handoff scenario, where a downstream consumer has to act on a disposition) shows the closed set still under- or over-determines what a consumer needs, or if measured runs show some value in the set is never assigned in practice, the disposition vocabulary is worth revisiting.

## Where the rule lives

`skills/causal-identification-review/SKILL.md` § Routing and its per-route procedure, and the record template it governs (to be written; this record predates them).
