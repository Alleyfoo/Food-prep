# R6: academic foundations of culinary process modelling and recipe adaptation

**Question.** How do established academic and industrial approaches
represent:
- culinary transformations;
- complete cooking processes;
- ingredient substitutions;
- alternative routes to finished dishes?

Is there a better representation, method or concept than what Food-prep
built in R1-R5? The aim was to find out, not to confirm.

This is a comparative research round with no implementation. It replaces
the planned interface round, which moves to R7 (`../roadmap.md`). Branch
`claude/r6-academic-foundations-becfd4`, from main 71f4dac. Nothing was
cooked.

## Answer

**No approach read is a better replacement for Food-prep's representation,
but the literature names eight concepts worth taking. It also shows that
the app does not yet use what R3-R5 built.**

1. **What academic researchers have already solved.**
   - A typed step-and-material unit, the same as R1's.
   - Parallel components and joins.
   - Retrieval from an inventory (FOON).
   - Equipment-independent against kitchen-bound recipes, validated in
     trial before use (ISA-88).
   - Storage policies and maximum waits (State-Task Network).
   - Formal detection and repair of what a substitution breaks (the UCL
     logic, untested on recipes).
   - Alignment of recipes for one dish.
   - One process overview tested with people cooking (Buykx).
2. **What Food-prep already represents adequately, or better.**
   - Operations on typed states, with three-valued applicability: the only
     approach found that keeps unknown apart from false.
   - **Structural roles** (container, wrapper, layer). Only a role check
     refuses curly kale and raw rutabaga; similarity methods accept both.
   - Recombination and fraction accounting.
   - **Readiness against doneness**: no counterpart anywhere.
   - Observable failure checks with causes.
   - Documented routes kept apart from combinations of their steps.
   - **Members after assembly**: nobody models this. R5's documented
     endpoints (22 of 28) go furthest of anything found.
3. **Which existing approaches could solve the remaining problems.**
   - ISA-88's **general, master and control levels**: which values belong
     to the dish, to one kitchen, or to tonight. The kitchen test becomes a
     control record.
   - Y402's **violation plus repair** for substitutions.
   - **Step correspondence between routes**, for reading only, with a
     documented `compensated_by` ("the long covered bake replaces the
     blanch"). This closes K8's false negative without a simulator.
   - Storage class and maximum wait for intermediates.
   - History recorded only where a source ties a rule to it.
   - Objective kept apart from mechanism.
   - The observed member named in a check.
4. **What happens to a cooking process when a component changes.**
   - A primary change breaks named requirements: the role, the state, or
     processing shared with other members.
   - Each break needs a documented repair:
     - a parameter;
     - an added or changed operation;
     - a structural change;
     - a change on another member.
   - The result also gets a status:
     - documented;
     - quality risk;
     - documented failure;
     - analog;
     - no practice;
     - combination not documented;
     - safety not established.
   - Substitutability depends on role, current state and co-processing,
     not on identity (`substitution-impact.md`).
5. **How complete alternative routes are kept distinct.**
   - Keep each documented route whole, with its sources.
   - Never compose steps across sources. FOON retrieval, Trier streams and
     generalisation, and alignment aggregation all would, unmarked.
   - Mark any asked-for combination as "each part documented, the whole
     not".
   - Distinguish four things: a version of a step, an alternative route,
     a different product, and the same route in another kitchen
     (`alternative-routes.md`).
6. **What the mindmap should expose.**
   - Outcomes first: documented dishes and transfers per ingredient, as
     familiar and less usual uses, each with its verdict and one
     condition.
   - A dish opens as a **component-branch overview** with checks and
     dependencies.
   - Routes as **aligned columns**.
   - A swap as a changed branch with its reasons, refusals included.
   - An entry from a held state.
   - The ingredient network stays an exploration view, capped at about 20
     edges (`visual-representations.md`).
7. **What R7 should implement and avoid.**
   - Implement: wire the existing R3-R5 records into the app, which today
     reads none of them, in the views above, plus a form to record kitchen
     tests.
   - Avoid:
     - schema changes in the same round;
     - composed routes;
     - similarity substitutes;
     - computed schedules;
     - notations shown to the cook;
     - done-when checks shown as safety limits;
     - scores (`r7-recommendation.md`).

**Sources.** 113 entries (110 distinct works):
- 51 read as full text;
- 17 as full text through a summarising fetch;
- 28 in part;
- 17 as an abstract or landing page only.

Five load-bearing claims were checked against raw PDF text; all were
confirmed, with one wording correction (`limitations.md`).

**Open questions.** 54 in a single register (`open-questions.md`):
- 12 kitchen tests;
- 5 supermarket checks;
- 8 food-safety questions;
- 22 academic or representation questions;
- 7 interface evaluations.

## Documents

| File | Contents |
| --- | --- |
| `research-brief.md` | Scope, the fixed cases K1-K9 (and K1-x, K2-x), evaluation questions E1-E6, evidence rules; committed before any reading |
| `evidence-ontologies.md` | Y100-Y117: FoodOn and OBO planned processes, objective against mechanism, PO2/TransformON, design patterns |
| `evidence-foon-robotics.md` | Y201-Y219: FOON, task-tree retrieval, similarity substitution, LLM plus FOON, KnowRob |
| `evidence-cbr-workflows.md` | Y300-Y313: Trier POCBR, CookingCAKE, streams, generalisation, Taaable, temporal adaptation, CookIIS |
| `evidence-substitution.md` | Y401-Y420: the substitution ODP, UCL logic, review-mined and learned finders, Shidochi, evaluation weaknesses |
| `evidence-recipe-graphs.md` | Y500-Y516: r-FG (Japanese and English), RiCoRecA, action graphs, state tracking, cross-recipe alignment |
| `evidence-industrial-process.md` | Y600-Y616: ISA-88, Grafcet, STN/RTN, process-manufacturing recipes, HACCP, food-service history |
| `evidence-visualisation.md` | Y700-Y712: RecipeScape, ingredient networks, Buykx, comparative layouts, Japanese cooking support |
| `sources.md` | Verified bibliography index: every Y id, URL, citation, version read; duplicates; failed-page summary |
| `literature-review.md` | Per area: what is published, what is claimed, what is unsolved |
| `representation-comparison.md` | Food-prep R1-R5 layer by layer against the literature; Q1 two traversals; Q5 reuse; retain, extend, replace |
| `substitution-impact.md` | Q3: what substitutability depends on, the draft categories against the literature, the revised outcome set, the cases |
| `alternative-routes.md` | Q4: versions, routes, products, combinations, kitchens; why combination is dangerous; what to extend |
| `case-studies.md` | K1-K9 mapped into each approach, on paper |
| `visual-representations.md` | Q6: which representation answers which cook's question; what the mindmap should expose; what only adds complexity |
| `open-questions.md` | The consolidated R1-R6 register (54), by what each question needs |
| `limitations.md` | Method, spot check, what could not be settled, boundaries kept |
| `r7-recommendation.md` | What R7 should implement and avoid, and how to know it worked |

## Boundaries kept

- `src/`, `tests/`, every schema, all culinary data, and every R1-R5
  document and frozen file are unchanged (`git diff origin/main` is empty
  on them).
- The full suite passes (1013).
- No prototype, generator, score, ML experiment or simulator.
