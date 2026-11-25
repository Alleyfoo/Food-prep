# Evidence: ingredient substitution

(2026-11-25. Method: web search, then full text read wherever an open copy
existed (PMC, publisher open access, arXiv, university repository, author
copy); PDFs were downloaded by the fetch tool and converted to text locally
with `pdftotext`, and the text was read section by section. Citations were
followed backward from the two starting sources and forward through the 2024
survey (Y414) and the papers that cite GISMo (Y411, Y420). Search languages:
English, Japanese, German. Blocked: PMC's browser check (Y408 fallback to the
Frontiers PDF worked), HAL (Anubis bot block on two Taaable papers and one
INRAE review), CORE (403), Europe PMC (403), the IEICE FIT2013 server (405),
the first UCL repository URL (403; the direct PDF link from search worked).
Work stopped once for a usage limit and resumed; nothing read before the stop
was re-fetched.)

Notation used below: **[pub Ynnn §x]** = the capability is stated or shown in
that source; **[inf]** = inferred in R6 by this agent, not claimed by the
source.

## Sources

### Y401 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8837940/
- citation: Ławrynowicz A., Wróblewska A., Adrian W. T., Kulczyński B.,
  Gramza-Michałowska A. (2022). Food Recipe Ingredient Substitution Ontology
  Design Pattern. *Sensors* 22(3):1095. DOI 10.3390/s22031095.
- version read: PMC full text.
- type: primary research (ontology design).
- E1: an OWL ontology design pattern. A recipe is a *plan specification*
  (not a process) with an ingredient set and an instruction set. A
  substitution is a reified n-ary *specification* that links the recipe, the
  replaced and the replacing ingredient specification, an **objective**
  (e.g. more fibre, no sugar) and **conditions** of three kinds:
  technological, dietary, cultural (§4.4). Its effects are an *ingredient
  set transformation* and an *instruction set transformation* (§4.4). Two
  settings: a context-free substitution and a recipe-specific one (§4.4).
  Distinguishes a **substitute** (process kept, similar product) from an
  **analog** (ingredients and process changed to imitate the original)
  (§1.1); an "empty" substitution means omission; obligatory against optional
  ingredients (§1.1, §4.4). Worked example: pancakes, where the substitution
  adds a "melt butter" step 0 (Tables 3-4).
- E2: 12 competency questions, 3 motivating scenarios (lack of product,
  allergy, diabetes; Table 2), one worked example, pattern published on
  OntologyDesignPatterns.org. **No evaluation** against data, no populated
  knowledge base, no user study. The substitution-ratio competency question
  (CQ9) is posed but not shown encoded.

### Y402 — https://discovery.ucl.ac.uk/id/eprint/10220617/1/dke-substitution-logic.pdf
- citation: Bikakis A., Diallo A., Dickens L., Hunter A., Miller R. (2026).
  A commonsense reasoning framework for substitution in cooking. *Data &
  Knowledge Engineering* 163:102558. DOI 10.1016/j.datak.2026.102558 (received
  2024-02-15, online 2026-01-22, CC BY).
- version read: repository PDF of the published article (39 pp.), full text.
- type: primary research (formal framework).
- E1: a recipe is a set of clauses in a clausal (propositional, grounded)
  logic over timepoints: *do* atoms (action term with durations, locations,
  modifiers), *onhand* atoms (food term with qualities, counts, measures),
  *consume* atoms; preparation, consumption, ramification and background
  clauses, plus **integrity constraints** (§3). A cooking session = recipe +
  assumptions (what is on hand) + constraints/background (Def. 2).
  Substitution happens at three levels: **term** (swap an ingredient,
  equipment, an action's parameter), **condition** (swap atoms in a clause's
  body) and **clause** (swap whole steps, adding or removing steps) (§5).
  **Primary** substitution = for a missing item or an action that cannot or
  will not be done; **secondary** substitution = a mitigation that restores
  consistency with the integrity constraints after the primary one (§6,
  Defs. 15-16; Fig. 4). A minimal mitigation is the smallest such tuple
  (Def. 14, 16). No mitigation need exist (Prop. 11); one always exists if
  the constraint set is "sensible" (Prop. 12). Candidates come from distance
  measures: a **role distance** (Jaccard over an ingredient's roles *per
  recipe type*, e.g. thicken, bind, shorten, aerate, glaze; Def. 5), word
  embeddings, or operational knowledge such as substitution tables (§4).
  Four **drivers** (§7, Fig. 1): similarity to the missing item; similarity
  to the original dish; minimal secondary changes; improve a specified dish
  property; §7.5 shows each pair can choose differently. A **typology of
  integrity constraints** (§8.1): action duration, onhand quantity, consume
  quantity and availability, onhand location, parallel actions, preparation
  (an intermediate requires its action, e.g. sliced carrot requires slice,
  Ex. 38), equipment (one oven; two items in the oven at different
  temperatures conflict), properties of food items (a dish named chicken
  supreme requires chicken; a beef burger without meat loses meaty flavour).
  Constraints are grouped by how they can be obtained: fixed, pattern-based,
  general (from knowledge graphs) (§8.2). Minimal inconsistent subsets
  localise the problem and point to the kind of mitigation (Def. 21, §8.3).
  Recipe properties: finite, viable, minimal, consistent (§10).
- E2: definitions, propositions with proofs, worked examples (spaghetti to
  fusilli cooking time, Ex. 41-42; sliced to grated carrot, Ex. 38; chicken
  supreme to butter beans, Ex. 43; layered cake in one oven, Ex. 52).
  **No implementation, dataset, evaluation or user study** in this paper
  (searched for "evaluat", "experiment", "implement": none beyond a remark
  that grounding allows SAT solvers, §3.3.2). Integrity constraint
  generation from knowledge graphs is future work (§8.2, §10).

### Y403 — https://arxiv.org/pdf/2306.09042 (abstract page https://arxiv.org/abs/2306.09042)
- citation: Bikakis A., Diallo A., Dickens L., Hunter A., Miller R. (2023).
  A Graphical Formalism for Commonsense Reasoning with Recipes. arXiv
  2306.09042 v1 (no venue listed).
- version read: arXiv v1 PDF, full text.
- type: primary research (formalism).
- E1: a recipe is a labelled bipartite graph of comestible nodes and action
  nodes with a typing function into type hierarchies (§3). **Acceptability
  tuples** (input type, action type, output type), e.g. (raw carrot, chop,
  chopped carrot), make a recipe acceptable when every arc triple is in the
  set (Def. 4, §4); tuples can be inferred up and down the hierarchy. **Type
  substitution** relabels nodes (Def. 12); a primary substitution set plus a
  minimal secondary set restores acceptability (Defs. 13-14); a cost sums
  distances (Def. 15); a preferred pair minimises cost (Def. 16).
  **Structural substitution** replaces a subgraph by another with the same
  frontier (Def. 20) and subsumes type substitution (Prop. 10). §7 notes a
  distance may be recipe-relative: aquafaba for egg in baking, not in an
  omelette.
- E2: definitions and figures only; no evaluation.

### Y404 — https://discovery.ucl.ac.uk/id/eprint/10211668/1/Hunter_18606_pub.pdf (landing page https://jair.org/index.php/jair/article/view/18606)
- citation: Bikakis A., D'Asaro F. A., Diallo A., Dickens L., Hunter A.,
  Miller R. (2025). A Graphical Formalism for Reasoning about Substitution in
  Resource Transforming Procedures. *Journal of Artificial Intelligence
  Research* 84, Article 1. DOI 10.1613/jair.1.18606.
