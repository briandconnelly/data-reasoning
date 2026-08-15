# Phase A, attempt 2 — SHIP on the gates, null on the effect, mechanism refuted

Governed by `2026-08-11-veto-fix-prereg.md` § Phase A.
Attempt 1 is void and recorded separately in `2026-08-11-phaseA-void.md`; this attempt repeats the same preregistered design under the same frozen texts, fixture, seed, and gates, with the instrument's usage-limit blind spot closed.

## The run

300 invocations, `claude-opus-5`, matched-pair interleaved at query level with alternating order, seed 20260811.
**300 valid, 0 void, 0 usage-limit refusals.**
Both description digests verified per row against the frozen files.

## Verdict: SHIP

| Gate | Checks | Outcome |
| --- | --- | --- |
| 1, instrument | baseline P0 = 0.9583 ≥ 0.8 | PASS |
| 2, no harm | treatment P0 = 0.9583 ≥ 0.8; treatment N1 = 0.0000 ≤ 0.2; ΔN1 = −0.0333 ≤ +0.10; treatment N2 = 0.0000 ≤ 0.2 | PASS |
| 3, ship | ΔP1 = +0.0333 ≥ 0 | PASS |

| Arm | baseline | treatment | Δ |
| --- | --- | --- | --- |
| P0 (8) | 0.9583 | 0.9583 | 0.0000 |
| P1 (20) | 0.4000 | 0.4333 | +0.0333 |
| N1 (10) | 0.0333 | 0.0000 | −0.0333 |
| N2 (6) | 0.0000 | 0.0000 | 0.0000 |
| F (6, never gated) | 0.1667 | 0.1111 | −0.0556 |

The swap ships. `SKILL.md`'s description now byte-matches `frozen-2026-08-11-treatment.txt`.

## What the ship verdict does and does not mean

**It is not evidence that the edit helps.** ΔP1 = +0.0333 with an exact paired sign-flip 95% interval of **[−0.0667, +0.1333]**, p = 0.78 — the interval comfortably includes zero. Per query, 4 improved, 14 were unchanged, and 2 worsened; the two that worsened moved −0.333 and −0.667, which is the same magnitude as the movers in the other direction. This is a null result.

The ship rule was preregistered as ΔP1 ≥ 0 with no harm, and the preregistration states plainly why: *"The sign rule at ΔP1 = 0 ships the swap on the conflict-removal argument alone; that is a policy choice recorded here."* The edit removes an internal contradiction in the description at zero character cost, and it measurably costs nothing. That is the entire case for it. Anyone reading this as "the fix worked" is reading it wrong.

## The preregistered mechanism prediction is refuted

The preregistration recorded one directional prediction: the four 0.33-tier queries — the overview / rundown / context / tell-me-about phrasings that issue #5 item 1 argues are suppressed by the activity-veto reading — should rise under the treatment.

**They did not move at all. Both descriptions scored 0.0000 on all four.**

Not one of the 24 invocations across those four queries triggered, under either wording. The hypothesis that the "prose summarizing" phrasing suppresses that specific tier predicts a lift there above all else, and the tier is inert to the change. Whatever keeps those queries from triggering, it is not the word order of the exclusion clause.

Issue #5's item 1 is therefore **half sustained and half refuted**: the internal contradiction it identified is real and is now fixed, but the mechanism it proposed for the 0.33 tier — the causal claim that made the fix look valuable — does not survive its own preregistered test.

## Drift against the historical numbers

The baseline arm here is the shipped text, which `decisions/003` measured at P1 = 0.517.
**Fresh, the same text measures 0.400** — a drop of 0.117 with no wording change between them.
The four mechanism queries are starker: 0.33 historically, 0.000 in both arms here.

This is the disclosure the preregistration asked for, and it is the reason the historical numbers were demoted to reference only rather than used as a comparison arm. A treatment-versus-history design would have read this 0.117 environmental drift as an effect of the edit.

## Disclosure, not gates

- **Order diagnostics.** By run: baseline 0.30 / 0.38 / 0.34, treatment 0.32 / 0.38 / 0.32 — no decay, unlike attempt 1. By which-arm-ran-first: when baseline led, baseline 0.36 and treatment 0.40; when treatment led, baseline 0.32 and treatment 0.28. Position within a pair is worth more attention than the description in this data, which is precisely why the design counterbalances it.
- **Tag breakdown** (Phase B tags; `boundary` and `temporality` have no comparable second cell and are reported only for completeness). By scope: `whole` moved +0.0909 (11 queries) while `facet` moved −0.0370 (9 queries). Both cells are small and neither was preregistered as a hypothesis; this is a lead for a future balanced design, not a finding.

## Bookkeeping

- Archive: `runs/artifacts/2026-08-11-phaseA/` — full 300-row `results.jsonl`, manifest, run log, and the analysis output. Transcripts (600 files, 7.5 MB) are not committed; every row names its transcript, and the archived results carry the per-row digests, endings, and timings.
- `frozen-description.txt` is untouched, per `README.md`.
- Phase D is now owed: the description changed, so the T13/T14 seam pair must be re-measured under the repaired wording.
