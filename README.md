# food-prep

A local-first **ingredient transformation knowledge map**. The pilot ingredient is **tomato**.

The core object is not the recipe — it is the **transformation record**:

```
ingredient → technique → transformed component → missing roles → next ingredient
```

Given "I have tomatoes. What can I do with them?", the engine returns a small set of
high-value transformation branches (raw, salsa, roast, simmer, dry, pickle, freeze, can,
…), the reusable component each yields, the culinary roles still missing afterward, and
the common fillers that complete the dish — all backed by SQLite and curatable YAML.

This implements the prototype described in the Tomato Transformation Map research report:
~12 tomato transformations, ~12 role buckets, 30–50 pairing fillers, 8–10 reusable
components, evidence-linked, Finland-aware supermarket availability.

## Design principles

- **Transformations are finite; recipes are not.** Prep modifiers (slice, dice, peel) are
  separated from state-changing techniques (roast, simmer, dry).
- **Missing-role logic is the scarce layer.** No reviewed dataset models "what does a
  roasted tomato still need?" — that is hand-curated here.
- **Hybrid, not fully learned.** Hand-authored ontology first; corpus/statistical
  enrichment later.
- **Local-first.** SQLite only, no network, no cloud APIs.

## Install

```bash
pip install -e ".[dev]"
```

## Use

```bash
# build the SQLite db from the curated YAML
foodprep build

# "I have tomatoes. What can I do with them?"
foodprep ask "what can I do with tomatoes"

# "I roasted them — now what?"
foodprep ask "i roasted them now what"

# batch-prep ideas
foodprep batch

# what unlocks the most transformations
foodprep hub
```

## Layout

```
src/foodprep/
  schema.sql        SQLite schema (centre of gravity: transformations + missing roles)
  data/tomato.yaml  curated tomato ontology
  db.py             connection + schema bootstrap
  loader.py         YAML -> SQLite
  query.py          query engine (the brief's prompts)
  cli.py            command line
tests/              pytest suite
```