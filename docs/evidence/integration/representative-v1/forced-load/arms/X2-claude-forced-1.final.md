**No, don't use this model to set October–December staffing.** It would very likely miss the 10% bar by a wide margin.

**Why the 3.6% doesn't apply.** I reproduced it exactly. It comes from scoring on 20% of days chosen at random. Each of those days sits between training days. The model averages the 4 nearest same-weekday days, and in that test it could look at days on both sides. Your October–December forecast has no days after the cut-off. Its 4 nearest neighbours are all from late September, so it forecasts roughly September's level for every future month.

**Backtest that matches your use.** I re-ran the analyst's own code with origins at 16 month-ends from Mar-2025 to Jun-2026. At each origin I used only data up to that point, forecast the next 3 monthly totals and scored them against actuals.

| | Result |
|---|---|
| Average error of the 3 monthly totals, across the 16 origins | 19.1% |
| Range across origins | 3.6% to 33.3% |
| Origins within 10% | 2 of 16 |
| Sep-2025 origin (same time of year, forecasting Oct–Dec 2025) | 23.8% |

At the Sep-2025 origin the monthly errors were 14%, 25% and 33%, all too low.

**What it forecasts now.** The ticket data shows a strong seasonal cycle. Volume falls through the summer, then rises about 25–30% from September to December, in both years.

| 2026 month | Analyst model | Same month last year | Illustrative seasonal × 8.7% growth |
|---|---|---|---|
| Oct | 36,861 | 39,912 | 43,381 |
| Nov | 35,758 | 43,333 | 47,099 |
| Dec | 37,334 | 51,568 | 56,050 |

The 8.7% is year-over-year growth for Jul–Sep. The last column is a rough reference and I haven't validated it. Even so, the model's forecast is flat and sits well below last year's actuals. December would be off by about a third, which would leave you understaffed in the busiest month.

**Limits of this check.**
- There are only 24 months of data, so the 16 backtest origins overlap heavily. Treat 19% as the typical size of the miss, not a precise estimate.
- With one prior year, I could only test a seasonal alternative at a few origins, and I haven't done that formally.
- The missing seasonality shows up in the numbers, but I haven't tested other possible causes such as a growth trend or one-off events.

**Next step.** Ask the analyst to re-fit with a seasonal and trend component, such as last year's same month scaled by recent growth. Then score it with the rolling-origin backtest above, forecasting 1–3 months ahead and requiring the 10% bar to hold. The scripts are in `scripts/` (`bt.py`, `fc.py`, `cov.py`) if you want to reuse them. I didn't write a ledger file, since the estimation route doesn't need one.
