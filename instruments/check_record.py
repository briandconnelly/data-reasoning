#!/usr/bin/env python3
# instruments/check_record.py
"""Fixture-neutral structural validator for data-reasoning records.

Scope and limits are owned by
skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md;
this file enacts that scope and does not restate it. Operationally: it checks
required sections, closed vocabularies, and non-empty required slots; it
suspends completeness findings while a record still carries template
placeholders (the skills mandate writing the template before filling it).

Exit codes: 0 clean, 1 findings (one per stdout line), 2 not a recognized
record or unreadable.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SIGNATURES = {
    "# Investigation: ": "ledger",
    "# Exploration: ": "exploration",
    "# Identification Review: ": "review",
    "# Decision Record: ": "decision",
    "# VoI Record: ": "voi",
}

REQUIRED_SECTIONS = {
    "ledger": [
        "## Problem",
        "## Hypotheses",
        "## Sources",
        "## Data Validity",
        "## Tests",
        "## Amendments",
        "## Conclusion",
    ],
    "exploration": ["## Frame", "## Orientation record"],
    "review": ["## Question", "## Handoff"],
    "decision": [
        "## Decision frame",
        "## Decision-state model",
        "## Evidence and update",
        "## Robustness",
        "## Verdict",
        "## Handoff",
    ],
    "voi": ["## VoI"],
}

STATUSES = {"REFUTED", "UNRESOLVED"}
OUTCOMES = {"NOT_TESTED", "CONSISTENT", "CONTRADICTED", "NON_DISCRIMINATING"}
DISPOSITIONS = {"identified-if", "assumption-contradicted", "unresolved", "not-constructible"}
DECIDE_VERDICTS = {"robust", "prior-sensitive", "loss-sensitive", "dominated"}
VOI_VERDICTS = {"worth-it", "not-worth-it", "sensitive", "break-even-only"}

PLACEHOLDER = re.compile(r"<[^<>\n]+>")
DELIMITERS = (" —", " -", ";", ":", " (", ",")
MIN_TABLE_ROWS = 2  # header + at least one data row

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
CELL_SPLIT = re.compile(r"(?<!\\)\|")


def _strip_fences(text: str) -> str:
    """Blank out fenced code blocks (backtick or tilde, up to 3-space indent)
    so quoted records and code samples are never scanned as record content.
    Line count is preserved."""
    out = []
    fence: str | None = None
    for line in text.split("\n"):
        m = FENCE.match(line)
        if fence is None:
            if m:
                fence = m.group(1)[0]
                out.append("")
                continue
            out.append(line)
        else:
            if m and m.group(1)[0] == fence:
                fence = None
            out.append("")
    return "\n".join(out)


def detect(text: str) -> str | None:
    first = text.lstrip().split("\n", 1)[0]
    for prefix, kind in SIGNATURES.items():
        if first.startswith(prefix):
            return kind
    return None


def _is_placeholder(value: str) -> bool:
    v = value.strip()
    return not v or v == "..." or bool(PLACEHOLDER.search(v))


def _normalize(value: str) -> str:
    """Strip surrounding emphasis/code markers, which are presentation only."""
    return value.strip().strip("`*").strip()


def _leading_token(value: str, allowed: set[str]) -> str | None:
    """The value must BE an allowed token, or start with one followed by a
    delimiter (annotations after the token are legitimate)."""
    v = _normalize(value)
    for tok in sorted(allowed, key=len, reverse=True):
        if v == tok:
            return tok
        if v.startswith(tok) and v[len(tok) :].startswith(DELIMITERS):
            return tok
    return None


def _section(text: str, heading: str) -> str:
    start = text.find("\n" + heading + "\n")
    if start < 0:
        return ""
    rest = text[start + 1 + len(heading) :]
    nxt = rest.find("\n## ")
    return rest if nxt < 0 else rest[:nxt]


def _table_rows(section: str) -> list[list[str]]:
    """All markdown table rows in a section as cell lists, header included.

    Cells are split on unescaped pipes only: a `\\|` inside a cell (e.g. a
    shell pipeline quoted in a Method cell) does not shift the columns.
    Known residual leniency: a pipe inside an inline code span still splits;
    that can only shift a cell downstream to a column the checks below don't
    key on by name, which is at worst a false negative, never a false
    positive on a checked column.
    """
    rows = []
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if line.startswith("|") and not set(line) <= {"|", "-", " ", ":"}:
            cells = [c.strip() for c in CELL_SPLIT.split(line)]
            if cells and cells[0] == "":
                cells = cells[1:]
            if cells and cells[-1] == "":
                cells = cells[:-1]
            rows.append(cells)
    return rows


def _column(rows: list[list[str]], name: str) -> list[str]:
    """Values of the column whose header contains `name`; [] if absent."""
    if not rows:
        return []
    header = [h.lower() for h in rows[0]]
    idx = next((i for i, h in enumerate(header) if name.lower() in h), None)
    if idx is None:
        return []
    return [r[idx] for r in rows[1:] if idx < len(r)]


def _require_column(rows: list[list[str]], name: str, where: str, findings: list[str]) -> bool:
    """True if `rows`' header has a column matching `name`; else records a
    finding and returns False. An empty table is left to the dedicated
    empty-table finding, not duplicated here."""
    if not rows:
        return False
    if not any(name.lower() in h.lower() for h in rows[0]):
        findings.append(f"{where}: table lacks a {name!r} column")
        return False
    return True


def _slot_values(body: str):
    """Values sitting in slot positions: '- Label: value' lines, table data
    cells, and the title line's remainder."""
    lines = body.split("\n")
    if lines:
        first = lines[0]
        if ": " in first:
            yield first.split(": ", 1)[1]
    for line in lines[1:]:
        stripped = line.strip()
        if stripped.startswith("- ") and ":" in stripped:
            yield stripped.split(":", 1)[1]
        elif stripped.startswith("|") and not set(stripped) <= {"|", "-", " ", ":"}:
            yield from (c.strip() for c in CELL_SPLIT.split(stripped.strip("|")))


