#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Check an identification-review record's schema-scope contract.

This is a machine encoding of the record's *shape*, not its content: required
fields present, the Route value drawn from its closed set, every per-Design
Disposition value drawn from its closed set, route-aware block structure
(``review``/``construct`` require at least one Design block and no Bound
block; ``bound`` requires the Bound block and no Design blocks), the Handoff
Dispositions slot reusing exactly the disposition values assigned above --
set equality, neither fabricating nor omitting -- (or the literal ``none``
when the record's route assigns none), an ``identified-if`` disposition
carrying at least one assumption probe run with its result recorded (probes
that are empty or ``none run`` reject that disposition and no other), the
per-assumption assessment gates (issue #40: every assumption carries an
``A<n>`` id and exactly one probes-table row, each row's assessment is drawn
from its closed set, ``not-testable-here`` pairs with the probe cell ``NONE``
and a reason, and the disposition is one the assessments allow --
``_check_assessments`` states the scope), and forbidden certification vocabulary
(``valid``, ``certified``) absent from disposition slots. The
closed-set vocabulary and its semantics are governed by
``../SKILL.md`` § Routing (authority) and are already fixed
by decision -- see
``../decisions/004-dispositions-never-certify.md`` and
``skills/hypothesis-driven-analysis/decisions/004-single-authority-for-normative-rules.md``
for why this checker, rather than a reference file, is the one place outside
SKILL.md and the catalog's assertion rows where these strings legitimately
live in operable (as opposed to descriptive) form: a checker enforces, it
does not restate a rule for a reader.

Explicitly NOT this checker's claim:

- Whether the record preceded reasoning. That is scored from archived
  tool-call manifests per scenario, the way ``hypothesis-driven-analysis``'s
  ``check_prereg.py`` scores preregistration ordering -- a transcript-level
  fact this file never sees.
- The semantic quality of any assumption, probe, or threat entry (whether a
  named assumption is the *right* one, whether a probe result is correctly
  interpreted). Only structural presence is checked.

Advisory-only: a regex heuristic scans the record for digit-based
point-estimate patterns (``4.2 percentage points``, ``15%``) outside the
Bound block's Computed endpoints slot, which is numeric output's one licensed
home per ``decisions/005-numeric-policy.md``. This is a warning, never a gate
failure -- it is a known-limited heuristic (digits only; a spelled-out number
such as "four percentage points" is a documented miss, pinned by
``test_advisory_numeric_scan_documented_miss_spelled_out_number`` in the
paired test file) meant to prompt a human second look, not to police prose.

Exit codes:
  0  no gate failures (advisory warnings may still be printed)
  1  one or more gate failures
  2  UNVERIFIABLE: the record file could not be read
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROUTES = frozenset({"review", "construct", "bound"})
DISPOSITIONS = frozenset(
    {"identified-if", "assumption-contradicted", "unresolved", "not-constructible"}
)
FORBIDDEN_WORDS = ("valid", "certified")

# Per-assumption assessments (SKILL.md's per-route procedure, the authority
# for what each value means). RUN_ASSESSMENTS are the values a probe that ran
# can end on; `not-testable-here` pairs with the literal probe cell NO_PROBE.
ASSESSMENTS = frozenset(
    {"contradicted", "not-contradicted", "non-discriminating", "not-run", "not-testable-here"}
)
RUN_ASSESSMENTS = frozenset({"contradicted", "not-contradicted", "non-discriminating"})
BLOCKING_ASSESSMENTS = frozenset({"non-discriminating", "not-run"})
NO_PROBE = "NONE"
PROBE_COLUMNS = ("assumption", "probe", "assessment", "evidence or reason")

# A table counts as present-with-data when it carries a header row, a
# separator row, and at least one data row -- three pipe-delimited lines.
_MIN_TABLE_LINES = 3

EXIT_OK = 0
EXIT_GATE_FAILURE = 1
EXIT_UNVERIFIABLE = 2

_SECTION_HEADER = re.compile(r"^## (.+)$", re.MULTILINE)
_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$", re.MULTILINE)
# Any leading whitespace marks a sublist item: records indent nested lists
# with 2 spaces, 4 spaces, or tabs interchangeably, and an item the sublist
# collector misses is not picked up by the paragraph fallback either (its
# stripped form starts with "- ", which ends paragraph collection), so a
# narrower pattern here reads a populated slot as empty.
_SUBLIST_ITEM = re.compile(r"^[ \t]+- .+$")

# A probes slot whose content records no run result: the literal `none`,
# `none run`, `not run`, or `n/a`, optionally backtick-wrapped, optionally
# followed by a dash-introduced rationale (same dash discipline as
# _NONE_DISPOSITION below). SKILL.md's disposition semantics make
# `identified-if` conditional on probes run and reported, so a Design block
# pairing that disposition with one of these slots is rejected; other
# dispositions legitimately carry them (a named-only design ends
# `not-constructible`).
_NO_RESULT_PROBES = re.compile(
    r"^`?(?:none(?:\s+run)?|not\s+run|n/a)`?(?:\s+[—-]\s+.+)?$",
    re.IGNORECASE,
)

# The literal `none` Handoff Dispositions value, optionally backtick-wrapped,
# optionally followed by a trailing rationale introduced by an em-dash or a
# hyphen-dash surrounded by whitespace (never a bare hyphen -- a token like
# `not-constructible` must not be mistaken for `none` plus a rationale, so
# the dash must be padded by whitespace on both sides to count as one).
_NONE_DISPOSITION = re.compile(r"^`?none`?(?:\s+[—-]\s+.+)?$")

# Advisory-only heuristic: a digit-led number immediately followed by a unit
# word/symbol commonly used to report an effect size. Deliberately narrow --
# see the module docstring's "Advisory-only" section for its documented gap
# (spelled-out numbers).
_NUMERIC_ESTIMATE = re.compile(
    r"[-+]?\d+(?:\.\d+)?\s*(?:percentage\s+points?|pp|percent|%|points?)\b",
    re.IGNORECASE,
)


def _bullet_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"^- {re.escape(label)}:[ \t]*(.*)$", re.MULTILINE)


