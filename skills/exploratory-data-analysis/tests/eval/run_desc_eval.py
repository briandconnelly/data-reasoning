#!/usr/bin/env python3
"""Validity-aware matched-pair trigger eval for two frozen skill descriptions.

Replaces skill-creator's ``run_eval.py`` for single-description trigger evals.
It mirrors that script's detection method exactly so results stay comparable:

Detection method (mirrored from skill-creator ``scripts/run_eval.py``):

- A synthetic command file is written to ``<project_root>/.claude/commands/``
  named ``{skill_name}-skill-{uuid4.hex[:8]}.md``. The 8-hex-char unique ID is
  fresh per invocation, so parallel or leftover files cannot contaminate a run.
  The file body is a YAML block scalar (``description: |``) holding the
  description indented by two spaces, followed by
  ``# {skill_name}`` and ``This skill handles: {description}``.
- ``claude -p <query> --output-format stream-json --verbose
  --include-partial-messages --model <model>`` runs with cwd at the project
  root and the ``CLAUDECODE`` env var removed.
- Trigger signal: the first ``tool_use`` content block in the stream. If its
  tool is ``Skill`` or ``Read`` and the accumulated ``input_json_delta`` JSON
  (or the fallback full assistant message's ``skill`` / ``file_path`` input)
  contains the unique command name, the query triggered. Any other first tool
  means no trigger. A ``result`` event ends detection.
- The stream is consumed live, line by line, and the session is stopped the
  instant detection reaches a decisive verdict, exactly as the original does.

Termination semantics (preregistration, "Instruments" -> "Termination
semantics"): an invocation is ``valid`` when either the session completed
normally with a result event, or detection reached a decisive verdict and this
harness terminated the session; ``void`` covers timeout, nonzero exit, or an
unparseable stream *before* a decisive verdict. A nonzero exit caused by this
harness's own termination is therefore never void. Each row records which
valid ending occurred in ``ending``.

Differences from the original (the point of this script):

- stderr is captured to a file per attempt, never discarded.
- Every stdout line is archived to the transcript as it arrives.
- Timeouts, nonzero exits, and unparseable streams before a decisive verdict
  are recorded as ``status=void`` (with ``invalid_reason``) and
  ``triggered=null``, never as non-triggers. A stream that exits cleanly and
  parses but neither decides nor carries a result event is void as
  ``no_result_event``: the preregistration's validity definition does not
  cover it, and scoring it as a non-trigger is the exact failure this
  instrument exists to prevent.
- A void attempt is retried immediately, at most twice (3 attempts total),
  each with a fresh process and fresh unique ID; all attempts are archived.
- Two descriptions run as matched pairs, interleaved at the query level.

Determinism: for run ``r`` (1-based), the query visit order is the selected
fixture indices shuffled by ``random.Random(seed * 1000 + r).shuffle(...)``.
Within a query, arm A goes first when ``(query_index + r) % 2 == 0``, else B.
Execution is strictly sequential (num-workers=1 semantics).

Outputs under ``--out-dir``:

- ``results.jsonl`` — one JSON object per attempt (a retry is a fresh
  invocation and gets its own row). Refuses to run if it already exists.
- ``manifest-<utcstamp>.json`` — argv, seed, model, claude CLI version,
  git SHA, fixture and description sha256s, and the query order per run.
- ``transcripts/<stem>.stdout.jsonl`` and ``<stem>.stderr.log`` per attempt,
  where ``<stem>`` is ``q{query_index:03d}-{arm_label}-r{run}-a{attempt}``.

Descriptions are read from the frozen files as rendered text: exactly one
trailing newline is stripped, the sha256 of the resulting string is recorded,
and the text is embedded via the same block-scalar construction as the
original (never YAML-escaped).
"""

from __future__ import annotations

import argparse
import codecs
import hashlib
import json
import os
import random
import re
import select
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

