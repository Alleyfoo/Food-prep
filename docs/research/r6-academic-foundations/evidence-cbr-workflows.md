# Evidence: case-based reasoning and recipe workflow adaptation (process-oriented CBR)

- **Date read:** 2026-11-25.
- **Method:** web search, then the full text where a free copy existed: CEUR-WS, the Trier group's own repository (wi2.uni-trier.de), IJCAI proceedings, arXiv, the IIETA publisher copy, DFKI. WebFetch returned most PDFs as binary. Those files were saved locally and their text extracted with pypdf, and that extracted text was read. "Repository PDF" below means this route.
- **Search languages:** English and German. No French query was sent; the French journal article (Y311) was found through an English query. No Italian or Spanish CBR-cooking work came up.
- **Blocked:**
  - ResearchGate (403);
  - HAL (Anubis bot wall);
  - core.ac.uk (403, two papers);
  - DFKI's older CookIIS 2009 PDF and the Kumar 2022 paper (403);
  - the Uni Trier EVER project summary (403);
  - the Semantic Scholar API (429), so forward citations come from the papers read, not from an index.
- **Ids:** Y300-Y313.

## Sources

### Y300 — https://ceur-ws.org/Vol-1520/paper23.pdf
- **Citation:** Müller, G., Bergmann, R. (2015). CookingCAKE: A Framework for the adaptation of cooking recipes represented as workflows. In: Kendall-Morwick, J. (ed.), Workshop Proceedings of ICCBR 2015 (Computer Cooking Contest), Frankfurt. CEUR-WS vol. 1520, pp. 221-232. Pages and editor are confirmed by Y304's reference list. DOI: none.
- **Version read:** CEUR-WS PDF, full text, 12 pages. The ResearchGate copy named in the task returned 403; the CEUR copy replaced it.
- **Type:** primary research / system description (Computer Cooking Contest entry).
- **E1, representation:**
  - A recipe is a block-oriented workflow (§2):
    - tasks are preparation steps; data items are ingredients;
    - control-flow blocks are sequence, AND, XOR and LOOP, nested but never interleaved (one start node, one end node);
    - data-flow edges link tasks and data items.
  - Tasks and data items are annotated from two taxonomies, one of preparation steps and one of ingredients (§2.1).
  - Similarity is that of the least common ancestor. A general query term matches any term below it with similarity 1.
  - The query is POQL: desired and undesired ingredients or steps (§2.2). POQL is also said to capture time restrictions and "do not bake vegetables", but this paper does not show either.
- **E1, purpose:** adapt a retrieved recipe to a query.
- **Three adaptation methods are integrated (§3-4):**
  - generalisation and specialisation (Y303);
  - compositional adaptation by workflow streams (Y302);
  - transformational adaptation by learned operators: a deletion streamlet plus an insertion streamlet, learned from pairs of cases. In the Fig. 5 example, mayonnaise is replaced by tomatoes, and the "combine" task must become "chop" at the same time.
- **Pipeline:**
  1. Generalise the whole case base.
  2. Learn streams and operators from the generalised case base.
  3. Retrieve.
  4. Adapt: streams first, then operators.
  5. Specialise.
- **E2, demonstrated:**
  - a case base of 61 sandwich workflows, modelled by hand from WikiTaaable and other web recipes;
  - WikiTaaable's ontology reduced to single inheritance, with similarity values annotated by hand;
  - a running web demo;
  - output as text (the block structure flattened into one sequence), a process view, and an XML file recording the source case and the ingredients added and removed (§5).
- **E2, counts reported:** more than 9·10^21 recipes obtainable by generalisation and specialisation; 197 streams; 7,870 operators (1,306 replace, 3,903 insert, 2,661 delete).
- **E2, not evaluated in this paper:** the quality of any adapted recipe.
- **Stated behaviour:** the system "does not execute any adaptations if no adaptation knowledge is present" (§5). It may then return a recipe that does not fully meet the query.

### Y301 — https://www.wi2.uni-trier.de/shared/publications/2014_MuellerBergmannCCC.pdf
- **Citation:** Müller, G., Bergmann, R. (2014). Compositional Adaptation of Cooking Recipes using Workflow Streams. Computer Cooking Contest, ICCBR 2014 workshop. Venue as listed on Y313; no page numbers or DOI verified.
- **Version read:** repository PDF, full text, 8 pages.
- **Type:** primary research (position paper; "first steps").
- **E1, partial workflow (§2.1):**
  - the subgraph for a subset of tasks, with every data node linked to those tasks;
  - only the control blocks that still contain tasks are kept;
  - extra control-flow edges preserve the original execution order.
- **E1, ontology annotations (claimed):** skills, tools, time on steps; dietary information on ingredients.
- **E1, streams (§3):**
  - A stream is a set of transitively data-flow-connected tasks, cut at **creator tasks** (tasks that make a new ingredient).
  - Each task belongs to exactly one stream.
  - In the pizza example, the streams are dough, sauce, pizza and toppings.
  - The **anchors** of a stream are the data nodes it shares with another stream of the same workflow (sauce, dough, pizza).
- **E1, change request (§4.1):**
  - Hand-made, or derived from the gap between the query and the retrieved case.
  - It may name tools that must or must not be used, the number of cooks, and their skill.
- **E1, replacing a stream (§4.2):** the old stream is removed and the new one inserted after the last control element of the old one.
- **E1, ideas proposed but not implemented (§4.3):**
  - **Stream chains.** Inserting a stream may require another stream that makes its input (a tomato-sauce stream needs a sieved-tomatoes stream). Chaining stops when the needed input is already in the workflow, or when no stream produces it (it is then a raw ingredient).
  - **Removing superfluous streams** whose product is no longer used.
  - **Parallel streams** when two cooks are available.
- **E2:** no evaluation. The authors report "first satisfactory results" only for streams with identical anchors, and refer to Y302. Stated limits: similarly structured workflows must exist, and the workflows must be block-oriented.

