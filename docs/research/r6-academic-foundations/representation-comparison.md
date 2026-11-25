# Food-prep's representation against the literature (Q1, Q2, Q5)

This file takes each layer of what R1-R5 built, sets the approaches read in
R6 beside it, and gives a qualitative verdict with its reasons. Evidence ids
resolve in `sources.md`; the full analyses are in the seven `evidence-*.md`
files. "Inferred" marks a reading made in R6.

The question was whether a better representation already exists, not
whether the literature confirms Food-prep. A framework was not credited for
resembling Food-prep. Where Food-prep turned out stronger, that is said
plainly with the reason; where it turned out weaker, likewise.

## Verdict in one paragraph

**No approach read is a better replacement for any layer of Food-prep's
representation. Eight concepts are worth adopting or extending.**

The academic and industrial models agree on the unit Food-prep already
uses: a step with typed input and output materials whose state changes.
That is R1's operation on a material:
- FOON's functional unit (Y201);
- the OBO planned process (Y100);
- PO2's step (Y102);
- the State-Task Network's state and task (Y605);
- the r-FG's action between food spans (Y501);
- the Trier workflow's task and data item (Y302).

**No model read solves the problem R3 and R5 share: what a member undergoes
after it is joined.** Every model treats the joined material as one
material. R5's documented member endpoints (22 of 28) are further than
anything read.

Food-prep is also ahead on four other points:
- **readiness against doneness**: no counterpart anywhere;
- **structural roles** (container, wrapper, layer): only Y402's per-dish
  role functions come near;
- **keeping documented routes apart** from combinations of their steps;
- **unknown kept apart from false**.

Where the literature is ahead, it offers eight concepts. Each fits the
project's rules: no scores, nothing simulated, provenance kept.
1. ISA-88's **general, master and control recipe levels** (Y602, Y603).
2. **Substitution as violation plus repair** (Y402).
3. **Step correspondence between alternative routes** (Y503), restricted to
   reading.
4. **Objective kept apart from mechanism** (Y101).
5. **Storage-policy classes and a maximum wait** between named steps (Y605,
   Y607).
6. **History recorded for an intermediate** where a rule depends on it
   (Y604, Y612).
7. **Naming the observed member** in a check (PO2's object of interest,
   Y102).
8. **The two traversals as two projections of one graph** (Y100).

## Layer by layer

### R1: operations on one material, three-valued applicability, fractions

| Concept | Literature | Verdict | Reason |
| --- | --- | --- | --- |
| operation = typed input material → output material(s) with new state | FOON functional unit (Y201, Y208); OBO planned process with input and output (Y100, Y104); STN task between states (Y605); r-FG action between food spans (Y501); PO2 step (Y102) | **already equivalent** | the same shape everywhere; Food-prep's state is **typed** (firmness, moisture, cooked ...), where FOON (Y201) and r-FG (Y501) use free labels |
| several outputs (peel + peeled stem; juice + pulp) | FOON output lists (Y201, Y213); STN fractions and by-products (Y605); HACCP diagrams must show by-products and waste (Y611); r-FG splits (Y501 §4.12) | **already equivalent** | the published FOON hash-brown record drops the peel and has no squeeze step (Y213). Splits and recombination are where state-tracking models fail most (Y507) |
| three-valued applicability with reasons (unknown is never false) | none found. OWL is open-world but no source uses it for applicability. Workflows, FOON and STN are closed: a step is there or not | **Food-prep stronger** | no approach read separates "not applicable" from "not known" |
| culinary function of an operation (per-function lists) | objective against mechanism: the same objective reached by different mechanisms (Y101); IAO "intended process endpoint" (Y112) | **extend** | R1's functions are close to objectives. Y101's separation would let R5's alternatives be grouped by what they achieve ("soften the rutabaga before the shared bake"). Y101's own rule, swapping by equal objective, would accept K2-x, so grouping must stay descriptive (AR21) |
| equipment state as readiness (oven preheated, pan hot) | FOON treats utensil states as objects (Y201); r-FG tool spans and preheating branches (Y501) | **extend**, small | not in R5's data (no "preheat" in `processing_conditions.yaml`); add only where sources state it (AR15) |
| `Material.key()` equivalence (part plus resulting state) | every model merges equal labels: FOON by name and state (Y201), Trier by label (Y302), STN by state (Y605), Y113 by type. Ontologies record history but never say when two histories are interchangeable (Y100, Y101). History matters for data comparability (Y101 §1, frozen carrots) and for safety (Y612, danger-zone passes); industry keeps a record per intermediate lot (Y604) | **retain, extend** | the literature confirms `key()` is a **lossy projection, not an error** (Y100 §2.1.2). Keep it for structure; record history only where a source ties a rule to it (soaked raw against quick-boiled, K2-x; cooled twice). Never infer history |

### R2: construction patterns and holding mechanisms

