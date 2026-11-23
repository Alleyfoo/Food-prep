# First impressions — seven views, E1 interface

**Build:** `experimental/ux-shared-context` at `f4ba729` (E0 + E1), Streamlit 1.50.
**State:** a fresh page load on a fresh server, which is the documented default.
That means Cook › Ingredient Explorer, broccoli / roasted broccoli, nothing on
hand, and the example plate in Plate Balance.
**Captures:** `screenshots/desktop/*.png` (1400 px) and `screenshots/narrow/*.png` (390 px),
from [`evidence/capture_views.py`](evidence/capture_views.py).

**Method.** Each screen was judged on its own, before I re-read the earlier
UX conclusions (that comparison is in
[research-reconciliation.md](research-reconciliation.md)). The reviewer is
expert, not first-time, so every "a first-time user would…" line is an
**assumption**. Lines marked **Observed** are what the screen shows.

The seven questions per screen: **purpose · first noticed · invited action ·
essential vs supplementary · terms needing explanation · can the result be
identified · natural next step.**

---

## Global chrome (on every screen)

- **Observed:**
  - Title "Ingredient Foundry". The subtitle reads "A local cooking map for
    turning ingredients into useful components, seeing what taste roles are
    missing, and finding the next sensible move."
  - The "What do I have right now?" panel has a monospace helper line,
    "sorts suggestions into available now · missing but useful · not paired
    here yet". This panel shows only on Cook and Experiment (it is absent on
    Map and Journeys).
  - The section pills (Cook / Explore / Experiment) sit above the tab pills,
    and then comes the context strip, e.g. "INVESTIGATING Roasted broccoli ·
    from broccoli  AVAILABLE nothing entered".
- **Assumption:**
  - The subtitle names three jobs in one sentence, and two of its words
    ("components", "taste roles") are the app's own terms. A newcomer learns
    it is about cooking, not what to do first.
  - "What do I have right now?" is the clearest invitation on the page, and
    the helper line under it is the least readable text on the page.
- **Orientation:**
  - The context strip answers "what am I looking at", and it is the one place
    where subject and on-hand items sit side by side. It is small, grey and
    uppercase, and it sits below two pill rows. Whether people notice it is
    untested.
  - "Investigating" (the subject) and "Available" (ingredients on hand) are
    separated well in the strip. They are not separated in the content: on
    the Ingredient Explorer, the subject is "broccoli" in the picker and
    "roasted broccoli" in the strip.
- **Cook / Explore / Experiment:** the words do not say which questions each
  answers. "Explore" and "Experiment" share their first two letters and a
  similar idea (trying things). **Assumption:** a first-time user cannot
  predict where "leftovers" or "unusual pairing" lives.

## 1 · Ingredient Explorer (Cook, default landing)
`desktop/1-ingredient-explorer.png`, `narrow/1-ingredient-explorer.png`

| Question | Finding |
| --- | --- |
| Purpose | Observed: "Broccoli — 5 ways to transform it, ranked cooking before preservation." It appears to be a catalogue of what you can do to broccoli. |
| First noticed | Observed: the large mint "B" disc, then the accent-bordered first card, **Raw Assemble**. |
| Invited action | Weak. Nothing on the cards is clickable. The only controls are the ingredient picker and the "Best branches / Choose technique" mode pills. |
| Essential / supplementary | Essential: the technique name, its one-line sensory summary, and "Try" / "Use in". Supplementary: tags, risks, confidence pills, and the dotted (medium-confidence) chips. They all have the same visual weight, so about 70 chips appear before any single recommendation. |
| Terms | "branches", "Raw Assemble", "HIGH", "ranked cooking-before-preservation", "Missing" (missing from what?), "Best branches", dotted chips (no legend). |
| Result identifiable? | **No.** Two emphases compete. The accent border sits on Raw Assemble (rank 1), while "● The dish you are investigating" marks *Roast*, the second card. Observed: the strip says roasted broccoli, the picker says broccoli, and the bordered card is raw broccoli. |
| Next step | Unclear. Suggestions are labels, not links, so "Try lemon" leads nowhere. |

Narrow: the tab row wraps raggedly ("Ingredient Explorer" alone, then three
tabs below). The B disc takes about a fifth of the first screen, and the first
card starts below the fold.

## 2 · Component Explorer (Cook)
`desktop/2-component-explorer.png`

