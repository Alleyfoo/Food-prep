# Food-prep's information structures

Counts are from the built database at `ed2971e` (in-memory, from the YAML).
The question is not "what is on a card" but "what shape is the data". A
layout fits the data when its structure matches one of these shapes.

## 1. Entities (things with attributes)

| Entity | Rows | Key attributes | User-facing name |
| --- | --- | --- | --- |
| Ingredient (raw) | 89 (11 own a technique tree) | kind, family, base roles, availability | ingredient |
| Technique | 37 | heat, moisture change, preservation flag | way to prepare |
| Prepared ingredient (component) | 62 | kind, keeps, freezes, batch value; sensory profile (56) | prepared ingredient |
| Role | 15 | role family (seasoning, structure, richness…) | what it still needs |
| Flavour route | 3 (on 13 prepared ingredients) | description, dimensions, risks, **attestation** | route |
| Scout analogy rule | 51 | mechanism, shared function, risk, **inference strength** | idea |
| Evidence source | 12 | type (dataset, official, culinary) | source |
| Tasting trial | 1 | verdict, observations, safety | tasting |

## 2. Relationships (the bulk of the data)

| Relation | Rows | Cardinality | Carries |
| --- | --- | --- | --- |
| ingredient **becomes** prepared ingredient, via technique | 61 transformations | 1 ingredient : many states | flavour/texture shift, confidence, risks |
| prepared ingredient **becomes** prepared ingredient | 1 (boiled → smashed roasted potato) | chain | same |
| prepared ingredient **needs** role | 250 | many : many | priority, note |
| role **filled by** filler, *for* a prepared ingredient | 303 pairings | ternary (state, role, filler) | confidence, application, availability, context |
| prepared ingredient **fits** route | 15 | many : many | fit reason |
| route **uses** ingredient | 9 | many : many | contribution, **optionality** (required / supporting / finish) |
| prepared ingredient **may take** idea (analogy applied) | generated per state | many : many | strength, novelty class, protocol |
| transformation **backed by** source | 75 | many : many | claim scope |
| pairing **backed by** source | 288 | many : many | claim scope |
| prepared ingredient **used in** dish context | 239 | many : many | strength |

**The shape that matters:**
- The core is a **ternary relation**, prepared ingredient × role × filler.
- Around it sits a **bipartite graph** of states and routes, and a
  **generated layer** of ideas.
- Cards flatten the ternary relation into one card per state, with roles as
  rows and fillers as chips. That works for reading one state, and fails for
  reading *across* states or *from* a filler.

## 3. Transformations

- Mostly a **tree of depth one**: raw → state, 60 of 61.
- One chain: boiled → smashed and roasted.
- Each step has before/after attributes (flavour shift, texture shift) and
  a *confidence*.
- **Display consequence:** for most ingredients a full graph adds little
  over a list of steps. The graph earns its place on the *needs / pairings /
  routes* side, not the transformation side.

## 4. Alternatives

Alternatives exist at three levels, and today they are not distinguished:

| Level | Example | Where it lives |
| --- | --- | --- |
| Alternative **preparations** of one ingredient | roasted vs steamed broccoli | transformations |
| Alternative **fillers** for one role | fat: garlic confit, ghee, olive oil | pairings, ordered by application then confidence |
| Alternative **routes** for one state | creamy and acidic vs sour and toasted nut | flavour routes |

- Comparing preparations is a **row-vs-row** task. Choosing a filler is a
  **within-cell** task. Choosing a route is a **set-cover** task (what you
  have against what the route requires).

## 5. Uncertainty (four different kinds)

| Kind | Field | Values | Meaning |
| --- | --- | --- | --- |
| How sure the curation is | `confidence` (transformations, pairings) | pairings: high 144 · medium 127 · low 13 · medium high 3 · **experimental 16**; transformations: high 48 · medium high 9 · medium 4 | the editor's judgement |
| How well attested a structure is | `attestation` (routes) | medium high … | how common, **not** how good |
| How sound a generated idea's reasoning is | `inference_strength` (analogy rules) | high … low | **not** how good the result is |
| How novel an idea looks in recipes | novelty `result_class` | common 25 · uncommon 23 · underpowered 24 · established 15 · insufficient coverage 11 · rare 6 | corpus search, not quality |

On top of these there is **absence**:
- **56 of 250 needed roles have no Cook pairing.**
- 5 transformations have no sensory profile.
- Only 13 prepared ingredients have a route.
- Absence is information ("nobody wrote it down"), and is not the same as
  "not needed" or "doesn't work".

## 6. Supporting evidence

- Evidence is attached to **two different objects**:
  - to the transformation (75 links, all 61 covered);
  - to the pairing (288 links; the 16 experimental pairings have none).
- Corpus co-occurrence counts on pairings are **0 for all 303**. The column
  exists but is not backfilled in this build, so no layout should imply
  corpus support for a pairing.
- Tasting trials attach to *(analogy, state, candidate)*. There is 1: brown
  butter on roasted broccoli, "works".

## 7. Facts vs suggestions: one record can be several things at once

Brown butter on roasted broccoli is all of these:
1. an **experimental pairing** (curated, `confidence = experimental`, kept
   out of Cook views);
2. a **Scout idea** (analogy *browned fat for plain fat*, strength medium
   high, novelty "underpowered");
3. **tested** once (2026-08-12, "works").

The cards in the Ingredient Explorer show none of these: experimental
pairings are filtered out of Cook. Scout shows 2 and 3. **No current view
shows all three together**, which is the clearest single case for an
explicit status label.

## Status vocabulary used in R3

One label per relation, read from the data, never inferred:

| Status | Rule |
| --- | --- |
| Curated | transformation, need, pairing or route with a non-experimental confidence |
| On hand | a curated pairing or route element whose filler the user typed as available |
| Source | an evidence link |
| Idea | a Scout idea or an experimental pairing |
| Tested | an idea with at least one tasting trial |
| Not recorded | a needed role with no pairing, or a missing section, shown as a hatched cell |

Implemented in `prototype/model.py`. Tested in `tests/test_r3_layouts.py`
(e.g. brown butter must be Idea and Tested, never Curated).
