#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the `b10-entity` fixture has lost any property B10 depends on.

    uv run skills/exploratory-data-analysis/tests/fixtures/validate_b10.py \
        skills/exploratory-data-analysis/tests/fixtures/b10-entity

1. The entity resolves to exactly two ids, with a rename recorded in
   accounts.csv, and other accounts share every file (the entity is a subset).
2. The entity has no billing and no ticket rows in exactly two months.
3. contract_status.csv covers exactly one of those months (as `paused`) and
   is silent about the other, for every account.
4. plan_changes.csv dates exactly one change for the entity; billing's first
   month on the new plan is that effective month, and billed volume drops by
   more than 30% exactly one month later.
5. Every other account has a billing row in every month.
6. Regenerating from the committed generator reproduces the bytes.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
GENERATOR = HERE / "generate_b10.py"
MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]
ENTITY_IDS = 2
EMPTY_MONTHS = 2
MIN_OTHER_ACCOUNTS = 2
DROP_FRACTION = 0.7


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:  # noqa: PLR0912, PLR0915 -- one linear pass per fixture property
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture", type=Path)
    fx = ap.parse_args().fixture
    accounts = read(fx / "accounts.csv")
    billing = read(fx / "billing.csv")
    tickets = read(fx / "tickets.csv")
    contract = read(fx / "contract_status.csv")
    changes = read(fx / "plan_changes.csv")

    entity_ids = [a["account_id"] for a in accounts if "Northgate" in a["account_name"]]
    if len(entity_ids) != ENTITY_IDS:
        fail(f"entity should resolve to two ids, found {entity_ids}")
    # On a resolved row, not on any account: an unrelated account carrying the
    # word would otherwise stand in for the entity's own rename marker.
    if not any("formerly" in a["account_name"] for a in accounts if a["account_id"] in entity_ids):
        fail("rename is not recorded on either Northgate row in accounts.csv")
    others = [a["account_id"] for a in accounts if a["account_id"] not in entity_ids]
    if len(others) < MIN_OTHER_ACCOUNTS:
        fail("the entity must be a subset: need at least two other accounts")
    # Property 1's "other accounts share every file": without this, stripping
    # every non-Northgate row from tickets, contract_status or plan_changes
    # would leave the entity as the whole table and B10's subset control gone.
    for name, table in (
        ("tickets.csv", tickets),
        ("contract_status.csv", contract),
        ("plan_changes.csv", changes),
    ):
        if not any(r["account_id"] in others for r in table):
            fail(f"the entity must be a subset: {name} carries no other account")

    ent_bill = [b for b in billing if b["account_id"] in entity_ids]
    ent_tix = [t for t in tickets if t["account_id"] in entity_ids]
    bill_months = {b["month"] for b in ent_bill}
    tix_months = {t["opened"][:7] for t in ent_tix}
    empty = [m for m in MONTHS if m not in bill_months and m not in tix_months]
    if len(empty) != EMPTY_MONTHS:
        fail(f"entity should have exactly two empty months, found {empty}")

    covered = {c["month"] for c in contract if c["account_id"] in entity_ids}
    covered_empty = [m for m in empty if m in covered]
    if len(covered_empty) != 1:
        fail(f"contract_status should cover exactly one empty month, covers {covered_empty}")
    if not any(
        c["status"] == "paused" and c["month"] == covered_empty[0]
        for c in contract
        if c["account_id"] in entity_ids
    ):
        fail("the covered empty month is not recorded as paused")
    silent = next(m for m in empty if m not in covered)
    if any(c["month"] == silent for c in contract):
        fail(f"contract_status must be silent about {silent} for every account")

    by_month = {b["month"]: b for b in ent_bill}
    ent_changes = [c for c in changes if c["account_id"] in entity_ids]
    if len(ent_changes) != 1:
        fail(f"plan_changes.csv should date exactly one entity change, found {len(ent_changes)}")
    change_m = ent_changes[0]["effective_date"][:7]
    first_new = next(
        (m for m in MONTHS if m in by_month and by_month[m]["plan"] == ent_changes[0]["to_plan"]),
        None,
    )
    if first_new != change_m:
        fail(
            f"billing's first {ent_changes[0]['to_plan']} month {first_new} is not the dated "
            f"change month {change_m}"
        )
    later = [m for m in MONTHS if m in by_month and m > change_m]
    if not later:
        fail("no billed month after the plan change")
    drop_m = later[0]
    before = int(by_month[change_m]["billed_volume"])
    after = int(by_month[drop_m]["billed_volume"])
    if MONTHS.index(drop_m) - MONTHS.index(change_m) != 1 or after >= DROP_FRACTION * before:
        fail(
            "volume must drop >30% exactly one month after the plan change: "
            f"{change_m}={before}, {drop_m}={after}"
        )

    for acc in others:
        months = {b["month"] for b in billing if b["account_id"] == acc}
        if months != set(MONTHS):
            fail(f"{acc} is missing billing months {set(MONTHS) - months}")

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "generate_b10.py"
        src.write_text(GENERATOR.read_text(encoding="utf-8"), encoding="utf-8")
        subprocess.run([sys.executable, str(src)], check=True, capture_output=True)
        for p in sorted((Path(tmp) / "b10-entity").iterdir()):
            if p.read_bytes() != (fx / p.name).read_bytes():
                fail(f"{p.name} differs from a fresh regeneration")
    print("OK: b10-entity keeps every property it sets")


if __name__ == "__main__":
    main()
