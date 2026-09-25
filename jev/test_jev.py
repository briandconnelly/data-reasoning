"""Tests for the optional Jev tooling.

Run: uv run --with pytest pytest jev

Offline tests use a fake transport, so they check plumbing, parsing, and
labelling, never Jev's judgment. The `live` tests at the bottom ask Jev real
questions with known answers and skip without TYPESAFE_API_KEY; a skip is not
a pass, so run them with the key before trusting a change to a question.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import grade  # noqa: E402
import jev_client  # noqa: E402
import route  # noqa: E402
import semantic_check  # noqa: E402

REPO = HERE.parent
S22 = (
    REPO / "skills/hypothesis-driven-analysis/tests/runs/artifacts/2026-09-20-cheap-route-validity"
)
S15_FINAL = S22 / "s15-post.scratch/ledger.md"
S15_PLAN = S22 / "s15-scoring/s15-post.plan-ledger.md"
live = pytest.mark.skipif(not jev_client.available(), reason="TYPESAFE_API_KEY not set")


def fake(answers: dict[str, dict[str, Any]], seen: list[dict[str, Any]] | None = None):
    def transport(body: dict[str, Any]) -> dict[str, Any]:
        if seen is not None:
            seen.append(body)
        return {
            "model": "jev-fake",
            "answers": {k: answers[k] for k in body["questions"]},
            "usage": {"input_tokens": 1},
        }

    return transport


def noul(p: float) -> dict[str, Any]:
    return {"type": "noul", "noul": p}


# --- client ---------------------------------------------------------------


def test_no_key_is_unavailable_not_a_pass(monkeypatch):
    monkeypatch.delenv(jev_client.KEY_VAR, raising=False)
    with pytest.raises(jev_client.JevUnavailable):
        jev_client.evaluate("x", {"q": {"type": "noul", "instructions": "?"}})


def test_missing_answer_is_unavailable():
    with pytest.raises(jev_client.JevUnavailable):
        jev_client.evaluate("x", {"a": {}, "b": {}}, transport=lambda _b: {"answers": {"a": {}}})


def test_probability_of_pass():
    hi, lo = 0.7, 0.3
    assert jev_client.probability_of_pass(noul(hi)) == hi
    choice = {"type": "choice", "choice": "b", "probabilities": {"a": lo, "b": hi}}
    assert jev_client.probability_of_pass(choice, "a") == lo
    with pytest.raises(ValueError, match="pass option"):
        jev_client.probability_of_pass(choice)
    with pytest.raises(ValueError, match="score"):
        jev_client.probability_of_pass({"type": "score", "score": 1.0})


def test_missing_pass_option_probability_is_unavailable_not_fail():
    choice = {"type": "choice", "choice": "b", "probabilities": {"b": 1.0}}
    with pytest.raises(jev_client.JevUnavailable):
        jev_client.probability_of_pass(choice, "a")


def test_model_is_pinned_not_aliased():
    assert jev_client.MODEL != "jev-latest"
    seen: list[dict[str, Any]] = []
    jev_client.evaluate("x", {"q": {}}, transport=fake({"q": noul(1)}, seen))
    assert seen[0]["model"] == jev_client.MODEL


# --- grade ----------------------------------------------------------------


@pytest.mark.parametrize(
    ("p", "expected"), [(0.39, "fail"), (0.4, "abstain"), (0.6, "abstain"), (0.61, "pass")]
)
def test_label_band_edges(p, expected):
    assert grade.label(p, (0.4, 0.6)) == expected


def test_status():
    assert grade.status("pass", True) == "agree"
    assert grade.status("pass", False) == "disagree"
    assert grade.status("fail", False) == "agree"
    assert grade.status("abstain", True) == "abstain"
    assert grade.status("pass", None) == "unreferenced"


def write_arm(d: Path, arm: str, result: str, files: dict[str, str]) -> None:
    events = [{"type": "system"}, {"type": "result", "result": result}]
    (d / f"{arm}.jsonl").write_text("\n".join(json.dumps(e) for e in events) + "\n")
    (d / f"{arm}.prompt.txt").write_text("the task")
    scratch = d / f"{arm}.scratch"
    scratch.mkdir()
    for name, body in files.items():
        (scratch / name).write_text(body)


def wave_file(tmp_path: Path, arms: list[dict], **extra) -> Path:
    wave = {
        "title": "t",
        "abstain_band": [0.4, 0.6],
        "reference_scorer": "a named scorer",
        "items": {
            "i1": {"question": {"type": "noul", "instructions": "?"}},
            "i2": {"question": {"type": "noul", "instructions": "?"}},
        },
        "arms": arms,
        **extra,
    }
    path = tmp_path / "wave.json"
    path.write_text(json.dumps(wave))
    return path


def test_arm_state_reads_final_result_and_scratch(tmp_path):
    write_arm(tmp_path, "a1", "the answer", {"ledger.md": "L", "day-01.out": "42"})
    (tmp_path / "a1.scratch" / "blob.bin").write_bytes(b"\xff\xfe\x00binary")
    state = grade.arm_state(tmp_path, "a1")
    assert state == {
        "user_prompt": "the task",
        "final_answer": "the answer",
        "files_written": {"day-01.out": "42", "ledger.md": "L"},
    }


def test_redaction_blinds_every_field(tmp_path):
    write_arm(tmp_path, "a1", "see /tmp/arm-s2-pre-x1/work", {"arm-s2-pre-x1.md": "arm-s2-pre-x1"})
    state = grade.redacted(grade.arm_state(tmp_path, "a1"), [[r"arm-[\w-]+", "arm-run"]])
    assert "pre" not in json.dumps(state)
    assert state["files_written"] == {"arm-run.md": "arm-run"}


def test_grade_sends_the_redacted_state(tmp_path, monkeypatch):
    monkeypatch.setattr(grade, "REPO", tmp_path)
    write_arm(tmp_path, "a1", "arm-s2-pre-x1", {})
    arms = [{"dir": ".", "arm": "a1", "items": {"i1": True}}]
    wave = grade.load_wave(wave_file(tmp_path, arms, redact=[[r"arm-[\w-]+", "arm-run"]]))
    seen: list[dict[str, Any]] = []
    grade.grade(wave, transport=fake({"i1": noul(0.9)}, seen))
    assert seen[0]["state"]["final_answer"] == "arm-run"


def test_load_wave_refuses_unnamed_reference_scorer(tmp_path):
    arms = [{"dir": "x", "arm": "a1", "items": {"i1": True}}]
    path = wave_file(tmp_path, arms, reference_scorer=None)
    with pytest.raises(ValueError, match="who scored"):
        grade.load_wave(path)


def test_control_only_wave_needs_no_reference_scorer(tmp_path):
    arms = [{"dir": "x", "arm": "a1", "kind": "control", "items": {"i1": False}}]
    assert grade.load_wave(wave_file(tmp_path, arms, reference_scorer=None))


def test_load_wave_refuses_band_not_straddling_half(tmp_path):
    path = wave_file(tmp_path, [], abstain_band=[0.6, 0.8])
    with pytest.raises(ValueError, match="straddle"):
        grade.load_wave(path)


def test_grade_counts_each_status(tmp_path, monkeypatch):
    monkeypatch.setattr(grade, "REPO", tmp_path)
    write_arm(tmp_path, "a1", "ok", {})
    write_arm(tmp_path, "a2", "ok", {})
    arms = [
        {"dir": ".", "arm": "a1", "items": {"i1": True, "i2": True}},
        {"dir": ".", "arm": "a2", "items": {"i1": False, "i2": None}},
    ]
    wave = grade.load_wave(wave_file(tmp_path, arms))
    report = grade.grade(wave, transport=fake({"i1": noul(0.9), "i2": noul(0.5)}))
    assert report["counts"] == {"reference": {"agree": 1, "abstain": 2, "disagree": 1}}
    assert report["models"] == ["jev-fake"]
    assert "| a2 | i1 | reference | FAIL | 0.9 | disagree |" in grade.render(report)


def test_controls_are_counted_apart(tmp_path, monkeypatch):
    monkeypatch.setattr(grade, "REPO", tmp_path)
    write_arm(tmp_path, "a1", "ok", {})
    arms = [
        {"dir": ".", "arm": "a1", "items": {"i1": True}},
        {"dir": ".", "arm": "a1", "kind": "control", "items": {"i2": False}},
    ]
    report = grade.grade(
        grade.load_wave(wave_file(tmp_path, arms)),
        transport=fake({"i1": noul(0.9), "i2": noul(0.1)}),
    )
    assert report["counts"] == {"reference": {"agree": 1}, "control": {"agree": 1}}


def test_oversize_state_is_not_checked(tmp_path, monkeypatch):
    monkeypatch.setattr(grade, "REPO", tmp_path)
    monkeypatch.setattr(grade, "MAX_STATE_CHARS", 10)
    write_arm(tmp_path, "a1", "a long answer", {})
    wave = grade.load_wave(wave_file(tmp_path, [{"dir": ".", "arm": "a1", "items": {"i1": True}}]))
    report = grade.grade(wave, transport=fake({}))
    assert report["counts"] == {"reference": {"not_checked": 1}}


def test_size_guard_counts_the_longest_question(tmp_path, monkeypatch):
    monkeypatch.setattr(grade, "REPO", tmp_path)
    write_arm(tmp_path, "a1", "ok", {})
    state_size = len(json.dumps(grade.arm_state(tmp_path, "a1")))
    monkeypatch.setattr(grade, "MAX_STATE_CHARS", state_size + 5)
    wave = grade.load_wave(wave_file(tmp_path, [{"dir": ".", "arm": "a1", "items": {"i1": True}}]))
    wave["items"]["i1"]["question"]["instructions"] = "x" * 50
    report = grade.grade(wave, transport=fake({"i1": noul(0.9)}))
    assert report["counts"] == {"reference": {"not_checked": 1}}


def test_main_exits_2_when_any_point_is_skipped(tmp_path, monkeypatch):
    monkeypatch.setattr(grade, "REPO", tmp_path)
    monkeypatch.setattr(grade, "MAX_STATE_CHARS", 10)
    monkeypatch.setattr(grade.jev_client, "_http_transport", fake({}))
    write_arm(tmp_path, "a1", "a long answer", {})
    path = wave_file(tmp_path, [{"dir": ".", "arm": "a1", "items": {"i1": True}}])
    out = tmp_path / "report.json"
    assert grade.main([str(path), "--out", str(out)]) == grade.EXIT_UNAVAILABLE
    assert json.loads(out.read_text())["counts"] == {"reference": {"not_checked": 1}}


def test_malformed_choice_answer_marks_only_that_point(tmp_path, monkeypatch):
    monkeypatch.setattr(grade, "REPO", tmp_path)
    write_arm(tmp_path, "a1", "ok", {})
    path = wave_file(tmp_path, [{"dir": ".", "arm": "a1", "items": {"i1": True, "i2": True}}])
    wave = grade.load_wave(path)
    wave["items"]["i2"] = {"question": {"type": "choice"}, "pass_option": "yes"}
    bad = {"type": "choice", "choice": "no", "probabilities": {"no": 1.0}}
    report = grade.grade(wave, transport=fake({"i1": noul(0.9), "i2": bad}))
    assert report["counts"] == {"reference": {"agree": 1, "not_checked": 1}}


def test_size_guard_counts_all_questions_together(tmp_path, monkeypatch):
    monkeypatch.setattr(grade, "REPO", tmp_path)
    write_arm(tmp_path, "a1", "ok", {})
    wave = grade.load_wave(
        wave_file(tmp_path, [{"dir": ".", "arm": "a1", "items": {"i1": True, "i2": True}}])
    )
    for item in ("i1", "i2"):
        wave["items"][item]["question"]["instructions"] = "x" * 40
    state_size = len(json.dumps(grade.arm_state(tmp_path, "a1")))
    one_question = len(json.dumps(wave["items"]["i1"]["question"]))
    # Each question fits beside the state on its own; the two together do not.
    monkeypatch.setattr(grade, "MAX_REQUEST_CHARS", state_size + one_question + 5)
    report = grade.grade(wave, transport=fake({"i1": noul(0.9), "i2": noul(0.9)}))
    assert report["counts"] == {"reference": {"not_checked": 2}}


def test_load_wave_refuses_an_arm_with_no_items(tmp_path):
    path = wave_file(tmp_path, [{"dir": ".", "arm": "a1", "items": {}}])
    with pytest.raises(ValueError, match="asks no items"):
        grade.load_wave(path)


def test_main_exits_2_when_unavailable(tmp_path, monkeypatch):
    monkeypatch.delenv(jev_client.KEY_VAR, raising=False)
    monkeypatch.setattr(grade, "REPO", tmp_path)
    write_arm(tmp_path, "a1", "ok", {})
    path = wave_file(tmp_path, [{"dir": ".", "arm": "a1", "items": {"i1": True}}])
    assert grade.main([str(path)]) == grade.EXIT_UNAVAILABLE


@pytest.mark.parametrize(
    "path", sorted(HERE.glob("*/*/wave.json")), ids=lambda p: str(p.relative_to(HERE))
)
def test_committed_wave_files_are_well_formed(path):
    wave = grade.load_wave(path)
    for arm in wave["arms"]:
        assert (REPO / arm["dir"] / f"{arm['arm']}.jsonl").is_file(), arm["arm"]


# --- route ----------------------------------------------------------------


def test_catalog_prompts_shapes():
    text = "\n".join(
        [
            "### A",
            '**Prompt:** "Why did X drop?"',
            "### B",
            "**Prompt** (verbatim):",
            "",
            "> first line",
            "> second line",
            "### C",
            "**Prompt:** as Scenario A, but with a hole.",
            "### D",
            "**Prompt S22a (mini):**",
            "",
            "> Is that true?",
        ]
    )
    assert route.catalog_prompts(text) == [
        ("A", "Why did X drop?"),
        ("B", "first line second line"),
        ("D", "Is that true?"),
    ]


def test_real_catalogs_yield_no_empty_or_marker_prompts():
    at_least = 50  # 60 standalone prompts on 2026-09-24; a parser regression drops far below
    total = 0
    for skill in route.SKILLS:
        prompts = route.catalog_prompts(
            (REPO / "skills" / skill / "tests/scenarios.md").read_text()
        )
        assert prompts, skill
        for _heading, prompt in prompts:
            assert prompt
            assert not prompt.startswith("**"), prompt
        total += len(prompts)
    assert total >= at_least


def routed(prompts: list[tuple[str, str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "id": route.prompt_id(c, p),
            "catalog": c,
            "scenario": h,
            "prompt": p,
            "choice": choice,
            "confidence": 0.9,
            "probabilities": {choice: 0.9},
            "model": "m",
        }
        for c, h, p, choice in [(*t[:3], t[3]) for t in prompts]
    ]


def test_route_labels_are_keyed_by_prompt_not_heading():
    rows = routed(
        [("c", "Scenario 22", "first prompt", "none"), ("c", "Scenario 22", "second prompt", "hda")]
    )
    assert rows[0]["id"] != rows[1]["id"]
    labels = {rows[0]["id"]: "none", rows[1]["id"]: "none"}
    assert "Labelled: 1/2 agree" in route.summarize(rows, labels)


def test_route_labels_naming_no_prompt_are_refused():
    rows = routed([("c", "Scenario 22", "first prompt", "none")])
    with pytest.raises(ValueError, match="name no current prompt"):
        route.summarize(rows, {"Scenario 22": "none"})


def test_route_reads_the_frozen_goldens():
    shortest_real = 100  # each golden is several sentences; an empty or stub read is shorter
    desc = route.frozen_descriptions()
    assert set(desc) == set(route.SKILLS)
    assert all(len(d) > shortest_real for d in desc.values())
    assert route.NONE_OPTION in route.route_question(desc)["criteria"]


# --- semantic check -------------------------------------------------------


def test_semantic_check_parses_a_real_ledger():
    hyps, stop = semantic_check.plan_time_states(S15_PLAN.read_text())
    assert [h["id"] for h in hyps] == ["H1", "H2", "H3", "H4", "H5"]
    assert stop


def test_semantic_check_sends_no_outcome_text():
    text = S15_FINAL.read_text()
    assert "REFUTED" in text  # the known positive: outcomes are in the file
    seen: list[dict[str, Any]] = []
    semantic_check.check(text, transport=fake({"follows": noul(0.9), "stop": noul(0.9)}, seen))
    sent = json.dumps([b["state"] for b in seen])
    for token in ("REFUTED", "CONSISTENT", "CONTRADICTED", "NON_DISCRIMINATING", "UNRESOLVED"):
        assert token not in sent


def test_semantic_check_rejects_non_ledger():
    with pytest.raises(ValueError, match="not a full-route ledger"):
        semantic_check.plan_time_states("# Notes\n\nnothing here\n")


def test_semantic_check_refuses_a_ledger_without_stop_condition():
    text = S15_PLAN.read_text()
    no_stop = "\n".join(ln for ln in text.splitlines() if "Stop condition" not in ln)
    with pytest.raises(ValueError, match="no Stop condition"):
        semantic_check.plan_time_states(no_stop)


def test_semantic_check_verdicts():
    assert semantic_check.verdict(0.2) == "flag"
    assert semantic_check.verdict(0.5) == "abstain"
    assert semantic_check.verdict(0.8) == "ok"


# --- live: real Jev answers with known correct values ---------------------

BAD_COLUMNS = [
    "id",
    "claim",
    "Candidate explanation",
    "Prediction if true",
    "Prediction if false",
    "Necessary prediction (failure refutes)",
    "Cheapest adequate test",
    "Data needed",
]
BAD_ROW = [
    "H1",
    "causal",
    "The 2026-06-01 pricing change deterred new signups.",
    "...",
    "...",
    "Mobile app crash rate rose in May.",
    "T1",
    "...",
]


def md_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


BAD_LEDGER = "\n".join(
    [
        "# Investigation: why did signups fall",
        "",
        "## Problem",
        "",
        "- Stop condition: stop as soon as one explanation is confirmed.",
        "",
        "## Hypotheses",
        "",
        md_row(BAD_COLUMNS),
        md_row(["---"] * len(BAD_COLUMNS)),
        md_row(BAD_ROW),
        "",
    ]
)


@pytest.fixture(scope="module")
def s15_verdicts() -> dict[str, str]:
    report = semantic_check.check(S15_PLAN.read_text())
    return {r["id"]: r["verdict"] for r in report["results"]}


# H3 and H4 were legitimately refuted in this arm (s15-scoring/scoring.md), and
# its stop condition is outcome-independent; each is its own test so a fix or
# a regression in one is visible on its own.
@live
def test_live_refuted_h3_is_not_flagged(s15_verdicts):
    assert s15_verdicts["H3"] != "flag"


@live
@pytest.mark.xfail(
    strict=True,
    reason="known false positive, 2026-09-24: jev-1.13.0 flags H4 (p~0.34), a data-artifact "
    "hypothesis both scorers accepted as legitimately refuted; see jev/README.md",
)
def test_live_refuted_h4_is_not_flagged(s15_verdicts):
    assert s15_verdicts["H4"] != "flag"


@live
@pytest.mark.xfail(
    strict=True,
    reason="known false positive, 2026-09-24: jev-1.13.0 flags the S15 stop condition "
    "(p~0.35), which fixes a decision criterion independent of the answer",
)
def test_live_s15_stop_condition_is_not_flagged(s15_verdicts):
    assert s15_verdicts["Problem"] != "flag"


@live
def test_live_bad_ledger_is_flagged():
    by_id = {r["id"]: r["verdict"] for r in semantic_check.check(BAD_LEDGER)["results"]}
    assert by_id["H1"] == "flag"
    assert by_id["Problem"] == "flag"


@live
def test_live_route_known_cases():
    q = {"route": route.route_question(route.frozen_descriptions())}
    why = jev_client.evaluate(
        {
            "request": "Weekly checkout conversion dropped from 3.1% to 2.5% week over week. "
            "Why? The events export is attached."
        },
        q,
    )
    lookup = jev_client.evaluate({"request": "What's the median order value in orders.csv?"}, q)
    assert why["answers"]["route"]["choice"] == "hypothesis-driven-analysis"
    assert lookup["answers"]["route"]["choice"] == route.NONE_OPTION


@live
def test_live_grade_controls():
    wave = grade.load_wave(HERE / "pilot/2026-09-24/wave.json")
    ctrl = {**wave, "arms": [a for a in wave["arms"] if a["arm"] in {"s22a-pre", "s22b-pre"}]}
    points = {(p["arm"], p["item"], p["kind"]): p for p in grade.grade(ctrl)["points"]}
    assert points[("s22a-pre", "S22a.3", "reference")]["jev"] == "pass"
    assert points[("s22b-pre", "S22a.3", "control")]["jev"] == "fail"
