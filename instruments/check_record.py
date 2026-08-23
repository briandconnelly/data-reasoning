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
ROUTES = {"review", "construct", "bound"}
DECIDE_VERDICTS = {"robust", "prior-sensitive", "loss-sensitive", "dominated"}
VOI_VERDICTS = {"worth-it", "not-worth-it", "sensitive", "break-even-only"}

# A template placeholder is `<` + a letter + text without `<`, `>`, `=` + `>`.
# Inequalities (`< 1.5`, `<5%`) start with a space or digit; HTML attributes
# carry `=`; bare HTML tags are excluded by name below, and a Markdown
# autolink (`<https://...>`, `<name@example.com>`, `<mailto:...>`) is real
# record content, not a template blank, so it is excluded too. Residual:
# `<q and r>` with a letter-initial inequality still reads as a placeholder.
PLACEHOLDER = re.compile(r"<([A-Za-z][^<>\n=]*)>")
HTML_TAGS = frozenset(
    {
        "a",
        "b",
        "br",
        "code",
        "details",
        "div",
        "em",
        "hr",
        "i",
        "img",
        "kbd",
        "li",
        "ol",
        "p",
        "pre",
        "span",
        "strong",
        "sub",
        "summary",
        "sup",
        "table",
        "td",
        "th",
        "tr",
        "u",
        "ul",
    }
)


def _has_placeholder(value: str) -> bool:
    for m in PLACEHOLDER.finditer(value):
        inner = m.group(1).strip().rstrip("/").strip().lower()
        if inner in HTML_TAGS:
            continue
        if "://" in inner or "@" in inner or inner.startswith(("http", "mailto:")):
            continue
        return True
    return False


# A slot value, or a required section's whole content, that says it is
# pending is the sanctioned plan-stage state: the skills write the record
# before the analysis fills it.
# "pending" states the slot is unfilled; it is the whole value, optionally
# followed by an annotation introduced by a delimiter ("pending — waiting
# on the export"); an ASCII dash must be whitespace-delimited so the
# hyphenated word "pending-state" is not read as marker plus annotation.
# Prose that merely opens with the word ("Pending replication by another
# team, the result stands") is a filled slot and must not suspend the
# completeness checks.
PENDING = re.compile(r"^\(?\s*pending(?:\s*[)\u2014\u2013:;]|\s+-{1,2}(?=\s|\Z)|\s*\Z)", re.I)
# The section-level marker must be the canonical parenthesized form (e.g.
# "(pending -- to be completed after Analysis)"), not merely a passage that
# happens to start with the word: a table cell or a sentence of ordinary
# prose can start with "pending" without the section being in-progress.
SECTION_PENDING = re.compile(r"^\(\s*pending\b.*\)\Z", re.I | re.S)

DELIMITERS = (" —", " -", ";", ":", " (", ",")
MIN_TABLE_ROWS = 2  # header + at least one data row

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
CELL_SPLIT = re.compile(r"(?<!\\)\|")
INLINE_COMMENT = re.compile(r"<!--.*?-->")


def _strip_hidden(text: str) -> tuple[str, bool]:
    """Blank out what a reader never sees — fenced code blocks and HTML
    comments — in one pass, so the two cannot hide each other's delimiters.
    Line count is preserved. Per CommonMark: a fence closes only on a same-
    character run at least as long as the opener with nothing but whitespace
    after it; `<!--` inside a fence is code; a comment never closed runs to
    the end of the document. Returns (body, fence_still_open_at_eof)."""
    out: list[str] = []
    fence: tuple[str, int] | None = None
    in_comment = False
    for line in text.split("\n"):
        if fence is not None:
            m = FENCE.match(line)
            if (
                m
                and m.group(1)[0] == fence[0]
                and len(m.group(1)) >= fence[1]
                and not line[m.end() :].strip()
            ):
                fence = None
            out.append("")
            continue
        if in_comment:
            out.append("")
            if "-->" in line:
                in_comment = False
            continue
        m = FENCE.match(line)
        if m:
            fence = (m.group(1)[0], len(m.group(1)))
            out.append("")
            continue
        visible = INLINE_COMMENT.sub("", line)
        if "<!--" in visible:
            visible = visible[: visible.index("<!--")]
            in_comment = True
        out.append(visible.rstrip())
    return "\n".join(out), fence is not None


# The colon must be present, either inside the emphasis ("**Verdict:**") or
# immediately after it ("**Verdict**:"). Without it the line has no label
# delimiter and is not a slot.
LABEL_EMPHASIS = re.compile(r"^- (\*\*|__|\*|_)([^*_:\n]+?)(?::\1|\1:)\s*")


def _unemphasize(line: str) -> str:
    """'- **Verdict:** x', '- **Verdict**: x', '- *Verdict*: x' -> '- Verdict: x'.
    Emphasis on a slot label is presentation, not a different slot."""
    return LABEL_EMPHASIS.sub(lambda m: f"- {m.group(2)}: ", line, count=1)


CODE_SPAN = re.compile(r"(`+)(?:(?!\1)[^\n])+?\1")


