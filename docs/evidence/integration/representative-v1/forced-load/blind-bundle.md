### G01 (cell X2)

**No, not as built.** If you staff from this model, expect October to December to come in about 15–35% under actual volume.

**Why the 3.6% doesn't apply to your use**
- The analyst held out 20% of days at random. Each held-out day sits between training days, and the model averages the 4 nearest same-weekday days, so it is mostly interpolating from neighbors a week or two away.
- Forecasting October to December is different. Every nearest same-weekday day is in late September, so the forecast comes out flat at September's level. The model has no seasonality or trend.
- Volume is strongly seasonal. Monthly totals run from about 28k in summer to about 52k in December and January.

**What the model forecasts now**

| Month | Model forecast | Same month last year |
|---|---|---|
| Oct | ~36.9k | 39.9k |
| Nov | ~35.8k | 43.3k |
| Dec | ~37.3k | 51.6k |

Volume is up about 8–9% year over year (July to September 2026 against 2025). Last year's pattern scaled by that growth implies roughly 43k, 47k and 56k. The model would leave you understaffed by about 15%, 24% and 33%. That is far outside your 10% tolerance.

**Backtest with the model's own code**
I fit it on data through each quarter-end and compared monthly totals for the next three months with actuals:

| Forecast origin | Months forecast | Avg abs error of monthly totals |
|---|---|---|
| Sep 2025 | Oct–Dec 2025 | 23.8% (-14%, -25%, -33%) |
| Dec 2025 | Jan–Mar 2026 | 3.6% |
| Mar 2026 | Apr–Jun 2026 | 33.3% |
| Jun 2026 | Jul–Sep 2026 | 7.1% |

Only one of the four windows meets your 10% bar, and that one is a quiet stretch. The Sep 2025 origin had only a year of history, but the failure doesn't depend on that, since the model ignores seasonality either way.

**Recommendation**
- Don't use this model for the October to December staffing.
- A seasonal-naive forecast (same month last year × the recent year-over-year growth) is a sensible baseline and a better interim planning number than the model.
- I haven't backtested it, and with only two years of data the growth factor is uncertain. I'd test it the same way before relying on it.
- Any replacement should be evaluated by forecasting forward from a cutoff date and scoring monthly totals, not by random holdout.

I can build and backtest the seasonal baseline if you'd like.

### G02 (cell X3)

**Deploy Model B.**

Your retention team will call the top 500 customers on one list, so I compared the models on that cutoff. I took the 500 highest scores from each model on the 10,000 holdout customers (13.8% churned overall).

| | Model A | Model B |
|---|---|---|
| Churners in top 500 | 173 (34.6%) | 302 (60.4%) |
| Overall AUC | 0.687 | 0.817 |

- **Size of the gap:** Model B reaches about 129 more churners with the same 500 calls. The two top-500 lists share only 117 customers.
- **Reliability:** I resampled the holdout 500 times to test this. Model B came out ahead in every resample, by roughly 98 to 153 churners (95% interval).
- **Data quality:** The file has 10,000 unique customers with no missing values.

- **Single quarter:** This is one quarter of holdout data. If customer behavior shifts, the gap could narrow, so track the top-500 hit rate after deployment.
- **Past churn only:** The holdout shows who churned. It doesn't show who would have stayed because of a call, so it can't tell you which model's list is better for retention.

### G03 (cell X3)

**Deploy Model B.** It finds far more actual churners in the top 500 than Model A, and the gap is much larger than sampling noise.

I ranked all 10,000 holdout customers by each model's score and counted how many of the top 500 actually churned. The overall churn rate is 13.8% (1,377 churners), so a random list of 500 would catch about 69.

| | Churners in top 500 | Precision@500 | AUC |
|---|---|---|---|
| Model A | 173 | 34.6% | 0.687 |
| Model B | 302 | 60.4% | 0.817 |

- **The gap is large:** B finds 129 more churners than A in the top 500. Bootstrapping the holdout customers 1,000 times gives a 95% interval of +99 to +153 churners for B over A. The interval is nowhere near zero.
- **It holds across list sizes:** B also leads at the top 100 (81 vs 48), 250 (179 vs 99), 1,000 (505 vs 305) and 2,000 (783 vs 533).
- **AUC agrees:** B leads by 0.115 to 0.144 at 95%, so the ranking is better overall and not only at the top.

Data checks: there are no missing values or duplicate customer IDs. Scores are nearly all distinct (9,747 unique values for A, 9,485 for B), so ties at the cutoff of 500 don't affect the result.