_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_INLINE_COMMENT = re.compile(r"<!--.*?-->")
_BACKTICK_RUN = re.compile(r"`+")


def _code_span_interiors(line: str) -> list[tuple[int, int]]:
    """(start, end) of every inline code-span interior. A span closes on a
    backtick run of exactly the opener's length, and a backslash-escaped
    backtick outside a span is literal text that opens nothing."""
    runs = [(m.start(), m.end()) for m in _BACKTICK_RUN.finditer(line)]
    spans: list[tuple[int, int]] = []
    i = 0
    while i < len(runs):
        start, end = runs[i]
        slashes = 0
        while start - slashes - 1 >= 0 and line[start - slashes - 1] == "\\":
            slashes += 1
        opener = start + 1 if slashes % 2 else start
        width = end - opener
        if width <= 0:
            i += 1
            continue
        for j in range(i + 1, len(runs)):
            nxt_start, nxt_end = runs[j]
            if nxt_end - nxt_start == width:
                spans.append((end, nxt_start))
                i = j + 1
                break
        else:
            i += 1
    return spans


def visible_markdown(text: str) -> str:
    """`text` with fenced blocks and HTML comments blanked, line count kept.
    An assumption or probe row that survives only inside a comment or a
    fenced example is documentation, not record content, and must not move
    the disposition gate."""
    out: list[str] = []
    fence: tuple[str, int] | None = None
    in_comment = False
    for line in text.split("\n"):
        if fence is not None:
            m = _FENCE.match(line)
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
        m = _FENCE.match(line)
        if m and not (m.group(1)[0] == "`" and "`" in line[m.end() :]):
            fence = (m.group(1)[0], len(m.group(1)))
            out.append("")
            continue
        visible = line
        masked = list(visible)
        for start, end in _code_span_interiors(visible):
            for k in range(start, end):
                masked[k] = "\x01"
        shadow = "".join(masked)
        for m2 in reversed(list(_INLINE_COMMENT.finditer(shadow))):
            visible = visible[: m2.start()] + visible[m2.end() :]
            shadow = shadow[: m2.start()] + shadow[m2.end() :]
        opener = shadow.find("<!--")
        if opener != -1:
            visible = visible[:opener]
            in_comment = True
        out.append(visible)
    return "\n".join(out)


