#!/usr/bin/env python3
# instruments/check_record.py
"""Fixture-neutral structural validator for data-reasoning records.

Scope and limits are owned by
skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md;
this file enacts that scope and does not restate it. Operationally: it checks
required sections, closed vocabularies, and the presence and non-emptiness of
each record kind's required slots; it suspends completeness findings while a
record still carries template placeholders or `pending` slots (the skills
mandate writing the template before filling it).

`--final` is the completed-record mode: nothing suspends completeness, and a
slot still holding a placeholder, `...`, or `pending` is a finding. The hook
runs the default mode on every write because a write is not a delivery; a
caller that knows the record is done runs `--final`.

Exit codes: 0 clean, 1 findings (one per stdout line), 2 not a recognized
record, unreadable, or bad usage.
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

# Issue #76: a profile-route exploration log may carry an improvised title,
# `# Entity profile: ...` or `# Exploration (<qualifier>): ...`. This is a
# second, narrowly scoped rule beside the exact-prefix table above, and it
# maps only to the exploration kind. hooks/check_record_hook.py and both
# matchers in hooks/check_record_hook.sh mirror it; the hook suite holds the
# four in agreement.
EXPLORATION_TITLE = re.compile(r"# (Entity profile|Exploration)( \([^)]*\))?: ")

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

# `- Label:` bullet slots a completed record of each kind must carry, keyed by
# the section that owns them. Labels are the shipped templates' own; the unit
# suite keeps them byte-identical to the templates so a renamed slot fails
# there rather than silently orphaning a check. Only inline-valued slots are
# listed: a label that heads a nested list (Consequences, Evidence,
# Identifying assumptions) has no value on its own line to check.
REQUIRED_SLOTS = {
    "ledger": {
        "## Problem": [
            "Decision informed",
            "Falsifiable question",
            "Success criteria",
            "Stop condition",
            "Effort budget",
        ],
        "## Data Validity": [
            "Collection method",
            "Coverage matrix",
            "Coverage baseline",
            "Source completeness semantics",
        ],
        "## Conclusion": ["Answer", "Best supported", "Limitations"],
    },
    "exploration": {
        "## Frame": ["Scope", "Effort budget", "Stop rule"],
        "## Orientation record": ["Schema and grain", "Quality", "Coverage", "Absence semantics"],
    },
    "review": {
        "## Question": [
            "Causal question, restated as a counterfactual contrast",
            "Estimand",
            "Assignment mechanism as stated",
            "Route",
        ],
        "## Handoff": ["Facts", "Assumptions", "Dispositions"],
    },
    "decision": {
        "## Decision frame": [
            "Route",
            "Actions",
            "Decision owner",
            "Reversibility",
            "Deadline or forcing event",
            "Favored if true",
            "Loss ratio",
            "Decision threshold (posterior odds)",
        ],
        "## Decision-state model": [
            "Proposition",
            "Residual reading",
            "Claim class",
            "Identification basis",
            "Identification conditions",
            "Ledger mapping",
        ],
        "## Evidence and update": ["Prior odds", "Independence", "Posterior odds"],
        "## Robustness": ["Prior class swept", "Loss range swept", "Crossover"],
        "## Verdict": ["Verdict", "Recommended action", "Conditions"],
        "## Handoff": ["Open factual disputes", "Identification gaps", "VoI question"],
    },
    "voi": {
        "## VoI": [
            "Route",
            "Pending decision",
            "Signal model",
            "Value basis",
            "Value calculation",
            "Upper bound",
            "Cost",
            "Verdict",
        ],
    },
}

STATUSES = {"REFUTED", "UNRESOLVED"}
OUTCOMES = {"NOT_TESTED", "CONSISTENT", "CONTRADICTED", "NON_DISCRIMINATING"}
DISPOSITIONS = {"identified-if", "assumption-contradicted", "unresolved", "not-constructible"}
ROUTES = {"review", "construct", "bound"}
ASSESSMENTS = {
    "contradicted",
    "not-contradicted",
    "non-discriminating",
    "not-run",
    "not-testable-here",
}
DECIDE_VERDICTS = {
    "robust",
    "prior-sensitive",
    "loss-sensitive",
    "evidence-sensitive",
    "dominated",
    "indifferent",
    "resolved",
}
# A resolved record (decision-analysis decisions/008) takes its own sections
# and slots: no odds-only field, and a Resolution section in this order.
RESOLVED_SECTIONS = [
    "## Decision frame",
    "## Decision-state model",
    "## Resolution",
    "## Verdict",
    "## Handoff",
]
RESOLVED_SLOTS = {
    "## Decision frame": REQUIRED_SLOTS["decision"]["## Decision frame"][:5],
    "## Decision-state model": REQUIRED_SLOTS["decision"]["## Decision-state model"],
    "## Resolution": [
        "Excluded state",
        "Surviving state",
        "Accepted evidence",
        "Structural exclusion",
        "Exclusion assumptions",
        "Surviving-state possibility",
        "Surviving-state loss difference",
    ],
    "## Verdict": REQUIRED_SLOTS["decision"]["## Verdict"],
    "## Handoff": REQUIRED_SLOTS["decision"]["## Handoff"],
}
RESOLUTION_ORDER = [
    "Excluded state",
    "Surviving state",
    "Observations",
    "Accepted evidence",
    "Structural exclusion",
    "Exclusion assumptions",
    "Surviving-state possibility",
    "Surviving-state losses",
    "Surviving-state loss difference",
]
ODDS_ONLY_SECTIONS = ["## Evidence and update", "## Robustness"]
# Every odds-only slot label, rejected anywhere in a visible resolved record.
ODDS_ONLY_LABELS = [
    "Favored if true",
    "Loss ratio",
    "Decision threshold (posterior odds)",
    "Prior odds",
    "Evidence",
    "Independence",
    "Posterior odds",
    "Prior class swept",
    "Loss range swept",
    "Crossover",
]
# The nested tables each decision skeleton carries, beside its inline slots.
DECISION_NESTED_TABLES = [
    ("## Decision frame", "Consequences"),
    ("## Evidence and update", "Evidence"),
]
RESOLVED_NESTED_TABLES = [
    ("## Decision frame", "Consequences"),
    ("## Resolution", "Observations"),
    ("## Resolution", "Surviving-state losses"),
]
# A `- Verdict:` line, with or without emphasis on the label, and its value.
VERDICT_LINE = re.compile(r"^\s*- (?:(\*\*|__|\*|_)Verdict(?::\1|\1:)|Verdict:)(.*)$")
READS_RESOLVED = re.compile(r"^[`*_\s]*resolved(?![\w-])")
RESOLVED_STATES = {"proposition true", "proposition false"}
RESOLVED_PROSE = [
    "Accepted evidence",
    "Structural exclusion",
    "Exclusion assumptions",
    "Surviving-state possibility",
]
RESOLVED_RECOMMENDATIONS = {"no preference", "returned to owner"}
VOI_VERDICTS = {"worth-it", "not-worth-it", "sensitive", "break-even-only", "upper-bound-only"}
VOI_VALUE_BASES = {"signal-model", "upper-bound"}

# The decision skill's provenance classes (SKILL.md § Numeric Policy), and
# the two that count as belief-grade for losses: a `robust` verdict needs
# losses someone actually stated, because robustness across priors says
# nothing when a hypothetical loss ratio reverses the decision.
PROVENANCE = {
    "user-elicited",
    "externally-sourced",
    "estimated-from-data-in-hand",
    "sensitivity-only",
}
LOSS_PROVENANCE_FOR_ROBUST = {"user-elicited", "externally-sourced"}
# The no-supported-prior form (decision-analysis SKILL.md § Numeric Policy;
# spellings in the template's § Slot notes).
NO_PRIOR_SENTINEL = "none supported — see Robustness"
NO_LR_SENTINEL = "none supported"
PROVENANCE_MENTION = re.compile(r"provenance:\s*`?([A-Za-z][A-Za-z-]*)`?")
# Shared slots for the statewise verdicts in Numeric Policy.
STATEWISE_NONE_NEEDED = (
    ("## Decision frame", "Favored if true"),
    ("## Evidence and update", "Prior odds"),
    ("## Evidence and update", "Posterior odds"),
    ("## Robustness", "Prior class swept"),
    ("## Robustness", "Crossover"),
)

# A template placeholder is `<` + a letter + text without `<`, `>`, `=` + `>`.
# Inequalities (`< 1.5`, `<5%`) start with a space or digit; HTML attributes
# carry `=`; bare HTML tags are excluded by name below, and a Markdown
# autolink (`<https://...>`, `<name@example.com>`, `<mailto:...>`) is real
# record content, not a template blank, so it is excluded too. Residual:
# `<q and r>` with a letter-initial inequality still reads as a placeholder.
PLACEHOLDER = re.compile(r"<([A-Za-z][^<>\n=]*)>")
# A CommonMark URI autolink is a scheme (RFC 3986: a letter, then letters,
# digits, `+`, `.` or `-`) followed by `:` -- `tel:`, `urn:` and `news:` as
# much as `https:`. Matching the scheme grammar rather than a list of schemes
# keeps a real autolink from reading as a template blank.
AUTOLINK_SCHEME = re.compile(r"[A-Za-z][A-Za-z0-9+.\-]*:")
# The WHATWG element index as of 2026-08. HTML is a living vocabulary, so
# this set is maintained, not complete for all time: a tag outside it reads
# as a template placeholder, and one placeholder marks the whole record in
# progress, so an omission here suppresses every completeness finding.
HTML_TAGS = frozenset(
    {
        "a",
        "abbr",
        "address",
        "area",
        "article",
        "aside",
        "audio",
        "b",
        "base",
        "bdi",
        "bdo",
        "blockquote",
        "body",
        "br",
        "button",
        "canvas",
        "caption",
        "cite",
        "code",
        "col",
        "colgroup",
        "data",
        "datalist",
        "dd",
        "del",
        "details",
        "dfn",
        "dialog",
        "div",
        "dl",
        "dt",
        "em",
        "embed",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "head",
        "header",
        "hgroup",
        "hr",
        "html",
        "i",
        "iframe",
        "img",
        "input",
        "ins",
        "kbd",
        "label",
        "legend",
        "li",
        "link",
        "main",
        "map",
        "mark",
        "menu",
        "meta",
        "meter",
        "nav",
        "noscript",
        "object",
        "ol",
        "optgroup",
        "option",
        "output",
        "p",
        "picture",
        "pre",
        "progress",
        "q",
        "rp",
        "rt",
        "ruby",
        "s",
        "samp",
        "script",
        "search",
        "section",
        "select",
        "selectedcontent",
        "slot",
        "small",
        "source",
        "span",
        "strong",
        "style",
        "sub",
        "summary",
        "sup",
        "table",
        "tbody",
        "td",
        "template",
        "textarea",
        "tfoot",
        "th",
        "thead",
        "time",
        "title",
        "tr",
        "track",
        "u",
        "ul",
        "var",
        "video",
        "wbr",
    }
)


def _has_placeholder(value: str) -> bool:
    for m in PLACEHOLDER.finditer(value):
        inner = m.group(1).strip().rstrip("/").strip().lower()
        # a boolean attribute carries no `=` ("<details open>"), so compare
        # the tag name rather than the whole span
        if inner.split(" ", 1)[0] in HTML_TAGS:
            continue
        if AUTOLINK_SCHEME.match(inner) or "@" in inner:
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

DELIMITERS = (" —", " -", ";", ":", " (")
MIN_TABLE_ROWS = 2  # header + at least one data row

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
CELL_SPLIT = re.compile(r"(?<!\\)\|")
INLINE_COMMENT = re.compile(r"<!--.*?-->")
ESCAPED_LT = re.compile(r"(?<!\\)((?:\\\\)*)\\<")


def _opens_fence(line: str, m) -> bool:
    """A fence opener's info string may not contain a backtick when the fence
    is made of backticks (CommonMark): such a line is ordinary text."""
    return not (m.group(1)[0] == "`" and "`" in line[m.end() :])


def _strip_hidden(text: str) -> tuple[str, bool, bool, int | None]:
    """Blank out what a reader never sees — fenced code blocks and HTML
    comments — in one pass, so the two cannot hide each other's delimiters.
    Line count is preserved. Per CommonMark: a fence closes only on a same-
    character run at least as long as the opener with nothing but whitespace
    after it; `<!--` inside a fence is code; a comment never closed runs to
    the end of the document. Returns (body, fence_still_open_at_eof,
    comment_still_open_at_eof, index of the line where that unfinished block
    opened, or None)."""
    out: list[str] = []
    fence: tuple[str, int] | None = None
    in_comment = False
    opened_at: int | None = None
    for i, line in enumerate(text.split("\n")):
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
            close = line.find("-->")
            if close == -1:
                out.append("")
                continue
            # The rest of the closing line is ordinary text and may open
            # another comment.
            visible, opened = _strip_comment(line[close + 3 :])
            in_comment = opened
            if opened:
                opened_at = i
            out.append(visible.rstrip())
            continue
        m = FENCE.match(line)
        if m and _opens_fence(line, m):
            fence = (m.group(1)[0], len(m.group(1)))
            opened_at = i
            out.append("")
            continue
        visible, opened = _strip_comment(line)
        if opened:
            in_comment = True
            opened_at = i
        out.append(visible.rstrip())
    still_open = fence is not None or in_comment
    return "\n".join(out), fence is not None, in_comment, opened_at if still_open else None


# The colon must be present, either inside the emphasis ("**Verdict:**") or
# immediately after it ("**Verdict**:"). Without it the line has no label
# delimiter and is not a slot.
LABEL_EMPHASIS = re.compile(r"^- (\*\*|__|\*|_)([^*_:\n]+?)(?::\1|\1:)\s*")


def _unemphasize(line: str) -> str:
    """'- **Verdict:** x', '- **Verdict**: x', '- *Verdict*: x' -> '- Verdict: x'.
    Emphasis on a slot label is presentation, not a different slot."""
    return LABEL_EMPHASIS.sub(lambda m: f"- {m.group(2)}: ", line, count=1)


BACKTICK_RUN = re.compile(r"`+")


def _code_span_interiors(line: str) -> list[tuple[int, int]]:
    """(start, end) of every inline code-span interior. Per CommonMark a span
    closes on a backtick run of exactly the opener's length, and a
    backslash-escaped backtick outside a span is literal text that opens
    nothing."""
    runs = [(m.start(), m.end()) for m in BACKTICK_RUN.finditer(line)]
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


def _blank_code_spans(line: str, fill: str) -> str:
    """`line` with code-span interiors replaced by `fill`, index-for-index."""
    out = list(line)
    for start, end in _code_span_interiors(line):
        for k in range(start, end):
            if fill != "\x00" or out[k] == "|":
                out[k] = fill
    return "".join(out)


def _mask_code_pipes(line: str) -> str:
    """Hide `|` inside inline code spans from the cell splitter; `_unmask`
    restores it inside the cell."""
    return _blank_code_spans(line, "\x00")


def _strip_comment(line: str) -> tuple[str, bool]:
    """Drop HTML comments a reader never sees, ignoring `<!--` and `-->` that
    Markdown renders as code. Returns (visible, comment_left_open)."""
    # `<` after an odd run of backslashes is escaped literal text, not a
    # comment opener; an even run escapes only the backslashes themselves.
    masked = ESCAPED_LT.sub(lambda m: m.group(1) + "\x01\x01", _blank_code_spans(line, "\x01"))
    for m in reversed(list(INLINE_COMMENT.finditer(masked))):
        line = line[: m.start()] + line[m.end() :]
        masked = masked[: m.start()] + masked[m.end() :]
    opener = masked.find("<!--")
    if opener != -1:
        return line[:opener], True
    return line, False


def _unmask(cell: str) -> str:
    return cell.replace("\x00", "|")


_FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)


def strip_frontmatter(text: str) -> str:
    """Drop a leading YAML frontmatter block. Frontmatter is metadata a host
    added; the record starts after it. An unterminated block is left alone."""
    return _FRONTMATTER.sub("", text, count=1)


def detect(text: str) -> str | None:
    """Kind of record, or None. A title signature alone is not enough: a
    user's own note titled `# Investigation: …` is not a ledger. The record
    must also carry at least one of its kind's required headings, visible to
    a reader: one quoted inside a closed fence or closed HTML comment does
    not count. An unterminated fence or comment blanks everything after it,
    so when either is open at EOF and nothing visible corroborates, the raw
    text from where that block opened is searched instead: a malformed real
    record stays recognized and check() reports what it could not see (fail
    closed). A heading must have heading syntax in the raw line too, so
    removing an inline comment cannot manufacture one."""
    text = strip_frontmatter(text)
    kind = title_kind(text.lstrip().split("\n", 1)[0])
    if kind is None:
        return None

    required = REQUIRED_SECTIONS[kind]
    raw = text.split("\n")
    visible, _, _, opened_at = _strip_hidden(text)
    for shown, line in zip(visible.split("\n"), raw, strict=True):
        h = shown.rstrip()
        if h in required and line.startswith(h.split(" ", 1)[0] + " "):
            return kind
    if opened_at is not None and any(line.rstrip() in required for line in raw[opened_at:]):
        return kind
    return None


def title_kind(title: str) -> str | None:
    """Kind a document title line signals, or None. The title alone does not
    make a record; `detect` also requires a required heading."""
    for prefix, kind in SIGNATURES.items():
        if title.startswith(prefix):
            return kind
    if EXPLORATION_TITLE.match(title):
        return "exploration"
    return None


def _is_placeholder(value: str) -> bool:
    v = value.strip()
    return not v or v == "..." or _has_placeholder(v)


def _normalize(value: str) -> str:
    """Strip surrounding emphasis/code markers, which are presentation only."""
    return value.strip().strip("`*").strip()


# SKILL.md § Profile Route fills "Frame-lite", not Frame: a profile record's
# frame heading is `## Frame` or `## Frame-lite`, optionally annotated, and
# Frame-lite owes no Stop rule because its budget doubles as the stop rule.
FRAME_HEADING = re.compile(r"^## Frame(-lite)?(?=$|\s)", re.M)
FRAME_LITE_SLOTS = ["Scope", "Effort budget"]


def _frame_heading(body: str) -> str:
    """The exploration record's actual frame heading line, or `## Frame`
    when none is present (so the missing-section finding names the
    canonical one)."""
    m = FRAME_HEADING.search(body)
    if m is None:
        return "## Frame"
    return body[m.start() : body.find("\n", m.start())].rstrip()


def _verdict_lines(body: str) -> list[re.Match]:
    return [m for ln in body.splitlines() if (m := VERDICT_LINE.match(ln))]


def _resolved(body: str, kind: str) -> bool:
    """Any visible `- Verdict:` line reading `resolved`, however written,
    makes the record a resolved one (decision-analysis decisions/008)."""
    return kind == "decision" and any(
        READS_RESOLVED.match(m.group(2)) for m in _verdict_lines(body)
    )


def _required_sections(body: str, kind: str) -> list[str]:
    if _resolved(body, kind):
        return RESOLVED_SECTIONS
    headings = REQUIRED_SECTIONS[kind]
    if kind != "exploration":
        return headings
    return [_frame_heading(body) if h == "## Frame" else h for h in headings]


def _required_slots(body: str, kind: str) -> dict[str, list[str]]:
    if _resolved(body, kind):
        return RESOLVED_SLOTS
    slots = REQUIRED_SLOTS.get(kind, {})
    if kind != "exploration":
        return slots
    frame = _frame_heading(body)
    lite = frame.startswith("## Frame-lite")
    out = {}
    for heading, labels in slots.items():
        if heading == "## Frame":
            out[frame] = FRAME_LITE_SLOTS if lite else labels
        else:
            out[heading] = labels
    return out


HEADER_ALIASES = {
    # The shipped ledger template's header for the column the checks call
    # `necessary prediction` (references/ledger-template.md § Hypotheses).
    "necessary prediction (failure refutes)": "necessary prediction",
}


def _header_key(h: str) -> str:
    """A header's identity: lower-cased, whitespace collapsed, then mapped
    through the alias table. Identity, not containment: `unnecessary
    prediction` is not `necessary prediction`, and `outcome (rationale)` is
    not `outcome`."""
    key = " ".join(_normalize(h).lower().split())
    return HEADER_ALIASES.get(key, key)


def _leading_token(value: str, allowed: set[str]) -> str | None:
    """The value must BE an allowed token, or start with one followed by a
    delimiter (annotations after the token are legitimate). A comma is not a
    delimiter because it reads as a list, which would falsely accept
    comma-separated token values."""
    v = _normalize(value)
    for tok in sorted(allowed, key=len, reverse=True):
        if v == tok:
            return tok
        if v.startswith(tok) and v[len(tok) :].startswith(DELIMITERS):
            return tok
    return None


LIST_SEPARATOR = re.compile(r"\s*(?:,|;|\band\b)\s*")
PARENTHETICAL = re.compile(r"\([^()]*\)")


def _mentions_only(value: str, allowed: set[str]) -> bool:
    """True when `value` is a list -- comma, semicolon, or `and` separated --
    whose every item begins with an allowed token (annotations after a token
    are legitimate, as in `_leading_token`). A separator inside a
    parenthetical annotation does not split the list. An empty list is not a
    list."""
    v = _normalize(value)
    # Mask parentheticals so their commas are not separators, keeping offsets.
    masked = PARENTHETICAL.sub(lambda m: "(" + "x" * (len(m.group()) - 2) + ")", v)
    items, start = [], 0
    for m in LIST_SEPARATOR.finditer(masked):
        items.append(v[start : m.start()])
        start = m.end()
    items.append(v[start:])
    items = [i for i in items if i.strip()]
    return bool(items) and all(_leading_token(i, allowed) is not None for i in items)


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
    """Values of the column whose header is `name`; [] if absent."""
    if not rows:
        return []
    keys = [_header_key(h) for h in rows[0]]
    idx = next((i for i, k in enumerate(keys) if k == name.lower()), None)
    if idx is None:
        return []
    return [r[idx] for r in rows[1:] if idx < len(r)]


def _require_column(rows: list[list[str]], name: str, where: str, findings: list[str]) -> bool:
    """True if `rows`' header has a column named `name`; else records a
    finding and returns False. An empty table is left to the dedicated
    empty-table finding, not duplicated here."""
    if not rows:
        return False
    if not any(_header_key(h) == name.lower() for h in rows[0]):
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
        stripped = _unemphasize(line.strip())
        if stripped.startswith("- ") and ":" in stripped:
            yield stripped.split(":", 1)[1]


def _slot_value(section: str, label: str) -> str | None:
    """The value of the first `- label:` bullet in `section`, or None when
    no such bullet exists. Emphasis around the label is ignored; the label
    itself must match the template's byte for byte. A value may continue on
    the following lines -- a wrapped prose paragraph (the VoI record's prose
    slots) or an indented sub-list (a coverage matrix written as one bullet
    per cell) -- so those are read when the label's own line is empty.

    Only an *unindented* bullet, heading, or table ends the value, the same
    extent rule `_nested_span` uses: a nested bullet belongs to its parent
    slot, and reading it as the next sibling reported filled slots empty."""
    lines = section.splitlines()
    for i, line in enumerate(lines):
        stripped = _unemphasize(line.strip())
        if not stripped.startswith("- " + label + ":"):
            continue
        value = stripped[len(label) + 3 :].strip()
        if value:
            return value
        continuation: list[str] = []
        for nxt in lines[i + 1 :]:
            t = nxt.strip()
            if not t:
                if continuation:
                    break
                continue
            indented = nxt[:1].isspace()
            if not indented and t.startswith(("- ", "#", "|")):
                break
            continuation.append(t)
        return " ".join(continuation)
    return None


def _unfilled(value: str) -> bool:
    """A slot or cell still carrying template state: empty, `...`, a
    placeholder, or a bare `pending` marker -- read through any emphasis or
    code markers around it, which are presentation only."""
    v = _normalize(value)
    return not v or v == "..." or _has_placeholder(v) or bool(PENDING.match(v))


def _check_labels(section: str, heading: str, labels, final: bool, findings: list[str]) -> None:
    """Missing / empty / (final mode) still-unfilled findings for each
    `- label:` bullet in `section`, reported under `heading`."""
    for label in labels:
        value = _slot_value(section, label)
        if value is None:
            findings.append(f"{heading}: required '- {label}:' slot is missing")
        elif not value:
            findings.append(f"{heading}: required slot '{label}' is empty")
        elif final and _unfilled(value):
            findings.append(f"{heading}: required slot '{label}' is still unfilled: {value!r}")


def _check_slots(body: str, kind: str, final: bool, findings: list[str]) -> None:
    for heading, labels in _required_slots(body, kind).items():
        section = _section(body, heading)
        if not section.strip():
            continue  # the missing/empty-section finding already covers it
        _check_labels(section, heading, labels, final, findings)


def _nested_span(section: str, label: str) -> str | None:
    """The lines nested under the `- label:` bullet in `section` -- up to the
    next top-level bullet or the section's end -- or None when the bullet is
    absent."""
    lines = section.splitlines()
    start = next(
        (
            i
            for i, ln in enumerate(lines)
            if _unemphasize(ln.strip()).startswith("- " + label + ":")
        ),
        None,
    )
    if start is None:
        return None
    span: list[str] = []
    for ln in lines[start + 1 :]:
        if ln.startswith("- "):
            break
        span.append(ln)
    return "\n".join(span)


# Header columns each nested table must carry, from the shipped templates.
# Consequences has a blank corner cell and per-state columns named by the
# record, so only its width is fixed.
NESTED_TABLE_COLUMNS = {
    "Consequences": [],
    "Evidence": ["item", "lr", "provenance", "source, reference class, conditioning"],
    "Assumption probes": ["assumption", "probe", "assessment", "evidence or reason"],
    "Threat register": ["threat", "probe", "result"],
    "Observations": ["observation", "source"],
    "Surviving-state losses": ["action", "loss", "provenance"],
}
NESTED_TABLE_MIN_WIDTH = {"Consequences": 3}


def _check_nested_table(
    section: str, heading: str, label: str, final: bool, findings: list[str]
) -> None:
    """A `- label:` bullet with a table under it carrying the template's
    columns and at least one data row as wide as its header; in final mode
    every cell of that table must be filled."""
    span = _nested_span(section, label)
    if span is None:
        findings.append(f"{heading}: required '- {label}:' slot is missing")
        return
    table = _table_rows(span)
    if not table:
        findings.append(f"{heading}: '- {label}:' has no table under it")
        return
    header, rows = table[0], table[1:]
    keys = [_header_key(h) for h in header]
    for col in NESTED_TABLE_COLUMNS.get(label, []):
        if col not in keys:
            findings.append(f"{heading}: '- {label}:' table lacks a {col!r} column")
    width = max(len(header), NESTED_TABLE_MIN_WIDTH.get(label, 0))
    if not rows:
        findings.append(f"{heading}: '- {label}:' has no table rows under it")
        return
    for i, row in enumerate(rows, 1):
        if len(row) < width:
            findings.append(
                f"{heading}: '- {label}:' row {i} has {len(row)} cells, header has {width}"
            )
        if final:
            for cell in row:
                if _unfilled(cell):
                    findings.append(
                        f"{heading}: '- {label}:' row {i} cell still unfilled: {cell!r}"
                    )


def _check_nested_list(
    section: str, heading: str, label: str, final: bool, findings: list[str]
) -> None:
    """A `- label:` bullet with at least one indented sub-bullet under it."""
    span = _nested_span(section, label)
    if span is None:
        findings.append(f"{heading}: required '- {label}:' slot is missing")
        return
    items = [ln.strip()[2:] for ln in span.splitlines() if ln.strip().startswith("- ")]
    if not items:
        findings.append(f"{heading}: '- {label}:' has no items under it")
        return
    if final:
        for item in items:
            if _unfilled(item):
                findings.append(f"{heading}: '- {label}:' item still unfilled: {item!r}")


def _toplevel_table(section: str) -> list[list[str]]:
    """The section's own table rows -- the unindented ones. A table nested
    under a `- Label:` bullet belongs to that slot and is checked by
    `_check_nested_table`; reading it here would double-report it."""
    return _table_rows("\n".join(ln for ln in section.splitlines() if not ln[:1].isspace()))


def _section_unfilled(content: str) -> bool:
    """A required section whose whole content is still template state: the
    canonical `(pending -- ...)` marker, a bare `pending`, or an ellipsis.
    Placeholder syntax *inside* an otherwise written section is left to the
    cell and slot checks, which can say which cell is at fault."""
    v = _normalize(content)
    return bool(SECTION_PENDING.match(content) or PENDING.match(v) or v == "...")


def _check_table_cells(body: str, kind: str, final: bool, findings: list[str]) -> None:
    """Each required section's own table: every data row as wide as its
    header, and -- in final mode -- every cell filled.

    The width check runs in both modes because a short row is a structural
    defect, not an unfinished one: `_column` skips the cells a short row is
    missing, so an unchecked narrow row is exactly how an empty Method or
    Outcome reaches a clean result. Fill state stays final-mode only, since a
    write is not a delivery (decision 006).

    Exception: a Tests row whose outcome is NOT_TESTED may carry `pending`
    evidence. That is the row's honest state, not template residue."""
    for heading in _required_sections(body, kind) if kind in REQUIRED_SECTIONS else []:
        rows = _toplevel_table(_section(body, heading))
        if len(rows) < MIN_TABLE_ROWS:
            continue  # no table here, or the empty-table finding covers it
        header, data = rows[0], rows[1:]
        keys = [_header_key(h) for h in header]
        outcome_idx = next((i for i, k in enumerate(keys) if k == "outcome"), None)
        for n, row in enumerate(data, 1):
            if len(row) < len(header):
                findings.append(
                    f"{heading} row {n}: has {len(row)} cells, header has {len(header)}"
                )
            if not final:
                continue
            not_tested = (
                outcome_idx is not None
                and outcome_idx < len(row)
                and _leading_token(row[outcome_idx], OUTCOMES) == "NOT_TESTED"
            )
            for idx, cell in enumerate(row):
                if not _unfilled(cell):
                    continue
                col = keys[idx] if idx < len(keys) else f"column {idx + 1}"
                if not_tested and col == "evidence":
                    continue
                findings.append(f"{heading} row {n}: {col!r} cell still unfilled: {cell!r}")


