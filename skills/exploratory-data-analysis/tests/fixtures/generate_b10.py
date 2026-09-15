#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate the `b10-entity` fixture for the B10 entity-profile scenario.

Four accounts across 2026-01..2026-06 in a billing table and a ticket table
keyed on `account_id`, so the named entity is a subset of every file. The
entity, Northgate Clinic, resolves to two ids: `ACC-1042` through March and
`ACC-1077` from April, after a rename to "Northgate Health Partners" recorded
in `accounts.csv`. It has no billing or ticket rows in February and in June.
`contract_status.csv` covers February (status `paused`) and says nothing about
June, so one hole is genuine inactivity on independent evidence and the other
is UNKNOWN. Its plan changes from `standard` to `enterprise-annual` in March
and its billed volume drops in April -- the causal story the fixture invites
and does not support. Deterministic from a fixed seed on this module's own
`random.Random`. Run from the repo root:

    uv run skills/exploratory-data-analysis/tests/fixtures/generate_b10.py
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "b10-entity"
RNG = random.Random(20260915)

DECEMBER = 12
MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]
ENTITY_IDS = {"ACC-1042": MONTHS[:3], "ACC-1077": MONTHS[3:]}
ENTITY_EMPTY_MONTHS = {"2026-02", "2026-06"}
ENTITY_PLAN = {
    "2026-01": "standard",
    "2026-03": "enterprise-annual",
    "2026-04": "enterprise-annual",
    "2026-05": "enterprise-annual",
}
ENTITY_VOLUME = {"2026-01": 1840, "2026-03": 1910, "2026-04": 1120, "2026-05": 1085}
ENTITY_RATE = {"standard": 0.42, "enterprise-annual": 0.31}

OTHER_ACCOUNTS = {
    "ACC-1003": ("Riverbend Dental", "standard", 900),
    "ACC-1019": ("Summit Orthopedics", "enterprise-annual", 2600),
    "ACC-1058": ("Pinecrest Family Practice", "standard", 1300),
}
TICKET_CATEGORIES = ["billing-question", "integration", "outage-report", "feature-request"]


def month_days(ym: str) -> list[date]:
    y, m = (int(x) for x in ym.split("-"))
    first = date(y, m, 1)
    nxt = date(y + (m == DECEMBER), m % DECEMBER + 1, 1)
    return [first + timedelta(days=i) for i in range((nxt - first).days)]


def billing() -> list[dict[str, str]]:
    rows = []
    for acc_id, (_, plan, base) in OTHER_ACCOUNTS.items():
        for ym in MONTHS:
            vol = int(base * RNG.uniform(0.92, 1.08))
            rows.append(
                {
                    "account_id": acc_id,
                    "month": ym,
                    "plan": plan,
                    "billed_volume": str(vol),
                    "amount_usd": f"{vol * ENTITY_RATE[plan]:.2f}",
                }
            )
    for acc_id, months in ENTITY_IDS.items():
        for ym in months:
            if ym in ENTITY_EMPTY_MONTHS:
                continue
            plan = ENTITY_PLAN[ym]
            vol = ENTITY_VOLUME[ym]
            rows.append(
                {
                    "account_id": acc_id,
                    "month": ym,
                    "plan": plan,
                    "billed_volume": str(vol),
                    "amount_usd": f"{vol * ENTITY_RATE[plan]:.2f}",
                }
            )
    rows.sort(key=lambda r: (r["month"], r["account_id"]))
    return rows


def tickets() -> list[dict[str, str]]:
    rows = []
    n = 0
    for acc_id in OTHER_ACCOUNTS:
        for ym in MONTHS:
            for _ in range(RNG.randint(1, 3)):
                n += 1
                d = RNG.choice(month_days(ym))
                rows.append(
                    {
                        "ticket_id": f"T-{5000 + n}",
                        "account_id": acc_id,
                        "opened": d.isoformat(),
                        "category": RNG.choice(TICKET_CATEGORIES),
                    }
                )
    for acc_id, months in ENTITY_IDS.items():
        for ym in months:
            if ym in ENTITY_EMPTY_MONTHS:
                continue
            for _ in range(RNG.randint(1, 2)):
                n += 1
                d = RNG.choice(month_days(ym))
                cat = "billing-question" if ym == "2026-04" else RNG.choice(TICKET_CATEGORIES)
                rows.append(
                    {
                        "ticket_id": f"T-{5000 + n}",
                        "account_id": acc_id,
                        "opened": d.isoformat(),
                        "category": cat,
                    }
                )
    rows.sort(key=lambda r: (r["opened"], r["ticket_id"]))
    return rows


def accounts() -> list[dict[str, str]]:
    rows = [
        {"account_id": acc_id, "account_name": name, "valid_from": "2025-01-01", "valid_to": ""}
        for acc_id, (name, _, _) in OTHER_ACCOUNTS.items()
    ]
    rows.append(
        {
            "account_id": "ACC-1042",
            "account_name": "Northgate Clinic",
            "valid_from": "2025-01-01",
            "valid_to": "2026-03-31",
        }
    )
    rows.append(
        {
            "account_id": "ACC-1077",
            "account_name": "Northgate Health Partners (formerly Northgate Clinic)",
            "valid_from": "2026-04-01",
            "valid_to": "",
        }
    )
    rows.sort(key=lambda r: r["account_id"])
    return rows


def contract_status() -> list[dict[str, str]]:
    # Independent source: covers Jan-May for every account, silent about June.
    rows = []
    for ym in MONTHS[:5]:
        for acc_id in OTHER_ACCOUNTS:
            rows.append({"account_id": acc_id, "month": ym, "status": "active"})
        for acc_id, months in ENTITY_IDS.items():
            if ym in months:
                status = "paused" if ym == "2026-02" else "active"
                rows.append({"account_id": acc_id, "month": ym, "status": status})
    rows.sort(key=lambda r: (r["month"], r["account_id"]))
    return rows


def write(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    write(billing(), OUT / "billing.csv")
    write(tickets(), OUT / "tickets.csv")
    write(accounts(), OUT / "accounts.csv")
    write(contract_status(), OUT / "contract_status.csv")
    (OUT / "README.md").write_text(
        "Account data extract, 2026-01 through 2026-06.\n"
        "billing.csv: one row per account per billed month. tickets.csv: support tickets.\n"
        "accounts.csv: account ids and names with validity windows.\n"
        "contract_status.csv: monthly contract status from the contracts system.\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