- version read: repository PDF of the published article (45 pp.), full text
  skimmed by section, §5.1 and §10 read closely. (The JAIR PDF link itself
  returned no text.)
- type: primary research + implementation.
- E1: the Y403 graph extended: by-products as explicit outputs (§4, e.g.
  pasta water; reuse of by-products named "exploitation"), parameterised
  action and consumable types as syntactic sugar ("bake at T for M minutes",
  §3.1), composition of recipes from subrecipes (§7), type and structural
  substitution (§8-9), domains beyond cooking (DIY, manufacturing, water
  treatment, crisis response, §11). §5.1: acceptability tuples should be
  built **from established practice** of the users' context or culture when
  reasoning conservatively, relaxed when exploring; candidate sources are
  mining Recipe1M and LLMs (their PizzaCommonsense corpus).
- E2: an answer-set-programming implementation in clingo (on GitHub) that
  checks recipe validity against given acceptability tuples, extracts tuples
  from given recipes, and searches for least-cost secondary type
  substitutions (example: uncooked spaghetti to uncooked fusilli) (§10).
  §10.1 "Experimental evaluations" measure **CPU time only** (tuple
  discovery, type substitution, solver configurations); the authors state the
  purpose is to test the definitions on case studies, not scalability. No
  evaluation of whether the substitutions found are good.

