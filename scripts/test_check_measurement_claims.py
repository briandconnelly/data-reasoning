"""Tests for scripts/check-measurement-claims.py."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent


def _load(name: str, path: Path):
    # Register before exec: a @dataclass under `from __future__ import
    # annotations` resolves its module through sys.modules at class-creation
    # time and raises AttributeError when the entry is missing.
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mc = _load("check_measurement_claims", SCRIPTS / "check-measurement-claims.py")

WIDENING = "skills/exploratory-data-analysis/tests/runs/artifacts/2026-08-15-widening"
EDA_GOLDEN = "9a4e874b8af2220d1faa26d4a958a6e687439f44f49195b9abb64daef426e80d"
EDA_AT_4EFDEEC = "7fc858af152f80129bfa2840e534ec2e657c4fec61767bd7e244c34420fb9e6a"

GOOD_ENTRY = f"""
[eda-widening-2026-08-15]
skill = "exploratory-data-analysis"
artifact = "{WIDENING}/seam-gate4.md"
source = "sha256:{EDA_GOLDEN}"
anchor = "the sha256 of the rstripped C3 text"
covers = ["{WIDENING}/seam"]
"""

ANNOT = (
    "`[measured: skill=exploratory-data-analysis state=current evidence=eda-widening-2026-08-15]`"
)

# Line numbers for fencing tests
FENCE_COMMENT_HIDDEN_LINE = 3
FENCE_COMMENT_TAIL_LINE = 5
FENCE_BACKTICK_HIDDEN_LINE = 4
FENCE_BACKTICK_VISIBLE_LINE = 6


def _registry(tmp_path: Path, body: str) -> dict:
    reg = tmp_path / "measured-descriptions.toml"
    reg.write_text(body, encoding="utf-8")
    return mc.parse_registry(reg)


def test_annotation_regex_parses_trailing_backticked_form():
    m = mc.ANNOTATION.search(f"Claim text. {ANNOT}")
    assert m is not None
    assert m.group(1) == "exploratory-data-analysis"
    assert m.group(2) == "current"
    assert m.group(3) == "eda-widening-2026-08-15"


def test_annotation_regex_allows_trailing_whitespace_only():
    assert mc.ANNOTATION.search(f"Claim. {ANNOT}   ") is not None
    assert mc.ANNOTATION.search(f"Claim. {ANNOT} and more prose") is None
    assert mc.ANNOTATION.search(f"Claim. {ANNOT.strip('`')}") is None


def test_registry_parses_entry(tmp_path):
    entries = _registry(tmp_path, GOOD_ENTRY)
    e = entries["eda-widening-2026-08-15"]
    assert e.skill == "exploratory-data-analysis"
    assert e.source == ("sha256", EDA_GOLDEN)
    assert e.covers == (f"{WIDENING}/seam",)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (("exploratory-data-analysis", "no-such-skill"), "unknown skill"),
        (("sha256:", "md5:"), "source"),
        ((f'artifact = "{WIDENING}', 'artifact = "/abs'), "repo-relative"),
        ((f'artifact = "{WIDENING}', 'artifact = "../x'), "repo-relative"),
        ((f'covers = ["{WIDENING}/seam"]', 'covers = "not-a-list"'), "covers"),
        (('anchor = "the sha256 of the rstripped C3 text"', 'anchor = ""'), "anchor"),
    ],
)
def test_registry_rejects_malformed_entries(tmp_path, mutation, message):
    old, new = mutation
    with pytest.raises(mc.RegistryError, match=message):
        _registry(tmp_path, GOOD_ENTRY.replace(old, new))


def test_registry_rejects_non_hex_git_source(tmp_path):
    with pytest.raises(mc.RegistryError, match="git"):
        _registry(tmp_path, GOOD_ENTRY.replace(f"sha256:{EDA_GOLDEN}", "git:main"))


def test_unknown_evidence_key_is_violation(tmp_path):
    entries = _registry(tmp_path, GOOD_ENTRY)
    lines = [(3, ANNOT.replace("eda-widening-2026-08-15", "nope"))]
    violations = mc.check_annotations(Path("f.md"), lines, entries)
    assert len(violations) == 1
    assert "R1" in violations[0]
    assert "nope" in violations[0]


def test_skill_mismatch_with_entry_is_violation(tmp_path):
    entries = _registry(tmp_path, GOOD_ENTRY)
    lines = [(3, ANNOT.replace("exploratory-data-analysis", "hypothesis-driven-analysis"))]
    violations = mc.check_annotations(Path("f.md"), lines, entries)
    assert len(violations) == 1
    assert "R1" in violations[0]


def test_malformed_or_misplaced_annotation_is_violation(tmp_path):
    entries = _registry(tmp_path, GOOD_ENTRY)
    lines = [
        (3, "Claim. `[measured: skill=exploratory-data-analysis evidence=x]`"),
        (4, f"Claim. {ANNOT} trailing prose"),
    ]
    violations = mc.check_annotations(Path("f.md"), lines, entries)
    assert len(violations) == 2  # noqa: PLR2004
    assert all("R1" in v for v in violations)


def test_visible_lines_strips_fences_and_comments():
    text = (
        "one\n"
        "```toml\n"
        "[measured: skill=x state=current evidence=y]\n"
        "```\n"
        "two <!-- hidden [measured: skill=x state=current evidence=y] --> tail\n"
        "three\n"
    )
    numbered = dict(mc.visible_lines(text))
    assert numbered[1] == "one"
    assert FENCE_COMMENT_HIDDEN_LINE not in numbered
    assert "hidden" not in numbered[FENCE_COMMENT_TAIL_LINE]
    assert "tail" in numbered[FENCE_COMMENT_TAIL_LINE]
    assert numbered[6] == "three"


def test_visible_lines_multiline_html_comment_keeps_numbering():
    text = "a\n<!--\n[measured: skill=x state=current evidence=y]\n-->\nb\n"
    numbered = dict(mc.visible_lines(text))
    assert numbered[1] == "a"
    assert "[measured:" not in numbered.get(3, "")
    assert numbered[5] == "b"


def test_visible_lines_unclosed_html_comment_hides_to_eof():  # [review]
    text = "a\n<!-- never closed\n[measured: skill=x state=current evidence=y]\n"
    joined = "\n".join(line for _, line in mc.visible_lines(text))
    assert "[measured:" not in joined
    assert "a" in joined


def test_visible_lines_fence_tracks_opener_char_and_length():  # [review]
    text = (
        "````\n"
        "~~~ not a closer for a backtick fence\n"
        "``` not a closer either: shorter than the opener\n"
        "[measured: skill=x state=current evidence=y] still fenced\n"
        "````\n"
        "visible [measured: skill=x state=current evidence=y]\n"
    )
    numbered = dict(mc.visible_lines(text))
    assert FENCE_BACKTICK_HIDDEN_LINE not in numbered
    assert FENCE_BACKTICK_VISIBLE_LINE in numbered


def test_visible_lines_indented_code_is_not_a_fence():  # [review]
    text = "    ```\nvisible\n    ```\n"
    numbered = dict(mc.visible_lines(text))
    assert numbered[2] == "visible"


def test_check_registry_flags_missing_artifact(tmp_path):
    entries = _registry(
        tmp_path,
        GOOD_ENTRY.replace(f"{WIDENING}/seam-gate4.md", f"{WIDENING}/does-not-exist.md"),
    )
    violations = mc.check_registry(entries, referenced={"eda-widening-2026-08-15"})
    assert any("R2" in v and "does-not-exist.md" in v for v in violations)


def test_check_registry_flags_anchor_not_in_artifact(tmp_path):
    entries = _registry(
        tmp_path,
        GOOD_ENTRY.replace("the sha256 of the rstripped C3 text", "no such sentence anywhere"),
    )
    violations = mc.check_registry(entries, referenced={"eda-widening-2026-08-15"})
    assert any("R2" in v and "anchor" in v for v in violations)


def test_check_registry_accepts_real_anchor(tmp_path):
    entries = _registry(tmp_path, GOOD_ENTRY)
    assert mc.check_registry(entries, referenced={"eda-widening-2026-08-15"}) == []


def test_check_registry_flags_dead_entry(tmp_path):
    entries = _registry(tmp_path, GOOD_ENTRY)
    violations = mc.check_registry(entries, referenced=set())
    assert any("R2" in v and "no claim references" in v for v in violations)


def _entry(source: str) -> mc.Entry:
    form, _, value = source.partition(":")
    return mc.Entry(
        key="k",
        skill="exploratory-data-analysis",
        artifact=f"{WIDENING}/seam-gate4.md",
        source=(form, value),
        anchor="x",
        covers=(),
    )


def test_desc_hash_rstrips():
    assert mc.desc_hash("abc\n") == mc.desc_hash("abc")


def test_golden_hash_matches_known_value():
    assert mc.golden_hash("exploratory-data-analysis") == EDA_GOLDEN


def test_frontmatter_description_parity_with_freeze_checker():
    freeze = _load("check_description_freeze", SCRIPTS / "check-description-freeze.py")
    for skill in mc.SKILLS:
        skill_md = mc.REPO_ROOT / "skills" / skill / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        assert mc.frontmatter_description(text) == freeze.read_description(skill_md)


def test_frontmatter_description_without_frontmatter_raises():
    with pytest.raises(mc.SourceError, match="frontmatter"):
        mc.frontmatter_description("# no frontmatter\n")


def test_resolve_sha256_source_is_identity():
    assert mc.resolve_source(_entry(f"sha256:{EDA_GOLDEN}")) == EDA_GOLDEN


def test_resolve_file_source_hashes_frozen_file():
    frozen = "skills/exploratory-data-analysis/tests/eval/frozen-2026-08-15-C3.txt"
    assert mc.resolve_source(_entry(f"file:{frozen}")) == EDA_GOLDEN


def test_resolve_git_source_reads_description_at_commit():
    assert mc.resolve_source(_entry("git:4efdeec")) == EDA_AT_4EFDEEC


def test_resolve_git_source_unresolvable_raises():
    with pytest.raises(mc.SourceError, match="cannot be resolved"):
        mc.resolve_source(_entry("git:0000000000000000000000000000000000000000"))


def test_resolve_git_source_in_shallow_clone_names_the_cause(monkeypatch):  # [review]
    monkeypatch.setattr(mc, "shallow", lambda: True)
    with pytest.raises(mc.SourceError, match="shallow clone"):
        mc.resolve_source(_entry("git:0000000000000000000000000000000000000000"))


def test_state_current_requires_golden_match():
    violations = mc.check_state(Path("f.md"), 3, "current", _entry("git:4efdeec"))
    assert any("R3" in v and "state=current" in v for v in violations)
    assert mc.check_state(Path("f.md"), 3, "current", _entry(f"sha256:{EDA_GOLDEN}")) == []


def test_state_historical_requires_golden_mismatch():
    violations = mc.check_state(Path("f.md"), 3, "historical", _entry(f"sha256:{EDA_GOLDEN}"))
    assert any("R3" in v and "state=historical" in v for v in violations)
    assert mc.check_state(Path("f.md"), 3, "historical", _entry("git:4efdeec")) == []


TRIGGER_ARTIFACT = (
    "skills/exploratory-data-analysis/tests/runs/artifacts/"
    "2026-08-11-t13-t14-trigger-harness-evidence.md"
)
TWO_ENTRIES = (
    GOOD_ENTRY
    + f"""
