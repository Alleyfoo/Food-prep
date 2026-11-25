# Case studies: K1-K9 across the approaches

The cases were fixed in `research-brief.md` before any reading. Each case
below is mapped, on paper, into the approaches it tests. Every mapping is an
**R6 inference** from the published concepts, which carry Y ids. No
external framework was implemented.

The full per-aspect tables (aspects a-j: components, states, members after
assembly, dependencies, alternatives, substitution, starting state,
provenance, unknown against false, readability) are in each area's evidence
file, under "Approach analyses".

Approach abbreviations:
- **ONT:** OBO/FoodOn and PO2 process ontologies (Y100-Y104);
- **FOON:** functional object-oriented network and task-tree retrieval
  (Y201-Y206);
- **WF:** Trier cooking workflows, streams and generalisation (Y300-Y303);
- **TAA:** Taaable (Y311);
- **LOG:** UCL substitution logic (Y402-Y404);
- **RFG:** recipe flow graph and cross-recipe alignment (Y501, Y503);
- **ISA:** ISA-88 recipe types (Y602, Y603);
- **STN:** State-Task Network with storage policies (Y605, Y607);
- **VIS:** component-branch overview (Y703) and aligned comparison (Y707).

Outcome words: **preserved**, **extend** (needs an extension), **cannot**
(cannot be represented).

## K1 Potato-rutabaga gratin

Food-prep holds:
- R4 transfer `rutabaga_gratin` on `gratin_dauphinois`;
- R5 sequence: blanch (readiness) → layer → bake (doneness);
- member endpoints: potato "no resistance"; rutabaga "some give" against
  "no resistance";
- `depends`: blanch because of the bake;
- four alternatives.

| Approach | How it would hold K1 | Survives | Lost |
| --- | --- | --- | --- |
| FOON | units: slice → blanch → layer → bake; the gratin node carries the state | components, intermediate states | members after the bake (the composite holds the state); why the blanch exists; times (Y201, Y217) |
| WF | AND block (potato branch ∥ rutabaga branch) → layer → bake; "until crisp-tender" as a text facet (Y308) | components, parallelism | readiness against doneness; failure; members after the join (Y310 §2) |
| LOG | primary: potato → rutabaga in a layer role. A duration constraint in the shared oven is violated; secondary repairs are a blanch, or a longer bake (Y402 §8.1, Ex. 52) | **the dependency, as a repair**; alternative repairs | sources per repair; never cooked |
| RFG + alignment | one flow graph per source; aligned, "bake" matches "bake" in all routes and the blanch aligns to "none" in the long-bake route (Y503) | alternatives kept as separate graphs | why the long bake needs no blanch (duration dropped, Y503 §3.4); K1-x would come out of transitive composition |
| ISA | **general recipe**: stages prepare, pre-cook rutabaga, assemble, bake, rest, with parameter ranges and sources. **Master recipe**: this oven, this dish, covered or not. **Control recipe**: tonight's batch, the kitchen test (Y602, Y603) | the level of each value; the kitchen test as a record | members after assembly; why the blanch exists |
| VIS | two branches joining at "layer"; four routes as aligned columns | what a cook chooses between | no evaluated form for "some give against no resistance" |
| **Food-prep now** | all of the above except the value level and the repair link | members after the join (documented), dependency, alternatives, conflicts | the long-bake alternative is text, not a walkable route; the model rejects it (K8) |

**Finding.** Food-prep already holds more of K1 than any single approach.
LOG explains the dependency as a repair; ISA explains which values belong
to the kitchen. Both are worth taking. Neither can say what the rutabaga
is like at the end: that is KT1.

## K2 Chickpea against dried-pea falafel

Food-prep holds:
- `falafel/raw_soaked`: soak (readiness), grind, rest, fry (doneness);
- transfer `pea_falafel`, documented, with the P15 quality risk;
- the Q505 safety gap.