def _in_progress(body: str) -> bool:
    return any(v.strip() == "..." or PLACEHOLDER.search(v) for v in _slot_values(body))


def _check_claim(value: str, where: str, findings: list[str]) -> None:
    if _is_placeholder(value):
        return
    v = _normalize(value)
    if v in ("causal", "data-artifact") or re.fullmatch(r"descriptive( \(estimand: .+\))?", v):
        return
    findings.append(
        f"{where}: claim class {v!r} is not in the closed set "
        f"causal / descriptive (estimand: ...) / data-artifact"
    )


def check(text: str) -> list[str]:  # noqa: PLR0912, PLR0915 -- one findings pass per record kind
    kind = detect(text)
    if kind is None:
        raise ValueError("not a recognized record")
    findings: list[str] = []
    body = _strip_fences(text)
    in_progress = _in_progress(body)

    if not in_progress:
        for heading in REQUIRED_SECTIONS[kind]:
            if ("\n" + heading + "\n") not in body:
                findings.append(f"required section missing: {heading}")

    if kind == "ledger":
        # No id-grammar check on `id` cells (e.g. H1 vs H4 (retrospective)):
        # the template's own retrospective-hypothesis form breaks a strict
        # grammar, and leniency wins when a fix would force a false positive.
        hyp = _table_rows(_section(body, "## Hypotheses"))
        hyp_ok = in_progress or _require_column(hyp, "claim", "Hypotheses", findings)
        if hyp_ok:
            for v in _column(hyp, "claim"):
                _check_claim(v, "Hypotheses", findings)
        if not in_progress:
            if len(hyp) < MIN_TABLE_ROWS:
                findings.append("Hypotheses: table has no data rows")
            if _require_column(hyp, "necessary prediction", "Hypotheses", findings):
                for i, v in enumerate(_column(hyp, "necessary prediction"), 1):
                    if not v.strip():
                        findings.append(f"Hypotheses row {i}: necessary prediction is empty")
        tests = _table_rows(_section(body, "## Tests"))
        if in_progress or _require_column(tests, "outcome", "Tests", findings):
            for v in _column(tests, "outcome"):
                if _is_placeholder(v):
                    continue
                if _leading_token(v, OUTCOMES) is None:
                    findings.append(
                        f"Tests: outcome {v!r} does not begin with a value from the "
                        f"closed set {sorted(OUTCOMES)}"
                    )
        if not in_progress and len(tests) < MIN_TABLE_ROWS:
            findings.append("Tests: table has no data rows")
        concl = _table_rows(_section(body, "## Conclusion"))
        if in_progress or _require_column(concl, "status", "Conclusion", findings):
            for v in _column(concl, "status"):
                if _is_placeholder(v):
                    continue
                if _normalize(v) not in STATUSES:
                    findings.append(
                        f"Conclusion: status {_normalize(v)!r} is not REFUTED or UNRESOLVED "
                        f"(the status set is closed)"
                    )
        if in_progress or _require_column(concl, "claim", "Conclusion", findings):
            for v in _column(concl, "claim"):
                _check_claim(v, "Conclusion", findings)
        if not in_progress and len(concl) < MIN_TABLE_ROWS:
            findings.append("Conclusion: per-hypothesis table has no data rows")

    elif kind == "review":
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith(("- Disposition:", "- Dispositions:")):
                value = stripped.split(":", 1)[1]
                if _is_placeholder(value) or _normalize(value) == "none":
                    continue
                if _leading_token(value, DISPOSITIONS) is None:
                    findings.append(
                        f"disposition {_normalize(value)!r} does not begin with a value "
                        f"from the closed set {sorted(DISPOSITIONS)} — 'valid' and "
                        f"'certified' are not dispositions"
                    )
        if not in_progress:
            handoff = _section(body, "## Handoff")
            if not any(line.strip().startswith("- Dispositions:") for line in handoff.splitlines()):
                findings.append("Handoff: required '- Dispositions:' slot is missing")

    elif kind in ("decision", "voi"):
        allowed = DECIDE_VERDICTS if kind == "decision" else VOI_VERDICTS
        heading = "## Verdict" if kind == "decision" else "## VoI"
        section = _section(body, heading)
        for line in section.splitlines():
            stripped = line.strip()
            if stripped.startswith("- Verdict:"):
                value = stripped.split(":", 1)[1]
                if _is_placeholder(value):
                    continue
                if _leading_token(value, allowed) is None:
                    findings.append(
                        f"verdict {_normalize(value)!r} does not begin with a value "
                        f"from the closed set {sorted(allowed)}"
                    )
        if not in_progress and not any(
            line.strip().startswith("- Verdict:") for line in section.splitlines()
        ):
            findings.append("Verdict: required '- Verdict:' slot is missing")

    return findings


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: check_record.py <record.md>", file=sys.stderr)
        return 2
    try:
        text = Path(argv[0]).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"unreadable: {exc}", file=sys.stderr)
        return 2
    try:
        findings = check(text)
    except ValueError:
        return 2
    for f in findings:
        print(f)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