[eda-trigger-2026-08-11]
skill = "exploratory-data-analysis"
artifact = "{TRIGGER_ARTIFACT}"
source = "git:4efdeec"
anchor = "repo at `4efdeec` throughout"
covers = [
  "skills/exploratory-data-analysis/tests/runs/2026-08-11-t13-trigger.md",
  "skills/exploratory-data-analysis/tests/runs/2026-08-11-t14-trigger.md",
]
"""
)


def _line_rules(tmp_path, line):
    entries = _registry(tmp_path, TWO_ENTRIES)
    return mc.check_line_rules(Path("f.md"), 7, line, entries)


def test_lint_unbound_claim_fails(tmp_path):
    violations, _ = _line_rules(
        tmp_path, "`seam-gate4.md` is a measured arm for the shipped description."
    )
    assert any("R4" in v and "unbound" in v for v in violations)


def test_lint_bound_claim_passes(tmp_path):
    violations, refs = _line_rules(
        tmp_path, f"`seam-gate4.md` is a measured arm for the shipped description. {ANNOT}"
    )
    assert violations == []
    assert refs == {"eda-widening-2026-08-15"}


@pytest.mark.parametrize(
    "verb_phrase",
    ["measured", "measures", "re-validated against", "ran against", "rerun against", "arms for"],
)
def test_lint_vocabulary(tmp_path, verb_phrase):
    violations, _ = _line_rules(tmp_path, f"`seam-gate4.md` {verb_phrase} the description.")
    assert any("R4" in v for v in violations)


def test_lint_directory_mention_counts(tmp_path):
    violations, _ = _line_rules(
        tmp_path,
        "the description's measured arms are in `tests/runs/artifacts/2026-08-15-widening/`.",
    )
    assert any("R4" in v for v in violations)


def test_lint_ignores_line_without_description_word(tmp_path):
    violations, _ = _line_rules(tmp_path, "`seam-gate4.md` measured the seam routing.")
    assert violations == []


def test_lint_ignores_line_without_verb(tmp_path):
    violations, _ = _line_rules(tmp_path, "`seam-gate4.md` and the description are both mentioned.")
    assert violations == []


def test_two_annotations_on_one_line_fail(tmp_path):
    entries = _registry(tmp_path, TWO_ENTRIES)
    other = ANNOT.replace("eda-widening-2026-08-15", "eda-trigger-2026-08-11")
    line = f"claim one {ANNOT.rstrip('`')}` and claim two {other}"
    violations = mc.check_annotations(Path("f.md"), [(7, line)], entries)
    assert any("R1" in v for v in violations)


def test_two_skills_in_one_sentence_need_two_lines(tmp_path):  # [review]
    line = (
        "`tests/runs/2026-08-11-t13-trigger.md` measured both descriptions at 4efdeec. "
        + ANNOT.replace("eda-widening-2026-08-15", "eda-trigger-2026-08-11").replace(
            "state=current", "state=historical"
        )
    )
    violations, refs = _line_rules(tmp_path, line)
    # One annotation binds one skill; the sentence about the other skill has no
    # binding and the checker cannot see it. This test pins the documented
    # limit: the line passes R4/R5, and decision 007 is what requires the split.
    assert violations == []
    assert refs == {"eda-trigger-2026-08-11"}


def test_uncovered_mention_on_annotated_line_fails(tmp_path):
    violations, _ = _line_rules(
        tmp_path,
        "`seam-gate4.md` and `tests/runs/2026-08-11-t13-trigger.md` measured the "
        f"description. {ANNOT}",
    )
    assert any("R5" in v and "2026-08-11-t13-trigger.md" in v for v in violations)


def test_file_under_covered_directory_passes(tmp_path):
    violations, _ = _line_rules(
        tmp_path, f"`seam/t13-rep3.jsonl` and `seam-gate4.md` measured the description. {ANNOT}"
    )
    assert violations == []


def test_ancestor_directory_mention_is_not_covered(tmp_path):  # [review]
    violations, _ = _line_rules(
        tmp_path, f"the arms in `tests/runs/` measured the description. {ANNOT}"
    )
    assert any("R5" in v and "tests/runs" in v for v in violations)


def test_explicitly_covered_directory_mention_passes(tmp_path):
    violations, _ = _line_rules(
        tmp_path,
        f"the seam arms in `{WIDENING}/seam/` measured the description. {ANNOT}",
    )
    assert violations == []


def test_check_file_runs_all_line_rules(tmp_path):
    entries = _registry(tmp_path, GOOD_ENTRY)
    f = tmp_path / "claims.md"
    f.write_text(
        "Fine line.\n"
        "`seam-gate4.md` is a measured arm for the shipped description.\n"
        f"Bound: `seam-gate4.md` measured the description. {ANNOT}\n",
        encoding="utf-8",
    )
    violations, referenced = mc.check_file(f, entries)
    assert len(violations) == 1
    assert "R4" in violations[0]
    assert ":2:" in violations[0]
    assert referenced == {"eda-widening-2026-08-15"}


def test_check_file_ignores_fenced_annotations(tmp_path):
    entries = _registry(tmp_path, GOOD_ENTRY)
    f = tmp_path / "claims.md"
    f.write_text(
        "Example follows.\n```\n`x.md` measured the description. "
        "`[measured: skill=bad state=current evidence=bad]`\n```\n",
        encoding="utf-8",
    )
    violations, _ = mc.check_file(f, entries)
    assert violations == []


def test_in_scope_matches_citation_checker_classes():
    root = mc.REPO_ROOT
    eda = root / "skills/exploratory-data-analysis"
    assert mc.in_scope(eda / "decisions/006-description-freeze-until-measured.md")
    assert mc.in_scope(root / "skills/hypothesis-driven-analysis/tests/scenarios.md")
    assert not mc.in_scope(eda / "tests/runs/2026-08-11-t13-trigger.md")
    assert not mc.in_scope(root / "README.md")


def test_main_reports_out_of_scope_explicit_file(tmp_path, capsys):
    outside = tmp_path / "outside.md"
    outside.write_text("x\n", encoding="utf-8")
    rc = mc.main([str(outside)])
    err = capsys.readouterr().err
    assert rc == 0
    assert "NOT checked" in err


def _real_corpus_violations() -> list[str]:
    registry = mc.parse_registry(mc.REGISTRY_PATH)
    violations: list[str] = []
    referenced: set[str] = set()
    for target in mc.scope_files():
        v, refs = mc.check_file(target, registry)
        violations.extend(v)
        referenced.update(refs)
    violations.extend(mc.check_registry(registry, referenced))
    return violations


def test_real_corpus_is_clean():
    assert _real_corpus_violations() == []


def test_known_positive_the_original_false_claim_bound_honestly_fails(tmp_path):
    """The claim from b4e9d535, bound to the arms' true evidence with the
    currency it asserted, must fail R3."""
    registry = mc.parse_registry(mc.REGISTRY_PATH)
    f = tmp_path / "decision.md"
    f.write_text(
        "`tests/runs/2026-08-11-t13-trigger.md` and `2026-08-11-t14-trigger.md` are measured "
        "trigger arms for the description decision 005 adopted. "
        "`[measured: skill=exploratory-data-analysis "
        "state=current evidence=eda-trigger-2026-08-11]`\n",
        encoding="utf-8",
    )
    violations, _ = mc.check_file(f, registry)
    assert any("R3" in v and "state=current" in v for v in violations)


def test_known_positive_the_original_false_claim_unbound_fails(tmp_path):
    registry = mc.parse_registry(mc.REGISTRY_PATH)
    f = tmp_path / "decision.md"
    f.write_text(
        "`tests/runs/2026-08-11-t13-trigger.md` and `2026-08-11-t14-trigger.md` are measured "
        "trigger arms for the description decision 005 adopted.\n",
        encoding="utf-8",
    )
    violations, _ = mc.check_file(f, registry)
    assert any("R4" in v for v in violations)
