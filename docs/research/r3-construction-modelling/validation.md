# R3 step 3: expressiveness and traceability (design set)

The 27 design dishes (`dish-selection.md`) are recorded in
`src/foodprep/data/constructions.yaml` and checked by
`foodprep.constructions.validate`. The full per-route table, with step counts
and everything missing, is generated: `validation-tables.md`
(`py -3.11 docs/research/r3-construction-modelling/run.py`). Any dish can be
shown with `foodprep construction <dish>`.

## What was checked, for every route

1. **Reachable from raw parts with valid R1 operations.** Every material
   starts from a part in `part_properties.yaml` (or a fraction of another
   material) and every step is applied by `operations.apply` after
   `operations.assess`. Nothing is assumed: an inapplicable step is a failure,
   an unstated property is an unknown. Documented alternatives (`or`) are
   assessed too.
2. **Recombination and structure recorded.** Each join is one of six assembly
   operations with roles; each role's requirements are checked on the member
   (a container is hollow, a coagulant sets on heat, a dry phase takes up
   water). Recombination links are derived, not labelled. Every fraction a
   step makes is used, discarded in the data, or marked `usually_discarded` by
   the model (peels); anything else is "unaccounted".
3. **The final state is consistent with documented practice.** Each route's
   `final` state (cooked, crisp, browned, hollow, filled ...) is checked on the
   computed result, and each `expects` claim (cooled before shaping, not
   mashed, still raw, dewatered) on the computed state at that point.
4. **Every relationship cites R2 recipe ids.** Every route, material and
   assembly carries recipe ids; every id cited in a route is in that route's
   list; every id exists in R2's `recipes.md` with a URL (in `recipes.md` or
   `sources.md`). `tests/test_constructions.py` checks all of this.

## Results

- **27 dishes, 43 routes.** 13 dishes fully represented, 14 partly, 0 not.
  By route: 26 fully, 17 partly, 0 not.
- **No step was inapplicable or unknown on a main path.** All 236 main-path
  steps are applicable. The two failures are a documented alternative (E12b's
  braise) and a container role (gemista's tomato), both below.
- **66 claims checked** (`expects` and `final`), all consistent with the
  computed states.
- **9 recombination links derived** from the data: settled starch (latkes,
  gamja-jeon), salt-drawn juice as the batter liquid (onion pakoda, shredded
  hobak-jeon), scooped flesh into the filling (both zucchine ripiene routes,
  both gemista routes), inner leaves into the filling (kaalikääryleet E12a).
- **Every pattern and every water route appears.** C1-C9 each have three or
  more dishes; all nine water routes W1-W9 are recorded; every join operation
  is used.

| Pattern | Dish | Verdict | What is missing (short) |
| --- | --- | --- | --- |
| C1 | latkes | fully | |
| C1 | gamja-jeon (own starch, bought starch) | fully | |
| C1 / C2 | rösti (raw, boiled) | partly | E1c seals loose cooked strands in fat before pressing: refused by one cooking per sequence |
| C2 | aloo tikki | fully | |
| C2 + C7 + C9 | arancini, supplì | fully | |
| C2 + C9 | croquetas | partly | the béchamel is all pantry additions: its starch and setting are asserted, not derived from a part |
| C3 | falafel | fully | |
| C3 | medu vada | fully | |
| C3 | akara | fully | |
| C4 | mücver | fully | |
| C4 | carrot patties (crumbs, courgette dewatered, raw potato) | partly | E18b ties the egg amount to the final heat: amounts are not modelled |
| C4 | onion pakoda (own juice, salt late) | partly | rinsing (A1b) is not an operation |
| C5 | raggmunk | fully | |
| C5 | okonomiyaki | partly | mucilage is not a property; "cabbage last" is an order constraint the model cannot check |
| C5 | kakiage | partly | a temporary support (nori, paper) is not a container |
| C6 | tortilla de patatas | fully | |
| C6 | frittata | partly | a lid's steam is not distinguished from an open pan |
| C6 / C2 | porkkanalaatikko (porridge, raw-carrot custard, purée custard) | fully | |
| C7 | zucchine ripiene (cooked flesh, blanched flesh) | fully | |
| C7 | kaalikääryleet (inner leaves, trimmed rib) | partly | braising the parcels (E12b alternative): `braiser` requires a fibrous vegetable |
| C7 | gemista (oven raw rice, pot) | partly | the tomato vessel fails (flesh without skin); rice cooking inside is not computed; one container per assembly |
| C8 | gratin dauphinois (raw, simmered) | partly | the binding phase thickening is recorded, not computed |
| C8 | parmigiana (floured, egg in sauce) | partly | binding phase; salting "removes bitterness" (M9a) is not in `degorger` |
| C6 / C8 | kaalilaatikko (egg-milk, broth, reduced cream) | partly | the cream reducing around the pieces is not computed |
| C9 | tempura | partly | surface water and batter temperature are not properties |
| C2 + C9 | korokke | fully | |
| C9 / C4 | hobak-jeon (sliced, shredded) | partly | surface water (W9) is not a property |

## What "partly" means here

No dish is partly because the model could not describe its materials. The
partial verdicts come from five kinds of missing understanding, which
`evaluation.md` turns into requirements for R4:

1. **What happens inside an assembly during the final heat is not
   computed.** The assembled whole takes its carrier's state (the shell, the
   wrapper, the first layer). So a thickening binding phase (gratin,
   parmigiana, kaalilaatikko E14b) and raw rice cooking in a vessel (gemista)
   are recorded claims, not checked ones. This is the largest gap: all C8
   dishes and one C7 dish.
