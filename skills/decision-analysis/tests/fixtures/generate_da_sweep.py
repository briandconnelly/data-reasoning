#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate the `da-sweep` fixture: two packets for DA-S9 and DA-S10.

Each packet supplies a supported prior (a census base rate), a supported
likelihood ratio (a vendor characterization, or a quota-drawn reference
class), and nothing that states a loss: the cell's prompt states the losses
exactly, so they are `user-elicited` and belief-grade, and no other gate in
`decision-analysis` § Numeric Policy can explain the verdict.

- `s9-lr-range/`: a point prior (odds 40/160 = 0.25) and a ratio the vendor
  pins only to a range, 0.5 to 4. With a loss ratio of 2 (threshold 0.5) the
  posterior range 0.125 to 1 straddles the threshold although the prior class
  and the losses are points: the likelihood-ratio range alone flips the
  action (crossover at a ratio of 2).
- `s10-loss-matrix/`: a point prior (odds 7/200 = 0.035) and a point ratio
  (18/20 over 6/20 = 3), so posterior odds 0.105. The prompt's four-cell loss
  matrix, ship = (10, 0) and hold = (1, 1), gives an incremental loss ratio
  of 9 (threshold 1/9, about 0.111): ship. Reading the raw 10:1 gives a
  threshold of 0.1: hold.

`validate_da_sweep.py` holds both packets to these properties. Deterministic
from a fixed seed on this module's own `random.Random`. Run from the repo root:

    uv run skills/decision-analysis/tests/fixtures/generate_da_sweep.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "da-sweep"
RNG = random.Random(20261109)

# s9: every checksum-mismatch alert since 2024, each with its confirmed outcome.
S9_ALERTS = 200
S9_CORRUPT = 40
# The vendor's range for the ratio of re-read persistence rates.
S9_RATIO_LOW, S9_RATIO_HIGH = "0.5", "4"

# s10: every release since 2023 (a census) and the spike reference class
# (quota-drawn: 20 regressions, 20 clean releases).
S10_RELEASES = 207
S10_REGRESSIONS = 7
S10_REF_REAL, S10_REF_REAL_SPIKE = 20, 18
S10_REF_CLEAN, S10_REF_CLEAN_SPIKE = 20, 6

S9_README = """\
# Checksum-mismatch alert on db-07

Tonight at 02:14 the nightly integrity job flagged a block checksum mismatch on
`db-07`. The on-call engineer re-read the block at 02:31 and the mismatch
persisted.

Files:

- `evidence/alert_history.csv` is a census: every checksum-mismatch alert our
  fleet has raised since 2024-01-01, one row each, with the outcome the
  follow-up review confirmed (`confirmed_corruption`). No alert is missing and
  none was sampled. Re-read checks only began this month, so the history does
  not record whether a mismatch persisted.
- `evidence/vendor-note.md` is the storage vendor's published characterization
  of re-reads on this controller family.
"""

S9_VENDOR_NOTE = f"""\
# Vendor note SV-2291: persistence of checksum mismatches across a re-read

Published by the controller vendor, revision 3.

Across the vendor's field population of this controller family, a mismatch that
reflects real on-disk corruption persists across an immediate re-read more
often than a transient mismatch does. The ratio of the two persistence rates
(persists given real corruption, divided by persists given a transient fault)
depends on the controller firmware revision: the vendor measures it at
{S9_RATIO_LOW} on the oldest supported revision and {S9_RATIO_HIGH} on the
newest, and gives no figure in between. Firmware revisions in a customer fleet
are not exposed by the controller's management interface.
"""

S10_README = """\
# Release 4.12 canary: error-rate spike

Release 4.12's canary showed an error-rate spike in its first hour.

Files:

- `evidence/release_history.csv` is a census: every release we have shipped
  since 2023-01-01, one row each, with whether the post-release review
  confirmed a real regression (`real_regression`). No release is missing and
  none was sampled.
- `evidence/spike_reference.csv` is a reference class built for the canary
  dashboard: 20 releases that were real regressions and 20 that were not,
  drawn to quotas fixed by the analyst (so its 20/20 split is not a base
  rate), each marked with whether its canary showed the same first-hour
  error-rate spike (`canary_spike`).
"""


def alert_history() -> list[dict[str, str]]:
    outcomes = [True] * S9_CORRUPT + [False] * (S9_ALERTS - S9_CORRUPT)
    RNG.shuffle(outcomes)
    return [
        {
            "alert_id": f"CKS-{1000 + i}",
            "quarter": f"{2024 + (i - 1) // 100}-Q{1 + (i - 1) % 4}",
            "confirmed_corruption": "true" if c else "false",
        }
        for i, c in enumerate(outcomes, 1)
    ]


def release_history() -> list[dict[str, str]]:
    outcomes = [True] * S10_REGRESSIONS + [False] * (S10_RELEASES - S10_REGRESSIONS)
    RNG.shuffle(outcomes)
    return [
        {
            "release": f"{3 + (i - 1) // 100}.{(i - 1) % 100}",
            "real_regression": "true" if r else "false",
        }
        for i, r in enumerate(outcomes, 1)
    ]


def spike_reference() -> list[dict[str, str]]:
    real = [True] * S10_REF_REAL_SPIKE + [False] * (S10_REF_REAL - S10_REF_REAL_SPIKE)
    clean = [True] * S10_REF_CLEAN_SPIKE + [False] * (S10_REF_CLEAN - S10_REF_CLEAN_SPIKE)
    RNG.shuffle(real)
    RNG.shuffle(clean)
    rows = [(True, s) for s in real] + [(False, s) for s in clean]
    RNG.shuffle(rows)
    return [
        {
            "release": f"ref-{i:02d}",
            "real_regression": "true" if r else "false",
            "canary_spike": "true" if s else "false",
        }
        for i, (r, s) in enumerate(rows, 1)
    ]


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def write_text(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    s9 = OUT / "s9-lr-range"
    write_text(S9_README, s9 / "README.md")
    write_csv(alert_history(), s9 / "evidence" / "alert_history.csv")
    write_text(S9_VENDOR_NOTE, s9 / "evidence" / "vendor-note.md")
    s10 = OUT / "s10-loss-matrix"
    write_text(S10_README, s10 / "README.md")
    write_csv(release_history(), s10 / "evidence" / "release_history.csv")
    write_csv(spike_reference(), s10 / "evidence" / "spike_reference.csv")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
