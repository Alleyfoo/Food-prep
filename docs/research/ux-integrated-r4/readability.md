# Readability: information density and the competing layout decisions

**Method.** An expert walkthrough of the running prototype at 1440 × 900, plus mechanical counts from `evidence/capture_workspace.py` (`screenshots/metrics.json`). There are **no participants and no scores**. These findings describe what the structure makes possible or hard; they do not show what people will do with it.

## The five decisions the brief asked about

### 1. Table versus matrix

| | Summary table (default) | Needs × roles matrix |
| --- | --- | --- |
| Answers at a glance | which rows have routes (K1); coverage per row (dots); row-specific gaps | which ingredient fills which role in which preparation; where lemon sits (K7); role-by-role differences across all rows |
| Density (broccoli) | 4 data columns | 10 role columns, up to 4 names per cell |
| Needs a legend | 3 dot symbols | 6 marks: name, ● on hand, ◇ experimental, ✓ tasted, hatched, — |
| Width | fits the 10:11 split | needs the 7:5 split; cabbage adds a `mild_base` column, a pairing-only role |

**Finding.**
- The matrix is the only representation that answers "where does X sit across every preparation" without a trace. It is also the best way to see sparsity *relative to siblings*: a hatched cell among filled ones.
- Its cost is real. It is the only view that needs a six-mark legend, and once the right pane is open it has to share the screen.
- **Keep it as a switchable column set, not the default.**

### 2. Table versus fact sheet: what belongs where

What moved during the build:
- **Out of the default overview:**
  - from → technique and step confidence (now a subline under the name);
  - the source counts (now the *Evidence* column set).
  - In the first render, seven columns in about 600 px broke route names one letter per line.
- **Kept in the overview:** what is needed to *choose a row*:
  - needs coverage (●◐○);
  - route names, with required on hand;
  - ideas and tasted counts;
  - gaps specific to the row.
- **Only in the sheet:** everything that needs a sentence or a per-record table:
  - role notes;
  - each pairing's dimensions;
  - route elements with optionality;
  - sources with claim scope;
  - idea reasoning;
  - tasting conditions.

**Finding.** The overview works as an index for choosing rows, not as a place to read data. Each time a reason or a per-relation attribute went into the overview, the overview got worse, and nothing could be done there that the sheet did not do better.

### 3. Graph versus relationship table

Edge and node counts for each trace (from the model):

| Focus | Step 1 | Step 2 | Step 3 |
| --- | --- | --- | --- |
| roasted broccoli | 15 edges · 16 nodes | 30 · 27 | 40 · 29 |
| lemon (broccoli) | 3 · 4 | 12 · 6 | 15 · 8 |
| roasted cabbage | 15 · 16 | 23 · 22 | n/a |
| smashed roasted potato | 7 · 8 | 8 · 9 | n/a |

What the graph shows **that the table does not**:
- **Convergence.** Three preparations meet at one lemon node, and the route element and the pairing land on the same node.
- **The chain**: boiled potato → smashed roasted potato.
- **The density of the generated layer.** On roasted broccoli at step 2, six dashed idea edges fan out from the state.
- **One-node identity.** Brown butter is one box labelled *experimental · idea · tasted*, with two edges.

What the graph **cannot** do:
- **Show attributes.** Sources, scope, availability and testing are in the table.
- **Stay readable at step 2 or 3 for a preparation.** At 27–29 nodes and the pane's width, labels fall to about 7 px.

**Finding.**
- The graph earns its place for **small foci**: an ingredient, a route, a source, or a preparation at step 1. There it shows structure in one glance.
- For a preparation at step 2 or more it duplicates the table and is illegible. The table is the reliable representation.
- **Recommended:** keep both, but collapse the graph automatically above about 20 edges and say so.

### 4. Status presentation: dimensions without badge soup

R3 used one badge per relation. R4 uses three strategies, one per density level:

