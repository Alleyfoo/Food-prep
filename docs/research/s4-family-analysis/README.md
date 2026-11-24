# S4: what families cooks add, against the model's missing roles

**Question.** S3 grouped ideas by family (acid, fat, salt, umami, sweet,
protein, carb). Families are big enough to count reliably where single
ingredients are not: lingonberry is in 222 recipes, some acid in hundreds of
thousands. So, for each ingredient and technique: which families do cooks
add, does that match what the model says each state is missing, and which
families appear together?

Run on 2026-11-24 over the full RecipeNLG `full_dataset.csv`
(2,231,142 recipes). Code: `src/foodprep/family_profiles.py`, counted in the
same pass as the member pairs by `scripts/count_family_pairs.py` (~28 min).
Counts: `src/foodprep/data/family_profiles.yaml`. Try
`foodprep family-profile broccoli`.

## Compared against what already exists first

| Existing system | What it is | Relation to families |
| --- | --- | --- |
| `roles` in tomato.yaml | What an ingredient does on a plate | **Families are these roles.** No new vocabulary. (`sweet` is used in ingredients' `base_roles` but was never declared as a role.) |
| `base_roles` per ingredient | Which roles an ingredient fills | families.yaml must carry them (tested); it adds a level per family, forms and a corpus pattern |
| `missing_roles` per curated state | What the model says a state lacks | **The claim this analysis checks** |
| Flavour dimensions (vocabularies.yaml) | What you taste: salty, sour, rich_fatty... | A separate layer for routes and the Taste Circle; `ROLE_TO_FLAVOUR_DIMENSION` maps roles onto it |
| `INGREDIENT_FLAVOUR_DIMENSIONS` (query.py) | A hand-written ingredient-to-dimension table | **The real duplicate**: a third copy of ingredient membership, beside base_roles and families.yaml. Left as it is; worth deriving from one source later |
| `corrections` (too_bitter, too_rich...) | Generic repair advice | Agrees with the family mechanisms (too bitter: fat, sweetness, salt) |

## Method

- A recipe has a family when its ingredient list names any member of it at
  level medium or above. Two acids in one recipe count once.
- 21 everyday members were added first so the shares mean something:
  cooking oil, mayonnaise, cheese, sour cream, buttermilk, wine, orange,
  mustard, pickles, beef, pork, turkey, shellfish, fish, beans, tortilla,
  crackers, mushroom, Worcestershire, jam, dried fruit. Families now have
  75 members.
- A member that is a part of the target is not counted for it (tomato gel
  for tomato). Tomato does count as acid and umami for broccoli and avocado.
- Techniques come from the directions, as in S2. A recipe can have several.
- The curated check maps each state's technique to a corpus word (raw
  assemble, raw slaw and salsa are all `raw`; simmer is `boil`), and the
  corpus cannot tell florets from stems, so parts share one row.
- A curated missing family is **agrees** when half the recipes or more add
  it, **partly** between one in five and half, and a **gap** under one in
  five. A family the model does not list but half the recipes or more add is
  **unlisted**.

## What it says

### Broccoli: share of recipes with each family

| Technique | Recipes | acid | fat | salt | umami | sweet | protein | carb |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| any recipe | 2,231,142 | 42% | 79% | 69% | 35% | 46% | 69% | 31% |
| all broccoli | 49,247 | 35% | 93% | 84% | 64% | 15% | 81% | 51% |
| bake | 23,395 | 23% | 95% | 85% | 56% | 3% | 86% | 57% |
| soup | 16,201 | 26% | 92% | 83% | 67% | 5% | 82% | 57% |
| boil | 14,721 | 39% | 92% | 86% | 73% | 12% | 80% | 60% |
| sauté | 7,472 | 28% | 96% | 79% | 77% | 8% | 74% | 64% |
| raw | 3,502 | 69% | 93% | 82% | 69% | 45% | 76% | 39% |
| steam | 3,315 | 44% | 90% | 84% | 62% | 16% | 73% | 48% |
| stir-fry | 3,005 | 44% | 92% | 85% | 85% | 36% | 80% | 49% |
| roast | 947 | 61% | 94% | 90% | 65% | 22% | 68% | 49% |

