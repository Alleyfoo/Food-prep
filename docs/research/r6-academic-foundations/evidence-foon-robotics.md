# Evidence: FOON and robotic cooking knowledge representations

Date read: 2026-11-25. Method: web search (English, Japanese, German), then
full text where it could be had. arXiv PDFs were fetched with the fetch tool,
which saved the binary, and converted locally with `pdftotext`; the extracted
text was read directly. HTML pages (arXiv HTML, ar5iv, Frontiers) were read
through the fetch tool's summary of the whole page, so they are marked
"HTML, read via fetch summary". Forward citations came from the Semantic
Scholar citations listing for the 2016 FOON paper (first 100 of more). One
FOON dataset file was read from the authors' repository. Search languages:
English, Japanese, German. Blocked: MDPI (403), the Japanese ANLP 2024 PDF
(CID fonts did not decode; the English arXiv version of the same work was
read instead), IEEE Xplore not tried (paywall).

Ids Y201-Y219. Food-prep case ids K1-K9 are from the R6 brief.

## Sources

### Y201 - https://arxiv.org/pdf/1902.01537 (record: https://digitalcommons.usf.edu/esb_facpub/81/)
- citation: D. Paulius, Y. Huang, R. Milton, W. D. Buchanan, J. Sam, Y. Sun,
  2016, "Functional Object-Oriented Network for Manipulation Learning",
  IEEE/RSJ IROS 2016, pp. 2655-2662, DOI 10.1109/IROS.2016.7759413 (venue,
  pages and DOI from the USF repository record).
- version read: arXiv v4 (28 Nov 2020), full text. The USF record has no PDF.
- type: primary research.
- E1: a bipartite directed graph of object-state nodes and motion nodes
  (Sec. II). An object node is an object in a state; containers (bowl, pan,
  oven) are objects that hold ingredients (II-A). Each object node is unique
  by name and attributes; motion nodes of one type may repeat (II-A). The
  **functional unit** (input object nodes, one motion node, output object
  nodes) is the minimum learning unit, one atomic action (II-C, Fig. 1); a
  tool's state changes too (knife clean -> dirty, II-A). A per-video
  **subgraph** is annotated by hand; subgraphs are merged into a **universal
  FOON** by a union that keeps a unit only if no identical unit exists (III-B,
  Alg. 1); a parser relabels objects for consistency and writes a records
  file of changes, using WordNet to spot duplicates (III-B).
- E2: 60 videos, 2169 nodes (1229 object nodes, 792 motion instances of 57
  types), 3223 edges (III-B). Centrality analysis: bowl most central;
  pick-and-place then pour most frequent (V). **Task tree retrieval**
  (VI-A, Alg. 2): from a goal node, backward search for units that output
  it; a unit is taken when all its inputs are in the kitchen list K,
  otherwise its missing inputs become sub-goals. Fig. 7-8: two videos'
  ways of making barbecued ribs merged, and a tree mixing both. Motion
  generation by motion harmonics, shown in a Unity simulation (IV, VI-B).
  Demonstrated: graph construction, statistics, one retrieval example,
  simulated motions. Claimed (not evaluated): that merged trees are
  "novel" useful ways to cook (VI-A), similarity-based inference (VII).

### Y202 - https://arxiv.org/pdf/1807.02189v2
- citation: D. Paulius, A. B. Jelodar, Y. Sun, 2018, "Functional
  Object-Oriented Network: Construction & Expansion", IEEE ICRA 2018,
  pp. 5935-5941 (venue and pages as cited in Y206 and Y204); DOI not
  verified.
- version read: arXiv v2 (31 Jul 2020), full text.
- type: primary research.
- E1: adds an object node's **motion identifier** and **ingredient
  content** (II-A); compares FOON to Petri nets (I). Three **levels of
  abstraction** (III-B): 1 object only, 2 object-state (all mixtures
  collapse to one "ingredients mixed inside" node), 3 object-state-content
  (composition kept). Two **generalisations** (IV): FOON-EXP copies units
  for every pair of objects whose WordNet Wu-Palmer similarity is at least
  0.89 (IV-A); FOON-GEN replaces objects by 56 hand-corrected categories
  (spices, leafy and root vegetables, open containers...) over 359 objects
  (IV-B).
- E2: 65 videos; Table I node counts per level (Level 3: 1676 object nodes).
  Experiment (V): 10 trials x 100 random goal nodes with a random subset of
  224 kitchen items; counts goals for which **a task tree was found**:
  REG 15-53, EXP 14-62, GEN 66-87 (Table IV); GEN fastest (Table III).
  Demonstrated: GEN finds trees more often and faster. **Not evaluated**:
  whether any found tree is correct; the authors state that de-generalising
  categories back to objects is still needed (V-C, VI) and ask whether
  scissors can stand for a knife, which depends on what is cut (V-C).

### Y203 - https://arxiv.org/pdf/1905.00502v4.pdf
- citation: D. Paulius, K. S. P. Dong, Y. Sun, 2021, "Task Planning with a
  Weighted Functional Object-Oriented Network", IEEE ICRA 2021 (as cited in
  Y204, Y206); DOI 10.1109/ICRA48506.2021.9561680 per a Crossref search
  result, not opened.
- version read: arXiv v4 (25 Mar 2021), read in part (abstract, weight and
  path-tree sections, searched in the extracted text).