| Concept | Literature | Verdict | Reason |
| --- | --- | --- | --- |
| nine patterns by holding mechanism (H1-H11), water routes (W1-W9) | nothing equivalent found. Y402 has role functions per recipe type; acceptability tuples (Y403) say which material may fill a node; food-science functional-role sources could not be read (AR9) | **Food-prep ahead** (insufficient comparison evidence) | no model read explains why a dish holds together; R2 remains the project's own finding |

### R3: dishes as constructions (routes, materials, six joins with roles)

| Concept | Literature | Verdict | Reason |
| --- | --- | --- | --- |
| independently processed materials joined later | workflow data flow with AND blocks (Y302); DAG with merges (Y501, Y500); ISA-88 parallel process stages (Y602); STN (Y605); FOON trees (Y201) | **already equivalent** | parallel branches and joins are universal |
| six joins with **structural roles** (container, wrapper, layer, coat, matrix, mix) and per-role requirements | Y402 role function per recipe type; acceptability tuples (Y403, Y404); no role in ISA-88, FOON, r-FG or the workflows | **Food-prep stronger** | only roles explain why napa can replace kale, and why curly kale and raw rutabaga fail. Similarity methods endorse both failures (Y206, Y408) |
| recombination derived from fraction origins | r-FG defines splits and recombination (Y501); SIMMR drops them (Y505); models fail most here (Y507) | **already equivalent**; Food-prep checks it | R3 derives 13 links and checks that every fraction is used or discarded; Y507's conservation check is the same idea |
| an assembly takes its carrier's state (the known gap) | **unsolved everywhere**: FOON (Y201), Trier workflows (Y310 §2), ISA-88 and STN (Y602, Y605), ontologies (Y100: OWL cannot keep a member's identity through a change; Y104 assumes parts unchanged). Y507 records per-step world states, but its handling of merges was not verified | **retain R5's documented member endpoints; extend** | nothing to adopt. Two small aids: PO2's **object of interest** (Y102) names which member a check observes; a per-step member state (Y507) is the place to write kitchen-test results (KT6) |
| several containers for one filling; several pieces as one member | Y403 subgraphs; one-to-many is future work in Y408 | **open** (AR6) | no published solution |
| route = one documented way to the dish; dish may have several | separate cases (Y300), graphs (Y501), master recipes and versions (Y602, Y603) | **already equivalent** | see `alternative-routes.md` |

### R4: transfers

| Concept | Literature | Verdict | Reason |
| --- | --- | --- | --- |
| a documented route with one material swapped, re-checked by role requirements | Y402 integrity constraints after a primary substitution; Taaable grafting a documented preparation (Y311); Trier adaptation cases (Y305) | **already equivalent** for detection | see `substitution-impact.md` |
| the repair (blanch, shave the rib) recorded as the answer to a violation; alternative repairs | Y402 minimal secondary substitutions; Proposition 11 shows a repair need not exist (checked in raw text) | **adopt the concept** | makes K1's two repairs (blanch; long covered bake) and K1-x (their combination) visible as what they are |
| driver of the substitution; substitute against analog | Y402 §7 (four drivers); Y401/Y105 (analog) | **extend** | Lidl supply and "a part already bought" are drivers; pea falafel against *vatana vada* is an identity question |

### R5: processing conditions and sequences

| Concept | Literature | Verdict | Reason |
| --- | --- | --- | --- |
| observable done-when and failed-if checks | Grafcet receptivities and exception transitions (Y602); r-FG "until" spans with timing edges (Y500, Y501); RiCoRecA Until (Y502); ontology outcome termination (Y110) and sensing (Y100 Fig. 25); COB "failed planned process" marks an instance, not an observable failure (Y100) | **already equivalent; R5 richer on failure** | failure checks with causes have no counterpart in the cooking literature read (Y310, Y302, Y501) |
| **readiness against doneness** | nothing in any area. The nearest: an objective can be part of a larger objective (Y101); ISA-88 says an operation moves a material from one state to another (Y602 p. 138) | **Food-prep-specific; retain** | the distinction is the user's ("the 3-5 minutes of blanching ... is intended to make it ready for the next operation") and is documented by cooks (Q231, Q330, Q317). No model would have produced it |
| `depends`: a stage exists because of a later one | RiCoRecA's Why tag (Y502); objectives (Y101) | **already equivalent** in concept; R5 ties it to sources | - |
| HACCP critical limits against done-when | critical limits must be **validated**, monitored and corrected (Y611) | **keep apart** | a done-when check is a cook's observation, never a safety limit. R5's `basis` column already separates authority rules from cooks' rules |
| per-source times | master-recipe values: each assumes someone's oven, pot and dish (Y602) | **extend**: the level of a value | most sources do not state their equipment (open question in `evidence-industrial-process.md`), so the mark can only be "equipment stated" or "not stated" |
| active work against elapsed time | STN task durations (Y605); parallel-cooking schedulers (Y709) | **already equivalent** for what a cook needs | schedulers optimise time, which the project does not want |
| intermediates with keeping times and authorities | STN storage policies: unlimited, finite, none, zero-wait (Y605); maximum wait between two named stages in a fish plant (Y607); intermediate-lot records (Y604); Ruokavirasto cooling (Y613) | **extend** | "how long it keeps" covers finite storage. "Use it at once" (zero-wait: grated potato before it browns, falafel paste before frying) and "at most N hours between step A and step B" are not expressible today. No source gave such limits for culinary intermediates (AR14) |
| `alternatives` kept apart; conflicts as versions | ISA-88 versions with trial (Y603); separate cases (Y300) | **already equivalent; Food-prep stricter** | the cooking literature combines steps across sources (Y201, Y300, Y503) |
| `from_state`: routes through a state I have | FOON retrieval from an inventory (Y201, Y206); partial workflows (Y301, defined, not demonstrated); Y402's "onhand" intermediates | **already equivalent** in concept | FOON retrieval composes a new tree from that state, while `from_state` lists documented routes only. Food-prep's is the safer reading |

