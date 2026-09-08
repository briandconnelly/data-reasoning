"""The shared-section checker must catch drift and must be able to fail.

Two mechanisms, two halves. decisions/001-shared-gate-authority.md (EDA)
enumerates the invariants the costly-collection and data-rules copies must
preserve; the checker freezes bytes and routes any editor to that list. The
authorization gate is rendered from one authority file into every carrier
instead, so the second half of this suite checks that the rendered copies
match it and stay visible to a reader
(skills/hypothesis-driven-analysis/decisions/007-shared-text-is-rendered-not-copied.md).
"""

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

MIN_SECTION_SIZE = 150
EXPECTED_ERROR_CODE = 2

SCRIPTS = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "check_shared_sections", SCRIPTS / "check-shared-sections.py"
)
css = importlib.util.module_from_spec(spec)
spec.loader.exec_module(css)

REPO = SCRIPTS.parent


def make_fake_repo(tmp_path: Path) -> Path:
    fake = tmp_path / "repo"
    shutil.copytree(REPO / "skills", fake / "skills")
    shutil.copytree(REPO / "scripts" / "shared-sections", fake / "scripts" / "shared-sections")
    return fake


def test_every_target_extracts_real_content():
    """Known positive: each configured section extracts non-trivially."""
    for skill, heading, _slug in css.TARGETS:
        text = (REPO / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        block = css.extract_section(text, heading)
        assert block.startswith(heading + "\n")
        assert len(block) > MIN_SECTION_SIZE, (skill, heading)


def test_missing_heading_is_an_error_not_a_pass():
    with pytest.raises(ValueError, match="heading not found"):
        css.extract_section("# nothing here\n", "### Costly collection (modifier, not a route)")


def test_extraction_stops_at_next_same_or_higher_heading():
    text = "## Data Rules\n\nline one\n\n## Next Section\n\nnope\n"
    block = css.extract_section(text, "## Data Rules")
    assert "line one" in block
    assert "nope" not in block


def test_extraction_ignores_headings_inside_code_fences():
    text = "## Data Rules\n\n```\n## Not A Heading\n```\nline two\n\n## Next\n"
    block = css.extract_section(text, "## Data Rules")
    assert "line two" in block
    assert "## Not A Heading" in block


def test_boundary_blank_line_changes_are_detected():
    """The frozen slice is exact bytes, including boundary blank lines."""
    a = css.extract_section("## Data Rules\n\nbody\n\n## Next\n", "## Data Rules")
    b = css.extract_section("## Data Rules\n\nbody\n\n\n## Next\n", "## Data Rules")
    assert a != b


def test_drift_is_detected(tmp_path, capsys):
    """Mutation check: a one-character edit to any copy must fail the run."""
    fake = make_fake_repo(tmp_path)
    victim = fake / "skills" / "exploratory-data-analysis" / "SKILL.md"
    victim.write_text(
        victim.read_text(encoding="utf-8").replace(
            "Cost never changes the route", "Cost rarely changes the route"
        ),
        encoding="utf-8",
    )
    assert css.run(fake, update=frozenset()) == 1
    assert "001-shared-gate-authority.md" in capsys.readouterr().err


def test_update_is_targeted(tmp_path, capsys):
    """--update refreshes only the named golden, so a drift elsewhere still fails."""
    fake = make_fake_repo(tmp_path)
    victim = fake / "skills" / "exploratory-data-analysis" / "SKILL.md"
    old_cost = (
        "Cost never changes the route: a metered warehouse makes profiling more expensive, "
        "not more inferential."
    )
    new_cost = (
        "Cost never changes the route: a metered warehouse makes profiling costlier, "
        "not more inferential."
    )
    old_provenance = (
        "Minimize collection, redact secrets and personal data, and record provenance "
        "for every source."
    )
    new_provenance = (
        "Minimize collection, redact secrets and personal data, and record provenance "
        "for each source."
    )
    victim.write_text(
        victim.read_text(encoding="utf-8")
        .replace(old_cost, new_cost)
        .replace(old_provenance, new_provenance),
        encoding="utf-8",
    )
    css.run(fake, update=frozenset({"eda-costly-collection"}))  # refreshes only that golden
    assert css.run(fake, update=frozenset()) == 1  # the un-updated data-rules drift still fails
    capsys.readouterr()  # drain
    css.run(fake, update=frozenset())
    err = capsys.readouterr().err
    assert "eda-data-rules" in err
    assert "eda-costly-collection" not in err


def test_unknown_update_target_is_an_error():
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "check-shared-sections.py"), "--update", "no-such-slug"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == EXPECTED_ERROR_CODE