### Y302 — https://www.wi2.uni-trier.de/shared/publications/2014_MuellerBergmannICCBR.pdf
- **Citation:** Müller, G., Bergmann, R. (2014). Workflow Streams: A Means for Compositional Adaptation in Process-Oriented CBR. In: Lamontagne, L., Plaza, E. (eds.), ICCBR 2014, Cork. LNCS 8765, pp. 315-329, Springer. Volume and pages come from the reference lists of Y303 and Y306. DOI not verified. Y313 notes a best PhD student paper award.
- **Also read:** a one-page LWA 2014 resubmission notice (abstract only, CEUR-WS vol. 1226, https://ceur-ws.org/Vol-1226/paper41.pdf).
- **Version read:** repository PDF, full text, 15 pages.
- **Type:** primary research.
- **E1, formal definitions:**
  - **Workflow (Def. 1):** nodes are data, task and control nodes. Control-flow edges link sequence nodes; data-flow edges run data to task or task to data. Control-flow edges give a strict partial order.
  - **Block structure (Def. 2):** only the control flow is restricted by blocks; the data flow is not.
  - **Creator task (eq. 1):** a task that produces a data node it does not consume. A task that both consumes and produces the same node (for example "grate" on cheese) is not a creator task: the data node keeps its name through processing.
  - **Data-flow connected (eq. 2):** t1 runs before t2 and t2 consumes a node t1 produces.
  - **Streams (Def. 4):** a partition of the tasks.
  - **Anchors (Def. 5):** a stream's data nodes that tasks in other streams produce or consume.
  - **Substitutability:** two streams are substitutable if their anchor sets are identical. This guarantees that no data node is left produced but never consumed, or consumed but never produced.
- **E1, change request:** an ADD list and a DELETE list. They may use general terms ("DELETE meat" makes a dish vegetarian).
- **E1, adaptation:**
  1. For each stream, find candidates with identical anchors.
  2. Keep those with no DELETE node and the most ADD nodes.
  3. Take the most similar of those.
- **E2, set-up:**
  - 240 pizza workflows produced by a generator built on the Fast Downward planner: 17 ingredients, 8 task types, AND blocks but no XOR or LOOP;
  - 230 in the case base, 10 as tests; 920 streams.
- **E2, H1 (change requests are met):** met in 10 of 10. The authors call this unsurprising, since all the workflows are similar pizzas.
- **E2, H2 (quality), a blinded rating:**
  - 5 experts, 10 pairs of test and adapted workflows;
  - 5 items on a 5-point scale: intelligibility, correctness of order and data flow, process optimisation, plausibility, overall quality.
  - Aggregated quality: the adapted workflow was at least as good in 22 of 50 ratings (44 %).
  - Overall quality alone: 66 % (Table 1).
  - The mean difference was 0.27 per item in favour of the originals (Table 2).
- **E2, what was not done:** nothing was cooked, and the workflows are planner output, not real recipes.
- **E2, claim:** adapted workflows are consistent and semantically correct by construction, which the paper checks rather than evaluates.

### Y303 — http://www.wi2.uni-trier.de/publications/2015_MuellerBergmannFLAIRS.pdf
- **Citation:** Müller, G., Bergmann, R. (2015). Generalization of Workflows in Process-Oriented Case-Based Reasoning. 28th International FLAIRS Conference, Hollywood (Florida), AAAI Press, pp. 391-396. Pages come from Y306's reference list. One bibliographic record lists Russell and Eberle as co-authors; others list them as editors (not verified). DOI: none found.
- **Version read:** repository "technical report" version of the accepted paper, full text, 14 pages.
- **Type:** primary research.
- **E1, representation:**
  - A workflow is a semantically labelled graph (W = N, E, S, T), after Bergmann and Gil.
  - Two taxonomies are used, one of tasks and one of ingredients. Leaves are concrete; inner nodes stand for the set of leaves below them.
  - Similarity uses an admissible mapping (type-preserving, partial, injective) and takes the best mapping. The measure is asymmetric: it is 1 when the query is a subgraph of the case.
- **E1, generalisation (Def. 4):**
  - W* generalises W only if a **graph isomorphism** exists and every node of W* is equal to or more general than its counterpart.
  - Algorithm 1: a node's term is raised one level when the parent's similarity value plus the share of its children seen in similar cases (similarity of at least Δ) reaches Δψ.
  - The original leaf term is kept in **OrigSpec(n)**.
  - Algorithm 2 repeats this until no case changes, keeping only the most general cases.
- **E1, specialisation (Algorithm 3):** take the query term if it is more specific; otherwise restore OrigSpec.
- **E2, data:** 60 pasta workflows modelled by hand from studentrecipes.com (average 25 nodes and 64 edges; 162 ingredients, 67 tasks; with AND, XOR and LOOP). 10 are queries and 50 the case base. A second case base of 70 adds 20 generated variants.
- **E2, H1 (quality), a blinded comparison:**
  - 5 experts, 10 pairs, a scale from -3 to +3;
  - correctness of preparation was worse after adaptation in 24 % of ratings, culinary quality in 46 %, aggregated quality in 44 %;
  - paired t-test p = 0.11 (Table 1).
- **E2, H2 (retrieval):** the case base shrank about 17 % and retrieval time about 13 % on the 70-case base. Coverage rose to about 6·10^10 and 2·10^13 specific workflows (Table 2).
- **E2, what was not done:** nothing was cooked.
- **Named limit:** abstraction (fewer, coarser tasks such as "prepare sauce") is a different operation and is left to future work.

### Y304 — https://ceur-ws.org/Vol-1815/paper29.pdf
- **Citation:** Müller, G. (2016). Workflow Modelling Assistance by Means of Process-oriented Case-based Reasoning. Proceedings of the ICCBR 2016 Workshops, Atlanta, pp. 272-276. CEUR volume number taken from the URL. DOI: none.
- **Version read:** CEUR-WS PDF, full text, 5 pages.
- **Type:** doctoral-consortium summary.
- **E1:** the whole Trier pipeline in one figure: generalise the case base, learn streams and operators, retrieve with POQL, adapt in chains W → W1 → ... → Wn as a search, then specialise.
- **E1, two further strands:**
  - adaptability-aware retrieval: the best match is not necessarily the most adaptable case;
  - workflow completion, which infers information missing from badly modelled cases.
- **E2:** no new results. Plans for an overall blind evaluation and for interactive adaptation.
- **Points to:** the dissertation, Müller 2018 (not read, see the failed table).

### Y305 — http://www.wi2.uni-trier.de/publications/2010_MinorEtalICCBR.pdf
- **Citation:** Minor, M., Bergmann, R., Görg, S., Walter, K. (2010). Towards Case-Based Adaptation of Workflows. ICCBR 2010, LNAI 6176, pp. 421-435, Springer. Volume and pages confirmed by Y300 and Y306. DOI not verified.
- **Version read:** repository PDF, full text, 15 pages.
- **Type:** primary research. The domain is university office workflows, not cooking.
- **E1, the adaptation case:** a stored adaptation episode made of:
  - the original workflow;
  - the change request;
  - the adapted workflow;
  - add and delete lists of chains. Each chain has a **pre anchor** (the element after which the change starts) and a **post anchor** (the first element no longer affected).
- **E1, reuse:**
  1. Map the anchors into the new workflow, by one of four methods (PRAM, POAM, CAM, MAM).
  2. Apply additions where an anchor was mapped.
  3. Apply deletions only when every element is matched above a threshold, inside the same control structure.
- **E2:**
  - 19 adaptation cases and 9 test problems, elicited from secretaries in interviews.
  - Experiment 1: only CAM and MAM rebuilt all 19 cases.
  - Experiment 2: the best adaptation case for each test problem was chosen by hand, and CAM and MAM did best.
  - The authors say the set is too small for statistics.

### Y306 — https://www.wi2.uni-trier.de/shared/publications/2024_ICCBR_RuleBasedAdaptation_MalburgEtAl.pdf
- **Citation:** Malburg, L., Hotz, M., Bergmann, R. (2024). Improving Complex Adaptations in Process-Oriented Case-Based Reasoning by Applying Rule-Based Adaptation. ICCBR 2024, LNCS 14775, pp. 50-66, Springer. DOI 10.1007/978-3-031-63646-2_4. DOI as listed on Y313.
- **Version read:** repository PDF (author version), full text, 17 pages.
- **Type:** primary research, with code at gitlab.rlp.net/procake (link not followed).
- **E1, representation (NEST graphs, §2.1):**
  - semantic descriptions on nodes and edges;
  - data nodes carry name, amount and unit;
  - data-flow edges state what a task consumes and what results.
- **E1, operators restated (§2.2), after Müller 2018 and the 2015 operators paper:**
  - A **streamlet** is built around a **head data node**: it takes the tasks directly connected to that node, and its **anchor task** is the task that only consumes the head node.
  - Applying a delete streamlet removes the head node and every "unproductive" task left with no data edges.
  - Insertion requires similar anchor tasks that produce the same output.
  - Operators are learned from pairs of workflows in the case base.
- **E1, the new method:** the same knowledge encoded as Drools rules, a precondition plus a conclusion.
- **E2, set-up:** leave-one-out over 40 cooking workflows (about 21 nodes and 56 edges each). The operator repositories average 2,623 operators.
- **E2, results:**
  - Every result was syntactically correct.
  - Rules improved semantic similarity to the query more than operators, especially with 20 % of the knowledge; differences significant at p < 0.05.
  - Rules took much more time.
- **E2, what was not measured:** culinary quality. The only outcome is similarity to the query.

### Y307 — https://ijcai.org/proceedings/2018/762.md
- **Citation:** Zeyen, C., Müller, G., Bergmann, R. (2018). A Conversational Approach to Process-oriented Case-based Reasoning. IJCAI 2018, pp. 5404-5408. DOI not verified.
- **Version read:** the publisher's Markdown full text, read through the fetch tool's summariser. It was not quoted.
- **Type:** primary research.
- **E1, method:**
  - Workflow fragments ("features") and their generalised forms are mined offline.
  - They are ranked by how much they split the case base.
  - A dialogue asks about one feature at a time. A user who accepts a feature is asked about more specific and larger ones.
  - Answers build a POQL query: desired fragments go into the query workflow, undesired ones into restriction workflows.
- **E2:**
  - Cooking domain, 61 workflows.
  - A simulated user found the target in all 60 scenarios, with about 10.25 questions.
  - 8 users with 4 scenarios each: success 15/16 manual against 14/16 conversational; the required time was about halved.
- **Stated limits:** the dialogue starts from an empty query. Starting from a pre-modelled query is possible but was not investigated.

### Y308 — http://www.wi2.uni-trier.de/publications/2012_WWW_SchumacherEtal.pdf
- **Citation:** Schumacher, P., Minor, M., Walter, K., Bergmann, R. (2012). Extraction of Procedural Knowledge from the Web: A comparison of two workflow extraction approaches. WWW'12 Workshop, Lyon. Pages and DOI not verified.
- **Version read:** repository PDF, full text, 7 pages.
- **Type:** primary research.
- **E1, the extracted workflow:** tasks; input and output products; and **task facets**, such as "in a large skillet" and "until tender" attached to a sauté. Two extractors were compared: GATE term-based and SUNDANCE frame-based.
- **E2:**
  - About 25,000 recipes crawled; 40 extracted and scored by one expert.
  - Mean score 1.3 for the term-based and 6.0 for the frame-based extractor (scale of 0-10 implied by Fig. 7, not stated).
  - Dictionaries: 95 verbs and 2,781 ingredients.
- **Relevance:** this is where the Trier case bases come from (cited as [18] in Y300). A done-when condition survives here only as a free-text facet.

### Y309 — https://www.ijcai.org/Proceedings/13/Papers/445.pdf
- **Citation:** Dufour-Lussier, V., Le Ber, F., Lieber, J., Martin, L. (2013). Case Adaptation with Qualitative Algebras. IJCAI 2013, pp. 3002-3006. This is an extended abstract of the ICCBR 2012 best paper, "Adapting spatial and temporal cases", LNAI 7466, pp. 77-91 (not read). Authors' affiliations: LORIA Nancy, ICube Strasbourg, INRA Mirecourt.
- **Version read:** publisher PDF, full text, 5 pages.
- **Type:** primary research.
- **E1, representation:** a case is a qualitative constraint network (QCN) in INDU, which is Allen's interval relations combined with relations between durations. Cooking actions, ingredient states and durations are intervals.
- **E1, domain knowledge, for example:**
  - rice cooks 18 minutes;
  - the end of cooking x meets the interval "x cooked";
  - 18 minutes is shorter than 25.
- **E1, adaptation is revision:** "reduce adaptation to an inconsistency repair" (§3.2).
  - The substitution σ (mushroom ↝ carrot) is split into an abstraction (mushroom ↝ x) and a refinement (x ↝ carrot).
  - The source, abstracted, is revised by the target plus "x equals carrot".
  - The result is the set of scenarios at minimum distance from the source; distance is measured on a neighbourhood graph of relations.
  - The search is A*.
  - Pairs with no stated relation get the universal relation B, the "unspecified relation".
- **E2:**
  - **Example:** carrot risotto from mushroom risotto in Taaable. The mushrooms went in 2 minutes before the end. Carrots need 25 minutes and rice 18.
  - **Result:** the revision returns scenarios in which the vegetable interval changes from "finishes, shorter" to "finished-by, longer" than the rice. The carrot therefore has to start before the rice: the actions are reordered.
  - **Implementation and its limits:** a Perl prototype (revisor.loria.fr). The authors call it time-consuming and not yet integrated into Taaable.
  - **Evidence base:** one worked example, no dataset.

### Y310 — https://arxiv.org/pdf/1304.3879.pdf
- **Citation:** Dufour-Lussier, V., Le Ber, F., Lieber, J., Nauer, E. (2013). Automatic Case Acquisition From Texts for Process-Oriented Case-Based Reasoning. arXiv:1304.3879v1, a preprint submitted to Information Systems. Final publication not verified.
- **Version read:** arXiv v1, sections 1-5 read, 27 pages. Section 6 was skimmed.
- **Type:** primary research.
- **E1, formalisms compared (§2):**
  - **Workflows (UML activity diagrams):** cannot express durations ("reflux 3 hours") or fine temporal relations ("dry immediately after"). They also cannot say what "meanwhile" means: simmer-then-cook, cook-then-simmer and both at once are all valid readings.
  - **Allen and INDU:** can express those, but not disjunctions or loops.
  - **Conclusion:** process-oriented CBR needs both.
- **E1, "until al dente" (§4.3):** represented either as a task with an explicit end condition, or as a loop. In interval terms, "cook pasta" meets the state interval "pasta al dente".
- **E1, two adaptation methods summarised in §3:**
  - **Grafting (Taaable; Dufour-Lussier et al. 2010, not read).** When ingredient α is replaced by β, the sequence of actions applied to α is replaced by the most similar "typical use" of β found in another recipe. Example: a mango that is peeled, sliced and pitted, against figs.
  - **Revision-based adaptation (Y309).**
- **E1, intermediate products (§4.2):**
  - **Evolutive anaphora:** "sauce" refers to the result of the simmer.
  - Food components are treated as consumable resources. Each action removes components from the current set D_s and adds new ones.
  - I(F) gives a component's set of ingredients.
  - A "batter" is any available component that contains an ingredient from its target set.
  - Universal references ("dry ingredients") are resolved through the ontology.
- **E2, extraction against 15 hand-made workflows (Minor et al.):**
  - control flow: recall 75 %, precision 91 %;
  - data flow: recall 73 %, precision 99 %;
  - with the part-of-speech errors corrected: 89 % and 100 % (Tables 1-2).

### Y311 — https://iieta.org/download/file/fid/5259
- **Citation:** Gaillard, E., Lieber, J., Nauer, E. (2017). TAAABLE : un système de raisonnement à partir de cas qui adapte des recettes de cuisine. Revue d'intelligence artificielle 31(1-2), 207-235. DOI 10.3166/RIA.31.207-235. In French.
- **Version read:** publisher PDF (IIETA). Sections 1-4, 5.1-5.3 and 6-7 read, 30 pages.
- **Type:** system description and synthesis.
- **E1, ontology (§5.1):** six hierarchies: food, dish type, dish role, origin, diet, action.
- **E1, retrieval (§3):**
  - The query is generalised minimally, by a best-first search over generalisations "a ↝ b" and deletions of negated terms.
  - Cost of a ↝ b = K_τ · (N(b) − N(a)) / N(⊤), where N counts the recipes in a class. This is a risk proxy: the share of recipes in b that are not in a.
  - K_ingredient = 100 and K_origin = 1000, chosen by practice.
  - Generalising to "Food" costs infinity.
  - Costs are kept in the wiki and corrected by hand.
- **E1, adaptation:**
  - **Rules (§4.2):** substitutions C ∧ D ↝ C ∧ P under a context C, each with a cost. Example: in a green salad, vinegar ↝ lemon juice and salt.
  - **Specific rules:** rules taken from variants written in the recipe itself (butter ↝ margarine) have context = that recipe and **cost 0** (no risk).
  - **Quantities (§4.3):** revision-based, as linear constraints, preserving sugar, alcohol and volume.
  - **Preparation text (§4.4):** the "prototype" of an ingredient is one sequence of actions applied to it in one recipe. For mango ↝ fig, the closest fig prototype is chosen by formal concept analysis (recipe #53: cut, mix), and the matching text is grafted in.
- **E1, adaptation knowledge (§5.2):** a triple (context, ingredients to replace, replacing ingredients). It is specific when the context is one recipe, generic when it is a class of recipes. Each substitution is a WikiTaaable page.
- **E2, results:** Computer Cooking Contest results (§6):
  - 2nd in 2008 and 2009; 1st in 2010, plus the adaptation challenge;
  - the 2015 jury prize, and the public prizes for cocktails and sandwiches.
  - From 2014 the public cooked and tasted the outputs blind.
  - The paper itself contains no controlled evaluation.
- **Related systems (§6):**
  - CookIIS adapts the preparation text only by string substitution.
  - It credits "CookingCakeWF (Minor et al., 2010)" with workflow-based preparation adaptation. Y305 is not about cooking, so the attribution is not verified.

### Y312 — https://www-live.dfki.de/fileadmin/user_upload/import/5324_cookiis2010.pdf
- **Citation:** Newo, R., Bach, K., Hanft, A., Althoff, K.-D. (2010). On-Demand Recipe Processing based on CBR. CookIIS entry, Computer Cooking Contest 2010, University of Hildesheim. Venue and pages not verified; the text calls itself the CCC-2010 candidate paper.
- **Version read:** DFKI PDF, full text, 10 pages.
- **Type:** system description.
- **E1, representation:** one recipe per case. The ingredients are the problem; the title and the preparation text are the solution. The case base has 1,484 recipes. There is no process structure.
- **E1, adaptation:**
  - **Community-based:** in comments on about 70,000 recipes from a large cooking community, an OLD ingredient (in the recipe) and a NEW one (only in the comment) of the same class count as a substitution suggestion. This gives 2,967 suggestions for 410 ingredients.
  - **Model-based:** sibling and nephew concepts in the ingredient model.
  - **In-place:** the replacement is written into the ingredient list and the preparation text by string matching (plurals, synonyms, last word, class name). Original and replacement are both marked in HTML so the user can see what changed.
- **E1, revise step:** the user can exclude, with one click, an ingredient they lack or dislike.
- **E2:** the preprocessing effects are reported (§6). Adaptation quality is not evaluated.

### Y313 — https://procake.uni-trier.de/publications/
- **Citation:** ProCAKE publication list, University of Trier. Read in two parts, about 51 entries from 2005 to 2026.
- **Version read:** web page.
- **Type:** publication list (bibliographic only).
- **What it gives:** confirms the Trier titles and venues used here, and the later strands:
  - graph neural network retrieval (2023);
  - similarity explanation by visualisation (ICCBR 2023, 2026);
  - optimal sequences of adaptation rules (ICCBR 2025);
  - vision-based retrieval of semantic workflows (2026, accepted);
  - CBRkit, a Python toolkit (ICCBR 2024).
- **Not read beyond titles.** The German-language PhD by Schmalen (2011), *Adaptives Workflow Management*, is listed, but no full text is online.

## Failed pages and abstract-only

| URL or query | Why | Fallback tried |
| --- | --- | --- |
| researchgate.net/publication/281842938 (CookingCAKE) | 403 | CEUR-WS copy (Y300), read |
| hal.archives-ouvertes.fr/hal-00912767 (Taaable chapter, DOI 10.1007/978-3-642-38736-4_7) | Anubis bot wall | RIA 2017 French article (Y311), read instead; the chapter itself not read |
| core.ac.uk/download/49875754.pdf (Gaillard et al. 2012, generic adaptation-knowledge extraction) | 403 | none found; not read |
| core.ac.uk/download/49897464.pdf (Cordier, Gaillard, Nauer, adaptation knowledge acquisition) | 403 | none found; not read |
| scispace.com / typeset.io Taaable chapter PDF | redirect, then empty page | none |
| dfki.de/.../5315_CookIIS09.pdf | 403 | CookIIS 2010 (Y312), read |
| dfki.de/.../12583_2022_Kumar_FLAIRS.pdf | 403 | none; content unknown |
| uni-trier.de/.../EVER/EVERprojectSummary.pdf (DFG project EVER, Trier and Frankfurt, 2011-2017) | 403 | search snippet only, not used as evidence |
| api.semanticscholar.org paper search (two queries) | 429 | forward links taken from Y304, Y306, Y307, Y311, Y313 |
| Müller and Bergmann (2015), Learning and Applying Adaptation Operators in POCBR, ICCBR 2015, LNCS 9343, pp. 259-274, DOI 10.1007/978-3-319-24586-7_18 | no free copy found | **not read**; described second-hand in Y300 §3.3 and Y306 §2.2 |
| Müller and Bergmann (2015), POQL, LWA 2015, CEUR-WS 1458, pp. 247-255 | not fetched (a mirror URL only) | **not read**; described in Y300 §2.2 and Y307 |
| Müller and Bergmann (2016), Case completion of workflows for POCBR, ICCBR 2016, DOI 10.1007/978-3-319-47096-2_20 | no free copy found | **not read**; Y304 one sentence |
| Müller, G. (2018), Workflow Modeling Assistance by Case-based Reasoning, Springer Vieweg, DOI 10.1007/978-3-658-23559-8 (Trier dissertation) | paywall | **not read** |
| Bergmann and Gil (2014), Similarity assessment and efficient retrieval of semantic workflows, Inf. Syst. 40:115-127 | preprint listed on Y313, not fetched | **not read**; described in Y303 |
| Minor, Bergmann, Görg (2014), Case-based adaptation of workflows, Inf. Syst. 40:142-152 | publisher only | **not read** |
| Dufour-Lussier et al. (2010), Text adaptation using formal concept analysis, LNCS 6176, pp. 96-110 | not fetched | **not read**; grafting described in Y310 §3.1 and Y311 §4.4 |
| Hotz, Malburg, Bergmann (2025), optimal sequences of adaptation rules, ICCBR 2025 | listed on Y313, not fetched (time) | **not read** |
| German-language Trier dissertations on workflow modelling | none found online in German; the Müller dissertation is in English | gap |

## Searches

| Language | Query | Useful? |
| --- | --- | --- |
| en | CookingCAKE framework adaptation cooking recipes represented as workflows CEUR-WS | yes: Y300, Y301 |
| en | Müller Bergmann "Generalization of Workflows in Process-Oriented Case-Based Reasoning" FLAIRS 2015 pdf | yes: Y303, Y304 |
| en | Müller Bergmann "Learning and Applying Adaptation Operators..." ICCBR 2015 | bibliographic only; led to Y306 |
| en | "adaptation operators" process-oriented case-based reasoning ... streamlets pdf wi2.uni-trier.de | no new full text |
| en | Taaable case-based cooking system adaptation knowledge WikiTaaable Cordier Lieber Nauer paper pdf | leads only (blocked) |
| en | Dufour-Lussier Lieber Nauer Toussaint adaptation of cooking recipe ... temporal qualitative ICCBR | yes: Y309, Y310 |
| en | Taaable personalized cooking adaptation "adaptation knowledge" ... hal.science pdf | yes: Y311 (French) |
| en | Müller Bergmann "Case completion of workflows ..." ICCBR 2016 | bibliographic only |
| en | Gilbert Müller "Workflow Modeling Assistance by Case-based Reasoning" dissertation ... 2018 | bibliographic only |
| en | POQL query language ... LWA 2015 CEUR Vol-1458 | bibliographic only; led to Y307 |
| en | CookIIS Computer Cooking Contest Hanft Newo Bach Ihle Althoff adaptation recipes paper | yes: Y312 |
| de | Kochrezepte Workflows fallbasiertes Schließen Adaption Universität Trier Bergmann | leads only (EVER project, blocked); no German-language paper found |
| en | process-oriented case-based reasoning cooking recipes workflow adaptation large language models 2024 2025 Trier | confirms Y306 as the latest cooking-domain POCBR adaptation paper found; nothing on LLMs |

## Citation trail

- **Backward from Y300:**
  - Bergmann and Gil 2014 (similarity): not read; described in Y303.
  - Dufour-Lussier et al. 2010: not read; Y310 and Y311 describe it.
  - Minor et al. 2010 → **Y305**.
  - Müller and Bergmann 2014 → **Y302**.
  - Müller and Bergmann 2015 FLAIRS → **Y303**.
  - Adaptation operators 2015: not read.
  - POQL: not read.
  - Schumacher et al. 2012 → **Y308**.
  - Reichert 2000, *Dynamische Ablaufänderungen in Workflow-Management-Systemen*, and Dadam et al. 2009, *Von ADEPT zur AristaFlow BPM Suite*, both in German: the source of the correctness-by-construction principle. Not read.
- **Backward from Y303:**
  - Bergmann and Vollrath 1999 (generalised cases);
  - Garijo, Corcho, Gil 2013 (scientific workflow fragments);
  - Gaillard et al. 2014, Tuuurbine (generalisation and specialisation over RDFS, Nancy);
  - Zito-Wolf and Alterman 1992 (multicases for procedural knowledge).
  - None of these was read.
- **Backward from Y309 and Y310:**
  - Lieber 2007 (revision-based "conservative adaptation"); Cojan and Lieber 2009;
  - Pujari et al. 1999 (INDU);
  - Cojan et al. 2011, Knowledge extraction for improving case retrieval and recipe adaptation (CCC).
  - None read.
- **Forward from Y300 and Y302:**
  - Y304 (2016);
  - Y307 (2018, same 61-workflow cooking case base);
  - Y306 (2024: cites Y302, Y303, the operators paper and Müller 2018; still uses cooking workflows);
  - Y311 (2017, positions Taaable against "CookingCakeWF").
- **Forward from Y306:** Hotz et al. 2025 (on Y313, not read).
- **Forward from Y309:** Y310 cites it as the revision method to extend to workflows. No later integration into Taaable is reported in Y311.
- **Missing:** a forward index (Semantic Scholar, Google Scholar) could not be read, so later citing work outside Trier and Nancy was not found.

## Approach analyses

### A. Semantic cooking workflow: tasks, data items, control-flow blocks (Trier POCBR: Y300, Y302, Y303, Y306, Y308)

- **E1, unit:** one recipe is one workflow graph. Its parts are:
  - task nodes, the preparation steps;
  - data nodes, the ingredients and intermediate products;
  - data-flow edges, for consume and produce;
  - control flow as nested blocks: sequence, AND, XOR, LOOP;
  - taxonomy labels on tasks and on ingredients.
- **E1, purpose:** retrieval and adaptation of whole recipes against a query of desired and undesired elements.
- **E2, demonstrated:** case bases of 60 pasta (Y303), 61 sandwich (Y300, Y307), 40 cooking workflows (Y306) and 240 generated pizzas (Y302); extraction from text (Y308, Y310); implementation in CAKE and ProCAKE.
- **E2, claimed and not shown:** time, tool and skill annotations used in adaptation (Y300, Y301).
- **How intermediate products are named:** three different ways, with no rule between them. *Inferred in R6 from the definitions and figures.*
  - **As a new dish component** made by a creator task: dough, sauce, pizza (Y302 eq. 1).
  - **As a state-named ingredient:** "sieved tomatoes" (Y301 Fig. 6).
  - **Not at all:** an ingredient keeps its name through processing, as with cheese grated then sprinkled (Y302 Fig. 4). A grated cheese and a raw cheese are the same data item.

**E3, mapping on paper (inferred in R6):**
- **K1 (gratin):**
  - streams: peel → slice → blanch (rutabaga); peel → slice (potato); then a creator task "layer" producing the gratin, then "bake".
  - The four alternative sequences are four separate cases.
  - Nothing records that the blanch exists because of the bake, and blanched and raw rutabaga are the same data node "rutabaga".
- **K2 (falafel):** the stream soak → drain → grind → mix → shape → fry. The two pulses are two cases.
- **K3 and K7:** independent streams (leaves, filling) joined by a creator task "wrap", then "bake" acts on the roll as one data node. For arancini, "cooled risotto" is a data node only if the modeller names it so.
- **K9:** "squeeze" produces pulp and juice (two output data nodes); "decant" consumes the juice and produces starch; "mix" consumes starch and pulp. The data flow represents this directly.

**E4, what survives:**

| Aspect | K1 gratin | K2 falafel | K3/K7 rolls, arancini | K9 latkes |
| --- | --- | --- | --- | --- |
| a. components and joins | preserved: streams and creator tasks (Y302) | preserved | preserved: wrap or coat as creator tasks | preserved: multi-output task (Def. 1) |
| b. intermediates, readiness against doneness | extend: no state on data nodes; "until tender" only as a text facet (Y308) | extend: "soaked" is not a state unless named | extend: "cooled rice" only if named | preserved as a named data node |
| c. member after assembly | cannot: after the join only the assembled node is processed | n/a | cannot: rice finishing inside the roll is invisible | n/a |
| d. why a stage exists | cannot: no dependency or objective field | cannot | cannot | cannot |
| e. alternative routes kept apart | preserved as separate cases; XOR blocks inside one case are possible | preserved as separate cases | preserved (arancini against supplì as two cases) | n/a |
| f. substitution and consequences | see approaches C and D | see C and D | see C and D | n/a |
| g. start from a state I have | extend: partial workflows exist (Y301 §2.1), but a state is not a typed node | extend | extend | extend |
| h. provenance | cannot per claim: the case's source recipe only (Y300 XML output) | cannot | cannot | cannot |
| i. unknown against false | cannot: similarity is numeric | cannot | cannot | cannot |
| j. readable for a cook | extend: a flattened step list with ingredients per step, plus a process view (Y300 §5) | same | same | same |

- **E5, against Food-prep:**
  - **Equivalent to R3 constructions:**
    - independently processed materials ≈ streams;
    - assemblies ≈ creator tasks;
    - a material taken `from` another material's step output ≈ a multi-output data flow (latkes `settled`).
  - **Where Food-prep is richer:**
    - R1 `Material.key()` gives each intermediate a part and a state;
    - R5 adds endpoint kind, done-when and failed-if checks, member endpoints after the join, and dependency links.
  - **Where Trier is more explicit:** control flow (AND, XOR, LOOP blocks), which R5 sequences leave implicit. Independent materials can run in parallel, but no field says so.
- **E6:**
  - Graph definitions and block rules: published (Y302, Y303, Y306).
  - The three naming practices: inferred in R6.
  - All K mappings: inferred in R6.
- **Verdict: extend.**
  - Food-prep already has the data-flow half, with richer state.
  - The only part it lacks is explicit control-flow relations between steps: parallel (AND) and options (XOR) inside one route.
  - Evidence that this helps a cook: none found. Y310 shows that AND blocks cannot even say what "meanwhile" means.

### B. Generalised workflows (Y303, used in Y300)

- **E1:**
  - One generalised case stands for the set of all specialisations of its taxonomy terms.
  - It is learned when similar cases show sibling terms at the same graph position.
  - **Graph isomorphism is required.**
  - OrigSpec keeps each node's original term.
  - Purpose: more coverage, a smaller case base, faster retrieval.
- **E2:**
  - Demonstrated: 60 pasta workflows.
  - After specialisation, culinary quality was rated worse in 46 % of 50 expert ratings (p = 0.11 on aggregated quality).
  - Coverage was about 10^10 to 10^13 workflows, and 9·10^21 for 61 sandwiches (Y300).
  - **None of the generated workflows was cooked.**

**E3, mapping (inferred):**
- **K1:** the four alternative gratin sequences are not isomorphic (blanch present or absent; simmer in cream; pre-cook both), so they **stay apart**. Two sources with the same structure but different roots (potato-rutabaga against potato-celeriac) would merge into "root vegetable". The same holds for potato against rutabaga inside one structure.
- **K2:** chickpea and dried pea falafel have identical structure, so they generalise to "pulse" when both are in the case base. Specialisation to "lentil" or to "kidney bean" would then be produced without any document. This is exactly the unverified combination R4 forbids.
- **K6:** kale is a sibling of cabbage in any leaf taxonomy, so a generalised cabbage roll specialises to kale with no notice of the curly-leaf problem.

**E4, what survives:**

| Aspect | K1 | K2 | K6 |
| --- | --- | --- | --- |
| e. routes kept apart | preserved: non-isomorphic routes never merge (Def. 4) | merged: same-structure variants become one case | merged |
| f. substitution and consequences | cannot: only labels change, never structure | cannot: P15's dryness is not visible | cannot |
| h. provenance | extend: OrigSpec keeps the original term per node | extend | extend |
| i. unknown against false | cannot: a specialisation is accepted by taxonomy alone | cannot | cannot |
| other aspects | as in approach A | | |

- **E5, against Food-prep:**
  - Food-prep's R3 routes and R5 alternative sequences already stay apart without generalisation.
  - R4 accepts a swap only per documented route. R4's `kale_rolls` (not_worth_it) is the case this approach would have accepted.
- **E6:** the algorithm and its numbers are published (Y303, Y300). The K mappings are inferred in R6.
- **Verdict: not suited.**
  - The approach is built to multiply coverage, which counts unverified specialisations as solutions.
  - The one transferable idea, that structurally different routes are never merged, is **already equivalent** to how R5 keeps alternative sequences apart.

### C. Compositional adaptation by workflow streams (Y301, Y302, used in Y300)

- **E1:**
  - The case base is cut into streams at creator tasks.
  - A stream may be replaced by another case's stream with **identical anchors**: it consumes and produces the same shared data items.
  - Purpose: adapt a recipe without hand-made adaptation knowledge.
- **E2:**
  - Demonstrated: 240 generated pizzas, 10 adaptations.
  - Change requests were met 10 out of 10, on very similar pizzas.
  - Aggregated quality was at least equal in 44 % of 50 blinded expert ratings (Y302).
  - Stream chains and the removal of superfluous streams are proposed only (Y301).
  - **Nothing was cooked.**
- **E3, mapping (inferred):** this is the mechanism that produces Food-prep's unverified combinations.
  - **K1-x:**
    - Case A (G16, G18) has the stream peel → slice → blanch 10 min "almost tender", with anchor *rutabaga* into the layering.
    - Case B (G7, G8) has peel → slice (raw), with the same anchor, followed by a long covered bake.
    - Because data nodes carry ingredient names, not states, the anchors are **identical**. The stream method would substitute A's rutabaga stream into B and declare the result "semantically correct". That is K1-x.
  - **K2-x:**
    - The "quick soak" stream (boil 5 min, Q109) produces *chickpeas*, and so does the overnight soak.
    - It is substitutable into the raw-soaked route even though Q114 says that route must never use cooked pulses. The only guard is a POQL undesired element that someone must already know to write.
  - **K2, chickpea to pea:** replace the "soak chickpeas" stream by a "soak dried peas" stream from another case. The anchors differ (*chickpeas* against *peas*), so the stream is not substitutable unless the anchor condition is weakened by taxonomy, which Y302 names as future work. The transfer is then not representable as stream substitution, only as a label change (approach B) or as an operator (approach D).
  - **K9:** the starch stream (decant juice → settled starch) has anchors {juice, starch}. A latke case without it has no "juice" anchor. A stream chain would add it as a pre-processing stream; deleting it would leave "juice" produced and never consumed, which the anchor rule forbids. The recombination is respected.

**E4, what survives:**

| Aspect | K1 / K1-x | K2 / K2-x | K3 / K4 | K9 |
| --- | --- | --- | --- | --- |
| a. components and joins | preserved: streams = components | preserved | preserved: one filling stream reused for two vessels has identical anchors (K4) | preserved |
| b. intermediates, readiness against doneness | cannot: the anchor has no state, so "almost tender" and raw are the same anchor | cannot: soaked against boiled pulses are the same anchor | cannot | preserved: named node |
| c. member after assembly | cannot | n/a | cannot: rice finishing in the roll not visible | n/a |
| d. why a stage exists | cannot: why the blanch exists is lost when streams are swapped | cannot | cannot | extend: anchors make the starch's use visible, not its purpose |
| e. alternatives kept apart | **cannot: designed to combine them**; K1-x is a normal output | **cannot**: K2-x is a normal output | — | — |
| f. substitution and consequences | extend: consequences limited to the data-flow interface (orphans, missing producers; stream chains, Y301) | extend | preserved for a vessel swap with the same filling | preserved |
| g. start from a state | extend: chaining stops when an anchor is already present (Y301 §4.3) | extend | extend | extend |
| h. provenance | cannot: the output mixes cases; only the source case is logged (Y300) | cannot | cannot | cannot |
| i. unknown against false | cannot | cannot | cannot | cannot |
| j. readable | as in approach A | | | |

- **E5, against Food-prep:**
  - **Same idea:** an R3 material, its `from` and the assembly roles it fills.
  - **Food-prep's state key is the stricter interface:** R4 re-validation compares `Material.key()` (part plus resulting state), so a blanched and a raw rutabaga are different interfaces where Trier sees the same anchor.
  - **What Food-prep does not do:** recombine documented streams.
  - Y302's own claim of "semantic correctness" is purely data-flow ordering. This is the R6 name for the K8 false positive: a structural check accepts what cooks reject.
- **E6:** the anchor rule, stream definition and evaluation are published (Y302). The chain rule is proposed in Y301. The K1-x and K2-x derivations are inferred in R6.
- **Verdict: not suited** as a method: it produces exactly the unverified combinations Food-prep keeps out, with weak quality evidence and no cooking.
- **Concept worth recording:** "identical anchors" is the precise published name for the structural test that K1-x and K2-x pass while still being undocumented. It is useful vocabulary for R6's comparison, and is **already equivalent** to R4 re-validation, which is stricter because of state.

### D. Transformational adaptation: adaptation cases, learned operators, rules (Y305, Y300 §3.3, Y306)

- **E1, three forms:**
  - **Adaptation case (Y305):** the original workflow, the change request, the adapted workflow, and add and delete chains placed by pre and post anchors.
  - **Operator (Y300, Y306):** a deletion streamlet plus an insertion streamlet, learned from pairs of cases. The mayonnaise → tomato operator also changes "combine" into "chop".
  - **Rule (Y306):** precondition and conclusion in Drools.
- **E1, purpose:** carry a known change, including its consequences on tasks, to a new workflow.
- **E2:**
  - Y305: office workflows, 19 cases and 9 tests; no cooking.
  - Y306: 40 cooking workflows. The outcome is only similarity to the query; no culinary rating.
  - Y300: 7,870 learned operators from 61 sandwiches, with no evaluation.
- **E3, mapping (inferred):**
  - **K2, chickpea → pea, as an adaptation case:**
    - original workflow = `falafel/raw_soaked`;
    - change request = DELETE chickpea, ADD dried peas;
    - adapted workflow = the pea route;
    - add chains = a longer soak, plus the cooks' levers for dryness (coarse grind, moist aromatics, P4);
    - delete chains = none.
    - This is structurally the R4 transfer `pea_falafel`.
  - **K3, kale → napa:** as an operator learned from the pair (cabbage roll, napa roll), the deletion streamlet is "boil whole head and peel leaves", and the insertion is "detach leaves raw, blanch 1-2 min, shave the rib" (N2, N3, N6). R4 records exactly these steps with citations.
  - **K6:** no operator exists for curly kale, because no document pairs it. Y300's rule, no adaptation without knowledge, would then decline, which agrees with R4's "not_worth_it" for an absence of evidence. It does not record why.

**E4, what survives:**

| Aspect | K2 (adaptation case) | K3 (operator) | K6 |
| --- | --- | --- | --- |
| d. why a stage exists | cannot: the add chain has no reason field | cannot | cannot |
| f. substitution and consequences | **preserved**: add and delete lists make the consequences explicit | **preserved**: an exchange operator carries its task changes | extend: absence of knowledge, no adaptation |
| h. provenance | extend (Y305): the source episode is the provenance; learned operators have none | cannot for learned operators | — |
| i. unknown against false | cannot | cannot | extend: "no knowledge, no adaptation" (Y300 §5) is close to "unknown", but it is not recorded |
| e. alternatives kept apart | cannot: an operator chain is searched to maximise similarity (Y304, Y306) and can mix several cases' operators | | |
| other aspects | as in approach A | | |

- **E5, against Food-prep:**
  - An R4 transfer is an adaptation case with a verdict and citations.
  - What Y305 has that R4 lacks: **the diff itself**, as add and delete chains anchored in the base route. R4 stores the new materials and the swap, but not "steps added: blanch; steps removed: whole-head boil" as a first-class list.
- **E6:**
  - The Y305 structure is published.
  - The operator definition and the mayonnaise example are published (Y300, Y306).
  - The K2, K3 and K6 mappings and "R4 lacks the diff" are inferred in R6 from the R4 schema seen in `transfers.yaml`.
- **Verdict:**
  - **Already equivalent** for adaptation cases (Y305 ≈ R4).
  - **Extend** for one field: record each transfer's add and delete steps against its base route, as anchored chains. This makes aspect f, the consequences elsewhere, readable at a glance.
  - Learned operators and rules: **not suited**. They are learned without provenance and judged only by similarity to the query.

### E. Taaable: minimal query generalisation, contextual substitution rules, preparation by grafting (Y311, Y310 §3.1)

- **E1:**
  - Unit: a recipe indexed by ontology classes.
  - Retrieval: the cheapest generalisation of the query, with cost estimated from the share of recipes.
  - Adaptation knowledge: (context, replaced, replacing) triples. They are **specific** (one recipe) or **generic** (a class); those taken from variants written in the recipe cost 0.
  - Preparation: the ingredient's action sequence is replaced by the closest "prototype" of the new ingredient from another recipe.
  - Quantities: revision under linear constraints.
- **E2:**
  - Contest results; from 2014 the outputs were cooked and tasted blind by the public (Y311 §6).
  - No controlled study is in the paper read.
  - The mango → fig example is shown (§4.4).
- **E3, mapping (inferred):**
  - **K2:** a generic rule (falafel class, chickpea ↝ dried pea) under Taaable's cost would be cheap, because both are pulses. The preparation graft takes the "pea prototype" from another recipe, for instance soup peas: no soak (Q104-Q106). That is the wrong prototype for a raw grind. R5 found that every falafel soaks the peas.
  - **K3:** grafting the napa-leaf prototype from N6 into the cabbage roll is R4's `napa_cabbage_rolls` materials block, which takes its steps from recipes N1, N6 and N10.
  - **K4:** the onion-vessel prototype (layers that slip if overboiled, O12, O15) would be grafted from farcis niçois into the courgette dish.
  - **Specific rule at cost 0:** a recipe's own written variant ("or simmer in the cream", G5, G9) is Taaable's zero-risk rule. Food-prep's alternative sequences keep the same thing, as documented.

**E4, what survives:**

| Aspect | K2 | K3/K4 | K8 |
| --- | --- | --- | --- |
| f. substitution and consequences | extend: consequences confined to the replaced ingredient's own actions; the effect on shared steps (fry, bind) is not checked | preserved for the wrapper's or vessel's own preparation | cannot: no timing |
| h. provenance | extend: specific rules point to their recipe; a prototype points to its recipe number (#53) | preserved by prototype origin | — |
| e. alternatives kept apart | extend: written variants become zero-cost rules, applied rather than kept as routes | | |
| i. unknown against false | cannot: a cost, never "unknown" | | |
| d. why a stage exists | cannot | | |
| g. start from a state | cannot | | |

- **E5, against Food-prep:**
  - Prototype grafting is **what R4 already does by hand with citations**: a transfer's swapped material takes its op chain from recipes of the new ingredient.
  - The specific and generic contexts map onto R4's per-route transfers. Food-prep only has the specific kind.
  - Taaable's retrieval cost is a numeric risk score, which Food-prep's rules exclude.
- **E6:** the rules, costs and grafting are published (Y311, Y310). The K mappings are inferred.
- **Verdict: already equivalent** for prototype grafting and specific contextual substitutions.
- **Not suited** for the cost-based retrieval, which is a scoring model.

### F. Revision-based adaptation with qualitative temporal constraints (Y309, Y310 §2-3)

- **E1:**
  - A case is a network of qualitative interval relations (INDU: Allen relations plus relative durations) between cooking actions and ingredient states.
  - Domain knowledge holds durations ("carrot cooks 25 min") and the rule that cooking x meets "x cooked".
  - Adaptation: apply the substitution through an abstraction, then revise minimally to restore consistency.
  - The result: actions are **reordered** so that both finish together.
  - Pairs with no known relation carry the universal relation (unspecified), not a false one.
- **E2:** one worked example (carrot risotto). A Perl prototype, described by its authors as slow and not integrated. No dataset, no cooking.
- **E3, mapping (inferred):** this is the one approach in the area that speaks to K1 and K8.
  - **K1 dependency:**
    - Domain knowledge: rutabaga in the bake takes longer than potato (Q231, Q234).
    - Source (potato gratin): both kinds of slice share the bake interval.
    - The substitution potato ↝ rutabaga for half the slices makes "the same bake finishes both" inconsistent.
    - Revision must either start the rutabaga earlier (a pre-cook: the blanch, or the simmer in cream) or lengthen the bake (raw slices with a 90-min covered bake, G7, G8).
    - So the **dependency "blanch exists because of the bake" becomes a derivable repair**, and the **two working repairs come out as two scenarios**, which is the shape of R5's alternative sequences.
  - **K8:**
    - The raw short bake (G20, G21: still crunchy) is inconsistent and rejected.
    - The raw long covered bake is consistent and accepted.
    - That is exactly the false negative and false positive pair that a structure-only check gets wrong (R4 before A2, and approach C).
  - **K1-x:** the 10-min almost-tender blanch followed by the 90-min bake is consistent for "rutabaga cooked". Overcooking is not a constraint unless domain knowledge states an upper bound (the "some give" against "no resistance" conflict). The algebra can represent such a bound, but nobody has documented one.
  - **K2-x:** "never cooked before grinding" (Q114) is a qualitative constraint (cook before grind is forbidden). The quick-soak graft would be inconsistent and repaired away, if Q114 is in the domain knowledge.

**E4, what survives:**

| Aspect | K1 | K8 | K1-x / K2-x |
| --- | --- | --- | --- |
| b. readiness against doneness | extend: state intervals ("x cooked") exist; readiness as a separate state type is not described | extend | extend |
| c. member after assembly | preserved: each member's cooking interval runs inside the shared bake interval | preserved | — |
| d. why a stage exists | **preserved as derivable**: the pre-cook is the repair that restores consistency | preserved | preserved |
| e. alternatives kept apart | preserved: revision returns a *set* of minimal scenarios | — | extend: K1-x is consistent unless an upper bound is documented |
| f. substitution and consequences | **preserved**: the core of the method | preserved | preserved if Q114 is in the domain knowledge |
| i. unknown against false | **preserved**: the unspecified relation B (Y309 §5) | | |
| h. provenance | cannot: nothing per constraint in the method; Food-prep would have to add it | | |
| a., g., j. | cannot: no data-flow (Y310 §2: the algebra lacks loops and options); no cook-facing output | | |

- **E5, against Food-prep:**
  - R5 records dependency links, per-source times, and member endpoints after a join, each as a cited claim.
  - What it cannot do is *check* a sequence against them. The R5 README says time is not in the R4 structural model (K8).
  - The INDU network is the published formalism for exactly that check. It keeps "not known" as its own value, which matches R1's three-valued rule.
- **E6:**
  - The method, the example and the unspecified relation are published (Y309).
  - The workflow-against-algebra trade-off is published (Y310 §2).
  - Every K mapping is inferred in R6.
- **Verdict: extend.** Food-prep has the durations and dependencies as data. The concept to add is relations between the time intervals of members (for example, the bake must end when both are done), so that a candidate sequence can be checked rather than only described.
- **Evidence for scale is insufficient:** one example, and a slow prototype.

### G. Conversational retrieval of workflows (Y307)

- **E1:** a dialogue over mined workflow fragments builds the query.
- **E2:**
  - 61 cooking workflows; 60 simulated scenarios; 8 users.
  - Required time about halved; success 14/16 against 15/16.
  - The dialogue starts from an empty query. A pre-modelled starting point was not investigated.
- **E3, mapping (inferred):** for Q5, "I have cooked rice from yesterday" (K7) would have to be a fragment feature in the dialogue. Nothing in the paper supports starting from it.
- **E4:**
  - j: extend, because questions about fragments are readable;
  - g: cannot, as published;
  - everything else as in approach A.
- **E5:** no Food-prep counterpart. It is relevant to R7 (interface), not to representation.
- **E6:** published (Y307).
- **Verdict: insufficient evidence** (one small study). It is not a representation question.

### H. CookIIS: community-mined substitutions and in-place text replacement (Y312)

- **E1:**
  - The recipe is text; the ingredients are the problem description.
  - Substitutions are mined from user comments as co-occurrence of an old and a new ingredient of the same class (2,967 suggestions).
  - The preparation text is rewritten by string matching, with the original kept visible.
- **E2:** a system description; adaptation quality was not evaluated.
- **E3:** K2 or K3 would come out as "replace chickpeas with peas" in the text, with no change to steps.
- **E4:**
  - f: cannot, because the steps never change;
  - h: extend, because a suggestion counts community comments but cites none;
  - j: preserved, because the change is marked in place.
- **E5:** below R4. The one idea for a reader is to show both the replaced and the original text (Q6).
- **E6:** published (Y312).
- **Verdict: not suited.**

### Text-to-workflow extraction (Y308, Y310 §4)

- **Out of R6 scope:** Food-prep curates by hand.
- **One concept bears on Q2 and Q5:** Y310's "food components as consumable resources", each with its ingredient set I(F). It identifies an intermediate by **what went into it**. Food-prep's `Material.key()` identifies it by **part and resulting state**.
- **Verdict: not suited** as a method; noted for Q5.

## Answers to Q1-Q6 from this area

**Q1, unit and two traversals.**
- **Unit:** the whole recipe as one case (a workflow graph). Streams are a derived sub-unit cut at the steps that create a new component (Y302).
- **Ingredients to dish:** POQL retrieval with desired and undesired elements (Y300).
- **Dish to production:** the case itself is the "how". There is no separate second traversal: the same graph serves both.
- **Taaable** indexes the recipe by ontology classes and keeps the preparation as text plus extracted actions (Y311).

**Q2, complete processes.**
- **Representation in the Trier formalism (Y302):**
  - data flow: tasks consume and produce data items;
  - control flow: nested sequence, AND, XOR and LOOP blocks;
  - parallelism: AND blocks.
- **Intermediate products are named inconsistently** (approach A): as new components, as state-named ingredients, or not at all when the name persists through processing.
- **Completion and failure:**
  - completion only as a text facet ("until tender", Y308), or as a loop or end condition ("until al dente", Y310 §4.3);
  - failure checks: none found;
  - readiness against doneness: none found.
- **Durations, waits, "meanwhile":** workflows cannot express them (Y310 §2). INDU interval networks can (Y309, Y310). Nothing found combines the two in an implemented cooking system.
- **Members after assembly:** not representable in the workflow form. Representable as nested intervals in INDU (inferred).

**Q3, substitution and its inconsistencies.** Four published mechanisms:
1. **Stream substitution with identical anchors** (Y302). It guarantees only a data-flow interface. Stream chains add the producers a new stream needs, and superfluous streams are removed (Y301, proposed).
2. **Operators and adaptation cases.** These carry the task changes that go with an ingredient swap: add and delete lists (Y305); mayonnaise → tomato needs chop instead of combine (Y300).
3. **Grafting** (Taaable). It replaces the ingredient's own action sequence with the closest documented one for the new ingredient (Y311 §4.4).
4. **Revision-based repair** (Y309). Apply the substitution, then repair the inconsistencies with domain knowledge by minimal change. This is the only published method that reorders steps because of durations.

- **Real-world evidence for the results:** none of the four was validated by cooking in the papers read. The expert ratings are mixed: about 44-46 % of ratings had the adapted workflow worse (Y302, Y303).

**Q4, alternative routes.**
- **Many workflows of the same dish are kept as separate cases.**
- **Generalisation** merges only structurally identical ones (graph isomorphism, Y303 Def. 4), so differently sequenced routes stay apart.
- **Compositional adaptation and operator chains deliberately combine cases.** Because anchors carry ingredient names, not states, they would produce Food-prep's K1-x and K2-x and judge them correct (approach C, inferred).
- **The published size of this space** (9·10^21 recipes from 61, Y300) is the clearest statement of how far "valid by structure" runs ahead of "documented".
- **Taaable's closest analogue to a "documented variant":** variants written in a recipe become zero-cost specific rules (Y311).

**Q5, reuse of existing preparations.**
- **Formally defined, never demonstrated:**
  - partial workflows (Y301, Y302);
  - a chaining rule that stops when an intermediate is already present (Y301);
  - a conversational query with no pre-modelled start (Y307).
- **Case completion** (2016) was not read.
- **Equivalence of intermediates:**
  - Trier: equal if the label is equal;
  - Y310: equal if the set of ingredients is equal;
  - neither looks at process history.
- **Whether equivalent-looking states with different histories are interchangeable:** nothing found addresses this.

**Q6, visualisation.**
- CookingCAKE: a flattened step list with ingredients per step, a process graph view, and a generated recipe name (Y300 §5).
- Taaable: the original recipe and three adaptation layers (ingredients, quantities, text) on demand (Y311 §2).
- CookIIS: in-place mark-up of replaced against original text (Y312).
- Trier, later: similarity explanation by visualisation (titles on Y313, not read).
- No user study of these views for a person deciding what to cook was found.

## Open questions this area leaves

1. **Learned operators:** the operators paper (ICCBR 2015) and the Müller 2018 dissertation were not read. Do they report how often an operator's task changes were culinarily wrong, or any operator provenance?
2. **Workflow plus time:** has anyone implemented the revision-based temporal adaptation (Y309) on a real recipe base, or combined it with workflows as Y310 proposed? Nothing after 2013 was found. The ICCBR 2012 full paper was not read.
3. **Case completion:** does the 2016 case-completion paper infer missing intermediate states? That would bear on Q5 and on Food-prep's nine route steps without a source for their endpoint kind.
4. **Taaable's adaptation-knowledge acquisition:** core.ac.uk returned 403 and the HAL chapter was blocked. Does WikiTaaable record a source per substitution, and were any grafted preparations cooked?
5. **German-language Trier work:** none was found online. The EVER project summary (403) may list German reports, and the Chefkoch-based demonstrator is mentioned only in a snippet.
6. **Forward citations outside Trier and Nancy** are unknown (Semantic Scholar 429).
7. **Fit with Food-prep:** would explicit relations between member time intervals (approach F) catch K8 without accepting K1-x? That is an R6 comparison question; no source tests it.
