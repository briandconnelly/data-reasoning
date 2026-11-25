#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate the `da-ruled-out` fixture: two packets for DA-S12 and DA-S13.

The pair separates a structural exclusion from a zero count (decisions/008).

- `s12-partition-loss/`: the orders partition on db-03 was lost overnight.
  Each fact sits in its own file: the partition lived only on db-03's local
  disk (storage topology), the build-412 compaction job modifies data only on
  the host where it executes (its design document), the job never executed
  on db-03 (process accounting) and db-03 never ran build 412 (deploy log),
  and db-03's device log records a disk fault in the window. So direct
  modification by the job is structurally impossible, and the loss is
  possible without it. The owner's losses over (job directly modified the
  partition, it did not) are roll back = (0, 4) and hotfix = (6, 1): neither
  action dominates across both states, so an odds analysis would need a
  ratio, while in the surviving state the difference 4 - 1 = 3 prefers the
  hotfix. Every fact is stated as verified, so `decide` is reachable without
  adjudication.
- `s13-zero-events/`: zero corruption events over 100 host-weeks, one week on
  each of 100 distinct hosts, which the packet treats as independent and
  says why; sourced rates 0.02 (defective firmware, vendor advisory) and
  0.005 (fleet baseline) with comparable reference classes; the owner's
  prior odds 1, held fixed; losses over (defect, no defect) of roll out =
  (10, 0) and keep piloting = (1, 1). The ratio of zero events is
  (0.98 / 0.995)^100, about 0.2189, the threshold is 1/9, and the
  prior-odds crossover is about 0.5075: keep piloting, robustly. Reading the
  zero count as elimination gives posterior odds 0 and roll out.

The prompts each cell sends are written beside the packets, under
`da-ruled-out-prompts/`, so a staged packet never carries its own prompt.
`validate_da_ruled_out.py` holds both packets to these properties.
Deterministic from a fixed seed on this module's own `random.Random`. Run
from the repo root:

    uv run skills/decision-analysis/tests/fixtures/generate_da_ruled_out.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "da-ruled-out"
PROMPTS = HERE / "da-ruled-out-prompts"
RNG = random.Random(20261125)

S13_HOSTS = 100
S13_DEFECT_RATE = "0.02"
S13_BASELINE_RATE = "0.005"

S12_PROMPT = """\
We suspect the new compaction job in build 412 directly modified or deleted the orders \
partition on db-03 last night, and we must choose by noon between rolling back to build 411 \
and keeping build 412 with a hotfix. Here is the incident packet ({FIXTURE_PATH}). Roll back \
or hotfix?
"""

S13_PROMPT = """\
The vendor's new disk firmware has shown zero corruption events in our pilot. Should we roll \
it out fleet-wide this week or keep piloting another month? Packet: {FIXTURE_PATH}.
"""

S12_README = """\
# db-03 orders partition loss

Last night the orders partition on `db-03` was lost. We must choose by noon
between rolling back to build 411 and keeping build 412 with a hotfix.

Every fact in these files was verified by the storage on-call lead this
morning; none is in dispute.

Files:

- `evidence/incident-timeline.md`: what was lost, and when.
- `evidence/storage-topology.md`: where the orders partition was held.
- `evidence/compaction-design.md`: the build-412 compaction job's design.
- `evidence/process-accounting.csv`: every process that executed on db-03
  during the incident window.
- `evidence/deploy-log.csv`: which build each database host was running.
- `evidence/db-03-device-log.txt`: db-03's disk controller log for the window.
- `evidence/owner-losses.md`: the decision owner's losses for each action.
"""

S12_TIMELINE = """\
# Incident timeline

- 01:40: the orders partition on db-03 was last read successfully.
- 02:55: queries against the orders partition on db-03 began failing.
- 03:10: on-call confirmed the partition's files were gone from db-03's local
  disk.

The incident window is 01:40 to 03:10.
"""

S12_TOPOLOGY = """\
# Storage topology: orders partition

The orders partition was held only on db-03's local disk. It had no replica,
was not on any shared volume, and was not on network storage. No other host
mounted or could reach db-03's local disk.
"""

S12_DESIGN = """\
# Compaction job (build 412): design

The compaction job rewrites partitions on the host where it executes. It opens
partition files through the local filesystem only, holds no network storage
client, and issues no remote commands, so it can modify data only by executing
on the host that holds that data.
"""

S12_DEVICE_LOG = """\
2026-11-24T01:52:07Z db-03 sd1 controller: medium error, unrecovered read
2026-11-24T01:52:09Z db-03 sd1 controller: remapping failed, sector range marked bad
2026-11-24T02:31:44Z db-03 sd1 controller: filesystem journal write failed
2026-11-24T02:54:58Z db-03 sd1 controller: device reset
"""

