# R3 step 4: generalisability (held-out set)

## How the freeze was enforced

1. The held-out dishes and their recipe ids were recorded in
   `dish-selection.md` and committed (84dc664) before any schema work.
2. The schema was frozen at commit e8a2e54:
   `src/foodprep/data/construction_freeze.yaml` (written by
   `run.py --freeze`) records the schema's field lists, the vocabularies
   (patterns, mechanisms, water routes, gap kinds), a hash of every
   operation's definition, the catalogue settings (scales, default-false
   flags, functions), every property key, and hashes of
   `constructions.py` and `operations.py`.
3. Only then were the held-out recipe sections of R2's `recipes.md` read.
4. The held-out dishes were added as **data only** (commit 6beda68):
   dish entries, two staged parts (spinach, bread) and 15 additions. Nothing
   in `operations.yaml`, `operations.py`, `constructions.py` or the freeze
   file changed (`git diff e8a2e54 -- <those files>` is empty).
5. `tests/test_constructions.py::test_held_out_dishes_rely_on_nothing_changed_after_the_freeze`
   fails if the schema, vocabularies, catalogue settings or code differ from
   the freeze, if a held-out dish uses an operation that was added or changed
   after it, or if its parts or additions use a property key that did not
   exist at the freeze.

So a "fit" below means the dish was expressed in the vocabulary that existed
before the dish was seen. Where it does not fit, the change it would need is
named and **not made**.

## Results

8 held-out dishes, 14 routes: 2 dishes fully represented, 6 partly, 0 not.
Generated detail: `generalisation-tables.md`.

| # | Dish | Verdict | What fitted | What would need a structural change (not made) |
| --- | --- | --- | --- | --- |
| H1 | draniki / deruny (E5a, E5b-c) | **fully** | both routes: salt-drawn juice settled and its starch returned (E5a), or squeezed juice (E5b-c); "salt late" checked as a claim | nothing |
| H2 | kolokythokeftedes (M4a, M4b) | **fully** | salt, then squeeze, then egg + feta + self-raising flour; the oven route with a cornmeal coat; the pan route with a rest | nothing (new additions only: feta, self-raising flour, cornmeal) |
| H3 | chawanmushi (A8a) | partly | the custard as a mix of egg and three volumes of cooled dashi, strained; claims "not aerated" and "strained" checked | **`cuire_vapeur` requires a solid** ("steams a solid"): steaming a liquid that sets would need the same `sets_on_heat` waiver `frire`, `rissoler` and `cuire_four` got before the freeze. The cup (a mould) is not represented |
| H4 | farcis niçois (M16a, M16b) | partly | the courgette vessel and its recombined flesh, bread soaked in milk (`tremper` on a new staged part) | **several vessels share one filling** (one container per assembly); **`rotir` refuses courgette** as too watery to brown, though M16b roasts it soft at 160 C; the tomato vessel fails as in gemista |
| H5 | pierogi ruskie / vareniki (E16a, E16b) | partly | the cooled potato filling (C2), the boiled parcel, the claim that the filling is cooled | **doughs**: the dough's flexible, rolled state is asserted, because `abaisser` (roll out) has no outputs and there is no dough material; sealing, scalding (H3) and starch in the cooking water are not operations or properties |
| H6 | spanakopita / ıspanaklı börek (M8a, M8b) | partly | salt-squeezed spinach (M8a); raw spinach whose water is managed by wetting the yufka less (M8b, W8), with the claim checked; bought yufka as an addition layer | **doughs** as in H5 (M8a); washing is not an operation (as rinsing in A1b) |
| H7 | zha qie he (A12a, A12b) | partly | the filling, the coats, the second fry (allowed for assembled pieces) | **a hinged pocket (连刀)**: no operation makes two joined slices into a container, so `farcir`'s container check fails ("a hollow to fill"); starch dusted inside as glue has no role |
| H8 | moi moi (A19a, A19b) | partly | the akara paste unchanged (soak, skin, grind) and the claim "not aerated, still raw" | **`cuire_vapeur` refuses the paste** as not "tender enough to steam through": `mixer` sets a paste's firmness but leaves the dried seed's toughness, a state-update error of R1's kind. The mould is not represented |

## What this says about reusability

**The model is reusable, not merely accommodating its 27 dishes.** The
evidence:

- **The parts of the model that came from the design set carried over
  unchanged.** All six joins, the role checks, recombination, `expects` and
  `final` claims, routes and the seven new single-material operations
  (`tremper`, `decortiquer`, `creuser`, `fendre`, `reposer`, `refroidir`,
  `faconner`) were used by held-out dishes they were not designed for:
  - `tremper` soaked bread (farcis), not only pulses;
  - `decortiquer` and the akara paste carried straight into moi moi;
  - `creuser` and `farcir` carried into farcis;
  - `degorger` + `decanter` returned starch in draniki by a water route the
    design set never used for it (salt first, E5a);
  - `superposer` held yufka sheets and a sauce, which no design dish had.
- **The easy case needed nothing.** Draniki is the design set's nearest
  relative; it fitted with no new term at all. Kolokythokeftedes needed only
  three new additions.
