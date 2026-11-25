# Evidence: visualisation of recipes and culinary knowledge for people deciding what to cook

- **Date read:** 2026-11-25 (all sources).
- **Method:** web search (English, Japanese, German-language results via English queries), then the full text where it could be reached. PDFs were saved by the fetch tool and converted to text locally (pdftotext; PyMuPDF for the Japanese PDFs, whose text pdftotext could not decode). Forward citations of the central paper (Y700) were listed through the Semantic Scholar API.
- **Search languages:** English, Japanese. German appears through Y704, a study run in German in Bavarian home kitchens. No Nordic-language HCI work on recipe visualisation was found.
- **Blocked or partial:**
  - ACM DL PDFs (403).
  - The Nottingham repository (403).
  - The KIXLAB archive page (404).
  - Several Japanese PDFs needed a second extractor.
  - Two papers were read only in part, and the parts are named in each entry.
- **Scope note:** this area asks what a home cook can *read and decide* from a representation. Most sources here are HCI or visualisation studies, not representation formalisms, so E3/E4 are applied to the *representation family* each source evaluates (or fails to evaluate) for a cook.

## Sources

### Y700 — https://recipescape.kixlab.org/RecipeScape_CHI_2018__Camera_Ready_.pdf
- **Citation:** Minsuk Chang, Léonore V. Guillain, Hyeungshik Jung, Vivian M. Hare, Juho Kim, Maneesh Agrawala. 2018. *RecipeScape: An Interactive Tool for Analyzing Cooking Instructions at Scale.* CHI 2018, Montréal. DOI 10.1145/3173574.3174025 (printed on the paper).
- **Version read:** the authors' camera-ready PDF, linked from the project page https://recipescape.kixlab.org/. The page gives the link as a relative path, resolved against that page. Read in full.
- **Type:** primary research (system + qualitative user study).
- **E1, what it represents:**
  - Each recipe is an **ordered tree**: the first child of every node is a cooking action, and its siblings are the ingredients the action involves.
  - Recipes are compared by tree edit distance. Relabel costs come from word-embedding similarity, so "mix" to "add" costs less than "mix" to "heat".
  - Recipes are clustered hierarchically and laid out by distance (Gram-matrix MDS).
  - Three views:
    - RecipeMap: a point cloud of clusters; a star marks the most representative recipe of each cluster.
    - RecipeDeck: unlabeled trees side by side, with a pairwise comparison of action sequences and a Venn diagram of ingredients.
    - RecipeStat: a histogram of where each frequent action, or action–ingredient pair, occurs in the process.
  - **Purpose:** analysis of hundreds of recipes of *one dish*, for cooking professionals and culinary students.
- **E2, what it shows:**
  - **Formative interviews:** 10 professionals.
  - **Pipeline on Epicurious data:**
    - 487 chocolate-chip-cookie and 510 tomato-pasta recipes;
    - crowd correction fixed 9,987 action labels, 40% of the final 24,975 action verbs.
  - **Evaluation:**
    - **Experts:** 4, in 2-hour sessions.
    - **Culinary students:** 7, in 90-minute sessions.
    - **Format:** qualitative; there was no baseline comparison, and the authors say so deliberately.
  - **Demonstrated:**
    - 2 of the experts and 5 of the 7 students said the clusters reflect different ways of cooking.
    - Every participant started from RecipeMap and then read individual recipes.
    - The professional chef read the map's centre as must-have ingredients and its edge as personal or "exotic" additions.
    - The journalist used pairwise comparison of adjacent recipes to find replaceable ingredients and actions.
    - 4 of 7 students found the tree diagram especially helpful for picturing the whole process.
  - **Problems the authors report:**
    - RecipeStat assumed knowledge of histograms that some participants lacked.
    - Clusters come without explanations.
    - Parser errors are offset by showing the source text beside each tree.
  - **Scope set by the authors:**
    - "Real-time cooking support" was excluded from the design goals.
    - The tool is not designed to improve cooking skills.
    - An earlier sequence-based representation gave clusters dominated by recipe length, which motivated the tree (Figure 8).

### Y701 — https://arxiv.org/pdf/1111.3919v2
- **Citation:** Chun-Yuen Teng, Yu-Ru Lin, Lada A. Adamic. *Recipe recommendation using ingredient networks.* WebSci 2012, pp. 298–307. Publisher DOI not verified (dblp lists the venue); arXiv 1111.3919.
- **Version read:** arXiv v2 PDF, full text (extracted locally).
- **Type:** primary research (network analysis + prediction). No user study.
- **E1:**
  - Two ingredient networks built from Allrecipes:
    - a **complement network** of ingredients that co-occur more than chance (§5);
    - a directed, weighted **substitute network** mined from review phrases such as "replace a with b" (§6.3). Edge weight is p(b|a); suggestions seen fewer than 5 times are dropped.
  - Communities found with a random-walk map equation.
  - **Purpose:** predicting which of two related recipes is rated higher.
- **E2:**
  - **Data:** about 46k recipes and about 2M reviews.
  - **Complement network:** splits into a savory and a sweet community. Ubiquitous ingredients (egg, salt) are pushed to the periphery of the drawing because their many edges are all weak (§5, Fig. 2).
  - **Substitute network:** forms clusters of "functionally equivalent" ingredients (Table 3). One cluster groups mushroom, broccoli, kale, carrot and zucchini. The substitute network also correlates with a rating-based preference network.
  - **Prediction:** accuracy .792 with all features; network features alone .786.
  - **Use for cooks: suggested, not tested.** The authors propose matching one's pantry against a cluster (§6.3) and flagging omittable or substitutable ingredients in an interface (§8).

