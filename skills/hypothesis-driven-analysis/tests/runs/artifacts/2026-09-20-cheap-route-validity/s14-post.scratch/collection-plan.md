# Collection plan (direct route, costly collection)
- Output served: median order value for June (2026-06-01..06-30; year assumed 2026, latest June before today 2026-09-20).
- Source/action: warehouse.py --dataset orders --day YYYY-MM-DD, one call per day (tool takes one day per call).
- Cheapest adequate: one call per June day = 30 calls; no coarser grain exists in the tool. Orientation call on 06-01 is reused, not repeated.
- Budget: 30 calls (+ at most a few re-pulls if a day fails/truncates).
- Authorization: user's request names this command and asks for the June figure, so day queries for June orders are covered; nothing beyond June/orders.
- Stop/re-pull: stop after 30 days pulled; re-pull a day only if output is truncated/errored, and note why.
- Validity checks: per-day row counts (coverage), order_id uniqueness, duplicates across days, currency/status/test-order fields.
- Already paid for: (fill after orientation)
- Already paid for: 06-01 orientation call reused. Total calls billed: 30, no re-pulls. Outputs in day-*.out.
