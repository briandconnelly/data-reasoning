#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the `da-sweep` fixture has lost any property it exists to set.

    uv run skills/decision-analysis/tests/fixtures/validate_da_sweep.py \
        skills/decision-analysis/tests/fixtures/da-sweep

Properties, each one the DA-S9 / DA-S10 cells depend on. The arithmetic is
recomputed here from the packet files, exactly, rather than imported from the
generator or a checker.

1. s9's census fixes prior odds 40/160 = 0.25, and states that it is a census.
2. s9's vendor note bounds the ratio to 0.5-4 on every firmware revision,
   gives no narrower figure, says why no point is available (revision not
   exposed), and claims no direction for the ratio that 0.5 would contradict.
3. s9 with the prompt's losses restore = (1, 1), keep serving = (3, 0): the
   incremental ratio 2 gives threshold 1/2; posterior odds 0.125-1 straddle
   it while the prior and the losses are points, so only the ratio range
   flips the action, at a ratio of 2 inside 0.5-4. The raw 3:1 reading
   (threshold 1/3) is straddled too, so the verdict does not turn on the
   orientation rule, while its crossover (4/3) differs from the scored 2.
4. s10's census fixes prior odds 7/200 = 0.035, states that it is a census
   with an explicit cutoff, and the release under decision (6.0) appears in
   neither the census nor the reference class.
5. s10's reference class fixes the ratio 18/20 over 6/20 = 3 and states that
   it was drawn to quotas, so its split is not a base rate.
6. s10 with the prompt's matrix ship = (10, 0), hold = (1, 1): the
   incremental ratio 9 gives threshold 1/9, the raw 10:1 gives 1/10, and the
   posterior 0.105 lies strictly between them, so the readings disagree.
7. No packet file states a prior, posterior, probability, odds, or a loss:
   those come from the analysis and the prompt, never from the fixture.
8. Regenerating from the committed generator reproduces every byte.
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).parent
GENERATOR = HERE / "generate_da_sweep.py"

S9_PRIOR = Fraction(1, 4)
S9_RATIO = (Fraction(1, 2), Fraction(4))
S9_LOSSES = {"restore": (Fraction(1), Fraction(1)), "serve": (Fraction(3), Fraction(0))}
S9_CROSSOVER = Fraction(2)
S10_PRIOR = Fraction(7, 200)
S10_RATIO = Fraction(3)
S10_TARGET = "6.0"
S10_LOSSES = {"ship now": (Fraction(10), Fraction(0)), "hold one week": (Fraction(1), Fraction(1))}

FORBIDDEN = re.compile(
    r"\b(prior|posterior|probab\w*|likelihood|odds|loss\w*|cost\w*|\$\d|engineer-days?)\b", re.I
)
FILES = (
    "s9-lr-range/README.md",
    "s9-lr-range/evidence/alert_history.csv",
    "s9-lr-range/evidence/vendor-note.md",
    "s10-loss-matrix/README.md",
    "s10-loss-matrix/evidence/release_history.csv",
    "s10-loss-matrix/evidence/spike_reference.csv",
)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def odds(flags: list[bool]) -> Fraction:
    yes = sum(flags)
    return Fraction(yes, len(flags) - yes)


def check_s9(fx: Path) -> None:
    pkt = fx / "s9-lr-range"
    alerts = rows(pkt / "evidence" / "alert_history.csv")
    prior = odds([r["confirmed_corruption"] == "true" for r in alerts])
    if prior != S9_PRIOR:
        fail(f"s9 census gives prior odds {prior}, not {S9_PRIOR}")
    readme = (pkt / "README.md").read_text(encoding="utf-8")
    if "is a census" not in readme or "none was sampled" not in readme:
        fail("s9 README must state that the alert history is a census")
    if "persisted" in alert_history_header(alerts):
        fail("s9 alert history must not record re-read persistence (it would pin the ratio)")
    note = (pkt / "evidence" / "vendor-note.md").read_text(encoding="utf-8")
    flat = " ".join(note.split())
    m = re.search(r"lies between (\S+) and (\S+) on every firmware revision", flat)
    if m is None:
        fail("s9 vendor note no longer bounds the ratio on every firmware revision")
    stated = (Fraction(m.group(1)), Fraction(m.group(2)))
    if stated != S9_RATIO or "no narrower figure" not in flat or "not exposed" not in flat:
        fail(f"s9 vendor note must bound the ratio to {S9_RATIO} and say why: {stated}")
    if re.search(r"more often|less often|more frequent|less frequent", flat):
        fail("s9 vendor note must not claim a direction the 0.5 endpoint contradicts")
    (r_h, r_n), (s_h, s_n) = S9_LOSSES["restore"], S9_LOSSES["serve"]
    incremental = (s_h - r_h) / (r_n - s_n)  # restore is favored if true
    raw = s_h / r_h
    post = (prior * S9_RATIO[0], prior * S9_RATIO[1])
    for threshold in (1 / incremental, 1 / raw):
        if not (post[0] < threshold < post[1]):
            fail(f"s9 posterior {post} does not straddle threshold {threshold}")
    if (1 / incremental) / prior != S9_CROSSOVER or not (S9_RATIO[0] < S9_CROSSOVER < S9_RATIO[1]):
        fail("s9 ratio crossover is not 2 inside the vendor range")
    if (1 / raw) / prior == S9_CROSSOVER:
        fail("s9's raw-reading crossover must differ from the scored one")


