# Reference research — Qlik Sense and Celonis Process Explorer

**Method and limits.** No interactive access to either product was available.
Everything below comes from official documentation read on 2026-11-22. Each
fact carries its source. Anything not documented in the pages read is marked
**unverified**; nothing is filled in from memory or from screenshots.

- **Qlik Sense:** all pages loaded (help.qlik.com, several releases, last
  updated Oct–Nov 2026). Confidence: **high**.
- **Celonis:** the current documentation (`docs.celonis.com`,
  `documentation.celonis.com`) redirects to a sign-in, including the
  Process Explorer and Multi-object Process Explorer pages. What could be read
  is the public **legacy Celonis 4.6/4.7 help** (last modified 2024), one
  official **blog post** (2022) and one **community product update**
  (2024-05-29). Confidence: **medium** for the single-object Process Explorer,
  **low** for current and multi-object behaviour.

---

## A. Qlik Sense — associative exploration

### A1. Selections are global and survive navigation
- "Selections are global": a selection made in one visualization "is
  reflected in all related visualizations, no matter what sheet they are on."
  The selections bar "shows all selections regardless of which sheet they
  were made on."
  [Selection states (Qlik Cloud)](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Selections/selection-states.htm)
- Sheet actions can also set selections on navigation.
  [Exploring with selections](https://help.qlik.com/en-US/sense/May2026/Subsystems/Hub/Content/Sense_Hub/Selections/SelectionsToolbar/work-with-selections.htm)
- Selections and locks are **not saved** with the app; they last for the
  session. (Same page.)

### A2. Selection states: what is in, what is out, and why
| State | Shown as | Meaning |
| --- | --- | --- |
| Selected | green, check mark | the user's choice |
| Possible | white | still associated with the current selection |
| Alternative | light grey | would be possible if this field had no selection; excluded "only by a single selection" |
| Excluded | dark grey | not associated, because of a selection in **another** field |
| Selected excluded | dark grey, check mark | chosen earlier, then excluded by a later selection elsewhere |

Sources: [Associative selection model (May 2025)](https://help.qlik.com/en-US/sense/May2025/Subsystems/Hub/Content/Sense_Hub/Selections/associative-selection-model.htm),
[Selection states (Qlik Cloud)](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Selections/selection-states.htm).

The docs present grey values as **information, not noise**: they "can bring
you new information about relationships that were not known before" (e.g. a
region with no sales reps). Light grey versus dark grey tells you *what*
excluded a value: your own field, or another field. That is the only "why"
mechanism documented; no tooltip or explanation panel is described
(**unverified**).

### A3. History and recovery
- Selections bar: **step back**, **step forward**, **clear all**. Step back
  goes "all the way to the first selection in the session"; step forward only
  appears after stepping back; clear all keeps locked selections.
  [Step back/forward](https://help.qlik.com/en-US/sense/November2025/Subsystems/Hub/Content/Sense_Hub/Selections/SelectionsToolbar/step-back-forward-selections.htm)
- "All the selections you have made during this session are stored."
  [Selection states (Qlik Cloud)](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Selections/selection-states.htm)
- Locks stop a selection being changed or cleared, but step back can still
  pass them. (Step back/forward page.)

### A4. Seeing the whole selection at once
- The selections bar shows each active selection as a chip with a mini state
  bar; clicking one opens view / edit / clear / search / lock.
  [Exploring with selections](https://help.qlik.com/en-US/sense/May2026/Subsystems/Hub/Content/Sense_Hub/Selections/SelectionsToolbar/work-with-selections.htm)
- The **selections tool** gives "an overview of every dimension and field in
  an app", in two parts: active selections, and all app dimensions (master
  items by default; *Show fields* for everything).
  [Using the selections tool](https://help.qlik.com/en-US/sense/November2025/Subsystems/Hub/Content/Sense_Hub/Selections/use-selection-tool.htm)

### A5. Discovering unexpected relationships
- **Smart search** searches "the entire data set ... from any sheet"; results
  "show the combinations of matches found in the entire Qlik Sense database"
  and are based on field associations. Choosing a result applies it as a
  selection. Searching within a selection that excludes the term returns "No
  matches found within your current selection".
  [Smart search](https://help.qlik.com/en-US/sense/May2026/Subsystems/Hub/Content/Sense_Hub/Search/use-smart-search-tool.htm),
  [Using search results](https://help.qlik.com/en-US/sense/May2026/Subsystems/Hub/Content/Sense_Hub/Search/smart-search-data.htm)
- **Associative insights** search the model for excluded values after a
  selection (mentioned on the selections-tool page; details not read →
  **unverified**).

---

## B. Celonis — process and relationship exploration

### B1. Complexity is controlled, most-frequent first *(legacy 4.6/4.7)*
- The default graph is the **baseline**: "the most frequent end-to-end variant
  of the process."
- **Activities** and **Connections** panels each have a slider with
  *Less* / *More* / *Reset*. Each step adds the next most frequent activity or
  connection, or removes the least frequent one shown.
- **List view** lets the user pick activities or connections by hand instead.
- **Fixed Layout** stops the graph re-arranging when connections change.

Sources: [Process Explorer — Celonis 4.7](https://help.celonis.com/cpm47/en/process-explorer),
[Celonis 4.6](https://help.celonis.com/cpm46/en/process-explorer).
The blog confirms the default shows "the most common activities and
connections filtered on case frequency".
[Process Explorer vs Variant Explorer](https://www.celonis.com/blog/celonis-ems-process-explorer-and-variant-explore-whats-the-difference)

### B2. Inspecting one object and its neighbours *(legacy)*
- Clicking an activity opens **Activity Details**: occurrence statistics, and
  tabs **"Cases come from"** and **"Cases go to"** listing the most common
  predecessors and successors. Clicking one of those opens **Connection
  Details**, which links back to its activities.
- Clicking an edge opens **Connection Details** with its own statistics.

Sources: the two legacy help pages above.

### B3. Turning a look into a filter *(legacy)*
- Activity Details → **Select cases**: *With this activity*, *Without this
  activity*, *Starting with…*, *Ending with…*. Connection Details: *With /
  Without this connection*. This "filters the analysis according to the
  activity and the chosen filtering option".
- Hiding activities is **analysis-wide**: "Only the selected activities will
  be shown in the entire analysis."
- How the resulting filter is displayed and removed, and whether other
  components visibly update: **unverified** (not in the pages read).

### B4. Switching the measure on the same graph *(legacy)*
- One graph, several readings: *Case Frequency*, *Activity Frequency*,
  *Throughput Time* (median, average, trimmed mean), chosen from a KPI/frequency
  control. A play control animates cases over time.

### B5. Multi-object exploration *(2024 community update only)*
- The Multi-object Process Explorer uses **two multi-sliders** (objects and
  connections), with one colour-coded slider per object type matching the
  graph. Moving one adds the next most common event **for that object only**,
  plus whatever connecting events it needs; shared events appear as empty
  circles for other objects.
  [Multi-sliders in Process Explorer](https://community.celonis.com/product-updates/multi-sliders-in-process-explorer-2024-05-29-3571)
- Choosing object types, focusing on one, and moving to tables or individual
  objects: **unverified** (the docs page is sign-in gated).

### B6. Two representations, two purposes *(blog)*
- **Variant Explorer** "shows all the different paths (or variants)";
  **Process Explorer** shows the most common activities and connections
  without committing to one path, and is good for "finding infrequent
  activities". [Blog](https://www.celonis.com/blog/celonis-ems-process-explorer-and-variant-explore-whats-the-difference)

---

## Patterns extracted, with evidence strength

| # | Pattern | Product | Evidence |
| --- | --- | --- | --- |
| P1 | One global selection that every view respects | Qlik | docs, high |
| P2 | Excluded items stay visible, greyed, as information | Qlik | docs, high |
| P3 | Two kinds of exclusion (own choice vs elsewhere) | Qlik | docs, high |
| P4 | Session history: step back, forward, clear | Qlik | docs, high |
| P5 | One place showing every active selection | Qlik | docs, high |
| P6 | Global search that lands as a selection | Qlik | docs, high |
| P7 | Start from the most frequent path, add detail on demand | Celonis | legacy docs + blog, medium |
| P8 | Click a node for its details and its neighbours (from / to) | Celonis | legacy docs, medium |
| P9 | Turn an inspected object into a filter for the whole analysis | Celonis | legacy docs, medium |
| P10 | Same graph, switchable measure | Celonis | legacy docs, medium |
| P11 | Per-object-type expansion of a multi-type graph | Celonis | community post, low |
| P12 | A separate "paths" view beside the aggregate graph | Celonis | blog, medium |
