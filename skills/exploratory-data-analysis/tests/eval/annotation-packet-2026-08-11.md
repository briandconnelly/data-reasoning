# Annotation packet — query classification

You are classifying 20 short queries about a public library system.
Classify each query on three independent fields, using only the query text.
Do not look for any other file, result, expectation, or context; nothing else is needed, and consulting anything else invalidates the annotation.

## Fields

Assign exactly one value per field per query.

**scope** — what the query asks about.

- `whole` — the entity as such (the whole branch, the whole program, the whole account).
- `facet` — one named aspect of an entity (its hold queue, its attendance, its wait times).

**temporality** — the time framing the query itself states.

- `snapshot` — no time span or evolution is stated; the query asks how things are.
- `longitudinal` — the query states a time span or asks about evolution over time ("over the last two years", "has evolved", "since the renovation").

**boundary** — what the query asserts.

- `clean` — asks for information; asserts nothing about direction of change.
- `named-effect` — asserts a directional change as given ("has grown", "the drop", "fell"), whether or not it asks why.
- `frontier` — you judge the query genuinely ambiguous between the categories above, or otherwise unclassifiable on the definitions given. Use this sparingly and say why in the notes column.

## How to record

Return a table with one row per query ID, columns: `id`, `scope`, `temporality`, `boundary`, `notes`.
Use `notes` only for a `frontier` call or a genuine difficulty; leave it empty otherwise.
Classify every query. Do not skip any, and do not add commentary outside the table.

## Queries

| id | query |
| --- | --- |
| Q01 | What can you tell me about patron 55902's account activity? |
| Q02 | Tell me about how the Hillcrest branch uses its meeting rooms. |
| Q03 | Tell me everything about the Spanish-language holdings at Northgate. |
| Q04 | Give me context on branch 7's hold queue behaviour. |
| Q05 | Tell me about branch 14's circulation and staffing. |
| Q06 | Tell me about how the Riverside branch has evolved over the last two years. |
| Q07 | Give me the narrative on how the Westview branch's membership has grown. |
| Q08 | Give me an overview of the digital lending service. |
| Q09 | Tell me about the reference desk's question volume and mix. |
| Q10 | Describe the makerspace's usage patterns. |
| Q11 | Characterize the audiobook collection's circulation. |
| Q12 | Give me a picture of patron 71044's account since they joined. |
| Q13 | Tell me about the periodicals collection at branch 3. |
| Q14 | Analyze the recent borrowing pattern of patron 40117. |
| Q15 | Profile the teen section at Central Library. |
| Q16 | Tell me about the summer reading program cohort. |
| Q17 | I want a full picture of the large-print collection across branches. |
| Q18 | Walk me through the interlibrary loan program's activity. |
| Q19 | What's the story with the bookmobile route's usage? |
| Q20 | Give me a rundown on the Eastside branch — holds, checkouts, everything. |
