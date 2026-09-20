#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the s22 fixture has lost any property it exists to set.

Scenario 22 scores whether a cheap-route answer was computed on the right rows.
Each packet is only a test while its one planted fault still decides the answer
and nothing else does, and the ways that stops being true are quiet:

  a-fanout
    - the account history loses its duplicate keys, so the plain join is right;
    - `segment` drifts across an account's versions, so the "true" total starts
      to depend on which version a run picks -- a convention the prompt leaves
      unstated;
    - the true and inflated totals stop straddling $1M with room to spare;
    - the order ledger grows a hole, which makes completeness a second live
      fault beside the join.
  b-truncated
    - the export stops being cut mid-day at the row cap;
    - a day goes missing before the cut, so the gap, not the cut, is the story;
    - the rows' total drifts over $1M (the claim becomes TRUE on its face), or
      so far under it that the absent days would need more than the covered
      days ever show, and FALSE becomes the defensible answer.
  c-hole
    - the hole closes, or widens to the whole file (a day with no orders at all
      is visible in a per-day count, and the packet exists to need the crossed
      day-by-region view);
    - the rows' total crosses $1M, or the gap per absent day grows past what
      EMEA's slowest covered day shows, and FALSE becomes defensible.
  The packets' correct outcomes rest on two completions both being compatible
  with the file -- nothing more was sold, or the absent days ran like the
  covered ones -- not on the cut proving the export incomplete: a source's own
  missingness pattern cannot establish its completeness either way.

`test_validate_s22.py` pins each of these as a known positive: a validator that
cannot fail is indistinguishable from a fixture that is fine.

    uv run skills/hypothesis-driven-analysis/tests/fixtures/validate_s22.py \
        skills/hypothesis-driven-analysis/tests/fixtures/s22-cheap-route-validity
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

CLAIM_USD = 1_000_000.0
Q2 = (date(2026, 4, 1), date(2026, 6, 30))
H1 = (date(2026, 1, 1), date(2026, 6, 30))

# The realized totals, to the cent: scored runs are checked against these, so a
# regenerated fixture that moves them must fail here rather than in a run record.
FANOUT_TRUE_USD = 925_797.78
FANOUT_INFLATED_USD = 1_227_245.07
TRUNCATED_PARTIAL_USD = 862_691.37
HOLE_PARTIAL_USD = 972_510.46

FANOUT_TRUE_CEILING = 960_000.0
FANOUT_INFLATED_FLOOR = 1_040_000.0
TRUNCATED_PARTIAL_CEILING = 950_000.0
TRUNCATED_PROJECTED_FLOOR = 1_030_000.0
EXPORT_ROW_CAP = 10_000
LAST_EXPORT_DAY = date(2026, 6, 11)
MIN_VERSIONED_ENTERPRISE = 3
PLAIN_DUPLICATE = 2
HOLE_REGION = "EMEA"
HOLE = (date(2026, 6, 3), date(2026, 6, 16))
HOLE_PARTIAL_CEILING = 985_000.0


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _days(start: date, end: date) -> list[date]:
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


def check_fanout(root: Path) -> list[str]:  # noqa: PLR0912 -- one flat list of properties
    errors: list[str] = []
    accounts = _rows(root / "accounts.csv")
    orders = _rows(root / "orders.csv")

    segments: dict[str, set[str]] = defaultdict(set)
    versions: dict[str, list[date]] = defaultdict(list)
    for a in accounts:
        segments[a["account_id"]].add(a["segment"])
        versions[a["account_id"]].append(date.fromisoformat(a["valid_from"]))
    drifted = sorted(k for k, v in segments.items() if len(v) > 1)
    if drifted:
        errors.append(f"a-fanout: segment changes across versions of {drifted}")
    n_versions = Counter(a["account_id"] for a in accounts)
    ent_multi = [k for k, c in n_versions.items() if c > 1 and "Enterprise" in segments[k]]
    if len(ent_multi) < MIN_VERSIONED_ENTERPRISE:
        errors.append("a-fanout: fewer than three Enterprise accounts carry duplicate keys")
    if not any(n_versions[k] > PLAIN_DUPLICATE for k in ent_multi):
        errors.append("a-fanout: no Enterprise account has more than two versions")
    if not any(c > 1 and "Enterprise" not in segments[k] for k, c in n_versions.items()):
        errors.append("a-fanout: only Enterprise accounts are versioned (a segment tell)")

    ids = [o["order_id"] for o in orders]
    if len(ids) != len(set(ids)):
        errors.append("a-fanout: order_id is not unique")
    unknown = sorted({o["account_id"] for o in orders} - set(segments))
    if unknown:
        errors.append(f"a-fanout: orders reference unknown accounts {unknown[:3]}")
    present = {date.fromisoformat(o["order_date"]) for o in orders}
    missing = [d for d in _days(*H1) if d not in present]
    if missing:
        errors.append(f"a-fanout: the order ledger has no rows on {missing[:3]}")
    if present - set(_days(*H1)):
        errors.append("a-fanout: orders fall outside H1 2026")

    true_total = inflated = as_of = 0.0
    for o in orders:
        day = date.fromisoformat(o["order_date"])
        if not (Q2[0] <= day <= Q2[1]) or "Enterprise" not in segments.get(o["account_id"], ()):
            continue
        amount = float(o["amount_usd"])
        true_total += amount
        inflated += amount * n_versions[o["account_id"]]
        # An as-of join keeps exactly one version whenever one was in force;
        # every account's first version predates H1, so it always is.
        as_of += amount * min(1, sum(1 for v in versions[o["account_id"]] if v <= day))
    if round(true_total, 2) != FANOUT_TRUE_USD:
        errors.append(f"a-fanout: true total {true_total:.2f} != documented {FANOUT_TRUE_USD}")
    if round(inflated, 2) != FANOUT_INFLATED_USD:
        errors.append(f"a-fanout: inflated total {inflated:.2f} != {FANOUT_INFLATED_USD}")
    if round(as_of, 2) != round(true_total, 2):
        errors.append("a-fanout: an as-of join no longer reaches the true total")
    if not true_total < FANOUT_TRUE_CEILING < CLAIM_USD:
        errors.append(f"a-fanout: true total {true_total:.2f} is not clearly below $1M")
    if not inflated > FANOUT_INFLATED_FLOOR > CLAIM_USD:
        errors.append(f"a-fanout: inflated total {inflated:.2f} is not clearly above $1M")
    return errors


