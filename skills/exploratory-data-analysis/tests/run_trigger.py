"""Trigger-scenario harness for the EDA/HDA two-skill catalog seam check.

Measures prompted dispatch: which skill an arm declares (via a machine-readable
ROUTE token) and consults when both skill catalog entries are presented in the
prompt. This is not deployment activation — each arm is one ``claude -p``
subprocess given the catalog text directly, whose stream-json transcript is
archived as JSONL; a detector then extracts the declared route and SKILL.md
reads into a TSV row.

Scenario definitions and scoring rules live in ``tests/scenarios.md``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

REPO = Path("/Users/bdc/projects/data-reasoning").resolve()
EDA_SKILL = REPO / "skills/exploratory-data-analysis/SKILL.md"
HDA_SKILL = REPO / "skills/hypothesis-driven-analysis/SKILL.md"

SCENARIOS: dict[str, str] = {
    "t13": "Tell me about the Northgate Clinic account.",
    "t14": "Why did the Northgate Clinic account's spend drop last quarter?",
    "c-eda": (
        "I have a CSV of library checkout events. What's in this data — "
        "profile it, anything interesting or anomalous?"
    ),
    "c-hda": (
        "Our checkout conversion rate dropped 20% last month. Why did it drop — what's driving it?"
    ),
    "c-none": "Convert 100 miles to kilometers.",
}

EDA_CATALOG_ENTRY = "**exploratory-data-analysis**\nDescription: {EDA_DESCRIPTION}"
HDA_CATALOG_ENTRY = "**hypothesis-driven-analysis**\nDescription: {HDA_DESCRIPTION}"
EDA_PATH_LINE = (
    "- exploratory-data-analysis: /Users/bdc/projects/data-reasoning"
    "/skills/exploratory-data-analysis/SKILL.md"
)
HDA_PATH_LINE = (
    "- hypothesis-driven-analysis: /Users/bdc/projects/data-reasoning"
    "/skills/hypothesis-driven-analysis/SKILL.md"
)

# Verbatim dispatch-prompt template; long lines are split with implicit
# string concatenation only, so the joined text is exactly the template.
# {CATALOG_ENTRIES} and {CATALOG_PATHS} are filled in the per-rep catalog
# order (eda-first or hda-first).
PROMPT_TEMPLATE = "\n".join(
    [
        "You are the main agent on a data-analysis task for a user.",
        "",
        "Two skills are installed. Their catalog entries:",
        "",
        "{CATALOG_ENTRIES}",
        "",
        "Each skill's full instructions live at:",
        "{CATALOG_PATHS}",
        "",
        "If a skill applies to the user's request, read its SKILL.md and follow it "
        "as your working method. If none applies, proceed without one.",
        "",
        "Before your first tool call — or, if you make no tool calls, at the start "
        "of your reply — output a single line in exactly this form: "
        "`ROUTE: exploratory-data-analysis` or `ROUTE: hypothesis-driven-analysis` "
        "or `ROUTE: none`. Then give one or two sentences explaining why.",
        "",
        "The user's request:",
        "",
        '"{SCENARIO_PROMPT}"',
        "",
        "Write any working files you produce (notes, logs, intermediate results) "
        "to {SCRATCH_DIR} — do not write anywhere inside "
        "/Users/bdc/projects/data-reasoning.",
        "",
        "Do not read anything under /Users/bdc/projects/data-reasoning"
        "/skills/exploratory-data-analysis/tests/ or "
        "/Users/bdc/projects/data-reasoning/skills/hypothesis-driven-analysis"
        "/tests/.",
        "",
        "Your final message is your report to the user.",
    ]
)

ROUTE_RE = re.compile(
    r"^\s*ROUTE:\s*(exploratory-data-analysis|hypothesis-driven-analysis|none)\s*$",
    re.MULTILINE,
)
ROUTE_MAP = {
    "exploratory-data-analysis": "eda",
    "hypothesis-driven-analysis": "hda",
    "none": "none",
}

DESC_MIN_CHARS = 900
DESC_MAX_CHARS = 1024

SUFFIX_RE = re.compile(r"^[A-Za-z0-9_-]+$")

TSV_COLUMNS = [
    "scenario",
    "rep",
    "suffix",
    "catalog_order",
    "started_utc",
    "duration_s",
    "exit_code",
    "model",
    "session_id",
    "route",
    "valid",
    "invalid_reason",
    "read_eda_skill",
    "read_hda_skill",
    "wrote_files_count",
    "prompt_sha256",
    "jsonl_sha256",
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_description(skill_md: Path) -> str:
    """Parse the single-quoted YAML ``description:`` scalar from a SKILL.md."""
    text = skill_md.read_text(encoding="utf-8")
    marker = "\ndescription: '"
    start = text.find(marker)
    if start < 0:
        sys.exit(f"FATAL: no single-quoted description scalar in {skill_md}")
    i = start + len(marker)
    chars: list[str] = []
    n = len(text)
    closed = False
    while i < n:
        c = text[i]
        if c == "'":
            if i + 1 < n and text[i + 1] == "'":
                chars.append("'")
                i += 2
                continue
            closed = True
            break
        chars.append(c)
        i += 1
    raw = "".join(chars)
    if not closed or "\n---" in raw:
        sys.exit(f"FATAL: unterminated description scalar in {skill_md}")
    desc = re.sub(r"\n[ \t]*", " ", raw).strip()
    if not DESC_MIN_CHARS <= len(desc) <= DESC_MAX_CHARS:
        sys.exit(
            f"FATAL: description in {skill_md} is {len(desc)} chars; "
            f"expected {DESC_MIN_CHARS}-{DESC_MAX_CHARS}"
        )
    return desc


def catalog_order_for_rep(order: str, rep: int) -> str:
    """Resolve --order to a concrete per-rep catalog order."""
    if order == "alternate":
        return "eda-first" if rep % 2 == 1 else "hda-first"
    return order


def build_prompt(
    eda: str, hda: str, scenario_prompt: str, scratch_dir: str, catalog_order: str
) -> str:
    if catalog_order == "eda-first":
        entries = EDA_CATALOG_ENTRY + "\n\n" + HDA_CATALOG_ENTRY
        paths = EDA_PATH_LINE + "\n" + HDA_PATH_LINE
    else:
        entries = HDA_CATALOG_ENTRY + "\n\n" + EDA_CATALOG_ENTRY
        paths = HDA_PATH_LINE + "\n" + EDA_PATH_LINE
    return (
        PROMPT_TEMPLATE.replace("{CATALOG_ENTRIES}", entries)
        .replace("{CATALOG_PATHS}", paths)
        .replace("{EDA_DESCRIPTION}", eda)
        .replace("{HDA_DESCRIPTION}", hda)
        .replace("{SCENARIO_PROMPT}", scenario_prompt)
        .replace("{SCRATCH_DIR}", scratch_dir)
    )


def detect_route(texts: list[str]) -> str:
    """Find the first ROUTE token across assistant text blocks, in order.

    Backticks are stripped before matching so a code-span-wrapped token
    (`ROUTE: ...`) still matches. No token anywhere -> "unclear".
    """
    for text in texts:
        match = ROUTE_RE.search(text.replace("`", ""))
        if match:
            return ROUTE_MAP[match.group(1)]
    return "unclear"


def read_events(jsonl_path: Path) -> tuple[list[dict], int]:
    """Read JSON-object events from a JSONL file, counting parse failures."""
    events: list[dict] = []
    parse_failures = 0
    for line in jsonl_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            event = json.loads(stripped)
        except json.JSONDecodeError:
            parse_failures += 1
            continue
        if isinstance(event, dict):
            events.append(event)
        else:
            parse_failures += 1
    return events, parse_failures


def assistant_blocks(event: dict):
    """Yield content blocks (as dicts) from an assistant event."""
    content = event.get("message", {}).get("content", [])
    if not isinstance(content, list):
        return
    for block in content:
        if isinstance(block, dict):
            yield block


@dataclass
class TranscriptScan:
    """Aggregates pulled from one stream-json transcript's events."""

    model: str = ""
    session_id: str = ""
    assistant_events: int = 0
    has_result_event: bool = False
    result_text: str | None = None
    tool_uses: list[dict] = field(default_factory=list)
    texts: list[str] = field(default_factory=list)


