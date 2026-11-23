# Mechanical comparison of the variants

**Method.** Each state was opened in all its conditions on the same prototype and data, at 1440 × 900, using `evidence/capture_variants.py`.
- **Screenshots:** `screenshots/<state>/<condition>.png`.
- **Composites:** `screenshots/side-by-side/`.
- **Numbers:** `screenshots/metrics.json`.

These are counts only. They show what each encoding costs in space and how much must be decoded. They do not show which one people read better. That is the session's job ([session-plan.md](session-plan.md)).

## Overview: A against B against C

| State | Measure | A: code | B: labelled | C: named roles |
| --- | --- | --- | --- | --- |
| broccoli (5 rows) | rows fully in view | **5 of 5** | 4 of 5 | **5 of 5** |
| | median row height | **63 px** | 100 px | 80 px |
| | words in the table | **127** | 214 | 168 |
| cabbage (8 rows) | rows in view | 7 of 8 | 7 of 8 | 7 of 8 |
| | median row height | **63 px** | 80 px | 80 px |
| | words | **140** | 246 | 170 |
| potato (10 rows) | rows in view | **7 of 10** | 6 of 10 | 6 of 10 |
| | median row height | **63 px** | 80 px | 80 px |
| | words | **190** | 292 | 212 |
| scan: cabbage, paired with lemon | rows in view | **6 of 8** | 5 of 8 | 5 of 8 |
| scan: potato, a need with no curated pairing | rows in view | 6 of 10 | 6 of 10 | 6 of 10 |
| all states | legend-dependent marks | 33–44 | 0 | 0 |
| | legend | 47 words | none | none |
| | cells whose names are only in a tooltip | 10–14 | 0 | 0 |

### Findings

1. **C costs close to what A costs in words** (+12 to +32% over A). B costs +54 to +76% over A. C is 21–31% shorter than B in every state.
2. **The name cell sets a floor under every row; the encoding adds to it.**
   - The name cell is identical in all variants. It sets a floor of 63 px: the name, a wrapped subline and the actions.
   - **A sits on the floor.** C rows are 17 px above it (80 px) in every state. B rows are 17 px above it too, except broccoli, where they are 37 px above (100 px).
   - **In filtered views the floor rises to 80 px,** because the name cell gains an "excluded: …" line. There the three encodings are the same height.
   - So the visible-row difference between the variants is 0–1 rows at this width. Removing about 17 px from the name cell would be worth as much to every variant as switching B to A.
3. **A hides 10–14 names per screen in tooltips.** Every "which role?" or "what is on hand?" question needs a hover per row in A. B and C answer it in the cell.
4. **C answers "which role?" at a glance.** B gives the count ("3 of 4 covered") and names the missing role only in *Not recorded*. C puts the missing role, hatched, next to the covered ones.

## Fact sheet: full against dense

| Record | Measure | full | dense |
| --- | --- | --- | --- |
| roasted broccoli | pane heights | 5.76 | **4.31** (−25%) |
| | section headings in the first pane screen | 3 | **4** |
| | section 7 starts at | 2,231 px | **1,657 px** |
| roasted cabbage | pane heights | 4.89 | **3.71** (−24%) |
| | headings in the first screen | 3 | **4** |
| smashed roasted potato | pane heights | 2.70 | **2.16** (−20%) |
| | headings in the first screen | 2 | **4** |

**Finding.** Dense recovers most of the length R4.1 added over R4. R4 was 4.48, 3.74 and 1.93 pane heights; dense is 4.31, 3.71 and 2.16 (broccoli now includes the tasting observation, which R4 did not show). It keeps every fact and every link, which a test checks.

**The open question is whether 13 px type and the four-column attribute grid slow reading.** The grid puts two unrelated attributes on one line, for example "Flavour tags … Texture tags".

## What this narrows down for the session

- **The overview question is no longer "symbols or sentences".** It is whether **C's named tokens** keep B's accuracy at A's word count, and whether **A's speed advantage survives** once the tooltip hovers are counted.
- **B is the safe reference**: it is R4.1.
- **For the sheet,** the question is whether dense costs accuracy. If it does not, it is the better default, because it is shorter at no loss of content.
- **Before the session, the name cell should stay fixed.** Changing it at the same time would confound the encoding comparison. It is the next lever after the session.
