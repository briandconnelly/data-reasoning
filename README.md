# data-reasoning

A plugin for Claude Code and Codex that helps your agent explore data, investigate explanations, review causal claims, and weigh decisions under uncertainty.
Use it for questions like "What's in this dataset?", "Why did signups drop?", or "Should we ship or wait?".
It provides four skills:

| Skill | What it does |
| --- | --- |
| [exploratory-data-analysis](skills/exploratory-data-analysis/) | Orient before interpreting, count every look, and report promising patterns with the search that found them. |
| [hypothesis-driven-analysis](skills/hypothesis-driven-analysis/) | Test competing explanations with preregistered predictions, adequate tests, and a precommitted stop rule. |
| [causal-identification-review](skills/causal-identification-review/) | Review whether a design identifies a causal effect, on which assumptions, and how each could break. |
| [decision-analysis](skills/decision-analysis/) | Weigh two actions under one binary uncertainty and recommend acting, waiting, or collecting more evidence. |

Start with whichever skill fits your question; each knows when to hand off to another.
None of them overclaims: exploration never confirms a hypothesis, a review never certifies a design, and a verdict never authorizes execution.
A bundled hook checks the structure of records written through the host's file tools; see [Record validation](docs/record-validation.md) for coverage.
Claude Code users can also choose the optional `Data Answer` output style for answer-first responses.

## Install

Claude Code:

```
/plugin marketplace add briandconnelly/data-reasoning
/plugin install data-reasoning@data-reasoning
```

Codex:

```bash
codex plugin marketplace add briandconnelly/data-reasoning
codex plugin add data-reasoning@data-reasoning
```

Start a new Codex session after installing, then follow [Installing](docs/installing.md) to trust and verify the hook.
The plugin is also listed in [briandconnelly-plugins](https://github.com/briandconnelly/briandconnelly-plugins).

## Learn more

- [Installing](docs/installing.md): verifying a Codex install and recovering one that carries test skills.
- [Record validation](docs/record-validation.md): what the hook checks, which writes it covers, and how to run the validator by hand.
- [Output style](docs/output-style.md): what `Data Answer` adds and how to select it.
- [Evidence status](docs/evidence-status.md): what has been measured, what has not, and what each skill costs in context.

## Development

Development happens on the `dev` branch, which carries the test suites, fixtures, and archived runs; `main` holds only the runtime tree that installs fetch.
See `AGENTS.md` for the branch rules.
All gates run through [prek](https://github.com/j178/prek):

```bash
prek run --all-files
```

## License

MIT
