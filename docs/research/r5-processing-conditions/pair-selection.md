# R5 pair selection

Written on 2026-11-25, **before any R5 source was read**. The list comes
from the steps the documented dishes (R3, `constructions.yaml`) and the five
worth-cooking transfers (R4, `transfers.yaml`, `kitchen-tests.md`) actually
use. A script walked every route and every derived transfer route and listed
each (starting part, operation) with the step's existing `evidence` string;
the candidates below are the ones where that string, or R4's "one thing to
get right", is a processing condition (a time, a temperature, an endpoint,
"don't overdo it").

A **pair** is (ingredient part or assembly, operation). It is attached to
one or more **steps**, addressed as `dish/route/owner/step` (R3) or
`transfer:<id>/owner/step` (R4), where `owner` is the material or assembly
and `step` the 1-based step number. The same pair can carry different
endpoints in different steps; that is recorded per step, not averaged.

Selection rules, fixed before reading:

1. Every R4 "one thing to get right" that is a condition gets a pair
   (blanch rutabaga; don't overboil onion; bake napa covered with liquid;
   soak but don't cook peas, grind coarse).
2. Every kitchen test in `r4-transfers/kitchen-tests.md` must be runnable
   with a completion and a failure check, so its base-dish steps get a pair
   too (cabbage head, courgette vessel, chickpea falafel, carrot patties).
3. Among R3-only steps, take the ones whose existing evidence string already
   names a failure that is about doing (overcooked, over-soaked, cold oil,
   watery), and which add a kind of step not covered yet: steaming, cooling
   a cooked starch, salting a grated vegetable.
4. Skip pure cuts (`emincer`, `raper` as geometry), whose condition is a
   size, already in the step's evidence; slice thickness is recorded as a
   factor on the cooking pair it changes. Skip meat, dough and egg-custard
   steps (outside the vegetable scope or R3 held-out failures that are
   about assertion, not condition), except where rule 3 applies.
5. No simmered dried peas: no R3 route or R4 transfer simmers them. The pea
   soup endpoint ("cooked until they crush") is recorded only as the
   contrasting role on the soaking pair, if a source states it.

| # | Pair id | Part / owner | Operation | Steps (where used) | Why chosen |
| --- | --- | --- | --- | --- | --- |
| 1 | `soak_dried_peas` | dried_peas.dried_seed | tremper | `transfer:pea_falafel/pea/1` | R4: soak, never cook; P15 found soak time drives water uptake; Finnish staple, Finnish packet text may exist |
| 2 | `soak_chickpeas` | chickpea.dried_seed | tremper | `falafel/raw_soaked/chickpea/1` | Base of the pea-falafel kitchen test; R2 sources disagree (overnight, 24 h, 12 h warm) |
| 3 | `soak_urad_dal` | urad_dal.dried_seed | tremper | `medu_vada/beaten_paste/dal/1` | A3a gives an *upper* limit (not over 4 h) against A3b overnight: a documented conflict with a failure |
| 4 | `soak_black_eyed_beans` | black_eyed_bean.dried_seed | tremper | `akara/aerated_paste/beans/1`, `moi_moi/steamed/beans/1` | Short soak for skinning (15 min to 1.5 h); "hot water part-cooks them" is a failure condition |
| 5 | `grind_soaked_peas` | dried_peas.dried_seed (soaked) | broyer / mixer | `transfer:pea_falafel/pea/2` | R4: grind coarse; fine grind makes them dense (P4) |
| 6 | `grind_soaked_chickpeas` | chickpea.dried_seed (soaked) | mixer | `falafel/raw_soaked/chickpea/2` | Base of 5; R2 has fine against bulgur-like |
| 7 | `rest_pulse_paste` | falafel paste | reposer | `falafel/raw_soaked/paste/1`, `transfer:pea_falafel/paste/1` | Make-ahead point (1 h to overnight against none); an intermediate state for batch preparation |
| 8 | `fry_pulse_paste` | falafel paste | frire | `falafel/raw_soaked/paste/3`, `transfer:pea_falafel/paste/3` | Deep-frying a paste; "falls apart", "dry and hard" are R4 failures |
| 9 | `steam_bean_paste` | moi moi paste | cuire_vapeur | `moi_moi/steamed/paste/1` | The only steaming of a vegetable paste in R3; endpoint "firm with no wet residue" |
| 10 | `blanch_rutabaga` | rutabaga.root (sliced) | blanchir | `transfer:rutabaga_gratin/rutabaga/3` | R4: 3-5 min or it stays crunchy |
| 11 | `bake_gratin` | gratin (layered) | cuire_four | `gratin_dauphinois/raw_long_bake/gratin/1`, `transfer:rutabaga_gratin/gratin/1`, `transfer:rutabaga_gratin_raw/gratin/1` | R4: covered then uncovered; the 90-min covered bake for raw rutabaga (G7, G8) is a time condition A2 cannot express |
| 12 | `simmer_potato_in_milk` | potato.tuber (sliced) | mijoter | `gratin_dauphinois/simmered_then_baked/potato/3` | The other gratin route; "until tender" in about 8 min; the gratin's alternative to a long bake |
| 13 | `rest_gratin` | gratin (baked) | refroidir / rest | `gratin_dauphinois/simmered_then_baked/gratin/2`, `transfer:rutabaga_gratin` (rest 25 min, G7) | Cutting cleanly; overnight chill is a make-ahead point |
| 14 | `blanch_onion_vessel` | onion.bulb (peeled, whole or halved) | blanchir | `transfer:onion_vessel/vessel/2`, `farcis_nicois/meat_baked/onion/2` | R4: don't overboil or the layers slip |
| 15 | `blanch_courgette_vessel` | courgette.fruit (whole) | blanchir | `zucchine_ripiene/cooked_flesh/courgette/1`, `zucchine_ripiene/blanched_flesh/courgette/1`, `farcis_nicois/meat_baked/courgette/1` | The comparison vessel in the onion test; "drained while still firm" |
| 16 | `bake_stuffed_vegetables` | stuffed vessel | cuire_four | `transfer:onion_vessel/stuffed/1`, `farcis_nicois/*/stuffed/1`, `zucchine_ripiene/*/stuffed/1` | The onion test's bake; "is the onion tender at 30 min" |
| 17 | `blanch_cabbage_head` | cabbage.head (cored, whole) | blanchir | `kaalikaaryleet/inner_leaves/cabbage/1`, `kaalikaaryleet/trimmed_rib/cabbage/1` | Base of the napa test; Finnish dish, Finnish sources |
| 18 | `blanch_napa_leaves` | napa_cabbage.head (leaves) | blanchir | `transfer:napa_cabbage_rolls/napa/2` | R4: 1-2 min or microwave; going mushy is the failure |
| 19 | `bake_cabbage_rolls` | rolls | cuire_four | `kaalikaaryleet/*/rolls/1`, `transfer:napa_cabbage_rolls/rolls/1` | R4: bake covered with liquid; edges dry or scorch |
| 20 | `cook_rice_for_filling` | rice.grain | cuire_anglaise | `kaalikaaryleet/*/rice/1`, `transfer:napa_cabbage_rolls/rice/1`, `arancini/arancini/rice/1` | A packet-instruction step (Lidl rice); "can be done the day before" is a make-ahead point with a food-safety question (cooked rice) |
| 21 | `salt_grated_courgette` | courgette.fruit (grated) | degorger / presser | `kolokythokeftedes/baked/courgette/2-3`, `mucver/squeezed/courgette/2`, `carrot_patties/courgette_dewatered/courgette/3` | Salting and draining grated vegetables; "water comes out" is an observable endpoint; watery mass is the failure |
| 22 | `peel_broccoli_stem` | broccoli.stems | eplucher (then raper) | `transfer:broccoli_stem_patties/stem/1-2` | R4: peel the stem; "stringy" is the failure |
| 23 | `cook_vegetable_patty` | grated-vegetable patty | rissoler / cuire_four | `carrot_patties/crumbs/patty/1`, `transfer:broccoli_stem_patties/patty/1`, `kolokythokeftedes/pan_fried/mass/3`, `mucver/squeezed/mass/3` | Pan-frying and oven-baking a patty; "do not turn until firm", "cold oil makes them break" |
| 24 | `boil_potato_for_rosti` | potato.tuber (whole, in skin) | cuire_anglaise | `rosti/boiled/potato/1`, `korokke/breaded_mash/potato/1`, `aloo_tikki/cornflour/potato/1` | Parboiled or fully cooked is a known disagreement; waterlogged potato does not hold (A2a) |
| 25 | `chill_cooked_potato` | potato.tuber (boiled) | refroidir | `rosti/boiled/potato/2`, `aloo_tikki/cornflour/potato/2` | Cooling a cooked starch; overnight to two days "entscheidend" (E1c); the clearest "prepare for tomorrow" step |

Twenty-five pairs, at the top of the brief's range. If the evidence for a
pair cannot be found, the pair stays in the data with its fields `unknown`;
it is not dropped, so the gap is visible.

Not selected, and why: kale blanching (kale rolls are not worth cooking);
the vareniki boil (dough, R3 asserts its state); chawanmushi (egg custard);
croquetas (béchamel); tempura and kakiage frying (batter, not in an R4
test); latkes and draniki frying (covered by pair 23's failure kinds, can be
added later); rice for porkkanalaatikko (porridge, the same part as 20 in a
different role, kept out to stay within 25).

## Scope change (2026-11-25, from the user, after the pairs above were fixed)

The user changed the unit of R5 from the pair to the **complete processing
sequence**: each component's chain from raw part to plate, including what it
goes through after it is joined. In the user's words, the 3-5 min blanch "isn't
intended to make the rutabaga edible. It's intended to make it ready for the
next operation", and a record that misses the bake is "half a cooking process".
Four requirements:

1. A condition belongs to a step within the whole route. The pairs above stay,
   as defaults that hang off route steps.
2. Every step's endpoint says whether it is **readiness** (ready for the next
   operation) or **doneness** (ready to eat), with the source that says so.