| Approach | How it would hold K2 | Survives | Lost |
| --- | --- | --- | --- |
| FOON | chickpea → pea by WordNet or word similarity (Y206) | a candidate | the state requirement (raw, soaked); wrong substitutes were 39% of errors in the published evaluation (Y206, checked in raw text) |
| WF / TAA | an adaptation case or operator, chickpea → pea, with its task changes (Y305); Taaable grafts the pea's soak from another recipe (Y311) | the swap with its steps | why it holds (H3); the safety question |
| LOG | a type substitution in a paste role; acceptability of a raw-soaked node (Y403) | structure | quality (P15), safety |
| RFG | soak, grind, shape and fry as actions; "until golden" as a state span | the sequence | the never-cook constraint (Q114) is not an action property; **K2-x** aligns a 5-min boil with an overnight soak (Y503 categories) |
| ONT | "hydrated pulse" as an objective. Y101's swap-by-objective would accept a quick boil | the objective | **K2-x** is accepted: "hydrated" is not enough (AR21) |
| ISA | a new raw material at site level, re-validated by trial (Y602 p. 137, Y603) | the trial requirement | - |
| **Food-prep now** | role H3 (raw pulse paste) checked; state flags raw and soaked; documented transfer with a quality risk; safety recorded as a gap | the state dependence; the quality risk; the gap | whether frying is the required "treatment" (FS1); the pea "soaked enough" check (KT7) |

**Finding.** Every similarity or objective method would let K2-x through.
Food-prep's state flags and source-bound routes stop it. No source read can
settle the safety question.

## K3 Napa-cabbage rolls

Food-prep holds `kaalikaaryleet` (inner leaves; trimmed rib) and the
transfer `napa_cabbage_rolls`. The rice member "finishes in the roll", and
the bake is covered with liquid.

| Approach | Survives | Lost |
| --- | --- | --- |
| WF, ISA (parallel stages), RFG | three branches (leaves, rice, meat) and a join (Y302, Y602, Y501) | the rice finishing after the join (Y602: one material after assembly) |
| LOG | a wrapper requirement (bends, large enough), as an integrity constraint | - |
| FOON | kale → cabbage is a published top-5 similar pair (Y206 Fig. 7, checked in raw text) | the reason it works or fails |
| VIS | "what runs in parallel": the component-branch overview (Y703) | - |
| **Food-prep now** | branches, the wrapper role, member endpoints for the leaves and rice (Q317 "lekko al dente"), the rib repair, the covered bake | the Finnish source does not state a cover; the rice endpoint after the bake has no source (KT6) |

## K4 Stuffed onion halves against courgette vessels

| Approach | Survives | Lost |
| --- | --- | --- |
| LOG, Y403 | a container node; structural substitution of a subgraph | no container role; one filling for two vessels needs one-to-many (AR6) |
| ISA | one filling stage feeding two container stages | no structural role |
| WF | two container branches into one bake | the onion's different preparation must be an operator (Y305) |
| **Food-prep now** | the container role (`farcir`), the onion as lifted inner layers (`creuser`), the overboil failure (layers slip, O12, O15) | several containers for one filling (R3 schema gap); the onion's layer structure is stood in by `creuser` (R4 limitations) |

**Finding.** No approach has structural roles, so none can say why an onion
half stands as a vessel. Food-prep's role check is the stronger
representation here.

## K5 Broccoli-stem patties

| Approach | Survives | Lost |
| --- | --- | --- |
| FOON, RFG | peel as a split with two outputs (Y201, Y501) | FOON's published hash-brown record drops the peel (Y213); the stem as a reused part is not a concept |
| STN | the stem as a by-product state of another process (Y605) | - |
| VIS | "what can I do with the stems?": no evaluated leftover interface found | - |
| **Food-prep now** | R1 peeling produces the peeled stem and the peel; the transfer mixes the stem with carrot (one stem is 100-150 g) | the cooked-inside check for a grated stem (KT6); the amount is evidence, not a property |