| Question | Finding |
| --- | --- |
| Purpose | Observed: "Something you already cooked — you do not always start from raw." It is clear that this is for leftovers or prepared things. |
| First noticed | The "RB" disc and "Roasted Broccoli", then the white card of chips. |
| Invited action | Reading. Next moves are grouped by role (SALT sea salt, ACID lemon…), which is the most actionable layout in Cook. |
| Essential / supplementary | Essential: "Next moves" and "Use in". Supplementary: tags, risks, storage. The two flavour route cards below hold most of the explanation. |
| Terms | "May need", "Flavour routes — 2 directions from this state", "ATTESTED HIGH", "Dimensions", "Culture", "Elements", "Fit". The raw id `olive_oil` shows in Elements, and titles are in Title Case ("Sour And Toasted Nut"). |
| Result identifiable? | Mostly. "Next moves" reads as the answer. |
| Next step | "Download .md" sits between the answer and the routes, so it looks like the next step, but it is an export. |

## 3 · Plate Balance (Cook)
`desktop/3-plate-balance.png`

| Question | Finding |
| --- | --- |
| Purpose | Observed: "Plate items" with mashed potatoes and a chickpea patty already filled in. It reads as a plate check. |
| First noticed | The four KPI tiles, with "HARD GAPS 3" ringed. |
| Invited action | Editing the plate (multiselect). Nothing says the starting plate is an **example**. |
| Essential / supplementary | Essential: "Missing — hard gaps" (acid / herb / crunch with fillers) and "Avoid adding more of: more fat / cream". Supplementary: the Items KPI, "Already provides" (body, carb, fat, mild base, protein, salt, umami). |
| Terms | "hard gaps", "target roles missing", "may want more · soft flags", "heaviness 3.5 / 5 rich", "body", "mild base", and "Cook mode — no experimental pairings" (monospace caption). |
| Result identifiable? | Yes, if the reader trusts "Missing" as the answer. KPI tiles come first and turn the answer into numbers ("3"). |
| Next step | None. The fillers are chips, so they can't be added to the plate. |

The context strip adds: "This view works on plate items or fillers, not on the
current dish." This is honest, but it means the strip's subject (roasted
broccoli) is not on this screen at all.

## 4 · Taste Circle (Cook)
`desktop/4-taste-circle.png` (re-captured with a 10 s settle, see note)

| Question | Finding |
| --- | --- |
| Purpose | Observed: a radial diagram with roasted broccoli at the centre and 11 taste dimensions around it. The instruction says "Click a dimension to see what fills it, click an ingredient to lock it in." The purpose is clear: build a dish by taste. |
| First noticed | The circle. Green nodes are "provided" and peach nodes "N options", with a legend below. |
| Invited action | **Clear.** It is the only screen with an explicit instruction, a legend, and a side panel saying "Nothing expanded — click a dimension…". |
| Essential / supplementary | Well split: dimensions are shown first, with fillers one click away. |
| Terms | "40 / 56" (unlabelled position counter), ◀ ▶ (tooltip only: "Next component"), "0 of 8 open dimensions filled. A plate does not need all eleven — only the ones this destination asks for." The sentence gives three counts (8, eleven, "this destination"), and no destination has been chosen. |
| Result identifiable? | Yes: "Your dish" lists what is locked in. |
| Next step | Clicking a dimension. "Surprise me" is the filled primary button, so a random action has the strongest visual call. |

**Observed (verified in browser):** ▶ steps to the next of 56 components
(roasted broccoli → roasted cabbage). Under E1 this changes the **shared
subject in every view**. The only label is a hover tooltip.

**Capture note:** the first automated capture, taken 4 s after clicking the
tab, still showed the *previous* view's cards faded under the Circle/Cards
pills. The re-capture waited 10 s. A newcomer would see a slow transition
where the old content looks like the new view (medium confidence; headless
timing).

## 5 · Map (Explore)
`desktop/5-map.png`, `narrow/5-map.png`

| Question | Finding |
| --- | --- |
| Purpose | Observed: "How it can be cooked, what each state becomes, what pairs with it and where it goes. Drag nodes to explore." The map shows all of broccoli, and roasted broccoli has the dark ring. |
| First noticed | A dense network of about 70 nodes in four shapes and colours, with labels about 6 px high at 1400 px. At 390 px the labels are gone. |
| Invited action | Dragging, which the copy names. Nothing invites selecting, filtering or reading. |
| Essential / supplementary | No distinction. Every node and edge is drawn at once. |
| Terms | Node shapes and colours have **no legend**. "Cook paths / Scout ideas" is a third pill level. |
| Result identifiable? | **No.** At default zoom the reviewer could not read which node was roasted broccoli without the "dark ring" hint. |
| Next step | None visible. Hovering gives tooltips (not checked here; R1 reported raw ids). |

## 6 · Journeys (Explore)
`desktop/6-journeys.png`

