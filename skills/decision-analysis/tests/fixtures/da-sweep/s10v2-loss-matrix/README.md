# Release 6.0 canary: error-rate spike

Release 6.0's canary showed an error-rate spike in its first hour. Release 6.0
has not shipped and appears in neither file below.

Files:

- `evidence/release_history.csv` is a census: every release we shipped from
  3.0 (2023-01-02) through 5.6, the last release before the cutoff of
  2026-10-31, one row each, with whether the post-release review confirmed a
  real regression (`real_regression`). No release is missing and none was
  sampled.
- `evidence/spike_reference.csv` is the canary-telemetry consortium's
  reference class, as counts: from its complete census of comparable
  first-hour canaries across member companies, 20,000 canaries of releases
  later confirmed as real regressions and 20,000 of releases confirmed as
  not, drawn to those fixed quotas (so its 20,000/20,000 split is not a base
  rate), each counted by whether it showed the same first-hour error-rate
  spike (`canary_spike`). The census holds millions of canaries, so a
  reference class this size is routine.
