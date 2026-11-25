# R4: controlled transfers, practical discovery

**Question.** Can the system help us find something useful to cook?

R1-R3 described transformations, identified construction mechanisms and
represented 35 documented dishes. R4 is the first test of practical value: take
a documented construction, carry it over to another ingredient a Finnish home
cook can buy at Lidl, and decide from the evidence whether the result is
**good food**, not merely something that holds together. Rejecting a
candidate counts as a result. Plan and earlier rounds: `../roadmap.md`.

Branch `claude/determined-ardinghelli-a9d75d`, from main after PR #7
(c1629d6). Nothing was cooked in this round.

## Answer

**Yes, five things worth cooking were found, but the search found them and
the model checked them.** Each one is made and liked somewhere, has one known
way to go wrong, and fits a Finnish kitchen and (mostly) Lidl's shelf. None
is new to cooking, and four are new to the Finnish table. The model explains
each one's structure (why it holds) and agrees with the evidence on every
transfer it can be compared on. That holds only after one small, documented
extension, made because the most promising transfer exposed a real gap. It
cannot judge quality, which is what decides every one of these dishes. That
is the kitchen test's job.

| Candidate (base dish) | Lidl FI | Verdict | Why | The one condition |
| --- | --- | --- | --- | --- |
| **Potato and rutabaga gratin** (gratin dauphinois) | rutabaga in season now; all else regular | **worth cooking** | UK, Irish, German, Swiss, North American practice; cheap, Finnish, seasonal | blanch **only the rutabaga** 3-5 min, or it stays crunchy (G20, G21) |
| **Hollowed onion halves** (stuffed courgette) | onions regular | **worth cooking** | Nice and Liguria do it the courgette's way, in the same tray | do not overboil: the layers slip apart |
| **Napa-cabbage rolls** (kaalikääryleet), replacing kale | not confirmed | **worth cooking** | Japan, Germany, Russia: liked, easier to roll than cabbage | shave the thick rib; bake covered with some liquid |
| **Falafel from dried peas** (falafel) | split peas only in a campaign | **worth cooking**, as a comparison | German, British, Swedish, Indian (vatana vada) practice; holds with no binder | it can come out dry and hard (P15): grind coarse, keep the onion and herbs |
| **Broccoli-stem patties** (carrot patties) | fresh broccoli not seen | **worth cooking**, for a part already bought | recent zero-waste recipes, no failures | peel the stem; mix with carrot (one stem is 100-150 g) |
| Kale-leaf rolls (kaalikääryleet) | curly kale, small bags, Aug-Oct | **not worth it** | every kale roll uses large flat kale; curly is untested and fiddly | replaced by napa cabbage |
| Raw rutabaga in the gratin (control) | - | **rejected** | documented failure (G20, G21) | kept to test the model |

**What the model contributes**, in practice:
- a checklist of what a substitute must do, taken from the documented
  dish: bend and be large enough to wrap; supply starch to the dairy; stand as
  a large blanched half; set on heat when raw;
- one real correction: it accepted raw rutabaga in a gratin, which cooks
  report fails. Amendment A2 (data only: `cooks_slowly` and one layer
  requirement) fixes it with **no effect on any of R3's 57 routes**;
- a record of each transfer's assumptions that a kitchen test can falsify.

**What it cannot do:** say whether any of it tastes good (dry falafel, sharp
rutabaga, stringy rib); handle time (a 90-min covered bake, overboiled
onions); express several pieces as one member (two small leaves as one
wrapper; one filling for two kinds of vessel). Two of its agreements (peas set
on heat; curly kale leaves too small) rest on properties set from the same
evidence, so they are not independent support (`model.md`).

**Lidl.** lidl.fi shows only current offers; the regular range (about 3000
products) is not online, and expired offer pages are deleted. So "not found"
usually means unknown. Rutabaga, potatoes, dairy, eggs and onions are
established. Dried peas, fresh broccoli and napa cabbage need a shelf check
(`catalogue.md`).

## Documents

| File | Contents |
| --- | --- |
| `catalogue.md` | Step 1: the Lidl FI boundary, method and its limit, status per item, what changed in the ingredient data |
| `lidl-pages.md` | The Lidl page-by-page record (ids L1-L18; napa and pointed cabbage L19-L26 are in `evidence-napa.md`), failed pages, method |
| `candidates.md` | Steps 2, 3, 5: per candidate, availability, documented practice, quality evidence, verdict |
| `evidence-pea-falafel.md`, `evidence-kale-onion.md`, `evidence-napa.md`, `evidence-gratin-stems.md` | The research notes: every source read (P, K, O, N, G, B ids), search logs per language, failed pages, synthesis |
| `sources.md` | Generated index: every evidence id with the URL read |
| `model.md` | Step 4: what the model explains and cannot, per transfer; agreement with the evidence |
| `model-tables.md`, `model-tables-before-a2.md` | Generated: each transfer through the R3 validator, after and before amendment A2 |
| `limitations.md` | Step 6: the one extension (A2) and its zero effect on R3; the limitations recorded, not fixed |
| `kitchen-tests.md` | One test per transfer worth cooking: what to compare, how to judge, taste, when to stop |
| `evaluation.md` | Against the brief's criteria; behaviour changes; cost; limits; what R5 should take |
| `run.py` | Writes `sources.md` and `model-tables.md`: `py -3.11 docs/research/r4-transfers/run.py` |

## What was built

- **`src/foodprep/data/transfers.yaml`**: seven transfers as changes to
  documented routes, each with Lidl availability, evidence ids, what the
  evidence says, a verdict with reasons, the model's explanation and limits,
  and a kitchen test. No scores.
- **`src/foodprep/transfers.py`**: derives a transfer's route and runs R3's
  validator on it **unchanged**, next to the base route; accepts R4 evidence
  ids where R3 expects R2 recipe ids; reports whether the model holds and
  whether it agrees with the evidence. CLI: `foodprep transfer [id]`.
- **Data**: `dried_peas` and `napa_cabbage` ingredients, Lidl notes on
  rutabaga, kale and broccoli (`tomato.yaml`); staged parts `rutabaga.root`,
  `kale.leaves`, `dried_peas.dried_seed`, `napa_cabbage.head`
  (`part_properties.yaml`).
- **Amendment A2** (`construction_freeze_amendments.yaml`): `cooks_slowly`
  and the `superposer` layer requirement; `rutabaga.root` is slow.
- **Tests**: `tests/test_transfers.py` (21): data well formed, every cited id
  resolves to a URL, the derived routes have no structural errors, pinned
  model verdicts and agreement, A2's effect, generated tables current, CLI.
