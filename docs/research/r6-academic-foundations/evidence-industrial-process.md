# Evidence: industrial batch processing, production planning and process diagrams applied to food

- Date read: 2026-11-25.
- Method: web search to find sources; WebFetch to read them. Where WebFetch
  returned a PDF it could not decode, the saved PDF was converted locally with
  `pdftotext` and the relevant chapters read from the text. Every source below
  says which version and which parts were read.
- Search languages: English, Finnish (Ruokavirasto self-monitoring), German
  (NAMUR NE 33). No French, Italian or Japanese industrial-process source was
  reached; Grafcet's French origin is covered only through the Lund thesis
  (Y602). That is a gap.
- Blocked: the ISA-88 standards themselves (paywalled; free previews of Parts 3
  and 4 read instead), ScienceDirect (403), Springer (login redirect), MDPI
  (403), core.ac.uk (403), econbiz and mediaTUM (Anubis bot wall), FAO's own
  repository (403; the same FAO PDF was read from a university mirror). Details
  in "Failed pages".
- Scope note: none of these frameworks was built for a home cook. All mappings
  of K1-K9 below are made on paper in R6 and are marked **inferred** unless a
  Y id is given for the capability.

## Sources

### Y600 — https://www.isa.org/standards-and-publications/isa-standards/isa-88-standards
- citation: ISA (International Society of Automation), "ISA-88 Standards"
  catalogue page, n.d. (accessed 2026-11-25).
- version read: publisher web page (catalogue only).
- type: standard (catalogue).
- E1/E2: lists the parts. Part 1 Models and Terminology (ISA-88.00.01-2010);
  Part 2 Data Structures and Guidelines for Languages (ISA-88.00.02-2001);
  Part 3 General and Site Recipe Models and Representation
  (ISA-88.00.03-2003); Part 4 Batch Production Records (ISA-88.00.04-2006);
  technical reports TR88.00.02-2022 (machine and unit states),
  TR88.0.03-1996 (possible recipe procedure presentation formats),
  TR88.95.01-2008 (using ISA-88 and ISA-95 together). It does not describe the
  models. Used only to fix part numbers and titles.

### Y601 — https://en.wikipedia.org/wiki/ISA-88
- citation: Wikipedia contributors, "ISA-88", n.d. (accessed 2026-11-25).
- version read: web page.
- type: survey (tertiary).
- E1/E2: corroborates the procedural levels (procedure, unit procedure,
  operation, phase; some may be omitted), the process model (process stage,
  process operation, process action), the four recipe types and the recipe
  contents (header, formula, equipment requirements, procedure, other
  information). Used only as a pointer; its reference list led to Arzén &
  Johnsson (1996) and so to Y602.

### Y602 — https://lup.lub.lu.se/search/files/4689442/8840032.pdf
- citation: Johnsson, Charlotta, 1999, *A Graphical Language for Batch
  Control*, doctoral thesis (monograph), Department of Automatic Control, Lund
  Institute of Technology, Lund University. ISRN LUTFD2/TFRT-1051-SE, ISSN
  0280-5316. DOI: none found.
- version read: repository PDF (Lund University Publications, "publisher's
  PDF, version of record"). Read: contents; ch. 3.1 (Grafcet steps,
  transitions, receptivities, pp. 33-36); ch. 6 entire (batch processing,
  ISA-S88.01, scheduling, industry practice, pp. 131-147); ch. 7.3 (G2 batch
  scenario, pp. 155-156); ch. 8.3 opening (multi-dimensional recipes,
  pp. 175-177); ch. 9 introduction (recipe analysis, p. 193). Not read:
  chs. 2, 4, 5 in full, appendices.
- type: thesis (primary research with implementation).
- E1: the unit is the **recipe procedure as a sequential function chart**
  (steps with actions, transitions with receptivities), structured by the
  ISA-S88.01 procedural levels and executed as tokens in Grafchart, a
  Grafcet/Petri-net based language. Purpose: recipe representation and
  execution in batch control, plus deadlock analysis of resource allocation.
- E2, what it shows:
  - An open, careful paraphrase of ISA-S88.01 (1995) (ch. 6.3, Fig. 6.1): the
    **process model** (process, process stage, process operation, process
    action) is equipment-independent; the **physical model** (process cell,
    unit, equipment module, control module); the **procedural control model**
    (procedure, unit procedure, operation, phase) is equipment-dependent; an
    operation "takes the material being processed from one state to another"
    (p. 138); a unit procedure runs within a single unit; a phase is the
    smallest process-oriented task and may be decomposed into SFC steps and
    transitions.
  - The four recipe types (pp. 136-137): **general** (enterprise level, no
    knowledge of the equipment), **site** (language, units of measure and raw
    materials adjusted to the site), **master** (targeted to one process cell;
    derived from a general recipe or created stand-alone), **control** (a
    copy of the master completed with scheduling, operational and equipment
    information; an instantiation for one batch). General and site recipes are
    equipment-independent; master and control recipes are equipment-dependent.
    A recipe holds administrative information (header), formula, equipment
    requirements and procedure.
  - The control activity model (Fig. 6.4) separates recipe management,
    production planning and scheduling, production information management
    (collection and storage of batch histories), process management, unit
    supervision and process control.
  - Industry practice in 1999 (ch. 6.5): commercial recipe editors use steps
    and transitions; execution is shown by colour (executing green, done red,
    halted yellow); plant status is a text list because drawing all recipes
    was too messy; resource needs are lists, either named units or a group of
    "equally good" units; no commercial system detected deadlocks.
  - Grafcet transitions carry a **receptivity**: a logical condition, an
    event, or both; a transition fires when its preceding steps are active and
    its receptivity becomes true (ch. 3.1). Grafchart adds exception
    transitions (ch. 5.6, seen in the text, not studied).
  - Demonstrated: an implementation in G2 of one simulated batch cell (three
    raw-material tanks, two mixers, three buffers, two reactors, three product
    tanks; two products from three reactants; network structure; several
    batches at once) (ch. 7.3); recipes as charts, as object tokens, and as
    multi-dimensional charts where each token carries its own procedure
    (ch. 8.1-8.3); transformation of recipes plus shared resources into a
    Petri net for deadlock analysis (ch. 9). No user study; no food plant.
  - The thesis introduces batch processes with a cake (preparation, baking,
    cooling and storing), taken from Rosenhof and Ghosh 1987 (p. 131). Only an
    illustration.

### Y603 — https://cdn.standards.iteh.ai/samples/13990/b459f27e02f74751b01fb3998f41d3d0/IEC-PAS-61512-3-2004.pdf
- citation: IEC/PAS 61512-3:2004, *Batch control - Part 3: General and site
  recipe models and representation*, first edition 2004-11; text identical in
  this preview to ANSI/ISA-88.00.03-2003. Publisher IEC (copyright ISA 2003,
  IEC 2004).
- version read: publisher's free preview (iTeh Standards), 14 pages: table of
  contents, introduction, clauses 1 (scope), 3 (definitions), 4.1-4.3.3. The
  normative clauses 5-8 (header, formula, procedure, equipment requirements,
  life-cycle states, object model, process procedure chart, transformation to
  master recipes) were **not** readable; only their titles were.