- type: primary research.
- E1: each functional unit gets a **success rate** (0-1) for a given robot,
  dependent on motion and objects; weights are robot-specific and were
  estimated from the authors' experience; impossible motions get 0. A
  **path tree** enumerates all combinations of units reaching the goal so the
  best overall success rate is chosen; tasks are split between robot and
  human assistant.
- E2: experiments with a NAO robot and human help; abstract reports higher
  success with collaboration. Weights are robot capability, not culinary
  outcome.

### Y204 - https://arxiv.org/pdf/2106.00158
- citation: D. Paulius, A. Agostini, Y. Sun, D. Lee, 2021, "A Road-map to
  Robot Task Execution with the Functional Object-Oriented Network", arXiv
  2106.00158 (Y205 and Y206 say featured at UR 2021; not verified).
- version read: arXiv v1, full text.
- type: position paper.
- E1/E2: dataset then 111 subgraphs (II-B). Object nodes identified by type,
  states and sometimes ingredient make-up; motions may be manipulations or
  non-manipulation actions such as frying or baking (II-A). States are what
  tells a robot an action is complete (II-A). Proposes a domain-independent
  UNIFOON grounded into a robot-specific PLANFOON by learning from
  demonstration (III). No experiments.

### Y205 - https://arxiv.org/pdf/2106.00728
- citation: M. S. Sakib, H. Baez, D. Paulius, Y. Sun, 2021, "Evaluating
  Recipes Generated from Functional Object-Oriented Network", arXiv
  2106.00728 (featured at UR 2021 per Y206; not verified).
- version read: arXiv v1, full text.
- type: primary research (small user study).
- E1: rules to turn a task tree into recipe sentences (III-A); portions are
  not in FOON and come from outside; tool-state sentences are dropped.
- E2: 111 FOON recipes vs 111 Recipe1M+ recipes; 9 participants rated 10
  recipes each; t-test and TOST found no significant difference in rated
  correctness, completeness, clarity (Table I). Demonstrated: raters could
  not tell the two apart on those scales. Not shown: that FOON recipes cook.

### Y206 - https://arxiv.org/pdf/2207.03693
- citation: M. S. Sakib, D. Paulius, Y. Sun, 2022, "Approximate Task Tree
  Retrieval in a Knowledge Network for Robotic Cooking", IEEE Robotics and
  Automation Letters (preprint header: accepted June 2022); arXiv DOI
  10.48550/arXiv.2207.03693; journal DOI not verified.
- version read: arXiv v1, full text.
- type: primary research.
- E1: input = an ingredient list of (object, state) pairs plus a dish type
  (Fig. 1). 140 subgraphs from YouTube, ActivityNet and EPIC-KITCHENS
  (II-A). Step 1 (III-A, Alg. 1): among recipes of the same dish class (30
  classes), choose the reference goal node whose stored ingredient list has
  the highest spaCy word-vector similarity; two items count as similar above
  0.90. Step 2 (III-B, Alg. 2): best-first backward search; heuristic =
  overlap between a node's ingredients and the wanted ingredients. Kitchen
  assumed to hold all items, possibly in another state. Step 3 (III-C,
  Table I): modify the tree per ingredient: (1) exact object and state, no
  change; (2) other object, same state: rename (chopped jalapeno -> chopped
  chili pepper; a copy of the units is made if both are needed); (3) same
  object, other state: retrieve units that make the leaf state from the
  given state (whole -> diced tomato); (4) both differ: rename then add
  units. State choice uses a 12-category state taxonomy (from Jelodar &
  Sun 2019) with ties broken by the state most frequent for the dish type;
  the motion is the verb most often used with that state. New branches are
  attached to units that accept many inputs (mix, add to container), never
  to cut units; attachment rules differ per dish type.
- E2: 500 Recipe1M+ recipes (salad, cake, soup, omelette, drinks; 100
  each), judged **by hand** per ingredient via a **progress line** (the
  sequence of states and motions one ingredient passes through, Fig. 4b) on
  a 0/1/2 scale. 76% of recipes fully correct with modification (Fig. 5).
  Error shares (V): incorrect substitution 39%, incorrect state 27%,
  incorrect motion 14%, incorrect integration 20%. Example: apricot's
  nearest FOON object is lemon, so apricot gets squeezed (V). Fig. 7 lists
  top-5 substitutes, e.g. kale -> broccoli, cabbage, zucchini, arugula,
  celery; turnip -> radish, cabbage, carrot, broccoli, celery. Irreversible
  states (melted cheese when diced is wanted) are not counted as errors
  (V). Proposed fix: a user chooses among the top-5 candidates. Same 9-person
  survey design as Y205. Evaluation called subjective by the authors (VI).

### Y207 - https://arxiv.org/abs/2112.02433
- citation: M. S. Sakib, D. Paulius, Y. Sun, 2021, "Functional Task Tree
  Generation from a Knowledge Graph to Solve Unseen Problems", arXiv.
- version read: **abstract only** (earlier form of Y206).

### Y208 - https://arxiv.org/pdf/2207.05800v4.pdf
- citation: D. Paulius, A. Agostini, D. Lee, 2022/2023, "Long-Horizon Task
  Planning and Execution with Functional Object-Oriented Networks", arXiv
  v4 26 Jan 2023; Semantic Scholar lists IEEE RA-L 2022 (not verified).
