# R2 step 5: transferable applications (INFERENCE)

> **This file is inference, not evidence.** Steps 1-4 (`recipes.md`,
> `mechanisms.md`, `patterns.md`, `requirements.md`) report what recipes do.
> This file asks which vegetables could meet a pattern's requirements. Each
> row says whether this round found a recipe that already does it
> ("documented", with ids) or whether it is reasoning only ("inference").
> Under the user's first filter ("has anybody actually eaten this before?"),
> an inference row is a question for the next search, not a suggestion to cook.

**Ingredient scope.** Candidates are the vegetables in the project's
catalogue (`tomato.yaml`). Its README calls it "what the local Lidl actually
sells", and its availability classes approximate a Finnish Lidl-style shop.
The vegetables are potato, carrot, onion, garlic, cabbage, courgette,
broccoli, cucumber, tomato, rutabaga, kale, greens, corn, avocado and apple.
Pantry items the patterns need are partly in the catalogue (eggs, rice,
bread, rye crumbs, white beans, cream, cheeses) and partly not. **Wheat flour,
rye flour, potato starch, oat flakes and dried pulses are not in the
catalogue.** Their regular Lidl Finland availability was assumed and **not
checked** this round. Bell pepper and aubergine, the most common Mediterranean
vessels, are not in the catalogue either.

**Equipment.** Every pattern uses only R1's `ordinary_equipment` (knife,
grater, pot, pan, oven, sieve, bowl, colander, baking tray, whisk, towel,
cloth, blender, spoon, fork). One caveat: C3 pastes are made in a food
processor or meat grinder (M2b, M1b). A blender needs added water to turn,
and that works against "grind with little water" (A3a, A18a). Inference: C3
in a home blender is a practical risk; A10b and A3a do use a blender or mixie
successfully for other pastes.

## By pattern

### C1. Released-starch cake (needs raw starch >= high)

| Candidate | Fit | Status |
| --- | --- | --- |
| potato | the only catalogue vegetable with releasable raw starch | documented: E1-E7, A10 |
| potato as the starch carrier for a starch-poor vegetable (carrot, courgette, rutabaga grated in) | the potato's starch binds the mix | documented: E18d porkkanapihvit (raw grated potato in carrot patties); a RecipeNLG hand-check sentence squeezes courgette, potato and carrot together |
| rutabaga, carrot alone | starch low: will not bind by C1; they belong to C4 | inference |

### C2. Cooked-starch mass (needs starch >= medium, cooked, cooled)

| Candidate | Fit | Status |
| --- | --- | --- |
| potato (boiled in skin, cooled) | yes | documented: E1a, A2, A6, M14 |
| rice (porridge or cooked, cooled) | yes | documented: E15, E17a, M11 |
| bread, rye crumbs (soaked) | yes | documented: E11 |
| rutabaga, cooked and mashed | starch low, mash is wet: needs drying (`dessecher`) or a starch partner | documented as a starch-partnered bake: E17a "lanttu- ja porkkanalaatikko" (rutabaga + carrot with rice porridge); as a formed cake: inference |
| leftover cooked vegetables bound by mashed potato | potato supplies the starch | documented pattern (M14 potato + fish; RecipeNLG 15% of potato cakes start from leftover mash); with vegetables: inference |

### C3. Raw pulse paste (needs dried pulses, soaked, not cooked)

| Candidate | Fit | Status |
| --- | --- | --- |
| canned white beans (in the catalogue) | **no**: cooked pulses do not make a C3 paste; they become a binder-held mash (C4-like) | evidence: every native falafel recipe uses raw pulses; the cooked American version adds flour/crumbs/egg |
| dried chickpeas, dried fava | yes, if available | documented: M1, M2. Availability not checked |
| dried yellow or green split peas (Finnish pea-soup staple) | probably: a soaked raw pulse | **inference**, not searched. One weak hint: a reader comment on A18a reports akara made from red lentils. Next search: split-pea, chana-dal or lentil vadas and fritters in Hindi, Gujarati or Bengali sources |

### C4. Bound watery vegetable (water >= high, starch low; water removed or used; dry phase + usually egg)

| Candidate | Fit | Status |
| --- | --- | --- |
| courgette | yes: the reference case | documented: M3, M4, M18a, E19, A17 |
| carrot | water high, firm: not squeezed in any recipe read | documented: E18a-d |
| onion, own-juice batter (C4b) | yes | documented with gram flour: A1a. With wheat flour (gram flour not in the catalogue): **inference**, but A9b does the same with plain flour and courgette |
| spinach / greens | salt-rub and squeeze, as a filling | documented: M8a |
| kale | tough leaf: blanch or massage, then chop and squeeze | inference by analogy with M8a; not searched |
| cabbage, shredded | releases water on salting | documented as a dumpling filling only by analogy (A11 is courgette); cabbage in batter is C5 (A7) |
| broccoli stems, grated (R1 zero-waste part) | firm, water medium, starch low: like carrot, probably no squeezing | **inference**; RecipeNLG has broccoli fritters by title (not separated from florets); not searched in other languages |
| rutabaga, grated raw | very firm, starch low: like carrot | inference; not searched |
| cucumber | water very high, eaten raw: squeezing leaves little | inference: poor fit; no fritter found |
| apple (with grated potato or in batter) | | not in scope of this round's evidence |