def scan_events(events: list[dict]) -> TranscriptScan:
    """Fold transcript events into a TranscriptScan."""
    scan = TranscriptScan()
    for event in events:
        kind = event.get("type")
        if kind == "system":
            scan.model = event.get("model", "") or scan.model
            scan.session_id = event.get("session_id", "") or scan.session_id
        elif kind == "assistant":
            scan.assistant_events += 1
            for block in assistant_blocks(event):
                if block.get("type") == "text" and block.get("text"):
                    scan.texts.append(block["text"])
                elif block.get("type") == "tool_use":
                    inputs = block.get("input", {})
                    if not isinstance(inputs, dict):
                        inputs = {}
                    scan.tool_uses.append(
                        {
                            "name": block.get("name", ""),
                            "path": inputs.get("file_path") or inputs.get("path"),
                        }
                    )
        elif kind == "result":
            scan.has_result_event = True
            if isinstance(event.get("result"), str):
                scan.result_text = event["result"]
    return scan


def validity_problems(scan: TranscriptScan, exit_code: int) -> list[str]:
    """List validity failures for a scanned transcript; empty means valid."""
    problems: list[str] = []
    if not scan.model:
        problems.append("empty model")
    if not scan.session_id:
        problems.append("empty session_id")
    if scan.assistant_events < 1:
        problems.append("no assistant events")
    if not scan.has_result_event:
        problems.append("no result event")
    if exit_code != 0:
        problems.append(f"exit code {exit_code}")
    return problems