- version read: arXiv v4, full text (extracted).
- type: primary research.
- E1: a FOON is G = {O, M, E}; a unit FU = {Oin, Oout, m} compared to the
  precondition-action-effect of planning operators (II). Each unit becomes a
  PDDL **macro-operator** with object-centred predicates in/on/under and
  state predicates such as is-whole, is-sliced, is-mixed (III-A, Fig. 3);
  each macro step is then solved as its own **micro** problem from perceived
  object poses (III-B). Action contexts (previous, current, next action +
  trajectory) select motion primitives (IV).
- E2: CoppeliaSim, a universal FOON of 3 subgraphs, Bloody Mary and Greek
  salad, 25 trials each: success 96% / 92% (cocktail whole / partial
  ingredient subset), 80% / 84% (salad) (Table I). An HTN version needed 8
  method variants for pouring alone and 19 methods in total (V-B). FOON-based
  planning faster than one classical problem or HTN (Fig. 8-9). Partial
  recipes are made by dropping ingredients at PDDL level. Stated limitation:
  open-loop execution.

### Y209 - https://arxiv.org/pdf/2309.09181
- citation: M. S. Sakib, Y. Sun, 2023, "From Cooking Recipes to Robot Task
  Trees - Improving Planning Correctness and Task Efficiency by Leveraging
  LLMs with a Knowledge Network", arXiv 2309.09181 v1; Semantic Scholar
  lists ICRA (not verified).
- version read: arXiv v1, full text (extracted).
- type: primary research.
- E1: ChatGPT writes a recipe from a meal specification; a GPT-3 model
  fine-tuned on 180 FOON recipe/task-tree pairs converts it into functional
  units; five trees are generated and merged into a **mini-FOON**, then into
  a **super-FOON** with FOON (III). Units are rejected if malformed or if
  their **state transition is not in a list of transitions observed in
  FOON** (sliced -> whole would be rejected) (III-C). Names normalised
  (plural to singular) (III-D). Weighted retrieval by motion cost (III-E).
- E2: 60 Recipe1M+ recipes (salad, drink, muffin), judged by hand via
  progress lines; vs Y206: +4% salad, +6% drink, +45% muffin (IV-B). The
  fine-tuned model alone reached 67% (V-A). Cost lowered vs the first tree
  in 40% of recipes (IV-C). Limitations: new names for states or motions
  (e.g. garnish), token limits, missing orientation and quantity knowledge.

### Y210 - https://arxiv.org/pdf/2401.07868v1.pdf
- citation: M. S. Sakib, Y. Sun, 2024, "Consolidating Trees of Robotic
  Plans Generated Using Large Language Models to Improve Reliability",
  arXiv v1; header names International Journal of Artificial Intelligence
  and Robotics Research (World Scientific); volume/DOI not verified.
- version read: arXiv v1, read in part (method and results sections
  searched in the extracted text).
- type: primary research.
- E1: GPT-4 prompted with allowed actions and available objects produces
  JSON task trees; each object node has label, states, ingredients
  (contents) and container (Fig. 3). Several trees are merged; units whose
  transition is absent from FOON are discarded (e.g. chopped -> whole); a
  unit judged wrong in one tree is replaced by the version that is right in
  the others. Converted to PDDL for execution.
- E2: 400 recipes (5% FOON, 95% Recipe1M+); a cheaper plan than the first
  tree in 25% of cases with 5 trees. (Accuracy figures not extracted.)

### Y211 - https://arxiv.org/html/2409.12262v3
- citation: D. Paulius, A. Agostini, B. Quartey, G. Konidaris, "Bootstrapping
  Object-level Planning with Large Language Models", arXiv v3 (Mar 2025);
  Semantic Scholar lists ICRA 2024 (not verified).
- version read: arXiv HTML, read via fetch summary.
- type: primary research.
- E1/E2: an LLM writes an object-level plan (OLP) as a FOON (units in JSON)
  from a similar example plan; units become PDDL subgoals for task and motion
  planning (III). Tested only on block pick-and-place tasks (tower,
  spelling, organising): success 76%, 62%, 77.14%, better than LLM-Planner,
  LLM+P, DELTA (V, Table I). Assumes an exact object-to-scene mapping; no
  recovery. Defines object-level planning as planning object state changes
  without committing to how they are achieved (I).

### Y212 - https://arxiv.org/html/2503.21564v1
- citation: R. Takebayashi, V. H. Isume, T. Kiyokawa, W. Wan, K. Harada,
  2025, "Cooking Task Planning using LLM and Verified by Graph Network",
  arXiv v1 (Osaka); Semantic Scholar lists IEEE CASE (not verified).
- version read: arXiv HTML, read via fetch summary.
- type: primary research.
- E1: an LLM reads cooking-video frames and subtitles, outputs target
  object nodes and actions; each action is loaded as a functional unit with
  variables and checked against the current environment state (hand empty,
  object location); a mismatch is returned to the LLM to replan (III-E).
- E2: 10 short videos; full plan graphs for 4/5 recipes vs 1/5 for a
  few-shot LLM baseline (Table III); one real dual-arm run (beef bowl).
  Stated limits: an added node cannot be revised later; no recovery from
  real failures. No substitution mechanism.

### Y213 - https://github.com/davidpaulius/foon_api and https://raw.githubusercontent.com/davidpaulius/foon_api/master/FOON-111/0039-crispy_hash_browns.txt
- citation: D. Paulius, M. S. Sakib, foon_api repository (GPL-3.0),
  accessed 2026-11-25; folder FOON-111.