def _check_nested_tables(body: str, kind: str, final: bool, findings: list[str]) -> None:
    """Completed decision records carry a Consequences table and an Evidence
    table; a `- Label:` line with nothing under it is the omission finding 2
    of the 2026-09-15 review reproduced."""
    if kind != "decision":
        return
    tables = (
        (
            ("## Decision frame", "Consequences"),
            ("## Resolution", "Observations"),
            ("## Resolution", "Surviving-state losses"),
        )
        if _resolved(body, kind)
        else (("## Decision frame", "Consequences"), ("## Evidence and update", "Evidence"))
    )
    for heading, label in tables:
        section = _section(body, heading)
        if section.strip():
            _check_nested_table(section, heading, label, final, findings)


DESIGN_SLOTS = ["Design", "Data requirements", "Disposition"]
BOUND_SLOTS = ["Assumption ledger", "Bound logic", "Computed endpoints"]


def _check_review_route_blocks(body: str, final: bool, findings: list[str]) -> None:
    """A review or construct record owes at least one Design block carrying
    the template's slots, assumption list, and probe and threat tables; a
    bound record owes the Bound block and its slots. The route's own value is
    checked elsewhere; here an unrecognized route owes nothing extra."""
    route = _slot_value(_section(body, "## Question"), "Route")
    token = _leading_token(route, ROUTES) if route else None
    if token in ("review", "construct"):
        designs = [h.rstrip() for h in re.findall(r"^## Design: .*$", body, re.M)]
        if not designs:
            findings.append(f"route {token!r}: no '## Design: <name>' block")
        for h in designs:
            section = _section(body, h)
            _check_labels(section, h, DESIGN_SLOTS, final, findings)
            _check_nested_list(section, h, "Identifying assumptions", final, findings)
            disposition = _slot_value(section, "Disposition") or ""
            # SKILL.md per-route procedure: a design that cannot run has
            # nothing to probe, so its assumptions owe no assessed rows.
            if _leading_token(disposition, DISPOSITIONS) != "not-constructible":
                _check_nested_table(section, h, "Assumption probes", final, findings)
            _check_nested_table(section, h, "Threat register", final, findings)
    elif token == "bound":
        bound = _section(body, "## Bound")
        if not bound.strip():
            findings.append("route 'bound': required section missing: ## Bound")
        else:
            _check_labels(bound, "## Bound", BOUND_SLOTS, final, findings)


