# cs5-bounds ground truth

Not part of the fixture directory handed to arms -- generated here so `validate_cs5.py` can check its own independent recomputation against a value fixed at generation time, per `skills/causal-identification-review/tests/scenarios.md` CS5.

## Lee (2009) trimming bounds (computed from the generated data)

- lower: -0.019370
- upper: 0.273608

Computed by trimming the invited cohort's observed `retained_30d` distribution (the lower-attrition cohort) down to the non-invited cohort's survival rate, from the bottom (lower endpoint) and from the top (upper endpoint), then subtracting the non-invited cohort's observed mean.
