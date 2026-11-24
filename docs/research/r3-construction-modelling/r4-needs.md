# What R4 needs from R3

R4 is controlled transfers: carry a documented construction to another Lidl
ingredient (rösti from another root, other leaves as wrappers, other
containers, Finnish dried peas as falafel, rutabaga in a gratin). For each
candidate, first search whether someone already makes it; only then give the
physical rationale. R3 gives R4 the rationale's vocabulary, and shows where
it is still too thin.

## What R4 can use as it is

- **Each documented construction names the requirements a substitute must
  meet**, in checkable form: the role requirements of its joins (a container
  must be hollow and stand; a wrapper must bend or be cohesive; a dry phase
  must take up water; a coagulant must set on heat) and the route's `expects`
  claims (cooled before shaping, dewatered before the egg, still raw, not
  mashed). A transfer is then: replace one part in a route with another part,
  re-run `validate_route`, and read which requirements still hold. R3 did
  not run any transfer; this is the mechanism R4 can use.
- **`foodprep construction <dish>`** prints a dish's materials, operations,
  joins, recombination and the reasons, for the search step.
- **Potato, onion, cabbage, aubergine, rice, the dried pulses, spinach and
  bread** now have parts the operation engine reads (`staged_parts`), so
  `foodprep explore potato` works.

## What R4 must add or decide first

Ordered by how many transfers each blocks.

1. **Parts for the transfer targets.** Rutabaga, beetroot, parsnip, celeriac,
   kale, Finnish dried peas and the other Lidl candidates have no part
   properties, so no transfer to them can be checked. Add them as staged
   parts, with sources, before any transfer (data only, as in R3's held-out
   step).
2. **The state inside an assembly during the final heat.** R3's largest gap
   (all C8 dishes, gemista): the assembled whole takes its carrier's state,
   so a binding phase that thickens, or rice that cooks inside a vessel, is a
   claim. A transfer that changes a member (rutabaga in a gratin: does it give
   starch to the cream?) needs that member's state computed. Smallest step:
   apply the final heat to every member, not only the carrier, and record
   member states.
3. **One statement about materials that set on heat**, instead of one waiver
   per operation. `cuire_vapeur` lacks it (chawanmushi, moi moi failed). A
   material-level rule fits better than four waivers.
4. **Doughs** (C7c, pastry layers): a dough material and outputs for
   `abaisser` (roll out), so a dough wrapper is computed rather than
   asserted. Needed before any filled-dough transfer (pierogi with other
   fillings, karjalanpiirakka).
5. **Containers.** A role that takes several containers (one filling, many
   vessels: gemista, farcis), and an operation that makes a pocket without
   hollowing (zha qie he's hinged slices). Needed before "other vegetables as
   containers".
6. **Missing operations and state updates:** rinsing or washing (A1b, E1d,
   M8b), a second heating before assembly (E1c), `mixer` lowering toughness,
   `rotir` allowing a slow roast of a very watery vegetable (M16b).
7. **Properties R1 and R3 both lack:** surface water (W9), mucilage
   (okonomiyaki's yam), temperature and time (ice-cold batter, "cabbage
   last"), and variety (waxy or floury potato). Without them, R4 can state
   these conditions but not check them.
8. **The tomato's decomposition.** A tomato vessel is flesh and skin; the
   part model separates them. Either a "whole fruit" view of a decomposed
   ingredient, or accept that tomato vessels are recorded, not checked.

## Rules for R4 that R3 suggests

- Keep the freeze discipline: choose held-out transfers before changing the
  model, and record which changes a transfer needed.
- A transfer is a hypothesis until found in practice or cooked. Mark it as
  inference in the data (a new `split`, or a transfer file that references a
  documented route), never as a documented dish.
- Ask the kitchen tests R2 proposed (`../r2-construction-patterns/evaluation.md`)
  first: they compare documented variants and would test claims R3 could only
  record (settled starch vs flour, three water routes for courgette, rösti
  stored one or two days, a courgette shell refilled with its own flesh).
