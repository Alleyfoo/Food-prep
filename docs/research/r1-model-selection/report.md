# R1 report: statistical and machine-learning model selection

Method: [README.md](README.md). Numbers: `results/` (rerun with `run.py`).
Run on 2026-11-24 against CulinaryDB (45,772 recipes) and the ontology on main.

## Decision

| Task | Outcome | In one line |
| --- | --- | --- |
| **Pairing** | **B, then C** | Our functional representation adds clearly over recipe statistics, and tree ensembles add a further, meaningful improvement over the best statistical model. |
| **Scout** | **B, and D for machine learning** | Only functional knowledge works. Recipe statistics are close to useless, and no learner beats a plain role-similarity score. Too little independent evidence to train on. |

**The distinction you wanted tested holds up.** Describing *why* an ingredient
is useful predicts things that recipe co-occurrence does not. That's the
strongest single finding, and it holds in both tasks.

**No engine needs to commit to LightGBM.** It was competitive, never the best.

## Pairing: which ingredient adds something to this state

Held out one ingredient at a time; 54 prepared states with curated pairings
(286 right answers) across 10 ingredients. Butter's states have no curated
pairings. Scores are NDCG@10 means over states, where 1.0 means every curated
pairing is ranked at the top.

| Model | Features | NDCG@10 | Recall@10 | MRR | Worst ingredient |
| --- | --- | --- | --- | --- | --- |
| Extra trees | D | **0.457** | 0.480 | 0.667 | 0.225 (apricot) |
| Random forest | D | 0.444 | 0.489 | 0.637 | 0.168 (apricot) |
| Histogram gradient boosting | D | 0.424 | 0.459 | 0.634 | 0.245 (apricot) |
| LightGBM LambdaRank | D | 0.423 | 0.456 | 0.639 | 0.215 (apricot) |
| LightGBM classifier | D | 0.400 | 0.440 | 0.622 | 0.172 (apricot) |
| **Bayesian scoring (best statistical)** | C | 0.381 | 0.450 | 0.586 | 0.217 (apricot) |
| Logistic regression | D | 0.330 | 0.399 | 0.483 | 0.263 (cabbage) |
| Curated frequency | none | 0.313 | 0.327 | 0.526 | 0.189 (tomato) |
| Hybrid statistical | C | 0.269 | 0.323 | 0.413 | 0.172 (potato) |
| SVD embeddings | A | 0.257 | 0.318 | 0.356 | 0.057 (rutabaga) |
| Co-occurrence | A | 0.251 | 0.317 | 0.347 | 0.148 (cabbage) |
| Popularity (corpus) | A | 0.243 | 0.246 | 0.483 | 0.165 (cabbage) |
| Smoothed lift / PPMI | A | 0.214 | 0.266 | 0.342 | 0.103 (rutabaga) |
| Flavour compatibility | B | 0.134 | 0.140 | 0.289 | 0.039 (apricot) |

Every model covers every state (coverage 1.0). The full table, with NDCG@5,
recall@5 and MAP, is in `results/summary.csv`.

**Against the best statistical model** (Bayesian scoring on C), with a paired
bootstrap that resamples whole ingredients:

| Model | Difference in NDCG@10 | 95% interval | Ingredients better |
| --- | --- | --- | --- |
| Extra trees [D] | +0.076 | +0.033 to +0.132 | 9 of 10 |
| Random forest [D] | +0.063 | +0.018 to +0.100 | 8 of 10 |
| LightGBM LambdaRank [D] | +0.042 | +0.008 to +0.094 | 7 of 10 |
| Histogram gradient boosting [D] | +0.043 | −0.004 to +0.094 | 7 of 10 |
| LightGBM classifier [D] | +0.020 | −0.028 to +0.064 | 6 of 10 |

**What each feature set adds** (random forest, the steadiest learner; paired,
by ingredient):

| Step | Difference in NDCG@10 | 95% interval | Ingredients better |
| --- | --- | --- | --- |
| C (both) over A (culinary only) | +0.104 | +0.067 to +0.150 | 10 of 10 |
| C (both) over B (functional only) | +0.081 | +0.052 to +0.117 | 10 of 10 |
| D (full context) over C | +0.027 | +0.003 to +0.051 | 6 of 10 |

Extra trees shows the same direction, with wider intervals.

**Reading it**
- **Recipe statistics alone are weak**, and on their own they don't even beat
  "fillers that are usually curated" (curated frequency 0.313 against the best
  corpus scorer, 0.257). Smoothed lift does *worse* than raw co-occurrence: it
  favours rare, specific partners, while curated pairings lean on everyday
  fillers.
- **Functional knowledge and recipe statistics complement each other.**
  Neither set alone gets far; together they gain about 0.1 NDCG on every
  ingredient.
- **The hand-written complementarity rule is the weakest model of all**
  (flavour compatibility, 0.134). The functional features are useful as
  inputs to a learner, not as a fixed formula. The learner finds combinations
  the formula misses: which roles matter for which serving forms and
  techniques.
- **The hybrid statistical model underperforms Bayesian scoring.** A weighted
  sum of standardised scores is too blunt; the binned, smoothed likelihoods
  do better.
- **Fruit is the hard case.** Apricot is the worst held-out ingredient for
  almost every model. It's one of only two fruits among ten vegetables, so a
  model trained on the others learns vegetable habits.

## Scout: which ingredient can do the source's job here

93 substitution contexts with 104 right answers across 10 ingredients. In
**strict** mode (the main one), a model gets no credit for a substitution it
saw on another ingredient.

