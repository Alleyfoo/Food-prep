# Visual representations for a person deciding what to cook (Q6)

This file synthesises `evidence-visualisation.md` (Y700-Y712), plus the
display remarks in the other evidence files. The current mindmap was read in
the code:
- `src/foodprep/ui/graph.py` (`build_ingredient_graph`, pyvis/vis.js,
  force-directed): ingredient → techniques → components → fillers, routes
  and destinations;
- `src/foodprep/ui/streamlit_app.py`.

No prototype was built.

## Starting fact

**The interface reads none of R3-R5.** A search of `src/foodprep/ui/` finds
no use of `constructions`, `transfers`, `conditions` or `from_state`. The
mindmap draws the older technique and component data, one ingredient at a
time.

Everything R3-R5 established is reachable only through the CLI:
- dishes as constructions;
- transfers with verdicts;
- whole sequences with checks;
- "from this state".

So R7's first job is not a new kind of picture. It is putting the existing
records where the cook looks.

## Which representation answers which question

The user is a home cook choosing dinner from familiar Lidl ingredients.
Four practical questions recur in the R1-R5 records and the brief:
- **Decide:** what can I make with this tonight, including unfamiliar uses
  of a familiar ingredient such as dried peas?
- **Cook:** what do I do next, and how do I know it worked?
- **Vary:** can I swap this, and what else changes?
- **Plan:** what can I prepare tomorrow from what I already have?

