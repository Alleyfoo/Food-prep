# Comparison matrix — ten criteria

**Confidence** reflects evidence, not importance: *observed* = seen in the
running app or code; *documented* = read in official docs; *legacy* = Celonis
4.6/4.7 docs only; *hypothesis* = needs real users. No scores. Qlik and Celonis
are described from documentation, not from hands-on use.

Pattern ids (P1–P12) refer to [reference-research.md](reference-research.md);
finding ids (A1, B2, C3…) to [workflow-evaluation.md](workflow-evaluation.md).

---

### 1. Discoverability
- **Food-prep:** sections named by intent (Cook / Explore / Experiment); tab
  names are nouns of the data (Component Explorer, Filler Profiles). No search.
- **Qlik:** smart search from any sheet; the selections tool lists every field (P5, P6).
- **Celonis:** one Process Explorer entry per analysis; sliders always visible (P7).
- **Assessment:** sections are a strength. Inside them, the cook must know the
  data model to choose a tab. Nothing finds "roasted broccoli" across views.
- **Possible improvement:** a single subject search that lands in the right
  view.
- **Evidence:** observed (structure); hypothesis (whether names confuse).

### 2. Navigation
- **Food-prep:** every view is self-contained; one cross-link (Filler →
  Ingredient Explorer); a section switch resets to the first tab (A3).
- **Qlik:** sheets are free to switch; selections follow (P1).
- **Celonis:** graph → details → connection → activity, circularly (P8).
- **Assessment:** following a question across views means re-entering it.
  Graph, cards and journeys describe the same objects with no links (B3).
- **Possible improvement:** "open this in…" links between views for the same
  subject; remember the last tab per section.
- **Evidence:** observed.

### 3. Context preservation
- **Food-prep:** one global selection (on hand); six independent subject
  pickers (A1); per-view state is kept (Taste Circle's dish and open fan
  survived a round trip).
- **Qlik:** "Selections are global", across sheets (P1).
- **Celonis:** filters and hidden activities apply to the whole analysis (P9; legacy).
- **Assessment:** the largest gap found. The on-hand list proves the pattern
  already works here; the subject simply was not given the same treatment.
- **Possible improvement:** one shared "current subject" (ingredient + state)
  that views read, with each view still able to override it.
- **Evidence:** observed (probe output).

### 4. Relationship clarity
- **Food-prep:** typed, coloured nodes and labelled edges, but no legend (B4);
  labels ≈6.6 px at the default fit; raw-id tooltips.
- **Qlik:** associations shown through state colours in every list (P2).
- **Celonis:** "Cases come from / go to" lists make neighbours explicit (P8; legacy).
- **Assessment:** the data model is rich and the encoding is consistent; the
  screen does not explain it.
- **Possible improvement:** a legend; a neighbour list for the focused node.
- **Evidence:** observed (measured).

### 5. Progressive disclosure
- **Food-prep:** strong in cards (top 5 branches, expanders, Scout one at a
  time) and Taste Circle (fan on demand, paging). Weak in the Map: everything
  at once (B1).
- **Celonis:** baseline path first, then *More* one step at a time (P7; legacy).
- **Qlik:** charts reduce as selections narrow (P1).
- **Assessment:** the Taste Circle already does the Celonis move (show
  dimensions, expand one). The Map does not.
- **Possible improvement:** open the Map focused on one state with its direct
  neighbours, and expand outward on request.
- **Evidence:** observed.

### 6. Feedback
- **Food-prep:** availability partition and route rows update on pick; Taste
  Circle rail narrates ("lemon is in your kitchen"); Map clicks change only
  edge weight.
- **Qlik:** state colours change everywhere; the selections bar shows what
  is active (P2, P5).
- **Celonis:** a details panel on every click (P8).
- **Assessment:** good where it exists (Taste Circle is the best). There's no
  summary of "what is currently applied", and the on-hand list vanishes on
  Explore while still applying (A2).
- **Possible improvement:** a persistent context line ("Roasted broccoli · you
  have lemon, garlic") on every view.
- **Evidence:** observed.

### 7. Explanation
- **Food-prep:** best in class for *why it works*: journeys' causal text,
  route "fit", Scout's two separate claims. Weak for *why not*: 45 rejection
  reasons hidden (C3); unrecorded and experimental items look the same in Cook
  (C2).
- **Qlik:** light vs dark grey says what excluded a value (P3).
- **Celonis:** occurrence statistics per node (P8; legacy).
- **Assessment:** an existing strength, plus one switched-off feature that
  would cover the gap.
- **Possible improvement:** show rejected Scout ideas with their reasons; in
  Cook, mark "untested idea in Scout" separately from "nothing recorded".
- **Evidence:** observed.

### 8. Cognitive load
- **Food-prep:** vocabulary to learn: component, state, filler, route,
  destination, role, Cook/Scout. Eight tabs over three sections. The ingredient
  vs state distinction is fundamental and unexplained at the point of choice (A4).
- **Qlik / Celonis:** both expect trained analysts; neither is a model for a
  home cook.
- **Assessment:** lower than either reference for the core tasks (cards read
  plainly) and higher than needed for moving between them.
- **Possible improvement:** carry the subject (removes re-picking) before
  adding any new concept.
- **Evidence:** observed (vocabulary); hypothesis (actual difficulty).

### 9. Error recovery
- **Food-prep:** Reset in Taste Circle; clear the on-hand box; no undo, no
  history; changing the state resets the Taste Circle dish without warning.
- **Qlik:** step back / forward through the session; clear all except locked (P4).
- **Celonis:** *Reset* on sliders (P7; legacy); filter removal **unverified**.
- **Assessment:** low stakes (nothing is written except tastings, which are
  append-only by design), so full history is probably not worth its weight.
- **Possible improvement:** warn before a subject change wipes a built dish.
- **Evidence:** observed; benefit of history is a hypothesis.

### 10. Visual readability
- **Food-prep:** cards follow a 14 px floor and a consistent palette. The Map
  breaks it badly (6.6 / 5.6 px labels at fit). On route cards, availability is colour-only (C4).
- **Qlik / Celonis:** not assessed visually (no access).
- **Assessment:** the cards and Taste Circle are the app's visual strength;
  the Map is the exception.
- **Possible improvement:** fewer nodes per view (see 5) before any styling
  change; add a non-colour cue for "you have this".
- **Evidence:** observed (measured).

---

## Summary

| Criterion | Food-prep today | Biggest lever |
| --- | --- | --- |
| Discoverability | sections good, tabs data-named, no search | subject search |
| Navigation | views are islands | links between views |
| Context | on-hand global, subject not | shared subject |
| Relationships | rich model, unexplained graph | legend + neighbours |
| Disclosure | cards/Taste Circle good, Map all-at-once | focused Map |
| Feedback | strong locally, no "what's applied" | context line |
| Explanation | strong "why", hidden "why not" | show rejections |
| Cognitive load | plain cards, too much re-picking | shared subject |
| Recovery | low stakes, minimal tools | warn before wipe |
| Readability | cards good, Map illegible at fit | focused Map |
