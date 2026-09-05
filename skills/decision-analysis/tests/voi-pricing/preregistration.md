# VoI price and bound correction

Registered 2026-09-04 before behavioral arms and production wording edits.
Ordering follows `skills/hypothesis-driven-analysis/tests/PROTOCOL.md`.

## Scope

The reported defect is directly present in the shipped VoI Value calculation sentence: it derives the price from the loss spread alone, including when a signal model exists but the price is missing.
These probes reach the VoI signal, calculation, cost, verdict, and associated Numeric Policy text and template.
They do not measure description activation, the decide route, sibling handoffs, live hooks, or collection authorization.
The existing DA-S5 and DA-S7 ask shapes are represented by the priced and unpriced cases; their original fixtures remain unrun.

## Packet and expected outcomes

`prompts.json` contains seven independent user requests with all available data in the prompt.
Each uses a descriptive binary state, two actions, elicited monetary losses, and no collection or causal inference.
This avoids unrelated identification, missing-preference, and collection gates.

| Cell | Expected arithmetic | Required distinction |
| --- | --- | --- |
| uninformative | Gross value 0; total-cost break-even 0 | No positive price from the loss spread |
| missing-price | Gross value 30; remaining fee threshold 25 after delay cost 5 | Missing fee does not erase a known signal model |
| missing-model | Perfect-information bound 50 | Fee 10 below the bound does not establish worth |
| missing-prior | Finite bound no larger than loss spread 100; a tighter justified bound is accepted | No invented prior or pull-specific price |
| priced | Gross value 30; net value -10 | Price compared with actual signal value |
| equality | Gross value 30; net value 0 | No strictly positive-value recommendation |
| missing-delay | Gross value 30; fee threshold 25 minus unknown delay cost | No unconditional numeric fee threshold |

Score each cell on arithmetic and distinction separately, quoting the archived answer when adjudicating ambiguity.
Old-wording arms are not required to use verdict tokens introduced by the correction.
New-wording arms must additionally produce records accepted by the schema checker.

## Run design

Use fresh agents with no inherited task history, the packet, and either the frozen old skill/template or final new skill/template.
Restrict reads to those inputs and writes to an isolated output directory; do not reveal this preregistration or expected outcomes.
Each arm processes the named cases separately; within-arm context is shared, so these are dependent smoke-test cells, not independent statistical replicates.
Run one old-wording and one new-wording canary; exclude both from scored validation.
The requested Claude design review could not run because its authenticated account reported a session limit; a same-model independent review is supplementary, and the cross-model review remains outstanding.
After design/wording review and mechanical checks, run one fresh old-wording and one fresh new-wording validation arm.
Archive dispatch prompts, input hashes, agent identifiers, returned answers, and generated records.
No claim about tool non-use, precommitment timing, cost savings, or population-level effectiveness is scored from final answers alone.

Amended before scored validation: the independent review identified the missing-delay case, added as a seventh cell after the six-cell old canary.
The new canary returned a harness usage-limit error, but its six records and answer file were recovered from its isolated output directory.
Its arithmetic and distinctions were correct, but all six records failed schema validation because their Value calculation label line was empty; several also annotated bare sentinels.
The next draft clarifies that presentation contract in the affected skill/template slots before another canary or scored validation.
Scored old/new validation was held until the final presentation fix; no canary result is promoted into validation evidence.
The second new-wording canary got all seven arithmetic/distinction cells right but again emitted multiline prose slots; the checker now reads continuation paragraphs for Signal model and Value calculation and accepts code-formatted provenance tokens.
Neighboring bullets and headings remain boundaries, with regression tests preventing borrowed values or provenance.
This is a presentation fix within the VoI schema; arithmetic remains outside the checker's scope.
Results are recorded in `../runs/2026-09-04-voi-pricing.md`.

## Decision table

| Outcome | Disposition |
| --- | --- |
| Reinspection disproves the claimed semantic defect before any edit | No wording change |
| Old wording produces all correct outcomes | Report no observed behavioral failure; a definition correction may still proceed on the mathematical counterexample |
| Canary shows an unrelated gate or ambiguous packet | Repair and re-register the packet before scored validation |
| New validation misses any arithmetic or distinction, or produces an invalid record | Revise and remeasure affected cells before marking the PR ready |
| New validation passes all cells | Ship as a scoped correction with smoke evidence, without a measured-lift claim |