3. Every member of an assembly gets its own endpoint for the heat after the
   join (the gratin's layers, a roll's leaf and filling, a vessel and its
   filling, a patty's parts). This is R3's gap (an assembly takes its carrier's
   state), recorded as data; nothing is computed and `constructions.py` is not
   touched.
4. Documented dependencies between stages (this stage exists because of that
   later one), and documented failures when a stage is skipped or overdone.
   Sources that split the work differently are **alternative sequences**, kept
   apart.

### Sequences selected

Chosen by the same rules as the pairs: every R4 worth-cooking transfer, whole,
and the base route its kitchen test compares it with, whole.

| Sequence | Steps | Why |
| --- | --- | --- |
| `transfer:rutabaga_gratin` | 6 | R4 worth cooking; the user's example |
| `gratin_dauphinois/raw_long_bake` | 3 | its kitchen-test base; `gratin_dauphinois/simmered_then_baked` and `transfer:rutabaga_gratin_raw` are recorded as alternative sequences |
| `transfer:onion_vessel` | 7 | R4 worth cooking |
| `zucchine_ripiene/blanched_flesh` | 5 | the courgette vessel in the onion test |
| `transfer:napa_cabbage_rolls` | 6 | R4 worth cooking |
| `kaalikaaryleet/trimmed_rib` | 5 | its kitchen-test base, Finnish |
| `transfer:pea_falafel` | 7 | R4 worth cooking |
| `falafel/raw_soaked` | 7 | its kitchen-test base |
| `transfer:broccoli_stem_patties` | 5 | R4 worth cooking |
| `carrot_patties/crumbs` | 3 | its kitchen-test base |

Ten sequences, 54 route steps. Pairs 3, 4, 9, 21, 24 and 25 (urad dal,
black-eyed beans, moi moi, salted courgette, rösti potato) belong to R3 routes
outside these sequences; they stay attached to their steps as pair data, and
their routes are not claimed to be documented end to end.
