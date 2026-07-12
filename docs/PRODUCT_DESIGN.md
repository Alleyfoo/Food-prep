# Food-prep product design

Food-prep is a local-first cooking knowledge system with two equally important
product modes:

- **Cook** turns an ingredient or prepared state into a useful, explainable
  next path using established culinary knowledge.
- **Scout** identifies plausible but uncommon combinations, explains their
  compatibility and uncertainty, and proposes a controlled tasting method.

The core object is a transformed ingredient state, not a recipe. Product
answers should form a short causal journey:

`ingredient -> preparation -> transformation -> sensory change -> flavour route -> correction or finish -> destination`

## Product principles

1. Model transformed states rather than treating an ingredient as fixed.
2. Help the user make the next good move instead of enforcing universal plate
   completeness.
3. Keep compatibility, novelty, and risk as separate claims.
4. Let curated culinary knowledge define meaning; corpus occurrence supplies
   evidence about commonness, not compatibility by itself.
5. Explain recommendations through cause and effect rather than opaque scores
   or raw tag lists.
6. Treat uncertainty honestly. "Not observed" always refers to a named,
   scoped body of evidence.
7. Keep food-safety claims independent from flavour confidence.

## First product proof: one ingredient, two truths

Before expanding the catalogue, one pilot ingredient must support:

- four complete Cook journeys;
- at least three destination types;
- at least three reusable flavour routes;
- one Scout hypothesis generated through an explicit analogy;
- separate compatibility and novelty evidence;
- a small tasting protocol and an honestly recorded result.

The existing Streamlit tabs remain valuable as the **Workshop** interface for
curation, inspection, and debugging. A guided consumer interface follows only
after the text journey and reasoning loop are convincing.

## Boundaries

Food-prep is not initially a recipe database, meal-planning service, nutrition
optimizer, autonomous recipe generator, or proof that an unobserved pairing has
never existed. Machine learning, embeddings, cloud infrastructure, and broad
catalogue expansion are deliberately postponed.

Speculative flavour experiments must use safely prepared ingredients. Canning,
anaerobic storage, fermentation, preservation, wild foods, allergens, and raw
animal products require recognized safety guidance rather than speculative
reasoning.
