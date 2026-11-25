# What happens to a cooking process when a component changes (Q3)

Synthesis of `evidence-substitution.md` (Y401-Y420), `evidence-cbr-workflows.md`
(Y300-Y313) and `evidence-foon-robotics.md` (Y201-Y219), applied to the fixed
cases. Y ids resolve in `sources.md`. "Inferred" marks a reading made in R6,
not a result any paper publishes.

## Short answer

A substitution is a **primary change** that breaks some of the
requirements the original route met, followed by zero or more **repairs**
(secondary changes) that restore them. Only one published line of work
models it this way: the UCL commonsense framework and its graph formalism
(Y402-Y404). It detects violated integrity constraints after the primary
substitution and searches for minimal secondary substitutions. It also
proves that a repair need not exist. **None of it was tested on real
recipes or cooked.**

Food-prep's R4 already does the detection half:
- R4 re-runs R3's role requirements on the swapped route, for example
  "a wrapper must bend" or "a layer must not cook slowly unless blanched".
- That is the same idea as Y402's integrity constraints, applied to
  documented routes.

What R4 lacks is the second half:
- the repair is not recorded as **the answer to a named violation**;
- several repairs of one violation are not kept as alternatives.

The gratin shows both gaps at once:
- the violation is `cooks_slowly` in a shared bake;
- two documented repairs fix it: blanch the rutabaga, or bake longer and
  covered.

Substitutability is decided by:
- the material's **role in this construction**;
- its **current state**;
- its **processing requirements relative to the members it is processed
  with**.

Identity alone does not decide it. Identity and category similarity are
what statistical substitute finders use. They are the weakest predictor in
the evidence read, and they would endorse the two substitutions Food-prep
rejected (K6, K8).

## What substitutability depends on, in the evidence

| Factor | Published evidence | Food-prep now |
| --- | --- | --- |
| Identity or category | taxonomy distance (FoodOn, Y408); composition-table weights (Y405); ontology generalisation (Taaable, Y413); WordNet or word similarity (FOON, Y202, Y206) | not used to decide; families exist for the Taste Circle only |
| Functional role in this dish | role function per recipe type (Y402 §4.1); recipe-relative acceptability: aquafaba replaces egg in baking, not in an omelette (Y403 §7); egg in a cake against in a glaze (Y414) | **R3 roles with `requires`** (container, wrapper, layer, binding ...) on every assembly |
| Current material state | the one impossible case in Y405: steamed rice where uncooked rice works; SHARE's judges could not tell raw from pre-processed ingredients (Y412); data-driven methods strip state (Y406, Y408) | R1 state flags on every material; R3 checks them at each join |
| Processing requirements | characteristic actions (Y405); duration and preparation constraints (Y402 §8.1); acceptability tuples (Y403-Y404) | R1 applicability per operation; A2 `cooks_slowly` |
| Other components (shared heat, shared equipment) | one oven at one temperature for several items (Y402 Ex. 52); an ingredient removed that a later step uses (Y413) | only through A2's layer requirement; no shared-equipment notion |
| Driver of the substitution | similarity to the item, to the dish, minimal change, or a property (Y402 §7) | implicit: Lidl availability and cost (R4 `lidl`) |
| Dish identity | a named dish keeps its defining ingredient (Y402 Ex. 43); the main complaint about edited recipes (Y412 §6); "analog" against "substitute" (Y401) | not recorded; falafel from peas is still called falafel, and in India *vatana vada* (R4) |

**Inferred:** the decisive factors are the three Food-prep already holds:
- the role, as R3 `requires`;
- the state, as R1 flags;
- processing relative to co-processed members, as A2.

The literature adds two factors Food-prep does not record: the **driver**
and **dish identity**.

## The draft categories against the literature

The user's draft is compared in full in `evidence-substitution.md` (Q3,
table). In short:
- the draft is **equivalent** to Shidochi's outcome scale (Y405: fine /
  needs change / impossible / hard to judge) at its ends;
- it is **finer** in the middle, because it names "structural" and
  "affects other components" as outcomes;
- Y402 has these as mechanisms (term, condition and clause substitution)
  but gives them no outcome labels.

The literature adds categories the draft lacks:
- **omission** as a substitution (the empty substitute, Y401, Y406);
- a **quantity or ratio change** with no new ingredient (Y406; Y401);
- **dish identity changes**: the result is an analog with another name
  (Y401, Y402, Y412);
- **fits, but the quality changes**: feasibility kept apart from taste
  (Y411: the two are weakly negatively correlated; Y402: "consistent"
  against "similar dish");
- **one-to-many**: several pieces for one, such as overlapped small leaves
  (Y408, future work).

