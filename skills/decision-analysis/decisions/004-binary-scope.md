# 004 — v1 scope: one binary proposition, two actions

Status: accepted, 2026-08-09.

## Question

What decision-state geometry does v1 support?

## Decision

One binary proposition and two actions (`../SKILL.md` § Routing states the scope; § Degraded Modes states the out-of-scope behavior).
The 2026-08-09 Codex design review settled it: odds-form arithmetic with a single crossover is only well-defined at this scope — beyond it, decision boundaries are regions and unconditional-LR products double-count evidence — so `tests/check_decision.py` rejects records outside the scope rather than approximating them.

## Reopening condition

A finite consequence-matrix extension with normalized joint probabilities, conditional evidence factors, and per-dimension crossovers — specified, checkable, and worth its test surface.
