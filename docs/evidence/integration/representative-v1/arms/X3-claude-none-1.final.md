**Deploy Model B.** It's clearly better for the way you'll use it.

Your retention team will call the 500 highest-scored customers, which is the top 5% of a list like the 10,000-customer holdout. So I compared the models on how many actual churners each one puts in its top 500. The baseline churn rate in the holdout is 13.8% (1,377 of 10,000).

| | Model A | Model B |
|---|---|---|
| Churners in top 500 | 173 (34.6% precision) | 302 (60.4% precision) |
| Lift over the 13.8% baseline | about 2.5x | about 4.4x |
| AUC (overall ranking quality) | 0.687 | 0.817 |

- **Calls that reach a churner:** Model B finds about 129 more churners than Model A in the same 500 calls. I bootstrapped the holdout 1,000 times. The gap stayed between 98 and 152 churners in every case I checked at the 95% level, so it isn't noise.
- **Overall ranking:** Model B's AUC is also much higher, so it isn't winning only at the top of the list.

**Caveats:**
- This is one quarter of holdout data. If customer behavior shifts next quarter, both models could do worse. I'd still expect B to stay ahead.
- Precision measures who churns, not who is saved. If the retention call works better on some kinds of customers than others, the best list could differ. The file has no data on that.
- Tied scores are rare (253 for A, 515 for B). They don't change the result.