MAX_ATTEMPTS = 3
TRIGGER_TOOLS = ("Skill", "Read")
DRY_RUN_PREVIEW_COUNT = 2
EXCERPT_CHARS = 300
READ_CHUNK_BYTES = 8192
SELECT_POLL_S = 1.0
TERMINATE_GRACE_S = 5.0


@dataclass(frozen=True)
class Arm:
    """One description arm: its label, rendered text, and content hash."""

    label: str
    text: str
    sha256: str


@dataclass(frozen=True)
class Invocation:
    """One planned query-x-arm execution slot."""

    query_index: int
    query: str
    arm: Arm
    run: int
    ordinal: int
    which_first: str


@dataclass(frozen=True)
class ProcessResult:
    """Raw outcome of one claude process, before validity classification."""

    timed_out: bool
    returncode: int | None
    verdict: bool | None
    session_id: str | None
    parsed_any: bool
    decided_on_result: bool


@dataclass(frozen=True)
class AttemptOutcome:
    """Classification of one claude process attempt."""

    status: str
    invalid_reason: str | None
    triggered: bool | None
    session_id: str | None
    started_utc: str
    duration_s: float
    ending: str | None


@dataclass(frozen=True)
class Config:
    """Resolved run configuration."""

    fixture: Path
    out_dir: Path
    model: str
    runs: int
    timeout: int
    seed: int
    skill_name: str
    project_root: Path
    dry_run: bool


