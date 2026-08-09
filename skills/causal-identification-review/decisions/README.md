# Decision Log

This skill does not exist yet as agent-facing prose.
Its scenario catalog will record measured claims in `tests/runs/artifacts/` and open questions as issues, the same as the other two skills in this plugin.
Neither of those captures the third kind: calls settled by *argument* — where the evidence was a reasoning failure, a cross-model critique, or a textbook/discipline test rather than a run.
Those are the ones that drift, because the next reader inherits the conclusion without the constraint that produced it, and re-litigates it from scratch.

This directory is also the durable home for the candidate-analysis reasoning that used to live in `potential-new-features.md`.
That file was deleted from the working tree on 2026-08-08 after the plan it fed was drafted, and was never tracked by git.
`.superpowers/sdd/2026-08-08-causal-identification-review-skill/candidate-analysis-preserved.md` holds a verbatim reproduction of the sections these decisions cite, but that workspace is gitignored and transient.
The decision records below are what carries that reasoning forward once the workspace is gone; each one restates the arguments it draws on, in its own words, attributed to their source.

One file per decision, `NNN-slug.md`, with five parts:

- **Question** — the decision point, stated so someone who disagrees would recognize it.
- **Positions** — what was actually argued, including the position that lost.
- **What settled it** — the argument or evidence, not the authority who made the call.
- **Reopening condition** — what would make this worth revisiting.
  A decision with no reopening condition is a belief.
- **Where the rule lives** — a pointer.

Six decisions (D1–D6), one file each, so each can be reopened independently of the others.

## The pointer rule

This decisions log follows the same pointer rule as `skills/hypothesis-driven-analysis/decisions/README.md` § "The pointer rule", stated once there and not repeated here — see that file for what the rule is and why it exists.

The owning file for every operable rule these records name is `skills/causal-identification-review/SKILL.md`.
That file does not exist yet.
Until it does, a record's "Where the rule lives" pointer names it as the future home rather than a live one — the record is naming a decision that precedes the prose it will govern, not skipping the pointer rule because there is nowhere yet to point.
