# Workflow evaluation — Tests A, B, C

**What this is:** a developer walkthrough of the running app (Streamlit 1.50,
1400×900, fresh session), plus two AppTest probes for exact state. **It is
not first-time-user testing.** It shows what is broken, contradictory or
unreachable; it cannot show what a new person would find hard. Evidence lives
in [`screenshots/evidence/`](screenshots/evidence/).

---

## Test A — Selection continuity (Qlik)

*Roasted broccoli, lemon and garlic on hand.*

| Step | Result | Evidence |
| --- | --- | --- |
| 1. Select roasted broccoli | Cook › Component Explorer, type in the state picker. 2 clicks + typing. | `testA-1-component-explorer-roasted-broccoli.jpg` |
| 2. Say what I have | "What do I have right now?": lemon, garlic. Holds; clicking the box before each pick avoids a known focus loss. | same |
| 3. Find flavour combinations | Two route cards (*Creamy and acidic*, *Sour and toasted nut*). Lemon is marked on hand by colour only. Garlic is "Not paired here yet", though **garlic confit** is suggested as a fat two lines above it; the app never connects garlic to garlic confit. | same |
| 4. Into Taste Circle | Shows roasted broccoli, but **only because it is the default** (see the control). Lemon is recognised: "lemon is in your kitchen" when Sour is opened. | `testA-2-taste-circle-sour-lemon-on-hand.jpg` |
| 5. Related ingredients and destinations | Taste Circle has fillers but **no destinations**. Destinations need Explore › Map, which shows **broccoli as a whole ingredient** (47 nodes), not the roasted state. The "What do I have" box is not shown there, and on-hand items are not marked on the graph. | `testB-1-map-default-broccoli.jpg` |
| 6. Return without rebuilding | Picks (lemon, garlic) survive. Taste Circle keeps its dish and open fan. But returning to Cook **lands on Ingredient Explorer**, not the Taste Circle tab that was open. | `testA-3-return-to-cook-lands-on-first-tab.jpg` |

**Control: does the subject carry?** The
[probe](screenshots/evidence/testA-subject-continuity-probe.py) picks roasted
tomato in Component Explorer and tomato in Ingredient Explorer, then reads every
other view ([output](screenshots/evidence/testA-subject-continuity-output.txt)):

```
Taste Circle shows      : roasted_broccoli_component
Map shows               : broccoli
Journeys shows          : broccoli
Scout shows             : roasted_broccoli_component
Back in Cook, tab       : Ingredient Explorer
Component Explorer kept : roasted_tomato_component
```

**Findings (observed):**
- A1 · **The subject never carries between views.** Six pickers, each
  independent. The scenario appeared to work only because broccoli is every
  view's default; with any other subject the cook re-picks it in each view.
- A2 · **The on-hand list does carry**, the app's one global selection,
  but it disappears from screen on Explore while still applying there.
- A3 · **Section switching loses position** (always the first tab).
- A4 · **Ingredient and state are different subjects with no bridge.** Map and
  Journeys take "broccoli"; Taste Circle and Scout take "roasted broccoli".
- A5 · Terminology: "component", "state", "after-state", "filler", "route" and
  "destination" all appear on the way; only some are explained in context.

---

## Test B — Relationship navigation (Celonis)

*What can roasted broccoli become?*

| Step | Result | Evidence |
| --- | --- | --- |
| 1. Find broccoli in the graph | Explore › Map opens on broccoli (default). The ingredient node is larger and green; nothing labels it as the start. | `testB-1-map-default-broccoli.jpg` |
| 2. Find the roast transformation | A blue diamond labelled "roast", at **≈6.6 px** at the default fit. Readable only after zooming. Edge labels ("via", "becomes", "used in") are **≈5.6 px**. | `testB-2-map-labels-at-default-zoom.png` |
| 3. The resulting component and its properties | A purple node "roasted broccoli". Hover shows a raw id ("Component: roasted_broccoli_component"). **No properties anywhere on the Map**: tags, risks, missing roles and storage live in Component Explorer, with no link to it. | measured via the component's debug hook |
| 4. Related additions and destinations | 18 nodes connect to roasted broccoli (fillers, routes, destinations), mixed with every other state's neighbours, 47 nodes in all. No legend for the six node types. | — |
| 5. Focus on one path | Clicking the node bolds its 18 edges (vis-network default) and nothing else happens: no dimming of the rest, no details panel, no filter, no "expand / collapse". | `testB-3-map-roasted-broccoli-selected.png` |
| 6. Connect it to Journeys | Explore › Journeys, journey 2 "Roasted broccoli with a sour and nutty finish" names the same route (*Sour and toasted nut*) and destinations (side dish, grain bowl) that sit on the Map, but **neither view references the other**, and Journeys has its own ingredient picker. | `screenshots/explore_journeys.png` |

