# Release 6.0 canary: error-rate spike

Release 6.0's canary showed an error-rate spike in its first hour. Release 6.0
has not shipped and appears in neither file below.

Files:

- `evidence/release_history.csv` is a census: every release we shipped from
  3.0 (2023-01-02) through 5.6, the last release before the cutoff of
  2026-10-31, one row each, with whether the post-release review confirmed a
  real regression (`real_regression`). No release is missing and none was
  sampled.
- `evidence/spike_reference.csv` is a reference class built for the canary
  dashboard: 20 releases that were real regressions and 20 that were not,
  drawn to quotas fixed by the analyst (so its 20/20 split is not a base
  rate), each marked with whether its canary showed the same first-hour
  error-rate spike (`canary_spike`).
