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
- ``{skill_name}`` comes from ``--skill-name`` when given (recorded as
  ``explicit``), else from the fixture path's ``skills/<name>/`` segment
  (recorded as ``derived-from-path``). There is no fallback: a fixture path
  with no such segment aborts the run. The command name is part of what the
  model routes on, so a wrong name silently changes what is measured.
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

Usage limits (``invalid_reason="usage_limit"``): when the account has no quota
left, ``claude -p`` exits 0 and emits a well-formed stream that carries no tool
call at all, so every other validity check passes and the invocation would be
scored as a legitimate non-trigger. It is a non-execution, not a negative. The
stream is therefore also scanned for usage-limit signals, in this order of
preference (all three were observed together in every affected transcript of the
300-invocation run that exposed this):

- a ``rate_limit_event`` event whose ``rate_limit_info.status`` (or
  ``overageStatus``) is ``rejected``;
- an ``assistant`` event with ``error == "rate_limit"``;
- a ``result`` event with ``api_error_status == 429``;
- as a text fallback, assistant text or the ``result`` string matching
  ``USAGE_LIMIT_TEXT`` (e.g. "You've hit your session limit - resets 4pm").

Only a stream that has not yet reached a decisive verdict can be classified this
way: a usage limit that arrives after a tool call has already decided the
invocation does not undo that decision. The consequences are:

- the attempt is ``status="void"``, ``invalid_reason="usage_limit"``,
  ``triggered=null`` — never ``triggered=false``;
- it is *not* retried. A usage limit does not clear in seconds, so a retry
  would only burn the cell's budget on the same non-execution;
- it does not consume one of the cell's ``MAX_ATTEMPTS`` executions, because no
  execution happened;
- the whole run aborts immediately with a nonzero exit and an operator message
  naming the ordinal it stopped at. Everything already written is preserved and
  ``--resume`` continues the run once the quota resets.

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
  invocation and gets its own row). Refuses to run if it already exists,
  unless ``--resume`` is given.
- ``manifest-<utcstamp>.json`` — argv, seed, model, claude CLI version,
  git SHA, fixture and description sha256s, and the query order per run.
  Every invocation writes a new manifest; an existing one is never
  overwritten (a same-second collision gets a ``-<n>`` suffix).
- ``transcripts/<stem>.stdout.jsonl`` and ``<stem>.stderr.log`` per attempt,
  where ``<stem>`` is ``q{query_index:03d}-{arm_label}-r{run}-a{attempt}``.
  The attempt number is part of the stem, so a resumed attempt of a cell
  can never overwrite a stranded attempt of the same cell.

Resuming (``--resume``), for a run interrupted partway through:

- The refusal to touch an existing ``results.jsonl`` is the default and stays
  the default; ``--resume`` is the only way to reopen one, and it opens the
  file for append, never for truncation.
- A *cell* is ``(query_index, run, arm_label)``. A cell is complete when it
  has a ``valid`` row, or when it has spent ``MAX_ATTEMPTS`` executions on
  ``void`` rows (its retries are spent; re-running it would break the
  preregistered at-most-2-retries rule). Complete cells are skipped. A cell
  below that budget was interrupted mid-retry: it resumes at ``highest
  attempt + 1``, so its new rows and transcripts never collide with the
  stranded ones.
- A ``usage_limit`` void row is a non-execution, so it spends nothing: it
  never makes a cell complete, and a cell whose only row is one re-runs from
  a full budget of ``MAX_ATTEMPTS`` executions. Its attempt *number* is still
  spent, so the resumed attempt cannot overwrite the stranded transcript,
  which means a cell's attempt numbers may exceed ``MAX_ATTEMPTS`` while its
  executions never do.
- An attempt the interruption killed before its row was written is not an
  attempt: it has no verdict and no ``status``, so it consumes no retry and
  its partial transcript is rewritten when that attempt number runs again.
  Only rows in ``results.jsonl`` count, and every transcript a row names is
  left untouched. A final line left truncated by a crash is likewise dropped.
