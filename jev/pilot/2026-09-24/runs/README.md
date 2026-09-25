# Archived pilot runs

Per-point outputs of the pilot's runs, kept so the record's figures recompute.

- `run2-host-only.json`: the host question set alone; the Codex set's file had failed to load.
- `run3-both.json` … `run6-both.json`: both sets, every point, identical requests repeated.
- `questions-codex-raw.json`: Codex's blind question set exactly as it returned it, with its pass rules and split notes; `../wave.json` carries the same questions.
- `run_pilot.py.txt`: the script that produced these runs, kept as text because it is evidence of what ran, not tooling: it reads paths in a session scratchpad that no longer exist.
  It decides PASS at p > 0.5 or by the chosen option, which is not `grade.py`'s rule (probability of the pass option, with an abstain band), so its figures and `../grade-report.json`'s are not the same measurement.

Two things these files do not show.
The first run of the host set, which scored 49 of 49, was overwritten and is not here.
Each row's `kind` reads `human` where it means the agent-scored reference: the label was written before the pilot found that no person had scored these points (issue #51), and it is left as written because the files are evidence.
