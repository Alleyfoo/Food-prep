# R5: documented processing conditions

**Question.** For the steps that the documented dishes (R3) and the
worth-cooking transfers (R4) use, can Food-prep record **what you actually
need to do**: under which conditions, for how long (elapsed and active), how
you know it is done, and how you know it failed? And can it say what you can
do **from an intermediate state you already have**?

**Scope change during the round (from the user).** The unit is the **whole
processing sequence**, not the isolated operation: each component from raw
part to plate, including what it goes through after it is joined. "The 3-5
minutes of blanching isn't intended to make the rutabaga edible. It's
intended to make it ready for the next operation." So every step says whether
its endpoint is **readiness** (ready for the next operation) or **doneness**
(ready to eat); every member of an assembly has its own endpoint in the heat
after the join; stages that exist because of a later one are linked; sources
that split the work differently are kept as alternative sequences
(`pair-selection.md`, last section).

Branch `claude/r5-processing-conditions-e51e0f`, from main after PR #8
(fd6e886). Nothing was cooked. Plan and earlier rounds: `../roadmap.md`.

## Answer

**Yes, for most of it, and only from documented practice.** Food-prep now
records, for the five R4 dishes worth cooking and their five kitchen-test
bases, every step from raw part to plate:
- the conditions,
- the elapsed time as each source gives it,
- the kind of active work,
- an observable done-when check,
- what failure looks like and its stated cause,
- and whether the step makes something ready for the next step or ready to eat.

It says what each member of an assembly goes through after the join, and
why some stages exist. Given a state you have, `foodprep from` lists the
documented routes that pass through it and the rest of the sequence, and
says plainly when what you have is **not ready to eat**. No time or endpoint
is derived, averaged or predicted; conflicting instructions stay as
separate versions.

The rutabaga, end to end, as the data now records it
(`foodprep conditions transfer:rutabaga_gratin`):