def _label_region(body: str, label: str) -> str:
    """Raw text from ``- <label>:`` to the next top-level ``- `` bullet or
    heading, exclusive of both. Unlike ``find_bullet``/``find_sublist``, this
    returns the slot's content verbatim (not parsed into an inline value or a
    stripped item list), so callers that need to regex over raw table rows or
    raw sub-bullet lines -- rather than a presence/parsed check -- have
    something to search."""
    m = re.search(rf"^- {re.escape(label)}:.*$", body, re.M)
    if m is None:
        return ""
    rest = body[m.end() :]
    nxt = re.search(r"^(- [A-Z]|#{1,6} )", rest, re.M)
    return rest if nxt is None else rest[: nxt.start()]


# An assumption is *defined* as `A<digits>:` -- the shape every fixture and
# the template's id convention use. Keying on the definition syntax rather
# than on a list of item separators is what makes the scan independent of the
# slot's shape: inline, sub-list, paragraph, and any separator between items
# are all covered by the same rule, and a bare mention of `A1` with no colon
# is a reference, not a definition.
_ASSUMPTION_DEF = re.compile(r"(?<![A-Za-z0-9])(A\d+)[*_`]*\s*:")


_TABLE_DELIMITER = re.compile(r"^[\s|:-]+$")
MIN_TABLE_CELLS = 2
MIN_PROBE_ROW_CELLS = 3  # assumption, probe, result


def _data_row_cells(line: str) -> list[str] | None:
    """Cells of a Markdown table data row, or None when `line` is not one: a
    row is pipe-delimited on both sides with at least two cells, and the
    header delimiter row (`| --- | --- |`) carries no data."""
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    if _TABLE_DELIMITER.match(stripped):
        return None
    inner = stripped[1:-1]
    masked = list(inner)
    for start, end in _code_span_interiors(inner):
        for k in range(start, end):
            if masked[k] == "|":
                masked[k] = "\x00"
    for i, ch in enumerate(inner):  # an escaped pipe is cell content
        if ch == "|" and i and inner[i - 1] == "\\":
            masked[i] = "\x00"
    cells = ["".join(masked[a:b]).replace("\x00", "|").strip() for a, b in _cell_bounds(masked)]
    return cells if len(cells) >= MIN_TABLE_CELLS else None


def _cell_bounds(masked: list[str]) -> list[tuple[int, int]]:
    bounds, start = [], 0
    for i, ch in enumerate(masked):
        if ch == "|":
            bounds.append((start, i))
            start = i + 1
    bounds.append((start, len(masked)))
    return bounds


def _row_records_a_run(cells: list[str]) -> bool:
    """True when a probes-table row records a probe that actually ran: the
    probe and result cells are populated and neither is a no-result marker.
    An id on an empty or `not run` row names an assumption that was never
    probed, which is exactly what `identified-if` claims did not happen."""
    if len(cells) < MIN_PROBE_ROW_CELLS:
        return False
    return all(cell and not _NO_RESULT_PROBES.match(cell) for cell in cells[1:MIN_PROBE_ROW_CELLS])


def _assumption_ids(body: str) -> list[str]:
    """Assumption ids defined in the ``- Identifying assumptions:`` slot, in
    order, a repeated definition kept so the caller can report it.

    Scans the inline value on the label line together with the raw region
    below it, so every shape the slot is accepted in is covered without
    enumerating separators.
    """
    m = re.search(r"^- Identifying assumptions:(.*)$", body, re.M)
    if m is None:
        return []
    slot = m.group(1) + "\n" + _label_region(visible_markdown(body), "Identifying assumptions")
    return [d.group(1) for d in _ASSUMPTION_DEF.finditer(slot)]


def find_bullet(body: str, label: str) -> str | None:
    """The value of a ``- <label>:`` bullet, or None if the slot is empty.

    Tries three shapes, in that order, because these gates only need to
    confirm the labeled slot is *present* -- not that it takes one specific
    layout: (1) inline text on the label's own line (``- Label: value``);
    (2) an indented sublist directly below a bare ``- Label:`` line; (3) a
    prose paragraph directly below a bare ``- Label:`` line. Returns None
    only when none of the three finds anything, i.e. the slot really is
    empty (immediately followed by the next bullet, a new section, a blank
    line, or end of text).
    """
    match = _bullet_pattern(label).search(body)
    if match is None:
        return None
    inline = match.group(1).strip()
    if inline:
        return inline
    sublist = find_sublist(body, label)
    if sublist:
        return "; ".join(sublist)
    return _find_paragraph(body, label)