def find_project_root() -> Path:
    """Walk up from cwd looking for .claude/, as run_eval.py does."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".claude").is_dir():
            return parent
    return current


def default_skill_name(fixture: Path) -> str:
    """Derive the skill name from a skills/<name>/... fixture path."""
    parts = fixture.resolve().parts
    if "skills" in parts:
        index = parts.index("skills")
        if index + 1 < len(parts):
            return parts[index + 1]
    return "skill"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_frozen_description(path: Path) -> str:
    """Read a frozen description file, stripping exactly one trailing newline."""
    return path.read_text(encoding="utf-8").removesuffix("\n")


def build_command_content(skill_name: str, description: str) -> str:
    """Build the synthetic command file body exactly as run_eval.py does."""
    indented_desc = "\n  ".join(description.split("\n"))
    return (
        f"---\n"
        f"description: |\n"
        f"  {indented_desc}\n"
        f"---\n\n"
        f"# {skill_name}\n\n"
        f"This skill handles: {description}\n"
    )


class StreamTriggerState:
    """Incremental stream-event detector, mirroring run_eval.py's state machine.

    ``feed`` returns True/False once the stream decides, or None while
    undecided (which is when run_eval.py's loop reads the next line).
    """

    def __init__(self, clean_name: str) -> None:
        self.clean_name = clean_name
        self.pending_tool: str | None = None
        self.accumulated = ""

    def feed(self, stream: dict) -> bool | None:
        stream_type = stream.get("type", "")
        if stream_type == "content_block_start":
            return self._block_start(stream)
        if stream_type == "content_block_delta" and self.pending_tool:
            return self._block_delta(stream)
        if stream_type in ("content_block_stop", "message_stop"):
            if self.pending_tool:
                return self.clean_name in self.accumulated
            return False if stream_type == "message_stop" else None
        return None

    def _block_start(self, stream: dict) -> bool | None:
        block = stream.get("content_block", {})
        if block.get("type") != "tool_use":
            return None
        name = block.get("name", "")
        if name not in TRIGGER_TOOLS:
            return False
        self.pending_tool = name
        self.accumulated = ""
        return None

    def _block_delta(self, stream: dict) -> bool | None:
        delta = stream.get("delta", {})
        if delta.get("type") != "input_json_delta":
            return None
        self.accumulated += delta.get("partial_json", "")
        return True if self.clean_name in self.accumulated else None


def assistant_decision(event: dict, clean_name: str) -> bool | None:
    """Mirror run_eval.py's fallback: judge only the first tool_use item.

    Returns None when the assistant message holds no tool_use block, because
    run_eval.py's inner loop then falls through and keeps reading the stream.
    """
    for item in event.get("message", {}).get("content", []):
        if item.get("type") != "tool_use":
            continue
        name = item.get("name", "")
        tool_input = item.get("input", {})
        return (name == "Skill" and clean_name in tool_input.get("skill", "")) or (
            name == "Read" and clean_name in tool_input.get("file_path", "")
        )
    return None


class LiveDetector:
    """Run run_eval.py's detection over a stream consumed line by line.

    ``feed_line`` returns the decisive verdict once the stream decides, and
    None while undecided. run_eval.py's ``triggered`` accumulator is only ever
    set True immediately before returning, so a ``result`` event decides False,
    exactly as here. The detector keeps no event history: only the verdict, the
    session id, and whether any line parsed at all.
    """

    def __init__(self, clean_name: str) -> None:
        self.clean_name = clean_name
        self.state = StreamTriggerState(clean_name)
        self.verdict: bool | None = None
        self.session_id: str | None = None
        self.parsed_any = False
        self.decided_on_result = False

    def feed_line(self, line: str) -> bool | None:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            return self.verdict
        if not isinstance(event, dict):
            return self.verdict
        self.parsed_any = True
        self._record_session(event)
        if self.verdict is not None:
            return self.verdict
        event_type = event.get("type")
        if event_type == "stream_event":
            decision = self.state.feed(event.get("event", {}))
        elif event_type == "assistant":
            decision = assistant_decision(event, self.clean_name)
        elif event_type == "result":
            decision = False
            self.decided_on_result = True
        else:
            decision = None
        if decision is not None:
            self.verdict = decision
        return self.verdict

    def _record_session(self, event: dict) -> None:
        """Prefer the result event's session_id; fall back to the first seen."""
        session_id = event.get("session_id")
        if not session_id:
            return
        if event.get("type") == "result" or self.session_id is None:
            self.session_id = session_id


def drain_buffer(buffer: str, out, detector: LiveDetector) -> tuple[str, bool | None]:
    """Archive every complete line in ``buffer``, feeding each to the detector.

    Lines keep being archived after the verdict lands, so whatever already
    arrived reaches the transcript; only the detector stops deciding.
    """
    verdict = detector.verdict
    while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        out.write(line + "\n")
        stripped = line.strip()
        if stripped and verdict is None:
            verdict = detector.feed_line(stripped)
    out.flush()
    return buffer, verdict


def stream_process(process: subprocess.Popen, out, detector: LiveDetector, timeout: float) -> bool:
    """Consume stdout live until the detector decides, EOF, or the timeout.

    Returns True if the whole invocation timed out. Every byte read is written
    to ``out`` as it arrives; nothing beyond one partial line is held.
    """
    deadline = time.monotonic() + timeout
    buffer = ""
    stdout = process.stdout
    assert stdout is not None
    # Incremental so a multibyte character split across two reads survives.
    decoder = codecs.getincrementaldecoder("utf-8")("replace")
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            drain_buffer(buffer, out, detector)
            return True
        ready, _, _ = select.select([stdout], [], [], min(SELECT_POLL_S, remaining))
        chunk = os.read(stdout.fileno(), READ_CHUNK_BYTES) if ready else b""
        if ready and not chunk:
            # EOF: the child closed stdout, so nothing more can arrive.
            break
        if chunk:
            buffer += decoder.decode(chunk)
            buffer, verdict = drain_buffer(buffer, out, detector)
            if verdict is not None:
                break
        elif process.poll() is not None:
            break
    buffer += decoder.decode(b"", final=True)
    if buffer:
        out.write(buffer)
        if detector.verdict is None and buffer.strip():
            detector.feed_line(buffer.strip())
        out.flush()
    return False


def stop_process(process: subprocess.Popen) -> int | None:
    """Stop the child if it still runs; return its exit code."""
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=TERMINATE_GRACE_S)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
    return process.returncode


