# Research roadmap: from ingredients to dinner

Where the culinary research stands, which questions are answered, and what
comes next. Written at the start of R3 (2026-11-24) as a consolidation, so the
next rounds build on the answers instead of reopening them.

The goal, in the user's words: food-prep should eventually "help us make
dinner rather than giving us homework about dinner".

The method, unchanged since R1:
- documented dishes first ("has anybody actually eaten this before?");
- the evidence decides the ontology;
- multilingual sources;
- Lidl Finland ingredients and a home kitchen;
- practical usefulness before novelty;
- no new scoring;
- represent why a dish works, not the recipe.

## The research questions so far

| # | Question | Status | Where |
| --- | --- | --- | --- |
| 1 | **Decomposition.** What separable parts does an ingredient have, and is each one food? | answered, implemented | ADR 0002, `tomato.yaml` parts, `part_properties.yaml` |
| 2 | **Operations.** What does one culinary operation do to one material, and when does it apply? | answered, implemented | R1: 95 operations in `operations.yaml`, three-valued applicability with reasons |
| 3 | **Materials and secondary outputs.** Which operations give a second useful material (peel, juice and pulp, vegetable water, core)? | answered, implemented | R1: multi-output separations in `operations.py` |
| 4 | **Bounded sequences.** What can two or three operations in a row make, and how should it be shown? | answered | R1 benchmark: per-function, simplest-first lists recover about 40% of established preparations; a global score recovers almost none, so scoring stopped |
| 5 | **Construction patterns and holding mechanisms.** How do cooks build a dish from separately processed materials, and what holds it together? | answered within scope | R2: nine patterns C1-C9, mechanisms H1-H11, water routes W1-W9, recombination is ordinary practice |
| 6 | **Representing complete constructions.** Can the model describe a real dish from raw parts to its finished structure, and show why it works? | answered, implemented (R3, PR #7) | 35 dishes; structure yes, what happens inside an assembly partly |
| 7 | **Discovering useful unfamiliar preparations.** Can a documented construction be carried over to another Lidl ingredient with a physical reason, and does it work? | answered, R4 (not cooked) | `r4-transfers/`: five transfers worth cooking, one not; the search finds them, the model checks structure, the kitchen judges quality |
| 8 | **Executing a documented step.** What do you actually need to do for a step to work: conditions, elapsed and active time, how you know it is done or failed, readiness against doneness, through the whole sequence; and what can you do from a state you already have? | answered, R5 (not cooked) | `r5-processing-conditions/`: 25 pairs, 10 whole sequences, 17 intermediate states, from documented practice only |
| 9 | **Helping someone decide what to cook.** Can the Taste Circle, families, operations, constructions and conditions answer "what can I make with this tonight"? | open, R7 (planned as R6 until R6 became the academic round) | `r6-academic-foundations/r7-recommendation.md` |
| 10 | **Academic foundations.** How do established academic and industrial approaches represent transformations, whole processes, substitutions and alternative routes, and is there something better than R1-R5? | answered, R6 (literature only) | `r6-academic-foundations/`: no replacement found; eight concepts to adopt or extend; the app reads none of R3-R5 yet |

### What each finished round established

- **R1, culinary operations** (`r1-culinary-operations/`, PR #5).
  - Operations are defined once, independent of ingredients, and applied by
    material properties. Every result carries its reasons ("firm enough to
    hold a narrow strip", "peel first").
  - The most productive operations make a second material: peel, juice and
    pulp, drained pieces and vegetable water.
  - Enumeration works; ranking does not. The global ranking recovered 0-2 of
    42 established preparations; per-function lists ordered simplest-first
    recover 14-17. That list is now the default `foodprep explore` view, and
    scoring work has stopped.
  - The two established preparations the engine could not reach both needed
    recombination (stuffed courgette, courgette peel cake).
- **R2, construction patterns** (`r2-construction-patterns/`, PR #6).
  - 127 recipe pages for 59 dishes, read in 20 languages besides English,
    plus RecipeNLG counts for 27 dishes.
  - Dishes hold together in nine ways, grouped by the mechanism whose removal
    makes them fail: released starch (C1), cooked starch (C2), raw pulse paste
    (C3), bound watery vegetable (C4), batter matrix (C5), egg matrix (C6),
    container and filling (C7), layered assembly (C8), coated piece (C9).
  - A binder is needed only for watery, starch-poor vegetables. Every pattern
    manages a water budget, by one of nine routes. Patterns nest.
  - The model already produces most components, but lacks recombination,
    assembly, a cooled state, water uptake, settled starch and a soak, and
    disagrees with the recipes in two places (squeezed pulp marked as a
    binder; courgette "does not hold its shape cooked").
  - Recommendation (Option D): record documented constructions as data
    before writing any rules.

## The agreed roadmap

No further theoretical research round. The next three rounds implement and
validate, each against documented dishes.

### R3: represent documented dishes

Can food-prep represent an existing dish from raw ingredients through to its
finished construction, in a way that shows it understands why the
preparation works? About 27 design dishes from R2 (three per pattern) and a
held-out set chosen before the schema is designed. It answers three
questions:
- **expressiveness:** established preparations are described accurately;
- **generalisability:** held-out dishes need no schema change;
- **traceability:** every construction traces to R2 recipe ids and URLs.

Representing a dish is not reproducing a recipe: quantities and conditions
are evidence attached to relationships, not steps to follow. No construction
rules, no generator, no scoring. Results: `r3-construction-modelling/`.

### R4: controlled transfers

Carry a documented construction over to another Lidl ingredient: rösti from
another root, other leaves as wrappers, other vegetables as containers,
Finnish dried peas as falafel, rutabaga in a gratin. For each candidate, in
this order:
1. search whether someone already makes it, in the relevant languages;
2. only then give the physical rationale, from the R3 representation: which
   component requirement the new ingredient meets, and which it does not.

Novelty comes last, and every transfer stays marked as inference until it is
found in practice or cooked.

**Status after R4 (2026-11-25, `r4-transfers/`).** Done, nothing cooked.
- Lidl FI's website lists offers only, so the ingredient boundary is
  recorded per item as regular, seasonal, campaign or not found
  (`catalogue.md`); dried peas, fresh broccoli and napa cabbage need a shelf
  check.
- Worth cooking: potato and rutabaga gratin (blanch the rutabaga), onion
  halves as vessels beside courgettes, napa-cabbage rolls (replacing curly
  kale), pea falafel as a comparison with chickpea, broccoli stems with
  carrot in patties. Not worth it: curly kale as a wrapper. None is new to
  cooking; four are new to the Finnish table.
- The model agreed with the evidence on every comparable transfer once one
  data-only amendment (A2, `cooks_slowly` on a gratin layer) fixed the gap the
  gratin exposed; A2 changed nothing in R3. It explains structure, not
  quality; every verdict ends in a kitchen test (`kitchen-tests.md`).

### R5: documented processing conditions

Renamed by the user after R4: every R4 "one thing to get right" was a
processing condition (blanch the rutabaga, don't overboil the onion, bake the
napa rolls covered, soak but never cook the peas), and R4 listed time and
temperature as its largest gap. During the round the user widened the unit
from the isolated operation to the **whole processing sequence**: each
component from raw part to plate, readiness (ready for the next operation)
kept apart from doneness (ready to eat), each member's endpoint in the heat
after a join, and the documented reasons one stage exists for a later one.

**Status after R5 (2026-11-25, `r5-processing-conditions/`).** Done, nothing
cooked.
- `processing_conditions.yaml` and `conditions.py`: 25 (part, operation) pairs
  and 10 whole sequences (the five R4 dishes worth cooking and their
  kitchen-test bases, 54 steps). Each step has an endpoint kind, observable
  done-when and failed-if checks, and each source's own times, with active
  work kept apart from elapsed time. There are 23 dependency links and 31
  alternative sequences, and 17 intermediate states with keeping times, 10
  of them from food-safety bodies. `foodprep conditions` and `foodprep from`
  ("from this state, what next", with "not ready to eat" for a readiness
  state).
- Nothing is derived, simulated or ranked; 43 conflicts kept as versions; no
  change to R3 or R4 results, no amendment.
- The evidence stops inside some assemblies (the onion in a falafel, the
  cream in a rutabaga gratin, a farci filling), at pea-specific checks, at
  Lidl packet text, and at keeping times for raw intermediates. The kitchen
  tests (`r5-processing-conditions/kitchen-tests.md`) now carry concrete
  checks for every step.

### R6: academic foundations of culinary process modelling and recipe adaptation

Added by the user after R5, in place of the interface round, which moved to
R7. It is a comparative literature round with no implementation. It looked
at seven areas:
- food process ontologies;
- FOON and robotics;
- case-based workflow adaptation;
- substitution;
- recipe flow graphs;
- industrial batch processes;
- visualisation.

It compared each against R1-R5 on nine fixed cases (K1-K9), chosen before
reading.

**Status after R6 (2026-11-25, `r6-academic-foundations/`).** Done, nothing
cooked.
- **No approach read replaces any layer of Food-prep.** The literature uses
  R1's unit (a step with typed input and output materials).
- Food-prep is ahead on several points:
  - structural roles;
  - three-valued applicability;
  - readiness against doneness;
  - failure checks;
  - keeping documented routes apart from combinations of their steps.
- **Nobody models what a member undergoes after assembly.** R5's
  documented endpoints go furthest of anything found.
- **Concepts to adopt or extend** (data, in a later round, not R7):
  - ISA-88's general, master and control recipe levels (the kitchen test
    is the control record);
  - substitution as a violation with documented repairs (Y402);
  - step correspondence between routes, with a documented
    `compensated_by` (closes K8's false negative without a simulator);
  - storage class and maximum wait for intermediates;
  - history only where a source ties a rule to it;
  - objective against mechanism;
  - naming the member a check observes.
- **Every approach that composes steps from several sources** (FOON
  retrieval, Trier streams and generalisation, alignment aggregation)
  would produce unverified combinations unmarked. Food-prep's rule stands.
- **The app reads none of R3-R5.** R7's first job is to put those records
  where the cook looks.
- A consolidated register of 54 open questions:
  - 12 kitchen tests;
  - 5 supermarket checks;
  - 8 food-safety questions;
  - 22 academic or representation questions;
  - 7 interface evaluations.

### R7: integrate into the interface

Planned as R6 and moved to R7 when R6 became the academic round. The text
below is kept as it was written before that change. "R6" in it means this
interface round. R6's recommendation for it is
`r6-academic-foundations/r7-recommendation.md`:
- outcome first, per ingredient;
- a dish as a component-branch overview with R5's checks;
- routes as aligned columns, with no column for a combination;
- a swap as a changed branch, refusals included;
- an entry from a held state (`from_state`);
- a form that records kitchen tests;
- the mindmap demoted to exploration;
- no schema change, composed route, similarity substitute, schedule or
  score.

Make it useful in the app: the Taste Circle, ingredient families, operations
and constructions working together, so the app can answer:
- what can I make with this vegetable;
- what to do with its discarded parts;
- what role it can fill in a dish;
- safe substitutions;
- how to improve the flavour.

The sensory and pairing system complements constructions; it is not replaced.

What R4 suggests for R6: the useful unit is a documented construction paired
with what is in season and in the shop, carrying its one known failure
("rutabaga is in season; it goes into a gratin if you blanch it first").
Availability should come from the user's own shelf checks, not lidl.fi, and
kitchen-test results should flow back into `transfers.yaml` and the tasting
record.

What R5 adds for R6: show a sequence with the member the cook has highlighted:
what is done, what remains, the next step's done-when and failed-if checks,
and the one dependency that explains it. `foodprep from` is the "cook now or
prepare for tomorrow" primitive (remaining steps, kinds of work, how long the
state keeps and on whose authority). Conflicts appear as choices, "not found"
as itself.

The split into R3-R7 is a proposal (it was R3-R6 before R6 became the academic round); rounds may merge if the work shows they
should.
