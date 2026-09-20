#!/usr/bin/env bash
# Run one named arm of the 2026-09-20 cheap-route data-validity wave.
# usage: run_wave.sh <arm-name> <cell> <baseline|pre|post>     (from the repo root)
# <arm-name> is the archive name (e.g. canary-s22a-post, s22a-pre); <cell> picks prompt and fixture.
set -euo pipefail
name=$1 cell=$2 arm=$3
T=skills/hypothesis-driven-analysis/tests
W=$T/runs/artifacts/2026-09-20-cheap-route-validity
case $cell in
  s22a|s22c) fixture=$T/fixtures/s22-cheap-route-validity/a-fanout ;;
  s22b) fixture=$T/fixtures/s22-cheap-route-validity/b-truncated ;;
  s11) fixture=$T/fixtures/s11-mini ;;
  s13) fixture=$T/fixtures/s13-conjunctive ;;
  s2) fixture=$T/fixtures/s1-conversion/orders.csv ;;
  s14) fixture=$T/fixtures/s10-fanout ;;
  s9) fixture=$T/fixtures/s9-ab/signups.csv ;;
  s15) fixture=$T/fixtures/s15-assist-rollout ;;
  *) echo "unknown cell $cell" >&2; exit 2 ;;
esac
case $arm in
  baseline) skill=() ;;
  pre) skill=(--skill hypothesis-driven-analysis --skill-ref main) ;;
  post) skill=(--skill hypothesis-driven-analysis) ;;
  *) echo "unknown arm $arm" >&2; exit 2 ;;
esac
exec uv run $T/run_arm.py --name "$name" --prompt-file "$W/prompts/$cell.txt" \
  "${skill[@]}" --fixture "$fixture" --out "$W"
