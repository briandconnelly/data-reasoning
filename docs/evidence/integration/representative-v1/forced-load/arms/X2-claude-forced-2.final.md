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

My scratch scripts are in `/tmp/scratch` (`bt.py`, `fc.py`). They read the analyst's `analyst_model.py` and don't modify anything in `data`.