- version read: README and one subgraph file, via fetch summary.
- type: dataset / implementation.
- What it shows: subgraph text format with O (object, with an
  active/passive flag), S (state; `contains {...}` for contents,
  `in [bowl]` for location) and M (motion with start/end time or "Assumed")
  lines, units separated by `//`. Tools: graph analyser (merge, retrieval,
  centrality), parser, JSON converter, FOON_view; generalisation uses
  WordNet and ConceptNet/gensim embeddings. The **hash browns** file (closest
  FOON record to K9 latkes): peel, grate into bowl, add onion, parsley,
  flour, corn starch, salt, pepper, mix into one "potato mixture" node with
  a contents list, add egg, place in a pre-heated greased skillet, flip,
  cook, plate. **No squeezing or draining step, and the peel is not
  represented**; the skillet carries its own states (greased, heated).

### Y214 - https://arxiv.org/abs/1805.06956
- citation: A. B. Jelodar, M. S. Salekin, Y. Sun, 2018, "Identifying Object
  States in Cooking-Related Images", arXiv (v3 Oct 2018).
- version read: **abstract only**.
- type: primary research / dataset. 17 frequent cooking objects, 11 states,
  9309 labelled images, ResNet classifier per object. Basis of FOON's state
  vocabulary for perception (cited in Y204, Y206).

### Y215 - https://ar5iv.labs.arxiv.org/html/1807.02192
- citation: D. Paulius, Y. Sun, 2019, "A Survey of Knowledge Representation
  in Service Robotics", Robotics and Autonomous Systems 118:13-30 (as cited
  in Y204, Y205).
- version read: ar5iv HTML, first 100k of 131k characters, via fetch
  summary.
- type: survey.
- What it says: many representations omit object states although states are
  needed to tell when an action is complete (Sec. 2.1, 5.3); FOON, action
  tree banks, KnowRob/openEASE, RoboEarth, RoboBrain, Ramirez-Amaro's
  semantic trees reviewed; ingredient substitution not discussed; no common
  ontology standard (5.7).

### Y216 - https://ai.uni-bremen.de/papers/beetz18knowrob.pdf
- citation: M. Beetz, D. Bessler, A. Haidu, M. Pomarlan, A. K. Bozcuoglu,
  G. Bartels, 2018, "KnowRob 2.0 - A 2nd Generation Knowledge Processing
  Framework for Cognition-enabled Robotic Agents", IEEE ICRA 2018,
  pp. 512-519, DOI 10.1109/ICRA.2018.8460964 (venue/DOI from DBLP and
  Crossref search listings, not opened).
- version read: university repository PDF, read in part (introduction to
  inner-world simulation, about the first half).
- type: primary research (system paper).
- E1: a Prolog first-order time-interval logic knowledge base built largely
  on demand from the robot's control data; ontology at the core; inner-world
  physics simulation; **narrative-enabled episodic memories (NEEMs)** that
  link recorded episodes to symbolic stories of what was done, why, with
  what result. The knowledge bases may be redundant or inconsistent, so
  several hypotheses are computed and checked for plausibility.
- E2: evaluated by example queries (grasping a cup to pour); motion-level,
  not recipe-level. No recipe or substitution representation in the part
  read.

### Y217 - https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2025.1682031/full
- citation: M. Kuempel, M. Scheibl, J.-P. Toeberg, V. Hassouna, P. Cimiano,
  B. Wrede, M. Beetz, 2025, "Everything robots need to know about cooking
  actions: creating actionable knowledge graphs to support robotic meal
  preparation", Frontiers in Robotics and AI 12, DOI
  10.3389/frobt.2025.1682031.
- version read: publisher full text HTML (open access), via fetch summary
  (first 100k of 102.5k characters).
- type: primary research.
- E1: six action cores (cutting, pouring, mixing, preparing, pick and
  place, cook and cool) split into action groups with motion parameters,
  input/output objects, tools, constraints; RDF triples such as Dicing
  requiresPriorTask Julienning (Table 3). Recipe verbs matched by spaCy and
  cosine similarity (threshold 0.56).
- E2: Recipe1M+ verbs covered 54% by direct match, about 76.5% with
  similarity; simulated PR2 cutting. Stated: no recipe states, no process
  timing (waiting for a cake), alternatives abstracted away (3.4, 5.3).

### Y218 - https://arxiv.org/html/2410.02874v2
- citation: N. Kanazawa, K. Kawaharazuka, Y. Obinata, K. Okada, M. Inaba,
  2024, "Real-World Cooking Robot System from Recipes Based on Food State
  Recognition Using Foundation Models and PDDL", arXiv v2; journal (Advanced
  Robotics per a search listing) not verified.
- version read: arXiv HTML, read via fetch summary.
- type: primary research.
- E1: GPT-4 converts a recipe into 10 cooking functions; each becomes a
  PDDL goal; a planner adds omitted actions (fetch water, turn on stove,
  hold bowl) (3.1-3.2). **Food state change** detected by CLIP image
  features with a linear probe trained on a few labelled time series
  (butter melting, water boiling, egg cooking) (4).
- E2: detection timing errors of +3.8 s, -1.1 s, -6.7 s on validation
  (Table 2); PR2 cooked sunny-side-up egg and boiled-sauteed broccoli; the
  butter was judged melted too early in one run; edible by tasting; no
  success rate. No substitution or alternative routes.