### Y702 — https://pmc.ncbi.nlm.nih.gov/articles/PMC3240947
- **Citation:** Yong-Yeol Ahn, Sebastian E. Ahnert, James P. Bagrow, Albert-László Barabási. 2011. *Flavor network and the principles of food pairing.* Scientific Reports 1:196. DOI 10.1038/srep00196.
- **Version read:** PMC full text (read through the fetch tool's summary of the full page).
- **Type:** primary research. No user evaluation.
- **E1:**
  - A bipartite ingredient–flavour-compound network (381 ingredients, 1,021 compounds) projected onto ingredients. An edge means at least one shared compound; its weight is the number of shared compounds.
  - Recipe data: about 56k recipes from three sites.
- **E2:**
  - Pairing of compound-sharing ingredients is over-represented in North American and Western European recipes and avoided in East Asian ones.
  - **The full network is too dense to draw.** The published figure is a statistically extracted *backbone*, while the measurements use the full network.
  - **Stated limits:**
    - the compound data is incomplete;
    - concentrations are ignored;
    - some ingredients serve structure or colour, not flavour;
    - preparation changes flavour.
  - No claim of practical value for cooks.

### Y703 — https://etheses.whiterose.ac.uk/id/eprint/5158/1/Lucy%20Buykx%20accepted%20thesis.pdf
- **Citation:** Lucy Buykx. 2013. *Interactive recipe instructions: supporting cooks with better designs.* PhD thesis, University of York. Record page: https://etheses.whiterose.ac.uk/id/eprint/5158/.
- **Version read:** repository PDF. **Read in part:**
  - the abstract and table of contents;
  - Ch. 6 limitations (§6.4.4);
  - Ch. 7 study design (§7.1–7.2), the overview screen flow (Fig. 67–70), and the overview results, limitations and conclusions (§7.4.3–7.4.4).
  - Chapters 2–5 and 8 were not read.
- **Type:** primary research (controlled cooking studies with real cooks).
- **E1:**
  - The RECIPE2 study (Ch. 7) compares three ways of presenting a recipe on an iPad:
    - **control:** a traditional ingredient list plus steps;
    - **segmented-with-pictures**;
    - **overview.**
  - The **overview** is a flowchart:
    - each branch is a component or sub-goal with a title;
    - short step extracts open the full text and a goal-state picture;
    - preparation instructions sit just before the ingredient is used;
    - the ingredient list is split and aligned beside the steps that use it (§7.4.3).
- **E2:**
  - **Design:** 24 cooks, 3 recipes, Latin-square repeated measures (§7.2).
  - **Ratings:** the overview received the highest rating for well-organised instructions.
  - **What cooks said:**
    - 10 cooks named the flowchart layout as what they liked most;
    - cooks said it let them plan and do tasks in parallel and prepare later ingredients ahead;
    - one cook said it showed the rationale behind the timings.
  - **What did not change:** time to complete, the number of tasks done in parallel, and overall counts of problems and errors.
  - **How cooks used the detail:**
    - detailed step pop-ups were visible for about 29% of the time, less than half of step-visible time in the other formats;
    - 14 cooks used a "quick details" mode of under 10 s per look;
    - the author reads this as the overview, the context, mattering more than the current step's detail.
  - **One clear error reduction:**
    - a control-format paragraph mixed two components, the gremolata and the dressing;
    - in that format cooks combined or confused them;
    - with the components drawn apart in the overview, no cook made those errors.
  - **Prep before cooking:** only 1 of 24 cooks did mise en place before starting; 22 prepared ingredients as they went.
  - **Limitations (§7.4.4):**
    - skill is measured only by self-report;
    - cooks vary more than formats do, so time and error measures were too insensitive;
    - a lab kitchen;
    - recipe familiarity confounds the results (gremolata was unknown to most cooks).

### Y704 — https://arxiv.org/pdf/2112.04788v2
- **Citation:** Alexander Frummet, David Elsweiler, Bernd Ludwig. *"What can I cook with these ingredients?" – Understanding cooking-related information needs in conversational search.* ACM Transactions on Information Systems (2022). DOI 10.1145/3498330 appears in a Crossref search result, which was not opened, so the DOI is not verified; the publisher page was not read.
- **Version read:** arXiv v2 PDF. **Read in part:** abstract, method (§3), taxonomy definitions (Table 2), conversational cues (§4.2), comparison with earlier taxonomies (§6). The classification experiments were skimmed.
- **Type:** primary research (in-situ study, Wizard-of-Oz).
- **E1:**
  - A hierarchical taxonomy of information needs voiced while cooking.
  - Level 0 has two classes: fact-based and competence-oriented.
  - Level 1 has 11 categories, including:
    - Recipe;
    - Ingredient;
    - Amount;
    - Time;
    - Preparation;
    - Cooking technique;
    - Equipment;
    - Knowledge;
    - Meal;
    - Temperature;
    - a next-step category.
- **E2:**
  - **Setting:**
    - 45 participants, cooking in their own kitchens, in German (much of it Bavarian dialect);
    - each received a box of about €10 of ingredients and had to cook a meal they had not cooked before;
    - a human experimenter played the assistant.
  - **Data:** 38.75 hours recorded, 2,376 turns.
  - **Recipe needs:** participants chose the recipe inside the conversation and often used ingredients as search terms, for example a dish with lentils, chickpeas and tomatoes.
  - **Next-step needs:** these were often signalled only by discourse markers ("Mhm?"), which need context to interpret.
  - **Agreement:** inter-rater κ 0.75 at level 1.
  - **Classification:** BERT reached F1 of about 40%.
  - **Substitution** did not appear as a level-1 category in the text read; the level-2 codes were not inspected.

### Y705 — https://arxiv.org/pdf/1709.00293.pdf (served as v1)
- **Citation:** Mershack Okoe, Radu Jianu, Stephen Kobourov. *Revisited Experimental Comparison of Node-Link and Matrix Representations.* arXiv:1709.00293v1, 2017.
- **Later version, not read:** search results describe an extended TVCG version, *Node-Link or Adjacency Matrices: Old Question, New Insights* (2018/2019), with two datasets.
- **Version read:** arXiv v1, full text (extracted locally).
- **Type:** primary research (crowdsourced controlled experiment).
- **E1:** compares node-link diagrams and adjacency matrices on 14 graph tasks over one real scale-free network (258 nodes, 1,090 edges).
- **E2:**
  - **Participants:** 557 crowd workers, between-subjects.
  - **Node-link was better** for most connectivity and topology tasks: neighbours, paths, whether two nodes are connected.
  - **Group tasks** were roughly equal; matrices were better at estimating the number of clusters.
  - **Memorability:** the results section says node-link was better on recall (T11); the introduction says the two were similar. This is an internal inconsistency in v1.
  - **No decision or choice tasks** were tested.

### Y706 — https://www.cmu.edu/joss/content/articles/volume5/McGrathBlythe/MBNoJava.html
- **Citation:** Cathleen McGrath, Jim Blythe. *Do you see what I want you to see? The effects of motion and spatial layout on viewers' perceptions of graph structure.* Journal of Social Structure. Volume 5 is taken from the URL path; the year is not verified.
- **Version read:** journal HTML (non-Java version), through the fetch tool's summary of the full page.
- **Type:** primary research (experiment).
- **E1:** the same network drawn in different spatial layouts (status on the vertical axis vs centrality in the middle), with or without motion between the formal and informal networks.
- **E2:**
  - **Participants:** 133 students.
  - **Effects on accuracy:**
    - motion had a significant effect;
    - layout alone did not;
    - motion and layout interacted.
  - **Meaning read into layout:**
    - viewers brought their own organisational vocabulary and read the vertical layout as a formal chain of command, although the drawing showed an informal network;
    - the authors warn that any direct mapping of an attribute to position creates unintended inferences, and that placing partners close together does the same.
  - The 1997 predecessor (McGrath, Blythe & Krackhardt, *Social Networks* 19(3):223–242) was seen as a bibliographic record and summary only (abstract only, see Failed pages). It reports that perceived prominence, bridging and grouping changed with spatial arrangement for 80 viewers.

### Y707 — https://arxiv.org/pdf/2009.00192v1
- **Citation:** Sehi L'Yi, Jaemin Jo, Jinwook Seo. 2020. *Comparative Layouts Revisited: Design Space, Guidelines, and Future Directions.* arXiv:2009.00192. Listed as IEEE VIS (InfoVis) 2020; the TVCG DOI was not verified.
- **Version read:** arXiv v1 PDF. Guidelines (§5.2), limitations and conclusion read in full; §1–4 skimmed.
- **Type:** systematic review (127 papers, 15 with quantitative user studies). It is a survey, used here for its synthesis of primary studies.
- **E1:** three layouts for comparison:
  - **juxtaposition**, either chart-wise or item-wise;
  - **superposition**, with items overlaid;
  - **explicit encoding**, which draws the difference itself.
- **E2, seven guidelines:**
  1. Avoid chart-wise juxtaposition for local differences; it almost never beat the other layouts.
  2. If it cannot be avoided, add landmarks or highlight the matching items.
  3. In superposition, align the marks to be compared.
  4. Do not blend colours in superposition.
  5. Avoid explicit encoding on its own: it is unfamiliar to novices and decontextualised.
  6. Use hybrids instead; four studies found them superior for specific tasks.
  7. Avoid animation for large differences; large changes between two node-link diagrams confused people.

### Y708 — https://pure.uva.nl/ws/files/149990210/Examining_the_user_evaluation_of_multi-list_recommender_interfaces.pdf
- **Citation:** Alain D. Starke, Edis Asotic, Christoph Trattner, Ellen J. Van Loo. 2023. *Examining the user evaluation of multi-list recommender interfaces in the context of healthy recipe choices.* ACM Transactions on Recommender Systems 1(4), Article 18. DOI 10.1145/3581930, as given by the repository record https://dare.uva.nl/id/32f4439b-c8d4-4ea5-b2d8-753e0195b2d8.
- **Version read:** the final published PDF from the University of Amsterdam repository. **Read in part:** abstract, introduction, Study 1 design and results (§3), Study 2 results (§4.2.1).
- **Type:** primary research (two online experiments).
- **E1:** recipes shown either in one list or in several lists, each labelled with a food goal; explanations per list were present or absent.
- **E2, Study 1** (N = 366; 5 recipes in one list vs 5 lists × 5 recipes):
  - multi-list raised perceived diversity, and that raised choice satisfaction;
  - multi-list also raised choice difficulty, an effect that diversity mediated;
  - choices matching the user's goal raised understandability.
- **E2, Study 2** (N = 164; similar set sizes, personalised explanations or not):
  - multi-list was slightly more understandable;
  - results on difficulty and satisfaction were mixed.
- **Outcome measure:** choices were hypothetical ("would like to prepare at home"); nothing was cooked.

### Y709 — https://ubi-naist.github.io/paper/IPSJ/202006_DICOMO_nakabe_paracook.pdf
- **Citation:** 中部 仁, 水本 旭洋, 諏訪 博彦, 安本 慶一 (Jin Nakabe, Teruhiro Mizumoto, Hirohiko Suwa, Keiichi Yasumoto). 2020. 複数レシピで並行調理する際の調理環境に応じた最適調理手順作成法と評価 (*Minimizing cooking time for multiple parallel recipes under arbitrary cooking environment*).
  - **Venue:** DICOMO 2020 (IPSJ symposium), taken from the file name; not verified.
  - **Abstract record:** a related IPSJ record exists at https://ipsj.ixsq.nii.ac.jp/records/210857 (not opened).
- **Version read:** the lab's repository PDF, in Japanese. Abstract, introduction, related work and problem formulation (§1–4) read; the evaluation was read through the abstract.
- **Type:** primary research (algorithm, computational evaluation).
- **E1:**
  - Each recipe becomes a **task graph**: nodes are cooking tasks, edges are precedence.
  - Cooking several recipes in parallel is solved as task scheduling. Resources (cook, knife, board, bowl…) are processors, and **washing-up** is an overhead that depends on the state of each resource.
  - The method extends the DF/IHS algorithm.
- **E2:**
  - Against hand-made plans for menus built from real recipes, the optimised plans cut total time, washing-up included, by about 15%.
  - **No study of how the plan is shown to cooks** appears in the sections read.
  - **Related work cited by the paper (not read):**
    - multi-dish scheduling by simulated annealing, with tasks classed into six types such as cut and mix;
    - multi-cook scheduling as RCPSP.

### Y710 — https://www.ipa.go.jp/archive/files/000005836.pdf
- **Citation:** 浜田 玲子 (Reiko Hamada). 平成15年度 (FY2003) 未踏ソフトウェア創造事業 (IPA Mitou programme) report, 家庭におけるマルチメディア調理支援 (*Multimedia cooking support in the home*).
- **Version read:** publisher PDF (IPA), one page, read in full.
- **Type:** implementation report (developer description). Not peer reviewed; no evaluation.
- **E1:** the system behind "Cooking Navi" (Hamada et al., ACM Multimedia 2005, not read):
  - recipe text is aligned with cooking video;
  - the text's structure is displayed, with the current task highlighted;
  - an optimisation panel recomputes the best order of tasks to suit the kitchen (one or two gas rings) and the cook's actual progress;
  - multiple recipes and multiple cooks are supported, with a "next" button per task.
- **E2:** claims only. It claims cooks need only follow the proposed order to finish every dish in the shortest time. Nothing is demonstrated.

### Y711 — https://star.rcast.u-tokyo.ac.jp/old/content/files/pdf/conference/full_paper/17. panavi.pdf
- **Citation:** Daisuke Uriu, Mizuki Namai, Satoru Tokuhisa, Ryo Kashiwagi, Masahiko Inami, Naohito Okude. *panavi: Recipe Medium with a Sensors-Embedded Pan for Domestic Users to Master Professional Culinary Arts.* CHI 2012, Austin. DOI not verified.
- **Version read:** repository PDF (University of Tokyo RCAST). Abstract, related work, design process and user study read; the implementation was skimmed.
- **Type:** primary research (research through design).
- **E1:**
  - A frying pan with temperature and motion sensors.
  - Instructions are situated in the moment: projected images, LEDs and vibration react to sensed temperature and pan movement, alongside text and video on a display.
  - The model recipe is carbonara.
- **E2:**
  - **Preliminary study:** 2 amateurs.
  - **Main study:** 4 users in their twenties, studied with video-cued recall.
  - **Finding behind the design change:** controlling temperature alone did not give a good sauce, because stirring and shaking also matter. Motion sensing was added as a result.
  - **Results:** qualitative, with no comparison condition.
  - The paper cites Hamada et al.'s Cooking Navi (MM '05) as a reference (ref. 13).

