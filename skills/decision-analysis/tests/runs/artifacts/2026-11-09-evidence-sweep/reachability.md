# Reachability: which cells the 2026-11-09 change reaches

Settled before any arm runs, under `../../../../hypothesis-driven-analysis/tests/PROTOCOL.md` § What owes a rerun: a cell owes arms when its decision point traverses an edited sentence.
The judgement reads each fixture and prompt against the edited text; "reaches" means the cell's record must take a value the sentence governs, not merely that the agent may read it.
Revised 2026-11-10 with the review's scope rulings: the shipped validator stays structural, and the likelihood-ratio clause reads the stated threshold at the stated prior.
The preregistration for the new cells and the paid controls is `prereg.md` beside this file.

## Edits

| ID | Edit | Where |
| --- | --- | --- |
| E1 | "Orientation has its home here." and the three sentences after it: the Favored if true slot, the incremental loss ratio r, the favored action preferred above the threshold, 1/r when no threshold is stated (replaces "hold wins where posterior odds exceed one over the loss ratio") | `SKILL.md` § Numeric Policy |
| E2 | `dominated` bullet: "no higher … under both states, ties included", and Favored if true takes `none needed` | § Numeric Policy |
| E3 | `evidence-sensitive` bullet | § Numeric Policy |
| E4 | `robust` bullet adds "and at every likelihood ratio within the supported ranges" | § Numeric Policy |
| E5 | "The prior and loss clauses test their own quantity with each supported likelihood ratio held anywhere within its stated range." | § Numeric Policy |
| E6 | "Comparisons with the threshold are exact: …" (replaces "A tie counts as a flip") | § Numeric Policy |
| E7 | "A range whose endpoints are equal is a point, and a point never flips the action on its own." (replaces "a range that is a single point cannot flip") | § Numeric Policy |
| E8 | The all-point exact tie → `prior-sensitive` | § Numeric Policy |
| E9 | Removed: "v1 sweeps the prior class and the loss range only: a likelihood ratio stated as a range is carried through the posterior range and named in Conditions, never swept on its own." | § Numeric Policy |
| E10 | Decision frame paragraph names "the action the proposition favors" | § The Decide Route |
| E11 | Robustness paragraph adds "or what likelihood-ratio product" | § The Decide Route |
| E12 | Verdict set adds `evidence-sensitive`; the recommendation mapping adds it to `returned to owner` | § The Decide Route |
| T1 | New skeleton slot `- Favored if true:` | template |
| T2 | Crossover skeleton names the likelihood-ratio product | template |
| T3 | Slot notes: `none needed` covers Favored if true; `flips at likelihood ratio` is a Crossover phrase | template § Slot notes |
| K | Shipped validator findings an agent can see through the hook or `--final`: a missing Favored if true slot, `none needed` there outside `dominated`, and the loss-provenance cap on `evidence-sensitive`; no arithmetic | `instruments/check_record.py` |

## Loss interpretation of the existing prompts

DA-S1 ("missing a real regression costs us roughly ten times what a needless one-week hold costs") and DA-S8 ("between 2 and 20 times") state the loss as a ratio of regrets — the cost of shipping a real regression relative to holding, over the cost of a needless hold relative to shipping — which is E1's r with hold favored if the regression is real.
Their thresholds (0.1; 0.05–0.5) and every 2026-11-08 assertion value are therefore unchanged by E1.
DA-S3 states no loss; E1 reaches it only through the slot.

## Cell by cell

| Cell | Route and decision points | Edits reached | Owes a rerun? |
| --- | --- | --- | --- |
| DA-S1 | decide; no stated threshold, a rounded loss of 10, the point ratio 4.5, no supported prior | E1 (the slot; the threshold as 1/r), E10, E12 (the closed set it chooses from), T1–T3, K; E7 through its point loss range, a restatement with the same consequence | **yes** — measured and shipping; paid as a control (canary, pre 1, post 1) |
| DA-S1x | as DA-S1, exact loss | as DA-S1 | **yes** — unpaid debt |
| DA-S2 | decide; unsourceable ratios | E1, E10, E12, T1–T3, K; E3–E5 and E9 only if a record keeps a supported ratio range | no arm has ever run (`unrun`); its fixture is still to be generated; nothing extra owed |
| DA-S3 | decide; no losses, so the loss cap governs | E1 and T1 (the slot is required with no numeric loss), E10, K; E2 on its `dominated` branch; the cap decides before E3–E8 | **yes** — unpaid debt (its shipped wording already post-dates its arms) |
| DA-S4 | decide or decline; a causal proposition | E1, E10, E12, T1–T3 only if a record is written | no arm has ever run; nothing extra owed |
| DA-S5 | voi | none: no edited sentence lies on the VoI route and the VoI template block is unchanged | no |
| DA-S6 | routing | none | no |
| DA-S7 | voi | none | no |
| DA-S8 | decide; elicited prior range, loss range 2–20, the point ratio 4.5; double flip | E1, E5 (vacuous at a point ratio), E10, E12, T1–T3, K; the prior clause decides before E3, E4, E8 | **yes** — wording already marked not shipping-as-measured; paid as a control (canary, pre 1, post 1) |
| DA-S9 | new | E3, E4, E5, E6, E7, E9, E11, E12, E1 (its four-cell losses), T2, T3 | preregistered |
| DA-S10 | new | E1, E4, E10, T1 | preregistered |
| VoI route generally | voi | none | no |

## Debt this wave leaves unpaid

- DA-S1x and DA-S3 reach E1, E10, T1, and K and are not rerun.
- DA-S1 and DA-S8 get one canary, one pre, and one post arm each: enough to catch a gross regression, no more.
- E8 (the all-point exact tie) is reached by no fixture in the catalog; it is checker-enforced and unmeasured.
- K's wording is agent-read through the hook; no arm isolates it.
- Codex is unmeasured for every edit.