def detect(jsonl_path: Path, exit_code: int) -> dict:
    """Parse a stream-json transcript and extract dispatch evidence."""
    events, parse_failures = read_events(jsonl_path)
    scan = scan_events(events)
    problems = validity_problems(scan, exit_code)
    tool_uses = scan.tool_uses
    texts = scan.texts
    first_text = texts[0] if texts else ""
    final_text = scan.result_text if scan.result_text is not None else (texts[-1] if texts else "")
    wrote_files = [t["path"] for t in tool_uses if t["name"] == "Write" and t["path"]]
    return {
        "model": scan.model,
        "session_id": scan.session_id,
        "tool_uses": tool_uses,
        "read_eda_skill": any(
            t["name"] == "Read" and t["path"] == str(EDA_SKILL) for t in tool_uses
        ),
        "read_hda_skill": any(
            t["name"] == "Read" and t["path"] == str(HDA_SKILL) for t in tool_uses
        ),
        "first_text": first_text,
        "route": detect_route(texts),
        "wrote_files": wrote_files,
        "json_parse_failures": parse_failures,
        "valid": not problems,
        "invalid_reason": "; ".join(problems) if problems else "-",
        "final_text_sha256": sha256_text(final_text) if final_text else "-",
        "jsonl_sha256": sha256_file(jsonl_path),
    }


def run_rep(prompt: str, rep_base: Path, model: str, timeout: int, cwd: Path) -> int:
    """Run one claude arm; archive stdout to <rep_base>.jsonl, stderr to .stderr."""
    jsonl_path = rep_base.with_suffix(".jsonl")
    stderr_path = rep_base.with_suffix(".stderr")
    cmd = [
        "claude",
        "-p",
        prompt,
        "--model",
        model,
        "--output-format",
        "stream-json",
        "--verbose",
        "--allowedTools",
        "Read",
        "Write",
        "Glob",
        "Grep",
    ]
    with jsonl_path.open("wb") as out, stderr_path.open("wb") as err:
        proc = subprocess.Popen(cmd, stdout=out, stderr=err, cwd=cwd)
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            err.write(f"\nharness: killed after {timeout}s timeout\n".encode())
    return proc.returncode


def check_summary_not_duplicate(summary_path: Path, scenario: str, rep: int, suffix: str) -> None:
    """Hard-fail if summary.tsv already has a row for (scenario, rep, suffix)."""
    if not summary_path.exists():
        return
    lines = summary_path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return
    header = lines[0].split("\t")
    try:
        idx = {c: header.index(c) for c in ("scenario", "rep", "suffix")}
    except ValueError:
        sys.exit(
            f"FATAL: {summary_path} header lacks scenario/rep/suffix columns; "
            "it predates this harness version — move it aside before rerunning"
        )
    for line in lines[1:]:
        fields = line.split("\t")
        if (
            fields[idx["scenario"]] == scenario
            and fields[idx["rep"]] == str(rep)
            and fields[idx["suffix"]] == suffix
        ):
            sys.exit(
                f"FATAL: {summary_path} already has a row for scenario={scenario} "
                f"rep={rep} suffix={suffix}; pass a fresh --rerun-suffix <tag>"
            )


def append_summary_row(summary_path: Path, row: dict) -> None:
    write_header = not summary_path.exists()
    with summary_path.open("a", encoding="utf-8") as fh:
        if write_header:
            fh.write("\t".join(TSV_COLUMNS) + "\n")
        fh.write("\t".join(str(row[c]) for c in TSV_COLUMNS) + "\n")


