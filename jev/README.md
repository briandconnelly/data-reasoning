# Jev grading aids (optional)

Development tooling that asks TypeSafe's Jev model narrow, typed questions about this repo's archived runs, catalog prompts, and ledgers.
It is optional: every tool needs `TYPESAFE_API_KEY`, and without it reports "not checked" and exits 2.
Nothing here ships: `jev/` is not on `scripts/build-release-tree.py`'s allowlist, and no skill, hook, or instrument imports it.
The code is stdlib-only and pins `jev-1.13.0` rather than the moving `jev-latest` alias.
Why this exists, and what was argued against it, is `skills/hypothesis-driven-analysis/decisions/009-jev-is-a-second-scorer.md`.

## Rules for using the output

This section is the one home of these rules; other files point here.

1. A Jev answer is never the only score for an assertion, and a Jev label is never cited as a measured result in a run record, a catalog, a decision record, or the README.
2. Every point Jev answers inside the abstain band, and every point where it disagrees with the reference label, goes to a person who reads the arm before deciding.
   Check the rubric text before blaming either scorer: a disagreement is as often an unwritten rule, or a lenient reference, as a Jev error.
3. Questions are frozen before anyone reads the reference labels or Jev's answers for the arms they will grade.
   A rewording after either is a new question set with its own result; the original result is kept, not replaced.
4. Reference labels name their scorer (`reference_scorer` in a wave file), and an agent scorer is named as one; an agreement rate against an agent scorer is agreement with that agent, not with a person.
5. "Not checked" — no key, no network, a missing answer, a state over Jev's budget — is never read as a pass.
6. Nothing here runs inside the plugin, its hook, or a skill, and no agent-read wording points an agent at it; wording that did would owe measured arms (`skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md`).
7. A change of model version is a new calibration: questions validated on one version are not evidence about the next.

## Tools

`grade.py` — a second scorer over archived arms.
A wave file (`pilot/2026-09-24/wave.json` is a worked example) names the frozen questions, the abstain band, each arm as `run_arm.py` archived it, and optionally the existing scorer's labels.
Each arm is sent as one state: the prompt, the final answer, and every text file the arm wrote.
The report lists agreements, disagreements, and abstentions, and prints the ones a person must read.
Arm entries marked `"kind": "control"` carry labels the wave's author constructed, such as a verdict question asked of an arm whose correct verdict differs, and are counted apart.

```bash
python3 jev/grade.py jev/pilot/2026-09-24/wave.json --out report.json
```

`route.py` — routes every standalone catalog prompt against the frozen descriptions in `scripts/frontmatter-descriptions/`, plus a "none of these" option, and lists the prompts Jev cannot place.
It measures whether a prompt's text separates the routes as the descriptions draw them.
It is Jev's routing, not the agent's, so it does not bear on the description freeze in `skills/exploratory-data-analysis/decisions/006-description-freeze-until-measured.md`; its use is choosing which prompts deserve real agent arms.
`--labels` scores agreement against a file mapping scenario headings to intended routes; no such file exists yet.

```bash
python3 jev/route.py --out routing.json
```

`semantic_check.py` — **experimental, not validated.**
For a full-route ledger it asks whether each hypothesis's necessary prediction follows from its candidate explanation, and whether the stop condition is fixed independently of the answer: the two questions decision 006 names as beyond structural checks.
Only Plan-time text is sent, so an outcome cannot move an answer.
On its one real known-negative — the S15 post arm's plan, whose H3 and H4 both scorers accepted as legitimately refuted — it flags H4 (p≈0.34) and the stop condition (p≈0.35), and a strict `xfail` in `test_jev.py` records that.
It catches the planted-bad ledger in the same suite.
Until a question set passes known-legitimate plans, its output is a prompt to look, not a finding.

```bash
python3 jev/semantic_check.py path/to/ledger.md
```

## Tests

```bash
uv run --with pytest pytest jev
```

Offline tests check plumbing with a fake transport and never Jev's judgment.
The four `live` tests ask real questions with known answers and skip without the key; a skip is not a pass, so run them with the key after changing any question.

## What the 2026-09-24 pilot showed

`pilot/2026-09-24/record.md`.