def _check_assessments(section: str, heading: str, findings: list[str]) -> None:
    """Every assessment cell of a Design block's probes table begins with a
    value from the closed set (SKILL.md per-route procedure); a cell still
    in template state is left to the table's own fill check."""
    span = _nested_span(section, "Assumption probes")
    if span is None:
        return
    for value in _column(_table_rows(span), "assessment"):
        if _unfilled(value):
            continue
        if _leading_token(value, ASSESSMENTS) is None:
            findings.append(
                f"{heading}: assessment {_normalize(value)!r} does not begin with a value "
                f"from the closed set {sorted(ASSESSMENTS)} — 'valid' and 'certified' are "
                f"not assessments"
            )


def _in_progress(body: str, kind: str | None = None) -> bool:
    """`body` is already stripped; pass the record's `kind` when known so it
    is not re-detected from stripped text."""
    if any(v.strip() == "..." or _has_placeholder(v) for v in _slot_values(body)):
        return True
    # A slot value, or a required section's whole content, that says it is
    # pending is the sanctioned plan-stage state. Prose that merely begins
    # with the word is not.
    if any(PENDING.match(v.strip()) for v in _bullet_slot_values(body)):
        return True
    kind = kind or detect(body) or ""
    return any(
        SECTION_PENDING.match(_section(body, h).strip())
        for h in (_required_sections(body, kind) if kind else [])
    )


