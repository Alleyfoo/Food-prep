# What R7 should implement, and what it should avoid

R7 is interface integration in the existing Streamlit app. This is R6's
evidence-based recommendation for it. Evidence:
- `visual-representations.md` (Q6);
- `representation-comparison.md` (Q1, Q5);
- `alternative-routes.md` (Q4);
- `substitution-impact.md` (Q3).

It is a recommendation, not a design. Nothing here was built or tested with
the user.

## The finding that decides R7's scope

**The app reads none of the R3-R5 data.** `src/foodprep/ui/` never touches
`constructions`, `transfers`, `conditions` or `from_state`. The mindmap
(`ui/graph.py`) draws ingredient → technique → component from the older
data.

Every answer R3-R5 produced is reachable only from the CLI:
- 35 dishes as constructions;
- five transfers worth cooking and two refusals;
- ten whole sequences with done-when and failed-if checks;
- 17 intermediate states with keeping times.

So R7's job is to **put existing records where the cook looks**, not to
invent new data or new kinds of picture. That keeps R7 cheap, and it keeps
it testable against the kitchen tests that are already due.

## Implement

Ordered by how directly each step helps make dinner.

1. **"What can I make with this?": outcome first.**
   - A read-only query over `constructions.yaml` and `transfers.yaml` by
     ingredient part. These are two traversals of one graph (Y100);
     `representation-comparison.md` Q1 covers it.
   - Show the documented dishes and transfers the ingredient enters, as a
     short list in two labelled groups: *familiar uses* and *less usual
     uses*. Grouped lists help (Y708); similarity maps do not
     (`visual-representations.md`). For dried peas: pea soup, and pea
     falafel.
   - Each entry gives:
     - its verdict;
     - its **one condition** ("blanch only the rutabaga");
     - availability from the user's own shelf checks (R4: never from
       lidl.fi);
     - whether it has been cooked;
     - any recorded quality risk or safety gap, in words.
2. **A dish opens as a component-branch overview.**
   - Buykx's study is the only representation tested with people cooking
     (Y703). Show one branch per independently prepared member from the R3
     route, joining at the assembly.
   - Each step carries what R5 already holds:
     - *ready for the next step* or *ready to eat*;
     - the done-when and failed-if checks;
     - the kinds of work and the times, each with its sources;
     - the one dependency that explains it.
   - After the join, each member keeps its own line: "rice finishes in the
     roll"; "rutabaga: some give, or no resistance (sources differ)".
   - "Not found" is shown as itself.
3. **Alternatives as aligned columns.**
   - For a dish with several documented routes, show each route as a
     column, with corresponding steps on one row and "none" where a route
     has no such step (Y707, indirect).
   - R5 `alternatives` that are not yet whole routes appear as cited text
     in their column.
   - A **rejected** route is a column too (K8).
   - Conflicts within a step are shown as choices ("3-5 min, or about 10
     min until almost tender"), never one merged number.
   - **An unverified combination never gets a column**
     (`alternative-routes.md`).
4. **A swap is a changed branch, with its reason.**
   - Show an R4 transfer as the base dish's overview with the substituted
     branch marked, and its repairs on it ("napa: shave the rib; bake
     covered").
   - A refused swap stays visible with its reasons (curly kale). A
     context-free similarity display would endorse it (Y701, Y206).
5. **Start from what I have.**
   - An entry point backed by `conditions.from_state`: pick a held state
     (cooked rice, soaked peas, blanched rutabaga).
   - The overview of each documented route through it opens with that
     branch marked done, so only the remaining steps show. Cooks rarely
     prepare everything first (Y703).
   - Show how long the state keeps and on whose authority.
   - Say "not ready to eat" for a readiness state.
   - Say "history not considered" where R1's `key()` matched it.
6. **Demote the mindmap.**
   - Keep it as an exploration view, not the decision view.
   - Make its second ring the outcomes (dishes and transfers), not the
     techniques.
   - Keep R4.1's rule: above about 20 edges the table is the default.
7. **Record what was cooked.**
   - A small form that writes a kitchen test's observations (actual times,
     the endpoint reached, the verdict) as a **control record** on the
     route (ISA-88's batch-level record, Y602, Y604).
   - It is shown beside the documented values, never merged into them.
   - KT1-KT6 are the first users of this form.
8. **Label the Taste Circle** as documented pairings, not predicted taste.
   A shown taste value shifts ratings without tasting (Y712).

## Deliberately avoid

- **New data schema in the interface round.** The data extensions R6
  recommends belong to a separate data round, after R7 shows which ones a
  cook actually needs:
  - violation and repair on transfers;
  - `compensated_by` and step correspondence between routes;
  - the level of a value;
  - storage class and maximum wait;
  - sourced history on intermediates;
  - the substitute/analog flag and driver.
- **Any generated or composed route.**
  - No route built from the steps of several sources.
  - No "best route".
  - No preference order among valid routes (Y608's preference ranking is a
    score).
- **Similarity-based substitutes.** They endorse K6 and K8 (Y206, Y408,
  Y701).
- **One force graph for a dish's routes.** It superposes alternatives
  without alignment.
- **Process notations shown to the cook**: BPMN, flow graphs, FOON trees,
  ISA-88 procedure charts, state-chain graphs. They are built for
  annotators, robots and operators (Y500).
- **A computed schedule** or multi-dish planner. The kinds of work
  (waiting, regular, continuous) are enough to plan by (Y709, Y710 optimise
  time, which nobody asked for).
- **Done-when checks presented as safety limits.** Critical limits are
  validated (Y611). Keeping times show their authority, and "not known"
  where none exists (FS2-FS5).
- **Any food-safety claim from structure or tradition.** Pea falafel shows
  the Q505 gap in words until FS1 is answered.
- **Scores, ranks and predicted taste.**

## How to know whether R7 worked

Cheap checks, in `open-questions.md` IE1-IE7. Each is done by the user,
alongside cooking that is due anyway:
- **IE2:** cook KT1 (the gratin) or KT3 (napa rolls) from the overview, and
  note where it confused you.
- **IE4:** for the gratin, choose tonight's route from the aligned columns
  and say why.
- **IE1:** on two evenings, decide what to cook once with the outcome list
  and once with the mindmap.
- **IE3:** read back three cases: K6 (not documented), K8 (documented to
  fail) and K1-x (not known). Can you tell them apart?
- **IE5:** start once from a real leftover.

R7 succeeds if a dinner gets decided and cooked from it with less looking
up than before. A better-looking graph does not count.
