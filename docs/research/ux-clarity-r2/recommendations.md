# Recommendations — clarity before complexity

**Nothing here is implemented.**

**Priority order:** Clarity > Usability > Consistency > Reliability > Polish.
Accessibility, correctness and data safety are **mandatory minimums**: an
item that breaks one of them is listed first, whatever its category.

**Format of each issue:** Observed behaviour → User consequence → Evidence →
Possible improvement → Confidence. There are no numerical scores.

**IDs** refer to [research-reconciliation.md](research-reconciliation.md)
(N = new in R2, S = suspected, D/R1 = earlier research). Screenshots are
under `screenshots/`.

---

## Mandatory minimums (fix whatever the category)

### M1 · A small arrow silently changes the subject everywhere (N3) — correctness of state
- **Observed:** Taste Circle's ▶ / ◀ step through all 56 components. Under
  E1, the step moves the shared subject in every view (URL `state=` changes).
  The only label is a hover tooltip, "Next component".
- **Consequence:** a cook browsing Taste Circle returns to the Ingredient
  Explorer and finds a different ingredient, with no way back (no history).
  E1's shared context becomes a trap.
- **Evidence:** browser check (roasted broccoli → roasted cabbage, strip and
  URL both changed).
- **Possible improvement:** either label the control as a subject change
  ("Next dish: roasted cabbage ▸"), or make it local to Taste Circle (the
  E1a variant for this control only). Decide alongside the E1a/E1b question.
- **Confidence:** high that it happens; medium that users hit it.

### M2 · The Map has no legend and no keyboard route (R1 B4, D12, E1 limitation) — accessibility
- **Observed:** four node types are distinguished only by shape and colour.
  There is no key on the page, the canvas is not keyboard-operable, and the
  labels are about 6 px at 1400 px and absent at 390 px.
- **Consequence:** the Map is unusable without a mouse and good vision, and
  its meaning is unrecoverable without prior knowledge.
- **Evidence:** `desktop/5-map`, `narrow/5-map`.
- **Possible improvement:** a text legend, as Taste Circle already has. A
  text alternative already exists in Journeys and the cards, so link to it
  from the Map ("Same information as a list → Journeys"). No graph changes.
- **Confidence:** high.

### M3 · The tasting confirmation gives developer instructions (N5) — data safety and clarity
- **Observed:** after "Save permanently" the message reads "Saved to
  C:\…\tastings.yaml. Commit that file to keep the record — it is the one
  the app rebuilds from."
- **Consequence:** the cook doesn't know whether the save worked or whether
  it will be lost unless they do something they don't understand. The real
  rule (the record stays on this machine; commit to share it) is not stated.
