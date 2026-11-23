# Presentation model: dimensions instead of one status

Implemented in [`prototype/r4_model.py`](prototype/r4_model.py). Tested in
`tests/test_r4_workspace.py`.

## What was wrong with R3's single status

R3 gave every relation one label: curated, on hand, source, idea, tested or
not recorded. That label answered several independent questions at once, so
one answer had to win:
- A curated pairing that was on hand became "on hand" and stopped saying it was curated.
- An experimental pairing became "idea", which made it look like the same kind of thing as a generated Scout hypothesis.
- A tested idea became "tested" and lost its inference strength.

Brown butter on roasted broccoli shows the problem. In the database it is
three records:

| Record | Table and key | What it says |
| --- | --- | --- |
| Experimental pairing | `pairings.pairing_id`, role *fat*, `confidence = experimental` | An editor recorded brown butter as a fat for this preparation, without grading it |
| Scout hypothesis | analogy `browned_fat_for_plain_fat_on_toasted_state`, candidate `brown_butter` | Generated: brown butter could replace olive oil because both provide fat and browned butter reinforces toasted aromas (inference strength *medium high*) |
| Tasting trial | `tasting_trials` on (analogy, component, candidate) | 2026-08-12, verdict "works", eaten as a normal meal rather than as a controlled test; ratio and temperature not measured |

Availability is a fourth fact. It depends only on what the user entered.

## The dimensions

Each record carries every dimension that applies, independently:

| Dimension | Values | Read from | Applies to |
| --- | --- | --- | --- |
| **Knowledge type** | curated · experimental pairing · Scout idea (generated) | `pairings.confidence = 'experimental'` → experimental; Scout generator → generated; everything else curated | every record |
| **Confidence** | the value *with its field name* | `confidence` (transformations, pairings), `attestation` (routes), `inference_strength` (analogy rules) | step, pairing, route, idea |
| **Availability** | on hand · not on hand · n/a | the user's on-hand list only | pairings, route elements, ideas |
| **Evidence** | sources (title, type, recorded claim scope) · "no source recorded" · "no source table for routes" | `transformation_evidence`, `pairing_evidence`, `evidence_sources` | steps, pairings |
| **Testing** | untested · trials (date, verdict, conditions) · n/a | `tasting_trials` by analogy, component and candidate ids | ideas |
| **Coverage** | recorded · not recorded · not applicable | whether a curated pairing exists for a needed role, whether a route or profile exists | needs, sections |
| **Optionality** | required · supporting · finish · n/a | `flavour_route_elements.optionality` | route elements |

Rules the model follows:
- **The confidence field's name stays with its value.** `confidence`, `attestation` and `inference_strength` measure different things: the editor's judgement, how common a structure is, and how sound an analogy's reasoning is. They are shown as "medium high (attestation)" or "medium high (inference strength)" and never on a shared scale.
- **An experimental pairing's confidence is "not graded".** The database stores "experimental" in the `confidence` field. That value marks a knowledge type, not a level, so it is shown as *not graded (recorded as "experimental")*. The database terminology stays visible.
- **Recipe frequency is not evidence here.** `corpus_cooccurrence_count` is 0 on all 303 pairings because the column was never backfilled, so it is not shown as a number anywhere. Novelty classes (a corpus search for Scout ideas) belong to the idea record and are labelled as a search class, not quality.
- **Tasting results stay on the idea they tested.** A trial is attached to an analogy, a component and a candidate, not to a pairing, so the model does not move "tested" onto the experimental pairing.
- **Absence is never negative.** A needed role with no curated pairing has coverage "not recorded". It is never "not needed" or "doesn't work".

## Linking records that describe the same pair

Records are linked only by database ids:
- the pairing's `ingredient_id`, plus the `component_id` that its `works_best_with_transformation_id` produces;
- the idea's `substitute_ingredient_id`, plus its component.

They are never matched by name. A link records its basis ("same component_id and ingredient_id") and keeps both records:

```
link: roasted broccoli (component 40) × brown butter (ingredient 54)
  pairing:<id>                                          experimental pairing for fat, no source
  idea:browned_fat_for_plain_fat_on_toasted_state:40:54  Scout idea, medium high, tested 1×: works
```

What is deliberately **not** linked:
- **Route elements and pairings.** Lemon is a *required element* of "Creamy and acidic", and separately a *curated pairing* for acid on roasted broccoli. These are two different claims: one about a route, one about a role. They share an ingredient node in the trace, but they stay two edges with different labels, and the route trace calls the pairing a "separate pairing record".
- **A trial and a pairing.** Explained above.

Across all 12 tree ingredients there are **11 links**:
- 3 join an experimental pairing to the Scout idea for the same pair: brown butter on roasted broccoli, rye crumbs on roasted cabbage, miso on tomato sauce base.
- **8 join a curated pairing to a Scout idea that proposes the same ingredient.** Examples: eggs on fried potato, dill on boiled potato, capers on potato salad. Scout presents as "new" something Cook already records. This was visible only once records were linked by id. It is logged in recommendations, not fixed, because the recommendation logic is out of scope.

## Other structure the model had to handle

- **54 pairings fill a role the preparation does not list as a need.** One example is potato as `mild_base` on braised cabbage. R3 dropped these from the graph. R4 shows them in all four representations:
  - in the overview matrix, as an extra column after the needed roles;
  - in the fact sheet, as "(not a listed need)";
  - in the compare view, as a role row;
  - in the trace, as a role node marked "(not a listed need)".

  A test found this while checking that every pairing appears everywhere.
- **Stable ids.** Every record id is built from database keys, for example `pairing:<pairing_id>`, `need:<transformation_id>:<role>`, `route:<route_id>:<component_id>`, `element:<route_id>:<ingredient_id>:<component_id>`, `idea:<analogy_id>:<component_id>:<ingredient_id>`. Ids do not change with the on-hand list, which tests check.