- The at-most-2-retries rule is enforced across sessions, not per session:
  total executions for a cell never exceed ``MAX_ATTEMPTS`` however many
  resumes it took to get there.
- The plan is regenerated from the same seed, fixture, and arms, and must
  cover every cell already present in ``results.jsonl``; otherwise the run
  aborts rather than append rows from an incompatible plan.
- Both description sha256s, the fixture sha256, and the resolved skill name are
  recompared against the most recent manifest in the out-dir. Any difference
  aborts the run, naming the value that changed: resuming across an edited
  description, an edited fixture, or a different skill name would mix
  configurations within one result set.
- The resumed invocation writes its own manifest, recording ``resumed``, the
  complete/remaining cell counts, and the provenance values it verified.

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
MANIFEST_PATTERN = re.compile(r"manifest-(\d{8}T\d{6}Z)(?:-(\d+))?\.json\Z")
UNCOVERED_CELLS_SHOWN = 10
GENERIC_SKILL_NAME = "skill"
USAGE_LIMIT_REASON = "usage_limit"
REJECTED_STATUS = "rejected"
RATE_LIMIT_ERROR = "rate_limit"
HTTP_TOO_MANY_REQUESTS = 429
EXIT_STARTUP_ERROR = 1
EXIT_USAGE_LIMIT = 2
# Text fallback for the usage-limit refusal, for the day the structured fields
# change. Kept narrow on purpose: a pattern that also matches an ordinary answer
# would turn real non-triggers into voids and destroy the measurement.
USAGE_LIMIT_TEXT = re.compile(
    r"hit your (?:\w+ ){0,2}limit"
    r"|(?:usage|session|rate|quota) limit (?:reached|exceeded)"
    r"|(?:reached|exceeded) your (?:\w+ ){0,2}limit"
    r"|\blimits?\b.{0,40}\bresets?\b[^\w\n]{0,4}\d",
    re.IGNORECASE,
)

# A cell is one planned unit of work: (query_index, run, arm_label).
CellKey = tuple[int, int, str]


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
    usage_limit_signal: str | None


@dataclass(frozen=True)
class AttemptOutcome:
    """Classification of one claude process attempt.

    ``usage_limit_signal`` names the event field that proved the usage limit; it
    is operator diagnostics only, and is None for every other outcome.
    """

    status: str
    invalid_reason: str | None
    triggered: bool | None
    session_id: str | None
    started_utc: str
    duration_s: float
    ending: str | None
    usage_limit_signal: str | None = None


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
    skill_name_resolution: str
    project_root: Path
    dry_run: bool
    resume: bool


@dataclass(frozen=True)
class CellProgress:
    """Where one interrupted cell picks up.

    ``next_attempt`` is the next unused attempt *number* (so a resumed attempt
    can never overwrite a stranded transcript). ``attempts_spent`` counts only
    real executions, so a ``usage_limit`` void — a non-execution — leaves the
    cell's retry budget untouched while still consuming its attempt number.
    """

    next_attempt: int
    attempts_spent: int


FIRST_CELL_PROGRESS = CellProgress(next_attempt=1, attempts_spent=0)


@dataclass(frozen=True)
class ResumeState:
    """What an existing results.jsonl says about each cell's progress.

    ``complete`` holds cells that must be skipped. ``progress`` holds where
    cells interrupted mid-retry pick up; a cell absent from it starts fresh.
    """

    complete: frozenset[CellKey]
    progress: dict[CellKey, CellProgress]
    rows_read: int

    def progress_for(self, key: CellKey) -> CellProgress:
        return self.progress.get(key, FIRST_CELL_PROGRESS)


