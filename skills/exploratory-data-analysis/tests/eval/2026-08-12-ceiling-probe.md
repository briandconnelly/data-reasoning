# Ceiling probe — can any wording claim generic speech acts?

**Interpretation rule written before the probe ran.**
This is an exploratory probe, not a preregistered measurement: no gates, no ship consequence, no verdict. It exists to tell issue #17 which kind of problem it is looking at before anyone spends effort on wording.

## The question

Phase C measured, with content held byte-identical, that the shipped description triggers 0.833 on `Profile X.` and 0.033–0.133 on the generic frames.
Issue #17 asks whether that gap is a property of *this wording* or of *generic asks* — whether the description under-claims, or whether a generic ask does not read as skill-worthy however the skill is described.

## Design

Same instrument, same detector, same presentation as Phase C — only the description text differs, so the arms stay comparable.

- **Arm A**: the shipped description (`frozen-2026-08-11-treatment.txt`, 1019 chars).
- **Arm B**: a deliberately over-claiming **ceiling** description (1009 chars) that names the generic frames explicitly and states that the phrasing does not matter. It keeps the adjudication exclusion and the bounded-descriptive exclusion.
- 16 queries: 4 bases from the Phase C fixture (2 whole, 2 facet) × 4 speech acts, taken verbatim.
- 2 runs per query per arm = 64 invocations.

The `profile` rendering is included as a within-probe control: it should reproduce roughly its Phase C rate under arm A, or the probe is not measuring what Phase C measured.

**Arm B is not a proposal and must never ship as written.** It is built to over-claim, and it is untested against N1, N2, and the seam — the exclusions it would most likely damage. Its only job is to establish a ceiling.

## What each outcome would mean

| Generic-frame rate under arm B | Reading |
| --- | --- |
| Rises to roughly the `profile` level | Wording **is** the lever. The shipped description under-claims, and issue #17 is a solvable wording problem — subject to whatever the over-claiming costs on N1/N2/seam, which this probe does not measure. |
| Stays near the arm A floor | Wording is **not** the lever. Even an explicit, unambiguous claim fails to recruit generic asks, so the blocker lies in how skills are selected rather than in this description, and issue #17 should pivot away from rewording. |
| Rises partway | Both matter. Wording buys something but does not close the gap; a wording fix alone would leave most of the population uncovered. |

## Limits, stated in advance

Four bases, two runs per cell, one invented domain, and a single hand-authored ceiling description. This can distinguish "large effect" from "no effect"; it cannot estimate how much of the gap a shippable wording would recover, and it says nothing about what over-claiming costs on the exclusion arms.

## Result

Appended after the probe ran; nothing below this line existed beforehand.
64 invocations, 64 valid, 0 void.

| Speech act | shipped | ceiling |
| --- | --- | --- |
| `Profile X.` | 0.500 | 0.875 |
| `Give me an overview of X.` | 0.125 | **1.000** |
| `Give me a rundown on X.` | 0.125 | **1.000** |
| `Tell me about X.` | 0.125 | **0.750** |
| **generic (3 acts pooled)** | **0.125** | **0.917** |

**Reading: wording is the lever.** The generic frames move from 0.125 to 0.917 — a lift of about 0.79 — under a description that claims them explicitly, with the queries, instrument, detector, and presentation all held fixed. Generic asks are recruitable; the shipped description simply does not recruit them.

Issue #17 is therefore a wording problem, and the pivot-away-from-rewording branch of the table above is closed.

### Control check

The `profile` rate under the shipped arm reads 0.500 here against Phase C's 0.833, which looks like a failed control until the comparison is made properly: Phase C's 0.833 averages ten bases, and these four sit below it. Restricted to the same four bases, Phase C's shipped arm gives **profile 0.583 and generic 0.028**, against the probe's 0.500 and 0.125.
The probe reproduces the shipped arm's behaviour on the queries it shares, so the ceiling arm's lift is not an artifact of a different measurement.

### What this does not establish

- **The ceiling description is a rewrite, not a single-variable edit.** It differs from the shipped text in many ways at once, so it shows *that* some wording recruits generic asks, not *which* change does it. A shippable edit is a separate design problem.
- **The cost is entirely unmeasured.** Arm B was never run against N1, N2, or the seam — the exclusion arms an over-claiming description is most likely to damage. It also lifted `profile` (0.500 → 0.875), which is the signature of a description that claims more of everything, and "more of everything" is exactly what the bounded-descriptive and adjudication boundaries exist to prevent. A follow-up that measures only the gain is measuring the easy half.
- Four bases, two runs per cell, one invented domain. This separates a large effect from no effect; it does not estimate how much of the gap a *shippable* wording would recover.
