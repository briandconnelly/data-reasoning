# Phase B — orthogonal annotation of the P1 arm

Governed by `2026-08-11-veto-fix-prereg.md` § Phase B; its field definitions and the consistency-check framing live there and are not restated.
Raw labels are committed unreconciled at `f5b2ce8` in `annotations-a-2026-08-11.md` and `annotations-b-2026-08-11.md`; the joined tags are `tags-2026-08-11.json`.

## Agreement

Two fresh sessions of the same model labeled all 20 P1 queries from `annotation-packet-2026-08-11.md` alone, with the ID-to-index key withheld.

| Field | Agreement |
| --- | --- |
| scope | 20/20 |
| temporality | 20/20 |
| boundary | 20/20 |

Zero disagreements across 60 judgments, so reconciliation was vacuous and no reconciliation file exists.

**This is consistency evidence, not independent validation, and perfect agreement is the weakest possible version of it.** Both annotators are the same model reading the same definitions written by the same operator; they share whatever blind spots the definitions contain. Identical output is what correlated annotators produce when the definitions are unambiguous *or* when both are wrong in the same way, and this design cannot distinguish those. What it does establish is that the field definitions are applied reproducibly, which is the property the tags need to be usable at all.

Neither annotator invoked `frontier` on any query.

## The tags cannot support per-tag comparison on two of three fields

| Field | Cells | Usable for a per-tag P1 comparison? |
| --- | --- | --- |
| scope | whole 11, facet 9 | Yes — both cells large enough to report, though still small |
| temporality | snapshot 17, longitudinal 3 | No — a 3-query cell cannot separate signal from noise |
| boundary | clean 19, named-effect 1 | No — a single query is not a cell |

This is a finding about issue #5's item 2, not a defect in the annotation.
The proposal there was to split P1 into three subclasses and compare them; the existing arm was never constructed to balance these factors, so two of the three splits have nothing to compare.
The tags are still worth carrying — they document the arm's real composition and let a reader see *why* a per-tag claim is unavailable — but `analyze_ab.py --tags` output for `temporality` and `boundary` is disclosure only and must not be read as a comparison.
A follow-up that genuinely wants boundary or temporality effects must author queries that balance them, as Phase C does for speech act.

## What the annotation confirms about Westview

Issue #5 argued that "Give me the narrative on how the Westview branch's membership **has grown**" is not a clean entity-profile query, because it asserts a named directional effect and is therefore arguably closer to `hypothesis-driven-analysis` territory.

Both annotators, blind to that argument and to the query's observed 1.00 trigger rate, independently labeled it the **only** `named-effect` query in the arm, and one of only three `longitudinal` ones.
That is genuine support for the issue's reading, obtained without access to the outcome that motivated it.

It does **not** follow that the query should move arms. Its destination is a fixture-revision decision, deferred to Phase C authorship per the preregistration, and Phase C's bases were authored snapshot-only precisely so this factor does not ride along with the speech-act contrast.
Moving it now, after seeing both its rate and its label, would be selection on the outcome.

## Effect on Phase A

None. Tags are not gates, do not enter any arm mean, and were produced without access to any result.
