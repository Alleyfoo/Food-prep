# Manual eval — tomato transformation engine

Captured post-patch. Each prompt is marked below the output: `useful` / `too many` / `missing filler` / `too generic` / `actually surprising`.

Pre-patch state: test 1 'what can I do' returned a flat 12-row list (no flavour/missing/add); test 2 component-first returned the same generic list; test 5 hub counted without explaining why; test 6 scout did not exist; test 4 meal-repair only worked for bread+raw tomato.

## Test 1 — does the graph feel like a cook?

### Q: what can I do with tomatoes?
```
What you can do with tomato (top branches by confidence + reuse):
reduce
  → reduced_tomato_base
  → Strong umami, caramelized, very concentrated · Thick, dense
  → missing: fat, hydration, acid
  → add: acid: vinegar · hydration: stock, pasta_water · fat: brown_butter
  → use in: beans, braise, pasta, pizza, soup, stew

simmer
  → tomato_sauce_base
  → Deepened, rounded, integrated with aromatics · Saucy, cohesive
  → missing: fat, aromatic, carb, herb, protein
  → add: herb: basil · protein: eggs, white_beans · aromatic: garlic, onion · carb: pasta, rice · fat: olive_oil, butter
  → use in: beans, eggs, pasta, rice, stew

char
  → charred_tomato_component
  → Smokier, sweeter, deeper · Softened, blistered
  → missing: acid, herb, fat, carrier
  → add: herb: cilantro, parsley · acid: lime, capers, sumac · fat: olive_oil · carrier: tortilla
  → use in: beans, dip, grains, smoky_sauce, taco

roast
  → roasted_tomato_component
  → Sweeter, deeper, more savory, concentrated · Soft, collapsed, jammy
  → missing: salt, acid, herb, carb, protein
  → add: herb: basil, parsley, fennel_pollen · protein: eggs, soft_cheese · carb: pasta · salt: sea_salt · acid: lemon, lingonberry_vinegar
  → use in: bowl, pasta, pizza, soup, toast

salsa
  → tomato_salsa_component
  → Fresh, sharp, bright; spicy if chile added · Chunky, spoonable
  → missing: carrier, fat, protein
  → add: protein: white_beans · fat: avocado · carrier: tortilla
  → use in: bowl, dip, taco, wrap

(12 tomato transformations total — ask 'what is missing from <technique> tomato' for detail, or 'what can I do with <component>' for an after-state.)
```

**Mark:** useful — product shape: technique → component → flavour/texture → missing → add → use. Cooking moves lead (reduce/simmer/char/roast/salsa); storage branches (can/freeze/dry/pickle) demoted. Capped at 5 — avoids the 'too many options' UX risk.

### Q: I roasted tomatoes, now what?
```
After roast you have roasted_tomato_component (confidence high).
roast
  → roasted_tomato_component
  → Sweeter, deeper, more savory, concentrated · Soft, collapsed, jammy
  → missing: salt, acid, herb, carb, protein
  → add: salt: sea_salt · herb: basil, parsley, fennel_pollen · carb: pasta · acid: lemon, lingonberry_vinegar · protein: eggs, soft_cheese
  → use in: bowl, pasta, pizza, soup, toast
```

**Mark:** useful — after-state with priority-ordered gaps and fillers per gap. protein now filled (eggs/soft_cheese).

### Q: what can I add after making tomato sauce?
```
After simmer you have tomato_sauce_base (confidence high).
simmer
  → tomato_sauce_base
  → Deepened, rounded, integrated with aromatics · Saucy, cohesive
  → missing: fat, aromatic, carb, herb, protein
  → add: protein: eggs, white_beans · herb: basil · aromatic: garlic, onion · fat: olive_oil, butter · carb: pasta, rice
  → use in: beans, eggs, pasta, rice, stew
```

**Mark:** useful — sauce gaps (fat/aromatic/carb/herb/protein) with fillers grouped.

### Q: what can I batch prep from tomatoes?
```
Batch-prep from tomato (high/very-high reuse):
  - simmer -> tomato_sauce_base  (batch=very_high, freezes=True, keeps=medium, conf=high)
  - reduce -> reduced_tomato_base  (batch=very_high, freezes=True, keeps=medium, conf=high)
  - freeze -> frozen_tomato_base  (batch=very_high, freezes=True, keeps=long, conf=high)
  - can -> canned_tomato_base  (batch=very_high, freezes=False, keeps=long, conf=high)
  - roast -> roasted_tomato_component  (batch=high, freezes=True, keeps=medium, conf=high)
  - char -> charred_tomato_component  (batch=high, freezes=True, keeps=medium, conf=high)
  - soup -> tomato_soup_base  (batch=high, freezes=True, keeps=medium, conf=medium_high)
  - dry -> dried_tomato_component  (batch=high, freezes=False, keeps=long, conf=medium)
```