def find_project_root() -> Path:
    """Walk up from cwd looking for .claude/, as run_eval.py does."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".claude").is_dir():
            return parent
    return current


class StartupError(RuntimeError):
    """A precondition failed; the run must not start and nothing may be written."""


class SkillNameError(StartupError):
    """The skill name could not be resolved; the run must not start."""


def derive_skill_name(fixture: Path) -> str | None:
    """Derive the skill name from a skills/<name>/... fixture path.

    Returns None when the path carries no usable ``skills/<name>`` segment, and
    also when the derived name is the generic ``skill`` — that name is exactly
    what the old silent fallback produced, so it can never be trusted as a
    derivation. Callers abort instead of guessing.
    """
    parts = fixture.resolve().parts
    if "skills" in parts:
        index = parts.index("skills")
        if index + 1 < len(parts) and parts[index + 1] != GENERIC_SKILL_NAME:
            return parts[index + 1]
    return None


def resolve_skill_name(explicit: str | None, fixture: Path) -> tuple[str, str]:
    """Return (skill_name, resolution) or raise; never falls back silently."""
    if explicit:
        return explicit, "explicit"
    derived = derive_skill_name(fixture)
    if derived is None:
        raise SkillNameError(
            f"cannot derive a skill name: the fixture path {fixture.resolve()} contains "
            f"no 'skills/<name>' component (a component named 'skills' followed by a "
            f"name other than '{GENERIC_SKILL_NAME}'). The synthetic command name is "
            f"part of what the model routes on, so guessing it would silently change "
            f"what is measured. Pass --skill-name <name> explicitly."
        )
    return derived, "derived-from-path"


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


def assistant_text(event: dict) -> str:
    """Concatenate the text blocks of an assistant event's message."""
    content = event.get("message", {}).get("content", [])
    if not isinstance(content, list):
        return ""
    return "\n".join(
        item.get("text", "")
        for item in content
        if isinstance(item, dict) and item.get("type") == "text"
    )


def rate_limit_event_signal(event: dict) -> str | None:
    """Only ``status`` counts.

    A healthy session also emits ``rate_limit_event``, and its sibling
    ``overageStatus`` reads ``rejected`` there too — that field reports whether
    overage billing is available (``overageDisabledReason: org_level_disabled``),
    not whether the request was served. Treating it as a usage limit voided a
    normal answered invocation in testing.
    """
    info = event.get("rate_limit_info")
    info = info if isinstance(info, dict) else {}
    if info.get("status") == REJECTED_STATUS:
        return f"rate_limit_event.rate_limit_info.status={REJECTED_STATUS}"
    return None


def assistant_usage_limit_signal(event: dict) -> str | None:
    if event.get("error") == RATE_LIMIT_ERROR:
        return f"assistant.error={RATE_LIMIT_ERROR}"
    if USAGE_LIMIT_TEXT.search(assistant_text(event)):
        return "assistant text matched USAGE_LIMIT_TEXT"
    return None


def result_usage_limit_signal(event: dict) -> str | None:
    if event.get("api_error_status") == HTTP_TOO_MANY_REQUESTS:
        return f"result.api_error_status={HTTP_TOO_MANY_REQUESTS}"
    result_text = event.get("result")
    if isinstance(result_text, str) and USAGE_LIMIT_TEXT.search(result_text):
        return "result text matched USAGE_LIMIT_TEXT"
    return None


USAGE_LIMIT_SIGNALS = {
    "rate_limit_event": rate_limit_event_signal,
    "assistant": assistant_usage_limit_signal,
    "result": result_usage_limit_signal,
}


def usage_limit_signal(event: dict) -> str | None:
    """Name the usage-limit signal this event carries, or None.

    Structured fields are preferred and checked first; the text match is a
    fallback for the day those fields change. See the module docstring for what
    each signal looks like in a real transcript.
    """
    detect = USAGE_LIMIT_SIGNALS.get(str(event.get("type")))
    return None if detect is None else detect(event)


