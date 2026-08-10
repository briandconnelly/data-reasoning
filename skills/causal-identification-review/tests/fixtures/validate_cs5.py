#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the cs5-bounds fixture has lost any property CS5 needs.

Ground truth and floors are preregistered in scenario CS5
(`skills/causal-identification-review/tests/scenarios.md`). Every threshold
is a floor the committed seed clears with margin, so a failure here means the
fixture changed rather than that a bound was tight.

Run against the fixture directory:

    uv run skills/causal-identification-review/tests/fixtures/validate_cs5.py \
        skills/causal-identification-review/tests/fixtures/cs5-bounds
"""

from __future__ import annotations

import argparse
import csv
import filecmp
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generate import CS5_GROUND_TRUTH, build_cs5

BOUNDS_WIDTH_FLOOR = 0.05
"""Trap 2: upper - lower must exceed this -- a degenerate (equal-attrition)
draw would collapse the bound to a point and entangle this scenario with
HDA's null-result sensitivity gate instead of testing the bound route."""

NUMERIC_TOLERANCE = 1e-6

EXPECTED_FILES = {"outcomes.csv", "assignment_note.md"}


def load(directory: Path) -> tuple[list[dict], list[dict]]:
    with (directory / "outcomes.csv").open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    invited = [r for r in rows if r["cohort"] == "invited"]
    non_invited = [r for r in rows if r["cohort"] == "non_invited"]
    return invited, non_invited


def _lee_bounds(
    treated_observed: list[int], control_observed: list[int], n_treated: int, n_control: int
) -> tuple[float, float]:
    """Independent Lee (2009) trimming-bounds reimplementation.

    Deliberately not imported from `generate.py`: this validator checks the
    generator's own recorded bounds against a second, separately written
    computation, so a bug shared by both implementations is the only way a
    mismatch could hide.
    """
    survival_treated = len(treated_observed) / n_treated
    survival_control = len(control_observed) / n_control
    control_mean = sum(control_observed) / len(control_observed)

    if survival_treated < survival_control:
        raise ValueError(
            "treated survival rate is below control's -- monotonicity direction assumed by "
            "this fixture does not hold in the data"
        )

    trim_fraction = (survival_treated - survival_control) / survival_treated
    ordered = sorted(treated_observed)
    trim_count = round(trim_fraction * len(ordered))

    keep_low_removed = ordered[trim_count:] if trim_count else ordered
    keep_high_removed = ordered[: len(ordered) - trim_count] if trim_count else ordered

    upper = (sum(keep_low_removed) / len(keep_low_removed)) - control_mean
    lower = (sum(keep_high_removed) / len(keep_high_removed)) - control_mean
    return min(lower, upper), max(lower, upper)


def _parse_ground_truth_bounds() -> tuple[float, float] | None:
    if not CS5_GROUND_TRUTH.exists():
        return None
    lower = upper = None
    for line in CS5_GROUND_TRUTH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip("- ").strip()
        if stripped.startswith("lower:"):
            lower = float(stripped.split(":")[1].strip())
        if stripped.startswith("upper:"):
            upper = float(stripped.split(":")[1].strip())
    if lower is None or upper is None:
        return None
    return lower, upper


def _trap_1_monotonicity_direction(invited: list[dict], non_invited: list[dict]) -> list[str]:
    invited_attrition = sum(1 for r in invited if r["retained_30d"] == "") / len(invited)
    non_invited_attrition = sum(1 for r in non_invited if r["retained_30d"] == "") / len(
        non_invited
    )
    if invited_attrition >= non_invited_attrition:
        return [
            f"trap 1: invited attrition {invited_attrition:.3f} is not below non-invited "
            f"attrition {non_invited_attrition:.3f} -- the stated monotonicity direction "
            "(invitation keeps customers observed longer) does not hold"
        ]
    return []