def _unfilled_cell(value: str, where: str, final: bool, findings: list[str]) -> bool:
    """True when `value` is template state the vocabulary check must skip; in
    final mode that state is itself a finding."""
    if final and _unfilled(value):
        findings.append(f"{where}: cell still unfilled: {value!r}")
        return True
    return _is_placeholder(value)


def _check_claim(value: str, where: str, findings: list[str], final: bool = False) -> None:
    if _unfilled_cell(value, where, final, findings):
        return
    v = _normalize(value)
    if v in ("causal", "data-artifact") or re.fullmatch(r"descriptive( \(estimand: .+\))?", v):
        return
    findings.append(
        f"{where}: claim class {v!r} is not in the closed set "
        f"causal / descriptive (estimand: ...) / data-artifact"
    )


def _check_provenance_vocab(body: str, findings: list[str]) -> None:
    """Every `provenance:` mention on a decide slot, and every provenance
    cell of the Evidence table, names a class from the closed set; and
    `sensitivity-only` never appears in Evidence and update."""
    for heading in ("## Decision frame", "## Evidence and update", "## Robustness"):
        section = _section(body, heading)
        for line in section.splitlines():
            if not line.strip().startswith(("- ", "|")):
                continue
            for cls in PROVENANCE_MENTION.findall(_unemphasize(line.strip())):
                if cls not in PROVENANCE:
                    findings.append(
                        f"{heading}: provenance {cls!r} is not in the closed set "
                        f"{sorted(PROVENANCE)}"
                    )
    evidence = _section(body, "## Evidence and update")
    _check_no_prior_form(evidence, findings)
    if "sensitivity-only" in evidence:
        findings.append(
            "## Evidence and update: sensitivity-only provenance may not appear here; "
            "it belongs in Robustness (SKILL.md § Numeric Policy)"
        )