| Question | Finding |
| --- | --- |
| Purpose | Observed: "Broccoli — 4 complete cook paths. Each one reads left to right: preparation → transformation → sensory change → flavour route → correction → destination." This is a clear purpose: worked examples. |
| First noticed | The heading, then Journey 1 (stir-fried stems). |
| Invited action | Reading. This is the most narrative and readable screen ("Choose this route for…", "Watch for"). |
| Essential / supplementary | Essential: the title, "Choose this…" and "Watch for". The left-to-right chain is supplementary, and it wraps mid-chain over three lines, so it doesn't read left to right. |
| Terms | "correction" ("too rich", "too bitter" are the correction *triggers*, not corrections). |
| Result identifiable? | Yes per journey. "● Built on the dish you are investigating" sits *between* cards, so it is ambiguous whether it belongs to the card above or below (it belongs to the card below). |
| Next step | "…or continue into the crushed-broccoli journey" appears as text, not a link. The "What do I have" panel is absent here, and the on-hand items don't affect journeys. |

## 7 · Scout (Experiment)
`desktop/7-scout.png`

| Question | Finding |
| --- | --- |
| Purpose | Observed: a warning banner ("Hypotheses come from analogy rules applied to transformed states. They are not classics."), then "Roasted Broccoli + Brown Butter". It is clearly an idea to try. |
| First noticed | The bordered hypothesis title. |
| Invited action | Clear: there is a "Smallest test" with ratio / success / failure / correction / safety, then "Next hypothesis" and "Record a tasting". |
| Essential / supplementary | Well layered. The answer (pairing) comes first, then why, the two claims (Compatibility "Plausible", Novelty "Too rare to tell"), the test, and the history. |
| Terms | "analogy rules", "transformed states", "corpus", "flavour reinforcement", "analogy substitution", "Strength of this argument: medium high". "Transformed state" is the third name for what Cook calls "Something you already cooked". |
| Result identifiable? | Yes. |
| Next step | Clear: run the smallest test. "Other candidates" (eggs, lingonberry vinegar…) are buttons styled as plain text, so they don't look clickable. |

---

## Cross-screen observations

1. **Seven screens, at least four names for one concept.** The prepared thing
   is called a "component" (tab name), "Something you already cooked",
   "Transformed state", "Prepared state" (Taste Circle placeholder), "state"
   (strip, map), and "the dish you are investigating". *Observed.*
2. **Chips look like controls but aren't.** On Cook screens, chips carry the
   suggestions but can't be clicked. In Scout, the clickable items look like
   plain text. *Observed.* Whether users try to click chips is an
   *assumption* to test.
3. **Confidence vocabulary varies:** HIGH, MEDIUM HIGH, ATTESTED HIGH,
   "Strength of this argument: medium high", and dotted chips. *Observed.*
4. **Three pill levels look alike:** section, tab, and view/mode
   (Best branches / Choose technique, Circle / Cards, Cook paths /
   Scout ideas). *Observed.*
5. **The clearest screens** (Taste Circle, Scout, Journeys) state their
   purpose in one sentence and show one subject. **The least clear**
   (Ingredient Explorer, Map) show everything about the subject at once.

## Phase 2 — clarity at desktop and narrow widths

| Dimension | Desktop (1400 px) | Narrow (390 px) |
| --- | --- | --- |
| **Visual hierarchy** | Every Cook card uses one level of label (small caps grey) and one level of chip. The answer rows (Try, Next moves, Missing) weigh the same as Tags and Risks. Taste Circle and Scout have a real hierarchy: title, then claim, then detail. | The same, stacked. The subject disc and title take most of the first screen. On the Ingredient Explorer, the first recommendation chip is about 1.3 screens down. |
| **Language** | About 20 coined or technical terms on first screens (see per-view tables). Sentences are good where they exist (Journeys, Scout, Taste Circle hint). Labels are the problem, not prose. | Unchanged. The monospace helper text wraps into two lines of 9 px-looking type. |
| **Density** | Ingredient Explorer: 5 cards × about 8 rows. After entering three on-hand items (T1), 5 cards × about 11 rows. Map: about 70 nodes. | Cards become very tall columns of chips. The Map's labels drop out entirely, leaving shapes without names. |
| **Feedback** | On-hand picks update the strip and cards (good), but nothing at the top summarises what changed. A view switch can leave the previous view faded for several seconds (Taste Circle capture). Tasting save shows a green confirmation and the new history line (good), worded for a developer (see task T5). | Same. The strip wraps to two lines cleanly (E1 check confirmed). |
| **Orientation: subject vs on hand** | The strip separates them clearly. In the content, the on-hand items appear inside every card (AVAILABLE NOW / MISSING BUT USEFUL), so the two ideas merge again. | The strip stays readable. |
| **Orientation: Cook / Explore / Experiment** | The section names describe *modes*, not *questions*. Only Experiment has a single destination (Scout), so it has no tab row, and the layout shifts. | Section pills fit on one row. The tab row wraps unevenly (known D22). |
