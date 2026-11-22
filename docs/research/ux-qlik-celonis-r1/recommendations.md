# Recommendations

Opportunities ranked by **(evidence of the problem) × (benefit) ÷ (cost and
risk)**. Each names the transferable pattern, what it would preserve, and what
stays uncertain. **Nothing here is implemented.** The next step needs review
(see [prototype-plan.md](prototype-plan.md)).

## What Food-prep already does well

1. **Explaining why.** Journeys' causal chains, route "fit" text and Scout's
   separate Compatibility / Novelty / Result claims go further than either
   reference documents. Qlik explains through colour alone; Celonis through
   statistics.
2. **Honest absence.** "Not paired here yet", "absence here means nobody has
   written one", "Too rare to tell": missing evidence is never presented as
   incompatibility.
3. **Progressive disclosure where it was designed in.** Taste Circle's
   expand-one-dimension fan is the same move as Celonis's "add detail on
   demand", and it is the app's most legible screen.
4. **One working global selection.** The on-hand list already behaves like a
   Qlik selection: set once, respected by five views.
5. **A clear Cook/Scout boundary**, which neither reference needs but which
   this domain does.

## Where the current model creates unnecessary work

- Re-picking the subject in every view (A1). It's the most frequent cost, and it
  is invisible in testing because every default is broccoli.
- Hunting for one object's properties across three views (B3).
- Reading a full graph before seeing the part that matters (B1).
- Visiting three sections to learn whether a pairing is unknown, experimental
  or unsuitable (C2).

## Prioritised opportunities

### R1 · Shared subject across views — *high priority*
- **Pattern:** Qlik P1 (global selection), applied to one thing only.
- **Proposal to test:** one "current subject" (an ingredient, optionally a
  state) that views open on, with each view's picker still able to change it.
  Choosing roasted broccoli implies broccoli where a view needs the ingredient.
- **Preserves:** each view's own controls and state (Taste Circle's dish).
- **Evidence:** observed (A1, probe). **Benefit:** hypothesis.
- **Risk / uncertainty:** whether a picker change in one view should move
  the others or only set a default. Qlik moves everything; that may surprise a
  cook who is comparing two states. Settling that is the experiment's job.

### R2 · Show why ideas were rejected — *high priority, smallest change*
- **Pattern:** Qlik P2/P3 (excluded values as information).
- **Proposal to test:** let Scout show its rejected hypotheses, which it
  already computes along with their reasons (45 for roasted broccoli), behind
  the existing expander.
- **Preserves:** Scout's one-at-a-time flow; rejects stay collapsed.
- **Evidence:** observed (dead code path, C3).
- **Uncertainty:** whether 45 reasons help or overwhelm; grouping by reason may
  be needed.

### R3 · Focused graph with expansion — *medium priority*
- **Pattern:** Celonis P7 (baseline first, add on demand) + P8 (inspect a
  node with from/to).
- **Proposal to test:** the Map opens on one state and its direct neighbours;
  clicking a node shows its details and neighbour lists and can expand it.
  The full graph stays one control away.
- **Preserves:** the existing graph engine and component (clicks already
  reach Python for the Taste Circle).
- **Evidence:** observed (B1, B2, measured label sizes).
- **Uncertainty:** whether cooks use the Map at all once cards and journeys
  carry the subject; the Map may matter less than its size suggests.

### R4 · Distinguish four statuses in Cook — *medium priority*
- **Pattern:** Qlik's state vocabulary (P2), not its colours.
- **Proposal to test:** on Cook cards, keep "Not paired here yet" for unknown,
  and add a quiet *"untested idea in Scout →"* marker where a hypothesis
  exists. Surface the existing `unsuitable_provided` and "Avoid when" where they
  apply.
- **Preserves:** Scout ideas are never presented as Cook advice.
- **Evidence:** observed (C2, miso vs mango).
- **Uncertainty:** whether any pointer to Scout reads as endorsement.

### R5 · Link the three representations — *lower priority*
- **Pattern:** Celonis P12 (aggregate graph beside path views) + P8.
- **Proposal:** "See in Map" on a journey or component card; "Open card"
  from a Map node. Depends on R1 (a shared subject makes links trivial).

### Small fixes noticed (not experiments)
- Remember the last tab per section (A3).
- Keep the on-hand list visible (read-only) on Explore while it applies (A2).
- Add a non-colour cue for on-hand items (C4); a Map legend (B4).
- Readable tooltips (no raw ids).

## Rejected or deferred ideas

| Idea | Why not now |
| --- | --- |
| Full Qlik selection model (every field selectable, green/white/grey everywhere) | Built for analysts slicing tables; a cook has one or two things in mind. The *vocabulary* of states transfers (R4); the mechanics would add load. |
| Selection history with step back/forward (Qlik P4) | Stakes are low and Streamlit makes it costly; revisit only if R1 makes people lose their place. |
| Locks (Qlik) | No scenario found where a cook needs to protect a selection. |
| Measure switching on the graph (Celonis P10) | Food-prep has no throughput-like measure worth toggling; confidence is already shown. |
| Multi-object sliders (Celonis P11) | Evidence is one community post; node types here are few and fixed. |
| Merging tabs into fewer screens | The brief warns against it, and no evidence says screen count is the problem; context loss is. |
| Question-led home screen ("What are you trying to do?") replacing tabs | Sections already approximate intent. Test only after R1, because re-picking would undermine any question-led entry. |
| Replacing the graph engine | Excluded by the brief and unnecessary; the component already supports clicks. |

## Remaining uncertainties
- All benefits above are hypotheses until the task scripts run with real
  people (`docs/usability/task-scripts.md`).
- Celonis behaviour is taken from legacy 4.x docs; current and multi-object
  behaviour is unverified because the docs are sign-in gated.
- Whether cooks think in ingredients or in states may decide how R1 behaves.
