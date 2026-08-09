#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the cs4-facts fixture has lost any fact CS4 needs.

Ground truth is preregistered in scenario CS4
(`skills/causal-identification-review/tests/scenarios.md`): the sheet must
admit regression discontinuity and instrumental variable, and must carry a
stated reason each of difference-in-differences and matching/
selection-on-observables is a decoy.

Run against the fixture directory:

    uv run skills/causal-identification-review/tests/fixtures/validate_cs4.py \
        skills/causal-identification-review/tests/fixtures/cs4-facts
"""

from __future__ import annotations

import argparse
import filecmp
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generate import build_cs4

EXPECTED_FILES = {"facts.md"}

REQUIRED_PHRASES = (
    # Regression discontinuity: the hard eligibility cutoff.
    "$50,000",
    "auto-enrolled",
    # Instrumental variable: batch order as instrument.
    "onboarding batch",
    "independent of any merchant's chargeback history",
    # Difference-in-differences decoy: no pre-period.
    "was not retained",
    "90 days following each merchant's own enrollment date",
    # Matching/selection-on-observables decoy: unrecorded discretion.
    "unrecorded judgment calls",
    # Prospective RCT permitted, named only.
    "prospective randomized experiment",
)

FORBIDDEN_DESIGN_MECHANICS = (
    "power calculation",
    "minimum detectable effect",
    "minimum-detectable-effect",
    "sample-ratio mismatch",
    "sample size calculation",
)
"""Trap 2: the sheet may name a prospective RCT but must not carry its
mechanics -- D3's exclusion."""


def _trap_1_required_facts(text: str) -> list[str]:
    lowered = text.lower()
    out = []
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lowered:
            out.append(f"trap 1: facts.md does not state {phrase!r}")
    return out


def _trap_2_no_design_mechanics(text: str) -> list[str]:
    lowered = text.lower()
    out = []
    for phrase in FORBIDDEN_DESIGN_MECHANICS:
        if phrase in lowered:
            out.append(f"trap 2: facts.md carries prospective-design mechanics {phrase!r}")
    return out


def _trap_3_directory(directory: Path) -> list[str]:
    found = {p.name for p in directory.iterdir()}
    missing = EXPECTED_FILES - found
    extra = found - EXPECTED_FILES
    out = []
    if missing:
        out.append(f"trap 3: fixture directory is missing {sorted(missing)}")
    if extra:
        out.append(f"trap 3: fixture directory has unexpected entries {sorted(extra)}")
    return out


def _trap_4_bytes_reproduce(directory: Path) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp) / "cs4-facts"
        build_cs4(tmp_dir)
        comparison = filecmp.dircmp(tmp_dir, directory)
        out = []
        if comparison.left_only:
            out.append(f"trap 4: regeneration produces extra files {sorted(comparison.left_only)}")
        if comparison.right_only:
            out.append(f"trap 4: committed fixture has extra files {sorted(comparison.right_only)}")
        _, mismatch, errors = filecmp.cmpfiles(
            tmp_dir, directory, comparison.common_files, shallow=False
        )
        if mismatch or errors:
            out.append(f"trap 4: byte mismatch on regeneration: {sorted(mismatch + errors)}")
        return out


def check(directory: Path) -> list[str]:
    text = (directory / "facts.md").read_text(encoding="utf-8")
    return [
        *_trap_1_required_facts(text),
        *_trap_2_no_design_mechanics(text),
        *_trap_3_directory(directory),
        *_trap_4_bytes_reproduce(directory),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    if not args.directory.exists() or not (args.directory / "facts.md").exists():
        print(f"FAIL trap 0: {args.directory / 'facts.md'} does not exist")
        print("\n1 trap(s) lost.")
        return 1

    failures = check(args.directory)
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        print(f"\n{len(failures)} trap(s) lost.")
        return 1
    print("cs4-facts: every trap intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
