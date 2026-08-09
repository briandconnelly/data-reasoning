# cs3-rollout ground truth

Not part of the fixture directory handed to arms -- generated here so `validate_cs3.py` can check its own independent recomputation against a value fixed at generation time, per `skills/causal-identification-review/tests/scenarios.md` CS3.

## Planted pre-trend (computed from the generated data)

- West pre-period completion-time slope: -0.534174 s/day (falling).
- East pre-period completion-time slope: -0.021315 s/day (flat).

## Documented ground-truth disposition

Both designs the review can construct from this fixture end on `assumption-contradicted`:

- The West-only before/after design's implicit no-confounding-events assumption is falsified by the concurrent price promotion (`promotions.log`, and the `avg_order_value` shift in West with no matching shift in East).
- The West-vs-East difference-in-differences design's parallel-trends assumption is falsified by the planted differential pre-trend above.

No design in this fixture reaches `identified-if` or `unresolved`. Synthetic control is infeasible by construction: the fixture holds exactly two regions, so there is no donor pool.
