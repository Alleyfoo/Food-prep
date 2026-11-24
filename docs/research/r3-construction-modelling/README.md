# R3: construction modelling

**Question.** Can food-prep represent an existing dish from raw ingredients
through to its finished construction, in a way that shows it understands why
the preparation works?

An implementation and validation round, not a literature study. It builds on
R1 (`../r1-culinary-operations/`: operations on one material) and R2
(`../r2-construction-patterns/`: nine construction patterns from 127
multilingual recipes). The overall plan is in `../roadmap.md`.

Branch `claude/objective-sanderson-dddccc`, from main after PR #6 (ae959af).

## Answers

| Question | Success criterion | Answer |
| --- | --- | --- |
| **Expressiveness** | The model describes established preparations accurately | **Yes for materials and structure; partly for what happens inside an assembly.** All 27 design dishes (43 routes, nine patterns) are described from raw parts: every one of 236 main-path steps is an applicable R1 operation, 66 documented claims hold on the computed states, and 9 recombination links are found. 13 dishes are fully represented, 14 partly, 0 not. Every "partly" names what is missing (`validation.md`) |
| **Generalisability** | Previously unmodelled dishes need no structural (schema) changes | **Mostly.** 8 held-out dishes chosen before design were represented after a schema freeze with data only: no new field, relation or code. 2 fit fully, 6 partly. Their failures need operation-level changes (steaming a setting liquid, doughs, a hinged pocket, two R1 state updates) and one schema-level change (several containers per filling) (`generalisation.md`) |
| **Traceability** | Every construction traces to documented practice | **Yes.** Every route, material and join cites R2 recipe ids; every id resolves to a recipe in `recipes.md` with a URL that was read; a test enforces it. Quantities and conditions appear only as evidence on the relation they support |

**What the model now understands about why a dish works**, using the brief's
stuffed courgette (`foodprep construction zucchine_ripiene`):
- the courgette is one material that `creuser` splits into a shell and its
  scooped flesh, and the validator finds that the flesh returns to the dish
  (recombination);
- the shell holds through baking because it is a large blanched half (the
  container check waives "does not hold its shape" for a large piece);
- the flesh becomes filling after it is chopped and cooked down (water driven
  off, W5), not squeezed;
- egg (sets on heat) and breadcrumb (takes up water, "per compattare") change
  the filling's holding, each checked against its role;
- the assembled vessel takes the final bake, and its final state (cooked,
  hollow, filled) matches the recipe.

What it does **not** compute is the filling's own change in the oven: that
remains a recorded claim, here and in every layered dish.

## What was built

- **ADR 0003** (`../../adr/0003-documented-constructions.md`): dishes as data
  over the operation model.
- **`src/foodprep/data/constructions.yaml`**: 35 documented dishes (27
  design, 8 held-out), 57 routes, with the vocabularies (patterns C1-C9,
  mechanisms H1-H11, water routes W1-W9) and additions.
- **`src/foodprep/constructions.py`**: loader and validator (applicability of
  every step, role checks, claims, derived recombination, unaccounted
  fractions, citations), the freeze manifest, and rendering.
- **`operations.yaml`**: 14 operations added, all outside the generator
  (`tremper`, `refroidir`, `reposer`, `creuser`, `fendre`, `decortiquer`,
  `detacher_feuilles`, `faconner` and the joins `melanger`, `incorporer`,
  `farcir`, `envelopper`, `superposer`, `revetir`); outputs for `decanter`,
  `egoutter`, `foisonner`; the one-cooking rule waived for assembled
  materials; `presser`'s binder flag made conditional on starch.
- **`part_properties.yaml`**: `staged_parts` for potato, onion, cabbage,
  aubergine, rice, chickpea, urad dal, black-eyed bean, spinach and bread
  (read by the operation engine, not by the family generator or the UI).
- **CLI:** `foodprep construction [dish]`.
- **Tests:** `tests/test_constructions.py` (30 tests): well-formed data,
  pinned verdicts, recombination, structure, moisture and heat vocabulary,
  traceability against R2, the validator catching malformed and false data,
  the freeze. The full suite passes.

## Documents

| File | Contents |
| --- | --- |
| `../roadmap.md` | Step 0: research questions and their status; R3-R5 |
| `dish-selection.md` | Step 1: design set (27) and held-out set (8), reasons, Lidl gaps; held-out recorded before design |
| `../../adr/0003-documented-constructions.md` | The new concept, the vocabulary added, the freeze |
| `validation.md` | Step 3: expressiveness and traceability of the design set |
| `validation-tables.md` | Generated: every design route, steps, claims, recombination, what is missing |
| `generalisation.md` | Step 4: how the freeze was enforced; held-out results; reusable or accommodating |
| `generalisation-tables.md` | Generated: every held-out route |
| `evaluation.md` | Decisions and costs, effect on existing behaviour, limits |
| `r4-needs.md` | What R4 (controlled transfers) needs |
| `run.py` | Regenerates the tables: `py -3.11 docs/research/r3-construction-modelling/run.py` |

## Main findings

1. **R1's single-material operations describe the components of real dishes
   almost completely.** With 8 added single-material operations, every
   design dish's materials are reachable from raw parts. R2's Option D worked:
   recording dishes first showed exactly which terms were missing.
2. **Six joins are enough for nine patterns.** Mix, matrix, contain, wrap,
   layer and coat cover C1-C9 and their nesting (arancini: a cooked-starch
   mass wraps a filling and is coated). The patterns are combinations of
   joins and transformations, which supports R2's view that they are
   relationships, not dish types.
3. **Recombination needs no special construct.** A material that starts from
   another material's fraction and reaches the same dish is found by the
   validator: 13 links over both sets.
4. **The biggest gap is inside the assembly.** An assembled dish takes its
   carrier's state, so a thickening binding phase (C8) or rice cooking inside
   a vessel is a recorded claim. All four layered dishes are partly
   represented for this reason.
5. **The held-out test separated structure from accommodation.** The
   structure generalised; operation requirements written per dish did not
   (steam got no "sets on heat" exception because no design dish was
   steamed). Doughs are the largest missing material.
6. **R2's two contradictions are resolved where dishes need it**, and R1's
   benchmark summary is unchanged by it (14/42 and 17/42).

## Not done, and limits

- Nothing was cooked. Every dish is documented practice; the claims are the
  recipes' claims, checked for consistency with the model, not tested.
- R2's recipe paraphrases rest on a summarising fetch tool, spot-checked at
  12 of 127 (R2 `evaluation.md`). R3 did not re-read pages.
- Lidl availability uses the catalogue as a proxy; 40 of 56 additions (pantry staples,
  dairy, meat, Japanese and Indian staples) and 5 of 10 staged parts
  (aubergine, spinach, three dried pulses) are not catalogued. No C3 dish has a catalogued main ingredient.
- Meat and fish fillings are recorded as additions, not modelled.
- No transfer was attempted; that is R4.
