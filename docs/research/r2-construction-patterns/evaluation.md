# R2 evaluation

## Where the evidence contradicted an initial expectation

Expectations are listed as they stood before the recipes were read: in the
brief, in the R1 handoff, or in the model. Each is checked against the
evidence.

| # | Expectation | What the recipes showed | Verdict |
| --- | --- | --- | --- |
| 1 | A patty or fritter needs a binder, a bulk and a flavouring (the kind of role list the brief warned against) | Three patterns hold with **no added binder**: C1 released starch, C2 cooked starch, C3 raw pulse paste. Containment (C7) needs none in the filling. A binder is needed only when the main material is watery and starch-poor (C4) | contradicted. Binding is decided by how the main material is transformed, not by the dish's shape |
| 2 | Egg is the main binder | Egg is optional in the Belarusian classic draniki (E5b), egg-free porkkanalaatikko (E17a), Finnish cabbage rolls (E12), most falafel (M1, M2) and akara (A18a tried it, dropped it). In nem it is **capped because it adds water** (A13b-c). Where it is near-universal (courgette fritters, 92%), it works together with flour | contradicted as a general rule; holds for C4 |
| 3 | Grated vegetables must be dewatered | Only about a third of corpus latke and courgette-fritter recipes write it down (31%, 34%). Raggmunk (E6), placki E3b, bolinho A17b and börek M8b keep the water and balance it elsewhere. Pakoda and hobak-jeon (A1a, A9b) use it as the batter liquid. Carrot is never squeezed (E18) | contradicted: the **water budget** is universal, dewatering is one of nine routes |
| 4 | Rösti holds through the potato's own starch (the brief's example) | Boiled rösti holds through **cooked, retrograded** starch after one or two days of storage (E1a, E1c). The Zürich raw version **rinses** the grated potato (E1d), which removes surface starch, and still holds. The claim that "only starch holds rösti together" came from a search snippet that was never read | partly supported. Starch is involved, but two different states of it, and the crust (H9) does structural work too |
| 5 | Falafel holds through ground soaked chickpeas | Confirmed in all 10 Arabic-language recipes. But under the same name, the American corpus mostly cooks or cans the chickpeas and adds flour, crumbs or egg | confirmed for the tradition. The name covers two mechanisms |
| 6 | The handoff's structural roles: shell, filling, substance, flavour, final thermal step | **Shell/filling** fits C7 only. **Flavour** never appears as a structural role in any recipe. The **final thermal step** is more structural than expected: crust before turning (8 sources), hot fat, starch in the dumpling water, a drier mass for baking | partly supported. "Flavour" dropped; the final step promoted |
| 7 | R1's `binder` function and `presser` pulp marked `binder: true` | Squeezed starch-poor pulp is what *needs* binding (C4) | contradicted (`requirements.md`) |
| 8 | Courgette `holds_shape_cooked: false` | Courgette is the most common vessel: blanched, hollowed, refilled and baked, and it stands (M16, M17) | contradicted for whole or halved shells |
| 9 | Recipes disagree on when to salt | They state the same reason; timing follows what happens to the water next (`mechanisms.md`, section 3) | resolved, not contradictory |
| 10 | Gołąbki use raw rice that cooks inside | No Polish or Finnish recipe read did; all used cooked grain. Raw rice does appear in Turkish sarma, Greek oven gemista and 30% of corpus cabbage rolls | contradicted for the Polish and Finnish sources read |
| 11 | Cheese in fritters works as a binder | It is often present (58% of corpus courgette fritters), but **no source states** a binding role (M3b explicitly gives none) | not supported, and not refuted |
| 12 | English-only searching misses established practice (R1 Z-1) | Confirmed again. The settled-starch return (convergence 1) is written down in German, Polish, Hebrew, Russian, Ukrainian and Korean, but only in 3% of the English-language corpus. Raw-pulse falafel is the norm in Arabic and the exception in the English corpus | confirmed |

## Answers to the step 2 questions, in one line each

- **Which ingredients give structural integrity?** Depends on the pattern:
  - the main material itself (C1-C3);
  - egg and flour together with the vegetable's remaining water (C4);
  - a batter (C5) or egg (C6);
  - a wrapper or shell (C7);
  - a thickened liquid (C8);
  - a surface coat (C9).