def test_boundary_blank_line_drift_fails_run(tmp_path):
    """A boundary blank-line edit must fail the production comparison path."""
    fake = make_fake_repo(tmp_path)
    victim = fake / "skills" / "exploratory-data-analysis" / "SKILL.md"
    victim.write_text(
        victim.read_text(encoding="utf-8").replace(
            "\n\n## The Lifecycle (explore route)", "\n\n\n## The Lifecycle (explore route)"
        ),
        encoding="utf-8",
    )
    assert css.run(fake, update=frozenset()) == 1


def test_clean_repo_passes():
    assert css.run(REPO, update=frozenset()) == 0


def test_commented_out_heading_is_not_found():
    heading = "## Data Rules"
    text = f"# Skill\n\n<!--\n{heading}\n\nhidden\n-->\n\n## Other\n\nvisible\n"
    with pytest.raises(ValueError, match="heading not found"):
        css.extract_section(text, heading)


def test_comment_opener_inside_a_fence_does_not_hide_a_later_section():
    heading = "## Data Rules"
    text = f"# Skill\n\n```\n<!--\n```\n\n{heading}\n\nvisible rule\n\n## Other\n\nx\n"
    block = css.extract_section(text, heading)
    assert block.startswith(heading + "\n")
    assert "visible rule" in block


def test_tilde_fenced_heading_is_not_found():
    heading = "## Data Rules"
    text = f"# Skill\n\n~~~\n{heading}\n\nfenced, not live\n~~~\n\n## Other\n\nx\n"
    with pytest.raises(ValueError, match="heading not found"):
        css.extract_section(text, heading)


def test_a_shorter_backtick_run_does_not_close_a_longer_fence():
    heading = "## Data Rules"
    text = f"# Skill\n\n````\n```\n{heading}\n\nfenced, not live\n````\n\n## Other\n\nx\n"
    with pytest.raises(ValueError, match="heading not found"):
        css.extract_section(text, heading)


def test_comment_delimiter_inside_inline_code_does_not_hide_a_section():
    heading = "## Data Rules"
    text = (
        f"# Skill\n\nThe token `<!--` is documented.\n\n{heading}\n\nreal rule\n\n## Other\n\nx\n"
    )
    block = css.extract_section(text, heading)
    assert block.startswith(heading + "\n")
    assert "real rule" in block


def test_escaped_backticks_do_not_shield_a_comment_opener():
    """Both backticks are escaped, so CommonMark sees no code span and the
    `<!--` really does open a comment that hides the section."""
    heading = "## Data Rules"
    text = f"# Skill\n\na \\`<!--\\` b\n\n{heading}\n\nhidden\n\n-->\n\n## Other\n\nx\n"
    with pytest.raises(ValueError, match="heading not found"):
        css.extract_section(text, heading)


def test_a_backtick_fence_info_string_may_not_contain_a_backtick():
    heading = "## Data Rules"
    text = f"# Skill\n\n```bad`info\n\n{heading}\n\nreal rule\n\n## Other\n\nx\n"
    block = css.extract_section(text, heading)
    assert "real rule" in block


# --- the rendered authorization gate -------------------------------------
#
# The gate text has one home, scripts/shared-sections/authorization-gate.md,
# rendered into each carrier between marker comments. These cases replace the
# three per-skill parity tests (test_gate_parity*.py) and scripts/
# test_extractor_parity.py, which guarded four hand-maintained copies.

