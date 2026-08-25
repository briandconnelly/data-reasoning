# 007 — Description-measurement claims are bound to registry evidence

Status: accepted, 2026-08-23.

## Context

Issue #20: a decision record claimed two run records were measured arms for the description decision 005 adopted, and every gate passed it.
The arms had parsed the descriptions at `4efdeec`, seven days before commit `4c72ca2` applied the adopted text; the citations resolved, the quotes were accurate, and the claim was false.
The gates answered "does this reference point at real content?" and none answered "does this content support this claim?".
This record lives here for the same reason 001, 002, and 006 do: it is a cross-skill contract, and this directory is where those live.

## Decision

A description-measurement claim — prose stating that a run record or run artifact measured a skill's frontmatter `description` — is bound to evidence, and `scripts/check-measurement-claims.py` enforces the binding as a prek gate.

### The annotation

The claim line ends with exactly one annotation, wrapped in backticks, with this grammar:

```
[measured: skill=<slug> state=current|historical evidence=<key>]
```

- `skill` is one of the four canonical slugs, always explicit, never inferred from where the claim lives.
- `state=current` asserts the evidence measured the description that ships today (the freeze golden of decision 006); `state=historical` asserts it measured an older text.
- `evidence` names an entry in `scripts/measured-descriptions.toml`.

### The registry

An entry records the artifact that attests the measurement, the skill, a `source` (`sha256:<hex>`, `file:<frozen description file>`, or `git:<commit>`), an `anchor` quote that must appear in the artifact's visible Markdown, and optionally `covers`, the other files of the same runs.
One entry attests one measured text: a contrast between two texts is two entries, and the claims about it are two lines.
Adding an entry carries a review duty: the person adding it confirms the anchor sentence actually attests the tuple.
The gate verifies identity and consistency from then on; it cannot judge the anchor's aptness, and this sentence is the honest statement of that limit.

### The rules the gate enforces

- R1 — every annotation parses, is placed at the end of its line, names a known skill, and cites an entry for that skill.
- R2 — every entry's artifact exists and visibly carries its anchor; an entry no claim cites is a violation.
- R3 — the entry's source resolves to description text; `current` requires its hash to equal the skill's golden, `historical` requires it to differ.
- R4 — a line that names a run record or run artifact beside "description" and a measurement verb must carry an annotation.
  This is best-effort detection of missing annotations, not semantic completeness: prose that names no artifact can still make an unchecked claim, so write measurement claims with the artifact named on the same line.
- R5 — one annotation per line, and every artifact the line mentions must be the cited entry's artifact or in its `covers`.
  A claim about two skills' descriptions, or about two texts, is two lines with two annotations.

Negative assertions ("never ran the shipped text") are out of the gate's scope and carry no annotation.

## Consequences

- The false claim this record descends from fails twice under the gate: unbound as written, and hash-mismatched if bound honestly.
- When decision 006 unfreezes a description and the golden refreshes, every `state=current` claim for that skill fails until re-stated.
  That is intended: a new shipped text invalidates currency claims about the old one.
- Frozen evidence is never edited to satisfy this gate; the registry and its anchors carry the binding instead.
- The checker, the hook, and this directory's README point here and do not restate these rules.