### Y712 — https://arxiv.org/pdf/2108.01427
- **Citation:** Arngeir Berge, Vegard Velle Sjøen, Alain D. Starke, Christoph Trattner. 2021. *Changing Salty Food Preferences with Visual and Textual Explanations in a Search Interface.* Joint Proceedings of the ACM IUI 2021 Workshops (HEALTHI), CEUR-WS. arXiv:2108.01427.
- **Version read:** arXiv PDF, full text (extracted locally).
- **Type:** primary research (online experiment, workshop paper).
- **E1:**
  - A **taste map**: a five-axis pentagon of basic tastes beside each search result and recipe. Only the salty axis was computed.
  - In the boosted condition the salty value also counts salt-replacer herbs and spices, with a text explanation.
- **E2:**
  - **Participants:** 200 (Prolific and MTurk).
  - **Ratings:**
    - recipes containing salt replacers were rated about 0.2 points higher on a 1–7 scale when boosted;
    - the displayed taste-map value strongly predicted the rating given (β = 2.68, p < 0.001).
  - **No tasting:** the ratings are of recipes on screen.
  - **Limits:** only 3 salt-replacer ingredients were in the sample, and the authors cannot separate an explanation effect from salience.

## Failed pages and abstract-only

| URL or query | why | fallback tried |
| --- | --- | --- |
| https://kixlab.github.io/projects-archive/recipescape | 404 | the project page recipescape.kixlab.org, then the PDF linked from it (Y700) |
| https://dl.acm.org/doi/pdf/10.1145/3173574.3174025 | 403 | authors' camera-ready PDF (Y700) |
| https://nottingham-repository.worktribe.com/OutputFile/933297 (Hyland, Crabtree, Fischer, Colley, Fuentes, on anticipating "what do you want for dinner") | 403 | none found; **not read**, not cited as evidence |
| https://etheses.whiterose.ac.uk/id/eprint/5158/ (Buykx record page) | read: record and abstract | the full PDF was then read in part (Y703) |
| https://arxiv.org/abs/2112.04788v2, https://arxiv.org/abs/2108.01427, https://arxiv.org/abs/2009.00192v1 | abstract pages | PDFs read (Y704, Y712, Y707) |
| McGrath, Blythe & Krackhardt 1997, *The effect of spatial arrangement on judgments and errors in interpreting graphs*, Social Networks 19(3) | **abstract only** (search record; no open full text found) | the open follow-up was read (Y706) |
| Gleicher et al. 2011, *Visual comparison for information visualization*, Information Visualization 10(4) | **abstract only** (Colorado repository record via search) | L'Yi et al. review (Y707), which systematises it |
| Hamada et al. 2005, *Cooking navi: assistant for daily cooking in kitchen*, ACM MM '05 | not read (seen only as a reference in Y711 and an OpenAlex search hit) | the developer's 2003 IPA report (Y710) |
| Chang, Hare, Kim, Agrawala 2017, RecipeScape LBW, CHI EA | not read (cited in Y700 as the sequence-representation precursor) | none |
| ISS-SP-035 (IEICE 2018 poster, 下鵜瀬 et al.); IEICE 2012 並行調理支援 report; Okayama thesis (松島, 2015); ANLP 2025 P3-12 (LLM multi-recipe plans) | search snippets only; not opened | Y709 read as the representative Japanese work |
| Starke et al. 2023 interface study, Berge et al. 2021: PDFs initially unreadable through the fetch tool | compressed PDF | extracted locally from the saved file |
| Food-waste / leftover recipe-suggestion interfaces | only student course projects and a vendor survey found (UW CSE440 projects, an FU Berlin course blog, a Frigidaire survey) | **nothing peer-reviewed found**; none cited as evidence |
| "Visual and textual explanations" mobile ingredient-driven recommender (RecSys 2015 workshop, Macquarie/unibz record) | search record only | not pursued |

