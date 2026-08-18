# 006 — The four routing descriptions are frozen against unmeasured change

Status: accepted, 2026-08-18.

## Context

The frontmatter descriptions of all four skills are the routing layer: they alone decide which skill activates, and they all sit near the 1024-character ceiling.
Their measurement status is uneven, per `skills/hypothesis-driven-analysis/tests/scenarios.md` § "Owed measurements as of 2026-08-08": `hypothesis-driven-analysis`'s description was re-validated on 2026-08-08 with one trigger arm per scenario (S2, S3, S17, S18), with the n=1 caution left open; this skill's, `causal-identification-review`'s, and `decision-analysis`'s descriptions, and every cross-skill routing seam, rest on zero arms.
Decision 005 widened this skill's description ahead of any measurement, and the 2026-08-18 plugin review flagged the direction: every unmeasured widening spends ceiling budget that a measured confusion may later need, with nothing showing whether it routed a single additional ask correctly.
This record lives in this skill's decisions directory because cross-skill contracts already live here (001, the shared gate; 002, the handoff contract).

## Decision

The four `description` values are frozen at their 2026-08-18 baselines (which include `decision-analysis`'s same-day binary-scope correction).
`scripts/check-description-freeze.py` pins each against a golden in `scripts/frontmatter-descriptions/` via a prek hook.

Unfreezing a description requires, in one change: at least one measured trigger arm covering the edited description, run under `skills/hypothesis-driven-analysis/tests/PROTOCOL.md`'s ordering; the golden refreshed with `--update <skill>`; and a dated note here naming the measurement artifact.
For `hypothesis-driven-analysis` that batches with whatever reruns its own scenarios file states are owed for the change.
A correction of an outright factual error in a description (a wrong skill name, a broken value) may bypass the measurement requirement but still requires the golden refresh and a dated note here saying why the bypass was honest.

## Consequences

- Adding trigger surface to any skill now costs a measurement first — that is the point.
- The freeze does not measure anything itself; it only stops the unmeasured surface from growing while the owed measurements remain owed.
- The pin is a change detector: it makes an unmeasured edit loud and diff-visible, and this record governs the refresh; it cannot verify that the measurement happened.
