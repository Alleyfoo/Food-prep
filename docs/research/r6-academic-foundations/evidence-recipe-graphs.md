# Evidence: Recipe flow graphs, recipe annotation and procedural-text state tracking

- Date read: 2026-11-25 (one interruption from a usage limit; reading resumed the same day).
- Method: WebSearch to find sources, WebFetch to read them. ACL Anthology PDFs did
  not convert to text through WebFetch; the saved PDF files were then read
  page by page (marked "repository PDF, read in full"). HTML full texts
  (Frontiers, ar5iv/arXiv HTML) were read through WebFetch, which returns a
  model-written digest of the page rather than verbatim text; these are marked
  "HTML full text (via fetch digest)" and their details are less certain than
  the PDF reads. Forward citations were taken from the Semantic Scholar API.
- Search languages: English queries only. Japanese work (Kyoto/Tokyo group)
  was reached through its English-language papers and English metadata of
  Japanese journals; the Japanese-language journal version of Visual Recipe
  Flow was downloaded but not read (see the failed table). No German, French,
  Italian or Spanish work in this area was found or searched for.
- Blocked or unreadable: PDF-to-text in WebFetch for every ACL/LREC PDF
  (fallback: saved PDF read directly, succeeded); one Japanese PDF not read;
  one Kyoto paper (Yamakata et al. 2016, "major workflow") not found.
- Food-prep files consulted for the mapping: `processing_conditions.yaml`
  (transfer `rutabaga_gratin` and `gratin_dauphinois/raw_long_bake`,
  lines 1235-1330), plus the round summary given in the brief.

## Sources

### Y500 — https://aclanthology.org/2020.lrec-1.638.pdf (landing page https://aclanthology.org/2020.lrec-1.638/)
- citation: Yoko Yamakata, Shinsuke Mori, John Carroll, 2020, "English Recipe
  Flow Graph Corpus", Proceedings of LREC 2020, Marseille, pp. 5187-5194,
  ELRA. DOI: none listed on the Anthology page.
- version read: repository PDF (ACL Anthology), read in full (8 pages).
- type: dataset + primary research.
- E1: each recipe's procedure text is annotated (1) with ten "recipe named
  entity" (r-NE) tags on text spans: F food (explicitly "also intermediate
  products"), T tool, D duration, Q quantity, Ac action by chef, Ac2
  discontinuous part of an action, Af action by food, At action by tool,
  Sf food state, St tool state (Table 1); and (2) with a flow graph: a DAG
  with a single root, nodes are r-NEs, 13 labelled edges (Table 4): Agent,
  Targ, Dest (container), t-comp, F-comp (food used as a tool), F-eq, F-part-of,
  F-set, T-eq, T-part-of, A-eq, V-tm (head verb for timing), other-mod.
  Nodes without incoming edges are ingredients; the node without outgoing
  edges is the end product; a directed path from action A to B means A must
  precede B (§4.1). Purpose: a computable representation of procedures for
  search, reasoning, smart kitchens, robots (§1-2).
- E2 demonstrated: 300 English recipes from Allrecipes (100 most-popular per
  category + 200 random), 38,062 tokens, 15,435 r-NEs, 15,861 edges (Tables
  2, 6). Annotators: one native English speaker (100-r) and two Japanese
  homemakers who had annotated the Japanese corpus (200-r). Agreement: r-NE
  90.5 F1; flow graph 82.3 F1 (on 100-r, one annotator as gold). Annotation
  time: 37 min per recipe for the graph, falling to 26 min. Automatic: BERT-NER
  87.6 F1; edge detection 71.1 F1 from gold r-NEs, 43.3 end-to-end (Table 5).
  Equality/part edges (F-eq 19.9%, F-part-of 12.3%, T-eq 13.0% recall) are
  the hardest because they create confluences a spanning tree cannot hold
  (§4.2, Table 6).
- Worked example (Fig. 3, Fig. 4): "Bake ... 50 to 55 minutes, until a skewer
  inserted into centre of loaf comes out clean" becomes Bake[Ac] with
  other-mod from 50_to_55_minutes[D] and V-tm from comes_out[At], which has
  clean[St], skewer[T] via inserted[Ac], and centre[F] F-part-of loaf[F].
  "Preheat oven to 180 C" is an Ac on a T with St modifiers; the later
  "preheated" is joined to it by A-eq. So completion conditions and tool
  preparation are captured as text spans hanging off the action.
- Stated limit: the graph is an internal symbolic representation, not meant
  to be shown verbatim to a cook (§4.1).

### Y501 — https://aclanthology.org/L14-1594.pdf (landing page https://aclanthology.org/L14-1594/)
- citation: Shinsuke Mori, Hirokuni Maeta, Yoko Yamakata, Tetsuro Sasada,
  2014, "Flow Graph Corpus from Recipe Texts", Proceedings of LREC 2014,
  Reykjavik, pp. 2370-2377, ELRA. DOI: none listed.