- **Evidence:** `tasks/T5-5`.
- **Possible improvement:** lead with the outcome ("Saved. It now appears in
  the trial history below."). Put the file and commit detail in smaller,
  secondary text for the project owner.
- **Confidence:** high.

### M4 · Contradictory pairing labels on one card (N7) — correctness as perceived
- **Observed:** Roast lists "garlic — not paired here yet" and, two rows up,
  "garlic confit — missing but useful".
- **Consequence:** the cook holding garlic can't tell whether to use it.
- **Evidence:** `task-logs/T1-2-after-on-hand.txt`.
- **Possible improvement:** when an on-hand item is the base of a suggested
  filler, say so ("garlic → make garlic confit").
- **Confidence:** high (observed); fix shape uncertain.

---

## Critical comprehension failures (Clarity)

These stop a newcomer from understanding what the screen is telling them.

### C1 · Emphasis points away from the answer on the landing screen (N1)
- **Observed:** the accent border marks rank 1 (Raw Assemble). "● The dish
  you are investigating" marks card 2 (Roast). The picker says "broccoli",
  the strip "roasted broccoli". With on-hand items, rank 1 is the card that
  uses them least.
- **Consequence:** the first card a newcomer reads is neither their subject
  nor their best match. "What is the app recommending?" has three visual
  answers.
- **Evidence:** `desktop/1`, `tasks/T1-2`.
- **Possible improvement:** one emphasis only. Either the investigated dish
  or the best match for the on-hand items gets the border, not rank order.
- **Confidence:** high (observed); impact predicted (test T1).

### C2 · The answer to "what can I make with what I have?" is a sub-row (N2)
- **Observed:** "Routes with what you have — Creamy and acidic: yogurt, lemon
  · also needs dill" is row 9–11 of card 2. No summary appears near the
  on-hand box or the strip.
- **Consequence:** T1 is reachable but predicted hard to *find*. The
  on-hand box's effect is spread thinly across 5 cards × 4 new rows.
- **Evidence:** `tasks/T1-2`, `T1-3`, task log.
- **Possible improvement:** a one-line answer above the cards when items are
  on hand. Built from data the cards already compute, it would read: "With
  yogurt and lemon: roast it, dress it creamy and acidic (add dill)." See
  the smallest experiment below.
- **Confidence:** high (observed); impact predicted.

### C3 · One concept, four-plus names; about 20 coined terms on first screens (D6, still open)
- **Observed:**
  - The same prepared thing is called a component (tab), "something you
    already cooked", "transformed state", "prepared state" and "the dish you
    are investigating".
  - Other first-screen terms include branch, Raw Assemble, HIGH, hard gaps,
    soft flags, target roles, body, mild base, attested, analogy rules,
    corpus, append-only.
- **Consequence:** each screen must be learned separately. Cross-screen
  links (E1's whole point) are invisible when the names differ.
- **Evidence:** `first-impressions.md` per-view "Terms" rows.
- **Possible improvement:** one user-facing word for a prepared state
  ("dish" or "cooked …"), used in tab name, eyebrow, Scout picker and strip.
  Remove one-screen jargon first (as D6 proposed).
- **Confidence:** high (observed); which word works is for users to say.

### C4 · The Map's default view answers no question (B1, S5)
- **Observed:** about 70 nodes on arrival, no focus, dragging is the only
  invited action, and it is presented as a peer of Journeys.
- **Consequence:** a newcomer can't tell what it's for or what to do. It
  reads as decoration or as a puzzle.
- **Evidence:** `desktop/5-map`; `progressive-disclosure.md`.
- **Possible improvement (no graph change):** frame it as an overview ("See
  how broccoli's options connect"), and offer it from the cards rather than
  as a first-class destination. R1's R3 (focused default) stays the later,
  larger option.
- **Confidence:** medium. That it is unclear is observed; how it is used is
  untested.

## Minor comprehension issues (Clarity)

| ID | Observed → consequence | Evidence | Possible improvement | Confidence |
| --- | --- | --- | --- | --- |
| C5 | Plate Balance opens on an unlabelled example plate, and its KPIs (3 / 0 / 3.5) precede the plain answer → the user can't tell the plate is an example, and reads numbers before advice | `desktop/3`, `tasks/T2-1` | label it "Example plate — change it"; answer before tiles | high / predicted |
| C6 | Taste Circle counts sentence (8 / eleven / "this destination") and unlabelled "40 / 56" → numbers without meaning | `desktop/4` | one count, or none | high |
| C7 | Scout banner uses "analogy rules", "transformed states", "corpus" → the first words of Experiment are researcher terms | `desktop/7` | plain caution: "Untested ideas, reasoned from similar pairings. Try a small amount first." | high |
| C8 | Journeys marker "● Built on the dish…" sits between cards → ambiguous ownership | `desktop/6` | attach it inside the card | medium |
| C9 | Section names describe modes, not questions; Explore / Experiment are near-homonyms (S2) | first look | test question-first entry (navigation-comparison) | low |

## Usability

| ID | Observed → consequence | Evidence | Possible improvement | Confidence |
| --- | --- | --- | --- | --- |
| U1 | Suggestion chips are not actionable; clickable "Other candidates" look like text (N6) → no next step from a suggestion, and the hidden step goes unseen | `desktop/1,2,7` | give actionable items a button look and keep tags as tags; link "Use in" / journeys where a target exists | high / predicted |
| U2 | "What do I have" can't be edited on Explore (strip shows it read-only) → a cook on Journeys must leave to change it | `desktop/5,6` | show the box on all sections, or link "change" in the strip | high |
| U3 | Journeys' "continue into the crushed-broccoli journey" is plain text → a dead end | `desktop/6` | an in-page anchor | high |
| U4 | Verdict defaults to "Works" (N11) → a hurried save records an unchosen success | `tasks/T5-4`, `_tasting_reset` | no default; require a choice | high; mitigated by the review step |
| U5 | Escape clears the on-hand list; the multiselect loses focus between picks (known) → lost input | E1 limitations | keep on the Streamlit upgrade watch list | high |

## Consistency

| ID | Observed | Evidence | Possible improvement | Confidence |
| --- | --- | --- | --- | --- |
| K1 | Three look-alike pill levels (section, tab, view/mode) (D5) | `desktop/1,4,5` | a visibly smaller control for view/mode toggles | high |
| K2 | Confidence vocabulary: HIGH, MEDIUM HIGH, ATTESTED HIGH, dotted chips, "strength of this argument" | `desktop/1,2,7` | one scale, one wording, one legend | high |
| K3 | Title Case route names and raw id `olive_oil` (N10) | `desktop/2` | sentence case; pretty names | high |
| K4 | Map and Taste Circle use colour differently, and only one has a legend (D12) | `desktop/4,5` | share Taste Circle's convention | high |

## Reliability

| ID | Observed | Evidence | Possible improvement | Confidence |
| --- | --- | --- | --- | --- |
| L1 | The previous view lingers faded after a tab switch (N4) | first 4-taste-circle capture | measure interactively; consider a lighter first render for Taste Circle | medium |
| L2 | Tab out of a selectbox shows the wrong value (pre-existing) | E1 limitations | focused follow-up already noted | high |
| L3 | Stale frame after a rapid double save (known) | E1 limitations | — | high |

## Polish (design preference)

- The large initial disc (B / RB) costs a fifth of the narrow first screen.
- "Download .md" placed between the answer and the routes.
- "Surprise me" as Taste Circle's primary button.
- Monospace helper captions read as code.
- The tab row wraps raggedly at 390 px (D22).

---

## Elements to preserve

1. **Taste Circle's layering:** one subject, an instruction, a legend, and
   alternatives on click. It is the model for the rest.
2. **Scout's structure:** answer → why → two separate claims → smallest test
   → record → history.
3. **Honest absence copy:** "Not paired here yet", "absence here means nobody
   has written one", "Too rare to tell… Finding none proves nothing".
4. **Journeys' prose:** "Choose this route for…" and "Watch for".
5. **The context strip and shared subject** (E1). M1 is a reason to bound
   them, not to remove them.
6. **The tasting review step**, with the ratio prefilled from the smallest
   test.

---

## Completion questions

1. **Is the purpose understandable?**
   - Partly. The domain (cooking, ingredients) is clear at once.
   - The *job* is not: the subtitle lists three, in app vocabulary.
   - Screens that state one purpose (Taste Circle, Scout, Journeys, Component
     Explorer) are understandable. The landing screen and the Map are not.
2. **Is the next action identifiable on each screen?**
   - **Yes:** Taste Circle (click a dimension), Scout (smallest test /
     record).
   - **Partly:** Component Explorer (next moves, but as text), Plate Balance
     (fillers, but not addable), Journeys (prose).
   - **No:** Ingredient Explorer (nothing clickable on the cards), Map (drag
     only).
3. **What are the most confusing concepts or navigation?**
   - The many names for a prepared state.
   - Emphasis on the landing screen that points away from the subject.
   - Explore vs Experiment.
   - Look-alike pill levels.
   - The Taste Circle arrow that moves the whole app's subject.
4. **Too much information too early?**
   - **Yes**, on the Ingredient Explorer (5 cards × 8–11 rows) and the Map
     (about 70 nodes).
   - **No**, on Taste Circle and Scout, which show the same depth in layers.
   - So the problem is ordering, not volume.
5. **Would question-first navigation help?** Probably for first-time
   orientation (T1, T3 and T5 start from tool names that do not name the
   question), and probably not for repeat use. A hybrid (questions as entry
   points and tool descriptions, rails kept) is supported. Replacement is
   not. This can be tested with existing deep links and no code (test pack,
   optional comparison).
6. **Which elements should be preserved?** See the list above.
7. **What should be tested with real users?**
   - T1's findability (C1, C2).
   - Whether the strip and the investigated-dish marker are noticed (S1).
   - Whether chips are clicked (S3).
   - What people think the Map is for (S5).
   - Explore / Experiment guesses (S2).
   - The question-card entry vs rails.
   - Everything is in [usability-test-pack.md](usability-test-pack.md).

---

## The three most consequential problems

1. **The landing screen's emphasis and answer placement (C1 + C2).** It is
   the first screen everyone sees and the screen for the most common task
   (T1). The answer exists but sits in a sub-row of the second card, under a
   bordered card that is neither the subject nor the best match.
2. **Vocabulary fragmentation (C3).** About 20 coined terms and four-plus
   names for the central object undo the shared-context work. Users can't
   see that the views are about the same thing.
3. **A shared subject that can move silently (M1).** E1's main gain (one
   subject everywhere) becomes a liability when a tooltip-only arrow changes
   it, with no history to undo.

## The smallest useful experiment

**Run sessions 1–3 of the test pack before changing anything.** It costs no
code, uses the build as it is, and decides whether C1/C2 (findability) and
S1 (strip noticed) are real.

If T1 fails or stalls for two or more of three participants, the smallest
**code** experiment is **E3 · answer line**, on the Ingredient Explorer only:

- **When:** items are on hand.
- **What:** one sentence above the cards, built only from data the cards
  already compute (the routes with what you have, plus missing items).
- **Emphasis:** the accent border moves to the card that sentence names.
  No other card changes.
- **Measure:** rerun T1 with 2–3 new participants, comparing time-to-answer
  and whether the answer they give uses what they have.
- **Does not touch:** navigation, the Map, vocabulary, or other views.
