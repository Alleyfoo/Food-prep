# S3: possibilities from techniques, labelled by recipes

**Question.** S2 counted what cooks do with each part. That only shows what
recipes already hold. Can the model generate what a part *could* become from
its physical properties, techniques and acid, and then use RecipeNLG only to
say which of those ideas recipes do not show?

Run on 2026-11-24 over the full RecipeNLG `full_dataset.csv`
(2,231,142 recipes). Code: `src/foodprep/possibilities.py` (generator),
`src/foodprep/pair_counts.py` and `scripts/count_acid_pairs.py` (counts).
Try it with `foodprep possible broccoli --part stems`.

## How an idea is made

Three hand-curated tables, none of them built from recipes:

| Table | Holds | Example |
| --- | --- | --- |
| `part_properties.yaml` | What a part physically is: water, fibre, toughness, fat, sugar, acidity, bitterness, pigment, flavour | Broccoli stems: medium water, high fibre, sweet, mild, green |
| `technique_rules.yaml` | What a technique needs from a part, and what it does | Frying needs medium water or less; it browns and crisps |
| `acid.yaml` | Acid sources with their own character, and the mechanisms by which acid changes a part | Lingonberry: very acid, astringent, keeps raw; `quick_pickle` needs a firm part and a strong liquid acid |

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

## What the counts say

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

- **Counts are co-occurrence, not use.** "Cranberry with broccoli" in 48
  recipes says they share a list (often a salad), not that cranberry acts
  as the acid. Rare and not seen are what this method trusts; common means
  little, as in the novelty check on CulinaryDB.
- **The tables are a first draft.** Ten parts, ten techniques, thirteen acid
  sources, six mechanisms. Each property is a judgement and needs checking,
  for example that tomato skin should not be steamed.
- **No tasting yet.** The ideas are hypotheses. The next step for any of them
  is a Scout protocol and a recorded tasting, as for brown butter.
- **Licence.** RecipeNLG is for non-commercial research. Only counts are
  committed (`pair_counts.yaml`).

## Next

- Turn the top Scout ideas into protocols (lingonberry on roasted broccoli
  stems already waits for the picking season).
- Add more modifier mechanisms beyond acid: fat, salt, sugar, umami, smoke.
- Add parts for carrot (tops, peel) and banana (peel), whose properties
  already fit these techniques.
