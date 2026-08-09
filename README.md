# data-reasoning

A Claude Code and Codex plugin for reasoning from data: structured exploration that generates honest leads, and hypothesis-driven investigation that adjudicates them.

## Skills

| Skill | What it covers |
| --- | --- |
| [exploratory-data-analysis](skills/exploratory-data-analysis/) | Structured exploratory data analysis — orient before interpreting, count every look, consolidate ranked leads with their search context, and hand adjudication to hypothesis-driven-analysis. |
| [hypothesis-driven-analysis](skills/hypothesis-driven-analysis/) | Guide empirical investigations with PPDAC and the scientific method — competing hypotheses, preregistered predictions, adequate tests, and a precommitted stop rule. |

The two are a pair.
Exploration generates hypotheses and never confirms them; adjudication is `hypothesis-driven-analysis`'s work.
Both carry the same authorization gate, and `skills/exploratory-data-analysis/decisions/001-shared-gate-authority.md` names `hypothesis-driven-analysis/SKILL.md` as its single authority — a test keeps the copy from drifting.

The pairing is a design claim, not a measured one.
`hypothesis-driven-analysis` has an archived scenario suite behind it (`skills/hypothesis-driven-analysis/tests/`); `exploratory-data-analysis` has none — its scenarios are authored and no arm has run (`skills/exploratory-data-analysis/tests/scenarios.md`).
No run has yet exercised a handoff between the two.
Per `skills/hypothesis-driven-analysis/tests/scenarios.md` § "Owed measurements as of 2026-08-08", the descriptions that decide which skill activates also rest on zero valid arms.
Treat the routing between them, and the handoff itself, as unverified.

## Installation

### Claude Code

```
/plugin marketplace add briandconnelly/briandconnelly-plugins
/plugin install data-reasoning
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