**Mark:** useful — ranked by reuse + freezer/keeps flags.

### Q: what ingredient unlocks the most tomato transformations?
```
Ingredients that unlock the most tomato transformations:
  - olive_oil unlocks char, dry, raw_assemble, roast, simmer because it fills fat (5 transformations)
  - basil unlocks raw_assemble, roast, simmer, soup because it fills herb (4 transformations)
  - white_beans unlocks char, salsa, simmer because it fills carb, protein (3 transformations)
  - pasta unlocks reduce, roast, simmer because it fills carb (3 transformations)
  - bread unlocks raw_assemble, salt_and_drain, soup because it fills body, carb, carrier (3 transformations)
  - onion unlocks raw_assemble, salsa, simmer because it fills aromatic, crunch (3 transformations)
  - garlic unlocks char, simmer, soup because it fills aromatic (3 transformations)
  - sea_salt unlocks raw_assemble, roast because it fills salt (2 transformations)
  - stock unlocks reduce, soup because it fills body, hydration (2 transformations)
  - eggs unlocks roast, simmer because it fills protein (2 transformations)
```

**Mark:** useful — now explains WHY (which techniques + which roles), not just a count.

## Test 2 — component-first queries

### Q: what can I do with roasted_tomato_component?
```
roasted_tomato_component (a reusable component)
  made by: roast (confidence high)
  tastes/feels: Sweeter, deeper, more savory, concentrated · Soft, collapsed, jammy
  use it in: bowl, pasta, pizza, soup, toast
  if building a meal on it, still missing: salt, acid, herb, carb, protein
  add: carb: pasta · acid: lemon, lingonberry_vinegar · herb: basil, parsley, fennel_pollen · salt: sea_salt · protein: eggs, soft_cheese
```

**Mark:** useful — starts from the after-state; lists uses + what a meal built on it still needs. Previously returned the generic 12-list.

### Q: what can I do with tomato_sauce_base tomorrow?
```
tomato_sauce_base (a reusable component)
  made by: simmer (confidence high)
  tastes/feels: Deepened, rounded, integrated with aromatics · Saucy, cohesive
  use it in: beans, eggs, pasta, rice, stew
  if building a meal on it, still missing: fat, aromatic, carb, herb, protein
  add: protein: eggs, white_beans · aromatic: garlic, onion · fat: olive_oil, butter · carb: pasta, rice · herb: basil
```

**Mark:** useful — component-first recognised despite the 'tomorrow' noise.

### Q: what can I do with reduced_tomato_base?
```
reduced_tomato_base (a reusable component)
  made by: reduce (confidence high)
  tastes/feels: Strong umami, caramelized, very concentrated · Thick, dense
  use it in: beans, braise, pasta, pizza, soup, stew
  if building a meal on it, still missing: fat, hydration, acid
  add: fat: brown_butter · acid: vinegar · hydration: stock, pasta_water
```

**Mark:** useful — reduced base uses (stew/braise/pizza) surfaced.

### Q: what tomato components freeze well?
```
tomato components that freeze well:
  - roast -> roasted_tomato_component
  - char -> charred_tomato_component
  - simmer -> tomato_sauce_base
  - reduce -> reduced_tomato_base
  - soup -> tomato_soup_base
  - freeze -> frozen_tomato_base
```

**Mark:** useful — freezer-friendly list, fresh excluded.

## Test 3 — missing-role sanity

Expected: gaps differ by transformation (raw→salt/fat/herb/crunch/carrier; roast→salt/acid/herb/carb; soup→body/cream/crunch/protein; pickle→mild_base/fat/protein). If gaps were identical the data would be too generic.

### Q: what is missing from raw tomato?
```
raw_assemble
  → fresh_tomato_component
  → Bright, juicy, sweet-acidic · Juicy, soft, sometimes watery
  → missing: salt, fat, herb, crunch, carrier
  → add: fat: mozzarella, olive_oil · herb: basil · crunch: croutons, cucumber, onion · carrier: (no curated filler) · salt: sea_salt
  → use in: bowl, caprese, panzanella, salad, sandwich, toast
```

### Q: what is missing from roasted tomato?
```
roast
  → roasted_tomato_component
  → Sweeter, deeper, more savory, concentrated · Soft, collapsed, jammy
  → missing: salt, acid, herb, carb, protein
  → add: acid: lemon, lingonberry_vinegar · herb: basil, parsley, fennel_pollen · protein: eggs, soft_cheese · salt: sea_salt · carb: pasta
  → use in: bowl, pasta, pizza, soup, toast
```

