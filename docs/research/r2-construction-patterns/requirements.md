# R2 step 4: physical requirements

What each component of each pattern must be, written in the vocabulary of
`src/foodprep/data/part_properties.yaml` (properties of a part) and
`operations.yaml` (R1 operation requirements and output states), so that it
can later be checked against the model. Every requirement points to recipes
that show it. **Exists** = the model already has the term. **Partial** = a
term exists but does not say what the evidence needs. **Missing** = no term.

Property values use the model's scale: none < low < medium < high <
very_high. Thresholds below (">= high") are readings of the recipes, not
measurements. They are first guesses to be tested, not facts.

## Per pattern

### C1. Released-starch cake

| Component | Requirement | Model term | Status | Evidence |
| --- | --- | --- | --- | --- |
| main material | starch >= high, **raw** (not cooked) | `starch`; state `cooked: false` | partial: `starch` exists, but potato has no parts in `part_properties.yaml` yet | E1b, E4-E7, A10 |
| | cut fine enough to break cells: grated, shredded, blended | `raper` → piece fine, shape shreds; `mixer` → smooth | exists | all |
| | firmness >= medium (to grate) | `firmness`; `raper` requires >= medium | exists | |
| expressed liquid | separates into water (discarded) and settled starch (returned) | `presser` gives juice + pulp; `decanter` (let settle) exists but has **no outputs** | missing output: settled starch fraction | E2b, E3a, E4, E5, E10, A10a |
| assembly | water lowered by squeezing, **starch kept** | `presser` lowers water | partial: no way to say "the starch stays" | E7a "do not rinse" |
| final heat | pan with hot fat; crust before turning | `frire` (deep-fry); `sauter`, `rissoler` | partial: "crust as structure" and "pan-fry a formed cake" are not distinct from frying pieces | E7a, E19a, E4a |

### C2. Cooked-starch mass

| Component | Requirement | Model term | Status | Evidence |
| --- | --- | --- | --- | --- |
| main material | starch >= medium (potato, rice, bread, roux) | `starch` | partial: potato, rice and bread have no parts in `part_properties.yaml` | A2, A6, M11, M13, E11 |
| | cooked (gelatinised) | state `cooked: true` (`cuire_anglaise`, `cuire_vapeur`) | exists | |
| | **cooled / rested before shaping** | none | missing state (`cooled` or `set`) | convergence 9 |
| | not waterlogged: cooked in the skin, drained at once, steam released | `water` | partial: no notion of "cooked without taking up water" | A6a, A2a |
| | mashed, riced or grated | `ecraser` (mash) → piece fine | exists | E16a, M14 |
| C2b raw part | raw starch + cooked starch, or raw starch + boiling liquid | none | missing: combining two states of one ingredient; scalding | E8-E10, A16 |
| second cooking | the formed mass is fried, baked or boiled again | `frire`, `cuire_four` require `cooked: false` ("one primary cooking per sequence") | **conflict**: the rule blocks every C2 dish (boiled rösti, korokke, croquetas) | all C2 |

### C3. Raw pulse paste

| Component | Requirement | Model term | Status | Evidence |
| --- | --- | --- | --- | --- |
| pulse | dried, **soaked, not cooked** | no soak operation; `white_beans` is an ingredient without parts | missing: `tremper` (soak/rehydrate) and a `soaked` state | M1, M2, A3, A18, A19 |
| | skinned (fava, black-eyed peas) | `ecosser`, `monder` exist for pods and peels | partial | A18, A19 |
| paste | ground with little water, fine enough to hold | `broyer` / `mixer` → piece fine, smooth | exists; "little water" is not expressible | M1c, A3a |
| | optionally aerated | `foisonner`, `fouetter` exist with **no outputs** | missing state `aerated` | A3a, A18a, M1c |
| | a coagulating protein + starch (what sets it) | no protein property in use | missing | |
| final heat | deep-fry, or steam in a mould | `frire`, `cuire_vapeur` | exists | |

### C4. Bound watery vegetable

