# How construction could relate to the existing model (options only)

Nothing here is decided or implemented. The brief asked for options. Each is
judged against what the evidence in `patterns.md` and `requirements.md`
needs.

## What the evidence asks of a model

1. **Several independently processed components** in one preparation. Each
   component has its own operation path: the courgette shell is blanched and
   hollowed, its flesh is chopped and sautéed, the rice is par-toasted.
2. **A structural relation between them**, from a small set seen in the
   recipes:
   - binds itself (C1-C3);
   - is bound by a dry phase and coagulant (C4);
   - is suspended in a batter (C5);
   - is set in egg (C6);
   - contains or wraps (C7);
   - is layered with a thickened phase (C8);
   - is coated (C9).
3. **Nesting.** A component can itself be a construction: the cepelinai
   wrapper is a C2b dough, and the arancini rice ball is C2a inside a C9 coat.
4. **Recombination of fractions.** A fraction from one component's operation
   goes into another component of the same preparation:
   - scooped flesh into the filling (M7, M16, M17);
   - inner cabbage leaves into the filling (E12a);
   - settled starch back into the mass (C1);
   - salt-drawn juice as the batter liquid (C4b);
   - the tomato pulp as the cooking liquid of raw rice (M7a).
5. **Assembly operations and a final thermal step on the assembled whole**
   (fill, roll, seal, layer, coat, then fry, bake, boil or steam). Several
   components are already cooked: two cookings are normal.
6. **Order and state constraints** that span components: cool before the egg,
   salt late, add wet vegetables last, dewater the filling before wrapping.

This is a set of **structural relationships between materials**. It does not
say which flavours go together. Nothing in the evidence calls for a new
pairing score, so none is proposed.

## What already exists

| Existing piece | What it covers | What it lacks for construction |
| --- | --- | --- |
| R1 `operations.yaml` + `operations.apply/explore` | produces component materials: grated, salted-and-drained, blanched-flexible, hollowed shell + core fraction, mashed, fried. These are the **component producers** | one input per operation; "one primary cooking per sequence"; no outputs for `decanter`, `egoutter`, `congeler`, `foisonner`, `malaxer`, `abaisser` |
| `Material.adds` and `kind: composite` (operations.py) | an operation can bring named ingredients (salt, fat, egg white); the result is a composite | the added things are bare ingredients, not processed components with their own paths |
| R1 `functions`: `wrapper`, `edible_vessel`, `binder`, `thickener`, `moisture_carrier` | tag a single material as fit for a structural role | predefined, one material at a time; `binder` disagrees with the evidence (`requirements.md`) |
| `tomato.yaml` transformations: `input_component` | chains one state into the next (`smash_roast` takes `boiled_potato_component`): two cookings in sequence, as C2 needs | one input; a chain, not a combination |
| `byproducts` (+ `uses`) | a transformation yields a second component with its own destinations (`tomato_water_component`: soup, broth, pantry base) | the byproduct leaves for another dish; there is no way to say it goes back into this one |
| `uses` | names the dish contexts a component is good for (salad, hash, filling ...) | a destination label, not a structure |

## Options

### Option A: curated fields only, no new concept

Express a construction as a curated `tomato.yaml` transformation:
- a `uses` value such as `filling` or `patty`;
- `byproducts` for the scooped flesh;
- `input_component` for the pre-cooked vessel.

- **For:** no schema change, no code change.
- **Against:**
  - `input_component` is singular, so the second component disappears.
  - Nothing records which component is the shell.
  - Recombination (point 4) cannot be expressed.
  - It hides the pattern, so nothing is learnt across dishes.

Fits one or two showcase dishes, not the nine patterns.

### Option B: multi-input operations inside `operations.yaml`

Add assembly operations (`farcir` fill, `rouler` roll, `lier_masse` bind a
mass, `superposer` layer, `enrober` extended) whose `requires` name several
inputs.

- **For:** one vocabulary; reuses the applicability engine's three-valued
  checks.
- **Against:**
  - Every R1 operation and `explore` assume one input material. Multi-input
    search explodes combinatorially, and that is the generator the user does
    not want yet ("no need to generate 37,000 vegetable patties").
  - Operations would carry dish structure, which is a different level.

### Option C: a separate construction layer (new concept)

A new data file, for example `constructions.yaml`, beside `operations.yaml`.
- One entry per **pattern** (C1-C9): its mechanism, its components, the
  requirements of each component as property predicates in the same syntax
  R1 `requires` uses (`water: ">=high"`, `flexible: true`, `cooled: true`),
  the water routes it allows, its order constraints, and its final thermal
  steps.
- One list of **documented instances**: dish, tradition, recipe ids, and the
  component paths in R1 operation ids. This is the R1 benchmark idea applied
  to construction.
- Components would be filled by R1 materials (component producers).
  Recombination would be a component whose source is a named fraction of
  another component in the same instance.
- **For:**
  - Matches the evidence one to one: patterns, components, relations,
    nesting (a component can name another pattern), recombination.
  - Keeps operations single-input.
  - Every pattern stays traceable to its recipes.
- **Against:**
  - A new concept and a new file.
  - The component names (shell, filling, matrix, coating) are needed, though
    they come from the patterns and not from a predefined list.
  - It invites a generator, which is not wanted yet.

### Option D: documented instances only (Option C's second half, first)

Record 20-40 documented constructions from `recipes.md` as data. For each:
the components, each component's R1 operation path, the relation, the
recombination links and the final step. Write no pattern rules and no
generator.

- **For:**
  - It is the "vocabulary before code" step.
  - It tests whether R1 operations can describe every component of real
    dishes, and lists exactly which operations, outputs and states are
    missing.
  - It is a benchmark for any later rules.
- **Against:** it produces nothing new by itself. That is intended.

## Vocabulary changes the evidence supports, whichever option

These are small, single-material changes inside the existing model
(`requirements.md` has the evidence for each):
- a `cooled` (or `set`) state;
- an `aerated` state (outputs for `foisonner`, `fouetter`);
- a `soaked` state and a soak operation (`tremper`);
- `decanter` outputs: settled solids + clear liquid;
- `congeler` output that softens leaves (`flexible`);
- make `presser`'s `binder: true` on pulp conditional on the material
  (starch, protein);
- `holds_shape_cooked` depending on piece size (courgette shell vs pieces);
- a hollowing operation that removes flesh, not only a seed core;
- part properties for potato, cabbage, onion, rice and bread, which are
  already catalogue ingredients;
- an exception to "one primary cooking per sequence" when a cooked component
  is assembled and cooked again.

## Recommendation

**Option D first**: documented instances described in R1 operation ids,
plus the small vocabulary changes above. Revisit Option C only when D shows
that the patterns hold across those instances. Do not build a generator.
Reasons:
- D follows the user's order: understand before generating.
- It keeps every construction traceable to a real dish.
- It is the cheapest test of whether the nine patterns are the right cut: an
  instance that fits no pattern, or two, will show up.