### Q: what is missing from tomato soup?
```
soup
  → tomato_soup_base
  → Softer acidity, rounded, aromatic · Liquid to thick depending on bread/cream
  → missing: body, cream, crunch, protein
  → add: body: bread, stock · crunch: croutons · protein: (no curated filler) · cream: cream
  → use in: chilled_soup, soup
```

### Q: what is missing from pickled tomato?
```
pickle
  → pickled_tomato_component
  → Sharper, sweet-sour, spiced · Firm-pickled or jammy-chutney
  → missing: mild_base, fat, protein
  → add: fat: (no curated filler) · protein: grilled_fish, tofu · mild_base: potato
  → use in: cheese_board, condiment, relish, sandwich
```

**Mark:** useful — gaps genuinely differ by family (raw needs carrier, roast needs acid, soup needs cream/body, pickle needs mild_base). Not generic.

## Test 4 — meal repair

### Q: I have mashed potatoes and roasted chickpea patties. What taste is missing?
```
You have: mashed_potatoes, roasted_chickpea_patty
  provided roles: body, carb, fat, mild_base, protein, salt, umami
  missing for a balanced plate: acid, herb, crunch
  add:
    - acid: vinegar, lime, tomato, lemon
    - herb: basil, parsley, cilantro, thyme
    - crunch: croutons, cucumber, onion, rye_crumbs
```

**Mark:** actually surprising (good) — engine recognises both plate items, unions provided roles (cream counts as fat), and lands on acid/herb/crunch exactly as predicted. Pre-patch it latched onto 'roasted' and returned the tomato roast branch.

### Q: I have pasta and tomato sauce. What is missing?
```
You have: pasta, tomato_sauce
  provided roles: acid, body, carb, hydration, umami
  missing for a balanced plate: salt, fat, herb, crunch, protein
  add:
    - salt: sea_salt
    - fat: olive_oil, butter, mozzarella, soft_cheese
    - herb: basil, parsley, cilantro, thyme
    - crunch: croutons, cucumber, onion, rye_crumbs
    - protein: mozzarella, eggs, white_beans, parmesan
```

**Mark:** useful — recognises pasta (carb) + sauce (acid/umami), reports missing salt/fat/herb/crunch/protein. carb correctly satisfied.

### Q: I have bread and raw tomatoes. What should I add?
```
You have: bread, raw_tomato
  provided roles: acid, carb, carrier, crunch, hydration
  missing for a balanced plate: salt, fat, herb, protein
  add:
    - salt: sea_salt
    - fat: olive_oil, butter, mozzarella, soft_cheese
    - herb: basil, parsley, cilantro, thyme
    - protein: mozzarella, eggs, white_beans, parmesan
```

**Mark:** useful — bread (carb/crunch) + raw tomato (acid) → missing salt/fat/herb/protein → caprese-on-toast.

### Q: I have roasted tomatoes and beans. What makes this less heavy?
```
To lighten a heavy/rich plate, add brightness and crunch:
  - acid: vinegar, lime, tomato, lemon  (cuts richness)
  - herb: basil, parsley, cilantro, thyme  (freshness)
  - crunch: croutons, cucumber, onion, rye_crumbs  (contrast)
  avoid: more fat / body / cream — that makes it heavier.
```

**Mark:** useful — lighten intent recommends acid/herb/crunch and explicitly warns against more fat/body/cream.

## Test 5 — hub (explained)
```
Ingredients that unlock the most tomato transformations:
  - olive_oil unlocks char, dry, raw_assemble, roast, simmer because it fills fat (5 transformations)
  - basil unlocks raw_assemble, roast, simmer, soup because it fills herb (4 transformations)
  - white_beans unlocks char, salsa, simmer because it fills carb, protein (3 transformations)
  - pasta unlocks reduce, roast, simmer because it fills carb (3 transformations)
  - bread unlocks raw_assemble, salt_and_drain, soup because it fills body, carb, carrier (3 transformations)
  - onion unlocks raw_assemble, salsa, simmer because it fills aromatic, crunch (3 transformations)
  - garlic unlocks char, simmer, soup because it fills aromatic (3 transformations)
  - sea_salt unlocks raw_assemble, roast because it fills salt (2 transformations)
  - stock unlocks reduce, soup because it fills body, hydration (2 transformations)
  - eggs unlocks roast, simmer because it fills protein (2 transformations)
```
**Mark:** useful — each filler now lists the techniques it unlocks and the roles it fills.