- type: standard (partial).
- E1: the unit is the **equipment-independent recipe** (EIR), a superclass of
  general and site recipes that follows the process model (process stage,
  operation, action) (def. 3.1). A product family and product grades are
  defined (3.4, 3.5).
- E2:
  - General and site recipes describe "in manufacturing terms" the materials,
    equipment requirements, chemical and physical transformations needed to
    make a product, without regard to specific equipment (4.2.1); they must be
    executable in differently built process cells and at several sites
    (4.2.2).
  - The counts in Fig. 1 illustrate the fan-out: one general recipe per
    produced material, one site recipe per site, one master recipe per process
    cell and material, one control recipe per batch; a change to one general
    recipe can change hundreds of master recipes (4.2.2).
  - The hierarchy may be collapsed or expanded (only general recipes; or an
    extra equipment-independent level for an area) (4.2.3).
  - EIRs are either the input to trial or pilot production (converted to a
    master recipe for the pilot equipment, scaled up and validated) or the
    result of it; development is iterative (4.3.2-4.3.3).
  - Contents titles show the standard has its own graphical notation (the
    process procedure chart, clause 7), recipe life-cycle states (5.8) and a
    clause on transforming EIRs to master recipes, including
    stage-to-unit-procedure mapping (clause 8). Not read.

### Y604 — https://cdn.standards.iteh.ai/samples/16242/38071704ea2d42d3bce8183bd2310574/IEC-PAS-61512-4-2007.pdf
- citation: IEC/PAS 61512-4:2007, *Batch control - Part 4: Batch production
  records*. Superseded by IEC 61512-4:2009 (not read).
- version read: publisher's free preview (iTeh Standards): scope, normative
  references, definitions 3.1-3.5, clause 4.2 (pp. 8-12).
- type: standard (partial).
- E1: the unit is the **batch production record**: the subset of execution
  and business information kept for a batch or another element of batch
  production (a lot, a campaign, a pre-weigh), according to a record
  specification (3.2, 3.4).
- E2:
  - Batch history is all execution information collected for one batch (3.1).
  - A record may reference the records of intermediate materials (4.2,
    example 5) and of purchased ingredients (example 6); records can be
    combined into the record of a final product (example 7).
  - A record may be made **for a lot of intermediate material, to track its
    storage and handling between its production and its consumption in
    different batches** (4.2.3, example 4).
  - Record content and format are left to the user; the PAS gives the model.

### Y605 — https://lin.engin.umich.edu/wp-content/uploads/sites/551/2021/10/Mixed-Integer-Linear-Programming-in-Process-Scheduling.pdf
- citation: Floudas, Christodoulos A.; Lin, Xiaoxia, 2005, "Mixed Integer
  Linear Programming in Process Scheduling: Modeling, Algorithms, and
  Applications", *Annals of Operations Research* 139, 131-162. DOI not
  verified (not printed on the pages read).
- version read: repository PDF (author's group site), publisher layout. Read:
  abstract, sec. 1.1 (problem components, process representation, Figs. 1-2),
  the storage-policy paragraph in sec. 1, sec. 3 opening (applications).
- type: survey (of primary MILP work).
- E1: the scheduling problem is given by production recipes, equipment,
  **intermediate storage policy**, requirements, resources and horizon
  (sec. 1.1). Recipes are drawn as a **State-Task Network** (STN; Kondili,
  Pantelides and Sargent 1993): a directed bipartite graph of state nodes
  (raw, intermediate, final materials) and task nodes (operations), with the
  fraction of a state consumed or produced on each arc. The **Resource-Task
  Network** (RTN; Pantelides 1993) treats equipment, storage and utilities as
  resources consumed at a task's start and produced at its end.
- E2: Fig. 1 shows the features STN captures: tasks with several inputs and
  outputs, a shared raw material, the same state produced by different tasks,
  and recycle to an earlier task. Storage policies named: unlimited (UIS),
  finite (FIS), no intermediate storage (NIS) and **zero-wait** (ZW), the last
  for a state that must be consumed at once (Janak, Lin and Floudas 2004 as
  summarised). Applications listed are mainly chemical and consumer goods.
  This is a survey; demonstrations are in the cited papers (not read).

### Y606 — https://jckantor.github.io/ND-Pyomo-Cookbook/notebooks/04.05-Scheduling-Multipurpose-Batch-Processes-using-State-Task_Networks.html
- citation: Kantor, Jeffrey C., n.d., "Scheduling Multipurpose Batch
  Processes using State-Task Networks", *ND Pyomo Cookbook* (Jupyter
  notebook).
- version read: web page (full).
- type: implementation.
- E1/E2: a runnable Pyomo encoding of the Kondili 1993 example: 9 states
  (3 feeds, 4 intermediates, 2 products) and 5 tasks on 4 units. Each state
  has a storage capacity, an initial inventory and a price (negative for
  intermediates, to discourage work in progress); each unit has min/max batch
  sizes and the tasks it can perform; output arcs carry fractions and
  durations (Reaction_2 sends 40 % to a product and 60 % to an intermediate).
  Demonstrates that the representation is executable; the objective (profit)
  is the scheduling purpose, not knowledge.

### Y607 — https://zenodo.org/records/3987973/files/On%20the%20Optimization%20of%20Production%20Scheduling%20in%20Industrial%20Food%20Processing%20Facilities.pdf
- citation: Georgiadis, Georgios P.; Ziogou, Chrysovalantou; Kopanos,
  Georgios; Mariño Pampín, Borja; Cabo, Daniel; Lopez, Miguel; Georgiadis,
  Michael C., 2019, "On the Optimization of Production Scheduling in
  Industrial Food Processing Facilities", in Kiss, Zondervan, Lakerveld,
  Özkan (eds.), *Proceedings of the 29th European Symposium on Computer Aided
  Process Engineering (ESCAPE 29)*, Elsevier. DOI and series volume not
  verified.
- version read: repository PDF (Zenodo), publisher layout, full (6 pp.).
- type: primary research (industrial case).
- E1: a general-precedence MILP over product batches, stages and parallel
  units, for weekly scheduling of a canned-fish plant (Frinsa del Noroeste,
  Ribeira, Spain): thawing, filling and sealing, sterilising, packing.
- E2: demonstrated on one real week (136 final products; >400 product codes
  in the plant) with a two-step decomposition; solved in about 1 h (GAMS,
  CPLEX); the optimised schedule fitted five days where the manual schedule
  needed an extra Sunday shift (sec. 4). The model includes sequence-dependent
  changeovers and a **maximum waiting time Qp between sealing and
  sterilisation "to ensure microbiological integrity"** (constraint 6). Batch
  stages are run at maximum capacity by industrial practice (sec. 3). The
  generalisation to "most food" make-and-pack plants is claimed, not shown.

### Y608 — https://docs.oracle.com/cd/E18727_01/doc.121/e13091/T320995T321003.htm
- citation: Oracle, *Oracle Process Manufacturing Product Development User's
  Guide*, chapter "Recipes". Release not verified (path suggests 12.1).
- version read: vendor documentation web page; the first 100,000 of 126,838
  characters.
