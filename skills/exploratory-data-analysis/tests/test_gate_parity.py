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


COMMENT = re.compile(r"<!--.*?-->", re.S)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def visible_text(text: str) -> str:
    """Text an agent reads as instruction: no HTML comments, no fenced blocks."""
    text = COMMENT.sub("", text)
    out: list[str] = []
    fence: tuple[str, int] | None = None
    for line in text.split("\n"):
        m = FENCE.match(line)
        if fence is None:
            if m:
                fence = (m.group(1)[0], len(m.group(1)))
                continue
            out.append(line)
        elif m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1]:
            fence = None
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