### Y405 — https://pubdb.vislab.is.i.nagoya-u.ac.jp/~murase/pdf/376-pdf.pdf
- citation: Shidochi Y., Takahashi T., Ide I., Murase H. (2009). Finding
  Replaceable Materials in Cooking Recipe Texts Considering Characteristic
  Cooking Actions. Proc. ACM Multimedia 2009 Workshop on Multimedia for
  Cooking and Eating Activities (CEA'09), Beijing, pp. 9-14. DOI
  10.1145/1630995.1630998 (DOI from Y402's reference list and a search
  record; not verified on the ACM page).
- version read: author PDF (Nagoya University), full text. Japanese-language
  versions (JSAI 2008; a journal article "Finding Replaceable Materials by
  Cooking Recipe Mining") were found by search but not read.
- type: primary research.
- E1: Japanese recipes (Ajinomoto recipe site) grouped into "recipe groups"
  by the last term of the dish name (croquette, gratin, curry, roll...)
  (§2.2). Each material gets a vector of its **characteristic cooking
  actions** within the group (TF-IDF over group verbs; actions occurring with
  the material in >75 % of the group's recipes) (§2.4). Materials whose
  action vectors are close (cosine), weighted by whether they are of the same
  kind in the Japanese Food Composition Table, are "replaceable" (§2.4-2.5).
  The premise, stated: a material can be substituted if its corresponding
  cooking actions match (§2.4).
- E2: 6,789 recipes classified; experiment on 391 recipes in nine groups, 168
  materials, 92 candidate pairs (§3.1). Evaluation by **one judge** (a
  housewife with a dietitian's qualification) on 40 substituted recipes plus
  13 originals, with **three categories plus N/A**: (1) materials and
  procedure appropriate; (2) materials appropriate but the cooking procedure
  must change; (3) replacement impossible; N/A hard to judge. Result: 15 /
  15 / 1 / 9 (Table 4); 75 % judged 1 or 2. The one impossible case was
  macaroni to *steamed* rice in macaroni salad; the authors note it would work
  with *uncooked* rice and warn about pre-cooked materials (§3.2.2). Two
  pizza toasts were cooked and tasted; opinions split (§3.3). Conclusions:
  substituting a material alone is insufficient; materials and their cooking
  actions should be replaced together, with their order (§4).

### Y406 — https://arxiv.org/pdf/1111.3919v3 (abstract https://arxiv.org/abs/1111.3919)
- citation: Teng C.-Y., Lin Y.-R., Adamic L. A. (2012). Recipe recommendation
  using ingredient networks. Proc. 4th ACM Web Science Conference (WebSci
  '12), pp. 298-307 (venue and pages from arXiv record and Y402's references).
- version read: arXiv v3 PDF, full text.
- type: primary research (data mining).
- E1: from 46,337 allrecipes.com recipes and 1,976,920 reviews (§3), a
  directed weighted **substitute network**: an edge a to b weighted by the
  share of suggested replacements of a that name b, from patterns such as
  "replace a with b", "b instead of a"; pairs suggested fewer than 5 times
  dropped (§5.3). Also review-mined modifications: increase / decrease
  quantity, omit, add (§5.1-5.2). Ingredient extraction **strips state
  words** ("chopped", "cold") and quantities (§3.1), so substitution is
  between bare ingredient names.
- E2: clusters of mutually substituted ingredients (Table 2, Fig. 6-7); 60.1
  % of reviews signal a modification; reviews with modifications rate higher
  (§5). The substitute network contributes to predicting recipe ratings
  (accuracy .792 with nutrition; substitution features 39.8 % of network
  feature importance) (§6). No direct validation that the mined pairs are
  correct.

### Y407 — https://arxiv.org/pdf/1607.08807 (abstract https://arxiv.org/abs/1607.08807)
- citation: Achananuparp P., Weber I. (2016). Extracting Food Substitutes
  From Food Diary via Distributional Similarity. arXiv 1607.08807 v1; "to
  appear at HealthRecSys'16" (venue publication not verified).
- version read: arXiv v1 PDF, full text.
- type: primary research.
- E1: a food item's context is the other foods logged in the same meal
  (MyFitnessPal public diaries); substitutability = cosine similarity of PPMI
  or SVD vectors (§2). Foods are whole logged entries (e.g. sandwiches,
  bacon), not recipe ingredients.
- E2: 9,896 users, 1,919,024 meals, ~717 k unique entries (Table 1); 100
  protein-group queries, top-10 candidates per method, 2,000 pairs rated by 3
  crowd workers each on a 7-point scale (§4.1); prec@1 0.75-0.77 at the
  lenient threshold (Table 2). Limits stated: workers mostly outside the US
  (cultural bias), 10 % of entries discarded (§6).

### Y408 — https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2020.621766/pdf
- citation: Shirai S. S., Seneviratne O., Gordon M. E., Chen C.-H.,
  McGuinness D. L. (2021). Identifying Ingredient Substitutions Using a
  Knowledge Graph of Food. *Frontiers in Artificial Intelligence* 3:621766.
  DOI 10.3389/frai.2020.621766.
- version read: publisher PDF, full text (PMC copy blocked by a browser
  check).
- type: primary research.
- E1: DIISH, a heuristic combining four scores over FoodKG: FoodOn class
  similarity, word-embedding similarity, co-occurrence profiles, and PPMI of
  ingredient against recipe context (the other ingredients), with
  coefficients tuned on 100 development targets (§2.3). Dietary constraints
  filter candidates by FoodOn class paths and USDA nutrients (§2.1-2.2).
  Ingredient states are merged: "tomatoes", "ripe tomatoes" and "diced
  tomatoes" map to one FoodOn tomato class (§2.3).
- E2: ground truth from substitution guides (AllRecipes, Food Network,
  Colorado State, North Dakota State), The Cook's Thesaurus, and pattern
  matches in 1.1 million Food.com reviews (§2.4.1, Table 1); MAP, MRR, recall
  at k; DIISH beats each component (§3). Limitations (§4.2): FoodOn class
  structure and wrong links (e.g. "baking potato" linked to "potatoes
  gratine"); ground truth incomplete (squash for potato missing). Table 6:
  for target **potato**, ground truth lists cauliflower, sweet potato,
  **rutabaga**, parsnip, with no recipe context.

### Y409 — https://www.scitepress.org/Papers/2021/102020/102020.pdf
- citation: Pellegrini C., Özsoy E., Wintergerst M., Groh G. (2021).
  Exploiting Food Embeddings for Ingredient Substitution. Proc. 14th Int.
  Joint Conf. on Biomedical Engineering Systems and Technologies (BIOSTEC
  2021), Vol. 5: HEALTHINF, pp. 67-77, SCITEPRESS (venue and pages from Y402
  and Y403 reference lists; the PDF read is the SciTePress paper with this
  title).
- version read: publisher PDF, full text.
- type: primary research.
- E1: explicitly **context-free** substitutes (§1): Food2Vec (word2vec on
  Recipe1M+ instructions), FoodBERT and a multimodal FoodBERT, and a
  FoodBERT relation extractor over comments (§4-5). A substitute is defined
  as one the annotators "can think of several dishes" for (§6.1).
- E2: human evaluation of 200 pairs per method by **two authors** with
  amateur cooking experience (kappa 0.72); a ground truth of 42 ingredients
  (708 pairs) seeded from a substitution book and **extended with correct
  predictions of the evaluated approaches** (§6.1.2); FoodBERT precision
  0.806-0.844 (§6.3). §2 summarises earlier evaluations as small-scale
  cooking tests or qualitative analysis.

### Y410 — https://arxiv.org/pdf/2302.07960 (abstract https://arxiv.org/abs/2302.07960)
- citation: Fatemi B., Duval Q., Girdhar R., Drozdzal M., Romero-Soriano A.
  (2023). Learning to Substitute Ingredients in Recipes. arXiv 2302.07960 v1
  (no peer-reviewed venue listed).
- version read: arXiv v1 PDF, full text.
- type: primary research + dataset (Recipe1MSubs) + implementation.
- E1: substitution as ranking: given a recipe (title, ingredient set,
  instructions) and a source ingredient s, rank a target y so that the
  ingredient set becomes I minus s plus y; one-to-one only (§2). Tuples are
  directional and may hold only in that recipe (§2). GISMo: a graph network
  over FlavorGraph (6,653 ingredients, co-occurrence and flavour molecules)
  plus a **context embedding = the mean of the recipe's ingredient
  embeddings** (title in ablation); instructions are not used (§3).
- E2: Recipe1MSubs: pairs from Recipe1M user comments by keyword patterns
  and heuristics (exactly two ingredients, close to the keyword, one of them
  in the recipe); 49,044 / 10,729 / 10,747 train/val/test (§2). MRR 31.51,
  Hit@1 20.56, Hit@10 54.27 against a lookup-table + frequency baseline at
  MRR 27.66 (Table 1). All recorded targets for the same source and recipe
  count as correct; any valid substitute nobody wrote in a comment counts as
  wrong. Integrated into an image-to-recipe generator; failure cases include
  generic instructions after an apparently minor substitution (Fig. 12).
  No human validation of the dataset.

### Y411 — https://ceur-ws.org/Vol-4196/paper_20.pdf
- citation: Loesch J., Schimmel D., Erdem F., Kalkavan D., Bilgin Z., Celebi
  R. (2025). Enhancing GISMo: Integrating Recipe Contexts into a Graph-Based
  Ingredient Substitution Module. SWAT4HCLS 2025, CEUR Workshop Proceedings
  Vol. 4196 (published 2026-04-22).
- version read: CEUR PDF, full text.
- type: primary research + dataset (ArcSubs).
- E1: GISMo with richer graphs: ingredient-recipe bipartite graphs, cooking
  actions as nodes (verbs and nouns extracted per step), a DAG approximating
  instruction dependencies (§4).
- E2: **ArcSubs**, the only expert-validated in-context set found: four
  domain experts (an appliance maker's staff) judged Recipe1MSubs pairs
  shown with the full recipe, answering yes/no: fits the recipe; major taste
  change; major nutrition change; **requires major modification of the
  cooking process**; changes food category (§3.1). Fleiss kappa: fits 0.73,
  process 0.58, category 0.67, taste poorer; experts declined the nutrition
  question (§3.2). Fit correlates negatively with needing major process
  change (§3.2). 656 samples, 448 recipes, 182 pairs kept by majority "fits"
  (§3.3). Removing 20 % of FlavorGraph edges did not hurt GISMo (§4). Richer
  context raised diversity, not ranking metrics (§8).

### Y412 — https://arxiv.org/pdf/2105.08185v2 (abstract https://arxiv.org/abs/2105.08185)
- citation: Li S., Li Y., Ni J., McAuley J. (2022). SHARE: a System for
  Hierarchical Assistive Recipe Editing. EMNLP 2022 (per arXiv record);
  arXiv 2105.08185 v2.
- version read: arXiv v2 PDF, full text skimmed, evaluation and limitations
  read closely.
- type: primary research + dataset (RecipePairs).
- E1: recipe editing for seven dietary constraints: first edit the ingredient
  list (insertions, deletions), then **regenerate the steps** with a language
  model; quantities omitted (§5). RecipePairs: 83 K pairs of a base recipe
  and a same-named recipe in a dietary category (§3).
- E2: automatic metrics; 336 recipes judged by crowd home cooks for
  constraint violation (Kendall tau 0.762); a **cooking study**: seven home
  cooks cooked 21 edited recipes; none reported difficulty; most common
  complaint (19 %) that the dish did not resemble the base recipe name (§6).
  Judges asked whether listed ingredients were raw or pre-processed (§6).
  Limitations: no guarantee the output is edible, coherent or safe (§8).

### Y413 — https://arxiv.org/pdf/0912.0132 (abstract https://arxiv.org/abs/0912.0132)
- citation: Badra F., Cordier A., Lieber J. (2009). Opportunistic Adaptation
  Knowledge Discovery. ICCBR 2009, Seattle (per arXiv record); arXiv
  0912.0132 v1.
- version read: arXiv v1 PDF, full text.
- type: primary research (CBR, Taaable).
- E1: Taaable adaptation knowledge as substitutions A ⇝ B between
  conjunctions of literals, with the context in the left side, e.g. "soup
  and pepper ⇝ soup and ginger" (pepper replaced by ginger *in soups*) (§3).
  Ontology axioms give generalisation substitutions; an extra adaptation
  knowledge base holds richer ones; differences between pairs of recipes
  ("variations" such as {oil =, peanut oil -, olive oil +}) are mined as
  frequent itemsets and interpreted as substitutions, and **each must be
  validated by a user acting as expert, in the problem-solving context**
  (§4-5).
- E2: prototype on 862 CCC 2008 recipes, demonstrated on use cases (one
  cake example in detail, §5.3); no quantitative evaluation. §3.3 gives two
  failures of ontology-only adaptation: removing peanut oil from a recipe
  where the oil is **used to sauté** the bok choy makes it unfeasible; raw
  leek replacing green onion **used as a garnish** changes the soup too much
  (a better adaptation fries the leek).

### Y414 — https://arxiv.org/pdf/2501.01958 (abstract https://arxiv.org/abs/2501.01958)
- citation: Kim H., Venkataramanan R., Sheth A. (2024). A Survey on Food
  Ingredient Substitutions. arXiv 2501.01958 v1 (submitted 2024-10-25).
- version read: arXiv v1 PDF, full text skimmed by section.
- type: survey (used only as a pointer).
- E1/E2: classifies work by data source (recipe sites, comments, curated
  guides, open datasets; §5.1), technique (rule-based, embeddings, knowledge
  graphs, "theoretical" designs; §5.2), extra knowledge (nutrition, health
  labels, recipe context, images, flavour; §5.3), applications (§5.4),
  safety (§5.5). Notes that benchmark datasets are rare and that comment
  data is unvalidated (§5.1, §5.5.2); notes ontologies do not capture how
  cooking methods change an ingredient's function (§5.2.4). Recipe context
  example: egg in cake against egg as a glaze (§5.3.3). No taxonomy of
  substitutions by process change.

### Y420 — https://arxiv.org/abs/2412.04922 (abstract only)
- citation: Senath T., Athukorala K., Costa R., Ranathunga S., Kaur R.
  (2024). Large Language Models for Ingredient Substitution in Food Recipes
  using Supervised Fine-tuning and Direct Preference Optimization. arXiv
  2412.04922 v1.
- version read: **abstract only**.
- type: primary research.
- E1/E2 (from abstract): LLMs fine-tuned on Recipe1MSubs; best Hit@1 22.04
  (Mistral-7B, SFT + DPO). No human evaluation or instruction change
  mentioned in the abstract.

## Failed pages and abstract-only

| URL or query | why | fallback tried |
| --- | --- | --- |
| https://discovery.ucl.ac.uk/id/eprint/10220617/ | 403 | direct repository PDF from search: read (Y402) |
| https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7861309/ and pmc.ncbi.nlm.nih.gov | 301, then browser check (captcha) | Frontiers `/text` 404; Frontiers `/pdf`: read (Y408) |
| https://jair.org/index.php/jair/article/view/18606/27221 | fetch returned no text | UCL repository PDF: read (Y404) |
| https://hal.archives-ouvertes.fr/hal-00720481 (Gaillard, Nauer, Lefevre, Cordier 2012, generic cooking adaptation knowledge) | Anubis bot block | none readable; not used |
| https://core.ac.uk/download/49875754.pdf | 403 | none; not used |
| Gaillard, Lieber, Nauer 2015, *Improving ingredient substitution using FCA and adaptation of ingredient quantities* (HAL hal-01240383; CEUR Vol-1520 proceedings) | HAL blocked; the large CEUR proceedings PDF not tried for lack of time | **not read**; known only from Y414 and Y408 reference lists |
| Boscarino C., Koenderink N., Nedović V., Top J. (2014), *Automatic extraction of ingredient's substitutes*, UbiComp '14 Adjunct, pp. 559-564, DOI 10.1145/2638728.2641334 (Dutch recipe data, context of substitution rules, per Y414) | only a repository record and Crossref seen in search | **not read** |
| https://www.ieice.org/publications/conference-FIT-DVDs/FIT2013/data/pdf/D-003.pdf (Japanese, FIT2013: extracting substitutable, addable and omittable ingredients; a search summary reports 37.5 % judged appropriate) | 405 | **not read**; the 37.5 % figure is a search snippet, not evidence |
| Japanese: Mizuno et al. (Nagoya), substitute detection by similarity of cooking processes; Ritsumeikan recipe recommender on ingredient essentiality; Tsukuba 2017 master's thesis on arranging recipes | found by Japanese search, not fetched | **not read** |
| https://hal.inrae.fr/hal-04180318v1/document (egg replacement review) | Anubis bot block | none |
| PMC8774821 (vegan egg review), PMC12651232 (AI-enabled ingredient substitution review with functional and sensory framework), Europe PMC copy | PMC browser check / 403 | **not read**: no food-science functional-role source read in this area |
| https://arxiv.org/pdf/2105.08185v2 via fetch summariser | binary | local text extraction: read (Y412) |
| SHARE recipe-edit evaluation details beyond §6 | not needed | — |

## Searches

| language | query | useful? |
| --- | --- | --- |
| en | "A Commonsense Reasoning Framework for Substitution in Cooking" | yes: Y402 PDF, Y403, Y404 |
| en | Shirai Seneviratne 2021 "Identifying Ingredient Substitutions Using a Knowledge Graph of Food" Frontiers | yes: Y408 |
| en | Taaable adaptation knowledge substitution "in the context of" ingredient Gaillard Lieber Nauer closed itemset | partly: Y413; others blocked |
| en | Shidochi Takahashi Ide Murase 2009 "replaceable materials" ... | yes: Y405 |
| en | ingredient substitution large language models recipe benchmark 2024 2025 context-aware | yes: Y411, Y420 |
| en | egg replacers review functional properties emulsifying foaming binding gelation bakery open access | leads only; all copies blocked |
| en | Gaillard Lieber Nauer "Improving ingredient substitution using formal concept analysis" Taaable | led to Y414 |
| en | Boscarino ... "Automatic extraction of ingredient's substitutes" | record only |
| ja | 代替食材 レシピ 推定 調理手順 論文 | yes as leads (Japanese line of work tying substitutes to cooking actions); none read in full |
| de | Zutaten Ersetzung Rezept Adaption Fallbasiertes Schließen Substitution Zutat Kontext | no German primary work on substitution found; led back to Y404 |

Not searched for lack of budget: French (Taaable theses), Italian, Spanish;
Pacifico et al. 2021 (allergy-safe substitution via Food.com interactions),
Lawo et al. 2020 (veganizer), Kazama et al. 2018 (local-cuisine
substitution with flavour), Yamanishi et al. 2015 — all named in Y409/Y414,
not read.

## Citation trail

- Backward from Y401: Taaable (Gaillard et al. 2015, 2017), IntelliMeal,
  DIISH (Y408), FoodOn's "has food substance analog" (criticised as
  symmetric and context-free). Followed: Y408.
- Backward from Y402/Y403/Y404: Y401, Y408, Food2Vec (Y409), Teng et al.
  (Y406), Shidochi et al. (Y405), FoodKG, Taaable 3 textual preparation
  adaptation and CookingCAKE (left to the CBR area, Y300s), Olteteanu &
  Falomir 2016 (object replacement by shape/material/role; not read).
  Followed: Y405, Y406, Y408, Y409.
- Forward from Y402/Y403: the same group's JAIR 2025 paper (Y404) and its
  PizzaCommonsense corpus (Diallo et al. 2024; not read, belongs to Y500s).
- Backward from Y406: Shidochi (Y405). From Y407: Boscarino 2014 (not read).
  From Y409: Druck & Pang 2012, Wiegand et al. 2012, Reiplinger et al. 2014
  (comment relation extraction; not read), Kazama 2018, Yamanishi 2015
  (cooking-tested evaluations; not read).
- Forward from Y410 (GISMo): Y411, Y420; SHARE (Y412) is cited in Y410 as
  the work that edits instructions too.
- Survey Y414 used to check coverage; it confirms no taxonomy by process
  change exists in the computational literature it covers.

## Approach analyses

Relevant cases for this area: K2, K3, K4, K5, K6, K1/K8 (and K1-x, K2-x).
K7 and K9 are not substitution cases; they are mentioned only where an
approach has something specific to say about them.

### A. Inconsistency-directed substitution in logic (Y402)

- **E1.** Unit: a cooking session (recipe clauses + what is on hand +
  integrity constraints). Purpose: a theory of substitution for reasoning
  systems; candidates by distance, consequences by constraint violation,
  repairs as secondary substitutions.
- **E2.** Demonstrated: definitions, propositions, worked examples.
  Claimed, not shown: that constraints can be generated from knowledge
  graphs; that it scales via SAT. No data, no evaluation, no cook.
- **E3 mapping (on paper) [inf unless marked].**
  - K2: primary term substitution `chickpea ⇝ dried_pea` in the onhand
    assumptions. Preparation constraint: "soaked pea" requires a soak action
    (pattern of [pub Y402 §8.1 Preparation]); action-duration constraint on
    the soak (12 h, P3/P15) from a knowledge graph triple [pattern pub Y402
    Ex. 51]. The raw-soaked rule "never boiled before frying" (Q114) is an
    integrity constraint with a negated *do(boil)* atom; K2-x (5 min boil
    quick-soak, Q109) then violates it and the minimal inconsistent subset
    names exactly that clause [pattern pub Y402 Def. 21]. P15 dryness is a
    "properties of food items" constraint only if someone writes the property
    down; the framework cannot predict it.
  - K3: primary `cabbage ⇝ napa_cabbage`. The whole-head blanch exists only
    to make cabbage leaves come off; with napa it is unnecessary but not
    inconsistent, so the framework keeps it (a mitigation is triggered only
    by inconsistency) unless the "minimal change" driver or a constraint
    "blanch requires a non-pliable head" removes it. The rib shave (N2) would
    need a property constraint on the wrapper.
  - K4: primary `courgette ⇝ onion`; secondary: the hollowing action becomes
    lifting inner layers (condition substitution), the blanch gets a
    duration constraint (overboiled layers slip, O10/O12). "Container must be
    hollow and stand" has no counterpart except as a hand-written property
    constraint. Two vessels sharing one filling: two clauses consuming parts
    of one filling quantity, handled by consume-quantity constraints [pattern
    pub Y402 §8.1].
  - K5: closest of all to a published example: Ex. 38 substitutes the
    intermediate (sliced carrot for chopped carrot) and repairs the
    producing action. Here `grated_carrot ⇝ grated_broccoli_stem`, secondary:
    add *peel* before *grate* (preparation constraint "grated stem requires
    peeled stem"). Reuse of a by-product (stem of a head used elsewhere) is
    not represented in Y402 (it is in Y404).
  - K6: primary `cabbage ⇝ curly_kale`; a property constraint "wrapper leaf
    must close around the filling" with `leaf_size(curly_kale) = small`
    makes it inconsistent; mitigation would be a clause substitution that
    wraps with several overlapped leaves (expressible: several onhand items
    consumed by one wrap action). Without evidence about leaf size, classical
    logic has no "unknown": either the constraint fires or it does not.
  - K1/K8: primary `potato ⇝ rutabaga` for some layers. An action-duration
    constraint "rutabaga slices need ≥ X min at oven temperature" makes the
    raw version (K8) inconsistent with the 60-min base bake. Two minimal
    mitigations: (a) condition/clause substitution adding a blanch (the
    documented K1 route); (b) term substitution of the bake duration to ~90
    min covered (G7, G8). Both are produced as separate mitigations, so the
    framework keeps the alternative that Food-prep's R4 model rejects (time
    is in Y402, not in Food-prep). But (b) changes the bake for the potato
    layers too: the framework sees that only if a constraint on potato
    doneness at 90 min exists (equipment/oven constraints are the published
    mechanism for interactions in one oven, [pub Y402 §8.1 Equipment;
    Ex. 52]). K1-x (blanch *and* long bake) is a non-minimal mitigation, so
    the "minimal secondary changes" driver would not propose it; nothing
    marks it as undocumented.
- **E4 table.**

| aspect | K2 | K3/K6 | K4 | K5 | K1/K8 |
| --- | --- | --- | --- | --- | --- |
| a. components and joins | extend: clauses produce intermediates, but no join types (mix vs matrix) | cannot: no wrap/wrapper role beyond hand-written constraints | cannot: no container role | preserved: intermediate as onhand item | extend: layers are separate onhand items; layering is an action |
| b. intermediate states, readiness/doneness | preserved: food terms carry qualities (soaked, raw) | extend: pliability is a quality, no readiness notion | extend | preserved | extend: duration constraints, not doneness tests |
| c. member after assembly | cannot: one bake affects all; only by constraints written per member | extend | extend | n/a | extend: needs per-layer constraint in a shared bake |
| d. why a stage exists | extend: a step is justified only by the constraint it satisfies; no recorded objective | extend | extend | preserved for peel (preparation constraint) | **preserved as a mechanism**: the blanch appears as the mitigation of a named violation |
| e. alternative routes with evidence | extend: several minimal mitigations kept, no evidence attached | extend | extend | extend | extend: blanch vs long bake both found; no citation |
| f. substitution consequences | **preserved, central**: primary/secondary with localisation | preserved | preserved | preserved | preserved |
| g. start from a state on hand | preserved: assumptions = what is on hand, incl. intermediates | preserved | preserved | preserved | preserved |
| h. provenance | cannot: no source field | cannot | cannot | cannot | cannot |
| i. unknown vs false | cannot: classical, closed constraint set | cannot (K6 is the test) | cannot | cannot | cannot |
| j. readable for a cook | extend: violations name the clause to change; logic not cook-facing | extend | extend | extend | extend |

- **E5.** Meets R4 directly: an R4 transfer = primary substitution (`swap`)
  plus replaced specs (`materials`, `steps`, `assemblies`) = term +
  condition + clause substitutions; R3's validator = consistency check;
  amendment A2 (`cooks_slowly`) = adding an integrity constraint that turned
  K8 from consistent to inconsistent. What Food-prep does not have: (1) a
  secondary change **recorded as the repair of a named violation** (R4
  records the blanch as a step with evidence, not as "because the bake
  requirement failed"); (2) **several minimal mitigations kept as
  alternatives** (R5 keeps alternative sequences, but not derived from a
  violation); (3) **durations** in constraints (the reason K8's 90-min route
  is a false negative); (4) the **driver** of a substitution and the four
  drivers' disagreement. What Y402 lacks that Food-prep has: three-valued
  applicability, provenance, role requirements of assemblies, documented
  practice as the source of constraints.
- **E6.** Published: primary/secondary, three substitution levels, IC
  typology, drivers, minimal mitigation, minimal inconsistent subsets
  [Y402 §5-8]. Inferred: all K mappings; that this would fix K8's false
  negative (only if a duration constraint for rutabaga in a covered bake is
  written from evidence).
- **Verdict: adopt the concept** (primary vs secondary substitution, with
  each secondary change linked to the requirement whose violation it
  repairs, and more than one repair kept when several are minimal). Reason:
  it is exactly the step Food-prep's R4 performs informally and the K1/K8
  pair shows why the link matters. **Insufficient evidence** that the
  framework works on real recipes: nothing is evaluated [Y402].

### B. Recipe graphs with acceptability tuples; type and structural substitution (Y403, Y404)

- **E1.** Unit: a bipartite graph of comestibles and actions, typed;
  validity = every (input, action, output) triple is an acceptability tuple.
  Purpose: formal comparison, composition and substitution of procedures.
- **E2.** Demonstrated: definitions, an ASP implementation that finds least-
  cost secondary type substitutions (spaghetti to fusilli) and timing runs
  [Y404 §10]. Not shown: correctness of substitutions on any set of recipes.
- **E3 mapping [inf].**
  - K2: type substitution of the input node chickpea → dried pea; secondary
    substitutions relabel "soaked chickpea" → "soaked pea", "chickpea paste"
    → "pea paste" until every triple is an acceptability tuple. Whether
    (soaked pea, grind, pea paste) is acceptable is a lookup in the tuple
    set; K2-x adds a node "boiled soaked pea" whose triple (boiled soaked
    pea, grind, paste) is acceptable only if some documented recipe gives it.
    Acceptability tuples built "from established practice" [pub Y404 §5.1]
    is Food-prep's documented-practice rule.
  - K3: structural substitution replaces the subgraph "head → blanch whole
    head → detach leaves" by "head → detach leaves" (same frontier: leaves).
  - K4: structural substitution of the vessel subgraph; the filling node
    feeds two fill actions (onion and courgette) — a comestible with out-
    degree 2 is allowed, so one filling for two vessels is representable,
    which R3 cannot (several containers per assembly).
  - K5: type substitution plus a structural one inserting a peel action;
    the discarded stem of a head used for another dish is a by-product node
    [pub Y404 §4 by-products] reused in a second recipe (composition, §7).
  - K6: (curly kale leaf, wrap, roll) absent from the tuples → not acceptable.
    Absent means unacceptable: no unknown.
  - K1/K8: (raw rutabaga slices, bake 60 min, tender layer) absent → K8
    rejected; (raw rutabaga slices, bake covered 90 min, tender layer)
    present if documented (G7, G8) → the long-bake route is accepted, because
    the action type can carry a duration [pub Y404 §3.1]. But a bake is one
    action node; per-layer outcomes need per-layer output nodes from one
    action (allowed: an action may have several outputs).
- **E4 table.**

| aspect | K2 | K3/K6 | K4 | K5 | K1/K8 |
| --- | --- | --- | --- | --- | --- |
| a. components and joins | preserved: subgraphs and composition | extend: join is an action, no roles | preserved for sharing a filling; extend for roles | preserved | preserved |
| b. intermediate states | preserved: every intermediate is a typed node | preserved | preserved | preserved | extend: no readiness/doneness distinction |
| c. member after assembly | extend: one action with several outputs | extend | extend | n/a | extend |
| d. why a stage exists | cannot: no objective on actions | cannot | cannot | cannot | cannot: a blanch is just a node |
| e. alternative routes | extend: different graphs, each separately valid | extend | extend | extend | preserved structurally (two graphs), no evidence link |
| f. substitution consequences | preserved: secondary type / structural substitution | preserved | preserved | preserved | preserved |
| g. start from a state on hand | preserved: an intermediate can be an input node | preserved | preserved | preserved | preserved |
| h. provenance | extend: tuples "from established practice" but no citation field | extend | extend | extend | extend |
| i. unknown vs false | cannot: missing tuple = unacceptable | cannot | cannot | cannot | cannot |
| j. readable for a cook | preserved: graphs are drawable | preserved | preserved | preserved | preserved |

- **E5.** Acceptability tuples ≈ R1's applicability of an operation to a
  material producing a new state, but R1 is three-valued, has reasons and
  conditions, and computes outputs from properties instead of listing every
  triple; Y404's by-products ≈ R1 fractions and R3 recombination; structural
  substitution ≈ R4's replaced specs.
- **E6.** Published: graph, tuples, type/structural substitution, by-products,
  ASP search, timing [Y403, Y404]. Inferred: mappings; that one filling for
  two vessels fits (out-degree > 1 is allowed by Def. 1 but not discussed
  for cooking).
- **Verdict: already equivalent** for acceptability tuples (R1 is the richer
  form); **extend** for one detail: a shared intermediate feeding several
  joins (K4's one filling, two vessels) is ordinary in a graph and missing in
  R3.

### C. Ontology design pattern for substitution (Y401)

- **E1.** Unit: a substitution specification attached to a recipe
  specification, with objective, conditions (technological / dietary /
  cultural), and ingredient-set and instruction-set transformations.
  Purpose: shared vocabulary for systems and knowledge graphs.
- **E2.** Competency questions and one example; no population, no
  evaluation [Y401 §4-5].
- **E3 mapping [inf].** K2: a recipe-specific substitution, objective
  "local cheap staple", technological condition "binds without additive
  when raw-soaked"; *substitute* (process kept) in Y401's sense. K1: the
  blanched version is a substitution with an instruction-set transformation
  (add blanch); K8 cannot be stated as a failure: the pattern records
  suggestions, not outcomes. K4: an instruction-set transformation (hollow
  → lift layers). K6: nothing records "rejected" or "no documented practice".
  None of the process consequences are derived; they are written.
- **E4 table** (one column: the pattern does the same thing for every case).

| aspect | all relevant cases |
| --- | --- |
| a. components and joins | cannot: ingredient set + instruction set, no structure between them |
| b. intermediate states | cannot |
| c. member after assembly | cannot |
| d. why a stage exists | extend: objective is on the substitution, not on steps |
| e. alternative routes | extend: several substitutions per recipe, unrelated to each other |
| f. substitution consequences | extend: instruction-set transformation is recorded, not derived or checked |
| g. start from a state on hand | cannot |
| h. provenance | extend: OBO alignment, no source per claim shown |
| i. unknown vs false | cannot (OWL is open-world, but the pattern defines no status for a substitution) |
| j. readable for a cook | extend: objective and conditions are readable labels |

- **E5.** R4 transfer records `question`, `proposed`, `evidence_says`,
  `verdict`; it has no field for the **objective/driver** typed as Y401's
  conditions (technological, dietary, cultural) and does not distinguish
  substitute from **analog**.
- **E6.** All capabilities published as design only [Y401]; mappings inferred.
- **Verdict: extend.** Take two concepts: the substitution's objective with
  typed conditions, and the substitute/analog distinction (whether the
  process is kept). Nothing else is new against R4.

### D. Characteristic-action similarity within a dish group (Y405)

- **E1.** Unit: a material's vector of characteristic cooking actions inside
  a recipe group (dish type). Purpose: find replaceable materials to adapt
  recipe texts.
- **E2.** 391 recipes, 92 candidates, one expert judge on 40 recipes, three
  outcome categories + N/A; two dishes cooked [Y405 §3]. Small, one judge,
  Japanese home recipes.
- **E3 mapping [inf].** K1: the paper's own "gratin" group found potato ⇝
  cauliflower and tofu judged appropriate [pub Y405 Table 5]; rutabaga
  would pass if its action vector in gratins (slice, bake) matched potato's;
  the blanch would be invisible, because characteristic actions are those
  above 75 % in the group, so K8 is a false positive unless the judge marks
  category 2. K2: chickpea and pea share (soak, grind, shape, fry) in a
  falafel group → replaceable; P15 dryness invisible. K3/K6: napa and kale
  have similar action vectors in a "roll" group if documented; curly kale
  absent from the group → never proposed (absence ≠ rejection). K4: onion's
  actions as a vessel (blanch, scoop, fill, bake) — only if stuffed onions are
  in the same dish group. K5: broccoli stem has no action profile as a
  patty material unless recipes exist; peeling would appear as a
  characteristic action.
- **E4 table.**

| aspect | all relevant cases |
| --- | --- |
| a. components and joins | cannot: per-material action bags, no structure |
| b. intermediate states | cannot; the paper itself warns about pre-cooked materials (steamed vs uncooked rice) |
| c. member after assembly | cannot |
| d. why a stage exists | cannot |
| e. alternative routes | cannot |
| f. substitution consequences | extend: evaluation category 2 marks "procedure must change" but the method does not say what |
| g. start from a state on hand | cannot |
| h. provenance | extend: a candidate traces to the recipes of its group |
| i. unknown vs false | extend: the evaluation has an N/A category; the method has none |
| j. readable for a cook | extend: pairs per dish type |

- **E5.** The premise (same characteristic actions within a dish type →
  substitutable) is what R1 applicability makes explicit per operation;
  R4's re-validation of the op chain is the stricter, explained version.
- **E6.** Published: method, categories, counts, rice failure [Y405].
  Inferred: K mappings.
- **Verdict: already equivalent** (R1 + R4 do this with reasons). Its
  evaluation scheme is the most useful thing here: it is the only published
  outcome scale that separates "works as is", "works with a procedure
  change", "impossible" and "cannot judge", and it matches four of the
  user's draft categories (see Q3).

### E. Context-scoped adaptation knowledge in CBR (Taaable, Y413)

- **E1.** Unit: a substitution between conjunctions of properties, scoped by
  context (dish type) in its left side; learned from differences between
  recipes; validated by a user in the problem-solving context.
- **E2.** Prototype on 862 recipes, use cases only [Y413 §5].
- **E3 mapping [inf].** Every Food-prep transfer is a scoped substitution
  "falafel ∧ chickpea ⇝ falafel ∧ pea"; "gratin ∧ potato ⇝ gratin ∧ potato ∧
  rutabaga". Learned from variations between documented recipes of the same
  dish = R4's search for documented transfers. Y413's two failures are the
  same failures R3/R4 were built to catch: removing oil that sautés (a
  component's role in a step), raw leek replacing cooked-as-garnish onion
  (state and role).
- **E4.** Not tabulated separately: the representation of preparation is
  outside this paper (textual preparation adaptation in Taaable is in the
  CBR area, Y300s). On aspects f, h, i: f extend (ingredients only), h extend
  (the source recipe pair is known), i extend (an unvalidated substitution
  is a candidate, not knowledge).
- **E5.** R4 transfer is scoped to one base route (equivalent). Validation
  "by an expert in context" ≈ R4's evidence plus kitchen test.
- **E6.** Published: representation, mining, validation, failures [Y413].
- **Verdict: already equivalent** (scope by dish/route; validation in
  context).

### F. Statistical and learned substitute finders (Y406, Y407, Y408, Y409, Y410, Y411, Y420)

Grouped because they share the unit: a (source, target) ingredient pair,
optionally with context = co-occurring ingredients (or meal), ranked by a
score.

- **E1.** Purpose: recommend candidate substitutes (healthier, available,
  allowed). Context, when used, is the ingredient set (Y410), the recipe
  context as other ingredients (Y408), the meal (Y407), the dish group
  (Y405 above); no work in this group uses the process except Y411, which
  adds actions as graph nodes without effect on ranking metrics.
- **E2.** Demonstrated: rankings against ground truth mined from review or
  comment patterns (Y406, Y408, Y410), curated guides (Y408), crowd ratings
  (Y407), author labels (Y409), four experts (Y411). See Q3 for how weak.
- **E3 mapping [inf].**
  - K1/K8: DIISH's ground truth already lists rutabaga for potato, context-
    free [pub Y408 Table 6]; any of these methods would propose raw rutabaga
    in a gratin with no process change: K8 is the archetypal false positive.
  - K2: chickpea → pea appears only if reviewers wrote it; the raw-soaked vs
    cooked distinction is erased by normalisation (states stripped [pub Y406
    §3.1]; "diced tomatoes" = tomato [pub Y408 §2.3]); K2-x is invisible.
  - K3/K6: napa/cabbage/kale are near neighbours in any embedding; curly vs
    flat kale is one vocabulary item or two depending on normalisation;
    leaf size and the wrapper role are absent. K6 cannot be "not worth it":
    a candidate is ranked, never rejected with a reason.
  - K4: courgette ⇝ onion would be scored as ingredients in a stuffed dish;
    the vessel role is invisible.
  - K5: "broccoli stem" is normalised to broccoli (FlavorGraph vocabulary
    merges variants [pub Y410 §4]); the by-product reuse disappears.
- **E4 table.**

| aspect | all relevant cases |
| --- | --- |
| a. components and joins | cannot |
| b. intermediate states | cannot: states are normalised away |
| c. member after assembly | cannot |
| d. why a stage exists | cannot |
| e. alternative routes | cannot |
| f. substitution consequences | cannot (Y411 asks experts whether a major process change is needed, as a label, not a model) |
| g. start from a state on hand | cannot |
| h. provenance | extend: review-mined pairs trace to reviews (Y406, Y408, Y410); learned scores do not |
| i. unknown vs false | cannot: an unseen valid pair counts as wrong in every metric |
| j. readable for a cook | extend: a ranked list of names |

- **E5.** Nothing in R1-R5 corresponds; the closest use for Food-prep is as
  a **source of candidates** to look up in documented practice (as R4 did by
  hand).
- **E6.** Published: as listed per source. Inferred: K mappings.
- **Verdict: not suited** (built to rank candidate names, not to say whether
  a process still works).

### G. Generative recipe editing (Y412)

- **E1.** Unit: a whole recipe (ingredient list + step text) rewritten to a
  dietary constraint.
- **E2.** 83 K pairs; crowd judges; seven cooks, 21 recipes cooked [Y412 §6].
- **E3 [inf].** K1 would be "a gratin without potato" only if the constraint
  asked for it; regenerated steps may or may not contain a blanch; nothing
  checks. K2-x would be whatever the language model writes.
- **E4.** All aspects *cannot* except j (*preserved*: readable recipe text)
  and f (*extend*: steps change, unchecked).
- **E5.** No counterpart; its cooking study is the only kitchen evidence in
  this area, and its main complaint (dish no longer resembles the base
  name) is a dish-identity failure Food-prep's verdicts do not name.
- **Verdict: not suited.**

### H. Food-science functional-role substitution (egg replacers, binders, flour replacements)

- No source read in full: every open copy found was blocked (see failed
  pages). Search snippets are not evidence.
- **Verdict: insufficient evidence** (from this area). Y402's role function
  (thicken, bind, aerate... per recipe type) [pub Y402 §4.1] and Y414's
  "egg in cake vs egg as glaze" [pub Y414 §5.3.3] are the only role-based
  statements read.

## Answers to Q1-Q6 from this area

**Q3 (in depth). When is an ingredient genuinely substitutable, and how are
inconsistencies found and resolved?**

1. *What substitutability depends on, in the literature read.*
   - Identity / category: taxonomy distance (Y408 FoodOn; Y405 weights
     same-kind materials from a food composition table; Y413 ontology
     generalisation).
   - Functional role in the dish type: a role function per recipe type
     (Y402 §4.1); recipe-relative distance (aquafaba for egg in baking, not
     in an omelette, Y403 §7); egg in cake vs glaze (Y414 §5.3.3); oil that
     sautés cannot be dropped (Y413 §3.3).
   - Current state of the material: Y405's only impossible case was steamed
     rice for macaroni (uncooked rice would work); Y402 food terms carry
     qualities and intermediates can be substituted (Ex. 38); SHARE's judges
     asked whether ingredients were raw or pre-processed (Y412 §6). The
     data-driven methods remove state (Y406 §3.1, Y408 §2.3).
   - Processing requirements: characteristic actions (Y405); action-duration
     and preparation constraints (Y402 §8.1); acceptability tuples (Y403-4).
   - Interaction with other components: equipment / oven constraints when
     items share an oven at different temperatures (Y402 §8.1, Ex. 52); a
     removed ingredient that other steps use (Y413); co-occurring
     ingredients as context (Y407, Y408, Y410).
   - The driver of the substitution changes what counts as acceptable (Y402
     §7: similarity to item vs to dish vs minimal change vs a property).
   - Dish identity: a constraint that a named dish keeps its defining
     ingredient (Y402 Ex. 43); cooks' main complaint about edited recipes
     (Y412 §6).
   - Direction: substitution tuples are directional and recipe-bound (Y410
     §2; Y406's network is directed).
2. *How inconsistencies are found and resolved.* Only Y402-Y404 have a
   mechanism: a primary substitution, then integrity constraints or
   acceptability tuples fail, minimal inconsistent subsets point to the
   clause or node to change, and minimal secondary substitutions repair it
   (Y402 §6, §8; Y403 Defs. 13-16; Y404 §10 implements the search). Y402
   proves a repair need not exist. None of these was tested on real
   recipes. Y412 regenerates steps and checks nothing. Every other approach
   leaves the process to the cook.
3. *Draft categories against the literature.*

| user's draft | Y405 (outcome scale) | Y402 (mechanism) | Y401 / Y411 / others | comment |
| --- | --- | --- | --- | --- |
| direct | 1: materials and procedure fine | empty mitigation (Prop. 10) | Y401 "substitute" (process kept) | equivalent everywhere |
| needs parameter changes | part of 2 | term substitution on an action's parameter (duration: fusilli 12 min) | Y406 increase/decrease quantity | Y402 makes this a distinct level; Y405 lumps it with 2 |
| needs additional/different operations | part of 2 | condition and clause substitution (add peel, change slice to grate) | Y401 instruction-set transformation; Y411 "major process modification" (yes/no, kappa 0.58) | the literature does not separate "different op" from "added op" |
| needs structural/assembly changes | — | clause substitution; Y403-4 structural (subgraph) substitution | Y401 "analog" | no work has assembly roles (container, wrapper); structure = subgraph |
| affects other components | — | equipment and quantity constraints across items (one oven, shared quantity) | Y413 oil used in another step | present in Y402 as a constraint type, never as an outcome category |
| incompatible | 3: impossible | no mitigation exists (Prop. 11) | — | equivalent |
| insufficient evidence | N/A: hard to judge | none (closed world) | Y411 experts declined the nutrition question | only human-judged scales have it |

   Categories in the literature that the draft lacks:
   - **omission** as a substitution (Y401 empty substitution; Y406 omit);
   - **quantity / ratio change** without a different ingredient (Y406;
     Y401 CQ9);
   - **dish identity changes** ("analog", renamed dish; Y401, Y402 Ex. 43,
     Y412's main complaint);
   - **fits but changes quality** (taste) as separate from feasibility
     (Y411: fit and major taste change weakly negatively correlated; Y402
     separates "consistent" from "similar dish");
   - **one-to-many** substitutions (several ingredients for one; Y408 §4.2
     future work; K6's overlapped leaves);
   - **the driver** of the substitution, which decides between candidates
     (Y402 §7).
   What the draft has that the literature lacks: "affects other components"
   and "structural/assembly" as named **outcomes** (Y402 has the mechanisms
   but no outcome labels), and **insufficient evidence** in any automatic
   method.
4. *Evaluation and ground truth, and how weak.*
   - Formal works: none (Y401, Y402, Y403); Y404 measures CPU time only.
   - Review/comment patterns (Y406, Y408, Y410): unvalidated, one-to-one,
     tied to one recipe, directional; a valid substitute nobody wrote is
     scored wrong; process changes are never part of the label.
   - Curated substitution guides (Y408): context-free; potato ⇝ rutabaga
     listed with no condition.
   - Author labelling and self-extended ground truth (Y409: two authors;
     the ground truth grew with the methods' own correct predictions).
   - One expert (Y405), three crowd workers per pair with cultural mismatch
     (Y407), four company experts (Y411; process question kappa 0.58).
   - Cooking: Y405 cooked two pizza toasts; Y412 had seven cooks cook 21
     recipes without a side-by-side with the base recipe. **No work found
     compares a substituted dish with the original in a kitchen**, which is
     what R4's kitchen tests do.
   - Headline numbers are low where the task is in-context ranking (GISMo
     Hit@1 20.56; LLM Hit@1 22.04, Y420 abstract), and the metric itself
     cannot tell a wrong substitute from an unrecorded good one.

**Q5. Reuse of preparations; are equivalent states interchangeable when
their histories differ?** Two findings only. (1) Pre-cooked materials are
the one documented failure in Y405 (steamed vs uncooked rice), and SHARE's
judges could not tell raw from pre-processed ingredients (Y412): a material's
state matters to substitutability and is usually not recorded. (2) Y402
represents intermediates as onhand items with qualities, so a cook can start
from an intermediate (assumptions), and substitution of intermediates is
published (Ex. 38); Y404 adds by-products for reuse across recipes. No source
read asks whether two materials in the same state with different histories
(e.g. K2-x: soaked vs quick-boiled pulse) are interchangeable; Y402 could
express the difference only by putting the history into the food term.

**Q1, Q2, Q4, Q6.** Q4: Y402's several minimal mitigations and Y403-4's
alternative subgraphs are the only representations of alternative routes in
this area; neither attaches evidence. Q1, Q2, Q6: nothing found beyond what
the process-representation areas cover (Y402 has durations and equipment
constraints, Y404 has graphs and by-products; both are reported for those
areas to weigh).

## Open questions this area leaves

1. Should R4 record each added or changed step as the **repair of a named
   requirement violation** (Y402's secondary substitution), so a transfer
   says "blanch because `cooks_slowly` in a shared bake", and so several
   repairs (blanch vs 90-min covered bake) are kept as alternatives with
   their own evidence? This would also make K1-x visibly a combination of
   two repairs.
2. Durations: Y402 and Y404 put time into constraints; K8's false negative
   is a missing duration. Is a duration on a requirement (not a simulator)
   within Food-prep's rules?
3. Should a transfer carry its **driver** (similarity to the ingredient,
   to the dish, minimal change, or a property such as cost or local supply)
   and Y401's **substitute vs analog** flag?
4. Should "dish identity changes" and "fits but quality changes" become
   outcome categories next to the user's draft?
5. Not read and possibly important: Taaable's textual preparation
   adaptation and FCA substitution (Gaillard et al. 2015), Boscarino et al.
   2014 (context of substitution rules), the Japanese process-similarity
   line (Mizuno et al.; FIT2013), and any food-science source on functional
   roles of binders and egg or flour replacers. The food-science gap matters
   most for K2 (binding without additive) and was not closed here.
6. No source tests substitutions against the original dish in a kitchen.
   Food-prep's kitchen tests are, as far as this search reached, the
   stronger form of ground truth; whether a published protocol for such
   tests exists in sensory science was not searched.