2. **Surface water, temperature, time and order** are not properties:
   patting dry (W9), ice-cold batter, "cabbage last", a lid, the egg amount
   for oven or pan. They are kept as cited evidence.
3. **Two operations are missing:** rinsing (A1b, and the Zürich rösti of
   E1d) and a second heating of a cooked material before assembly (E1c).
4. **Decomposition mismatches containers.** The tomato is decomposed into
   flesh and skin; a tomato vessel is both, so `tomato.flesh` alone fails the
   container check. A dish of several vessels with one filling needs several
   assemblies.
5. **R1 requirements written for single vegetables** do not fit parcels:
   braising cabbage rolls fails `braiser`'s "fibrous enough" requirement.

## Traceability

- 27 dishes and 43 routes cite 59 distinct R2 recipe ids (`recipes` fields),
  and the new operations' `documented_in` cites the recipes they come from.
- Every id resolves to a recipe in R2's `recipes.md` and to a URL that was
  read. M2c is on the page of M1a, as its heading says.
- No design dish cites a held-out recipe id, and no operation written before
  the freeze does.
- Quantities and conditions appear only in `evidence` strings on the step or
  relation they support (for example "135-140 C about 15 min to dehydrate
  (M12c)" on the tortilla's oil step). There is no quantity field.

## After the post-freeze validator amendment A1 (PR #7 review, 2026-11-24)

*Added after R3; the results above are the original R3 record and are not
changed.*

Review of PR #7 found two faults in the validator by static inspection, and
both were reproduced with tests that failed on the frozen code:
- **Recombination** was counted whenever a fraction reached the result,
  because reachability follows a fraction back to its source, so extraction
  alone would have counted. It now needs two materials of the same origin,
  each entering the dish by its own route.
- **Edibility at joins**: an assembly took only its carrier's edibility. A
  join is now not food if any member is not food, with R1's reason (unsafe or
  inapplicable).

The design set rerun on the corrected validator
(`validation-tables-a1.md`, compared route by route with the original
`validation-tables.md`):

| | Original R3 | After A1 |
| --- | --- | --- |
| dishes fully / partly / not | 13 / 14 / 0 | 13 / 14 / 0 |
| routes fully / partly / not | 26 / 17 / 0 | 26 / 17 / 0 |
| recombination links | 9 | 9 |
| dishes whose verdict changed | | none |
| dishes that gained or lost a recombination link | | none |

Per dish: no change for any of the 27. All 9 links already joined two
materials entering the dish by their own routes (for example the potato pulp
and its settled starch in latkes), and no design dish has a non-food member.
The amendment record is
`src/foodprep/data/construction_freeze_amendments.yaml`.