def _trap_2_bounds_match_and_nondegenerate(
    invited: list[dict], non_invited: list[dict]
) -> list[str]:
    out = []
    invited_observed = [int(r["retained_30d"]) for r in invited if r["retained_30d"] != ""]
    non_invited_observed = [int(r["retained_30d"]) for r in non_invited if r["retained_30d"] != ""]

    try:
        lower, upper = _lee_bounds(
            invited_observed, non_invited_observed, len(invited), len(non_invited)
        )
    except ValueError as exc:
        return [f"trap 2: {exc}"]

    if upper - lower < BOUNDS_WIDTH_FLOOR:
        out.append(
            f"trap 2: bounds width {upper - lower:.4f} is below the {BOUNDS_WIDTH_FLOOR} "
            "non-degeneracy floor"
        )

    recorded = _parse_ground_truth_bounds()
    if recorded is None:
        out.append("trap 2: cs5-bounds-ground-truth.md is missing or unparseable")
    else:
        recorded_lower, recorded_upper = recorded
        if abs(recorded_lower - lower) > NUMERIC_TOLERANCE:
            out.append(
                f"trap 2: recorded lower {recorded_lower:.6f} does not match recomputed "
                f"lower {lower:.6f}"
            )
        if abs(recorded_upper - upper) > NUMERIC_TOLERANCE:
            out.append(
                f"trap 2: recorded upper {recorded_upper:.6f} does not match recomputed "
                f"upper {upper:.6f}"
            )
    return out


def _trap_3_no_point_estimate_columns(directory: Path) -> list[str]:
    """The fixture must not carry a risk-score or point-estimate column --
    nothing here should let a run skip straight to a naive comparison."""
    with (directory / "outcomes.csv").open(encoding="utf-8") as handle:
        header = next(csv.reader(handle))
    forbidden = {"risk_score", "effect", "point_estimate"}
    leaked = forbidden & set(header)
    if leaked:
        return [f"trap 3: outcomes.csv carries forbidden column(s) {sorted(leaked)}"]
    return []


def _trap_4_assignment_note(directory: Path) -> list[str]:
    out = []
    note_path = directory / "assignment_note.md"
    if not note_path.exists():
        return ["trap 4: assignment_note.md is missing"]
    text = note_path.read_text(encoding="utf-8").lower()
    required_phrases = (
        "randomized",
        "enrollment wave",
        "differentially missing",
        "monotonicity",
        "keep a customer observed longer",
        "never shorten",
    )
    for phrase in required_phrases:
        if phrase not in text:
            out.append(f"trap 4: assignment_note.md does not state {phrase!r}")
    return out


def _trap_5_directory(directory: Path) -> list[str]:
    found = {p.name for p in directory.iterdir()}
    missing = EXPECTED_FILES - found
    extra = found - EXPECTED_FILES
    out = []
    if missing:
        out.append(f"trap 5: fixture directory is missing {sorted(missing)}")
    if extra:
        out.append(f"trap 5: fixture directory has unexpected entries {sorted(extra)}")
    return out


def _trap_6_bytes_reproduce(directory: Path) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp) / "cs5-bounds"
        tmp_gt = Path(tmp) / "cs5-bounds-ground-truth.md"
        build_cs5(tmp_dir, tmp_gt)
        comparison = filecmp.dircmp(tmp_dir, directory)
        out = []
        if comparison.left_only:
            out.append(f"trap 6: regeneration produces extra files {sorted(comparison.left_only)}")
        if comparison.right_only:
            out.append(f"trap 6: committed fixture has extra files {sorted(comparison.right_only)}")
        _, mismatch, errors = filecmp.cmpfiles(
            tmp_dir, directory, comparison.common_files, shallow=False
        )
        if mismatch or errors:
            out.append(f"trap 6: byte mismatch on regeneration: {sorted(mismatch + errors)}")
        if not filecmp.cmp(tmp_gt, CS5_GROUND_TRUTH, shallow=False):
            out.append("trap 6: regenerating does not reproduce the ground-truth file")
        return out


def check(directory: Path) -> list[str]:
    invited, non_invited = load(directory)
    return [
        *_trap_1_monotonicity_direction(invited, non_invited),
        *_trap_2_bounds_match_and_nondegenerate(invited, non_invited),
        *_trap_3_no_point_estimate_columns(directory),
        *_trap_4_assignment_note(directory),
        *_trap_5_directory(directory),
        *_trap_6_bytes_reproduce(directory),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    if not args.directory.exists() or not (args.directory / "outcomes.csv").exists():
        print(f"FAIL trap 0: {args.directory / 'outcomes.csv'} does not exist")
        print("\n1 trap(s) lost.")
        return 1

    failures = check(args.directory)
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        print(f"\n{len(failures)} trap(s) lost.")
        return 1
    print("cs5-bounds: every trap intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