### C5. Batter matrix

| Candidate | Fit | Status |
| --- | --- | --- |
| cabbage | yes; wet cabbage added last | documented: A7a-c (needs grated yam; its mucilage has no catalogue equivalent; egg-only batters exist, A7b-c add egg) |
| potato strands | yes | documented: E6 raggmunk |
| corn kernels | yes | documented: RecipeNLG corn fritters (856 recipes) |
| carrot strips, onion | yes | documented: A5 kakiage |
| courgette | yes | documented: M18b |

### C6. Egg-set matrix

| Candidate | Fit | Status |
| --- | --- | --- |
| potato (oil-poached) | yes | documented: M12 |
| courgette (sautéed) | yes | documented: M20 |
| carrot, rutabaga (cooked, puréed or grated, with rice) | yes; egg optional | documented: E17a-c |
| cabbage (with grain) | yes; egg optional | documented: E14a |
| broccoli | yes | documented: RecipeNLG quiche and casseroles (broccoli quiche among titles) |

### C7. Container and filling

| Candidate | Fit | Status |
| --- | --- | --- |
| courgette as a vessel | yes (blanch, hollow, refill with its own flesh) | documented: M16, M17 |
| tomato as a vessel | yes, raw; pulp is the rice's liquid | documented: M7a, M16b |
| onion as a vessel | yes, boiled and hollowed | documented: M16a, M17b |
| avocado half | the stone cavity is already a vessel | documented as a serving cup (S2 hand check); as a baked filled vessel: not searched |
| potato or rutabaga, hollowed after cooking | firm, holds shape | inference for rutabaga; not searched |
| cabbage leaves as a wrapper | yes | documented: E12, E13 |
| kale leaves, large broccoli leaves as a wrapper | leafy, large, flexible after blanching: they match R1's `wrapper` function | **inference only**. R1 already records broccoli leaves as `flexible: true`, `piece: large`. Next search: Portuguese/Brazilian *couve* leaves and Turkish *karalahana sarması* (collard-type rolls) as the nearest documented cases |
| inner cabbage leaves, scooped courgette flesh back into the filling | the vessel's own trimmings | documented: E12a, M7, M16, M17 |

### C8. Layered assembly

| Candidate | Fit | Status |
| --- | --- | --- |
| potato slices, not rinsed | yes: their starch thickens the dairy | documented: M15b |
| cabbage with grain | yes | documented: E14b |
| courgette slices, salted and fried, layered like parmigiana | likely | inference: the Italian *parmigiana di zucchine* exists but was not read this round |
| rutabaga slices in a gratin | starch low: needs flour in the dairy or a potato layer | inference |

### C9. Coated piece

| Candidate | Fit | Status |
| --- | --- | --- |
| courgette slices: flour, then egg | yes | documented: A9a |
| onion rings, broccoli florets, courgette sticks | yes | documented: RecipeNLG breaded vegetables (titles) |
| carrot, sweet root strips in tempura | yes | documented: A4a (vegetables generally), A5 |
| cabbage leaf pieces, kale | thin leaves crisp fast in batter | inference |

## What this suggests trying first

Ordered by evidence. These are documented elsewhere and new only to the
model:

1. **Courgette as a vessel refilled with its own flesh** (C7a + recombination;
   M16, M17). It answers the Portuguese *curgete recheada* question from R1
   directly. The collector could not find a readable Portuguese recipe page
   this round, but the Niçois and Ligurian versions show the same sequence:
   blanch, hollow, cook the flesh, bind, refill, bake.
2. **Grated courgette fritter, salt-squeeze-bind** (C4a). Variants differ only
   in the water route, so it is a good kitchen test of W1 vs W2 vs W6
   (`evaluation.md`).
3. **Potato as the binder for another grated vegetable** (C1 inside C4, E18d).
   It uses no egg or flour and only catalogue items.
4. **Settled potato starch returned** (C1, convergence 1). Comparing a latke
   made with returned starch against one made with flour is the cleanest test
   of the strongest convergence in this round.

Speculative, each needing a "has anybody eaten this?" search first: split-pea
paste fritters, kale or broccoli-leaf rolls, grated rutabaga or broccoli-stem
cakes.