def _find_paragraph(body: str, label: str) -> str | None:
    """Prose paragraph directly below a bare ``- <label>:`` line, i.e. lines
    that are neither blank, nor a new ``- `` bullet, nor a new ``## `` section
    header. The caller has already ruled out an inline value and a sublist."""
    lines = body.splitlines()
    collecting = False
    collected: list[str] = []
    for line in lines:
        if not collecting:
            if line.strip() == f"- {label}:":
                collecting = True
            continue
        stripped = line.strip()
        if stripped == "" or stripped.startswith(("- ", "## ")):
            break
        collected.append(stripped)
    return " ".join(collected) if collected else None


def find_sublist(body: str, label: str) -> list[str]:
    """Indented ``- item`` lines (any leading whitespace) directly under a
    ``- <label>:`` bullet."""
    lines = body.splitlines()
    items: list[str] = []
    collecting = False
    for line in lines:
        if line.strip() == f"- {label}:":
            collecting = True
            continue
        if collecting:
            if _SUBLIST_ITEM.match(line):
                items.append(line.strip()[2:].strip())
                continue
            if line.strip() == "":
                continue
            collecting = False
    return items


def has_table_with_data_row(body: str, label: str) -> bool:
    """True if a ``- <label>:`` bullet is followed by a markdown table that
    carries at least one data row (header + separator + >=1 data row, i.e.
    >=3 pipe-delimited lines)."""
    lines = body.splitlines()
    collecting = False
    pipe_lines = 0
    for line in lines:
        if line.strip() == f"- {label}:":
            collecting = True
            continue
        if collecting:
            if _TABLE_ROW.match(line):
                pipe_lines += 1
                continue
            if line.strip() == "":
                continue
            break
    return pipe_lines >= _MIN_TABLE_LINES


def split_sections(text: str) -> list[tuple[str, str]]:
    """``(header, body)`` for each top-level ``## `` section, in document order."""
    matches = list(_SECTION_HEADER.finditer(text))
    sections: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections.append((m.group(1).strip(), text[start:end]))
    return sections


def _disposition_value(raw: str) -> str:
    """The closed-set token from a disposition/route bullet, stripping any
    trailing dash-introduced rationale (``identified-if — because ...`` or
    ``identified-if - because ...`` -> ``identified-if``) and any
    backtick-wrapping (`` `identified-if` `` -> ``identified-if``) -- a
    value's markup is not part of the value, so a backtick-wrapped token
    compares against the closed set the same as a bare one. An em-dash
    splits wherever it appears; a hyphen-dash splits only when padded by
    whitespace on both sides, so a token like ``not-constructible`` is
    never mistaken for a value plus a rationale -- the same dash
    discipline as ``_NONE_DISPOSITION`` and ``_NO_RESULT_PROBES``."""
    return re.split(r"—|\s+-\s+", raw, maxsplit=1)[0].strip().strip("`")


def _is_none_disposition(raw: str) -> bool:
    """True if a Handoff Dispositions value is the literal ``none``, tolerant
    of backtick-wrapping and a trailing rationale (``none — no Design block
    is carried``, ``none - ...``). A record's route assigning no disposition
    still substantively means "none" whether or not a rationale follows it;
    only the *reuse* semantics (below) are decided by ``assigned_dispositions``,
    not this shape check."""
    return bool(_NONE_DISPOSITION.match(raw.strip()))


def _check_forbidden(value: str, slot_name: str, findings: list[str]) -> None:
    """Forbidden-vocabulary gate, scoped to the isolated disposition VALUE token.

    Decision 004 forbids an unconditional verdict *value* (``valid``,
    ``certified`` standing in as the disposition itself), not the ordinary
    word "valid" wherever it appears in a disposition's rationale prose --
    "valid instrument" and "internal/external validity" are standard
    causal-inference vocabulary a rationale will legitimately use. So this
    checks only the already-isolated value token (the text before the first
    dash-introduced rationale, the same isolation the closed-set check uses
    via ``_disposition_value``), never the full raw bullet.
    """
    for word in FORBIDDEN_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", value, re.IGNORECASE):
            findings.append(f"forbidden vocabulary '{word}' found in {slot_name} value: {value!r}")


