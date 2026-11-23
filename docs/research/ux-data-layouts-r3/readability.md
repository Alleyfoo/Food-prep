# Readability by data task

**Method.**
- An expert walkthrough of each layout in the running prototype, on the
  same data, starting with the ingredient chosen and nothing else set.
- *Steps* counts the clicks or selections needed before the answer is on
  screen.
- The outcome is one of:
  - **direct:** the answer is in one place;
  - **partial:** some of it, or only with interpretation;
  - **not supported:** the layout cannot answer it without visiting every
    record.
- There are **no numeric scores and no participants**. This shows what each
  structure *can* express, not what people will do with it.

The **Cards** column is the current card representation, all cards
expanded (see `layouts.md`).

## The tasks

| # | Task type | Question (same data for all) |
| --- | --- | --- |
| K1 | Scan | Which broccoli preparations have a flavour route? |
| K2 | Compare | How do roasted and steamed broccoli differ in what they need and what is paired? |
| K3 | Trace | Where does lemon fit across broccoli, as a pairing and as a route ingredient? |
| K4 | Explain | Why is lemon connected to roasted broccoli, and what backs it? |
| K5 | Fact vs suggestion | Is brown butter on roasted broccoli recorded, an idea, or tested? |
| K6 | Gaps | What is not known about smashed roasted potato? |
| K7 | Filter by what I have | Which cabbage preparations can use the lemon I have? |

## Results

| | Cards | L1 Associative table | L2 Relationship explorer | L3 Overview / detail |
| --- | --- | --- | --- |  --- |
| **K1 Scan** | **not supported** without items on hand: routes appear only as "Routes with what you have". With items, scan 5 cards over 3.3 screens | **direct**, 0 steps: Routes column. Or 1 step: *Has: flavour route* greys the others with the reason | **not supported**: one focus at a time, so 5 refocuses | **direct**, 0 steps: Routes column in the overview |
| **K2 Compare** | partial: two cards far apart, rows align but chips do not | **direct**, 0 steps: adjacent rows, roles as aligned columns | partial: 2 focuses, compared from memory | **direct**, 2 selections: pivot with roles, routes, ideas and gaps on aligned rows |
| **K3 Trace** | partial: find "lemon" in each of 5 cards; route membership only in route rows | partial, 1 step: *Paired with: lemon* finds pairings but **not route membership** | **direct**, 1 step: focus lemon shows 3 pairings (acid), 2 routes, and which preparations each fits | **not supported**: no reverse lookup |
| **K4 Explain** | partial: "acid: lemon, have it", no reason | partial: cell shows lemon and priority, no reason | partial: neighbour row shows confidence and "sources: 1", but not which source | **closest**: role note "lemon/sherry vinegar", route *why it fits*, sources for the step. **Still missing the pairing's own source title** (roast culinary), which no layout shows |
| **K5 Fact vs suggestion** | **not supported**: experimental pairings are filtered out of Cook cards | partial: dashed badge in the fat cell, "1 tested" in Ideas, but which idea was tested is not shown | direct but **duplicated**: dashed pairing *and* amber "tasted: works" node | **direct**: dashed badge in the fat row, plus an Ideas table row "works (2026-08-12)" under "not recommendations" |
| **K6 Gaps** | partial: "(no curated filler)" ×3 as plain text; no route row is silently absent | **direct, with context**: hatched cells beside nine filled siblings. Noise: "no flavour route" repeated on every potato row | **direct**: three grey "(nothing recorded)" nodes; the chain from boiled potato is visible | **direct**: hatched sections and a Not recorded box, without sibling context |
| **K7 Filter by on hand** | direct but long: "Available now: lemon" / "Not paired here yet: lemon" on each of 8 cards, 4.5 screens | **direct**, 0–1 steps: ● lemon in the acid column, or *Paired with: lemon* | direct, 1 step: focus lemon | partial: overview dots show *that* something is on hand, not *what* |

## What the pattern says

Each structure is clearly better at some tasks and clearly worse at others.
None wins overall:

| Data task | Representation that supports it best here | Why (structure, not looks) |
| --- | --- | --- |
| Scan and filter across preparations | **Table** (L1, L3 overview) | records are rows and attributes are columns; filtering greys rather than hides |
| Compare many | **Matrix** (L1 table B) | the ternary relation (state × role × filler) maps onto rows × columns × cell |
| Compare two or three in depth | **Pivot** (L3 compare) | attributes become rows, so every difference sits on one line |
| Trace from an ingredient or along a chain | **Graph + neighbour list** (L2) | the only structure that goes *from a filler* to states and routes |
| Explain one record; tell facts from ideas | **Fact sheet** (L3 detail) | fixed sections per relation type; ideas kept in their own labelled box |
| See what is missing | **Matrix in context**, then the sheet | sparsity is relative to siblings; an absolute list can't show that |

**Cards** sit between a fact sheet and a list. They hold one record's facts,
like a sheet, but without fixed sections for routes, evidence, ideas and
gaps. Repeated as a list, they make every cross-record task a scrolling
task.

## Cross-cutting findings

1. **An explicit status label is the largest single readability gain, and
   it is independent of layout.** K5 is unanswerable in cards today and
   answerable in every layout once status is a field.
2. **"Not recorded" must be a visible state.** It must be distinct from "not
   needed" (—) and never silently omitted. Cards omit the routes row; all
   three layouts kept a hatched placeholder.
3. **A gap shared by every row belongs above the table, not in every row.**
   "No flavour route" ×10 on potato is noise.
4. **A record with two statuses must appear once, with both.** Brown butter
   as two graph nodes reads as two things.
5. **Graph density follows the generated layer.** For roasted cabbage, six
   dashed ideas outweigh the curated structure. The step control is
   necessary, not decorative.
6. **Evidence is attached to two objects** (the step and the pairing). No
   layout yet shows the pairing's own source by name. That is the remaining
   gap for "why".
