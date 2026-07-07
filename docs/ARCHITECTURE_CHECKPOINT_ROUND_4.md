# Architecture Checkpoint — Round 4

> Freeze of the mental model as of the end of Round 4, before the Round 5
> filler pack and the Round 6 cabbage tree. The project is now just complex
> enough that future-me or agent-me can accidentally flatten it. This file
> exists so the distinctions below stay distinct.

## The one line to remember

**Co-occurrence can support evidence, but `curated_role_fit` owns the culinary
role.**

That prevents the future CulinaryDB goblin from declaring that garlic fixes
desserts because it saw garlic near everything. CulinaryDB (or FlavorDB, or any
corpus) tells you *that two ingredients appear together*. It does not tell you
*what role one fills for the other*. Garlic + onion co-occur ~8000 times in
CulinaryDB — and that is real evidence — but garlic fills **aromatic** for
onion, not acid, not crunch. The corpus count goes in
`pairings.corpus_cooccurrence_count`; the culinary judgement of which role that
co-occurrence actually supports goes in `pairings.curated_role_fit`. The count
can be huge and the role-fit still "no, that's the wrong role." Both are
allowed to be true at once.

## The terms, frozen

### full ingredient
An ingredient that deserves a **technique tree** — a set of
`ingredient → technique → component` transformations with per-state missing
roles. Currently `tomato`, `onion`, `potato`. A full ingredient is where the
*transformation record* (the core object of this project) actually lives.
`kind: full`. The test of "full" is: does this ingredient change character
meaningfully across techniques, and do those states have *different* missing
roles? If yes → full. If a single role-filler would do → filler.

### filler ingredient
An ingredient that fills a role and needs no technique tree. Most pantry items
(lemon, vinegar, cream, mustard, …). `kind: filler`. They have `base_roles`
(what they provide) and appear in `pairings` (which missing role they fill for
which transformation). They do **not** have transformation rows of their own.
The plate engine suggests them via `_fillers_for_role`, which reads pairings —
so a filler with no pairings is invisible to the plate engine.

### both ingredient
Has a technique tree **and** still appears as a filler in other ingredients'
pairings. Only `potato` so far (`kind: both`): it has boil/mash/roast/… and it
is also a `mild_base` filler for tomato/pickle. This is the escape hatch for an
ingredient that is genuinely both a transformation subject and a role provider.
Do not reach for `both` lightly — if an ingredient is mostly a filler, leave it
`filler`.

### component profile
A **plate item that is not a transformation output** — or not one we model as a
tree. `mashed_potatoes`, `pasta`, `bread`, `chickpea_patty`, `green_salad`, …
Lives in `component_profiles` (separate YAML file, richer schema:
`provides_roles` / `flavour_tags` / `texture_tags` / `missing_risks` /
`heaviness_score` / `dryness_score`). This is the table that lets the engine
reason about *meals*, not just tomato. A component profile is the unit the
plate balance engine evaluates. A raw ingredient on a plate (onion, butter)
that has no profile is recognised as an `ingredient` (base_roles count) and
warned for lacking balance data — softer than "unknown", still honest.

### transformation
The **core object** of the project: `ingredient → technique → component →
missing roles → next ingredient`. One row in `transformations` plus its
`transformation_missing_roles`, `transformation_tags`, and `component_uses`.
This is *not* a recipe. The centre of gravity is the transformation record and
its missing-role gaps, not ingredient→ingredient co-occurrence.

### missing role
A role a transformation's output component tends to lack, curated by hand with
a priority (`high`/`medium`/`low`) and a note. This is the **scarce, valuable
layer** — it is hand-authored, not corpus-derived. It is what makes "I roasted
tomatoes, now what?" return a *useful* answer instead of a flat dump. Missing
roles differ by state: raw tomato needs carrier; roasted needs acid; sauce
needs aromatic + carb. If they didn't differ, the data would be generic and
worthless.

### target_gap
**Hard gaps** = `TARGET_ROLES − provided` on a plate, where
`TARGET_ROLES = [salt, fat, acid, herb, crunch, carb, protein]`. These are the
roles *no* plate item provides, so they definitely need filling. In the plate
balance output this is "missing for a balanced plate:". Fillers are suggested
grouped by these roles.