- type: implementation (commercial ERP documentation).
- E1: a **recipe = formula + routing + processing instructions**. The formula
  holds material relationships (product, ingredients, byproducts); the
  routing holds operations, activities and resources. Formulas and routings
  are built separately; one routing can serve several formulas and one
  formula several routings. Materials are attached to routing steps; an
  intermediate can be split between steps by percentage (worked example:
  step 1 makes 30 lb intermediate and 5 lb byproduct; the intermediate goes
  25 % to product, 35 % to step 2, 40 % to step 3).
- E2: **validity rules** say when, where and how a recipe applies: by
  organisation (plant or lab, blank = global), use (production, planning,
  costing, regulatory, technical), dates, quantity range, process loss,
  status, and a **preference** number when several recipes make the same
  product. The page also maps its recipes to S88 general, site and master
  recipes, and mentions seasonal formulations and dated substitute items.
  Documentation of a product; no evaluation.

### Y609 — https://www.iaorifors.com/paper/31320 (abstract only)
- citation: Houba, Iris H. G.; Hartog, Rob J. M.; Top, Jan L.; Beulens,
  Adrie J. M.; van Berkel, Linda N., 2000, "Using recipe classes for
  supporting detailed planning in food industry: A case study", *European
  Journal of Operational Research* 122(2), 367-373. DOI
  10.1016/S0377-2217(99)00239-8 (from the MaRDI portal record).
  Authors, volume, issue and pages verified on EconPapers and IAOR; MaRDI
  gives the year as 2001, EconPapers and IAOR as 2000.
- version read: **abstract only** (IAOR paraphrase; ScienceDirect 403).
- type: primary research (prototype).
- E1/E2 (from the abstract): a "recipe class" holds the information of a
  typical food-industry recipe and also **generates the activities and
  constraints** a constraint-satisfaction scheduler needs; argued to reduce
  modelling effort because scheduling libraries lacked a recipe concept.
  Implemented and tested in a prototype for a salad factory (MaRDI lists ILOG
  Schedule and CPLEX). Nothing beyond the abstract can be judged.

### Y610 — https://research.tue.nl/en/publications/evaluation-of-three-production-planning-procedures-for-the-use-of/ (abstract only)
- citation: Bertrand, J. W. M.; Rutten, W. G. M. M., 1999, "Evaluation of
  three production planning procedures for the use of recipe flexibility",
  *European Journal of Operational Research* 115(1), 179-194. DOI
  10.1016/S0377-2217(98)00166-0.
- version read: **abstract only** (TU/e portal).
- type: primary research (simulation).
- E1/E2: **recipe flexibility** = making the same product with a different
  recipe, because raw-material quality varies, a cheaper material still meets
  specification, or the standard recipe's materials are unavailable.
  Simulation for an animal-feed cost structure; the optimal procedure gains
  about 4 % profit under some conditions; a simple myopic one may suffice.

### Y611 — https://wbmoodle.hswt.de/mod/resource/view.php?id=167518
- citation: FAO and WHO, 2023, *General Principles of Food Hygiene*, Codex
  Alimentarius Code of Practice CXC 1-1969 (adopted 1969, amended 1999,
  revised 1997, 2003, 2020, 2022), Rome. DOI 10.4060/cc6125en (printed in the
  document).
- version read: publisher PDF (FAO/WHO 2023 printing) served from a
  university course mirror (Hochschule Weihenstephan-Triesdorf Moodle),
  because FAO's repository returned 403. Read: definitions (sec. 2.3),
  sec. 13.1-13.2 (process description, time and temperature control),
  sec. 19.4-19.10 (HACCP steps 4-10).
- type: standard.
- E1: the unit is a **step** in a **flow diagram**: "a systematic
  representation of the sequence of steps used in the production or
  manufacture of food" (def.). A **critical control point** is a step where
  an essential control measure is applied; a **critical limit** is "a
  criterion, observable or measurable", at a CCP, that separates acceptable
  from unacceptable food; **monitoring** is the scheduled measurement or
  observation against it; **corrective action** re-establishes control and
  decides the disposition of affected product (def.; 19.9-19.10).
- E2:
  - The flow diagram covers all steps of a specific product including rework;
    shows the sequence and interaction of steps, where raw materials,
    ingredients and **intermediate products enter**, where **reworking and
    recycling** take place, where end products, **intermediate products,
    waste and by-products** are released; complex operations may be split into
    linked modules; it must be **confirmed on site** at all stages and hours
    of operation (19.4-19.5; also 13.1).
  - One flow diagram may serve several products made with similar steps
    (19.4; 13.1). For restaurants it may follow receipt, storage, preparation
    and cooking (13.1).
  - Critical limits "should be measurable or observable"; criteria include
    time, temperature, moisture, pH, aw, contact time, viscosity, or
    observable settings; several parameters may limit one step (heat
    treatment: time and temperature) (19.8).
  - Critical limits must be **validated** (studies, literature, regulation,
    competent authority or third-party studies) (19.8).
  - The cook step and the cooling step can both be CCPs for the same hazard
    (cook for vegetative cells of a spore-former; cooling against germination
    and growth of the spores) (19.7-19.8 text).
  - Time and temperature control should consider the food, time in the growth
    zone, intended shelf life, packaging, and intended use (further cooking or
    ready to eat); systems specify tolerable limits and are validated,
    monitored and recorded (13.2.1-13.2.2).
  - Monitoring frequency: continuous where possible (time, temperature);
    observable limits are rarely continuous (19.10).

### Y612 — https://www.fda.gov/media/71976/download
- citation: U.S. Food and Drug Administration, 2006 (April), *Managing Food
  Safety: A Manual for the Voluntary Use of HACCP Principles for Operators of
  Food Service and Retail Establishments*. Landing page:
  https://www.fda.gov/food/hazard-analysis-critical-control-point-haccp/managing-food-safety-manual-voluntary-use-haccp-principles-operators-food-service-and-retail
- version read: publisher PDF (86 pp.); read ch. 2 (pp. 13-20) and the
  glossary entries for danger zone and process approach.
- type: standard (government guidance).
- E1: the **process approach**: instead of one HACCP plan per product, the
  many food flows of a kitchen are grouped by how many times the food passes
  through the temperature danger zone (41-135 °F): Process 1, no cook step
  (receive, store, prepare, hold, serve); Process 2, same-day service (one
  trip: ... cook, hold, serve); Process 3, complex food preparation (two or
  more trips: ... cook, cool, reheat, hot hold, serve) (pp. 13-15).
- E2:
  - Operational steps named: receiving, storing, preparing, cooking, cooling,
    reheating, holding, assembling, packaging, serving, selling (p. 14).
  - A single menu item (example: chicken salad sandwich) is often made by
    combining components produced by different processes (p. 15).
  - Control measures are mostly the same for a process class, but **critical
    limits for cooking stay specific to each food** (chicken 165 °F for 15 s;
    meatloaf 155 °F for 15 s); some steps (refrigerated storage, hot holding)
    have limits common to all foods (p. 16).
  - For Process 3 the manual lists cooking, cooling against spore-forming or
    toxin-forming bacteria, hot and cold holding or time alone, date marking
    of ready-to-eat food held over 24 h, and reheating (p. 20).
  - Guidance; no evaluation reported.

