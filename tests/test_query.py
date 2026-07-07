"""End-to-end tests for the tomato transformation engine."""

from foodprep import query


# ---- data integrity --------------------------------------------------------

def test_schema_populated(conn):
    assert conn.execute("SELECT count(*) FROM ingredients").fetchone()[0] >= 30
    # 12 tomato + 4 onion + 9 potato
    assert conn.execute("SELECT count(*) FROM transformations").fetchone()[0] == 25
    assert conn.execute("SELECT count(*) FROM roles").fetchone()[0] >= 12
    assert conn.execute("SELECT count(*) FROM pairings").fetchone()[0] >= 30
    assert conn.execute("SELECT count(*) FROM component_profiles").fetchone()[0] >= 5
    # ingredient kind guardrail: full transformation ingredients exist
    kinds = {r[0] for r in conn.execute("SELECT DISTINCT kind FROM ingredients").fetchall()}
    assert {"full", "filler"} <= kinds


# ---- onion (second ingredient — proves the loader generalizes) -----------

def test_onion_transformations_loaded(conn):
    rows = query.transformations_for_ingredient(conn, "onion")
    techs = {r["technique"] for r in rows}
    assert {"raw_assemble", "saute", "caramelize", "pickle"} == techs


def test_onion_what_can_i_do(conn):
    out = query.answer(conn, "what can I do with onion?")
    assert "caramelized_onion_component" in out
    assert "missing:" in out
    # tomato is not leaking into the onion answer
    assert "tomato_sauce_base" not in out


def test_onion_caramelize_next(conn):
    out = query.answer(conn, "I caramelized onions, now what?")
    assert "caramelized_onion_component" in out
    assert "acid" in out  # caramelized onion needs acid to balance sweetness
    assert "vinegar" in out


def test_onion_component_first(conn):
    out = query.answer(conn, "what can I do with caramelized_onion_component?")
    assert "caramelized_onion_component" in out
    assert "use it in:" in out
    assert "soup" in out or "stew" in out or "sandwich" in out


def test_onion_hub(conn):
    out = query.hub_explained(conn, "onion")
    assert "unlocks" in out
    # vinegar balances both raw and caramelized onion
    assert "vinegar" in out


def test_ingredient_detection_onion(conn):
    assert query._detect_ingredient("what can I do with onion?", conn) == "onion"
    assert query._detect_ingredient("what can I do with tomatoes?", conn) == "tomato"


# ---- potato (third full transformation ingredient) -----------------------

def test_potato_transformations_loaded(conn):
    rows = query.transformations_for_ingredient(conn, "potato")
    techs = {r["technique"] for r in rows}
    assert {"boil", "mash", "roast", "fry", "gratin", "bake", "soup",
            "salad", "hash"} == techs


def test_potato_kind_is_both(conn):
    # potato has a technique tree AND remains a filler (mild_base) — `both`
    row = conn.execute(
        "SELECT kind FROM ingredients WHERE canonical_name = 'potato'"
    ).fetchone()
    assert row["kind"] == "both"


def test_potato_what_can_i_do(conn):
    out = query.answer(conn, "what can I do with potatoes?")
    assert "mashed_potato_component" in out
    assert "missing:" in out
    # potato answer must not leak tomato storage branches
    assert "canned_tomato_base" not in out


def test_potato_mash_now_what(conn):
    out = query.answer(conn, "I mashed potatoes, now what?")
    assert "mashed_potato_component" in out
    # mash needs acid/crunch/freshness(herb)/protein — NOT more fat
    assert "acid" in out
    assert "crunch" in out
    assert "protein" in out


def test_potato_component_first(conn):
    out = query.answer(conn, "what can I do with roasted_potato_component?")
    assert "roasted_potato_component" in out
    assert "use it in:" in out


# ---- meal repair: honesty + potato plate combos --------------------------

def test_meal_repair_roasted_potato_tomato_sauce(conn):
    out = query.answer(conn,
        "I have roasted potatoes and tomato sauce. What is missing?")
    assert "missing for a balanced plate:" in out
    assert "roasted_potato" in out
    assert "tomato_sauce" in out
    # roasted potato gives carb/umami; sauce gives acid/umami/body/hydration
    # -> still missing salt, fat, herb, crunch, protein
    assert "salt" in out
    assert "fat" in out
    assert "herb" in out
    assert "protein" in out
    # carb is satisfied by potato — not in the missing list
    assert "carb" not in out.split("missing for a balanced plate:")[1].split("add:")[0]


