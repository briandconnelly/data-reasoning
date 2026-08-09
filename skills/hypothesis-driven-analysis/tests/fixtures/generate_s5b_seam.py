#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate the s5b-seam fixture: the E1 seam scenario and the S5 replacement.

Deliberately a separate script from `generate.py`, with its own RNG instance.

`generate.py` drives every legacy fixture from one module-level `RNG`, in the
call order fixed by its `main()`. Anything drawing from that stream inherits a
dependency on every builder ahead of it: an edit to S1 would silently change
this fixture's bytes, and archived runs pin fixture digests. The same repo
already learned this once -- S6 burns its 41 historical global draws unchanged
"so downstream fixtures that share RNG (s9, s15) stay byte-identical", and
samples new data from a scenario-local RNG. This file takes the local-RNG half
of that lesson and skips the coupling entirely.

Run from the repo root:

    uv run skills/hypothesis-driven-analysis/tests/fixtures/generate_s5b_seam.py

The ground truth it plants is documented in `s5b-seam-ground-truth.md` --
deliberately outside the `s5b-seam/` directory the arms are handed, which the
validator requires to hold `events.csv` alone -- and preregistered as scenario
E1 in `skills/exploratory-data-analysis/tests/scenarios.md`.
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).parent
OUTDIR = HERE / "s5b-seam"

SEED = 20260809
"""Fixture-local seed. Independent of generate.py's stream by construction."""

N_DRAWS = 7000
"""Events drawn before the coverage hole removes any; the file carries fewer."""

START = date(2026, 5, 1)
DAYS = 61
"""2026-05-01 through 2026-06-30 inclusive."""

DISCOVERY_DAYS = 46
"""Days 0-45 (05-01..06-15) — the window A3's prompt quarantines looks to."""

RESERVE_MIN, RESERVE_MAX = 7, 21
"""Admissible reserve family: any window ending on the final day, this long."""

REGIONS = (("na", 0.45), ("eu", 0.32), ("apac", 0.23))
PLANS = (("starter", 0.45), ("growth", 0.30), ("enterprise", 0.25))
ENDPOINTS = (("/search", 0.35), ("/export", 0.34), ("/ingest", 0.21), ("/report", 0.10))

VERSIONS = (
    # (name, share on day 0, share on the last day). Versions drift the way
    # real ones do -- old builds decline, new ones climb -- so the export does
    # not read as synthetic. The affected version sits on a flat plateau across
    # the whole window, which keeps T's cell the same size wherever an arm
    # puts its reserve.
    ("3.9.4", 0.09, 0.02),
    ("4.0.1", 0.11, 0.03),
    ("4.0.7", 0.12, 0.05),
    ("4.1.2", 0.14, 0.09),
    ("4.1.9", 0.21, 0.21),
    ("4.2.0", 0.13, 0.15),
    ("4.2.3", 0.17, 0.17),
    ("4.3.1", 0.03, 0.17),
    ("4.4.0", 0.00, 0.11),
)
"""Nine versions. The affected one (4.2.3) is neither the newest nor the oldest,
and its window-wide count sits mid-pack -- the validator fails if either stops
holding, because nothing may distinguish it before a relationship is inspected."""

N_ACCOUNTS = 420
"""Accounts carry a FIXED plan and region, assigned once here.

An earlier revision drew both per event, which left 882 of 899 accounts holding
several plans at once. A canary arm caught it, and correctly downgraded the
decoy to a possible labelling artifact on the strength of it: `enterprise` was
not a cohort, so an `enterprise`-shaped pattern meant little."""

SATURDAY = 5
"""`date.weekday()` numbers Monday 0; Saturday and Sunday are 5 and 6."""

WEEKEND_WEIGHT = 0.55
"""Saturday and Sunday carry a little over half a weekday's traffic. Without
this the daily volume is flat, which a canary arm read as a sign the export was
synthetic."""

BASE_ERROR = 0.03

T_ENDPOINT, T_VERSION, T_LIFT = "/export", "4.2.3", 0.20
"""The true lead: constant across all 61 days, so it reproduces in whatever
late window an arm reserves rather than one the fixture presumes."""

