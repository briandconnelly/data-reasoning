# data-reasoning

A Claude Code and Codex plugin for reasoning from data: structured exploration that generates honest leads, hypothesis-driven investigation that adjudicates them, and causal identification review that turns a dead end into a reviewed, assumption-bounded design.

## Skills

| Skill | What it covers |
| --- | --- |
| [exploratory-data-analysis](skills/exploratory-data-analysis/) | Structured exploratory data analysis — orient before interpreting, count every look, consolidate ranked leads with their search context, and hand adjudication to hypothesis-driven-analysis. |
| [hypothesis-driven-analysis](skills/hypothesis-driven-analysis/) | Guide empirical investigations with PPDAC and the scientific method — competing hypotheses, preregistered predictions, adequate tests, and a precommitted stop rule. |
| [causal-identification-review](skills/causal-identification-review/) | Review whether a design — proposed, claimed, or still to be found — identifies a causal effect and on what assumptions, with candidate designs, breakable identifying assumptions, probes run against them, and an evidence-bounded disposition that never certifies. |

Exploration generates hypotheses and never confirms them; adjudication is `hypothesis-driven-analysis`'s work; `causal-identification-review` is the constructive continuation when adjudication concludes nothing identifies the effect, or when a claimed design needs its identifying assumptions checked before anyone trusts it.
All three skills carry the same authorization gate verbatim, and `skills/exploratory-data-analysis/decisions/001-shared-gate-authority.md` names `hypothesis-driven-analysis/SKILL.md` as its single authority — two parity tests (EDA↔HDA and CIR↔HDA) keep the copies from drifting.

The pairing is a design claim, not a measured one.
`hypothesis-driven-analysis` has an archived scenario suite behind it (`skills/hypothesis-driven-analysis/tests/`); `exploratory-data-analysis` has none — its scenarios are authored and no arm has run (`skills/exploratory-data-analysis/tests/scenarios.md`).
No run has yet exercised a handoff between the two.
Per `skills/hypothesis-driven-analysis/tests/scenarios.md` § "Owed measurements as of 2026-08-08", the descriptions that decide which skill activates also rest on zero valid arms.
Treat the routing between them, and the handoff itself, as unverified.
`causal-identification-review` differs: measurement wave 1 (n=1 per cell) has been scored, with the verdict row recorded in `skills/causal-identification-review/tests/scenarios.md` § "Global verdict table".

## Installation

### Claude Code

This repository is its own plugin marketplace (`.claude-plugin/marketplace.json`).
Add it, then install the plugin from it:

```
/plugin marketplace add briandconnelly/data-reasoning
/plugin install data-reasoning@data-reasoning
```

### Codex

Add this repository as a marketplace, then install the plugin from it:

```bash
codex plugin marketplace add briandconnelly/data-reasoning
codex plugin add data-reasoning@data-reasoning
```

Start a new Codex session after installation so the bundled skills are available.

## Development

All gates run through [prek](https://github.com/j178/prek):

```bash
prek run --all-files
```

## License

MIT
