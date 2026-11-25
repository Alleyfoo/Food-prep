# R6 research brief: scope, fixed cases and evaluation protocol

Written 2026-11-25, **before any source was read** in this round, so the
cases and the questions cannot be chosen to suit what the literature turns
out to say. The user's full brief is the specification; this file restates
the parts the evidence agents and the comparison need, and fixes the
examples.

## Question

How do established academic and industrial approaches represent culinary
transformations, complete cooking processes, ingredient substitutions and
alternative routes to finished dishes, and is there a better representation,
method or concept than what Food-prep built in R1-R5?

The aim is to find out, not to confirm. A framework is not preferred because
it resembles Food-prep, and none is preferred because it is new.

## Scope

- Research and documentation only. No change to `src/`, `tests/`, schemas,
  culinary data, or any R1-R5 result or frozen file.
- No interface implementation (that is R7), no generator, scoring model,
  ML experiment or heat/moisture simulator.
- No claim of culinary success without a kitchen test; no claim of food
  safety from structure or tradition alone.
- A conceptual mapping on paper is enough. External frameworks are not
  implemented.

## Research questions (from the user's brief)

- **Q1** Unit of representation; one model, two traversals
  (ingredients to dishes, dish to how to produce it)?
- **Q2** Complete processes: parallel components, waits, intermediate
  states, secondary outputs and recombination, assembly and members after
  it, parameters and objectives, observable completion and failure,
  readiness against doneness.
- **Q3** When is an ingredient genuinely substitutable; how do models find
  and resolve the inconsistencies a substitution introduces?
- **Q4** Alternative routes to the same dish: variants against different
  products against unverified combinations of documented steps.
- **Q5** Reuse of existing preparations; are apparently equivalent states
  interchangeable when their histories differ?
- **Q6** Visualisation for a person deciding what to cook.

## Fixed cases

Chosen from existing R3-R5 records only. Ids K1-K9 are used in every R6
document. Data locations are given so a mapping can be checked against what
Food-prep actually holds.

| Id | Case | Food-prep records | What it tests |
| --- | --- | --- | --- |
| K1 | **Potato-rutabaga gratin** | transfer `rutabaga_gratin` on `gratin_dauphinois`; R5 sequence `transfer:rutabaga_gratin`; 4 alternative sequences; A2 `cooks_slowly` | processing dependencies (blanch exists because of the bake), alternative heat routes, member endpoints after layering, conflicting doneness (some give / no resistance) |
| K2 | **Chickpea against dried-pea falafel** | `falafel/raw_soaked`; transfer `pea_falafel`; R5 pulse pairs; Q505 safety gap | substitution of the main material; hydration (soak), grinding, binding without additive (H3 raw pulse paste); quality risk (P15 dry, hard); the raw-soaked paste safety question |
| K3 | **Napa-cabbage rolls** | `kaalikaaryleet` (`inner_leaves`, `trimmed_rib`); transfer `napa_cabbage_rolls` | independently prepared components (leaves, rice filling, meat), wrapper substitution, assembly, members after the bake (rice finishes in the roll) |
| K4 | **Stuffed onion halves against courgette vessels** | `zucchine_ripiene` (`cooked_flesh`, `blanched_flesh`); `farcis_nicois`; transfer `onion_vessel` | structural function (a container), different preparation of the container (onion layers slip if overboiled), one filling for two kinds of vessel |
| K5 | **Broccoli-stem patties** | `carrot_patties` routes; transfer `broccoli_stem_patties` | reuse of a secondary material (a stem often discarded), peeling as a prerequisite, binding (egg, crumbs) |
| K6 | **Rejected curly-kale rolls** | transfer `kale_rolls` (`not_worth_it`) | failed or unsupported substitution: structurally plausible, no documented practice with curly kale, small leaves |
| K7 | **Arancini** (added established construction) | `arancini` (`arancini`, `suppli` routes) | three nested patterns (cooked-starch mass wraps a filling and is coated), a cooled cooked starch made the night before (a reusable intermediate), two routes that cook the rice differently (boiled against risotto) |
| K8 | **Raw-rutabaga gratin** (added negative case) | transfer `rutabaga_gratin_raw` (`rejected`); R5 alternative (a) raw slices with a ~90 min covered bake (G7, G8) | a documented failure (G20, G21) that the model accepted before A2, and a working route the model would still reject (time is not in the model): a false positive and a false negative of structural checking |
| K9 | **Latkes** (added for secondary outputs) | `latkes/settled_starch` | a secondary output (settled starch from the squeezed juice) returned to the mass: recombination inside one dish |

Two sub-cases of K2 and K1 are kept for Q4, because they are **unverified
combinations of documented steps** rather than documented routes:
- K2-x: a "quick soak" by boiling 5 min (Q109) put into the raw-soaked route,
  which another source says must never be cooked (Q114);
- K1-x: the 10 min "almost tender" blanch (G16, G18) followed by the long
  covered bake of the raw-slice route (G7, G8). Each half is documented; the
  combination is not.

