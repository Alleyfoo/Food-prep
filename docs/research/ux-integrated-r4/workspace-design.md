# Workspace design: layout and selection model

## Layout (desktop, 1440 × 900)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Ingredient │ On hand (global) │ Filter: has │ Filter: paired with │ Filter: gap │ hide excluded │
├──────────────────────────────────────────────────────────────────────────────┤
│ Context bar: ingredient · on hand ✕ · filters ✕ · selected ✕ · compare ✕ · trace ✕ · reset all │
├───────────────────────────────────┬──────────────────────────────────────────┤
│ A. OVERVIEW (always visible)      │ [Detail] [Compare (n)] [Trace]           │
│ column set: Summary | Sensory |   │ B. fact sheet / C. compare / D. trace    │
│   Needs × roles | Evidence        │ (the pane scrolls on its own; the        │
│ (scrolls on its own)              │  overview stays where it was)            │
└───────────────────────────────────┴──────────────────────────────────────────┘
```

- **The overview never leaves the screen.** Detail, compare and trace share the right-hand pane, and each pane scrolls on its own. This answers the brief's main question directly: no investigation step replaces the overview.
- **The filter bar replaces the sidebar.** The first build kept the sidebar, and it took about 260 px, which squeezed the overview until route names broke one letter per line. This was found in the first render and changed before evaluation.
- In the *Needs × roles* column set the overview gets more width (7:5 instead of 10:11), because the matrix needs it.

### A. Overview: associative table

- **The default column set is Summary**, with a deliberately short set of columns:
  - prepared ingredient, with a subline *from → technique · step confidence*;
  - **Needs**, as dots: ● curated pairing on hand, ◐ curated pairing recorded, ○ no curated pairing. A count such as "4/6" sits beside them, and the full list is in a tooltip.
  - **Flavour routes**, with "required on hand x/y" when something is on hand;
  - **Ideas**, with how many were tasted;
  - **Not recorded**: only the gaps specific to that row.
- **Other column sets are chosen deliberately:**
  - *Sensory*: flavour and texture shift, risks, keeps, freezes, batch.
  - *Needs × roles*: the R3 matrix. Needed roles come first, then roles that only appear on pairings.
  - *Evidence*: step sources, with ✓ where a claim scope is recorded; pairing sources with counts; pairings without a source; pairing claim scopes.
- **Gaps shared by every row are stated once**, in a banner above the table, for example "For every potato preparation: no flavour route". They are not repeated in rows. This fixes the R3 noise.
- **Each row has three controls:**
  - the name opens the record's detail;
  - ☐ pins it for comparison;
  - ⇄ traces it.

### B. Detail: fact sheet in 8 fixed sections

1. Identity and transformation
2. Sensory attributes and risks
3. Needed culinary roles
4. Recorded pairings
5. Flavour routes and their elements
6. Evidence and provenance
7. Experimental ideas and tasting results
8. Missing or incomplete knowledge

How the sheet presents information:
- **Tables carry the dimensions as labelled columns, not badges.** The pairings table has these columns: Role, Ingredient, Knowledge, Confidence, Application, Availability, Source · claim scope.
- **A section with no data stays in place and says so** on a hatched background, for example "no flavour route recorded for this preparation". A missing role is never phrased as an instruction.
- **Route elements are listed with their optionality**, with *required* in bold. A note under the routes says supporting and finish elements are optional. The card's "also needs dill" problem from R3 cannot occur here, and a test checks this.
- **The selected record stays highlighted in the overview.** If the active filters exclude it, the sheet says so in a banner.

### C. Compare

- **Pinned records become aligned columns.** The rows are grouped: Identity, Sensory, Needs and pairings (one row per role), Routes, Ideas, Evidence, Not recorded.
- **Rows that differ are marked ≠.** A count such as "13 of 19 rows differ" is shown, and *show only differences* hides the identical rows.
- **Missing data is explicit:**
  - a hatched cell means "needed, no curated pairing";
  - **—** means "not a recorded need".
- **Pinned rows keep a blue edge in the overview**, so you can go back to the overview and the compare set is still there.

### D. Trace

- **What you can trace:** a prepared ingredient (⇄), any ingredient (a link everywhere it is named), a route, or a source.
- **The step control reveals relationships deliberately:**
  1. Direct relationships. For a preparation: origin, needs, curated pairings, and needs with nothing recorded. For an ingredient: the preparations it is paired with.
  2. Adds routes and their elements, experimental pairings and Scout ideas.
  3. Adds sources.
- **One edge list drives both the graph and the table**, so they cannot disagree, and a test checks this. Each real entity is one node: brown butter appears once, labelled *experimental · idea · tasted*, with two edges.
- **The table drops columns that are n/a on every row** and names them, so a lemon trace doesn't carry an empty *Testing* column.

## Selection model

All state is in the URL ([`prototype/r4_state.py`](prototype/r4_state.py)). Every click is a link, so **the browser's Back button returns to the previous context**, and any state can be shared or captured.

| Scope | Keys | Affects | Notes |
| --- | --- | --- | --- |
| **Global** | `ingredient`, `have`, `has`, `paired`, `gap`, `hide` | every pane | On hand changes availability everywhere. Filters grey overview rows, add a banner in detail and compare, and mark excluded preparations in the trace |
| **Shared selection** | `rec` (selected record), `cmp` (pinned, ≤ 3), `trace` (focus) | read by every pane | Opening another pane never clears them. Each is shown in the context bar with ✕ |
| **Local** | `pane`, `cols`, `depth`, `diff`, `answer` | only their own pane | Changing the column set doesn't change the selection |

Rules that prevent unexpected jumps:
- **Pinning the first row while another record is selected compares the two.** The selected record is the natural reference. The Compare pane opens only once two are pinned.
- **Clicking an ingredient in the sheet opens Trace and keeps `rec` and `cmp`.** The trace table offers "back to <selected record>".
- **Clicking a preparation in the trace opens its sheet and keeps the trace focus**, so the Trace tab still shows it.
- **Changing the ingredient drops `rec`, `cmp` and a preparation or route trace**, because they belong to the old ingredient. **An ingredient or source trace survives:** tracing lemon across broccoli and then cabbage is a legitimate investigation.
- **Recovery:**
  - every part of the context bar has ✕;
  - "clear filters" and "reset all" are links;
  - Back undoes the last step.

Interaction paths verified in the running prototype (browser) and in tests:

| Path | Result |
| --- | --- |
| Overview → Detail | Clicking *roasted broccoli* opens its sheet; the row stays highlighted |
| Overview → Compare | With roasted selected, ☐ on *steamed* compares the two (13 of 19 rows differ). The overview still shows both pinned |
| Detail → Trace | *lemon* in the pairings table opens Trace focused on lemon; selected and compare kept |
| Trace → Detail | *steamed broccoli* in the trace table opens its sheet; the trace focus stays in the Trace tab |
| Filters → all panes | *paired with lemon* on cabbage: overview "1 of 8 match" with reasons; excluded records get a banner in detail and compare and a mark in the trace |

## Prototype costs (not design findings)

- **Each click reloads the Streamlit page** (about 1–2 s), because links are plain URLs. A production build would update in place.
- **The graph is Graphviz.** At depth 2 or more for a preparation (27–29 nodes), its labels are too small to read at pane width. See [readability.md](readability.md).
