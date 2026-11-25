# ADR 0003: Documented constructions are recorded as data over the operation model

- Status: Accepted
- Date: 2026-11-24
- Round: R3 (`docs/research/r3-construction-modelling/`)

## Context

R1 gave the model single-material operations: one material in, one or more
materials out, with applicability and reasons. R2 read 127 recipes and found
that dishes are built from **several independently processed materials**
joined by a small set of structural relations (bind, contain, wrap, layer,
coat, set in a matrix), often with a fraction of one material returned into
another (recombination). R2 recommended Option D: record documented
constructions as data before writing any construction rule.

Nothing in the model could say "this filling goes into that shell", or "the
starch that settled out of this juice goes back into the mass". The
operation engine's single-material assumption is what keeps its search
bounded, and R2 warned that multi-input operations in the generator would
turn into the generator the user does not want.

## Decision

### 1. A construction is a dish, with one or more routes

`src/foodprep/data/constructions.yaml` holds documented dishes. A dish has
one or more **routes**: alternative ways to the same dish (raw or boiled
rösti), or, when R2 found it, two constructions under one dish name
(sliced or shredded hobak-jeon). Each route has:

- `materials`: independently processed materials. Each starts from a part
  (`potato.tuber`) or from an output of another material's step
  (`{material: shell, step: creuser, output: flesh}`), and has a list of
  **R1 operation steps**. The validator applies them with `operations.apply`
  and records each step's applicability. Nothing is assumed applicable.
- `assemblies`: joins. Each names an **assembly operation** and fills its
  roles with materials, other assemblies (nesting) or additions. It may
  then take further R1 steps (shape, rest, fry, bake).
- `result`: the assembly (or material) that is the finished dish.
- `final`: what documented practice says the result is (cooked, crisp,
  hollow ...), checked against the computed state.
- `holds_by` (R2 mechanisms H1-H11), `water` (R2 water routes W1-W9),
  `patterns` (C1-C9), `recipes` (R2 ids), `why` (one paragraph), `gaps`.

### 2. Additions are ingredients used as they are

Eggs, flour, crumbs, milk, cheese, oil, spices and meat fillings are
**additions**: listed once with the properties a role check needs
(`sets_on_heat`, `water_uptake`, `liquid` ...) and the catalogue ingredient
they are, or `null` when the ingredient is not in the catalogue (a Lidl
gap). They go through no R1 operations, as in R1's `Material.adds`.

### 3. Assembly operations live in `operations.yaml`, outside the generator

Six joins are operations with `generator: false`, so the bounded search and
the family generator never see them:

| Operation | Relation | Roles (carrier first) |
| --- | --- | --- |
| `melanger` | one phase from several materials | `body` + `starch`, `dry_phase`, `coagulant`, `liquid`, `fat`, `thickener`, `leavening`, `flavour`, `inclusion` |
| `incorporer` | pieces set in a matrix (batter, egg) | `matrix`, `inclusion` |
| `farcir` | a container holds a filling | `container`, `filling` |
| `envelopper` | a leaf, sheet or cohesive mass wraps a filling | `wrapper`, `filling` |
| `superposer` | layers held by a binding phase | `layer`, `binding` |
| `revetir` | a piece coated in order (dry, wet, dry) | `piece`, `coat` |

Each role has `requires` in R1's syntax. These are single-material checks
like R1's (a container must be hollow; a coagulant must set on heat; a dry
phase must take up water). They are not construction rules: they never say
that a dish works, only that the data's claim about a member is consistent
with that member's properties.

An assembly's state is its **carrier's** state (container, wrapper, first
layer, matrix, body) plus the operation's output flags (`assembled`, `filled`
...). Where a recipe says the mix changes (flour takes up the water), the
dish records a `state` override with `because` (the members responsible) and
recipe ids. The model does not derive mixture chemistry.

### 4. Recombination is derived, not labelled