| Stage | Endpoint kind | Time (each source's own) | Done when | Failed if |
| --- | --- | --- | --- | --- |
| peel | readiness | - | - | - |
| slice | readiness | - | 2-3 mm (Q231, Q232) | - |
| **blanch** | **readiness** | 3 min (Q231, G1); 4 (Q233); 5 (Q232); about 10 (G16, G18) | "crisp-tender": softened slightly, not fully cooked (Q231, Q232) | skipped: still crunchy when the potato is done (G20, G21) |
| layer with raw potato and cream | (a join) | - | - | - |
| **bake** (the rutabaga inside the gratin) | **doneness** | 55-60 min covered then uncovered (Q231); 40-50 (Q233); 60-80 (Q232) | some give, al dente (Q231) **or** no resistance (Q232, Q233, Q234): a conflict, kept | still crunchy: not blanched (G20, G21) |
| rest | finishing stage | a few minutes (Q231); 25 min (Q234); 1 h warm (Q232) | - | - |

It records **why**: rutabaga is denser than potato and needs longer in the
same bake (Q231, Q234), so the blanch exists because of the bake. It also
records four alternative sequences: raw slices and a 90-min covered bake (G7,
G8), a simmer in the gratin liquid (G5, G9), pre-cooking both (Q232), and the
rejected raw short bake.

### In numbers

- **25 pairs** (part, operation), chosen from route steps before any reading
  (`pair-selection.md`):
  - 24 have an observable completion condition; 25 have failure conditions;
  - 23 have both a documented elapsed time and a documented kind of active work;
  - 43 conflicts are kept as versions;
  - confidence: 19 established, 2 documented, 4 conflicting.
- **10 sequences, 54 route steps**: the five worth-cooking transfers whole,
  plus their five kitchen-test bases whole.
  - Every step has an endpoint kind: 44 readiness, 10 doneness. 45 cite a
    source for it; 9 rest on route order alone, mostly peeling.
  - 47 steps have a done-when check; 32 have a failure check; 22 a documented time.
  - 22 of 28 member entries after a join have their own endpoint.
  - 23 dependency links, 22 skip/underdo/overdo failures, 31 alternative sequences.
- **17 intermediate states** with how long they keep. 10 of them carry a
  keeping rule from a public food-safety body: Ruokavirasto, UK FSA, Food
  Standards Scotland, NHS, BfR, Mattilsynet, FSAI, and two US university
  extensions.
- **187 new sources** (Q ids) read in 15 languages; 142 are cited in the
  data, plus 86 R2/R4 ids. A raw-text spot check of 12 pages confirmed every
  sampled paraphrase (`evaluation.md`).

### What worked

- **Readiness against doneness is documented, in so many words.**
  - Rutabaga "crisp-tender" and "will not be fully cooked" (Q231, Q232).
  - Courgette "solo a metà cottura", only half-cooked (Q330).
  - Napa leaves "elastyczne, ale nie ugotowane", flexible but not cooked (Q317).
  - Rice "lekko al dente" because it softens in the oven (Q317).
  - The same operation runs to fully soft in another role: rutabaga for
    lanttulaatikko (Q210, Q216), onion layers that must roll (Q329, O15).
- **Dependencies are stated by cooks.**
  - Blanch because the bake alone is too slow for a dense root.
  - Soak the peas for the raw grind: split peas need no soak for soup
    (Q104-Q106), but every falafel soaks them.
  - Keep chickpeas raw because the paste must set in the oil.
  - Half-cook the rice because it finishes in the roll.
  - Peel the broccoli stem because the skin stays tough.
- **Failure checks are concrete and observable.**
  - Layers slip or tear (O12, O15).
  - The ball falls apart in the oil, with eight documented causes.
  - The patty breaks when turned before it sets.
  - The leaf tears or will not bend.
  - The knife meets resistance.
- **Active against elapsed time** separates cleanly. Soaks, chills and
  bakes are waiting; frying, skinning and squeezing are continuous or
  regular work; blanching a cabbage head is regular (lift, peel, return).

### Where the evidence stops

- **Inside the assembly, for minor members.** No source states an
  endpoint for:
  - the onion inside a falafel ball;
  - the cream in a rutabaga gratin;
  - the egg in a vegetable farci;
  - the rice after a cabbage-roll bake;
  - a grated stem inside a patty.

  The kitchen test is the only evidence there.
- **Peas specifically.** No observable "soaked enough" test, no over-soak
  failure, no "cooked through" check for a pea falafel. Finnish packet
  text was unreachable (Lidl's pages are 404; S-kaupat pages truncated).
- **Lidl Finland.** No packet text at all; other brands' packets (Foodin,
  Kymppi, Ben's Original, Myllyn Paras, Kespro) stand in and are marked.
- **Keeping times for raw intermediates.** Nobody gives a fridge time for:
  - soaked uncooked pulses;
  - blanched unfrozen vegetables;
  - salted grated courgette;
  - boiled potatoes, from an authority.

  Ruokavirasto gives cooling rules (+6 °C within 4 h) but no day counts.
- **Food safety of raw-soaked falafel.** Ruokavirasto says beans must never
  be eaten only soaked (Q505), and the pea and chickpea packets say "not
  untreated". No body read says whether deep-frying a raw pulse paste is
  that treatment. Recorded as a gap, not resolved.

### How it feeds R6 (the interface)

- The unit to show is a **sequence with the member you have highlighted**:
  what is done, what remains, the next step's done-when and failed-if
  checks, and the one dependency that explains it ("blanch: the bake alone
  won't soften it in time").
- `foodprep from` is the "cook now or prepare for tomorrow" primitive.
  It gives the remaining steps with times and kinds of work, plus how long
  the state keeps and on whose authority. It says "not ready to eat" for a
  readiness state. Nothing here plans meals.
- Show conflicts as choices ("3-5 min, or 10 min until almost tender"),
  never one merged number. Show "not found" as itself.
- Kitchen-test results (`kitchen-tests.md`) should write back to the
  sequence's member endpoints, because that is where the evidence stops.

## Documents

| File | Contents |
| --- | --- |
| `pair-selection.md` | The 25 pairs, chosen before reading; the scope change and the 10 sequences |
| `research-brief.md` | The brief the five evidence agents followed (rules, fields, output format) |
| `evidence-pulses.md`, `evidence-gratin-potato.md`, `evidence-vessels-leaves.md`, `evidence-patties.md`, `evidence-holding.md` | Every source read (Q100-Q551), failed pages, searches per language, synthesis per pair, sequence notes |
| `sources.md` | Generated: every Q id with its URL |
| `condition-tables.md` | Generated: every pair, its default, its per-step fields, conflicts, gaps |
| `sequence-tables.md` | Generated: every sequence member by member, raw to plate |
| `intermediate-tables.md` | Generated: each intermediate state, how long it keeps, the routes through it |
| `conflicts.md` | The notable conflicts, at pair and sequence level |
| `intermediate-states.md` | What "from this state" supports, and the batch-preparation reading |
| `kitchen-tests.md` | R4's kitchen tests with concrete completion and failure checks |
| `limitations.md` | What was not found, and what the model does not do |
| `evaluation.md` | Against the brief; spot check; frozen results; tests |
| `run.py` | Writes the generated files: `py -3.11 docs/research/r5-processing-conditions/run.py` |

## What was built

- **`src/foodprep/data/processing_conditions.yaml`**: a controlled vocabulary;
  25 pairs; 10 sequences; 17 intermediate states. Every value cites sources.
- **`src/foodprep/conditions.py`**:
  - loads and validates the data: fields, vocabulary, parts, operations,
    whole-route coverage, member coverage after heat, forward dependencies,
    and every evidence id resolving to a page that was read;
  - walks R3 routes and R4 transfers with `operations.apply`, as the R3
    validator does, without changing them;
  - answers `for_step`, `for_pair`, `render_sequence` and `from_state`.
    `from_state` uses R1's `Material.key()` equivalence and also accepts
    state flags and step addresses.
- **CLI**:
  - `foodprep conditions [pair | ingredient[.part] | dish[/route] | transfer:<id> | step]`;
  - `foodprep from <ingredient.part> [operations or flags...]`;
  - `foodprep from <step address>`.
- **Tests**: `tests/test_conditions.py`.
- `constructions.py`, `operations.py`, `transfers.py`, their data and every
  frozen table are unchanged. No amendment A3 was needed.
