Food-prep — Product and System Design
Status
Concept and design direction.
Food-prep currently contains a working ingredient-transformation ontology, SQLite data model, query layer, test suite, CLI, and Streamlit exploration interface. The existing implementation proves that transformed ingredient states, missing culinary roles, pairings, and plate profiles can be represented as structured data.
It does not yet fully express the intended product.

1. Product vision
Food-prep is a local-first cooking knowledge system built around two connected questions:
    1. What useful thing can I do next with the food I have?
    2. What ingredient combinations should plausibly work, despite being rare or absent in conventional recipe material?
These are not separate products.
The first question provides practical cooking value and establishes a structured baseline of known culinary behaviour.
The second question uses that structure to explore the edges of established cooking knowledge.
Food-prep should therefore support two modes:
Cook
Cook helps the user turn an ingredient or prepared component into something useful.
It answers:
    • What can this ingredient become?
    • How will each transformation change it?
    • What can I do with the state I already have?
    • Which ingredients I own are useful here?
    • What flavour or texture is missing?
    • What is the next sensible move?
    • Where can this path lead?
Cook should prefer established, culturally recognisable and reasonably reliable combinations.
Scout
Scout searches for plausible but uncommon culinary combinations.
It answers:
    • What combination appears structurally compatible?
    • Why should it work?
    • Which known culinary relationship supports the hypothesis?
    • How common is the combination in available recipe evidence?
    • What is the likely failure mode?
    • How can the idea be tested in a small, controlled way?
Scout does not claim to discover combinations nobody has ever cooked.
It identifies combinations that are uncommon or absent in the evidence searched, despite having understandable culinary support.

2. The important question
The central research question is:
Given what is known about ingredient transformation, flavour balance, texture, culinary function and established analogies, which ingredient combinations should plausibly work but are rare or not observed in known recipe material?
This question must remain visible throughout the project.
The practical Cook system should not gradually consume the whole project and reduce Scout to a novelty tab. Cook provides the map of known territory. Scout uses that map to identify promising gaps.
The project is not primarily a recipe generator.
It is a system for modelling:
    • how ingredients change;
    • what transformed states contribute;
    • what those states need;
    • how culinary combinations are structured;
    • which known structures could support unfamiliar combinations;
    • how speculative ideas can be tested honestly.

3. Product promise
A concise product promise:
Food-prep maps how ingredients change and what can happen next. It helps users follow reliable cooking paths or investigate combinations that appear plausible but uncommon in established recipe culture.
A more user-facing version:
Start with an ingredient, a prepared component, or food already on your plate. Food-prep shows a few useful paths forward, explains how each move changes flavour and texture, and can suggest uncommon combinations worth testing carefully.

4. Design principles
4.1 The recipe is not the core object
Recipes are nearly infinite and often repeat the same underlying structures.
Food-prep should model reusable culinary knowledge:
    • transformations;
    • ingredient states;
    • flavour directions;
    • texture changes;
    • functional roles;
    • destinations;
    • corrections;
    • transitions;
    • analogies;
    • evidence.
A recipe may later be generated or assembled from these structures, but it is not the foundation.
4.2 Transformed state matters
An ingredient is not one fixed culinary object.
Raw broccoli, steamed broccoli, charred broccoli and fermented broccoli stem have different:
    • flavour profiles;
    • textures;
    • risks;
    • useful pairings;
    • possible destinations;
    • correction needs.
Compatibility should therefore normally be evaluated against a transformed state, not only against a raw ingredient name.
4.3 Cooking is a journey, not a card
The current transformation card is useful but too static.
The product-facing model should be:
ingredient → preparation → transformation → flavour direction → correction or finish → destination
Examples:
broccoli → sliced stems → stir-fried → salty and umami → vinegar finish → rice bowl
cabbage → shredded → salted and rested → sour and nutty dressing → sesame finish → cold side dish
roasted mushroom → crushed → tart berry contrast → toasted seed finish → toast or dumpling filling
Each stage should create meaningful next steps.
4.4 Model momentum before completeness
The system does not need to prove that every dish is universally balanced.
It needs to help the user make the next good move.
“Missing roles” should be treated as contextual advice, not as a universal law that every plate must contain salt, fat, acid, herb, crunch, carbohydrate and protein.
4.5 Novel does not mean good
Low recipe co-occurrence is not evidence of quality.
A Scout candidate must be supported independently by compatibility reasoning.
The target is:
high or moderate compatibility evidence + low observed usage
Not:
low observed usage = interesting
4.6 Explain the chain of inference
A Scout result should never be only a mysterious score.
It should explain:
    • what transformation state is being considered;
    • what the dominant sensory characteristics are;
    • what the candidate contributes;
    • whether it reinforces or contrasts;
    • what known analogy supports the idea;
    • why the combination appears uncommon;
    • what could go wrong;
    • how to test it.
