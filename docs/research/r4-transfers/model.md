# R4 step 4: does the model explain why each transfer works or fails?

Each transfer is data in `src/foodprep/data/transfers.yaml`: one documented
route from R3 (`constructions.yaml`) plus only what the transfer changes (a
material swapped, steps added, an assembly rewritten). `foodprep.transfers`
builds the derived route and runs it through R3's validator,
`constructions.validate_route`, **unchanged**: every step through R1's
`assess`/`apply`, every assembly role checked, every claim (`expects`,
`final`) checked against the computed state, recombination derived. The
transfer cites R4 evidence ids where it departs from the base; inherited
steps keep their R2 recipe ids. Full step-by-step output: `model-tables.md`
(and `model-tables-before-a2.md`, the same run before amendment A2).

"Holds" means no step, role or claim fails. "Agrees" compares that with what
the evidence says about the result. A transfer's R3 verdict is *partly*
whenever it records a model gap, so the verdict column says less than
holds/agrees.

| Transfer | Model | Evidence | Agrees | What did the work |
| --- | --- | --- | --- | --- |
| pea falafel | holds | works, with a dryness risk | yes | a property set from the evidence (`sets_on_heat`) |
| kale rolls (curly) | fails: leaf too small | indirect only | not comparable | a value set from the evidence (`piece: medium`) |
| napa-cabbage rolls | holds | works, shave the rib | yes | the head's leaves come off raw; recombination of the rib |
| rutabaga gratin (blanched) | holds | works | yes | the potato starch claim; A2's layer requirement is met |
| rutabaga gratin, raw (control) | fails (after A2) | fails | yes after A2, **no before** | A2 |
| broccoli-stem patties | holds | works (thin evidence) | yes | firmness and water of the stem, peel-first rule |
| onion vessel | holds | works | yes | the large-piece waiver for a vessel; recombination |

## Per transfer

### Pea falafel

- **Explains.** Why no binder is needed and why the peas must not be boiled:
  a soaked raw pulse is `sets_on_heat`, so frying a soft paste is applicable
  (R2 H4), exactly as for chickpea, and the claim "soaked, not cooked" holds.
- **Cannot.** It cannot *derive* that peas set on heat: the property was
  written from the evidence (P2, P4, P15), so its agreement is not independent
  support. It cannot predict the documented weakness: the lower water uptake
  (P15) is recorded (`water_uptake: medium` against chickpea's `high`), but
  nothing turns it into "dry and hard when fried"; grind coarseness and the
  moisture onion adds are not properties.
- **Agrees** on structure; is silent on quality.

### Kale rolls (curly kale)

- **Explains.** It names the requirement that decides the question: a wrapper
  must bend (blanching makes kale flexible, as it does cabbage) and must be
  large enough to close around the filling.
- **Cannot.** The verdict follows from one value this round set by reading
  the evidence: bagged curly kale leaves `piece: medium`. A test shows that
  with `large` (flat kale) the same route passes. So the model restates the
  evidence; it does not test it. Frilled edges, stiffness after blanching and
  two or three small leaves overlapped as one wrapper (K13) are not
  expressible: a wrapper is one material.
- **Agreement:** not comparable; the evidence on curly kale is indirect.

### Napa-cabbage rolls

- **Explains.** Why no whole-head boil is needed: `detacher_feuilles` needs a
  pliable head; a cabbage head is not (blanch first), a napa head is. The
  shaved rib minced into the filling (N3) is derived as recombination (napa ->
  `equeuter` [ribs] -> filling).
- **Cannot.** That the rib *must* be shaved or it stays stringy (N2):
  `equeuter` is applicable, not necessary. Whether thin leaves dry out
  uncovered. One modelling choice to note: the simmered alternative (N1) is
  `mijoter`; `braiser` would be inapplicable (napa is not fibrous enough to
  need a long braise), which fits N12's warning that it goes mushy.
- **Agrees.**

### Potato and rutabaga gratin, and its raw control

- **Explains.** Where cohesion comes from: the claim that the potato layer
  supplies starch to thicken the dairy holds (potato `starch: high`, rutabaga
  `low`), which is why recipes keep potato at least half or add flour. After
  amendment A2, why the rutabaga is blanched: a layer that `cooks_slowly` must
  be blanched or cooked before the shared bake.
- **Before A2 the model disagreed with the evidence.** It accepted the raw
  control (thin raw rutabaga with the potato), which two cooks report staying
  crunchy (G20, G21). An assembly takes its first layer's state, and no
  property said that a dense root softens more slowly than potato. This is the
  one limitation this round fixed (`limitations.md`).
- **Cannot, even after A2.** It does not compute the dairy thickening or the
  rutabaga softening in the oven: A2 is a requirement on a member at the join,
  not a simulation. The third documented fix, a covered bake of about 90 min
  (G7, G8), is a matter of time, which the model does not have, so the model
  would wrongly reject that route.

### Broccoli-stem patties

- **Explains.** Why the stem is peeled first (grating is conditional on a
  tough outer layer: "peel first: the tough layer shreds into strings") and
  why it is not squeezed: the peeled stem is firm and only `water: medium`,
  like carrot, which R2 found is never squeezed (C4).
- **Cannot.** How much stem a head gives (100-150 g), and whether a thin
  patty cooks a raw grated stem enough for sensitive stomachs (B15).
- **Agrees**, on thin evidence.

### Onion vessel

- **Explains.** The same requirements as the courgette, met the same way:
  onion pieces do not hold their shape cooked, but a large blanched half
  stands (the container waiver for a large piece); the inner layers return to
  the filling (recombination is derived: vessel -> `creuser` [flesh] ->
  filling).
- **Cannot.** That an onion is layers, not flesh (`creuser` stands for
  lifting out inner layers), and why overboiled layers slip apart (O10, O12).
  The Nice and Ligurian practice of one filling for onion and courgette in one
  tray needs several containers per assembly, R3's known schema gap.
- **Agrees.**

## What this says about the model

- **It agrees with the evidence on all six comparable transfers after A2**,
  and on five of six before it. But agreement is cheap where the deciding
  property was written from the same evidence (peas `sets_on_heat`, curly
  kale `piece`). The checks that carry information are the ones whose deciding
  property was there before R4: the stem's firmness and water (R1), the napa
  head versus the cabbage head (`detacher_feuilles`, R3), the vessel waiver
  (R3), the potato's starch (R3).
- **It explains structure, not quality.** In every transfer worth cooking, the
  open question is quality (pea falafel dry? rutabaga sharp? napa rib
  stringy? stem noticeable?), and none of it is in the model. That is by
  design (no scoring), and it is why each verdict rests on the evidence and
  ends in a kitchen test.
- **It found nothing the search did not.** Every useful fact about these
  transfers (blanch the rutabaga, shave the napa rib, grind peas coarse, halve
  the onion) came from documented practice. The model's value here is as a
  checklist of requirements a substitute must meet, and as a way to record a
  transfer so that its assumptions can be tested.