The draft has one category no automatic method has: **insufficient
evidence**. Closed-world logic (Y402) and every learned finder (Y406-Y410,
Y420) must answer yes or no. Only human-judged scales allow "hard to
judge" (Y405).

### Revised outcome set (R6 proposal, on paper only)

A substitution outcome has two parts:
- the **kind of repair** the evidence documents;
- a **status** for the result.

They are kept apart because a substitution can be structurally repaired
and still be untested (K2), or work and change the dish (an analog).

**Repair kinds** (several can apply to one substitution):

| Repair kind | Meaning | Case |
| --- | --- | --- |
| none | the role's requirements hold as they are | K3 napa leaf as a wrapper (it bends; one leaf per roll) |
| parameter | the same operations, with another time, size, temperature or cover | K8's working route: raw slices with about 90 min covered (G7, G8); K3 a covered bake with liquid (Q313, Q317, N9) |
| added or changed operation | a step is added to, or changed in, the substituted material's own chain | K1 blanch the rutabaga (G1, Q231); K5 peel the stem (B ids, R4); K3 shave the rib |
| structural | the assembly changes: another join, several pieces per member, several containers for one filling | K6 two or three overlapped curly-kale leaves as one wrapper (K13); K4 onion and courgette vessels in one tray (O3, O5) |
| cross-member | a repair applied to another member or to the shared step | K1 the longer covered bake changes the potato's bake too; K4 the filling cooked for two kinds of vessel |
| omission or quantity | an ingredient dropped or its amount changed | not needed by K1-K9; listed because the literature has it |

**Result status:**

| Status | Meaning | Case |
| --- | --- | --- |
| documented | the substituted route is found in practice, with its repairs | K1, K3, K4, K5, K2 (R4 `status: documented`) |
| documented, quality risk | found in practice; a source reports a worse result | K2 pea falafel: dry and hard (P15) |
| documented failure | a source reports that it fails | K8 raw short bake (G20, G21) |
| analog | works, but makes another dish | not among K1-K9; R4's pea falafel is still called falafel |
| no documented practice | structurally plausible, not found in practice | K6 curly kale |
| combination not documented | each repair is documented separately, the combination is not | K1-x, K2-x |
| safety not established | structure and tradition cannot settle it | K2 raw-soaked pea paste (Q505) |

None of these is a score. They are statuses that sit beside R4's existing
`verdict` and `evidence_says`. They do not replace them.

## How inconsistencies are found and repaired, by approach

