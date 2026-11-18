#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Run one full-catalog integration arm (issue #96) headlessly and archive it.

One arm is one host subprocess in a fresh temporary directory that holds only
the staged fixture. The plugin condition installs the runtime tree that
`scripts/build-release-tree.py` builds from HEAD: `--plugin-dir` on Claude Code,
`codex plugin add` into a fresh `CODEX_HOME` on Codex. The preregistration
(`docs/evidence/integration/2026-11-17-full-catalog/prereg.md`) defines the
cells, conditions, and scoring; this script only runs and archives.

Archived under --out as `<name>.prompt.txt`, `.command.json`, `.jsonl`
(the host's JSON event stream), `.stderr`, and `.manifest.json`, which records
host and model versions, the staged commit, and the observed skill route.

    uv run scripts/run_integration.py --cell I1 --host claude --condition plugin \\
        --name I1-claude-plugin-1 --out docs/evidence/integration/2026-11-17-full-catalog
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS = (
    "exploratory-data-analysis",
    "hypothesis-driven-analysis",
    "causal-identification-review",
    "decision-analysis",
)

S15 = REPO / "skills/hypothesis-driven-analysis/tests/fixtures/s15-assist-rollout"

CELLS: dict[str, tuple[Path, str]] = {
    "I1": (
        REPO / "skills/hypothesis-driven-analysis/tests/fixtures/s1-conversion",
        "How many orders in `{DATA}/orders.csv` were placed on 2026-06-10 (UTC)?",
    ),
    "I2": (
        REPO / "skills/hypothesis-driven-analysis/tests/fixtures/s5b-seam",
        "Here's two months of our API event logs (`{DATA}/events.csv`). "
        "Nobody has looked at it closely. Take a look, tell me what's going on, "
        "and if anything looks like a real problem, check whether it actually "
        "holds up before you tell me it's real.",
    ),
    "I3": (
        REPO / "skills/causal-identification-review/tests/fixtures/cs3-rollout",
        "We rolled out the new checkout flow to the West region on 2026-03-15; "
        "East stayed on the old flow. Median checkout completion time in West "
        "dropped afterwards. How much faster did the new flow make checkout? "
        "I need a number for the Q2 review. Data is in `{DATA}`.",
    ),
    "I4": (S15, ""),  # Scenario 15's prompt, from PROBLEM.md, data line rewritten
}


def cell_prompt(cell: str, data: Path) -> str:
    fixture, template = CELLS[cell]
    if cell == "I4":
        text = (fixture / "PROBLEM.md").read_text(encoding="utf-8")
        body = text.split("\n", 2)[2].strip()  # drop the title line
        body = body.replace("in this directory:", f"in `{data}`:")
        return body
    return template.replace("{DATA}", str(data))


def build_release(dest: Path) -> None:
    """The runtime tree an install fetches, built by the repo's own builder."""
    dirty = subprocess.run(
        [
            "git",
            "-C",
            str(REPO),
            "status",
            "--porcelain",
            "--",
            "skills",
            "hooks",
            "instruments",
            ".claude-plugin",
            ".codex-plugin",
            ".agents/plugins",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    if dirty.strip():
        raise SystemExit("plugin files differ from HEAD; commit before running an arm")
    subprocess.run(
        ["uv", "run", "-q", str(REPO / "scripts/build-release-tree.py"), str(dest)], check=True
    )


def install_codex_plugin(release: Path, env: dict[str, str]) -> str:
    log = []
    for cmd in (
        ["codex", "plugin", "marketplace", "add", str(release)],
        ["codex", "plugin", "add", "data-reasoning@data-reasoning"],
    ):
        r = subprocess.run(cmd, env=env, capture_output=True, text=True, check=False)
        log.append(f"$ {' '.join(cmd)}\nexit={r.returncode}\n{r.stdout}{r.stderr}")
        if r.returncode:
            raise SystemExit("\n".join(log))
    return "\n".join(log)


def observed_route(events: list[dict], host: str) -> list[str]:
    route: list[str] = []
    pat = re.compile(r"(" + "|".join(SKILLS) + r")/SKILL\.md")
    for text in _tool_inputs(events, host):
        for skill in SKILLS:
            if f"data-reasoning:{skill}" in text or text.strip('"') == skill:
                route.append(skill)
        for m in pat.finditer(text):
            route.append(m.group(1))
    return list(dict.fromkeys(route))


def _tool_inputs(events: list[dict], host: str):
    for ev in events:
        if host == "claude" and ev.get("type") == "assistant":
            for block in ev.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    yield json.dumps(block.get("input", {}))
        if host == "codex" and ev.get("type") in ("item.started", "item.completed"):
            item = ev.get("item", {})
            if item.get("type") in ("command_execution", "file_read", "mcp_tool_call"):
                yield json.dumps(item)


def final_message(events: list[dict], host: str) -> str:
    if host == "claude":
        for ev in reversed(events):
            if ev.get("type") == "result":
                return ev.get("result", "")
        return ""
    last = ""
    for ev in events:
        item = ev.get("item", {}) if ev.get("type") == "item.completed" else {}
        if item.get("type") == "agent_message":
            last = item.get("text", "")
    return last


def host_command(args: argparse.Namespace, base: Path, root: Path, prompt: str):
    """The host argv and environment for one arm, installing the plugin if asked."""
    env = dict(os.environ)
    release = Path(tempfile.mkdtemp(prefix="int-plugin-")) / "data-reasoning"
    if args.host == "claude":
        cmd = ["claude", "-p", prompt, "--model", "sonnet", "--output-format", "stream-json"]
        cmd += ["--verbose", "--setting-sources", "project"]
        cmd += ["--permission-mode", "bypassPermissions"]
        if args.condition == "plugin":
            build_release(release)
            cmd += ["--plugin-dir", str(release)]
        return cmd, env
    home = Path(tempfile.mkdtemp(prefix="int-codex-home-"))
    shutil.copy2(Path.home() / ".codex" / "auth.json", home / "auth.json")
    env["CODEX_HOME"] = str(home)
    if args.condition == "plugin":
        build_release(release)
        log = install_codex_plugin(release, env)
        base.with_suffix(".install.log").write_text(log, encoding="utf-8")
    cmd = ["codex", "exec", "--json", "--skip-git-repo-check", "-s", "workspace-write"]
    return [*cmd, "-C", str(root), prompt], env


def read_events(path: Path) -> list[dict]:
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        with contextlib.suppress(json.JSONDecodeError):
            events.append(json.loads(line))
    return events


def model_of(events: list[dict], stderr: str, host: str) -> str | None:
    if host == "codex":
        m = re.search(r"model:\s*(\S+)", stderr)
        return m.group(1) if m else None
    for ev in events:
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            return ev.get("model")
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", required=True, choices=sorted(CELLS))
    ap.add_argument("--host", required=True, choices=["claude", "codex"])
    ap.add_argument("--condition", required=True, choices=["plugin", "none"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--timeout", type=int, default=1800)
    args = ap.parse_args()

    ref = subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
    ).stdout.strip()
    args.out.mkdir(parents=True, exist_ok=True)
    base = args.out / args.name
    root = Path(tempfile.mkdtemp(prefix=f"int-{args.name}-"))
    data = root / "data"
    shutil.copytree(CELLS[args.cell][0], data)
    prompt = cell_prompt(args.cell, data)
    base.with_suffix(".prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    cmd, env = host_command(args, base, root, prompt)
    version = subprocess.run(
        [args.host, "--version"], check=False, capture_output=True, text=True
    ).stdout.strip()

    shown = [c if c != prompt else "<prompt.txt>" for c in cmd]
    base.with_suffix(".command.json").write_text(
        json.dumps({"cwd": str(root), "argv": shown}, indent=2) + "\n", encoding="utf-8"
    )
    start = time.monotonic()
    with base.with_suffix(".jsonl").open("w") as out, base.with_suffix(".stderr").open("w") as err:
        proc = subprocess.run(
            cmd,
            cwd=root,
            env=env,
            stdout=out,
            stderr=err,
            stdin=subprocess.DEVNULL,
            timeout=args.timeout,
            check=False,
        )
    duration = round(time.monotonic() - start)

    events = read_events(base.with_suffix(".jsonl"))
    model = model_of(events, base.with_suffix(".stderr").read_text(encoding="utf-8"), args.host)
    route = observed_route(events, args.host)
    base.with_suffix(".final.md").write_text(
        final_message(events, args.host) + "\n", encoding="utf-8"
    )
    manifest = {
        "name": args.name,
        "cell": args.cell,
        "host": args.host,
        "condition": args.condition,
        "skills_ref": ref,
        "host_version": version,
        "model": model,
        "exit": proc.returncode,
        "duration_s": duration,
        "observed_route": route,
        "ran_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    base.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{args.name}: exit={proc.returncode} model={model} route={route} dur={duration}s")


if __name__ == "__main__":
    main()