def classify_attempt(
    process_result: ProcessResult, started_utc: str, duration_s: float
) -> AttemptOutcome:
    """Decide valid/void per the preregistration's termination semantics.

    A decisive verdict makes the attempt valid whatever the exit code, because
    the nonzero exit is this harness's own termination. Void therefore reaches
    only streams that never decided. The two valid endings are the two the
    preregistration names: a result event is a normal completion, any earlier
    decisive verdict is an early stop by this harness.
    """
    session_id = process_result.session_id
    if process_result.verdict is not None:
        ending = "completed" if process_result.decided_on_result else "terminated_on_detection"
        return AttemptOutcome(
            "valid", None, process_result.verdict, session_id, started_utc, duration_s, ending
        )
    if process_result.timed_out:
        invalid_reason = "timeout"
    elif process_result.returncode != 0:
        invalid_reason = f"nonzero_exit:{process_result.returncode}"
    elif not process_result.parsed_any:
        invalid_reason = "unparseable_stream"
    else:
        invalid_reason = "no_result_event"
    return AttemptOutcome("void", invalid_reason, None, session_id, started_utc, duration_s, None)


def run_attempt(config: Config, arm: Arm, query: str, stem: Path) -> AttemptOutcome:
    """Run one claude process; archive stdout/stderr live; classify the result."""
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{config.skill_name}-skill-{unique_id}"
    commands_dir = config.project_root / ".claude" / "commands"
    command_file = commands_dir / f"{clean_name}.md"
    stdout_path = stem.with_suffix(".stdout.jsonl")
    stderr_path = stem.with_suffix(".stderr.log")
    cmd = [
        "claude",
        "-p",
        query,
        "--output-format",
        "stream-json",
        "--verbose",
        "--include-partial-messages",
        "--model",
        config.model,
    ]
    env = {key: value for key, value in os.environ.items() if key != "CLAUDECODE"}
    detector = LiveDetector(clean_name)
    started_utc = datetime.now(UTC).isoformat()
    start = time.monotonic()
    timed_out = False
    returncode: int | None = None
    try:
        commands_dir.mkdir(parents=True, exist_ok=True)
        command_file.write_text(build_command_content(config.skill_name, arm.text))
        with stdout_path.open("w", encoding="utf-8") as out, stderr_path.open("wb") as err:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=err,
                cwd=config.project_root,
                env=env,
            )
            try:
                timed_out = stream_process(process, out, detector, config.timeout)
            finally:
                returncode = stop_process(process)
                if process.stdout is not None:
                    process.stdout.close()
    finally:
        command_file.unlink(missing_ok=True)
    duration_s = round(time.monotonic() - start, 3)
    process_result = ProcessResult(
        timed_out=timed_out,
        returncode=returncode,
        verdict=detector.verdict,
        session_id=detector.session_id,
        parsed_any=detector.parsed_any,
        decided_on_result=detector.decided_on_result,
    )
    return classify_attempt(process_result, started_utc, duration_s)


def sanitize_label(label: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "_", label)


def plan_invocations(config: Config, queries: list[tuple[int, str]], arms: dict[str, Arm]):
    """Yield the full deterministic execution plan.

    For run r (1-based): shuffle selected fixture indices with
    random.Random(seed * 1000 + r); within a query, A first when
    (query_index + r) % 2 == 0, else B.
    """
    ordinal = 0
    query_text = dict(queries)
    for run in range(1, config.runs + 1):
        order = [index for index, _ in queries]
        random.Random(config.seed * 1000 + run).shuffle(order)
        for query_index in order:
            first, second = ("A", "B") if (query_index + run) % 2 == 0 else ("B", "A")
            for arm_key in (first, second):
                ordinal += 1
                yield Invocation(
                    query_index=query_index,
                    query=query_text[query_index],
                    arm=arms[arm_key],
                    run=run,
                    ordinal=ordinal,
                    which_first=arms[first].label,
                )