| Component | Requirement | Model term | Status | Evidence |
| --- | --- | --- | --- | --- |
| main material | water >= high, starch <= low (courgette, spinach, aubergine) | `water`, `starch` | exists (courgette fruit: water very_high, starch none) | M3, M4, M18a, E19 |
| | grated, shredded or chopped | `raper`, `hacher` | exists | |
| water step | salt and drain | `degorger` (requires water >= high, piece <= medium; lowers water by 1; outputs `vegetable_water`) | exists | E19b, M4a, M18a, A11 |
| | squeeze | `presser` | exists, but its pulp output is flagged `binder: true` (see below) | M3, A17a |
| | or keep the water as batter liquid (C4b) | `degorger` marks `vegetable_water` `usually_discarded` | partial: the fraction exists, but no use of it as a batter liquid | A1a, A9b |
| dry phase | absorbs the remaining water: flour, crumbs, soaked bread, cheese, raw grated potato | R1 `thickener` function (piece fine/powder, starch or fibre) is close | missing: a property for **water uptake** by a dry addition | M4a stated; A11b, A13b, A2a |
| egg | coagulating, amount tied to the final step | `eggs` is an ingredient without parts | missing | E18b |
| rest | the dry phase hydrates before shaping | none | missing (`rested`/time) | M3b, E18c, E19a |
| final heat | pan or oven; a drier mass for the oven | `frire` requires water <= medium (or coated, or thin) | exists, and **agrees with the evidence**: courgette has to lose water before it can fry | M4a, M14c, E18b |

### C5. Batter matrix

| Component | Requirement | Model term | Status | Evidence |
| --- | --- | --- | --- | --- |
| batter | flour + liquid (+ egg), mixed little, cold | `enrober` (coat with batter) sets `coated` on a piece | partial: no batter that *contains* pieces | E6, A7, A5, M18b |
| inclusion | any firmness; wet vegetables added last | — | missing ordering | A7a |
| binder from the material | grated yam (nagaimo) thickens the batter | R1 lists **mucilage** as a missing property | missing (confirmed) | A7a-c |

### C6. Egg-set matrix

| Component | Requirement | Model term | Status | Evidence |
| --- | --- | --- | --- | --- |
| pieces | cooked, water lowered (oil-poached, sautéed) | `confire`, `sauter`, `suer` lower water | exists | M12c, M20a |
| | cooled before the egg (in bakes) | none | missing `cooled` | E17c, E10c |
| egg phase | egg (or egg + dairy/dashi up to ~1:3) | none | missing | A8, M12 |
| | can be replaced by a starch phase (porridge, reduced cream) | — | | E17a, E14b |
| final heat | gentle: pan + flip or lid, steam, oven | `cuire_four`, `cuire_vapeur` | partial (conflict with "one primary cooking" again) | |

### C7. Container and filling

| Component | Requirement | Model term | Status | Evidence |
| --- | --- | --- | --- | --- |
| vessel (C7a) | hollowable: soft centre, firm wall | `seed_core`; `evider` requires `has_seed_core`, firmness >= medium; outputs `hollow` shell + `core` fraction | exists | M7, M16, M17, A14 |
| | or openable without hollowing (split belly, hinged slices) | `inciser` (score) | partial | M5, A12 |
| | holds its shape through cooking | `holds_shape_cooked` | exists | |
| | softened first by heat (fried, baked, blanched) when its wall is thick | `blanchir`, `frire`, `rotir`, then baked again | conflict with "one primary cooking" | M5, M16a, M17 |
| scooped flesh | **goes back into the filling** | `evider` outputs a `core` fraction, but nothing links a fraction back into a construction | missing link | M7, M16, M17; RecipeNLG 38% |
| leaf wrapper (C7b) | leafy, piece large/whole, `flexible: true` after softening | `leafy`, `piece`, `flexible`; `blanchir` sets `flexible: true`; R1 `wrapper` function | exists (cabbage leaves have no part properties yet) | E12, E13, M6 |
| | freezing as an alternative softener | `congeler` exists with **no outputs** | missing output | RecipeNLG 2% |
| | thick rib trimmed | `parer` (trim) | exists | E12b, E13a |
| dough wrapper (C7c) | thin, sealable, survives boiling or frying | none (doughs are not modelled) | missing | E15, E16, A11, A13 |
| filling | low free water, cooled, or pre-cooked "until its liquid evaporates" | `water`, `cooked` | partial (no `cooled`) | A11a, E16, M5a |
| | raw rice that cooks inside needs liquid and headroom | none | missing | M6, M7a |
| assembly | fill, roll, fold, seal, pack, weigh down | none | missing operations | E13a, M6 |

### C8. Layered assembly

| Component | Requirement | Model term | Status | Evidence |
| --- | --- | --- | --- | --- |
| layer pieces | water lowered (salt-drain, fry) | `degorger`, `frire` | exists | M9 |
| binding phase | a liquid that thickens around them: starch from the potato itself (slices not rinsed), reduced sauce, cheese, egg | `lier` (thicken a liquid) | partial: the starch comes from another layer | M15b, M9b |
| assembly | layer, bake, **chill before cutting** | none | missing `layer`, `cooled` | M15b |

