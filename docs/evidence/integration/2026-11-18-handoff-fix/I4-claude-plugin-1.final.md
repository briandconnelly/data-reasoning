# Decision memo: Should Assist expand company-wide?

**Recommendation: no. Don't book any savings, and don't expand yet.** The data doesn't show that Assist made recovery faster. On a like-for-like basis it points the other way.

## 1. The headline is a mix effect

Median time to close did fall, from 436 to 326 minutes. But the incident mix changed at the cutover.

| | Manual (Jun 1–7) | Assist (Jun 8–14) |
|---|---|---|
| sev1 / sev2 / sev3 incidents | 28 / 84 / 98 | 14 / 42 / 154 |
| Share that is sev3 | 47% | 73% |

The change is exact. Both groups went from 4 / 12 / 14 per day to 2 / 6 / 22 per day on June 8. Total volume stayed at 15 per group per day. Sev3 incidents close fastest, so a shift toward sev3 lowers the overall median regardless of the workflow.

Within each severity, Assist is slower. These are medians for incidents with a close record:

| Severity | Manual TTC (min) | Assist TTC (min) | Assist − Manual (95% CI) | Responder min, manual → Assist |
|---|---|---|---|---|
| sev1 | 1,100 | 1,659 | +559 (464 to 715) | 240 → 312 |
| sev2 | 513 | 740 | +228 (182 to 256) | 99 → 137 |
| sev3 | 167 | 302 | +135 (116 to 150) | 39 → 65 |

- **No overlap:** In every severity, every closed Assist incident took longer than every manual one.
- **Adjusted effect:** After adjusting for severity, service group and intake channel, Assist closes about 1.66× slower. It also uses about 33 more responder-minutes per incident (CI 31 to 35).
- **Responder minutes overall:** Unadjusted, they are flat (90.2 vs 90.9 per incident). So even the raw data gives no responder-time saving.

The "extra work on hard incidents" claim from responders is borne out. The worst gap is on sev1.

## 2. Other fields point the same way

- **Missing closures:** 10 of 210 Assist incidents have no close record, against 1 of 210 manual. Seven are sev1 or sev2, and five are sev1 (5 of 14 Assist sev1). Each has been open at least 8.5 days at the extract. Every number above uses closed incidents only, so it flatters Assist.
- **Reopens:** All 9 closed Assist sev1 incidents were reopened within 72 hours. None of the 28 manual sev1 incidents were. Reopens elsewhere were zero in both arms.
- **Handoffs:** Assist sev1 incidents show about 0.4 handoffs against 5.9 under manual. Together with the reopens, that suggests sev1s are being closed without proper escalation. Sev2 and sev3 handoffs are higher under Assist (4.0 vs 3.0 and 1.5 vs 0.5).
- **Staffing changed at the same moment.** Active responders rose from 12 to 14 (identity) and from 11 to 13 (storage). Scheduled hours rose about 18%. Interruption minutes also rose sharply (identity 12 → 74 a day, storage 29 → 59). Assist is therefore not the only change at the cutover.

## 3. Responder-hours I can credibly attribute

**Zero saved.** The Finance figure is the median drop of about 110 minutes × 210 incidents, or roughly 383 hours (my reconstruction, since I haven't seen their number). It has three problems:

- It is built on the mix artifact.
- Elapsed time to close is not responder time.
- Raw responder minutes show no change.

My estimate of the opposite effect, holding severity mix at the Assist-week level:

- **+6,640 responder-minutes, about +110 hours,** over the Assist week (sampling CI roughly 105 to 116 hours).
- **A further 25–34 hours** if the 10 unclosed Assist incidents cost anything like their peers. They have no minutes recorded, so the true cost is probably higher still.
- **Net:** about 135–145 more hours.

Treat this as an upper bound on Assist's own effect, because staffing and interruptions moved at the same time.

## 4. What the data can and cannot establish

**It can establish:**
- The headline improvement is a composition artifact.
- At the same severity, closed Assist incidents were slower and cost more responder time.
- Sev1 handling under Assist looks worse on closure, reopens and handoffs.

**It cannot establish:**
- **Causation, in either direction.** There is one cutover, no holdout and no concurrent control. Staffing, interruptions and the severity mix all changed on June 8. A before-and-after comparison can't separate them from Assist. "Every incident followed the workflow active when it opened" fixes the assignment rule, not the confounding.
- **Why the severity mix shifted.** If the real incident mix changed, adjusting for severity is correct. If Assist's triage re-labels incidents, so that sev1s and sev2s are being downgraded to sev3, then severity is itself an Assist outcome. That would make Assist's slower sev3s even harder to explain. Whichever it is, the headline doesn't hold. This is the first thing to ask the service owners.
- **Whether the 11 missing records are open incidents or an extract gap.** Closure times in the file stop on June 15, which suggests they may be extract gaps. Either way, the missingness is lopsided toward Assist and high severity.
- **Generalization.** The sample is two service groups and one week each.

## 5. Next steps

1. Don't book the Finance savings.
2. Find out why the severity mix and the staffing changed on June 8, and why the 10 Assist incidents have no close record.
3. Audit the 9 reopened Assist sev1 incidents.
4. Before expanding, run a staggered or randomized rollout with a concurrent control. Randomize at the incident or group level, and leave staffing unchanged. Pre-specify severity-adjusted time to close, responder minutes and reopen rate as the outcomes.

Analysis scripts are in `/tmp/an/` (`a.py`, `b.py`, `c.py`). The analysis used pandas and statsmodels, run via `uv`.