def _check_question(body: str | None, findings: list[str]) -> str | None:
    if body is None:
        findings.append("Question block missing")
        return None
    if find_bullet(body, "Causal question, restated as a counterfactual contrast") is None:
        findings.append("Question block: counterfactual contrast is missing or empty")
    if find_bullet(body, "Estimand") is None:
        findings.append("Question block: Estimand is missing or empty")
    if find_bullet(body, "Assignment mechanism as stated") is None:
        findings.append("Question block: Assignment mechanism as stated is missing or empty")
    route_raw = find_bullet(body, "Route")
    if route_raw is None:
        findings.append("Question block: Route is missing or empty")
        return None
    route_value = _disposition_value(route_raw)
    if route_value not in ROUTES:
        findings.append(f"Route {route_value!r} is not in the closed set {sorted(ROUTES)}")
    return route_value


def _check_design(header: str, body: str, findings: list[str]) -> str | None:
    """Check one Design block; return its disposition value when it is drawn
    from the closed set, so the Handoff reuse check knows what was assigned."""
    if find_bullet(body, "Design") is None:
        findings.append(f"Design block ({header!r}): name is missing or empty")
    # Presence only: a sublist (the canonical shape for assumptions), a table
    # (the canonical shape for probes/threats), or plain prose under the
    # label all satisfy these three gates -- find_bullet tries all three.
    # The semantic quality of what's there is out of scope either way
    # (module docstring's "Explicitly NOT this checker's claim").
    if find_bullet(body, "Identifying assumptions") is None:
        findings.append(
            f"Design block ({header!r}): at least one identifying assumption is required"
        )
    probes_table = has_table_with_data_row(body, "Assumption probes")
    probes_inline = find_bullet(body, "Assumption probes")
    if not (probes_table or probes_inline):
        findings.append(
            f"Design block ({header!r}): assumption probes table is missing or has no data row"
        )
    if find_bullet(body, "Data requirements") is None:
        findings.append(f"Design block ({header!r}): Data requirements is missing or empty")
    if not (
        has_table_with_data_row(body, "Threat register") or find_bullet(body, "Threat register")
    ):
        findings.append(
            f"Design block ({header!r}): threat register table is missing or has no data row"
        )
    disposition_raw = find_bullet(body, "Disposition")
    if disposition_raw is None:
        findings.append(f"Design block ({header!r}): Disposition is missing or empty")
        return None
    disposition_value = _disposition_value(disposition_raw)
    if disposition_value not in DISPOSITIONS:
        findings.append(
            f"Design block ({header!r}): disposition {disposition_value!r} is not in the "
            f"closed set {sorted(DISPOSITIONS)}"
        )
    _check_forbidden(disposition_value, f"Design block ({header!r}) disposition", findings)
    # identified-if is earned by probes run and reported (SKILL.md's
    # disposition semantics, the paragraph after the closed set): a block
    # assigning it over an empty or `none run` probes slot claims probe
    # support the record does not carry. A probes table with a data row
    # carries run results by shape; an inline value carries them unless it
    # is one of the no-result forms.
    if (
        disposition_value == "identified-if"
        and not probes_table
        and (probes_inline is None or _NO_RESULT_PROBES.match(probes_inline.strip()))
    ):
        findings.append(
            f"Design block ({header!r}): disposition 'identified-if' requires at "
            "least one assumption probe run with its result recorded -- the "
            "probes slot is empty or records no run result ('none', 'none run')"
        )
    _check_assessments(header, body, disposition_value, findings)
    return disposition_value if disposition_value in DISPOSITIONS else None


# Emphasis or code markup around an id is markup, not part of the id.
_ROW_ASSUMPTION_ID = re.compile(r"[*_`]*(A\d+)[*_`]*")
_SUBLIST_ASSUMPTION_ID = re.compile(r"[*_`]*A\d+[*_`]*\s*:")


