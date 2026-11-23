# Relationship tracing: R4 against R4.1

**Method.** The same trace states were opened in both prototypes with the same URLs. Counts come from the model through `r41_views.trace_edges`, which is R4's edge list, unchanged. Screen measurements are from `evidence/capture_compare.py` (`screenshots/metrics.json`). There are no participants.

## When the graph collapses

`GRAPH_LIMIT = 20` relationships. The cells give relationships / entities, then what R4.1 does with the graph.

| Focus | Step 1 | Step 2 | Step 3 |
| --- | --- | --- | --- |
| roasted broccoli (preparation) | 15 / 16, shown | **30 / 27, collapsed** | **40 / 29, collapsed** |
| lemon (ingredient, broccoli) | 3 / 4, shown | 12 / 6, shown | 15 / 8, shown |
| brown butter (ingredient) | 0, none | 2 / 2, shown | 2 / 2, shown |
| roast_culinary (source 10) | 4 / 5, shown | 4 / 5, shown | 4 / 5, shown |
| roasted cabbage (preparation) | 15 / 16, shown | **23 / 22, collapsed** | **31 / 24, collapsed** |
| smashed roasted potato (preparation) | 7 / 8, shown | 8 / 9, shown | 9 / 10, shown |

**Across every preparation of all 12 tree ingredients:**
- 39 of the 183 preparation traces (61 preparations × 3 steps) are above the limit.
- None of them is at step 1. The largest step-1 trace has 15 relationships.

**The rule matches R4's own finding.** The graph was legible for ingredients, routes, sources and step-1 preparations, and illegible for a preparation at step 2 or more. The limit separates exactly those two groups in the three datasets:
- **Shown:** every ingredient, source and route trace measured, plus every step-1 preparation.
- **Collapsed:** the two rich preparations at steps 2 and 3.
- **Exception:** the sparse potato stays drawn at every step, and its 8–9 edges are readable.

**When collapsed,** the pane says *"Graph collapsed: 30 relationships among 27 entities are too many to read as a graph at this width. Every relationship is in the table below."* It offers *Show the complete graph*.

**When revealed** (`graph=1`), the graph is drawn under the table, so the table does not move. The toggle is local: a test checks that ingredient, on hand, filters, `rec`, `cmp`, `trace`, pane and step all survive it. The graph code (`trace_dot`) is unchanged apart from the focus colour, so nothing is lost.

## Where the table starts

`trace_table_y` is the number of pixels from the top of the right-hand pane to the first relationship row. The pane is about 600 px tall.

| State | R4 | R4.1 |
| --- | --- | --- |
| roasted broccoli, step 2 (30 edges) | 709 px, below the graph, off the first screen | **195 px**, under the collapsed-graph note |
| roasted cabbage, step 2 (23 edges) | 726 px, off the first screen | **212 px** |
| roasted broccoli, step 1 (15 edges) | 628 px | 644 px (graph drawn above) |
| lemon, step 2 (12 edges) | 441 px | 474 px (graph drawn above) |
| brown butter, step 2 (2 edges) | 208 px | 224 px |
| smashed roasted potato, step 2 (8 edges) | 362 px | 374 px |

**Pane length in pane heights** (`pane_screens`):
- roasted broccoli, step 2: 5.60 → 3.20;
- roasted cabbage, step 2: 3.70 → 2.44;
- lemon, step 2: 3.30 → 2.05.

For lemon the graph is drawn in both versions. The shorter pane comes from the table: names no longer wrap letter by letter, and R4's 33 broken words became 0.

**Where the graph is drawn, the table starts 12–33 px lower than in R4.** That is the bold relationship count and the step labels.

Source: `screenshots/metrics.json`, `trace_table_y` and `pane_screens`.

## Reading the table

| Property | R4 | R4.1 |
| --- | --- | --- |
| Entity names | `overflow-wrap:anywhere` on every cell, so names could break at any letter in narrow columns | entity links never wrap. Words never break. The table scrolls sideways inside the pane when it must |
| Source column | narrow, broke titles such as *roast_culinary* | minimum width of 12 em. Title, type and claim scope stay together |
| Claim scope | "scope" was not shown in the trace table (R4 passed `scope=False`) | shown per link when any link in the table has one. If none does, it is stated once above the table. Roasted broccoli's step source does carry a scope ("roasted broccoli with oil/salt/lemon/cheese"), so at step 2 every link shows its own |
| Repeated From | repeated in full on every row | greyed when equal to the row above, so runs of edges from one entity read as a block |
| Relation types | text | text, unchanged |
| Columns n/a everywhere | dropped and named | dropped and named, unchanged |
| Experimental and generated records | italic amber, dashed underline for generated | italic brown with the words "experimental pairing" or "Scout idea (generated)". The dashed underline was dropped, because the style no longer carries meaning on its own |

**Tried and dropped: one group row per From entity.** Edges for a preparation alternate between the preparation (→ role) and the role (→ ingredient). Grouping therefore produced about one header row per edge, and the table became longer without becoming easier to read. Greying repeated From values gives the same visual block without the extra rows.

## What tracing still cannot show

- **A graph above 20 edges is still illegible when revealed.** R4.1 does not try to fix the graph. It makes the table the default reading surface and keeps the graph one click away.
- **Claim scope.** No pairing-to-source link has one. Only transformation (step) sources carry claim scopes. Either way the claim scope is shown wherever it is recorded.
- **Convergence**, for example three preparations meeting at one lemon node, is still visible only in the graph. For an ingredient trace the graph stays drawn, because ingredient traces stay small (15 or fewer at step 3 for lemon), so convergence is still visible where it matters most.
