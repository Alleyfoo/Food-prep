# Progressive disclosure — five surfaces against five levels

**The five levels** (from the brief):

1. **Essential answer** — what to do, in one line.
2. **Next action** — what to click or cook next.
3. **Explanation** — why.
4. **Alternatives** — what else would work.
5. **Evidence** — confidence, sources, history.

**Good disclosure** shows L1–L2 first, offers L3 on request, and keeps L4–L5
one step away. Each surface below is rated on **what is shown at first
sight** (above the fold at 1400 px, default state). The ratings are
qualitative, not numerical scores.

## Summary

| Surface | L1 answer | L2 next action | L3 why | L4 alternatives | L5 evidence | Pattern |
| --- | --- | --- | --- | --- | --- | --- |
| Ingredient cards | buried | none (chips not clickable) | shown at once (tags, risks) | shown at once (5 cards) | shown at once (HIGH, dotted chips) | **everything at once** |
| Journeys | first (title + "Choose this…") | text only | shown at once, but readable | shown at once (4 journeys) | absent | **narrative, front-loaded** |
| Taste Circle | first (subject + dimensions) | first (click a dimension) | on request (fan, side panel) | on request (options per dimension) | absent | **layered, the model to keep** |
| Map | absent | absent (drag only) | implicit in edges | everything | absent | **evidence without an answer** |
| Scout | first (pairing title) | shown (smallest test, record) | shown (two sentences) | on request (next hypothesis, candidates) | shown (claims, history) | **layered; order is right** |

---

## Ingredient cards (Ingredient Explorer; same renderer in Taste Circle › Cards)

**At first sight:**
- Five cards, each with technique, state, confidence pill, sensory line,
  TAGS, RISKS, MISSING, TRY (by role) and USE IN.
- With on-hand items entered, also AVAILABLE NOW, MISSING BUT USEFUL, NOT
  PAIRED HERE YET and ROUTES WITH WHAT YOU HAVE.

**Problem:**
- L1 (what to cook) and L5 (confidence, tags) share the same visual level.
- L4 (four other techniques) is fully expanded *before* L1 is settled.
- The row that answers T1 is the 9th of 11 on the second card.

**What already exists that could carry layering (no change made):**
- The "Best branches / Choose technique" mode is a natural L4 switch.
- The "● The dish you are investigating" marker is a natural L1 anchor.
- The sensory line is a natural one-line L1.

## Journeys

**At first sight:** four complete journeys, each with title, chain, result,
additions and watch-for.

**Strengths:**
- The best L1+L3 writing in the app ("Choose this route for…").
- "Watch for" is a valuable, rare L3.

**Problems:**
- The six-step chain (L3) sits between the title (L1) and the "Choose this…"
  sentence, which is the real L1. It wraps over three lines, so its
  left-to-right logic is lost.
- L2 ("continue into the crushed-broccoli journey") is prose, not a control.
- There is no L5 at all. That may be acceptable, since journeys are curated.

## Taste Circle

**At first sight:** the subject in the centre, 11 dimensions as nodes
(provided / N options / thin), a legend, and the instruction "Click a
dimension…". The side panel says "Nothing expanded".

**Why it works:**
- One answer is visible (what this dish already has).
- One action is named.
- Alternatives (options per dimension) appear only on click.
- The side panel reflects the state ("Your dish").

**Weak points:**
- The counts sentence ("0 of 8 open… does not need all eleven… this
  destination") mixes three numbers.
- The ◀ ▶ subject stepper changes the shared subject, labelled only by a
  tooltip.
- "Surprise me" is the primary button.

## The relationship Map

**At first sight:**
- The full graph for the ingredient: about 70 nodes, four node types
  distinguished by shape and colour, dashed and solid edges with tiny edge
  labels, and no legend.
- The subject is marked by a dark ring. At 390 px there are no labels.

**Is the default view understandable?** At default zoom, **no**. The
reviewer could not read node labels at 1400 px without zooming, and could
find the subject only through the hint sentence. Shapes and colours have no
key on the page (R1 B4, still open).

**Better suited to exploration or navigation?** **Exploration.**
- **Navigation** needs a starting node, a readable neighbourhood and a way to
  act on a node. The Map gives none of these at default zoom; dragging is
  the only invited action.
- **Exploration** needs breadth and the "shape" of the space. The Map does
  give an immediate sense that broccoli fans out into five states, each with
  fillers and destinations. That is a real L4/L5 value: it shows how much
  there is.

**Conclusion:** the Map is an **evidence / overview layer (L4–L5) presented
as if it were a destination**. It is reached as a peer tab of Journeys, with
no question it answers first. **No graph changes are proposed here.** What to
test (see the test pack): ask users what the Map is for after 30 s, and
whether they would use it to *find* something or to *look around*.

## Scout

**At first sight:**
1. Caution banner.
2. Pairing title (L1).
3. Two-sentence reason (L3).
4. Two claims, Compatibility and Novelty (L5 written as L3).
5. Smallest test (L2).
6. Next hypothesis / Record a tasting (L2).
7. Trial history (L5).

**Strengths:** the order is right. Answer, then reason, then how to try it,
then the evidence. Alternatives (other candidates, next hypothesis) are one
click away.

**Weak points:**
- The banner opens with researcher terms ("analogy rules", "transformed
  states").
- "Strength of this argument: medium high" re-introduces a score inside the
  claims.
- The analogy source ("roasted broccoli with olive oil" for cabbage + brown
  butter) is L5 evidence placed at L1 prominence, with no route between the
  two.

---

## Cross-cutting findings

1. **The app already has two good disclosure models** (Taste Circle, Scout)
   and two that show everything at once (ingredient cards, Map). The good
   ones are the screens that read best in first impressions.
2. **Chips are used at every level** (answer, alternative, evidence). In the
   clear screens, levels are separated by *layout* (centre / fan / panel;
   title / claims / test). In the dense ones, the chip is the only unit, so
   nothing separates levels.
3. **L2 (next action) is the weakest level overall.** Suggestions are text,
   not links, and the one strong action button in Cook (Taste Circle) is
   random ("Surprise me").
