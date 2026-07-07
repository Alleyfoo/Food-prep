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


def test_meal_repair_boiled_potato_onion_admits_unknown(conn):
    out = query.answer(conn,
        "I have boiled potatoes and onion. What is missing?")
    # boiled potato is a known profile; onion is not — engine says so honestly
    assert "boiled_potatoes" in out
    assert "no profile for" in out
    assert "onion" in out


def test_meal_repair_unknown_profile_steak(conn):
    out = query.answer(conn, "I have steak and eggs. What is missing?")
    # steak has no profile — honesty message names it
    assert "no profile for" in out
    assert "steak" in out


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