- version read: repository PDF (ACL Anthology), read in full (8 pages).
- type: dataset (Japanese recipes) + annotation standard.
- E1: the original r-FG scheme on Japanese Cookpad recipes: eight r-NE tags
  (F, T, D, Q, Ac, Af, Sf, St; Table 1) and 13 arc labels (Table 2). A
  vertex is a character span with start and end position in the text (§3).
  Key definitions:
  - An arc from action to action means the result of the first action is
    the object of the second ("washed carrot", not carrot; §4.1).
  - When the same food is named again after an action changes it, the
    earlier action is linked to the new mention by F-eq: the corpus
    deliberately distinguishes the object before and after an action
    (§4.4), unlike ordinary coreference corpora.
  - F-part-of (potato -> skin), F-set (carrot, cabbage -> "vegetables").
  - V-tm: a clause giving the timing or condition of another action, e.g.
    water boils[Af] -V-tm-> add[Ac] (§4.10, §4.12).
  - A-eq: a verb repeated only to identify an object ("the carrot you
    sliced") must not be executed again (§4.9).
  - Why a DAG and not a tree (§4.12): food separation (egg into yolk and
    white used in different actions; half a sauce used early and the rest
    later), but most branching in the corpus comes from coreference.
- E2 demonstrated: 266 recipes: 200 random and 66 recipes of one dish
  (nikujaga, beef and potato). Per recipe ~6.5-6.9 sentences, 36-48 r-NEs,
  38.6 arcs (Tables 3-5); arcs exceed vertices by about 3.3 per recipe, the
  measure of how far graphs are from trees. Annotation: 5-10 min for tags,
  ~40 min for arcs in a spreadsheet, with an online checker that the result
  is a rooted DAG (§5, §6). No inter-annotator agreement figure; a
  language-dependency test on one English/Japanese recipe pair: 23/23
  vertices matched, 16/22 arcs, 20/22 after swapping d-obj/i-obj (F 0.9; §6.2).
- Claimed, not demonstrated here: that the corpus "enables" comparing
  recipes of the same title (§6.1) and smarter search (§7.3). The 66
  nikujaga recipes are reported only as statistics "very similar" to the
  random set; no cross-recipe comparison is made in this paper.

### Y502 — https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1550604/full
- citation: Filippos Ventirozos, Mauricio Jacobo-Romero, Haifa Alrdahi, Sarah
  Clinch, Riza Batista-Navarro, "RiCoRecA: rich cooking recipe annotation
  schema", Frontiers in Artificial Intelligence vol. 8 (2025), published
  12 January 2026. DOI 10.3389/frai.2025.1550604.
- version read: publisher HTML full text (via fetch digest), two passes
  (body; then reference list). Some body details may be lost in the digest.
- type: annotation schema + dataset + primary research.
- E1: one schema combining entity tags, relations and coreference, to turn
  recipes into workflows for IoT kitchen devices. Tags: Action, Ingr, Tool,
  Part of Ingr/Tool, Coreference of Ingr/Tool, Msr & Sett (measures and
  device settings), **Why** (reason for an action), **If**, **Until**,
  **Repeat** (control keywords), **State of Ingr/Tool** (the required state,
  linked to Until). Relations: Modifier, Member, **Or** (alternatives between
  predicates or entities), **Join** (parallel predicates), Dependency
  (ordering, which yields a timeline). Intermediate products are handled as
  coreference ("dough" refers back to its ingredients; "preheated oven" is a
  tool coreference). Implicit entities are recovered with a table of which
  entities take part in which predicate.
- E2 demonstrated: 156 English recipes (from FoodBase/Allrecipes), mean 9.3
  sentences; 8,056 tags and 8,006 relations by the first annotator. Agreement
  (F, against the first author, 50 recipes each): NER 0.886/0.908, relations
  0.809/0.871, membership 0.822/0.890, antecedents 0.714/0.807; Repeat, Part of
  Tool and Join were least reliable. Seq2seq models: PEGASUS-X NER 0.883,
  relations 0.830, antecedents 0.626; LongT5 much lower. Long-range Dependency
  links were the weak point.
- Not addressed (per the paper): alternative recipes for one dish,
  recombination, substitution (mentioned only as future application).

### Y503 — https://aclanthology.org/2021.emnlp-main.554.pdf (landing page https://aclanthology.org/2021.emnlp-main.554)
- citation: Lucia Donatelli, Theresa Schmidt, Debanjali Biswas, Arne Köhn,
  Fangzhou Zhai, Alexander Koller, 2021, "Aligning Actions Across Recipe
  Graphs", Proceedings of EMNLP 2021, pp. 6930-6942. DOI
  10.18653/v1/2021.emnlp-main.554. Code/data: github.com/coli-saar/ara (link
  as printed in the paper; not opened).
- version read: repository PDF, read in full (13 pages incl. appendix).
- type: dataset (ARA) + primary research.
- E1: unit is the **action** node; Y500-style full graphs (Fig. 2) are
  distilled into action graphs keeping only actions, with paths between
  actions becoming edges (§3.4). Alignment = for each action of a longer
  source recipe, the best corresponding action of a shorter target recipe of
  the same dish, or "None" (§4.1-4.2). Purpose: aggregate how a dish is made
  across recipes; stated future goal is aggregating several graphs of one dish
  into common and distinct parts (§6) — **not done in the paper**.
- E2 demonstrated: parser trained on Y500 (tagger 89.6 F1; parser 78.2 F1 on
  gold tags, 72.3 end-to-end; Tables 1-2). ARA: 10 dishes x 11 recipes = 110
  recipes, 1,592 source actions, >= 3 crowd votes each, 250 Prolific workers;
  190 actions with no plurality adjudicated by authors (Table 3, §4.2). Vote
  agreement with the final label 69.3%; author accuracy on 10 pairs 79%;
  majority baseline ("None") 31.3%. Model accuracy: base 66.3%, with parent
  and child actions 72.4% (Table 4). Dishes (App. B.1): baked ziti, blueberry
  banana bread, cauliflower mash, chocolate chip cookies, garam masala, pizza
  dough, orange chicken, pumpkin bread, chicken tortilla soup, waffles.
- Disagreement analysis (§4.3, 100 hard questions): many-to-one 26% (e.g. one
  "Add" combines milk, butter and vanilla into eggs, another adds yolks and
  vanilla to milk — sequential position matches but arguments differ);
  implicit actions 24%; let/light verbs 22%; no best alignment 17%;
  one-to-many 6%; negative and conditional events 2%.
- Design assumption: transitive closure — an alignment source->secondary
  target is approximated through an intermediate recipe (§4.1).

### Y504 — https://aclanthology.org/D15-1114.pdf (landing page https://aclanthology.org/D15-1114/)
- citation: Chloé Kiddon, Ganesa Thandavam Ponnuraj, Luke Zettlemoyer, Yejin
  Choi, 2015, "Mise en Place: Unsupervised Interpretation of Instructional
  Recipes", Proceedings of EMNLP 2015, Lisbon, pp. 982-992. DOI
  10.18653/v1/D15-1114.
- version read: repository PDF, read in full.
- type: primary research.
- E1: action graph: each action = verb + arguments; argument = (syntactic
  type DOBJ/PP, semantic type food/location/other, text spans), plus
  **implicit arguments** with empty spans for elided objects ("Bake for 50
  minutes"). A connection links the output of an earlier action (or 0 = new
  raw ingredient/location) to an argument span; food edges propagate
  ingredients, location edges propagate places (preheated oven -> bake) (§2).
  Composite names ("batter", "dressing") are modelled by the ingredients that
  flow into them (§3.2.2).
- E2 demonstrated: 2,456 unannotated Allrecipes recipes for 20 dish names;
  33 dev and 100 hand-labelled test recipes (~13 actions each). Connection F1
  80.0 with oracle segmentation (sequential baseline 72.0), 66.8 with
  automatic segmentation (§7-8, Table 1). 82% of correct outgoing
  connections are to the next action (§8 errors).
- Stated: the origin-reuse prior makes reusing one output less likely, with
  egg separation into yolk and white noted as a counterexample (fn. 2).
  Future work: durations, tools, amounts, nested locations (§10). The paper
  says it learns from redundancy across many recipes of the same dish (§1, §9)
  but does not align them.

### Y505 — https://aclanthology.org/D15-1090.pdf (landing page https://aclanthology.org/D15-1090/)
- citation: Jermsak Jermsurawong, Nizar Habash, 2015, "Predicting the
  Structure of Cooking Recipes", Proceedings of EMNLP 2015, Lisbon,
  pp. 781-786. DOI 10.18653/v1/D15-1090.
- version read: repository PDF, read in full.
- type: primary research + derived dataset.
- E1: SIMMR (Simplified Ingredient Merging Map in Recipes): a dependency tree
  whose leaves are ingredient-list items and whose internal nodes are whole
  instructions; an edge means the output of one feeds the next (§3.2). Built
  by converting MILK annotations of the CMU CURD corpus (Y515). Simplifying
  assumptions: one output per instruction (MILK `separate` ignored, 3% of
  recipes; 1.3% are discards such as draining fat); non-food instructions
  (preheat, line the tin) pass through the previous mixture; ingredients not
  on the list (cooking spray) are dropped (§3.3).
- E2 demonstrated: 260 recipes, 50/20/30 split. Ingredient-to-instruction
  linking 95.3% edge accuracy; instruction-to-instruction 91.3%; whole tree
  93.5% vs baseline 85.7% (Tables 1-2, §4.4). 89% of instruction links go to
  the next instruction; long-distance links are 12.3% of edges and 91.7% of
  errors (§4.3).
- Stated insight (§3.2): several actions can be reordered without changing the
  recipe as long as the order of combinations is kept.

### Y506 — https://ar5iv.labs.arxiv.org/html/2005.09606 (abstract page https://arxiv.org/abs/2005.09606 also read)
- citation: Angela Lin, Sudha Rao, Asli Celikyilmaz, Elnaz Nouri, Chris
  Brockett, Debadeepta Dey, Bill Dolan, 2020, "A Recipe for Creating
  Multimodal Aligned Datasets for Sequential Tasks", Proceedings of ACL 2020,
  pp. 4871-4884. DOI 10.18653/v1/2020.acl-main.440 (from search results and
  Y503's reference list; the DOI page itself was not opened).
- version read: HTML full text via ar5iv (via fetch digest); arXiv abstract
  page shows v1 (19 May 2020). Which arXiv version ar5iv rendered: not verified.
- type: dataset (Microsoft Research Multimodal Aligned Recipe Corpus) +
  primary research.
- E1: unit is the **instruction sentence** (text) or transcript sentence
  (video). Dishes grouped by exact title match (>= 3 recipes). Pairwise
  unsupervised HMM+IBM1 alignment, widened jump window because recipes reorder
  steps; an instruction can align to several. Joint alignment per dish: graph
  of instructions with pairwise edges above probability 0.5, reduced by a
  maximum spanning tree to a forest; a path with at most one node per recipe
  is a set of jointly aligned instructions.
- E2 demonstrated: ~150K pairwise alignments over 4,262 dishes (abstract).
  Text-text gold: 200 pairs, 5 dishes, 3 expert annotators per pair; two or
  more agreed on 65% of instructions, all three on 42%. Text-text F1 54.55
  (RoBERTa 50.44); text-video F1 70.30. Ingredient substitutions and
  one-step-to-many breakdowns are extracted at a 0.9 threshold. No stated
  handling of steps that cannot be aligned beyond the threshold.

### Y507 — https://arxiv.org/html/2507.17232v2
- citation: Mashiro Toyooka, Kiyoharu Aizawa, Yoko Yamakata, 2025, "A Highly
  Clean Recipe Dataset with Ingredient States Annotation for State Probing
  Task", arXiv:2507.17232v2 (28 Aug 2025). Venue: not verified (template
  text on the page).
- version read: arXiv HTML v2 (via fetch digest).
- type: dataset + evaluation.
- E1: Japanese recipes from NHK's "Minna no Kyou no Ryouri" (~25,000
  collected; 100 annotated). The ingredient list is the initial world state;
  after each step annotators record the transformation as (input, output)
  pairs, 1-to-1, 1-to-N or N-to-1; states are **free text**, no controlled
  vocabulary. A spreadsheet checker blocks ingredients from vanishing or
  appearing unintentionally.
