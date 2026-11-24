# Kitchen experiments

About five per ingredient, chosen from the generator's output and checked
against existing practice (`sources.md`, `web_…` ids). Every one is achievable
in an ordinary kitchen unless the equipment line says otherwise.

**Status of every item: unverified possibility.** None has been tested. A
result goes into `tastings.yaml` as tested or failed, as with the brown
butter tasting.

How to read each experiment:

- **Generator rank:** where the final material sits among that ingredient's
  ranked sequences. "Unranked" means the generator produced the material but
  its last step adds no function the model can name. Several useful
  preparations are unranked, which is a finding in itself (`evaluation.md`).
- **Prior practice:** what the web check found.

Safety for every experiment:

- Taste courgette raw first and discard a very bitter one (`poison_squash`).
- Fridge pickles keep about a week.
- Anything kept in oil is refrigerated and used within 4 days
  (`cdc_botulism`).

---

## Broccoli

### B-1 Stem peel as a seasoning powder
- **Start:** the peel of 2 broccoli stems (`eplucher` → peel fraction)
- **Sequence:** peel → déshydrater → moudre
- **Materials:** strips of peel → brittle dried peel → green powder
- **Rationale:** the peel is thin, low in water and very fibrous, so it dries
  fast and shatters. Grinding spreads its colour and green-bitter flavour.
- **Function:** seasoning powder, colouring
- **Limitations:** fibre may stay gritty; flavour may be more straw than
  broccoli; low yield
- **Equipment:** oven, spice grinder (or mortar)
- **Prior practice:** **no evidence found for the peel alone** (`web_b2`);
  whole-stalk and leaf powders exist
- **Generator rank:** 365 of 5,090
- **Test:**
  1. Dry the peel at 100 °C for 60–90 min until it snaps.
  2. Grind it and sieve it.
  3. Taste on buttered toast against plain toast.
- **Judge:** stays green; tastes recognisably of broccoli rather than hay; not
  gritty after sieving.

### B-2 Pickled ribbons of peeled stem
- **Start:** broccoli stems
- **Sequence:** peel (inner branch) → rubans (peeler) → acidifier
- **Rationale:** peeled stems are dense, sweet and sheetable. Thin ribbons
  pickle in minutes and stay crunchy.
- **Function:** vegetable noodles, acid carrier
- **Limitations:** a thin stem shreds (needs about 4 cm across, `web_b1`); the
  green dulls in acid
- **Equipment:** peeler, jar
- **Prior practice:** stem noodles established (`web_b1`); pickled stems
  established (`web_b4`); pickled *ribbons* not found specifically
- **Generator rank:** 2,440 of 5,090
- **Test:** ribbons from one stem in 1:1 vinegar and water with 1 tsp salt and
  1 tsp sugar, 30 min.
- **Judge:** crunchy, not woody; the ribbon holds when lifted with a fork.

### B-3 Leaves split two ways: blades as wraps, ribs as pickle
- **Start:** 4 large broccoli leaves
- **Sequence:**
  - blades: équeuter → blanchir
  - ribs: équeuter → émincer → acidifier
- **Rationale:** the blade is a broad, flexible sheet; the rib is a firm
  strip. One separation gives two uses.
- **Function:** wrapper; crunchy contrast and acid carrier
- **Limitations:** the leaves may be too small or too holed to wrap; the ribs
  may be stringy
- **Equipment:** knife, pot, jar
- **Prior practice:** the collard-wrap technique is established; for broccoli
  leaves specifically, only leaf chips were found (`web_b3`)
- **Generator rank:**
  - ribs: 1,054 of 5,090;
  - blades: unranked. The model already counts raw leaves as a wrapper, so
    blanching "adds nothing". Whether raw leaves are pliable enough is exactly
    what the test decides.
- **Test:**
  1. Wrap rice in a raw blade and in a blade blanched for 20 s.
  2. Pickle the sliced ribs for 30 min.
- **Judge:** the wrap rolls without cracking and bites through cleanly; the
  ribs stay crisp.

### B-4 Roasted leaf crumbs as a topping
- **Start:** broccoli leaves
- **Sequence:** rôtir → écraser
- **Rationale:** the leaves are thin, so they crisp in the oven like kale.
  Crushed, they become a green crisp topping.
- **Function:** crisp component, coating
- **Limitations:** too little oil gives papery chips (`web_b3`); they soften
  within a day
- **Equipment:** oven
- **Prior practice:** leaf chips niche (`web_b3`); crumbs not checked
- **Generator rank:** 1st of 5,090
- **Test:**
  1. Toss with 1 tsp oil and salt.
  2. Roast at 160 °C for 10–15 min.
  3. Crush over pasta.
