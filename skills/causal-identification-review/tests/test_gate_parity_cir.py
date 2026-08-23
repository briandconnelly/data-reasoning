"""causal-identification-review's authorization gate must match HDA's verbatim.

Mirrors `skills/exploratory-data-analysis/tests/test_gate_parity.py`. Skills
install standalone -- a harness may load any one of them without the others
on disk -- so each skill carries its own verbatim copy of the shared
authorization-gate text rather than pointing at another skill's file
(AGENTS.md: one home per normative rule, everywhere else a copy or a
pointer). `hypothesis-driven-analysis/SKILL.md` § "Authorization gate
(always binds)" is that one home; this check keeps this skill's copy from
drifting from it.
"""

import re
from pathlib import Path

import pytest

SKILLS_DIR = Path(__file__).resolve().parents[2]
HDA_SKILL = SKILLS_DIR / "hypothesis-driven-analysis" / "SKILL.md"
CIR_SKILL = SKILLS_DIR / "causal-identification-review" / "SKILL.md"
HEADING = "### Authorization gate (always binds)"
MIN_GATE_LENGTH = 1000


FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
INLINE_COMMENT = re.compile(r"<!--.*?-->")


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
        visible = INLINE_COMMENT.sub("", line)
        if "<!--" in visible:
            visible = visible[: visible.index("<!--")]
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


@pytest.mark.parametrize("path", [HDA_SKILL, CIR_SKILL], ids=["hda", "cir"])
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
    assert gate_block(CIR_SKILL) == gate_block(HDA_SKILL)


def test_commented_out_gate_is_not_a_gate():
    """A gate wrapped in an HTML comment is not loaded as instruction, so the
    extractor must not find it — the known negative for this instrument."""
    text = CIR_SKILL.read_text(encoding="utf-8")
    block = gate_block(CIR_SKILL)
    disabled = text.replace(block, "<!--\n" + block + "\n### (disabled)\n-->")
    assert disabled != text
    with pytest.raises(ValueError):  # noqa: PT011
        gate_block_from_text(disabled)


def test_fenced_gate_is_not_a_gate():
    text = CIR_SKILL.read_text(encoding="utf-8")
    block = gate_block(CIR_SKILL)
    disabled = text.replace(block, "```text\n" + block + "\n```")
    with pytest.raises(ValueError):  # noqa: PT011
        gate_block_from_text(disabled)


def test_unclosed_comment_also_hides_the_gate():
    """CommonMark: an HTML comment opened and never closed runs to end of
    document, so everything after `<!--` is hidden from a reader."""
    text = CIR_SKILL.read_text(encoding="utf-8")
    block = gate_block(CIR_SKILL)
    disabled = text.replace(block, "<!--\n" + block)
    assert disabled != text
    with pytest.raises(ValueError):  # noqa: PT011
        gate_block_from_text(disabled)


def test_comment_opener_inside_a_fence_does_not_hide_the_gate():
    text = CIR_SKILL.read_text(encoding="utf-8")
    block = gate_block(CIR_SKILL)
    decoy = "```text\n<!--\n```\n\n"
    assert gate_block_from_text(decoy + text) == block


def test_fence_closer_with_info_string_keeps_the_fence_open():
    text = CIR_SKILL.read_text(encoding="utf-8")
    block = gate_block(CIR_SKILL)
    disabled = text.replace(block, "```text\n```python\n" + block + "\n```")
    assert disabled != text
    with pytest.raises(ValueError):  # noqa: PT011
        gate_block_from_text(disabled)