**Limits**
- **Single holdout:** This is one quarter's holdout. The bootstrap covers sampling noise but not drift between this quarter and next, such as seasonality or a change in who the customers are. The size of the gap makes a reversal unlikely, but I can't test it from this file. Re-check precision@500 after the first quarter in production.
- **Scope of the comparison:** B is better at finding customers who would churn. Whether calling them reduces churn, or whether A's list would respond better to a call, is a causal question this data can't answer. It only supports the choice of model, not an estimate of the retention team's impact.
- **Scoring pipeline:** I assumed next quarter's scores are produced the same way as these. If B depends on features that are only available in some cases, check that first.

The scripts are in `[path]

### G04 (cell X3)

**Deploy Model B.**

I scored both models on the 10,000 holdout customers (13.8% churned). I measured them the way you'll use them, as the 500 highest-scored customers on one list.

| | Model A | Model B |
|---|---|---|
| Churners in the top 500 | 173 (34.6%) | 302 (60.4%) |
| Overall AUC | 0.687 | 0.817 |

- **Size of the gap:** B finds about 129 more churners than A in a 500-call list. A bootstrap over customers puts that gap at roughly 100 to 150, so B is better in essentially every resample.
- **Agreement:** The two top-500 lists share only 117 customers, so the choice changes who gets called.
- **Baseline:** Calling 500 customers at random would reach about 69 churners, so A is better than random but B is much better.
- **Data checks:** There were no duplicate customer IDs. No scores were tied at the top-500 cutoff, so the list is well defined.

This is one quarter of holdout data, so I can't say how stable B's lead is over time. With a gap this large, I wouldn't expect the ranking of the two models to flip.

### G05 (cell X3)

**Deploy Model B.** Its top 500 holds about 74% more actual churners than Model A's.

The metric is the number of real churners among each model's 500 highest-scored customers. That matches how the retention team will use it.

On last quarter's 10,000 holdout customers (1,377 churned, a 13.8% base rate):

| | Model A | Model B |
|---|---|---|
| Churners in top 500 (precision 34.6% vs 60.4%) | 173 | 302 |
| Churners in top 100 | 48 | 81 |
| Churners in top 1,000 | 305 | 505 |
| AUC | 0.687 | 0.817 |
| Accuracy at 0.5 cutoff | 84.6% | 79.5% |

- **Size of the gap:** B finds 129 more churners than A in the top 500. A paired bootstrap over customers (1,000 resamples, 95% interval) puts that gap at +99 to +153. The whole interval is far above zero, so this is not sampling noise. The same ordering holds at every list size I checked, from 100 to 2,000.
- **Why the accuracy numbers point the wrong way:** the team's current report ranks A higher, at 84.6% against 79.5% accuracy. That metric doesn't fit this decision, for two reasons:
  - The 0.5 cutoff doesn't match the 500-call list. A flags only 533 customers at 0.5, while B flags 2,394.
  - With 86% non-churners, accuracy mostly rewards a model for staying quiet.
  - The 500-call list depends only on ranking, and B ranks better.
- **Data checks:** there are no missing values or duplicate customers. Neither model has tied scores at the 500th-place cutoff, so the top-500 lists are unambiguous.

**Limits:**
- The 302 and 173 figures come from last quarter's customers. Next quarter's absolute numbers will shift if churn rates or the customer mix change. The size of B's lead is the reliable part. I can't test whether it holds under drift with this file.
- I didn't test whether the 129 extra churners are saveable. Calling a customer who would have churned anyway, or who can't be retained, wouldn't help. That needs a retention-outcome measurement, and it applies equally to either model.
- `models.md` says both models were trained on the same data. I couldn't check that, and I assumed the holdout customers weren't in the training data.

### G06 (cell X2)

**No, don't use it for the October–December totals.** The 3.6% figure is real, but it doesn't measure what you need.

**Why the 3.6% doesn't apply**
- I reproduced it exactly. The analyst held out random days, so each test day sat between training days a week or two on either side. That tests interpolation inside the data.
- Staffing needs the model to forecast 1–3 months past the last data point. The model has no seasonality or trend term. It averages the four nearest same-weekday values, so for future days it just repeats the last four weeks of September.
- Volume is strongly seasonal. Each year it bottoms out in June–July (about 28–30k a month), then climbs to a peak of about 48–52k in December–January. September 2026 was 35.8k.

**Backtest of your use case**
I forecast the three months after a cutoff date using only data up to that date. Errors are on monthly totals.

| Forecast origin | Mean abs error of the 3 monthly totals | Detail |
|---|---|---|
| 2025-09-30 (same season as now) | **23.8%** | −14%, −25%, −33%, all under |
| 2026-03-31 (spring decline) | **33.3%** | +14%, +34%, +52%, all over |
| 2025-06-30 | 6.9% | Flat season, but September was −16% |
| 2025-12-31 | 3.6% | Flat season |
| 2026-06-30 | 7.1% | Flat season, but September was −16% |

- The model only does well when the next three months look like the last month. It misses at each seasonal turn, and October–December is one of those turns.
- The same-season case (origin 2025-09-30) fails the 10% bar by a wide margin.
- These backtests are few and overlap. With two years of data I have five origins, and none has a full prior year behind it. They show the pattern but don't give a precise error rate.

**What it forecasts for Q4 2026**
- It predicts Oct 36.9k, Nov 35.8k, Dec 37.3k.
- As a rough comparison, last year's Oct–Dec scaled by this year's Jan–Sep growth (+9.3%) gives about 43.6k, 47.4k and 56.4k.
- That comparison is a sanity check, not a validated forecast. Even so, the model would under-staff by roughly 15%, 25% and 34%. That matches the backtest and would hit December hardest.

**What I'd do instead**
- Use a model with seasonality and growth. Examples are last year's same-month volume times YoY growth, or a regression or Prophet-style model with annual seasonality.
- Validate it with a rolling-origin backtest at the same 1–3 month horizon, not random holdout.
- With only two years of history, set staffing for December with a wide range rather than a single number.

My scratch scripts are in `[path] (`bt.py`, `fc.py`). They read the analyst's `analyst_model.py` and don't modify anything in `data`.

