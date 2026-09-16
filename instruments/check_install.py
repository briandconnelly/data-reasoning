#!/usr/bin/env python3
"""Check a packaged skill surface and exercise its hook without claiming host activation."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path

SHIPPED_SKILLS = (
    "causal-identification-review",
    "decision-analysis",
    "exploratory-data-analysis",
    "hypothesis-driven-analysis",
)


def check_surface(root: Path) -> list[str]:
    manifest = json.loads((root / ".codex-plugin/plugin.json").read_text())
    skills = root / manifest["skills"]
    expected = {skills / name / "SKILL.md" for name in SHIPPED_SKILLS}
    actual = set(skills.rglob("SKILL.md"))
    findings = [
        f"Unexpected discoverable skill: {p.relative_to(root)}" for p in sorted(actual - expected)
    ]
    findings.extend(
        f"Missing shipped skill: {p.relative_to(root)}" for p in sorted(expected - actual)
    )
    return findings


def check_hook(root: Path) -> list[str]:
    config = json.loads((root / "hooks/hooks.json").read_text())
    command = config["hooks"]["PostToolUse"][0]["hooks"][0]["command"]
    env = {**os.environ, "PLUGIN_ROOT": str(root)}
    env.pop("CLAUDE_PLUGIN_ROOT", None)
    with tempfile.TemporaryDirectory(prefix="data-reasoning-hook-") as scratch:
        record = Path(scratch) / "record.md"
        record.write_text(
            "# Decision Record: hook smoke test\n\n## Verdict\n\n- Verdict: optimal\n"
        )
        payload = {
            "tool_name": "apply_patch",
            "cwd": scratch,
            "tool_input": {
                "command": "*** Begin Patch\n*** Update File: record.md\n@@\n*** End Patch\n"
            },
        }
        result = subprocess.run(
            ["sh", "-c", command],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            env=env,
            timeout=40,
            check=False,
        )
    if result.returncode != 2 or "verdict 'optimal'" not in result.stderr:  # noqa: PLR2004
        return [f"Hook smoke test failed (exit {result.returncode}): {result.stderr.strip()}"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "plugin_root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    root = args.plugin_root.resolve()
    try:
        findings = check_surface(root) + check_hook(root)
    except (OSError, ValueError, KeyError, IndexError, subprocess.SubprocessError) as exc:
        print(f"Install check failed: {exc}")
        return 1
    for finding in findings:
        print(finding)
    if findings:
        print("Use the runtime release package; see README Installation for recovery.")
        return 1
    print("PASS: skill discovery surface and direct hook execution.")
    print("Host activation/trust was NOT tested; use the live edit probe in README Installation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