def _check_no_prior_form(evidence: str, findings: list[str]) -> None:
    """The no-supported-prior form's pairings: an unquantified evidence row
    carries the sentinel in both its LR and provenance cells with a reason
    beside it, and the belief-slot sentinel fills Prior odds and Posterior
    odds together. Other provenance cells are checked against the closed set."""
    rows = _table_rows(evidence)
    lr_cells = _column(rows, "lr")
    source_cells = _column(rows, "source, reference class, conditioning")
    for i, cell in enumerate(_column(rows, "provenance")):
        cls = _normalize(cell)
        if cls == NO_LR_SENTINEL or (
            i < len(lr_cells) and _normalize(lr_cells[i]) == NO_LR_SENTINEL
        ):
            lr = _normalize(lr_cells[i]) if i < len(lr_cells) else ""
            if not (cls == NO_LR_SENTINEL and lr == NO_LR_SENTINEL):
                findings.append(
                    f"## Evidence and update: row {i + 1}: {NO_LR_SENTINEL!r} fills the LR and "
                    f"provenance cells together, or neither"
                )
            if i < len(source_cells) and not _normalize(source_cells[i]):
                findings.append(
                    f"## Evidence and update: row {i + 1}: an unquantified item carries its "
                    f"reason in the source cell"
                )
            continue
        if cls and not _unfilled(cls) and cls not in PROVENANCE:
            findings.append(
                f"## Evidence and update: provenance {cls!r} is not in the closed set "
                f"{sorted(PROVENANCE)}"
            )
    prior = _slot_value(evidence, "Prior odds")
    posterior = _slot_value(evidence, "Posterior odds")
    if prior is not None and posterior is not None:
        pr, po = _normalize(prior) == NO_PRIOR_SENTINEL, _normalize(posterior) == NO_PRIOR_SENTINEL
        if pr != po:
            findings.append(
                f"## Evidence and update: {NO_PRIOR_SENTINEL!r} fills Prior odds and Posterior "
                f"odds together, or neither"
            )


