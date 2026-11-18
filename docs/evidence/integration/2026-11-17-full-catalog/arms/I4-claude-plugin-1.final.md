**Recommendation: don't expand on this evidence, and don't book any responder-hour savings.** The full memo is at `assist_decision_memo.md` in the working directory.

**Did Assist cause faster recovery? The data say no.**
- **The headline drop is a mix shift.** Median time to close fell from 436 to 330 min. On June 8 the daily severity mix per group went from 4 sev1 / 12 sev2 / 14 sev3 to 2 / 6 / 22. Sev3 incidents close fastest, and there were far more of them.
- **Within every severity Assist is slower.** Median minutes to close:

| Severity | Manual | Assist | Change |
|---|---|---|---|
| sev1 | 1,100 | 1,659 | +51% |
| sev2 | 512 | 740 | +44% |
| sev3 | 167 | 302 | +81% |

  - The sev1 Assist figure covers closed incidents only, so it understates the delay.
  - Adjusting for severity, service group and intake channel, Assist is about 1.7x slower.
  - The pattern holds in both groups and on every day of the Assist week.
- **Open incidents hide part of the delay.** 10 Assist incidents had no close record 8.5 to 15 days after opening, against 1 manual. Five of the 14 Assist sev1 incidents are among them, so closed-only metrics flatter Assist.

**Responder-hours we can credibly attribute to Assist: none saved, and probably a net cost.**
- **Raw responder minutes are flat.** Mean per incident is 90.2 for manual and 90.9 for Assist.
- **Holding severity fixed, Assist adds time.** About +33 min per incident, which over 210 incidents is roughly +110 to +130 responder-hours. This is a lower bound, since the 10 open incidents have no minutes recorded.
- **I couldn't reproduce Finance's number.** If it multiplies the median time-to-close gap by incident count (about 370 hours), it is wrong. Time to close is elapsed time rather than labor, and the gap is mix.

**The other fields back up the responders.**
- **Reopens:** all 9 closed Assist sev1 incidents were reopened within 72 hours, against 0 of 209 manual incidents.
- **Handoffs:** sev1 handoffs fell from 5.9 to 0.4 per incident.
- **Possible reading:** hard incidents may be closed too early or stall under Assist. That is a hypothesis; the data don't establish it.
- **Staffing:** it rose by 2 responders per group on the same day, which should have sped things up. So understaffing doesn't explain the slowdown.

**What the data can't establish:**
- **Why the severity mix changed.** Either Assist changed how severity gets assigned, or that week's incidents were genuinely lighter.
  - The simple version of the first story, where heavy incidents were relabeled sev3, doesn't fit. Assist sev3 times are tightly clustered with no long tail.
  - The "no savings" conclusion on raw responder minutes doesn't depend on which story is true.
- **A clean causal size.** The design is one week before and one week after, with no holdout. It can't be separated from the calendar week or the staffing change. Treat the +33 min as a consistent adjusted association, not a precise causal number.
- **Generalisation.** Only two groups and 28 sev1 incidents.

**Next steps, in the memo:**
1. Run a randomised or stepped test, with severity fixed before treatment.
2. Audit whether Assist influences severity assignment.
3. Review the 5 open and 9 reopened sev1 incidents with the responders.
4. Hold the rollout-plan savings line at zero until the test reports.

Scripts and intermediate files are in `/tmp/an`.
