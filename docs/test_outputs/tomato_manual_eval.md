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

---

# Round 4 — Plate Balance Engine (Cook mode)

## Goal
A component-level meal-repair engine: given a set of plate items (component
profiles and/or raw ingredients), aggregate what the plate provides, what it
risks lacking, and suggest missing-role fillers. Kept separate from Scout mode.
No large new ingredient tree added (per the user's constraint).

## What it does
`query.plate_balance(conn, text)` (exposed as `foodprep plate "<items>"` and
routed from `answer()` on `"balance"` / `"plate of"` / `"plate balance"` /
`"<items> ... what is missing?"`):

- **Recognise each item** via `_recognise_plate_item` — three kinds:
  - `profile` — matches a `component_profiles` entry (longest term wins; the
    `_component` / `_base` suffix is stripped so `roasted_tomato_component`
    maps to `roasted_tomato`).
  - `ingredient` — matches a raw ingredient by name/alias (`_match_ingredient`),
    contributes its `base_roles`.
  - `unknown` — neither; reported honestly with `"no profile for: X — unknown
    item; add a component_profiles entry"`.
- **Aggregate provided roles** — union of profile `provides` and ingredient
  `base_roles`, run through `_canon_role` (ROLE_CANON + a small
  `MISSING_TERM_TO_ROLE` map: sauce→hydration, fresh_side/freshness→herb).
- **Aggregate missing_risks** — union of profile `missing_risks`, canonicalised.
- **Plate-level heaviness / dryness** — mean of profile `heaviness_score` /
  `dryness_score`, with qualitative reads (`_heaviness_label`:
  heavy/rich/balanced/light; `_dryness_label`: dry/medium/moist) and lean
  warnings when h_avg≥4 / d_avg≥3.5.
- **Two-tier missing logic** — the key distinction:
  - `target_gap` = `TARGET_ROLES - provided` → "missing for a balanced plate:"
    (hard gaps — fillers grouped by role, Cook mode excludes experimental).
  - `flagged_more` = `risk_roles - target_gap` → "also flagged by item profiles
    (may want more):" (roles the plate *provides* but a profile still flags —
    e.g. roasted_tomato provides acid yet lists acid as a risk: "provides some,
    may need more"). This stops the engine from telling you to "add protein" to
    a gratin that already provides protein.
- **Cook vs Scout separation** — `plate_balance` is labelled "Cook mode" and
  `_fillers_for_role(..., include_experimental=False)` excludes experimental
  pairings (rye_crumbs absent). Scout (`query.scout`) stays labelled "Scout /
  experimental" and surfaces them. Verified by `test_cook_and_scout_are_separate`.

## Honesty
- Unknown items are named, not guessed (`test_plate_balance_unknown_component_warns`).
- Known-but-profile-less ingredients (onion) are recognised as ingredients with
  base-role contributions AND warned for lacking balance data — softer than
  "unknown", still honest (`test_plate_balance_ingredient_input`). The round-3
  honesty test was updated from "unknown" to "(ingredient)" to match.
- Empty plate input ("what is missing?" with no items) returns "Name the plate
  items..." rather than guessing (`test_plate_balance_empty_input_prompts_for_items`).

## Tests
52 passing (was 42). +11 plate-balance: known profiles, ingredient input,
component-name input, unknown-component warn, `balance` trigger routing,
flagged-more vs hard-gap separation, heaviness/dryness reads, Cook excludes
experimental, Cook/Scout separation, empty-input prompt.

## Notes
- Routing for `answer()` tightened so bare "plate" does not false-trigger on
  incidental "on a plate" — only `balance` / `plate of` / `plate balance` /
  missing+≥2-items route to `plate_balance`. `meal_repair` remains as a
  backward-compat wrapper to `plate_balance`.
- No new ingredient tree added (round-4 constraint honoured). The engine reuses
  existing profiles and ingredient base_roles.

---

# Round 5 — Filler pack + architecture checkpoint

## Checkpoint
`docs/ARCHITECTURE_CHECKPOINT_ROUND_4.md` freezes the mental model before the
filler pack: full / filler / both ingredient, component profile, transformation,
missing role, target_gap, flagged_more, Cook / Scout mode, plate balance, corpus
evidence, curated_role_fit. The one line it exists to protect:

> Co-occurrence can support evidence, but `curated_role_fit` owns the culinary
> role.

## Goal
Strengthen the plate engine with a rich filler pack rather than a new ingredient
tree. Each filler answers five questions: roles / repairs / avoid_when / Finnish
supermarket availability / Cook-or-Scout.

## What was done
- **Two new filler fields** — `repairs` and `avoid_when` — added to the
  `ingredients` table (nullable TEXT, newline-joined plate-condition tags) and
  the loader. These are **per-filler profile data**, surfaced via
  `filler_profile`. They are deliberately NOT wired into `plate_balance` as a
  plate-condition matcher — that would be exactly the half-built condition
  layer the checkpoint warns against. The plate engine still reasons from
  roles + pairings; the pack helps by adding `base_roles` + Cook pairings for
  the new fillers so they enter the suggestion pool.
- **12 fillers enriched**: lemon, vinegar, mustard, yogurt, cream, butter,
  pickles, soy_sauce, rye_crumbs (all existed) + sauerkraut, fresh_herbs, chili
  (genuinely new). Each carries `repairs` + `avoid_when` + Finnish availability.
- **Alias reconciliation (anti-hedgerow)**: `pickled_cucumber` and
  `rye_breadcrumbs` are name variants of existing fillers — added as aliases to
  `pickles` and `rye_crumbs` rather than duplicate canonicals. `sauerkraut` gets
  the alias `hapankaali`.
- **Cook pairings added** for sauerkraut / fresh_herbs / chili / pickles /
  rye_crumbs so the plate engine can suggest them. rye_crumbs is now Cook for
  potato (gratin/soup crunch) AND Scout for roasted tomato (experimental) — the
  nuance its profile surfaces.
- **`query.filler_profile(conn, name)`** — renders the five-question profile.
  Cook/Scout is *derived* from the filler's pairings: any non-experimental →
  Cook; experimental-only → Scout; both → "Cook (also has N Scout pairings)".
- **Routing**: `answer()` now routes filler-subject prompts ("what can I do
  with lemon", "what does mustard repair", "tell me about sauerkraut") to
  `filler_profile` instead of falling through to tomato branches. Full/both
  ingredients (tomato/onion/potato) keep their branch view — gated by
  `_has_transformations`.
- **CLI**: `foodprep filler <name>` (+ `cmd_filler`).

## Honesty / guardrail alignment
- No role was invented for "freshness" (the user's example used it loosely) —
  freshness is delivered by acid or herb in context; `MISSING_TERM_TO_ROLE`
  already maps the cook-term. No new role = no hedgerow.
- `repairs` / `avoid_when` are free-form plate-condition tags (heavy, fatty,
  already_high_acid, dairy_long_cook, …) — a distinct vocabulary from roles,
  kept out of the role engine.
- The two round-4 Cook/Scout tests were updated: rye_crumbs is no longer
  experimental-only (it's Cook for potato now), so the demonstration of
  "Cook excludes experimental" moved to `lingonberry_vinegar` (experimental-only
  acid filler — in Scout, never in Cook).

## Tests
61 passing (was 52). +9 round-5: filler pack loads with repairs/avoid_when;
alias reconciliation (no duplicate canonicals); filler_profile answers the
five questions; alias input resolves; Scout-only filler labelled; filler
subject routes to profile not tomato branches; full ingredient keeps branches;
new fillers are Cook-suggestable (in the pool); round-5 ontology-rot guard
(pairings still have roles, transformations still 25).


## Round 6 — cabbage (fourth full ingredient) + risks guardrail

Cabbage is the stress-test ingredient the user picked: cheap, everyday, and
capable of many food states (raw / salted / fried / roasted / braised / soup /
pickled / fermented). It is `kind: full` with its own technique tree, the
fourth full ingredient after tomato / onion / potato. The point is that one
boring ingredient yields eight different *after-states* with eight different
missing-role sets — exactly what the transformation record is for.

### What was added
- **Schema**: `transformations.risks TEXT` — newline-separated caveats
  (`harsh_when_raw`, `sulfurous_if_overcooked`, …). Loader reads it;
  `branch_detail` / `render_branch` / `component_first` surface a `→ risks:`
  line. This is the home for the cabbage sulfur/harshness concept.
- **Data** (`tomato.yaml`): `cabbage` ingredient (`kind: full`, FI
  very_common); 8 components (raw/salted/stir-fried/roasted/braised/soup/
  pickled/fermented); 8 transformations each carrying `flavour_shift`,
  `texture_shift`, `tags_after`, `risks`, `missing_roles`, `uses`, `evidence`,
  `confidence`; `sulfurous` + `vegetal` flavour tags and a `slaw` dish context.
- **Pairings**: ~45 Cook pairings across all 8 cabbage transformations
  (every declared missing role has at least one Cook filler — verified no
  "(no curated filler)" gaps) + 3 experimental/Scout pairings
  (lingonberry_vinegar+raw_slaw, rye_crumbs+roast, smoked_yogurt+soup) so
  `scout cabbage` returns something.
- **Component profiles** (`component_profiles.yaml`): 8 cabbage plate items
  (cabbage_slaw / salted_cabbage / fried_cabbage / braised_cabbage /
  roasted_cabbage / cabbage_soup / fermented_cabbage / pickled_cabbage) with
  provides / flavour / texture / missing_risks / heaviness / dryness.
- **Query**: cabbage technique detection patterns (`slaw`, `stir[- ]?fr…`,
  `brais…`, `ferment…`) added — `ferment` deliberately does *not* match
  "sauerkraut" so "what is missing from sauerkraut" still routes to the
  sauerkraut *filler profile*, not the cabbage tree. `scout()` gained an
  optional `ingredient` filter and is routed for `scout <ingredient>`.

### The guardrail (the whole point of the round)
Sulfur/harshness is modelled as **flavour tags + transformation risks**,
never as a role:

- `tags_after: flavour: [sulfurous, sweet, vegetal]`
- `risks: [harsh_when_raw, sulfurous_if_overcooked]`
- `missing_roles` stays clean: `acid / fat / salt / herb / protein / carb /
  body / mild_base / cream / crunch`. No `freshness` role (per the round-4
  checkpoint — freshness is delivered by herb/acid in context, not a bucket).

Two tests defend this: `test_cabbage_sulfur_is_not_a_role` asserts no role
name encodes sulfur/harsh/freshness/pungent; `test_cabbage_sulfur_lives_in_tags_and_risks`
asserts the `sulfurous` tag exists, raw_slaw carries `harsh_when_raw`, and a
heat transformation carries `sulfurous_if_overcooked`. This stops a future
contributor from "fixing" cabbage by inventing a `sulfur` role — exactly the
hedgerow the checkpoint warns against.

### Cook vs Scout separation
- Cook: all ~45 non-experimental cabbage pairings — suggested by `branch` /
  `plate_balance` in Cook mode.
- Scout: the 3 experimental pairings — surfaced by `scout cabbage` (and the
  routed `scout cabbage` answer), labelled "plausible but uncommon — NOT
  classic".
- sauerkraut (round-5 filler) stays `kind: filler`; cabbage-the-ingredient
  owns the `ferment` tree. The two coexist cleanly.

### Tests
68 passing (was 61). +7 round-6: cabbage is `full`; all 8 techniques load; every
transformation has ≥1 missing role; sulfur is not a role; sulfur lives in
tags+risks; Cook/Scout pairings split correctly (via the
works_best_with_transformation_id FK, since `pairings.ingredient_id` is the
filler not the target); branch view renders the risks line. `test_schema_populated`
and `test_no_ontology_rot` updated to 33 transformations (12+4+9+8).


## Round 7 — Streamlit slice (handles on the engine, no new ontology)

MVP-2 is now presentable. Round 7 added no ingredient, no corpus work, no new
roles — just handles on the engine so a human can walk the graph. The UI is 5
tabs that map 1:1 to the existing query API, rendered as cards + chips (not
tables), with a debug expander per card.

### Files
- `src/foodprep/ui/streamlit_app.py` — the app (5 tabs).
- `src/foodprep/ui/design.css` — card/chip design system (adapted from the
  parcel-ops Control Tower language: eyebrows, mono labels, accent-bordered
  cards, tabular nums, Streamlit chrome overrides).
- `app.py` — root launcher so `streamlit run app.py` works from the repo root.
- `.streamlit/config.toml` — headless + warm-paper theme + port 8501.

### The five tabs
1. **Ingredient Explorer** — selectbox of the 4 tree ingredients
   (tomato/onion/potato/cabbage); mode = best branches | choose technique;
   each branch is a card with Tags / Risks / Missing / Try (fillers grouped by
   the role they fill) / Use in. Risks show visibly, **never** as missing roles.
2. **Component Explorer** — pick an after-state component; shows what produced
   it (`cabbage + roast`), storage, tags, risks, may-need, next-move fillers,
   uses. Proves the stateful entry point (you don't always start from raw).
3. **Plate Balance** — multiselect plate items; KPIs (items / hard gaps /
   may-want-more / heaviness) then sections: Already provides / Missing hard
   gaps + suggested fillers / May want more / Risks / Avoid adding more of /
   No balance profile for. The best demo tab.
4. **Filler Profiles** — the PIM tab: roles / repairs / avoid_when / FI
   availability / Cook-or-Scout mode / pairings for any ingredient.
5. **Scout** — experimental pairings only, filtered by ingredient, each a
   purple-bordered card with the disclaimer: "These are role-compatible but
   uncommon or experimental. Taste a small amount before serving."

### Engine handles added to `query.py` (read-only, no ontology change)
`tree_ingredients`, `techniques_for_ingredient`, `branch_card`,
`all_branch_cards`, `component_card`, `components_list`, `profiles_list`,
`ingredients_list`, `plate_balance_detail`, `filler_profile_detail`,
`scout_rows`, `_transformation_tags`. The three big string renders
(`plate_balance`, `filler_profile`, `scout`) were refactored to compute a
structured dict first, then render — so the UI and the string CLI share one
truth and the acceptance tests target the dicts.

### Guardrail improvement that fell out of the UI work
`fillers_for_transformation` / `fillers_by_role` now default to **Cook mode**
(exclude `experimental`), with `include_experimental=False`. Previously the
branch view's "Try" line listed *all* pairings for a transformation, which
let a Scout-only filler (`lingonberry_vinegar` for raw_slaw acid) leak into
the Cook branch view. Now the branch/component Cook views are clean of
Scout-only suggestions; experimental pairings live only in the Scout tab
(via `scout_rows`). This tightens the Cook/Scout separation the round-4
checkpoint demands. The existing `plate_balance` Cook path already excluded
experimental (`_fillers_for_role`), so behaviour there is unchanged.

### Smoke verification
`streamlit run app.py` boots headless, serves HTTP 200, and the
`/_stcore/health` endpoint reports `ok`. Importing the module executes all 5
tab bodies against a freshly-built in-memory DB without error (benign
"missing ScriptRunContext" warnings only).

### Tests
76 passing (was 68). +8 round-7 acceptance tests (`tests/test_ui_handles.py`),
all query-level (no Selenium/browser): ingredient list includes the 4 trees;
cabbage techniques = the 8; cabbage branch cards carry risks (raw_slaw →
harsh_when_raw, roast → sulfurous_if_overcooked); component_card resolves
roasted_tomato_component (and braised_cabbage_component risks); plate balance
returns missing roles for mashed_potatoes + roasted_chickpea_patty
(acid/herb/crunch hard gaps with Cook fillers); filler_profile_detail
resolves sauerkraut as `kind: filler` (not cabbage ferment) while cabbage is
`full`; scout cabbage returns exactly the 3 experimental pairings; Cook mode
excludes Scout-only pairings from both plate_balance and the cabbage branch
Cook view.