def claude_version() -> str:
    try:
        out = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        return out.stdout.strip() or out.stderr.strip()
    except OSError as exc:
        return f"unavailable: {exc}"


def git_sha() -> str:
    out = subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    return out.stdout.strip()


def resolve_rep_cwd(scratch_root: Path, rep_name: str) -> Path:
    """Resolve a rep's working directory and hard-fail if it is inside the repo."""
    cwd = (scratch_root / rep_name).resolve()
    if cwd.is_relative_to(REPO):
        sys.exit(
            f"FATAL: rep cwd {cwd} is inside the repo {REPO}; "
            "pass a --scratch-root outside the repository"
        )
    return cwd


def rep_name(scenario: str, rep: int, suffix: str | None) -> str:
    base = f"{scenario}-rep{rep}"
    return f"{base}-{suffix}" if suffix else base


@dataclass(frozen=True)
class RepPlan:
    """One planned rep: its number, catalog order, and file basename."""

    rep: int
    catalog_order: str
    name: str


@dataclass
class RunContext:
    """Resolved per-invocation inputs shared by every rep."""

    args: argparse.Namespace
    out_dir: Path
    scratch_root: Path | None
    eda: str
    hda: str
    scenario_prompt: str


def write_manifest(ctx: RunContext, rep_plan: list[RepPlan]) -> Path:
    args = ctx.args
    out_dir = ctx.out_dir
    scratch_root = ctx.scratch_root
    eda = ctx.eda
    hda = ctx.hda
    scenario_prompt_shas = {
        f"{sid}/{order}": sha256_text(build_prompt(eda, hda, sprompt, "{SCRATCH_DIR}", order))
        for sid, sprompt in SCENARIOS.items()
        for order in ("eda-first", "hda-first")
    }
    manifest = {
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "harness_args": {
            "scenario": args.scenario,
            "reps": args.reps,
            "out_dir": str(out_dir),
            "scratch_root": str(scratch_root) if scratch_root else None,
            "model": args.model,
            "timeout": args.timeout,
            "start_rep": args.start_rep,
            "order": args.order,
            "rerun_suffix": args.rerun_suffix,
            "dry_run": args.dry_run,
        },
        "rep_plan": [asdict(plan) for plan in rep_plan],
        "claude_version": claude_version(),
        "repo_git_sha": git_sha(),
        "eda_skill_md_sha256": sha256_file(EDA_SKILL),
        "hda_skill_md_sha256": sha256_file(HDA_SKILL),
        "eda_description_sha256": sha256_text(eda),
        "hda_description_sha256": sha256_text(hda),
        "eda_description_len": len(eda),
        "hda_description_len": len(hda),
        "filled_prompt_sha256_per_scenario_order": scenario_prompt_shas,
        "filled_prompt_note": (
            "SCRATCH_DIR left as the literal placeholder {SCRATCH_DIR}; "
            "per-rep prompt_sha256 in summary.tsv covers the fully filled prompt"
        ),
        "prompt_template": PROMPT_TEMPLATE,
    }
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    manifest_path = out_dir / f"manifest-{args.scenario}-{stamp}.json"
    counter = 2
    while manifest_path.exists():
        manifest_path = out_dir / f"manifest-{args.scenario}-{stamp}-{counter}.json"
        counter += 1
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--scenario", required=True, choices=sorted(SCENARIOS))
    parser.add_argument("--reps", type=int, required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument(
        "--scratch-root",
        help="directory for per-rep scratch cwds; required unless --dry-run, "
        "must resolve outside the repository",
    )
    parser.add_argument("--model", default="claude-opus-5")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--start-rep", type=int, default=1)
    parser.add_argument(
        "--order",
        choices=["eda-first", "hda-first", "alternate"],
        default="alternate",
        help="catalog order in the prompt; alternate = odd reps eda-first, even hda-first",
    )
    parser.add_argument(
        "--rerun-suffix",
        help="tag appended to rep filenames (<scenario>-rep<K>-<tag>.*) so a rerun "
        "preserves the original files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="fill and print each rep's prompt, write manifest, do not invoke claude",
    )
    args = parser.parse_args()

    if args.rerun_suffix is not None and not SUFFIX_RE.match(args.rerun_suffix):
        sys.exit("FATAL: --rerun-suffix must match [A-Za-z0-9_-]+ (no dots)")
    if not args.dry_run and not args.scratch_root:
        sys.exit("FATAL: --scratch-root is required unless --dry-run")
    return args


def refuse_existing_rep(ctx: RunContext, plan: RepPlan, jsonl_path: Path) -> None:
    """Hard-fail rather than overwrite any existing rep transcript."""
    args = ctx.args
    original = ctx.out_dir / f"{args.scenario}-rep{plan.rep}.jsonl"
    if original.exists() and not args.rerun_suffix:
        sys.exit(
            f"FATAL: {original} already exists; pass --rerun-suffix <tag> to "
            f"rerun this rep as {args.scenario}-rep{plan.rep}-<tag>.* while "
            "preserving the original files"
        )
    if jsonl_path.exists():
        sys.exit(
            f"FATAL: {jsonl_path} already exists; pass a fresh --rerun-suffix "
            "tag — existing rep files are never overwritten"
        )


def execute_rep(ctx: RunContext, plan: RepPlan) -> None:
    """Run one rep end to end: launch, detect, record, report."""
    args = ctx.args
    rep = plan.rep
    name = plan.name
    catalog_order = plan.catalog_order
    suffix = args.rerun_suffix or "-"
    rep_base = ctx.out_dir / name
    jsonl_path = rep_base.with_suffix(".jsonl")
    refuse_existing_rep(ctx, plan, jsonl_path)
    check_summary_not_duplicate(ctx.out_dir / "summary.tsv", args.scenario, rep, suffix)
    if ctx.scratch_root is None:
        sys.exit("FATAL: --scratch-root is required unless --dry-run")
    cwd = resolve_rep_cwd(ctx.scratch_root, name)
    cwd.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(ctx.eda, ctx.hda, ctx.scenario_prompt, str(cwd), catalog_order)
    started_utc = datetime.now(UTC).isoformat(timespec="seconds")
    t0 = time.monotonic()
    exit_code = run_rep(prompt, rep_base, args.model, args.timeout, cwd)
    duration_s = round(time.monotonic() - t0, 1)
    evidence = detect(jsonl_path, exit_code)
    evidence.update(
        scenario=args.scenario,
        rep=rep,
        suffix=suffix,
        catalog_order=catalog_order,
        started_utc=started_utc,
        duration_s=duration_s,
        exit_code=exit_code,
        prompt_sha256=sha256_text(prompt),
    )
    (ctx.out_dir / f"{name}.detect.json").write_text(
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
    )
    evidence["wrote_files_count"] = len(evidence["wrote_files"])
    append_summary_row(ctx.out_dir / "summary.tsv", evidence)
    if not evidence["valid"]:
        print(
            f"!!! WARNING: {name} produced an INVALID transcript "
            f"({evidence['invalid_reason']}) — do not score this rep !!!",
            file=sys.stderr,
        )
    print(
        f"{args.scenario} rep {rep}: exit={exit_code} "
        f"route={evidence['route']} "
        f"valid={evidence['valid']} "
        f"read_eda={evidence['read_eda_skill']} "
        f"read_hda={evidence['read_hda_skill']} "
        f"duration={duration_s}s"
    )


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    scratch_root = Path(args.scratch_root).resolve() if args.scratch_root else None
    ctx = RunContext(
        args=args,
        out_dir=out_dir,
        scratch_root=scratch_root,
        eda=parse_description(EDA_SKILL),
        hda=parse_description(HDA_SKILL),
        scenario_prompt=SCENARIOS[args.scenario],
    )
    rep_plan = [
        RepPlan(
            rep=rep,
            catalog_order=catalog_order_for_rep(args.order, rep),
            name=rep_name(args.scenario, rep, args.rerun_suffix),
        )
        for rep in range(args.start_rep, args.start_rep + args.reps)
    ]
    write_manifest(ctx, rep_plan)

    if args.dry_run:
        for plan in rep_plan:
            scratch = (
                str(scratch_root / plan.name) if scratch_root else f"<scratch-root>/{plan.name}"
            )
            print(f"=== rep {plan.rep} ({plan.catalog_order}) ===")
            print(build_prompt(ctx.eda, ctx.hda, ctx.scenario_prompt, scratch, plan.catalog_order))
            print()
        return

    for plan in rep_plan:
        execute_rep(ctx, plan)


if __name__ == "__main__":
    main()
