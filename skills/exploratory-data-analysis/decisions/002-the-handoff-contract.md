# 002 — What crosses the handoff, and who owns each half of it

Status: accepted, 2026-08-08.

## Context

`README.md` calls the two skills a pair, and the pairing runs on one mechanism: exploration produces a lead, and `hypothesis-driven-analysis` adjudicates it.
Nothing specifies what travels between them.
A cross-model design review on 2026-08-08 (Claude, Codex, and a third-model review of the resulting plan) found the seam carries no contract at all, and that the gaps are structural rather than stylistic:

- an EDA lead cites a *look* id (`L3`), while an HDA test's evidence cell must cite a *source* id, so evidence lineage does not survive the crossing;
- EDA's lead classes (`pattern`, `data-quality`, `descriptive`) are not HDA's claim classes (`causal`, `descriptive`, `data-artifact`);
- EDA precommits a confirmation reservation at Frame time, before any lead exists, and nothing ever checks that the reserved evidence can execute the confirming test a lead names;
- EDA's orientation record and its already-paid collection have no documented path into HDA's Plan;
- HDA's routing table was written for an ask arriving from a user, not for a lead arriving pre-formed.

None of this is measured behavior.
Every item above is a static fact about the two texts, verified by reading them; the behavioral claims that motivated an earlier draft of this record were withdrawn when re-reading dissolved them (see *Rejected*).
That distinction matters here more than usual, because `hypothesis-driven-analysis/tests/PROTOCOL.md` step 0 requires verifying a reported failure before designing a fix, and this record is the design phase for exactly that reason.

## Decision

### The contract has two halves with different owners

EDA owns **emission**: what a handoff packet contains.
HDA owns **intake**: what happens when a pre-formed hypothesis arrives.
These are scope-different statements, not two statements of one rule, so each skill states its own side and neither paraphrases the other — the same disposition `001-shared-gate-authority.md` already reached for the `retrospective` promotion condition and the co-loaded-skill-is-a-tool rule.

The split is forced by standalone installation.
A harness may load either skill without the other on disk, so HDA cannot point at an EDA file, and an intake rule written in terms of "an EDA packet" would be dead text in an HDA-only install.
**HDA's intake rule is therefore written for a hypothesis that arrives already shaped by someone's look at the data, whatever produced it** — a pasted lead, a colleague's hunch, a dashboard someone stared at, or an EDA packet.
That framing is strictly more general than the seam it was written for, costs nothing in an HDA-only install, and is the reason the packet must be self-describing rather than requiring EDA's vocabulary to interpret.

### There is no class-translation table, because none is needed

An earlier draft specified a mapping from EDA's lead classes to HDA's claim classes.
That was wrong: HDA's Plan already requires labelling every hypothesis with its claim class, and an imported lead is an ordinary input to that existing step.
A translation table would create a second home for a rule HDA already owns.

What follows instead:

1. EDA's `pattern`, `data-quality`, and `descriptive` are **search-provenance labels, not claim classes**, and the packet says so in those terms, so an intake never reads one as if it were an HDA claim class.
2. Claim class is assigned at intake, under HDA's existing rule and nowhere else.
3. A `descriptive` lead usually arrives without an estimand, because EDA does not require one and HDA does; naming it is intake work, not a defect in the packet.
4. The one case needing an explicit destination is a `data-quality` lead with no statable failure mechanism. HDA admits a `data-artifact` row only on a concrete failure mechanism, so a mechanism-less quality lead is **a Data Validity entry, not a hypothesis-table row**. Without this, such leads either get promoted as ritual entries or dropped silently.

### Incoming leads route on what they carry

EDA requires every reported lead to record its plausible-but-untested alternatives.
A lead therefore usually arrives *with named live rivals*, which is HDA's `full` condition, not its `mini` condition — `mini` requires that no rival explanation competes for the claim.
A lead that carries no such alternatives is one claim and routes `mini` on its own merits.

Several independent leads are several routings, each on its own row.
They are not one routing over a batch, and the fall-through sentence ("if nothing matches … answer it directly") is not reached by a batch of individually-routable claims.

### Orientation inheritance is grain-scoped, not a binary

