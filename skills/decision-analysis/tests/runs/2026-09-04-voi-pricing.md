# VoI price and bound correction: focused checks

Scope and decision criteria: `../voi-pricing/preregistration.md`.
Raw records, answer files, offered input snapshots, SHA-256 hashes, and agent identifiers: `artifacts/2026-09-04-voi-pricing/manifest.json`.

## Results

One fresh old-wording arm and one fresh new-wording arm each answered seven cases after three canaries.
Each arm shared context across its cases; these are dependent smoke-test cells, not independent replications.
The old wording already produced correct arithmetic and distinctions in all seven validation cells, so this run demonstrates no behavioral lift.
The change proceeds as a definition and schema correction: the previously conflated deliverables now have distinct recorded bases and verdicts.

| Case | Old wording | New wording | New record schema |
| --- | --- | --- | --- |
| uninformative | Gross 0; no positive fee | Gross 0; no positive fee | Pass |
| missing-price | Gross 30; fee threshold 25 | Gross 30; fee threshold 25 | Pass |
| missing-model | Perfect-information bound 50; purchase unestablished | Perfect-information bound 50; upper-bound-only | Pass |
| missing-prior | Justified tighter bound 50; no invented prior | Loose loss-spread bound 100; no invented prior | Pass |
| priced | Gross 30; net -10 | Gross 30; net -10 | Pass |
| equality | Net 0; indifference | Net 0; not-worth-it under the nonpositive convention | Pass |
| missing-delay | Fee threshold 25 minus unknown delay | Fee threshold 25 minus unknown delay | Pass |

Arithmetic and distinction scores are 7/7 for both arms; the new schema passes 7/7.
For example, the new answer file says the missing-delay threshold is "$25-D", and the missing-model record distinguishes its 50 bound from the actual report's unknown value.
The expected 14 validation records and 19 canary records are all archived; answer summaries are additional files, not additional scored cells.
This evidence applies only to the archived input snapshots; the subsequent bound, provenance, and verdict amendments are listed as unmeasured in `../scenarios.md`.

## Canary findings

The old six-case canary got all arithmetic and distinctions right.
The first new six-case canary also got them right, but emitted empty label lines followed by calculation paragraphs and annotated bare sentinels; all six records failed the schema.
It returned a harness usage-limit error after writing its artifacts, which were recovered without editing.
The second new seven-case canary respected the sentinel clarification and the unknown-delay formula, but used continuation paragraphs and code-formatted provenance.
The checker now accepts those presentations in the two VoI prose slots, with regression tests ensuring adjacent fields cannot supply their content or provenance.
Neither canary is counted in the validation scores.

## Limits

The complete original DA scenario suite, description activation, sibling handoffs, live hooks, and token/cost premiums remain unmeasured.
No tool non-use or precommitment timing assertion is scored: complete tool-call transcripts are unavailable for these delegated arms.
The draft snapshot was reconstructed from the offered revision; evaluator-read hash attestation is unavailable.
Cross-model review availability and the independent same-model finding are recorded in `artifacts/2026-09-04-voi-pricing/reviews.md`.