### Y219 - https://www.anlp.jp/proceedings/annual_meeting/2024/pdf_dir/E1-3.pdf
- citation: Kanazawa et al. (JSK, University of Tokyo), NLP2024 (30th annual
  meeting of the Association for Natural Language Processing, Japan), March
  2024, pp. 127-; Japanese title concerns a real-world cooking robot from
  recipe text with foundation models and classical planning. Full title
  transliteration not verified.
- version read: PDF obtained; body text did not decode (CID fonts). Treated
  as **abstract only**; the English Y218 was read instead.

## Failed pages and abstract-only

| URL or query | why | fallback tried |
| --- | --- | --- |
| https://digitalcommons.usf.edu/esb_facpub/81/ | record only, links to IEEE DOI, no PDF | arXiv 1902.01537 v4 read (Y201) |
| arXiv PDFs via fetch (Y201-Y210, Y216) | fetch returned binary | saved file converted with pdftotext, text read |
| https://mdpi.com/2218-6581/11/6/123 (Takata et al., Graph-Based Framework on Bimanual Manipulation Planning from Cooking Recipe, Robotics 2022) | HTTP 403 | none; not used as evidence |
| Takata et al., IROS 2022, dual-arm planning from language and cooking images | no open copy found | none; cited only as cited in Y212 |
| https://www.anlp.jp/.../E1-3.pdf | Japanese CID fonts did not decode | English version Y218 |
| "A Unified Framework Integrating Object-oriented Task Learning and Knowledge-based Task Planning for Long-horizon Cooking Tasks" (IJCAS 2025, listed by Semantic Scholar) | not found online | none |
| "Task Planning for Long-Horizon Cooking Tasks Based on LLMs" (IROS 2024, listed by Semantic Scholar) | not searched further (time) | none |
| https://arxiv.org/abs/2112.02433 | abstract only (superseded by Y206) | Y206 read in full |
| https://arxiv.org/abs/1805.06956 | abstract only | none |
| ar5iv 1807.02192 | only first 100k of 131k chars read | none |
| Y203, Y210, Y216 | read in part | key sections searched in extracted text |

## Searches

| language | query | useful? |
| --- | --- | --- |
| en | "Functional Object-Oriented Network for Manipulation Learning" pdf arXiv | yes (Y201) |
| en | "Functional Object-Oriented Network: Construction & Expansion" arXiv | yes (Y202) |
| en | Sakib Sun FOON large language model task tree long-horizon cooking arXiv | yes (Y209, Y210, Y212) |
| en | "Task Planning with a Weighted Functional Object-Oriented Network" arXiv | yes (Y203, Y208) |
| en | Jelodar Sun "object state" cooking images dataset recognition arXiv | yes (Y214) |
| en | FOON dataset github foon_api subgraph file format | yes (Y213) |
| en | "A Unified Framework Integrating Object-oriented Task Learning ..." | no |
| en | KnowRob 2.0 second generation knowledge processing framework pdf | yes (Y216) |
| en | Takata Harada "Efficient Task/Motion Planning for a Dual-arm Robot ..." | partly (403) |
| ja | 調理ロボット レシピ 作業計画 グラフ 食材 状態 論文 | yes (Y219 -> Y218); recipe flow graph hits left to the Y500 area |
| de | Roboter Kochen Rezept Wissensrepräsentation Handlungsplan Dissertation Universität Bremen Pfannkuchen | yes (Y217); Mueller 2008 TUM dissertation found, not read |
| en | Kanazawa Kawaharazuka Okada Inaba cooking robot recipe food state recognition PDDL | yes (Y218) |

## Citation trail

- Backward from Y206: Y201, Y202, Y203 (as ref [14]), Y205, Y214's sequel
  (Jelodar & Sun ICIP 2019, state taxonomy, not read), KnowRob (Tenorth &
  Beetz 2009, not read; Y216 read instead), "Robotic roommates making
  pancakes" (Beetz et al. 2011, not read), Mueller & Bergmann ICCBR 2017
  and Gaillard et al. ICCBR 2015 (left to the Y300 area), Shirai et al. 2020
  food KG substitution (left to Y400).
- Backward from Y201/Y202: Petri nets (Y202 compares FOON to them; left to
  Y600), manipulation action tree bank (Yang et al. 2014, not read), semantic
  event chains (Aksoy et al., not read).
- Forward (Semantic Scholar citations of Y201, first 100 of more): Y202,
  Y203, Y204, Y205, Y206, Y207, Y208, Y209, Y211, Y212, Y214; a run of 2022
  arXiv class reports on FOON search algorithms (2211.xxxxx, not read); a
  2024 "Prompting Task Trees using Gemini" report (not read); industrial
  assembly uses of FOON (CASE 2022, arXiv 2204.02274, not read); food state
  recognition papers (not read).
- Forward from KnowRob line: Y217 (Bremen/Bielefeld 2025).
- Japanese line: Y219 -> Y218.

## Approach analyses

### A. FOON core: functional units, universal FOON, task tree retrieval (Y201, Y202, Y204, Y205, Y213)

- **E1** Unit: the functional unit (input object-state nodes -> one motion
  -> output object-state nodes). Object nodes = type + state labels +
  (optionally) contents + container location; utensils have states too. A
  recipe = a subgraph from one video; knowledge base = union of subgraphs.
  Purpose: symbolic robot task planning.