## Test 6 — scout

### Q: what unusual but viable pairing works with roasted tomato?
```
Scout / experimental (plausible but uncommon — NOT classic):
  - rye_crumbs + roast: rye crumbs: carrier + crunch; Nordic-available; plausible with roasted tomato
  - lingonberry_vinegar + roast: lingonberry vinegar: acid + berry brightness; experimental
  - orange_zest + roast: orange zest: aromatic acid; experimental with roasted tomato
  - fennel_pollen + roast: fennel pollen: herbal aromatic; rare, experimental with roasted tomato
  (These are speculative — labelled so no one pretends they're tradition.)
```

### Q: what tomato pairings are plausible but uncommon?
```
Scout / experimental (plausible but uncommon — NOT classic):
  - rye_crumbs + tomato: rye crumbs: carrier + crunch; Nordic-available; plausible with roasted tomato
  - smoked_yogurt + tomato: smoked yogurt: fat + smoke + acid; plausible with charred tomato
  - lingonberry_vinegar + tomato: lingonberry vinegar: acid + berry brightness; experimental
  - sumac + tomato: sumac: tangy acid + umami; plausible with charred tomato
  - brown_butter + tomato: brown butter: nutty fat; plausible cutting concentrated tomato
  - walnut + tomato: walnut: crunch + fat; plausible with dried tomato
  - orange_zest + tomato: orange zest: aromatic acid; experimental with roasted tomato
  - miso + tomato: miso: umami; plausible enriching tomato sauce
  - fennel_pollen + tomato: fennel pollen: herbal aromatic; rare, experimental with roasted tomato
  (These are speculative — labelled so no one pretends they're tradition.)
```

### `foodprep scout roast`
```
Scout / experimental (plausible but uncommon — NOT classic):
  - rye_crumbs + roast: rye crumbs: carrier + crunch; Nordic-available; plausible with roasted tomato
  - lingonberry_vinegar + roast: lingonberry vinegar: acid + berry brightness; experimental
  - orange_zest + roast: orange zest: aromatic acid; experimental with roasted tomato
  - fennel_pollen + roast: fennel pollen: herbal aromatic; rare, experimental with roasted tomato
  (These are speculative — labelled so no one pretends they're tradition.)
```
**Mark:** useful — experimental pairings labelled 'NOT classic'; Nordic scouts (rye crumbs, lingonberry vinegar) present; no pretending they are tradition.

## Onion — second ingredient (schema stress test)

Proves the loader is ingredient-agnostic (no tomato special-casing). Onion transformations informed by CulinaryDB co-occurrence (garlic, tomato, butter, parsley, cilantro, vinegar, thyme, beef, potato, beans, bread, cheese).

### Q: what can I do with onion?
```
What you can do with onion (top branches by confidence + reuse):
caramelize
  → caramelized_onion_component
  → Deeply sweet, jammy, browned · Jammy, soft, collapsed
  → missing: salt, acid, herb, carb, protein, hydration
  → add: salt: sea_salt · carb: bread · protein: parmesan, grilled_fish · hydration: stock · herb: thyme · acid: vinegar
  → use in: braise, pizza, sandwich, soup, stew, toast

saute
  → sauteed_onion_component
  → Sweetened, softened, aromatic · Soft, translucent
  → missing: fat, salt, aromatic, herb, carb
  → add: salt: sea_salt · carb: rice · herb: thyme · fat: butter, olive_oil · aromatic: garlic
  → use in: beans, braise, rice, smoky_sauce, soup, stew

raw_assemble
  → raw_onion_component
  → Sharp, pungent, crisp · Crisp, crunchy
  → missing: salt, acid, fat, herb, crunch
  → add: crunch: cucumber · salt: sea_salt · fat: olive_oil · acid: vinegar · herb: parsley, cilantro
  → use in: dip, salad, salsa, sandwich, taco

pickle
  → pickled_onion_component
  → Sharp, sweet-sour, bright · Crisp-pickled
  → missing: mild_base, fat, protein
  → add: mild_base: potato, white_beans · fat: soft_cheese · protein: (no curated filler)
  → use in: cheese_board, salad, sandwich, taco

(4 onion transformations total — ask 'what is missing from <technique> onion' for detail, or 'what can I do with <component>' for an after-state.)
```

