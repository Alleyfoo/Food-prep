# Model design: culinary operations in the existing architecture

Written before implementation. It records what the existing model already
supports, what changes, and why no parallel ontology or graph is needed.

## What already exists

| Need in the brief | Existing structure | Verdict |
| --- | --- | --- |
| Anatomical parts | `parts` in tomato.yaml (ADR 0002), with edibility and the prep step that separates them | Reuse as the starting materials |
| Physical properties of parts | `part_properties.yaml` (water, fibre, toughness, fat, sugar, acidity, bitterness, umami, flags, pigment, flavour) | Reuse and extend with the properties operations need |
| Operation definitions | `techniques` in tomato.yaml (name, is_modifier, heat_type, moisture_change) for the database; `technique_rules.yaml` (requires, effects) for the family generator | Two partial definitions of the same thing. Operations **replace** `technique_rules.yaml` and **link** to tomato.yaml techniques by id, so there is still one rule per technique |
| Geometric forms | Prep modifiers (`slice`, `dice`, `grate`, `peel`...) and the `preparations` vocabulary (sliced, shredded, grated, peeled, scored...) | Reuse. Cuts produce a `preparations` id; the missing classical cuts are added to that vocabulary |
| Processed states | Curated transformations → output components | Reuse unchanged as the *established* layer |
| Chains | `input_component` (smashed potatoes start from boiled potatoes) | The same semantics as a step in a sequence |
| Several outputs | `byproducts` (salting tomatoes also yields tomato water) | The same semantics as a multi-output operation |
| Runtime hypotheses | `possibilities.py`: generated, labelled, never written to the ontology | The same pattern for generated sequences |
| Evidence | `evidence_sources`, confidence and uncertainty vocabularies, Scout hypothesis classes, tastings | Reuse; operation sequences get evidence types of their own (below) |

**Conclusion:** the curated transformation graph can already represent
intermediate materials (`input_component`) and branching outputs
(`byproducts`). A generated sequence is a runtime chain of such steps. It is
**not** written into tomato.yaml: the brief forbids expanding the ontology for
speculative possibilities. A sequence that is tested and works can later be
promoted to curated transformations with exactly these two fields.

## Changes

1. **`operations.yaml` replaces `technique_rules.yaml`.** One reusable
   definition per operation, independent of ingredients, with the fields of the
   brief (French and English names, aliases, categories, input requirements,
   equipment, parameters, mechanisms, outputs, property changes, applications,
   limitations, safety, evidence, confidence).
   - An operation that is also a tomato.yaml technique names it in
     `technique:`; a test checks the link.
   - The ten rules the family generator used keep their `requires` and
     `effects` and are marked `family_state: true`. `possibilities.py` reads
     those, so its behaviour does not change.
   - A cut names the `preparations` id it produces.
2. **Classical cuts join the `preparations` vocabulary** (julienne, brunoise,
   bâtonnet, macédoine, paysanne, chiffonade, tourné, rondelles, ribbons,
   wedges, tronçons). The vocabulary already holds sliced, grated, scored and
   so on; these are the same kind of thing.
3. **`part_properties.yaml` gains properties** that operations need:
   `firmness`, `shape`, `flexible`, `sheetable`, `starch`, `pectin`,
   `emulsifies`, `holds_shape_cooked`, `piece`, and `outer_layer` (the
   properties of a peel that is not a part of its own). Values follow the
   existing levels and flags.
4. **Carrot and courgette are added** to tomato.yaml as ingredients with
   parts (carrot root and greens; courgette fruit), and to
   `part_properties.yaml`. They get no curated transformations in this round.
5. **A new runtime module, `operations.py`**, assesses applicability,
   applies operations to materials, and explores bounded sequences. It reads
   the same YAML as everything else and writes nothing.

## Material identity

A **material** is a part plus what has been done to it, not a new ingredient:

| Kind | Example | Where it comes from |
| --- | --- | --- |
| part | broccoli stems | tomato.yaml `parts` |
| fraction | broccoli stem peel, carrot pulp, courgette water | an operation's secondary output, from the part's `outer_layer` or by extraction |
| geometry | carrot julienne | a cutting operation; named by a `preparations` id |
| state | roasted carrot, dried peel | a thermal, chemical or mechanical operation |
| composite | breaded courgette | an operation that adds an ingredient (`adds:`) |

Each material carries its properties, its edibility, the path that made it,
and the added ingredients. Two paths that end in the same ingredient, part,
fraction, form and properties are **the same material**; the generator keeps
the shortest path and lists the others.

**Known asymmetry.** Tomato skin is a part (ADR 0002 made it one because the
curated model processes it into a powder). Broccoli stem peel, carrot peel and
courgette skin are `outer_layer` fractions. Rule: a layer becomes a part when
the curated model processes it as a thing of its own.

## Applicability

Three-valued, unlike the family generator:

- A requirement on a property the material **does not state** is *unknown*,
  never false. The only exceptions are the flags `part_properties.yaml`
  records only when true (`thin`, `leafy`, `liquid`, `browns_when_cut`); that
  convention is documented in the file.
- Results: **applicable**, **conditional** (a stated condition applies, such
  as "peel first: the outer layer is too tough"), **inapplicable**, **unknown**,
  **unsafe** (the material is not safe to eat, or the operation's
  `unsafe_when` holds).
- Every result carries its reasons: each requirement's `why`, met or unmet.
- A part that is not food is *inapplicable* (avocado skin: not eaten) or
  *unsafe* when its curated reason is safety (avocado stone).

## Sequences

- Each step must accept its input, change at least one property, and give
  outputs that can be inputs again.
- Bounded: depth 3; an operation once per path; cuts only make pieces smaller;
  unknown and unsafe steps are not taken; equivalent materials merge.
- Deterministic: operations and parts are visited in a fixed order.
- Every path keeps the reasons for every step.

## Evidence

Kept apart, as the brief asks:

| Type | Stored where |
| --- | --- |
| Established operation | `operations.yaml` `evidence` + `confidence` |
| Established applicability | an operation's `established_on` list (ingredient.part) |
| Established application | the experiment list (`experiments.md`), from sources checked this round |
| Mechanistic inference | any generated step that is not established on the material |
| Unverified possibility | a generated path |
| Personally tested / failed | `tastings.yaml`, unchanged |

RecipeNLG is not used to decide what can be explored. No new corpus run is
needed for this round.

## Functions

What a material is *for* (crisp component, noodle or sheet, seasoning powder,
broth base, thickener, wrapper...) is a third vocabulary, separate from roles
(what a plate lacks) and flavour dimensions (what you taste). Functions are
derived from the material's properties by rules in `operations.yaml`. Where a
function is also a role (crunch), the link is named, not merged.
