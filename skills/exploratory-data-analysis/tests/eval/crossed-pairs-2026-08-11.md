# Crossed speech-act fixture — Phase C of the veto-fix wave

Companion to `crossed-pairs-2026-08-11.json`; the design, estimand, and decision rules are in `2026-08-11-veto-fix-prereg.md` § Phase C and are not restated here.
Authored and committed before any Phase A arm ran and before any Phase A result existed.

## What it is

Ten entity-facet bases over the invented public library system, each rendered in four speech acts — `profile`, `overview`, `rundown`, `tell-me-about` — for 40 queries.
Every query is synthetic; none is drawn from, paraphrased from, or modeled on any real user's traffic.

## Content parallelism

Within a base, the four renderings differ **only** by the speech-act frame.
Each is built as frame + one content phrase + period, where the content phrase is exactly the text following "Profile " in that base's profile rendering:

| Speech act | Frame |
| --- | --- |
| profile | `Profile {content}.` |
| overview | `Give me an overview of {content}.` |
| rundown | `Give me a rundown on {content}.` |
| tell-me-about | `Tell me about {content}.` |

The drafted fixture did not satisfy this: for facet bases the profile rendering was entity-first ("Profile the bookmobile route — missed-stop counts.") while the three generic renderings were facet-first ("Give me an overview of missed-stop counts for the bookmobile route.").
Because the preregistered contrast is exactly profile versus the generic acts, that word-order difference would have varied with the speech act and confounded the estimand.
All four renderings were rebuilt from the single content phrase before the fixture was committed, and the parallelism was verified mechanically for all ten bases.

## Standing properties, verified mechanically

- All 40 queries are snapshot-temporality: a regex over `evolv|grown|grew|chang|trend|over the (last|past)|since|increas|decreas|drop|rise|rose|fell|improv|declin` matches nothing.
- No query asserts a directional effect or a claim to check.
- No query duplicates a query in `entity-profiling-eval.json` or `holdout.json`.
- Scope: four whole-entity bases (1, 2, 7, 9), six entity-facet bases (3, 4, 5, 6, 8, 10).

## Entity reuse, disclosed

Three bases reuse an entity that appears in an existing fixture, each with a different facet:

- Base 4, Central Library's graphic novel collection — the graphic novel collection appears in `holdout.json` at system scope; this base narrows to one library and pins renewal counts.
- Base 5, the bookmobile route — appears in `entity-profiling-eval.json` P1 as facet-vague "usage"; this base pins missed-stop counts.
- Base 8, the interlibrary loan program — appears in P1 as facet-vague "activity"; this base pins request turnaround times.

Reuse is disclosed rather than removed: these entities carry known measurement history, and a per-base analysis can check whether reused-entity bases behave differently from new ones.
The remaining seven bases introduce entities absent from both fixtures.

## Limits

Ten bases authored by one agent over one invented domain, reviewed by the operator.
The precision this supports, and the confirmatory threshold it must clear, are stated once in the preregistration; nothing here widens either.