4.7 Curated knowledge owns culinary meaning
Corpus co-occurrence can support or challenge a hypothesis, but it should not independently invent culinary roles.
“Frequently seen together” does not explain why ingredients work together.
A pairing may co-occur because of geography, availability, recipe convention or dataset bias. Culinary role and transformation fit should remain explicit.
4.8 Honest uncertainty
The system must distinguish:
    • established;
    • plausible;
    • speculative;
    • unsupported;
    • unknown.
“Not found” must always mean:
not observed in the searched evidence
It must not mean:
nobody has ever cooked this

5. Flavour and texture model
The existing role system should remain available for practical functions such as acid, fat, protein, carbohydrate and carrier.
However, the main sensory model should become more expressive and less tied to a generic Western balanced-plate checklist.
A Chinese-culinary-inspired flavour framework can provide the conceptual foundation, without claiming to represent all Chinese cuisines or a single authentic doctrine.
Primary flavour dimensions
    • salty
    • sour
    • sweet
    • bitter
    • umami
    • pungent
    • aromatic
    • nutty or toasted
    • fresh or green
    • fermented or funky
    • rich or fatty
Texture dimensions
    • crisp
    • crunchy
    • tender
    • soft
    • silky
    • juicy
    • dry
    • chewy
    • sticky
    • dense
    • creamy
    • fibrous
Additional behaviour
Each state should also describe:
    • intensity;
    • moisture;
    • heaviness;
    • temperature suitability;
    • dominant versus supporting use;
    • common failure risks.
Transformation effects
Transformations should describe directional changes rather than only resulting labels.
Examples:
    • roasting increases sweetness, browning, toasted character and concentration;
    • charring may add smoke and bitterness;
    • steaming softens while preserving freshness and moisture;
    • frying increases richness, browning and crispness;
    • crushing may release pungency or create a sauce-compatible texture;
    • salting and draining reduces water and concentrates flavour;
    • fermenting increases acidity, funk and sometimes umami;
    • blanching may reduce harshness while preserving colour and freshness.
The transformation itself becomes part of the explanation.

6. Core concepts
6.1 Ingredient
The canonical food item.
Examples:
    • broccoli
    • cabbage
    • mushroom
    • blackcurrant
    • sesame
    • potato
6.2 Preparation
A physical change that does not necessarily create a new cooked state.
Examples:
    • chopped
    • sliced
    • shredded
    • crushed
    • grated
    • peeled
    • scored
    • separated into stems and florets
Preparation matters because shape changes:
    • surface area;
    • moisture loss;
    • browning;
    • cooking time;
    • texture;
    • sauce adherence;
    • possible destinations.
6.3 Transformation
A state-changing process.
Examples:
    • steam
    • roast
    • char
    • stir-fry
    • simmer
    • salt and drain
    • ferment
    • pickle
    • dry
6.4 Component or state
The reusable result of preparation and transformation.
Examples:
    • charred broccoli florets
    • steamed broccoli stems
    • fermented cabbage
    • roasted mushroom paste
    • caramelised onion
    • salted cucumber
Components should be directly usable by both ingredient exploration and plate reasoning.
The current separation between transformed components and independently authored plate profiles should eventually be removed or explicitly linked.
6.5 Flavour route
A reusable seasoning or balancing direction.
Examples:
    • soy and garlic
    • sesame and vinegar
    • ginger and scallion
    • chilli and fermented umami
    • sweet and sour
    • toasted nut and sharp fruit
    • creamy and acidic
    • browned aromatic and herb
A flavour route should specify:
    • flavour dimensions;
    • typical ingredients;
    • suitable transformations;
    • possible finishes;
    • common destinations;
    • unsuitable states;
    • likely risks.
