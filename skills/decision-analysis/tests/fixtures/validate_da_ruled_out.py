#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the `da-ruled-out` fixture has lost any property it exists to set.

    uv run skills/decision-analysis/tests/fixtures/validate_da_ruled_out.py \
        skills/decision-analysis/tests/fixtures/da-ruled-out

Properties, each one the DA-S12 / DA-S13 cells depend on. The arithmetic is
recomputed here from the packet files, exactly where it can be, rather than
imported from the generator or a checker.

1. s12 states each exclusion fact in its own file: the partition was held
   only on db-03's local disk; the job modifies data only where it executes;
   process accounting for the whole window shows no compaction process on
   db-03; the deploy log shows db-03 never ran build 412 while other hosts
   did; db-03's device log records a disk fault inside the window. The
   README says the facts are verified and not in dispute.
2. s12's owner losses: neither action dominates across both states (so the
   odds form would need a ratio the packet never supplies), while in the
   surviving state the difference roll back - hotfix = 4 - 1 = 3 > 0 names
   the hotfix; the same table read across both states would not.
3. s13's pilot is zero events over 100 host-weeks on 100 distinct hosts, and
   the README states the independence and why.
4. s13's rates 0.02 and 0.005 recompute the ratio (0.98 / 0.995)^100, about
   0.2189; with prior odds 1 and losses roll out = (10, 0), keep piloting =
   (1, 1), the threshold is 1/9, posterior odds 0.2189 lie above it (keep
   piloting), the prior-odds crossover is about 0.5075, outside the fixed
   prior 1, and reading zero events as elimination (posterior 0) gives roll
   out instead. The exact Bernoulli 95% bound 1 - 0.05^(1/100) is about
   0.0295, below the defect rate.
5. Nothing in s13 makes corruption impossible under the new firmware, and no
   s12 file states a probability or a likelihood ratio.
6. Each prompt carries `{FIXTURE_PATH}` once, and the s12 prompt names the
   narrowed proposition: direct modification by the job.
7. Regenerating from the committed generator reproduces every byte.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).parent
GENERATOR = HERE / "generate_da_ruled_out.py"

S12 = "s12-partition-loss"
S13 = "s13-zero-events"
FILES = (
    f"{S12}/README.md",
    f"{S12}/evidence/incident-timeline.md",
    f"{S12}/evidence/storage-topology.md",
    f"{S12}/evidence/compaction-design.md",
    f"{S12}/evidence/process-accounting.csv",
    f"{S12}/evidence/deploy-log.csv",
    f"{S12}/evidence/db-03-device-log.txt",
    f"{S12}/evidence/owner-losses.md",
    f"{S13}/README.md",
    f"{S13}/evidence/pilot-log.csv",
    f"{S13}/evidence/vendor-advisory.md",
    f"{S13}/evidence/fleet-baseline.md",
    f"{S13}/evidence/owner-decision.md",
)
PROMPTS = ("da-s12.txt", "da-s13.txt")
N_WEEKS = 100
RATIO = (0.2188, 0.2190)
CROSSOVER = (0.5074, 0.5076)
BOUND = (0.0295, 0.0296)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def read(fx: Path, rel: str) -> str:
    return (fx / rel).read_text(encoding="utf-8")


def rows(fx: Path, rel: str) -> list[dict[str, str]]:
    with (fx / rel).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def table(text: str) -> dict[str, tuple[Fraction, Fraction]]:
    """The two action rows of a three-column Markdown loss table."""
    out = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and re.fullmatch(r"\d+", cells[1]) and re.fullmatch(r"\d+", cells[2]):  # noqa: PLR2004
            out[cells[0]] = (Fraction(cells[1]), Fraction(cells[2]))
    return out


def minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def check_s12(fx: Path) -> None:
    for rel, phrase in (
        (f"{S12}/README.md", "verified"),
        (f"{S12}/README.md", "none is in dispute"),
        (f"{S12}/evidence/storage-topology.md", "only on db-03's local disk"),
        (f"{S12}/evidence/storage-topology.md", "no replica"),
        (f"{S12}/evidence/compaction-design.md", "only by executing"),
        (f"{S12}/evidence/incident-timeline.md", "01:40 to 03:10"),
    ):
        if phrase not in read(fx, rel):
            fail(f"{rel} lost {phrase!r}")
    procs = rows(fx, f"{S12}/evidence/process-accounting.csv")
    if not procs or {r["host"] for r in procs} != {"db-03"}:
        fail("process accounting must cover db-03 alone")
    times = sorted(minutes(r["time"]) for r in procs)
    if times[0] > minutes("01:40") or times[-1] < minutes("03:10"):
        fail("process accounting does not cover the whole incident window")
    if any("compact" in r["process"] for r in procs):
        fail("a compaction process executed on db-03: the exclusion is gone")
    deploys = {r["host"]: r["build"] for r in rows(fx, f"{S12}/evidence/deploy-log.csv")}
    if deploys.get("db-03") != "411" or "412" not in deploys.values():
        fail("the deploy log must show db-03 on 411 while build 412 ran elsewhere")
    faults = [
        ln
        for ln in read(fx, f"{S12}/evidence/db-03-device-log.txt").splitlines()
        if "error" in ln and minutes("01:40") <= minutes(ln[11:16]) <= minutes("03:10")
    ]
    if not faults:
        fail("db-03's device log names no fault inside the window")
    losses = table(read(fx, f"{S12}/evidence/owner-losses.md"))
    rollback, hotfix = (
        losses.get("roll back to build 411"),
        losses.get("keep build 412 with a hotfix"),
    )
    if rollback is None or hotfix is None:
        fail(f"owner losses lost an action row: {losses}")
    dominates = all(a <= b for a, b in zip(rollback, hotfix, strict=True)) or all(
        b <= a for a, b in zip(rollback, hotfix, strict=True)
    )
    if dominates:
        fail("one action dominates across both states: the exclusion would not matter")
    difference = rollback[1] - hotfix[1]
    if difference != 3:  # noqa: PLR2004
        fail(f"surviving-state difference is {difference}, not 3")
    for rel in FILES[:8]:
        if re.search(r"\b(probab\w*|likelihood|odds|ratio)\b", read(fx, rel), re.I):
            fail(f"{rel} states a probability or ratio")


