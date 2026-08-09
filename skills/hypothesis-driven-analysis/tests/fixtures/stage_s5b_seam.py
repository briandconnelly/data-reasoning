#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Stage the s5b-seam fixture for an arm, outside the repo and under a neutral name.

Never hand an arm the fixture in place. Two canary arms showed why:

- One ran `git status` at the end of its work and saw `s5b-seam-ground-truth.md`
  and `generate_s5b_seam.py` in the listing. It did not open them, and said so --
  but the filenames alone announce that the data is a seeded fixture, and
  `s5b-seam` names the scenario. That is the defect that invalidated the original
  Scenario 5, one level up from the data.
- The other was told in its prompt to confine its looks to a date window. Its
  orientation coverage check spanned the whole file, because that is what a
  coverage check does, and it touched held-out timestamps before its plan
  existed. A quarantine an honest agent breaks by following the skill correctly
  is a harness defect, not an arm defect.

So: copy the data to a neutral directory outside the repo, and for the arm that
needs a quarantine, enforce it by withholding the rows rather than by asking.

    uv run .../stage_s5b_seam.py --arm a1 --into /tmp/run-42
    uv run .../stage_s5b_seam.py --arm a3 --into /tmp/run-42
    uv run .../stage_s5b_seam.py --release-holdout --into /tmp/run-42

`--arm a1` stages the whole export: that arm chooses its own reservation, so it
must be able to see everything. `--arm a3` stages the discovery window only and
parks the held-out rows out of reach until `--release-holdout` is called, which
is the point at which the arm's retrospective predictions are already on disk.
"""

from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path

HERE = Path(__file__).parent
SOURCE = HERE / "s5b-seam" / "events.csv"

STAGED_DIRNAME = "api-events"
"""Neutral. Nothing in the name says fixture, scenario, or seam."""

HOLDOUT_DIRNAME = ".withheld"
"""Parked beside the staged directory, never inside it."""

CUTOFF = "2026-06-16"
"""First held-out date. Rows on or after this are withheld from the a3 arm."""


def _write(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def stage(arm: str, into: Path) -> Path:
    with SOURCE.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    staged = into / STAGED_DIRNAME
    if staged.exists():
        shutil.rmtree(staged)
    withheld = into / HOLDOUT_DIRNAME
    if withheld.exists():
        shutil.rmtree(withheld)

    if arm == "a1":
        _write(staged / "events.csv", rows, fieldnames)
    elif arm == "a3":
        window = [r for r in rows if r["ts"][:10] < CUTOFF]
        holdout = [r for r in rows if r["ts"][:10] >= CUTOFF]
        _write(staged / "events.csv", window, fieldnames)
        _write(withheld / "events-holdout.csv", holdout, fieldnames)
    else:  # pragma: no cover - argparse constrains this
        raise SystemExit(f"unknown arm {arm!r}")
    return staged


def release(into: Path) -> Path:
    source = into / HOLDOUT_DIRNAME / "events-holdout.csv"
    if not source.is_file():
        raise SystemExit(f"no withheld rows at {source}")
    target = into / STAGED_DIRNAME / "events-holdout.csv"
    shutil.copy2(source, target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arm", choices=("a1", "a3"))
    parser.add_argument("--release-holdout", action="store_true")
    parser.add_argument("--into", type=Path, required=True)
    args = parser.parse_args()

    if args.release_holdout:
        print(release(args.into))
        return 0
    if not args.arm:
        parser.error("--arm is required unless --release-holdout is given")
    staged = stage(args.arm, args.into)
    rows = sum(1 for _ in (staged / "events.csv").open(encoding="utf-8")) - 1
    print(f"{staged}  ({rows} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