def _check_verdict_coupling(body: str, final: bool, findings: list[str]) -> None:
    """A `robust`, `prior-sensitive`, or `evidence-sensitive` verdict's losses
    carry belief-grade provenance; statewise verdicts use the Numeric Policy
    sentinels; `robust`
    needs a supported ratio. A slot still in template state is skipped
    outside final mode, like every other slot."""
    if _resolved(body, "decision"):
        _check_resolved(body, final, findings)
        return
    verdict_value = _slot_value(_section(body, "## Verdict"), "Verdict")
    if verdict_value is None or _unfilled(verdict_value):
        return
    verdict = _leading_token(verdict_value, DECIDE_VERDICTS)
    if verdict is None:
        return
    if "\n## Resolution\n" in body:
        findings.append(
            f"## Resolution: '## Resolution' belongs only to a resolved record; found it under "
            f"{verdict!r} (SKILL.md § The Decide Route)"
        )
    if verdict == "robust":
        _check_robust_has_a_supported_ratio(body, findings)
    if verdict in ("robust", "prior-sensitive", "evidence-sensitive"):
        _check_belief_grade_losses(body, verdict, final, findings)
    _check_none_needed_slots(body, verdict, final, findings)
    recommended = _slot_value(_section(body, "## Verdict"), "Recommended action")
    if (
        recommended is not None
        and (final or not _unfilled(recommended))
        and (_normalize(recommended) == "no preference") != (verdict == "indifferent")
    ):
        findings.append(
            "## Verdict: '- Recommended action:' must read 'no preference' "
            "exactly when the verdict is indifferent (SKILL.md § The Decide Route)"
        )


def _resolution_sections(body: str) -> list[str]:
    """Every visible `## Resolution` section, duplicates included."""
    parts = re.split(r"\n(?=## )", body)
    return [
        p.split("\n", 1)[1] if "\n" in p else ""
        for p in parts
        if p.rstrip() == "## Resolution" or p.startswith("## Resolution\n")
    ]


def _check_model_review(body: str, findings: list[str]) -> None:
    """Evidence impossible under both states reaches no verdict, under any;
    every Resolution section is read, so a duplicate cannot hide the marker."""
    sections = _resolution_sections(body)
    if len(sections) > 1:
        findings.append(f"## Resolution: duplicate section '## Resolution' ({len(sections)} found)")
    if any(
        (v := _slot_value(s, "Surviving state")) is not None and _normalize(v).lower() == "none"
        for s in sections
    ):
        findings.append(
            "## Resolution: '- Surviving state:' reads 'none': evidence impossible under both "
            "states goes to model review, never a verdict (SKILL.md § Numeric Policy)"
        )


def _check_resolution_slots(resolution: str, final: bool, findings: list[str]) -> None:
    """Order, state tokens, and the prose slots of a resolved record."""
    lines = [_unemphasize(ln.strip()) for ln in resolution.splitlines()]
    order = [
        next((i for i, ln in enumerate(lines) if ln.startswith(f"- {label}:")), -1)
        for label in RESOLUTION_ORDER
    ]
    if -1 not in order and order != sorted(order):
        findings.append("## Resolution: the labels must appear in the skeleton's order")
    for label in RESOLUTION_ORDER:
        if sum(ln.startswith(f"- {label}:") for ln in lines) > 1:
            findings.append(f"## Resolution: '- {label}:' must appear exactly once")
    excluded = _slot_value(resolution, "Excluded state")
    surviving = _slot_value(resolution, "Surviving state")
    if (
        excluded is not None
        and (final or not _unfilled(excluded))
        and _normalize(excluded) not in RESOLVED_STATES
    ):
        findings.append(
            f"## Resolution: '- Excluded state:' must read one of "
            f"{sorted(RESOLVED_STATES)}; found {excluded!r}"
        )
    if surviving is not None and (final or not _unfilled(surviving)):
        s = _normalize(surviving)
        if s.lower() != "none" and s not in RESOLVED_STATES:
            findings.append(
                f"## Resolution: '- Surviving state:' must read one of "
                f"{sorted(RESOLVED_STATES)} or 'none'; found {surviving!r}"
            )
        elif excluded is not None and s == _normalize(excluded):
            findings.append(
                "## Resolution: '- Excluded state:' and '- Surviving state:' must differ"
            )
    for label in RESOLVED_PROSE:
        value = _slot_value(resolution, label)
        if value is not None and _normalize(value).lower() == "none":
            findings.append(f"## Resolution: '{label}' must state its content, not 'none'")


