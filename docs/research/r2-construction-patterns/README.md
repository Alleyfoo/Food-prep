# R2: construction patterns

**Question.** How do cooks build preparations from separately processed
materials? What holds a fritter, a stuffed vegetable, a roll or a layered
bake together, and could the food-prep model express it? This is research
only: no implementation, no generator, no scoring.

**Why now.** R1 (`../r1-culinary-operations/`) models what single operations
and short sequences do to one material. The Portuguese courgette dishes raised
in its review (curgete recheada: hollow, combine the flesh with a filling,
refill, bake; bolo de casca de curgete: ground peel in a cake) need
**recombination**, and the engine has none.

Branch `claude/unruffled-khayyam-7dd685`, from main after PR #5 (7f2ce25).

## Method: the evidence decides the ontology

The order was recipes → observed mechanisms → patterns → physical
requirements → transferable applications. No roles were defined beforehand.

1. **Recipes.** Three research agents, one per region, read recipes in each
   tradition's own language: 127 pages, 59 dishes, 20 languages besides
   English. Their briefs: record each recipe's operation sequence, the reasons
   it states, and where recipes of the same dish disagree; do not classify.
   For a second witness, `count_construction.py` counted 27 dishes (55,036
   recipes) in the 2.2-million-recipe RecipeNLG corpus. It measured how often
   recipes write down each step, and the rules were hand-checked at 12-15 of
   15.
2. **Mechanisms.** For every dish: what gives structure, what makes it hold,
   whether a binder is needed, how water is handled, what is essential. Names
   were given only after reading.
3. **Patterns.** Dishes grouped by the mechanism whose removal makes them
   fail, never by appearance.
4. **Requirements** of each component, in the vocabulary of
   `part_properties.yaml` and `operations.yaml`, with missing terms flagged.
5. **Transfers** to the catalogue's Lidl-based vegetables, last, and marked
   as inference.

## Documents

| File | Contents |
| --- | --- |
| `recipes.md` | Step 1: 127 recipes as paraphrased operation sequences, by region (ids E, M, A) |
| `recipenlg.md` | Step 1, corpus: what the counts say and how the rules were checked |
| `recipenlg-counts.md`, `recipenlg-counts.yaml` | Generated count tables (counts only) |
| `count_construction.py` | The counting script: `py -3.11 docs/research/r2-construction-patterns/count_construction.py PATH/full_dataset.csv` |
| `sources.md` | Every URL actually read, failed pages, independence notes |
| `mechanisms.md` | Step 2: per-dish answers, mechanisms H1-H11, water routes W1-W9, 13 convergences, contradictions |
| `patterns.md` | Step 3: nine patterns C1-C9 with the recipes behind each; look-alikes that hold differently |
| `requirements.md` | Step 4: component requirements mapped to model terms; missing terms; where the model disagrees with the evidence |
| `transfers.md` | Step 5 (**inference**): which catalogue vegetables could meet each pattern |
| `model-relation.md` | Options for relating construction to the model; recommendation |
| `evaluation.md` | Where the evidence contradicted expectations, limits, kitchen tests |

## Findings

1. **Dishes hold together in nine ways, and appearance does not predict
   which.** The nine construction patterns, by holding mechanism:
   - C1 released-starch cake;
   - C2 cooked-starch mass;
   - C3 raw pulse paste;
   - C4 bound watery vegetable;
   - C5 batter matrix;
   - C6 egg-set matrix;
   - C7 container and filling;
   - C8 layered assembly;
   - C9 coated piece.

   A flat fried cake of grated vegetable can be C1 (rösti, draniki), C4
   (mücver) or C5 (raggmunk). "Falafel" is C3 in every Arabic recipe read and
   a binder-held cooked mash in the American corpus.
2. **Whether a binder is needed depends on the material's transformation,
   not on the dish.** No binder is needed when the main material becomes its
   own cohesive phase:
   - raw starch released by grating (C1);
   - starch cooked and cooled (C2);
   - raw soaked pulses ground (C3);
   - a filling held by a container (C7).

   Egg and flour are needed for watery, starch-poor vegetables (C4: corpus
   courgette fritters 92% egg). Egg is often optional elsewhere. Two
   traditions cap it because it adds water (A13).
3. **Every pattern manages a water budget, by one of nine routes.** Salt and
   squeeze, squeeze, drain, settle and return the starch, dry by heat, absorb,
   prevent release, use the water, dry the surface. Recipes that seem to
   disagree on salting (early or late) are consistent once you see what
   happens to the water next.
4. **Strong convergences across independent traditions:**
   - returning the settled potato starch (German, Polish, Ashkenazi,
     Russian/Belarusian/Ukrainian, Korean; Swedish by not rinsing);
   - raw soaked pulses ground without binder (Egypt/Levant, South India,
     West Africa);
   - cooling a cooked mass before shaping (13 traditions);
   - not turning until the crust has set (8 sources, 7 traditions);
   - a dry layer before a wet coating (Japan, Mexico, Korea, China);
   - baking calls for a drier mass than frying (Greek, Portuguese, Swedish).
5. **Recombination is ordinary practice.**
   - Hollowed vegetables get their own flesh back in all five Mediterranean
     stuffed-vegetable dishes read (corpus: 38% of stuffed
     courgette/aubergine).
   - Finnish cabbage rolls take the inner leaves into the filling.
   - Latkes and draniki return the potato's own starch.
   - Pakoda and hobak-jeon use the vegetable's own salt-drawn juice as the
     batter liquid.
6. **Patterns nest** (a C2 dough wraps a filling in cepelinai; a C9 coat goes
   on a C2 rice ball). So construction is a set of structural relationships
   between components, not a list of dish types.
7. **The model already holds part of it, and disagrees with the evidence in
   places.**
   - Already there: R1 operations produce the components (salted and drained
     courgette, blanched flexible leaf, hollowed shell + core fraction);
     `frire` already requires dry-enough input.
   - Missing:
     - a cooled state;
     - water uptake by dry additions;
     - outputs for settled starch;
     - a soak operation;
     - assembly operations;
     - recombination;
     - an exception to "one primary cooking per sequence".
   - Disagreeing: `presser` marks squeezed pulp as a binder, and courgette is
     marked as not holding its shape when cooked. Both contradict the recipes.

## Recommendation

- **Model (Option D in `model-relation.md`).** Record 20-40 documented
  constructions from `recipes.md` as data. For each, give the components'
  operation paths in R1 operation ids, the structural relation, the
  recombination links and the final step. Add the small vocabulary changes
  listed in `requirements.md`. No pattern rules and no generator yet. This
  tests whether the nine patterns are the right cut, and whether R1 can
  describe real components.
- **Kitchen.** Cook the four paired tests in `evaluation.md`: settled starch
  vs flour; courgette by three water routes; rösti stored 1 vs 2 days;
  courgette shell refilled with its own flesh. Each compares documented
  variants, not novelties.
- **Next searches** before any transfer is suggested:
  - Portuguese *curgete recheada* itself;
  - split-pea vadas;
  - kale and broccoli-leaf rolls (via *couve* and *karalahana sarması*);
  - *parmigiana di zucchine*.
