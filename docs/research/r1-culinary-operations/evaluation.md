# Evaluation: results, limitations and recommendation

Software tests pass (`tests/test_operations.py` and the full suite). That shows
the model is consistent. **It says nothing about culinary usefulness.** No
experiment has been cooked yet.

## How the model was corrected along the way

The generator's output was read after every run, and the model was fixed when
it produced nonsense. These are negative findings about the first version of
the model, and the rule that now prevents each:

| Nonsense produced | Cause | Fix |
| --- | --- | --- |
| 36,995 distinct materials for broccoli | thirteen interchangeable cuts × repeated cooking × finishing steps | one cut and one primary cooking per path; equivalent cuts merge |
| "Purée → crunchy contrast" | purées kept their raw firmness | purée, blend, mash and pound set firmness and thinness |
| "Roasted leaves → wrapper" | roasted and fried pieces stayed pliable | crisp material is no longer flexible |
| "Chopped avocado → sieve → seasoning powder" | sifting accepted wet material | sifting refines dry powders only |
| Liquids "pushed through a sieve with a ladle" | fouler had no solid requirement | fouler needs a moist solid |
| Gels salted and drained; gels steeped | operations meant for plant tissue accepted gels | salting, pressing and infusing need tissue |
| Infusions of watery courgette and fatty avocado ranked top | infusing had no flavour-transfer condition | infusing needs dry or aromatic, lean material |
| "Cut into ribbons, then peel the ribbons" | separation accepted cut material | peel and hollow before cutting |
| "Fry, then bread" as the canonical avocado fries | coating accepted cooked material | coat before cooking |
| A peel from stir-fried stems cooked again | fractions forgot their parent's state | fractions inherit processing state |
| 31 operations on tomato core | the engine ignored the curated `only_techniques` | the curated restriction is honoured (2 operations) |
| Thin watery pieces could not be fried | the family generator's frying rule | thin pieces waive the water rule |
| Ripe avocado "braised", "confited", "simmered" | no heat sensitivity | `heat_sensitive` blocks long heat |
| "Roast → marinate" outranked "roast" | extra steps were never questioned | the last step must add a function to be ranked |

**What the log shows:** the operation definitions themselves were mostly
right. The errors were in **state propagation**: what an operation does to
firmness, flexibility, moisture, thinness and state flags. A material model
lives or dies on those updates.

## Answers to the research questions

**1. Can operations be represented independently of ingredients?** Yes.

- 95 operations are defined once, with input requirements, outputs and
  property changes.
- They apply to 13 parts of 5 ingredients without one ingredient-specific
  rule, apart from three curated exceptions inherited from the family
  generator: no steaming tomato skin, no stir-frying or simmering avocado.
- Separations draw on part data (`outer_layer`, `seed_core`), not on the
  operation.

**2. Which properties are enough to decide applicability?** For this catalogue
and this set:

- composition: water, fibre, toughness, firmness, fat, sugar, acidity,
  bitterness, umami, starch, pectin;
- geometry: shape, piece, thin, flexible, sheetable, leafy;
- structure: outer layer, seed core;
- processing state: cooked, blanched, crisp, smooth, gelled, coated, cut;
- edibility and heat sensitivity.

No step was ever blocked as *unknown*, because every property asked about is
stated for all 13 parts. That shows the set is complete for these materials,
not in general.

**3. Which properties are missing?** Each was found from a wrong or missing
result:

- **Ripeness:** avocado pickling depends on it (A-1).
- **Stringiness or chewiness of fibre:** stem peel frying (B-5) and courgette
  core (Z-3) turn on it.
- **Slime or mucilage:** the courgette core.
- **Heat-generated bitterness** beyond the one flag.
- **Aroma volatility:** infusions are now gated on "dry or lean" as a proxy.
- **Emulsion stabilisers:** pectin is a waiver now; proteins and mustard are
  absent.
- **Sensory change from heat:** browning and smoke are flavour, not function
  (see question 9).

**4. Can the existing architecture represent intermediate materials and
branches?** Yes, without a new graph:

- `input_component` already chains states;
- `byproducts` already gives one step several outputs;
- the generator is a runtime analogue, so nothing speculative enters
  tomato.yaml.

Promoting a tested sequence means writing it as curated transformations with
those two fields. Unchanged: the family generator reads the same rules from
operations.yaml and gives identical output for broccoli, tomato and avocado
(2,236 ideas, checked).

**5. Which operations produce the most diverse useful materials?** Counted by
distinct function sets among ranked sequences (`results.md`):

| Rank | Operation | distinct function sets |
| ---: | --- | ---: |
| 1 | émincer | 229 |
| 2 | blanchir | 180 |
| 3 | acidifier | 161 |
| 4 | fermenter | 159 |
| 5 | enrober | 156 |
| 6 | éplucher | 144 |

- Thin slicing, blanching and acid treatments open the most doors.
- Peeling matters because it creates a second material.
- Pressing and salt-and-drain are the most productive per use: one step, two
  useful outputs (juice and pulp; drained pieces and vegetable water).

**6. Can sequences generate meaningful possibilities without recipe data?**
Partly.

- **Yes:** every one of the brief's example sequences is generated. So are
  the established zero-waste preparations: pulp crackers, peel crisps, tomato
  skin powder, courgette water, broccoli leaf chips, stem noodles.