### G07 (cell X2)

**No, don't use the analyst's model for the October–December forecast. A simple seasonal alternative looks usable, but its evidence is thin.**

**Why the 3.6% doesn't apply**

The analyst held out random days. Every test day had training days on both sides of it, so the model only had to fill gaps. I reproduced their 3.6% exactly. Your use is a forecast three months past the last data point. The model has no seasonality or trend. It predicts each day as the average of the last four same-weekday values, so it carries September's level forward. Your ticket volume swings a lot over the year. Monthly averages run from about 900 a day in summer to about 1,700 in winter.

**Backtest of your actual use case**

I ran the analyst's model as if forecasting the next three months from different cutoff dates, using only data available at that point, and compared monthly totals.

| Forecast start | Month 1 error | Month 2 error | Month 3 error | Average absolute error |
|---|---|---|---|---|
| Oct 2025 (same season as now) | −14% | −25% | −33% | **23.8%** |
| Jul 2025 | +4% | −1% | −16% | 6.9% |
| Jan 2026 | −3% | 0% | +8% | 3.6% |

Across 15 starting points, only 2 came in under your 10% bar. The typical miss was 15–30%, and it was often worse than 30% in the third month. For this forecast, the model would probably predict flat volume near September's roughly 1,200 a day. Last year's volume rose about 30% from September to October–December, and 2024 showed a similar rise.

**A seasonal alternative**

I tried last year's same-month total multiplied by the recent year-over-year growth, which is about 1.087 now. It stayed within about 1–2% on every backtest I could run, with an average absolute error of 0.6–1.2%. It gives these totals:

| Month | Forecast total tickets |
|---|---|
| October 2026 | ~43,400 |
| November 2026 | ~47,100 |
| December 2026 | ~56,100 |

**Caveats**

- There are only two years of data. That gives one prior-year comparison, and my backtests only cover forecasts starting January to June 2026. I could not test a forecast starting in October.
- The same data was used to pick the method and to test it, so the 1% errors are probably optimistic.
- The method assumes this year's seasonal shape and growth hold. A product launch, an outage, a pricing change or a holiday-calendar shift would break it.
- I haven't built a proper seasonal model. It would be worth the analyst doing that and backtesting it on forecasts made three months ahead.

**Recommendation**

Don't staff from the current model. Use the seasonal numbers as a provisional baseline for staffing. Plan a buffer or a mid-quarter re-check, because the evidence behind them is limited. October is already complete, so you could also compare it to the 43,400 estimate now. A big miss there would be an early warning for November and December.

