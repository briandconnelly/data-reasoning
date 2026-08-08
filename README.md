# data-reasoning

A Claude Code plugin for reasoning from data: structured exploration that generates honest leads, and hypothesis-driven investigation that adjudicates them.

## Skills

| Skill | What it covers |
| --- | --- |
| [exploratory-data-analysis](skills/exploratory-data-analysis/) | Structured exploratory data analysis — orient before interpreting, count every look, consolidate ranked leads with their search context, and hand adjudication to hypothesis-driven-analysis. |
| [hypothesis-driven-analysis](skills/hypothesis-driven-analysis/) | Guide empirical investigations with PPDAC and the scientific method — competing hypotheses, preregistered predictions, adequate tests, and a precommitted stop rule. |

The two are a pair. Exploration generates hypotheses and never confirms them; adjudication is `hypothesis-driven-analysis`'s work. Both carry the same authorization gate, and `skills/exploratory-data-analysis/decisions/001-shared-gate-authority.md` names `hypothesis-driven-analysis/SKILL.md` as its single authority — a test keeps the copy from drifting.

## Installation

```
/plugin marketplace add briandconnelly/briandconnelly-plugins
/plugin install data-reasoning
```

## Development

All gates run through [prek](https://github.com/j178/prek):

```bash
prek run --all-files
```

## License

MIT