D_PLAN, D_ENDPOINT, D_PEAK, D_ZERO_DAY = "enterprise", "/search", 0.18, 40
"""The decoy: decays linearly to zero by day 40 (06-10). A decay rather than a
step means no boundary in the data coincides with one an arm might pick."""

HOLE_DAYS = (13, 14, 15)
"""05-14..05-16: every apac row is absent, with no independent denominator
anywhere in the directory, so absence semantics can only be UNKNOWN."""

HOLE_REGION = "apac"

FIELDS = (
    "event_id",
    "ts",
    "account_id",
    "plan",
    "region",
    "endpoint",
    "client_version",
    "status",
)


def _pick(rng: random.Random, table) -> str:
    r = rng.random()
    acc = 0.0
    for row in table:
        acc += row[1]
        if r < acc:
            return row[0]
    return table[-1][0]


def _version_table(day: int):
    """Version shares for one day, interpolated between the endpoints."""
    frac = day / (DAYS - 1)
    weights = [(name, lo + (hi - lo) * frac) for name, lo, hi in VERSIONS]
    total = sum(w for _, w in weights)
    return [(name, w / total) for name, w in weights]


def _day_weights() -> list[float]:
    """Weekday/weekend traffic shape, so daily volume is not flat."""
    weights = []
    for day in range(DAYS):
        stamp = START + timedelta(days=day)
        weights.append(WEEKEND_WEIGHT if stamp.weekday() >= SATURDAY else 1.0)
    return weights


def _accounts(rng: random.Random) -> list[dict]:
    """One fixed plan and region per account, drawn once."""
    return [
        {
            "account_id": f"a{100 + i}",
            "plan": _pick(rng, PLANS),
            "region": _pick(rng, REGIONS),
        }
        for i in range(N_ACCOUNTS)
    ]


def _error_probability(day: int, plan: str, endpoint: str, version: str) -> float:
    p = BASE_ERROR
    if endpoint == T_ENDPOINT and version == T_VERSION:
        p += T_LIFT
    if plan == D_PLAN and endpoint == D_ENDPOINT and day < D_ZERO_DAY:
        p += D_PEAK * (1 - day / D_ZERO_DAY)
    return p


def build(outdir: Path) -> None:
    rng = random.Random(SEED)
    accounts = _accounts(rng)
    days = list(range(DAYS))
    weights = _day_weights()

    rows = []
    for _ in range(N_DRAWS):
        day = rng.choices(days, weights=weights, k=1)[0]
        account = accounts[rng.randrange(N_ACCOUNTS)]
        endpoint = _pick(rng, ENDPOINTS)
        version = _pick(rng, _version_table(day))
        hour, minute = rng.randrange(24), rng.randrange(60)
        roll = rng.random()

        # The coverage hole. Drawn after every field so removing a row never
        # shifts the stream for the rows that survive.
        if day in HOLE_DAYS and account["region"] == HOLE_REGION:
            continue

        probability = _error_probability(day, account["plan"], endpoint, version)
        stamp = START + timedelta(days=day)
        rows.append(
            {
                "ts": f"{stamp.isoformat()}T{hour:02d}:{minute:02d}Z",
                "account_id": account["account_id"],
                "plan": account["plan"],
                "region": account["region"],
                "endpoint": endpoint,
                "client_version": version,
                "status": "error" if roll < probability else "ok",
            }
        )

    # Ids are assigned HERE, after the hole, so the sequence is gapless.
    #
    # An earlier revision numbered rows by loop index and skipped some, leaving
    # 82 absent ids. A canary arm found them, read them as ~1.2% uniform
    # per-record dropout, and never noticed the regional hole that actually
    # caused them -- the fixture was handing out a louder, wrong mechanism than
    # the one it meant to plant.
    rows.sort(key=lambda row: row["ts"])
    for index, row in enumerate(rows):
        row["event_id"] = f"e{index:05d}"

    outdir.mkdir(parents=True, exist_ok=True)
    with (outdir / "events.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    build(OUTDIR)


if __name__ == "__main__":
    main()