S12_LOSSES = """\
# Owner's losses

Supplied by the storage on-call lead, who decides, in hours of service impact.
"The job" is the build-412 compaction job.

| action | the job directly modified the partition | the job did not |
| --- | --- | --- |
| roll back to build 411 | 0 | 4 |
| keep build 412 with a hotfix | 6 | 1 |
"""

S12_PROCESSES = (
    "postgres",
    "pg_walwriter",
    "pg_checkpointer",
    "node_exporter",
    "sshd",
    "logrotate",
    "backup-agent",
)
S12_HOSTS = ("db-01", "db-02", "db-03", "db-04", "db-05")

S13_README = """\
# Disk firmware pilot

The vendor's new disk firmware has been piloted on part of the fleet. We must
choose between rolling it out fleet-wide this week and keeping piloting
another month.

Files:

- `evidence/pilot-log.csv`: the pilot, one row per host-week.
- `evidence/vendor-advisory.md`: the vendor's advisory on the defect.
- `evidence/fleet-baseline.md`: our fleet's measured corruption rate.
- `evidence/owner-decision.md`: the decision owner's settled inputs.
"""

S13_ADVISORY = f"""\
# Vendor advisory VA-0417: silent-corruption defect

Some builds of this firmware family carry a write-path defect. On firmware
that carries it, the vendor's field data from its fleet census shows a silent
corruption rate of {S13_DEFECT_RATE} per host-week, measured over host-weeks of
the same drive model under comparable write loads. The advisory does not say
whether the new firmware build carries the defect.
"""

S13_BASELINE = f"""\
# Fleet baseline

Over the last two years our fleet, on firmware without the defect, measured a
silent corruption rate of {S13_BASELINE_RATE} per host-week, from the integrity
scanner's census of every host-week on the same drive model under the same
write loads as the pilot.
"""

S13_OWNER = """\
# Owner's settled inputs

From the storage platform owner, who decides. These are settled and are not
to be revisited in this decision.

- Odds that the new firmware carries the advisory's defect, before the pilot:
  1 (even).
- Losses, in incident-equivalents:

  | action | firmware carries the defect | it does not |
  | --- | --- | --- |
  | roll out fleet-wide this week | 10 | 0 |
  | keep piloting another month | 1 | 1 |
"""

S13_SAMPLING = f"""\
Each row of `pilot-log.csv` is one week on one host: {S13_HOSTS} distinct hosts,
one week each, so no host contributes two weeks. The hosts were drawn from
separate racks, power feeds, and drive batches, so the pilot treats the
{S13_HOSTS} host-weeks as independent trials of the same corruption rate.
"""


def process_accounting() -> list[dict[str, str]]:
    rows = []
    for minute in range(100, 191, 5):  # 01:40 to 03:10
        for name in RNG.sample(S12_PROCESSES, 4):
            rows.append(
                {
                    "host": "db-03",
                    "time": f"{minute // 60:02d}:{minute % 60:02d}",
                    "process": name,
                    "build": "411",
                }
            )
    return rows


def deploy_log() -> list[dict[str, str]]:
    return [
        {
            "host": host,
            "build": "411" if host == "db-03" else "412",
            "deployed": "2026-11-20" if host == "db-03" else "2026-11-23",
        }
        for host in S12_HOSTS
    ]


def pilot_log() -> list[dict[str, str]]:
    hosts = RNG.sample(range(1000, 9000), S13_HOSTS)
    return [
        {
            "host": f"host-{h}",
            "week": f"2026-W{40 + i % 6}",
            "corruption_events": "0",
        }
        for i, h in enumerate(hosts)
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
    s12 = OUT / "s12-partition-loss"
    write_text(S12_README, s12 / "README.md")
    write_text(S12_TIMELINE, s12 / "evidence" / "incident-timeline.md")
    write_text(S12_TOPOLOGY, s12 / "evidence" / "storage-topology.md")
    write_text(S12_DESIGN, s12 / "evidence" / "compaction-design.md")
    write_csv(process_accounting(), s12 / "evidence" / "process-accounting.csv")
    write_csv(deploy_log(), s12 / "evidence" / "deploy-log.csv")
    write_text(S12_DEVICE_LOG, s12 / "evidence" / "db-03-device-log.txt")
    write_text(S12_LOSSES, s12 / "evidence" / "owner-losses.md")
    s13 = OUT / "s13-zero-events"
    write_text(S13_README + "\n" + S13_SAMPLING, s13 / "README.md")
    write_csv(pilot_log(), s13 / "evidence" / "pilot-log.csv")
    write_text(S13_ADVISORY, s13 / "evidence" / "vendor-advisory.md")
    write_text(S13_BASELINE, s13 / "evidence" / "fleet-baseline.md")
    write_text(S13_OWNER, s13 / "evidence" / "owner-decision.md")
    write_text(S12_PROMPT, PROMPTS / "da-s12.txt")
    write_text(S13_PROMPT, PROMPTS / "da-s13.txt")
    print(f"wrote {OUT} and {PROMPTS}")


if __name__ == "__main__":
    main()