def test_meal_repair_boiled_potato_onion_ingredient(conn):
    # Round 4: onion is now recognised as an ingredient (provides aromatic),
    # not "unknown". It still has no component_profile, so the engine warns
    # that it lacks balance data — honest about the limit without pretending
    # onion is a stranger.
    out = query.answer(conn,
        "I have boiled potatoes and onion. What is missing?")
    assert "boiled_potatoes" in out
    assert "onion (ingredient)" in out          # recognised, not unknown
    assert "no profile for" in out               # but no balance profile
    assert "onion" in out


def test_meal_repair_unknown_profile_steak(conn):
    out = query.answer(conn, "I have steak and eggs. What is missing?")
    # steak is neither a profile nor an ingredient — honesty message names it
    assert "no profile for" in out
    assert "steak" in out
    assert "unknown item" in out


def test_potato_gratin_too_heavy(conn):
    out = query.answer(conn,
        "I have potato gratin and it is too heavy. What lightens it?")
    assert "acid" in out
    assert "herb" in out
    assert "crunch" in out
    assert "avoid" in out.lower()  # warns against more fat/body/cream


def test_no_ontology_rot(conn):
    # transformations without missing roles: only none (freeze/can carry mild_base low)
    n = conn.execute("""
        SELECT count(*) FROM transformations t
        WHERE NOT EXISTS (SELECT 1 FROM transformation_missing_roles mr
                          WHERE mr.transformation_id = t.transformation_id)
    """).fetchone()[0]
    assert n == 0
    # pairings with no role
    assert conn.execute("SELECT count(*) FROM pairings WHERE role_id IS NULL").fetchone()[0] == 0
    # components with no future uses
    assert conn.execute("""
        SELECT count(*) FROM components c WHERE NOT EXISTS (
            SELECT 1 FROM component_uses cu WHERE cu.component_id = c.component_id)
    """).fetchone()[0] == 0
    # transformations with no tags
    assert conn.execute("""
        SELECT count(*) FROM transformations tr WHERE NOT EXISTS (
            SELECT 1 FROM transformation_tags tt WHERE tt.transformation_id = tr.transformation_id)
    """).fetchone()[0] == 0
    # every transformation has evidence
    assert conn.execute("""
        SELECT count(*) FROM transformations t WHERE NOT EXISTS (
            SELECT 1 FROM transformation_evidence e WHERE e.transformation_id = t.transformation_id)
    """).fetchone()[0] == 0


# ---- test 1: product shape -------------------------------------------------

def test_what_can_i_do_is_product_shape(conn):
    out = query.answer(conn, "what can I do with tomatoes?")
    # the product shape: technique → component → flavour/texture → missing → add → use
    assert "→" in out
    assert "missing:" in out
    assert "add:" in out
    # not an unbounded 12-row flat dump — capped to top branches
    assert out.count("→") <= 5 * 5
    # the answer must be the multi-branch product shape, not a single-branch dump
    # (regression guard for the "can" modal being misparsed as the canning technique)
    branch_lines = [ln for ln in out.splitlines() if ln and not ln.startswith((" ", "→", "What", "("))]
    assert len(branch_lines) >= 4  # top 5 branches
    assert "canned_tomato_base" not in out.splitlines()[0]  # not a single-branch answer


def test_branches_ranked_and_capped(conn):
    rows = query.top_branches(conn, "tomato", limit=5)
    assert len(rows) == 5
    # confidence high before medium
    assert rows[0]["confidence"] == "high"


def test_roast_now_what_is_product_shape(conn):
    out = query.answer(conn, "I roasted tomatoes, now what?")
    assert "roasted_tomato_component" in out
    assert "missing:" in out
    assert "add:" in out
    # protein gap is now curated (was unfilled before)
    assert "eggs" in out or "soft_cheese" in out


