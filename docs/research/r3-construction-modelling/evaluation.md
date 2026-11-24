# R3 evaluation

## Decisions, and what they cost

| Decision | Why | Cost |
| --- | --- | --- |
| Dishes as routes of materials and assemblies (ADR 0003), not a new graph | R2's Option D; reuses R1 operations, `apply`, `assess` and the property vocabulary unchanged | none of the old code paths changed; one helper (`check_requires`) was factored out of `assess` |
| Joins as operations in `operations.yaml` with `generator: false` | the brief preferred extending existing structures; keeps the generator single-material | the operation catalogue grows from 95 to 109 entries; R1's generated docs describe the 95 |
| Additions (eggs, flour, milk, cheese, meat) used as they are | as R1's `Material.adds`; pantry items have no parts and no decomposition evidence | a dish made only of additions (croquetas' béchamel) has its state asserted, not derived |
| An assembly takes its carrier's state | the simplest rule that lets R1's thermal operations judge the assembled whole | what happens to the other members during the final heat is not computed (the main gap) |
| Mixture changes recorded as `state` + `because` | the evidence states them ("flour takes up the remaining liquid", M4a; "until not runny", M3b) | four dishes depend on an asserted water or setting change; each names the members responsible |
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
