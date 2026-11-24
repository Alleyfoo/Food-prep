# S3: possibilities from techniques, labelled by recipes

**Question.** S2 counted what cooks do with each part. That only shows what
recipes already hold. Can the model generate what a part *could* become from
its physical properties, techniques and acid, and then use RecipeNLG only to
say which of those ideas recipes do not show?

Run on 2026-11-24 over the full RecipeNLG `full_dataset.csv`
(2,231,142 recipes). Code: `src/foodprep/possibilities.py` (generator),
`src/foodprep/pair_counts.py` and `scripts/count_family_pairs.py` (counts).
Try it with `foodprep possible broccoli --part stems`, one family with
`--family protein`, and the families themselves with `foodprep families`.

**Update, same day: families.** The first version knew only acid. Ideas are
now generated and sorted per *family*: what an ingredient brings to a dish.
The families are the ontology's own roles, so they tie into the existing
model. See "Families" below.

## How an idea is made

Three hand-curated tables, none of them built from recipes:

| Table | Holds | Example |
| --- | --- | --- |
| `part_properties.yaml` | What a part physically is: water, fibre, toughness, fat, sugar, acidity, bitterness, pigment, flavour | Broccoli stems: medium water, high fibre, sweet, mild, green |
| `technique_rules.yaml` | What a technique needs from a part, and what it does | Frying needs medium water or less; it browns and crisps |
| `families.yaml` | Families (acid, fat, salt, umami, sweet, protein, carb), their members with a level in each family, and the mechanisms by which a member changes or completes a part | Lingonberry: acid very high, astringent, keeps raw; `quick_pickle` needs a firm part and a strong liquid acid |

part × technique gives a state. state × acid mechanism × acid source gives
an idea with its reason, its risks (green turns olive, sweet reads as
dessert, bitter on bitter) and safety notes (rhubarb leaves, fridge pickle
only). A part that is already acid (tomato gel) gets no acid. It is a source
itself.

Only then does RecipeNLG label the idea, by how often the ingredient and the
acid source are listed together against what chance predicts
(ingredient recipes × source recipes ÷ all recipes):

| Label | Rule | Kind of idea |
| --- | --- | --- |
| Common | not rare, and 100+ recipes | Cook |
| Seen | not rare, fewer than 100 | Cook |
| Rare | under 30% of what chance predicts | Scout |
| Not seen | 0 recipes where chance predicts 5 or more | Scout |
| Untested | chance predicts under 5: the corpus cannot judge | Scout |
| Own part / Part as acid | the acid is a part, e.g. tomato gel; recipes list only the whole tomato | Scout |

## Families

| Family | Kind | Says | Members | Mechanisms |
| --- | --- | --- | ---: | --- |
| acid | modifier | brightens and sharpens | 17 | brighten browned, cut fat, slow browning, quick pickle, soften leaves, lift mild |
| fat | modifier | carries flavour and gives body | 14 | brown in fat, coat raw, round bitter, enrich soft |
| salt | modifier | seasons and sharpens every other taste | 10 | draw water, suppress bitter, season through, crisp finish |
| umami | modifier | makes it taste savoury and deep | 13 | deepen mild, echo browning |
| sweet | modifier | balances sharp and bitter | 6 | balance acid, balance bitter, glaze |
| protein | partner | makes it a meal | 9 | yolk as sauce, creamy against crisp, crisp against soft, same pan |
| carb | partner | carries and fills | 9 | soak juice, sauce for starch, base for fast, crunch on soft |

- **A member belongs to every family it brings, with a level in each.** Soy
  sauce is salt very high and umami high; bacon is fat, salt, umami and
  protein. A member counts in a family from `medium` up. The output says
  "also umami", so the cook sees what else it brings.
- **Members are tied to the ontology.** Where a member is a `tomato.yaml`
  ingredient, all its `base_roles` that are families must appear in its
  families (a test checks this).
- **A part that already has a family gets nothing from it.** Tomato gel gets
  no acid, avocado flesh no fat, tomato skin no umami. Each is then a member
  for other parts instead: tomato gel is acid and umami, tomato skin powder
  is umami. Sweet, in turn, now has something to do for the gel: balance it.
- **Modifiers change the part, partners complete the plate.** Protein and
  carb mechanisms are about the state, not the part alone: a soft yolk
  dresses a softened or browned vegetable, a creamy cheese contrasts crisp
  edges, bread soaks tomato juice.
- **Risks travel across families.** A salty member in another family (miso as
  umami) warns to season after it; a sweet member in another family
  (balsamic as acid) warns it may read as dessert.

### What the families show for broccoli

| Family | Scout ideas (rare, not seen, untested, part as member) |
| --- | --- |
| acid | rhubarb 1 vs 146, cranberry 48 vs 539, green mango, sumac, pomegranate molasses, lingonberry and sea buckthorn (untested), tomato gel |
| fat | brown butter: 0 vs 5, untested |
| umami | tomato gel, tomato skin powder |
| sweet | maple syrup 73 vs 465, sugar, pomegranate molasses |
| salt, protein, carb | none: every member is common or seen |

