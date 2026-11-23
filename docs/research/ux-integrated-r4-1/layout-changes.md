# Layout changes: R4 → R4.1

Presentation only. These are unchanged from R4:
- the model (R4's `r4_model.py`, imported as-is);
- the URL context and its three scopes;
- the pane architecture (overview + one right-hand pane);
- the seven dimensions.

There is one new URL key, `graph`. It is local to the trace pane.

Code:
- [`prototype/r41_views.py`](prototype/r41_views.py), forked from R4's `r4_views.py`;
- [`prototype/r41_state.py`](prototype/r41_state.py), which is R4's state module plus `graph` and `compare_letter`;
- [`prototype/app.py`](prototype/app.py).

## One vocabulary for the shared selection (Phase 6)

R4 used yellow for the selected row and a blue edge for pinned rows. The trace focus was a blue outline in the graph, so it shared a colour with the compare pins, and it had no marker in the overview at all.

R4.1 gives each concept one colour and one word, used the same way in every place it appears:

| Concept | Colour | Word | Where it shows |
| --- | --- | --- | --- |
| Inspected record (`rec`) | amber background | **in detail** | overview row tag, row background, fact-sheet title, context bar chip ("In detail"), Detail tab top edge |
| Compare set (`cmp`) | blue left edge | **compare A / B / C** | overview row tag, compare column header, context bar chip ("A · roasted broccoli"), Compare tab label ("Compare (2): A roasted broccoli, B steamed broccoli") |
| Trace focus (`trace`) | violet | **traced**, or **in trace** for rows the trace reaches | overview row tags, trace title, graph focus node (was blue), context bar chip ("Tracing"), Trace tab top edge |
| Filter exclusion | grey text | **excluded: reason** | overview row, banners in detail and compare, trace rows. The context bar adds "7 of 8 rows excluded" |
| On hand | green | **on hand** | always written out, never a dot alone |
| Hypothesis | brown italic | **experimental**, **idea** | never only a style |
| Not recorded | hatched | **not recorded**, **no … recorded** | never only a pattern |

The overview's row controls are now words: *add to compare*, *compare with roasted broccoli*, *remove from compare*, and *trace*. They replace ☐, ☑ and ⇄.

The one place where pinning does more than add a row is still pinning while a record is in detail: that compares the two. R4.1 now says so on the link itself ("compare with roasted broccoli"). In R4 this was only in a tooltip.

Local controls never touch the global or shared selection. A parametrised test covers the column set, trace step, differences-only, graph reveal and pane switch.

## Overview (Phase 2)

| R4 (Summary columns) | R4.1 | Why |
| --- | --- | --- |
| ☐ column | removed; *add to compare* under the name | a symbol that needed a legend |
| **Needs**: `●◐●◐◐ 6/6` | **Curated pairings**: "8 pairings · all 6 needed roles covered", then "on hand: lemon (acid)" when something is entered | `6/6` read as "6 of 6 on hand" as easily as "6 of 6 covered". The dots needed a three-mark legend. On hand is now named, not encoded |
| **Flavour routes**: "Creamy and acidic 2/2 req. on hand" | route name, then "all required on hand", or "not on hand: walnut" | names the missing required element instead of a fraction |
| **Ideas**: "6 · 1 tasted" | **Hypotheses and tastings**: "experimental pairing: brown butter (fat)", "6 Scout ideas", "tasted: brown butter, works" | R4 left experimental pairings out of the overview entirely. Now they are shown, separately from the curated facts |
| **Not recorded** | **Not recorded**: knowledge gaps only | missing ingredients never go here (see the fact sheet, section 8) |
| ⇄ column | removed; *trace* under the name | a symbol |
| subline "raw broccoli → roast · high" | "raw broccoli → roast · confidence high" | "high" alone did not say what was high |

Other changes:
- **Fewer columns.** The default goes from 7 columns to 5. When every row lacks a flavour route, for example potato, the route column is dropped and the banner says so once. That leaves 4.
- **Sticky header.** The header row, and in the matrix the legend row, stay visible while the overview scrolls.
- **Unchanged:** filters grey rows with a reason, *hide excluded* removes them, and "n of N match the filters" is kept.

The overview gets half the width instead of 10/21, about 30 px more at 1440 px.

## Fact sheet (Phase 3)

- **A section index** sits at the top of the sheet and stays pinned while the pane scrolls. It lists the eight sections in four bands, each entry with its size: "4 Pairings (9)", "7 Ideas and tastings (6 ideas · 1 tasted)". Each entry jumps to its section.
- **The bands separate kinds of information:**
  - *Attributes*: sections 1–2;
  - *Relationships*: sections 3–5;
  - *Evidence and testing*: sections 6–7;
  - *Gaps*: section 8.

  The eight numbered sections are unchanged.
- **Section 4 is grouped by role.** A role row reads "fat · needed · priority high" or "mild base · not a listed need", and the pairing rows follow it. The role is no longer repeated in every row.
- **Claim scope is stated once when it is uniformly missing.** None of the 288 pairing-to-source links in the database has a claim scope, so R4 printed "scope: not recorded" under every source (8 times for roasted broccoli). R4.1 states it once under the table. Where some link does carry a scope, each link shows its own, as before.
- **The availability column is dropped when nothing is on hand.** The sheet says "nothing is entered as on hand, so availability is not assessed" instead of printing "not on hand" on every row.
- **Section 6 carries the details of each source.** Each source is listed once, with type, the pairings it backs, and claim scope. The sources' own descriptions of themselves are behind a *How each source describes itself* disclosure, labelled as the source's own words. This is the only progressive disclosure in the sheet: those texts are not claims about the record.
- **Section 7 has three groups:**
  1. *Recorded tasting results* (date, idea, verdict, conditions);
  2. *Experimental pairings* (editor-recorded, ungraded; a pointer to their row in section 4);
  3. *Scout ideas*, with the tasted ones first.

  In R4, the trial conditions were a muted line under the ideas table.
- **Section 8 splits two kinds of absence:**
  - *Not recorded in the database (knowledge)*, hatched, with a link to the section concerned;
  - *Not on hand (your ingredients)*, on a separate green-edged box. For example, "Sour and toasted nut: required walnut not on hand". With nothing entered it says that availability is not assessed and that this is not a data gap.
- **The analogy rule moves under the candidate name.** It was a narrow 8th column of the ideas table, where every rule name wrapped over several lines.

## Compare (Phase 4)

- **Lettered records.** Each pinned record has a letter (A, B, C) in the column header, the overview row, the context bar and the Compare tab.
- **Plain-language cells.** Each pairing is on its own line, with "experimental" and "on hand" written out. "Linked idea tasted" moved out of the role cell, into its own row in the *Hypotheses and testing* group, beside a new *Experimental pairings* row.
- **The difference marker is the word "differs"** in a red tag. Identical rows are greyed and labelled "same". With *show only the rows that differ*, the count of hidden rows is shown.
- **Missing and not applicable are both words:**
  - "needed, no curated pairing recorded" (hatched);
  - "not a listed need" (grey).

  R4 used a hatched cell and "—".
- **No legend.** R4 repeated the matrix legend above every comparison.

## Trace (Phase 5)

- **The table is the reading surface.** For more than 20 relationships (`GRAPH_LIMIT`), the graph is collapsed and a note says how many relationships and entities there are. *Show the complete graph* (`graph=1`, local) draws it **below** the table, so the table keeps its place. At 20 or fewer, the graph is drawn above the table, as in R4.
- **The step labels read "Step 1: direct relationships"**, and so on. The relationship count is in bold.
- **Repeated From values are greyed**, so a run of edges from the same entity reads as a group. R4.1 first tried group header rows instead, but preparation traces alternate between preparation, role and ingredient, so almost every edge got its own group. That was dropped.
- **Names are never broken mid-word.** R4 set `overflow-wrap:anywhere` on every table cell. Entity names in the trace are now `nowrap`. The table scrolls sideways inside the pane if it must. The *Sources* column has a minimum width.
- **Source titles, types, claim scopes, relation types, knowledge, confidence (with its scale), availability, testing and optionality are all kept.** Columns that are n/a on every row are still dropped and named. A uniformly missing claim scope is stated once above the table.
- **The graph focus is violet**, the trace colour. It used to be blue, the compare colour.

## Matrix (Phase 7)

| R4 mark | R4.1 |
| --- | --- |
| `name` (curated) | name |
| `● name` (on hand) | green name + "on hand" |
| `◇ name` (experimental) | italic name + "experimental" |
| `✓` (a linked Scout idea was tasted) | **dropped from the cell.** It joined two records in one cell. The tasting is in the sheet (section 7), in compare (*Scout ideas* row) and in the trace |
| hatched + "needed · no curated pairing" | hatched + "needed, no curated pairing recorded" |
| `—` (not a listed need) | **empty cell** (tooltip: "not a listed need for this preparation"). A pairing in an unlisted role adds "not a listed need" under it |
| comma-separated names | one pairing per line |

The legend sits in the sticky table header. It is now two sentences about hatched and empty cells, not six marks. Cell text no longer breaks mid-word ("parmesa/n", "crouto/ns" in R4).

The matrix stays an optional column set, not the default.

## Not changed

- The model, every record and every dimension.
- The URL keys and their scopes, apart from the new local key `graph`.
- Filters and their reasons.
- The column sets, apart from wording.
- The trace steps.
- The edge list behind the graph and the table.
- The E3 checkbox: still off by default and not developed further.