- **Which transformations make it hold?**
  - starch released raw and gelatinised in the pan;
  - starch cooked and retrograded by cooling;
  - partial gelatinisation by scalding;
  - grinding soaked raw pulses;
  - egg coagulation;
  - flour hydration;
  - crust formation;
  - a thickened liquid setting;
  - containment and packing.
- **Is a separate binder necessary?** No for C1-C3 and inside C7; yes for C4.
  The same dish name can fall either side (falafel).
- **How is moisture handled?** Nine routes, W1-W9. Salt timing follows the
  route.
- **What is essential vs optional?** Per dish in `mechanisms.md` section 1.
  Generally essential: the water is dealt with; cooked masses are cooled; the
  crust forms before turning. Generally optional: egg, flour, salting before
  squeezing, resting.
- **Convergence:** 13 cases across independent traditions (`mechanisms.md`,
  section 4). The strongest are settled starch returned (6 traditions), raw
  pulse paste (3 regions), cooling before shaping (13 traditions) and not
  turning before the crust has set (7 traditions).

## Spot check of `recipes.md` against the source pages

On 2026-11-24, 12 recipes were re-read as **raw page text** in the built-in
browser (`get_page_text`, or a DOM text extract with `javascript_exec` where
the page text was too long). No summarising tool was used, and every page
loaded. The sample was stratified:
- 3 E, 4 M, 5 A recipes, in 10 languages;
- M13a, the quantity flagged earlier;
- the recipes behind the strongest convergences: settled starch returned
  (German, Polish, Russian, Korean) and raw pulse paste without binder
  (falafel, vada, akara);
- the salt-and-squeeze courgette filling;
- the own-juice batter;
- a stuffed vegetable that gets its own flesh back.

Each was checked for the operation sequence and its order, the essential
steps, the quantities behind a claim, and the stated reasons. A **major**
discrepancy would be one that changes a mechanism, pattern or convergence
claim.

| Id | URL | Language | Read as | Result | Correction |
| --- | --- | --- | --- | --- | --- |
| E2b | https://www.koeln.de/?p=76323 | German | raw page text | match | none. Sieve, 15 min, settled starch returned, 2 eggs + 2 tbsp flour or oats per kg; no reason given, as recorded |
| E3a | smaker.pl …placki-ziemniaczane-wg-magdy-gessler… | Polish | raw page text | minor | order: egg and flour are mixed in **before** the starch is returned (with the sour cream). Starch return, quantities and the sour-cream reason confirmed |
| E5a | https://t-j.ru/draniki/ | Russian | raw page text (after a bot-check redirect) | minor | order: egg and flour before the starch. "About 10 min" standing time and the stated reason "densifies the mass" are **not on the page**; removed. Salt 5-7 min, squeeze reason, 1 egg + 1 tbsp flour per 600 g, crust before turning confirmed. Reader comments not visible in the raw read: marked unverified |
| M2a | mawdoo3.com …الفلافل_الشامية | Arabic | raw page text | match | raw chickpeas soaked overnight; canned as an alternative in the list; blend, spices, baking powder, shape, fry; no egg, flour or bread |
| M12c | https://andaluciainforma.es/?p=14348 | Spanish | DOM text extract | match | 135-140 °C 15 min "to dehydrate the potato"; hot potato into 9 beaten eggs; rest 15 min so it "drinks" the egg |
| M13a | directoalpaladar.com …croquetas-jamon-iberico-huevo-duro… | Spanish | raw page text | minor | the page itself says "1 cucharada sopera colmada" of flour for 600 ml milk: the rendering was faithful, and the error is probably the source's. Omitted stated reason added: film so the béchamel does not form a skin |
| M17a | gustoblog.it …zucchine-ripiene-alla-ligure… | Italian | DOM text extract | match | blanch 10 min, scoop, chop, cook the flesh with onion, eggs + parmesan + ricotta, crumbs "per compattare", bake 200 °C 30 min |
| A3a | hebbarskitchen.com/hi/medu-vada-recipe-medhu-vadai/ | Hindi | DOM text extract | match | 3 h soak, longer absorbs oil (more than 4 h watery), 4 tbsp water, beat in circles for air, 2 tbsp rice flour, salt just before frying |
| A9b | https://www.10000recipe.com/recipe/6855442 | Korean | DOM text extract | match | shred, salt, 5 min until water comes out, add (wheat) flour, "물은 넣지 마세요"; a reviewer added egg when it fell apart |
| A10a | https://www.10000recipe.com/recipe/6850115 | Korean | DOM text extract | match | blend with water, sieve, settle, pour off, starch "핵심 포인트", salt only, flip once |
| A11a | https://post.smzdm.com/p/ak852x3r/ | Chinese | DOM text extract | match | salt 10 min "非常关键" against wrapper splitting, squeeze hard, rough chop, cooled scrambled egg, stir one way, salt last |
| A18a | https://ounjealadun.com/2015/03/14/secret-to-great-akara-balls/ | English | raw page text | match | never too much water, aerate until doubled, fold pepper in three additions, salt last, deep pan; eggs tried and dropped |