- **83 of 86 held-out steps were applicable.** None was unknown: the property
  vocabulary was enough to judge every step.
- **4 recombination links were found** in held-out data without any change.

**But the failures are not random, and three of them are structural:**

1. **Steaming a setting liquid** (chawanmushi, moi moi). The design set had
   no steamed dish, so the `sets_on_heat` exception reached frying, pan and
   oven but not steam. This is the model accommodating its design set: the
   exception was written per operation, as dishes needed it, instead of as
   one statement about materials that set on heat.
2. **Doughs** (pierogi, spanakopita M8a). The design set had no dough
   wrapper, so a dough can only be asserted. R2 had already flagged doughs as
   unmodelled; the held-out set confirms they are the largest missing
   material class (C7c).
3. **Containers that are not hollowed** (zha qie he's hinged pocket) and
   **dishes of several containers** (farcis, as gemista in the design set).
   The container relation assumes one scooped vessel.

And two R1 errors surfaced that the design set did not hit:
- `mixer` does not lower toughness (moi moi);
- `rotir` forbids a very watery vegetable even when it is roasted slowly
  until soft (farcis M16b).

**Verdict.** The structure (materials with operation paths, joins with
roles, derived recombination, cited claims) generalised: no held-out dish
needed a new field, a new relation or new code to be *described*. What did
not generalise are particular operation requirements, one missing kind of
material (doughs) and two kinds of container (pockets, several vessels).
Every held-out *failure* would be removed by operation-level changes (a
`sets_on_heat` waiver on `cuire_vapeur`, `mixer` lowering toughness, outputs
for `abaisser` with a dough material, a pocket-making operation); only "several
containers" touches the schema (a role that takes a list). The remaining
model gaps (moulds, washing, the inside of an assembly) are the same kinds the
design set already recorded. That is the list R4 needs (`r4-needs.md`).

Measured the same way as the design set:

| | Design set (27) | Held-out set (8) |
| --- | --- | --- |
| dishes fully represented | 13 (48%) | 2 (25%) |
| routes fully represented | 26 of 43 (60%) | 4 of 14 (29%) |
| main-path steps applicable | 236 of 236 | 83 of 86 |
| dishes with an inapplicable step or role | 2 | 4 |

The drop from design to held-out is the honest size of the accommodation:
the design-set fit overstates how far the model reaches. Measured on dishes
it had not seen, a quarter fit fully and every one is at least partly
described, with each shortfall named.

## After the post-freeze validator amendment A1 (PR #7 review, 2026-11-24)

*Added after R3; the held-out results above are the original R3 record and
are not changed.*

**What changed.** After the held-out step, review of PR #7 found two faults
in the validator (`constructions.py`) by static inspection. Both were
reproduced with tests that failed on the frozen code before it was changed:
- **Recombination** was counted whenever a fraction reached the result,
  because reachability follows a fraction back to its source; extraction
  alone (potato pressed, only its juice used) would have counted. It now
  needs two materials of the same origin, each entering the dish by its own
  route; intermediates that never enter the dish are walked through.
- **Edibility at joins.** An assembly took only its carrier's edibility, so
  an edible shell could hide a non-food filling. A join is now not food if any
  member is not food, with R1's reason, so the steps after it are unsafe or
  inapplicable.

**How the freeze was kept.** The original manifest `construction_freeze.yaml`
is unchanged and a test pins its bytes. The correction is recorded as
amendment A1 in `src/foodprep/data/construction_freeze_amendments.yaml`
(date, reason, what changed, effect, the new hash of `constructions.py`). The
freeze test accepts exactly the original manifest plus documented amendments
and fails on any undocumented change; `run.py --freeze` refuses to overwrite
the original. A1 changed only the checker: operations, schema, property keys
and `operations.py` are as frozen, so the held-out dishes are still expressed
in the vocabulary that existed before they were seen.

**Results on the corrected validator** (`generalisation-tables-a1.md`,
compared route by route with the original `generalisation-tables.md`):

| | Original R3 | After A1 |
| --- | --- | --- |
| held-out dishes fully / partly / not | 2 / 6 / 0 | 2 / 6 / 0 |
| held-out routes fully / partly / not | 4 / 10 / 0 | 4 / 10 / 0 |
| held-out recombination links | 4 | 4 |
| design dishes fully / partly / not | 13 / 14 / 0 | 13 / 14 / 0 |
| all recombination links (design + held-out) | 13 | 13 |

| Held-out dish | Original R3 | After A1 | Change |
| --- | --- | --- | --- |
| draniki | fully | fully | none |
| kolokythokeftedes | fully | fully | none |
| chawanmushi | partly | partly | none |
| farcis niçois | partly | partly | none |
| pierogi ruskie / vareniki | partly | partly | none |
| spanakopita / börek | partly | partly | none |
| zha qie he | partly | partly | none |
| moi moi | partly | partly | none |

No dish gained or lost a recombination link: the four held-out links
(draniki twice, farcis twice) already joined two materials entering the dish
by their own routes, and no held-out dish has a non-food member. The
conclusion about reusability above is unaffected.