- **E2** Demonstrated: hand-annotated graphs (60 -> 65 -> 111 -> 140
  videos), merging, backward retrieval against a kitchen inventory, a
  simulated execution, a 9-person rating study of tree-to-text recipes
  (Y205). Claimed, not tested: that cross-video recombination yields useful
  new ways to cook (Y201 VI-A).
- **E3 mapping (on paper, R6 inference unless marked)**
  - K1 gratin: units peel(potato) -> sliced(potato); peel(rutabaga) ->
    sliced; boil(slices, water, pot) -> blanched slices; place layers in
    dish -> dish contains {potato, rutabaga}; pour(cream) -> dish contains
    {..., cream}; bake(dish, oven) -> baked gratin. The raw-slice route is a
    second unit `bake(covered)` from raw slices to the same goal node. Both
    sit in one universal FOON; the search takes the first unit whose inputs
    are all available (Y202 III-D) and may splice the blanch of one source
    with the bake of the other: **this is K1-x, produced as a normal
    result**. "Blanch exists because of the bake" has no slot. Conflicting
    doneness (some give / no resistance) collapses to one state label.
  - K2 falafel: nodes soaked chickpea -> ground (with onion, herbs) ->
    mixture -> shaped -> fried. Pea substitution is Y206 Case 2 (same state,
    new object name): every unit is kept, only the name changes. Soak time,
    coarse grind, the dryness risk (P15) and the raw-soaked safety question
    (Q505) have no place. K2-x (boil-soak) yields a node "soaked pea"
    identical to the cold-soaked one, so the never-cook rule (Q114) is lost.
  - K3 cabbage rolls: blanch(leaves); cook(rice) part-way; mix(rice, meat)
    -> filling; wrap -> rolls (whether a wrap motion is among the 57 types
    was not verified); bake -> rolls cooked. Rice finishing inside the roll
    is invisible: the state goes to the composite "rolls".
  - K4 onion vessels: an onion layer would have to be a container-like object
    holding the filling (`in [onion layer]`); FOON's containers are utensils;
    an ingredient as container is not shown in any paper read.
  - K5 broccoli-stem patties: a cut unit may output both florets and stem;
    the annotation practice in Y213 drops peels, so discarded fractions
    usually do not exist in the data.
  - K7 arancini: "cooked rice (chilled)" is just a node; if present in the
    kitchen list K the search stops there (start from a state you have).
    Boiled vs risotto rice are two units into either one node (same label:
    merged) or two (different labels: kept).
  - K9 latkes: representable as units squeeze(grated potato) -> squeezed
    potato + liquid (in bowl); let stand -> starch settled; pour off ->
    starch; mix(squeezed potato, starch, egg, flour) -> mixture. Multiple
    outputs are allowed (Y201 Fig. 1). The real FOON hash-brown record
    (Y213) has no squeeze and no liquid at all.

- **E4 table**

| aspect | K1 | K2 | K3/K4 | K7 | K9 |
| --- | --- | --- | --- | --- | --- |
| a components and joins | preserved: branches into a mix/place unit; container + contents | preserved | extend: wrap/stuff as a motion, ingredient-as-container not shown | extend: nested joins become nested contents lists | preserved |
| b intermediate states, readiness vs doneness | extend: states exist as labels; no readiness/doneness distinction | extend | extend | extend: chilled rice is a node, keeping time absent | extend: no wait/settle time |
| c member after assembly | cannot: state applies to the composite (same gap as R3) | n/a | cannot (rice finishes in roll) | cannot | n/a |
| d why a stage exists | cannot | cannot | cannot | cannot | cannot |
| e alternative routes kept apart with evidence | cannot: union merge, search recombines across sources; subgraph files keep the source video but the merged unit carries no source list in the papers read | cannot | n/a | cannot | n/a |
| f substitution consequences | see approach B | see B | see B | n/a | n/a |
| g start from state already had | preserved: kitchen list K stops the search | preserved | preserved | preserved | preserved |
| h provenance | extend: per-video subgraph with timestamps; lost or implicit after merge | extend | extend | extend | extend |
| i unknown vs false | cannot: no unit = cannot make; closed world | cannot | cannot | cannot | cannot |
| j what a person reads | extend: progress line per ingredient (Y206) and generated recipe text (Y205) | extend | extend | extend | extend |

- **E5** The functional unit is R1's operation applied to a material with
  several output fractions (R1); the kitchen list K is R5 `from_state`;
  contents lists are R3 assemblies with a carrier. FOON lacks R1's
  three-valued applicability and reasons, R3/R4 citations per claim, R5
  endpoint kinds, times, dependency links and conflict versions. FOON has
  what Food-prep chose not to have: a search that recombines steps across
  sources. FOON also tracks **utensil states** (skillet greased, heated;
  knife dirty) as unit inputs/outputs.
- **E6** Published: unit structure (Y201 II), merge (Y201 III-B, Y202 III-A),
  levels (Y202 III-B), retrieval (Y201 VI, Y202 III-D), utensil states
  (Y201 II-A, Y213), progress line (Y206 IV-A), text generation (Y205).
  Inferred in R6: all K mappings, the K1-x/K2-x recombination consequence,
  the "same gap as R3" reading of composite states.
