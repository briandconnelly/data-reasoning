# 007 — Text that ships in several skills is rendered from one source

Decided 2026-09-02.

## Question

All four skills bind the same authorization gate, and skills install standalone — a harness may load any one of them without the others on disk.
So the gate text has to be *inside* each `SKILL.md` at read time; a carrier cannot point at another file and expect an agent to follow the pointer.
Four files therefore hold the same bytes.
Where does that text live, and what keeps the four in step?

## Positions

*Parity-tested copies.* What shipped first, and what this record replaces.
Each carrier held a hand-maintained copy, and each copy had its own parity test comparing it to `hypothesis-driven-analysis/SKILL.md` (`skills/exploratory-data-analysis/decisions/001-shared-gate-authority.md`).
It works as an alarm, and it caught nothing wrong in a year of edits.
What it does not do is remove the four homes: an editor who wants to change the gate still edits four files by hand and finds out afterwards whether they matched.
The tests also carried a byte-identical hidden-text extractor in each of three files, which then needed its own parity test to keep the three copies of the *checker* from drifting — an alarm on the alarm.

*Extraction to a reference file.* Rejected.
The gate would live in `references/` and each `SKILL.md` would point at it.
The S19 finding rules this out: reference files go unread, and a rule that reaches an agent only when it opens a second file is a rule that does not reach it (`skills/hypothesis-driven-analysis/decisions/004-single-authority-for-normative-rules.md` records the measurement — arms reached the intended disposition 6/6 when the rule was in `SKILL.md`, the file they always read).
Authorization is the one rule that must never depend on a second read.

*Rendering.* Adopted.
The text lives once in `scripts/shared-sections/authorization-gate.md`.
Each `SKILL.md` carries a rendered copy between marker comments, so the shipped bytes an agent reads are unchanged.
`scripts/check-shared-sections.py` both writes the authority into the carriers and fails a run in which a carrier has drifted from it or has stopped being visible to a reader; that script documents its own interface.

## What settled it

Rendering keeps what the copies bought (the text is in the file the agent reads) and drops what they cost (four places to edit, three extractor copies, four hooks).
The choice between an alarm and a generator is not close once the generated artifact is byte-identical to what the alarm was defending: an alarm tells you the four homes disagree, a generator means there is one home.

The migration itself was the evidence that no wording moved: markers were inserted, `--render` was run and changed nothing, and the three parity tests were run one last time and passed (33 passed, 2026-09-02) before being deleted.

## Consequences

- Changing the gate touches one file where it used to touch four, and a hand edit to a carrier's copy fails the hook instead of shipping.
- Each `SKILL.md` gains two HTML comment lines, which render as nothing and are not instruction text.
- The three per-skill parity tests, `scripts/test_extractor_parity.py`, and their four prek hooks are gone; `check-shared-sections` watches all four `SKILL.md` files, which is what the deleted hooks watched between them.
- The reworded shared sections (costly collection, data rules) are deliberately *not* migrated: they differ per skill by design, so they keep the golden-freeze mechanism EDA decision 001 governs.

## Reopening condition

A host that rejects HTML comments in `SKILL.md`, or a measured arm showing the markers change agent behavior.
Either would mean the rendered copy is no longer free, and the question becomes which carrier form to use, not whether to render.

## Where the rule lives

`AGENTS.md`, repo-wide.
`scripts/shared-sections/authorization-gate.md` is the gate text's one home; `scripts/check-shared-sections.py` renders and enforces, and owns no rule.