## Searches

| language | query | useful? |
| --- | --- | --- |
| en | RecipeScape interactive tool analyzing cooking instructions at scale CHI 2018 | yes (Y700) |
| en | Chang Guillain … RecipeScape pdf arxiv | led to the project page |
| en | Cooking Navi assistant for daily cooking in kitchen Hamada multimedia | partly (Y711, pointer to Y710) |
| en | user study recipe search by ingredients "what to cook" home cooks interface evaluation | partly (pointer to Y704; rest student projects) |
| en | Teng Lin Adamic "Recipe recommendation using ingredient networks" arxiv | yes (Y701) |
| en | Ahn Ahnert Bagrow Barabási flavor network … | yes (Y702) |
| en | node-link vs adjacency matrix readability user study Ghoniem Fekete; Okoe Jianu Kobourov | yes (Y705) |
| en | visualizing recipe steps parallel dependencies timeline home cooks user study multiple dishes | yes (Y703) |
| en | Frummet Elsweiler "What can I cook with these ingredients" | yes (Y704) |
| en | McGrath Blythe Krackhardt effect of spatial arrangement … | yes (Y706; 1997 paper abstract only) |
| ja | 調理支援 レシピ 手順 並行作業 提示 インタフェース 評価 実験 論文 | yes (Y709, Y710); no Japanese presentation-interface user study found |
| en | Gleicher … Visual comparison for information visualization … pdf | partly (Y707) |
| en | HCI study leftovers food waste app "what to cook" fridge inventory … | no (student projects only) |
| en | interactive recipe recommender interface user study ingredient-based exploration visualization explanation | yes (Y708, Y712) |
| en | qualitative study how households decide what to cook for dinner … HCI | partly (Hyland et al. blocked; CHI 2023/2025 and CSCW 2024 family-meal studies found but not read) |
| en (API) | Semantic Scholar citations of DOI 10.1145/3173574.3174025 | yes (forward trail) |

## Citation trail

- **Backward from Y700:**
  - It builds on ingredient and flavour networks (Teng et al. → Y701; Ahn et al. → Y702).
  - It builds on workflow-comparison interfaces (Delta, Kong et al. 2012; Sifter, Pavel et al. 2013: not read).
  - It builds on its own LBW precursor (not read).