Two materials of the same origin, each entering the construction by its own
route (through an assembly role or as the result), form a recombination link:
one starts from a fraction of the other, directly or through intermediates
that never enter the dish. A fraction whose source only feeds it is
extraction, not recombination. The validator lists the links. (Corrected
after the freeze, amendment A1.)

A join is food only if every member is: a member that is not food makes the
assembly not food, with R1's reason, so later steps are unsafe or
inapplicable (amendment A1). Every fraction a step produces must be used, or listed in that step's
`discard`, or the validator reports it as unaccounted.

### 5. "Why it works" is checkable claims, each cited

- `expects` on a step or an assembly member: the state documented practice
  requires at that point (`cooled: true` before shaping cooked starch;
  `water: "<=medium"` before the egg). Checked against the computed state.
- `final` on the route, checked the same way.
- Quantities and conditions are `evidence` strings attached to the step or
  relation they support, never steps to follow.

### 6. Minimum vocabulary added (each needed by a design dish)

- Operations (all `generator: false`): `tremper` (soak), `refroidir` (cool),
  `reposer` (rest), `creuser` (scoop out flesh), `fendre` (halve
  lengthwise), `decortiquer` (rub skins off soaked pulses),
  `detacher_feuilles` (separate a head's leaves from its heart), `faconner`
  (shape), and the six joins above.
- Outputs for existing operations that had none: `decanter` (settled solids
  + clear liquid), `egoutter` (drained + liquid), `foisonner` (aerated).
- States and properties: `soaked`, `cooled`, `rested`, `halved`, `formed`,
  `assembled`, `cohesive`, `aerated`, `sets_on_heat`, `water_uptake`.
- `refroidir` makes cooked starch `cohesive` (R2 H2, 13 traditions).
- `cuire_anglaise` and `mijoter` raise the water of a material that takes
  up water (`water_uptake`), so cooked rice is not dry.
- **One primary cooking per sequence** keeps its meaning for the generator,
  and is waived for an `assembled` material (R2: two cookings are normal
  once components are joined): `frire`, `rissoler`, `cuire_four`, `paner`,
  `enrober`.
- A material that `sets_on_heat` and is still raw (beaten egg, a raw pulse
  paste, a batter) can be fried or baked although it is liquid or smooth
  (R2 H4, H5, H6).
- Parts for construction ingredients (potato, onion, cabbage, aubergine,
  rice, dried pulses) go in a new `staged_parts` section of
  `part_properties.yaml`. The operation engine reads them. The family
  generator and the decomposition UI do not, because these parts have not
  been through ADR 0002's decomposition (descriptions, evidence, edibility).

### 7. R2's contradictions, fixed where a dish needs them

- `presser` no longer marks every pulp `binder: true`; only pulp with
  starch `>= high` is a binder (latkes yes, mücver no).
- Courgette `holds_shape_cooked: false` stays (it describes cut pieces). A
  container's shape requirement is waived for a large or whole piece, so a
  halved courgette shell stands (M16, M17).

## What this does not do

- No general construction rules, no generator, no scoring.
- It does not compute what happens inside an assembly during the final
  cooking (raw rice cooking in a tomato shell). The route records the claim.
- It does not model doughs, temperatures, times or surface water.

## Consequences

- Every documented dish can be checked: each step's applicability, each
  member's role, each claim, each recipe id.
- The schema is **frozen** before the held-out dishes are represented.
  `src/foodprep/data/construction_freeze.yaml` records the schema fields,
  the operation definitions and property keys at the freeze, and
  `tests/test_constructions.py` fails if a held-out dish depends on
  anything changed after it. The manifest is never rewritten: corrections
  are documented amendments (`construction_freeze_amendments.yaml`; A2, R4,
  adds `cooks_slowly` and a gratin-layer requirement with no effect on R3; A1 is the
  PR #7 validator correction). A later round that changes the schema on
  purpose records a new freeze and keeps R3's results as history.
- Existing behaviour is unchanged: the new operations are outside the
  generator, the waivers name states only the new operations set, and the
  family generator reads neither `staged_parts` nor assembly operations.
  The one deliberate change is the `presser` binder flag (R2's
  contradiction).
