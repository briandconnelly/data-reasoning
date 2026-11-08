import random, math

LR = (9 / 10) / (2 / 10)
print("LR", LR)
for po in (1 / 50, 1 / 20, 1 / 10, 1 / 5):
    post = po * LR
    print(f"prior 1:{1 / po:.0f} -> post odds {post:.3f} p={post / (1 + post):.3f}")
for po in (1 / 50, 1 / 10, 1 / 5):
    print(round(po, 3), [("hold" if k * po * LR > 1 else "ship") for k in (2, 5, 10, 20)])
random.seed(0)
n = 200000
h = 0
for _ in range(n):
    po = 10 ** random.uniform(math.log10(1 / 50), math.log10(1 / 5))
    k = 10 ** random.uniform(math.log10(2), math.log10(20))
    h += k * po * LR > 1
print("hold frac", h / n)