- **Protein and carb partners are all familiar.** Eggs, chicken, rice, pasta
  and the rest are cooked with broccoli, tomato and avocado as often as
  chance predicts or more. The new ideas sit in the modifiers.
- **Brown butter on broccoli is untested in the corpus, yet it is the one
  idea already tasted** (2026-08-12, verdict "works"). That is the kind of
  idea this method is for.
- **Avocado with sugar is rare here** (2,459 vs 10,312), though sweet avocado
  drinks are everyday food in Indonesia, Vietnam and Brazil. Like the banana
  peel, this is one kitchen culture's absence, not a verdict.

## What the counts say (acid, first version)

Pairs listed together, against chance:

| Acid source | Recipes | with broccoli | with tomato | with avocado |
| --- | ---: | --- | --- | --- |
| lemon | 239,743 | 4,680 / 5,292, common | common | 6,917 / 2,884, common |
| lime | 74,602 | 584 / 1,647, common | common | 9,416 / 897, common |
| vinegar | 197,827 | 5,200 / 4,367, common | common | common |
| cranberry | 24,440 | 48 / 540, **rare** | 391 / 3,421, **rare** | 41 / 294, **rare** |
| rhubarb | 6,600 | 1 / 146, **rare** | 34 / 924, **rare** | 3 / 79, **rare** |
| sumac | 877 | 4 / 19, **rare** | common | seen |
| green mango | 532 | 1 / 12, **rare** | common | seen |
| redcurrant | 1,207 | seen | seen | 1 / 15, **rare** |
| lingonberry | 222 | 0 / 4.9, **untested** | 1 / 31, **rare** | 0 / 2.7, **untested** |
| sea buckthorn | 4 | untested | untested | untested |

- **Lemon, lime and vinegar are what recipes mean by acid.** They are the
  Cook suggestions and hidden by default.
- **The tart fruits are possible by mechanism but nearly absent.** Cranberry
  and rhubarb are common ingredients in this corpus (24,440 and 6,600
  recipes), yet broccoli meets rhubarb once where chance predicts 146. These
  are the loud absences: the strongest Scout ideas.
- **Lingonberry is the case the corpus cannot judge.** It is in only 222 of
  2.2 million recipes. With broccoli, chance predicts five, so even zero
  says nothing. That is exactly where generation has to stand on its own:
  lingonberry is very acid, astringent and keeps raw, so the mechanisms say
  it can brighten roasted stems, quick-pickle raw stems, and cut the fat of
  avocado. The corpus only adds "never tried here".
- **Tomato gel as an acid** is invisible to recipe counts either way, so it is
  labelled as the generator's own idea.

## Limits

These were sharpened by the review of PR #4 (2026-11-24).

- **A label is evidence about the pair, not the preparation.** `label()` uses
  the ingredient-member count over all recipes. A pair that is common in
  soups is labelled common when it is suggested for roasting, even if no
  recipe roasts it. The per-technique counts shown in brackets are recipes
  whose directions mention the technique *anywhere*, not necessarily for the
  target ingredient. The output states this scope (`LABEL_SCOPE`) wherever a
  label appears; a UI must show it too. Labelling per technique would need
  techniques tied to the ingredient in the directions, which the sentence
  rules of S2 could provide later.
- **"Already has it" is an assumption, not a fact.** `already_has()` drops a
  whole family when the part supplies it at a high level: avocado gets no
  fat ideas. But sesame oil would still bring an aroma, and another fat can
  do a different job (crisping, carrying a spice). The rule is deliberate
  and tested; it should be revisited, for example by keeping members whose
  mechanism is not the family's main effect.
- **Counts must match the ontology they were made from.** Both generated
  files record `families_sha256`, a checksum of the content of
  families.yaml. The output warns when they differ, and a test fails, so an
  edited family definition forces a recount (scripts/count_family_pairs.py,
  ~28 min) before the labels are trusted again.
- **Counts are co-occurrence, not use.** "Cranberry with broccoli" in 48
  recipes says they share a list (often a salad), not that cranberry acts
  as the acid. Rare and not seen are what this method trusts; common means
  little, as in the novelty check on CulinaryDB.
- **Sugar and other baking staples inflate "chance".** Sugar is in a third
  of all recipes, mostly desserts, so any savoury ingredient looks rare with
  it. Rare against a baking staple says savoury and sweet are separate
  sections, not much more.
- **The tables are a first draft.** Ten parts, ten techniques, seven
  families with 54 members and 27 mechanisms. Each property is a judgement and needs checking,
  for example that tomato skin should not be steamed.
- **No tasting yet.** The ideas are hypotheses. The next step for any of them
  is a Scout protocol and a recorded tasting, as for brown butter.
- **Licence.** RecipeNLG is for non-commercial research. Only counts are
  committed (`pair_counts.yaml`).

## Next

- Turn the top Scout ideas into protocols (lingonberry on roasted broccoli
  stems already waits for the picking season).
- More families: herb, aromatic, heat, crunch and smoke are roles in the
  ontology too.
- Add parts for carrot (tops, peel) and banana (peel), whose properties
  already fit these techniques.
