# ADR 0002: Ingredients are decomposed into parts before they are processed

- Status: Accepted
- Date: 2026-11-24

## Context

The model so far treats each ingredient as one whole thing that a technique
turns into a state: tomato, roast, roasted tomato. Real ingredients hold
several different things:

- Broccoli has florets, stems and leaves. They want different cuts and
  different heat, and they end up in different dishes.
- A tomato has skin, seeds and gel, and flesh.
- An avocado has flesh that carries fat, plus a skin and a stone that are
  not food.

Until now, parts reached the model only indirectly:

- as cutting steps (`peel`, `deseed`) that discarded what they removed;
- as by-products of one step (tomato water, milk solids);
- in free-text descriptions ("tender stems").

So the model could not say what to do with broccoli stems. It could not say
that tomato skin is worth keeping. Nor could it say that avocado skin is not
food.

## Decision

The core chain becomes:

```
ingredient → decomposition → processing → use as food
```

- **Decomposition.** An ingredient has *parts*: things you can physically
  separate in a kitchen. Each part records:
  - whether it is food (`yes`, `conditional` or `no`, with a reason);
  - the prep step that separates it (`trim`, `peel`, `deseed`, `stone`);
  - the roles it provides. Avocado's fat is what the *flesh* provides; it is
    not a separate object.
- **Processing.** A transformation may name the part it acts on. Stir-fried
  broccoli stems and roasted florets are different transformations of the
  same ingredient. A transformation with no part acts on the whole
  ingredient, which keeps every existing record valid.
- **Use as food.** This is unchanged. Each output component carries its dish
  contexts, missing roles and pairings, so a part's possibilities are the
  uses of everything its transformations produce.
- **Cut forms** (slices, dice, matchsticks) are not parts. They stay as prep
  modifiers that change how a part behaves, not what it is.

## Consequences

- New `ingredient_parts` table and a nullable `transformations.part_id`. The
  unique step now includes the part, so florets and stems can both be
  stir-fried.
- The loader rejects:
  - a transformation whose part belongs to another ingredient;
  - processing a part that is not food;
  - a part separated by a step that is not a prep modifier.
- `foodprep parts <ingredient>` shows the decomposition and each part's
  paths to food.
- Parts are added one ingredient at a time. Broccoli, tomato and avocado are
  first; the other ingredients keep working as whole-ingredient paths.
- R1's pairing and Scout data are unchanged. Later, pairings can be recorded
  per part (lemon on tomato flesh), which is finer evidence for a future
  round.