### C9. Coated piece

| Component | Requirement | Model term | Status | Evidence |
| --- | --- | --- | --- | --- |
| piece | surface dry (pat dry, flour dust) | `paner` (flour-egg-crumb), `enrober` (batter) set `coated` | exists | A4a, A9a, A14 |
| | inside not wet enough to steam through the coat | `water` | exists | A6a |
| coat | dry → wet → (dry) order; egg foam (A14) | `paner` is one step | partial: order and the foam are not expressed | A14, M13b |
| final heat | hot oil; double fry if the inside is wet | `frire` requires `cooked: false` | conflict for the second fry | A12b, A13 |

## Missing terms, collected

Ordered by how many patterns need them.

| Missing term | Kind | Patterns | Evidence |
| --- | --- | --- | --- |
| **construction itself**: a component made from other components | concept | all | everything in `patterns.md` |
| relax "one primary cooking per sequence" for an assembled component | rule | C2, C6, C7a, C8, C9 | boiled rösti, karnıyarık, parmigiana, double frying |
| `cooled` / `set` state (rested after cooking) | state | C2, C4, C6, C7, C8 | convergence 9 |
| **water uptake** of a dry addition (flour, crumbs, bread, rice, poha) | property | C4, C5, C7 | M4a, A11b, A13b, A2a |
| settled-starch fraction (`decanter` outputs) | operation output | C1, C2b | convergence 1 |
| soak / rehydrate operation (`tremper`) and a `soaked` state | operation | C3, C2 (bread), C7 (leaves, husks) | M1, A3, A18, E11, M6, A15 |
| coagulating protein (egg, raw pulse) as a property | property | C3, C4, C6, C9 | |
| starch **state**: raw-releasable vs gelatinised (whether starch level alone is enough is untested) | property or state | C1, C2 | E7a vs E1a |
| `aerated` (outputs for `foisonner`, `fouetter`) | state | C3, C5, C6 | convergence 13 |
| mucilage (already missing in R1) | property | C5 | nagaimo in okonomiyaki, A7 |
| assembly operations: fill, roll, wrap, fold, seal, layer, pack, coat-in-sequence | operations | C7, C8, C9 | |
| reuse of a fraction inside the same construction (scooped flesh, inner leaves, settled starch, salt-drawn juice) | link | C1, C4b, C7 | M7, E12a, E5, A9b |
| ordering constraints (salt late, wet last, cool before egg) | rule | C1, C4, C5, C6 | section 3 of `mechanisms.md` |
| outputs for `egoutter`, `congeler`, `malaxer`, `abaisser` | operation outputs | C7, C4 | |
| part properties for potato, cabbage, onion, eggs, rice, bread, pulses | data | all | these are ingredients in `tomato.yaml` but have no parts in `part_properties.yaml` |

## Where the current model disagrees with the evidence

- **`presser` marks the pressed pulp `binder: true`** for any material. The
  evidence says the opposite for starch-poor vegetables. Squeezed courgette is
  the thing that needs binding, not a binder (C4: every recipe adds egg and
  flour). Squeezed raw potato binds because of its starch, and only if the
  starch is kept (C1). A binder flag should depend on the material (starch,
  protein), not on the operation.
- **R1's structure functions** (`binder`, `wrapper`, `edible_vessel`,
  `moisture_carrier`, `thickener`) were predefined roles. Measured against the
  recipes:
  - `edible_vessel` (hollow) and `wrapper` (flat, flexible, leafy) match C7a
    and C7b.
  - `thickener` is close to the water-uptake role in C4.
  - `binder` as a property of one component is too simple. In C1-C3 the main
    material binds itself after a transformation. In C4 the binding is a
    combination (egg + flour + the water left).
  - Containment (C7) needs no binder at all.
- **Courgette `holds_shape_cooked: false`.** Courgette is the most common
  vessel in the evidence: blanched 5-10 min, hollowed, filled and baked
  25-30 min, and it still stands (M16a, M17a-b; RecipeNLG stuffed courgette).
  The flag probably describes small cut pieces going soft. A whole or halved
  shell behaves differently, so the property depends on piece size.
- **`evider` requires `has_seed_core`**, and the courgette's seed core is
  marked "only large courgettes". The recipes hollow ordinary courgettes and
  aubergines by scooping out flesh, not only seeds (M17, M7b). Hollowing a
  vessel is a different operation from removing a seed core.
- **`frire` requires water <= medium unless coated or thin.** This agrees
  with the evidence: every fried courgette mass removes or absorbs water
  first. It is the one R1 rule that already encodes a construction
  requirement.
