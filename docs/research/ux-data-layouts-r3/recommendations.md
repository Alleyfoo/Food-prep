# Recommendations: R3 data presentation

## Acceptance question: did we find a better way to represent and navigate the data?

**Yes, for most data tasks, with one caveat: no person has used it yet.**
The evidence is structural. The layouts can express things the cards cannot:
- tasks the cards **cannot** answer: scanning for routes without items on
  hand (K1), and recorded vs idea vs tested (K5);
- tasks they answer only by scrolling across preparations: compare (K2),
  trace (K3) and on-hand filter (K7).

Each of these became direct in at least one alternative structure
([readability.md](readability.md)).

**No single layout is the answer.** The finding is a *combination* matched to
the data's shape ([information-structures.md](information-structures.md)):

| Data task | Use |
| --- | --- |
| Scan, filter, compare many | **table / matrix** |
| Compare two or three | **pivot** |
| Trace from an ingredient, follow a chain | **graph with a neighbour list** |
| Explain one record, tell fact from idea, see its gaps | **fact sheet** |

## Proposed structure to test next (not built)

One **overview/detail workspace** per ingredient:

1. **Overview = the associative table.**
   - Rows are prepared ingredients.
   - Two switchable column sets: *attributes* and *needs × roles*.
   - Filters grey rows out with the reason.
   - Gaps shared by every row are stated once, above the table.
2. **Detail = the fact sheet**, for the selected row, with fixed sections:
   - attributes;
   - needs and pairings;
   - routes with *why it fits*;
   - evidence;
   - ideas, labelled "not recommendations";
   - not recorded.
3. **Compare = pivot**, when 2–3 rows are selected. It replaces the sheet.
4. **Trace = relationship panel on demand.** Clicking any ingredient name
   (lemon, brown butter) opens the graph and neighbour list focused on it,
   with the step control. The graph is a tool for tracing, not the home
   view.
5. **One status vocabulary everywhere:** curated · on hand · source · idea ·
   tested · not recorded. It is a field in the data model, not styling.

The cards would then be replaced by the fact sheet, which holds the same
facts plus the sections cards lack. E3's answer-first panel could sit above
the overview as a derived summary. Whether it still earns its place once the
table exists is an open question.

## What is *not* recommended

- **A graph as the main view.** It is the only structure for tracing (K3),
  but it can't scan (K1) or compare (K2), and it fills with ideas on
  incomplete records.
- **Cards for cross-record work.** Every cross-preparation task becomes a
  3–4.5-screen scroll.
- **Declaring any of the three "optimal".** Each lost at least one task
  outright.

## Issues the prototype surfaced (outside R3's scope, logged only)

| Issue | Where | Why it matters |
| --- | --- | --- |
| Cards print route elements recorded as *finish* under "also needs" | `render.routes_with_what_you_have_html` | Turns an optional garnish into a requirement. Representation defect. |
| `corpus_cooccurrence_count` is 0 on all 303 pairings | data build | Any "seen in recipes" claim for pairings would be empty. Don't display it until backfilled. |
| Pairing-level sources (288 links) are only counted, never named, in any view | query layer and UI | The missing piece for answering "why this pairing?" (K4). |
| Experimental pairings are invisible in the Cook views | by design (`fillers_by_role`) | Correct for recommending. For *reading the data*, they need to appear, labelled as ideas. |

## Open questions (for a desktop session with people)

1. Do people read the status labels, and can they tell *idea* from *tested*
   without being told?
2. Is the needs × roles matrix readable to someone who doesn't know what a
   "role" is, or does it need the attributes view first?
3. Do people find the trace panel when they need it, or does it need its own
   entry point?
4. With a table in place, does the answer-first summary (E3) still help, or
   does it duplicate the table?

A three-person desktop session on tasks K1–K7, comparing cards with the
proposed workspace, would answer these. It has **not** been run. Nothing in
this round is a user result.

## Next step

- Build the combined workspace (items 1–5 above) as one desktop prototype,
  still outside the product app, on the same model.
- Run K1–K7 with three people.
- Only then decide whether it replaces the Ingredient Explorer and Component
  Explorer.
- Responsive layout and polish come after the structure is settled.
