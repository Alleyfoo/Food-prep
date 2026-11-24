# R3 step 1: dish selection

Two sets, both drawn from R2's `recipes.md` (ids E, M, A; URLs in
`../r2-construction-patterns/sources.md`).

- The **design set** is what the schema was designed against.
- The **held-out set** was chosen and recorded **before** schema design
  began, and committed in the same commit as this file. Its recipe sections
  in `recipes.md` were not opened while designing. What had already been
  seen of them is listed below, so the test's cleanliness can be judged.

## How dishes were chosen

1. **Evidence quality.** Prefer dishes with two or more recipes from
   independent sites, and recipes in R2's spot check (`evaluation.md`: E2b,
   E3a, E5a, M2a, M12c, M13a, M17a, A3a, A9b, A10a, A11a, A18a re-read as raw
   page text). Avoid dishes resting on one weak or non-independent source
   (M19b, A20a).
2. **Lidl Finland availability.** The proxy is the ingredient catalogue in
   `src/foodprep/data/tomato.yaml`, which its README describes as "what the
   local Lidl actually sells". An ingredient outside that catalogue is a
   **gap**: its regular Lidl Finland availability was not checked in this
   round (as in R2). Meat and fish in fillings are outside the vegetable
   scope. They are recorded as additions, not modelled.
3. **Spread.** About three dishes per pattern, so every holding mechanism is
   represented. Prefer dishes that exercise a requirement of the brief:
   recombination, nesting, alternative routes, cooling, resting, soaking,
   water used rather than removed.

## Design set (27 dishes)

| Pattern | Dish | R2 ids | Why chosen | Main ingredients in the catalogue | Gaps |
| --- | --- | --- | --- | --- | --- |
| C1 released starch | latkes | E4a, E4b | settled starch returned (convergence 1); two Hebrew sources | potato, onion, eggs | flour or matzo meal (pantry, not catalogued) |
| C1 | gamja-jeon | A10a, A10b | starch returned with nothing else (A10a spot-checked); bought-starch alternative (A10b) | potato | potato starch (pantry) |
| C1 | rösti | E1a, E1b, E1c, E1d | **alternative routes to one dish**: raw (C1) and boiled-and-stored (C2a) | potato, butter | |
| C2 cooked starch | aloo tikki | A2a, A2b | cooked potato mass, cornflour or poha against water | potato | cornflour, poha, peas (not catalogued); A2b is diffusion |
| C2 | arancini and supplì | M11a, M11b | **nesting**: cooked rice mass (C2) around a filling (C7), coated (C9) | rice, mozzarella, tomato | ragù meat; breadcrumbs from bread |
| C2 | croquetas | M13a, M13b | roux-milk gel as the cooked starch (M13a spot-checked) | butter, eggs, bread (crumbs) | flour, milk, jamón (not catalogued) |
| C3 raw pulse paste | falafel (Levantine, Sudanese) | M2a, M2b, M2c | raw soaked chickpeas, no binder (M2a spot-checked) | onion, garlic, parsley, cilantro | dried chickpeas (not catalogued) |
| C3 | medu vada | A3a, A3b | soak time and grinding water as the control; aerated (A3a spot-checked) | | urad dal, rice flour (not catalogued) |
| C3 | akara | A18a, A18b, A18c | aerated pulse paste, egg tried and dropped (A18a spot-checked) | onion | black-eyed beans (not catalogued) |
| C4 bound watery vegetable | mücver | M3a, M3b | squeezed courgette + egg + flour; rest | courgette, eggs, dill, onion | flour |
| C4 | carrot patties (morotsbiffar, porkkanapihvit) | E18a-d | Nordic; carrot never squeezed; raw grated potato as dry phase (E18d) | carrot, potato, eggs | halloumi, flour, oats |
| C4 | onion pakoda / bhajiya | A1a, A1b | **water used, not removed** (C4b): salt-drawn onion juice is the only liquid | onion, potato (A1b) | gram flour, rice flour |
| C5 batter matrix | raggmunk | E6a, E6b | the vegetable is not dewatered; batter is the matrix | potato, eggs | flour, milk |
| C5 | okonomiyaki | A7a, A7b, A7c | cabbage in batter, wet vegetables last; grated yam as thickener | cabbage, eggs | flour, nagaimo, dashi |
| C5 | kakiage | A5a | temporary container until the batter sets | carrot, onion | flour |
| C6 egg matrix | tortilla de patatas | M12a, M12b, M12c | potatoes dehydrated in oil before the egg (M12c spot-checked) | potato, onion, eggs, olive oil | |
| C6 | frittata di zucchine | M20a | sautéed courgette set in egg | courgette, eggs, parmesan | |
| C6 | porkkanalaatikko | E17a, E17b, E17c | Finnish; **alternative routes**: egg custard (C6) or porridge only (C2a); cool before the egg | carrot, rice, eggs | milk, syrup |
| C7 container and filling | zucchine ripiene alla ligure | M17a, M17b | the brief's stuffed courgette; **recombination** of the scooped flesh (M17a spot-checked) | courgette, eggs, parmesan, bread | ricotta |
| C7 | kaalikääryleet / kåldolmar | E12a, E12b | Finnish; blanched leaf wrap; **inner leaves into the filling** | cabbage, rice, onion | minced meat; syrup |
| C7 | gemista | M7a, M7b | **raw rice cooks inside**, tomato pulp as its liquid (recombination + water used) | tomato, rice, onion, olive oil | peppers |
| C8 layered assembly | gratin dauphinois | M15a, M15b | potato's own starch thickens the cream; chill before cutting | potato, cream, garlic, butter | milk |
| C8 | parmigiana di melanzane | M9a, M9b | salt-drained, fried layers; sauce, cheese; two cookings | tomato, mozzarella, parmesan, basil, olive oil | aubergine |
| C8 | kaalilaatikko | E14a, E14b | Finnish; set by egg-milk (E14a) or by reduced cream and grain (E14b) | cabbage, rice, onion, cream | minced meat; milk; syrup |
| C9 coated piece | tempura | A4a, A4b | batter coat on raw pieces; cold batter, little mixing | carrot, onion, courgette | flour |
| C9 | korokke | A6a | **nesting**: C2 potato mass, breaded (C9); why they burst | potato, onion, eggs | flour, panko, minced meat |
| C9 | hobak-jeon | A9a, A9b | sliced and coated (C9, A9a) vs shredded with own juice (C4b, A9b spot-checked): one dish name, two constructions | courgette, eggs | flour |