DA_SKILL = REPO / "skills" / "decision-analysis" / "SKILL.md"
GATE = "authorization-gate"
GATE_OPEN = f"<!-- shared: {GATE} -->"
GATE_CLOSE = f"<!-- /shared: {GATE} -->"
MIN_GATE_LENGTH = 1000


def marked_region(text: str) -> str:
    """The marker pair and everything between it, exactly as it sits in `text`."""
    region = GATE_OPEN + "\n" + css.extract_marked(text, GATE) + GATE_CLOSE
    assert region in text
    return region


def test_marked_gate_extracts_real_content():
    """The instrument can surface a known positive, so an empty match cannot pass.

    Run against every carrier, not just the authority: a comparison of blocks
    the extractor silently truncated the same way would pass while checking
    nothing.
    """
    for skill in css.GATE_CARRIERS:
        text = (REPO / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        block = css.extract_marked(text, GATE)
        assert "None of the following is authorization" in block, skill
        assert len(block) > MIN_GATE_LENGTH, skill


def test_every_carrier_matches_the_authority_verbatim():
    authority = (REPO / css.GATE_AUTHORITY).read_text(encoding="utf-8")
    for skill in css.GATE_CARRIERS:
        text = (REPO / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        assert css.extract_marked(text, GATE) == authority, skill


def test_known_positive_the_real_repo_passes():
    assert css.run_gate(REPO, render=False) == 0


def test_gate_check_fails_on_a_one_character_drift(tmp_path, capsys):
    fake = make_fake_repo(tmp_path)
    victim = fake / "skills" / "decision-analysis" / "SKILL.md"
    victim.write_text(
        victim.read_text(encoding="utf-8").replace(
            "Authorization is affirmative and specific to the action;",
            "Authorization is affirmative and specific to the actions;",
        ),
        encoding="utf-8",
    )
    assert css.run_gate(fake, render=False) == 1
    assert "decision-analysis" in capsys.readouterr().err


def test_render_restores_a_drifted_block(tmp_path):
    fake = make_fake_repo(tmp_path)
    victim = fake / "skills" / "decision-analysis" / "SKILL.md"
    before = victim.read_text(encoding="utf-8")
    victim.write_text(
        before.replace(
            "Authorization is affirmative and specific to the action;",
            "Authorization is affirmative and specific to the actions;",
        ),
        encoding="utf-8",
    )
    assert css.run_gate(fake, render=False) == 1
    assert css.run_gate(fake, render=True) == 0
    assert victim.read_text(encoding="utf-8") == before
    assert css.run_gate(fake, render=False) == 0


def test_missing_marker_pair_fails(tmp_path):
    fake = make_fake_repo(tmp_path)
    victim = fake / "skills" / "decision-analysis" / "SKILL.md"
    text = victim.read_text(encoding="utf-8")
    victim.write_text(
        text.replace(GATE_OPEN + "\n", "").replace(GATE_CLOSE + "\n", ""), encoding="utf-8"
    )
    assert css.run_gate(fake, render=False) == EXPECTED_ERROR_CODE
    assert css.run_gate(fake, render=True) == EXPECTED_ERROR_CODE


def test_two_marker_pairs_in_one_carrier_fail(tmp_path):
    fake = make_fake_repo(tmp_path)
    victim = fake / "skills" / "decision-analysis" / "SKILL.md"
    text = victim.read_text(encoding="utf-8")
    region = marked_region(text)
    victim.write_text(text.replace(region, region + "\n\n" + region), encoding="utf-8")
    with pytest.raises(ValueError, match="exactly one"):
        css.extract_marked(victim.read_text(encoding="utf-8"), GATE)
    assert css.run_gate(fake, render=False) == EXPECTED_ERROR_CODE


def test_gate_wrapped_in_an_html_comment_fails():
    """A gate wrapped in an HTML comment is not loaded as instruction, so the
    extractor must not find it — the known negative for this instrument."""
    text = DA_SKILL.read_text(encoding="utf-8")
    region = marked_region(text)
    disabled = text.replace(region, "<!--\n" + region + "\n### (disabled)\n-->")
    assert disabled != text
    with pytest.raises(ValueError):  # noqa: PT011
        css.extract_marked(disabled, GATE)


def test_gate_wrapped_in_a_code_fence_fails():
    text = DA_SKILL.read_text(encoding="utf-8")
    region = marked_region(text)
    disabled = text.replace(region, "```text\n" + region + "\n```")
    assert disabled != text
    with pytest.raises(ValueError):  # noqa: PT011
        css.extract_marked(disabled, GATE)


def test_unclosed_comment_before_the_gate_fails():
    """CommonMark: an HTML comment opened and never closed runs to end of
    document, so everything after `<!--` is hidden from a reader."""
    text = DA_SKILL.read_text(encoding="utf-8")
    region = marked_region(text)
    disabled = text.replace(region, "<!--\n" + region)
    assert disabled != text
    with pytest.raises(ValueError):  # noqa: PT011
        css.extract_marked(disabled, GATE)


def test_fence_closer_with_info_string_keeps_the_gate_hidden():
    """A closer carrying an info string does not close the fence, so the gate
    below it stays fenced and invisible."""
    text = DA_SKILL.read_text(encoding="utf-8")
    region = marked_region(text)
    disabled = text.replace(region, "```text\n```python\n" + region + "\n```")
    assert disabled != text
    with pytest.raises(ValueError):  # noqa: PT011
        css.extract_marked(disabled, GATE)


def test_comment_opener_inside_a_fence_does_not_hide_the_gate():
    text = DA_SKILL.read_text(encoding="utf-8")
    block = css.extract_marked(text, GATE)
    decoy = "```text\n<!--\n```\n\n"
    assert css.extract_marked(decoy + text, GATE) == block


def test_render_writes_nothing_when_any_carrier_is_broken(tmp_path):
    """A half-applied render is worse than none, so a fault in one carrier
    must abort before the others are written."""
    fake = make_fake_repo(tmp_path)
    drifted = fake / "skills" / "hypothesis-driven-analysis" / "SKILL.md"
    before = drifted.read_text(encoding="utf-8")
    drifted.write_text(
        before.replace(
            "Authorization is affirmative and specific to the action;",
            "Authorization is affirmative and specific to the actions;",
        ),
        encoding="utf-8",
    )
    after_drift = drifted.read_text(encoding="utf-8")
    broken = fake / "skills" / "decision-analysis" / "SKILL.md"  # last carrier
    broken.write_text(
        broken.read_text(encoding="utf-8").replace(GATE_OPEN + "\n", ""), encoding="utf-8"
    )
    assert css.run_gate(fake, render=True) == EXPECTED_ERROR_CODE
    assert drifted.read_text(encoding="utf-8") == after_drift


@pytest.mark.parametrize(
    ("prefix", "suffix"),
    [("```text\n", "```\n"), ("<!--\n", "-->\n")],
    ids=["fenced", "commented"],
)
def test_a_hidden_authority_fails_both_check_and_render(tmp_path, capsys, prefix, suffix):
    """The visibility rule guards the authority too, or it guards nothing.

    Hiding the authority body leaves every carrier's markers visible and every
    rendered block equal to it byte for byte, so nothing else in the checker
    notices — while all four skills now carry the gate as sample text. Render
    is how that damage gets written and check is how it should be caught, so
    neither path may accept it.
    """
    fake = make_fake_repo(tmp_path)
    authority = fake / css.GATE_AUTHORITY
    authority.write_text(prefix + authority.read_text(encoding="utf-8") + suffix, encoding="utf-8")
    before = {
        skill: (fake / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        for skill in css.GATE_CARRIERS
    }
    assert css.run_gate(fake, render=True) == EXPECTED_ERROR_CODE
    assert css.run_gate(fake, render=False) == EXPECTED_ERROR_CODE
    err = capsys.readouterr().err
    assert css.GATE_AUTHORITY in err
    for skill, text in before.items():
        assert (fake / "skills" / skill / "SKILL.md").read_text(encoding="utf-8") == text, skill
