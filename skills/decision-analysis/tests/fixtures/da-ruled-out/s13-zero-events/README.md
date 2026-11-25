# Disk firmware pilot

The vendor's new disk firmware has been piloted on part of the fleet. We must
choose between rolling it out fleet-wide this week and keeping piloting
another month.

Files:

- `evidence/pilot-log.csv`: the pilot, one row per host-week.
- `evidence/vendor-advisory.md`: the vendor's advisory on the defect.
- `evidence/fleet-baseline.md`: our fleet's measured corruption rate.
- `evidence/owner-decision.md`: the decision owner's settled inputs.

Each row of `pilot-log.csv` is one week on one host: 100 distinct hosts,
one week each, so no host contributes two weeks. The hosts were drawn from
separate racks, power feeds, and drive batches, so the pilot treats the
100 host-weeks as independent trials of the same corruption rate.
