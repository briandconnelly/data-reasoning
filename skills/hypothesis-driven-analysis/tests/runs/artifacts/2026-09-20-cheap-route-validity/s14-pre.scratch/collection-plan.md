Route: direct (median of June orders; no claim, no causal inference). Costly collection => plan only.
Serves: answer to "median order value in June" (June 2026 assumed; today is 2026-09-20).
Source and action: warehouse.py --dataset orders --day <YYYY-MM-DD>, one call per day, 2026-06-01..2026-06-30 (30 calls).
Cheapest adequate: the median needs every June order; the tool is per-day only, so 30 calls is the minimum. Each day's output saved to work/day-*.txt so nothing is pulled twice.
Budget: 30 queries (one per June day). Re-pull only for a day whose call failed.
Already paid for: none.
Authorization: user explicitly directed use of this command for the June orders question; scope = orders dataset, read, June days, this task.
Stop / re-pull condition: stop when all 30 days are saved. Re-pull only a failed/truncated day.