### Y613 — https://www.ruokavirasto.fi/globalassets/tietoa-meista/asiointi/oppaat-ja-lomakkeet/yritykset/elintarvikeala/elintarvikehuoneistot/omavalvonta-fin-2-jaahdytys.pdf
- citation: Ruokavirasto (Finnish Food Authority), 2021, "Näin huolehdit
  omavalvonnasta ravintolassa: Jäähdytys" (How to do self-monitoring in a
  restaurant: Cooling), leaflet, PDF metadata dated 2021-04-22. Produced in a
  project funded by the Ministry of Agriculture and Forestry (MMM).
- version read: publisher PDF, full (one page, Finnish).
- type: standard (authority guidance).
- E1/E2 (paraphrased from Finnish): food not served at once must be cooled
  immediately after cooking to below +6 °C within 4 h; thin layers, several
  containers or cutting speed cooling; **measure the temperature at the start
  and at the end of cooling, in the centre**; never cool outdoors or on a
  window sill; mark the preparation date; record temperatures and deviations
  as the business's own self-monitoring plan says. A Finnish instance of a
  critical limit with monitoring and recording.

### Y614 — https://ceur-ws.org/Vol-3998/paper02.pdf
- citation: Wellershaus, Finn (as printed; e-mail and ORCID give Janne);
  Köhler-Bußmeier, Michael; Sudeikat, Jan, 2025, "Modelling and Analysis of
  Self-Adaptive Systems using Petri Nets: A Robot Kitchen Case Study",
  PNSE'25 International Workshop on Petri Nets and Software Engineering,
  *CEUR Workshop Proceedings* Vol-3998, pp. 24-36. CC BY 4.0. DOI: none
  found.
- version read: publisher PDF (CEUR); read abstract, sec. 1-2 and Table 1;
  sec. 3 (MAPE loop) skimmed by search.
- type: primary research (simulation model).
- E1: a Hamburg robot kitchen in RENEW (coloured, timed Petri nets with
  nets-within-nets). Recipes are separate nets of steps; each step consumes
  basic ingredients and/or **intermediate dishes** and requires a robot
  capability; recipes have **several entry points** where steps are
  independent, so a scheduler can run them in parallel; an assembly station
  collects the required partial dishes, with an order lock so intermediates
  of different orders are not mixed (sec. 2).
- E2: two recipes (fried tofu with cooked beans and mashed potatoes; filled
  baked peppers). **Durations are held by the robot, not the recipe**,
  because they depend on hardware; for cooking, frying and baking "it is
  assumed the robot is able to recognize when a dish is cooked" (sec. 2).
  Purpose is self-adaptation and throughput, with deadlock analysis claimed
  possible; no culinary evaluation.

### Y615 — https://www.scitepress.org/publishedPapers/2024/129430/pdf/index.html
- citation: Rennane, Fatma Zohra; Meziane, Abdelkrim, 2024, "Leveraging
  Ontologies for Handicraft Business Process Modeling: Application for the
  Pastry-Making Domain", WEBIST 2024, pp. 226-233. DOI
  10.5220/0012943000003825.
- version read: publisher PDF (SciTePress), via WebFetch reading.
- type: primary research (ontology).
- E1/E2: despite the title, BPMN and UML appear only as background; the model
  is an OWL ontology (recipe, phases, ordered steps with action, input/output
  ingredients, duration, temperature, utensils) instantiated for one Algerian
  pastry (Makrout Louz). No intermediate products as such, no gateways or
  events, no completion or quality checks, no alternatives. Validation:
  reasoner consistency, SWRL step order, SPARQL competency questions; no user
  evaluation. Recorded here only because it was the closest "BPMN for
  cooking" hit; it belongs to the ontology area.

### Y616 — https://arxiv.org/abs/2101.08886 (abstract only)
- citation: Zallio, M.; Kelly, P.; Cryan, B.; Berry, D., 2021, "A co-Design
  approach to develop a smart cooking appliance. Applying a Domain Specific
  Language for a community supported appliance", arXiv:2101.08886v3.
- version read: **abstract only** (arXiv abstract page).
- type: primary research.
- E1/E2: a domain-specific language for a semi-automated cooking appliance
  for people with disabilities, developed by co-design. The abstract does not
  describe the representation; a search snippet (not evidence) says it uses a
  UML state diagram. Nothing judged.

## Failed pages and abstract-only

| URL or query | why | fallback tried |
| --- | --- | --- |
| https://www.sciencedirect.com/science/article/abs/pii/S0377221799002398 | 403 | IAOR (abstract, Y609), EconPapers, MaRDI, Semantic Scholar API (metadata, 11 citing papers) |
| https://www.econbiz.de/Record/using-recipe-classes-for-supporting-detailed-planning-in-food-industry-a-case-study/10005287523 | Anubis bot wall | IAOR |
| https://core.ac.uk/download/518573979.pdf | 403 | none found |
| https://lup.lub.lu.se/search/files/4689442/8840032.pdf | WebFetch could not decode the PDF | saved PDF converted with pdftotext (Y602) |
| https://cdn.standards.iteh.ai/... IEC-PAS-61512-3-2004.pdf and IEC-PAS-61512-4-2007.pdf | WebFetch could not decode | pdftotext on the saved PDFs (Y603, Y604); only the free preview pages exist |
| ISA-88 Parts 1-4 full text | paywalled | Y602 (thesis paraphrase of Part 1), Y603, Y604 (previews) |
| https://doi.org/10.4060/cc6125en -> fao.org card -> https://openknowledge.fao.org/handle/20.500.14283/cc6125en | 403 | same FAO PDF from a university mirror (Y611) |
| https://www.mpi.govt.nz/dmsdocument/44455/direct/ | empty content | Y611 |
| https://alertas.directoriolegislativo.org/...FAO.-Codex-Alimentarius-food-hygiene.pdf | cross-host redirect to a third-party mirror; not followed | Y611 |
| https://www.fda.gov/media/71976/download | WebFetch could not decode | pdftotext on saved PDF (Y612) |
| https://www.ruokavirasto.fi/...omavalvonta-fin-2-jaahdytys.pdf | WebFetch could not decode | pdftotext on saved PDF (Y613) |
| https://lin.engin.umich.edu/...Mixed-Integer-Linear-Programming-in-Process-Scheduling.pdf | WebFetch could not decode | pdftotext on saved PDF (Y605) |
| https://zenodo.org/records/3987973/files/...Food%20Processing%20Facilities.pdf | WebFetch could not decode | pdftotext on saved PDF (Y607) |
| https://ceur-ws.org/Vol-3998/paper02.pdf | WebFetch could not decode | pdftotext on saved PDF (Y614) |
| Kondili, Pantelides & Sargent 1993, *Comput. Chem. Eng.* 17(2) 211-227 (original STN paper) | no open copy found | described through Y605, Y606 |
| Lütke Entrup et al. 2005, "Mixed-integer linear programming approaches to shelf-life-integrated planning and scheduling in yoghurt production", *IJPR* 43(23) | no open copy found; only search snippets (not evidence) | none; **not read** |
| Akkerman & van Donk, "Analyzing scheduling in the food-processing industry: structure and tasks", *Cognition, Technology & Work* (DOI 10.1007/s10111-007-0107-7) | mediaTUM Anubis wall; Springer login redirect; unpaywall chain to the same DOI | none; **not read** |
| https://mdpi.com/2227-9717/7/7/438/htm (Georgiadis, Elekidis, Georgiadis 2019 review, *Processes* 7(7) 438) | 403 | none; **not read** |
| https://www.automation.siemens.com/sce-static/.../p03-02-batchsteuerung-mit-rezepten-11.pdf (German recipe-hierarchy training) | 404 | none |
| NAMUR NE 33 (2003), *Anforderungen an Systeme zur Rezeptfahrweise* | behind DIN/NAMUR paywall or login | none; Y602 cites NAMUR 1992 as one of the three terminology efforts |
| HALLAM-ICS S88 guide (gated content) | gated form; not tried | Y602 |
| https://www.iaorifors.com/paper/31320 | abstract only | (Y609) |
| https://research.tue.nl/... (Bertrand & Rutten) | abstract only | (Y610) |
| https://arxiv.org/abs/2101.08886 | abstract only read | (Y616) |