## Evaluation questions (fixed before reading)

For each academic or industrial approach (one at a time):

- **E1 Representation.** What is its actual unit (ingredient, action,
  object-state, workflow, recipe text span, batch phase)? What is it for
  (robot planning, retrieval, adaptation, annotation, scheduling,
  knowledge integration)?
- **E2 Published evidence.** What does the paper show it can do: dataset
  size, evaluation, implementation, user study? Separate what is
  demonstrated from what is claimed.
- **E3 Mapping K1-K9 on paper.** Express the relevant cases in its
  concepts.
- **E4 What survives.** For each case: preserved / needs an extension /
  cannot be represented, for these aspects:
  - a. independent components and their joins;
  - b. intermediate states, readiness against doneness;
  - c. what a member undergoes after assembly;
  - d. why a stage exists (dependency, objective);
  - e. alternative routes kept apart, each with its evidence;
  - f. substitution and its consequences elsewhere in the process;
  - g. starting from a state the cook already has;
  - h. provenance: every claim to a source;
  - i. unknown kept apart from false;
  - j. what a person deciding what to cook can read from it.
- **E5 Comparison** with the current Food-prep representation (R1
  operations, R2 patterns, R3 constructions, R4 transfers, R5 conditions).
- **E6 Published against inferred.** Mark every capability as published
  (with the source id) or inferred in R6.

**Verdict vocabulary** (qualitative, with reasons and citations):
- *adopt the concept*: Food-prep lacks it and should take it;
- *already equivalent*: Food-prep has it under another name;
- *extend*: Food-prep has part of it;
- *not suited*: built for another user or another question;
- *insufficient evidence*: not enough published to judge.

No weighted scores and no overall numerical ranking.

## Evidence rules for agents

1. **Read papers.** Find with search; read the full text where accessible
   (publisher open access, PMC, arXiv, university repository, author copy).
   Say which version was read (publisher, arXiv vN, repository PDF). A paper
   seen only as an abstract is marked **abstract only**; a snippet is not
   evidence.
2. **Never invent** a URL, DOI, author, year or venue. If a detail could
   not be verified, say "not verified". Never construct a URL by guessing a
   path.
3. Record every URL read and every page that failed (paywall, 403,
   ResearchGate block, timeout), with the fallback tried.
4. **Paraphrase.** Quotes under 15 words, only for a definition that matters.
5. **Follow citations** backward (what the paper builds on) and forward (who
   cites it: Semantic Scholar, Google Scholar listings if readable, the
   publisher's "cited by").
6. **Multilingual.** Include non-English work where it exists (German CBR
   work from Trier, Japanese recipe-flow work, French INRAE process
   ontologies, Italian, Spanish).
7. Prefer primary research, datasets, implementations and evaluated methods
   over surveys and general descriptions. A survey may point to primary work.
8. Do not use your own knowledge of a paper as evidence. If it was not read,
   it is not cited as read.
9. Date read: 2026-11-25.

## Evidence file format (each agent writes one file)

```
# Evidence: <area>
(date, method, search languages, what was blocked)
## Sources
### Ynnn — URL actually read
- citation: authors, year, title, venue, DOI (each "not verified" if not)
- version read: publisher full text | PMC | arXiv vN | repository PDF | abstract only
- type: primary research | dataset | standard | survey | thesis | implementation
- what it represents (E1), what it shows (E2), with section/figure pointers
## Failed pages and abstract-only
| URL or query | why | fallback tried |
## Searches
| language | query | useful? |
## Citation trail
backward and forward links followed, with Y ids
## Approach analyses
### <approach name>
- E1 representation and purpose
- E2 published evidence (demonstrated / claimed)
- E3 mapping of the relevant cases K1-K9 (on paper)
- E4 table: aspect a-j x relevant case: preserved / extend / cannot, one reason each
- E5 against Food-prep (which R round's concept it meets)
- E6 published (Y id) vs inferred in R6
- verdict (vocabulary above) with reasons
## Answers to Q1-Q6 from this area
only what this area's evidence supports; "nothing found" is a result
## Open questions this area leaves
```

Id ranges, one per area:

| Area | Ids | File |
| --- | --- | --- |
| Food process and recipe ontologies, operation objectives | Y100-Y199 | `evidence-ontologies.md` |
| FOON and robotic cooking knowledge | Y200-Y299 | `evidence-foon-robotics.md` |
| Case-based reasoning and workflow adaptation (CookingCAKE, ProCAKE, Trier) | Y300-Y399 | `evidence-cbr-workflows.md` |
| Ingredient substitution | Y400-Y499 | `evidence-substitution.md` |
| Recipe flow graphs, annotation and procedural NLP | Y500-Y599 | `evidence-recipe-graphs.md` |
| Industrial batch, planning and process diagrams (ISA-88, BPMN, HACCP flow, routings, Petri nets) | Y600-Y699 | `evidence-industrial-process.md` |
| Visualisation of recipes and culinary knowledge | Y700-Y799 | `evidence-visualisation.md` |
