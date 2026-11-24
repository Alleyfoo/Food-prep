# R3 evaluation

## Decisions, and what they cost

| Decision | Why | Cost |
| --- | --- | --- |
| Dishes as routes of materials and assemblies (ADR 0003), not a new graph | R2's Option D; reuses R1 operations, `apply`, `assess` and the property vocabulary unchanged | none of the old code paths changed; one helper (`check_requires`) was factored out of `assess` |
| Joins as operations in `operations.yaml` with `generator: false` | the brief preferred extending existing structures; keeps the generator single-material | the operation catalogue grows from 95 to 109 entries; R1's generated docs describe the 95 |
| Additions (eggs, flour, milk, cheese, meat) used as they are | as R1's `Material.adds`; pantry items have no parts and no decomposition evidence | a dish made only of additions (croquetas' béchamel) has its state asserted, not derived |
| An assembly takes its carrier's state | the simplest rule that lets R1's thermal operations judge the assembled whole | what happens to the other members during the final heat is not computed (the main gap) |
| Mixture changes recorded as `state` + `because` | the evidence states them ("flour takes up the remaining liquid", M4a; "until not runny", M3b) | 15 of 57 routes depend on an asserted change (water taken up, a matrix that sets, a dough that bends); each names the members responsible |
| Staged parts outside the family generator | they have not been through ADR 0002 decomposition | potato, onion, cabbage, rice exist twice (catalogue ingredient, staged part) until R5 decomposes them |
| One-cooking rule waived for `assembled` materials | R2: "two cookings are normal" (boiled rösti, korokke, parmigiana, double frying) | none for the generator, which never sets `assembled` |

## Existing behaviour

- The full test suite passes (922 tests before R3; the R3 tests are added).
- The family generator's fingerprint test is unchanged and green: it reads
  neither staged parts nor assembly operations, and the waivers name states
  only construction operations set.
- **One deliberate change:** `presser` no longer marks every pulp a binder,
  only starch-rich pulp. This is R2's first contradiction, and two design
  dishes need it (latkes binds through potato starch; mücver's squeezed
  courgette needs egg and flour). Its R1 test now pins the new behaviour.
  Rerunning R1's benchmark (`benchmark.py`) gives the same summary as PR #5
  (purpose-specific simplest-first 14/42, with the sensory term 17/42;
  global 0/42); only global ranks move, because squeezed carrot and
  courgette pulp lose the `binder` function. R1's generated files are left
  as they were, as the record of that round.
- R2's second contradiction (courgette `holds_shape_cooked: false`) is
  handled where a dish needs it: the container role waives the requirement
  for a large or whole piece. The courgette's part property is unchanged.

## Where R3 contradicted what was expected

| # | Expectation (brief, R2) | What representing the dishes showed | Verdict |
| --- | --- | --- | --- |
| 1 | Construction needs a separate layer (R2 Option C) | Materials with R1 paths plus six joins in `operations.yaml` were enough; no parallel model | not needed yet |
| 2 | Recombination needs its own construct (R2 "missing link") | It is derived: a material sourced from another's fraction that reaches the same dish | simpler than expected |
| 3 | The nine patterns are the right cut (R2) | Every design dish fits one or a combination; C8's mechanism (H10) occurs without layering (kaalilaatikko E14b is mixed); one route has no pattern at all (E14a with broth: nothing sets) | holds, with C8 better named by mechanism than by layering |
| 4 | Courgette `holds_shape_cooked: false` must change (R2) | A waiver on the container role for large pieces is enough; the property can stay | resolved at the point of use |
| 5 | The held-out dishes would show whether the model only accommodates the design set | They did: structure generalised, per-operation exceptions did not (steam), and doughs are missing | answered |
| 6 | Squeezed pulp is a binder (R1) | Only starch-rich pulp; the courgette dishes say the opposite | fixed (R2's contradiction) |

## Limits

- **Consistency, not truth.** The validator checks that a recorded dish is
  consistent with the model. If both the model and the data are wrong in the
  same way, it passes. Nothing was cooked.
- **Asserted states.** Fifteen of 57 routes rely on a `state` override (flour takes up
  water, egg sets milk, a dough is flexible). Each names the members
  responsible and is cited, but none is derived.
- **The assembly's state is its carrier's.** This hides the binding phase in
  C8 and the filling's change inside vessels (gemista, all stuffed dishes).
- **Evidence quality** is R2's: summaries of pages, spot-checked at 12 of
  127. Several sources are not independent (A2b, A18c), and some dishes rest
  on one recipe (kakiage A5a, frittata M20a, chawanmushi A8a, korokke A6a).
- **Lidl availability** is the catalogue proxy, not checked in a shop.
- **Not every documented detail is recorded.** Variants named on a page but
  not central (the page's alternative coatings for arancini, pork on
  okonomiyaki, stuffed onions in M17b) are left in evidence strings or gaps.

## Is it useful yet?

Not for making dinner directly: R3 represents dishes, it does not suggest
any. But it changes what R4 and R5 can do:
- a dish is now a set of checkable requirements, so a transfer can be checked
  against the requirements of the documented dish it comes from;
- `foodprep construction <dish>` explains why a dish works in terms of the
  same materials and operations the rest of the app uses;
- the staged parts make potato, onion, cabbage, rice and pulses explorable
  with the R1 engine (`foodprep explore potato`).