## Searches

| language | query | useful? |
| --- | --- | --- |
| en | "Using recipe classes for supporting detailed planning in food industry" | no (vendor pages) |
| en | recipe classes detailed planning food industry EJOR 2000 ... | yes: Houba authors, Bertrand & Rutten |
| en | ISA-88 general recipe site recipe master recipe control recipe ... pdf | partly (Scribd, vendor summaries not used) |
| en | Johnsson Årzén Grafchart batch control recipes ISA S88 Lund thesis pdf | yes: Y602 |
| en | HALLAM-ICS introduction to batch processing with S88 pdf | no |
| en | ISA-88 Part 3 general recipe process stage ... open access paper | yes: Y603 preview |
| en | ISA-88 batch control food industry case study ... | no academic sources (trade press only) |
| en | Codex Alimentarius CXC 1-1969 ... pdf flow diagram critical limits monitoring | yes: Y611 |
| en | "CXC_001e.pdf" codex general principles food hygiene | partly (older FAO texts) |
| en | State-Task Network Kondili Pantelides Sargent 1993 ... | yes: Y605, Y606 |
| en | shelf-life integrated planning scheduling yoghurt Lütke Entrup ... pdf | metadata only |
| en | Akkerman van Donk "Analyzing scheduling in the food-processing industry" | blocked |
| en | Georgiadis Elekidis 2019 Optimization-Based Scheduling ... food | yes: Y607 |
| en | open access food production scheduling intermediate products maximum holding time ... | yes: Y607 |
| en | cooking recipe modelled as Petri net paper | yes: Y614 |
| en | BPMN cooking recipe process model kitchen workflow paper | weak: Y615; no academic BPMN cooking model found |
| en | UML activity diagram state machine cooking recipe ... | weak: Y616 abstract; no academic source |
| en | FDA "Managing Food Safety" manual ... "process approach" | yes: Y612 |
| fi | Ruokavirasto omavalvonta ruoan jäähdytys 6 °C neljässä tunnissa kuumana pito 60 °C ohje | yes: Y613 |
| en | IEC 61512-4 batch production records sample pdf ... genealogy | yes: Y604 |
| de | NAMUR NE 33 Rezeptfahrweise Anforderungen Grundrezept Steuerrezept Chargenprozess | catalogue only |
| en | "Recipe-driven methods for the design and management of food catering production systems" | not found |

## Citation trail

- Backward from Y601 (Wikipedia references) to Arzén & Johnsson 1996, which led
  to the Lund thesis Y602.
- Backward from Y602: ISA 1995 (S88.01), NAMUR 1992, Williams 1988 (Purdue),
  IEC 61512-1 (1997), Fisher 1990 (batch plant classes), Rosenhof & Ghosh 1987
  (cake example), Shaw 1982 (batch definition). None read.
- Backward from Y605: Kondili et al. 1993 (STN), Pantelides 1993 (RTN), Janak,
  Lin & Floudas 2004 (UIS/FIS/NIS/ZW in a continuous-time model). Y606 is an
  executable reconstruction of Kondili 1993.
- Backward from Y607: Kopanos et al. 2010 (yoghurt), Baumann & Trautmann 2014
  (make-and-pack), Aguirre et al. 2017, Harjunkoski et al. 2014, Méndez et al.
  2006 (review). None read.
- Forward from Y609 (Semantic Scholar API, 11 citing records): "Recipe-driven
  methods for the design and management of food catering production systems"
  (2019), "Hierarchical production planning with flexibility in agroalimentary
  environment: a case study" (2010, 2012), "Quick-response decision-making in
  the food processing industry" (2007), "Post pandemic strategic planning of
  food catering production and distribution networks" (2022). None read; the
  catering title could not be located.
- Y611 points to the Codex *Guidelines for the Validation of Food Safety
  Control Measures* (CXG 69-2008) for validation of critical limits. Not read.
- Y608 maps its recipes back to S88 (Y602, Y603).

## Approach analyses

### A. ISA-88 recipe model (recipe types, process model, procedural model)

- **E1 representation and purpose.** Unit: a recipe = header + formula
  (inputs, outputs, process parameters) + equipment requirements + procedure
  (Y602 p. 136; Y603 contents; Y601). Procedure is either the
  equipment-independent process model (stage, operation, action) in general
  and site recipes, or the equipment-dependent procedural model (procedure,
  unit procedure, operation, phase) in master and control recipes (Y602
  Fig. 6.1). Purpose: specify and execute batch manufacture across sites and
  plants; communicate product knowledge separately from equipment (Y603
  4.2).
- **E2 published evidence.** A standard and its documented terminology (Y602,
  Y603). Demonstration in Y602 is a simulated chemical-style cell in G2, not
  food. Food use is reported only in trade press (search results, not read as
  evidence). The four levels and the equipment-independence boundary are
  published; nothing published tests them on cooking.
- **E3 mapping on paper (inferred).**
  - **K1 rutabaga gratin, general recipe:** process stages *prepare roots*
    (actions: peel, slice 2-3 mm), *pre-cook rutabaga* (operation blanch,
    action "hold until crisp-tender"), *assemble* (layer, add cream), *bake*,
    *rest*. Formula: inputs potato, rutabaga, cream, seasoning; process
    parameters as ranges with sources (blanch 3-10 min; bake 40-80 min);
    output gratin. Equipment requirement stated only as "an oven", "a pot".
  - **K1 master recipe for a home kitchen:** unit procedures bound to units
    (hob + pot: blanch; oven + one named dish: bake), with parameters fixed
    for that oven, that dish depth and whether it is covered. The *control
    recipe* is tonight's batch: actual minutes, the dish size, the observed
    endpoint. Food-prep's kitchen-test record is the nearest thing to a
    control recipe plus batch record.
  - **K8 raw-rutabaga gratin:** the working route (raw slices, about 90 min
    covered) is a different procedure with different process parameters, not
    a different structure. In ISA-88 terms the false positive and false
    negative of R4's structural check come from judging a procedure without
    its formula parameters. Y603 4.3.3 makes a general recipe something that
    is converted to a master recipe and **validated in trial**; a route
    therefore cannot be rejected or accepted on structure alone.
  - **K1-x and K2-x (unverified combinations):** an edited process action in a
    general recipe makes a new recipe version that has not been through
    trial (Y603 4.3.2-4.3.3 describe trial as the validation step). This
    matches Food-prep keeping such combinations apart as unverified.
  - **K3 napa-cabbage rolls:** process stages may be serial and/or parallel
    (Y602 p. 135): *leaves* (blanch), *rice filling* (half-cook), *meat* run
    as parallel stages, then *assemble* and *bake*. After *assemble* there is
    one material in process; the rice finishing inside the roll has no place
    of its own in the process model.
  - **K4 onion vessel vs courgette vessel:** one filling stage reused with two
    container stages; the container preparation differs (onion layers slip
    if overboiled). ISA-88 has no notion of structural role (container,
    filling).
  - **K7 arancini:** two general recipes or one recipe with two variants of
    the *cook rice* stage (boil vs risotto). The cooled rice made the night
    before is an intermediate between two batches; ISA-88 Part 1 describes it
    only as a material between stages, but Part 4 can give that lot its own
    record of storage and handling (Y604 4.2.3, example 4).
