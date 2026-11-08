# Worker return: active subscriptions by plan

Task: count subscriptions with status = 'active' on 2026-10-31, by plan.
Source: warehouse table `billing.subscriptions`, nightly load completed 2026-11-01 02:14 UTC.
Grain: one row per subscription; a customer with two subscriptions counts twice.

Query run:

    SELECT plan, COUNT(*) AS active
    FROM billing.subscriptions
    WHERE status = 'active'
      AND started_at <= '2026-10-31'
      AND (ended_at IS NULL OR ended_at > '2026-10-31')
    GROUP BY plan;

Output (3 rows):

| plan | active |
| --- | --- |
| basic | 41,210 |
| pro | 12,884 |
| enterprise | 1,067 |

Total: 56,161 active subscriptions; pro is 25.1% of the total.
