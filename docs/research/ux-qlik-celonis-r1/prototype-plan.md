# Prototype plan — research round 2 (proposed)

Three small experiments, each a throwaway prototype on its own branch, each
tested with **3–5 people who have not seen the app**, using the existing task
scripts plus one task per experiment. Smallest first. Nothing proceeds without
review of this plan.

Common rules:
- No changes to culinary logic, data or rules; no new dependencies.
- Measure with observation: task success, wrong turns, re-picks, and
  think-aloud quotes. No invented scores.
- Each experiment answers one question and has a stop condition.

---

## E1 · Shared subject (from R1) — *the smallest meaningful experiment*

**Question:** Do people expect the dish they're working on to follow them
between views, and does carrying it cut re-picking without surprising them?

**Prototype:** a single "current subject" set by any view's picker; other
views open on it (state → its ingredient where needed). A one-line context
strip on every view: *"Roasted broccoli · you have lemon, garlic"*. Two
variants on one switch:
- **E1a, default only:** other views open on the subject but keep their own
  picker afterwards.
- **E1b, linked:** changing the picker anywhere moves the subject everywhere
  (Qlik-like).

**Task:** "You roasted a tray of **cabbage** (not broccoli: defaults must not
hide the effect). Find something to add from what you have (lemon, garlic),
then build a dish around it, then see where it could go."

**Observe:** re-picks per participant; whether anyone is surprised that a
view changed (E1b) or didn't (E1a); whether the context strip is noticed.

**Stop / decide:** if E1a removes re-picking with no surprise, ship E1a
and drop E1b. If people miss the link, try E1b.

**Cost:** low. One session-state key, read at six pickers; one strip.

---

## E2 · Show the reasons (from R2 + R4)

**Question:** Does seeing *why* an idea was rejected, and *that* an untested
idea exists, help people trust and use Scout without mistaking ideas for
recommendations?

**Prototype:** Scout requests rejected hypotheses and shows them collapsed,
grouped by reason ("written for soup", "written for mash"…). On Cook cards,
where a Scout hypothesis exists for an item marked "Not paired here yet", add
"untested idea in Scout →".

**Task:** "Is miso a good idea on roasted broccoli? And mango?"

**Observe:** do people distinguish miso (untested idea) from mango (nothing
known)? Does anyone describe the Scout marker as "the app recommends miso"?
Do the rejection reasons get read, and do they make sense?

**Stop / decide:** if anyone reads the marker as a recommendation, keep the
reasons and drop the marker.

**Cost:** low. One call-site argument; one marker in card rendering.

---

## E3 · Focused Map (from R3)

**Question:** Does a Map that starts from one state and expands on click
answer "what can roasted broccoli become?" faster than the full graph, and
do people still want the full view?

**Prototype:** the Map opens on the current state (E1's subject if available)
and its direct neighbours only, with a legend. Clicking a node reports to the
app (the component already supports it): a side panel shows its details,
"comes from / goes to" lists, and an *Expand* button. *Show everything*
restores today's graph.

**Task:** "What can roasted broccoli become, and what would you serve it
with?" Run against today's Map as a baseline with half the participants.

**Observe:** time to a correct answer; whether anyone uses *Show everything*;
whether the panel or the graph carries the answer.

**Stop / decide:** if participants answer from the panel and ignore the graph,
the lesson is "link to cards", not "redesign the graph". Fold that into R5
instead.

**Cost:** medium. Click handling and a panel; the graph engine is unchanged.

---

## Order and dependencies

1. **E1 first.** It's cheapest and removes the cost that would contaminate the
   other two: every task otherwise starts with re-picking.
2. **E2** in parallel or next; it's independent and tiny.
3. **E3** last; it benefits from E1's shared subject.

## Not in this round
Question-led home screen, selection history, merging tabs, graph-engine
changes: see the rejected list in [recommendations.md](recommendations.md).