class LiveDetector:
    """Run run_eval.py's detection over a stream consumed line by line.

    ``feed_line`` returns the decisive verdict once the stream decides, and
    None while undecided. run_eval.py's ``triggered`` accumulator is only ever
    set True immediately before returning, so a ``result`` event decides False,
    exactly as here. The detector keeps no event history: only the verdict, the
    session id, whether any line parsed at all, and any usage-limit signal.

    A usage limit is only recognised while the verdict is still undecided: once
    a tool call has decided the invocation, a later rate-limit event cannot undo
    it. ``decided`` is what the reader loop stops on, because either outcome
    ends the invocation.
    """

    def __init__(self, clean_name: str) -> None:
        self.clean_name = clean_name
        self.state = StreamTriggerState(clean_name)
        self.verdict: bool | None = None
        self.session_id: str | None = None
        self.parsed_any = False
        self.decided_on_result = False
        self.usage_limit_signal: str | None = None

    @property
    def decided(self) -> bool:
        """True once nothing further in the stream can change the outcome."""
        return self.verdict is not None or self.usage_limit_signal is not None

    def feed_line(self, line: str) -> bool | None:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            return self.verdict
        if not isinstance(event, dict):
            return self.verdict
        self.parsed_any = True
        self._record_session(event)
        if self.decided:
            return self.verdict
        signal = usage_limit_signal(event)
        if signal is not None:
            self.usage_limit_signal = signal
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


def drain_buffer(buffer: str, out, detector: LiveDetector) -> tuple[str, bool]:
    """Archive every complete line in ``buffer``, feeding each to the detector.

    Lines keep being archived after the outcome lands, so whatever already
    arrived reaches the transcript; only the detector stops deciding. Returns
    the unconsumed tail and whether the detector has decided.
    """
    while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        out.write(line + "\n")
        stripped = line.strip()
        if stripped and not detector.decided:
            detector.feed_line(stripped)
    out.flush()
    return buffer, detector.decided


def stream_process(process: subprocess.Popen, out, detector: LiveDetector, timeout: float) -> bool:
    """Consume stdout live until the detector decides (a verdict or a usage
    limit), EOF, or the timeout.

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
            buffer, decided = drain_buffer(buffer, out, detector)
            if decided:
                break
        elif process.poll() is not None:
            break
    buffer += decoder.decode(b"", final=True)
    if buffer:
        out.write(buffer)
        if not detector.decided and buffer.strip():
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

    A usage limit is checked first: it is a non-execution, so it can never be
    scored as a trigger verdict of either polarity.
    """
    session_id = process_result.session_id
    if process_result.usage_limit_signal is not None:
        return AttemptOutcome(
            "void",
            USAGE_LIMIT_REASON,
            None,
            session_id,
            started_utc,
            duration_s,
            None,
            process_result.usage_limit_signal,
        )
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
        usage_limit_signal=detector.usage_limit_signal,
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


class ResumeError(StartupError):
    """A resume precondition failed; no row may be appended."""


def cell_of(invocation: Invocation) -> CellKey:
    return (invocation.query_index, invocation.run, invocation.arm.label)


def row_cell(row: dict) -> CellKey:
    return (int(row["query_index"]), int(row["run"]), str(row["arm_label"]))


def read_existing_rows(results_path: Path) -> list[dict]:
    """Parse an existing results.jsonl into rows.

    Only a final line left truncated by a crash is tolerated (rows are
    flushed one per line, so nothing else can be partial). Any other malformed
    or incomplete row aborts: guessing at it would misjudge which cells ran.
    """
    text = results_path.read_text(encoding="utf-8")
    lines = text.split("\n")
    ends_with_newline = text.endswith("\n")
    if ends_with_newline:
        lines.pop()
    rows: list[dict] = []
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            if number == len(lines) and not ends_with_newline:
                print(
                    f"Warning: final line {number} of {results_path} is truncated "
                    f"(crash mid-write); it is ignored and dropped before appending",
                    file=sys.stderr,
                )
                continue
            raise ResumeError(f"{results_path} line {number} is not valid JSON: {error}") from error
        if not isinstance(row, dict):
            raise ResumeError(f"{results_path} line {number} is not a JSON object")
        missing = [
            field
            for field in ("query_index", "run", "arm_label", "attempt", "status")
            if field not in row
        ]
        if missing:
            raise ResumeError(f"{results_path} line {number} lacks field(s): {', '.join(missing)}")
        rows.append(row)
    return rows