- **Also yes:** it generates the open ones the web check could not find: stem
  peel powder, courgette skin ribbons, courgette water reduction.
- **But** it generates them among thousands of variants (question 9).

**7. Which generated possibilities are established practice?** From the web
check (`sources.md`):

| Status | Preparations |
| --- | --- |
| Established | stem noodles, pickled stems, green purée, pulp crackers, carrot ribbons, carrot-top pesto, carrot juice glaze, salted courgette, zoodles, courgette chips, tomato consommé, scrap stock, avocado emulsion-purée, pickled firm avocado, grilled avocado, avocado fries |
| Niche | broccoli leaf chips, fermented stems, carrot peel crisps and powder, courgette water, tomato skin powder and crisps, tomato-seed vinaigrettes |

Only tomato skin powder is labelled *established path* by the model, because
`established_on` records documentation per operation and material, not per
combination. The web check is the better judge of established practice.

**8. Which remain interesting experimental hypotheses?**

- **No evidence found:** broccoli stem peel powder (B-1); courgette skin
  ribbons as a component (Z-1).
- **Steps not found:** courgette water reduced (Z-2); pickled ribbons of
  peeled stem (B-2); broccoli leaves as wraps (B-3); pulp sheets without a
  binder (C-1); tomato gel as the whole acid of a vinaigrette (T-3); tomato
  gel against browning (A-4).
- **Tests of model rules:** ripeness (A-1); heat sensitivity (A-2).
- **Expected failures, worth confirming:** courgette core thickener (Z-3);
  fried stem peel (B-5).

**9. Useful results or combinatorial noise?** Both, and the split is clear:

- **Enumeration and explanation are useful.** Applicability with reasons,
  multi-output separations and the branches are the strongest part. They
  found every established preparation and the open ideas.
- **Ranking is the weak part.**
  - The top of each list favours multi-purpose processed materials: crumbs,
    powders, broths.
  - Established, delicious preparations rank low: the carrot juice glaze is
    2,958th of 3,912.
  - Some are not ranked at all: grilled avocado, sautéed courgette skin.
  - **Reason:** the function vocabulary describes what a material is *for*
    structurally. It cannot see a preparation that does the same job
    *better*, or one that changes flavour (browning, smoke).
- **The ranking also over-rewards discarded parts** (halved, still visible)
  **and step counts.** Thousands of ranked sequences per ingredient is not a
  list a cook would read.
- **Verdict:** a candidate generator with good explanations, not yet a
  recommender. The weights were never fitted to anything, by design (no
  machine learning this round).

**10. What should be tested physically before expanding?** The experiments in
`experiments.md`, in this order:

1. **The open, cheap ones:** B-1, Z-1, Z-2, B-3. Each answers whether the
   model found something genuinely new.
2. **The model-rule tests:** A-1, A-2, B-5, Z-3. Each confirms or refutes a
   property the model has or lacks.
3. **The ranking controls:** C-2 (glaze), T-1 (skin powder). If the low-ranked
   control tastes better than the top-ranked crumbs, the ranking needs a
   sensory term before anything else.

## Limitations

- **Property values are judgement.** `part_properties.yaml` is curated by the
  author, not measured. "Firmness high" for broccoli stems is a reasonable
  reading, not a datum.
- **Levels are coarse.** Five levels cannot tell a crisp carrot from a
  slightly floppy one; real cooking depends on that.
- **Operation details are simplified.** Time, temperature and salt percentage
  are text (`parameters`), not modelled. "Dry" is one operation whether 2 h or
  12 h.
- **No interaction between materials.** Composites only record added
  ingredients. A-4 combines two materials outside the generator.
- **False novelty from English-only search** (found 2026-11-24). Z-1 was
  "no evidence found" in English but is a documented Portuguese preparation
  (*esparguete verde*). Every "no evidence found" here is provisional until
  searched in other culinary languages.
- **"Established path" overstates.** The label means every operation is
  documented on the starting material, not that the whole sequence is a
  documented preparation. The term should be refined (raised in the PR #5
  review).
- **No recombination.** The engine branches materials but cannot put
  processed materials back together: stuffed courgette, peel cake, farces,
  fritters. Two of the four Portuguese preparations need it (`benchmark.md`).
- **Sources.**
  - Reference works are cited as where a definition is standard, without page
    numbers.
  - Web checks relied mostly on search snippets.
  - "No evidence found" means two searches found nothing, not that nobody has
    done it.
- **Five ingredients.** The model's generality beyond them is untested.

## Recommendation

**Develop further, with changes to the underlying model before expanding.**

**Keep:**

- the operation catalogue;
- three-valued applicability with reasons;
- multi-output separations;
- bounded composition.

They work, they integrate with the existing architecture without
duplication, and they found every established preparation plus a handful of
open ones.

**Change before adding ingredients:**

1. Run the experiments first. Two or three tasting results will say more
   about ranking than any further rule.
2. Add the missing properties the experiments are designed to confirm:
   ripeness, stringiness, mucilage.
3. Give ranking a sensory term: browning, smoke and concentration as flavour
   value, so a better version of the same function can outrank a new but dull
   one. Candidates for the term are the existing flavour dimensions.
4. Present a short list per part, at most a few per function, instead of
   thousands of ranked paths.

**Do not:** add ingredients, deepen the search beyond 3, or tune weights
without tasting data. Each would grow the list without making it more useful.