- **Forward from Y700** (Semantic Scholar listing of 71 citing works, read as a list of titles only):
  - recipe-graph and procedural-NLP work (*Aligning Actions Across Recipe Graphs*, EMNLP 2021; *50 Ways to Bake a Cookie*, CIKM 2021; *A Graphical Formalism for Reasoning about Substitution in Resource Transforming Procedures*, JAIR 2025): this belongs to the recipe-graph and substitution areas (Y500, Y400);
  - cooking assistance (*Rewriting the Script*, DIS 2023; *A Recipe for Success?*, ASSETS 2024; *Aroma*, UIST 2025);
  - how-to video aggregation (*VideoMix*, IUI 2025), *TastePaths* (IUI 2022), *Recipe 2.0* (ICCC 2023).
  - **No citing work in the listing evaluates a dish-variation map with home cooks**, judged from titles only, so this is not verified.
- **Backward from Y703:**
  - Buykx's overview design came from graphic-designer flowchart recipes, and she cites Wang et al. 2008 recipe graphs as a possible source of the overview (not read).
  - She criticises Mennicken et al. 2010 and Hamada et al. 2005 for rating skill without a method (both not read).
- **Y711 → Y710:** panavi cites Hamada's Cooking Navi; Y710 is the developer's own report.
- **Y704 → earlier taxonomies:** Cunningham & Bainbridge (Google Answers); Vtyurina & Fourney (CHI 2018, 10 participants); Nouri et al. None of these were read.
- **Y707 → Gleicher et al. 2011** (abstract only).
- **Y706 → McGrath, Blythe & Krackhardt 1997** (abstract only).
- **Y708 and Y712** share an author (Starke) and the Trattner food-recommender line. Y701 is cited by the same community (survey arXiv 1809.02862, not read).

## Approach analyses

The six representation families named in the task are analysed one at a time. Each family names the sources that evaluate it. Throughout:
- "Food-prep now" means the Streamlit mindmap (`src/foodprep/ui/graph.py`, built as ingredient → techniques → components → fillers / routes / destinations) and the R4.1/R4.2 workspace.
- "Food-prep data" means the R1–R5 records.

### F1. Ingredient relationship networks (co-occurrence, flavour, substitute networks; Food-prep's current mindmap)

- **E1:**
  - **Unit:** the ingredient. An edge carries statistical association: co-occurrence (Y701), shared compounds (Y702) or review-mined replacement (Y701).
  - **Purpose:** analysis and rating prediction, not decision support.
- **E2:**
  - **Demonstrated:**
    - savory/sweet communities and substitute clusters (Y701);
    - cuisine-dependent compound sharing (Y702);
    - prediction accuracy .79 (Y701).
  - **Claimed, never tested:** that a cook could match a pantry against substitute clusters (Y701 §6.3, §8).
  - **Evidence that the drawing misleads:**
    - Y702 could not draw its own network and showed a filtered backbone;
    - in Y701's drawing the most connected ingredients (egg, salt) sit at the edge;
    - Y706 shows viewers read meaning into position;
    - Y705's advantage for node-link is limited to connectivity tasks;
    - Food-prep's own R4.1 found its trace graph illegible above about 20 relationships (`ux-integrated-r4-1/trace-evaluation.md`).
- **E3, mapping on paper:**
  - **K2:** an ingredient network can show *dried pea – chickpea* as substitutes only if reviews say so. It cannot say that the swap holds for falafel (soaked, ground raw) and not for hummus or soup.
  - **K6:** a context-free cluster like Y701's {mushroom, broccoli, kale, carrot, zucchini} would *propose* curly kale where cabbage leaves are used, which is the case Food-prep rejected (`not_worth_it`).
  - **K5:** broccoli stem would appear as a co-occurrence neighbour of broccoli, not as a material.

**E4** (relevant cases K2, K5, K6):

| aspect | K2 pea falafel | K5 broccoli-stem patties | K6 kale rolls |
| --- | --- | --- | --- |
| a components and joins | cannot: no components | cannot | cannot |
| b intermediate states, readiness | cannot: no states (soaked vs cooked pulse invisible) | cannot | cannot |
| c member after assembly | cannot | cannot | cannot |
| d why a stage exists | cannot | cannot | cannot |
| e alternative routes apart | cannot: a route is not a node | cannot | cannot |
| f substitution and consequences | extend: the substitute edge exists, but without dish context or consequences | extend: stem as substitute of carrot only if mined | cannot: a cluster edge would wrongly endorse kale; no negative edge |
| g start from a held state | cannot: ingredient, not state | cannot (stem is a part, not an ingredient node) | cannot |
| h provenance | extend: edge counts trace to reviews, not to a claim | extend | extend |
| i unknown vs false | cannot: absence of an edge = unknown and false at once | cannot | cannot |
| j what a cook reads | weak: "peas relate to chickpeas"; not "you can make falafel" | weak | misleading: kale looks interchangeable |

- **E5:**
  - Food-prep's mindmap is closer to F1 than to any other family: it starts from an ingredient and fans out. It is richer than F1, because it has techniques and components.
  - R4 transfers (dish-scoped, with verdicts including `not_worth_it` and `rejected`) are strictly more informative than a substitute network.
- **E6:**
  - **Published:** network construction and findings (Y701, Y702); the backbone needed for display (Y702); hubs drawn at the periphery (Y701 Fig. 2); layout-induced inference (Y706); node-link good for connectivity (Y705).
  - **Inferred in R6:** that these networks do not answer "what can I make tonight". No source tested them with cooks.
- **Verdict: not suited** as the decision surface for the home cook. There is no published evidence it helps a cook decide, and there is published evidence that the drawings need filtering and that position is over-read. The substitute-network concept is **already equivalent** in Food-prep (R4 transfers), in a stronger, dish-scoped form. Keep any ingredient graph as a secondary "explore" or trace view, where Y705's connectivity advantage applies.

### F2. Final-product / outcome maps (one dish's many versions; "what can this become")

- **E1:**
  - **RecipeScape (Y700)** uses a structural similarity map of many recipes of *one dish*: clusters of approaches, a prototype per cluster, outliers at the edge.
  - **Y708** uses outcome lists grouped by goal, one labelled list each.
- **E2:**
  - **Y700 demonstrated with analysts:**
    - clusters were read as "ways of cooking the dish";
    - the edge of the map was read as personal or creative variants;
    - adjacent recipes were compared to find replaceable ingredients.
  - **Y700 problems:** the clusters need explanation, and the statistics view assumed knowledge of histograms.
  - **Y708 demonstrated with lay users (online):** grouped lists raise perceived diversity and understandability, at the cost of choice difficulty.
  - **Not demonstrated by either:** any effect on what people actually cook.