def _check_resolved(body: str, final: bool, findings: list[str]) -> None:  # noqa: PLR0912, PLR0915 -- one pass over the resolved coupling
    """A resolved record's coupling (decision-analysis decisions/008): exactly
    one Verdict line reading `- Verdict: resolved`; no odds-only section or
    label anywhere (one still in template state waits for final mode); the
    section order; the Resolution slots and tables; the difference's
    provenance; and the recommendation that provenance allows, which waits,
    outside final mode, until the difference is filled. Belief-grade support
    means the difference and both losses rows carry a belief-grade class. The
    sign of the difference is arithmetic, so it is the dev checker's alone."""
    lines = _verdict_lines(body)
    if len(lines) != 1 or lines[0].group(0).strip() != "- Verdict: resolved":
        findings.append(
            "## Verdict: a resolved record carries exactly one '- Verdict:' line, which must "
            "read exactly '- Verdict: resolved' (no emphasis, code, or annotation); found "
            f"{[m.group(0).strip() for m in lines]!r}"
        )
    for heading in ODDS_ONLY_SECTIONS:
        if f"\n{heading}\n" in body:
            findings.append(
                f"## Verdict: a resolved record carries no odds-only field; found '{heading}'"
            )
    for label in ODDS_ONLY_LABELS:
        for line in body.splitlines():
            stripped = _unemphasize(line.strip())
            if not stripped.startswith(f"- {label}:"):
                continue
            if final or not _unfilled(stripped[len(label) + 3 :]):
                findings.append(
                    f"## Verdict: a resolved record carries no odds-only field; found '- {label}:'"
                )
                break
    order = [h for h in RESOLVED_SECTIONS if f"\n{h}\n" in body]
    seen = [ln.rstrip() for ln in body.splitlines() if ln.rstrip() in RESOLVED_SECTIONS]
    if list(dict.fromkeys(seen)) != order:
        findings.append(
            f"## Verdict: a resolved record's sections must appear in the order {RESOLVED_SECTIONS}"
        )
    frame = _section(body, "## Decision frame")
    resolution = _section(body, "## Resolution")
    if not resolution.strip():
        return  # the missing-section finding covers it
    _check_resolution_slots(resolution, final, findings)

    obs_span = _nested_span(resolution, "Observations")
    obs = _table_rows(obs_span) if obs_span is not None else []
    if obs:
        if [_header_key(h) for h in obs[0]] != ["observation", "source"]:
            findings.append(
                "## Resolution: '- Observations:' table header must be exactly "
                "'observation | source'"
            )
        for i, row in enumerate(obs[1:], 1):
            if len(row) != 2:  # noqa: PLR2004 -- observation, source
                findings.append(
                    f"## Resolution: '- Observations:' row {i} must be exactly two cells; "
                    f"found {row!r}"
                )

    actions_value = _slot_value(frame, "Actions") or ""
    names = [a.strip() for a in re.split(r"\s+vs\s+", _normalize(actions_value))]
    span = _nested_span(resolution, "Surviving-state losses")
    rows = _table_rows(span) if span is not None else []
    unsupported = False
    row_provs: list[str] = []
    if rows:
        if [_header_key(h) for h in rows[0]] != ["action", "loss", "provenance"]:
            findings.append(
                "## Resolution: '- Surviving-state losses:' table header must be exactly "
                "'action | loss | provenance'"
            )
        listed = []
        for row in rows[1:]:
            if len(row) != 3:  # noqa: PLR2004 -- action, loss, provenance
                findings.append(
                    f"## Resolution: '- Surviving-state losses:' row {row!r} must be three "
                    "cells wide"
                )
                continue
            action, loss, prov = (_normalize(c) for c in row)
            listed.append(action)
            row_provs.append(prov)
            if NO_LR_SENTINEL in (loss, prov):
                unsupported = True
                if loss != prov:
                    findings.append(
                        f"## Resolution: '- Surviving-state losses:' row {action!r}: "
                        f"{NO_LR_SENTINEL!r} fills the loss and provenance cells together"
                    )
            elif not _unfilled(prov) and prov not in PROVENANCE:
                findings.append(
                    f"## Resolution: '- Surviving-state losses:' row {action!r}: {prov!r} is "
                    "not a provenance class"
                )
        if not any(_unfilled(a) for a in listed) and (
            sorted(listed) != sorted(names) or len(listed) != len(names)
        ):
            findings.append(
                "## Resolution: '- Surviving-state losses:' must carry exactly one row per "
                f"framed action {names!r}; found {listed!r}"
            )

    difference = _slot_value(resolution, "Surviving-state loss difference")
    belief = False
    if difference is not None and (final or not _unfilled(difference)):
        if _normalize(difference) == NO_LR_SENTINEL:
            if not unsupported:
                findings.append(
                    "## Resolution: '- Surviving-state loss difference:' reads 'none supported' "
                    "exactly when a losses row does"
                )
        else:
            if unsupported:
                findings.append(
                    "## Resolution: '- Surviving-state loss difference:' reads 'none supported' "
                    "exactly when a losses row does"
                )
            provs = PROVENANCE_MENTION.findall(difference)
            if len(provs) != 1:
                findings.append(
                    "## Resolution: '- Surviving-state loss difference:' must carry exactly one "
                    "provenance class"
                )
            elif provs[0] not in PROVENANCE:
                findings.append(
                    f"## Resolution: provenance {provs[0]!r} is not in the closed set "
                    f"{sorted(PROVENANCE)}"
                )
            belief = (
                len(provs) == 1
                and provs[0] in LOSS_PROVENANCE_FOR_ROBUST
                and len(row_provs) == len(names)
                and all(p in LOSS_PROVENANCE_FOR_ROBUST for p in row_provs)
            )

    recommended = _slot_value(_section(body, "## Verdict"), "Recommended action")
    if recommended is None or (not final and _unfilled(recommended)):
        return
    if not final and (difference is None or _unfilled(difference)):
        return  # the coupling waits for a filled difference
    rec = _normalize(recommended)
    if rec not in (*names, *RESOLVED_RECOMMENDATIONS):
        findings.append(
            "## Verdict: a resolved verdict's '- Recommended action:' must name one of the "
            f"framed actions {names!r}, or read 'no preference' or 'returned to owner'; "
            f"found {recommended!r}"
        )
    elif not belief and difference is not None and rec != "returned to owner":
        findings.append(
            "## Verdict: a resolved verdict whose surviving-state losses or loss difference are "
            "not all belief-grade, or read 'none supported', requires '- Recommended action:' "
            "to read "
            f"'returned to owner'; found {recommended!r} (SKILL.md § Numeric Policy)"
        )


def _check_robust_has_a_supported_ratio(body: str, findings: list[str]) -> None:
    rows = _table_rows(_section(body, "## Evidence and update"))
    lrs = [_normalize(c) for c in _column(rows, "lr")]
    if lrs and all(v == NO_LR_SENTINEL for v in lrs):
        findings.append(
            "## Verdict: robust with every evidence row in the missing-ratio form; no "
            "quantitative update is supported, so hypothetical inputs alone cannot reach "
            "robust (SKILL.md § Numeric Policy)"
        )


def _check_belief_grade_losses(body: str, verdict: str, final: bool, findings: list[str]) -> None:
    slots = (("## Decision frame", "Loss ratio"), ("## Robustness", "Loss range swept"))
    for heading, label in slots:
        value = _slot_value(_section(body, heading), label)
        if value is None or (not final and _unfilled(value)):
            continue  # a missing slot is already its own finding
        provs = PROVENANCE_MENTION.findall(value)
        if len(provs) != 1 or provs[0] not in LOSS_PROVENANCE_FOR_ROBUST:
            findings.append(
                f"{heading}: a {verdict} verdict requires '- {label}:' to carry exactly one "
                f"provenance from {sorted(LOSS_PROVENANCE_FOR_ROBUST)}; any other class caps "
                f"the verdict at loss-sensitive; found {value!r} (SKILL.md § Numeric Policy)"
            )


def _check_none_needed_slots(body: str, verdict: str, final: bool, findings: list[str]) -> None:
    """Check the sentinel coupling from Numeric Policy."""
    loss_slots = (("## Decision frame", "Loss ratio"), ("## Robustness", "Loss range swept"))
    for heading, label in (*STATEWISE_NONE_NEEDED, *loss_slots):
        value = _slot_value(_section(body, heading), label)
        if value is None:
            continue
        is_sentinel = _normalize(value) == "none needed"
        if verdict == "indifferent" or (
            verdict == "dominated" and (heading, label) in STATEWISE_NONE_NEEDED
        ):
            if (not final and _unfilled(value)) or is_sentinel:
                continue
            findings.append(
                f"{heading}: a {verdict} verdict requires '- {label}:' to read exactly "
                f"'none needed'; found {value!r} (SKILL.md § The Decide Route)"
            )
        elif is_sentinel:
            findings.append(
                f"{heading}: '- {label}:' reads 'none needed', which is reserved for "
                f"dominated or indifferent records as specified for this slot; found {verdict!r} "
                f"(SKILL.md § The Decide Route)"
            )


def _check_decision_provenance(body: str, final: bool, findings: list[str]) -> None:
    """Numeric Policy, structurally (issue #60): the provenance vocabulary and
    the verdict-to-provenance coupling SKILL.md § Numeric Policy states."""
    _check_provenance_vocab(body, findings)
    _check_verdict_coupling(body, final, findings)


