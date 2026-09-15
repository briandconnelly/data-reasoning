import csv, math
from collections import defaultdict

path = "/var/folders/q1/yy47kpf51gb44d8wg1ywz4p80000gq/T/arm-s9-baseline-rmcm0e2u/data/signups.csv"

rows = []
with open(path) as f:
    r = csv.DictReader(f)
    for row in r:
        rows.append({
            "date": row["date"],
            "variant": row["variant"],
            "visits": int(row["visits"]),
            "signups": int(row["signups"]),
        })

by_variant = defaultdict(lambda: {"visits":0, "signups":0})
by_day = defaultdict(dict)
for row in rows:
    v = row["variant"]
    by_variant[v]["visits"] += row["visits"]
    by_variant[v]["signups"] += row["signups"]
    by_day[row["date"]][v] = row

nA, xA = by_variant["A"]["visits"], by_variant["A"]["signups"]
nB, xB = by_variant["B"]["visits"], by_variant["B"]["signups"]
pA = xA/nA
pB = xB/nB
diff = pB - pA
rel_lift = diff/pA

# Pooled z-test (proportion test)
p_pool = (xA+xB)/(nA+nB)
se_pool = math.sqrt(p_pool*(1-p_pool)*(1/nA+1/nB))
z = diff/se_pool

# unpooled SE for CI on difference
se_unpooled = math.sqrt(pA*(1-pA)/nA + pB*(1-pB)/nB)
ci_low = diff - 1.96*se_unpooled
ci_high = diff + 1.96*se_unpooled

# two-sided p-value from z using error function
def norm_sf(x):
    return 0.5*math.erfc(x/math.sqrt(2))
p_value = 2*norm_sf(abs(z))

print("=== Overall pooled totals ===")
print(f"A: visits={nA}, signups={xA}, rate={pA:.4%}")
print(f"B: visits={nB}, signups={xB}, rate={pB:.4%}")
print(f"Absolute diff (B-A): {diff:.4%}  (pct points: {diff*100:.2f})")
print(f"Relative lift: {rel_lift:.2%}")
print(f"Pooled z = {z:.3f}, two-sided p-value = {p_value:.5f}")
print(f"95% CI for absolute diff (unpooled SE): [{ci_low:.4%}, {ci_high:.4%}]")

print()
print("=== Daily conversion rates ===")
daily_diffs = []
daily_rel = []
print(f"{'date':12} {'A rate':>8} {'B rate':>8} {'diff(pp)':>9}")
for date in sorted(by_day.keys()):
    a = by_day[date]["A"]
    b = by_day[date]["B"]
    ra = a["signups"]/a["visits"]
    rb = b["signups"]/b["visits"]
    d = rb - ra
    daily_diffs.append(d)
    daily_rel.append(d)
    print(f"{date:12} {ra:8.3%} {rb:8.3%} {d*100:8.2f}")

n = len(daily_diffs)
mean_d = sum(daily_diffs)/n
var_d = sum((d-mean_d)**2 for d in daily_diffs)/(n-1)
sd_d = math.sqrt(var_d)
se_d = sd_d/math.sqrt(n)
t_stat = mean_d/se_d
# days B > A
wins_B = sum(1 for d in daily_diffs if d>0)

print()
print("=== Paired daily analysis (day as unit) ===")
print(f"n days = {n}")
print(f"mean daily diff (B-A) = {mean_d*100:.2f} pp, sd = {sd_d*100:.2f} pp, se = {se_d*100:.2f} pp")
print(f"paired t-stat = {t_stat:.3f} (approx df={n-1}, compare to t-crit ~2.16 for df=13, alpha=0.05 two-sided)")
print(f"days B beat A: {wins_B} / {n}")

# check for trend over time (novelty effect) - simple check of daily diff over time via correlation with day index
idx = list(range(n))
mean_idx = sum(idx)/n
cov = sum((idx[i]-mean_idx)*(daily_diffs[i]-mean_d) for i in range(n))
var_idx = sum((i-mean_idx)**2 for i in idx)
slope = cov/var_idx if var_idx else 0
print(f"trend slope of daily diff over time (pp/day): {slope*100:.3f}")

# visits balance check
print()
print("=== Sample size / balance check ===")
print(f"Total visits A: {nA}, B: {nB}, ratio B/A: {nB/nA:.3f}")