def test_next_intent_priority_ordered(conn):
    tr = query.transformation_by_technique(conn, "roast")
    d = query.branch_detail(conn, tr["transformation_id"])
    # missing roles returned in priority order (high before medium before low)
    priorities = [m["priority"] for m in d["missing"]]
    assert priorities == sorted(priorities, key=lambda p: {"high": 0, "medium": 1, "low": 2}[p])


def test_sauce_missing_roles(conn):
    tr = query.transformation_by_technique(conn, "simmer")
    gaps = {g["role_name"] for g in query.missing_roles(conn, tr["transformation_id"])}
    assert {"fat", "aromatic", "carb"} <= gaps


# ---- test 2: component-first ------------------------------------------------

def test_component_first_roasted(conn):
    out = query.answer(conn, "what can I do with roasted_tomato_component?")
    assert "roasted_tomato_component" in out
    assert "use it in:" in out
    # should mention real uses, not the generic 12-branch dump
    assert "pasta" in out or "pizza" in out or "toast" in out
    assert "What you can do with tomatoes" not in out


def test_component_first_sauce_base(conn):
    out = query.answer(conn, "what can I do with tomato_sauce_base tomorrow?")
    assert "tomato_sauce_base" in out
    assert "use it in:" in out
    assert "pasta" in out  # sauce base goes to pasta


def test_component_first_reduced(conn):
    out = query.answer(conn, "what can I do with reduced_tomato_base?")
    assert "reduced_tomato_base" in out
    assert "stew" in out or "braise" in out or "pizza" in out


def test_freeze_well_list(conn):
    out = query.answer(conn, "what tomato components freeze well?")
    assert "frozen_tomato_base" in out
    assert "fresh_tomato_component" not in out


# ---- test 3: missing-role sanity (gaps differ by state) --------------------

def test_missing_roles_differ_by_transformation(conn):
    raw = {g["role_name"] for g in query.missing_roles(
        conn, query.transformation_by_technique(conn, "raw_assemble")["transformation_id"])}
    roast = {g["role_name"] for g in query.missing_roles(
        conn, query.transformation_by_technique(conn, "roast")["transformation_id"])}
    soup = {g["role_name"] for g in query.missing_roles(
        conn, query.transformation_by_technique(conn, "soup")["transformation_id"])}
    pickle = {g["role_name"] for g in query.missing_roles(
        conn, query.transformation_by_technique(conn, "pickle")["transformation_id"])}
    # raw needs carrier; roasted needs acid; soup needs cream/body; pickle needs mild_base
    assert "carrier" in raw
    assert "acid" in roast
    assert "cream" in soup or "body" in soup
    assert "mild_base" in pickle
    # and they are not all identical — the data is not generic
    assert len({frozenset(raw), frozenset(roast), frozenset(soup), frozenset(pickle)}) >= 3


def test_missing_from_roasted_renders(conn):
    out = query.answer(conn, "what is missing from roasted tomato?")
    assert "roasted_tomato_component" in out
    assert "salt" in out and "acid" in out and "herb" in out


# ---- test 4: meal repair ----------------------------------------------------

def test_meal_repair_mash_chickpea(conn):
    out = query.answer(conn,
        "I have mashed potatoes and roasted chickpea patties. What taste is missing?")
    # expected: acid, herb/freshness, crunch (NOT fat — mash covers it via cream)
    assert "missing for a balanced plate:" in out
    assert "acid" in out
    assert "herb" in out
    assert "crunch" in out
    assert "fat" not in [w for w in out.split() if w == "fat"] or "fat" not in out.split("missing for a balanced plate:")[1].split("add:")[0]
    # the system recognises both items (not "only knows tomato")
    assert "mashed_potatoes" in out
    assert "chickpea_patty" in out  # alias matches "roasted chickpea patties"


def test_meal_repair_pasta_sauce(conn):
    out = query.answer(conn, "I have pasta and tomato sauce. What is missing?")
    # pasta gives carb, sauce gives acid; missing includes fat, herb, protein
    assert "missing for a balanced plate:" in out
    assert "fat" in out
    assert "herb" in out
    assert "protein" in out
    # carb should be satisfied (pasta) — not in missing
    assert "carb" not in out.split("missing for a balanced plate:")[1].split("add:")[0]