- **Verdict: already equivalent** for the unit (R1) and starting state (R5
  `from_state`); **not suited** for the merge-and-recombine retrieval as a
  source of routes, because it produces exactly the unverified combinations
  (K1-x, K2-x) that Food-prep keeps apart, and no paper evaluates whether
  recombined trees cook. **Extend (small)**: utensil/equipment state as part
  of readiness (pan heated, oven preheated) - check whether R5 holds this as
  state or only as a step (not checked by this agent).

### B. Similarity-based generalisation and substitution (Y202, Y206, Y207)

- **E1** Two mechanisms: (1) expand or compress the network by WordNet
  similarity or hand-made categories (Y202); (2) modify a retrieved tree by
  word-vector similarity per ingredient with four object/state cases, a
  state taxonomy and most-frequent-verb rules (Y206).
- **E2** Y202 measures only whether a tree is found (coverage), not whether
  it is right. Y206 measures correctness by hand: 76% of 500 recipes fully
  correct; 39% of errors are wrong substitutes, 27% wrong states.
- **E3**
  - K2: chickpea -> pea is a rename (Case 2); a coarse-grind and soak
    consequence cannot surface. FOON-GEN would map both to one legume
    category: identical trees.
  - K6 kale rolls: Y206 Fig. 7 lists cabbage among kale's top-5 FOON
    substitutes (published), so a FOON system would build kale rolls from a
    cabbage-roll tree with no objection (R6 inference). Food-prep records
    `not_worth_it` with cited reasons (no documented practice, small leaves).
    A false positive of similarity.
  - K1/K8: turnip's top-5 include radish, cabbage, carrot (published);
    rutabaga is not listed. A rename keeps or drops the blanch depending on
    which tree is the reference; time (the ~90 min covered bake) is not in
    FOON, so K8's false positive and false negative are both reproduced
    (inferred).
  - K3 wrapper swap (napa for white cabbage) would be a Case 2 rename;
    Food-prep's transfer validates it against documented practice.
- **E4** f substitution and consequences: **cannot** detect consequences
  elsewhere; errors are found only by a human reading progress lines. i:
  similarity threshold turns "not similar enough" into "not usable". h: the
  substitute's confidence is shown (raisin -> prunes 62.9%, Y206 Fig. 4b) but
  there is no source for why the substitution is valid.
- **E5** Meets R4 transfers, which do the opposite: start from a documented
  route, swap one material, re-validate with citations, give a verdict.
  FOON shows the published cost of not re-validating: about a quarter of
  trees wrong even after rules, most from the substitute itself (Y206 V).
- **E6** Published: thresholds, cases, error shares, examples (Y202, Y206).
  Inferred: K2/K6/K1/K8 outcomes.
- **Verdict: not suited** as a substitution method for Food-prep (no
  provenance, no consequence checking, similarity of words, not of
  function). The four-case table (object/state match) is **already
  equivalent** to R4's distinction between swapping a material and adding
  steps to reach the required state. The published error breakdown is
  useful evidence for R6's answer to Q3.

### C. Weighted FOON and path trees (Y203)

- **E1/E2** Robot-specific success rates per unit; all paths enumerated to
  pick the best product of rates; human takes hard steps. Weights estimated
  by the authors.
- **E3/E4** K1: the blanch route and the raw-bake route would get robot
  scores, not culinary evidence. e: alternatives are enumerated (path tree)
  but compared by a score.
- **E5** Food-prep forbids scoring/ranking. **Verdict: not suited.** The
  path tree (enumerate every route to a goal) is **already equivalent** to
  listing R3 routes and R5 alternative sequences, minus the score.

### D. FOON to PDDL, object-level vs task-level planning (Y208, Y211)

- **E1** A functional unit becomes a planning operator (preconditions =
  input states, effects = output states); each step is solved separately
  against perceived geometry. Object-level planning = what state changes,
  not how.
- **E2** Simulation only; high execution success on two recipes; faster
  than one big classical problem or an HTN that needed 8 pour variants.
- **E3/E4** Mostly robot concerns. For Food-prep the useful published
  observation is the split: a documented route is an object-level plan; the
  kitchen-specific work (which pot, fetch water) is task-level (Y208 I,
  Y211 I). i: PDDL predicates are true/false (closed world); R1's
  "unknown is never false" has no counterpart.
- **E5** Meets R1 (op = operator with applicability) and R5 (sequence).
  **Verdict: already equivalent** for the operator view; **not suited** for
  the planning machinery (no robot, no generator in scope).

### E. LLM plus FOON as verifier (Y209, Y210, Y211, Y212)

- **E1** LLM proposes units; FOON checks them: transitions never observed in
  FOON are rejected (Y209, Y210); several samples are merged and the unit
  confirmed by most samples wins (Y209 III-E, Y210); preconditions checked
  against the current kitchen state with feedback to the LLM (Y212).
- **E2** Gains over Y206 on 60 recipes (+45% for muffins, where FOON had
  one example) judged by hand; 4/5 vs 1/5 plan graphs (Y212).
- **E3/E4** K2-x and K1-x: each half is a known transition, so the
  transition check passes them (inferred). i: an unobserved transition is
  treated as wrong - unknown is made false, the opposite of Food-prep's rule.
- **E5** If an LLM ever proposed routes for Food-prep (outside R6/R7 scope),
  Food-prep's cited records could serve as the checker, but only with a
  three-valued outcome. **Verdict: not suited** now (no generator in scope);
  record as a concept: **documented records as a verifier, with
  unknown kept as unknown** (R6 inference).

