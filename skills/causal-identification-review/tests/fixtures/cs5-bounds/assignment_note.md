# Assignment and outcome-missingness notes

## Assignment

Invitations to the concierge onboarding call were randomized: within each monthly enrollment wave, invited customers were drawn by lottery from that wave's at-risk cohort.
The randomization was implemented and logged by the platform team; nothing about a customer's history entered the draw.
Randomization settles who was invited, but it does not identify the program's effect as a point here, because the 30-day outcome is differentially missing across the two cohorts (see below).

## Monotonicity assumption

The only licensed assumption about the missing 30-day outcomes is monotonicity of attrition: invitation can only keep a customer observed longer, never shorten the observation window.
This direction is stated here as a fact of the fixture, not inferred from the data.

## Why some outcomes are missing

Some invited and some non-invited customers churned before their 30-day retention outcome could be observed.
A blank `retained_30d` value means the customer churned before the 30-day window closed, not that the event was unrecorded or the export is incomplete.
The missing-outcome rate differs between the two cohorts, so the observed difference in retention rates cannot be read as the program's effect.