def is_usage_limit_row(row: dict) -> bool:
    return row.get("status") == "void" and row.get("invalid_reason") == USAGE_LIMIT_REASON


def build_resume_state(rows: list[dict]) -> ResumeState:
    """Classify every cell present in existing rows as complete or interrupted.

    Complete: any ``valid`` row, or MAX_ATTEMPTS spent executions. Interrupted:
    anything below that, which resumes at the next unused attempt number so the
    per-cell execution total stays capped at MAX_ATTEMPTS across sessions.
    ``usage_limit`` rows are non-executions and spend no budget, so a cell whose
    only row is one re-runs with its full budget.
    """
    by_cell: dict[CellKey, list[dict]] = {}
    for row in rows:
        by_cell.setdefault(row_cell(row), []).append(row)
    complete: set[CellKey] = set()
    progress: dict[CellKey, CellProgress] = {}
    for key, cell_rows in by_cell.items():
        highest = max(int(row["attempt"]) for row in cell_rows)
        spent = sum(1 for row in cell_rows if not is_usage_limit_row(row))
        if any(row["status"] == "valid" for row in cell_rows) or spent >= MAX_ATTEMPTS:
            complete.add(key)
        else:
            progress[key] = CellProgress(next_attempt=highest + 1, attempts_spent=spent)
    return ResumeState(frozenset(complete), progress, len(rows))


def verify_plan_covers(plan: list[Invocation], rows: list[dict], results_path: Path) -> None:
    """Abort unless the regenerated plan covers every cell already recorded."""
    planned = {cell_of(invocation) for invocation in plan}
    missing = sorted({row_cell(row) for row in rows} - planned)
    if not missing:
        return
    head = missing[:UNCOVERED_CELLS_SHOWN]
    shown = ", ".join(f"q{index} r{run} {label}" for index, run, label in head)
    hidden = len(missing) - len(head)
    more = f" (and {hidden} more)" if hidden else ""
    raise ResumeError(
        f"the regenerated plan does not cover {len(missing)} cell(s) already in "
        f"{results_path}: {shown}{more}. The plan arguments (seed, fixture, "
        f"--queries, --runs, labels) must match the interrupted run."
    )


def latest_manifest(out_dir: Path) -> Path:
    """Return the newest manifest by its embedded UTC stamp, then suffix."""
    candidates = []
    for path in sorted(out_dir.iterdir()):
        match = MANIFEST_PATTERN.fullmatch(path.name)
        if match:
            candidates.append(((match.group(1), int(match.group(2) or 0)), path))
    if not candidates:
        raise ResumeError(
            f"no manifest-<utcstamp>.json found in {out_dir}; "
            f"cannot verify description and fixture digests for --resume"
        )
    return max(candidates)[1]


