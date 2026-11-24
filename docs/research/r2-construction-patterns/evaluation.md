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

## Limits of this round

- **Read through summaries.** Agents read pages through a fetch tool that
  summarises; the paraphrases rest on that. A spot check by re-reading a page
  was not done this round. One implausible quantity is flagged (M13a).
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