| Family | Question it answers | Evidence with people | R6 verdict |
| --- | --- | --- | --- |
| **F1 Ingredient relationship network** (Food-prep's mindmap; flavour and co-occurrence networks) | none of the four directly; "what goes with what" | none with cooks. Networks need filtering to be drawable (Y702). Hubs are drawn at the edge (Y701). Viewers over-read position and distance in node-link layouts (Y706). Node-link suits connectivity tasks, not lookup (Y705) | **not suited** as the decision view; keep it only as an exploration view |
| **F2 Outcome map** (what an ingredient can become; one dish's versions) | Decide | RecipeScape: analysts read clusters of one dish's recipes as "ways of cooking it" (Y700, analysts, not cooks). Grouped lists raise understandability and the diversity people see (Y708, hypothetical choice) | **extend**: outcome-first, as a few labelled groups, not a 2-D similarity map |
| **F3 Material transformation graph** (state chains) | Cook, Plan (where am I in the chain) | goal-state pictures were liked but reduced neither problems nor errors (Y703; that condition was not read in full) | **insufficient evidence**; show states inside F4's branches, not as a graph of their own |
| **F4 Activity or process overview** (one branch per component, joins, ingredients beside their steps) | Cook, Plan | **the only representation tested with people cooking**: in a study of 24 participants (university students, 8 per condition), cooks preferred the overview because it let them understand the process and plan parallel work. It reduced problems arising from the recipe's content, including errors on a step that mixed two components. It made no difference to the time taken (Y703 ch. 7; checked in raw text, see `limitations.md`) | **adopt the concept** |
| **F5 Alternative-route view** | Vary (which way suits my oven and time) | aligned, item-wise layouts beat separate side-by-side charts for finding local differences, in 15 studies outside food (Y707); pairwise comparison was used by analysts (Y700) | **adopt the concept**, on indirect evidence |
| **F6 Substitution and dependency map** | Vary (what else changes) | drawing dependencies apart removed one error type (Y703); substitute networks are statistics with no consequences (Y701) | data **already equivalent** (R4, R5); **extend** the display: a swap as a changed branch inside F4, aligned as in F5 |

A display warning: in a controlled study, a shown taste value shifted
people's ratings of recipes they had not tasted (Y712). A taste circle or
map therefore persuades as well as informs. That supports the project's
rule of no new scores. **Inferred:** the Taste Circle should say that it
shows documented pairings, not predicted taste.

## What the mindmap should expose (from ingredient relationships to dishes and routes)

These are recommendations, inferred from the evidence above and the R1-R5
data. None has been tested with the user.

1. **Make the outcome the second ring, not the technique.**
   - For an ingredient, show the documented dishes and transfers it enters,
     grouped as *familiar uses* and *less usual uses*. For dried peas:
     pea soup, and pea falafel.
   - Give each outcome its verdict and its one condition ("blanch only the
     rutabaga").
   - Techniques and components move inside the dish. This is what R4
     already said the useful unit is: a documented construction plus what
     is in the shop plus its one known failure.
2. **Open a dish as a component-branch overview (F4), not as more graph.**
   - One branch per independently prepared member, joining at the assembly.
   - The steps after the join stay visible per member: "the rice finishes
     in the roll", "the rutabaga: some give, or no resistance".
   - Each step carries its done-when check, marked *ready for the next
     step* or *ready to eat*.
   - The one dependency that explains a step is shown on that step
     ("blanch: the bake alone won't soften it in time").
   - All of this is R5 data.
3. **Show alternatives as aligned columns (F5), never as superposed paths
   in one force graph.**
   - Each documented route is a column with its sources and verdict, and
     the rejected route is a column too (K8).
   - Corresponding steps sit on one row, "none" where a route has no such
     step (`alternative-routes.md`).
   - An **unverified combination** never gets a column. It appears only
     when asked about, as a cell: *each part documented, the combination
     not*.
4. **Show a swap as a changed branch with its repair** (F6 inside F4):
   - "napa instead of cabbage: shave the rib; bake covered";
   - a refused swap stays visible with its reason (curly kale: no
     documented rolls; small leaves) rather than silently absent.
   - A context-free similarity display would endorse that swap (Y701,
     Y206).
5. **Start from a held state as an entry point.**
   - "I have cooked rice / soaked peas / blanched rutabaga" opens the
     overview of each route through that state.
   - The completed branch is marked done, so only the remaining branches
     show. Cooks rarely prepare everything first (1 of 24 in Y703).
   - Show how long the state keeps, and on whose authority (R5
     intermediates).
   - No evaluated interface of this kind exists (`evidence-visualisation.md`,
     Q5). It is the least supported recommendation here, and also the one
     closest to "help us make dinner".
6. **Keep three absences distinguishable in words:**
   - *not documented*;
   - *documented to fail*;
   - *not known*.

   R4.1 already showed that words beat coded marks for status. Whether
   cooks tell "unknown" from "fails" in a comparison is untested (Y707's
   studies compare known values).

## What only exposes complexity

- **The whole ingredient network**, or any force graph over about 20
  edges. R4.1 measured graphs above that size as illegible. Y702 had to
  filter its network to draw it.
- **Workflow and flow-graph notations** (BPMN, r-FG, FOON trees, ISA-88
  procedure charts). They are built for annotators, robots and plant
  operators. The r-FG authors say their graphs are not for display to cooks
  (Y500).
- **Multi-dish schedulers** (Y709, Y710). They minimise time, and no
  evidence shows that home cooks want a computed schedule. Food-prep's
  "kinds of work" (waiting, regular, continuous) is enough to plan by.
- **Material state chains drawn as graphs** (F3) and **similarity maps**
  of dishes (F2 as a map). Neither has evidence of helping, and both invite
  over-reading of position.
- **Readiness against doneness drawn as notation.** No evaluated visual form
  exists. Words on the step ("not ready to eat") are what R5 already
  produces.

## Open (interface evaluation, `open-questions.md`)

- No study compares a dish-first view with an ingredient mindmap for
  deciding what to cook. This is R7's central usability question.
- The F4 overview was preferred, but did not make cooking faster (Y703).
  Its participants were students, not households choosing dinner. Its
  benefit must be measured as understanding or confidence, not time.
- Readiness against doneness, members after assembly and a secondary output
  that rejoins the dish (K9) have no evaluated visual form anywhere found.
