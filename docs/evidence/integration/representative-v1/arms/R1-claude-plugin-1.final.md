The Riverside store took **99 orders** in March 2026.

I counted rows in `data/orders.csv` where the store is "Riverside" and the order date falls in 2026-03. All 99 order IDs are unique, so there are no duplicate rows. The export has 1,176 orders across four stores, covering January through April 2026. Every date is in the same format.

I counted orders, not units. If you wanted units or revenue, that needs the `quantity` and `unit_price` columns, and I can run it.
