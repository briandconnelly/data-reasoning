# I3 on the current host, dev and PR 110

2026-11-25 UTC
Scorer: the dispatching Codex session (GPT-6).

All six runs used the ordinary I3 prompt with no skill named, the same fixture and integration harness, Claude Code 2.1.332, and `claude-sonnet-5-5`.
Each run staged a clean plugin build from its recorded revision.
I checked the observed route in each manifest and read the final answer for whether it gave a number as the flow’s effect.

| Revision | Loaded investigation | Then loaded causal identification review | Withheld a causal number and identified the concurrent promotion or pre-trend |
| --- | ---: | ---: | ---: |
| dev `807838a` | 3/3 | 2/3 | 3/3 |
| PR `746d10b` | 3/3 | 3/3 | 3/3 |

The second dev run named causal identification review as a possible follow-up but never invoked it.
The earlier ordinary-prompt failure on PR revision `0dbfdfb` remains in the [original record](2026-11-25-randomized-estimate-routing.md).
Neither revision reproduced that failure in this comparison.
Three runs per revision leave its cause and frequency unresolved.

A separate S9b run exercised the clarified bounds on the PR wording.
It reported the completed-sample range of −0.4 to +19.6 percentage points, distinguished sampling uncertainty, and withheld a verdict on the one-point threshold.
One explanation in the answer was too strong: a complete-case comparison can recover the arm rates under suitable within-arm missingness assumptions even if recording rates differ between arms.

[Prompts, commands, manifests, transcripts and answers](artifacts/2026-11-25-i3-current-host-comparison/)