- E2 demonstrated: two annotators on 100 recipes; with embedding matching at
  threshold 0.85, node F1 0.911, matched-edge F1 0.951, all-edge F1 0.860.
  Probing tasks (step reference, ingredient usage, ingredient tracing): GPT-4o
  avg 0.824; fine-tuned Qwen-2.5-VL-72B 0.919. Failures concentrate on
  **splitting, discarding and recombination** of ingredients; the paper says
  r-FG methods also struggle when ingredients are divided and recombined.

### Y508 — https://ar5iv.labs.arxiv.org/html/2209.05840 (Anthology entry https://aclanthology.org/2022.coling-1.315 seen in search only)
- citation: Keisuke Shirai, Atsushi Hashimoto, Taichi Nishimura, Hirotaka
  Kameko, Shuhei Kurita, Yoshitaka Ushiku, Shinsuke Mori, 2022, "Visual Recipe
  Flow: A Dataset for Learning Visual State Changes of Objects with Recipe
  Flows", Proceedings of COLING 2022, pp. 3570-3577 (pages from search
  result; not verified on the Anthology page). arXiv:2209.05840.
- version read: HTML full text via ar5iv (via fetch digest).
- type: dataset.
- E1: r-FG (Y501) per recipe plus, for each object an action needs, a
  **pre-action and post-action image** from fixed-camera cooking videos;
  states traced along Targ edges. Objects without a usable frame are marked
  missing.
- E2 demonstrated: 200 Japanese salad recipes (Kurashiru videos), 11,686 r-NEs,
  11,291 flows, 3,705 objects (2,551 with both images). Agreement (10 recipes,
  one re-annotator): r-NE 98.40 F, r-FG 86.11 F, images 72.80 F. Retrieval of
  the post-action image: best R@5 37.01 using verb + pre-image. The digest
  reports no explicit treatment of merged or post-mixing states.

### Y509 — https://www.jstage.jst.go.jp/article/tjsai/32/1/32_WII-F/_article/-char/en
- citation: Yoko Yamakata, Hirokuni Maeta, Takuya Kadowaki, Tetsuro Sasada,
  Shinji Imahori, Shinsuke Mori, 2017, "Cooking Recipe Search by Pairs of
  Ingredient and Action — Word Sequence v.s. Flow-graph Representation",
  Transactions of the Japanese Society for Artificial Intelligence 32(1),
  pp. WII-F_1-9. DOI 10.1527/tjsai.WII-F. Japanese title: not shown, not
  verified.