## Q1: one model, two traversals

Y100 (§2.1.2, Figs. 4-5) states the answer the user suspected. One graph of
processes and materials can be read two ways:
- **object-only:** what derives from what, which is ingredient → dishes;
- **process-only:** which step feeds which, which is dish → how to make it.

Y100 also says what each reading loses. FOON uses one network for both
directions, but going forwards from ingredients needs a dish type and word
similarity (Y206). CBR uses ingredient queries over the same cases (Y300).
No paper read evaluates both directions over many dishes.

**Inferred:** Food-prep's data is already one graph:
- R3 parts feed operations (R1);
- operations make materials;
- materials meet in assemblies;
- assemblies make routes;
- routes make dishes;
- R4 and R5 hang off routes and steps.

"What can I make with dried peas" is a query over constructions and
transfers by part (`dried_peas.dried_seed` appears in `pea_falafel`).
"How do I make it" is the route and its R5 sequence. These are two
traversals of the same data, not two systems. R7 needs a read-only query
for the first; the CLI has only the second (AR16).

The literature also suggests the unit a **person** reads. Cooks were
shown the dish with its component branches (Y703), and ingredients were
used as search queries, not explored as a graph (Y704). So "ingredient"
is the entry point and "dish with routes" is the thing shown.

## Q5: reuse of existing preparations

- **What exists.**
  - FOON starts from a kitchen inventory (Y201, Y206).
  - Trier defines partial workflows and a chaining rule that stops at an
    intermediate already present (Y301), but never demonstrated it.
  - Y402 treats onhand intermediates as assumptions.
  - Industry keeps a record per intermediate lot of how it was stored and
    handled (Y604).
  - Food service groups foods by how many times they passed through the
    danger zone (Y612).
- **Histories.** No academic source defines when two histories give
  interchangeable states.
  - The ontologies say same-named states are comparable only if their
    processing was comparable (Y101 §1, frozen carrots).
  - The safety sources say history matters (Y612).
  - Every computational model merges the states anyway (Y201, Y302, Y605).
- **For Food-prep.** `from_state` is sound in what it lists: documented
  routes only. It is silent on history, and that is the gap. The cases
  where history plausibly matters are named and sourced:
  - K2-x: a soaked-raw pulse against a quick-boiled pulse, for a paste
    that must set in oil (Q114);
  - cooked rice held overnight: K7, with FS7's conflict between
    authorities;
  - a blanched vegetable that is cooled and then reheated: no source
    found.

  Recommendation: record a history attribute on an intermediate only where
  a source ties a requirement to it, and otherwise say "history not
  considered". This is AR2 and FS8 in `open-questions.md`.

## Retain, extend, replace

| Layer | Recommendation | Why |
| --- | --- | --- |
| R1 operations, applicability, fractions | **retain** | same unit as the literature, richer state, the only three-valued applicability found |
| R1 `Material.key()` | **retain, extend** with sourced history | a lossy projection, as the literature says; it is the safety cases that need history |
| R2 patterns and mechanisms | **retain** | nothing comparable found |
| R3 constructions and roles | **retain**; extend member checks with object of interest | roles outperform every substitution method read on K6 and K8 |
| R3 assembly gap | **retain R5's documented endpoints**; fill from kitchen tests | unsolved everywhere; no simulator (project rule) |
| R4 transfers | **retain, extend** with violation, repair and driver | Y402's concept, untested on real recipes, but on paper it explains K1 and K1-x |
| R5 conditions and sequences | **retain, extend** with value level, storage class, step correspondence, `compensated_by` | readiness against doneness and failure checks are ahead of the literature |
| Interface | **replace the mindmap as the decision view** (not the data) | `visual-representations.md` |
| External frameworks (FOON, CBR workflows, ISA-88 software, OWL ontologies) | **do not adopt** as an implementation | each was built for another user (robot, adaptation engine, plant, data integration). Each would lose roles, three-valued applicability or route separation. None was tested on cooking outcomes |