def alert_history_header(alerts: list[dict[str, str]]) -> str:
    return ",".join(alerts[0].keys()) if alerts else ""


def check_s10(fx: Path) -> None:
    pkt = fx / "s10-loss-matrix"
    history = rows(pkt / "evidence" / "release_history.csv")
    prior = odds([r["real_regression"] == "true" for r in history])
    if prior != S10_PRIOR:
        fail(f"s10 census gives prior odds {prior}, not {S10_PRIOR}")
    ref = rows(pkt / "evidence" / "spike_reference.csv")
    real = [r["canary_spike"] == "true" for r in ref if r["real_regression"] == "true"]
    clean = [r["canary_spike"] == "true" for r in ref if r["real_regression"] == "false"]
    ratio = Fraction(sum(real), len(real)) / Fraction(sum(clean), len(clean))
    if ratio != S10_RATIO:
        fail(f"s10 reference class gives ratio {ratio}, not {S10_RATIO}")
    readme = (pkt / "README.md").read_text(encoding="utf-8")
    if "is a census" not in readme or "not a base" not in readme:
        fail("s10 README must state the census and the quota-drawn reference class")
    if "cutoff" not in readme or f"Release {S10_TARGET}" not in readme:
        fail("s10 README must name the release under decision and the census cutoff")
    named = {r["release"] for r in history} | {r["release"] for r in ref}
    if S10_TARGET in named:
        fail(f"release {S10_TARGET} has a resolved row: the fixture would leak the answer")
    posterior = prior * ratio
    (ship_h, ship_n), (hold_h, hold_n) = S10_LOSSES["ship now"], S10_LOSSES["hold one week"]
    incremental = (ship_h - hold_h) / (hold_n - ship_n)  # hold is favored if true
    raw = ship_h / hold_h
    if not (1 / raw < posterior < 1 / incremental):
        fail(f"s10 posterior {posterior} is not strictly between 1/{raw} and 1/{incremental}")


def check_tokens(fx: Path) -> None:
    for rel in FILES:
        for i, line in enumerate((fx / rel).read_text(encoding="utf-8").splitlines(), 1):
            if FORBIDDEN.search(line):
                fail(f"{rel}:{i} carries a belief or loss token: {line.strip()!r}")


def check_regeneration(fx: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "generate_da_sweep.py"
        src.write_text(GENERATOR.read_text(encoding="utf-8"), encoding="utf-8")
        subprocess.run([sys.executable, str(src)], check=True, capture_output=True)
        for rel in FILES:
            if (Path(tmp) / "da-sweep" / rel).read_bytes() != (fx / rel).read_bytes():
                fail(f"{rel} differs from a fresh regeneration")
        produced = {
            p.relative_to(Path(tmp) / "da-sweep").as_posix()
            for p in (Path(tmp) / "da-sweep").rglob("*")
            if p.is_file()
        }
        present = {p.relative_to(fx).as_posix() for p in fx.rglob("*") if p.is_file()}
        if produced != set(FILES) or present != set(FILES):
            fail(f"file set drifted: generator {sorted(produced)}, fixture {sorted(present)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture", type=Path)
    fx = ap.parse_args().fixture
    check_s9(fx)
    check_s10(fx)
    check_tokens(fx)
    check_regeneration(fx)
    print("OK: da-sweep keeps every property it sets")


if __name__ == "__main__":
    main()
