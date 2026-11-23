# The three layouts (plus the current cards for reference)

All of them read one model (`prototype/model.py`) built from the existing
query layer. The data is identical; only the structure differs. Status has
one visual code everywhere:
- **Curated:** plain outline.
- **On hand:** green with ●.
- **Source:** violet.
- **Idea:** dashed amber.
- **Tested:** solid amber.
- **Not recorded:** a hatched cell.

```powershell
py -3.11 -m streamlit run docs/research/ux-data-layouts-r3/prototype/app.py --server.port 8540
```

The state lives in the URL, for example
`?ingredient=broccoli&have=yogurt,lemon,garlic&layout=explorer&focus=lemon&level=2`.

## L1 Associative table

*From Qlik (filters grey rows out instead of removing them), ARIS's matrix
model, and ThoughtSpot's table-first answer.*

- **Filters:** *Needs role*, *Paired with* and *Has* (route, idea, tasting,
  source, something on hand).
  - Rows that fail a filter **stay in place, greyed**, with the reason
    ("excluded: no flavour route").
  - A count line says how many match.
- **Table A, prepared ingredients × attributes:** from, technique,
  confidence, flavour shift, keeps · freezes · batch, routes, ideas, sources,
  and a **Not recorded** column.
- **Table B, prepared ingredients × roles matrix:**
  - each cell lists the recorded pairings for that role, with their status
    and the role's priority;
  - **—** means "not a recorded need";
  - a hatched cell means "needed, nothing recorded".
- **Every relation as rows:** the long form, sortable (Qlik table box,
  Celonis OLAP table).

Screens: `screenshots/<dataset>/table(-full).png`,
`screenshots/tasks/filter-*.png`.

## L2 Relationship explorer

*From Celonis (focus node, "come from / go to", complexity slider) and ARIS
(typed object-to-object relations).*

- **Focus:** any prepared ingredient (●) or any filler.
- **Show** slider, four steps:
  1. needs and routes;
  2. plus pairings;
  3. plus ideas and sources;
  4. plus where it is used.
- **Graph** (left to right):
  - Origin → prepared ingredient → roles → fillers, and → routes → their
    elements.
  - Ideas hang off the state as dashed boxes; a tasted idea is a solid amber
    box with its verdict.
  - A needed role with nothing recorded is a grey dashed node "(nothing
    recorded)".
  - Edge style encodes status, edge label encodes priority, confidence or
    optionality.
- **Filler focus** reverses the direction. It shows every preparation the
  filler is paired with, and every route that uses it, with which
  preparations those routes fit.
- **Neighbour tables** beside the graph: *Comes from (n)* and *Goes to (n)*,
  each row with relation, node, status and details. They make the graph
  readable without hovering.

Screens: `screenshots/<dataset>/explorer(-full).png`,
`screenshots/tasks/trace-lemon-across-broccoli.png`.

## L3 Overview / detail workspace

*From UiPath (overview, then a comparison against a reference), ARIS (one
fact sheet per object) and ThoughtSpot (pivot compare).*

- **Overview:** a selectable table, one row per prepared ingredient.
  - Columns: needs as dots (● on hand · ◐ pairing recorded · ○ nothing
    recorded), routes, ideas, tasted, sources, confidence.
  - Clicking a row opens its sheet.
- **Fact sheet** (right), in fixed sections:
  - Attributes;
  - Needs and recorded pairings;
  - Flavour routes (with *why it fits* and *attestation*);
  - Evidence (source, type, what it supports);
  - **Ideas (Scout), not recommendations:** a dashed box, with reasoning
    strength, novelty and tasting verdict;
  - **Not recorded:** a hatched box.
  - Empty sections are kept and say so.
- **Compare (up to 3):** attributes and roles as rows, preparations as
  columns, so differences sit on one line.

Screens: `screenshots/<dataset>/workspace(-full).png`,
`screenshots/tasks/compare-roasted-vs-steamed.png`.

## Reference: current cards

`render.branch_card_html` with the same availability and routes, all cards
in rank order. It is shown so the comparison is against the real current
representation, not a straw man.

## What was deliberately not done

- No mobile layout, no typography or spacing polish, no animation.
- No new data and no change to any query or ranking. The model only reads.
- The prototype is **outside** the product app (`docs/research/…`). Nothing
  in `src/` changed.
