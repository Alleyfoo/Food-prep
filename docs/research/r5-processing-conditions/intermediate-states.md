# R5 intermediate states: "from this state, what next"

The second question of the round: given a state you already have, which
documented routes pass through an equivalent state, and what remains? The
generated detail is in `intermediate-tables.md`. This page says what the
query does and what it supports.

## How it works

`foodprep from <ingredient.part> <operations...>` builds the material you have
by applying the named R1 operations to the part with `operations.apply`,
keeping the main output, as a route keeps it. It then walks every R3 route
and R4 transfer the same way. A route matches where one of its materials
reaches a state with the same **R1 `Material.key()`**: same ingredient, part,
fraction, additions and properties. That is R1's existing equivalence; no new
matcher was written.

You can name the state in three ways:
- **operations**, for example `foodprep from rutabaga.root eplucher emincer blanchir`.
  This is exact equivalence. Grated and salted courgette meets
  kolokythokeftedes, but not mucver, whose courgette is squeezed unsalted.
- **flags**, for example `foodprep from chickpea.dried_seed soaked`. The first
  step at which the flag holds.
- **a step address**, for example `foodprep from falafel/raw_soaked/paste/1`.
  Use this for an assembly state, such as a rested falafel paste, which no
  part plus operations can name.

For each match it prints:
- the remaining steps of that route, **including the heat after the join**,
  each with its endpoint kind, time, kind of active work and done-when check;
- this member's own endpoint inside the assembly;
- the dependency that explains a remaining step ("why: ...");
- any finishing stage (the rest);
- the other members the joins still need;
- how long the state keeps and on what authority.

If the last step you did is a **readiness** step, it says so: "what you have
is a readiness state: ready for the next operation, not ready to eat".

```
foodprep from rutabaga.root eplucher emincer blanchir
  keeps: fridge, the whole assembled gratin, overnight before baking (cooking) [Q231]
  ...
  Potato and rutabaga gratin (transfer:rutabaga_gratin): rutabaga after 3 step(s); remaining:
    ! what you have is a readiness state: ready for the next operation, not ready to eat
    gratin 1 bake -> doneness  [conditions: bake_gratin]
      time: 55-60 min; 40-50 min; 60-80 min; active work: occasional
      rutabaga inside: done when some give, al dente ... ; no resistance, completely tender ...
    why: ... rutabaga is a very dense root and needs longer than potato ...
    then rest before cutting (a few minutes; 25 min; 1 h, held at 50 C)
    gratin also joins: potato, cream, milk, garlic, butter
```

## The 17 states recorded, and what keeps them

| State | Reached in | Keeps (best documented) | Authority? |
| --- | --- | --- | --- |
| soaked dried peas | pea falafel | not found; soak in the fridge over 4 h (NDSU) or 12 h (Colorado State) | yes, conflicting |
| soaked chickpeas | falafel | a 48 h fridge soak (one cook); fridge thresholds as above | partly |
| skinned black-eyed beans | akara, moi moi | frozen up to 6 months (cook) | no |
| soaked urad dal | medu vada | fridge if grinding is delayed, no time; batter 2-3 days (cooks) | no |
| rested falafel paste (step) | falafel | fridge 1-3 days, frozen 3-6 months (cooks); raw-component meals within 1 day (BfR) | general rule only |
| rested pea paste (step) | pea falafel | raw-component meals within 1 day (BfR) | general rule only |
| blanched rutabaga slices | rutabaga gratin | assembled gratin overnight (cook); frozen 10-12 months after a freezing blanch (Martat) | no |
| boiled whole potatoes | rosti, korokke, tikki | 1-2 days for rosti (cooks); cooked food 2-3 days (Martat, BfR); cool to +6 C within 4 h (Ruokavirasto) | general rule only |
| cooled boiled potatoes | rosti, tikki | 1-2 days (cooks); heated meals 2-3 days (BfR) | general rule only |
| simmered potato slices | gratin, simmered route | the next day (Q225), contradicted (Q235) | no |
| cooked rice | cabbage rolls, napa rolls, arancini | **fridge at most 24 h, cooled within 1 h, reheat once** (FSA, FSS, NHS); +6 C within 4 h (Ruokavirasto) | yes, conflicting |
| salted grated courgette | kolokythokeftedes | use at once (cooks); raw-component meals within 1 day (BfR) | general rule only |
| peeled grated broccoli stem | stem patties | cut vegetables are perishable, coldest part of the fridge (Ruokavirasto), no days | general rule only |
| blanched onion | onion vessel, farcis | chilled to the next day (one cook) | no |
| softened cabbage head | kaalikaaryleet | freeze the head instead of boiling it (Martat) | no |
| baked gratin (step) | gratin dauphinois | chilled overnight to cut (cooks); 2-3 days (Martat, BfR); do not freeze (cooks) | general rule |
| baked cabbage rolls (step) | kaalikaaryleet | with rice within 24 h, without 3 days, frozen 2-3 months (cook); casseroles frozen 1-3 months (Martat) | no |

## What this supports: cook now or prepare for tomorrow

Without any meal planning, the data can already answer the batch question
for these dishes:
- **Safe and documented to prepare the day before:**
  - boiled jacket potatoes for rosti (cooks call it decisive);
  - cooked rice for the rolls, within the UK's 24 h;
  - the assembled raw rutabaga gratin, kept overnight;
  - a baked gratin chilled to cut;
  - shaped raw falafel, 1 day, or frozen.
- **Documented as not keeping:**
  - salted courgette mixture (turns watery overnight);
  - simmered gratin slices (one source says never stop halfway).
- **Unknown:**
  - soaked pulses held after the soak;
  - blanched slices or leaves held unfrozen.

  The model says "not found" there rather than offering a time.

The Finnish authority (Ruokavirasto) gives cooling rules and temperatures on
every page read, but no day counts. Where a day count appears, it comes from
Martat (home economics), BfR, the UK bodies or cooks, and the data marks
which.
