# RecipeNLG: how often recipes take each construction step

Step 1 evidence from a corpus, to set beside the web recipes in
`recipes.md`. RecipeNLG is mostly North American home cooking (cookbooks.com,
food blogs), so it is one tradition with many voices, not a world sample.

- **Script:** `count_construction.py` (this folder). Run:
  `py -3.11 docs/research/r2-construction-patterns/count_construction.py PATH/full_dataset.csv`
- **Output:** `recipenlg-counts.md` (tables) and `recipenlg-counts.yaml`
  (the same counts, machine-readable). Counts only.
- **Hand-check sheet:** `data/corpus/recipenlg/r2_construction_check.tsv`
  (gitignored, because it holds recipe sentences): 15 sampled sentences
  per dish and feature.
- **Run:** 2026-11-24, all 2,231,142 recipes, 149 s. 27 dishes chosen by
  title, 55,036 recipes in all (largest: vegetable casseroles set with egg,
  11,647; smallest: pakora/bhaji, 251).

## How the rules were checked

Each feature is a text rule over the directions (or the ingredient list,
for additions). A recipe counts once per feature. Precision was judged by
reading 15 sampled sentences per pair (Claude, 2026-11-24):

| Dish, feature | Correct of 15 | Typical error |
| --- | ---: | --- |
| latkes, squeeze | 15 | none |
| courgette fritters, squeeze | 15 | none |
| courgette fritters, salt and rest | 15 | none |
| rösti / hash browns, squeeze | 13 | lemon juice squeezed over; liquid pressed out of a cooked dish |
| aubergine parmigiana, salt and rest | 13 | brining or simmering in salted water |
| stuffed courgette/aubergine, scooped flesh reused | 14 | a courgette-flower recipe |
| stuffed tomatoes, scooped flesh reused | 12 | "reserve for another recipe"; salting the inside |
| cabbage rolls, shell (leaves) pre-softened | 14 | a filling sentence |
| latkes, starch settled and kept | 14 | eggs "settling" in a bowl |

So the step rules are precise enough to quote to the nearest ten percent.
They do **not** measure recall: a recipe that says "grate the zucchini, mix
with egg and flour" and nothing about water counts as "no moisture removal",
whether or not the cook squeezed. Read every percentage as "at least this
many recipes write the step down".

The addition rules (egg, flour, crumbs ...) read the ingredient list, so
they are near-exact for presence; they cannot say what the egg is for. The
"main pre-cooked" and "final thermal step" rules are rougher (the first
cooking word before the first shaping word; the last thermal word) and were
not hand-checked: use them for direction, not for numbers. "Rösti / hash
browns" is dominated by American hash browns, many from frozen shredded
potato (28%), not Swiss rösti.

## What the counts say (the numbers are in `recipenlg-counts.md`)

1. **Grated-vegetable patties: the step that varies is the water, not the
   binder.** Latkes and courgette fritters almost always add egg (91%, 92%)
   and flour (75%, 74%). What separates recipes is whether they write down
   removing water: 31% of latke and 34% of courgette fritter recipes do
   (squeeze 28% / 31%; courgette also salt-and-rest 9%). Other vegetable
   fritters, mostly batters of corn kernels or cooked squash, do so in 9%
   and corn fritters in 2%: kernels and batters do not shed water the way a
   grated raw vegetable does.
2. **Latkes keep their own starch.** 3% of latke recipes (about 50) let the
   squeezed liquid stand, pour off the water and stir the settled potato
   starch back in. The same move is the core of Korean gamja-jeon and of
   draniki (see `recipes.md`); in RecipeNLG it is a minority practice next to
   the 75% that add flour.
3. **Rösti / hash browns are the one grated-potato dish that mostly adds no
   binder:** 65% add none of egg, flour, crumbs, oats, starch or meal (latkes
   4%). 13% cook the potatoes before grating or shaping (rough rule), and 28%
   start from frozen shredded potato, which is already blanched.
4. **Falafel in an American corpus is not traditional falafel.** 38% use
   canned chickpeas, 29% dried; 43% add flour, 30% crumbs, 28% egg. Only 28%
   add none of those. The traditional recipes in `recipes.md` grind soaked
   raw pulses and add no binder. Two different mechanisms under one name.
5. **Bean/veggie burgers** lean on crumbs (45%) and egg (44%) rather than
   flour (17%); 35% use canned beans, 25% chill before cooking.
6. **Stuffed vegetables recombine their own flesh.** Where a recipe hollows
   the vegetable, the scooped flesh goes into the filling in 38% of stuffed
   courgette/aubergine recipes and 27% of stuffed tomatoes (both counted
   over all recipes of the dish; scooping itself is written in 70% and 68%).
   An explicit discard is rare (4%, 11%). Peppers are rarely scooped (9%:
   their seeds and ribs are not food you put back); instead 49% pre-cook the
   pepper shell.
7. **A shell or wrapper that must bend is softened first.** 76% of cabbage
   roll recipes boil, blanch or (2%) freeze the leaves before rolling; 34% of
   vine-leaf recipes blanch or boil the leaves. Cabbage roll fillings
   use raw rice (30%) about as often as cooked (34%): raw rice cooks inside
   the roll in the liquid poured over (29%), the final step is a bake (46%)
   or a simmer (31%).
8. **Sealed doughs are crimped:** sealed/crimped in 46-62% of pierogi,
   dumpling and filled-pastry recipes; the filling is pre-cooked in 40-48%
   of pierogi and filled pastries.
9. **Aubergine dishes salt the aubergine** in 10% (parmigiana) and 15%
   (moussaka) of recipes; the reason given varies between bitterness, water
   and (once) "air". Parmigiana dredges or breads the slices in 61%.
10. **Set egg dishes:** frittata and quiche add egg in 98-99%. Quiche adds
    flour in 35% (crust); 28% of quiches and 45% of frittatas pre-cook a
    filling, the most common moisture step in these dishes (pre-cooking
    drives off water before the custard sets).
11. **Potato gratin sets without egg** (2%): 36% add flour to the milk, 56%
    add none of the counted additions and rely on the potato. Layering is
    written in 48%.
