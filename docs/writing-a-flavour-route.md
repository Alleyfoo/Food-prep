# Writing a flavour route

There are three routes. That is not a backlog — it is the bar working.

A route is the strongest claim in the ontology, so it is the hardest to earn.
This is the standard the existing three meet, written down so the fourth is
held to the same one.

## What a route claims

**A route claims that a structure is recognised. It does not claim the food
will be good.**

Read what the three existing routes say about themselves:

- *Creamy and acidic* — "General yogurt-and-citrus dressing structure."
- *Sour and toasted nut* — "General browned-vegetable, sharp-condiment, and
  nut structure."
- *Soy and garlic* — "A broad stir-fry structure, **not a claim about one
  regional recipe**."

Every one describes a *grammar*, and the third explicitly refuses to claim
more. That restraint is the point. Nothing in this system says a combination
tastes good except a recorded tasting.

This is why the column is called `attestation` and not `confidence`:
`attestation: high` means *this structure is well attested*, not *this will
be delicious*. See `tests/test_claim_vocabulary.py`.

## The three questions

Write the route only if all three answers are yes.

**1. Can you name the structure in general terms, without pointing at one
recipe?**
"Soy, garlic and a splash of acid on fast high-heat vegetables" is a
structure. "Chinese broccoli stir-fry" is a recipe. If you can only justify
it by naming one dish, it is not a route yet.

**2. Can you say what breaks it?**
Every route carries `risks`, and they are specific: "Too much soy masks fresh
green character; burnt garlic turns bitter." A route you cannot break is a
route you do not understand well enough to write. Vague risk text is the
clearest sign the structure has not been thought through.

**3. Can you say why this state fits it?**
`fit_reason` is per component, not per route — the same route attaches to
different states for different reasons. "The drained concentrated pieces
carry soy and raw garlic without going watery" earns the attachment. "Also
good on broccoli" does not.

## If an answer is no

It is a **Scout hypothesis**, not a route. That is a different object with
its own machinery — an analogy rule with a shared function, a meaningful
difference, an expected risk and a test protocol. Scout exists precisely so
that untested ideas have somewhere honest to live. Do not promote a guess to
a route because the Component Explorer looks empty without one.

## What a route needs

| Field | What it holds |
| --- | --- |
| `name` | The structure, in plain words |
| `description` | What the structure does, mechanically |
| `flavour_dimensions` | The dimensions it moves |
| `elements` | Ingredients with `required` / `supporting` / `finish` |
| `risks` | What breaks it, specifically |
| `cultural_context` | The general structure — never a single recipe |
| `attestation` | How well attested the structure is |
| `states` | Each component it fits, each with its own `fit_reason` |

## The obvious next one

`roasted_tomato_component` has no route and is the component the Component
Explorer opens on. Roasted tomato with basil, olive oil and garlic is a
structure that passes all three questions comfortably — it can be named
generally, it breaks in known ways (basil blackens if it goes in hot, garlic
turns acrid), and roasted tomato fits it for a statable reason.

45 of 58 components have no route. Most never will, and that is fine.