**Effect on the findings: none.**
- No mechanism, pattern or convergence changes. Convergence 1 (settled
  starch returned) stands on the step itself, which all four sampled
  recipes confirm. E5a was never cited for a stated reason in
  `mechanisms.md`.
- The order corrections do not touch any claim: no finding depends on
  whether egg goes in before or after the starch.

One useful side note from A18a's comments: a reader reports making akara
from red lentils. It is weak evidence, but it bears on the split-pea row in
`transfers.md`.

## Limits of this round

- **Read through summaries, spot-checked.** Agents read pages through a
  fetch tool that summarises, and the paraphrases rest on that. A stratified
  sample of 12 of the 127 was re-read as raw page text (see "Spot check"
  below). 9 matched, 3 had minor discrepancies, none major. The errors found
  were a changed step order (twice), a standing time and a stated reason that
  the page does not give (E5a), and an omitted stated reason (M13a).
  - The summariser tends to **smooth sequences into a tidier order** and,
    once in the sample, **supplied a plausible reason** the page does not
    state.
  - The other 115 recipes were not re-read. Treat their step order and
    "source says" reasons as reliable to roughly this level. The steps
    themselves and the quantities matched in every sampled case.
  - The M13a flour quantity is on the page itself, so the error is the
    source's, not the tool's.
- **Independence is uneven.** Some sites contribute several recipes
  (yemek.com, Mawdoo3, 10000recipe, mtvuutiset.fi), and some witnesses are
  copies or diffusion (M19b, A2b, A18c). `sources.md` lists them.
- **Coverage gaps:**
  - No Persian, Georgian, Caucasian, Ethiopian (Amharic), Southeast Asian
    beyond Vietnam, or Scandinavian-Baltic beyond those read.
  - Not reached: curgete recheada (Portuguese), imam bayıldı, biber dolması,
    dolmadakia, galettes, arepas, bánh xèo, pajeon, tamagoyaki.
  - The Portuguese stuffed-courgette sequence that motivated the round is
    supported by its Niçois and Ligurian neighbours, not by a Portuguese page.
- **RecipeNLG** measures what recipes write down (a lower bound), is mostly
  North American, and its pre-cook and final-step rules were not
  hand-checked (`recipenlg.md`).
- **Mechanism names** (retrogradation, gelatinisation) come from general food
  science where the recipes give no reason. They name what is done; they were
  not tested.
- **Nothing was cooked.** The patterns are documented practice, not
  kitchen-verified.

## Kitchen tests the evidence suggests (practical, not scored)

Each compares two documented variants of the same dish. No new dish is
involved.

1. **Latke with settled starch returned vs latke with flour** (C1;
   convergence 1). Same potato, same pan.
2. **Courgette fritter by three water routes:** salt-rest-squeeze (W1),
   squeeze only (W2), no squeeze plus extra flour (W6). Compare cohesion when
   turning and crispness (C4; M3, M4a, A17b).
3. **Boiled rösti from potatoes stored 1 day vs 2 days** (C2; E1c's
   "entscheidend").
4. **Courgette shell refilled with its own cooked flesh** (C7a; M17a). This
   is the documented form of the R1 recombination question.
