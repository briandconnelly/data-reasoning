# Crossed speech-act fixture — 2026-08-15, confirmatory set for issue #17

Companion to `crossed-pairs-2026-08-15.json`; the design, gates, and decision rules are in `2026-08-15-widening-prereg.md` and are not restated here.
Authored and committed before any screening or confirmatory arm of the widening wave ran, and no per-base result for these queries exists anywhere before the confirmatory wave — that ordering is what qualifies it as the confirmatory instrument after the 2026-08-11 fixture's per-base results were published.

## What it is

Ten entity-facet bases over an invented municipal transit agency, each rendered in the same four speech acts as the 2026-08-11 fixture — `profile`, `overview`, `rundown`, `tell-me-about` — for 40 queries.
Every query is synthetic; none is drawn from, paraphrased from, or modeled on any real user's traffic.
The domain is new: no entity here appears in the public library fixtures or in any earlier run.

## Content parallelism

Queries are constructed mechanically as frame + content phrase + period by `make_fixtures_2026_08_15.py`, so parallelism within a base holds by construction, and the same script re-verifies it, snapshot temporality, and cross-fixture uniqueness (`make_fixtures_2026_08_15.py --verify-only <file>`).
Scope composition mirrors the 2026-08-11 fixture exactly: whole-entity bases 1, 2, 7, 9; entity-facet bases 3, 4, 5, 6, 8, 10.

## Cost-arm companion

`cost-arms-2026-08-15.json` holds the 16 N1/N2 entries of `entity-profiling-eval.json`, copied verbatim, so the confirmatory wave can run the exclusion arms under the same instrument without dragging P0/P1/F along.
The arm definitions and expectations are `entity-profiling-eval.json`'s; that file stays the authority.

## Limits

Ten bases authored by one agent over one invented domain.
The precision this supports and the thresholds it must clear are stated once, in the preregistration; nothing here widens either.
After the confirmatory wave this fixture is frozen under the same no-refresh discipline as the 2026-08-11 fixtures.