def test_meal_repair_bread_raw_tomato(conn):
    out = query.answer(conn, "I have bread and raw tomatoes. What should I add?")
    # bread gives carb+crunch, tomato gives acid; missing salt, fat, herb, protein
    assert "missing for a balanced plate:" in out
    assert "salt" in out
    assert "fat" in out


def test_lighten_roast_beans(conn):
    out = query.answer(conn, "I have roasted tomatoes and beans. What makes this less heavy?")
    assert "acid" in out
    assert "herb" in out
    assert "crunch" in out
    assert "avoid" in out.lower()  # warns against more fat/body/cream


# ---- test 5: hub explained --------------------------------------------------

def test_hub_explains_why(conn):
    out = query.hub_explained(conn, "tomato")
    # olive oil should appear with the transformations it unlocks and the role it fills
    assert "olive_oil" in out
    assert "unlocks" in out
    assert "because it fills" in out
    # mentions actual technique names, not just a count
    assert "roast" in out or "simmer" in out or "raw_assemble" in out


# ---- test 6: scout ----------------------------------------------------------

def test_scout_labelled_experimental(conn):
    out = query.scout(conn, "roast")
    assert "Scout / experimental" in out
    assert "NOT classic" in out
    # Nordic scout example present
    assert "rye_crumbs" in out or "lingonberry" in out


def test_scout_ask_prompt(conn):
    out = query.answer(conn, "what unusual but viable pairing works with roasted tomato?")
    assert "Scout / experimental" in out
    assert "NOT classic" in out


# ---- prompt parsing --------------------------------------------------------

def test_parse_prompt_intents():
    assert query.parse_prompt("what can I do with tomatoes")["intent"] == "branches"
    assert query.parse_prompt("I roasted them now what")["intent"] == "next"
    assert query.parse_prompt("I roasted them now what")["technique"] == "roast"
    assert query.parse_prompt("what can I batch prep")["intent"] == "batch"
    assert query.parse_prompt("what unlocks the most")["intent"] == "hub"
    assert query.parse_prompt("what unusual pairing")["intent"] == "scout"


def test_ingredient_detection(conn):
    assert query._detect_ingredient("what can I do with tomatoes?", conn) == "tomato"
    assert query._detect_ingredient("what can I do with tomatoes", conn) == "tomato"


def test_batch_prep(conn):
    rows = query.batch_prep(conn)
    techniques = {r["technique"] for r in rows}
    assert {"simmer", "reduce", "freeze", "can"} <= techniques
    assert all(r["batch_prep_value"] in ("high", "very_high") for r in rows)


# ---- Round 4: Plate Balance Engine (Cook mode) ----------------------------
# Evaluates a set of known component profiles / ingredients and suggests
# missing-role fillers. Cook mode is kept separate from Scout mode.

def test_plate_balance_known_profiles(conn):
    out = query.plate_balance(conn, "mashed potatoes and roasted chickpea patties")
    assert "Cook mode" in out
    assert "mashed_potatoes (profile)" in out
    assert "chickpea_patty (profile)" in out
    # aggregates provided roles from both profiles
    assert "provided roles:" in out
    assert "protein" in out and "carb" in out
    # plate-level heaviness + dryness are reported with a qualitative read
    assert "plate heaviness:" in out
    assert "plate dryness:" in out
    # missing roles + fillers grouped by role
    assert "missing for a balanced plate:" in out
    assert "acid" in out and "herb" in out and "crunch" in out
    assert "add:" in out


def test_plate_balance_ingredient_input(conn):
    # onion is a known ingredient (not a profile) — contributes base_roles,
    # and the engine warns it lacks a balance profile.
    out = query.plate_balance(conn, "boiled potatoes and onion")
    assert "boiled_potatoes (profile)" in out
    assert "onion (ingredient)" in out
    assert "no profile for" in out
    # aromatic comes from onion's base_roles
    assert "aromatic" in out


def test_plate_balance_component_name_input(conn):
    # a transformation-output component name maps to its profile
    out = query.plate_balance(conn, "roasted_tomato_component and pasta")
    assert "roasted_tomato (profile)" in out
    assert "pasta (profile)" in out
    assert "missing for a balanced plate:" in out


