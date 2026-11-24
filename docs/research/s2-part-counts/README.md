# S2: what RecipeNLG cooks do with each part

**Question.** S1 found that RecipeNLG holds the decomposition steps of
ADR 0002 in its directions, but its keyword counts were rough. With the
official download in hand: for each part of a **tomato**, **broccoli** and **avocado**,
how often do cooks keep it, trim it, remove it, or buy the step done?

Run on 2026-11-24 over the full `full_dataset.csv` (2,231,142 recipes).
Code: `src/foodprep/part_evidence.py`. Run it with
`py -3.11 scripts/count_part_evidence.py`. Counts:
`src/foodprep/data/part_evidence.yaml`, which `foodprep parts` reads.

## Answer

| Part | Recipes naming it | Kept | Trimmed | Removed | Bought done | Level |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| broccoli florets | 13,613 | 13,542 | 0 | 8 | 0 | default |
| broccoli stems | 2,873 | 1,848 | 655 | 320 | 0 | used |
| broccoli leaves | 206 | 69 | 0 | 130 | 0 | removed |
| tomato flesh | 483 | 456 | 0 | 4 | 0 | default |
| tomato seeds and gel | 16,869 | 473 | 0 | 16,355 | 0 | removed |
| tomato skin | 17,232 | 911 | 0 | 12,927 | 3,021 | removed |
| tomato core | 4,293 | 46 | 0 | 4,242 | 0 | removed |
| avocado flesh | 1,440 | 1,402 | 0 | 1 | 0 | default |
| avocado skin | 10,154 | 235 | 0 | 9,891 | 0 | removed |
| avocado stone | 7,988 | 291 | 0 | 7,674 | 0 | removed |

Baselines:
- 49,246 recipes list broccoli. Broccoli rabe, broccolini and Chinese
  broccoli are excluded.
- 312,317 list tomato; 240,796 list the fruit rather than only a sauce,
  paste or juice.
- 26,838 list avocado (avocado oil excluded).

Each recipe is counted once, under the strongest class it shows, in the
order kept > trimmed > removed > cue > bought done > unclear. The table
leaves out the cue and unclear columns. For tomato skin, 313 recipes use it
only as a cooking cue ("until the skins split"). Those columns are in the
YAML file.

**What it says**
- **Tomato: the seeds and gel go, the skin goes, the core goes.**
  - When a recipe says anything about the seeds, 97% throw them out.
  - When it names the skin, three in four peel it, and almost one in five
    buys canned peeled tomatoes instead.
  - The few recipes that keep the seeds reserve the juice, leave them in on
    purpose ("do not seed"), or use the scraps in a stock. They are the
    seed of the tomato gel dressing path.
- **Broccoli stems are not as abandoned as S1 suggested.**
  - Among recipes that name the stems, 87% keep them (655 of those after
    peeling or trimming the ends); 11% discard them.
  - S1's "35 of 100 removed" counted peeling as removal. Peeling now counts
    as trimmed.
  - The silent majority is the real story: florets are named in 13,613
    recipes, stems in only 2,873. A recipe that says "cut into florets" and
    never mentions the stems has most likely thrown them away. The text
    cannot show that, so it is not counted.
- **Avocado: skin and stone go, as expected for parts that are not food.**
  - The few "kept" skins are shells reused as serving cups, or dicing the
    flesh in its skin.
  - The few "kept" stones are mostly pits put back in guacamole "to keep it
    green". The curated note on the stone says this does not stop browning.
    So the corpus records a common belief that the model already corrects:
    a case where practice and method disagree.
- **Broccoli leaves are rare and usually trimmed off.** That matches the
  curated description, "Usually thrown away".
- **Florets and flesh are what the ingredient means.** Recipes rarely name
  them because "broccoli" and "tomato" already do. They get the level
  `default`, so their rarity is never read as "rarely used".

**For the app.** `foodprep parts broccoli` now shows a practice line under
each part, for example:

> Cooks mostly remove it (RecipeNLG: kept in 911, removed in 12,927, bought
> done in 3,021 of 17,232 recipes naming it).

This line is practice, not edibility. Tomato skin is edible, and its curated
path makes a powder out of it. The counts show how rare that is, which is
what makes it a Scout-worthy idea rather than a reason to hide it.

## How it was counted

- Each ingredient line and each direction sentence is read on its own. A
  sentence counts for a part when it names the part ("stems") and either
  names the ingredient or the recipe has no other ingredient with that part.
  Parsley stems, bell-pepper seeds and bay leaves are the usual traps.
