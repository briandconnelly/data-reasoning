#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Run one integration arm headlessly and archive it.

Two suites share this harness, and each preregistration defines its cells,
conditions, and scoring; this script only runs and archives.

- I1-I4: the full-catalog suite (issue #96),
  `docs/evidence/integration/2026-11-17-full-catalog/prereg.md`. Its behaviour
  is unchanged by the representative suite: absolute data paths in the prompt,
  a workspace named after the arm, the host's model alias.
- R1, R2, X1-X3: the representative suite (issue #115),
  `docs/evidence/integration/representative-v1/prereg.md`. Before any host
  call these cells check that the fixture, prompt, prereg, and harness match
  HEAD and that the staged fixture bytes and prompt match the prereg's hashes;
  they need an explicit `--model`, run in a neutrally named workspace, and give
  the model a relative `data/` path, so the arm's name and condition never
  reach the prompt. R3 and R4 are placeholders and are refused at once.

One arm is one host subprocess in a fresh temporary directory that holds only
the staged fixture. The plugin condition installs the runtime tree that
`scripts/build-release-tree.py` builds from HEAD: `--plugin-dir` on Claude Code,
`codex plugin add` into a fresh `CODEX_HOME` on Codex.

Archived under --out as `<name>.prompt.txt`, `.command.json`, `.jsonl`
(the host's JSON event stream), `.stderr`, `.final.md`, and `.manifest.json`,
which records host version, requested and resolved model, the staged commit,
the observed skill route, and an execution `status` (`completed`, or
`invalid-execution: ...` on a timeout, a nonzero exit, a malformed line,
or no terminal success event, written even then). Representative cells also
record the prompt hash and per-file fixture digests. Every cell copies each file
the arm created or changed in its workspace into `<name>.workspace/` (I1-I4
since the wave-2 preregistration, `docs/evidence/integration/2026-11-wave2/`).

After the turn, from outside the arm, every cell also archives scratch files:
files under a system temp directory, outside the workspace and the harness's own
directories, that a tool call, tool output, or the final message names (or that
sit under a directory one names) and that were written after the arm started.
Each is copied to `<name>.scratch/<its absolute path>` and mapped in the
manifest's `scratch_files` with its digest. `named_paths` records every file
path the final message names, resolved against the arm's working directory,
with whether it exists and is readable and its digest. `--clear-scratch` then
removes the archived scratch originals so a later arm cannot read them.

    uv run scripts/run_integration.py --cell X2 --host claude --condition plugin \\
        --model claude-sonnet-4-5 --name X2-claude-plugin-1 \\
        --out docs/evidence/integration/representative-v1/arms
    uv run scripts/run_integration.py --cell X2 --host claude --condition plugin \\
        --name dry --out /tmp/unused --dry-run
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
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

# The representative suite (issue #115). Its preregistration,
# docs/evidence/integration/representative-v1/prereg.md, freezes these prompts
# by hash; a change here without a dated note there breaks the freeze.
REP = REPO / "docs/evidence/integration/representative-v1/fixtures"
CELLS.update(
    {
        "R1": (
            REP / "r-sales",
            "How many orders did the Riverside store take in March 2026? "
            "Our order export is `{DATA}/orders.csv`.",
        ),
        "R2": (
            REP / "r-sales",
            "Using `{DATA}/orders.csv`, what was the average order total at each "
            "store in February 2026? An order's total is unit_price times quantity.",
        ),
        "R3": (REP, ""),  # placeholder: awaits an owner-supplied user request
        "R4": (REP, ""),  # placeholder: awaits an owner-supplied user request
        "X1": (
            REP / "x1-supplier",
            "We have to pick one supplier for all 100,000 units next year: stay "
            "with Acme or move to Brightline. Brightline's trial batch, our Acme "
            "history, and the contract terms are in `{DATA}`. Brightline's trial "
            "had fewer defects than Acme usually has, and it is all we know about "
            "Brightline. Which supplier should we sign with?",
        ),
        "X2": (
            REP / "x2-forecast",
            "Our analyst built a model for daily support ticket volume; the notes, "
            "code, and two years of data (through September 30, 2026) are in "
            "`{DATA}`. They report under 4% error on held-out days. Today, with "
            "data through September, we set staffing for October, November, and "
            "December from each month's forecast total, and that works if the "
            "three monthly totals are within 10% of actual on average. Can we "
            "use it?",
        ),
        "X3": (
            REP / "x3-churn",
            "We have two candidate churn models scored on last quarter's holdout "
            "customers, with who actually churned: `{DATA}/holdout_scores.csv`. "
            "Next quarter our retention team will call the 500 customers the "
            "deployed model scores highest on one list like this one. Which model "
            "should we deploy?",
        ),
    }
)
PLACEHOLDERS = frozenset({"R3", "R4"})
REPRESENTATIVE = frozenset({"R1", "R2", "X1", "X2", "X3"})
PREREG = REPO / "docs/evidence/integration/representative-v1/prereg.md"
FROZEN_PATHS = (
    "docs/evidence/integration/representative-v1/prereg.md",
    "docs/evidence/integration/representative-v1/fixtures",
    "scripts/run_integration.py",
    "scripts/representative",
)
"""The frozen inputs: prereg, fixtures, and the harness that holds the prompts.
Arm outputs under representative-v1/arms/ are deliberately outside it, so a
replicate block runs without a commit after every arm."""


def data_path(cell: str, root: Path) -> Path:
    """What `{DATA}` renders as: relative for the representative suite, so the
    workspace path (and any name in it) never reaches the prompt."""
    return Path("data") if cell in REPRESENTATIVE else root / "data"


def file_digests(fixture: Path) -> dict[str, str]:
    return {
        str(f.relative_to(fixture)): hashlib.sha256(f.read_bytes()).hexdigest()
        for f in sorted(fixture.rglob("*"))
        if f.is_file()
    }


def prereg_hashes(cell: str, prereg: Path = PREREG) -> tuple[str, dict[str, str]]:
    """The prompt hash in the cell's own section and its fixture's file table rows."""
    text = prereg.read_text(encoding="utf-8")
    start = text.index(f"\n### {cell} \u2014")
    section = text[start : text.find("\n#", start + 1)]
    prompt = re.search(r"Prompt SHA-256: `([0-9a-f]{64})`", section)
    if not prompt:
        raise SystemExit(f"{cell}: the prereg section has no prompt hash")
    name = CELLS[cell][0].name
    rows = re.findall(rf"^\| `{re.escape(name)}/([^`]+)` \| `([0-9a-f]{{64}})` \|$", text, re.M)
    return prompt.group(1), dict(rows)


def verify_cell(cell: str, staged: Path, prereg: Path = PREREG) -> tuple[str, dict[str, str]]:
    """Refuse unless the staged fixture and the prompt match the prereg's hashes."""
    want_prompt, want_files = prereg_hashes(cell, prereg)
    got_prompt, got_files = prompt_sha256(cell), file_digests(staged)
    if got_prompt != want_prompt:
        raise SystemExit(f"{cell}: prompt hash {got_prompt} is not the prereg's {want_prompt}")
    if got_files != want_files:
        raise SystemExit(f"{cell}: staged fixture bytes differ from the prereg's hashes")
    return got_prompt, got_files


def require_clean(paths: tuple[str, ...] = FROZEN_PATHS, repo: Path = REPO) -> None:
    dirty = subprocess.run(
        ["git", "-C", str(repo), "status", "--porcelain", "--", *paths],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    if dirty.strip():
        raise SystemExit("fixtures, prompts, prereg, or harness differ from HEAD; commit first")


def cell_prompt(cell: str, data: Path) -> str:
    if cell in PLACEHOLDERS:
        raise SystemExit(f"{cell} is a placeholder: its prompt awaits the owner (see the prereg)")
    fixture, template = CELLS[cell]
    if cell == "I4":
        text = (fixture / "PROBLEM.md").read_text(encoding="utf-8")
        body = text.split("\n", 2)[2].strip()  # drop the title line
        body = body.replace("in this directory:", f"in `{data}`:")
        return body
    return template.replace("{DATA}", str(data))


def prompt_sha256(cell: str) -> str:
    """The hash the prereg freezes: the prompt with `{DATA}` left unexpanded."""
    return hashlib.sha256(cell_prompt(cell, Path("{DATA}")).encode("utf-8")).hexdigest()


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
    """The data-reasoning skills an arm loaded, in order, from what it asked to read.

    Only the request counts: a tool call's input (Claude Code) or a command's text (Codex).
    A command's output is never searched for skill names, because one SKILL.md names the
    others; it is read only to resolve a glob (`skills/*/SKILL.md`), and then only for the
    frontmatter `name:` line of each file the glob printed."""
    route: list[str] = []
    # A shell read may brace-expand several skills: skills/{a,b}/SKILL.md.
    pat = re.compile(r"(?:\{([^{}]*)\}|([\w-]+))/SKILL\.md")
    for text, output in _tool_requests(events, host):
        for skill in SKILLS:
            if f"data-reasoning:{skill}" in text or text.strip('"') == skill:
                route.append(skill)
        for m in pat.finditer(text):
            names = m.group(1).split(",") if m.group(1) is not None else [m.group(2)]
            route.extend(n for n in names if n in SKILLS)
        if GLOB_SKILL_READ.search(text):
            route.extend(n for n in FRONTMATTER_NAME.findall(output) if n in SKILLS)
    return [s for i, s in enumerate(route) if i == 0 or s != route[i - 1]]


# A glob metacharacter anywhere in the path token that ends in SKILL.md.
GLOB_SKILL_READ = re.compile(r"[^\s\"']*[*?\[][^\s\"']*SKILL\.md")
FRONTMATTER_NAME = re.compile(r"^name: ([\w-]+)\s*$", re.M)


def _tool_requests(events: list[dict], host: str):
    """(request text, output) per tool call; output is empty where none is recorded."""
    for ev in events:
        if host == "claude" and ev.get("type") == "assistant":
            for block in ev.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    yield json.dumps(block.get("input", {})), ""
        if host == "codex" and ev.get("type") == "item.completed":
            item = ev.get("item", {})
            if item.get("type") in ("command_execution", "file_read", "mcp_tool_call"):
                output = str(item.get("aggregated_output") or "")
                request = {k: v for k, v in item.items() if k not in OUTPUT_KEYS}
                yield json.dumps(request), output


OUTPUT_KEYS = {"aggregated_output", "output", "result", "content", "stdout", "stderr"}


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
        model = args.model or "sonnet"
        cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "stream-json"]
        cmd += ["--verbose", "--setting-sources", "project"]
        tools = "Read,Write,Edit,Bash,Glob,Grep,Skill"
        cmd += ["--tools", tools, "--allowedTools", tools]
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
    if args.model:
        cmd += ["-m", args.model]
    return [*cmd, "-C", str(root), prompt], env


def read_events(path: Path) -> list[dict]:
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        with contextlib.suppress(json.JSONDecodeError):
            events.append(json.loads(line))
    return events


def model_of(events: list[dict], codex_home: str | None, host: str) -> str | None:
    if host == "codex":
        # codex exec --json omits the model; the session rollout records it.
        models = set()
        for f in Path(codex_home or "").glob("sessions/**/*.jsonl"):
            models.update(re.findall(r'"model":"([^"]+)"', f.read_text(encoding="utf-8")))
        return ",".join(sorted(models)) or None
    for ev in events:
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            return ev.get("model")
    return None


def terminal_success(events: list[dict], host: str) -> bool:
    """The host's own successful-completion event closes the transcript: Claude
    Code's stream-json ends in a `result` event with subtype `success`, and
    `codex exec --json` in `turn.completed` (as every archived 2026-11-17 arm does)."""
    if not events:
        return False
    last = events[-1]
    if host == "claude":
        return (
            last.get("type") == "result"
            and last.get("subtype") == "success"
            and not last.get("is_error")
        )
    return last.get("type") == "turn.completed"


def execution_status(path: Path, host: str, code: int | None) -> str:
    """`completed` only on exit 0, every line parsing, and a terminal success event."""
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    events = []
    for line in lines:
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            return "invalid-execution: malformed transcript line"
    if code != 0:
        return f"invalid-execution: host exit {code}"
    if not events:
        return "invalid-execution: empty transcript"
    if not terminal_success(events, host):
        return "invalid-execution: no terminal success event"
    return "completed"


def run_host(cmd, root: Path, env: dict[str, str], base: Path, args: argparse.Namespace):
    """Run the host; anything short of a clean, successful run is an invalid
    execution with an explicit status, and everything is still archived."""
    start = time.monotonic()
    status, code = "completed", None
    with base.with_suffix(".jsonl").open("w") as out, base.with_suffix(".stderr").open("w") as err:
        try:
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
            code = proc.returncode
        except subprocess.TimeoutExpired:
            status = f"invalid-execution: timeout after {args.timeout}s"
    if status == "completed":
        status = execution_status(base.with_suffix(".jsonl"), args.host, code)
    return code, status, round(time.monotonic() - start)


def archive_workspace(root: Path, dest: Path, staged: dict[str, str]) -> list[str]:
    """Copy every file the arm created or changed, staged fixture files excepted; the
    prereg scores records wherever the arm wrote them."""
    kept = []
    for f in sorted(root.rglob("*")):
        rel = f.relative_to(root)
        if not f.is_file():
            continue
        in_data = rel.parts[0] == "data" and len(rel.parts) > 1
        key = str(Path(*rel.parts[1:])) if in_data else None
        unchanged = in_data and staged.get(key) == hashlib.sha256(f.read_bytes()).hexdigest()
        if not unchanged:
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest / rel)
            kept.append(str(rel))
    return kept


# Where an arm's scratch writes land outside its workspace: the system temp
# directories. A path elsewhere (a home directory, the repository) is never
# walked or copied.
TEMP_ROOTS = tuple(
    dict.fromkeys(Path(p).resolve() for p in ("/tmp", tempfile.gettempdir()) if Path(p).is_dir())
)
# Directories the harness itself creates for an arm (the built plugin and the
# Codex home), never the arm's own writes.
HARNESS_DIRS = ("int-plugin-", "int-codex-home-")
PATH_TOKEN = re.compile(r"(?<![\w.~-])(/[^\s\"'`<>|;&()*?\[\]{}$,\\]+)")
NAMED_TOKEN = re.compile(
    r"(?<![\w~/:.-])((?:/|\.{1,2}/)?[\w.~-]+(?:/[\w.~-]+)*"
    r"\.(?:md|txt|csv|tsv|json|ya?ml|py|ipynb|html|log|sql))(?![\w/-])"
)


def _under(path: Path, roots: tuple[Path, ...]) -> Path | None:
    return next((r for r in roots if path != r and path.is_relative_to(r)), None)


def mentioned_paths(events: list[dict], host: str, final: str) -> set[str]:
    """Absolute paths any tool request, tool output, or the final message names.
    Output is searched here (not for routes): a `mktemp -d` directory is often
    known only from what the command printed."""
    texts = [final]
    for request, output in _tool_requests(events, host):
        texts += [request.replace("\\n", "\n"), output]
    return {m.rstrip(".:") for t in texts for m in PATH_TOKEN.findall(t)}


def scratch_files(
    paths: set[str], root: Path, since: float, temp_roots: tuple[Path, ...] | None = None
) -> list[Path]:
    """Files under a temp root, outside the workspace and the harness's own
    directories, that a named path points at (or that sit under a named
    directory) and that were written at or after the arm started."""
    temp_roots = temp_roots or TEMP_ROOTS
    root = root.resolve()
    found: set[Path] = set()
    for raw in paths:
        p = Path(raw)
        with contextlib.suppress(OSError):
            p = p.resolve()
        temp = _under(p, temp_roots)
        if temp is None or p == root or p.is_relative_to(root):
            continue
        if any(part.startswith(HARNESS_DIRS) for part in p.relative_to(temp).parts):
            continue
        candidates = [p] if p.is_file() else sorted(p.rglob("*")) if p.is_dir() else []
        for f in candidates:
            with contextlib.suppress(OSError):
                if f.is_file() and f.stat().st_mtime >= since and not f.is_relative_to(root):
                    found.add(f)
    return sorted(found)


def archive_scratch(files: list[Path], dest: Path) -> dict[str, dict]:
    """Copy each scratch file to `dest`, keeping its absolute path below it, and
    return the mapping from original path to archived copy and digest."""
    mapping = {}
    for f in files:
        rel = Path(*f.parts[1:])
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest / rel)
        mapping[str(f)] = {
            "archived": str(Path(dest.name) / rel),
            "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
        }
    return mapping


def named_paths(final: str, root: Path) -> list[dict]:
    """Every file path the final message names, checked from outside the arm
    after the turn: whether it resolves (absolute, or relative to the arm's
    working directory) to a regular file the harness user can read, and its
    digest, so a scorer can match it to a record's archived bytes."""
    out = []
    for named in dict.fromkeys(NAMED_TOKEN.findall(final)):
        p = Path(named).expanduser()
        p = p if p.is_absolute() else root / p
        exists = p.is_file()
        readable = exists and os.access(p, os.R_OK)
        digest = hashlib.sha256(p.read_bytes()).hexdigest() if readable else None
        out.append(
            {
                "named": named,
                "resolved": str(p),
                "exists": exists,
                "readable": readable,
                "sha256": digest,
            }
        )
    return out


def clear_scratch(files: list[Path], temp_roots: tuple[Path, ...] | None = None) -> None:
    """Remove an arm's archived scratch originals and any directory they leave
    empty, up to the temp root, so the next arm cannot read or append to them."""
    temp_roots = temp_roots or TEMP_ROOTS
    for f in files:
        f.unlink(missing_ok=True)
        parent, temp = f.parent, _under(f, temp_roots)
        while temp is not None and parent != temp and parent.is_relative_to(temp):
            try:
                parent.rmdir()
            except OSError:
                break
            parent = parent.parent


def temp_entries(temp_roots: tuple[Path, ...] | None = None) -> set[str]:
    """The top-level entries of each temp root, before an arm starts."""
    entries: set[str] = set()
    for r in temp_roots or TEMP_ROOTS:
        with contextlib.suppress(OSError):
            entries.update(str(n) for n in Path(r).iterdir())
    return entries


def capture(
    files: list[Path], named: list[dict], before: set[str], dest_base: Path, clear: bool
) -> dict:
    """The manifest's capture fields: each scratch file's archived copy, digest,
    and whether its top-level temp entry predates the arm; and the named-path
    check, which `named` already holds because it ran before any clearing."""
    scratch = archive_scratch(files, dest_base.with_suffix(".scratch"))
    for path, entry in scratch.items():
        temp = _under(Path(path), TEMP_ROOTS)
        top = str(temp / Path(path).relative_to(temp).parts[0]) if temp else None
        entry["top_entry_preexisted"] = top in before
    if clear:
        clear_scratch(files)
    return {"scratch_files": scratch, "named_paths": named, "scratch_cleared": clear}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", required=True, choices=sorted(CELLS))
    ap.add_argument("--host", required=True, choices=["claude", "codex"])
    ap.add_argument("--condition", required=True, choices=["plugin", "none"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument(
        "--model",
        help="pin the host model id (required for representative cells; I1-I4 default to "
        "Claude's `sonnet` alias and Codex's default)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="stage the fixture, print the prompt and its hash, and stop before any host call",
    )
    ap.add_argument(
        "--clear-scratch",
        action="store_true",
        help="after archiving, remove the arm's scratch files outside its workspace so a "
        "later arm cannot read or append to them",
    )
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.cell in PLACEHOLDERS:
        raise SystemExit(
            f"{args.cell} is a placeholder: its prompt awaits the owner (see the prereg)"
        )
    representative = args.cell in REPRESENTATIVE
    if args.dry_run:
        root = Path(tempfile.mkdtemp(prefix="int-arm-"))
        shutil.copytree(CELLS[args.cell][0], root / "data")
        digest = prompt_sha256(args.cell)
        if representative:
            verify_cell(args.cell, root / "data")
        prompt = cell_prompt(args.cell, data_path(args.cell, root))
        print(f"cell={args.cell} sha256={digest} staged={root / 'data'}")
        print(prompt)
        return
    if representative and not args.model:
        raise SystemExit(f"{args.cell}: pass --model; the prereg pins one model id per host")
    if representative:
        require_clean()

    ref = subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
    ).stdout.strip()
    args.out.mkdir(parents=True, exist_ok=True)
    base = args.out / args.name
    prefix = "int-arm-" if representative else f"int-{args.name}-"
    root = Path(tempfile.mkdtemp(prefix=prefix))
    data = root / "data"
    shutil.copytree(CELLS[args.cell][0], data)
    integrity = {}
    if representative:
        digest, files = verify_cell(args.cell, data)
        integrity = {"prompt_sha256": digest, "fixture_sha256": files}
    prompt = cell_prompt(args.cell, data_path(args.cell, root))
    base.with_suffix(".prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    cmd, env = host_command(args, base, root, prompt)
    version = subprocess.run(
        [args.host, "--version"], check=False, capture_output=True, text=True
    ).stdout.strip()

    shown = [c if c != prompt else "<prompt.txt>" for c in cmd]
    base.with_suffix(".command.json").write_text(
        json.dumps({"cwd": str(root), "argv": shown}, indent=2) + "\n", encoding="utf-8"
    )
    staged = integrity.get("fixture_sha256") or file_digests(data)
    before, since = temp_entries(), time.time() - 1
    code, status, duration = run_host(cmd, root, env, base, args)

    events = read_events(base.with_suffix(".jsonl"))
    model = model_of(events, env.get("CODEX_HOME"), args.host)
    route = observed_route(events, args.host)
    final = final_message(events, args.host)
    base.with_suffix(".final.md").write_text(final + "\n", encoding="utf-8")
    # Both run from outside the arm, after the turn, and before any clearing.
    captured = capture(
        scratch_files(mentioned_paths(events, args.host, final), root, since),
        named_paths(final, root),
        before,
        base,
        clear=args.clear_scratch,
    )
    manifest = {
        "name": args.name,
        "cell": args.cell,
        "host": args.host,
        "condition": args.condition,
        "skills_ref": ref,
        "host_version": version,
        "requested_model": args.model,
        "model": model,
        "exit": code,
        "status": status,
        "duration_s": duration,
        "observed_route": route,
        "ran_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    manifest |= integrity
    manifest["workspace_files"] = archive_workspace(root, base.with_suffix(".workspace"), staged)
    manifest["data_modified"] = file_digests(data) != staged
    manifest |= captured
    base.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{args.name}: {status} exit={code} model={model} route={route} dur={duration}s")


if __name__ == "__main__":
    main()
