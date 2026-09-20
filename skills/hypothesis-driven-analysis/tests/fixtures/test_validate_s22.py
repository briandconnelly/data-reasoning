#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest"]
# ///
"""Known-positive probes for `validate_s22.py`.

A validator that passes and a validator that cannot fail look identical from the
outside, so each probe below breaks one property the s22 fixture exists to set
and asserts the validator names it. The committed fixture passing is the control.

Run: uv run skills/hypothesis-driven-analysis/tests/fixtures/test_validate_s22.py
"""

from __future__ import annotations

import csv
import shutil
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from validate_s22 import validate  # noqa: E402 -- path set up above

FIXTURE = HERE / "s22-cheap-route-validity"
Rows = list[dict[str, str]]


def _rewrite(path: Path, mutate: Callable[[Rows], Rows]) -> None:
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    header = list(rows[0])
    rows = mutate(rows)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=header, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def _dedupe_accounts(rows: Rows) -> Rows:
    first = {r["account_id"]: r for r in reversed(rows)}
    return list(first.values())


def _drift_segment(rows: Rows) -> Rows:
    first: dict[str, dict[str, str]] = {}
    for r in rows:
        if r["account_id"] in first and r["segment"] == "Enterprise":
            r["segment"] = "Mid-Market"
            break
        first.setdefault(r["account_id"], r)
    return rows


def _shrink_enterprise(rows: Rows) -> Rows:
    return [{**r, "amount_usd": f"{float(r['amount_usd']) * 0.8:.2f}"} for r in rows]


def _drop_a_day(day: str, column: str) -> Callable[[Rows], Rows]:
    return lambda rows: [r for r in rows if not r[column].startswith(day)]


def _drop_last_rows(rows: Rows) -> Rows:
    return rows[:-400]


def _scale(factor: float) -> Callable[[Rows], Rows]:
    return lambda rows: [
        {**r, "amount_usd": f"{float(r['amount_usd']) * factor:.2f}"} for r in rows
    ]


# (probe, packet file, mutation, a phrase the validator's message must carry)
MUTATIONS = [
    ("history deduplicated", "a-fanout/accounts.csv", _dedupe_accounts, "duplicate keys"),
    ("segment drifts across versions", "a-fanout/accounts.csv", _drift_segment, "segment changes"),
    ("inflated total falls under $1M", "a-fanout/orders.csv", _shrink_enterprise, "inflated total"),
    (
        "ledger grows a hole",
        "a-fanout/orders.csv",
        _drop_a_day("2026-05-13", "order_date"),
        "no rows on",
    ),
    ("export no longer at the row cap", "b-truncated/orders.csv", _drop_last_rows, "row cap"),
    (
        "a day missing before the cut",
        "b-truncated/orders.csv",
        _drop_a_day("2026-05-02", "order_ts"),
        "missing before the cut",
    ),
    ("partial total over $1M", "b-truncated/orders.csv", _scale(1.2), "not clearly below"),
    ("gap too wide to close", "b-truncated/orders.csv", _scale(0.8), "FALSE would be defensible"),
]


def test_committed_fixture_passes() -> None:
    assert validate(FIXTURE) == []


@pytest.mark.parametrize(
    ("name", "rel", "mutate", "phrase"), MUTATIONS, ids=[m[0] for m in MUTATIONS]
)
def test_validator_catches(tmp_path: Path, name: str, rel: str, mutate, phrase: str) -> None:
    broken = tmp_path / "fixture"
    shutil.copytree(FIXTURE, broken)
    _rewrite(broken / rel, mutate)
    errors = validate(broken)
    assert any(phrase in e for e in errors), f"{name}: validator said {errors}"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