- version read: **abstract only** (J-STAGE English abstract).
- type: primary research.
- E1/E2 (abstract): recipe text parsed into a flow graph; the actions applied
  to an ingredient are read by following the path from its node to the root;
  search for "a tomato is fried" reached 68.8% precision vs 61.5% for a
  bag-of-words baseline. This is the published use of the ingredient-to-dish
  traversal.

### Y510 — https://aclanthology.org/2023.findings-acl.261/
- citation: Yi Fan, Anthony Hunter, 2023, "Understanding the Cooking Process
  with English Recipe Text", Findings of ACL 2023, pp. 4244-4264. DOI
  10.18653/v1/2023.findings-acl.261.
- version read: **abstract only** (Anthology page).
- type: primary research.
- E2 (abstract): two-module BERT/BiLSTM/CRF tagger + BERT relation classifier
  on Y500, edge labels predicted, overall F1 92.2 (vs 43.3 end-to-end in Y500).
  Shows the Y500 annotation is learnable to a high level; adds nothing to the
  representation.

### Y511 — https://arxiv.org/abs/2406.15823
- citation: Yash Kumar Lal, Vanya Cohen, Nathanael Chambers, Niranjan
  Balasubramanian, Raymond Mooney, "CaT-Bench: Benchmarking Language Model
  Understanding of Causal and Temporal Dependencies in Plans", EMNLP 2024
  (accepted per arXiv page), arXiv:2406.15823v3.
- version read: **abstract only**.
- E2 (abstract): questions whether one recipe step must occur before or after
  another; best zero-shot F1 0.59, 0.73 with explanations and few-shot; models
  lean to predicting dependence, apparently from text order. Source corpus of
  the dependencies not stated on the abstract page.

### Y512 — https://arxiv.org/abs/2210.11431
- citation: Xiao Liu, Yansong Feng, Jizhi Tang, Chengang Hu, Dongyan Zhao,
  2022, "Counterfactual Recipe Generation: Exploring Compositional
  Generalization in a Realistic Scenario", EMNLP 2022 (per arXiv page),
  arXiv:2210.11431v1.
- version read: **abstract only**.
- E2 (abstract): Chinese recipe corpus; given a base recipe and one changed
  ingredient, generate the modified recipe; action-level annotations for
  evaluation. Models produce fluent text but often miss actions that needed
  changing and keep text tied to the old ingredient.

### Y513 — https://arxiv.org/abs/1711.05313
- citation: Antoine Bosselut, Omer Levy, Ari Holtzman, Corin Ennis, Dieter Fox,
  Yejin Choi, "Simulating Action Dynamics with Neural Process Networks",
  arXiv:1711.05313v2 (15 May 2018). Venue: not shown on the page; not verified.
- version read: **abstract only**.
- E1 (abstract): actions as learned "state transformers" updating entity
  states, including unstated effects. Tracked attributes and recipe data not
  given on the abstract page.

### Y514 — https://arxiv.org/abs/2205.12420
- citation: Te-Lin Wu, Caiqi Zhang, Qingyuan Hu, Alex Spangher, Nanyun Peng,
  "Learning Action Conditions from Instructional Manuals for Instruction
  Understanding", arXiv:2205.12420v2 (3 Jul 2024). Venue: not verified.
- version read: **abstract only**.
- E1 (abstract): predicts pre- and postconditions of actions in instructional
  manuals; human-annotated set plus weak supervision. Whether recipes are
  included: not verified.

### Y515 — https://www.cs.cmu.edu/~ark/CURD
- citation: CURD 1.0 (Carnegie Mellon University Recipe Database), 260 English
  recipes annotated in MILK, released 2 June 2008; cite as Dan Tasse, Noah A.
  Smith, "SOUR CREAM: Toward Semantic Processing of Recipes", Technical Report
  CMU-LTI-08-005, Carnegie Mellon University, May 2008.
- version read: dataset landing page only. **The technical report was not
  read**; MILK's command set is known here only through Y505's description
  (MILK has create_tool, combine, put, separate among its commands; combine
  names its output, e.g. "cheeses"; Y505 §3.3).
- type: dataset.

### Y516 — https://arxiv.org/abs/2608.24369
- citation: Lei Jiang, "Do Recipes Have Personas? Characterizing and
  Generating Creator Style in Attributed Procedural Graphs", arXiv:2608.24369v1
  (25 Aug 2026), stated accepted at Discovery Science 2026.
- version read: **abstract only**.
- E1/E2 (abstract): execution flow graphs from video transcripts, each tied to
  a creator; topological metrics separate creators' workflow habits. Relevant
  only as a sign that the same dish's workflows differ systematically by
  author, not only by wording.

## Failed pages and abstract-only
| URL or query | why | fallback tried |
| --- | --- | --- |
| https://aclanthology.org/2020.lrec-1.638.pdf (WebFetch) | PDF streams not converted to text | saved PDF read directly: succeeded (Y500) |
| https://aclanthology.org/L14-1594.pdf (WebFetch) | same | saved PDF read: succeeded (Y501) |
| https://aclanthology.org/2021.emnlp-main.554.pdf (WebFetch) | same | saved PDF read: succeeded (Y503) |
| https://aclanthology.org/D15-1114.pdf, https://aclanthology.org/D15-1090.pdf (WebFetch) | same | saved PDFs read: succeeded (Y504, Y505) |
| https://www.lsta.media.kyoto-u.ac.jp/mori/research/public/shirai-JNLP2023-30-3.pdf | Japanese journal version of Y508 (JNLP 2023, vol. 30 no. 3 per file name; not verified); 3.2 MB PDF not converted | saved locally but **not read** (time and context budget); gap |
| query "Yamakata Imahori Maeta Mori 2016 major workflow" | paper cited in Y503 (ICMEW 2016, extracting a major workflow) not found | none; gap. Most relevant missing item for Q4 |
| https://aclanthology.org/D15-1114/ and D15-1090/ landing pages | no abstract text on page | PDFs read instead |
| Lin et al. 2020 (Y506) DOI page | not opened | ar5iv HTML read |
| End-to-end Parsing of Procedural Text into Flow Graphs (Bhatt, Abdollahpouri Hosseini, Fancellu, Fazly, LREC-COLING 2024, pp. 5833-5842) | seen only in search results; not read; not used as evidence | none |
| A Benchmark for Recipe Understanding in Artificial Agents (LREC-COLING 2024) | title only in citation list; not read | none |
| Tasse & Smith 2008 SOUR CREAM tech report | not found as a readable file | CURD page read (Y515) |
| Bosselut et al. 2018 (Y513), Wu et al. (Y514), CaT-Bench (Y511), Counterfactual recipes (Y512), Fan & Hunter (Y510), Yamakata et al. 2017 (Y509), Jiang 2026 (Y516) | abstract only | none (budget) |
| Not read at all, cited by read papers: Hamada et al. 2000 (recipe trees, Japanese); Maeta et al. 2015 (procedural text framework, IWPT); Yamakata et al. 2013 (summarisation of recipes with flow graphs); Yamakata et al. 2016 (major workflow); Dalvi et al. 2019 (purpose of actions); Fang et al. 2022 (RecipeRef); Schumacher 2015 thesis; Chang et al. 2018 RecipeScape; Mori et al. 2014 Flowgraph2text; Shirai & Kim 2022 EaT-PIM | not reached | listed for follow-up; EaT-PIM belongs to the substitution area, RecipeScape to visualisation |
| Usage-limit interruption during the session | tool calls refused for a period | resumed; no page lost |