- **Judge:** crisp, not burnt-bitter; still crisp 10 min after topping.

### B-5 Fried stem-peel strips (likely negative)
- **Start:** broccoli stem peel
- **Sequence:** peel → frire
- **Rationale:** thin and low in water, so it should crisp in oil.
- **Function:** crisp component, garnish
- **Limitations:** very fibrous, so it may stay stringy and chewy. The model
  cannot predict that, which is why this is worth one test.
- **Equipment:** pot of oil
- **Prior practice:** carrot peel crisps exist (`web_c2`); broccoli peel not
  found
- **Generator rank:** 2,073 of 5,090
- **Test:** fry a handful at 170 °C for 1–2 min.
- **Judge:** shatters rather than chews. If it chews, record it as failed:
  evidence that fibre needs a "stringy" property the model lacks.

---

## Carrot

### C-1 Pressed pulp as a crisp sheet, without an added binder
- **Start:** 4 carrots
- **Sequence:** râper → presser (pulp branch) → cuire au four
- **Materials:** grated carrot → juice and pulp → baked sheet
- **Rationale:** the pulp keeps the fibre and some pectin. The model marks it
  as a binder, but nothing says whether it holds together without flax or
  egg.
- **Function:** structural or crisp component
- **Limitations:** established recipes add a binder and report fragile edges
  (`web_c1`)
- **Equipment:** grater, cloth, oven
- **Prior practice:** pulp crackers established *with* a binder (`web_c1`)
- **Generator rank:** unranked. Baking adds no function the pulp did not
  already have (binder, thickener). Whether the sheet holds is a texture
  outcome the model cannot see.
- **Test:**
  1. Spread the pulp 3 mm thick, with salt.
  2. Bake at 150 °C for about 40 min.
  3. Do a second tray with 1 tbsp flour per cup of pulp.
- **Judge:** lifts as one sheet and snaps. Compare the two trays.

### C-2 Carrot juice glaze (a control for the ranking)
- **Start:** carrot juice from C-1
- **Sequence:** presser (juice branch) → réduire → monter au beurre
- **Rationale:** the sugar concentrates; the butter emulsifies into a glossy
  sauce.
- **Function:** flavour concentrate, sauce base
- **Prior practice:** established chef technique (`web_c5`)
- **Generator rank:** 2,958 of 3,912. **This is why it is here:** an
  established, delicious preparation that the ranking places near the bottom.
- **Test:** reduce 250 ml of juice by half, then whisk in 20 g of cold butter
  off the boil.
- **Judge:** glossy and sweet-savoury. If it is excellent, the ranking needs a
  sensory term.

### C-3 Carrot peel crisps
- **Start:** peel of 6 carrots
- **Sequence:** peel → frire (or roast)
- **Function:** crisp component
- **Limitations:** burns within seconds at the end (`web_c2`)
- **Equipment:** pot or oven
- **Prior practice:** niche (`web_c2`)
- **Generator rank:** 2,675 of 3,912
- **Test:** fry at 170 °C for 1 min, or roast at 160 °C for 8–10 min and watch.
- **Judge:** crisp and sweet, not bitter or burnt.

### C-4 Carrot peel powder
- **Start:** carrot peel
- **Sequence:** peel → déshydrater → moudre
- **Function:** seasoning powder, colouring (orange)
- **Limitations:** dried peel can turn bitter (`web_c6`)
- **Equipment:** oven, grinder
- **Prior practice:** niche (`web_c6`)
- **Generator rank:** 444 of 3,912
- **Test:** dry at 90–100 °C until brittle, cool fully, grind. Sprinkle on
  hummus.
- **Judge:** orange, sweet-earthy, not bitter.

### C-5 Roasted carrot-top crumbs (uncertain)
- **Start:** carrot greens
- **Sequence:** rôtir → écraser
- **Rationale:** thin and leafy, so they crisp like the broccoli leaves of B-4.
- **Limitations:** carrot greens are already very bitter; roasting may
  concentrate the bitterness
- **Prior practice:** carrot-top pesto and chimichurri are established
  (`web_c4`); crisps not checked
- **Generator rank:** 1st of 3,912
- **Test:** roast as in B-4 and taste beside B-4.
- **Judge:** pleasant bitterness, like a crisp herb, rather than harsh. Run it
  next to B-4 to see whether bitterness, which the model ignores here, decides
  the outcome.

---

## Courgette

### Z-1 Courgette skin ribbons as a component of their own (two arms)
- **Start:** 2 firm courgettes
- **Sequence:**
  - arm A: éplucher (peel branch) → sauter, 1 min in oil with garlic;
  - arm B: éplucher → acidifier.