### F. KnowRob 2.0 and actionable knowledge graphs (Y216, Y217)

- **E1** KnowRob 2.0: time-interval logic, ontology at the core, episodic
  memories (NEEMs) linking low-level recordings to narratives; inconsistent
  knowledge handled by generating hypotheses and checking plausibility.
  AKG: action cores with motion parameters and prior-task relations; recipe
  verbs mapped to them.
- **E2** KnowRob 2.0: example queries only. AKG: verb coverage on
  Recipe1M+ (about 76.5%), simulated cutting.
- **E3/E4** Neither represents dishes, routes or substitution in what was
  read; AKG explicitly leaves out states, timing and alternatives (Y217
  3.4, 5.3). K1-K9 cannot be expressed beyond single actions.
- **E5** NEEM narratives resemble R5's per-source step records (what was
  done, observed result); "keep inconsistent knowledge, compare hypotheses"
  resembles R5 conflicts kept as versions; AKG's requiresPriorTask resembles
  R5 dependency links at the level of actions (R6 inference).
  **Verdict: not suited** (motion-level robot knowledge); the
  conflict-as-hypotheses idea is **already equivalent** to R5 versions.

### G. Observable state recognition for completion (Y214, Y218)

- **E1** Classifiers that recognise an object's state (Y214) or the moment
  a state changes during heating (Y218: butter melted, water boiling, egg
  cooked) from a few labelled series.
- **E2** Y218: seconds-level timing errors; one early "butter melted" on
  the robot; two dishes cooked and tasted. Y214 abstract only.
- **E3/E4** b: K1 "no resistance at the knife point" and K2 "golden
  crust" are R5 done-when checks; Y218 shows such checks can be machine
  observables, but readiness (ready for next op) and doneness (ready to eat)
  are not distinguished. Planner-filled preparatory steps (fetch water,
  turn on stove) are what R5 records as dependencies, without the reason.
- **E5** Meets R5 done-when / failed-if. **Verdict: already equivalent** at
  the concept level (completion by observation, not by time alone);
  **not suited** as implementation (vision, robot).

## Answers to Q1-Q6 from this area

- **Q1** Unit: the functional unit (object states in, one action, object
  states out), the same shape as R1 operations on materials (Y201, Y208).
  One graph serves dish -> how (backward retrieval from a goal node against
  a kitchen inventory, Y201 VI, Y202 III-D) and ingredients -> dish only
  with a dish type given, via similarity of ingredient lists to known goal
  nodes (Y206 III-A). No paper read runs a forward "what can I make from
  this" search; the inventory stops the backward search instead.
- **Q2** States are free labels plus contents and location; several
  outputs per unit are allowed (tool states, fractions) (Y201, Y213);
  parallel branches are implicit in the tree; waits, times, readiness vs
  doneness and reasons for a stage are absent (Y201-Y213; Y217 says so
  explicitly for its graph). A composite (mixture, filled dish) carries the
  state after assembly, so FOON has R3's known gap. Observable completion is
  handled by state recognition outside the graph (Y218).
- **Q3** Substitution = word or WordNet similarity (Y202, Y206). Published
  failure: 76% fully correct recipes, errors mainly wrong substitutes (39%)
  and wrong states (27%) (Y206); apricot squeezed like lemon. Inconsistencies
  are found by humans reading progress lines; proposed fix is a person
  choosing among top-5 (Y206). Y202's evaluation counts found trees, not
  correct ones. Kale -> cabbage is a published top-5 pair (Y206 Fig. 7),
  which a K6-style check would need to refuse.
- **Q4** Several units producing the same node are alternative routes
  (Y201 Fig. 7-8). The merge removes duplicates and the search freely
  recombines units from different sources, presented as a strength (Y201
  VI-A). Evidence per route is not kept in the merged network in the papers
  read; choice is first-executable, fewest steps, robot success rate (Y203)
  or motion cost (Y209). Nothing separates variants, different products and
  unverified combinations.
- **Q5** Starting from what is in the kitchen is native (inventory K,
  Y201, Y206 Case 3); irreversible states are acknowledged (melted cheese
  cannot become diced, Y206 V). Node identity is name + state (+ contents),
  so two "soaked" nodes with different histories are the same node (R6
  inference from Y201 II-A, Y202 III-A): equivalent states are treated as
  interchangeable.
- **Q6** Progress line per ingredient (Y206 Fig. 4b, Y209 Fig. 5) and
  generated recipe sentences rated by 9 people (Y205, Y206). These were made
  to let humans check trees, not to help someone choose what to cook.

## Open questions this area leaves

1. Does any FOON work keep a per-unit source list after merging, or detect
   that a retrieved tree mixes sources? Not found in the papers read; the
   code (foon_api) was not inspected.
2. Is there any evaluation of a recombined or substituted FOON tree by
   actually cooking it? None found; all correctness is human reading of
   text or progress lines.
3. The 2025 IJCAS "unified framework" for long-horizon cooking and the
   IROS 2024 LLM long-horizon cooking paper were not read.
4. Whether FOON's motion list includes wrap/roll/stuff (K3, K4, K7) was not
   verified.
5. Whether Food-prep's R5 already treats equipment state (pan hot, oven
   preheated) as a readiness state, as FOON does for utensils, was not
   checked by this agent.
6. KnowRob 2.0 was read only in part; whether NEEM narratives store
   failures with reasons in a way that matches R5 failed-if was not
   established.
