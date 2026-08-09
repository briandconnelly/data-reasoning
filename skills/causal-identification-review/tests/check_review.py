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
Dispositions slot reusing only disposition values assigned above (or the
literal ``none`` when the record's route assigns none), and forbidden
certification vocabulary (``valid``, ``certified``) absent from disposition
slots. The
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

# A table counts as present-with-data when it carries a header row, a
# separator row, and at least one data row -- three pipe-delimited lines.
_MIN_TABLE_LINES = 3

EXIT_OK = 0
EXIT_GATE_FAILURE = 1
EXIT_UNVERIFIABLE = 2

_SECTION_HEADER = re.compile(r"^## (.+)$", re.MULTILINE)
_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$", re.MULTILINE)
_SUBLIST_ITEM = re.compile(r"^  - .+$")

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
    """Indented ``  - item`` lines directly under a ``- <label>:`` bullet."""
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
    trailing em-dash rationale (``identified-if — because ...`` -> ``identified-if``)
    and any backtick-wrapping (`` `identified-if` `` -> ``identified-if``) --
    a value's markup is not part of the value, so a backtick-wrapped token
    compares against the closed set the same as a bare one."""
    return raw.split("—", 1)[0].strip().strip("`")


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
    em-dash, the same isolation the closed-set check uses via
    ``_disposition_value``), never the full raw bullet.
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
    if not (
        has_table_with_data_row(body, "Assumption probes") or find_bullet(body, "Assumption probes")
    ):
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
    return disposition_value if disposition_value in DISPOSITIONS else None


def _check_bound(body: str, findings: list[str]) -> str | None:
    if find_bullet(body, "Assumption ledger") is None:
        findings.append("Bound block: Assumption ledger is missing or empty")
    if find_bullet(body, "Bound logic") is None:
        findings.append("Bound block: Bound logic is missing or empty")
    endpoints = find_bullet(body, "Computed endpoints")
    if endpoints is None:
        findings.append("Bound block: Computed endpoints is missing or empty")
    return endpoints


def _check_handoff(
    body: str | None, assigned_dispositions: frozenset[str], findings: list[str]
) -> None:
    """Handoff structure plus disposition reuse.

    The template requires the Dispositions slot to reuse the value(s)
    assigned above verbatim, or to carry the literal ``none`` for a record
    whose route assigns no disposition (the bound route carries no Design
    block, so it assigns none). A closed-set token that appears nowhere
    above is a fabricated disposition, not a reuse, and fails the gate.
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
    if not mentioned:
        findings.append(
            "Handoff block: Dispositions names no closed-set disposition value and is not 'none'"
        )


def _scan_numeric_estimates(text: str, endpoints_value: str | None) -> list[str]:
    """Advisory-only point-estimate heuristic, masking the licensed endpoints slot.

    See the module docstring's "Advisory-only" section for scope and the
    documented digit-only limitation.
    """
    masked = text.replace(endpoints_value, "") if endpoints_value else text
    return [
        f"possible point estimate {m.group(0)!r} outside the Bound endpoints slot"
        for m in _NUMERIC_ESTIMATE.finditer(masked)
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

    endpoints_value: str | None = None
    if bound_body is not None:
        endpoints_value = _check_bound(bound_body, findings)

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

    warnings = _scan_numeric_estimates(text, endpoints_value)
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