| Approach | Detects | Repairs | Validated by cooking | Fit for Food-prep |
| --- | --- | --- | --- | --- |
| UCL primary/secondary substitution (Y402) | violated integrity constraints, minimal inconsistent subsets | minimal secondary substitutions of terms, conditions, clauses; proves when none exists | no | **adopt the concept**: name the violation and record the repair as its answer |
| Acceptability tuples, structural substitution (Y403, Y404) | a node or subgraph that is unacceptable in this recipe | swap a subgraph | no (CPU time only) | **already equivalent** to R3 roles; extend for one filling in two vessels (K4) |
| Trier stream substitution (Y302, Y300) | data-flow interface by ingredient **names** | swap a sub-workflow with the same inputs and outputs | no; 44-46% of expert ratings put the adaptation below the original | **not suited**: names without states let K1-x and K2-x through |
| Adaptation operators, add and delete lists (Y305, Y300 §3.3) | none: learned from pairs of cases | apply the stored change | no | **already equivalent** to an R4 transfer's changes, which are documented and not learned |
| Taaable grafting (Y311, Y413) | an ingredient whose preparation is missing | graft the new ingredient's preparation from another recipe | no | **already equivalent** to R4 taking a documented material chain from another dish |
| Revision with temporal constraints (Y309, Nancy, IJCAI 2013) | conflicts in durations and order after a swap | reorder steps by cooking time (carrot risotto) | no; one example | **extend** on paper only: a documented duration relation between members is what K8's false negative lacks |
| FOON similarity substitution (Y202, Y206) | humans reading progress lines | top-5 similar objects; a person chooses | no; 76% of recipes fully correct, 39% of errors were wrong substitutes | **not suited**: kale → cabbage is a published top-5 pair, so a K6 check would pass |
| Statistical finders (Y406-Y410, Y420) | none | a ranked list of substitutes | no; review-mined or self-extended ground truth | **not suited**: the guide behind Y408 lists rutabaga for potato with no condition (K8's false positive) |
| Food-science functional roles (binders, egg replacers) | - | - | - | **insufficient evidence**: no source could be read in R6 |

## The cases

- **K1 rutabaga gratin.**
  - Primary change: a layer that `cooks_slowly`.
  - Violation: the layer requirement in a shared bake, R4's A2. This is
    Y402's case of one oven for items with different needs.
  - Documented repairs, as alternatives:
    1. an added operation on the member: blanch 3-5 min (Q231);
    2. a parameter change on the shared step: a covered bake of about
       90 min (G7, G8);
    3. a changed operation: simmer in the gratin liquid (G5, G9);
    4. pre-cooking both members (Q232).
  - Food-prep records the first as the route and the others as
    alternatives, but not as answers to the same violation.
  - **K1-x** combines repair 1 (in its 10-min version, G16, G18) with
    repair 2. Each half is documented; the combination is not, and the
    longer blanch plus the longer bake may overcook. No source states the
    over-blanch failure (R5 limitations).
- **K8 raw-rutabaga gratin.**
  - The model accepted it before A2: a false positive, because it had no
    rate difference.
  - After A2 it still rejects repair 2 (the long covered bake): a false
    negative, because time is not in the model.
  - Y402's and Y309's duration constraints are the published concepts that
    would hold the difference. The project's rules allow it only as a
    **documented relation** ("the longer covered bake replaces the
    blanch", G7, G8), never as a computed one.
- **K2 chickpea → dried peas.**
  - The role is the H3 raw pulse paste. The state requirement (raw,
    soaked, ground) is met, so no structural repair is needed.
  - Parameter and operation repairs: grind coarse, keep the onion (P4).
  - Status: documented, with a quality risk (P15). Safety is not
    established (Q505).
  - **State dependence is the point:** soaked-raw against cooked peas
    produce different constructions. The cooked kind is the American
    bound mash (R2 finding 1). That is Y405's steamed-rice failure in
    another form.
- **K3 kale → napa** (and **K6 curly kale**).
  - The wrapper role needs a leaf that bends and is large enough.
  - Napa meets it with a rib repair (shave it) and a parameter repair
    (a covered bake).
  - Curly kale would need a structural repair (several overlapped leaves,
    one-to-many), and no practice was found. Status: no documented
    practice.
  - Similarity methods rate the kale-cabbage pair highly (Y206 Fig. 7;
    Teng's clusters, Y701). Only a role-plus-evidence check refuses it.
- **K4 courgette → onion vessel.**
  - The container role is kept.
  - The operation repair: lift out the inner layers instead of scooping
    the flesh (R4 records this as `creuser`).
  - A parameter repair: do not overboil, or the layers slip (O12, O15).
  - Cross-member: one filling for two kinds of vessel in one tray. This is
    R3's known schema gap. Y403 has subgraphs but no container role.
- **K5 carrot → broccoli stem.** An added operation (peel the stem) and a
  quantity issue: one stem is 100-150 g, so it is mixed with carrot. This
  is one-to-many in reverse: two materials fill one role.
- **K7 arancini, boiled rice → risotto rice.**
  - A documented second route, not a substitution. The rice reaches the
    same role (a cohesive cooled mass) by another operation.
  - In Y402's terms it is a clause substitution with an empty mitigation.
  - **Inferred:** the two routes meet at "cooled cooked rice", which is the
    reuse point Q5 asks about.
- **K9 latkes.** Substituting flour for the settled starch is a documented
  variant (R2 kitchen test 1): an ingredient replaces a secondary output.
  None of the substitution literature read represents a by-product as a
  candidate substitute, except Y404's by-products for reuse across
  recipes.

## Recommendation for Q3

- **Retain** R4's model:
  - a transfer is a documented route with one material swapped;
  - it is re-checked by R3's role requirements;
  - its verdict is cited.

  The literature has no better published detection method that has been
  tested on real recipes. Statistical and similarity methods are worse for
  this user, because they endorse K6 and K8.
- **Extend** (data only, a later round, not R6):
  1. Record each added or changed step on a transfer as the **repair of a
     named violation**, with its sources (Y402's concept).
  2. Keep several documented repairs of one violation as alternatives,
     marking a combination of repairs as not documented.
  3. Add `driver` (Lidl supply, cost, a part already bought) and a
     substitute-or-analog flag (Y401).
  4. Add the outcome statuses above that R4 lacks: "analog", "combination
     not documented" and "safety not established".
- **Do not adopt:**
  - learned or similarity-based substitute finders;
  - stream or operator recombination;
  - any automatic acceptance of a repair that is not documented.
- **Open:**
  - functional-role evidence from food science (binders, egg replacers)
    was not read;
  - no published protocol compares a substituted dish with the original in
    a kitchen. R4's kitchen tests are, as far as R6 reached, the stronger
    ground truth.

  Both are in `open-questions.md`.
