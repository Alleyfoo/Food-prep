# R3 versus R4 across tasks K1–K7

## Method

- **The same seven questions as R3** ([R3 readability](../ux-data-layouts-r3/readability.md)), run by the author in the running prototypes. There are no participants.
- **Start state:** the ingredient is chosen and the on-hand items are entered. Nothing else is set, as in R3.
- **Steps** are clicks or selections before the answer is on screen. **Screen changes** are switches of layout or page, which R4 has none of by design.
- **Outcome labels** (no scores):
  - **direct**: the answer is in one place;
  - **partial**: part of it, or only with interpretation;
  - **not supported**.
- **Comparison columns:**
  - *Cards*: the original cards;
  - *Best R3*: R3's best separate layout for that task, with the layout switch it required;
  - *R4*: the integrated workspace.

## Results

| Task | Cards | Best R3 (layout) | R4 integrated | Change |
| --- | --- | --- | --- | --- |
| **K1 Scan**: which broccoli preparations have flavour routes? | not supported without items on hand | direct, 0 steps (L1 or L3 overview) | **direct, 0 steps**: *Flavour routes* column in the default overview (roasted, steamed, stir fried). Or 1 step, *Has: a flavour route*: "3 of 5 match", raw and soup greyed with "excluded: no flavour route" | Same as R3's best. Routes now carry "required on hand x/y" |
| **K2 Compare** roasted vs steamed | partial: two cards 1+ screens apart | direct, 2 selections (L3 pivot, a separate layout from the L1 table) | **direct, 2 clicks**: select roasted, ☐ steamed. "13 of 19 rows differ", marked ≠; *show only differences* is 1 more. The overview stays visible with both rows pinned | **Better.** Differences are marked and can be isolated. No layout switch; the overview never leaves |
| **K3 Trace** lemon across broccoli | partial: find lemon in each of 5 cards | direct, 1 step, **in a different layout** (L2), with the context lost | **direct, 1 click** on any *lemon* link: matrix cell, sheet row, compare cell. Step 1 shows the 3 preparations paired with lemon (acid). Step 2 (1 click) adds the 2 routes where lemon is a required element, which preparations they fit, and the idea that replaces lemon (lingonberry vinegar). One lemon node | **Better.** The same answer without leaving the record. Route membership and pairing are separate edges into one node |
| **K4 Explain**: why lemon on roasted broccoli, and what backs it? | partial: "acid: lemon, have it" | partial, "closest" (L3 sheet), **no source named** | **direct as far as the data goes**, 0 steps once the sheet is open: role note "lemon/sherry vinegar"; pairing *curated · medium*; source **roast_culinary (culinary)**, *scope: not recorded*; 2 routes where lemon is **required**, with fit reasons. The source's own description is labelled as such, not as a claim | **Better.** The named source is now shown. **The remaining gap is in the data:** 0 of 288 pairing links have a claim scope |
| **K5 Evidence status**: is brown butter recorded, experimental or tested? | not supported: experimental pairings are filtered out | direct but **duplicated** (L2: two nodes); direct in L3 sheet | **direct, 0 steps** in the sheet. Section 4: *experimental pairing · not graded · no source recorded · "also a Scout idea (same ids)"*. Section 7: *Scout idea · medium high (inference strength) · underpowered · ✓ works 2026-08-12 · also recorded as experimental pairing for fat*, plus trial conditions (normal meal, ratio and temperature not measured). Trace: **one node**, two edges | **Better.** Three dimensions are kept apart, linked by ids, never merged |
| **K6 Coverage**: what is missing for smashed roasted potato? | partial: "(no curated filler)" ×3 as plain text | direct, with context (L1); noise "no flavour route" ×10 | **direct, 1 click**: overview banner "For every potato preparation: no flavour route" (once). The row's *Not recorded* says "no curated pairing for acid, herb, fat", hatched among 9 siblings. The sheet keeps sections 3–5 hatched, and section 8 lists the gaps with "nobody wrote it down". ☐ roasted potato gives a complete-vs-sparse compare | **Better.** The noise is gone; sibling context and record detail sit side by side |
| **K7 Filter**: which cabbage preparations have recorded pairings with the lemon I have? | direct but long: 8 cards, 4.5 screens | direct, 0–1 steps (L1) | **direct, 1 step**: *Filter · paired with: lemon* gives "1 of 8 match" (roasted cabbage), with 7 rows greyed and "excluded: no pairing with lemon". In the matrix, ● lemon in the acid column. The filter stays active: opening an excluded record shows a banner | Same as R3's best, plus the filter holds across panes |

**Summary of changes:**

| Against | Result |
| --- | --- |
| **The cards** | 5 tasks moved from *not supported* or *partial* to *direct* (K1, K2, K3, K5, K6). K4 became direct as far as the data goes. K7 went from 4.5 screens to 1 step |
| **R3's best layouts** | No task got worse. K2–K6 improved. **No R4 task needs a layout switch or a reselection.** In R3, the K2 → K3 → K4 sequence needed three layouts |

## Repeated navigation: one investigation, start to finish

Sequence: compare roasted and steamed, trace lemon, explain lemon on roasted, check brown butter, go back.

| | R3 | R4 |
| --- | --- | --- |
| Compare | L3, choose two in a multiselect | ☐ steamed (roasted selected) |
| Trace lemon | switch to L2, choose *lemon* in focus | click *lemon* in the compare cell |
| Explain lemon on roasted | switch to L3, re-select roasted, scroll to the role and routes | Detail tab (roasted still selected), section 4 |
| Brown butter status | stay in L3 (sheet) or L2 (two nodes) | same sheet, section 7, or click *brown butter* |
| Back to the previous step | re-select by hand | browser Back, or ✕ in the context bar |
| **Layout switches** | **3** | **0** |
| **Re-selections** | **2** | **0** |

