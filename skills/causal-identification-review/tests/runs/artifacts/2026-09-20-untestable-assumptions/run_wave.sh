#!/usr/bin/env bash
# Run one named arm of the 2026-09-20 untestable-assumptions wave (issue #40).
# usage: run_wave.sh <arm-name> <cell> <baseline|pre|post>     (from the repo root)
# <arm-name> is the archive name (e.g. canary-cs8-post, cs8-pre); <cell> picks prompt and fixture.
set -euo pipefail
name=$1 cell=$2 arm=$3
T=skills/causal-identification-review/tests
W=$T/runs/artifacts/2026-09-20-untestable-assumptions
case $cell in
  cs8) fixture=$T/fixtures/cs8-encouragement ;;
  cs3|cs6b) fixture=$T/fixtures/cs3-rollout ;;
  *) echo "unknown cell $cell" >&2; exit 2 ;;
esac
case $arm in
  baseline) skill=() ;;
  pre) skill=(--skill causal-identification-review --skill-ref main) ;;
  post) skill=(--skill causal-identification-review) ;;
  *) echo "unknown arm $arm" >&2; exit 2 ;;
esac
exec uv run skills/hypothesis-driven-analysis/tests/run_arm.py --name "$name" \
  --prompt-file "$W/prompts/$cell.txt" "${skill[@]}" --fixture "$fixture" --out "$W"