- **Broccoli gets less acid than the average recipe** (35% against 42%
  across the whole corpus, desserts included), but much more umami (64%
  against 35%). The "any recipe" row is the baseline; eggs in baking are why
  protein is 69% even there.
- **Fat and salt are near universal** (about 90% and 85% for every
  technique and all three ingredients). They are never the interesting
  family.
- **Acid is the family that depends on the technique.** Raw broccoli gets
  acid in 69% of recipes, roasted in 61%, but baked in 23%, soups 26%,
  sautéed 28%. A casserole or a soup is where broccoli usually goes without
  acid, so that is where the acid mechanisms (lift a mild soft state) have
  the most room.
- **Sweet follows dressings and sauces:** raw 45% (slaw dressings),
  stir-fry 36% (sauces), bake 3%.
- **Avocado almost always gets acid** (85% overall, 93% raw): lime and lemon
  are part of what avocado is in this corpus.
- **Tomato still gets acid in 60% of raw recipes** although it is acid
  itself (vinegar and lemon dressings).

### The model's missing roles against practice

- **No curated gap.** Every family the model lists as missing is one cooks
  add in at least one recipe in five, and mostly in half or more. The
  curated `missing_roles` describe practice well.
- **Partly** (listed as missing; 20–50% add it): broccoli acid when steamed
  (44%), stir-fried (44%) and sautéed leaves (28%); tomato acid when reduced
  (36%); carb for several states (about half).
- **Umami is the family the model leaves out.** It is unlisted but usual in
  almost every broccoli and tomato state (62–85%): cheese sauces, stock,
  soy, mushroom soup and tomato. If the model's missing roles are meant to
  match practice, umami belongs on most of them.
- **Protein is usual everywhere** (68–90%) and is listed for most states
  already.
- **Sweet is never a curated missing role**, yet 36–45% of raw and
  stir-fried broccoli recipes add it.

### Family sets

The most frequent exact sets for broccoli are fat + salt + umami + protein
+ carb (16%) and fat + salt + umami + protein (12%); the first set with acid
is 7%. For avocado the top set already includes acid (21%), and acid with
only salt and umami (guacamole-like) is 4%.

## Decision: umami joins the missing roles (2026-11-24)

The user chose to make the curated missing roles describe practice. Umami
was added (priority medium) to the six broccoli states where most recipes
add it and the state does not supply umami itself:

| State | Recipes adding umami | Umami filler added |
| --- | ---: | --- |
| raw florets | 69% | parmesan |
| steamed florets | 62% | parmesan |
| soup | 67% | stock |
| raw stem slaw | 69% | fish sauce |
| stir-fried stems | 85% | soy sauce |
| sautéed leaves | 77% | anchovy |

- **States that already supply umami were left alone.** Roasted and
  stir-fried florets and the cooked tomato states (roast, simmer, reduce,
  soup) list umami in their `state_profile.provides`. The check now reports
  these as "supplied by the state itself" instead of "not listed".
- **Miso on steamed broccoli was not added as a pairing.** It is an open
  Scout idea, and a curated pairing would quietly turn the hypothesis into an
  established fact.
- **Meal repair follows.** Steamed broccoli now asks for umami, and parmesan
  covers both protein and umami there. Pairings cite a new evidence source,
  `recipenlg_families`.
- After the change no broccoli or tomato state shows umami as "not listed".

## Limits

- **Co-occurrence, not use.** A family in the ingredient list may sit in a
  different component (cheese in the crust, lemon in the dessert).
- **Casseroles inflate protein and umami.** Cream of mushroom soup counts as
  umami, eggs as protein; 23,395 of the 49,247 broccoli recipes bake.
- **Technique words are rough**, as in S2: "dry" also catches "pat dry".
- **Parts collapse.** The corpus row for stir-fry serves both curated
  stir-fried florets and stems.
- **Herb, aromatic, heat and crunch are roles too** but not families yet, so
  the curated claims about them are not checked.
- **Licence.** RecipeNLG is for non-commercial research; counts only.

## Next

- Point the acid Scout ideas at the states where acid is least common in
  practice (baked and soup broccoli) rather than where it is already usual.
- Derive `INGREDIENT_FLAVOUR_DIMENSIONS` from families.yaml so membership
  lives in one place.
