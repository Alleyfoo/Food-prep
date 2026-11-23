# Reference systems: how they organize data

**Lens.** This looks at structure only: what the unit of display is, how
relationships are shown, how detail is reached, how uncertainty and evidence
are carried. Colours, branding and visual style are ignored on purpose.

**Method and limits.**
- No product was used hands-on. Everything comes from public documentation
  and community pages, read on 2026-11-22 (R1) and 2026-11-23 (this round).
- Each claim is tagged with how strongly it is supported:
  - **docs**: the vendor's own documentation;
  - **community**: a forum post or third-party write-up;
  - **unverified**: not found in what was read.
- Qlik and Celonis detail comes from R1
  (`research/ux-qlik-celonis-r1:docs/research/ux-qlik-celonis-r1/reference-research.md`).
  Only what matters for data structure is repeated here.

## Qlik Sense: associative fields and tables

| Structure | What it does | Evidence |
| --- | --- | --- |
| **Field lists / filter panes** | Each field's values are listed. Selecting values in one field re-states every other field as *possible*, *alternative* or *excluded*. | docs (R1) |
| **Excluded stays visible** | Grey values are kept on screen, not removed, and the docs call them information ("relationships that were not known before"). | docs (R1) |
| **Table and pivot objects** | Rows of records, with all associated objects re-filtering together. Some selection gestures are supported in tables, others are not. | docs ([Explore, discover and analyze, May 2025](https://help.qlik.com/en-US/sense/May2025/pdf/Explore,%20discover%20and%20analyze.pdf)) |
| **Global selection state** | One selection that every sheet respects, with step back and forward. | docs (R1) |

**Structural idea:**
- The *field* is the unit, not the record.
- Every attribute is a filter, and filtering explains itself by greying
  rather than hiding.

## Celonis: one object, its neighbours, and controlled complexity

| Structure | What it does | Evidence |
| --- | --- | --- |
| **Process graph with sliders** | It starts from the most frequent path, and *More / Less* adds or removes the next most or least frequent activities and connections. | docs, legacy 4.6/4.7 (R1) |
| **Activity details: "come from" / "go to"** | Clicking a node lists its predecessors and successors. Clicking one of those opens the connection, which links back. | docs, legacy (R1) |
| **OLAP table** | Configured dimensions and KPIs as columns, with sorting and search from the header. | docs ([OLAP table](https://docs.celonis.com/en/olap-table.html)) |
| **Object-centric data model** | Object types, event types, and the relations between objects and between events and objects. Browsable as a graph (types are nodes) or as a list. | docs ([object-centric data model](https://docs.celonis.com/en/the-object-centric-data-model)) |
| **Multi-object explorer** | One slider per object type. Events shared between objects are drawn differently. | community product update 2024 (R1); current docs need sign-in, **unverified** |

**Structural idea:**
- Relationships are first-class, and neighbours are listed as well as drawn.
- The amount shown is a control the user moves, not a fixed page.

## ARIS: objects, typed relationships, models attached to objects

| Structure | What it does | Evidence |
| --- | --- | --- |
| **Objects with maintained attributes** | Conventions say to fill an object's attributes (name, description, responsible role, category) before modelling it. | docs/conventions ([ARIS Community modelling guidelines](https://ariscommunity.com/accelerators/one-standard-process-architecture-process-modeling-guidelines-v1)) |
| **Typed connections** | Hierarchy is drawn with named connection types ("is process-oriented superior"). The allowed model types per object type are listed. | docs ([ARIS RCM modelling conventions](https://documentation.softwareag.com/aris/Risk_and_Compliance_Manager/10-0sr9/en/10-0sr9_Modeling_Conventions.pdf)) |
| **Assignment (drill-down)** | A detail model is *assigned* to an object, one level below it, so an overview object opens into its own model. | docs/conventions (same) |
| **Fact sheets and table view** | ARIS Connect offers standard views, including a *table view*, and a "Table fact sheet". | docs ([ARIS Connect functional matrix](https://documentation.softwareag.com/aris/Connect/10-0sr5/ycs10-0sr5e/10-0sr5_Functional_Product_Matrix.pdf)); fact-sheet content **unverified** (table of contents only) |
| **Matrix model** | Relationships between objects can be held in a matrix without drawing them. | community ([2011 answer](https://ariscommunity.com/users/srdsml/2011-08-12-question-add-relationships-object-without-displaying-connection-diagram)) |

**Structural idea:**
- One object has one sheet of attributes and typed relationships.
- The same relations can be a diagram, a table or a matrix.
- Detail is reached by assignment, not by a longer page.

## UiPath Process Mining: overview dashboards, compare against a reference

| Structure | What it does | Evidence |
| --- | --- | --- |
| **Overview dashboard** | Global KPIs, volume over time and the most frequent variants on one screen. | docs ([Overview](https://docs.uipath.com/process-mining/automation-cloud/latest/user-guide/overview---overview)) |
| **Process graph + metric selector** | One graph; a selector recalculates it on another metric. | docs ([Event analysis](https://docs.uipath.com/process-mining/automation-cloud/latest/user-guide/new-app-analysis-event-analysis)) |
| **Variants** | A variant is one fixed ordered path. Variants are listed and counted as alternatives. | docs (same) |
| **Root cause analysis** | A *selected* set is compared with a *reference* set, attribute by attribute, with an *Influence %* column. A "significant influencers" option hides values with little evidence, using both effect size and case count. | docs ([Root cause analysis](https://docs.uipath.com/process-mining/automation-cloud/latest/user-guide/root-cause-analysis)) |

**Structural idea:**
- Overview first, then a comparison table against an explicit baseline.
- Weak evidence is a filter state the user can see, not a silent cut.

## ThoughtSpot: the answer as a table, drill-down, pinned boards

| Structure | What it does | Evidence |
| --- | --- | --- |
| **Answer** | A search result that can be shown as a chart or a table. Answers are pinned to **Liveboards**. | docs ([Liveboards and Answers](https://docs.thoughtspot.com/cloud/latest/liveboards)) |
| **Drill down** | Into attributes (classic) or into measures and attributes (new experience). Back one step at a time in Answer Explorer, otherwise reset. | docs ([Drill down](https://docs.thoughtspot.com/cloud/latest/search-drill-down)) |
| **Pivot table** | A wide table that keeps its expansion state when pinned. | docs ([Pivot table](https://docs.thoughtspot.com/software/latest/chart-pivot-table)) |
| **SpotIQ insights** | Generated trends, outliers and explanations, kept apart from the answers the user built, with a narrative description. | docs ([SpotIQ](https://docs.thoughtspot.com/cloud/latest/spotiq)); narrative from a third-party write-up (community) |

**Structural idea:**
- The table is the default answer. A chart is one rendering of it.
- Machine-generated insight lives in its own space, apart from what the user
  asked for.

## Patterns relevant to Food-prep's data

| # | Pattern | Seen in | Food-prep use |
| --- | --- | --- | --- |
| R1 | **Attributes as filterable columns; excluded rows greyed with a reason** | Qlik | Compare preparations; find what fits on-hand items without losing the rest |
| R2 | **Focus object + "comes from / goes to" list + drawn graph** | Celonis, ARIS | Trace an ingredient through roles, routes and ideas |
| R3 | **Complexity as a user control** (more / less) | Celonis | Graph from needs only, up to ideas and sources |
| R4 | **One fact sheet per object; relations grouped by type** | ARIS | Explain one prepared ingredient fully |
| R5 | **Same relations as diagram, table or matrix** | ARIS, Celonis | Preparation × role matrix, relation rows and graph from one model |
| R6 | **Compare against an explicit reference, side by side** | UiPath, ThoughtSpot pivot | Roasted vs steamed broccoli |
| R7 | **Generated insight kept in a separate, labelled space** | ThoughtSpot SpotIQ | Scout ideas never mixed silently with curated pairings |
| R8 | **Weak evidence shown as a state, not silently dropped** | UiPath significance, Qlik grey | "Not recorded" as a visible cell, distinct from "not needed" |

Every one of these is a statement about **structure**: the unit of display,
how relations are listed, how detail is reached. None of them is a card.
