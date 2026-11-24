# Composition: operation sequences and generation rules

Code: `foodprep.operations.explore` and `ranked`. Try it:
`foodprep explore courgette --top 8`.

## How a sequence is built

A **material** is a part plus what has been done to it (`model-design.md`). A
step takes one material and one operation:

1. The operation must be **applicable or conditional** for the material.
   Unknown, inapplicable and unsafe steps are never taken.
2. Applying it gives **one or more output materials** with updated properties:
   - `set`: assign values;
   - `raise` / `lower`: move a level;
   - `add_flavour`;
   - `when_set`: conditional sets, e.g. thin pieces crisp in the oven;
   - a separation draws a fraction's properties from the part's `outer_layer`
     or `seed_core`.
3. The output must **differ** from its input. Each output is then available as
   the input of the next step.

**Branching:** when an operation gives several outputs, every output is its
own branch. Each step records its siblings. Example:

```
broccoli stems → éplucher
  ├─ inner (peeled stem) → julienne → acidifier       crunchy pickled garnish
  └─ peel (fraction)     → déshydrater → moudre       seasoning or colouring powder
```

Both branches are generated and continue independently (tested in
`test_branches_continue_independently`).

## The brief's example sequences

All can be generated. Final functions as the model names them:

| Sequence | Start | Final functions |
| --- | --- | --- |
| peel → dry → grind | carrot root (peel branch) | seasoning powder, colouring, crisp, flavour concentrate, coating, thickener |
| peel → julienne → fry | carrot root (inner branch) | crisp component, garnish |
| grate → press → reduce | carrot root (juice branch) | flavour concentrate, colouring |
| blanch → purée → sieve | broccoli florets | sauce base |
| roast → crush → infuse | broccoli stems | broth base, aromatic infusion, flavour concentrate, colouring |
| press → filter → gel | tomato flesh (juice branch) | moisture carrier |
| slice → salt and drain → dry | courgette fruit | crisp component, flavour concentrate, crunchy contrast |

**"Peel → julienne → fry" needed a rule change.** The family generator's frying
rule (water ≤ medium) rejected thin watery pieces, though fried carrot
shoestrings and courgette chips are established. Thin pieces now waive the
water rule (`waived_when: [{coated: true}, {thin: true}]`).

## Rules that bound the search

All of these are in the data (operations.yaml) or the engine, and tested:

| Rule | Where | Why |
| --- | --- | --- |
| Depth at most 3 | `MAX_DEPTH` | The brief's bound |
| An operation once per path | engine | No loops |
| The output must change a property | engine | No null steps |
| One primary cooking per path; blanching does not count | `cooked: false` on 16 cooking operations | Steamed-then-roasted-then-fried is noise; blanch-then-roast stays allowed |
| One cut per path; brunoise may refine julienne | `cut: false` on 17 cuts, brunoise waived on julienne | Thirteen interchangeable cuts × two more steps was most of the noise |
| Peel and hollow before cutting; peel raw produce | `eplucher`, `evider` | "Cut into ribbons, then peel each ribbon" was being generated first |
| Coat before cooking | `enrober`, `paner` | "Fry, then bread" was generated as the canonical avocado fries |
| Exhausted outputs end a path | `terminal: true` on spent solids | Spent solids give nothing more |
| A fraction keeps its parent's processing state | `STATE_FLAGS` | A peel taken from blanched stems is blanched too |
| Equivalent materials merge | `Material.key()` | Same part, fraction, properties and added ingredients make the same material, whatever the path. The cut's name is left out: paysanne and thin slices that give the same piece merge |
| The easiest equivalent path is shown | `_cost`: steps, then effort, then conditions | Others are kept as `alternates` |

**Determinism:** operations and parts are visited in catalogue order, and
breadth-first, so the same data always gives the same materials in the same
order (tested).

## What the bounds achieved

From `results.md`:

| Ingredient | distinct materials | merged as equivalent | no culinary function | ranked |
| --- | ---: | ---: | ---: | ---: |
| broccoli | 17,532 | 16,384 | 5,223 | 5,090 |
| carrot | 11,963 | 12,283 | 3,064 | 3,912 |
| courgette | 7,530 | 7,799 | 2,679 | 1,926 |
| tomato | 6,117 | 5,097 | 1,436 | 1,933 |
| avocado | 573 | 654 | 296 | 115 |

The first unbounded run gave 36,995 distinct materials for broccoli alone.
The rules removed about half. What remains is still large: depth 3 over 82
operations is combinatorial even with sensible rules. That is why ranking, and
the requirement that each step add a function, matter more than further
pruning (see `evaluation.md`).

## Ranking

`operations.rank` gives transparent components and a weighted sum:

| Component | Meaning | Weight |
| --- | --- | --- |
| usefulness | distinct function groups (texture, structure, flavour, base; appearance at half), capped at 3, as 0..1 | 3, multiplied by plausibility |
| plausibility | 0.8 to the power of the number of conditional steps | — |
| difference | properties changed from the start, capped at 6, as 0..1 | 1 |
| utilisation | the start or the fraction is usually discarded | 0.5 |
| experimental value | usefulness × the share of steps not documented on this material | 0.5 |
| effort | summed operation effort ÷ 9 | −1 |
| equipment | items outside ordinary kitchen equipment | −0.5 each |

A sequence is **not ranked at all** in three cases:

- it has no culinary function;
- it ends in an exhausted output;
- its last step adds no function its input lacked. A longer path must earn
  its extra step, so "roast → marinate" does not outrank "roast".

Rarity is not a component. RecipeNLG plays no part.

**Evidence label:**

- **established path:** every step is documented on this material
  (`established_on`);
- **mechanistic inference:** otherwise.

Tomato skin powder is an established path; almost everything else is
inference. That is correct: the catalogue documents operations, not most of
their combinations.
