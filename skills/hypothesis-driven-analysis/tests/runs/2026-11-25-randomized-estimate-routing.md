# Randomized estimates and the regional-rollout control

2026-11-25 UTC
Scorer: the dispatching Codex session (GPT-6).

One Claude Code run per scenario at revision `0dbfdfb`, model `claude-sonnet-5-5`.
These are spot checks of the revised instructions, with no pre-edit comparison.
The three S9 runs used the skill-arm harness with the catalog prompts and staged fixtures.
I3 used the integration harness with the plugin installed.
After I3 failed, a separate diagnostic repeated it with an explicit instruction to load hypothesis-driven analysis.

| Case | Observed result |
| --- | --- |
| S9, daily aggregates | Estimated +0.63 percentage points, 95% interval +0.15 to +1.12. Recorded 28 of 28 variant-days and unknown export completeness. The answer assumed complete signup recording. |
| S9a, complete outcomes | Estimated +2.0 points, 95% interval −0.7 to +4.7. Recorded complete coverage and said neither a positive effect nor a gain of at least one point was established. |
| S9b, incomplete outcomes | Identified the 200 missing B outcomes, distinguished the observed +2.0 points from the assignment effect, and reported possible completed-sample contrasts of −0.4 to +19.6 before sampling uncertainty. Both sign and threshold remained unresolved. |
| I3, ordinary prompt | **Failed.** All four plugin skills were advertised, none was invoked, and the answer recommended roughly 37 seconds of causal improvement for the Q2 review despite the coincident promotion. |
| I3, explicit-load diagnostic | Loaded hypothesis-driven analysis and causal identification review, labelled the roughly 50-second change descriptive, and withheld a causal estimate because of the pre-trend and concurrent promotion. |

The explicit-load diagnostic tests behavior once the instructions are reached.
Automatic activation remains an open issue on I3.
These single observations do not estimate an activation rate or attribute the failure to this patch.

[Prompts, manifests, transcripts and working records](artifacts/2026-11-25-randomized-estimate-routing/)