### Q: I caramelized onions, now what?
```
After caramelize you have caramelized_onion_component (confidence high).
caramelize
  → caramelized_onion_component
  → Deeply sweet, jammy, browned · Jammy, soft, collapsed
  → missing: salt, acid, herb, carb, protein, hydration
  → add: acid: vinegar · salt: sea_salt · hydration: stock · carb: bread · herb: thyme · protein: parmesan, grilled_fish
  → use in: braise, pizza, sandwich, soup, stew, toast
```

### Q: what can I do with caramelized_onion_component?
```
caramelized_onion_component (a reusable component)
  made by: caramelize (confidence high)
  tastes/feels: Deeply sweet, jammy, browned · Jammy, soft, collapsed
  use it in: braise, pizza, sandwich, soup, stew, toast
  if building a meal on it, still missing: salt, acid, herb, carb, protein, hydration
  add: salt: sea_salt · carb: bread · acid: vinegar · protein: parmesan, grilled_fish · hydration: stock · herb: thyme
```

## SQL integrity (post-patch)

All clean: every transformation has missing roles, every pairing has a role, every component has uses, every transformation has tags and evidence, no orphan pairings. (See `tests/test_query.py::test_no_ontology_rot`.)

## Round 3 — profiles split, ingredient kind, potato, honesty, corpus backfill

Round 3 generalises the engine beyond tomato+onion. Changes evaluated here:
- `component_profiles.yaml` as a separate file with a richer schema
  (provides / texture / missing_risks / heaviness_score / dryness_score; 21 profiles)
- ingredient `kind` guardrail: `full` (tomato, onion) / `filler` / `both` (potato)
- **potato** as the third full ingredient (9 transformations + ~46 pairings)
- meal-repair honesty: admits unknown plate items instead of silently ignoring them
- CulinaryDB corpus backfill via `foodprep backfill <dir>`: co-occurrence evidence
  attached to pairings; curated confidence and `curated_role_fit` left untouched

### Q: what can I do with potatoes?
`useful` — full product shape for a third ingredient; no tomato leak.

    What you can do with potato (top branches by confidence + reuse):
    roast
      -> roasted_potato_component
      -> Savory, browned, concentrated . Crisp outside, fluffy inside
      -> missing: acid, hydration, herb, protein
      -> add: protein: eggs . acid: lemon . herb: rosemary . hydration: stock
      -> use in: bowl, eggs, hash, salad
    ...
    (9 potato transformations total)

### Q: I mashed potatoes, now what?
`useful` — next-intent now detects the new potato techniques
(boil/mash/fry/gratin/bake/hash). Mash correctly wants acid/crunch/
freshness(herb)/protein, NOT more fat (mash already provides cream -> fat).

    After mash you have mashed_potato_component (confidence high).
    mash
      -> mashed_potato_component
      -> missing: acid, crunch, herb, protein
      -> add: protein: eggs, soft_cheese . crunch: croutons . herb: dill . acid: lemon, mustard

### Q: I have roasted potatoes and tomato sauce. What is missing?
`useful` — cross-ingredient plate reasoning (potato + tomato). Roasted potato
gives carb/umami, sauce gives acid/umami/body/hydration; still missing
salt/fat/herb/crunch/protein.

    You have: roasted_potato, tomato_sauce
      provided roles: acid, body, carb, hydration, umami
      missing for a balanced plate: salt, fat, herb, crunch, protein
      add: ...

### Q: I have boiled potatoes and onion. What is missing?
`actually surprising` — honest about the limits of the profile set: onion has
no component_profile (it is an aromatic, not a plate item), so the engine says
so explicitly instead of guessing.

    You have: boiled_potatoes
      no profile for: onion - add a component_profiles entry so I can reason about these.
      provided roles: carb, mild_base
      missing for a balanced plate: salt, fat, acid, herb, crunch, protein

### Q: I have potato gratin and it is too heavy. What lightens it?
`useful` — lighten path triggers on "too heavy"; recommends acid/herb/crunch and
warns against more fat/body/cream.

### Corpus backfill (CulinaryDB, 45,773 recipes)
`useful` — `foodprep backfill F:/download/google/CulinaryDB` attached evidence to
122 of 144 pairings (22 unresolved names like olive_oil / pasta_water, honestly
0). Top co-occurrence: garlic + onion = 8114 recipes — the exact case the user
flagged: huge co-occurrence does NOT mean garlic fixes every onion state.
Curated confidence and `curated_role_fit` are untouched: corpus is evidence, not
truth. Two pairings carry a `curated_role_fit` note demonstrating the guardrail
field is real and populated.

## Tests
42 passing (was 29): +5 potato, +4 meal-repair honesty/combos, +4 corpus
backfill. `test_no_ontology_rot` extended to assert the ingredient `kind`
guardrail (full + filler present).
