"""Tests for check-citations.py.

Run: uv run --with pytest pytest scripts/test_check_citations.py

The point of these is the known-positive discipline the skills in this repo
preach: a checker that reports nothing and a checker that cannot report
anything look identical from the outside. Each rule here has a case that must
fail and a case that must pass.
"""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "check_citations", Path(__file__).parent / "check-citations.py"
)
assert SPEC is not None
assert SPEC.loader is not None
cc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cc)

SENTENCE = "An absent record does not by itself establish the absence of the event."


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A miniature skill tree rooted at tmp_path, with cc pointed at it."""
    (tmp_path / "skill" / "tests" / "runs").mkdir(parents=True)
    (tmp_path / "skill" / "SKILL.md").write_text(f"# Skill\n\n## Analysis\n\n{SENTENCE}\n")
    (tmp_path / "skill" / "tests" / "runs" / "archive.md").write_text("frozen evidence\n")
    monkeypatch.setattr(cc, "REPO_ROOT", tmp_path)
    return tmp_path


def write(repo: Path, text: str) -> Path:
    path = repo / "skill" / "tests" / "scenarios.md"
    path.write_text(text + "\n")
    return path


def test_line_citation_into_live_file_is_flagged(repo):
    violations = cc.check(write(repo, "See SKILL.md line 164 for the rule."))
    assert len(violations) == 1
    assert "line-number citation" in violations[0]


def test_line_citation_colon_form_is_flagged(repo):
    assert cc.check(write(repo, "See SKILL.md:164 for the rule."))


def test_line_citation_into_frozen_archive_is_allowed(repo):
    assert cc.check(write(repo, "Measured in archive.md:253 and :257.")) == []


def test_frozen_match_is_segment_wise_not_substring(repo):
    """`nottests/runs/` contains the string "tests/runs/" without being one."""
    decoy = repo / "skill" / "nottests" / "runs"
    decoy.mkdir(parents=True)
    (decoy / "decoy.md").write_text("not an archive\n")
    assert not cc.in_frozen(decoy / "decoy.md")
    assert cc.in_frozen(repo / "skill" / "tests" / "runs" / "archive.md")
    assert cc.check(write(repo, "See decoy.md:12 for the rule."))


def test_attributed_quote_that_matches_passes(repo):
    assert cc.check(write(repo, f'SKILL.md\'s "{SENTENCE}" governs this.')) == []


def test_attributed_quote_that_does_not_match_is_flagged(repo):
    stale = "An absent record proves the event did not happen, which is what we assumed."
    violations = cc.check(write(repo, f'SKILL.md\'s "{stale}" governs this.'))
    assert len(violations) == 1
    assert "does not appear there" in violations[0]


def test_unattributed_quote_is_ignored(repo):
    """A filename far from the quote is a mention, not a citation."""
    stale = "An absent record proves the event did not happen, which is what we assumed."
    line = f'The run read SKILL.md and then wrote, in its own words, "{stale}"'
    assert cc.check(write(repo, line)) == []


def test_short_quote_is_ignored(repo):
    assert cc.check(write(repo, 'SKILL.md\'s "not in there" is short.')) == []


def test_quote_matches_across_reflowed_whitespace_and_dashes(repo):
    (repo / "skill" / "SKILL.md").write_text("# Skill\n\nThe rule — stated once —\nspans lines.\n")
    assert cc.check(write(repo, 'SKILL.md\'s "the rule - stated once - spans lines" holds.')) == []


class TestPinnedCitations:
    """A pin is checked against git, not trusted."""

    @pytest.fixture
    def pinned(self, repo):
        run = lambda *a: subprocess.run(  # noqa: E731
            ["git", "-C", str(repo), *a], check=True, capture_output=True, text=True
        )
        run("init", "-q")
        run("config", "user.email", "t@example.com")
        run("config", "user.name", "T")
        run("add", "-A")
        run("commit", "-qm", "initial")
        sha = run("rev-parse", "--short", "HEAD").stdout.strip()
        (repo / "skill" / "SKILL.md").write_text("# Skill\n\nThe rule was rewritten entirely.\n")
        return repo, sha

    def test_quote_stale_in_working_tree_passes_when_pinned(self, pinned):
        repo, sha = pinned
        assert cc.check(write(repo, f'SKILL.md@{sha}\'s "{SENTENCE}" was the wording then.')) == []

    def test_same_quote_without_the_pin_is_flagged(self, pinned):
        """The known positive: the pin is what makes the passing case pass."""
        repo, _ = pinned
        assert cc.check(write(repo, f'SKILL.md\'s "{SENTENCE}" was the wording then.'))

    def test_quote_absent_from_the_pinned_commit_is_flagged(self, pinned):
        repo, sha = pinned
        never = "A sentence that no commit of this file has ever contained anywhere."
        violations = cc.check(write(repo, f'SKILL.md@{sha}\'s "{never}" was the wording.'))
        assert len(violations) == 1
        assert "does not appear there" in violations[0]

    def test_unresolvable_pin_is_flagged_once(self, pinned):
        """One violation, not two.

        A pin git cannot resolve means the quote was never checked; also
        reporting it as absent would describe a comparison that never ran.
        """
        repo, _ = pinned
        violations = cc.check(write(repo, f'SKILL.md@abc1234\'s "{SENTENCE}" was the wording.'))
        assert len(violations) == 1
        assert "git cannot resolve" in violations[0]


def test_in_scope_accepts_a_multi_segment_scope_root(tmp_path, monkeypatch):
    """A scope root several directories deep must still match.

    Comparing only the first path segment matched nothing once the skills moved
    under `skills/`, and every file was filtered out while the check still
    exited 0 — a silent pass indistinguishable from a clean run.
    """
    root = tmp_path
    target = root / "skills" / "hypothesis-driven-analysis" / "SKILL.md"
    target.parent.mkdir(parents=True)
    target.write_text("# skill\n")

    monkeypatch.setattr(cc, "REPO_ROOT", root)
    monkeypatch.setattr(cc, "DEFAULT_SCOPE", ("skills/hypothesis-driven-analysis",))

    assert cc.in_scope(target)


def test_in_scope_rejects_a_file_outside_the_scope_root(tmp_path, monkeypatch):
    """The instrument can also say no, so the test above cannot pass vacuously."""
    root = tmp_path
    outside = root / "skills" / "some-other-skill" / "SKILL.md"
    outside.parent.mkdir(parents=True)
    outside.write_text("# skill\n")

    monkeypatch.setattr(cc, "REPO_ROOT", root)
    monkeypatch.setattr(cc, "DEFAULT_SCOPE", ("skills/hypothesis-driven-analysis",))

    assert not cc.in_scope(outside)


class TestCausalIdentificationReviewScope:
    """causal-identification-review joined DEFAULT_SCOPE on 2026-08-09.

    The prek hook's `files` regex was extended to this skill's paths earlier,
    but the module's own DEFAULT_SCOPE was not — so the hook handed the files
    over and the checker skipped every one ("NOT checked, and this is not a
    pass") while still exiting 0, green-lighting files it never read. These
    tests use the real DEFAULT_SCOPE, not a monkeypatched one, so they pin
    the shipped scope; the planted failure is the known positive that proves
    the newly-scoped files are actually read.
    """

    @pytest.fixture
    def cir_repo(self, tmp_path, monkeypatch):
        root = tmp_path / "skills" / "causal-identification-review"
        (root / "tests").mkdir(parents=True)
        (root / "SKILL.md").write_text(f"# Skill\n\n{SENTENCE}\n")
        monkeypatch.setattr(cc, "REPO_ROOT", tmp_path)
        return tmp_path

    def test_default_scope_names_the_skill(self):
        assert "skills/causal-identification-review" in cc.DEFAULT_SCOPE

    def test_cir_scenarios_file_is_in_scope(self, cir_repo):
        path = cir_repo / "skills" / "causal-identification-review" / "tests" / "scenarios.md"
        path.write_text("catalog\n")
        assert cc.in_scope(path)

    def test_cir_planted_bad_citation_fails(self, cir_repo):
        """Known positive: a CIR-scoped file with a stale attributed quote FAILS."""
        path = cir_repo / "skills" / "causal-identification-review" / "tests" / "scenarios.md"
        stale = "An absent record proves the event did not happen, which is what we assumed."
        path.write_text(f'SKILL.md\'s "{stale}" governs this catalog.\n')
        assert cc.in_scope(path)
        violations = cc.check(path)
        assert len(violations) == 1
        assert "does not appear there" in violations[0]

    def test_cir_resolving_citation_passes(self, cir_repo):
        path = cir_repo / "skills" / "causal-identification-review" / "tests" / "scenarios.md"
        path.write_text(f'SKILL.md\'s "{SENTENCE}" governs this catalog.\n')
        assert cc.in_scope(path)
        assert cc.check(path) == []