def verify_provenance(config: Config, arms: dict[str, Arm], manifest_path: Path) -> dict[str, str]:
    """Abort if any provenance value drifted since that manifest.

    Resuming across an edited description, an edited fixture, or a different
    skill name would mix configurations inside one result set, so every
    difference is named and the run stops.
    """
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    fixture_sha256 = sha256_text(config.fixture.read_text(encoding="utf-8"))
    drift = []
    recorded_skill_name = manifest.get("skill_name")
    if recorded_skill_name != config.skill_name:
        drift.append(
            f"skill name: manifest {recorded_skill_name!r} != current "
            f"{config.skill_name!r} (resolved: {config.skill_name_resolution})"
        )
    recorded_fixture = manifest.get("fixture_sha256")
    if recorded_fixture != fixture_sha256:
        drift.append(
            f"fixture {config.fixture}: manifest {recorded_fixture} != current {fixture_sha256}"
        )
    recorded_descriptions = manifest.get("descriptions") or {}
    for key, arm in arms.items():
        recorded = (recorded_descriptions.get(key) or {}).get("sha256")
        if recorded != arm.sha256:
            drift.append(
                f"description {key} (label {arm.label}): "
                f"manifest {recorded} != current {arm.sha256}"
            )
    if drift:
        raise ResumeError(
            f"provenance drift against {manifest_path}; refusing to resume:\n  "
            + "\n  ".join(drift)
        )
    verified = {
        "manifest": str(manifest_path),
        "skill_name": config.skill_name,
        "fixture_sha256": fixture_sha256,
    }
    for key, arm in arms.items():
        verified[f"description_{key}_sha256"] = arm.sha256
    return verified


def print_resume_summary(
    state: ResumeState,
    plan: list[Invocation],
    remaining: list[Invocation],
    verified: dict[str, str],
) -> None:
    interrupted = sorted(state.progress)
    print(
        f"[resume] rows read: {state.rows_read}\n"
        f"[resume] cells complete: {len(state.complete)}/{len(plan)}\n"
        f"[resume] cells interrupted mid-retry: {len(interrupted)}\n"
        f"[resume] cells remaining to run: {len(remaining)}",
        file=sys.stderr,
    )
    for key in interrupted:
        index, run, label = key
        cell = state.progress[key]
        print(
            f"[resume]   q{index} r{run} {label} continues at attempt "
            f"{cell.next_attempt} with {cell.attempts_spent} of "
            f"{MAX_ATTEMPTS} execution(s) spent",
            file=sys.stderr,
        )
    for name, value in verified.items():
        print(f"[resume] verified {name}: {value}", file=sys.stderr)


def prepare_resume(
    config: Config, arms: dict[str, Arm], plan: list[Invocation], results_path: Path
) -> tuple[ResumeState, list[Invocation], dict]:
    """Validate the resume preconditions and return what still has to run.

    Raises ResumeError if the existing rows, the regenerated plan, or the
    provenance recorded in the newest manifest disagree with this invocation.
    """
    rows = read_existing_rows(results_path)
    verify_plan_covers(plan, rows, results_path)
    verified = verify_provenance(config, arms, latest_manifest(config.out_dir))
    state = build_resume_state(rows)
    remaining = [item for item in plan if cell_of(item) not in state.complete]
    print_resume_summary(state, plan, remaining, verified)
    resume_info = {
        "results_file": str(results_path),
        "rows_read": state.rows_read,
        "cells_total": len(plan),
        "cells_complete": len(state.complete),
        "cells_remaining": len(remaining),
        "cells_continuing_at_attempt": {
            f"q{index}-r{run}-{label}": {
                "next_attempt": cell.next_attempt,
                "attempts_spent": cell.attempts_spent,
            }
            for (index, run, label), cell in sorted(state.progress.items())
        },
        "verified_provenance": verified,
    }
    return state, remaining, resume_info


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


def unique_manifest_path(out_dir: Path) -> Path:
    """Pick a manifest name that no existing file holds.

    Every invocation, resumed or not, writes its own manifest; a same-second
    collision takes a ``-<n>`` suffix rather than overwriting the earlier one.
    """
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    manifest_path = out_dir / f"manifest-{stamp}.json"
    suffix = 2
    while manifest_path.exists():
        manifest_path = out_dir / f"manifest-{stamp}-{suffix}.json"
        suffix += 1
    return manifest_path


def write_manifest(
    config: Config,
    arms: dict[str, Arm],
    desc_paths: dict[str, Path],
    queries: list[tuple[int, str]],
    resume_info: dict | None = None,
) -> Path:
    manifest_path = unique_manifest_path(config.out_dir)
    manifest = {
        "argv": sys.argv,
        "seed": config.seed,
        "model": config.model,
        "runs": config.runs,
        "timeout": config.timeout,
        "skill_name": config.skill_name,
        "skill_name_resolution": config.skill_name_resolution,
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
        "resumed": config.resume,
    }
    if resume_info is not None:
        manifest["resume"] = resume_info
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