def query_orders(config: Config, queries: list[tuple[int, str]]) -> dict[str, list[int]]:
    orders = {}
    for run in range(1, config.runs + 1):
        order = [index for index, _ in queries]
        random.Random(config.seed * 1000 + run).shuffle(order)
        orders[str(run)] = order
    return orders


def select_queries(fixture_items: list[dict], selector: str | None) -> list[tuple[int, str]]:
    """Select (fixture_index, query) pairs.

    Selector forms: None (all); comma-separated 0-based indices/ranges
    (e.g. "3", "1,4", "2-5"); otherwise a regex searched against query text.
    """
    pairs = [(index, item["query"]) for index, item in enumerate(fixture_items)]
    if selector is None:
        return pairs
    if re.fullmatch(r"\d+(-\d+)?(,\d+(-\d+)?)*", selector):
        wanted: set[int] = set()
        for part in selector.split(","):
            if "-" in part:
                low, high = part.split("-")
                wanted.update(range(int(low), int(high) + 1))
            else:
                wanted.add(int(part))
        return [(index, query) for index, query in pairs if index in wanted]
    pattern = re.compile(selector)
    return [(index, query) for index, query in pairs if pattern.search(query)]


def tool_version(cmd: list[str]) -> str:
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
        return completed.stdout.strip() or completed.stderr.strip()
    except (OSError, subprocess.SubprocessError) as error:
        # A missing or hung provenance command must not abort the run.
        return f"unavailable: {type(error).__name__}: {error}"


