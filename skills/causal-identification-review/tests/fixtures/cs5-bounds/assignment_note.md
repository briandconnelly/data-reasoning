# Assignment and outcome-missingness notes

## Assignment

Invitation to the concierge onboarding call was targeted by an internal risk score.
That risk score was never exported and does not appear anywhere in this fixture.
Nothing here supports a claim about who would have been invited under any other targeting rule, so no comparison group's assignment can be treated as independent of the outcome.

## Monotonicity assumption

The only licensed assumption about the missing 30-day outcomes is monotonicity of attrition: invitation can only keep a customer observed longer, never shorten the observation window.
This direction is stated here as a fact of the fixture, not inferred from the data.

## Why some outcomes are missing

Some invited and some non-invited customers churned before their 30-day retention outcome could be observed.
A blank `retained_30d` value means the customer churned before the 30-day window closed, not that the event was unrecorded or the export is incomplete.
The missing-outcome rate differs between the two cohorts.