def drop_truncated_tail(path: Path) -> None:
    """Discard a final line that a crash left unterminated, before appending.

    ``read_existing_rows`` already ignores such a line, and it carries no
    classifiable attempt. Removing it (rather than just terminating it) keeps
    the file parseable end to end, so a second resume does not trip over a
    malformed line that is no longer last.
    """
    data = path.read_bytes()
    if not data or data.endswith(b"\n"):
        return
    keep = data.rfind(b"\n") + 1
    with path.open("rb+") as handle:
        handle.truncate(keep)


class UsageLimitAbort(RuntimeError):
    """The account ran out of quota; the run stops and keeps what it has.

    Unlike StartupError this is raised mid-run, after rows were written, so its
    message must tell the operator exactly where the run stopped and how to
    continue it.
    """


def usage_limit_message(
    invocation: Invocation,
    attempt: int,
    plan_size: int,
    outcome: AttemptOutcome,
    results_path: Path,
) -> str:
    return (
        f"usage limit reached; the run stopped at ordinal {invocation.ordinal} of "
        f"{plan_size} (q{invocation.query_index} {invocation.arm.label} "
        f"r{invocation.run} attempt {attempt}).\n"
        f"  signal: {outcome.usage_limit_signal}\n"
        f"  The model never ran, so this attempt is recorded as status=void "
        f"invalid_reason={USAGE_LIMIT_REASON} triggered=null. It was not retried "
        f"(a usage limit does not clear in seconds) and it does not spend the "
        f"cell's retry budget.\n"
        f"  Everything already measured is preserved in {results_path}.\n"
        f"  Once the quota resets, re-run the same command with --resume: the "
        f"stopped cell re-runs from a fresh attempt and the run continues from "
        f"where it stopped."
    )


def execute_plan(
    config: Config,
    plan: list[Invocation],
    results_path: Path,
    state: ResumeState | None = None,
    total: int | None = None,
) -> None:
    """Run every invocation in ``plan``, appending one row per attempt.

    ``plan`` is the remaining work; ``total`` is the size of the full plan, so
    progress lines keep the ordinals of the original run. A cell interrupted
    mid-retry starts at its recorded next attempt number with its recorded
    executions already spent, which keeps the per-cell execution total at
    MAX_ATTEMPTS across sessions.

    Raises UsageLimitAbort on the first usage-limit void: that attempt is not
    retried and no further invocation is launched.
    """
    transcripts_dir = config.out_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    plan_size = len(plan) if total is None else total
    mode = "a" if config.resume else "w"
    if mode == "a" and results_path.exists():
        drop_truncated_tail(results_path)
    with results_path.open(mode, encoding="utf-8") as results:
        for invocation in plan:
            label = sanitize_label(invocation.arm.label)
            cell = FIRST_CELL_PROGRESS if state is None else state.progress_for(cell_of(invocation))
            attempt = cell.next_attempt
            spent = cell.attempts_spent
            while spent < MAX_ATTEMPTS:
                stem = transcripts_dir / (
                    f"q{invocation.query_index:03d}-{label}-r{invocation.run}-a{attempt}"
                )
                outcome = run_attempt(config, invocation.arm, invocation.query, stem)
                row = {
                    "skill_name": config.skill_name,
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
                    f"[{invocation.ordinal}/{plan_size}] q{invocation.query_index} "
                    f"{invocation.arm.label} r{invocation.run} a{attempt}: "
                    f"{outcome.status} triggered={outcome.triggered} "
                    f"ending={outcome.ending} reason={outcome.invalid_reason} "
                    f"{outcome.duration_s}s",
                    file=sys.stderr,
                )
                if outcome.invalid_reason == USAGE_LIMIT_REASON:
                    raise UsageLimitAbort(
                        usage_limit_message(invocation, attempt, plan_size, outcome, results_path)
                    )
                if outcome.status == "valid":
                    break
                spent += 1
                attempt += 1


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
        "--resume",
        action="store_true",
        help="Append to an existing results.jsonl, skipping cells already complete "
        "(without it, an existing results.jsonl is refused)",
    )
    parser.add_argument(
        "--queries",
        default=None,
        help="0-based index filter (e.g. 3 or 1,4 or 2-5) or regex on query text",
    )
    parser.add_argument(
        "--skill-name",
        default=None,
        help="Skill name embedded in the synthetic command file, used verbatim "
        "(default: derived from the fixture path's skills/<name>/ segment; a "
        "fixture path without one aborts the run instead of guessing)",
    )
    return parser.parse_args()


