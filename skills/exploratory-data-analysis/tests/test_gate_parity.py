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


def gate_block(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    start = text.index(HEADING)
    rest = text[start + len(HEADING) :]
    nxt = re.search(r"\n#{2,3} ", rest)
    end = start + len(HEADING) + (nxt.start() if nxt else len(rest))
    return text[start:end].strip()


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
