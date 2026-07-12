# Food-prep roadmap

Development follows one rule: prove the complete product loop with a small
ingredient set before expanding coverage.

## 0. Preserve the foundation

Keep the SQLite schema, YAML compiler, query layer, CLI, exports, tests, and
Streamlit Workshop working. Prefer additive schema evolution and compatibility
layers over deletion.

Exit: the current test suite passes and Cook/Scout parity is documented.

## 1. Establish shared language

Define canonical preparation, transformation, flavour, texture, correction,
destination, confidence, and uncertainty vocabularies. Store authorable values
in YAML and validate unknown or duplicate identifiers before database writes.

Exit: Cook and Scout can describe states with the same validated vocabulary.

## 2. Complete the broccoli pilot

Build four causal journeys covering stir-fried stems, roasted florets, steamed
and dressed florets, and roasted broccoli crushed into a sauce, spread, or
filling. Add structured data, query output, CLI rendering, and end-to-end tests.

Exit: a user can follow each path without reading database terminology.

## 3. Add destination-aware reasoning

Introduce destination profiles and replace universal plate targets with
contextual required, useful, optional, and unsuitable functions. Preserve the
current behavior as the `complete_savoury_plate` profile.

Exit: sides, soups, and complete plates receive different gap advice.

## 4. Unify states and profiles

Link transformed components to sensory and plate profiles so journey output can
enter destination reasoning directly. Retain lightweight compatibility profiles
for foods without full ingredient trees.

Exit: a journey state needs no separately authored shadow record.

## 5. Add reusable flavour routes

Start with soy and garlic, sesame and vinegar, and ginger and scallion; then add
chilli and umami, sweet and sour, and toasted nut and sharp fruit. Support
destination fit, available-ingredient matching, substitutions, risks, and
causal explanations.

Exit: Cook proposes coherent directions instead of loose additions.

## 6. Generate Scout hypotheses

Use transparent rules based on contrast, reinforcement, functional completion,
texture, transformation fit, aroma bridges, and analogy substitution. Preserve
rejection reasons and never allow rarity alone to imply quality.

Exit: Scout generates a plausible candidate without a manually authored final
pairing record.

## 7. Measure novelty

Ingest one legally usable recipe corpus locally. Normalize aliases, retain
corpus metadata, count co-occurrence and distinct contexts, and distinguish
zero observations from insufficient coverage.

Exit: every novelty statement names its evidence scope.

## 8. Close the tasting loop

Record the transformed state, candidate, ratio, smallest test, success
condition, likely failure, correction, safety note, and structured verdict.

Exit: one hypothesis is physically tested for the first product proof; five
recorded candidates complete the broader tasting phase.

## 9. Build the guided interface

Add a consumer Cook flow, first-class Scout view, and Workshop navigation only
after the text reasoning is convincing.

## 10. Expand carefully

Add an ingredient only when it contributes distinct states, sensory shifts,
multiple destinations and flavour routes, risks, Cook evidence, and a Scout
opportunity.