Flavour routes reduce the need to hard-code every pairing independently for every transformation.
6.6 Correction
A move made in response to the current sensory state.
Examples:
    • too flat → salt, acid or aromatic;
    • too sweet → acid, bitter or heat;
    • too bitter → fat, sweetness or salt;
    • too soft → crisp or crunchy finish;
    • too dry → sauce, broth or fat;
    • too rich → acid, freshness or pungency;
    • too watery → concentration, starch or drainage;
    • too aggressive → mild base, fat or dilution.
6.7 Destination
The kind of culinary outcome the path is moving toward.
Examples:
    • side dish
    • complete savoury plate
    • rice bowl
    • noodles
    • soup
    • salad
    • toast or sandwich
    • filling
    • sauce or base
    • condiment
    • preserved component
    • batch-prepared ingredient
Destinations provide context for what is genuinely missing.
A side dish, soup and complete meal should not be judged against the same target-role list.
6.8 Transition
A meaningful connection between states.
Suggested structure:
from_state → move → to_state → reason → confidence
Examples:
    • steamed broccoli → cool and dress → cold broccoli side → absorbs sour and nutty dressing well;
    • roasted mushroom → crush → mushroom paste → suitable for toast, dumpling filling or sauce base;
    • salted cabbage → ferment → fermented cabbage → longer storage, increased acidity and funk.
Transitions are the roadmap inside the food model.
6.9 Analogy
A known relationship that supports an unfamiliar one.
Examples:
    • tart berries work with rich savoury foods;
    • mushrooms share dark savoury and umami characteristics with some meat applications;
    • therefore mushroom plus tart berry may deserve testing in a transformed state.
An analogy should identify:
    • known pairing;
    • substituted element;
    • shared culinary function;
    • meaningful difference;
    • expected risk.

7. Cook mode
Purpose
Cook helps users make practical decisions from ingredients or prepared food.
Main entry points
    • I have an ingredient.
    • I already prepared or cooked it.
    • I have several ingredients available.
    • I have a plate that feels incomplete.
    • I want to make something for later.
    • I need to use leftovers.
Suggested interaction
    1. What do you have?
    2. What state is it in?
    3. What are you trying to make?
    4. How much effort do you want?
    5. Show a few useful paths.
Example output
Path: Roasted broccoli rice bowl
Prepare
Cut the florets small enough to brown while keeping the stems for slicing.
Transform
Roast or hard stir-fry.
What changes
Sweetness and toasted flavour increase. The surface becomes dry and browned while the interior stays tender.
Flavour direction
Salty, sour and nutty.
Use what you have
Soy provides salt and umami. Vinegar provides sourness. Sesame or peanuts provide toasted richness.
Destination
Rice bowl or noodle topping.
Watch for
Too much sweet sauce can make the browned broccoli cloying. Add acid before adding more sweetness.
Cook ranking factors
    • desired destination;
    • ingredient state;
    • available ingredients;
    • time and effort;
    • equipment;
    • confidence;
    • batch-prep value;
    • perishability;
    • number of useful available ingredients;
    • likely sensory coherence.
“Best branches” should eventually mean best for the current situation, not merely highest-confidence database records.

8. Scout mode
Purpose
Scout finds uncommon combinations that are worth tasting.
Candidate requirements
A candidate should normally have:
    1. a defined transformed state;
    2. at least one compatibility mechanism;
    3. at least one supporting analogy or structural reason;
    4. low or absent observed use in the searched corpus;
    5. a documented risk;
    6. a small tasting protocol.
Compatibility mechanisms
Reinforcement
The ingredients strengthen a shared characteristic.
Example:
    • roasted ingredient + toasted seed
Contrast
One ingredient balances a dominant quality in the other.
Example:
    • rich or sweet state + sharp sour ingredient
Functional completion
The candidate fills a missing culinary function.
Example:
    • dry dense component + hydration or sauce
Aroma bridge
A third characteristic or ingredient connects two otherwise distant elements.
Example:
    • mushroom + berry connected through black pepper, juniper or browned onion
Texture contrast
The pairing gains value through physical contrast.
Example:
    • soft component + crisp seed or pickle
Transformation fit
The candidate becomes plausible only after a particular state change.
Example:
    • raw cabbage + berry may be awkward;
    • charred or fermented cabbage + restrained berry acidity may be plausible.
Analogue substitution
A rare pairing is derived by substituting an ingredient with another that performs a similar culinary role.
Novelty model
Novelty must be scored separately from compatibility.
Suggested novelty classes:
    • common
    • established
    • uncommon
    • rare
    • not observed in searched material
    • insufficient evidence