- **E4 table** (P preserved, X extend, C cannot; one reason each).

| aspect | K1 | K3 | K7 | K8 |
| --- | --- | --- | --- | --- |
| a independent components and joins | P: parallel stages joined by a later stage (Y602) | P: three parallel stages, one assembly stage | P: rice, filling, coating stages | P |
| b intermediate states, readiness vs doneness | X: an operation moves material between states (Y602 p. 138) but there is no readiness/doneness distinction | X: same | X: intermediate exists; "not ready to eat" not expressible | X |
| c member after assembly | C: one material after joining | C: rice in the roll not represented | C | C |
| d why a stage exists | C: no dependency or objective field in what was read | C | C | C: why raw slices need 90 min is not expressible |
| e alternative routes kept apart, with evidence | X: separate master recipes per cell, separate recipe versions; no evidence field | X | X: two variants as two recipes | X |
| f substitution and its consequences | X: site recipe may change raw materials (Y602 p. 137) but re-validation is by trial, not by model | X | - | X |
| g start from a state the cook has | X: control recipes start from charged materials; no "from state" query | X | X: start from the intermediate lot (Y604) | - |
| h provenance | C: recipes have authors and versions (header), not per-claim sources | C | C | C |
| i unknown vs false | C: not in what was read | C | C | C |
| j what a person deciding can read | X: process procedure chart exists (Y603 clause 7, not read); commercial editors show step status by colour (Y602 6.5) | X | X | X |

