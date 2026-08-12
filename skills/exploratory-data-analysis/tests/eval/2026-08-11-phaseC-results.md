# Phase C — the speech act dominates; the veto swap does not touch it

Governed by `2026-08-11-veto-fix-prereg.md` § Phase C.
The fixture, estimand, estimator, support levels, and reopen rule were frozen before any arm ran, and the analyzer (`analyze_phasec.py`) was committed before the data existed.

## The run

240 scored invocations over the 40-query crossed-pair fixture — 10 entity-facet bases × 4 speech acts × 2 descriptions × 3 runs — `claude-opus-5`, matched-pair interleaved, seed 20260812.
240 valid, 1 void.

The void is worth naming: the account hit its usage limit at ordinal 140, and the instrument recorded it as `void / usage_limit / triggered=null`, refused to retry it, and aborted the run. On resume it verified the skill name, the fixture digest, and both description digests against the prior manifest, charged the interrupted cell **0 of 3** executions because the model never ran, and continued. This is the failure that silently destroyed Phase A attempt 1 as 179 false negatives, caught and contained.

## Verdict on the preregistered estimand: NOT_SUPPORTED

θ̄ = **−0.0333** (exact −1/30), exact sign-flip 95% interval **[−0.1333, +0.0667]**, p = 1.00.
Per base: 1 narrowed, 7 unchanged, 2 widened.

**REOPEN condition (θ̄ < 0 *and* the interval excludes 0): False.** The interval includes zero, so the preregistered rule does not reopen the Phase A ship decision, and the shipped edit stands.

The treatment did not narrow the gap between the explicit `profile` speech act and generic phrasings. Combined with Phase A, the wording change has now failed both of its preregistered directional tests.

## The finding that matters: speech act, not wording, decides

With entity, facet, and content held byte-identical inside every base, and only the speech-act frame varying:

| Speech act | baseline | treatment |
| --- | --- | --- |
| `Profile X.` | **0.8333** | **0.8000** |
| `Give me an overview of X.` | 0.1000 | 0.0667 |
| `Give me a rundown on X.` | 0.0333 | 0.0000 |
| `Tell me about X.` | 0.1333 | 0.0000 |

The description triggers about **0.8** on the literal word *profile* and about **0.0–0.13** on every generic phrasing of the identical request.
That is a gap of roughly 0.70–0.83 — between one and two orders of magnitude larger than anything the veto swap moved in either phase (±0.03).

This is the single largest effect measured anywhere in this wave, and it is not about the clause under test at all.

**Issue #5's item 3 is confirmed, and its diagnosis was right for the right reason.** The original fixture varies entity, facet, verb, and time framing together, so speech-act effects could not be separated from anything else; crossed pairs holding content constant were exactly the instrument needed. What they show is that the description's coverage of entity profiling is, in practice, keyed to one word.

It also explains what the earlier phases could not. The 0.33 tier in PR #4 — rundown, context, overview, tell-me-about — is not a tier suppressed by a veto's word order. It is the generic-speech-act population, sitting near its floor, and no wording change confined to the exclusion clause was ever going to lift it. P1's ceiling near 0.4 has the same cause: the arm is a mixture of one phrasing the description claims strongly and several it barely claims at all.

## Disclosure that cuts against the shipped edit

The treatment is **at or below** the baseline on all four speech acts (−0.033, −0.033, −0.033, −0.133), and its overall marginal on this fixture is lower (0.217 versus 0.275).
The preregistered estimand is the *gap*, not the level, and its interval includes zero; the level difference here is neither preregistered nor significant on any test this document is entitled to run, and Phase A's P1 moved the other way (+0.033).
It is recorded because a report that discloses only the disclosures favourable to what shipped is not trustworthy. The honest summary is that two null results with opposite signs bracket zero, which is what "no measured effect" looks like.

## Other disclosure

- **Scope**: whole-entity bases θ̄ = 0.0000 (4 bases, none moved); facet bases θ̄ = −0.0556 (6 bases, 1 narrowed, 3 unchanged, 2 widened). Both cells are small and neither was preregistered.
- **Order**: when baseline ran first, rates were 0.233 / 0.133; when treatment ran first, 0.317 / 0.300. Position within a matched pair again moves the number more than the description does — the same pattern as Phase A, and the reason counterbalancing is load-bearing rather than cosmetic.

## Bookkeeping

Archive: `runs/artifacts/2026-08-11-phaseC/` — the 241-row `results.jsonl`, both manifests (original and resume), both run logs, and the analyzer's text and JSON output. Transcripts are not committed; every row names its own.