def _probe_rows(body: str) -> tuple[list[str] | None, list[list[str]]]:
    """``(header_cells, data_rows)`` of the Assumption probes table, read from
    visible markdown only. The header is the row whose first cell is
    ``assumption``; a table without one has no header to key columns on."""
    rows = [
        cells
        for line in _label_region(visible_markdown(body), "Assumption probes").splitlines()
        if (cells := _data_row_cells(line))
    ]
    if rows and rows[0][0].strip().lower() == "assumption":
        return rows[0], rows[1:]
    return None, rows


def _defined_assumption_ids(where: str, body: str, findings: list[str]) -> list[str]:
    """The block's assumption ids, deduplicated, reporting an item without an
    id, an id defined twice, and a block that defines none."""
    for item in find_sublist(visible_markdown(body), "Identifying assumptions"):
        if not _SUBLIST_ASSUMPTION_ID.match(item):
            findings.append(f"{where}: assumption {item!r} carries no A<n> id")
    definitions = _assumption_ids(body)
    defined = list(dict.fromkeys(definitions))
    for aid in defined:
        if definitions.count(aid) > 1:
            findings.append(f"{where}: assumption id {aid} is defined more than once")
    if not defined:
        findings.append(f"{where}: no assumption carries an A<n> id")
    return defined


def _check_assessments(header: str, body: str, disposition: str, findings: list[str]) -> None:
    """Per-assumption assessment gates (issue #40).

    Binds every Design block but one ending ``not-constructible``, the
    exception SKILL.md's data-requirements sentence states. What is checked is
    shape and consistency: the template's four probes-table columns in order,
    ids on every assumption, one row per id, a closed-set assessment per row,
    the ``NONE``-plus-reason form of ``not-testable-here``, and the disposition
    the assessments reach. Whether an assessment is the *right* one is the
    scored arms' question, not this file's.

    The disposition must be the first SKILL.md's precedence list reaches from
    the assessments: a threat acts through the assumption it threatens, so
    nothing outside the rows can hold a design short of, or past, that value.
    """
    if disposition == "not-constructible":
        return
    where = f"Design block ({header!r})"
    header_cells, rows = _probe_rows(body)
    columns = [c.strip().lower() for c in header_cells or []]
    if columns != list(PROBE_COLUMNS):
        findings.append(
            f"{where}: the probes table's columns are {columns or 'absent'}, not "
            f"{list(PROBE_COLUMNS)} -- every named assumption owes an assessed row"
        )
        return
    col = PROBE_COLUMNS.index("assessment")
    before = len(findings)

    defined = _defined_assumption_ids(where, body, findings)

    assessed: dict[str, str] = {}
    for cells in rows:
        m = _ROW_ASSUMPTION_ID.fullmatch(cells[0].strip())
        # A row the gates cannot read is a finding, never a skip: a skipped row
        # can carry the contradiction the disposition then ignores.
        if m is None:
            findings.append(f"{where}: probe row's assumption cell {cells[0]!r} is not an A<n> id")
            continue
        if len(cells) != len(PROBE_COLUMNS):
            findings.append(
                f"{where}: probe row {m.group(1)} has {len(cells)} cells, "
                f"not the {len(PROBE_COLUMNS)} the table's columns name"
            )
            continue
        aid = m.group(1)
        if aid in assessed:
            findings.append(f"{where}: assumption {aid} has more than one probe row")
            continue
        assessed[aid] = cells[col].strip().strip("`").strip()
        if aid not in defined:
            findings.append(f"{where}: probe row {aid} names an assumption not defined above")
        _check_assessed_row(where, aid, cells, col, findings)
    for aid in defined:
        if aid not in assessed:
            findings.append(
                f"{where}: assumption {aid} has no probe row, so it carries no assessment"
            )
    if len(findings) == before:  # a disposition check over malformed rows only cascades
        _check_disposition_against(where, disposition, assessed, findings)