| Model | Features | NDCG@10 | Recall@10 | MRR |
| --- | --- | --- | --- | --- |
| **Functional similarity** (role overlap + same family − availability gap) | B | **0.311** | 0.554 | 0.269 |
| Context nearest neighbour | C | 0.266 | 0.500 | 0.218 |
| Hybrid statistical | C | 0.255 | 0.495 | 0.207 |
| Random forest | B | 0.238 | 0.430 | 0.211 |
| Logistic regression | C | 0.234 | 0.441 | 0.189 |
| LightGBM LambdaRank | B | 0.226 | 0.403 | 0.201 |
| LightGBM classifier | B | 0.208 | 0.366 | 0.188 |
| Bayesian scoring | B | 0.154 | 0.296 | 0.143 |
| Curated frequency | none | 0.091 | 0.231 | 0.081 |
| Rarely with the source (−PPMI) | A | 0.085 | 0.183 | 0.084 |
| SVD cosine to the source | A | 0.065 | 0.124 | 0.071 |
| Popularity | A | 0.053 | 0.161 | 0.042 |

No model beats functional similarity. Logistic regression, extra trees and
histogram gradient boosting are significantly *worse* (intervals entirely
below zero); the others' intervals cross zero, so they are not better. Almost
every model scores 0 on apricot (3 contexts).

**Reading it**
- **Recipe statistics do not find substitutes.** The best corpus-only model
  ("rarely with the source") reaches 0.085. The idea that alternatives rarely
  appear together is true but far too weak a signal on its own.
- **Role overlap does the work, and part of that is circular.** The Scout
  rules were written with the same role vocabulary ("both provide fat"), so
  functional similarity partly recovers how the rules were authored.
- **The roles miss texture.** In the novel review, walnut's top substitutes
  are avocado and ghee (both carry fat) and even cabbage. That loses the
  crunch, which is why walnut was there. Ghee and avocado are in the top five
  for about 40 contexts each, because they carry several roles.
- **Transfer mode is not a reason to learn.** With known rules allowed to
  carry over from other ingredients, extra trees reaches 0.768. That is
  memorisation of rules, and the rule engine already applies a rule's scope
  to new ingredients deterministically. It is not new ideas.

## The leakage probe

Adding `transformation_missing_roles` (the per-state notes that name curated
fillers) raises pairing NDCG@10 by about 0.1. LightGBM classifier goes from
0.400 to 0.513; its worst ingredient goes from 0.172 to 0.405. Excluding it
was right; with it included, every learner would look better than it is. It
does not help Scout (strict), where those roles are not the answer.

## Unknown, not wrong

The sheets in `results/*_novel_review_*.csv` list each model's top five
suggestions per state or context that are **not** curated, with an empty
verdict column for a person to fill in. A first pass by Claude, not a review:

- **Pairing:** many top uncurated suggestions look like gaps in the curated
  data rather than mistakes:
  - salt on braised cabbage, lemon on braised cabbage, vinegar on roasted
    broccoli, olive oil and thyme on baked potato.
  - Sea salt is the most frequent suggestion (top five for 25 states), which suggests salt
    is rarely written down as a pairing because it is assumed.
  - Some suggestions are odd: eggs on roasted apricot.

  If many suggestions hold up, the measured scores *understate* every model,
  most of all the better ones.
- **Scout:** the suggestions are sensible but conventional:
  - lemon → vinegar or lime;
  - basil → dill or parsley;
  - mozzarella → soft cheese.

  That is the safe half of Scout. Its interesting half, cross-category
  analogies like miso for butter, is what no model here proposes.

## Limits

- **Small and dependent data.** There are ten held-out ingredients, and within
  one ingredient the states share a base, so the intervals resample whole
  ingredients. A difference of 0.04 is near the limit of what this data can
  resolve.
- **The curated data is both the answer and part of the input.** The roles
  and sensory profiles were written by the same people as the pairings and
  rules. The leakage test proves no feature reads the answers, but the
  functional vocabulary and the answers share an author. Real confirmation
  needs held-out tastings or an outside curator.
- **One corpus, state-blind.** CulinaryDB cannot tell roasted broccoli from
  raw, so feature set A is identical for all states of one ingredient. 12
  rare fillers (sumac, za'atar, chili crisp…) have no embedding.
- **Small hyperparameter grids**, tuned within the training ingredients;
  larger searches might move learners by a few points, not past the
  intervals above.
- **XGBoost and CatBoost were not run** (not installed). At this data size
  they are not expected to change the outcome.

## What to do next

1. **Pairing:** use a tree ensemble (extra trees or random forest) on the full
   context (D) as the ranking engine. Keep Bayesian scoring on C as the
   transparent fallback and the explanation: it is 0.08 behind and can say
   why. The engine stays replaceable behind one scoring interface.
2. **Scout:** no machine learning yet. Use functional similarity to *suggest*
   substitutes for a person to turn into rules, and add texture and function
   detail to the roles (crunch from nuts versus crunch from crumbs), which the
   novel review shows is the missing piece.
3. **Review the novel-suggestion sheets.** Every confirmed suggestion is a new
   curated pairing, and it also fixes the evaluation's blind spot.
4. **More ingredients, especially fruit.** A second fruit-heavy batch would
   help most where the models fail most.
5. **Then R2:** FlavorDB aroma compounds, the one evidence source R1 left out
   on purpose, measured against these numbers.