def test_plate_balance_unknown_component_warns(conn):
    out = query.plate_balance(conn, "kangaroo and mash")
    assert "no profile for" in out
    assert "kangaroo" in out
    assert "unknown item" in out


def test_plate_balance_balance_trigger(conn):
    # the "balance" keyword routes here even without "I have"
    out = query.answer(conn, "balance potato gratin and toast")
    assert "Cook mode" in out
    assert "potato_gratin (profile)" in out
    assert "toast (profile)" in out


def test_plate_balance_flagged_more_separate_from_hard_gaps(conn):
    # gratin provides fat + protein; toast flags them as risks. The engine must
    # NOT list fat/protein as hard missing — they go under "may want more".
    out = query.plate_balance(conn, "potato gratin and toast")
    missing_section = out.split("missing for a balanced plate:")[1].split("add:")[0]
    assert "fat" not in missing_section
    assert "protein" not in missing_section
    assert "also flagged by item profiles (may want more)" in out
    assert "fat" in out  # but present in the flagged-more section


def test_plate_balance_heaviness_and_dryness_reads(conn):
    # two rich items -> heavy read; aggregated scores
    out = query.plate_balance(conn, "potato gratin and mashed potatoes")
    assert "plate heaviness:" in out
    assert "rich" in out or "heavy" in out


def test_plate_balance_cook_excludes_experimental(conn):
    # Cook mode must not surface Scout/experimental pairings. lingonberry_vinegar
    # is an experimental-only acid filler (its only pairing is experimental), so
    # even though this plate needs acid, Cook must not surface it. (rye_crumbs is
    # now Cook-viable for potato gratin/soup — Round 5 — so it is no longer the
    # right demonstration; it stays Scout only for roasted tomato.)
    out = query.plate_balance(conn, "mashed potatoes and roasted chickpea patties")
    assert "lingonberry_vinegar" not in out
    # and lingonberry_vinegar does exist in Scout, so the exclusion is meaningful
    assert "lingonberry_vinegar" in query.scout(conn, "roast")


def test_cook_and_scout_are_separate(conn):
    cook = query.plate_balance(conn, "mashed potatoes and roasted chickpea patties")
    scout = query.scout(conn, "roast")
    assert "Cook mode" in cook
    assert "Scout / experimental" in scout
    # rye_crumbs is Scout for roasted tomato (experimental) but Cook for potato
    # (gratin/soup) — so it appears in Scout and is now ALSO a Cook filler.
    # The clean Cook/Scout separation is shown by lingonberry_vinegar: Scout-only.
    assert "rye_crumbs" in scout
    assert "lingonberry_vinegar" in scout
    assert "lingonberry_vinegar" not in cook


def test_plate_balance_empty_input_prompts_for_items(conn):
    # a balance request with no plate items named -> ask for items, don't guess
    out = query.plate_balance(conn, "what is missing?")
    assert "Name the plate items" in out


# ---- Round 5: filler pack (repairs / avoid_when / filler_profile) ----------
# Each filler answers five questions: roles / repairs / avoid_when / Finnish
# availability / Cook-or-Scout. repairs + avoid_when are per-filler profile
# data surfaced via filler_profile; they are NOT wired into plate_balance
# (see docs/ARCHITECTURE_CHECKPOINT_ROUND_4.md — that would flatten the model).

def test_filler_pack_loaded_with_repairs_and_avoid(conn):
    # the 12 fillers in the round-5 pack all carry repairs + avoid_when
    pack = ["lemon", "vinegar", "mustard", "yogurt", "cream", "butter",
            "pickles", "soy_sauce", "sauerkraut", "fresh_herbs", "chili",
            "rye_crumbs"]
    rows = {r[0]: (r[1], r[2]) for r in conn.execute(
        "SELECT canonical_name, repairs, avoid_when FROM ingredients "
        "WHERE canonical_name IN ({})".format(",".join("?" * len(pack))),
        pack,
    )}
    assert set(rows) == set(pack)
    for name, (repairs, avoid) in rows.items():
        assert repairs, f"{name} has no repairs"
        assert avoid, f"{name} has no avoid_when"
    # the three genuinely new fillers exist and are kind filler
    for name in ("sauerkraut", "fresh_herbs", "chili"):
        row = conn.execute(
            "SELECT kind, base_roles FROM ingredients WHERE canonical_name = ?",
            (name,),
        ).fetchone()
        assert row["kind"] == "filler"
        assert row["base_roles"]


