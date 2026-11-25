# Literature review: what has already been solved

One section per area. Each says:
- what the work represents and what it is for;
- what is **published** (demonstrated with data, an implementation or a
  study) against what is only claimed;
- what it leaves unsolved.

Full entries, failed pages, search logs and citation trails are in the
seven `evidence-*.md` files. Ids resolve in `sources.md`.

## 1. Food process and recipe ontologies (`evidence-ontologies.md`)

**What it is.** OBO-family ontologies (FoodOn, BFO, OBI, IAO, COB) model a
food process as a *planned process*:
- typed input and output materials carrying qualities;
- a separate plan specification;
- optional objectives (Y100, Y104, Y112).

Dooley and Naravane separate a process's **mechanism** (how) from its
**objective** (why), so that different mechanisms can share one objective
(Y101). INRAE's PO2/TransformON records real transformation processes
(dairy, bread, among others) as steps with control parameters,
observations, and routes split by parameters or input compositions (Y102,
Y103). Two design patterns, state transition and material transformation,
give reusable shapes (Y108, Y109). A substitution design pattern reifies a
substitution with its conditions and instruction changes (Y105 = Y401).

**Published.**
- PO2 is used on real data, not cooking.
- The FoodOn requirements paper gives worked models and states the limits
  of OWL:
  - it cannot infer step order;
  - it cannot keep a material's identity through a change, so history
    becomes a provenance trail (Y100 §2.1.2, §2.1.5).
- It also shows that one process-and-object graph can be read as an
  object view or a process view (Y100 Figs. 4-5).

**Not solved.**
- No ontology distinguishes readiness from doneness.
- None models a member that keeps changing inside an assembly; FoodOn's
  "has part" assumes the part is unchanged (Y104).
- None says when two histories give interchangeable states. Y101 says
  same-named states are comparable only if their processing was comparable
  (frozen carrots), but gives no rule.
- No ontology was evaluated on cooking outcomes.
- schema.org Recipe and the recipe knowledge graphs hold text steps, not
  processes (Y107, Y106, Y114).

## 2. FOON and robotic cooking (`evidence-foon-robotics.md`)

**What it is.** A bipartite network of object nodes (name plus state,
contents, location) and motion nodes. A *functional unit* takes input
objects through one motion to output objects (Y201). Networks from many
videos are merged into a universal FOON (Y202). *Task-tree retrieval*
searches backwards from a goal against a kitchen inventory (Y201, Y206).
Later work weights units by robot success (Y203), compiles FOON to PDDL
(Y208), and uses LLMs with FOON as a verifier (Y209-Y212). KnowRob is a
broader robot knowledge base (Y216).

**Published.**
- Retrieval works on the merged network.
- Approximate retrieval with word or WordNet similarity made 76% of test
  recipes fully correct. Errors were 39% wrong substitutes, 27% wrong
  states, 14% wrong motions and 20% wrong integration (Y206; checked in
  raw text).
- Kale and cabbage appear as a similar pair (Y206 Fig. 7).
- FOON's correctness is judged by people reading generated text or
  progress lines. Nothing was cooked.

**Not solved.**
- Times, waits, reasons for a stage, and readiness against doneness are
  absent (Y217 says so for its own graph).
- After mixing or filling, the composite carries the state: R3's gap.
- The merge recombines units from different sources freely, presented as a
  strength (Y201 VI-A), with no evidence kept per route.

## 3. Case-based reasoning and workflow adaptation (`evidence-cbr-workflows.md`)

**What it is.**
- Trier's process-oriented CBR represents a recipe as a workflow:
  - tasks and data items (ingredients and intermediates);
  - control blocks for sequence, parallel, alternative and loop (Y302).
- Adaptation works in three ways:
  - swapping *workflow streams* that use and make the same ingredients
    (Y301, Y302);
  - *generalised workflows* (Y303);
  - learned *operators* with add and delete lists (Y305).
- CookingCAKE combines these for the Computer Cooking Contest (Y300).
- Nancy's Taaable adapts by minimal query generalisation, contextual
  substitution rules and grafting a documented preparation for the new
  ingredient (Y311, Y413).
- A revision-based method repairs temporal constraints after a swap (Y309).

**Published.**
- From 61 sandwich recipes, generalisation enables more than 9·10^21
  recipes (Y300 §5; checked in raw text). That is the clearest statement
  anywhere of how far "valid by structure" outruns "documented".
- In blind expert ratings, 44-46% of ratings put the adapted workflow below
  the original (Y302, Y303).
- Nothing was cooked.
- Durations and "meanwhile" cannot be expressed in plain workflows
  (Y310 §2).

**Not solved.**
- Intermediate products are named in three inconsistent ways.
- Readiness and failure are not represented.
- Stream interfaces check ingredient **names**, not states, so they would
  accept K1-x and K2-x.
- Starting from partial workflows is defined but never demonstrated.
- No German-language report was found online.

## 4. Ingredient substitution (`evidence-substitution.md`)

**What it is.**
- **Data-driven finders:**
  - substitute networks mined from recipe reviews (Y406 = Y701);
  - diet-log substitutes (Y407);
  - knowledge-graph substitutes (Y408, Y409);
  - learned in-context substitution on Recipe1MSubs (Y410);
  - LLMs (Y420, abstract).
- **Characteristic-action similarity** within a dish group (Shidochi et al.,
  Y405).
- **The ontology design pattern** (Y401).
- **The UCL logic**:
  - a *primary* substitution;
  - violated *integrity constraints*;
  - minimal *secondary* substitutions as repairs (Y402);
  - with a graph formalism and acceptability tuples (Y403, Y404).

**Published.**
- Y402 proves that a repair need not exist (Proposition 11; checked in raw
  text).
