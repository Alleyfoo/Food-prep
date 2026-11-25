# R5 evaluation

Against the brief, and the scope change the user made during the round.

## Against the question

| Asked | Result |
| --- | --- |
| 15-25 (part, operation) pairs from steps R3/R4 use, chosen before research | 25, written and committed (5e79923) before any source was read (`pair-selection.md`) |
| Conditions per pair, unknown otherwise | 25 pairs: 24 with an observable completion condition, 25 with failure conditions, 23 with both documented elapsed time and kind of active work; missing fields left unknown |
| Elapsed apart from active | `elapsed` is a list of each source's ranges; `active` is a kind (continuous, regular, occasional, none). Soaking is many hours of `none`; frying is minutes of `regular` (tested) |
| Observable completion primary, time a guide | Completion checks are the main field of every step; times are shown as each source's own range |
| Conflicts kept as versions | 43 on pairs, 31 alternative sequences; nothing averaged (tested: at least two distinct versions each) |
| Condition belongs to the step in a dish; default only where sources agree | Pairs carry a `default` and per-step `at`; sequences carry per-step fields; `for_step` merges default, then step |
| Intermediate states as starting points, reusing R1/R3 equivalence | `foodprep from`, by R1 `Material.key()`; also flags and step addresses; 17 states |
| Keeping times from food-safety bodies | 10 of 17 states have a food-safety rule (Ruokavirasto, FSA, FSS, NHS, BfR, Mattilsynet, FSAI, two US extensions); the rest are marked home economics or cooking, or not found |
| Multilingual, Finnish, Lidl packets, R2/R3 ids | 187 sources in 15 languages (Finnish, Swedish, Norwegian, German, French, Italian, Polish, Russian, Turkish, Greek, Arabic, Hebrew, Japanese, Korean, English varieties); Lidl packets not reachable (recorded); 86 R2/R4 ids reused |
| Every URL read recorded; failures recorded; no invented URL | Each evidence file lists every source read and every failed or snippet-only page. One constructed URL was fetched (404, unused, flagged) |
| Raw-text spot check | 12 pages, below |

## Against the scope change

| Asked | Result |
| --- | --- |
| The unit is the whole sequence | 10 sequences: the five worth-cooking transfers and their five kitchen-test bases, every route step present (validator refuses a missing step) |
| Readiness against doneness per step, with the source | 54 steps: 44 readiness, 10 doneness; 45 cite a source, 9 by route order alone |
| Heat after the join, per member | Every material inside a heated assembly has an entry (validator-enforced); 22 of 28 entries have an endpoint, 6 say "not found" |
| Dependencies between stages | 23 links, each pointing forward along the route (tested) |
| Skipped or overdone stages | 22 failures with `skipped`, `underdone` or `overdone` |
| Conflicts at sequence level | 31 alternative sequences, kept apart, linked to an R3 route or R4 transfer where one exists |
| "From this state" returns the remaining sequence and flags readiness | Yes: remaining steps include the bake or fry after the join, this member's endpoint there, the dependency, the rest; "not ready to eat" for a readiness state |
| How much is documented end to end | README: every step of the ten sequences has an endpoint kind and at least the route's own evidence; the evidence stops at six member endpoints, pea-specific checks, Lidl packets and raw-intermediate keeping times |

## Raw-text spot check

The evidence agents read pages through WebFetch, which returns a model-written
summary. Twelve pages, across eight languages and all five evidence files,
were fetched again as raw HTML (urllib, tags stripped). Each was searched for
the endpoint wording the evidence file paraphrased.

| Id | Language | Paraphrase checked | Raw text |
| --- | --- | --- | --- |
| Q111 | English | chickpeas soft enough to chop with a knife, still firm and mealy; sprouting | confirmed |
| Q129 | English (Nigerian) | skewer comes out clean after about 50 min; skins start wrinkling after 3 min | confirmed |
| Q203 | French | knife point goes in with no resistance | confirmed ("aucune résistance") |
| Q231 | English (German site) | blanch 3 min until crisp-tender; rutabaga is very dense, needs longer than potato | confirmed |
| Q232 | English (Irish) | simmer 5 min, tenderised slightly but not fully cooked | confirmed |
| Q302 | Finnish | 1 tsp salt per litre; peel leaves as they start to soften | confirmed |
| Q317 | Polish | about 2 min; "elastyczne, ale nie ugotowane"; too long and they fall apart when rolled; rice slightly al dente because it softens in the bake | confirmed |
| Q330 | Italian | 10 min only, half-cooked | confirmed ("solo a metà cottura") |
| Q400 | Turkish | squeeze until no water is left in the courgette | confirmed |
| Q428 | Japanese | peel thick, about 5 mm; the outer green is hard | confirmed |
| Q510 | Finnish | rutabaga 2-3 min for freezing, row ambiguous | confirmed, including the ambiguity |
| Q519 | English (UK) | rice: chill within an hour ideally, fridge at most 24 h, reheat once | confirmed |

12 of 12 confirmed. The first search for Q317 hit an earlier word and looked
like a miss; a second search found the phrase. R4 had no spot check; R2
checked 12 of 127.

## Frozen results: unchanged

- `construction_freeze.yaml` and `construction_freeze_amendments.yaml` are
  unchanged. So are `constructions.py`, `operations.py`, `transfers.py`,
  `constructions.yaml`, `operations.yaml`, `transfers.yaml`,
  `part_properties.yaml` and `tomato.yaml`, and every document in
  `r3-construction-modelling/` and `r4-transfers/`. `git diff main` on
  these paths is empty.
- R3's `run.py` (the `-a1` tables) and R4's `run.py` (`sources.md`,
  `model-tables.md`) were rerun on this branch: byte-identical, no diff.
- No amendment A3: the conditions layer reads the routes and walks them with
  `operations.apply`, as the R3 validator does, and writes nothing back
  (tested: R3 and R4 data equal before and after walking every route).
- The family-generator fingerprint test passes.

## Tests

- `tests/test_conditions.py`: 31 tests.
  - The data is well formed and every evidence id resolves.
  - 15-25 pairs, each on a documented step.
  - No scoring or prediction fields; every time and check is cited.
  - Conflicts are kept as versions; active and elapsed are distinct.
  - Every worth-cooking transfer is a whole sequence.
  - Readiness and doneness per step, with the rutabaga blanched AND baked.
  - Member endpoints after joins; dependencies point forward; skip and
    overdo failures; alternatives kept.
  - `from` with operations, flags and step addresses, using R1 equivalence.
  - Food-safety keeping times come from public bodies.
  - R3 and R4 data are untouched; the generated tables are current; the CLI.
- Full suite: **1013 passed** (982 before R5, plus 31).

## Behaviour changes

Two new CLI commands (`conditions`, `from`), one new module, one new data
file. No existing command, test or output changed.