| Where | Strategy | Result |
| --- | --- | --- |
| Fact sheet tables, trace table | **One labelled column per dimension**, plain text, with one style each: italic amber for experimental, dashed underline for generated, bold green "● on hand", "✓ works" for tested | No badges. Each cell answers one question. The pairings table is 7 columns wide, which fits the right pane |
| Trace table | **Columns that are n/a on every row are dropped and named** | A lemon trace has no *Testing* column; a brown-butter trace does |
| Matrix | **Glyph code**: ● on hand · ◇ experimental · ✓ tasted · hatched not recorded · — not a need | Compact, but a legend is required |
| Overview summary | **Counts and dots only** | Nearly no status marks |

**Finding.**
- **Yes, in tables.** Separate columns communicate knowledge type, confidence (with its scale named), availability, provenance and testing without stacking badges.
- **Only partly in the matrix.** The ✓ mark ("a linked idea was tasted") on a pairing cell is the one place where two records' dimensions meet in one cell. It needs the legend to be read correctly.
- **The database itself conflates two dimensions in one place:** `pairings.confidence = 'experimental'` is a knowledge type stored in a confidence field. R4 shows it as *not graded (recorded as "experimental")*.

### 5. The E3 answer-first panel

**Not shown by default.** It can be switched on with *E3 summary (eval.)* (`answer=1`). Screenshot: `tasks/E3-answer-summary-on.png`.

With roasted broccoli selected and yogurt, lemon and garlic on hand, the panel says:
- try creamy and acidic;
- you have yogurt and lemon;
- nothing else is required;
- dill is optional;
- why it fits;
- what to watch.

Every one of those facts is already visible in the workspace:
- the overview's route column ("Creamy and acidic 2/2 req. on hand");
- sheet section 5 (elements with optionality, fit reason);
- section 2 (risks).

| Task | Does E3 add anything? |
| --- | --- |
| K1–K7 | No. None of them is answered faster or more completely. E3 covers only the selected record and only its first route |
| "What should I cook with what I have?" | Possibly. It picks one route and says it in a sentence. But that is a *recommendation* task, which is outside this data-exploration study |

**Finding.**
- For exploring data, the panel repeats what the structured views already show. Above the overview it pushes the overview down by about 340 px. It appears unstyled here because the product CSS is not loaded, but it would still be a multi-line block when styled.
- Its "See the full roasted broccoli card" link points to a card the workspace no longer has. The panel was designed to sit above cards.
- It also introduces an ordering the workspace otherwise avoids ("try this one").
- **Keep it out of the data workspace.** Re-evaluate it only in a cooking-task study.

## Density and scrolling

- **The overview and the right pane scroll separately**, both 640 px tall. No investigation step pushes the overview off screen. In R3's L3, the sheet and overview shared the page scroll.
- **The fact sheet is long.** It is 3.5 screens of content for roasted broccoli, 3.0 for roasted cabbage and 1.8 for smashed roasted potato, against 2.0 for R3's L3 sheet. See [comparison.md](comparison.md). Sections are fixed and numbered, so a reader learns where "sources" is. But reaching section 6 or 7 on a complete record needs scrolling inside the pane.
- **Repeated navigation:**
  - K2 → K3 → K4 on the same record needs no reselection, because `rec` and `cmp` persist.
  - In R3 the same sequence meant switching layout three times and re-choosing the record in each.

## Duplicated or contradictory information found

- **Brown butter** is no longer duplicated in the graph: one node, two labelled edges. In the sheet it appears in two sections (4 and 7), each pointing to the other ("also a Scout idea (same ids)", "also recorded as experimental pairing for fat"). This is deliberate: two records, cross-referenced.
- **Eight Scout ideas propose an ingredient that is already a curated pairing** for that state, for example eggs on fried potato. The sheet now says "also recorded as: curated pairing for protein" next to the idea. Shown honestly, this looks like a contradiction: an "idea" that is already known. It comes from the generator, not from the layout (see recommendations).
- **No contradiction between panes was found.** All four render from one model, and a test checks that every pairing appears in all four.
