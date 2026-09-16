#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate the evidence files of the `da-s1-ledger` fixture.

The fixture is a completed hypothesis-driven-analysis ledger (`ledger.md`,
committed prose) that ends with two UNRESOLVED rows, one of whose evidence
pointers is a reproducible reference class an analyst can turn into a sourced
likelihood ratio, and nothing anywhere that states a prior or a loss. This
script writes the two CSVs the ledger cites; `validate_da_s1.py` holds the
ledger and the CSVs to the properties the cells depend on.

The fixture serves DA-S1 (prompt supplies losses) and DA-S3 (prompt supplies
none). Both reach `decision-analysis`'s no-supported-prior degraded mode; the
sourced ratio is what that mode must keep. Deterministic from a fixed seed on
this module's own `random.Random`. Run from the repo root:

    uv run skills/decision-analysis/tests/fixtures/generate_da_s1.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "da-s1-ledger"
RNG = random.Random(20260915)

# Reference class: 20 past canary rollouts where a p95 gap was observed between
# canary and control hosts. `real_regression` is what the post-mortem settled;
# `gap_over_40ms` is the observable this incident shares. The counts below fix
# the sourced ratio: P(gap | real) = 9/10, P(gap | not real) = 2/10, LR = 4.5.
REAL_WITH_GAP = 9
REAL_TOTAL = 10
NOISE_WITH_GAP = 2
NOISE_TOTAL = 10

# Per-host p95 on the incident day: canary hosts run the new pool config.
CANARY_HOSTS = 6
CONTROL_HOSTS = 6
CANARY_P95_MEAN = 468.0
CONTROL_P95_MEAN = 411.0
P95_SD = 14.0


def reference_class() -> list[dict[str, str]]:
    rows = []
    real = [True] * REAL_WITH_GAP + [False] * (REAL_TOTAL - REAL_WITH_GAP)
    noise = [True] * NOISE_WITH_GAP + [False] * (NOISE_TOTAL - NOISE_WITH_GAP)
    RNG.shuffle(real)
    RNG.shuffle(noise)
    incidents = [(True, g) for g in real] + [(False, g) for g in noise]
    RNG.shuffle(incidents)
    for i, (is_real, gap) in enumerate(incidents, 1):
        rows.append(
            {
                "incident_id": f"INC-{2400 + i}",
                "quarter": f"2025-Q{1 + (i - 1) % 4}",
                "real_regression": "true" if is_real else "false",
                "gap_over_40ms": "true" if gap else "false",
            }
        )
    return rows


def host_p95() -> list[dict[str, str]]:
    rows = []
    for i in range(1, CANARY_HOSTS + 1):
        rows.append(
            {
                "host": f"api-canary-{i:02d}",
                "arm": "canary",
                "p95_ms": f"{RNG.gauss(CANARY_P95_MEAN, P95_SD):.1f}",
            }
        )
    for i in range(1, CONTROL_HOSTS + 1):
        rows.append(
            {
                "host": f"api-ctl-{i:02d}",
                "arm": "control",
                "p95_ms": f"{RNG.gauss(CONTROL_P95_MEAN, P95_SD):.1f}",
            }
        )
    return rows


def write(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    write(reference_class(), OUT / "evidence" / "reference_class.csv")
    write(host_p95(), OUT / "evidence" / "host_p95.csv")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
