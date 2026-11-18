# Decision memo: expanding Assist to the rest of the company

**Recommendation: do not expand yet, and do not book any responder-hour savings.** The dashboard's drop in median time to close comes from a change in which incidents were counted, not from faster recovery. Within every severity tier, Assist incidents took longer and used more responder time. The strongest evidence of harm is on the hardest incidents.

## What the data shows

| Measure | Manual (Jun 1–7) | Assist (Jun 8–14) |
|---|---|---|
| Incidents | 210 | 210 |
| Median time to close | 7.27h | 5.44h (the dashboard headline) |
| Mean time to close (closed only) | 7.14h | 7.53h |
| Mean responder minutes per closed incident | 90.2 | 90.9 |
| Incidents with no closure record | 1 | 10 |
| Reopened within 72h | 0% | 4.5% of closed |

**1. The headline is a mix shift (Simpson's paradox).** The severity mix changed abruptly at cutover.

| Severity | Manual share | Assist share |
|---|---|---|
| sev1 | 13% | 7% |
| sev2 | 40% | 20% |
| sev3 | 47% | 73% |

The manual week was exactly 4 sev1, 12 sev2 and 14 sev3 incidents every day. In the Assist week it was about 1.3 sev1 and 6 sev2 a day. Total volume stayed at 15 per group per day, so total incident count did not change. A larger share of easy incidents pulls the median down. Within each severity, Assist is slower:

| Severity | Time to close, manual | Time to close, Assist | Responder minutes, manual | Responder minutes, Assist |
|---|---|---|---|---|
| sev1 | 17.9h | 28.2h | 240 | 312 |
| sev2 | 8.5h | 12.2h | 99 | 137 |
| sev3 | 2.9h | 5.1h | 39 | 65 |

The responders' complaint matches this. Holding severity mix fixed, Assist adds about 3.0h per incident (95% interval 2.9–3.2h) and about 32 responder minutes per incident (30–33). These intervals reflect sampling noise only. They do not cover the design problems below.

**2. The worst cases are missing from the Assist numbers.**
- 5 of 14 Assist sev1 incidents (36%) had no closure record after 8.5 to 15 days. No manual sev1 was left open.
- Those unclosed incidents are excluded from every Assist figure above, so the Assist numbers are flattering.
- All 9 sev1 incidents that did close under Assist were reopened within 72h.
- Those 9 also show about 0.4 handoffs, versus 5.9 under manual. That pattern suggests premature closure.

**3. The other fields do not support expansion either.**
- Handoffs are higher under Assist for sev2 (3.95 vs 3.01) and sev3 (1.52 vs 0.54).
- Staffing rose at cutover: 12→14 responders in identity and 11→13 in storage, with scheduled hours up about 20 a day.
- Interruption minutes were also higher in the Assist week. This is a second change made at the same time as the cutover.
- Staffing cannot explain Assist being slower. It does mean no speedup could be credited to Assist alone.

## Responder-hours attributable to Assist

**Credible savings: zero.**
- **Unadjusted:** responder minutes per incident are flat (+0.7 min, about +2.5 hours over 210 incidents), so there is no saving even before adjustment.
- **Severity-adjusted:** about +32 min per incident, roughly **+110 responder-hours of extra work** in the Assist week (closed incidents only).
- **Finance's likely headline:** a median-based saving of about 18 minutes per incident, or roughly 63 hours. That figure comes entirely from the severity-mix shift and should not be booked.
- **Missing records:** the 10 unclosed Assist incidents have no recorded minutes, so the +110 hours is probably an underestimate.

## What this data can and cannot establish

**It can establish:**
- The headline median drop is explained by mix, not speed.
- Assist-week incidents were slower and heavier within each severity.
- Sev1 closures under Assist are suspect.

**It cannot establish:**
- **Causation in either direction.** There is no holdout, only one pre-week, and staffing changed at the same moment as the workflow. "Every incident followed the workflow active when it opened" is true, but it does not make the comparison clean, because everything else also changed on June 8.
- **Why severity shifted.** Either Assist or intake changed how severity is assigned, or the incident mix genuinely changed. If Assist downgrades severity, then comparing within severity is itself biased, and I'd want to see the severity-assignment logic.
  - Even without adjusting for severity, Assist shows no gain in mean time to close, mean responder minutes, or closure completeness.
  - The conclusion "no demonstrated benefit" holds under both readings.
- **Whether the sev1 reopens and unclosed incidents are real recovery failures or recording artifacts.** The 11 missing activity rows need checking against the source system.
- **Anything after one week, or about service groups beyond identity and storage.**

## Before Monday

1. Check the 11 missing activity rows in the source system, especially the 5 sev1 incidents.
2. Find out who sets severity and whether Assist influences it.
3. Re-run any rollout with a holdout. Randomize incidents, or stagger a service group at a time. Compare within severity as assigned before the workflow acts.
4. Hold any savings booking until a rerun confirms a benefit.

I used only the three local exports. The scripts are in `/tmp/an/`. The analysis uses Python's standard library, because pandas was not available here.