- **Rationale:** the skin is thin, flexible and naturally ribbon-shaped, and
  firmer than the watery flesh, so it keeps a bite where courgette noodles go
  soggy.
- **Function:** vegetable noodles; acid carrier (arm B)
- **Limitations:** the skin of large fruit is tough or bitter (`web_z1`)
- **Equipment:** peeler, pan, jar
- **Prior practice:** **no evidence found**. The all-skin first strip is
  usually discarded (`web_z1`)
- **Generator rank:**
  - arm B: 211 of 1,926;
  - arm A: unranked. Sautéing adds no function to a "noodle" the model already
    has, which is the blind spot of C-2 again.
- **Test:**
  1. Peel thick strips with a Y-peeler.
  2. Do arm A and arm B.
  3. Peel the flesh as a third plate (zoodles) for comparison.
- **Judge:** keeps a bite after 1 min of heat; not bitter; better texture than
  the zoodles.

### Z-2 Courgette water, reduced to a seasoning
- **Start:** 2 courgettes
- **Sequence:** râper → dégorger (water branch) → réduire
- **Rationale:** salting draws out a salty, green liquid. Reducing it should
  concentrate the flavour into a savoury base, as tomato water does.
- **Function:** flavour concentrate, broth base
- **Limitations:** already salty, so it reduces into a salt bomb; the flavour
  may be faint
- **Equipment:** grater, colander, pan
- **Prior practice:** the water as broth or drink is niche (`web_z3`);
  reduction not found
- **Generator rank:** 60 of 1,926, the highest of the courgette experiments
- **Test:**
  1. Salt the grated courgette at 1.5% by weight.
  2. Squeeze after 20 min.
  3. Reduce the liquid to a quarter.
  4. Season a plain risotto with it.
- **Judge:** tastes of courgette, not just salt; the drained courgette still
  makes good fritters.

### Z-3 Seed core of a large courgette as a soup thickener (expected negative)
- **Start:** 1 large courgette
- **Sequence:** évider (core branch) → réduire en purée
- **Rationale:** the core is soft and very wet. Puréed, it might add body.
- **Limitations:** sources advise discarding it as bitter, slimy and fibrous
  (`web_z6`). Bitterness also raises the cucurbitacin concern: taste a crumb
  first.
- **Prior practice:** no evidence found; advised against
- **Generator rank:** 925 of 1,926
- **Test:**
  1. Taste a tiny raw piece.
  2. If it is not bitter, purée it into one portion of soup; leave another
     portion without it.
- **Judge:** thicker without sliminess or bitterness. Expect failure. A
  failure tells the model that the core needs properties it lacks (slime,
  bitterness risk).

### Z-4 Pressed courgette pulp, roasted into crumbs
- **Start:** pulp from Z-2 (or pressed grated courgette)
- **Sequence:** râper → presser (pulp branch) → rôtir
- **Function:** binder, flavour concentrate; maybe crisp
- **Limitations:** still damp, so it may steam instead of crisping
- **Generator rank:** 153 of 1,926
- **Test:** spread thin, roast at 180 °C and stir every 10 min until dry.
- **Judge:** dry, savoury crumbs that keep crisp over pasta.

### Z-5 Salting before drying courgette chips (a process question)
- **Sequence:** émincer → dégorger (drained branch) → déshydrater, against
  émincer → déshydrater
- **Rationale:** salting removes water first, so drying should be faster and
  the chips more evenly crisp.
- **Prior practice:** courgette chips established (`web_z5`); salting first
  not checked
- **Generator rank:** 690 of 1,926
- **Test:** two trays of 3 mm slices, one salted and blotted after 15 min.
  Oven at 110 °C; check every 20 min.
- **Judge:** time to crisp; evenness; taste.

---

## Tomato

### T-1 Tomato skin powder (a control: the curated path)
- **Sequence:** déshydrater → moudre on tomato skins
- **Prior practice:** niche but well documented (`web_t1`). This is the
  model's curated skin path, the one generated path labelled *established*.
- **Generator rank:** 508 of 1,933
- **Test:**
  1. Dry the skins at 60–100 °C until they shatter; ovens burn them easily.
  2. Grind them.
  3. Season eggs with them.
- **Judge:** intense tomato flavour; yield. The sources report very low yield.

### T-2 Clear tomato-water gel
- **Sequence:** filtrer → gélifier on the seeds and gel
- **Rationale:** strained gel gives a clear, acid, savoury liquid; agar sets
  it.
- **Function:** acid carrier, moisture carrier
- **Prior practice:** tomato consommé established (`web_t2`); the gel is
  niche (modernist practice)
