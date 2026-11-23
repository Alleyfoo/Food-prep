# R1: statistical and machine-learning model selection

**Question.** Does machine learning offer anything beyond a well-designed
statistical recommender for Food-prep? And does our own food representation,
which says *why* an ingredient is useful in a prepared state, add predictive
value on top of what recipe statistics already say?

**Outcomes decided in advance.** There is no obligation to end with a
machine-learning solution.

| Outcome | Decision |
| --- | --- |
| A | Simple culinary statistics are sufficient |
| B | Functional knowledge improves statistical recommendations |
| C | Machine learning provides a meaningful additional improvement |
| D | Insufficient evidence; more curated data is required |

The findings and the decision are in [report.md](report.md).

## The two tasks

They are different problems, so each is scored on its own.

- **Pairing: complementary relationships.** For a prepared state (roasted
  broccoli), rank every ingredient by whether it contributes something useful.
  The right answers are the curated pairings: 286 distinct (state, filler)
  pairs across 54 states. Butter's two states have none.
- **Scout: functional equivalence.** For a known pairing (roasted broccoli with
  olive oil), rank every ingredient by whether it can do the source's job
  there. The right answers are the substitutes the Scout rules propose: 104
  across 93 (state, source) contexts.

## Feature sets

| Set | Information |
| --- | --- |
| **A**, culinary only | CulinaryDB: popularity, co-occurrence, smoothed lift and PPMI, SVD embedding cosine (with the base ingredient; for Scout also with the source) |
| **B**, functional only | the filler's roles, family, availability and kind; the state's flavour and texture tags, roles provided, roles it risks missing, heaviness and dryness; derived complementarity (fills a missing role, duplicates a provided one, repairs, avoid-when); for Scout, role overlap with the source, same family, availability gap |
| **C**, combined | A + B |
| **D**, full context | C + preparation characteristics defined independently of pairings: technique heat type and moisture change, serving form, how well it keeps, transformation tags |
| **L**, leakage probe | D + `transformation_missing_roles`. Written per state, with notes that name the curated fillers ("olive oil or cheese"), so not independent. Used only to measure how much such a feature would inflate the scores. |

**Excluded as leakage:**
- `pairings.corpus_cooccurrence_count`: it is filled only for curated rows, so
  corpus counts are recomputed for every candidate;
- a Scout hypothesis's `compatibility_score` and `matched_dimensions`: they
  are computed from the rule being predicted;
- the pairing's role.

`tests/test_r1_leakage.py` changes the answers and checks that no feature column
moves.

## Models

**Statistical and knowledge-based**
- Corpus popularity; curated frequency (how often a filler is a right answer
  in the training ingredients, shrunk toward the base rate).
- Co-occurrence, smoothed lift / PPMI, SVD embedding cosine.
- Flavour compatibility (pairing): fills a missing role, minus duplication,
  plus repairs, minus avoid-when.
- Functional similarity, "rarely with the source", and context nearest
  neighbour (Scout).
- Bayesian scoring: naive Bayes with Beta-smoothed binned likelihoods and an
  empirical-Bayes candidate prior.
- K-nearest neighbours over prepared states (pairing).
- Hybrid statistical: a weighted sum of standardised evidence, with the weights
  chosen inside the training folds.

**Machine learning:** logistic regression, k-nearest neighbours over rows,
random forest, extra trees, histogram gradient boosting, LightGBM classifier,
and LightGBM LambdaRank (grouped by state for pairing, by substitution context
for Scout). XGBoost and CatBoost are not installed, so they were left out of
this round.

## Evaluation

- **Leave one ingredient out.** Each base ingredient's states are held out in
  turn, which copies adding a new ingredient. Hyperparameters are tuned by
  grouped 3-fold cross-validation over the remaining ingredients only.
- **Scout, strict ("new substitution").** Training rows whose (source,
  candidate) pair is a right answer in the test fold are removed, so a model
  cannot pass by memorising the same rule from another ingredient. **Scout,
  transfer** keeps them and measures reuse of known rules.
- **Metrics:**
  - NDCG@5 and @10, recall@5 and @10, MAP, MRR;
  - coverage (queries where the model's scores are not all tied);
  - worst held-out ingredient.
  - Ties are broken in a fixed random order, so tied scores earn nothing.
- **Comparisons.** Each model is compared against the best statistical model
  with a paired bootstrap that resamples whole held-out ingredients, plus the
  number of ingredients on which it is better.
- **Unknown is not wrong.** A pairing nobody wrote down is unknown, not a
  negative. Scores therefore measure "recovers what is curated". The novel
  review sheets list the top uncurated suggestions for a person to judge.
- **FlavorDB is left out**, so any improvement can be traced to its source.

## Reproduce

```powershell
py -3.11 docs/research/r1-model-selection/run.py
```

This needs the CulinaryDB corpus (see the README: `data/corpus/culinarydb/` or
`FOODPREP_CORPUS_DIR`). It writes `results/`; a full run takes about an hour on
a laptop. `--quick` runs four models as a smoke test.