## The three datasets

Mechanical counts are from `screenshots/metrics.json`, created by `evidence/capture_workspace.py`.
- *Full height* is the length of the `full=1` page (no inner scrolling) in 900 px screens, so it is comparable with R3's *height*.
- In normal use the overview and the right-hand pane scroll separately inside one 900 px screen.

| Dataset | State | Full height (screens) | Gap markers | Entity links | First screen shows |
| --- | --- | --- | --- | --- | --- |
| Complete | Overview + sheet | 3.51 | 4 | 65 | overview, detail |
|  | Matrix + sheet | 4.10 | 3 | 93 | overview, detail |
|  | Evidence cols + sheet | 3.51 | 7 | 60 | overview, detail |
|  | Trace, step 1 | 1.76 | 2 | 60 | overview, trace |
|  | Trace, step 2 | 4.26 | 5 | 89 | overview, trace |
| Incomplete | Overview + sheet | 3.02 | 4 | 56 | overview, detail |
|  | Matrix + sheet | 3.70 | 5 | 99 | overview, detail |
|  | Evidence cols + sheet | 3.02 | 12 | 56 | overview, detail |
|  | Trace, step 1 | 1.97 | 0 | 60 | overview, trace |
|  | Trace, step 2 | 3.00 | 1 | 74 | overview, trace |
| Sparse | Overview + sheet | 1.83 | 9 | 40 | overview, detail |
|  | Matrix + sheet | 1.92 | 12 | 97 | overview, detail |
|  | Evidence cols + sheet | 1.83 | 17 | 40 | overview, detail |
|  | Trace, step 1 | 1.17 | 3 | 47 | overview, trace |
|  | Trace, step 2 | 1.41 | 3 | 49 | overview, trace |

Reading notes:
- **Full height measures the longest column.** For the *sheet* states that is the fact sheet: 3.51 screens for roasted broccoli, against R3 L3's 1.99. The R4 sheet is **longer**, because it now carries the evidence tables, route elements with optionality, and the ideas table with dimensions. In use it scrolls inside its own pane, and the overview stays put.
- **R3's cards needed 3.3–4.5 screens.** They mixed the overview and the record into one page scroll.
- **The overview and one right-hand pane are on the first screen in every state.** Nothing pushes the overview away.
- **Entity links** count the one-click paths into another pane: the matrix adds about 30–60.
- **Gap markers** count hatched "not recorded" elements. The sparse record has the most, as it should. None of them is an instruction.

### Complete: roasted broccoli (yogurt, lemon, garlic on hand)
- **Overview:** the summary shows needs ◐◐●◐◐ with ● for the on-hand fillers, two routes with "2/2" and "1/2 req. on hand", and "6 · 1 tasted".
- **Sheet:** 9 pairings in one table, each with its source and "scope: not recorded".
- **Routes:**
  - *dill* is shown as a **finish**: not required, and not "also needs" as on the cards;
  - *olive oil* in "Sour and toasted nut" is **supporting**.
- **Trace at step 2:** 30 edges, 27 nodes. The structure is complete, but the graph text is too small to read at pane width, so the table is what you read.

### Incomplete: roasted cabbage (lemon on hand)
- **No route, stated once.** "No flavour route" is shared by all 8 cabbage preparations, so it moves to the banner, and roasted cabbage's row shows no gap of its own.
- **Ideas against curated structure.** Six Scout ideas, of which two are also recorded as other things:
  - rye crumbs is also an *experimental pairing* for crunch;
  - eggs is also a *curated pairing* for protein.
- **The trace at step 2 is readable** (23 edges): the generated layer is visibly dashed and amber, apart from the curated structure. Step 1 hides it entirely.
- **A pairing outside the listed needs.** *Potato for `mild_base`*, a role roasted cabbage does not list as a need, is shown in all four panes. R3 dropped it from its graph.

### Sparse: smashed roasted potato (nothing on hand)
- **The sheet does not look like a failure.** Sections 1–2 are fully recorded: a chained step from *boiled potato*, with a link, and a profile note explaining why the boil matters. Sections 3–5 are hatched with plain statements. Section 8 explains that a gap means "nobody wrote it down".
- **No section is empty or missing**, and no gap is phrased as an instruction (tested).
- **The trace shows the chain** (boiled potato → smashed roasted potato) and three "(no curated pairing)" nodes.
- **Compare with roasted potato** puts 4/4 paired needs next to 0/3, row by row.

## Where R4 became more complicated

- **More controls:**
  - a filter bar with five controls;
  - four column sets;
  - three panes;
  - three trace steps;
  - pinning;
  - a context bar.

  R3 had one layout radio and three filters per layout. The context bar and URL state make the extra state *visible*, but they do not make it *simpler*.
- **The fact sheet is long** for a complete record: 8 sections, 3 tables, and the ideas table. Detail of the right kind, but section 6 or 7 needs scrolling inside the pane.
- **The graph needs the step control to stay readable.** For a preparation at step 2 or more it is illegible at pane width; see [readability.md](readability.md).
- **The matrix needs a six-mark legend.**
- **Linking records by id exposes data oddities.** For example, Scout "ideas" that are already curated pairings. These read as contradictions until explained.
- **Prototype cost:** each click reloads the page in Streamlit (about 1–2 s).
