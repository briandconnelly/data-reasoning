# Output style

The plugin ships one optional output style, `Data Answer` (`output-styles/data-answer.md`): an analyst persona that answers data questions answer-first, with a short standing bar on reporting numbers you have not checked.
The file is the contract; this page does not restate it.

It supplies presentation and answer hygiene, not analysis method.
The skills decide what an answer must disclose and what a report must contain; the style yields to a skill's report format, its ordering, and its placement rules wherever one applies.

It adds no record-keeping to hypothesis-driven-analysis's ceremony-free `direct` route, but it does shape a direct answer: a source-and-freshness footer, an offer of the query.
Whether the split between the two holds under a real run is untested; treat it as a design claim, like the routing and handoffs in [Evidence status](evidence-status.md).

Select it through `/config` → Output style.
It sets `force-for-plugin: false`, so installing the plugin never changes the active style on its own, and `keep-coding-instructions: true`, so the default coding guidance stays in place for the code an analysis has to write.

Output styles are a Claude Code feature.
Codex has no equivalent, so a Codex install gets the four skills and no style.