**Findings (observed):**
- B1 · **The whole graph arrives at once.** 47 nodes / 80 edges for broccoli,
  80 / 120 for tomato, at label sizes below legibility. Celonis's documented
  answer, start from the most frequent path and add on demand (P7), has no
  equivalent here.
- B2 · **No inspect-a-node.** Celonis opens details plus "comes from / goes
  to" on click (P8). Here, clicking only highlights.
- B3 · **Graph, card and journey describe the same objects without linking.**
  Map nodes, Component Explorer cards and Journey steps are three views of one
  data model with no navigation between them.
- B4 · **No legend.** Colour and shape encode node type (the design reply
  calls this the graph's core meaning) but the screen never says which is
  which.
- B5 · Strength: the colour system is consistent across the Map, Taste Circle
  and chips, and Journeys' text is the clearest explanation in the app.

---

## Test C — Missing and uncertain relationships (Qlik)

*An unrecorded pairing: roasted broccoli + mango, with lemon (recorded) and
miso (a Scout hypothesis) on hand.* The
[probe](screenshots/evidence/testC-uncertain-relationships-probe.py) reads each
view ([output](screenshots/evidence/testC-uncertain-relationships-output.txt)).

| The user needs to tell apart… | Does the interface? | Where |
| --- | --- | --- |
| Unavailable (not on hand) | **Yes:** "Missing but useful" | Ingredient / Component Explorer, Plate Balance |
| Undocumented relationship | **Yes, wording only:** "Not paired here yet"; Filler Profiles "No pairings recorded yet"; routes "absence here means nobody has written one" | Cook cards, Filler Profiles, Component Explorer |
| Potentially unsuitable | **Partly:** "Avoid when" only on Filler Profiles; Plate "Avoid adding more of"; `unsuitable_provided` computed, **never shown** | scattered |
| Experimental hypothesis | **Yes, but walled off:** Scout only, with a "not classics" disclaimer | Experiment › Scout |
| Supported recommendation | **Implicitly:** suggested fillers in "Try" / "Missing but useful"; the card's confidence pill rates the *transformation*, not the pairing | Cook cards |

**Key observation:** on the Cook roast card, **miso and mango sit side by side
under "Not paired here yet"**. Yet miso is a live Scout hypothesis for roasted
broccoli (miso-butter rule) and mango has nothing anywhere. Cook does not tell
"there is an untested idea" from "nothing is known", and does not point to
Scout. Keeping Scout out of Cook is deliberate and right; *saying* an
experiment exists is a different thing from *recommending* it.

**Why something is excluded:** the app already computes this. For roasted
broccoli, Scout has **45 rejected hypotheses**, each with a reason such as
*"the rule's test is written for soup, and this state is cooked pieces"*. None
is reachable: the Scout tab never requests rejected hypotheses, so its "Show
rejected" expander cannot render. This is the nearest analogue to Qlik's grey
states (P2/P3) and it is switched off.

**Findings (observed):**
- C1 · Absence is worded honestly everywhere it appears. No screen says
  "doesn't go with", which meets the brief's rule that missing evidence is not
  incompatibility.
- C2 · Four different statuses (not on hand, unrecorded, experimental,
  unsuitable) are not visibly distinguished **in one place**; a cook must
  visit three sections to assemble them.
- C3 · The "why excluded" information exists and is hidden by a call-site
  default.
- C4 · On route cards, "you have this" is shown by colour alone (no text or
  icon), which fails for colour-blind users. Taste Circle nodes also rely on
  colour, but its rail names on-hand items in words.

---

## What needs real users (hypotheses, not findings)

- Whether cooks *want* one subject across views, or think per view (Qlik's
  model assumes the former).
- Whether the full Map is ever useful at first sight, or only after focusing.
- Whether "Not paired here yet" versus a hinted Scout idea reads as a
  recommendation to some people.
- Whether the section/tab split matches how people describe their intent.
