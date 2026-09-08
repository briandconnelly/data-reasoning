# 005 — Value of information is net expected improvement, not flip probability

Status: accepted, 2026-08-09.

## Question

The design draft priced a pull by the probability it flips the pending decision, and routed voi on the presence of a stated cost.

## Decision

Both rejected (2026-08-09 Codex design review); the operative definitions live in `../SKILL.md` § The VoI Route and § Routing.
What this record preserves is the two counterexamples that settled it: a rarely-flipping signal can be extremely valuable when it averts a catastrophic loss, and a frequently-flipping one worthless when consequences are nearly tied; and a cost-selected route would have contradicted every sibling skill's costly-collection rule.
What each counterexample requires operatively is stated only at the pointers above.

Extended 2026-09-04 after the project review found a second conflation: an unspecified price and an unspecified signal model both selected a loss-spread calculation.
An uninformative report has zero expected decision value despite nonzero losses, while a calibrated report can have a calculable fee threshold before a vendor states its price.
The corrected definitions and verdicts remain in `../SKILL.md` § The VoI Route; the template and checkers consume that authority.
The mathematical basis is the expected-utility comparison in [Duke's value-of-information lecture](https://www2.stat.duke.edu/~scs/Courses/Stat340/LectureSlides/Lec9_ValueInfo_Handouts.pdf) and the upper-bound interpretation of perfect information in [MIT's decision-analysis course](https://ocw.mit.edu/courses/ids-333-risk-and-decision-analysis-fall-2021/resources/unit-9-value-of-info-video-4/).
Focused validation is scoped in `../tests/voi-pricing/preregistration.md`; it does not settle the original suite's routing or premium measurements.

## Reopening condition

None foreseen; this is a definition correction, not a trade-off.