- A part word right after another ingredient's name is never ours: "fennel
  seed", "bay leaf", "potato skins".
- A removal verb counts only within a few words of the part. "Remove from
  the heat" moves the pot, not the part.
- One-word removals: "peeled", "seeded" and "cored" in "2 tomatoes, peeled,
  seeded and diced".
- Negations keep the part: "unpeeled", "do not seed", "leaving the core
  intact".
- Bought done only counts when a can comes first in the line, and only for
  the skin. "4 tomatoes, peeled, or 1 can" is fresh. Weights ("6 oz. each")
  are not cans.
- "2 stalks broccoli" measures whole spears and is not about stems.

## Hand check

Each run wrote a sample of up to 15 sentences per part and class to
`data/corpus/recipenlg/hand_check.tsv`, which is ignored by git because it
holds recipe text. Claude read every sampled sentence and judged it, and
the rules were fixed after each round. Agreement is the share of sampled
sentences whose class Claude judged right.

| Part, class | Round 1 | Round 2 | Round 3 (final rules) |
| --- | --- | --- | --- |
| tomato skin, removed | 15/15 | 15/15 | not resampled |
| tomato skin, cue | 15/15 | 15/15 | not resampled |
| tomato skin, bought done | 11/15 | 13/15 | not resampled |
| tomato skin, kept | 10/15 | ~7/15 | 11/15 |
| tomato seeds, removed | 14/15 | 15/15 | not resampled |
| tomato seeds, kept | ~1/15 | ~6/15 | ~6/15 |
| tomato core, removed | 15/15 | 15/15 | not resampled |
| tomato core, kept | ~1/15 | ~5/15 | ~7/15 |
| broccoli stems, kept | 15/15 | 15/15 | 13/15 |
| broccoli stems, trimmed | 11/15 | 14/15 | not resampled |
| broccoli stems, removed | 11/15 | 13/15 | 13/15 |
| broccoli leaves, removed | 13/15 | 14/15 | 15/15 |
| broccoli leaves, kept | ~1/15 | ~6/15 | ~5/15 |
| broccoli florets, removed | 0/15 | ~4/15 | (8 recipes left) |

Avocado was added afterwards with two rounds of its own:

| Part, class | Round 1 | Round 2 (final rules) |
| --- | --- | --- |
| avocado skin, removed | 15/15 | not resampled |
| avocado stone, removed | 15/15 | not resampled |
| avocado flesh, kept | ~13/15 | ~15/15 |
| avocado flesh, removed | 0/15 | (1 recipe left) |
| avocado skin, kept | ~8/15 | ~11/15 |
| avocado stone, kept | ~5/15 | ~5/15 |

The avocado changes also touched shared rules: "no skin or pit" counts as a
removal, and "scoop" and "mash" mean a part is used. Tomato counts moved by
six recipes at most; broccoli did not move.

What this means for the table:
- The big numbers are reliable to within about a tenth. They come from the
  classes that scored 13–15 of 15: tomato removals, stems kept and
  removed, leaves removed.
- The small "kept" counts for tomato seeds, tomato core and broccoli leaves
  are about half wrong. Read them as an upper bound: tomato seeds are kept
  in at most ~470 recipes, probably half that. The same holds for avocado
  skin and stone kept.
- The method fixed rules against one sample, so the next sample can show
  new errors. Round 3 drew a fresh sample to check that.

## Limits

- **Sentence rules miss context.** "Plunge into boiling water; peel." loses
  the tomato when "peel" stands in its own sentence. So removals are a lower
  bound, and the true removal share is if anything higher.
- **Technique counts are rough.** `techniques_when_used` in the YAML records
  which cooking words appear next to a kept part. "Dry" also catches "pat
  dry". Use it to rank, not to measure.
- **One kitchen culture, mostly American home cooking.** As in S1, absence
  means not popular here, never not food.
- **Licence.**
  - RecipeNLG's terms allow non-commercial research and educational use
    only. 588,044 of its rows come from Recipe1M, which has research-only
    terms of its own.
  - `by_source` in the YAML keeps the two parts apart, so the Recipe1M rows
    can be dropped if that ever matters.
  - Only counts are committed. Recipe text and the hand-check sheet stay in
    the ignored corpus folder.

## Next

- Named preparations (concassé) are still a separate decision. Concassé
  currently counts toward skin removal.
