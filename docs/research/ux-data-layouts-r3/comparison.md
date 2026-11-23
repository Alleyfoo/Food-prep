# Identical data across layouts

Three records were chosen for how complete they are, not for how good the
food is:

| Dataset | Record | What is recorded |
| --- | --- | --- |
| **Complete** | roasted broccoli; on hand yogurt, lemon, garlic | 6 needs, all paired; 2 routes; 6 ideas, 1 tested; 2 sources; profile |
| **Incomplete** | roasted cabbage; on hand lemon | 6 needs, all paired; **no route**; 6 ideas; 1 source |
| **Sparse** | smashed roasted potato; nothing on hand | 3 needs, **none paired**; no route; 1 idea; 1 source; the only chained step (from boiled potato) |

Each layout was captured with a fresh page per shot, at 1440 × 900, by
[`evidence/capture_layouts.py`](evidence/capture_layouts.py). Output is in
[`evidence/capture-output.txt`](evidence/capture-output.txt) and
`screenshots/metrics.json`.

## Mechanical counts

These are counts, not scores. *Height* is the page length in 900 px
screens. *Gap markers* are elements that say plainly that something is not
recorded. *Status badges* are elements that carry an explicit status.

| Dataset | Layout | Height | Gap markers | Status badges |
| --- | --- | --- | --- | --- |
| Complete | L1 table | 1.60 | 1 | 52 |
| | L2 explorer | 1.95 | 1 | 28 |
| | L3 workspace | 1.99 | 2 | 30 |
| | Cards | 3.31 | 0 | 0 |
| Incomplete | L1 table | 1.83 | 1 | 59 |
| | L2 explorer | 1.65 | 1 | 24 |
| | L3 workspace | 1.77 | 3 | 20 |
| | Cards | 4.53 | 0 | 0 |
| Sparse | L1 table | 2.05 | 6 | 74 |
| | L2 explorer | 1.13 | 4 | 16 |
| | L3 workspace | 1.37 | 7 | 9 |
| | Cards | 4.54 | 0 | 0 |

Reading notes:
- **Cards show zero status badges** because they carry no status apart from
  each card's confidence pill. The cards for the sparse record *do* say
  "(no curated filler)" three times, but as row text with no marker, so the
  gap counter does not find it. Cards are not silent about gaps; they just
  give them no visual weight.
- The L2 counts include the neighbour tables. L3's overview is a canvas data
  grid, so its row text is not in the DOM. The `records_visible` count in
  `metrics.json` is therefore **not comparable for L3** and is left out
  here.
- Length matters less on desktop than on a phone. It is reported because
  cards need 3.3–4.5 screens to show what the other layouts show in 1.1–2.0.

## What each dataset revealed

### Complete: roasted broccoli
- **Cards:**
  - Correct, but the comparison with the four other preparations is split
    across 3.3 screens.
  - Routes show as "Creamy and acidic: yogurt lemon, also needs dill". The
    route records dill as a **finish** (optional), but the card says *also
    needs*, so it collapses optionality. This is a representation defect,
    not a data defect.
- **L1:**
  - In the matrix, *lemon* on hand sits in the acid column of three rows at
    once. That is a cross-state fact no card shows.
  - The Routes column shows which preparations have routes in one glance.
- **L2:**
  - Brown butter appears **twice**, as an experimental pairing (dashed, under
    fat) and as a tasted idea (amber). This is true to the data (it is both),
    but a reader may take it for two different things. The fact sheet (L3)
    shows the two rows together and reads better.
- **L3:**
  - The fact sheet reads top to bottom: what it is, what it needs, routes
    with *why it fits*, sources, ideas (labelled "not recommendations"), and
    what is not recorded.
  - It was the only layout where a reader can answer "why" without
    interpreting a graph.

### Incomplete: roasted cabbage
- **Cards:** the card has no *Routes* row at all when no route exists. The
  absence is silent.
- **L1:** the Routes cell shows "—" and the Not recorded column says "no
  flavour route". With *Paired with: lemon*, the 8 rows stay and the
  non-matching ones grey out with "no pairing with lemon".
- **L2:**
  - Six dashed idea boxes outnumber the solid curated structure. At the
  "ideas and sources" step, suggestions dominate the picture.
  - The step control lets the reader go back to "needs and routes" and see
    only the curated structure.
- **L3:** the "no flavour route written" section is present, hatched.

### Sparse: smashed roasted potato
- **Cards:** "Try: acid (no curated filler)…" is honest, but reads like an
  instruction with an empty value.
- **L1 is the strongest layout here:**
  - Next to nine siblings with filled cells, the three hatched cells make
    the sparsity obvious.
  - Sparsity is relative, and only a table puts it in context.
  - **Weakness:** the *Not recorded* column says "no flavour route" on all
    ten potato rows, which is noise. A gap shared by every row belongs once,
    above the table, not on every row.
- **L2:**
  - The three grey "(nothing recorded)" nodes and one idea make the gap
    unmistakable.
  - It is also the only view that shows the chain *boiled potato →
    smash_roast → smashed roasted potato* as structure.
- **L3:** the most hatched sections, with every gap named, but without the
  sibling context L1 gives.

## Defects found and fixed during capture

These are not findings about the layouts. They are listed so the
screenshots can be trusted:
- duplicate graph edges when two preparations share a route;
- the neighbour table naming the role instead of the preparation for a
  filler focus;
- an unlabelled priority under matrix cells (it read as confidence);
- the focus-row highlight hiding the hatched "not recorded" pattern.
