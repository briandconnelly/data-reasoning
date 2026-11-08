#!/usr/bin/env python3
"""Run one arm of the supplied-numbers probe headlessly and archive it.

One arm is one `claude -p` subprocess with the Data Answer style active. The
plugin is staged by `scripts/build-release-tree.py` from the working tree, and
then its `output-styles/data-answer.md` is replaced with the style text at
`--style-ref`, so the pre and post arms differ only in that file. The arm's
cwd is a fresh empty directory; `--add-dir` names only the staged fixture
data. `--setting-sources project` and `--strict-mcp-config` keep user-level
settings, plugins, and connectors out; `--tools` omits Skill, so no skill can
be invoked and the style is the only plugin text in play.

Archived per arm beside this script: `<name>.prompt.txt`,
`<name>.command.json`, `<name>.jsonl`, `<name>.stderr`, `<name>.manifest.json`.
Follows the conventions of skills/hypothesis-driven-analysis/tests/run_arm.py.

    python3 run_probe.py --name f1-pre --fixture f1 --style-ref 76a8308
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
STYLE = "output-styles/data-answer.md"
TOOLS = ["Read", "Glob", "Grep", "Bash"]
SETTINGS = json.dumps({"outputStyle": "data-reasoning:Data Answer"})


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--fixture", required=True, choices=["f1", "f2", "f3", "f4"])
    ap.add_argument("--style-ref", required=True)
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--timeout", type=int, default=900)
    args = ap.parse_args()

    base = HERE / args.name
    if base.with_suffix(".jsonl").exists():
        sys.exit(f"refusing to overwrite {base}.jsonl")

    root = Path(tempfile.mkdtemp(prefix=f"probe-{args.name}-"))
    plugin = root / "plugin"
    subprocess.run(
        [sys.executable, str(REPO / "scripts" / "build-release-tree.py"), str(plugin)], check=True
    )
    style = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{args.style_ref}:{STYLE}"],
        capture_output=True,
        check=True,
    ).stdout
    (plugin / STYLE).write_bytes(style)
    data = root / "data"
    shutil.copytree(HERE / "fixtures" / f"{args.fixture}-data", data)
    work = root / "work"
    work.mkdir()

    prompt = (
        (HERE / "fixtures" / f"{args.fixture}.prompt.txt")
        .read_text(encoding="utf-8")
        .replace("{FIXTURE_PATH}", str(data))
    )
    base.with_suffix(".prompt.txt").write_text(prompt, encoding="utf-8")
    cmd = [
        "claude", "-p", prompt,
        "--model", args.model,
        "--output-format", "stream-json", "--verbose",
        "--setting-sources", "project",
        "--strict-mcp-config",
        "--plugin-dir", str(plugin),
        "--settings", SETTINGS,
        "--tools", *TOOLS,
        "--allowedTools", *TOOLS,
        "--add-dir", str(data),
    ]  # fmt: skip
    base.with_suffix(".command.json").write_text(
        json.dumps({"cwd": str(work), "argv": cmd}, indent=2) + "\n", encoding="utf-8"
    )
    started = datetime.now(UTC).isoformat()
    t0 = time.monotonic()
    with base.with_suffix(".jsonl").open("w") as out, base.with_suffix(".stderr").open("w") as err:
        try:
            exit_code = subprocess.run(
                cmd, stdout=out, stderr=err, cwd=work, timeout=args.timeout, check=False
            ).returncode
        except subprocess.TimeoutExpired:
            exit_code = -1
    duration = time.monotonic() - t0

    init: dict = {}
    result: dict = {}
    tool_uses = []
    for line in base.with_suffix(".jsonl").read_text(encoding="utf-8").splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            init = ev
        elif ev.get("type") == "assistant":
            for block in ev.get("message", {}).get("content", []) or []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tool_uses.append({"tool": block.get("name"), "input": block.get("input")})
        elif ev.get("type") == "result":
            result = ev
    hits = [
        f"tool call {i + 1}: {why}"
        for i, tu in enumerate(tool_uses)
        for why, bad in (("repository path", str(REPO)), ("a tests/ path", "/tests/"))
        if bad in json.dumps(tu["input"])
    ]
    manifest = {
        "name": args.name,
        "fixture": args.fixture,
        "started_utc": started,
        "duration_s": round(duration, 1),
        "exit_code": exit_code,
        "claude_version": init.get("claude_code_version"),
        "requested_model": args.model,
        "model": init.get("model"),
        "session_id": init.get("session_id"),
        "output_style_at_startup": init.get("output_style"),
        "plugins_at_startup": init.get("plugins"),
        "tools_at_startup": init.get("tools"),
        "mcp_servers_at_startup": init.get("mcp_servers"),
        "style_ref": args.style_ref,
        "style_sha256": sha(style),
        "fixture_files_sha256": {
            str(p.relative_to(data)): sha(p.read_bytes()) for p in sorted(data.rglob("*"))
        },
        "prompt_sha256": sha(prompt.encode()),
        "jsonl_sha256": sha(base.with_suffix(".jsonl").read_bytes()),
        "staging_root": str(root),
        "contaminated": hits,
        "tool_uses": tool_uses,
        "usage": result.get("usage"),
        "total_cost_usd": result.get("total_cost_usd"),
        "result_text": result.get("result"),
    }
    base.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"{args.name}: exit={exit_code} model={init.get('model')} "
        f"style={init.get('output_style')} tools={len(tool_uses)} contaminated={len(hits)}"
    )
    return 0 if exit_code == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
