# Investigation: did the connection-pool change regress checkout p95 on 2026-09-09?

## Problem

- Decision informed: whether the 2026-09-12 release, which carries the pool change, ships or holds.
- Falsifiable question: what explains the checkout p95 rising from ~410 ms to ~470 ms on the canary hosts on 2026-09-09 (ms, per request, all regions)?
- Success criteria: answered means one explanation accounts for the canary/control gap and survives a discriminating test.
- Stop condition: conclude when the remaining tests cannot run before the release decision, or when one hypothesis is refuted on its necessary prediction.
- Effort budget: 12 queries.

## Hypotheses

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | The new connection-pool configuration on the canary hosts regressed checkout p95 | canary p95 exceeds control p95 by more than 40 ms on the same traffic | canary and control p95 within noise of each other | the canary/control gap must exceed the 40 ms noise band | T1 | per-host p95 (S1) |
| H2 | data-artifact | The canary hosts' latency exporter changed its sampling on 2026-09-09, inflating measured p95 without any change in served latency | exporter config diff on canary hosts; raw access-log p95 flat | exporter config unchanged; raw access-log p95 also up | the raw access logs must not show the same gap | T2 | exporter config history, raw access logs (S3) |

## Sources

| id | Origin (file, query, system) | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | `evidence/host_p95.csv` — per-host p95 for 2026-09-09, canary and control arms | 2026-09-10 08:10Z | all 12 hosts, full day; the six canary hosts are the deploy tool's fixed rotation for this service, chosen before the change and independent of traffic or latency, and the control hosts served the same load-balanced traffic |
| S2 | `evidence/reference_class.csv` — 20 past canary rollouts, post-mortem status and whether the 40 ms gap appeared | 2026-09-10 08:20Z | every canary rollout since 2025-Q1 with a completed post-mortem |
| S3 | raw access logs for the canary hosts | not acquired — retained 7 days, restore request pending | none yet |

## Data Validity

- Collection method: S1 from the metrics pipeline's per-host p95 export; S2 from the incident tracker's post-mortem fields.
- Coverage matrix: S1 carries one row per host for 2026-09-09 — 6 canary, 6 control, none missing; S2 carries all 20 rollouts the tracker lists for the period.
- Coverage baseline: S1 host count checked against the deployment inventory (12 hosts); S2 count checked against the tracker's rollout list (20).
- Known instrument failures: the metrics pipeline's p95 is computed over 1-minute windows and hides sub-window spikes.
- Source completeness semantics: S1 — an absent host row would mean the exporter did not report, not that the host served nothing; none absent. S2 — a rollout without a post-mortem is not in the file by construction, so the reference class covers settled cases only. S3 — UNKNOWN; not acquired.
- Sensitivity checks performed: the 40 ms band is the largest canary/control gap seen on the five quiet days before 2026-09-09 (S1's pipeline, same hosts); a gap inside it would be NON_DISCRIMINATING.

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | canary/control p95 gap exceeds 40 ms | compare per-host p95 means across arms | CONSISTENT | S1: canary mean 468 ms, control mean 411 ms, gap 57 ms, every canary host above every control host |
| T2 | H2 | raw access-log p95 flat on canary hosts | recompute p95 from raw access logs | NOT_TESTED | S3 not acquired before the release decision; restore pending |
| T3 | H1 | in past rollouts, a gap over 40 ms is more common when a regression was real than when it was not | tabulate S2 by post-mortem status and gap | CONSISTENT | S2: 9 of 10 real regressions showed the gap; 2 of 10 non-regressions did — the table is reproducible from `evidence/reference_class.csv` |

## Amendments

- 2026-09-10: added T3 after T1 came back CONSISTENT, to put the observed gap in a reference class; it uses S2, which did not inform H1.

## Conclusion

- Answer: unresolved — the gap is real in the metrics pipeline, and the test that would separate a served-latency regression from an exporter artifact could not run.
- Best supported: H1, on T1 and T3; H2 is untested rather than weakened.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 and T3 CONSISTENT; T2, which could refute H2 and so isolate H1, did not run |
  | H2 | data-artifact | UNRESOLVED | T2 NOT_TESTED — raw logs not acquired |

- Limitations: the canary/control contrast is the only evidence of served latency and it comes from the same pipeline H2 questions; T3's reference class is 20 settled rollouts and says nothing about this rollout's base rate; no test discriminates H1 from H2 until S3 is restored.