def check(text: str, *, final: bool = False) -> list[str]:  # noqa: PLR0912, PLR0915 -- one findings pass per record kind
    """Findings for one record. `final` is the completed-record mode: template
    state no longer suspends completeness and is itself a finding."""
    text = strip_frontmatter(text)
    kind = detect(text)
    if kind is None:
        raise ValueError("not a recognized record")
    findings: list[str] = []
    body, unterminated_fence, _, _ = _strip_hidden(text)
    # An unterminated fence blanks everything after it (including any
    # genuinely-present later sections), so completeness findings there
    # would fail correct work — treat the record as in-progress instead.
    # Vocabulary checks still run on whatever body remains (the pre-fence
    # part).
    in_progress = unterminated_fence or (not final and _in_progress(body, kind))
    if unterminated_fence:
        findings.append("unterminated code fence: completeness past it was not checked")

    if not in_progress:
        for heading in _required_sections(body, kind):
            if ("\n" + heading + "\n") not in body:
                findings.append(f"required section missing: {heading}")
                continue
            content = _section(body, heading).strip()
            if not content:
                findings.append(f"required section empty: {heading}")
            elif final and _section_unfilled(content):
                # Final mode turns `_in_progress` off, so without this the
                # sanctioned plan-stage marker reads as finished content.
                findings.append(f"required section still unfilled: {heading}: {content!r}")
        _check_slots(body, kind, final, findings)
        _check_table_cells(body, kind, final, findings)
        _check_nested_tables(body, kind, final, findings)
        if kind == "review":
            _check_review_route_blocks(body, final, findings)

    if kind == "ledger":
        # No id-grammar check on `id` cells (e.g. H1 vs H4 (retrospective)):
        # the template's own retrospective-hypothesis form breaks a strict
        # grammar, and leniency wins when a fix would force a false positive.
        hyp = _table_rows(_section(body, "## Hypotheses"))
        hyp_ok = in_progress or _require_column(hyp, "claim", "Hypotheses", findings)
        if hyp_ok:
            for v in _column(hyp, "claim"):
                _check_claim(v, "Hypotheses", findings, final)
        if not in_progress:
            if len(hyp) < MIN_TABLE_ROWS:
                findings.append("Hypotheses: table has no data rows")
            if _require_column(hyp, "necessary prediction", "Hypotheses", findings):
                for i, v in enumerate(_column(hyp, "necessary prediction"), 1):
                    if not v.strip():
                        findings.append(f"Hypotheses row {i}: necessary prediction is empty")
                    else:
                        _unfilled_cell(v, f"Hypotheses row {i}", final, findings)
        tests = _table_rows(_section(body, "## Tests"))
        if in_progress or _require_column(tests, "outcome", "Tests", findings):
            for v in _column(tests, "outcome"):
                if _unfilled_cell(v, "Tests", final, findings):
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
                if _unfilled_cell(v, "Conclusion", final, findings):
                    continue
                if _normalize(v) not in STATUSES:
                    findings.append(
                        f"Conclusion: status {_normalize(v)!r} is not REFUTED or UNRESOLVED "
                        f"(the status set is closed)"
                    )
        if in_progress or _require_column(concl, "claim", "Conclusion", findings):
            for v in _column(concl, "claim"):
                _check_claim(v, "Conclusion", findings, final)
        if not in_progress and len(concl) < MIN_TABLE_ROWS:
            findings.append("Conclusion: per-hypothesis table has no data rows")

    elif kind == "review":
        # Vocabulary, like every closed set here, is checked whatever the
        # record's fill state and whatever the design's disposition.
        for h in re.findall(r"^## Design: .*$", body, re.M):
            _check_assessments(_section(body, h.rstrip()), h.rstrip(), findings)
        for line in body.splitlines():
            stripped = _unemphasize(line.strip())
            if stripped.startswith("- Disposition:"):
                value = stripped.split(":", 1)[1]
                if _unfilled_cell(value, "Disposition", final, findings):
                    continue
                if _leading_token(value, DISPOSITIONS | {"none"}) is None:
                    findings.append(
                        f"disposition {_normalize(value)!r} does not begin with a value "
                        f"from the closed set {sorted(DISPOSITIONS | {'none'})} — 'valid' and "
                        f"'certified' are not dispositions"
                    )
            if stripped.startswith("- Dispositions:"):
                # The Handoff slot carries every value assigned above, so it
                # is a collection (the template's "disposition value(s)"), or
                # the `none` sentinel for a route that assigns none. Every
                # item must itself be a closed-set value: a list is not a way
                # to smuggle `certified` in behind a valid first item.
                value = stripped.split(":", 1)[1]
                if _unfilled_cell(value, "Disposition", final, findings):
                    continue
                # A single value with an annotation was always accepted, and
                # stays so; the list form is the addition.
                if _leading_token(value, DISPOSITIONS | {"none"}) is None and not _mentions_only(
                    value, DISPOSITIONS
                ):
                    findings.append(
                        f"disposition {_normalize(value)!r} is neither 'none' nor a list of "
                        f"values from the closed set {sorted(DISPOSITIONS | {'none'})} — 'valid' "
                        f"and 'certified' are not dispositions"
                    )
            if stripped.startswith("- Route:"):
                value = stripped.split(":", 1)[1]
                if not _is_placeholder(value) and _leading_token(value, ROUTES) is None:
                    findings.append(
                        f"route {_normalize(value)!r} does not begin with a value from the "
                        f"closed set {sorted(ROUTES)}"
                    )

    elif kind in ("decision", "voi"):
        allowed = DECIDE_VERDICTS if kind == "decision" else VOI_VERDICTS
        heading = "## Verdict" if kind == "decision" else "## VoI"
        section = _section(body, heading)
        for line in section.splitlines():
            stripped = _unemphasize(line.strip())
            if stripped.startswith("- Verdict:"):
                value = stripped.split(":", 1)[1]
                if _unfilled_cell(value, "Verdict", final, findings):
                    continue
                if _leading_token(value, allowed) is None:
                    findings.append(
                        f"verdict {_normalize(value)!r} does not begin with a value "
                        f"from the closed set {sorted(allowed)}"
                    )
        # Closed slots beside the verdict: the record kind fixes its Route,
        # and a VoI record's Value basis is one of two values.
        closed = {"Route": {"decide"} if kind == "decision" else {"voi"}}
        if kind == "voi":
            closed["Value basis"] = VOI_VALUE_BASES
        for label, tokens in closed.items():
            for line in body.splitlines():
                stripped = _unemphasize(line.strip())
                if not stripped.startswith(f"- {label}:"):
                    continue
                value = stripped.split(":", 1)[1]
                if _unfilled_cell(value, label, final, findings):
                    continue
                if _leading_token(value, tokens) is None:
                    findings.append(
                        f"{label.lower()} {_normalize(value)!r} does not begin with a value "
                        f"from the closed set {sorted(tokens)}"
                    )
        if kind == "decision":
            _check_model_review(body, findings)
            _check_decision_provenance(body, final, findings)

    return findings


def main(argv: list[str]) -> int:
    final = "--final" in argv
    paths = [a for a in argv if a != "--final"]
    if len(paths) != 1:
        print("usage: check_record.py [--final] <record.md>", file=sys.stderr)
        return 2
    try:
        text = Path(paths[0]).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"unreadable: {exc}", file=sys.stderr)
        return 2
    try:
        findings = check(text, final=final)
    except ValueError:
        return 2
    for f in findings:
        print(f)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