## K6 Rejected curly-kale rolls

| Approach | Verdict it would give | Why |
| --- | --- | --- |
| FOON similarity (Y206), Teng's substitute clusters (Y701), substitution guides (Y408) | **accept** | kale and cabbage are near neighbours in every similarity space |
| LOG (Y402) | accept if the leaf meets the wrapper constraint; leaf size is not in its examples | closed world: no "insufficient evidence" |
| **Food-prep now** | **not worth it**, with reasons | the wrapper role needs large leaves; every kale roll found uses large flat kale; curly kale at Lidl comes in small bags (R4) |

**Finding.** K6 is the clearest case where context-free substitution
methods give the wrong answer for this user. A role check plus documented
practice gives the right one.

## K7 Arancini

| Approach | Survives | Lost |
| --- | --- | --- |
| STN | cooled rice mass as a state with finite storage (Y605) | - |
| ISA Part 4 | the night-before rice as an intermediate lot with a storage and handling record (Y604) | - |
| ONT, RFG | two routes, boiled against risotto rice, meeting at "cooled cooked rice"; correspondence is possible but not done (Y503) | - |
| FOON | nested wrap and coat as units; the composite holds the state | the three patterns nesting is only implicit |
| **Food-prep now** | three nested patterns (C2, C7, C9), `refroidir` makes the rice cohesive, two routes | a keeping time for cooled rice conflicts between authorities (FS7); `from` would match both routes' cooled rice by `key()` only if their states agree |

**Finding.** K7 is the plainest "prepare tomorrow" case. The industrial
storage-policy and lot-record concepts fit it. History matters only through
the rice-holding rule.

## K8 Raw-rutabaga gratin

| Approach | Short ordinary bake (G20, G21: fails) | Long covered bake (G7, G8: works) |
| --- | --- | --- |
| R4 before A2 | accepted (**false positive**) | accepted |
| R4 after A2 (now) | rejected | rejected (**false negative**) |
| RFG alignment | indistinguishable from the long bake ("bake" = "bake", Y503) | indistinguishable |
| ISA | a procedure judged without its formula parameters: both errors come from this (inferred) | a separate recipe; valid once in trial |
| LOG, Y309 | a duration constraint violated | a duration repair (Y309 reorders by cooking time; one example) |

**Finding.** K8 shows that structure alone gives a false positive and a
false negative on the same dish. The fix supported by the literature, and
allowed by the project's rules, is a **documented** parameter relation:
"the longer covered bake replaces the blanch, G7, G8". Food-prep would
record it as `compensated_by` (`alternative-routes.md`), not compute it.

## K9 Latkes

| Approach | Survives | Lost |
| --- | --- | --- |
| RFG | split (squeeze: juice and pulp), settle (starch and water), recombine (Y501 §4.12) | the most frequent model failure in state tracking (Y507) |
| SIMMR | - | splits are dropped (Y505) |
| STN | by-products and recycle (Y605) | - |
| LOG | flour substitutes for the settled starch: a by-product as a substitute is not in its examples | - |
| VIS | - | no evaluated visual form for a secondary output rejoining (`evidence-visualisation.md`) |
| **Food-prep now** | `decanter` gives settled starch and liquid; the validator derives the recombination link | - |

## Across the cases

- **Members after assembly** (K1, K3, K4, K5): no approach preserves them.
  Food-prep's documented endpoints are the most complete record found.
- **Unverified combinations** (K1-x, K2-x): produced as normal output by
  FOON retrieval, Trier streams and generalisation, alignment aggregation
  and swap-by-objective. Refused only by ISA-88's trial rule and by
  Food-prep's route separation.
- **Context-free substitution** (K6, K8): wrong for this user in both
  cases.
- **Time as a documented relation** (K1, K8): the one real gap the
  literature helps to name: LOG's duration constraints, ISA's formula
  parameters and Y309.
- **Readiness against doneness** (K1, K3): present in Food-prep only.