Patterns with fewer than three strong candidates: none. C5 has only one
kakiage recipe (A5a); it stays because it is the only temporary-container
case among the batters.

## Held-out set (8 dishes), recorded before schema design

| # | Dish | R2 ids | Pattern(s) per R2 | Why held out | Main ingredients, catalogue | Gaps |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | draniki / deruny | E5a, E5b, E5c | C1 | a close relative of the design C1 dishes: tests that the easy case needs nothing new | potato, onion | |
| H2 | kolokythokeftedes | M4a, M4b | C4 | a second C4 tradition with an oven variant | courgette, eggs, dill | flour, feta |
| H3 | chawanmushi | A8a | C6 | egg matrix with a liquid ratio and steaming | eggs | dashi |
| H4 | petits farcis niçois | M16a, M16b | C7a | several vessel vegetables in one dish | courgette, tomato, onion | peppers, aubergine |
| H5 | pierogi ruskie / vareniki | E16a, E16b | C7c + C2a | a **dough** wrapper (doughs are not modelled) around a cooked-potato filling | potato, onion | flour, quark |
| H6 | spanakopita / ıspanaklı börek | M8a, M8b | C8 + C4a | pastry sheets as layers around a salt-squeezed filling | eggs, onion, dill | spinach, filo or yufka, feta |
| H7 | zha qie he | A12a, A12b | C7 + C9 | hinged slices around a filling, battered, double fried | | aubergine, minced meat |
| H8 | moi moi | A19a, A19b | C3 | a raw pulse paste steamed in a mould, unaerated | onion | black-eyed beans |

**Why these:**
- They spread over seven of the nine patterns.
- Four are deliberately hard: a dough wrapper (H5), pastry layers (H6), a
  nested coat on a filled piece (H7) and a mould (H8).
- One is deliberately easy (H1), so a failure there would mean the model
  only accommodates its 27 dishes.
- None shares its R2 dish id with a design dish.

**What had already been seen of the held-out dishes** before this choice,
through R2's summary documents (`patterns.md`, `mechanisms.md` section 2,
`requirements.md`, `evaluation.md`):
- their pattern assignment and the mechanism lines that cite them;
- for E5a, the spot-check row (salt 5-7 min, squeeze, egg and flour, crust
  before turning);
- for A12 and A19, the one-line notes "double fry" (A12b) and "a mould for
  moi moi" (A19b).

Their recipe sections in `recipes.md` were not opened until the schema was
frozen (step 4).

## Gaps across both sets

- **Pantry staples are not catalogued**: wheat flour, potato starch,
  cornflour, rice flour, gram flour, milk, dried pulses. Every C3 dish
  depends on a dried pulse outside the catalogue, so C3 has no dish whose
  main ingredient is confirmed at Lidl Finland. Dried peas (R4's transfer
  candidate) are not catalogued either.
- **Aubergine** (parmigiana, zha qie he, farcis) is not in the catalogue.
- **Meat and fish fillings** (kaalikääryleet, kaalilaatikko, korokke,
  croquetas, arancini ragù) are outside the vegetable scope and recorded as
  additions only.
- **No Finnish dish in C1-C3, C5 or C9.** The Finnish dishes are
  porkkanalaatikko (C6), kaalikääryleet (C7), kaalilaatikko (C8) and carrot
  patties (C4); rårakor (E7, Finland-Swedish) was left out of both sets to
  keep C1 at three.