- **Generator rank:** 775 of 1,933
- **Test:**
  1. Strain the gel from 6 tomatoes through a cloth, hung, not pressed.
  2. Set it with 1% agar (boil, then cool).
  3. Cube it over mozzarella.
- **Judge:** clear, sets firm, tastes of tomato.

### T-3 Tomato gel as the whole acid of a vinaigrette
- **Sequence:** réduire en purée → émulsionner, with oil, on the seeds and gel
- **Rationale:** the gel is acid and pectin-rich. The model now allows pectin
  to hold added oil, but only as mechanistic inference.
- **Function:** acid carrier, sauce base
- **Prior practice:** vinaigrettes with seeds niche (`web_t3`). This also
  tests the S3 tomato-gel-as-acid idea.
- **Generator rank:** unranked (the emulsion adds no function over the purée)
- **Test:** blend the gel from 4 tomatoes with 3 tbsp oil and salt; no
  vinegar. Dress a green salad.
- **Judge:** holds as an emulsion for 10 min; sharp enough without vinegar.

### T-4 Core-only tomato stock
- **Sequence:** décocter on tomato cores
- **Prior practice:** scrap stocks established, usually mixed (`web_t5`)
- **Generator rank:** 676 of 1,933
- **Test:** simmer the cores of 10 tomatoes in 500 ml water for 30 min, then
  strain.
- **Judge:** tastes of tomato rather than green stalk. The decision is whether
  cores alone are worth a stock.

### T-5 Fried tomato skin crisps
- **Sequence:** frire on tomato skins
- **Prior practice:** niche (`web_t4`)
- **Generator rank:** 1,328 of 1,933
- **Test:** wide skins from large tomatoes, 2 min in oil at 170 °C.
- **Judge:** crisp and not burnt; thin strips char (`web_t4`).

---

## Avocado

Avocado is the narrowest material here. Its flesh is fat-rich,
heat-sensitive, and the only part that is food. Its experiments mostly test
the model's own rules.

### A-1 Ripe against firm avocado, quick-pickled (tests a missing property)
- **Sequence:** acidifier
- **Rationale:** the model blocks pickling ripe avocado: too soft to stay
  firm. The sources say firm, underripe fruit works (`web_a2`). The model has
  no ripeness property to tell the two apart.
- **Test:** pickle slices of one ripe and one firm avocado for 1 h.
- **Judge:** the firm one holds and the ripe one goes slimy. That confirms
  ripeness as a property to add.

### A-2 Short sear against long heat (tests `heat_sensitive`)
- **Sequence:** quartiers → griller (2 min), against baking at 180 °C for 20 min
- **Rationale:** the model allows short searing and blocks long heat as
  bitter.
- **Prior practice:** grilled avocado established (`web_a3`); bitterness with
  long heat reported (`web_a5`)
- **Generator rank:** unranked. The function vocabulary has nothing for
  "a grilled, warm component".
- **Judge:** the grilled wedge is good; the baked one bitter. That confirms the
  rule and the blind spot.

### A-3 Avocado with added oil: purée or emulsion?
- **Sequence:** réduire en purée → émulsionner (add 2 tbsp oil while blending)
- **Prior practice:** avocado "mayonnaise" established, but closer to a purée
  than an emulsion (`web_a1`)
- **Test:** blend one avocado with lemon, then stream in 2 tbsp oil. Compare
  with the plain purée after 1 h.
- **Judge:** the oil stays in; texture lighter than the purée.

### A-4 Tomato gel instead of lime on cut avocado (from S3)
- **Sequence:** cut avocado + tomato gel (a composite of two materials; the
  family generator's `slow_browning` idea, not this generator's)
- **Rationale:** a wet acid coating slows browning. The gel is acid, wet and
  savoury.
- **Test:** three cut halves: lime, tomato gel, nothing. Photograph them at
  0, 1 and 3 h.
- **Judge:** gel browns no faster than lime, and tastes good on avocado.

---

## Negative findings already recorded

| Possibility | Why it is out | Source |
| --- | --- | --- |
| Drying avocado | turns bitter and rancid at home; the model marks it unsafe | `web_a5` |
| Anything from the avocado stone | not established as safe to eat; unsafe for every operation | `avocado_seed` |
| Peeling, zesting, segmenting, shelling, pitting in this set | the structures do not exist here (tomato skin and avocado stone are parts already; vegetable peel is not zest) | `applicability-tables.md` |
| Monder on tomato | needs the whole fruit; the model only holds its parts | `applicability.md` |
| Chiffonade of carrot greens | feathery, not a sheet that can be rolled | `applicability.md` |
| Grinding fat-rich material to powder | it turns to paste | rule in `moudre` |