## Searches
| language | query | useful? |
| --- | --- | --- |
| en | Mori Maeta Yamakata Sasada "Flow Graph Corpus from Recipe Texts" LREC 2014 | yes (Y501) |
| en | Donatelli "Aligning Actions Across Recipe Graphs" EMNLP 2021 | yes (Y503) |
| en | Yamakata Imahori Maeta Mori 2016 "major workflow" ingredients tools actions | partly: found Y507, Y509; not the 2016 paper |
| en | Lin Rao Celikyilmaz 2020 "A Recipe for Creating Multimodal Aligned Datasets for Sequential Tasks" | yes (Y506) |
| en | "End-to-end Parsing of Procedural Text into Flow Graphs" LREC-COLING 2024 | metadata only |
| en | Tasse Smith "SOUR CREAM" MILK CMU-LTI-08-005 | yes (Y515 page) |
| en | "Visual Recipe Flow" dataset ... COLING 2022 | yes (Y508) |
| en (API) | Semantic Scholar citations of DOI 10.18653/v1/2021.emnlp-main.554 | yes: 29 citing papers, used for the forward trail |

## Citation trail
- Backward from Y500: Y501 (Japanese r-FG, read); Kiddon 2015 = Y504 (read);
  Jermsurawong & Habash = Y505 (read; Y500 lists it as 2014 with wrong pages,
  the Anthology record and the PDF say EMNLP 2015 pp. 781-786); Momouchi 1980
  PT-Chart and Hamada 2000 recipe trees (not read); Yamakata 2013 (not read).
- Backward from Y505: MILK/CURD (Y515, page only).
- Backward from Y503: Y500, Y504, Y505, Y506 (all read); Yamakata 2016 (not
  found); Chang 2018 RecipeScape (visualisation area, not read).
- Backward from Y502: Y500, Y501, Y503, Y504, Y505; Wu 2022 = Y514 (abstract);
  Dalvi 2019, Fang 2022, Schumacher 2015, EaT-PIM (not read).
- Forward from Y503 (Semantic Scholar, 29 papers): Y502, Y510 (abstract),
  Y511 (abstract), Y512 (abstract), Y516 (abstract); Bhatt 2024 (metadata);
  Graph2Vid, task-graph learning from egocentric video, CLMSM, Cultural
  Adaptation of Recipes, AMR splitting for recipes (titles only, not read).
- Forward/sideways from the Kyoto/Tokyo group: Y508 (Visual Recipe Flow),
  Y507 (ingredient states), Y509 (search by ingredient-action pairs).

## Approach analyses

Case notation on paper: `x[F]` food span, `[Ac]` action by chef, `[Af]`
action by food, `[Sf]`/`[St]` food/tool state, `[D]` duration, arrows are
labelled edges in the Y500/Y501 scheme.

### A. Recipe flow graph, r-FG (Y501 Japanese; Y500 English; used by Y503, Y508, Y509, Y510)

- **E1 representation and purpose.** One graph per recipe text. Nodes are
  text spans typed as food (ingredient, intermediate or final), tool,
  action (by chef, by food, by tool), state (food, tool), duration, quantity;
  edges are predicate-argument and identity/part relations; DAG with one
  root. Purpose: machine understanding of one written procedure (search,
  smart-kitchen support, video grounding, text generation).
- **E2 evidence.** Demonstrated: two corpora (266 Japanese incl. 66 of one
  dish, Y501; 300 English, Y500), annotation agreement 82.3 F1 on edges and
  90.5 on tags (Y500), parsers up to 92.2 F1 (Y510, abstract), image-state
  extension (Y508), ingredient-path search (Y509, abstract). Claimed only:
  usefulness for comparing recipes of one dish (Y501 §6.1).