def write_manifest(
    config: Config,
    arms: dict[str, Arm],
    desc_paths: dict[str, Path],
    queries: list[tuple[int, str]],
) -> Path:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    manifest_path = config.out_dir / f"manifest-{stamp}.json"
    manifest = {
        "argv": sys.argv,
        "seed": config.seed,
        "model": config.model,
        "runs": config.runs,
        "timeout": config.timeout,
        "skill_name": config.skill_name,
        "project_root": str(config.project_root),
        "claude_cli_version": tool_version(["claude", "--version"]),
        "git_sha": tool_version(["git", "-C", str(config.project_root), "rev-parse", "HEAD"]),
        "fixture": str(config.fixture),
        "fixture_sha256": sha256_text(config.fixture.read_text(encoding="utf-8")),
        "descriptions": {
            key: {
                "label": arm.label,
                "path": str(desc_paths[key]),
                "sha256": arm.sha256,
            }
            for key, arm in arms.items()
        },
        "selected_query_indices": [index for index, _ in queries],
        "query_order_per_run": query_orders(config, queries),
        "dry_run": config.dry_run,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest_path


def print_dry_run_preview(config: Config, plan: list[Invocation]) -> None:
    for invocation in plan[:DRY_RUN_PREVIEW_COUNT]:
        content = build_command_content(config.skill_name, invocation.arm.text)
        excerpt = content[:EXCERPT_CHARS].replace("\n", "\\n")
        print(
            f"[dry-run] ordinal={invocation.ordinal} run={invocation.run} "
            f"query_index={invocation.query_index} arm={invocation.arm.label} "
            f"which_first={invocation.which_first}\n"
            f"  query: {invocation.query}\n"
            f"  command file: .claude/commands/{config.skill_name}-skill-<UUID>.md\n"
            f"  content excerpt: {excerpt}"
        )


def execute_plan(config: Config, plan: list[Invocation], results_path: Path) -> None:
    transcripts_dir = config.out_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    with results_path.open("w", encoding="utf-8") as results:
        for invocation in plan:
            label = sanitize_label(invocation.arm.label)
            for attempt in range(1, MAX_ATTEMPTS + 1):
                stem = transcripts_dir / (
                    f"q{invocation.query_index:03d}-{label}-r{invocation.run}-a{attempt}"
                )
                outcome = run_attempt(config, invocation.arm, invocation.query, stem)
                row = {
                    "query_index": invocation.query_index,
                    "query": invocation.query,
                    "arm_label": invocation.arm.label,
                    "desc_sha256": invocation.arm.sha256,
                    "run": invocation.run,
                    "ordinal": invocation.ordinal,
                    "which_first": invocation.which_first,
                    "started_utc": outcome.started_utc,
                    "duration_s": outcome.duration_s,
                    "attempt": attempt,
                    "status": outcome.status,
                    "invalid_reason": outcome.invalid_reason,
                    "triggered": outcome.triggered,
                    "ending": outcome.ending,
                    "session_id": outcome.session_id,
                    "transcript_file": str(
                        stem.with_suffix(".stdout.jsonl").relative_to(config.out_dir)
                    ),
                    "stderr_file": str(stem.with_suffix(".stderr.log").relative_to(config.out_dir)),
                }
                results.write(json.dumps(row) + "\n")
                results.flush()
                print(
                    f"[{invocation.ordinal}/{len(plan)}] q{invocation.query_index} "
                    f"{invocation.arm.label} r{invocation.run} a{attempt}: "
                    f"{outcome.status} triggered={outcome.triggered} "
                    f"ending={outcome.ending} reason={outcome.invalid_reason} "
                    f"{outcome.duration_s}s",
                    file=sys.stderr,
                )
                if outcome.status == "valid":
                    break


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Matched-pair, validity-aware trigger eval for two frozen descriptions."
    )
    parser.add_argument("--fixture", required=True, type=Path, help="Eval set JSON file")
    parser.add_argument("--desc-a", required=True, type=Path, help="Frozen description A")
    parser.add_argument("--desc-b", required=True, type=Path, help="Frozen description B")
    parser.add_argument("--out-dir", required=True, type=Path, help="Output directory")
    parser.add_argument("--model", required=True, help="Model for claude -p")
    parser.add_argument("--runs", type=int, default=3, help="Paired runs per query")
    parser.add_argument("--timeout", type=int, default=390, help="Seconds per attempt")
    parser.add_argument("--seed", type=int, default=0, help="Shuffle seed")
    parser.add_argument("--label-a", default="A", help="Label for arm A")
    parser.add_argument("--label-b", default="B", help="Label for arm B")
    parser.add_argument("--dry-run", action="store_true", help="Plan and manifest only")
    parser.add_argument(
        "--queries",
        default=None,
        help="0-based index filter (e.g. 3 or 1,4 or 2-5) or regex on query text",
    )
    parser.add_argument(
        "--skill-name",
        default=None,
        help="Skill name embedded in the synthetic command file "
        "(default: derived from the fixture path's skills/<name>/ segment)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = Config(
        fixture=args.fixture,
        out_dir=args.out_dir,
        model=args.model,
        runs=args.runs,
        timeout=args.timeout,
        seed=args.seed,
        skill_name=args.skill_name or default_skill_name(args.fixture),
        project_root=find_project_root(),
        dry_run=args.dry_run,
    )
    fixture_items = json.loads(config.fixture.read_text(encoding="utf-8"))
    queries = select_queries(fixture_items, args.queries)
    if not queries:
        print("Error: no queries selected", file=sys.stderr)
        return 1
    desc_paths = {"A": args.desc_a, "B": args.desc_b}
    arms = {}
    for key, label in (("A", args.label_a), ("B", args.label_b)):
        text = read_frozen_description(desc_paths[key])
        arms[key] = Arm(label=label, text=text, sha256=sha256_text(text))
    config.out_dir.mkdir(parents=True, exist_ok=True)
    results_path = config.out_dir / "results.jsonl"
    if not config.dry_run and results_path.exists():
        print(f"Error: {results_path} already exists; refusing to overwrite", file=sys.stderr)
        return 1
    manifest_path = write_manifest(config, arms, desc_paths, queries)
    print(f"Manifest: {manifest_path}", file=sys.stderr)
    plan = list(plan_invocations(config, queries, arms))
    if config.dry_run:
        print_dry_run_preview(config, plan)
        return 0
    execute_plan(config, plan, results_path)
    print(f"Results: {results_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
