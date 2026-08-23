"""EDA's authorization gate must match HDA's verbatim.

decisions/001-shared-gate-authority.md names hypothesis-driven-analysis/SKILL.md
as the single authority for the authorization-gate text; this check keeps the
copy from drifting (AGENTS.md: one home per normative rule).
"""

import re
from pathlib import Path

import pytest

SKILLS_DIR = Path(__file__).resolve().parents[2]
HDA_SKILL = SKILLS_DIR / "hypothesis-driven-analysis" / "SKILL.md"
EDA_SKILL = SKILLS_DIR / "exploratory-data-analysis" / "SKILL.md"
HEADING = "### Authorization gate (always binds)"
MIN_GATE_LENGTH = 1000


FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
INLINE_COMMENT = re.compile(r"<!--.*?-->")


BACKTICK_RUN = re.compile(r"`+")


def code_span_interiors(line: str) -> list[tuple[int, int]]:
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


def shadow(line: str) -> str:
    """`line` with code-span interiors blanked index-for-index, so a delimiter
    Markdown renders as code is never read as markup."""
    out = list(line)
    for start, end in code_span_interiors(line):
        for k in range(start, end):
            out[k] = "\x01"
    return "".join(out)


def strip_comment(line: str) -> tuple[str, bool]:
    """Drop HTML comments a reader never sees, ignoring `<!--` and `-->` that
    Markdown renders as code. Returns (visible, comment_left_open)."""
    masked = shadow(line)
    for m in reversed(list(INLINE_COMMENT.finditer(masked))):
        line = line[: m.start()] + line[m.end() :]
        masked = masked[: m.start()] + masked[m.end() :]
    opener = masked.find("<!--")
    if opener != -1:
        return line[:opener], True
    return line, False


def visible_text(text: str) -> str:
    """Text an agent reads as instruction: no fenced blocks, no HTML comments.
    One pass tracks both states so neither can hide the other's delimiters;
    per CommonMark a closer has nothing but whitespace after its run, `<!--`
    inside a fence is code, and an unclosed comment runs to end of document."""
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
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        m = FENCE.match(line)
        if m:
            fence = (m.group(1)[0], len(m.group(1)))
            continue
        visible, opened = strip_comment(line)
        if opened:
            in_comment = True
        out.append(visible)
    return "\n".join(out)


def gate_block_from_text(text: str) -> str:
    text = visible_text(text)
    start = text.index(HEADING)  # ValueError when the gate is not visible
    rest = text[start + len(HEADING) :]
    nxt = re.search(r"\n#{2,3} ", rest)
    end = start + len(HEADING) + (nxt.start() if nxt else len(rest))
    return text[start:end].strip()


def gate_block(path: Path) -> str:
    return gate_block_from_text(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("path", [HDA_SKILL, EDA_SKILL], ids=["hda", "eda"])
def test_gate_block_extracts_real_content(path: Path):
    """The instrument can surface a known positive, so an empty match cannot pass.

    Run against both sides, not just the authority: a comparison of two blocks
    the extractor silently truncated the same way would pass while checking
    nothing.
    """
    block = gate_block(path)
    assert "None of the following is authorization" in block
    assert len(block) > MIN_GATE_LENGTH


def test_authorization_gate_matches_hda_verbatim():
    assert gate_block(EDA_SKILL) == gate_block(HDA_SKILL)


def test_commented_out_gate_is_not_a_gate():
    """A gate wrapped in an HTML comment is not loaded as instruction, so the
    extractor must not find it — the known negative for this instrument."""
    text = EDA_SKILL.read_text(encoding="utf-8")
    block = gate_block(EDA_SKILL)
    disabled = text.replace(block, "<!--\n" + block + "\n### (disabled)\n-->")
    assert disabled != text
    with pytest.raises(ValueError):  # noqa: PT011
        gate_block_from_text(disabled)


def test_fenced_gate_is_not_a_gate():
    text = EDA_SKILL.read_text(encoding="utf-8")
    block = gate_block(EDA_SKILL)
    disabled = text.replace(block, "```text\n" + block + "\n```")
    with pytest.raises(ValueError):  # noqa: PT011
        gate_block_from_text(disabled)


def test_unclosed_comment_also_hides_the_gate():
    """CommonMark: an HTML comment opened and never closed runs to end of
    document, so everything after `<!--` is hidden from a reader."""
    text = EDA_SKILL.read_text(encoding="utf-8")
    block = gate_block(EDA_SKILL)
    disabled = text.replace(block, "<!--\n" + block)
    assert disabled != text
    with pytest.raises(ValueError):  # noqa: PT011
        gate_block_from_text(disabled)


def test_comment_opener_inside_a_fence_does_not_hide_the_gate():
    text = EDA_SKILL.read_text(encoding="utf-8")
    block = gate_block(EDA_SKILL)
    decoy = "```text\n<!--\n```\n\n"
    assert gate_block_from_text(decoy + text) == block


def test_fence_closer_with_info_string_keeps_the_fence_open():
    text = EDA_SKILL.read_text(encoding="utf-8")
    block = gate_block(EDA_SKILL)
    disabled = text.replace(block, "```text\n```python\n" + block + "\n```")
    assert disabled != text
    with pytest.raises(ValueError):  # noqa: PT011
        gate_block_from_text(disabled)


def test_comment_delimiter_inside_inline_code_does_not_hide_the_gate():
    """A documentation example of the `<!--` token is code, not a comment
    opener, so it must not blank the live gate below it."""
    text = "The token `<!--` is documented here.\n\n## Authorization\n\nGate text lives here.\n"
    assert "## Authorization" in visible_text(text)
