# Decision memo: expanding Assist beyond the two pilot groups

## Recommendation
**Do not expand Assist yet, and do not book responder-hour savings in the rollout plan.** The data don't show that Assist caused faster recovery, and they point the other way. The credibly attributable saving is **0 responder-hours**. If the severity labels are taken at face value, the point estimate is a **cost of roughly 110 responder-hours** in the Assist week.

## Why the headline is misleading
The dashboard is arithmetically right. Median time to close fell from 436 to 326.5 minutes (−110), and the drop is stable under resampling. It comes from case mix, not from faster work.

| | Manual (Jun 1–7) | Assist (Jun 8–14) |
|---|---|---|
| Incidents | 210 | 210 |
| sev1 / sev2 / sev3 | 13% / 40% / 47% | 7% / 20% / 73% |

The mix is exactly 4/12/14 incidents per day in the manual week and exactly 2/6/22 per day in the Assist week, on all 14 days. Natural variation wouldn't be that regular. It looks like a rule-driven change at cutover, such as triage or severity labelling, not a shift in what arrived.

Sev3 incidents close fast, so a mix with more of them lowers the median regardless of the workflow. Within each severity, Assist is slower and costs more responder time:

| Severity | Median time to close (manual → Assist) | Mean responder minutes (manual → Assist) |
|---|---|---|
| sev1 | 1,100 → 1,659 min (+51%) | 240 → 312 |
| sev2 | 513 → 740 min (+44%) | 99 → 137 |
| sev3 | 167 → 302 min (+81%) | 39 → 65 |

This holds in both service groups and all three intake channels. The two weeks are flat internally, so there is no learning curve or pre-trend that would explain it.

## Responder-hours
- **Per incident, with no adjustment:** mean responder minutes are 90.2 under manual and 90.9 under Assist. That is no saving even before adjusting for mix. If Assist did relabel work as lower severity, the headline gain is only a labelling artefact.
- **Holding severity fixed:** at the manual mix, Assist costs +37 responder-minutes per incident (95% CI +35 to +39) and +233 minutes to close. At the Assist mix the figures are +32 and +182.
- **In hours:** applying the within-severity gaps to the 210 Assist incidents gives about **+111 responder-hours** in the week. That is 17 h on sev1, 27 h on sev2 and 67 h on sev3.
- **Undercount:** that figure leaves out the 10 Assist incidents that never closed and have no activity row. Priced at their severity averages they add at least ~34 hours.
- **Responders' complaint:** the data support it, but it isn't limited to difficult incidents. Sev3 got proportionally worse too.

I can't see Finance's calculation, so I can't say which step failed. Any conversion of the −110 minute headline into hours inherits the mix problem.

## Other fields, which agree with this
- **Unresolved incidents.** 10 of 210 Assist incidents have no close record 8.5 to 15 days after opening, against 1 of 210 under manual. Five are sev1, which is 5 of 14 Assist sev1 incidents. That means the Assist sev1 close times above are understated.
- **Reopens.** All 9 closed Assist sev1 incidents reopened within 72 hours, against 0 of 28 manual sev1. Across all severities it is 9 of 200 against 0 of 209.
- **Handoffs.** Sev1 handoffs fell from 5.9 to 0.4 while minutes rose and every incident reopened. Either handoffs aren't being logged or escalation isn't happening. That is a hypothesis to check, not something the data establish.
- **Staffing changed on the same day.**
  - Active responders rose from 12 to 14 in identity and from 11 to 13 in storage.
  - Scheduled hours rose about 18–20%.
  - Interruption minutes per day rose from 12 to 74 in identity and from 29 to 59 in storage.
  - Recorded incident hours as a share of scheduled hours fell from 24.5% to 19.9%.
  - Capacity went up, so no hours were released. Extra staff should have made close times faster, and they got slower.

## What the data can and cannot establish
**Can establish:**
- The headline median improvement is a composition effect.
- Within every severity, the Assist week was slower and used more responder time.
- Nothing in the data supports booking savings.
- The sev1 outcomes (unresolved incidents and reopens) are a concern.

**Cannot establish:**
- **Causation in either direction.** Assist, the staffing increase, the interruption increase and the severity shift all began at the same midnight. Without a holdout I can't separate them. The within-severity slowdown is large and uniform, but it is still a before/after comparison with one cutover, one week per arm and two groups. The service owners' "clean" claim only covers which workflow applied to each incident. It doesn't cover everything else that changed at cutover.
- **What produced the severity shift.** If Assist changed how incidents are classified, severity is itself an outcome. In that case the per-incident comparison (no saving) is the fairer one, and the stratified one is a sensitivity check.
- **Final outcomes for the unresolved incidents.** Responder minutes are only recorded for incidents with an activity row.
- **Whether the data are complete.** Responder minutes are as recorded in the export, and I haven't checked them against another source.

## Suggested next steps
1. **Today:** triage the 5 open Assist sev1 incidents (INC0211, INC0236, INC0273, INC0311, INC0404) and review the 9 reopened sev1 incidents. That is an operational risk whatever happens with the rollout.
2. **Before Monday:** ask what changed on June 8 in triage and severity rules, headcount and interruption sources. Ask Finance for their hours formula.
3. **If the pilot continues:** run a real comparison, such as a holdout or alternating assignment within each group. Fix severity at intake before assigning the workflow. Track close time and responder minutes by severity, plus reopens, unresolved incidents and handoff logging. Set the expansion criteria in advance.

I ran the analysis with Python's standard library, since pandas wasn't installed. The scripts are in `/private/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/an.uoli/`, and I can turn them into a tidy appendix if you want one.