Sources may include:
    • structured recipe datasets;
    • cookbook indexes;
    • ingredient co-occurrence data;
    • culinary pairing sources;
    • regional recipe corpora;
    • user tasting history.
Dataset absence must be recorded with source scope and search date.
Scout result format
Candidate
Charred cabbage + blackcurrant vinegar + toasted sesame
State
Charred cabbage: sweet, browned, mildly bitter, sulfurous, firm and soft.
Why it may work
    • Blackcurrant vinegar supplies sharp acidity and dark fruit.
    • Acid can balance the sweetness and richness produced by browning.
    • Sesame reinforces the toasted character and supplies fat.
    • The combination resembles the structure of browned vegetable + tart condiment + toasted seed.
Analogy
Cabbage commonly accepts vinegar and mustard. Tart berries commonly work with browned or rich savoury foods. Blackcurrant vinegar may occupy a similar sharp-condiment role while adding fruit aroma.
Novelty
Rare or not observed in the selected recipe corpus.
Main risk
The berry character may make the cabbage taste sweet or jam-like.
Small test
Dress one small piece with a few drops of blackcurrant vinegar and a pinch of toasted sesame. Taste before adding sweetness.
Success condition
The vinegar should sharpen the browned cabbage without reading as dessert.
Possible correction
If too fruity, increase salt or dilute with ordinary vinegar.

9. Scoring and ranking
Scout should avoid collapsing everything into one unexplained number.
Internally, separate scores may be useful, but the interface should show the reasoning.
Compatibility dimensions
    • flavour reinforcement;
    • flavour contrast;
    • functional role fit;
    • texture fit;
    • transformation fit;
    • analogy strength;
    • cultural precedent;
    • practical feasibility.
Novelty dimensions
    • direct co-occurrence frequency;
    • number of distinct recipe contexts;
    • regional diversity;
    • recency;
    • corpus coverage;
    • evidence quality.
Risk dimensions
    • likely domination;
    • conflicting bitterness;
    • excessive sweetness;
    • excessive acidity;
    • textural incompatibility;
    • aroma clash;
    • unsafe preparation or preservation;
    • dependence on precise ratios.
Candidate classes
Reliable Cook
Strong culinary precedent and good contextual fit.
Exploratory Cook
Uncommon but supported strongly enough for normal use.
Scout candidate
Plausible, rare and worth a small test.
Weak hypothesis
Interesting structural connection but insufficient support.
Rejected
Novel but lacking meaningful compatibility, impractical or predictably unpleasant.
Rejected candidates should be retained where useful. Knowing why an idea was rejected prevents the system from repeatedly rediscovering the same rubbish.

10. Storytelling and explanation
The storytelling layer is not decorative copy.
It is the user-visible form of the reasoning model.
Every path should answer:
    1. Where am I?
    2. What will this move change?
    3. Why would I choose it?
    4. What becomes possible afterward?
    5. What does the next ingredient contribute?
    6. What could go wrong?
    7. Where does the path end?
The system should prefer short chains of cause and effect over piles of tags.
Weak output:
Tags: sweet, umami, roasted. Missing: acid, herb, protein.
Stronger output:
Roasting makes the cabbage sweeter and more concentrated. A sharp vinegar prevents that sweetness becoming heavy, while toasted sesame reinforces the browned flavour. This route works best as a side dish or rice topping rather than as a complete meal by itself.
Tags can remain visible in the workshop and debug layers.
The main user interface should tell the story.

11. User interface structure
Main interface
Start
    • available ingredient or component;
    • current state;
    • desired outcome;
    • effort level;
    • optional available ingredients.
Result
Show approximately three paths.
Each path should include:
    • preparation;
    • transformation;
    • sensory change;
    • flavour route;
    • useful available ingredients;
    • missing element;
    • destination;
    • risk;
    • reason for ranking.
Scout interface
Scout should be a first-class view, not a warning cupboard at the back.
Possible sections:
    • promising candidates;
    • why they may work;
    • novelty evidence;
    • analogy chain;
    • smallest useful test;
    • tasting result;
    • rejected candidates.
Workshop interface
The current tabs remain valuable for development and curation:
    • Ingredient Explorer
    • Component Explorer
    • Plate Balance
    • Filler Profiles
    • Evidence
    • Raw records
    • Scout records
    • Ontology diagnostics
These should eventually sit under a Workshop, Model or Curator section.
The current interface is a strong ontology inspection tool. It should not be discarded merely because it is not the eventual consumer-facing product.

