# S1: sources for how ingredient parts are processed

**Question.** ADR 0002 decomposes an ingredient into parts before processing
them. CulinaryDB lists only ingredients, so it shows which parts are popular,
not how a cook separates and handles them. What do RecipeNLG and Jacques
Pépin say about the parts of a **tomato** and **broccoli**? Is each source
usable for Food-prep?

Run on 2026-11-24. Scripts and counts are in `evidence/`.

## Verdict

| Source | What it tells us | Usable? |
| --- | --- | --- |
| **RecipeNLG** | **Practice.** How often home cooks do each step to each part, and whether they keep the part or throw it away. | **Yes, as research evidence:** counts kept with the data, like the novelty cache. It needs the official download under its non-commercial terms. Raw recipe text stays out of the repo. |
| **Pépin** | **Method and judgement.** The named sequence of steps, and which parts an expert says are worth using. | **Yes, as a curation reference.** You record facts in your own words with a page or video citation. It cannot be imported: it is copyrighted and has no machine-readable form. |

The two sources disagree in exactly the useful place. Home cooks throw away
broccoli stems almost as often as they use them. Pépin calls the stems the
tastiest part. Neither source alone would tell the app that.

## RecipeNLG

**What it is.**
- 2,231,142 recipes with ingredient lines **and step-by-step directions**,
  mostly American home cooking (cookbooks.com and similar sites).
