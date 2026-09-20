#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate the s22-cheap-route-validity fixture (issue #38).

Scenario 22 asks whether a claim adjudicated on `mini`, or a figure reported on
`direct`, is computed on the right rows. S11's fixture is one clean table and
cannot fail that way, so each packet here plants one fault on which the answer
turns, and nothing else:

  a-fanout/     `accounts.csv` is a version-history table: several Enterprise
                accounts carry more than one row per `account_id` (a region or
                owner reassignment, each with its own `valid_from`). A plain
                join of orders to accounts on `account_id` repeats every order
                of those accounts once per version.
                GROUND TRUTH: Enterprise revenue for 2026 Q2 is below $1M, so
                the claim "exceeded $1M" is FALSE; the plain join reads above
                $1M and answers TRUE. `segment` never changes across an
                account's versions, so every sound way of resolving the
                history -- distinct account ids, latest version, as-of
                `order_date` -- reaches the same total, and the verdict does
                not turn on a convention the prompt leaves unstated.
                The prompt states that `orders.csv` is the complete order
                ledger, so completeness is closed and the join is the only
                live fault.

  b-truncated/  `orders.csv` is an export capped at exactly 10,000 rows. It
                opens on 2026-04-01 and stops partway through 2026-06-11, with
                orders on every day before that.
                GROUND TRUTH: the rows present sum below $1M, but they cover
                72 of the quarter's 91 days, and nothing says what an absent
                record means, so completeness is UNKNOWN. Two completions fit
                the file: nothing more was sold (below $1M), or the 19 absent
                days ran like the covered ones (past $1M even at the slowest
                covered day). The correct outcome is `NON_DISCRIMINATING` (or
                the same in words), with the observed total labelled partial.
                FALSE reads an absent record as an absent sale; TRUE rests on
                a projection.

Independently seeded, and kept out of `generate.py`, so neither this fixture
nor the ones that share that file's RNG stream can shift the other.

Run from the repo root:

    uv run skills/hypothesis-driven-analysis/tests/fixtures/generate_s22.py
"""

from __future__ import annotations

import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "s22-cheap-route-validity"

SEED_FANOUT = 20260920
SEED_TRUNCATED = 20260921

SEGMENTS = (("Enterprise", 24), ("Mid-Market", 20), ("SMB", 16))
REGIONS = ("AMER", "EMEA", "APAC")
OWNERS = ("j.alvarez", "m.okafor", "s.lindqvist", "r.banerjee", "t.nakamura", "c.moreau")

# Enterprise accounts (by ordinal within the segment) that carry extra versions,
# and how many rows each has in all. One triple-version account is included so
# "the inflation is exactly 2x" is not a shortcut to the truth.
ENTERPRISE_VERSIONS = {2: 2, 5: 2, 9: 3, 12: 2, 17: 2, 21: 2}
# Non-Enterprise accounts with history too, so versioning is not a segment tell.
OTHER_VERSIONS = {"Mid-Market": {3: 2, 11: 2}, "SMB": {6: 2}}

H1_START = date(2026, 1, 1)
H1_END = date(2026, 6, 30)

EXPORT_ROW_CAP = 10_000
Q2_START = datetime(2026, 4, 1)


def _write(path: Path, header: list[str], rows: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="\n", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {path.relative_to(HERE)} ({len(rows)} rows)")


def build_fanout(outdir: Path) -> None:
    rng = random.Random(SEED_FANOUT)
    accounts: list[list] = []
    ids_by_segment: dict[str, list[str]] = {}
    n = 0
    for segment, count in SEGMENTS:
        versions = ENTERPRISE_VERSIONS if segment == "Enterprise" else OTHER_VERSIONS[segment]
        for ordinal in range(count):
            n += 1
            account_id = f"A{1000 + n}"
            ids_by_segment.setdefault(segment, []).append(account_id)
            name = f"{segment.split('-')[0]} Account {n:02d}"
            valid_from = date(2024, 1, 1) + timedelta(days=rng.randrange(0, 600))
            for _ in range(versions.get(ordinal, 1)):
                accounts.append(
                    [
                        account_id,
                        name,
                        segment,
                        rng.choice(REGIONS),
                        rng.choice(OWNERS),
                        valid_from.isoformat(),
                    ]
                )
                # Later versions take effect during H1 2026, some inside Q2.
                valid_from = date(2026, 1, 15) + timedelta(days=rng.randrange(0, 150))
    # A history table is not grouped by key in the wild; interleave the versions.
    accounts.sort(key=lambda r: (r[5], r[0]))
    _write(
        outdir / "accounts.csv",
        ["account_id", "account_name", "segment", "region", "account_owner", "valid_from"],
        accounts,
    )

    typical = {"Enterprise": 4400.0, "Mid-Market": 1500.0, "SMB": 420.0}
    per_day = {"Enterprise": (1, 3), "Mid-Market": (2, 5), "SMB": (3, 8)}
    orders: list[list] = []
    seq = 0
    day = H1_START
    while day <= H1_END:
        for segment, _ in SEGMENTS:
            lo, hi = per_day[segment]
            for _ in range(rng.randint(lo, hi)):
                seq += 1
                amount = round(typical[segment] * rng.lognormvariate(0.0, 0.35), 2)
                orders.append(
                    [
                        f"O{200000 + seq}",
                        day.isoformat(),
                        rng.choice(ids_by_segment[segment]),
                        f"{amount:.2f}",
                    ]
                )
        day += timedelta(days=1)
    _write(outdir / "orders.csv", ["order_id", "order_date", "account_id", "amount_usd"], orders)


def build_truncated(outdir: Path) -> None:
    rng = random.Random(SEED_TRUNCATED)
    rows: list[list] = []
    seq = 0
    day = Q2_START
    while len(rows) < EXPORT_ROW_CAP:
        n_orders = rng.randint(128, 152)
        minutes = sorted(rng.randrange(0, 24 * 60) for _ in range(n_orders))
        for m in minutes:
            if len(rows) == EXPORT_ROW_CAP:
                break
            seq += 1
            amount = round(76.0 * rng.lognormvariate(0.0, 0.5), 2)
            rows.append(
                [
                    f"O{500000 + seq}",
                    (day + timedelta(minutes=m)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    f"C{rng.randrange(1, 4200):05d}",
                    f"{amount:.2f}",
                ]
            )
        day += timedelta(days=1)
    _write(outdir / "orders.csv", ["order_id", "order_ts", "customer_id", "amount_usd"], rows)


def main() -> None:
    build_fanout(OUT / "a-fanout")
    build_truncated(OUT / "b-truncated")


if __name__ == "__main__":
    main()