def precondition_error(config: Config, results_path: Path) -> str | None:
    """Return the reason this invocation must not start, or None.

    The refusal to touch an existing results.jsonl is the default; only
    --resume lifts it, and then the file must actually be there.
    """
    if config.resume and config.dry_run:
        return "--resume and --dry-run are mutually exclusive"
    if config.resume and not results_path.exists():
        return f"--resume given but {results_path} does not exist"
    if not config.dry_run and not config.resume and results_path.exists():
        return f"{results_path} already exists; refusing to overwrite"
    return None


def run_eval(args: argparse.Namespace) -> int:
    """Resolve the configuration, plan, and execute; raise StartupError to abort."""
    skill_name, skill_name_resolution = resolve_skill_name(args.skill_name, args.fixture)
    config = Config(
        fixture=args.fixture,
        out_dir=args.out_dir,
        model=args.model,
        runs=args.runs,
        timeout=args.timeout,
        seed=args.seed,
        skill_name=skill_name,
        skill_name_resolution=skill_name_resolution,
        project_root=find_project_root(),
        dry_run=args.dry_run,
        resume=args.resume,
    )
    config.out_dir.mkdir(parents=True, exist_ok=True)
    results_path = config.out_dir / "results.jsonl"
    blocked = precondition_error(config, results_path)
    if blocked:
        raise StartupError(blocked)
    fixture_items = json.loads(config.fixture.read_text(encoding="utf-8"))
    queries = select_queries(fixture_items, args.queries)
    if not queries:
        raise StartupError("no queries selected")
    desc_paths = {"A": args.desc_a, "B": args.desc_b}
    arms = {}
    for key, label in (("A", args.label_a), ("B", args.label_b)):
        text = read_frozen_description(desc_paths[key])
        arms[key] = Arm(label=label, text=text, sha256=sha256_text(text))
    plan = list(plan_invocations(config, queries, arms))
    remaining = plan
    state: ResumeState | None = None
    resume_info: dict | None = None
    if config.resume:
        state, remaining, resume_info = prepare_resume(config, arms, plan, results_path)
    manifest_path = write_manifest(config, arms, desc_paths, queries, resume_info)
    print(f"Manifest: {manifest_path}", file=sys.stderr)
    if config.dry_run:
        print_dry_run_preview(config, plan)
        return 0
    if config.resume and not remaining:
        print(f"All {len(plan)} cells already complete; nothing to run.", file=sys.stderr)
        print(f"Results: {results_path}", file=sys.stderr)
        return 0
    execute_plan(config, remaining, results_path, state, len(plan))
    print(f"Results: {results_path}", file=sys.stderr)
    return 0


def main() -> int:
    try:
        return run_eval(parse_args())
    except StartupError as error:
        print(f"Error: {error}", file=sys.stderr)
        return EXIT_STARTUP_ERROR
    except UsageLimitAbort as error:
        print(f"Aborted: {error}", file=sys.stderr)
        return EXIT_USAGE_LIMIT


if __name__ == "__main__":
    sys.exit(main())