def _check_assessed_row(
    where: str, aid: str, cells: list[str], col: int, findings: list[str]
) -> None:
    """One probes-table row: a closed-set assessment, and the probe and
    evidence cells that assessment owes."""
    probe = cells[1].strip().strip("`").strip()
    value = cells[col].strip().strip("`").strip()
    evidence = cells[col + 1].strip()
    if value not in ASSESSMENTS:
        findings.append(
            f"{where}: assumption {aid} assessment {value!r} is not in the "
            f"closed set {sorted(ASSESSMENTS)}"
        )
    elif value == "not-testable-here":
        if probe != NO_PROBE:
            findings.append(
                f"{where}: assumption {aid} is 'not-testable-here', so its probe "
                f"cell must be {NO_PROBE}, not {probe!r}"
            )
        if not evidence:
            findings.append(
                f"{where}: assumption {aid} is 'not-testable-here' with no reason given"
            )
    else:
        if probe == NO_PROBE or not probe or _NO_RESULT_PROBES.match(probe):
            findings.append(
                f"{where}: assumption {aid} is {value!r}, which names a probe -- "
                f"{NO_PROBE} or an empty probe cell belongs to 'not-testable-here' alone"
            )
        if value in RUN_ASSESSMENTS and (not evidence or _NO_RESULT_PROBES.match(evidence)):
            findings.append(f"{where}: assumption {aid} is {value!r} with no evidence recorded")


def _check_disposition_against(
    where: str, disposition: str, assessed: dict[str, str], findings: list[str]
) -> None:
    """The recorded disposition against the one the assessments reach."""
    values = set(assessed.values())
    if "contradicted" in values:
        contradicted = sorted(a for a, v in assessed.items() if v == "contradicted")
        expected, why = (
            "assumption-contradicted",
            f"assumption(s) {contradicted} are 'contradicted'",
        )
    elif values & BLOCKING_ASSESSMENTS:
        blocking = sorted(a for a, v in assessed.items() if v in BLOCKING_ASSESSMENTS)
        expected = "unresolved"
        why = f"assumption(s) {blocking} are {sorted(values & BLOCKING_ASSESSMENTS)}"
    elif "not-contradicted" not in values:
        expected, why = "unresolved", "no assumption is 'not-contradicted' by a probe run"
    else:
        expected, why = "identified-if", "no assumption is contradicted, blocking, or unprobed"
    if disposition != expected:
        findings.append(
            f"{where}: disposition {disposition!r} does not follow from the assessments "
            f"-- {why}, so the disposition is {expected!r}"
        )


def _check_bound(body: str, findings: list[str]) -> None:
    if find_bullet(body, "Assumption ledger") is None:
        findings.append("Bound block: Assumption ledger is missing or empty")
    if find_bullet(body, "Bound logic") is None:
        findings.append("Bound block: Bound logic is missing or empty")
    if find_bullet(body, "Computed endpoints") is None:
        findings.append("Bound block: Computed endpoints is missing or empty")


def _check_handoff(
    body: str | None, assigned_dispositions: frozenset[str], findings: list[str]
) -> None:
    """Handoff structure plus disposition reuse, checked as set equality.

    The template requires the Dispositions slot to reuse the value(s)
    assigned above verbatim, or to carry the literal ``none`` for a record
    whose route assigns no disposition (the bound route carries no Design
    block, so it assigns none). Reuse binds in both directions: a closed-set
    token that appears nowhere above is a fabricated disposition, and an
    assigned disposition the slot omits is a silently dropped one -- a
    downstream reader of the Handoff alone would never learn a design ended
    that way. Either direction fails the gate (the omission direction was
    added 2026-08-09 after the final cross-model review showed the check was
    one-directional).
    """
    if body is None:
        findings.append("Handoff block missing")
        return
    if find_bullet(body, "Facts") is None:
        findings.append("Handoff block: Facts is missing or empty")
    if find_bullet(body, "Assumptions") is None:
        findings.append("Handoff block: Assumptions is missing or empty")
    dispositions_raw = find_bullet(body, "Dispositions")
    if dispositions_raw is None:
        findings.append("Handoff block: Dispositions is missing or empty")
        return
    if _is_none_disposition(dispositions_raw):
        if assigned_dispositions:
            findings.append(
                "Handoff block: Dispositions is 'none' but the record assigns "
                f"disposition(s) {sorted(assigned_dispositions)} above"
            )
        return
    mentioned = {
        value
        for value in DISPOSITIONS
        if re.search(rf"(?<![\w-]){re.escape(value)}(?![\w-])", dispositions_raw)
    }
    fabricated = mentioned - assigned_dispositions
    if fabricated:
        findings.append(
            f"Handoff block: disposition(s) {sorted(fabricated)} appear nowhere above -- "
            "Dispositions must reuse the value(s) assigned above verbatim, or be 'none' "
            "for a record whose route assigns no disposition"
        )
    omitted = assigned_dispositions - mentioned
    if omitted:
        findings.append(
            f"Handoff block: assigned disposition(s) {sorted(omitted)} are not carried -- "
            "Dispositions must mention every disposition assigned above, not a subset"
        )
    if not mentioned:
        findings.append(
            "Handoff block: Dispositions names no closed-set disposition value and is not 'none'"
        )


