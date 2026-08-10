# 002 — Authority map with hypothesis-driven-analysis

Status: accepted, 2026-08-08.

## Question

Given `hypothesis-driven-analysis` already routes causal questions and already has a rule for what happens when nothing identifies the effect, how do the two skills divide authority so they cannot end up holding incompatible identification verdicts?

## Positions

*New skill owns identification review, HDA is untouched ("no HDA edits in v1").*
This was the plan's original position, and it matches how the candidate analysis frames the seam: HDA's honest conclusion that nothing identifies the effect is correct and a dead end, and the new skill is "the constructive continuation" — given that nothing identifies the effect today, name the design that would.
On this framing the new skill only had to exist next to HDA, not inside it.

*Three measured HDA amendment sentences (adopted).*
The 2026-08-08 Codex cross-model critique checked the untouched-HDA position against HDA's actual text — its routing rule (`skills/hypothesis-driven-analysis/SKILL.md` § "A causal question routes on its design") and its conclusion rule (same file, § Conclusion, causal-wording bar) — and found it incompatible with leaving both sections as they stood.
Leaving those sections alone while adding a new skill that also renders identification verdicts meant the two skills could disagree about whether a design identifies an effect, and the "constructive continuation" the candidate analysis promised would have nowhere on the HDA side to be reached from.
The critique's finding reversed the plan's original position; the settled amendment is three specific sentences added to HDA's SKILL.md, covering routing, the conclusion stop-with-limits, and the causal-wording bar.

## What settled it

The Codex critique's textual check against HDA's own routing and conclusion rules, not a preference between the two positions — the untouched-HDA position was falsifiable against HDA's shipped text, and it was checked and found false.

## Reopening condition

If HDA's routing or conclusion-wording rules change independently of this seam in a way the three amendment sentences no longer track, or if Phase 4 measurement shows the seam is unreachable or the two skills still diverge on a verdict, this authority map is worth revisiting.

## Where the rule lives

The new skill's route conditions and disposition vocabulary: `skills/causal-identification-review/SKILL.md` § Routing (to be written; this record predates it).
The three amended sentences: `skills/hypothesis-driven-analysis/SKILL.md`, which keeps final routing and the causal-wording bar authority.