- **E3 mapping on paper.**
  - K1 (one documented route, `transfer:rutabaga_gratin`): `potato[F] ->
    slice[Ac] (2-3 mm[St])`; `rutabaga[F] -> peel[Ac] -> slice[Ac] -> blanch[Ac]`
    with `3-5 min[D]` and `crisp tender[Sf] -V-tm->`; both sliced outputs
    `-targ-> layer[Ac] -dest-> dish[T]`; `cream[F] -targ-> pour[Ac]`;
    `-> bake[Ac]` with `oven[T]`, `55-60 min[D]`, and a V-tm sub-graph
    `knife[T] -t-comp-> insert[Ac] ... no resistance[Sf]`; `rest[Af]`. The
    member endpoints after layering (potato "no resistance", rutabaga "some
    give" in Q231 vs "no resistance" in Q232) can only be written as Sf spans
    hanging off the single bake action, linked to a member by F-part-of if the
    text names the member (the Y500 example "centre of loaf" shows F-part-of on
    an assembled food).
  - K9 (latkes): `potato[F] -> grate[Ac] -> squeeze[Ac]`; the squeezed liquid
    as a new F span with F-part-of from the grated mass; `settle[Af]`,
    `pour off[Ac]`, `starch[F]` returned `-targ-> mix[Ac]` with the mass. This
    is exactly Y501's reason for using a DAG (food separation, §4.12).
  - K5: peel with the skin as `skin[F] F-part-of stem[F]`; whether the peel
    goes on as a second output depends on the text naming it.
  - K4/K3: the vessel or wrapper as `Dest` (container) of `fill`/`roll`, or
    as `F-comp` (food used as a tool); neither label says "structural".
  - K2-x, K6, K8 verdicts: not representable as a recipe text (no text
    documents them); a graph records what one text says.
- **E4 table** (cases where the scheme applies: K1, K3, K5, K7, K9).

  | aspect | K1 | K3 | K5 | K7 | K9 | reason |
  | --- | --- | --- | --- | --- | --- | --- |
  | a components and joins | preserved | preserved | preserved | preserved | preserved | parallel branches merge at an action; join kind (layer, wrap, coat) only as the verb, no role typing beyond Dest/F-comp |
  | b intermediate states, readiness vs doneness | extend | extend | extend | extend | extend | Sf/D/V-tm keep "until tender" and times; no distinction between a readiness endpoint and a final doneness endpoint, no failure checks |
  | c member after assembly | cannot | cannot | n/a | cannot | n/a | after a merge only the merged node exists; a member state needs a text span plus F-part-of, not a modelled member |
  | d why a stage exists | cannot | cannot | cannot | cannot | cannot | edges give order and argument flow only; no purpose relation (RiCoRecA's Why, approach E, adds one) |
  | e alternative routes kept apart | preserved | preserved | preserved | preserved | preserved | one graph per text keeps them apart by construction, but with no link between them |
  | f substitution consequences | cannot | cannot | cannot | cannot | cannot | nothing re-checks a graph when a node changes |
  | g start from an existing state | extend | extend | extend | extend | extend | a graph can be cut at a node and a path from an ingredient read (Y509), but two recipes' "boiled potato" nodes are not identified as one state |
  | h provenance | preserved | preserved | preserved | preserved | preserved | every node is a span with text position (Y501 §3); provenance is per recipe text, not per claim across sources |
  | i unknown vs false | cannot | cannot | cannot | cannot | cannot | a missing edge means no annotated relation; no unknown |
  | j readable for a cook | cannot | cannot | cannot | cannot | cannot | Y500 states it is not meant to be shown to a cook |

- **E5 against Food-prep.** Meets R1 (operations on materials with state
  change: Y501's before/after distinction via F-eq is the same idea as R1's
  resulting state, but untyped), R3 (components and joins), R5 partly
  (durations, "until" states). Food-prep's material key (part + state) is a
  typed, cross-recipe identity that r-FG lacks; r-FG has typed *text*
  identity. Two r-FG concepts with no counterpart in the Food-prep records
  read for this file: **action by food as a trigger** (`water boils[Af]
  -V-tm-> add[Ac]`: the cook waits for a food event) and **tool state as its
  own branch** (preheat oven, grease tin, joined to the later use by A-eq/T-eq).
  Whether R5 already expresses these (e.g. as steps or completion checks on a
  pan) was not checked in full: inferred, not verified.
- **E6.** Published: tag and edge inventory, DAG reasons, agreement, sizes
  (Y500, Y501); ingredient-path search (Y509, abstract); image states (Y508).
  Inferred in R6: all K mappings, the E4 table, the two "no counterpart"
  concepts.
- **Verdict: not suited** as a replacement (its unit is a text span of one
  recipe, built for text understanding); **extend** for two concepts that
  Food-prep may lack: food-event triggers (Af + V-tm) and tool-state
  preparation as a parallel branch. Food-prep already has the stronger form
  of identity (typed state, cross-recipe), so r-FG does not replace R1-R3.

### B. Action graph with implicit arguments ("mise en place", Y504)

- **E1.** Action = verb + typed arguments, including implicit ones;
  connections route each earlier output to a later argument; food and
  location propagate separately. Purpose: unsupervised parsing.
- **E2.** Demonstrated: 80.0 F1 with oracle segmentation on 100 test
  recipes; learned knowledge (bake in oven; "batter" contains flour).
- **E3.** K1: `bake` has an implicit food argument fed by `layer`'s output and
  an implicit location fed by `preheat`. K9: the model's prior penalises
  reusing one output twice; the paper names egg separation as a counterexample
  (fn. 2), so a K9 recombination is expressible but disfavoured.
- **E4 (short).** a preserved (argument flow); b cannot (no states or
  durations; listed as future work); c cannot; d cannot; e preserved (one
  graph per recipe); f cannot; g cannot; h preserved per text span; i cannot;
  j cannot.
- **E5.** The only concept beyond A is **location propagation** (the oven
  preheated earlier is where the bake happens). Food-prep writes materials
  explicitly, so implicit-argument recovery is an NLP problem it does not have.
- **E6.** Published: Y504. Inferred: the K mappings.
- **Verdict: not suited** (built to parse unannotated text); location
  propagation folds into the tool-state point under A.

### C. Ingredient merging tree, SIMMR, and MILK/CURD (Y505, Y515)

- **E1.** Leaves are ingredient-list items, internal nodes are whole
  instructions, one output per instruction. MILK (via Y505) is richer:
  combine names its output, `separate` exists.
- **E2.** 260 CURD recipes; 93.5% edge accuracy (Y505).
- **E3.** K9 cannot be expressed in SIMMR (separate is dropped; Y505 §3.3);
  K1: blanched rutabaga and sliced potato merge at "layer", then a chain of
  single-input nodes (pour, bake, rest). Non-food steps (preheat) are folded
  into the previous node, so tool preparation disappears.
- **E4 (short).** a preserved for merges, cannot for splits; b cannot; c
  cannot; d cannot; e preserved; f cannot; g cannot; h preserved (instruction
  index); i cannot; j partly (a merge tree is readable; not tested).
- **E5.** Food-prep R3 assemblies with roles, plus R1 fractions, are a
  superset. Y505's stated observation that steps may reorder freely as long
  as the order of combinations is kept matches what R5 dependency links
  express (inferred correspondence).
- **Verdict: already equivalent** (Food-prep's R1+R3 cover it and keep the
  splits SIMMR drops).

### D. Cross-recipe alignment of the same dish (ARA, Y503; MM-ARC, Y506)

- **E1.** ARA: action-level correspondence from a longer recipe to a shorter
  recipe of the same dish, "None" allowed, judged by people reading both
  recipes. MM-ARC: sentence-level alignments across text and video recipes of
  a title, joined into multi-recipe sets by a spanning forest. Purpose:
  aggregate how a dish is made; ARA's goal of finding common and distinct
  parts is stated as future work (Y503 §6).
- **E2.** Demonstrated: ARA 110 recipes/10 dishes, human 79%, model 72.4%;
  MM-ARC 150K pairwise alignments, text-text F1 54.55, full three-way human
  agreement on only 42% of instructions. Claimed only: aggregation into common
  vs variant structure.
- **E3 mapping: the K1 gratin alternatives aligned** (taking the R5 main
  route and its `alternatives` list, `processing_conditions.yaml` 1285-1290,
  as five "recipes" of one dish; source = longest):

  | main route step (Q231) | pre-cook both (Q232) | simmer in liquid (G5, G9, Q229) | raw long bake (G7, Q234, G8) | raw short bake (G20, G21) |
  | --- | --- | --- | --- | --- |
  | blanch rutabaga 3-5 min | swede 5 min (aligned) + potato 1 min (extra, no counterpart in source) | simmer ~10 min in the cream (many-to-one: absorbs blanch **and** pour cream) | None | None |
  | pour cream | pour | (absorbed above) | pour | pour |
  | bake 55-60 min covered then uncovered | 60-80 min in a bain-marie (aligned bake) | 25-40 min (aligned bake) | ~50 min covered + uncovered, ~90 min total (aligned bake) | ordinary bake (aligned bake) |

  What the alignment shows: the decisive difference between the working raw
  long bake (K8's false negative) and the failing raw short bake (K8's
  documented failure) is not in the action correspondence at all; both align
  "bake" to "bake", and the difference lives in a duration modifier that
  action alignment ignores. And the "None" against the blanch says nothing
  about **why** the long-bake route can do without it (the longer covered bake
  compensates; R5 `depends` on Q231/Q234 says the blanch exists because of
  the bake).
  - **K1-x on paper.** ARA's transitive-closure design (§4.1) composes
    correspondences across recipes; an aggregation that takes "blanch" from
    the G16/G18 10-min "almost tender" source and "bake" from the raw long-bake
    source because each aligns to the main route's steps produces exactly the
    undocumented K1-x combination. Nothing in either corpus marks the result as
    unverified.
  - **K2-x on paper.** "Boil 5 min then stand" (Q109) and "soak overnight"
    would align as corresponding hydration actions (ARA's many-to-one and
    implicit-action categories). The constraint that the raw-soaked route
    must never be cooked (Q114) is a property of the route's later grinding
    and frying, not of the soak action, so action alignment cannot see it.
    ARA counts negative events ("avoid over mixing") as 2% of hard cases but
    has no representation for a prohibition tied to a state.
- **E4 table** (K1 alternatives, K2/K2-x, K1-x, K7 two rice routes).

  | aspect | K1 alts | K2 / K2-x | K1-x | K7 (arancini vs suppli rice) | reason |
  | --- | --- | --- | --- | --- | --- |
  | a components and joins | extend | extend | extend | extend | alignment is between actions; components only through the underlying graphs |
  | b intermediate states | cannot | cannot | cannot | cannot | action graphs drop states and durations (Y503 §3.4) |
  | c member after assembly | cannot | cannot | cannot | cannot | not modelled |
  | d why a stage exists | cannot | cannot | cannot | cannot | a "None" alignment does not say what compensates for the missing step |
  | e alternatives kept apart, each with evidence | preserved | preserved | **cannot (risk)** | preserved | each recipe keeps its own graph; the risk is in aggregation, which composes steps from different sources without a status for the result |
  | f substitution consequences | cannot | cannot | cannot | cannot | alignment does not re-check a route |
  | g start from a state | cannot | cannot | cannot | extend | correspondences could show that the boiled-rice and risotto routes meet at "cooled cooked rice"; not done in the papers |
  | h provenance | preserved | preserved | cannot | preserved | each node traces to its recipe; a composed route has mixed provenance with no flag |
  | i unknown vs false | extend | extend | cannot | extend | "None" is explicit (absent counterpart); there is no "not judged" |
  | j readable for a cook | extend | extend | extend | extend | ARA's motivation is explaining a dish at several levels of detail; no user study |

- **E5.** Meets R5's alternatives and conflict versions, and R4's idea of a
  route "with one thing changed". Food-prep keeps alternatives apart with
  sources (R5 `alternatives`, e.g. lines 1285-1290) but as one-line summaries;
  it has **no step-level correspondence** between a route and its
  alternatives. ARA shows such links must allow None, one-to-many and
  many-to-one (26% of hard cases), and that people judge correspondence by
  arguments as well as verbs.
- **E6.** Published: ARA design, sizes, agreement, disagreement categories,
  transitive-closure assumption (Y503); MM-ARC joint alignment and agreement
  (Y506). Inferred in R6: the K1 alignment table, the K1-x and K2-x risk
  readings.
- **Verdict: extend.** Food-prep could record, for alternatives of one dish,
  which step corresponds to which (with None and n:1 allowed) and what a
  missing step is compensated by, while never composing steps across sources
  into a route. The aggregation goal of this literature (Y503 §6, Y506 joint
  alignment) is **not suited**: it is the mechanism that produces K1-x/K2-x
  combinations; Food-prep's existing rule (documented routes only, unverified
  combinations named as such) is the stronger practice here.

### E. Rich annotation schema with control and purpose tags (RiCoRecA, Y502)

- **E1.** Entities plus control tags (If, Until, Repeat), purpose (Why),
  required state linked to Until, alternatives (Or), parallelism (Join),
  ordering (Dependency). Purpose: program kitchen devices from recipes.
- **E2.** 156 recipes; agreement 0.71-0.91 F; PEGASUS-X 0.83-0.88 F on tags
  and relations, weak on long dependencies (Y502).
- **E3.** K1: "blanch ... until crisp tender" -> Until + State-of-Ingr;
  "because rutabaga is dense" (if a source says so) -> Why on blanch. K1
  conflicting doneness: within one text only; across Q231 and Q232 the schema
  has no place. K2: "soak overnight; if using quick-soak, boil 5 min" -> If on
  an alternative branch, Or between the two soak predicates; the prohibition
  in Q114 has no tag (not verified that negation is absent; the digest names
  none).
- **E4 (short, K1/K2).** a preserved (Join, Member); b extend (Until + State,
  but no readiness vs doneness, no failure); c cannot; d **preserved** when the
  text states a reason (Why); e extend (Or keeps alternatives inside one text;
  across sources nothing); f cannot; g cannot; h preserved per span; i
  cannot; j cannot (device workflows).
- **E5.** Why ~ R5 `depends ... because`; Until + State ~ R5 completion checks;
  Or inside one source ~ R5 keeps alternatives, though R5 ties them to
  sources rather than to the text of one recipe. If (conditional step: "if
  still firm, 5 min more under foil", Q231 in R5 line 1264) is already written
  by Food-prep as text inside a completion check, not as a structured
  conditional (inferred from the record).
- **E6.** Published: tag set, sizes, agreement (Y502). Inferred: mappings and
  equivalences.
- **Verdict: already equivalent** for Why/Until/State (Food-prep's R5 has
  them with sources, and adds readiness vs doneness and failure, which
  RiCoRecA lacks); **extend** for the structured conditional (If) as a
  candidate refinement of R5 completion checks. Not suited as a whole
  (written for device control).

### F. Ingredient state tracking (Y507 world-state annotation; Y513 NPN; Y514 action conditions)

- **E1.** Y507: per step, the world state of every ingredient, with
  transformations as (input, output) pairs of 1:1, 1:N, N:1 and free-text
  states; a checker that nothing vanishes or appears unintentionally. Y513:
  learned action operators update entity state vectors. Y514: pre- and
  postconditions of actions.
- **E2.** Y507 demonstrated: 100 annotated Japanese recipes, edge F1
  0.86-0.95 between annotators; models fail mostly on split, discard and
  recombination. Y513, Y514: abstract only.
- **E3.** K9 is the hardest published case type: the settled starch is a 1:N
  split (liquid -> starch + discarded water) followed by an N:1 recombination
  (Y507's named failure mode). K5: peel is 1:2 (peel discarded, stem kept). K1
  members after layering: a world-state record per step would keep "potato:
  layered, raw slices" and "rutabaga: layered, blanched" separately after the
  join, which is what Food-prep's R3 gap (an assembly takes its carrier's
  state) lacks; Y507 does not say whether its states persist per member after
  N:1 merges (not verified).
- **E4 (short, K1/K5/K9).** a preserved; b extend (states recorded, free text,
  no readiness/doneness); c **extend** (a per-step world state is the natural
  place for members after joining; not confirmed for merges); d cannot; e
  preserved (per recipe); f cannot; g extend (a state is an explicit record
  that could be matched); h preserved (step index); i cannot; j cannot.
- **E5.** Meets R1 (state change, several fractions) and the R3 known gap.
  Food-prep's typed flags are stronger than free text. The **conservation
  check** (every material either used later, or explicitly discarded) is a
  validation concept; whether Food-prep's validators already check that every
  fraction is consumed or discarded was not checked: inferred.
- **E6.** Published: Y507 scheme and failure modes; Y513, Y514 abstracts.
  Inferred: K mappings, the bearing on the R3 gap, the conservation check.
- **Verdict: extend.** Two concepts worth testing on paper in Food-prep: (1)
  a per-step record of each member's state after an assembly (addresses the
  R3 gap directly; evidence that it is annotatable comes from Y507's
  agreement, but merges are its weakest area); (2) a conservation check on
  fractions. Y513 and Y514: **insufficient evidence** (abstracts only).

### G. Dependency and counterfactual benchmarks (Y511 CaT-Bench; Y512 counterfactual recipes)

- Abstract only. Y511 shows language models over-predict step dependence
  from text order; Y512 shows models swap an ingredient but miss the actions
  that should change. Both support, from outside, Food-prep's choice to state
  dependencies explicitly with reasons (R5) and to re-validate a whole route
  after a substitution (R4), but neither offers a representation.
- **Verdict: insufficient evidence.**

## Answers to Q1-Q6 from this area

- **Q1 unit; two traversals.** The established unit is a typed text span
  (food, tool, action, state, duration, quantity) in a rooted DAG per recipe
  (Y501, Y500); simplified variants keep only actions (Y503 §3.4) or whole
  instructions over ingredient leaves (Y505). Intermediate products are nodes
  only when the text names them ("batter"), otherwise the producing action
  stands for its output (Y501 §4.1). Y501 separates an object before and after
  an action, which is the same idea as Food-prep's state-bearing material, but
  without typed state. Ingredient-to-dish traversal is published as search by
  ingredient-action path (Y509, abstract). No work found here uses one model
  for both directions across many dishes: every graph is one recipe text.
- **Q2 complete processes.** Parallel components and merges: preserved by
  all DAG schemes. Splits and recombination (K9): defined in Y501 §4.12,
  dropped in SIMMR (Y505), disfavoured in Y504, and the main failure of
  current models (Y507). Completion conditions ("until a skewer comes out
  clean", "until crisp and golden") are annotated as state/action spans tied
  to the action by a timing edge (Y500 Fig. 3-4, Y503 Fig. 2) or by Until
  (Y502); durations as D. **No source in this area separates readiness from
  doneness, records failure states, or models what a member undergoes after
  assembly**; purpose is tagged only by RiCoRecA's Why (Y502).
- **Q3 substitution.** Nothing in this area represents substitution
  consequences. Y512 (abstract) shows that generated recipes miss the actions
  a swap should change; EaT-PIM (flow graphs for substitution) belongs to the
  substitution area and was not read here.
- **Q4 alternative routes.** Recipes of one dish are aligned at sentence level
  (Y506, by exact title, F1 54.55 text-text, 42% full human agreement) or
  action level (Y503, 72.4% model vs 79% human). Common vs variant parts are
  a stated goal, not a published result. The literature's own disagreement
  analysis (many-to-one 26%, implicit 24%, no best match 17%) shows that
  "corresponding step" is often not well defined, and its transitive-closure
  and joint-path designs would compose steps from different sources without
  marking the result as undocumented: the K1-x/K2-x risk. Food-prep's
  separation of documented routes from unverified combinations has no
  counterpart in this literature.
- **Q5 reuse of preparations.** Nothing found on identifying the same
  intermediate state across recipes or on whether histories matter; Y501's
  before/after distinction is within one recipe only.
- **Q6 visualisation.** Y500 says flow graphs are not for display to cooks.
  Y503's motivation (explaining a dish at several levels of detail) is
  unevaluated. RecipeScape (Chang et al. 2018, cited by Y503) is a pointer
  for the visualisation area; not read here.

## Open questions this area leaves

1. Yamakata et al. 2016 ("extracting a major workflow" from cooking text,
   ICMEW, per Y503's references) is the one paper that may merge recipe flow
   graphs of one dish into a common workflow; not found. Without it, the Q4
   answer rests on alignment papers whose aggregation step is unpublished.
2. The 66 nikujaga flow graphs (Y501) are the only same-dish set with full
   r-FG annotation; whether anyone compared them (Yamakata et al. 2013,
   summarisation with flow graphs) is unknown (not read).
3. Does Y507 keep separate member states after an N:1 merge? If yes, it is
   the closest published model of the R3 gap (members after assembly); the
   digest did not say.
4. Does Food-prep R5 already express food-event triggers ("when the water
   boils") and tool preparation (preheat, hot pan) as their own steps? If not,
   these are the two r-FG concepts worth a paper mapping.
5. Should Food-prep add step-level correspondence between a route and its
   alternatives (with None and n:1), and how to forbid that correspondence
   from being read as permission to combine steps (K1-x, K2-x)?
6. Japanese-language sources (Shirai et al. JNLP 2023; Sasada et al. 2015
   JNLP on recipe term definitions; Hamada et al. 2000) were not read; the
   Japanese line of work is covered here only through English papers.