def test_filler_pack_alias_reconciliation(conn):
    # pickled_cucumber and rye_breadcrumbs are name variants of existing
    # fillers — reconciled by alias, NOT duplicated (anti-hedgerow).
    assert query._match_ingredient(conn, "pickled cucumber") == "pickles"
    assert query._match_ingredient(conn, "rye breadcrumbs") == "rye_crumbs"
    assert query._match_ingredient(conn, "hapankaali") == "sauerkraut"
    # no duplicate canonicals were created for the variants
    names = {r[0] for r in conn.execute(
        "SELECT canonical_name FROM ingredients").fetchall()}
    assert "pickled_cucumber" not in names
    assert "rye_breadcrumbs" not in names


def test_filler_profile_answers_five_questions(conn):
    out = query.filler_profile(conn, "lemon")
    assert "lemon — filler profile" in out
    # 1. roles
    assert "roles filled:" in out and "acid" in out
    # 2. repairs
    assert "repairs plates that are:" in out
    assert "heavy" in out and "fatty" in out
    # 3. avoid_when
    assert "avoid when:" in out and "already_high_acid" in out
    # 4. Finnish availability
    assert "Finnish supermarket:" in out
    # 5. Cook or Scout (lemon has classic pairings -> Cook)
    assert "mode:" in out and "Cook" in out


def test_filler_profile_alias_input(conn):
    # alias input resolves to the canonical filler profile
    out = query.filler_profile(conn, "pickled cucumber")
    assert "pickles — filler profile" in out


def test_filler_profile_scout_only(conn):
    # an experimental-only filler (lingonberry_vinegar) is labelled Scout
    out = query.filler_profile(conn, "lingonberry_vinegar")
    assert "Scout / experimental" in out
    assert "Cook" not in out  # no classic pairings


def test_filler_subject_routes_to_profile_not_tomato_branches(conn):
    # "what can I do with lemon" — lemon is a filler (no tree) -> filler profile,
    # NOT the tomato branch dump (the old fallback behaviour).
    out = query.answer(conn, "what can I do with lemon")
    assert "lemon — filler profile" in out
    assert "What you can do with tomato" not in out


def test_filler_subject_does_not_steal_full_ingredient_branches(conn):
    # a full ingredient (potato) still gets its branch view, not a filler profile
    out = query.answer(conn, "what can I do with potatoes")
    assert "What you can do with potato" in out
    assert "filler profile" not in out


def test_new_fillers_are_cook_suggestable(conn):
    # the new fillers now have Cook (non-experimental) pairings, so the plate
    # engine's suggestion pool includes them — they were invisible before round
    # 5 (no pairings). They are medium-confidence, so they may not always be in
    # the top-4 shown on a given plate, but they ARE in the Cook pool.
    acid_pool = query._fillers_for_role(conn, "acid", limit=20)
    herb_pool = query._fillers_for_role(conn, "herb", limit=20)
    crunch_pool = query._fillers_for_role(conn, "crunch", limit=20)
    heat_pool = query._fillers_for_role(conn, "heat", limit=20)
    assert "sauerkraut" in acid_pool or "sauerkraut" in crunch_pool
    assert "fresh_herbs" in herb_pool
    assert "chili" in heat_pool
    # rye_crumbs is now Cook-viable for crunch (was experimental-only before
    # round 5; still Scout for roasted tomato).
    assert "rye_crumbs" in crunch_pool


def test_no_ontology_rot_round5(conn):
    # the round-5 additions keep the guardrails intact: every pairing still
    # has a role, and no transformation was added (fillers don't get trees).
    assert conn.execute(
        "SELECT count(*) FROM pairings WHERE role_id IS NULL").fetchone()[0] == 0
    assert conn.execute(
        "SELECT count(*) FROM transformations").fetchone()[0] == 25