An imported orientation record is evidence HDA may cite **at the grains it was validated at**, and no further.
HDA's coverage matrix already binds at the grain its own analysis uses, so a hypothesis that introduces a new grain, segment, or denominator owes its own matrix at that grain regardless of what was imported.
This mirrors EDA's own rule that a look changing the analytic population revalidates before its output can seed a lead.
"Inherit the orientation record" as a binary would license skipping exactly the check HDA's hardest-won rule exists to force.

### There is no shared budget envelope

HDA precommits its own effort budget at Problem time.
The packet reports EDA's spend as **context, not as an allowance**: what was already collected, at what grain and snapshot, and what metered spend was already paid.
That field exists to serve HDA's costly-collection rule — data already paid for is reused rather than re-bought — and for no other purpose.
An earlier draft of the plan described "one shared budget envelope" across the two skills; no rule in either skill defines or could enforce such a thing, and the phrase is withdrawn.

### Packet fields

Emission-side, owned by EDA and specified in `references/exploration-log-template.md`:
lead id and its search-provenance class; the associational statement; source ids with grain and snapshot, alongside the look ids; search context; noted-but-untested alternatives; the cheapest adequate confirming test; whether the confirmation reservation can execute that test; retrospective provenance; the orientation record and the grains it was validated at; and collection already paid for.

### Where each rule will live

- Packet contents, and the reservation-to-test adequacy statement: EDA `SKILL.md` and `references/exploration-log-template.md`.
- Intake of a pre-formed hypothesis, its routing, the mechanism-less quality-lead destination, and grain-scoped reuse of an imported orientation record: HDA `SKILL.md`, written generically per above.
- Nothing in this record is itself the operative statement of any of those rules; it records what was decided and where each rule goes.

## Rejected

**Amending HDA's `mini` row to carry a batch of leads.**
Proposed in the first plan draft and withdrawn.
It fails three ways: most handed-off leads carry named untested rivals and are `full`-shaped, so the amendment would route the seam's main traffic into a row that does not match it; `mini` has no retrospective label, no promotion bar, and no source-id requirement, so it is the one route lacking the safeguard the handoff depends on, and `compare_prereg.py` excludes the mini paragraph from its scope; and editing the row's condition supersedes S11 and S13, both measured 3/3 against the current table, plus S17 and arguably S12.
The additive alternative above owes no reruns of existing cells.

**A behavioral claim that agents fall through HDA's routing table on a batch of leads.**
Asserted in the first plan draft on a static reading, never observed in any arm.
Nothing in the routing section says a task routes exactly once, so N independent claim-only leads are plausibly N `mini` routings already.
Designing against an unverified behavioral premise is PROTOCOL.md's documented loss #3, and the fall-through risk is now a question for a canary arm rather than a premise for wording.

**Extracting the shared contract to one repo-level source both skills consume.**
Deferred again, as in `001-shared-gate-authority.md`.
It edits HDA, and the seam design it would encode has no measured runs behind it; extracting an unvalidated contract fixes its shape before anything has tested that the shape is right.
Revisit once the end-to-end seam fixture has run.

## Consequences

- Phase 3's HDA change shrinks to additive text: an intake rule, a routing sentence, the quality-lead destination, and grain-scoped reuse. Kept additive, it owes no reruns of existing cells, only new intake cells.
- HDA gains an intake rule broader than the seam that motivated it. That is deliberate, and it means the rule earns its body-text cost in an HDA-only install too — which matters, because HDA's body is under documented accrual pressure.
- The packet's usefulness now depends on EDA's reservation being adequate for the test a lead names, which nothing checked before. That check is new EDA prose and owes no arms today, because EDA has no measured arms to invalidate.
- This record lives in EDA's `decisions/`, so a maintainer working only in HDA will not see it. HDA's intake rule must therefore stand on its own without it — which the generic framing above already requires.
- The retrospective promotion bar is the load-bearing rule under all of this, and it is **unverified**: S5 is documented invalid and the debt is recorded in HDA's owed measurements. The end-to-end seam fixture is structurally the valid S5 the repo already owes — a lead is a signal unreachable from inventory and schema, and the reservation is the held-out slice to promote against. Building it once pays that debt and measures the seam.