12. Data model direction
The existing schema can evolve rather than being replaced wholesale.
Likely additions:
preparations
    • preparation_id
    • name
    • surface_area_effect
    • moisture_effect
    • texture_effect
    • notes
state_preparations
Links preparations to ingredient states.
flavour_dimensions
    • flavour_dimension_id
    • name
    • family
    • description
state_flavour_values
    • state_id
    • flavour_dimension_id
    • intensity
    • confidence
    • evidence
texture_dimensions
Equivalent structure for texture.
flavour_routes
    • route_id
    • name
    • description
    • confidence
    • cultural_context
flavour_route_elements
    • route_id
    • ingredient_id or function
    • contribution
    • optionality
    • notes
destinations
    • destination_id
    • name
    • required_functions
    • useful_functions
    • irrelevant_functions
    • constraints
state_transitions
    • from_state_id
    • move_type
    • move_id
    • to_state_id
    • reason
    • confidence
analogies
    • source_pairing
    • candidate_pairing
    • substituted_element
    • shared_function
    • meaningful_difference
    • confidence
    • notes
novelty_observations
    • candidate_pairing
    • corpus_id
    • observed_count
    • context_count
    • search_scope
    • search_date
    • result_class
tasting_trials
    • candidate_id
    • preparation
    • ratio
    • outcome
    • failure_mode
    • adjustment
    • verdict
    • notes
candidate_hypotheses
    • candidate_id
    • state_a
    • ingredient_or_state_b
    • compatibility_summary
    • novelty_class
    • risk_summary
    • status
The word filler should probably become an internal legacy concept or be replaced with a more neutral term such as:
    • addition;
    • supporting ingredient;
    • role provider;
    • pairing ingredient.
“Filler” makes sense in the current database logic but understates ingredients that can materially define the dish.

13. Evidence strategy
Food-prep should combine several evidence types without pretending they are equivalent.
Curated culinary evidence
Human-authored judgment about:
    • role;
    • transformation;
    • correction;
    • analogy;
    • likely failure.
Recipe-corpus evidence
Used for:
    • commonness;
    • context;
    • novelty;
    • recurring ingredient clusters.
Not used alone to declare culinary compatibility.
Scientific or aroma evidence
Potentially useful as secondary support.
Shared flavour compounds must not become the primary pairing rule. Chemical overlap can suggest a hypothesis but cannot guarantee sensory success.
User tasting evidence
Over time, controlled tasting results may become the most valuable original dataset in the project.
A result should record not only “worked” or “failed,” but:
    • state;
    • proportions;
    • preparation;
    • temperature;
    • supporting ingredients;
    • failure mode;
    • successful correction.

14. Safety and boundaries
Food-prep must treat food safety separately from flavour confidence.
The system should not casually improvise guidance for:
    • canning;
    • anaerobic storage;
    • fermentation;
    • preservation;
    • wild mushrooms;
    • toxic plants;
    • allergens;
    • raw animal products.
Preservation advice should rely on recognised safety sources and validated procedures.
Scout experimentation should normally focus on flavour combinations using safely prepared ingredients.
A speculative pairing must never imply speculative food safety.

15. Non-goals
Food-prep is not initially intended to be:
    • a complete recipe database;
    • a meal-planning subscription service;
    • a nutrition optimiser;
    • a grocery delivery system;
    • a universal model of culinary authenticity;
    • a claim that chemistry can predict taste;
    • an autonomous recipe generator;
    • a replacement for sensory testing;
    • proof that an absent corpus pairing has never existed.

16. Success criteria
The concept has become a product when it can do all of the following:
    1. Accept an ingredient or transformed component as a starting state.
    2. Show several meaningful next paths rather than a flat transformation list.
    3. Explain how each move changes flavour and texture.
    4. Use available ingredients to rank or complete the paths.
    5. Adjust advice according to the desired destination.
    6. Generate at least one Scout candidate through an explicit compatibility and analogy chain.
    7. Show separate compatibility and novelty evidence.
    8. Provide a small tasting protocol.
    9. Record the result of that tasting.
    10. Avoid presenting uncertainty or corpus absence as certainty.
The strongest proof is not the number of ingredients in the database.
It is one complete, convincing journey from:
known ingredient state
to:
useful path
and then, separately:
uncommon hypothesis
to:
controlled tasting result.