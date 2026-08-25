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
