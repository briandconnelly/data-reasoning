### B01 (cell X1)

**Sign with Acme.**

Brightline's trial looks better, but it is too small to tell you whether Brightline stays under the 3% penalty line. The penalty is large enough that the comparison turns on that line.

**The numbers**
- **Acme:** 1,000 defects in 50,000 units over 12 months, so 2.0%. Monthly rates stay between 1.85% and 2.09%. A full-year rate above 3% is effectively impossible. Expected cost is about 2,000 defects × $15 = **$30k**, with no penalty.
- **Brightline:** 1 defect in 150 units, so 0.67%. That is only 150 units over 5 days (30 a day). A trial this size is consistent with true rates anywhere from about 0.02% to 3.7% (95% interval).

**Cost at 100,000 units**
Defect cost is about $1.5M × the defect rate, plus a $1M penalty if the rate goes above 3%. The $15 return cost per defect is small next to the penalty. Brightline would save at most about $30k in returns if it were perfect. A 3% breach costs $1M. So Brightline only wins if the chance it exceeds 3% is below roughly 1.5–2%.

I put a few different priors on Brightline's true rate and updated on the trial:

| Prior on Brightline | Mean rate | P(>3%) | Expected cost |
|---|---|---|---|
| Uniform | 1.3% | 5.7% | ~$77k |
| Jeffreys | 1.0% | 2.8% | ~$43k |
| Skeptical (centered near Acme, 50 units' weight) | 1.0% | 1.7% | ~$32k |
| Skeptical (centered near Acme, 200 units' weight) | 1.4% | 2.0% | ~$42k |

Acme's expected cost is about $30k under every prior. The most optimistic prior I tried only roughly ties with it. The rest make Brightline $10–45k worse in expectation, and every one carries a real chance of a $1M hit that Acme doesn't.

**Caveats**
- A trial batch is often a supplier's best effort. A sample of 150 that happens to beat Acme's average is weak evidence, and the "fewer defects than usual" comparison makes it look stronger than it is.
- Acme's 2.0% comes from 50,000 units over a full year. Brightline's 0.67% comes from 150 units over 5 days, so the two estimates are not comparably reliable.
- The choice is also one-way for the year (no mid-year switch), so there's no chance to correct if Brightline disappoints.

**What would change my answer:** a larger Brightline trial. If they ship about 1,000–2,000 units across several weeks and the rate stays under ~1.5%, the chance of breaching 3% drops enough that Brightline would be worth considering. The most it can save is about $30k a year. Another route is to negotiate a contract with Brightline that covers the penalty or caps its defect rate. Neither is in the current terms.

### B02 (cell X1)

**Stay with Acme.** With all 100,000 units committed to one supplier, I’d prioritize limiting exposure to the $1 million penalty. Brightline’s trial suggests lower returns costs, but one batch gives too little evidence about how it will perform across a full production year.

- **Acme** had 1,000 defects in 50,000 units over 12 months, a 2.00% defect rate. At that rate, next year’s returns would cost **$30,000**. Acme history
- **Brightline** had 1 defect in 150 units, a 0.67% defect rate. If that rate holds, returns would cost **$10,000**, saving **$20,000**. At 3,001 defects, just over the contract threshold, returns and the penalty would total **$1,045,015**. Brightline trial · Contract terms

If Acme holds at 2% and Brightline either matches its trial rate or just crosses the penalty threshold, a **1.93% chance of the penalty** wipes out Brightline’s expected savings. That’s a break-even scenario. The trial alone can’t establish Brightline’s annual penalty probability, and Acme’s history is also an assumption about next year. The recommendation rests on limiting the downside of a year-long commitment. [link]

### B03 (cell X1)

**Sign with Acme for all 100,000 units.** Brightline’s trial had 1 defect in 150 units (0.67%), versus Acme’s 1,000 in 50,000 (2.00%). Acme stayed below 3% in every recorded month. Brightline’s single batch leaves enough uncertainty about full-year quality that the $1 million penalty outweighs the expected savings on returns. Brightline trial · Acme history · Contract terms

Using a uniform prior for each supplier’s defect rate and assuming each has a stable rate across shipments, I estimate the following costs. Purchase prices are identical.

| Supplier | Expected returns cost | Chance of exceeding 3% | Expected returns and penalty cost |
|---|---:|---:|---:|
| Acme | $30,000 | Negligible under the model | $30,000 |
| Brightline | $19,700 | 5.7% | $76,800 |

At those returns estimates, Brightline’s penalty risk would need to be about **1% or less** to break even. A Jeffreys prior lowers its estimated risk to 2.8% and its expected cost to about $42,600, still above Acme’s. Both estimates assume the trial represents Brightline’s production. With only one batch, the data can’t establish how much its quality varies across batches.

### B04 (cell R2)

| Store | February 2026 orders | Average order total |
|---|---:|---:|
| Harbor | 80 | $117.15 |
| Hillcrest | 78 | $101.80 |
| Old Town | 41 | $113.85 |
| Riverside | 90 | $111.25 |

I multiplied `unit_price` by `quantity` and averaged the order totals for each store, rounding to the nearest cent.

### B05 (cell R2)

| Store | Orders in February 2026 | Average order total |
|---|---:|---:|
| Harbor | 80 | 117.15 |
| Hillcrest | 78 | 101.80 |
| Old Town | 41 | 113.85 |
| Riverside | 90 | 111.25 |

I calculated each order total as `unit_price × quantity`, averaged the totals by store, and rounded to two decimal places.

### B06 (cell X2)

**I wouldn’t use this model to set October–December staffing.** In the only historical Q4 that could be tested using data available through September 30, the model’s monthly totals were off by **23.8% on average**, above your 10% limit. It underforecast all three months.

| 2025 month | Forecast from September 30 | Actual tickets | Underforecast |
|---|---:|---:|---:|
| October | 34,290 | 39,912 | 14.1% |
| November | 32,724 | 43,333 | 24.5% |
| December | 34,656 | 51,568 | 32.8% |

I froze the training data at September 30, forecast every day in the quarter from that cutoff, and averaged the three absolute percentage errors on the monthly totals. Across all seven historical quarters tested this way, the model missed the 10% limit three times.

I reproduced the analyst’s **3.6% daily error**. In that random split, 142 of 146 held-out predictions used at least one ticket count from a later date. For a forecast made on September 30, the model instead repeats the same seven weekday averages through December, so it cannot anticipate the kind of month-to-month rise seen in Q4 2025. Analyst’s model

Using the prior year’s same-month totals as a simple benchmark would have yielded **8.0% average error** in Q4 2025. That’s one comparable quarter. The supplied data end on September 30, 2026, so actual Q4 2026 accuracy remains unknown.

### B07 (cell R1)

The Riverside store took **99 orders** in March 2026, counting each distinct order ID once.

### B08 (cell R2)

Average order total per store in February 2026 (order total = unit_price × quantity):

| Store | Orders | Average order total |
|---|---|---|
| Harbor | 80 | $117.15 |
| Riverside | 90 | $111.25 |
| Old Town | 41 | $113.85 |
| Hillcrest | 78 | $101.80 |

Harbor had the highest average and Hillcrest the lowest. No rows had unparseable prices or quantities. I didn't check for duplicate order IDs.

### B09 (cell X2)

**I wouldn’t use this model to set October–December staffing.** In the one historical test that matches the staffing decision, the model missed the monthly totals by **23.8% on average**, above your **10%** limit. It underforecast all three months.

I trained the model on data available through September 30, 2025, forecast all three months from that cutoff, and gave each month equal weight in the average absolute percentage error.

| Month | Forecast tickets | Actual tickets | Absolute error |
|---|---:|---:|---:|
| October 2025 | 34,290 | 39,912 | 14.1% |
| November 2025 | 32,724 | 43,333 | 24.5% |
| December 2025 | 34,656 | 51,568 | 32.8% |

I reproduced the analyst’s **3.6% daily error**. The random split let the model use ticket counts from later dates for 142 of 146 held-out days. For a forecast made at the end of September, every future occurrence of a given weekday gets the same prediction, based on the last four observed counts for that weekday. That keeps the forecast flat by weekday throughout the quarter. Analyst’s model

The supplied data contain one complete October–December backtest and end on September 30, 2026. The 2026 quarter’s actual error is therefore unknown. The available like-for-like test failed the staffing criterion.

### B10 (cell X3)

**Deploy Model B** if the goal is to reach as many likely churners as possible with 500 calls. On last quarter’s holdout, Model B’s top 500 included **302 customers who churned**, compared with **173** for Model A. That’s **129 more observed churners** for the same call budget.

| Holdout metric | Model A | Model B |
|---|---:|---:|
| Observed churners in the top 500 | 173 | 302 |
| Precision at 500 | 34.6% | 60.4% |
| Overall accuracy at a 0.5 cutoff | 84.6% | 79.5% |

Model A leads on overall accuracy at 0.5, but the call list is built by rank. Precision at 500 measures how many of those calls go to customers who churned.

I resampled the 10,000 holdout customers 5,000 times, rebuilding both top-500 lists on each draw. The middle 95% of Model B’s leads ranged from **100 to 153 additional churners**. That range reflects customer sampling within last quarter. The recommendation assumes next quarter’s list is drawn from a similar population. If the goal is to maximize **churn prevented**, the holdout leaves that question open because it doesn’t measure who would stay as a result of a call.

### B11 (cell X1)

**Sign with Acme.**

**Acme.** Its 12-month history is 1,000 defects in 50,000 units, a 2.0% rate. Every month falls between 1.85% and 2.1%, so it is very stable.
- Over 100,000 units you'd expect about 2,000 defects, which costs about $30,000 in returns.
- The chance of passing the 3% penalty line is essentially zero. That would need about 1,000 extra defects, and annual noise at this volume is only about ±45.

**Brightline.** The trial found 1 defect in 150 units, or 0.67%. That is better than Acme's 2.0%, but 150 units is a very small sample.
- The 95% range for its true rate is roughly 0.1% to 4%.
- Under a neutral prior, its rate is above 3% with about 5.7% probability.
- The same trial would be seen about 20% of the time even if Brightline were exactly as good as Acme (2%). It would still be seen about 6% of the time if Brightline were at 3%.

**Expected cost.** The $1M penalty drives the decision.

| | Returns | Penalty risk | Expected total |
|---|---|---|---|
| Acme | ~$30k | ~$0 | **~$30k** |
| Brightline | ~$20k | ~5.7% × $1M ≈ $57k | **~$77k** |

Brightline's likely saving on returns is only about $10k. Its penalty exposure is several times larger than that. Brightline would only break even if the chance of exceeding 3% were about 1% or less, and 150 units can't show that.

**Caveats.**
- The trial is a single batch inspected over five days. Suppliers often send their best units for a trial, so production-scale quality could be worse.
- You have no month-to-month variation for Brightline, and Acme's history shows how much that matters.
- A different prior changes the exact numbers, but the conclusion holds unless you strongly believe Brightline is much better.

**What would change this.** If Brightline will accept a larger trial, around 1,000 or more units across several production lots, I'd re-run the comparison. It would also help to negotiate a defect-rate guarantee or a share of the penalty. Either would remove the tail risk that drives this result.

### B12 (cell R2)

| Store | February 2026 orders | Average order total |
|---|---:|---:|
| Harbor | 80 | 117.15 |
| Hillcrest | 78 | 101.80 |
| Old Town | 41 | 113.85 |
| Riverside | 90 | 111.25 |

For each store, I averaged `unit_price × quantity` across its February orders and rounded to two decimal places.

### B13 (cell R1)

The Riverside store took **99 orders** in March 2026, based on distinct order IDs in orders.csv.

### B14 (cell R1)

The Riverside store took **99 orders** in March 2026.

### B15 (cell X2)

**I wouldn’t use this model to set Q4 staffing.** In the only historical October–December backtest the data supports, the model averaged **23.8% absolute error across the three monthly totals**, above your 10% limit. It underforecast all three months.

I trained the analyst’s model on data through September 30, 2025, forecast all three months at once, and summed the daily predictions by month. The model received no new ticket counts during the quarter.

| Month | Forecast tickets | Actual tickets | Below actual |
|---|---:|---:|---:|
| October 2025 | 34,290 | 39,912 | 14.1% |
| November 2025 | 32,724 | 43,333 | 24.5% |
| December 2025 | 34,656 | 51,568 | 32.8% |

I reproduced the analyst’s **3.6% daily error**. The random holdout let the model use later ticket counts to predict earlier days. In 142 of 146 held-out predictions, at least one of the four neighbors came from after the day being predicted. At a September cutoff, every future Monday uses the same four observed Mondays, and the same applies to each other weekday. The forecast therefore has no way to capture a sustained rise or fall during the quarter.

The file ends September 30, 2026, so the actual error for Q4 2026 is still unverified. The available Q4 backtest failed the staffing threshold.

### B16 (cell X3)

Deploy **Model B**. On last quarter’s holdout, it ranked **302 actual churners** in its top 500, compared with **173** for Model A. That’s **129 more churners reached** with the same 500 calls.

| Model | Actual churners in top 500 | Precision at 500 |
|---|---:|---:|
| A | 173 | 34.6% |
| B | 302 | 60.4% |

Precision at 500 matches the team’s call capacity. The holdout measures how well each model targets customers who ultimately churned. The effect of calling them on retention remains unknown.

### B17 (cell R1)

The Riverside store took **99 orders** in March 2026, counting unique order IDs in the export.

### B18 (cell X2)

**No. I would not use this model to set October–December staffing.** In the only prior October–December backtest available, its monthly totals had **23.8% mean absolute percentage error**, above your 10% threshold. It underforecast all three months.

| 2025 month | Forecast tickets | Actual tickets | Absolute error |
|---|---:|---:|---:|
| October | 34,290 | 39,912 | 14.1% |
| November | 32,724 | 43,333 | 24.5% |
| December | 34,656 | 51,568 | 32.8% |

I froze the training data at September 30, 2025, forecast all three months from that cutoff, and weighted each month equally when averaging the errors. Forecast counts are rounded for display.

I reproduced the analyst’s **3.6% daily error**. The random holdout let the model use later ticket counts for 142 of 146 test days. At the September staffing cutoff, all future dates with the same weekday get the same prediction, so the model cannot capture a rise in demand across the quarter. Analyst notes · Model code

The supplied data supports one season-matched backtest. It establishes that the model missed your tolerance in 2025. The 2026 quarterly error remains unknown because the supplied actuals end September 30, 2026.

### B19 (cell X3)

**Deploy Model B for the 500-call list.** On last quarter’s 10,000-customer holdout, Model B put **129 more actual churners** in the top 500 than Model A did.

| Model | Actual churners in top 500 | Precision at 500 | Accuracy at 0.5 |
|---|---:|---:|---:|
| A | 173 | 34.6% | 84.60% |
| B | 302 | 60.4% | 79.45% |

Model A had higher accuracy at the team’s usual 0.5 cutoff. Model B had higher precision at 500, which matches how the retention team will select customers.

A paired bootstrap that reranked both models on each resampled list gave a 95% interval of **100 to 153 additional churners in Model B’s top 500**, assuming next quarter’s list is drawn from a similar customer population. The holdout measures who churned. Estimating how many customers the calls would retain requires evidence on the effect of outreach.

### B20 (cell X1)

**Stay with Acme.** For a commitment of all 100,000 units, I’d give more weight to Acme’s year of shipments than to Brightline’s single trial batch, given the $1 million penalty if annual defects exceed 3%.

Acme recorded **1,000 defects in 50,000 units (2.00%)**, which projects to **$30,000 in annual returns** if that rate holds. Brightline recorded **1 defect in 150 units (0.67%)**. If Brightline sustained that rate, returns would cost about **$10,000**, saving about **$20,000** at the same unit price.

Using $30,000 as Acme’s planning cost and $10,000 as Brightline’s expected returns cost, Brightline breaks even at a **2% chance of triggering the penalty**. The single trial batch gives too little evidence about full-year production to establish that the chance is below 2%. The recommendation assumes Acme’s history is a reasonable baseline for next year and gives priority to limiting the seven-figure downside.

[link]

### B21 (cell X2)

**I wouldn’t use this model to set October–December staffing.** In the prior October–December backtest, it underforecast all three months and averaged **23.8% absolute error** on monthly totals, above your 10% threshold.

I reproduced the analyst’s 3.6% daily error. The random holdout lets the model use later observations to predict earlier held-out days, often drawing on nearby weeks. At the September 30 staffing cutoff, all three months are forecast at once from the same four most recent observations for each weekday.

I reran the analyst’s code using only data available before each quarter, then summed the daily forecasts by month and averaged the three absolute percentage errors. The model met your threshold in **four of seven** complete quarters. Here’s how it performed in the one prior October–December quarter.

| Month | 2025 forecast | 2025 actual | Underforecast |
|---|---:|---:|---:|
| October | 34,290 | 39,912 | 14.1% |
| November | 32,724 | 43,333 | 24.5% |
| December | 34,656 | 51,568 | 32.8% |

Using data through September 30, 2026, the model forecasts **36,861** tickets for October, **35,758** for November, and **37,334** for December. The supplied data ends before those months, so their actual errors are unknown.

### B22 (cell X3)

**Deploy Model B.** With a budget of 500 calls, Model B’s top-ranked list contained 302 actual churners on last quarter’s holdout. Model A’s contained 173. That’s **129 more churners reached with the same number of calls**. Holdout scores

| Model | Churners in top 500 | Precision at 500 | Accuracy at 0.5 cutoff |
|---|---:|---:|---:|
| A | 173 | 34.6% | 84.6% |
| B | 302 | 60.4% | 79.5% |

Model A wins on the currently reported 0.5-cutoff accuracy. Precision at 500 matches how the retention team will actually select customers.

A paired bootstrap that rebuilt both top-500 lists on each resample gave a 95% interval of **100 to 153 additional churners** for Model B. The recommendation assumes next quarter’s customer mix and model performance are comparable to the holdout. The scores and churn outcomes measure how well each model targets likely churners. Estimating how many customers the calls would retain requires evidence on the effect of outreach.

### B23 (cell X3)

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

### B24 (cell R1)

The Riverside store took **99 orders** in March 2026.

I counted rows in `data/orders.csv` where the store is "Riverside" and the order date falls in 2026-03. All 99 order IDs are unique, so there are no duplicate rows. The export has 1,176 orders across four stores, covering January through April 2026. Every date is in the same format.

I counted orders, not units. If you wanted units or revenue, that needs the `quantity` and `unit_price` columns, and I can run it.

### B25 (cell R2)

| Store | February 2026 orders | Average order total |
|---|---:|---:|
| Harbor | 80 | $117.15 |
| Hillcrest | 78 | $101.80 |
| Old Town | 41 | $113.85 |
| Riverside | 90 | $111.25 |

I multiplied `unit_price` by `quantity` and averaged the resulting order totals by store, rounded to the nearest cent.

### B26 (cell X1)

**Sign with Acme for all 100,000 units.** Brightline’s trial had a lower defect rate, but the expected savings on returns are too small to justify the modeled risk of a $1 million penalty.

| Supplier | Observed defects | Expected returns cost | Chance of exceeding 3% | Expected total quality cost |
|---|---:|---:|---:|---:|
| Acme | 1,000 / 50,000 (2.00%) | $30,029 | Near zero | $30,029 |
| Brightline | 1 / 150 (0.67%) | $19,737 | 5.71% | $76,826 |

With identical unit prices, Brightline saves about **$10,300** in expected returns costs. That saving can absorb only about a **1.03%** chance of the penalty. The model puts Brightline’s chance at **5.71%**, adding roughly **$57,100** in expected penalty cost.

The estimates use a beta-binomial model with a uniform prior for each supplier’s defect rate. It assumes each supplier’s underlying rate is stable and that the observed units represent next year’s production. Using a Jeffreys prior instead lowers Brightline’s estimated penalty chance to **2.77%** and its expected quality cost to about **$42,600**, still above Acme’s. Brightline’s single batch leaves batch-to-batch variation unmeasured.

### B27 (cell R2)

Average order total by store for February 2026 (order total = unit_price × quantity):

| Store | Orders | Average order total |
|---|---|---|
| Harbor | 80 | $117.15 |
| Old Town | 41 | $113.85 |
| Riverside | 90 | $111.25 |
| Hillcrest | 78 | $101.80 |

The file had no missing values, and every order_id was unique. Each row is one product line, so I treated each row as an order.

### B28 (cell R1)

Riverside took **99 orders** in March 2026, based on unique order IDs in the export.

### B29 (cell X2)

**No, not as it stands.** The 3.6% error is real, but it measures a different task from the one you need. For October to December, the model would likely under-forecast badly.

**Why the 3.6% doesn't carry over**
- The analyst held out 20% of days at random. Each held-out day is predicted from the four nearest same-weekday days, and most of those are weeks on either side of it. That is interpolation inside a known stretch, and the model sees the future around each day.
- Your task is different. Nothing after September 30 exists yet, so the "nearest" days are always the last four weeks. The model then just repeats late-September levels and has no seasonality.
- I reproduced the 3.6% with their code.

**Backtest that matches your use**
I forecast each of the next three months using only data up to the origin, then scored the monthly totals. Ticket volume swings strongly with the season, from about 900 a day in summer to about 1,700 in winter.

| Origin | Analyst model, avg error across 3 months |
|---|---|
| Dec 2025 | 3.6% |
| Jan 2026 | 13.8% |
| Feb 2026 | 25.2% |
| Mar 2026 | 33.3% |
| Apr 2026 | 29.0% |
| May 2026 | 14.1% |
| Jun 2026 | 7.1% |

- Only the Dec 2025 and Jun 2026 origins came in under your 10% bar, and the Nov 2025 origin missed at 11.9%. That is 2 of 8.
- The misses were worst in the seasonal ramps. The model forecast roughly 30,000 to 40,000 tickets a month while actuals ran about 35,000 to 52,000.
- Your three months are an up-ramp, the same situation as the Mar–Apr origins.

**October to December forecast from the analyst's model**

| Month | Analyst model | Same month last year |
|---|---|---|
| Oct | 36,900 | 39,900 |
| Nov | 35,800 | 43,300 |
| Dec | 37,300 | 51,600 |

Last year's December was about 51,600 tickets, so the model's 37,300 is roughly 28% low. Staffing from it would leave you badly short in December.

**A simple alternative that passes the same backtest**
I tried last year's same day (364 days earlier), scaled by recent year-over-year growth. Over the origins from Dec 2025 on, it averaged 0.4% to 1.5% error on three-month monthly totals. The Nov 2025 origin was off by about 33%, but that is an artifact. There was less than a year of history then, so the growth rate couldn't be computed properly.

Its forecasts are:
- Oct: about 43,200
- Nov: about 47,700
- Dec: about 55,800

**Caveats**
- The alternative is only validated on about seven origins, with a single prior year to copy from. It also assumes this year's seasonal shape repeats, and a holiday shift or a product change could break that.
- Because the sample is small, I'd treat it as a reasonable starting point, not a settled number. Run it next to the analyst's model through October and adjust staffing as actuals come in.
- It also has no test against any event that wasn't in the two years of data.

My backtest script is at `/tmp/work/bt.py`. I didn't change anything in `data`.

### B30 (cell X3)

**Deploy Model B.** On last quarter’s holdout, it put 302 actual churners in the top 500, compared with 173 for Model A. That’s **129 more churners reached** for the same 500 calls.

| Holdout metric | Model A | Model B |
|---|---:|---:|
| Actual churners in top 500 | 173 | **302** |
| Precision at 500 | 34.6% | **60.4%** |
| Accuracy at the 0.5 cutoff | **84.6%** | 79.45% |

Precision at 500 matches the team’s calling policy because the team ranks customers and fills a fixed list. The holdout measures how many churners each model identifies. It doesn’t measure how many calls would prevent churn.

### B31 (cell X1)

**Stay with Acme** if the priority is limiting exposure to the $1 million penalty. Acme recorded 1,000 defects in 50,000 units (2.00%), with monthly rates between 1.85% and 2.09%. Brightline’s trial was better at one defect in 150 units (0.67%), but one batch gives no reliable estimate of how often full-year production would exceed the 3% penalty threshold.

At those observed rates, Brightline would save about **$20,000** in returns over 100,000 units. Assuming Acme repeats its historical rate and Brightline averages its trial rate in years without a penalty, a **2.87% chance** of triggering the penalty would erase those savings in expectation. That calculation uses the smallest possible breach, 3,001 defective units. A larger breach would lower the break-even probability.

Even if the trial units were independent and representative of full production, the one-sided 95% upper confidence limit for Brightline’s defect rate would be **3.12%**. With one batch and no midyear switch, Acme is the conservative choice. The expected-cost ranking depends on an annual penalty probability the trial cannot establish.

[link]

### B32 (cell R2)

| Store | February 2026 orders | Average order total |
|---|---:|---:|
| Harbor | 80 | $117.15 |
| Hillcrest | 78 | $101.80 |
| Old Town | 41 | $113.85 |
| Riverside | 90 | $111.25 |

I calculated `unit_price × quantity` for each February order, then averaged those totals by store and rounded to two decimal places.

### B33 (cell X2)

**No, don't use it as it stands.** The 3.6% figure is real, but it doesn't measure the thing you need.

**Why the number misleads.** The analyst held out 20% of days at random. Each held-out day sits between training days, so the model gets near-identical neighbors on the same weekday a week earlier and a week later. That only tests interpolation. You need to forecast 1–3 months past the last data point. For those days the "nearest 4 same-weekday days" are just the last four weeks of September. The model therefore repeats the September level and has no seasonality or trend.

**What the data shows.** Volume is strongly seasonal. It bottoms out around 900 a day in summer and peaks around 1,700 a day in December and January. It has also grown about 8–10% year over year, steadily, in every month.

**Backtest.** I refit the analyst's model at each month-start using only earlier data, then forecast the next three months. I compared monthly totals, which is your criterion. The model has only about 22 months of data, so I could run 12 origins.
- The three-month average error ranged from 3.6% to 33%.
- It passed your 10% bar in only 2 of 12 origins (3.6% and 7.1%).
- The median was about 19%.
- Errors grow with horizon, reaching 30–50% in month 3.
- The direction depends on the season. Forecasts made in autumn come out low, because the model projects a low level into the rising winter. Forecasts made in spring come out high.

**What it says for Oct–Dec 2026 versus last year.**

| Month | Model forecast | Oct–Dec 2025 actual | Last year × 1.08 growth |
|---|---|---|---|
| Oct | 36,861 | 39,912 | ~43,000 |
| Nov | 35,758 | 43,333 | ~46,800 |
| Dec | 37,334 | 51,568 | ~55,600 |

The model forecasts a flat quarter with December below last year's December. That is the same autumn under-forecast pattern as in the backtest. If you staffed to it, December would likely be understaffed by about 30%.

**What I'd do.** A seasonal approach, such as last year's same month scaled by recent year-over-year growth, is a better starting point. Year-over-year growth has stayed in a narrow 8–11% band. I couldn't backtest it properly for Oct–Dec, because there's only one prior year of history, so I can't promise it meets the 10% bar. It also assumes this December looks like last December. With two years of data, the spread in that ratio is the main uncertainty. Treat the table as a rough sanity range, not a validated forecast. I haven't built or validated a replacement model.

I didn't change any files. The backtest script is in `/tmp/bt.py` if you want to rerun it.

### B34 (cell X3)

**Deploy Model B.**

I scored both models on the 10,000 holdout customers. 1,377 of them churned, a base rate of 13.8%. Your use case is a call list of the 500 highest-scored customers, so I compared the models on that list.

| Metric | Model A | Model B |
|---|---|---|
| Precision in the top 500 (churners per 500 called) | 34.6% (173) | 60.4% (302) |
| Precision in the top 100 | 48% | 81% |
| Precision in the top 1,000 | 30.5% | 50.5% |
| AUC (overall ranking quality) | 0.687 | 0.817 |

- **Size of the gap:** B's list would reach about 129 more churners than A's. A bootstrap over customers gives a 95% interval of roughly 98 to 152 more, so the gap is not noise.
- **Consistency:** B is ahead at every list size I checked, and on AUC too. The result doesn't depend on exactly where the cutoff falls.
- **Different lists:** the two models' top-500 lists share only 117 customers, so the choice changes who gets called.

Two caveats:
- This assumes next quarter's scoring pool is about the same size as this holdout (about 10,000 customers). If the pool is much larger or smaller, 500 is a different fraction of it. B's lead held at every top-k I checked, so I'd expect the ranking to hold, but the exact precision would shift.
- Precision measures who churned, not who the calls would save. If the retention team's offer works better on some kinds of customers, such as those about to churn anyway, the best list could differ. The data here can't tell us that.

### B35 (cell R1)

The Riverside store took **99 orders** in March 2026.

### B36 (cell R2)

| Store | February 2026 orders | Average order total |
|---|---:|---:|
| Harbor | 80 | 117.15 |
| Hillcrest | 78 | 101.80 |
| Old Town | 41 | 113.85 |
| Riverside | 90 | 111.25 |

I calculated each order total as `unit_price × quantity` and rounded each store’s average to two decimal places.

### B37 (cell X3)

Deploy **Model B**. On last quarter’s holdout, it ranked **302 actual churners** in its top 500, versus **173** for Model A. That’s **129 more churners reached** with the same 500 calls.

| Model | Churners in top 500 | Precision at 500 |
|---|---:|---:|
| A | 173 | 34.6% |
| B | 302 | 60.4% |

Neither model had a score tie at the cutoff. This measures how well each model targets customers who churned. The holdout does not measure how many churns a call would prevent. Holdout scores

### B38 (cell X2)

No. The model averaged **23.8% absolute error on monthly totals** in the one October–December backtest supported by the data, exceeding your 10% staffing threshold.

I trained the model on data available through September 30, 2025, then forecast all three months without updating it. I summed the daily forecasts by month and gave each month equal weight in the average error.

| 2025 month | Forecast tickets | Actual tickets | Absolute error |
|---|---:|---:|---:|
| October | 34,290 | 39,912 | 14.1% |
| November | 32,724 | 43,333 | 24.5% |
| December | 34,656 | 51,568 | 32.8% |

I reproduced the reported **3.6% daily error**. The random holdout let the model use later ticket counts for 142 of 146 test days. At the September staffing cutoff, the model instead repeats a fixed weekly pattern across the whole quarter. In the backtest, it underforecast all three months as demand rose.

The supplied data ends September 30, 2026, so the 2026 forecasts can’t yet be scored from these files. The available backtest supports keeping this model out of the staffing decision.

### B39 (cell X1)

**Sign with Acme for all 100,000 units.** Brightline’s trial had a lower defect rate, but one 150-unit batch leaves enough uncertainty about full-year quality to outweigh the likely savings on returns.

Acme recorded **1,000 defects in 50,000 units (2.00%)** across 12 months. Brightline recorded **1 defect in 150 units (0.67%)**. If those observed rates held next year, Brightline would save about **$20,000** in returns. That saving would be erased by even a **2% chance** of triggering the **$1 million penalty** for more than 3,000 defects. Acme history · Brightline trial · Contract terms

Assuming each supplier has a stable defect rate and the samples are representative, two standard Bayesian priors put Brightline’s chance of triggering the penalty at **2.8% to 5.7%**, with expected returns and penalties totaling **$43,000 to $77,000**. The same model puts Acme at about **$30,000**, with a negligible chance of triggering the penalty. Those estimates depend on the model, and a single trial batch gives no way to measure how Brightline’s quality varies across production runs.

### B40 (cell R1)

Riverside took **99 orders** in March 2026.

I counted rows in `data/orders.csv` where the store is `Riverside` and the order date is in 2026-03. All 99 order IDs are distinct, so there are no duplicate rows. The store names and date formats were consistent, so no variants like "riverside" were missed.

This counts orders (rows), not units sold or revenue. I can compute those too if you want them.