- **E5 against Food-prep.** R3 routes are equipment-independent general
  recipes in all but name; R5 sequences mix in per-source times that are
  really master-recipe values (they assume someone's oven, pot and dish). R1
  operations correspond to process operations/actions. The control recipe and
  batch record have no Food-prep counterpart except `kitchen-tests.md`.
- **E6 published vs inferred.** Published: the four recipe types and their
  equipment-dependence (Y602, Y603); general recipe converted to master and
  validated in trial (Y603); intermediate-lot records (Y604); parallel stages
  (Y602). Inferred in R6: every K mapping above; the reading of K8 as a
  missing-parameter error; the use of the control recipe for kitchen tests.
- **Verdict.**
  - Recipe types general / master / control: **adopt the concept.** Food-prep
    lacks an explicit boundary between what a documented route says
    independent of equipment and what depends on one kitchen's oven, pot and
    dish, and the kitchen-test record has no defined status. The concept costs
    no scoring and keeps provenance per level. (Y602, Y603.)
  - Procedural levels (procedure, unit procedure, operation, phase): **already
    equivalent** in the parts that matter (route, material chain, operation);
    unit-binding is an equipment concern that a home cook does not need.
  - Formula separate from procedure (inputs, outputs, process parameters):
    **extend.** R5 holds parameters per step with sources; a formula-like list
    per route would let R4 show which parameters a substitution touches
    (inferred).
  - Batch production record for an intermediate lot (Part 4): **adopt the
    concept** for Q5 (history of a kept intermediate) and for kitchen tests.
    (Y604.)

### B. Sequential function charts, Grafcet / Grafchart and Petri nets

- **E1.** Unit: step (active/inactive, with actions) and transition (with a
  receptivity: condition, event, or both); parallel and alternative branches;
  in Grafchart, tokens may carry a recipe's own procedure; exception
  transitions (Y602 ch. 3.1, 5, 8.3). The robot kitchen uses coloured timed
  Petri nets whose places hold ingredients and intermediate dishes (Y614).
  Purpose: execution and verification (deadlock), throughput.
- **E2.** Y602: implementation in G2, deadlock analysis by transforming
  recipes and shared resources to a Petri net; Y614: a simulation of two
  recipes in RENEW. Neither evaluates culinary content. No academic BPMN or
  UML model of cooking was found and read (Y615 does not use BPMN; Y616
  abstract only).
- **E3 (inferred).**
  - **K1:** steps *blanch* -> transition receptivity "crisp-tender: softened
    slightly, not fully cooked" -> step *layer* -> ... -> *bake* with
    receptivity "knife meets some give / no resistance" (a conflict that
    would have to be two alternative receptivities). Exception transition
    "still crunchy when the potato is done" for the skipped blanch.
  - **K3:** parallel branch (leaves || rice || meat), synchronising
    transition into *assemble*.
  - **K9 latkes:** a parallel branch where the squeezed liquid settles while
    the shreds wait, rejoined when the starch is returned. Expressible as
    control flow; the material identity of the starch is not.
  - **K7:** the overnight cool is a step whose receptivity is time-based; the
    two cooking routes are an alternative branch.
- **E4 table.**

| aspect | K1 | K3 | K7 | K9 |
| --- | --- | --- | --- | --- |
| a components and joins | P: parallel branches + sync (Y602) | P | P | P: branch and rejoin |
| b readiness vs doneness | X: receptivity = done-when; kind of endpoint absent | X | X | X |
| c member after assembly | C: control flow, not material | C | C | C |
| d why a stage exists | C | C | C | C |
| e alternatives kept apart | X: alternative branches exist but merge into one chart; no per-branch evidence | X | X | - |
| f substitution | C: no material model in SFC (Y614 has material tokens but no substitution) | C | C | C |
| g start from a state | X: a chart can be started at any marking (inferred) | X | X | X |
| h provenance | C | C | C | C |
| i unknown vs false | C: a receptivity is true or not yet true | C | C | C |
| j readable for a person | P: step/transition charts are the industry's operator view (Y602 6.5) | P | P | P |

- **E5.** R5 done-when checks are receptivities; failed-if checks are
  exception transitions. Food-prep already keeps them as observable,
  per-source text, which a receptivity is not required to be.
- **E6.** Published: receptivity semantics (Y602 ch. 3.1); parallel and
  alternative branches (Y602); intermediate dishes, parallel entry points and
  hardware-held durations in a kitchen net (Y614). Inferred: all K mappings.
- **Verdict.** **Already equivalent** for observable completion and failure
  (done-when / failed-if). **Not suited** as the representation: control flow
  without material state, built for execution and deadlock analysis. One
  observation is worth keeping (Y614): the authors put durations in the
  equipment, not the recipe, and assumed doneness is sensed. That is
  independent support for separating equipment-bound times from the route
  (approach A).

### C. State-Task Network / Resource-Task Network and food scheduling models

- **E1.** Unit: states (materials, including intermediates, each with a
  storage policy, capacity, initial inventory) and tasks (operations with
  fractional inputs and outputs and durations on arcs) (Y605, Y606). RTN adds
  equipment and utilities as resources (Y605). Food scheduling models (Y607,
  Y609) add maximum waiting times between stages, changeovers and campaign
  rules. Purpose: optimise a schedule (profit, makespan).
- **E2.** STN and RTN are the standard representation in process scheduling
  (Y605 survey); Y606 runs the Kondili example. Y607 schedules a real
  canned-fish week (136 products, about 1 h solve), with a maximum wait Qp
  justified by microbiological integrity. Y609 (abstract only) a recipe class
  for a salad factory prototype. Bertrand & Rutten (Y610, abstract only)
  model recipe flexibility. Lütke Entrup et al. (yoghurt shelf life) was not
  read.
- **E3 (inferred).**
  - **K7 arancini STN:** states raw rice, cooked rice (boiled), cooked rice
    (risotto), cooled rice mass [storage: FIS, fridge, kept at most 24 h per
    the UK bodies in R5], filling, shaped ball, coated ball, fried arancini;
    tasks boil, risotto, cool, shape-and-fill, coat, fry. If the two cooking
    tasks produce the **same** state, STN, like `Material.key()`, forgets
    which route made it; to keep them apart they must be two states.
  - **K9 latkes:** task *squeeze* outputs shreds and liquid (fractions);
    task *settle* outputs starch and discarded water; task *mix* consumes
    shreds and starch. STN represents this split and return natively
    (Y605 Fig. 1 shows recycle to an earlier task).
  - **K2 falafel:** soaked raw pulses as a state with policy FIS (fridge, no
    authority time found in R5); the raw paste as a state that is fried
    without a long hold. Whether that is "zero-wait" is not documented.
  - **K1:** blanched rutabaga slices as a state; their hold before layering
    has no documented limit in R5.
- **E4 table.**

| aspect | K1 | K2 | K7 | K9 |
| --- | --- | --- | --- | --- |
| a components and joins | P: tasks with several inputs (Y605) | P | P | P |
| b intermediates, readiness vs doneness | X: intermediates and storage policies (Y605), no doneness | X | P for holding (FIS with capacity); X for doneness | X |
| c member after assembly | C: a mixed state has no members | C | C | C |
| d why a stage exists | C | C | C | C |
| e alternatives kept apart | X: several tasks may produce one state; separate states needed to keep routes apart | X | X | - |
| f substitution | X: recipe flexibility selects among recipes (Y610, abstract) | X | - | - |
| g start from a state | P: initial inventory of any state (Y606) | P | P | P |
| h provenance | C | C | C | C |
| i unknown vs false | C | C | C | C |
| j readable for a person | X: STN diagrams are compact; Gantt output is for planners (Y607) | X | X | X |

- **E5.** STN's state-plus-task graph is the same idea as R1's material
  (part + state) and operation with several output fractions; R5's
  intermediate states with keeping times are STN states with a storage
  policy. What STN adds: a named **storage policy class** (unlimited, finite,
  none, zero-wait) and a **maximum wait between two named tasks** (Y607
  constraint 6), which is not the same as a keeping time for a state in the
  fridge.
- **E6.** Published: STN, RTN, UIS/FIS/NIS/ZW (Y605); executable example
  (Y606); max waiting time in a food plant (Y607). Inferred: K mappings and
  the comparison with `Material.key()`.
- **Verdict.**
  - STN representation: **already equivalent** (R1 + R5).
  - Storage policy classes and maximum wait between tasks: **extend.**
    Food-prep records how long a state keeps, but not "must go straight on"
    or "at most N minutes before the next step". Each value would still need
    a source; none is to be inferred from structure.
  - RTN equipment resources and the optimisation itself: **not suited** now
    (scheduling and objectives are excluded by the no-scoring rule); open for
    the R7 question of two dishes needing the oven at different temperatures.
  - Houba's recipe class: **insufficient evidence** (abstract only).

### D. Process-manufacturing recipe: formula, routing, validity rules, co- and by-products

- **E1.** Recipe = formula (products, ingredients, byproducts) + routing
  (operations, activities, resources) + instructions; materials attached to
  steps with transfer percentages; validity rules select a recipe by
  organisation, use, dates, quantity, status and preference (Y608).
- **E2.** Vendor documentation of a working product; no evaluation (Y608).
  Recipe flexibility (Y610, abstract): alternative recipes for raw-material
  quality, cost or availability.
- **E3 (inferred).**
  - **K4:** one filling formula linked to two routings (onion vessel,
    courgette vessel) is exactly the many-to-many formula-routing link of
    Y608.
  - **K5 broccoli-stem patties:** in another dish's formula the stem is a
    byproduct; in the patty formula it is an ingredient. Y608 types a
    material per formula, so both views coexist.
  - **K9:** settled starch as an intermediate that returns (Y608's
    intermediate split between steps).
  - **K2 chickpea vs dried pea:** two formulas for one product with
    conditions of validity (which pulse is available); Y608 would add a
    preference number, which Food-prep must not.
- **E4 table.**

| aspect | K2 | K4 | K5 | K9 |
| --- | --- | --- | --- | --- |
| a components and joins | X: step-material links, no assembly roles | X | X | P: split and return by percentage (Y608) |
| b intermediates, readiness vs doneness | X: intermediates typed; no endpoint kind | X | X | X |
| c member after assembly | C | C | C | C |
| d why a stage exists | C | C | C | C |
| e alternatives kept apart | P: separate recipes with validity rules (Y608) | P: one formula, two routings | P | - |
| f substitution | X: substitute items with effective dates (Y608), no consequence check | X | X | - |
| g start from a state | C: not in what was read | C | C | C |
| h provenance | C: status and dates, not sources | C | C | C |
| i unknown vs false | C | C | C | C |
| j readable for a person | C: ERP forms | C | C | C |

- **E5.** R1 already types fractions (main output, secondary output); R3
  already keeps routes apart; R4 transfers are recipe flexibility with
  re-validation. Validity conditions (which kitchen, which season, which
  batch size) have no field in Food-prep.
- **E6.** Published: Y608 (all mechanisms), Y610 abstract. Inferred: K
  mappings.
- **Verdict.** Byproduct/co-product typing: **already equivalent.**
  Validity conditions without preference (availability, season, quantity,
  equipment): **extend**; preference ordering: **not suited** (ranking).

### E. HACCP flow diagram, critical control points, critical limits, monitoring

- **E1.** Unit: a step in a confirmed flow diagram, with inputs, intermediates,
  rework, by-products and waste; CCPs at steps where an essential control
  measure is applied; critical limits (observable or measurable, validated);
  monitoring; corrective action; records (Y611). In food service, flows are
  grouped by passes through the temperature danger zone (process approach,
  Y612). Finnish practice: cooling limit with start and end measurement in
  the centre and recording (Y613). Purpose: food safety assurance, not
  culinary knowledge.
- **E2.** International standard and two authority guidances; requirements,
  not evaluated models. The cook-plus-cooling pair as two CCPs for one
  hazard is in Y611; per-food cooking limits inside a common process class
  in Y612.
- **E3 (inferred; classification only, no safety claim).**
  - **K7 arancini (rice route):** flow receive -> store -> cook rice -> cool
    (overnight) -> shape and fill -> coat -> fry -> serve. In Y612's terms
    it has a cook and a cool before a second heat step, which is the shape of
    Process 3 (complex food preparation). Y611 names the cooling step as a
    possible CCP after a cook step. Food-prep's R5 already records the
    authorities' cooling and keeping rules for `cooked_rice` with their
    basis; nothing here adds a new safety value.
  - **K2 raw-soaked falafel:** the flow has no cook before the fry; the
    question R5 left open (is deep-frying a raw pulse paste the required
    treatment?) is in HACCP terms a missing **validated** critical limit at
    the fry step. Y611 says limits must be validated by studies, literature,
    regulation or authorities; structure cannot supply one. The gap stays a
    gap.
  - **K1, K3:** flows with parallel inputs and an assembly; Y611 asks the
    diagram to show where each intermediate enters; Y612 notes menu items
    combine components from different processes.
  - **K9:** the returned starch is "reworking and recycling" in Y611's list
    of what a flow diagram shows.
- **E4 table.**

| aspect | K2 | K3 | K7 | K9 |
| --- | --- | --- | --- | --- |
| a components and joins | P: inputs and intermediates entering the flow (Y611) | P | P | P |
| b intermediates, readiness vs doneness | X: intermediates and holding steps; readiness not a concept | X | P for holding limits; X for readiness | X |
| c member after assembly | C | C: the assembled item is the flow unit | C | C |
| d why a stage exists | X: a CCP states which hazard its control measure addresses (Y611) | X | X: cool exists against spore growth (Y611) | X |
| e alternatives kept apart | C: one flow diagram per product or product group | C | C | C |
| f substitution | C | C | C | C |
| g start from a state | X: a record of when the intermediate was made (Y613 date marking) | X | X | X |
| h provenance | X: limits must cite their validation (Y611) | X | X | X |
| i unknown vs false | X: a hazard without a control measure means the product or process must change (Y611 19.8) | X | X | X |
| j readable for a person | P: CCPs highlighted on the flow diagram (Y611); process classes and a danger-zone diagram (Y612) | P | P | P |

- **E5.** R5 sequences are flow diagrams with more culinary detail; R5
  keeping tables with a "basis" column already separate authority rules
  (food safety) from cooks' rules (cooking), which is the CCP versus
  ordinary-step distinction in other words. Done-when and failed-if are
  observable criteria like critical limits, but they are documented cook
  statements, **not validated limits**, and must not be presented as such.
- **E6.** Published: definitions and flow-diagram contents (Y611); process
  approach and per-food cooking limits (Y612); Finnish cooling check with
  centre measurement (Y613). Inferred: all K classifications.
- **Verdict.**
  - Flow diagram: **already equivalent** (R5 sequences).
  - Critical limit, monitoring, validation: **already equivalent** in the
    basis column; **extend** the wording so that no done-when check is ever
    shown as a safety limit, and so that a food-safety keeping rule says
    what is measured and where (Y613: start and end, in the centre).
  - Process approach (grouping by how many times a food went through the
    danger zone): **adopt the concept** as a recorded history attribute of an
    intermediate (cooked once; cooked and cooled; cooled and reheated), cited
    to Y612, because Food-prep's `from_state` equates states by
    `Material.key()` and so cannot tell a freshly cooked rice from a cooked,
    cooled, kept one. The attribute is descriptive, not a safety verdict.

### F. BPMN and UML activity/state diagrams for cooking

- **E1-E2.** No academic source read models a cooking recipe in BPMN or UML.
  Y615's title promises BPMN but uses an OWL ontology; Y616 is abstract only.
- **Verdict.** **Insufficient evidence.**

## Answers to Q1-Q6 from this area

- **Q1 unit; two traversals.** Industrial models split the unit in two: the
  material state (STN state, ISA-88 material, formula item) and the task or
  procedural element (Y602, Y605, Y608). That is Food-prep's R1 split. ISA-88
  adds a second axis Food-prep lacks: the same procedure at equipment-free
  and equipment-bound levels (Y602, Y603). Traversal from ingredients to
  products is not a published feature of ISA-88; STN graphs can be followed
  either way (inferred).
- **Q2 complete processes.**
  - Parallel components and joins: parallel process stages and SFC branches
    (Y602); intermediate dishes and parallel recipe entry points in a kitchen
    net (Y614).
  - Waits and holds: storage policies UIS/FIS/NIS/ZW (Y605) and maximum
    wait between named stages (Y607) are finer than "how long a state keeps".
  - Secondary outputs and recombination: fractions, byproducts and recycle
    (Y605, Y608); HACCP asks the diagram to show rework, recycling,
    by-products, waste (Y611).
  - Members after assembly: **nothing found**. Every industrial model treats
    the joined material as one material; Y614 collects intermediates and
    assumes doneness is sensed. This confirms Food-prep's known gap is not
    solved elsewhere.
  - Observable completion and failure: SFC receptivities and exception
    transitions (Y602); critical limits "measurable or observable" with
    monitoring and corrective action (Y611). Readiness against doneness: not
    a concept in any source read; ISA-88 only says an operation moves the
    material from one state to another (Y602 p. 138).
- **Q3 substitution.** Industrial practice changes raw materials at the site
  level (Y602 p. 137), with dated substitute items (Y608) or by recipe
  flexibility (Y610, abstract), and re-validates in trial (Y603 4.3.3). No
  model read checks a substitution's consequences inside the process.
- **Q4 alternative routes.** Kept as separate master recipes per cell and
  separate recipe versions (Y602, Y603), and as separate recipes with
  validity rules (Y608). Equipment-dependent variants are the master level.
  A new combination of validated steps is a new recipe needing trial
  (Y603), which supports keeping K1-x and K2-x unverified.
- **Q5 reuse and history.** Two published ideas: a record for an
  intermediate lot that tracks its storage and handling between production
  and consumption (Y604), and the food-service grouping of foods by how many
  times they passed through the danger zone (Y612). Both say that equal
  states with different histories are not interchangeable for safety
  purposes. STN, like `Material.key()`, merges them unless they are made
  separate states (Y605, inferred).
- **Q6 visualisation.** Operator views use step/transition charts with step
  status by colour and a text list for overall status (Y602 6.5); HACCP
  highlights CCPs on the flow diagram (Y611) and uses a danger-zone diagram
  (Y612). None was tested with home cooks.

## Open questions this area leaves

- Clauses 5-8 of ISA-88 Part 3 (formula, procedure, life-cycle states,
  process procedure chart, transformation to master recipes) were not
  readable. Whether the process procedure chart notation suits a home
  cook's route view is unknown.
- How Food-prep would mark a value as equipment-bound (home oven, dish depth,
  pot size) versus route-level, given that most cooks' sources do not state
  their equipment.
- Whether any source documents "zero-wait" or a maximum wait for culinary
  intermediates (raw falafel paste, grated potato for latkes, blanched
  leaves). Nothing read in this area gives one.
- Food-industry shelf-life planning (Lütke Entrup et al. 2005) and the
  food-scheduling structure paper (Akkerman & van Donk) were not readable;
  they may say how industry represents the shelf life of intermediates.
- No industrial or academic model read represents what a member undergoes
  after assembly.
- No French, Italian or Japanese industrial-process source was reached;
  NAMUR NE 33 (German) is paywalled.