def check_truncated(root: Path) -> list[str]:
    errors: list[str] = []
    rows = _rows(root / "orders.csv")
    if len(rows) != EXPORT_ROW_CAP:
        errors.append(f"b-truncated: {len(rows)} rows, not the {EXPORT_ROW_CAP}-row cap")
    stamps = [r["order_ts"] for r in rows]
    if stamps != sorted(stamps):
        errors.append("b-truncated: rows are not in timestamp order")
    ids = [r["order_id"] for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("b-truncated: order_id is not unique")

    daily: dict[date, float] = defaultdict(float)
    for r in rows:
        daily[date.fromisoformat(r["order_ts"][:10])] += float(r["amount_usd"])
    if not daily:
        return [*errors, "b-truncated: no rows"]
    first, last = min(daily), max(daily)
    if first != Q2[0]:
        errors.append(f"b-truncated: export opens on {first}, not {Q2[0]}")
    if last != LAST_EXPORT_DAY:
        errors.append(f"b-truncated: export ends on {last}, not {LAST_EXPORT_DAY}")
    if stamps and not stamps[-1][11:13] < "18":
        errors.append("b-truncated: the last day is not visibly cut short")
    gaps = [d for d in _days(first, last) if d not in daily]
    if gaps:
        errors.append(f"b-truncated: days missing before the cut: {gaps[:3]}")

    partial = sum(daily.values())
    if round(partial, 2) != TRUNCATED_PARTIAL_USD:
        errors.append(f"b-truncated: partial total {partial:.2f} != {TRUNCATED_PARTIAL_USD}")
    if not partial < TRUNCATED_PARTIAL_CEILING:
        errors.append(f"b-truncated: partial total {partial:.2f} is not clearly below $1M")
    full_days = [v for d, v in daily.items() if d != last]
    missing_days = (Q2[1] - last).days
    # One compatible completion, not a lower bound: the slowest covered day
    # repeated over the absent days. It must clear $1M for FALSE to be unsafe.
    projected = partial + missing_days * min(full_days, default=0.0)
    if not projected > TRUNCATED_PROJECTED_FLOOR:
        errors.append(
            f"b-truncated: even the slowest day repeated gives {projected:.2f}; "
            "FALSE would be defensible"
        )
    return errors


def check_hole(root: Path) -> list[str]:
    errors: list[str] = []
    rows = _rows(root / "orders.csv")
    by_day: dict[date, float] = defaultdict(float)
    by_cell: dict[tuple[date, str], float] = defaultdict(float)
    for r in rows:
        day = date.fromisoformat(r["order_ts"][:10])
        by_day[day] += float(r["amount_usd"])
        by_cell[(day, r["region"])] += float(r["amount_usd"])
    regions = {region for _, region in by_cell}
    empty_days = [d for d in _days(*Q2) if d not in by_day]
    if empty_days:
        errors.append(f"c-hole: days with no orders at all: {empty_days[:3]}")
    absent = sorted((d, g) for d in _days(*Q2) for g in regions if (d, g) not in by_cell)
    expected = [(d, HOLE_REGION) for d in _days(*HOLE)]
    if absent != expected:
        errors.append(f"c-hole: absent day-by-region cells are not the planted hole: {absent[:3]}")

    partial = sum(by_day.values())
    if round(partial, 2) != HOLE_PARTIAL_USD:
        errors.append(f"c-hole: partial total {partial:.2f} != {HOLE_PARTIAL_USD}")
    if not partial < HOLE_PARTIAL_CEILING:
        errors.append(f"c-hole: partial total {partial:.2f} is not clearly below $1M")
    covered = [v for (_, g), v in by_cell.items() if g == HOLE_REGION]
    needed = (CLAIM_USD - partial) / len(expected)
    # One compatible completion, not a lower bound: the absent cells at the
    # region's slowest covered day. It must clear the gap for FALSE to be unsafe.
    if not covered or not min(covered) > needed * 1.2:
        errors.append(
            f"c-hole: the hole needs {needed:.2f} a day, not clearly under the slowest "
            "covered day; FALSE would be defensible"
        )
    return errors


def validate(root: Path) -> list[str]:
    return [
        *check_fanout(root / "a-fanout"),
        *check_truncated(root / "b-truncated"),
        *check_hole(root / "c-hole"),
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture", type=Path)
    errors = validate(ap.parse_args().fixture)
    for e in errors:
        print(f"FAIL {e}", file=sys.stderr)
    if not errors:
        print("s22 fixture: every planted property holds")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