- No evaluation on real recipes was found in the full text.
- Learned finders have weak ground truth:
  - review-mined pairs;
  - context-free guides (the guide behind Y408 lists rutabaga for potato
    with no condition);
  - authors' own labels extended by the models' own predictions (Y409).
- Hit@1 is around 20% in context (Y410).
- No work compares a substituted dish with the original in a kitchen.

**Not solved.**
- Functional roles from food science: no source could be read.
- Substitution of states with different histories.
- Several pieces for one (one-to-many).

## 5. Recipe flow graphs and procedural NLP (`evidence-recipe-graphs.md`)

**What it is.**
- The Japanese recipe flow graph (r-FG):
  - typed spans (food, tool, action, state, duration, quantity);
  - edges in a rooted DAG per recipe (Y501), and its English corpus (Y500).
- Implicit-argument action graphs (Y504).
- Ingredient merge trees (Y505).
- A rich annotation schema with Why, If and Until tags (RiCoRecA, Y502).
- Per-step world-state annotation (Y507).
- **Cross-recipe alignment** of the same dish:
  - at action level (ARA: 79% human, 72.4% model; Y503, checked in raw
    text);
  - at sentence level (MM-ARC: text-text F1 54.55; Y506).

**Published.** Annotation agreement and corpus sizes. Models fail most on
splits, discards and recombination (Y507). The aggregation of aligned
recipes into a "common and variant" structure is stated as future work
(Y503 §6).

**Not solved.**
- No readiness against doneness and no failure states.
- No members after assembly (Y507's handling of merges was not verified).
- The r-FG authors say their graphs are not for display to cooks (Y500).
- The one paper that may merge flow graphs of one dish (Yamakata et al.
  2016) was not found.

## 6. Industrial batch, planning and process diagrams (`evidence-industrial-process.md`)

**What it is.** ISA-88 (IEC 61512) separates:
- a recipe's header, formula (inputs, outputs, parameters), equipment
  requirements and procedure;
- four recipe types:
  - *general* and *site*: equipment-independent;
  - *master*: for one cell;
  - *control*: one batch.

A general recipe is turned into a master recipe and validated in trial
(Y602, Y603). Part 4 keeps records for intermediate lots (Y604). Process
manufacturing systems keep separate recipes with validity rules and
co-products (Y608).

The State-Task Network schedules states and tasks under storage policies
(unlimited, finite, none, zero-wait) (Y605, Y606). A canned-fish plant adds
a maximum wait between stages (Y607). Grafcet transitions are observable
conditions (Y602).

The Codex General Principles require a flow diagram and critical limits
that are validated, monitored and corrected (Y611). Food service groups
foods by how many times they passed through the danger zone (Y612).
Ruokavirasto's cooling rule is Y613. A Petri-net robot kitchen (Y614) and a
pastry ontology (Y615) were read.

**Published.**
- The standards and their terminology; STN as a solved scheduling
  formulation; a real fish-plant schedule (Y607).
- No published test of ISA-88 on cooking.
- BPMN and UML for cooking: no academic model found.

**Not solved.** Every industrial model treats a joined material as one
material, so members after assembly are not represented. Readiness against
doneness is not a concept.

## 7. Visualisation for people deciding what to cook (`evidence-visualisation.md`)

**What it is.**
- RecipeScape clusters hundreds of recipes of one dish for analysts (Y700).
- Ingredient and flavour networks (Y701, Y702).
- Studies of graph perception:
  - node-link against matrix (Y705);
  - layout over-reading (Y706).
- A review of comparative layouts (Y707).
- Multi-list recommender interfaces (Y708).
- Japanese parallel-cooking schedulers (Y709, Y710) and a sensing kitchen
  (Y711).
- A taste-map persuasion study (Y712).
- **Buykx's controlled cooking study** of recipe presentations (Y703).

**Published.**
- Buykx: 24 participants (university students, 8 per condition)
  preferred an overview that showed the recipe's structure with its
  sub-goals. It let them understand the process and plan parallel work, and
  reduced problems from recipe content. It made no difference to cooking
  time (Y703 ch. 7; checked in raw text).
- Aligned, item-wise layouts beat separate charts for finding differences,
  in 15 studies outside food (Y707).
- A displayed taste value shifted ratings without tasting (Y712).
- Flavour networks had to be filtered to be drawable (Y702), and viewers
  over-read node position (Y706).

**Not solved.**
- No study compares a dish-first view with an ingredient map for deciding
  what to cook.
- No evaluated visual form for readiness against doneness, members after
  assembly, or a secondary output that rejoins the dish.
- No peer-reviewed leftover or "start from what I have" interface.

## What researchers have already solved, in short

| Problem | Solved by | Status for Food-prep |
| --- | --- | --- |
| a typed step-and-material unit | ontologies, FOON, STN, workflows, r-FG | Food-prep has it (R1) |
| parallel components and joins | workflows, ISA-88, STN, r-FG | Food-prep has it (R3) |
| retrieval from an inventory | FOON | Food-prep has the safer form (`from_state` lists documented routes only) |
| equipment-independent against equipment-bound recipes; trial before use | ISA-88 | **adopt** the levels |
| storage policies and maximum waits | STN, food-plant scheduling | **extend** intermediates |
| detecting and repairing what a substitution breaks (formally) | UCL logic (untested on recipes) | **adopt** the concept for R4 |
| aligning recipes of one dish | ARA, MM-ARC | **extend**: correspondence for reading only |
| a cook-tested process overview | Buykx | **adopt** for R7 |
| members after assembly | nobody | Food-prep's R5 records are the furthest found |
| readiness against doneness | nobody | Food-prep only |
| keeping combinations of documented steps unverified | ISA-88 (trial), nobody in cooking research | Food-prep's rule; keep it |
