# Identification Review Record Template

This template records a review's content.
`../SKILL.md` governs what that content means.
Every closed-vocabulary slot below — route, disposition — names only the slot: which value applies, what values exist, and what each value means are `../SKILL.md`'s to state, not this template's.
Fill in one record per causal question under review; repeat the Design block once per candidate design the record considers.

```markdown
# Identification Review: <one-line causal question>

## Question

- Causal question, restated as a counterfactual contrast: <what would differ in the outcome, for which units, had the cause taken a different value, over what timeframe>
- Estimand: <the precise quantity the contrast above asks for>
- Assignment mechanism as stated: <verbatim quote from the source material naming how the cause was assigned, with its citation> — or `UNSTATED` if no source names one
- Route: <value> — value set and selection conditions per `../SKILL.md` § Routing (authority)

## Design: <design name>

- Design: <name of the candidate identifying design>
- Identifying assumptions:
  - <assumption 1, stated as a claim evidence could break>
  - <assumption 2, stated as a claim evidence could break>
- Assumption probes:

  | assumption | probe | result |
  | --- | --- | --- |
  | <assumption> | <the check run against it> | <what the probe found> |

- Data requirements: <the records, fields, and coverage this design needs to run>
- Threat register:

  | threat | probe | result |
  | --- | --- | --- |
  | <named threat to identification> | <the check run against it> | <what the probe found> |

- Disposition: <value> — value set and per-disposition semantics per `../SKILL.md` § Routing, per-route procedure (authority)

<!-- Repeat the Design block above once per candidate design; omit it entirely for a record whose route carries no design. -->

## Bound

<!-- Present this block only for a record whose route carries no Design block; see `../SKILL.md` § Routing (authority) for which route that is. -->

- Assumption ledger: <the licensed assumption(s), stated as facts of the data, written before any endpoint below>
- Bound logic: <how the licensed assumption(s) translate into the endpoint computation>
- Computed endpoints: <lower, upper> — per `../SKILL.md` § Non-Goals and this block's per-route procedure (authority) for what numeric scope is permitted; this slot records the resulting values only

## Handoff

- Facts: <what was established — probes run, their results, data-requirement and coverage findings, quoted rather than paraphrased where the source wording matters>
- Assumptions: <the identifying assumption(s) carried forward from the Design or Bound block(s) above, stated as conditions any downstream estimate would be conditional on>
- Dispositions: <the disposition value(s) assigned above, reused verbatim — or `none` for a record whose route assigns no disposition>

This block states facts, assumptions, and dispositions only.
It does not recommend or prescribe which route a receiving investigation takes; that choice is the receiving investigation's own routing rule to make.
```