### flagged_more
**"May want more"** = roles that *some* item provides but a profile still lists
in `missing_risks` (e.g. `roasted_tomato` provides acid yet also flags acid: "a
little acid, may need more if too sweet"). These are soft suggestions, kept
*strictly separate* from `target_gap`. This is the distinction that stops the
engine from telling you to "add protein to a gratin that already provides
protein." In the output this is "also flagged by item profiles (may want more):".

### Cook mode
The default plate-balance / meal-repair mode. `plate_balance` is labelled
"Cook mode" and `_fillers_for_role(..., include_experimental=False)` **excludes
`experimental` pairings** — those are Scout's, not Cook's. Cook answers "what is
missing on this plate?" with classic, well-evidenced fillers only.

### Scout mode
`scout()` — experimental pairings, explicitly labelled "Scout / experimental"
and "NOT classic". Surfaces pairings with `confidence: experimental`
(e.g. `rye_crumbs` + roasted tomato). The label is the point: no one pretends
these are tradition. Cook and Scout are **separate code paths** with separate
labels, verified by `test_cook_and_scout_are_separate`.

### plate balance
`query.plate_balance(conn, text)` — the Round 4 engine. Evaluates a set of
plate items: aggregates provided roles (profiles + ingredient base_roles),
aggregates `missing_risks`, computes plate-level heaviness/dryness with a
qualitative read, derives `target_gap` + `flagged_more`, suggests fillers
grouped by role (Cook mode), and warns about items with no profile. Honest
about limits — it never invents roles or fillers it doesn't have. Backward-compat
alias `meal_repair`.

### corpus evidence
`pairings.corpus_cooccurrence_count` + `pairings.corpus_contexts`, populated by
`foodprep backfill <CulinaryDB-dir>` (`src/foodprep/corpus.py`). Keyed by
**Entity ID** (CulinaryDB file 02 is Title Case, file 04 is lowercase — only
Entity ID is stable across them; the name intersection is zero). This is
**evidence, not truth**: it never touches curated `confidence` or
`curated_role_fit`. 122/144 pairings got evidence on the real corpus; 22
resolved to 0 (olive_oil, pasta_water, …) — honest "no corpus evidence", not a
bug.

### curated role fit
`pairings.curated_role_fit` — the **guardrail field**. Hand judgement of
whether a corpus co-occurrence actually supports *this* pairing's role. The
whole ontology's resistance to "seen together = good." Currently 2 pairings
annotated (garlic+onion/saute, tomato+onion/saute) to prove the field is real
and populated. Extending this annotation is the single highest-value,
lowest-risk future task: it is where the corpus gets checked against culinary
reality.

## Non-negotiable distinctions (do not flatten these)

1. **Transformation record ≠ recipe.** Centre of gravity is the transformation
   and its missing roles. Recipes are downstream; we do not store them.
2. **Missing roles are hand-curated, never corpus-derived.** Co-occurrence
   invents nothing here.
3. **`target_gap` (hard) vs `flagged_more` (soft).** A role the plate provides
   is not a hard gap, even if a profile flags it. Never merge these two lists.
4. **Cook excludes experimental; Scout surfaces it.** Never let an
   `experimental` pairing leak into a Cook-mode answer unlabelled.
5. **`kind` guards the hedgerow.** `full` gets a tree; `filler` gets a role; \
   `both` is the rare escape hatch. Not every ingredient needs the full
   tomato/onion treatment — that is how the ontology becomes a hedgerow.
6. **Profiles ≠ transformations.** A plate item with no transformation tree
   (mash, beans, bread) is a `component_profile`, not an ingredient tree.
7. **Co-occurrence is evidence of presence, not of role.** That is the one
   line. `curated_role_fit` is the wall between them.

## What is deliberately NOT in the model (anti-hedgerow calls on record)

- No `final_confidence` column — redundant with `confidence`, which *is* the
  final curated truth.
- No "freshness" role — freshness is delivered *by* acid or herb in context;
  `MISSING_TERM_TO_ROLE` maps the cook-term "freshness"/"fresh_side" to `herb`.
  Adding a freshness role would be a hedgerow.
- No corpus-derived role invention. Ever.
- No per-ingredient "popularity score" or auto-ranking from co-occurrence.

## Where Round 5 / Round 6 plug in (without flattening)

- **Round 5 — filler pack**: adds `repairs` + `avoid_when` metadata to fillers
  and a `filler_profile` view answering the five questions (roles / repairs /
  avoid / Finnish availability / Cook-or-Scout). These are **per-filler
  profile data**, surfaced via `filler_profile`. They are *not* a plate-condition
  matcher inside `plate_balance` — wiring `avoid_when` into the engine is a
  deliberate future step, deferred so it isn't a half-baked condition layer
  that flattens the model. The plate engine benefits from the pack because the
  new fillers add `base_roles` + pairings → more Cook-mode suggestions.
- **Round 6 — cabbage**: the next *full* ingredient. Gives raw crunch / salted
  slaw / fried sweetness / roasted bitterness / braised softness / soup body /
  pickle / ferment — eight states with eight different missing-role sets. It
  connects to potato + onion + pickles + mustard + yogurt. Very
  Finnish-realistic. It is a full ingredient tree, so it earns `kind: full` and
  its own transformations/components — it is *not* a filler.

## The test that encodes the guardrail

`test_no_ontology_rot` asserts: every transformation has missing roles, every
pairing has a role, every component has a future use, every transformation has
tags, every transformation has evidence, and the ingredient `kind` guardrail is
populated (`full` + `filler` both present). If a future change silently empties
one of those, this test fails. Keep it green.