# R4 step 6: limitations found, and the one extension made

The rule: extend the model only where a transfer worth cooking exposes a
genuine limitation, and only as far as that transfer needs. Every limitation
the transfers met is listed below with what was done. One was fixed.

## Fixed: a layer that softens more slowly than the others (amendment A2)

- **Transfer.** Potato and rutabaga gratin (worth cooking).
- **What the model got wrong.** It accepted raw thin rutabaga slices layered
  with raw potato (`rutabaga_gratin_raw`, holds in
  `model-tables-before-a2.md`). Two cooks report that rutabaga stayed crunchy
  after 45 min and after over an hour (G20, G21); documented recipes blanch
  the rutabaga, and only the rutabaga (G1, G10, G11, G22). The cause in the
  model: an assembly takes its first layer's state (R3), and no property said
  that a dense root softens more slowly than potato in the same bake.
- **Smallest change that fixes it.** Data only, no code:
  - a property `cooks_slowly` in `operations.yaml`, recorded only when true,
    so a material that does not state it is not slow (no unknowns appear
    anywhere else);
  - one requirement on the `superposer` role `layer`: not `cooks_slowly`,
    *waived when the layer is blanched or cooked*;
  - `rutabaga.root` states `cooks_slowly: true` (its note cites G20, G21).
- **Why this and not more.** R3 listed "member states under the final heat"
  as its largest gap (`../r3-construction-modelling/r4-needs.md` item 2). The
  gratin did not need that: cooking each member through the final bake would
  mark the rutabaga `cooked` exactly as it marks the potato, so it would still
  not catch the failure. What the gratin needed was the difference in rate,
  checked where the members meet. A general cooking-rate or moisture model
  was not built.
- **Recorded as documented amendment A2** in
  `src/foodprep/data/construction_freeze_amendments.yaml` (new catalogue hash
  and `superposer` hash). `construction_freeze.yaml` and R3's original result
  tables are unchanged.
- **Effect on R3: none.** All 57 routes of the 35 documented dishes were
  compared before and after (verdict, failures, unknowns, claims, every step's
  status, recombination links): identical. R3's `run.py` writes byte-identical
  `-a1` tables. Design 13 fully / 14 partly, held-out 2 / 6, 13 recombination
  links. **Effect on R4:** only the control changes, from *holds* to *fails*
  on the new requirement; every other transfer is unchanged
  (`model-tables.md` against `model-tables-before-a2.md`).
- **Still not covered.** The third documented fix, a covered bake of about
  90 minutes for raw slices (G7, G8), is a matter of time, which the model
  does not have: the model would reject that route although it works.
  Recorded as a model gap on the transfer.
- **Tests.** `tests/test_transfers.py::test_a2_rutabaga_must_be_blanched_in_a_gratin`,
  `::test_a2_changes_no_documented_layer`; the freeze test accepts the
  documented amendment (its helper now replaces scalar entries such as the
  catalogue hash).

## Recorded, not fixed

None of these blocks a transfer worth cooking from being represented and
checked. Each is a reason the model cannot say something the evidence says.

| Limitation | Met in | Why it was not fixed |
| --- | --- | --- |
| **Quality is outside the model**: dryness and hardness of a fried paste (P15), the flavour of rutabaga with cream, a noticeable stem | pea falafel, gratin, stem patties | No scoring, by design. It is the kitchen test's question |
| **Time and temperature**: a covered 90-min bake, overboiled onion layers that slip, napa going mushy, a rib that softens only with long cooking | gratin, onion, napa | A time property would be the moisture-and-heat simulator the brief rules out; no transfer worth cooking failed for lack of it except the gratin's third route |
| **Several pieces as one member**: two or three small leaves overlapped as one wrapper (K13) | kale | Kale is not worth cooking; napa needs one leaf per roll |
| **Several containers for one filling** (onion and courgette in one tray, O3, O5) | onion vessel | R3's known schema gap; the transfer is checkable with the onion alone |
| **Layered bulbs**: an onion is layers, not flesh; `creuser` stands for lifting out inner layers | onion vessel | The operation gives the right shell and fraction; nothing depends on the difference |
| **Grind coarseness and added moisture** in a paste | pea falafel | Matters for quality only (dense or dry), not for whether it holds |
| **Amounts and yield**: one broccoli stem is 100-150 g | stem patties | Amounts are evidence, not properties (R3) |
| **A property set from the same evidence it is checked against** (peas `sets_on_heat`, curly kale `piece: medium`) | pea falafel, kale | Not a code limit but a method limit: such agreement is not independent support, and the documents say so |

## Limits of the evidence itself

- **Lidl's regular range is not online** (`catalogue.md`). Availability of
  dried peas, fresh broccoli and napa cabbage is unconfirmed, not absent.
- Most recipe pages were read through a summarising fetch tool; this round did
  not re-read a sample of them as raw text (R2 did, 12 of 127).
- Ratings are small samples on commercial sites; the only controlled quality
  study is one MSc thesis (P15) with a deliberately bare recipe.
- Nothing was cooked.
