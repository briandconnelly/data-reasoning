#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Run one baseline, pre-edit, or with-skill arm headlessly and archive it.

One arm is one `claude -p` subprocess. Everything the arm may read is staged
into a fresh directory outside the repository: the fixture directory (or file)
and, for a skill arm, a standalone copy of the skill directory without its
`tests/` tree. The arm's cwd is that staging root, `--add-dir` names it and
nothing else, and the prompt names only staged paths, so neither arm has a
path to the repository, its scenario catalogs, its run archive, or -- for a
baseline -- the skill. `--setting-sources project` keeps the machine's
user-level settings and plugins, including any installed release of this
plugin and its hook, out of the arm.

Bash is not a filesystem sandbox, so after the run every tool call is scanned
for the repository path, any other `SKILL.md`, and any `tests/` path; a hit is
recorded as `contaminated` in the manifest, and the preregistration says such
an arm is void. The `system` init event's tool list is archived as the
startup inventory, so a no-file-tools arm (`--tools Read,Glob,Grep`) can be
checked for what it was actually given.

Archived per arm under --out: `<name>.prompt.txt`, `<name>.command.json`,
`<name>.jsonl` (the stream-json transcript), `<name>.stderr`,
`<name>.manifest.json`, and a copy of everything the arm wrote to its scratch
directory under `<name>.scratch/`. A pre-edit arm stages the skill from a git
ref (`--skill-ref main`) so the same harness measures old and new wording.

    uv run skills/hypothesis-driven-analysis/tests/run_arm.py \
        --name s9-post --prompt-file prompts/s9.txt \
        --skill hypothesis-driven-analysis \
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
# {FIXTURE_PATH} in the scenario prompt is replaced with the staged path.
FRAME = "\n".join(
    [
        "You are the main agent on a data-analysis task for a user.",
        "{SKILL_LINES}",
        "The user's request:",
        "",
        '"{SCENARIO_PROMPT}"',
        "",
        "Write any working files you produce (notes, logs, records, intermediate results) "
        "to {SCRATCH_DIR}.",
        "Read only what the request and these instructions name; do not read anything else "
        "on this machine.",
        "Your final message is your report to the user.",
        "",
    ]
)

SKILL_LINES = "\n".join(
    [
        "",
        "A skill is installed. Its full instructions live at:",
        "{SKILL_PATH}",
        "",
        "Read that file and follow it as your working method; its references live beside it.",
        "",
    ]
)

DEFAULT_TOOLS = "Read,Write,Edit,Bash,Glob,Grep"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def hash_tree(root: Path) -> dict[str, str]:
    """sha256 of every file under `root` (or of `root` itself), keyed by path
    relative to `root`'s parent."""
    files = sorted(x for x in root.rglob("*") if x.is_file()) if root.is_dir() else [root]
    return {str(f.relative_to(root.parent)): sha256_bytes(f.read_bytes()) for f in files}


def stage_skill(skill: str, ref: str | None, dest: Path) -> Path:
    """Copy `skills/<skill>/` minus `tests/` into `dest`, from the working
    tree or from a git ref."""
    target = dest / skill
    if ref is None:
        src = REPO / "skills" / skill
        shutil.copytree(src, target, ignore=shutil.ignore_patterns("tests", "__pycache__", "*.pyc"))
    else:
        target.mkdir(parents=True)
        archive = subprocess.run(
            ["git", "-C", str(REPO), "archive", "--format=tar", ref, f"skills/{skill}"],
            capture_output=True,
            check=True,
        ).stdout
        subprocess.run(
            ["tar", "-x", "--strip-components=2", "-C", str(target), "--exclude", "tests"],
            input=archive,
            check=True,
        )
        shutil.rmtree(target / "tests", ignore_errors=True)
    return target


def scan(jsonl: Path) -> dict:
    model = ""
    session = ""
    init_tools: list[str] = []
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
            init_tools = ev.get("tools", init_tools) or init_tools
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
                            "input": json.dumps(inp)[:600],
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
        "init_tools": init_tools,
        "tool_uses": tool_uses,
        "assistant_texts": texts,
        "result_text": result_text,
        "usage": usage,
    }


