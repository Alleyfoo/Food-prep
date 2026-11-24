# Culinary Operations and Material Discovery R1

**Question.** What physically useful materials can be made from an
ingredient by single culinary operations and short combinations of them,
including ones recipes rarely or never show?

The aim was to find useful intermediate materials: textures, forms,
fractions. Complete recipes were out of scope. Five physically different
ingredients: broccoli, tomato and avocado (already decomposed), plus carrot
and courgette (added).

Branch `research/culinary-operations`, from main after PR #4 (04ced4e).

## Documents

| File | Contents |
| --- | --- |
| `model-design.md` | How operations fit the existing model; written before implementation |
| `sources.md` | References, safety facts, and the existing-practice check (28 preparations) |
| `operation-catalogue.md` | All 95 operations (generated from `operations.yaml`) |
| `applicability.md` | Ingredient-level findings; `applicability-tables.md` has every operation × part with reasons (generated) |
| `composition.md` | How sequences are built, the bounding rules, the ranking |
| `results.md` | Exploration statistics and top sequences (generated) |
| `experiments.md` | 24 kitchen experiments and the negative findings |
| `evaluation.md` | The model's corrections, answers to the ten research questions, limitations, recommendation |
| `run.py` | Regenerates the generated files: `py -3.11 docs/research/r1-culinary-operations/run.py` |

## What was built

- **`src/foodprep/data/operations.yaml`:** 95 operations in six overlapping
  categories, with French and English names and the fields of the brief.
  - It **replaces `technique_rules.yaml`**. The family generator reads the
    family states from it and gives identical output (pinned by a
    fingerprint test).
  - Every tomato.yaml technique is linked or explained.
  - Cuts name their `preparations` id; 11 classical cuts joined that
    vocabulary.
- **`part_properties.yaml`:** new properties for operations, including the
  peel as an `outer_layer` and the courgette `seed_core`. Carrot (root,
  greens) and courgette (fruit) were added, also in tomato.yaml as parts.
- **`src/foodprep/operations.py`:**
  - three-valued applicability with reasons (unknown is never false);
  - outputs with property updates;
  - multi-output separations and branches;
  - bounded search (depth 3) with equivalence merging;
  - functions and a transparent ranking.

  It writes nothing.
- **CLI:** `foodprep applicability <ingredient> [--part]` and
  `foodprep explore <ingredient> [--part] [--top]`.
- **Tests:** `tests/test_operations.py` (40 tests); the full suite passes.

## Findings

1. **Operations can be defined once and applied by properties.** 95
   operations cover 13 parts with no ingredient-specific rule beyond three
   inherited curated exceptions. Every result carries its reasons:
   - julienne on carrot applies, "firm enough to hold a narrow strip";
   - chiffonade on carrot greens does not, because they are feathery;
   - julienne on broccoli stems is conditional, "peel first".
2. **The existing architecture already holds the idea.** `input_component`
   chains and `byproducts` give several outputs, so generated sequences stay
   runtime hypotheses and can later be promoted without a new graph.
3. **The most productive operations create a second material.** Peeling,
   pressing and salt-and-drain each turn one part into two useful fractions:
   - peeled stem and stem peel;
   - juice and pulp;
   - drained pieces and vegetable water.
4. **Enumeration works; ranking does not yet.**
   - The generator produced every established zero-waste preparation the web
     check found.
   - It also produced three with no evidence found: stem peel powder,
     courgette skin ribbons, courgette water reduced.
   - But its ranking cannot see flavour or "the same job done better". The
     established carrot juice glaze ranks 2,958th of 3,912, and grilled
     avocado has no function at all.
5. **The model's errors were in state updates, not operation definitions.**
   Fourteen corrections, logged in `evaluation.md`, were all about what an
   operation does to firmness, moisture, flexibility and state.
6. **Missing properties, found by failures:** ripeness, fibre stringiness,
   mucilage, and a sensory term for heat.

## Recommendation

**Worth developing further, after changes to the underlying model.**

- **Keep** the catalogue, the applicability model and composition.
- **Before adding ingredients:**
  1. cook the experiments, open and cheap ones first (B-1, Z-1, Z-2, B-3);
  2. add the missing properties they test;
  3. give ranking a sensory term;
  4. show short lists instead of thousands of paths.

Success is more useful things to do with an ingredient, not more
combinations, and only tasting can show that.
