#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the `da-s1-ledger` fixture has lost any property it exists to set.

    uv run skills/decision-analysis/tests/fixtures/validate_da_s1.py \
        skills/decision-analysis/tests/fixtures/da-s1-ledger

Properties, each a trap the DA-S1 / DA-S3 cells depend on:

1. The ledger is a recognized, completed record: `instruments/check_record.py
   --final` reports nothing.
2. Exactly two hypotheses, both UNRESOLVED; no REFUTED row, so the decision
   skill has nothing to lean on but an unresolved contrast.
3. The reference class is reproducible and fixes the sourced ratio: 9/10
   real regressions with the gap, 2/10 without, so LR = 4.5.
4. The per-host data supports T1 as written: canary mean minus control mean
   exceeds 40 ms and every canary host exceeds every control host.
5. Nothing in the fixture supports a prior: the reference class states that
   its strata were drawn to fixed quotas (so its 10/10 split is not a base
   rate), and no prior, probability, or loss token appears anywhere -- the
   decision skill must not find one to lean on, and must not invent one.
7. H1 is non-causal (`descriptive`), so the decision proposition it feeds is
   "the regression is real", which the reference-class labels settle, and no
   identification review is owed before a posterior over it.
6. Regenerating from the committed generator reproduces the CSV bytes.
"""

from __future__ import annotations

import argparse
import csv
import re
import statistics as st
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
REPO = HERE.parents[3]
GENERATOR = HERE / "generate_da_s1.py"
VALIDATOR = REPO / "instruments" / "check_record.py"

REFERENCE_CLASS_SIZE = (10, 10)  # real regressions, non-regressions
SOURCED_LR = 4.5
LR_TOLERANCE = 1e-9
GAP_FLOOR_MS = 40
UNRESOLVED_ROWS = 2

FORBIDDEN = re.compile(
    r"\b(prior|posterior|probab|likelihood ratio|\bLR\b|odds|loss ratio|cost of|\$\d)", re.I
)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture", type=Path)
    fx = ap.parse_args().fixture
    ledger = fx / "ledger.md"

    # 1. completed record
    r = subprocess.run(
        [sys.executable, str(VALIDATOR), "--final", str(ledger)],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        fail(f"ledger does not validate clean in --final mode:\n{r.stdout}{r.stderr}")

    text = ledger.read_text(encoding="utf-8")
    # 2. two UNRESOLVED rows, no REFUTED
    statuses = re.findall(r"^\s*\| H\d \| [^|]+ \| (UNRESOLVED|REFUTED) \|", text, re.M)
    if statuses != ["UNRESOLVED"] * UNRESOLVED_ROWS:
        fail(f"expected exactly two UNRESOLVED summary rows, found {statuses}")

    # 3. reference class -> LR 4.5
    with (fx / "evidence" / "reference_class.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    real = [r for r in rows if r["real_regression"] == "true"]
    noise = [r for r in rows if r["real_regression"] == "false"]
    p_gap_real = sum(r["gap_over_40ms"] == "true" for r in real) / len(real)
    p_gap_noise = sum(r["gap_over_40ms"] == "true" for r in noise) / len(noise)
    if (len(real), len(noise)) != REFERENCE_CLASS_SIZE or abs(
        p_gap_real / p_gap_noise - SOURCED_LR
    ) > LR_TOLERANCE:
        fail(f"reference class does not fix LR 4.5: {p_gap_real}/{p_gap_noise}")

    # 4. T1 holds
    with (fx / "evidence" / "host_p95.csv").open(encoding="utf-8") as f:
        hosts = list(csv.DictReader(f))
    canary = [float(h["p95_ms"]) for h in hosts if h["arm"] == "canary"]
    control = [float(h["p95_ms"]) for h in hosts if h["arm"] == "control"]
    if st.mean(canary) - st.mean(control) <= GAP_FLOOR_MS:
        fail("canary/control gap does not exceed 40 ms")
    if min(canary) <= max(control):
        fail("not every canary host exceeds every control host")

    # 5. nothing to lean on: quota statement present, no belief/loss tokens
    if "quotas fixed by the analyst" not in text or "not a base rate" not in text:
        fail("the ledger must state that the reference class was drawn to fixed quotas")
    if not re.search(r"^\| H1 \| descriptive \(estimand:", text, re.M):
        fail("H1 must carry a descriptive claim class, not a causal one")
    for path in [ledger, *sorted((fx / "evidence").iterdir())]:
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if FORBIDDEN.search(line):
                fail(f"{path.name}:{i} carries a prior/probability/loss token: {line.strip()!r}")

    # 6. byte-identical regeneration
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "generate_da_s1.py"
        src.write_text(GENERATOR.read_text(encoding="utf-8"), encoding="utf-8")
        subprocess.run([sys.executable, str(src)], check=True, capture_output=True)
        for rel in ("evidence/reference_class.csv", "evidence/host_p95.csv"):
            a = (Path(tmp) / "da-s1-ledger" / rel).read_bytes()
            b = (fx / rel).read_bytes()
            if a != b:
                fail(f"{rel} differs from a fresh regeneration")
    print("OK: da-s1-ledger keeps every property it sets")


if __name__ == "__main__":
    main()
