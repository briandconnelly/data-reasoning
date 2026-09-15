#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Run one baseline or with-skill arm headlessly and archive its transcript.

One arm is one `claude -p` subprocess. The scenario prompt is wrapped in a
fixed frame (below) that names the scratch directory, forbids reading any
`tests/` tree, and -- for a with-skill arm -- names the SKILL.md to read and
follow. `--setting-sources project` keeps the machine's user-level plugins,
including any installed release of this plugin, out of the arm, so a baseline
arm has no skill and a with-skill arm has exactly the working-tree wording it
is told to read. The arm's cwd is its scratch directory, outside the repo, so
the repo's own AGENTS.md does not load.

Archived per arm under --out: `<name>.prompt.txt`, `<name>.jsonl` (the
stream-json transcript), `<name>.stderr`, `<name>.manifest.json` (tool-call
manifest with ordinals, final text, model, token usage, sha256 of prompt,
transcript, and every fixture file named), and a copy of everything the arm
wrote to its scratch directory under `<name>.scratch/`.

    uv run skills/hypothesis-driven-analysis/tests/run_arm.py \
        --name s9-with-skill --prompt-file prompt.txt \
        --skill skills/hypothesis-driven-analysis/SKILL.md \
        --fixture skills/hypothesis-driven-analysis/tests/fixtures/s9-ab \
        --out runs/artifacts/2026-09-15-remediation-wave
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

REPO = Path(__file__).resolve().parents[3]

# Verbatim frame; long lines are split with implicit concatenation only.
FRAME = "\n".join(
    [
        "You are the main agent on a data-analysis task for a user.",
        "{SKILL_LINES}",
        "The user's request:",
        "",
        '"{SCENARIO_PROMPT}"',
        "",
        "Write any working files you produce (notes, logs, records, intermediate results) "
        "to {SCRATCH_DIR} — do not write anywhere inside {REPO}.",
        "Do not read anything under a `tests/` directory inside {REPO} other than the "
        "fixture path(s) the request names.",
        "Your final message is your report to the user.",
        "",
    ]
)

SKILL_LINES = """
A skill is installed. Its full instructions live at:
{SKILL_PATH}

Read that file and follow it as your working method.
"""


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fixture_hashes(paths: list[Path]) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in paths:
        files = sorted(x for x in p.rglob("*") if x.is_file()) if p.is_dir() else [p]
        for f in files:
            out[str(f.relative_to(REPO)) if f.is_relative_to(REPO) else str(f)] = sha256_bytes(
                f.read_bytes()
            )
    return out


def scan(jsonl: Path) -> dict:
    model = ""
    session = ""
    tool_uses: list[dict] = []
    texts: list[str] = []
    usage: dict = {}
    result_text = None
    ordinal = 0
    for line in jsonl.read_text(encoding="utf-8").splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = ev.get("type")
        if kind == "system":
            model = ev.get("model", "") or model
            session = ev.get("session_id", "") or session
        elif kind == "assistant":
            for block in ev.get("message", {}).get("content", []) or []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    ordinal += 1
                    inp = block.get("input", {}) or {}
                    tool_uses.append(
                        {
                            "ordinal": ordinal,
                            "tool": block.get("name"),
                            "file_path": inp.get("file_path"),
                            "command": (inp.get("command") or "")[:400] or None,
                            "pattern": inp.get("pattern"),
                        }
                    )
                elif block.get("type") == "text":
                    texts.append(block.get("text", ""))
        elif kind == "result":
            result_text = ev.get("result")
            usage = ev.get("usage", {}) or {}
            usage["total_cost_usd"] = ev.get("total_cost_usd")
            usage["duration_ms"] = ev.get("duration_ms")
            usage["num_turns"] = ev.get("num_turns")
    return {
        "model": model,
        "session_id": session,
        "tool_uses": tool_uses,
        "assistant_texts": texts,
        "result_text": result_text,
        "usage": usage,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--prompt-file", required=True, type=Path)
    ap.add_argument("--skill", type=Path, default=None, help="SKILL.md path for a with-skill arm")
    ap.add_argument("--fixture", type=Path, action="append", default=[])
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--timeout", type=int, default=1500)
    ap.add_argument(
        "--allowed-tools",
        default="Read,Write,Edit,Bash,Glob,Grep",
        help="comma-separated; a no-file-tools arm passes Read,Glob,Grep",
    )
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    base = args.out / args.name
    if (base.with_suffix(".jsonl")).exists():
        sys.exit(f"refusing to overwrite {base}.jsonl; pick a new --name")

    scratch = Path(tempfile.mkdtemp(prefix=f"arm-{args.name}-"))
    skill_lines = ""
    if args.skill:
        skill_lines = SKILL_LINES.replace("{SKILL_PATH}", str(args.skill.resolve()))
    prompt = (
        FRAME.replace("{SKILL_LINES}", skill_lines)
        .replace("{SCENARIO_PROMPT}", args.prompt_file.read_text(encoding="utf-8").strip())
        .replace("{SCRATCH_DIR}", str(scratch))
        .replace("{REPO}", str(REPO))
    )
    base.with_suffix(".prompt.txt").write_text(prompt, encoding="utf-8")

    cmd = [
        "claude",
        "-p",
        prompt,
        "--model",
        args.model,
        "--output-format",
        "stream-json",
        "--verbose",
        "--setting-sources",
        "project",
        "--allowedTools",
        *args.allowed_tools.split(","),
        "--add-dir",
        str(REPO),
    ]
    started = datetime.now(UTC).isoformat()
    t0 = time.monotonic()
    with base.with_suffix(".jsonl").open("w") as out, base.with_suffix(".stderr").open("w") as err:
        try:
            proc = subprocess.run(
                cmd, stdout=out, stderr=err, cwd=scratch, timeout=args.timeout, check=False
            )
            exit_code = proc.returncode
        except subprocess.TimeoutExpired:
            exit_code = -1
    duration = time.monotonic() - t0

    written = sorted(x for x in scratch.rglob("*") if x.is_file())
    scratch_copy = args.out / f"{args.name}.scratch"
    if written:
        shutil.copytree(scratch, scratch_copy, dirs_exist_ok=True)

    info = scan(base.with_suffix(".jsonl"))
    manifest = {
        "name": args.name,
        "started_utc": started,
        "duration_s": round(duration, 1),
        "exit_code": exit_code,
        "claude_version": subprocess.run(
            ["claude", "--version"], capture_output=True, text=True, check=False
        ).stdout.strip(),
        "requested_model": args.model,
        "model": info["model"],
        "session_id": info["session_id"],
        "allowed_tools": args.allowed_tools.split(","),
        "skill": str(args.skill.resolve()) if args.skill else None,
        "skill_sha256": sha256_bytes(args.skill.read_bytes()) if args.skill else None,
        "prompt_sha256": sha256_bytes(prompt.encode()),
        "jsonl_sha256": sha256_bytes(base.with_suffix(".jsonl").read_bytes()),
        "fixtures": fixture_hashes(args.fixture),
        "scratch_dir": str(scratch),
        "files_written": [str(p.relative_to(scratch)) for p in written],
        "files_written_sha256": {
            str(p.relative_to(scratch)): sha256_bytes(p.read_bytes()) for p in written
        },
        "tool_uses": info["tool_uses"],
        "usage": info["usage"],
        "result_text": info["result_text"],
    }
    base.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"{args.name}: exit={exit_code} model={info['model']} tools={len(info['tool_uses'])} "
        f"files={len(written)} dur={duration:.0f}s tokens_out={info['usage'].get('output_tokens')}"
    )
    return 0 if exit_code == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
