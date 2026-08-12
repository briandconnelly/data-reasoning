# 004 — Speech act, not the exclusion clause, governs entity-profiling triggering

Status: accepted, 2026-08-12.
Disposes of issue #5 in full.

## Context

Issue #5 raised three findings against the entity-profiling work in PR #4, plus an owed measurement.
A four-phase wave was preregistered in `tests/eval/2026-08-11-veto-fix-prereg.md` and run against them.
This record states what the wave settled; the phase documents hold the numbers and are not restated here.

## Decision

Three things follow from the wave, and the third supersedes the other two in importance.

### 1. The exclusion's object is restored, on a null result

PR #4's compression changed `for summarizing prose documents` into `prose summarizing`, converting a veto on an object into a veto on an activity while the same description positively claims a named entity "whose story is wanted".
The contradiction is real. It is fixed by the word-order swap `or prose summarizing` → `or summarizing prose`, which costs zero characters — both texts are 1019 — and leaves the character multiset identical.

Issue #5 proposed restoring `summarizing prose documents` and asserted it "costs 5 characters against a ceiling with 5 to spare". That is arithmetically wrong: the full restoration costs +14 and the shortest object-restoring form costs +10, either of which overruns 1024. The zero-cost swap is what makes the edit single-variable, which was the issue's own stated requirement.

The swap ships on Phase A's preregistered rule — non-negative ΔP1 with no harm to the control arms — and on nothing else.
**There is no measured evidence that it helps.** ΔP1 = +0.033, 95% interval [−0.067, +0.133]; Phase C's θ̄ = −0.033, interval [−0.133, +0.067]. Two nulls with opposite signs, bracketing zero.

### 2. The mechanism issue #5 proposed for the 0.33 tier is refuted

Item 1 argued that the activity-veto reading suppresses the overview / rundown / context / tell-me-about phrasings that dominate the 0.33 tier, and that removing the conflict should lift them.
Phase A preregistered exactly that prediction and it failed: those four queries scored **0.000 under both descriptions**, 0 of 24 invocations each.
The tier is inert to the change.

### 3. Speech act governs triggering, by one to two orders of magnitude

Phase C crossed 10 entity-facet bases against 4 speech acts with entity, facet, and content held byte-identical inside each base, varying only the frame.

| Speech act | trigger rate (baseline description) |
| --- | --- |
| `Profile X.` | 0.833 |
| `Give me an overview of X.` | 0.100 |
| `Tell me about X.` | 0.133 |
| `Give me a rundown on X.` | 0.033 |

The description's entity-profiling coverage is, in practice, keyed to the literal word *profile*. Every generic phrasing of the identical request sits near the floor.

This resolves what the other phases could not. The 0.33 tier is not a population held down by a clause's word order; it is the generic-speech-act population near its floor, and no edit confined to the exclusion clause could have lifted it. P1's ceiling near 0.4 has the same cause: the arm mixes one phrasing the description claims strongly with several it barely claims.

**Issue #5's item 3 is confirmed, and its instrument was the right one.** The original fixture varies entity, facet, verb, and time framing together; crossed pairs holding content constant were required to see this, and they saw it immediately.

## What the wave settled on the other threads

- **Item 2, the P1 taxonomy.** Not adopted as proposed. The three subclasses are not mutually exclusive, so orthogonal fields (`scope`, `temporality`, `boundary`) replaced them. Applied blind by two annotators with 20/20 agreement across 60 judgements, they show the split **cannot be measured on this arm**: `boundary` divides 19/1 and `temporality` 17/3, leaving two of three fields with no second cell. Only `scope` (11/9) is comparable. The tags are committed as documentation of the arm's composition, not as a comparison. Separately, both annotators — blind to the issue's argument and to the query's observed 1.00 rate — independently marked Westview's "has grown" as the arm's only `named-effect` query, which supports the issue's reading of it. It does not move arms on that basis; doing so after seeing both its rate and its label would be selection on the outcome.
- **The owed deployment check.** Discharged in its two-skill form, before and after the edit: T13 5/5 to `exploratory-data-analysis` and T14 5/5 to `hypothesis-driven-analysis` both times. No collision at screening precision. The four-skill check with real installation remains owed; `decisions/003`'s statement of that debt stands.
- **The statistical limits.** Respected throughout, and one bit harder than the issue anticipated: the unchanged shipped description measured P1 = 0.517 in `decisions/003` and 0.400 in Phase A, drift larger than any effect the wave was looking for. This is why the historical results are reference only and why every comparison ran both arms contemporaneously. The issue's own proposal — re-measure and compare against history — would have read that drift as an effect of the edit.

## Extended advice

For anyone relying on this skill to catch entity-profiling asks: it will catch "profile this account" and will usually miss "tell me about this account", "give me an overview of this account", and "give me a rundown on this account", even though the description names the last of those as an example phrasing. That is a measured property of the current wording, not a prediction.

Two cautions on the numbers above. The 0.833 and 0.100 are means over 10 authored bases in one invented domain at 3 runs per cell; they establish the ordering and the rough magnitude, not precise rates. And within a matched pair, which description ran *first* moved rates by as much as 0.1–0.2 in both Phase A and Phase C — position effects are the same size as many effects worth detecting here, which is why counterbalancing is load-bearing in any follow-up.

## Recorded limitation

The wave measured triggering only. No behavioural arm ran; `tests/fixtures/` still does not exist for this skill, and B10 remains authored and unrun. Nothing here says what the profile route produces once it activates.

## When to reopen

- If a follow-up widens the description to claim generic speech acts, this record's rates are the baseline it must beat, and the crossed-pair fixture is the instrument.
- If `hypothesis-driven-analysis`'s description changes so that it claims entity asks more strongly (the trigger `decisions/003` already names), the seam results here become stale.
- If any future run of `tests/eval/` reports arm means without archived transcripts, treat them as unverifiable: the instrument that produced the historical numbers cannot distinguish a non-trigger from a quota refusal, and Phase A attempt 1 showed that failure producing 179 silent false negatives in a run that looked entirely normal.
