# 003 — Scope: bounds in, prospective design out

Status: accepted, 2026-08-08.

## Question

Two other candidates from the same review sit close enough to this skill's territory that the candidate analysis flagged both as unsettled: partial identification / bounds (Candidate 6), and prospective experiment design (Candidate 3).
Does either merge into this skill, and on what terms?

## Positions

*Candidate 6 as its own sibling skill (rejected).*
The candidate analysis left this open rather than deciding it: "whether it is its own skill or a route inside Candidate 2," noting only that bounds are usually reached once identification has already failed, which argues for one skill rather than two.
A sibling skill would have meant a fourth routing-surface entry doing work adjacent to, but disjoint from, this one.

*Candidate 3 merged in as a route of this skill (rejected).*
The candidate analysis also left this open: "Overlap with Candidate 2 is substantial — a randomized design is an identifying design... These may be one skill with two routes rather than two skills."
The plan settles this the other way: prospective mechanics (power, minimum detectable effect, sample-ratio-mismatch checks, sequential analysis, precommitment of an analysis before data lands) are excluded, kept as a distinct discipline this skill only names a design from, never designs.

*Settled: bounds absorbed as a route, prospective design excluded but nameable.*
The `bound` route is in scope and produces real numeric endpoints — computed under a precommitted assumption ledger — rather than only a plan for computing them (see 005 for why numberless bounds were rejected).
Prospective mechanics stay out entirely; the review may still name "a randomized experiment at unit U" as the identifying design without designing it, which keeps the seam open for a future skill to pick up.

## What settled it

For bounds: the candidate analysis's own case that bounds are the constructive form of an honest "cannot tell" — a range with a stated ledger, not a punt — argued for one skill over a sibling, and the Codex critique on numeric policy (see 005) supplied the missing piece that made "absorbed" actually mean something rather than being an unenforced router.
For prospective design: the textbook/discipline test again — designing a randomized experiment is execution mechanics belonging to a different discipline, while naming it as an admissible design is identification review's own business.

## Reopening condition

A prospective-design skill being built, at which point the naming output — "a randomized experiment at unit U" as an admissible design — becomes that skill's handoff seam.

## Where the rule lives

`skills/causal-identification-review/SKILL.md` § Non-Goals and § Routing (to be written; this record predates them).
