# Entity-profiling trigger eval

This fixture measures whether the skill's description triggers on entity-profiling asks — "tell me about this account's story" — as opposed to the dataset-flavored asks its description has always claimed.

Every query is synthetic.
The domain is an invented public library system, with three vendor-account queries in the N1 arm.
No query is drawn from, paraphrased from, or modeled on any real user's traffic.

Arms:

- `P1` — entity profiling. The target class. Expected to trigger.
- `P0` — positive control. Dataset-flavored asks the description already claims. Expected to trigger; proves the harness can surface a known positive.
- `N1` — `hypothesis-driven-analysis`-shaped. Minimal pairs with P1 on the same entities, differing only in whether a named effect is present. Expected not to trigger. Three entries use the tokens the description introduces, to test lexical attraction.
- `N2` — bounded descriptive. Expected not to trigger. Near-uninformative by construction and reported as a sanity row only.
- `F` — frontier. Shapes whose correct route is unsettled. Recorded, never scored.

Run it with `skill-creator`'s `scripts/run_eval.py`.
The procedure, the isolation requirements, and the preregistered gates are in the design record and in `decisions/003-entity-profiling-in-scope.md`.