def _mask_endpoints_slot(text: str) -> str:
    """The record text with the Bound block's Computed endpoints slot removed:
    the ``- Computed endpoints:`` label line plus the slot's own content
    (an inline value, an indented sublist, or a prose paragraph directly
    below it), whichever shape it takes. Masking the slot's region rather
    than string-replacing its parsed value keeps the mask working when the
    parsed form (a sublist joined with ``; `` for reporting) never appears
    verbatim in the text -- otherwise the scan would flag the one place
    numeric output is licensed."""
    pattern = _bullet_pattern("Computed endpoints")
    out: list[str] = []
    masking = False
    for line in text.splitlines():
        if not masking:
            if pattern.match(line):
                masking = True
            else:
                out.append(line)
            continue
        stripped = line.strip()
        if stripped == "":
            out.append(line)
        elif stripped.startswith("## ") or (line.startswith("- ") and not line.startswith("  ")):
            masking = False
            out.append(line)
        # anything else (a sublist item, continuation prose) is slot content: masked
    return "\n".join(out)


def _scan_numeric_estimates(text: str) -> list[str]:
    """Advisory-only point-estimate heuristic, masking the licensed endpoints slot.

    See the module docstring's "Advisory-only" section for scope and the
    documented digit-only limitation.
    """
    return [
        f"possible point estimate {m.group(0)!r} outside the Bound endpoints slot"
        for m in _NUMERIC_ESTIMATE.finditer(_mask_endpoints_slot(text))
    ]


def check_record(text: str) -> tuple[list[str], list[str]]:
    """Return ``(gate_findings, advisory_warnings)`` for a record's full text.

    An empty ``gate_findings`` list means the record satisfies the schema-scope
    contract; ``advisory_warnings`` never affects pass/fail.
    """
    findings: list[str] = []
    sections = split_sections(text)

    question_body = next((body for header, body in sections if header == "Question"), None)
    design_sections = [(h, b) for h, b in sections if h == "Design" or h.startswith("Design:")]
    bound_body = next((body for header, body in sections if header == "Bound"), None)
    handoff_body = next((body for header, body in sections if header == "Handoff"), None)

    route_value = _check_question(question_body, findings)

    assigned: set[str] = set()
    for header, body in design_sections:
        disposition = _check_design(header, body, findings)
        if disposition is not None:
            assigned.add(disposition)

    if bound_body is not None:
        _check_bound(bound_body, findings)

    # Route-aware structure: review/construct records carry Design blocks and
    # no Bound block; a bound record carries the Bound block and no Design
    # blocks.
    if route_value in ("review", "construct"):
        if not design_sections:
            findings.append(f"route {route_value!r} requires at least one Design block")
        if bound_body is not None:
            findings.append(f"route {route_value!r} must not carry a Bound block")
    elif route_value == "bound":
        if bound_body is None:
            findings.append("route 'bound' requires the Bound block")
        if design_sections:
            findings.append("route 'bound' must not carry Design blocks")
    elif not design_sections and bound_body is None:
        findings.append("record has neither a Design block nor a Bound block")

    _check_handoff(handoff_body, frozenset(assigned), findings)

    warnings = _scan_numeric_estimates(text)
    return findings, warnings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("record", type=Path)
    args = ap.parse_args(argv)
    try:
        text = args.record.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"UNVERIFIABLE: cannot read record {args.record}: {exc}")
        return EXIT_UNVERIFIABLE
    findings, warnings = check_record(text)
    for finding in findings:
        print(f"GATE: {finding}")
    for warning in warnings:
        print(f"ADVISORY: {warning}")
    if findings:
        return EXIT_GATE_FAILURE
    if not warnings:
        print("PASS: schema-scope contract satisfied, no advisory findings")
    else:
        print("PASS: schema-scope contract satisfied (advisory findings above)")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
