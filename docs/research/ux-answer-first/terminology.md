# Terminology — user-facing vocabulary (E3, limited review)

**Scope:** the strings on the affected workflow that name the central
object, a prepared ingredient. Identifiers, database fields, YAML and the
code's own comments are unchanged.

## The decision

| Concept | User-facing term | Example | Kept distinct from |
| --- | --- | --- | --- |
| Raw ingredient | **ingredient** | broccoli | its preparations |
| Prepared ingredient / state | **prepared ingredient** | roasted broccoli | the technique that makes it |
| Cooking technique | **way to prepare** (card title: the technique) | Roast | the result of it |
| Flavour route | **route** / its own name | Creamy and acidic | single pairings |
| Destination | **use in** / destination name | side dish, pasta | — |
| Experimental hypothesis | **hypothesis** / **idea** (Scout) | roasted broccoli + brown butter | recorded routes and pairings |
| A composed plate in Taste Circle | **your dish** (unchanged) | — | a prepared ingredient |

### Why "prepared ingredient"

- It covers every state in the catalogue: roasted, steamed, pickled,
  salted, **raw-assembled** and soup bases. "Cooked" would be wrong for
  pickled and raw. "Dish" would be wrong for a component, and it collides
  with Taste Circle's "Your dish", which is a different thing.
- It reads as ordinary language ("roasted broccoli is a prepared
  ingredient"). "Transformed state" and "component" are model vocabulary.
- R2 counted four or more names for this one thing (R2 C3). One name lets a
  reader see that the views are about the same object.

## What changed (user-facing strings)

| Before | After | Where |
| --- | --- | --- |
| Transformed state (label, eyebrow) | Prepared ingredient | Scout |
| Prepared state (label, eyebrow) | Prepared ingredient | Taste Circle |
| Choose a prepared state | Choose a prepared ingredient | Component Explorer, Scout, Taste Circle placeholders |
| ● The dish you are investigating | ● The prepared ingredient you are investigating | Ingredient Explorer (A and B) |
| ● Built on the dish you are investigating | ● Built on the prepared ingredient you are investigating | Journeys |
| …the dish you are investigating, has the dark ring | …the prepared ingredient you are investigating… | Map |
| no prepared state chosen | no prepared ingredient chosen | context strip |
| not on the current dish | not on the prepared ingredient you are investigating | Plate Balance / Filler Profiles note |
| …applied to transformed states | …applied to prepared ingredients | Scout disclaimer |
| Generated hypotheses for each transformed state | …for each prepared ingredient | Map › Scout ideas |
| "Broccoli states it can use" / "No state of …" | "Prepared broccoli it can use" / "No prepared …" | Taste Circle, Scout empty states |
| 5 ways to transform it, ranked cooking before preservation | 5 ways to prepare it. | Ingredient Explorer B (left column) |
| Showing top 5 of 5 branches · ranked cooking-before-preservation | Other ways to prepare broccoli · ranked cooking before preservation | Ingredient Explorer B |

`tests/test_answer_first.py::test_one_name_for_a_prepared_ingredient`
renders all eight views and fails if "transformed state", "prepared state",
"dish you are investigating" or "the current dish" appears in text, labels
or placeholders.

## Deliberately not changed

- **The tab name "Component Explorer".** Renaming a tab spends a learned name
  and changes its URL slug (`?tab=component-explorer`), which links and
  tests use. Its eyebrow, "Something you already cooked", already explains
  it in plain words. This is a candidate for the human test (does the tab
  name stop people?), not for this experiment.
- **"branches"** in variant A's eyebrow. A is the comparison baseline. Only
  the shared concept name was aligned there, so A and B differ in
  hierarchy, not in the word for the object.
- **"analogy rules", "corpus", "HIGH" / "MEDIUM HIGH", "hard gaps".** These
  are real jargon (R2 C3/C7/K2), but outside this workflow and this concept.
  A product-wide rewrite was out of scope.