- **E3:**
  - **K1 gratin:** Food-prep has *one* documented gratin plus transfers and four alternative sequences, not 500 recipes. A similarity map has nothing to cluster. What a cook needs is the outcome (gratin) with its routes as **named choices**.
  - **K2:** the outcome view for "dried peas" lists pea soup (familiar) and pea falafel (an unfamiliar use of a familiar ingredient) as separate labelled outcomes. Each has its own verdict and its safety gap (Q505).
  - **K7 arancini:** the outcome is shown with two named routes (arancini, supplì).

**E4** (K1, K2, K7; RecipeScape map plus Y708 lists):

| aspect | K1 gratin | K2 falafel | K7 arancini |
| --- | --- | --- | --- |
| a components and joins | extend: Y700's tree has action–ingredient branches, but no assembly of components | extend | extend: nesting (filling in starch mass in coating) not in the tree |
| b states, readiness | cannot: actions only | cannot | cannot (cooled rice from the night before not a node) |
| c member after assembly | cannot | cannot | cannot |
| d why a stage exists | cannot: histograms show *where* an action occurs, not why | cannot | cannot |
| e routes kept apart | preserved: a map point or cluster per recipe, with pairwise comparison | preserved | preserved: two routes as two points |
| f substitution consequences | extend: pairwise diff shows a different ingredient, not its consequence | extend | extend |
| g start from a held state | cannot | cannot | cannot |
| h provenance | preserved: each point is one source recipe, with its text shown | preserved | preserved |
| i unknown vs false | cannot: absent recipes are invisible | cannot | cannot |
| j what a cook reads | for analysts: "typical vs unusual"; for home cooks untested | labelled lists: "other things peas become" (Y708: understandable but harder to choose) | |

- **E5:**
  - Food-prep's R3 constructions and R4 transfers *are* the outcomes, and `foodprep from` gives the reverse direction.
  - What Food-prep lacks is a **view whose first level is the outcome (dish)**, not the ingredient.
- **E6:**
  - **Published:** cluster reading, edge = creative, pairwise comparison use (Y700); diversity, understandability and difficulty trade-off (Y708).
  - **Inferred in R6:** that home cooks would read an outcome-first list better than an ingredient fan-out, and that a similarity map is pointless at Food-prep's scale.
- **Verdict: extend.** Take the *outcome-first organisation* and the *pairwise side-by-side comparison* (Y700). Present outcomes as a few labelled groups (Y708), for example "familiar dishes" and "less usual uses", not as a 2-D similarity map. A map needs hundreds of items and explanations the clusters lack (Y700), and its positions invite over-reading (Y706).

### F3. Material transformation graphs (object/state chains)

- **E1:** no source in this area *visualises* material state chains for cooks. The nearest relatives:
  - Y700's tree, with actions over ingredients;
  - Y703's overview, where each branch ends in a component, and its pictures show the *goal state* of a step;
  - Y711's sensed state (temperature, motion) driving the next instruction.
- **E2:**
  - Y703 shows that goal-state pictures were liked but did not reduce problems or errors (the segmented-with-pictures condition, from the abstract and §7.4.2, not read in full).
  - Y711 shows qualitatively that cooks need cues on motion as well as temperature.
- **E3:**
  - **K1:** "raw slice → blanched almost tender (G16) → layered → baked until no resistance" is a state chain.
  - **K9:** "grated potato → squeezed → juice settles → starch returned" needs a secondary output that rejoins.
  - **K7:** the cooled cooked rice from the night before is a held state.
  - A cook needs each state named with its **done-when check**, which R5 has. Whether it is better drawn as a graph or as a vertical strip per component has no evidence in this area.

**E4** (K1, K7, K9):

| aspect | K1 | K7 | K9 |
| --- | --- | --- | --- |
| a | extend: Y703 branches give components; joins are drawn as merging branches | extend | extend: a recombination edge back into the mass is not in any evaluated design |
| b | extend: Y703 goal-state pictures; Y711 sensed cues; readiness vs doneness not separated anywhere | extend | extend |
| c | cannot: no evaluated design shows a member continuing after assembly | cannot | cannot |
| d | cannot | cannot | cannot |
| e | cannot (one route per drawing) | cannot | cannot |
| f | cannot | cannot | cannot |
| g | cannot | cannot: no "enter here with cooled rice" in any evaluated design | cannot |
| h | cannot | cannot | cannot |
| i | cannot | cannot | cannot |
| j | partly: a goal-state picture says what "done" looks like (liked, no error effect) | | |