def contamination(tool_uses: list[dict], staged_skill: Path | None) -> list[str]:
    """Tool calls that reach outside the staged tree: the repository, any
    SKILL.md other than the staged one, or any tests/ path."""
    hits = []
    for tu in tool_uses:
        text = tu["input"]
        if str(REPO) in text:
            hits.append(f"ordinal {tu['ordinal']}: repository path")
        if "SKILL.md" in text and (staged_skill is None or str(staged_skill) not in text):
            hits.append(f"ordinal {tu['ordinal']}: SKILL.md outside the staged skill")
        if "/tests/" in text:
            hits.append(f"ordinal {tu['ordinal']}: a tests/ path")
    return hits


def main() -> int:  # noqa: PLR0915 -- one linear pass: stage, run, archive
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--prompt-file", required=True, type=Path)
    ap.add_argument("--skill", default=None, help="skill directory name for a skill arm")
    ap.add_argument("--skill-ref", default=None, help="git ref to stage the skill from")
    ap.add_argument("--fixture", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--timeout", type=int, default=1500)
    ap.add_argument("--tools", default=DEFAULT_TOOLS, help="the built-in tools the arm is given")
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    base = args.out / args.name
    if base.with_suffix(".jsonl").exists():
        sys.exit(f"refusing to overwrite {base}.jsonl; pick a new --name")

    root = Path(tempfile.mkdtemp(prefix=f"arm-{args.name}-"))
    staged_fixture = root / "data" / args.fixture.name
    if args.fixture.is_dir():
        shutil.copytree(args.fixture, staged_fixture)
    else:
        staged_fixture.parent.mkdir(parents=True)
        shutil.copy2(args.fixture, staged_fixture)
    scratch = root / "work"
    scratch.mkdir()
    staged_skill = stage_skill(args.skill, args.skill_ref, root / "skills") if args.skill else None

    skill_lines = ""
    if staged_skill:
        skill_lines = SKILL_LINES.replace("{SKILL_PATH}", str(staged_skill / "SKILL.md"))
    scenario = (
        args.prompt_file.read_text(encoding="utf-8")
        .strip()
        .replace("{FIXTURE_PATH}", str(staged_fixture))
    )
    prompt = (
        FRAME.replace("{SKILL_LINES}", skill_lines)
        .replace("{SCENARIO_PROMPT}", scenario)
        .replace("{SCRATCH_DIR}", str(scratch))
    )
    base.with_suffix(".prompt.txt").write_text(prompt, encoding="utf-8")

    tools = args.tools.split(",")
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
        "--tools",
        *tools,
        "--allowedTools",
        *tools,
        "--add-dir",
        str(root),
    ]
    base.with_suffix(".command.json").write_text(
        json.dumps({"cwd": str(root), "argv": cmd}, indent=2) + "\n", encoding="utf-8"
    )
    started = datetime.now(UTC).isoformat()
    t0 = time.monotonic()
    with base.with_suffix(".jsonl").open("w") as out, base.with_suffix(".stderr").open("w") as err:
        try:
            proc = subprocess.run(
                cmd, stdout=out, stderr=err, cwd=root, timeout=args.timeout, check=False
            )
            exit_code = proc.returncode
        except subprocess.TimeoutExpired:
            exit_code = -1
    duration = time.monotonic() - t0

    written = sorted(x for x in scratch.rglob("*") if x.is_file())
    if written:
        shutil.copytree(scratch, args.out / f"{args.name}.scratch", dirs_exist_ok=True)

    info = scan(base.with_suffix(".jsonl"))
    hits = contamination(info["tool_uses"], staged_skill)
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
        "tools_requested": tools,
        "tools_at_startup": info["init_tools"],
        "skill": args.skill,
        "skill_ref": args.skill_ref or "working-tree",
        "skill_files_sha256": hash_tree(staged_skill) if staged_skill else None,
        "fixture": str(args.fixture),
        "fixture_files_sha256": hash_tree(staged_fixture),
        "prompt_sha256": sha256_bytes(prompt.encode()),
        "jsonl_sha256": sha256_bytes(base.with_suffix(".jsonl").read_bytes()),
        "staging_root": str(root),
        "files_written": [str(p.relative_to(scratch)) for p in written],
        "files_written_sha256": {
            str(p.relative_to(scratch)): sha256_bytes(p.read_bytes()) for p in written
        },
        "contaminated": hits,
        "tool_uses": info["tool_uses"],
        "usage": info["usage"],
        "result_text": info["result_text"],
    }
    base.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"{args.name}: exit={exit_code} model={info['model']} tools={len(info['tool_uses'])} "
        f"files={len(written)} dur={duration:.0f}s contaminated={len(hits)} "
        f"tokens_out={info['usage'].get('output_tokens')}"
    )
    return 0 if exit_code == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