I put the scripts in `[path] (`bt.py` and `seas.py`) and haven't changed anything in `data`.

### G08 (cell X2)

**No, don't use it for the October–December staffing. The 3.6% figure doesn't apply to this use, and the model is probably badly low for Q4.**

**Why 3.6% doesn't carry over.** I reproduced it (3.59%). The test hid 20% of days at random, so almost every test day had same-weekday training days on both sides, within a week or two. That is interpolation. Staffing needs a forecast 1 to 3 months past the last data point, and the model can't do that. For a future day, its 4 nearest same-weekday days are just the last 4 weeks of September, so it forecasts roughly a flat September level.

**The series is strongly seasonal.** Daily volume ran about 900 in July 2025, about 1,700 in January 2026, and about 900–1,000 in summer 2026. Q4 is the rising part of the cycle.

**Backtest that matches the real use.** I fit on data up to each month-end and forecast the next three calendar months, comparing monthly totals. There are 17 forecast origins.
- **Same season, September 2025 origin:** errors of −14%, −25% and −33% for months 1, 2 and 3, averaging 24% absolute. That origin is the only one that matches today's situation, so it is one sample.
- **Across all origins:** the three-month average absolute error ranged from 3.6% to 33% and exceeded 10% in 15 of 17. The model passes your 10% bar only near seasonal turning points, in about 2 of 17 origins.

**What it forecasts for Q4 2026** (my computation from the analyst's code):

| Month | Model | Same month last year | Last year × 1.087 (YoY growth, Jul–Sep) |
|---|---|---|---|
| Oct | 36,861 | 39,912 | 43,381 |
| Nov | 35,758 | 43,333 | 47,099 |
| Dec | 37,334 | 51,568 | 56,050 |

The model implies volume falls or stays flat through the holiday peak, which contradicts the one prior Q4 in the data. If this year repeats last year's seasonal shape, the model under-forecasts by roughly 15%, 24% and 33% (the same as the September 2025 backtest). That would mean about 20–25% short on average.

**Caveats.**
- The data has only two years. Seasonality rests on a single repeat, so "Q4 rises" is strongly suggested but not established.
- The YoY-scaled column is a rough reference. I haven't backtested it, because only one full prior year exists for most origins.
- I did not check for causes such as product changes or promotions that could explain the seasonality. They don't change the conclusion, since the model ignores seasonality either way.

**Recommendation.**
1. Don't staff from this model's totals.
2. Have the analyst re-evaluate with a forward-in-time split, forecasting 1 to 3 months ahead from each origin. They should add a seasonal and trend term, such as last year's same month times a growth factor.
3. Judge any replacement on whether its three monthly totals land within 10% of actual, not on daily MAPE.
4. Until then, plan staffing around the seasonal reference above, with a range around it.

Today is Nov 25 and the data stops at Sept 30. If October actuals exist, they would test this immediately, so please share them.

### G09 (cell X2)

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

**Next step.** Ask the analyst to re-fit with a seasonal and trend component, such as last year's same month scaled by recent growth. Then score it with the rolling-origin backtest above, forecasting 1–3 months ahead and requiring the 10% bar to hold. The scripts are in `scripts/` (`bt.py`, `fc.py`, `cov.py`) if you want to reuse them.

### G10 (cell X3)

**Deploy Model B.** Its top-500 list catches far more of the customers who actually churn.

Estimation on the 10,000 holdout customers, base churn rate 13.8%. Precision means the share of the called customers who actually churned.

| | Model A | Model B |
|---|---|---|
| Precision in top 500 (your call list) | 34.6% (173 churners) | 60.4% (302 churners) |
| Precision in top 100 | 48% | 81% |
| Precision in top 1,000 | 30.5% | 50.5% |
| AUC (ranking quality overall) | 0.687 | 0.817 |

- **Size of the gap:** B beats A by 25.8 points of precision at 500, about 129 more churners reached per list. A bootstrap over customers (2,000 resamples, 95% interval) puts the paired difference at +20 to +31 points. The whole interval is far above any plausible practical threshold.
- **Not a tie-breaking artifact:** Both models have clear score gaps at the 500 cutoff. B also wins at every list size I checked (100, 250, 500, 1,000) and on AUC, so the result doesn't depend on the exact 500 cutoff.
- **Different customers:** The two top-500 lists share only 117 customers, so the choice changes who gets called, not just the order.

**Limits:**
- The estimate assumes next quarter's customers and churn behavior look like last quarter's. Drift would move both models' absolute precision, but a 20+ point paired gap across all list sizes is unlikely to reverse.
- Precision at 500 is a prediction-quality measure, not a causal one. It says B finds likelier churners. It doesn't say calls will save them. If the team wants to call people they can actually persuade, that needs a separate test with a randomized holdout of the call list.
- I did not check how the holdout relates to the training data, or whether scores were calibrated or tuned against this holdout. If B's hyperparameters were selected on this same data, its numbers are somewhat optimistic. That is worth confirming, though the margin is large.
