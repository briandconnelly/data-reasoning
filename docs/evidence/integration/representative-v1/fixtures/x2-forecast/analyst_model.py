"""Analyst's ticket model: same-weekday nearest-neighbour average."""

import csv
import random
import sys
from datetime import date


def load(path):
    with open(path, newline="") as f:
        return [(date.fromisoformat(r["date"]), int(r["tickets"])) for r in csv.DictReader(f)]


def predict(train, day, k=4):
    same = [(abs((d - day).days), y) for d, y in train if d.weekday() == day.weekday()]
    same.sort()
    return sum(y for _, y in same[:k]) / k


def main(path):
    rows = load(path)
    rng = random.Random(7)
    test = set(rng.sample(range(len(rows)), len(rows) // 5))
    train = [r for i, r in enumerate(rows) if i not in test]
    errs = [abs(predict(train, rows[i][0]) - rows[i][1]) / rows[i][1] for i in sorted(test)]
    print(f"held-out MAPE: {100 * sum(errs) / len(errs):.1f}%")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "daily_tickets.csv")