- **E5:** Food-prep's R1 (material state) and R5 (intermediate states, keeping times, done-when / failed-if checks) are **ahead of anything evaluated here**.
- **E6:** **Published:** pictures liked without an error effect (Y703, abstract); motion matters (Y711). Everything else is inferred.
- **Verdict: insufficient evidence** on how to *show* state chains to cooks. Keep the representation (Food-prep's), and show it inside F4's overview as the end state of each branch, with its check. Do not show it as a separate graph. This is inferred and should be tested.

### F4. Activity / process diagrams (overview flowchart of component branches; schedules)

- **E1:**
  - **Y703:** the overview flowchart, with one branch per component or sub-goal, ingredients aligned to the steps that use them, and detail on demand.
  - **Y709/Y710:** a task graph with precedence and resources, scheduled into one order and presented a task at a time ("next").
  - **Y704:** the needs that arise during cooking (next step, time, amount, technique).
- **E2:**
  - **Y703 (24 real cooks, controlled):**
    - **preferred:** cooks rated the overview best organised and said it helped them plan parallel work;
    - **fewer errors where components were drawn apart:** the confusing two-component step;
    - **no measured change** in time, parallelism or overall errors;
    - **overview over detail:** cooks glanced at detail and relied on the overview.
  - **Y709:** about 15% shorter computed plans; no user evaluation.
  - **Y710:** claims only.
  - **Y704:** next-step and time needs are frequent and context-dependent.
- **E3:**
  - **K1:** three branches:
    - potato and rutabaga slices → blanch (shown *because* the bake follows: R5 dependency) → layer;
    - cream and garlic;
    - (gratin dish);
    - they join at "layer", then "bake until a knife meets no resistance", with the rutabaga branch marked `cooks_slowly`.
  - **K3:** leaves, rice filling and meat branches join at "roll". After the join, a note: rice finishes in the roll.
  - **K7:**
    - branch 1: rice cooked and cooled *the day before*, a held state;
    - branch 2: filling;
    - branch 3: coating;
    - nesting at assembly.
  - **K9:** the starch-settling branch loops back into the mass.

**E4** (K1, K3, K7, K9; Y703 overview with R5 data on paper):

| aspect | K1 | K3 | K7 | K9 |
| --- | --- | --- | --- | --- |
| a components and joins | preserved: branches per component join (Y703 §7.4.3) | preserved | preserved | preserved |
| b states, readiness | extend: Y703 shows steps and goal pictures; readiness vs doneness needs R5 labels on the branch end | extend | extend | extend |
| c member after assembly | extend: Y703 draws steps after the join, but no "this member keeps cooking" mark | extend: rice finishes in roll | extend | n/a |
| d why a stage exists | extend: one cook said the layout showed the rationale behind timings; R5 dependency text needed | extend | extend | extend |
| e alternative routes apart | cannot in one flowchart; see F5 | cannot | cannot | n/a |
| f substitution consequences | extend: a swapped ingredient would show on its branch; its consequences (blanch time) need R4/R5 | extend: wrapper swap = branch swap | n/a | n/a |
| g start from held state | extend: Y709/Y710 re-plan from current progress; a held state = a completed branch | n/a | extend: cooled rice = finished branch 1 | n/a |
| h provenance | extend: not in Y703; Food-prep's source ids per step | extend | extend | extend |
| i unknown vs false | cannot in Y703 | cannot | cannot | cannot |
| j what a cook reads | preserved: "what do I do next, what can run in parallel" (Y703 qualitative) | preserved | preserved | preserved |

- **E5:**
  - Food-prep's R3 construction (routes of independently processed materials joined by assembly operations) and its R5 sequences contain exactly the data Y703's overview draws.
  - The current UI does not draw it: the mindmap fans out from an ingredient, not from a dish's components.
- **E6:**
  - **Published:** ratings, quotes, error reduction on the mixed-component step, no time effect, quick-detail mode (Y703); computed time saving (Y709); needs taxonomy (Y704).
  - **Inferred in R6:** the R3/R5 → overview mapping, and the marks for after-assembly and readiness.
- **Verdict: adopt the concept.** Y703's component-branch overview is the only representation in this area tested with real cooks cooking. Food-prep has the data, but its interface lacks this view. A **multi-dish scheduler** (Y709/Y710) is **not suited** for now: it was built to minimise time, and there is no published evidence that cooks want or follow it.

### F5. Alternative-route graphs (keeping variants of one dish apart)

- **E1:**
  - **Y707:** juxtaposition (chart-wise or item-wise), superposition or explicit difference.
  - **Y700:** RecipeDeck side-by-side trees with pairwise comparison.
  - **Y708:** separate labelled lists.
- **E2:**
  - **Y707, synthesised from 15 user studies, none on recipes:**
    - separate side-by-side charts are worst for local differences;
    - aligned, item-wise layouts or hybrids are better;
    - a difference shown on its own confuses novices;
    - animating between two very different node-link graphs confuses people.
  - **Y700:** pairwise comparison was used by an expert to find replaceable steps (qualitative).
- **E3:**
  - **K1, four alternative sequences:**
    - one row per stage (slice, pre-cook, layer, bake), routes as columns, aligned item-wise;
    - only the differing cells are marked, such as blanch 10 min vs raw with a covered bake of about 90 min;
    - each column carries its own evidence and verdict.
  - **K1-x and K2-x:** an *unverified combination* has no column of its own. It would appear only as an explicitly unknown cell, so it never looks like a documented route.
  - **K8:** the raw-slice route that was rejected structurally but works with time (G7, G8) appears as a separate column, with its source. The model's false negative stays visible as a disagreement between the record and the structural check.

**E4** (K1, K1-x, K2-x, K8):

| aspect | K1 | K1-x | K2-x | K8 |
| --- | --- | --- | --- | --- |
| a | preserved: stages aligned across routes | preserved | preserved | preserved |
| b | extend: per-cell state labels from R5 | extend | extend | extend |
| c | extend | extend | n/a | extend |
| d | extend: why the blanch exists shown in its cell | extend | extend: "never cook" (Q114) shown against "quick soak by boiling" (Q109) | extend |
| e routes apart | preserved: one column per documented route (Y707 guideline 1: avoid chart-wise juxtaposition) | preserved only if an unverified combination is never drawn as a column | preserved, same condition | preserved |
| f | extend | extend | extend | extend |
| g | extend: enter at a row | extend | extend | extend |
| h | preserved: evidence per column | must show "each half documented, whole not" | same | preserved: the G20/G21 failure and the G7/G8 success both cited |
| i unknown vs false | extend: needs a third cell state (unknown) besides works / fails | extend | extend | extend |
| j | preserved: "which way suits my oven and time" | | | |

- **E5:** R5 already records alternative sequences and R4 records route-level verdicts. Food-prep's interface shows routes as nodes in one force graph, which merges them.
- **E6:**
  - **Published:** the layout guidelines (Y707, from non-food studies); pairwise comparison use (Y700).
  - **Inferred in R6:** that the guidelines transfer to cooking routes; the treatment of unverified combinations.
- **Verdict: adopt the concept** of *aligned item-wise juxtaposition* for routes of one dish. The evidence is indirect: general visualisation studies (Y707) plus one qualitative recipe study (Y700). Do not draw alternative routes in one shared force-directed graph, where they superpose without alignment.

### F6. Component substitution and dependency maps

- **E1:**
  - Substitute networks (Y701).
  - Dependency lines in the Y703 overview: the arrow from a preparation to the step that needs it.
  - Precedence edges in Y709's task graph.
- **E2:**
  - **Y701:** substitution as a mined statistic, with no consequences attached.
  - **Y703:** drawing dependencies apart removed the errors on the mixed step.
  - **Y709:** precedence plus resources gives computable schedules.
  - **No source shows a cook the downstream consequences of a swap.**
- **E3:**
  - **K4:** one filling, two vessels. The swap of vessel changes the vessel branch only ("onion layers slip if overboiled"), and the filling branch is untouched.
  - **K3:** the wrapper swap is the same pattern.
  - **K5:** a new first step, peeling the stem, is a prerequisite on the material branch.
  - **K6:** the swap is shown and refused, with the reason (small leaves, no documented practice).

**E4** (K3, K4, K5, K6):

| aspect | K3 | K4 | K5 | K6 |
| --- | --- | --- | --- | --- |
| a | preserved in a branch overview: the swap replaces one branch | preserved | preserved | preserved |
| b | extend | extend | extend | n/a |
| c | extend | extend | n/a | n/a |
| d | extend: why the leaf is blanched | extend: why the onion is parboiled briefly | extend: peeling exists because the stem skin is tough | extend |
| e | extend: original and swap as two aligned columns (F5) | extend | extend | extend |
| f substitution consequences | extend: highlight changed branch, unchanged branches dimmed (inferred) | extend | extend | preserved only if a refusal can be shown, which Y701 cannot |
| g | extend | extend | extend: "I have broccoli stems" as entry | n/a |
| h | extend: R4 transfer source | extend | extend | extend |
| i | extend | extend | extend | preserved in Food-prep (`not_worth_it`), cannot in Y701 |
| j | "can I swap this, and what else changes" | | | |

- **E5:** R4 transfers carry the swap, its verdict and its reason. R5 carries the dependencies. Neither is drawn as a consequence view today.
- **E6:**
  - **Published:** dependency drawing reduced one error type (Y703); a substitute network exists (Y701).
  - **Inferred in R6:** the consequence-highlight view; the refusal display.
- **Verdict: already equivalent** for the data (R4 transfers are richer than Y701). **Extend** for presentation: show a substitution as a changed branch inside the F4 overview, aligned against the original as in F5. There is no published evaluation of such a view, so its value is untested.

## Answers to Q1–Q6 from this area

- **Q1 (unit; two traversals):**
  - The evaluated cook-facing designs use the *dish with its component branches* as the unit a cook reads (Y703), not the ingredient.
  - The ingredient → dishes direction appears in practice as a search *query* (Y704: participants searched with ingredients), not as a graph to explore.
  - One model with two views is consistent with this evidence, but no source tested both views together.
- **Q2 (complete processes):**
  - Showing parallel components as separate branches with joins is the one process representation that real cooks rated better and that removed errors where components were mixed (Y703).
  - It did not make cooking faster.
  - Readiness vs doneness, members after assembly and secondary outputs (K9) have **no evaluated visual form** here.
- **Q3 (substitution):** in this area substitution was only mined statistically (Y701), with no dish context and no refusals. Nothing found on visualising the consequences of a substitution for cooks.
- **Q4 (alternative routes):**
  - For comparing variants, general visualisation evidence favours aligned, item-wise side-by-side layouts over separate side-by-side charts or animation (Y707). Y700 shows pairwise comparison in use.
  - **Inferred:** an unverified combination (K1-x, K2-x) must never be drawn as a column or path of its own; it appears only as an unknown cell.
  - Nothing found that tests this with cooks.
- **Q5 (reuse of an existing state):**
  - Scheduling systems re-plan from current progress (Y710 claims; Y709 computes).
  - Y703 found that cooks rarely prepare everything first (1 of 24), so a "start from what I have" view must show only the remaining branches.
  - No evaluated interface for "I already have cooled rice / stems / leftover X" was found. Food-waste interfaces found were student projects only. **Nothing peer-reviewed found.**
- **Q6 (visualisation for deciding what to cook):**
  1. **Decide** (what can I make tonight): outcome-first, a few labelled groups, each dish once with its verdict. This is supported indirectly (Y708: grouping raises understandability and diversity, and also difficulty). A similarity map or ingredient network is not supported (Y700 is for analysts; Y701/Y702 are untested with cooks; Y706: positions are over-read; Food-prep R4.1: graphs above about 20 edges are illegible).
  2. **Cook** (what do I do next): the component-branch overview with detail on demand (Y703).
  3. **Vary or swap:** aligned columns per documented route (Y707), with unverified combinations shown as unknown.
  4. **Taste displays:**
     - a displayed taste value shifts ratings without tasting (Y712; β = 2.68 for the taste-map value);
     - so a taste circle or map persuades as well as informs;
     - this supports Food-prep's rule of no new scores, and argues for labelling the circle as documented pairings, not predicted taste (inferred).

### K1–K9 mapped to what a cook needs to see

| Case | Cook's question | What to show | Family | Evidence |
| --- | --- | --- | --- | --- |
| K1 gratin | which way suits my oven and time? | one dish; 4 routes as aligned columns; blanch cell says why it exists; bake done-when | F5 + F4 | Y707 (indirect), Y703 |
| K1-x | can I blanch and then bake long? | an "unknown: each half documented, the combination not" cell; never a route | F5 | inferred |
| K2 pea falafel | what else can dried peas become? | outcome list "familiar: pea soup / less usual: pea falafel", verdict, P15 quality risk, Q505 safety gap stated | F2 | Y708 (indirect) |
| K2-x | can I quick-soak by boiling? | conflict shown: Q109 vs Q114, unknown | F5 | inferred |
| K3 napa rolls | what runs in parallel; can I swap the wrapper? | three branches joining at "roll"; "rice finishes in the roll" after the join; the wrapper swap as a changed branch | F4 + F6 | Y703 |
| K4 onion vessels | does my filling fit another vessel? | one filling branch, two vessel branches aligned; the vessel difference marked | F6 + F5 | Y703, Y707 (indirect) |
| K5 broccoli stems | what can I do with the stems? | entry from the held part; peeling as the first step of the branch | F2 + F4 | inferred; nothing found on leftover interfaces |
| K6 kale rolls | can I use curly kale? | swap shown and refused, with reasons, not silently absent | F6 | Y701 counter-example (a context-free cluster would endorse it) |
| K7 arancini | can I use yesterday's rice? | rice branch shown as complete when held; two routes (arancini, supplì) as columns | F4 + F5 | Y703; Y710 (claimed re-planning) |
| K8 raw-rutabaga gratin | why is this rejected if a source says it works? | rejected record and the G7/G8 working route side by side, each with its source | F5 | inferred |
| K9 latkes | what is this starch step? | a loop from the juice branch back into the mass, labelled | F4 | no evaluated form found |

## Open questions this area leaves

1. **No study puts a dish-first or route-first view in front of home cooks deciding what to cook.**
   - Y703 tested cooking, not deciding.
   - Y708 tested hypothetical choice from lists.
   - Whether an outcome-first view beats Food-prep's ingredient mindmap is untested. That is the core R7 usability question.
2. **Readiness against doneness, members after assembly, and secondary outputs that rejoin (K9)** have no evaluated visual form anywhere found.
3. **Effect of the overview on outcomes.** Y703's overview was preferred but changed neither time nor overall error counts, so the benefit may be confidence and understanding rather than speed. This needs a measure other than time.
4. **Showing an unknown.** Whether cooks distinguish "unknown" from "fails" in a comparison layout is untested. Y707's studies all compare known values.
5. **"Start from what I have" (Q5 / `foodprep from`).** No peer-reviewed interface evaluation was found for leftovers or held intermediate states. Food-waste apps exist mainly as student projects.
6. **Untested territory in Japanese work.** Japanese work found is on computing parallel schedules (Y709) and on situated sensing (Y711). No Japanese user study on *presenting* parallel plans was found, although snippets point to an IEICE 2012 prototype evaluation and a 2018 poster that were not read.
7. **Not read.** Hamada et al. 2005 (Cooking Navi), Gleicher et al. 2011, McGrath et al. 1997, Hyland et al. (blocked), and the CHI 2023/2025 and CSCW 2024 family-meal studies were not read. Any of them could change Q6's answer on how households decide.
