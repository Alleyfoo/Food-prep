# Evidence: Food process and recipe ontologies, operation objectives

- Date read: 2026-11-25 (one interruption from a usage limit; reading resumed the
  same day, nothing re-fetched).
- Method: WebSearch to find sources; WebFetch to read HTML; PDFs that WebFetch
  could not convert were saved and converted locally with `pdftotext`, then read
  as text (marked "repository PDF"). PMC articles behind a reCAPTCHA were read
  as full-text XML through the Europe PMC REST service (marked "Europe PMC
  full-text XML", the same article text as PMC). Frontiers and arXiv HTML read
  through WebFetch returns a model-written digest, not verbatim text; these are
  marked "(via fetch digest)" and their details are less certain. Forward
  citations were taken from the Semantic Scholar API.
- Search languages: English, French, German, Italian. French work was found
  and read (Y111 in French; Y115 French slides; the INRAE PO2 line Y102-Y103
  is French research published in English). German and Italian searches found
  no ontology of culinary processes or food states (see Searches).
- Blocked: every HAL page (hal.inrae.fr, agroparistech.hal.science,
  hal-lirmm) returned an Anubis bot block; PMC returned reCAPTCHA; Springer and
  nature.com redirected to a login; RPI DSpace 403; one INESC-ID PDF 404; one
  KSU host did not resolve. Fallbacks are in the failed-pages table.
- Food-prep files consulted for the mapping: the brief's round summary,
  `docs/research/r5-processing-conditions/README.md` (endpoint kinds, the
  rutabaga gratin table, counts) and case ids in
  `src/foodprep/data/processing_conditions.yaml`. Nothing was edited.

## Sources

### Y100 — https://www.semantic-web-journal.net/system/files/swj3096.pdf
- citation: Damion Dooley, Magalie Weber, Liliana Ibanescu, Matthew Lange,
  Lauren Chan, Larisa Soldatova, Chen Yang, Robert Warren, Cogan Shimizu, Hande
  K. McGinty, William Hsiao. "Food Process Ontology Requirements". Semantic Web
  15(4): 1133-1164, published 2024 (accepted 2022). DOI 10.3233/SW-223096.
  Volume/pages from the Wright State CoreScholar record
  (https://corescholar.libraries.wright.edu/cse/720, read); the journal page
  https://www.semantic-web-journal.net/node/3096 (read) gives submission
  2022-03-18, decision Accept, two reviews (one reviewer calls it a gap
  analysis rather than a survey).
- version read: accepted manuscript PDF from the journal's site (36 pp.),
  read in full. The typeset IOS/SAGE version was not read.
- type: survey / gap analysis with a design proposal (no evaluation).
- E1: reviews process modelling in OBO (OBI planned process, IAO plan
  specification, RO relations), OWL-Time, PROV-O, SOSA/SSN, Exact2, PO2 and
  schema.org Recipe; aims at one generic process model usable for recipes,
  labs and factories (sec. 1.1). Unit: a planned process that executes a plan
  specification, with specified inputs/outputs that are material entities
  carrying qualities that change from input to output (Fig. 11).
- E2 shows (published): a comparison table of process terms across five
  ontologies (Table 1, sec. 4.1); a prototype FoodOn recipe model with
  "ingredient set", "device set", "instruction set" of step specifications
  (Fig. 21, sec. 4.2); a partial "boiled carrots" model, diagram only (Figs.
  22-26). No dataset, no implementation test, no user study.
- Points used below:
  - Process objective as a desired output ("tenderized meat"); any process
    with a similar output "can be inferred to be a potential substitution"
    (sec. 2.1). Choice among them constrained by devices, time, skill.
  - Process-and-object model keeps a provenance trail; it can be projected to
    an object-only view (RO "derives from") or a process-only view (RO
    "directly provides input for"), each losing detail (sec. 2.1.2, Figs. 4-5).
  - A step "must be completed before proceeding to a subsequent dependent
    step"; ordering could in principle be inferred from input dependencies
    (sec. 2.1.3), but OWL reasoners cannot infer step order (sec. 2.1.5).
  - Input/output qualities let one state conditions to continue, e.g. "wait
    until the water is boiling" (sec. 2.1.3); end state of heating sensed by
    sound, sight or thermometer (Fig. 25).
  - OWL cannot assert that a process changed a quality of the same individual;
    input and output instances must be distinct; a shared tracking identifier
    is proposed as a workaround (sec. 2.1.5, Fig. 23, sec. 4.2).
  - Parallel and sequential order by RO Allen relations ("starts with",
    "preceded by"); parthood by "has component process" (sec. 3.1.1).
  - COB types a process instance as "completely executed" or "failed planned
    process"; "There is no 'work in progress' state" (sec. 3.1.2).
  - schema.org Recipe: steps as a list or free text, no concurrency, order
    implicit, built for retrieval (sec. 4.1.5).
  - Exact2 (lab protocols) recognised 83-95% of protocol actions (sec. 3.3,
    reported second-hand).

### Y101 — https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2023.1137961/full
- citation: Damion Dooley, Tarini Naravane, 2023, "Ontological how and why:
  action and objective of planned processes in the food domain", Frontiers in
  Artificial Intelligence 6: 1137961. DOI 10.3389/frai.2023.1137961.
  PMC10352767. Conceptual analysis article; reviewers listed include P. Buche
  (INRAE) and S. Despres.
- version read: Europe PMC full-text XML (PMC10352767), read in full; the
  Frontiers HTML was also read (via fetch digest). The PMC page itself was
  blocked.
- type: primary research (conceptual proposal), no evaluation.
- E1: splits planned food processes into "process by mechanism" (action
  specifications control the material's environment; no absolute end point)
  and "process by objective" (objective specification gives a completion
  metric) (sec. 1, 2.1, Table 1, Figs. 1-4). Purpose: data harmonisation of
  food composition data and dynamic process control (sec. 1).
- E2 shows: Table 1 with ~25 proposed terms (most new, managed in FoodOn's
  spreadsheet templates); a boiling-water reference instance (Fig. 5); a rice
  cooking model at macro and molecular scale (soak, heat in water,
  gelatinisation, pasting, cooling/retrogradation; Figs. 7-8); a schema of
  human and instrument sensing to decide that an objective is reached (Fig. 6).
  Knowledge graph hand-curated; no reasoning test.
- Points used below:
  - Objective specification: often "an expression of the quality(ies) or
    phenotype(s) of the output material" (sec. 1); can also be a proxy such
    as duration, energy or catalyst consumed (sec. 2.1).
  - Mechanism classes "will not specify an absolute threshold upon which to
    complete the process" (sec. 2.1).
  - "processes having equivalent objectives can be swapped" (Table 1 note);
    stove-top and microwave boiling share an objective, differ in mechanism
    (Fig. 4). Claimed, not demonstrated.
  - Recognising that an objective is reached "can be a component objective of
    a larger process" (sec. 1).
  - Food composition data for frozen carrots are comparable only if storing,
    soaking, blanching, boiling and freezing protocols are comparable (sec. 1).
  - Domestic recipes judge completion by time or mouthfeel (sec. 2.3).
  - Future work: OWL reasoning to identify equivalent processes and select
    components by goal and resource constraints (sec. 3).

### Y102 — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10477341/fullTextXML
- citation: Magalie Weber, Patrice Buche, Liliana Ibanescu, Stephane Dervaux,
  Herve Guillemin, Julien Cufi, Michel Visalli, Elisabeth Guichard, Caroline
  Penicaud, 2023, "PO2/TransformON, an ontology for data integration on food,
  feed, bioproducts and biowaste engineering", npj Science of Food 7: 47
  (article number from the Europe PMC metadata; not checked on the publisher
  page). DOI 10.1038/s41538-023-00221-2.
- version read: Europe PMC full-text XML, read in full. nature.com and
  link.springer.com redirected to a login.
- type: primary research + ontology + tools (INRAE, France).
- E1: PO2 core model v2.3 in three parts: Process (process, steps, input and
  output components; each step has a duration), Observation (SOSA/SSN: what
  was measured and how, by which material/method, at which scale), Result
  (values, units) (Results, Fig. 1). "A process can be divided into several
  routes depending on the control parameters or input compositions considered
  in the experimental design" (Results). Steps compose a "process itinerary".
  Purpose: integrating experimental data in food and bioproduct engineering.
- E2 shows (demonstrated): FoodEx2-based component hierarchy (4234 food
  classes, 759 feed), 396 step classes, 33 process classes; four use cases
  with published datasets (milk microfiltration + Bayesian network; biocomposite
  packaging + probabilistic relational models; LCA data retrieval; sensory
  data, in progress) (Discussion, Fig. 9); competency questions turned into
  queries (Methods); tools PO2 Manager (GUI to enter processes, itineraries,
  steps, compositions, observations) and SPO2Q query forms (Fig. 10).
  Limitations stated: high effort to learn PO2; manual data entry is slow and
  error-prone.
- Points used below: observations attach to a process, a step or an
  input/output composition, and a property is tied to an "object of interest"
  (PO2:hasObjectOfInterest) (Results); CQ5 asks how an attribute of an input
  or output changes during a step (Methods); metadata on material and method
  let one decide whether data from different projects are comparable
  (Discussion).

### Y103 — https://ceur-ws.org/Vol-3637/paper11.pdf
- citation: Magalie Weber, Patrice Buche, Liliana Ibanescu, Stephane Dervaux,
  2023, "PO2/TransformON: A New Domain Ontology for Integrating Food, Feed,
  Bio-products and Waste in a Circular and Sustainable Approach", IFOW 2023
  (JOWO 2023), CEUR Workshop Proceedings Vol-3637. DOI none shown.
- version read: repository PDF (CEUR), read in full.
- type: primary research (workshop version of Y102).
- E1/E2: same model as Y102; adds that a step is a sosa:Actuation with a
  temporal duration (sec. 3), that observations are about a process, step or
  input/output composition (sec. 3), and that the step list came from FoodEx2
  plus courses and books (sec. 4.2). No evaluation beyond Y102.

### Y104 — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6550238/fullTextXML
- citation: Damion M. Dooley, Emma J. Griffiths, Gurinder S. Gosal, Pier L.
  Buttigieg, Robert Hoehndorf, Matthew C. Lange, Lynn M. Schriml, Fiona S. L.
  Brinkman, William W. L. Hsiao, 2018, "FoodOn: a harmonized food ontology to
  increase global food traceability, quality control and data integration",
  npj Science of Food 2: 23. DOI 10.1038/s41538-018-0032-6.
- version read: Europe PMC full-text XML; read in parts (sections on food
  products, product relations, analogs, counts), not cover to cover.
- type: ontology + primary research.
- E1: food source, product type and process facets derived from LanguaL;
  over 27,000 classes drawing on 16 OBO ontologies; 9445 product-type classes.
- Points used below: "has ingredient" (component may no longer be
  discernible), "has part" (a food literally has a part of another food,
  unchanged, e.g. apple in a caramel apple), "composed primarily of", "derives
  from" (transformed by a process, e.g. applesauce from apple), "develops from
  part of" (Food products section). FoodOn avoids pre-composed terms such as
  "apple, raw, without skin, sliced, cooked, microwaved"; the cooking method
  goes in a separate field or relation. "has food substance analog" is
  symmetric, with no ratio or quality of substitution (Food analogs section).

### Y105 — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8837940/fullTextXML
- citation: Agnieszka Lawrynowicz, Anna Wroblewska, Weronika T. Adrian,
  Bartosz Kulczynski, Anna Gramza-Michalowska, 2022, "Food Recipe Ingredient
  Substitution Ontology Design Pattern", Sensors 22(3): 1095.
  DOI 10.3390/s22031095. PMC8837940.
- version read: Europe PMC full-text XML, read in full.
- type: primary research (ontology design pattern), Poland.
- E1: substitution modelled at the level of the recipe as a plan
  specification, not of a cooking event (sec. 4.4). A "food recipe ingredient
  substitution (specification)" is a reified n-ary relation with parts:
  conditions (technological, dietary, cultural), objectives (e.g. increased
  fibre), an "ingredient set transformation" and an "instruction set
  transformation" (sec. 4.4). Example: replacing melted butter with regular
  butter adds a melting step (sec. 3.2, Table 4).
- E2: competency questions (sec. 4.2), a pancake example (Tables 3-4),
  alignment to IAO/FoodOn/SIO/AFO (sec. 4.5), pattern published on
  ontologydesignpatterns.org. No implementation test, no dataset, no user study.
- Points used below: substitute (process unchanged) against analog (one or
  more ingredients and the process changed) (sec. 1.1); obligatory
  ingredients via FoodOn "has defining ingredient" or "has obligatory member"
  (sec. 4.4); context-free against in-recipe substitution (sec. 4.4).

### Y106 — https://www.semantic-web-journal.net/system/files/swj3534.pdf
- citation: Charalampos Chelmis, Bedirhan Gergin, "A Knowledge Graph for
  Semantic-Driven Healthiness Evaluation of Online Recipes" (RecipeKG),
  Semantic Web journal submission 3534, header "Semantic Web 0 (2022)";
  final publication status not verified.
- version read: submitted manuscript PDF from the journal site; read in parts
  (abstract, related work, sec. 3.3 on RDF representation).
- type: dataset + knowledge graph.
- E1/E2: Allrecipes recipes as schema.org metadata plus WhatToMake
  `hasIngredient`, FoodOn ingredient types, nutrition and SWRL health scores
  (sec. 3.3). Instructions are not modelled as processes. Its related work
  says FoodKG was then the only recipe-focused knowledge graph (sec. 2).

### Y107 — https://schema.org/Recipe
- citation: schema.org, "Recipe" type definition. Read 2026-11-25; version
  not recorded.
- version read: standard web page (via fetch digest). HowToStep and
  HowToSection pages were not read.
- type: standard.
- E1: `recipeIngredient` (text or list), `recipeInstructions` (text, or an
  ordered list of HowToStep/HowToSection), `cookingMethod` (text), `cookTime`,
  `prepTime`, `performTime`, `totalTime`, `tool`, `supply`, `yield`,
  `suitableForDiet`. No intermediate products, no step-to-ingredient links,
  no parallel branches, no variants on that page.

### Y108 — http://ceur-ws.org/Vol-2195/research_paper_1.pdf
- citation: Cogan Shimizu, Leah McEwen, Quinn Hirt, 2018, "Towards a
  Pattern-Based Ontology for Chemical Laboratory Procedures", WOP@ISWC 2018,
  CEUR Vol-2195, pp. 40-51 (authors and pages as cited in Y100; author names
  also on the PDF's first page).
- version read: repository PDF (CEUR), read in parts (sec. 2 pattern axioms,
  worked example, conclusion).
- type: primary research (ontology design patterns).
- E1: State Transition pattern generalised from Semantic Trajectory; an
  Action acts on exactly one State; a ChemicalActivity starts from one State
  and ends at one State; a State has at most one next State; a Simultaneous
  Action pattern (Fig. 3); EntityWithProvenance aligned to PROV-O (sec. 2).
  E2: one incident report encoded by hand; no evaluation.

### Y109 — https://www.semantic-web-journal.net/system/files/swj1303.pdf
- citation: Charles Vardeman II, Adila Krisnadhi, Michelle Cheatham, Krzysztof
  Janowicz, Holly Ferguson, Pascal Hitzler, Aimee P. C. Buccellato, 2017, "An
  Ontology Design Pattern and Its Use Case for Modeling Material
  Transformation", Semantic Web 8(5): 719-731, DOI 10.3233/SW-160231 (from
  search results and the journal node page https://www.semantic-web-journal.net/node/1303, read).
- version read: accepted manuscript PDF from the journal site; read in parts
  (sec. 1-3 including the cake example; sec. 4 skimmed).
- type: primary research (ontology design pattern).
- E1: MaterialTransformation with Input, Output, Catalyst (input not consumed
  or changed, e.g. bowl, spoon), spatial and temporal co-location of inputs;
  at least one input not among outputs and one output not among inputs
  (sec. 3). E2: worked examples (white cake: mixing then baking, the batter
  output reused as input, "used recursively"; concrete supply chain energy);
  no dataset evaluation.

### Y110 — https://arxiv.org/html/2509.04159v1
- citation: Aarush Kumbhakern, Saransh Kumar Gupta, Lipika Dey, Partha Pratim
  Das, 2025, "Towards an Action-Centric Ontology for Cooking Procedures Using
  Temporal Graphs", arXiv:2509.04159v1. Venue: none listed.
- version read: arXiv HTML v1 (via fetch digest).
- type: primary research (proposal).
- E1: a DAG of parameterised action nodes of three kinds, Process (state
  change), Transfer (environment change), Plate (final assembly,
  "currently undeveloped"); unnamed intermediate products whose provenance is
  recovered by walking back through the graph; interjections that pause or
  repeat; outcome-based termination ("browned and cooked through") (sec. 3).
- E2: one recipe encoded by hand (sec. 4); a comparison rubric designed and
  scored by the authors (sec. 5). No parser, no multi-recipe evaluation.

### Y111 — https://iieta.org/download/file/fid/27490 (landing page https://iieta.org/node/5083)
- citation: Sylvie Despres, "Construction d'une ontologie modulaire.
  Application au domaine de la cuisine numerique", Revue d'Intelligence
  Artificielle (RIA) 30, pp. 509-532, DOI 10.3166/RIA.30.509-532. Year not
  verified (volume 30).
- version read: publisher PDF (IIETA repository), in French; read in parts
  (abstract, sec. 2 knowledge models, sec. 3 modules and OWL profile).
- type: primary research (ontology engineering), France, Open Food System
  project with chefs, Institut Paul Bocuse and SEB.
- E1/E2: eight OWL2 modules (Aliment, Preparation, Materiel, Sensoriel,
  Nutrition, Cuisine, Personne, Unite); foods identified by part and by state
  (raw/cooked, smoked); a "produit" notion groups raw and prepared foods to
  describe transformations; the preparation part of a recipe is a process of
  instructions, a module "en cours de construction". The ontology is not
  published (partner agreement) (sec. 3.3).

### Y112 — http://www.ontobee.org/browser/rdf.php?o=IAO&iri=http://purl.obolibrary.org/obo/IAO_0000005
- citation: Information Artifact Ontology, term IAO_0000005 "objective
  specification" (Ontobee record, imported from OBI).
- version read: ontology term record (via fetch digest).
- type: standard (ontology term).
- E1: "A directive information entity that describes an intended process
  endpoint"; parent "directive information entity"; usage note: it answers
  "why did you do this experiment?"; a 2014 editor note describes the
  objective as marking the process endpoint.

### Y113 — https://arxiv.org/html/2306.09042v1
- citation: Antonis Bikakis, Aissatou Diallo, Luke Dickens, Anthony Hunter, Rob
  Miller, 2023, "A Graphical Formalism for Commonsense Reasoning with
  Recipes", arXiv:2306.09042v1 (10 pp., no venue listed). Found as a forward
  citation of Y100.
- version read: arXiv HTML v1 (via fetch digest); abstract page also read.
- type: primary research (formalism), no implementation.
- E1: a recipe is a labelled bipartite graph of comestible nodes (ingredients,
  intermediates, outputs, by-products) and action nodes, acyclic, each
  comestible with at most one incoming arc, nodes typed from hierarchies
  (sec. 3). Relations between recipes: equivalence (isomorphic), in-out
  alignment (same input and output types), finer-grained, more specific,
  subrecipe (sec. 5). Composition of subrecipes by matching a shared typed
  node, and decomposition into atomic subrecipes (sec. 6). Type substitution
  (replace a node's type; secondary substitutions repair violations of
  acceptability tuples (input type, action, output type)) and structural
  substitution (replace a subrecipe whose boundary matches) (sec. 7-8).
- E2: definitions, propositions and hand examples (pasta with fried onions,
  frozen peas, soup, toast). Durations live inside action labels; timing,
  equipment and quantities are future work (sec. 10).

### Y114 — https://foodkg.github.io/ (also /foodkg.html and /subs.html)
- citation: FoodKG project documentation (Rensselaer). The ISWC 2019 paper
  (Haussmann et al., DOI 10.1007/978-3-030-30796-7_10) was not read.
- version read: implementation documentation pages (via fetch digest).
- type: implementation / dataset.
- E1/E2: built from Recipe1M plus USDA nutrient data and FoodOn links; about
  63 million core triples; substitution data from the Cook's Thesaurus and
  Food.com reviews. The pages do not describe how steps or processes are
  represented.

### Y115 — https://pfia23.icube.unistra.fr/conferences/ic/presentations/session2/IC_2023_Ibanescu.pdf
- citation: Liliana Ibanescu (presenter), "Besoins ontologiques pour la
  transformation des aliments", slides, IC 2023 (Journees francophones
  d'Ingenierie des Connaissances, PFIA 2023). French presentation of Y100.
- version read: slide PDF, read in full (little text).
- type: presentation.
- Adds only: the PO2 domain specialisations listed in French (dairy gels,
  sausage making [IFOW 2020], plant powders, biocomposites, milk
  microfiltration).

### Y116 — https://ceur-ws.org/Vol-4176/ifow-1.pdf
- citation: Magalie Weber, Florian Duclos, Herve Guillemin, Stephane Dervaux,
  Julien Cufi, Michel Visalli, 2025, ConsomON (consumer food-choice
  ontology), JOWO 2025 / IFOW, CEUR Vol-4176 (title line not extracted; the
  abstract names the ontology).
- version read: repository PDF, read in part (abstract, sec. 1-2).
- type: primary research. Peripheral: models consumer choice, not cooking.
  States that PO2/TransformON holds about 9000 SKOS concepts on substances,
  steps, devices, procedures and process parameters (sec. 1).

### Y117 — https://arxiv.org/abs/2509.23776
- citation: Ebrahim Norouzi, Sven Hertling, Jorg Waitelonis, Harald Sack, 2025,
  "Semantic Representation of Processes with Ontology Design Patterns",
  arXiv:2509.23776v1 (SeMatS@ISWC per Semantic Scholar; not verified).
- version read: abstract only.
- type: survey of process ontologies for materials science (Germany, FIZ
  Karlsruhe); a forward citation of Y100. Not used as evidence.

## Failed pages and abstract-only

| URL or query | why | fallback tried |
| --- | --- | --- |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC10352767/ | reCAPTCHA page | Europe PMC full-text XML (read, Y101) and Frontiers HTML (read) |
| https://hal.inrae.fr/hal-03896435v1/document (Y100 preprint) | Anubis bot block | journal-site accepted manuscript (read, Y100) |
| https://link.springer.com/10.1038/s41538-023-00221-2, https://www.nature.com/articles/s41538-023-00221-2 | login redirect | Europe PMC XML (read, Y102) |
| https://public-pages-files-2025.frontiersin.org/.../frai.2023.1137961/text | only metadata and abstract returned | /full page and Europe PMC XML |
| https://agroparistech.hal.science/hal-03013147 (Buche et al. 2020, "Food transformation process description using PO2 and FoodOn", IFOW 2020) | Anubis bot block | none found; **not read** |
| https://hal-lirmm.ccsd.cnrs.fr/lirmm-01092185v1/document (Muljarto et al. 2014, Onto-FP, winemaking, MTSR 2014, CCIS 478, DOI 10.1007/978-3-319-13674-5_30 per search result) | Anubis bot block | none; **not read** (cited by Y111 as its intended process module) |
| Ibanescu et al. 2016, PO2 dairy gels, MTSR 2016, DOI 10.1007/978-3-319-49157-8_13 | HAL record only in search; HAL blocked | **not read**; PO2 read through Y102-Y103 |
| https://dspace.rpi.edu/items/2322e8ed-4227-4667-9113-69ec0748fb9f (FoodKG ISWC 2019) | HTTP 403 | project documentation (Y114); **paper not read** |
| https://www.inesc-id.pt/ficheiros/publicacoes/3615.pdf (Batista et al. 2006, cooking ontology with "food state", per search snippet only) | HTTP 404 | none; **not read**, no claim made |
| https://daselab.cs.ksu.edu/sites/default/files/swj1303.pdf | DNS failure | journal-site PDF (read, Y109) |
| https://www.semantic-web-journal.net/system/files/swj3096.pdf, swj1303, swj3534, CEUR PDFs | WebFetch could not read PDF text | saved PDF converted with pdftotext and read |
| https://arxiv.org/abs/2509.23776 (Y117) | not pursued (materials science) | abstract only |
| "A commonsense reasoning framework for substitution in cooking", Data & Knowledge Engineering 2026, DOI 10.1016/j.datak.2026.102558 | seen as a title in Semantic Scholar forward citations of Y100 only | **not read**; belongs to the substitution area |
| schema.org HowToStep / HowToSection pages | not fetched | Recipe page only (Y107) |

## Searches

| language | query | useful? |
| --- | --- | --- |
| en | "Food process ontology requirements" Semantic Web journal | yes (Y100 pages) |
| en | "Ontological How and Why" action and objective of planned processes in the food domain | yes (Y101) |
| en | PO2 Process and Observation Ontology food science dairy gels Ibanescu pdf hal | yes (leads; HAL blocked) |
| en | PO2/TransformON npj Science of Food 2023 ... | yes (Y102, Y103) |
| en | "Food transformation process description using PO2 and FoodOn" ceur-ws | partly (Y115, Y116; target blocked) |
| en | FoodKG semantics-driven knowledge graph food recommendation Haussmann ISWC 2019 pdf | partly (Y106, Y114) |
| en | "An ontology design pattern and its use case for modeling material transformation" ... | yes (Y109) |
| en | Muljarto Salmon Neveu Charnomordic Buche 2014 ontology-based model for food transformation processes winemaking | metadata only (Onto-FP not read) |
| it | ontologia ricette cucina processi di preparazione stato ingredienti ontologia italiana | no: no Italian process ontology found (only recipe-writing rules, theses on historical recipes) |
| de | Ontologie Kochrezepte Zubereitungsschritte Zustand Zutaten Wissensreprasentation Kochen | no: no German ontology of preparation states found (a Graz DH paper on historical recipes and a KIT robot thesis surfaced, not read) |
| fr | ontologie recettes de cuisine operations culinaires etats des aliments representation des connaissances | yes (Y111, Y110; Batista 2006 lead failed) |
| API | Semantic Scholar citations of Y100, Y101, Y102 | yes (Y113, Y117, Y115 title) |

## Citation trail

- Backward from Y100: PO2 (Y102, Y103; the 2016 MTSR paper not read), Exact2
  (reported only through Y100), OBI/IAO (Y112), Shimizu et al. (Y108, ref.
  [35]), schema.org (Y107), FoodOn (Y104), Lawrynowicz et al. (Y105, ref.
  [14]), Beetz et al. "Robotic roommates making pancakes" (ref. [4], left to
  the FOON/robotics area), FTTO and BPMN traceability (refs. [22-23], not read;
  Y100 says FTTO could not be obtained by its own authors either).
- Backward from Y109: Semantic Trajectory pattern (also the root of Y108's
  State Transition pattern); not read.
- Backward from Y111: Muljarto et al. 2014 Onto-FP (intended as the process
  module; blocked).
- Forward from Y100 (Semantic Scholar): Y101, Y105, Y113 (read); Y115 (French
  IC 2023 talk, read); Y117 (abstract); DKE 2026 substitution framework
  (title only); Munch et al. 2022 ESWA (PO2 + probabilistic models, not read).
- Forward from Y101: only three 2026 citing items, none on cooking processes.
- Forward from Y102: 15 items, mostly datasets and FAIR data; "OBO Foundry Food
  Ontology Interconnectivity" (JOWO 2024) seen as title only.
- No source in this area cites the Japanese recipe-flow work or the Trier CBR
  work; those are covered by other R6 areas.

## Approach analyses

Food-prep terms used below: R1 operation on a material (part + state flags),
three-valued applicability with reasons, fractions; R3 route = materials (op
chains) + assemblies (six joins, roles) + result; R4 transfer = swapped material
on a documented route, re-validated, verdict; R5 sequence = steps with endpoint
kind (readiness/doneness), done-when / failed-if checks, per-source times,
dependency links, conflicts kept as versions, alternative sequences,
intermediate states with keeping times, `from_state`.

### A. OBO planned-process model and the FoodOn recipe prototype (Y100, Y104, Y112)

- **E1** Unit: a planned process (instance) that executes a plan specification
  (information entity); specified inputs and outputs are material entities with
  qualities. A recipe is a plan specification with ingredient set, device set
  and instruction set of step specifications (Y100 sec. 4.2). Product relations
  from FoodOn: has ingredient, has part (unchanged), derives from (Y104).
  Purpose: knowledge integration and traceability across domains.
- **E2** Demonstrated: term comparison (Y100 Table 1); FoodOn as a populated
  ontology (Y104). Claimed/proposed only: the recipe model (diagram), the
  boiled-carrots model (partial diagram); no dataset, no test.
- **E3 mapping**
  - K1: plan spec "rutabaga gratin" with steps peel, slice, blanch, layer, bake;
    process instances linked by "directly provides input for"; the layered
    gratin is a new material; the rutabaga inside it "derives from" the blanched
    slices. Covered and uncovered baking as component processes; durations by
    OWL-Time. The two doneness conflicts would be two plan specifications.
  - K2: soak, grind, form, fry as material processing; chickpea or dried pea as
    specified input; "has food substance analog" between them (symmetric, no
    context, Y104).
  - K3/K4: leaves or onion layers "has part" of the roll/farci only if
    unchanged; the bake changes them, so "has ingredient" or a derives-from
    chain applies; the container role could be an RO role on the input (Y100
    sec. 3.1.1 role qualification).
  - K7: cooled cooked rice is the output of one process instance and the input
    of forming the next day; two routes = two plan specifications.
  - K9: a separating process with two outputs (liquid, solids), a settling
    process on the liquid, then a combining process taking the starch and the
    mass: a DAG of instances, representable.
- **E4** (cases in brackets)

| aspect | verdict | reason |
| --- | --- | --- |
| a components and joins [K3, K7] | preserved | processes plug together on shared input/output entities (Y100 Fig. 26); join kinds only as process classes, not six typed joins |
| b intermediate states, readiness/doneness [K1, K7] | extend | intermediates are output entities with qualities; no readiness/doneness distinction anywhere in Y100/Y104 |
| c member after assembly [K1, K3] | cannot (natively) | OWL cannot say the same rutabaga changed; distinct individuals plus a tracking identifier (Y100 sec. 2.1.5) |
| d why a stage exists [K1] | cannot | objective specs say what a step must produce, not that a later step needs it (Y100, Y112) |
| e alternative routes kept apart [K1, K7] | preserved | separate plan specifications; provenance via information entities (inferred in R6) |
| f substitution consequences [K2, K4] | cannot | analog relation has no context (Y104); nothing propagates |
| g start from a state I have [K7] | extend | "derives from" chains can be queried backward; not discussed (inferred) |
| h provenance per claim | extend | curator/definition sources on terms (Y100 sec. 1.2); claims inside recipes not addressed |
| i unknown vs false | preserved in principle | OWL open world (inferred in R6; not discussed in Y100) |
| j reader deciding what to cook | cannot | built for data integration, not for cooks |

- **E5** Meets R1 (op on material -> new state; FoodOn's refusal of pre-composed
  terms like "apple, raw, ... cooked, microwaved" matches R1's part + state
  flags) and R3 (op chains, joins). Y100's object-only / process-only
  projections (Figs. 4-5) describe what Food-prep does with `Material.key()`
  (object view, history dropped) and R5 sequences (process view).
- **E6** Published: Y100 secs. cited; Y104 relations. Inferred in R6: route
  separation via plan specs, open-world reading, all K mappings.
- **Verdict**: *already equivalent* for the process/material/fraction core
  (Y100, Y104 vs R1/R3); *not suited* as a replacement (purpose is cross-domain
  data integration; its own authors show only diagrams). One concept to
  *extend* with: state in Food-prep's documentation that `Material.key()` is
  the object-only projection that deliberately drops history (Y100 sec.
  2.1.2 names exactly what that projection loses). The FoodOn split "has part
  (unchanged)" against "has ingredient (no longer discernible)" (Y104) is a
  useful vocabulary for R3 joins, but neither relation covers a discernible
  member that changed, which is the R3 known gap; nothing better was found.

### B. Objective against mechanism (Y101, with Y112 and Y100 sec. 2.1)

- **E1** Unit: planned process classified twice: by mechanism (action
  specifications control the environment; no end point) and by objective
  (objective specification: output qualities or a proxy such as duration).
  Purpose: harmonise food-processing data; support control that starts/stops
  a mechanism when an objective threshold is reached.
- **E2** Demonstrated: a proposed hierarchy (Table 1, Figs. 1-4) and two worked
  models (boiling water, rice). Claimed: swapping processes with equivalent
  objectives; OWL inference of equivalent processes (future work, sec. 3).
- **E3 mapping**
  - K1: blanch = heating in water (mechanism) + objective "crisp-tender,
    softened slightly, not fully cooked" (R5 done-when); bake = direct heating
    of container + objective "some give" or "no resistance" (two objective
    specifications, kept as versions). The raw-slice route (G7, G8) reaches the
    same gratin-level objective by a longer bake; an objective-level index
    would show both routes under "rutabaga tender in gratin".
  - K2 and K2-x: soak's objective "hydrated pulse". A 5-min boil (Q109) and an
    overnight soak share that objective, so Y101's swap rule would allow the
    boil into the raw-soaked route, which Q114 forbids. The swap is only safe
    if the objective specification lists every output quality the next steps
    rely on (here: hydrated and not cooked). Inferred in R6.
  - K7: cooling cooked rice overnight: objective "firm, cool, shapeable mass";
    Y101's rice model describes retrogradation on cooling as a molecular
    mechanism (sec. 2.2), the same change seen from the food-science side.
  - K8: a structural check that ignores duration accepts the raw route and its
    failure equally; Y101 allows an objective expressed as a duration proxy
    (sec. 2.1), which is where R5 times sit.
- **E4**

| aspect | verdict | reason |
| --- | --- | --- |
| a components and joins | extend | combining/separating mechanisms exist (Table 1); no assembly roles |
| b readiness/doneness [K1, K7] | extend | objective specs give endpoints; "objective reached" may be a component of a larger objective (sec. 1), but readiness vs doneness is not named |
| c member after assembly [K1, K3] | cannot | not addressed |
| d why a stage exists [K1] | extend | gives the local "why" (desired output, Y112 "why did you do this"); not the downstream dependency that R5 records |
| e alternative routes [K1] | preserved | polyhierarchy: one objective, several mechanisms (Fig. 4) |
| f substitution consequences [K2-x] | cannot | swap by equivalent objective has no check of downstream needs (inferred) |
| g start from a state | extend | an objective-indexed library is proposed (sec. 3), not built |
| h provenance | extend | protocol instance graph for provenance of data (sec. 2.3); not per claim |
| i unknown vs false | not addressed | |
| j reader | cannot | not a user-facing model |

- **E5** R1 operations are mostly mechanism-plus-default-objective in one
  name (e.g. "blanch"); R5 done-when checks are objective specifications, and
  R5 per-source times are objective proxies in Y101's sense. R5 dependency
  links ("the blanch exists because of the bake") have no counterpart in Y101
  or OBO: Y101's "why" is the step's own output, Food-prep's is a later step's
  need.
- **E6** Published: definitions, swap claim, proxies, nested objectives (Y101,
  Y112). Inferred in R6: K mappings, the K2-x failure of objective swapping,
  the readiness reading of nested objectives.
- **Verdict**: *extend*. Food-prep already records objectives (done-when) and
  proxies (times) per step; what it lacks is the explicit split of an R1
  operation into a mechanism and an objective, which would let documented
  alternatives that reach the same objective by different mechanisms be
  grouped (K1 alternative heat routes). Y101's swap rule itself is *not
  suited*: it is unevaluated, and on K2-x it licenses a combination a source
  forbids, against Food-prep's documented-practice-first rule.

### C. PO2 and PO2/TransformON (Y102, Y103; INRAE, France)

- **E1** Unit: a transformation process made of steps (unit operations, each
  with a duration) with input and output compositions; observations (what was
  measured, how, by which material and method, at what scale) attached to a
  process, a step or a composition, with an object of interest; processes
  split into routes by control parameters or input compositions. Purpose:
  integrating experimental and industrial data for reuse and prediction.
- **E2** Demonstrated: populated vocabularies and four use cases with
  published datasets and probabilistic models (Y102 Discussion). Not shown:
  domestic cooking or recipes (pizza appears only as competency questions,
  Y102 Methods).
- **E3 mapping**
  - K1: process "rutabaga gratin" with itineraries (blanch 3-10 min then bake;
    raw slices with ~90 min covered bake). Each source's time and check is an
    observation in its own dataset (DCAT metadata); "some give" and "no
    resistance" are two observations of the same attribute with the rutabaga
    member as object of interest at the bake step, so the conflict stays as
    two results. The K8 failure ("still crunchy", G20, G21) is an observation
    on the raw itinerary's output: PO2 records negative outcomes as ordinary
    results.
  - K2: chickpea and dried pea as two input compositions of one process, i.e.
    an experimental design factor; the quality risk (P15 dry, hard) as an
    observed attribute.
  - K9: the squeeze step outputs juice and pulp compositions; a settling step
    outputs starch; a mixing step takes starch and pulp: representable.
  - K3/K4: assemblies are compositions; wrap, contain, layer are not
    distinguished (would need step classes).
- **E4**

| aspect | verdict | reason |
| --- | --- | --- |
| a components and joins [K3, K9] | extend | input/output compositions per step; no join roles |
| b intermediate states, readiness/doneness [K1, K7] | extend | intermediates observable (CQ4, CQ5); no endpoint kind |
| c member after assembly [K1, K3] | preserved (inferred) | an observation's object of interest can be a component inside the step's input or output composition (Y102 Results); not shown for culinary assemblies |
| d why a stage exists | cannot | no dependency or objective relation |
| e alternative routes with evidence [K1] | preserved | routes/itineraries per design; datasets carry metadata (Y102) |
| f substitution consequences [K2] | extend | substitution only as a design factor whose effects are observed, not propagated |
| g start from a state | extend | query by composition is possible (SPO2Q), not a feature |
| h provenance | preserved | dataset-level DCAT metadata, replicates (Y102) |
| i unknown vs false | not addressed | missing data handled by moving up the hierarchy (LCA use case, Y102) |
| j reader | cannot | expert data entry and query tools only |

- **E5** Itineraries = R3 routes / R5 alternative sequences; observations with
  per-dataset provenance = R5 per-source times and checks with citations.
  PO2 has no endpoint kind, no dependency links and no applicability.
- **E6** Published: model parts, routes sentence, counts, use cases, tools
  (Y102, Y103). Inferred in R6: all K mappings, the member-observation reading.
- **Verdict**: *already equivalent* for routes and per-source observations;
  *not suited* as a whole (built for quantitative experimental data in
  engineering). One concept to *extend* with: PO2's object of interest, i.e.
  record in an R5 check which material it is about when that material is a
  member inside an assembly (the rutabaga in the gratin, the rice in the
  roll). This addresses the R3 known gap only as a way of placing checks; it
  does not model what the member undergoes.

### D. Recipe ingredient substitution design pattern (Y105)

- **E1** Unit: a reified substitution specification attached to a recipe
  (plan specification): replaced and replacing ingredient specifications,
  conditions, objectives, ingredient-set and instruction-set transformations.
  Purpose: a schema for recommending substitutes.
- **E2** Demonstrated: the pattern and one pancake example. No implementation
  evaluation, no data.
- **E3 mapping**
  - K2: substitution chickpea -> dried peas; condition (technological): binds
    as a raw pulse paste without additive; objective: availability; ingredient
    set transformation; instruction set transformation (soak time). The
    outcome (P15 dry, hard) and the verdict have no slot.
  - K4: onion halves for courgette vessels; technological condition: must hold
    as a container; instruction set transformation: boil briefly so layers do
    not slip.
  - K6: no slot for "not worth it" or "no documented practice"; only possible
    substitutions are listed.
  - K8: raw rutabaga would be an analog in Y105's terms if the process
    changes (long covered bake), a substitute if it does not (sec. 1.1).
- **E4**

| aspect | verdict | reason |
| --- | --- | --- |
| a | extend | recipe-level sets only |
| b | cannot | no states |
| c | cannot | |
| d | extend | substitution objectives, not stage reasons |
| e | extend | substitute vs analog distinguishes same-process from changed-process variants |
| f substitution consequences [K2, K4] | preserved | instruction set transformation names the knock-on step changes |
| g | cannot | |
| h | cannot | no provenance slot |
| i | cannot | absence of a substitute is not represented |
| j | extend | competency questions are user questions ("what can replace X given my diet") |

- **E5** Equivalent to an R4 transfer without its verdict and citations; R4
  is richer (re-validation, worth_cooking / not_worth_it / rejected, sources).
- **E6** Published: pattern parts and the substitute/analog distinction
  (Y105). Inferred: K mappings.
- **Verdict**: *already equivalent* (R4 transfers). Worth taking as
  vocabulary (*extend*): the substitute/analog split, i.e. whether the swap
  keeps the documented process or needs a changed one, which separates K2
  (pea falafel, same route) from K8 (raw rutabaga, changed bake).

### E. State-transition and material-transformation design patterns (Y108, Y109)

- **E1** Unit: a transformation with inputs, outputs and catalysts (tools not
  changed), co-located in space and time (Y109); a state with at most one next
  state, actions acting on one state, simultaneous actions (Y108). Purpose:
  reusable modelling blocks (energy accounting; lab hazard analysis).
- **E2** Worked examples only (cake, concrete, one lab incident).
- **E3** K1: slicing, blanching, layering, baking as recursive transformations
  (Y109's cake: batter output reused as input). K9: two outputs, one reused:
  allowed (at least one output not among inputs). Y108's "at most one next
  state" cannot hold K9's split (one material, two successor states).
- **E4** a preserved (inputs/outputs), b extend, c cannot, d cannot, e cannot,
  f cannot, g extend, h extend (Y108 PROV-aligned entity), i not addressed,
  j cannot.
- **E5/E6** Matches R1 (operation on material -> new state, fractions);
  published Y108-Y109, mappings inferred.
- **Verdict**: *already equivalent* to R1.

### F. Bipartite recipe graph with composition and substitution (Y113)

- **E1** Unit: typed comestible and action nodes in an acyclic bipartite
  graph; relations between recipes (equivalent, in-out aligned, finer-grained,
  more specific, subrecipe); composition and decomposition; type and
  structural substitution with secondary repairs. Purpose: commonsense
  reasoning over recipes.
- **E2** Definitions and propositions only; no implementation, no data; timing,
  equipment, quantities deferred (sec. 10).
- **E3 mapping**
  - K7: "cook and cool rice" composes with "form, fill, coat" through the
    shared node "cooled cooked rice"; the boiled and risotto routes are in-out
    aligned but not isomorphic, which is a formal statement of "two routes to
    the same dish".
  - K1-x: composing the 10-min blanch with the raw-slice long bake needs the
    bake's input type "raw slice" to match "blanched slice"; strict type
    equality blocks it, the subtype generalisation the authors plan would let
    it through. Inferred in R6.
  - K2-x: if the node type is "soaked chickpea", the boiled quick-soak output
    composes with the raw-soaked route and the composition is accepted, though
    Q114 forbids it. Node identity by type collapses history. Inferred in R6.
  - K2: type substitution chickpea -> dried pea; acceptability tuples
    (pulse, grind, paste) must hold; secondary substitutions repair the rest.
  - K9: settled starch is an intermediate with one incoming arc, reused
    downstream: representable.
- **E4** a preserved (composition), b extend (states only as types), c cannot,
  d cannot, e extend (in-out alignment identifies alternatives; evidence not
  attached), f preserved in principle (secondary substitution), g preserved
  (compose from an existing typed node), h cannot, i cannot (acceptability
  tuples are binary), j cannot.
- **E5** Acceptability tuples are R1 applicability made binary and
  hand-written; composition by shared typed node is Food-prep's `from_state`
  through `Material.key()`; secondary substitution is R4 re-validation.
- **E6** Published: definitions (Y113). Inferred: K mappings and the K1-x /
  K2-x readings.
- **Verdict**: *extend* (the comparison relations, especially in-out
  alignment and "finer-grained", could name how R5 alternative sequences and
  R3 routes relate) and *insufficient evidence* as a working method. Its K2-x
  behaviour is the clearest illustration in this area of the Q5 risk that
  Food-prep's key-based equivalence shares.

### G. Action-centric temporal cooking graph (Y110)

- **E1** Process/Transfer/Plate nodes, unnamed intermediates with provenance
  by backward traversal, interjections, outcome-based termination.
- **E2** One recipe by hand, self-scored rubric.
- **E3** K1: blanch and bake as Process nodes with temperature, duration and
  outcome condition; layering would be Plate, which is undeveloped. K9:
  separation output reused: representable as a DAG.
- **E4** a extend (Plate undeveloped), b extend (outcome termination, no
  endpoint kind), c cannot, d cannot, e cannot (only orderings of one partial
  order), f cannot, g extend, h cannot, i cannot, j cannot.
- **Verdict**: *insufficient evidence*. Its parts that work are already in R5
  (outcome checks instead of fixed times).

### H. schema.org Recipe and recipe knowledge graphs (Y107, Y106, Y114)

- **E1** A recipe document: ingredient list, ordered instruction text, a
  cookingMethod string, durations. KGs add ingredient links (FoodOn, USDA) and
  scores; FoodKG adds substitution pairs from reviews and a thesaurus.
- **E2** Large deployed data (FoodKG ~63M triples, Y114); no process model.
- **E3** K1-K9: only as ingredient lists and instruction strings; no
  intermediates, members, alternatives or conditions.
- **E4** a-i cannot (instructions are text; Y100 sec. 4.1.5 says the same);
  j preserved only as display of a recipe page.
- **Verdict**: *not suited* for representation. Possibly relevant to R7 as an
  export format for a finished route (inferred in R6, not evaluated).

### I. Modular digital-kitchen ontology (Y111, French)

- **E1** OWL2 modules for food (part and state: raw/cooked, smoked),
  preparations, equipment, sensory qualification, nutrition; preparation as a
  process of instructions (module unfinished).
- **E2** Built with chefs, Institut Paul Bocuse and SEB; unpublished.
- **E3** K5: "stem" as a part of broccoli with state "peeled"; matches R1.
  Processes: no content to map.
- **Verdict**: *already equivalent* for part + state identification (R1);
  *insufficient evidence* for processes (not published).

## Answers to Q1-Q6 from this area

- **Q1 unit; one model, two traversals.** The sources converge on one unit:
  a process (step) with typed input and output materials carrying qualities,
  plus a separate plan specification (Y100 sec. 3.1, Y102, Y105 sec. 4.4,
  Y109). Y100 (sec. 2.1.2, Figs. 4-5) states that one process-and-object graph
  can be read as an object-only view (what derives from what) or a
  process-only view (which process feeds which), which is the
  ingredients-to-dish and dish-to-how pair in a single model; it also says what
  each projection loses. Y101 adds a third axis, objective, from which one
  could ask "what processes achieve this?". Y113 defines composition and
  decomposition on one graph. None of these was tested on a body of recipes;
  PO2 is the only model used on real data, and not for cooking.
- **Q2 complete processes.** Parameters and durations: OWL-Time and process
  profiles (Y100 secs. 2.1.3, 3.2), control parameters and observations (Y102).
  Objectives: IAO objective specification, "intended process endpoint" (Y112);
  objective vs mechanism (Y101). Observable completion: sensing by sound, sight
  or thermometer (Y100 Fig. 25), human or instrument (Y101 Figs. 6-7), outcome
  termination (Y110). Failure: COB "failed planned process", with no
  work-in-progress state (Y100 sec. 3.1.2); this marks a process instance, not
  an observable failure of the material as R5 does. Parallel order: Allen
  relations (Y100), simultaneous action (Y108); OWL cannot infer step order
  (Y100 sec. 2.1.5). Intermediate states: everywhere, as output entities.
  **Readiness against doneness: nothing found**; the nearest is Y101's remark
  that reaching an objective can be part of a larger objective. Members after
  assembly: no source models a discernible member that keeps changing; Y104's
  "has part" assumes it is unchanged and Y100 shows OWL cannot keep its
  identity across a change.
- **Q3 substitution.** Context-free analog relation (Y104) against a reified
  substitution with conditions, objectives and instruction-set changes (Y105);
  process substitution by equivalent objective (Y100 sec. 2.1, Y101, claimed);
  secondary substitutions that repair violated acceptability tuples (Y113,
  formal only). Only Y113 defines how an inconsistency introduced elsewhere is
  found; none is evaluated.
- **Q4 alternative routes.** Routes split by control parameters or input
  compositions in PO2 (Y102), several plan specifications for one output
  (Y100), polyhierarchy of mechanisms under one objective (Y101), in-out
  alignment (Y113). No source marks a combination of documented steps as
  unverified; Y101's swap rule would generate such combinations (K2-x).
- **Q5 reuse and histories.** Found: (1) Y101 sec. 1: data on a state such as
  "frozen carrots" are comparable only if the soaking, blanching, boiling and
  freezing protocols are comparable, so equal names do not mean equal states;
  (2) Y100 secs. 2.1.2 and 2.1.5: the object-only view drops the "how", and OWL
  cannot even keep one material's identity through a change, so history is
  kept as a provenance trail of distinct entities or a tracking identifier;
  (3) Y102: metadata on material and method decide whether data are
  comparable; (4) Y113: node identity by type, so two histories that end in
  the same type are interchangeable by construction (K2-x shows the risk);
  (5) Y110: provenance of an intermediate by walking back its graph. No source
  defines when two different histories give interchangeable states.
  Food-prep's `Material.key()` equivalence makes that claim implicitly; the
  sources say it is a projection that loses information, not that it is wrong.
- **Q6 visualisation.** Nothing found for a person deciding what to cook. Only
  modelling diagrams (Y100, Y101) and expert data-entry and query tools
  (PO2 Manager, SPO2Q, Y102).

## Open questions this area leaves

1. Should R5 checks name the material they observe (PO2 object of interest)
   when it is a member inside an assembly, and is that enough for the R3 gap
   or only a way to file checks?
2. Can R1 operations be split into mechanism and objective without
   re-coding R1, e.g. by grouping R5 alternative sequences under a shared
   objective? Which K1 alternatives would group, and does grouping invite the
   K2-x error?
3. What would an objective specification need to contain to make a
   same-objective swap safe (K2-x shows "hydrated" is not enough)? No source
   answers this.
4. When are two states with different histories interchangeable (Q5)? The
   ontologies record history but never decide this; Food-prep's key-based
   `from_state` decides it silently.
5. Readiness against doneness has no counterpart in any ontology read; is
   that a gap in the literature or a Food-prep-specific distinction? Other
   areas (robotics, industrial batch) may answer.
6. Not read and possibly relevant: Onto-FP (Muljarto et al. 2014, winemaking
   itineraries, French INRA), Buche et al. 2020 (PO2 + FoodOn, sausage
   making), the PO2 2016 paper, FoodKG's ISWC paper, Batista et al. 2006
   ("food state"). All blocked or missing.