def check_s13(fx: Path) -> None:  # noqa: PLR0912 -- one check per property
    pilot = rows(fx, f"{S13}/evidence/pilot-log.csv")
    if len(pilot) != N_WEEKS or len({r["host"] for r in pilot}) != N_WEEKS:
        fail("the pilot must be 100 host-weeks on 100 distinct hosts")
    if any(r["corruption_events"] != "0" for r in pilot):
        fail("the pilot is no longer zero events")
    readme = read(fx, f"{S13}/README.md")
    for phrase in ("independent", "no host contributes two weeks", "separate racks"):
        if phrase not in readme:
            fail(f"s13 README lost {phrase!r}")
    defect = Fraction(
        re.search(r"rate of ([\d.]+)", read(fx, f"{S13}/evidence/vendor-advisory.md"))[1]
    )
    base = Fraction(
        re.search(r"rate of ([\d.]+)", read(fx, f"{S13}/evidence/fleet-baseline.md"))[1]
    )
    ratio = float(((1 - defect) / (1 - base)) ** N_WEEKS)
    if not RATIO[0] < ratio < RATIO[1]:
        fail(f"the zero-event ratio recomputes to {ratio}, not about 0.2189")
    owner = read(fx, f"{S13}/evidence/owner-decision.md")
    if "1 (even)" not in owner or "settled" not in owner:
        fail("the owner's prior odds 1, held fixed, are gone")
    losses = table(owner)
    roll, keep = (
        losses.get("roll out fleet-wide this week"),
        losses.get("keep piloting another month"),
    )
    if roll != (10, 0) or keep != (1, 1):
        fail(f"owner losses changed: {losses}")
    threshold = (keep[1] - roll[1]) / (roll[0] - keep[0])  # favored keep if H: r = 9, 1/r
    prior = 1
    if not prior * ratio > threshold:
        fail("posterior odds no longer exceed the threshold: keep piloting is not preferred")
    eliminated_posterior = 0  # the zero count misread as ruling the defect out
    if not eliminated_posterior < threshold:
        fail("reading zero events as elimination no longer changes the action to roll out")
    crossover = float(threshold) / ratio
    if not CROSSOVER[0] < crossover < CROSSOVER[1] or crossover >= prior:
        fail(f"prior crossover {crossover} is not about 0.5075 and outside the prior 1")
    bound = 1 - 0.05 ** (1 / N_WEEKS)
    if not BOUND[0] < bound < BOUND[1] or not bound > float(defect):
        fail(f"the Bernoulli bound {bound} lost its relation to the defect rate")
    if not math.isclose(-math.log(0.05) / N_WEEKS, 0.02996, rel_tol=1e-3):
        fail("the Poisson bound no longer recomputes")
    for rel in FILES[8:]:
        if re.search(
            r"\b(impossible|cannot corrupt|ruled out|never corrupt\w*)\b", read(fx, rel), re.I
        ):
            fail(f"{rel} makes corruption impossible under the new firmware")


def check_prompts(prompts: Path) -> None:
    for name in PROMPTS:
        text = (prompts / name).read_text(encoding="utf-8")
        if text.count("{FIXTURE_PATH}") != 1:
            fail(f"{name} must carry {{FIXTURE_PATH}} exactly once")
    if "directly modified" not in (prompts / "da-s12.txt").read_text(encoding="utf-8"):
        fail("the s12 prompt lost the narrowed proposition")


def check_regeneration(fx: Path, prompts: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / GENERATOR.name
        src.write_text(GENERATOR.read_text(encoding="utf-8"), encoding="utf-8")
        subprocess.run([sys.executable, str(src)], check=True, capture_output=True)
        fresh = Path(tmp) / "da-ruled-out"
        for rel in FILES:
            if (fresh / rel).read_bytes() != (fx / rel).read_bytes():
                fail(f"{rel} differs from a fresh regeneration")
        for name in PROMPTS:
            if (Path(tmp) / prompts.name / name).read_bytes() != (prompts / name).read_bytes():
                fail(f"{name} differs from a fresh regeneration")
        produced = {p.relative_to(fresh).as_posix() for p in fresh.rglob("*") if p.is_file()}
        present = {p.relative_to(fx).as_posix() for p in fx.rglob("*") if p.is_file()}
        if produced != set(FILES) or present != set(FILES):
            fail(f"file set drifted: generator {sorted(produced)}, fixture {sorted(present)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture", type=Path)
    fx = ap.parse_args().fixture
    prompts = fx.parent / "da-ruled-out-prompts"
    check_s12(fx)
    check_s13(fx)
    check_prompts(prompts)
    check_regeneration(fx, prompts)
    print(
        "OK: da-ruled-out keeps every property it sets "
        "(s13 ratio 0.2189, prior crossover 0.5075; s12 surviving-state difference 3)"
    )


if __name__ == "__main__":
    main()