- Published by Poznań University of Technology
  ([paper](https://aclanthology.org/2020.inlg-1.4)).

**How it was read.**
- The official copy is behind a terms form, so the survey queried a public
  Hugging Face mirror (`Mahimas/recipenlg`, same 2,231,142 rows) through its
  read-only filter interface. Nothing was downloaded.
- Each query was a substring filter. A substring filter can pair "peeled"
  and "tomato" from different lines, so precision was checked on 100
  matching rows per query: does one sentence carry the pattern?
- Estimates below are total matches × precision.

**Tomato** (312,317 recipes list tomato)

| Step or part | Est. recipes | Precision | What the sentences show |
| --- | --- | --- | --- |
| peeled tomato in an ingredient line | ~24,800 | 0.53 | about a quarter are canned peeled tomatoes |
| seeded tomato in an ingredient line | ~16,900 | 0.62 | the seeds and gel are thrown away |
| cored | ~3,600 | 0.67 | the core is cut out, sometimes "reserve what is inside" for stuffed tomatoes |
| "peel the tomatoes" in directions | ~880 | 1.00 | often the full chain: blanch, peel, quarter, deseed |
| blanch or scald, then peel | ~470 | 0.25 | |
| score an X, boil, chill in cold water | ~200 | 0.85 | the textbook sequence, written out by home cooks |
| concassé | 133 | 1.00 | the French name, used in restaurant-style recipes |
| "tomato skin(s)" | ~330 | 1.00 | of 100: 44 removed, 26 a cooking cue ("until the skins split"), 12 used (tomato roses as garnish) |
| tomato water | 108 | — | includes sun-dried tomato soaking water; one recipe sieves the gel into tomato water on purpose |
| grated, skin left behind | ~56 | 0.10 | "grate tomatoes into a bowl, discard the skin" |

**Broccoli** (52,147 recipes list broccoli)

| Part | Est. recipes | Precision | What the sentences show |
| --- | --- | --- | --- |
| florets | 10,817 | — | the default part; most recipes never mention anything else |
| stems or stalks named | ~860 | 1.00 | of 100: 38 used, 35 removed, 27 unclear |
| stems peeled, then cut and cooked | 203 | 1.00 | "peel the stalks, cut into 1-inch pieces" |
| stems discarded or "saved for another use" | ~260 | 0.90 | mostly in raw broccoli salads |
| broccoli slaw | 565 | — | almost always a **bought bag** of shredded stems: the stem is a product in its own right |
| leaves | 36 | 1.00 | 21 removed, 12 used; one recipe dries and grinds them into a seasoning |
| stems cooked first or longer | ~50 | — | the different-cooking-time rule is rarely written down |

**What it can tell Food-prep**
- **The decomposition sequences are in the text.** "Blanch, peel, quarter
  and de-seed" and "trim the leaves, peel the stalks, cut into flowerets"
  are the separation steps of ADR 0002, written by thousands of cooks.
- **Kept versus thrown away, per part, with counts.** That is the corpus
  evidence level we discussed (used / rarely used / removed / not found),
  now with a real basis.
- **Surprises worth curating:**
  - bagged broccoli slaw makes stems a mainstream ingredient;
  - grating a tomato is another way to leave the skin behind;
  - tomato gel sieved into tomato water;
  - dried broccoli leaves as a seasoning.

**Limits**
- **Keyword matching is noisy.** Precision runs from 0.10 to 1.00, and the
  used/removed split came from rough keyword classes. Peeling a broccoli
  stem counted as "removed" even though the stem is then cooked. A proper
  pipeline needs sentence-level rules per part, and probably a small
  classifier for used / removed / cooking cue, checked by hand.
- **One kitchen culture.** Mostly American home cooking, so absence still
  means "not popular here", not "not food".
- **Licence:**
  - The terms allow **non-commercial research and educational use only**.
    They bind the employer too, if the researcher works for a company.
  - The Hugging Face mirrors are unofficial redistributions. They are fine
    for a look; real use should go through the official download at
    recipenlg.cs.put.poznan.pl.
  - Aggregate counts kept in the repo are a grey area. If Food-prep is ever
    commercial, this needs a fresh look.

## Jacques Pépin

**What it is.**
- *Jacques Pépin New Complete Techniques* (2012, 728 pages; Vegetables
  chapter from page 78). It revises *La Technique* and *La Méthode*; a 50th
  anniversary edition is listed for 2026.
- Companion material is free to view:
  - the Jacques Pépin Foundation's *Essential Pépin* videos;
  - PBS / KQED recipe pages.

**What it says about the reference ingredients**
- **Tomato:**
  - The publisher describes peeling and seeding a tomato as a basic
    technique used throughout the book.
  - Tomato skin becomes a garnish: tomato roses (book and Foundation
    video).
  - Pépin's tomato bread squeezes out the seeds and juice and rubs the
    flesh on toast.
  - His tall Greek salad keeps the stem caps to put back on as decoration.
- **Broccoli:**
  - A 49-second *Essential Pépin* video is devoted to peeling broccoli.
  - His recipes call the stems the tastiest part. Cooks throw them away
    because of the fibrous skin, so peel it, cut the stems up, and cook
    them with the florets, or dice and parboil them for risotto.
  - The book's table of contents does not visibly list broccoli, so its
    coverage there is unconfirmed.

**What it can tell Food-prep**
- **Named preparations** as exact sequences. Concassé is one; peeling
  broccoli stems is another.
- **Expert judgement that a part is worth using.** This is the evidence
  RecipeNLG cannot give: popular practice throws broccoli stems away, and
  an authority says they are the best part.
- **Uses for "waste" parts:** skin as a garnish, stem caps as decoration.

**Limits**
- **Copyrighted, with no API or dataset.** The book and videos can be read
  and watched, not imported. The companion pages are copyrighted too.
- **Curation by hand.** Each fact is recorded in our own words with a
  citation (book page, video title). For ten ingredients that's realistic.
  At hundreds it isn't.
- **One chef's method.** It is classical French technique, so it needs a
  second voice before it settles anything on its own.

## How the sources fit together

| Layer | Source | Answers |
| --- | --- | --- |
| Method | Pépin, curated by hand | How is this part separated and handled? Is it worth using? |
| Practice | RecipeNLG, counted | How often do cooks do that step, and do they keep or discard the part? |
| Popularity | CulinaryDB (existing) | How common is the ingredient and its partners? |
| Own evidence | tastings (existing) | Did it work when we tried it? |

A part that is food, recommended by the method layer, but mostly thrown away
in practice, is exactly what Cook should point out. An example: "Most
recipes discard broccoli stems; peel them and they're the sweetest part."
A part with no evidence in any layer is a Scout candidate with a tasting
protocol, not something to hide.

## Not checked

- Other processing sources found in passing:
  - Escoffier's *Le Guide Culinaire* (public domain);
  - ckbk.com, a subscription library of professional cookbooks with many
    "peeling and seeding tomatoes" entries; its terms were not read.
- Recipe1M+, another instruction dataset under a research licence.
- The full RecipeNLG terms page. The licence terms above come from the
  Hugging Face dataset card quoting them.

## Sources

- RecipeNLG paper: https://aclanthology.org/2020.inlg-1.4
- RecipeNLG dataset card (terms quoted): https://huggingface.co/datasets/recipe_nlg
- Mirror queried: https://huggingface.co/datasets/Mahimas/recipenlg
- *New Complete Techniques* (Google Books record): https://books.google.com/books/about/Jacques_P%C3%A9pin_New_Complete_Techniques.html?id=h1MH2KmhxdQC
- *Essential Pépin* videos: https://jp.foundation/video-series/essential-pepin
- Peeling tomatoes and tomato roses (video): https://jp.foundation/?p=296
- Pépin recipes, *More Fast Food My Way* (KQED): https://www.kqed.org/w/morefastfoodmyway/recipes.html
- *The Complete Pépin*, vegetables episode (PBS): https://www.pbs.org/video/vegetables-and-more-rtvxme