def _mask_code_pipes(line: str) -> str:
    """Hide `|` inside inline code spans from the cell splitter; `_unmask`
    restores it inside the cell."""
    return CODE_SPAN.sub(lambda m: m.group(0).replace("|", "\x00"), line)


def _unmask(cell: str) -> str:
    return cell.replace("\x00", "|")


def detect(text: str) -> str | None:
    """Kind of record, or None. A title signature alone is not enough: a
    user's own note titled `# Investigation: …` is not a ledger. The record
    must also carry at least one of its kind's required headings."""
    first = text.lstrip().split("\n", 1)[0]
    for prefix, kind in SIGNATURES.items():
        if first.startswith(prefix):
            body = "\n" + "\n".join(line.rstrip() for line in text.split("\n")) + "\n"
            if any(("\n" + h + "\n") in body for h in REQUIRED_SECTIONS[kind]):
                return kind
            return None
    return None


def _is_placeholder(value: str) -> bool:
    v = value.strip()
    return not v or v == "..." or _has_placeholder(v)


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
    Pipes inside inline code spans are masked before the split.
    """
    rows = []
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if line.startswith("|") and not set(line) <= {"|", "-", " ", ":"}:
            cells = [_unmask(c.strip()) for c in CELL_SPLIT.split(_mask_code_pipes(line))]
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
            yield from (
                _unmask(c.strip()) for c in CELL_SPLIT.split(_mask_code_pipes(stripped.strip("|")))
            )


def _bullet_slot_values(body: str):
    """Values of '- Label: value' bullet lines only -- not table cells, not
    the title. This is the slot position a bare 'pending' value legitimately
    sits in; a table cell (e.g. an Evidence column noting evidence is still
    pending for one row) is ordinary content, not a record-wide marker."""
    for line in body.split("\n")[1:]:
        stripped = line.strip()
        if stripped.startswith("- ") and ":" in stripped:
            yield stripped.split(":", 1)[1]


def _in_progress(body: str) -> bool:
    if any(v.strip() == "..." or _has_placeholder(v) for v in _slot_values(body)):
        return True
    # A slot value, or a required section's whole content, that says it is
    # pending is the sanctioned plan-stage state. Prose that merely begins
    # with the word is not.
    if any(PENDING.match(v.strip()) for v in _bullet_slot_values(body)):
        return True
    kind = detect(body) or ""
    return any(
        SECTION_PENDING.match(_section(body, h).strip()) for h in REQUIRED_SECTIONS.get(kind, [])
    )


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
    body, unterminated_fence = _strip_hidden(text)
    # An unterminated fence blanks everything after it (including any
    # genuinely-present later sections), so completeness findings there
    # would fail correct work — treat the record as in-progress instead.
    # Vocabulary checks still run on whatever body remains (the pre-fence
    # part).
    in_progress = unterminated_fence or _in_progress(body)
    if unterminated_fence:
        findings.append(
            "unterminated code fence: completeness past it was not checked "
            "(close the fence, then re-validate)"
        )

    if not in_progress:
        for heading in REQUIRED_SECTIONS[kind]:
            if ("\n" + heading + "\n") not in body:
                findings.append(f"required section missing: {heading}")
            elif not _section(body, heading).strip():
                findings.append(f"required section empty: {heading}")

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
            stripped = _unemphasize(line.strip())
            if stripped.startswith(("- Disposition:", "- Dispositions:")):
                value = stripped.split(":", 1)[1]
                if _is_placeholder(value):
                    continue
                if _leading_token(value, DISPOSITIONS | {"none"}) is None:
                    findings.append(
                        f"disposition {_normalize(value)!r} does not begin with a value "
                        f"from the closed set {sorted(DISPOSITIONS | {'none'})} — 'valid' and "
                        f"'certified' are not dispositions"
                    )
            if stripped.startswith("- Route:"):
                value = stripped.split(":", 1)[1]
                if not _is_placeholder(value) and _leading_token(value, ROUTES) is None:
                    findings.append(
                        f"route {_normalize(value)!r} does not begin with a value from the "
                        f"closed set {sorted(ROUTES)}"
                    )
        if not in_progress:
            handoff = _section(body, "## Handoff")
            if not any(
                _unemphasize(line.strip()).startswith("- Dispositions:")
                for line in handoff.splitlines()
            ):
                findings.append("Handoff: required '- Dispositions:' slot is missing")

    elif kind in ("decision", "voi"):
        allowed = DECIDE_VERDICTS if kind == "decision" else VOI_VERDICTS
        heading = "## Verdict" if kind == "decision" else "## VoI"
        section = _section(body, heading)
        for line in section.splitlines():
            stripped = _unemphasize(line.strip())
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
            _unemphasize(line.strip()).startswith("- Verdict:") for line in section.splitlines()
        ):
            findings.append("Verdict: required '- Verdict:' slot is missing")

    return findings


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: check_record.py <record.md>", file=sys.stderr)
        return 2
    try:
        text = Path(argv[0]).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
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
