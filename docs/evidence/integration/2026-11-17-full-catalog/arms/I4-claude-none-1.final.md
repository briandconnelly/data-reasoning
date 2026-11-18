# Decision memo: Assist expansion

**Recommendation: do not expand yet, and do not book any savings.** The data shows no responder-hour savings from Assist. The headline median drop comes from a change in severity mix. Within every severity level, Assist incidents closed more slowly and took more responder time. Expansion should wait for a proper holdout or staggered rollout.

## 1. Did Assist cause faster recovery?

The data does not support that. The dashboard's median is real, but it misleads.

| | Manual (Jun 1–7) | Assist (Jun 8–14) |
|---|---|---|
| Median time to close (closed incidents only) | 7.27 h | 5.44 h |
| Mean time to close (closed incidents only) | 7.14 h | 7.53 h |
| Mean responder minutes per incident | 90.2 | 90.9 |
| Severity mix (sev1 / sev2 / sev3) | 13% / 40% / 47% | 7% / 20% / 73% |

**Mix shift.** The Assist week had far more easy sev3 incidents and half as many sev1s. Daily sev1 volume dropped from exactly 4 to exactly 2 on every day from June 8. A pooled median rewards that shift even if the workflow does nothing.

**Within each severity, Assist is slower:**

| Severity | Median time to close, manual → Assist | Mean responder minutes, manual → Assist |
|---|---|---|
| sev1 | 18.3 h → 27.7 h | 240 → 312 |
| sev2 | 8.5 h → 12.3 h | 99 → 137 |
| sev3 | 2.8 h → 5.0 h | 39 → 65 |

Weighting both weeks to the manual severity mix, Assist averages **+3.9 h** to close (95% CI +3.6 to +4.1) and **+37 responder minutes** per incident (95% CI +35 to +39). The median on the same footing rises from 7.3 h to 10.8 h. These intervals reflect sampling noise only, not confounding.

**Unresolved incidents.** 10 Assist incidents and 1 manual incident had no closure recorded, even with at least 8 days elapsed. Five of the 14 Assist sev1s are still open, against 0 of 28 manual sev1s. Every dashboard figure above excludes them, so the Assist figures are flattering. Counting open incidents at their elapsed time, mean sev1 time to close under Assist is at least 125 h.

## 2. Credible responder-hours attributable to Assist

**Zero savings. The point estimate is a cost of about +100 responder-hours for the week.**

- Total recorded responder time is flat: 314 hours in the manual week and 303 in the Assist week. That is 200 closed Assist incidents against 209 manual.
- The Assist mix was easier, so the same incidents at manual per-severity rates would have taken about 201 hours. Assist used about 303, which is about +102 hours. The 10 open incidents would add more.
- Finance's translation of the median drop into hours is a mix artifact. It shouldn't go into the rollout plan.
- I have no cost basis for any positive savings figure.

## 3. Other fields point the same way

- **Reopens:** all 9 closed sev1 Assist incidents were reopened within 72 hours, against 0 of 28 manual sev1s. The 9 reopens come from 200 closed Assist incidents, and 0 of 209 manual incidents were reopened. Sev1 incidents may be closing prematurely, though the data can't confirm that.
- **Handoffs:** sev1 handoffs fell from 5.9 to 0.4, but sev2 rose from 3.0 to 4.0 and sev3 from 0.5 to 1.5. Assist adds coordination work on routine incidents, and sev1 incidents are handed off far less. This fits the responders' report of extra work on difficult incidents.
- **Staffing:** active responders rose from 12 to 14 (identity) and from 11 to 13 (storage) on June 8, the same day as cutover. Scheduled hours rose about 19%. Interruption minutes roughly tripled, from 21 to 67 per group-day. Capacity and interruption load changed at the same moment as the workflow.

## 4. What the data can and cannot establish

**Can establish:**
- The median improvement is a severity-mix effect.
- Assist shows no savings in responder time.
- Within-severity outcomes were worse, and there are open sev1s and reopens to explain.

**Cannot establish:**
- **Cause.** With one cutover, Assist is confounded with calendar week, the staffing increase and interruption load. This is a single week on one side and one on the other, with no holdout.
- **Whether Assist caused the severity mix shift.** If Assist or the cutover changed how incidents are triaged or labeled, the severity-matched comparison is biased. In that case the sev1 drop may be relabeling. The overall picture (flat responder time, higher mean time to close, open sev1s) still shows no benefit. Ask the service owners how severity is assigned and whether it changed on June 8.
- **Whether Assist is worse or just ineffective.** The slowdown could partly be the added responders or interruptions. The data can't separate them.
- **Longer-term or company-wide behavior.** Two service groups and 14 days is a small sample.

## 5. Next steps before Monday

1. Pull the 10 open Assist incidents and the 5 open sev1s, and ask why they remain open.
2. Review the reopened sev1s for premature closure.
3. Confirm whether severity assignment or triage changed on June 8.
4. If the workflow stays, run a staggered rollout or randomized holdout (by service group or by incident) with a pre-set closure and reopen definition. Report time to close including open incidents, per severity.

I worked from the local exports only. Pandas wasn't installed, so I used the Python standard library. The analysis scripts are in `/tmp/an/`.
