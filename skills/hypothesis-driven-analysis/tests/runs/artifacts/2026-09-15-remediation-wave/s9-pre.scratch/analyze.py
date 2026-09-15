import csv
import random
import math

path = "/var/folders/q1/yy47kpf51gb44d8wg1ywz4p80000gq/T/arm-s9-pre-le1bak1n/data/signups.csv"

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

dates = sorted(set(r["date"] for r in rows))
print(f"n_days={len(dates)} first={dates[0]} last={dates[-1]}")

by_day = {}
for r in rows:
    by_day.setdefault(r["date"], {})[r["variant"]] = (r["visits"], r["signups"])

# coverage check: every day has both A and B
missing = [d for d, v in by_day.items() if "A" not in v or "B" not in v]
print("days missing a variant:", missing)

variants = ["A", "B"]
totals = {v: {"visits": 0, "signups": 0} for v in variants}
for r in rows:
    totals[r["variant"]]["visits"] += r["visits"]
    totals[r["variant"]]["signups"] += r["signups"]

for v in variants:
    t = totals[v]
    rate = t["signups"] / t["visits"]
    print(f"variant {v}: visits={t['visits']} signups={t['signups']} rate={rate:.5f}")

pA = totals["A"]["signups"] / totals["A"]["visits"]
pB = totals["B"]["signups"] / totals["B"]["visits"]
diff = pB - pA
rel = diff / pA
print(f"pooled diff (B-A) = {diff:.5f} ({diff*100:.2f} pp)")
print(f"relative lift = {rel*100:.2f}%")

# Pooled two-proportion Wald 95% CI on the difference
nA, nB = totals["A"]["visits"], totals["B"]["visits"]
se = math.sqrt(pA*(1-pA)/nA + pB*(1-pB)/nB)
z = 1.959963985
lo, hi = diff - z*se, diff + z*se
print(f"pooled two-proportion 95% CI on diff: [{lo:.5f}, {hi:.5f}] -> [{lo*100:.2f}pp, {hi*100:.2f}pp]")

# Day-level bootstrap: resample days with replacement, recompute pooled rates each variant, take diff
random.seed(12345)
n_boot = 20000
boot_diffs = []
day_list = dates
for _ in range(n_boot):
    sample_days = [random.choice(day_list) for _ in range(len(day_list))]
    sv = {v: {"visits": 0, "signups": 0} for v in variants}
    for d in sample_days:
        for v in variants:
            vis, sig = by_day[d][v]
            sv[v]["visits"] += vis
            sv[v]["signups"] += sig
    bpA = sv["A"]["signups"] / sv["A"]["visits"]
    bpB = sv["B"]["signups"] / sv["B"]["visits"]
    boot_diffs.append(bpB - bpA)

boot_diffs.sort()
def pct(p):
    idx = int(p * (len(boot_diffs)-1))
    return boot_diffs[idx]

lo_b = pct(0.025)
hi_b = pct(0.975)
print(f"day-level bootstrap 95% CI on diff (B-A): [{lo_b:.5f}, {hi_b:.5f}] -> [{lo_b*100:.2f}pp, {hi_b*100:.2f}pp]")
print(f"bootstrap mean diff: {sum(boot_diffs)/len(boot_diffs)*100:.2f}pp")

# per-day rates for eyeballing
print("\nper-day rates:")
for d in dates:
    va, sa = by_day[d]["A"]
    vb, sb = by_day[d]["B"]
    ra, rb = sa/va, sb/vb
    print(f"{d}: A={ra:.3f} ({sa}/{va})  B={rb:.3f} ({sb}/{vb})  B-A={rb-ra:+.3f}")

wins_B = sum(1 for d in dates if (by_day[d]["B"][1]/by_day[d]["B"][0]) > (by_day[d]["A"][1]/by_day[d]["A"][0]))
print(f"\ndays B > A: {wins_B}/{len(dates)}")
