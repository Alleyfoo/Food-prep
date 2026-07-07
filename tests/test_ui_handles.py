"""Round 7 — Streamlit slice acceptance tests.

These exercise the query-level handles the UI is wired to, NOT Streamlit
internals (no Selenium/browser). If these pass, the five tabs have the data
they need to render. Run the UI itself with `streamlit run app.py`.
"""

from foodprep import query

CABBAGE_TECHS = {
    "raw_slaw", "salt_and_drain", "stir_fry", "roast",
    "braise", "soup", "pickle", "ferment",
}


# 1. Ingredient list includes tomato/onion/potato/cabbage.
def test_ingredient_list_includes_all_four_trees(conn):
    trees = set(query.tree_ingredients(conn))
    assert {"tomato", "onion", "potato", "cabbage"} <= trees


# 2. Valid techniques for cabbage include all 8 cabbage branches.
def test_cabbage_techniques_are_all_eight(conn):
    techs = set(query.techniques_for_ingredient(conn, "cabbage"))
    assert techs == CABBAGE_TECHS


# 3. Ingredient Explorer data includes risks for cabbage branches.
def test_cabbage_branch_cards_include_risks(conn):
    cards = query.all_branch_cards(conn, "cabbage")
    assert len(cards) == 8
    # at least the raw + a heat branch must carry a non-empty risks list
    by_tech = {c["technique"]: c for c in cards}
    assert by_tech["raw_slaw"]["risks"] == ["harsh_when_raw"]
    assert "sulfurous_if_overcooked" in by_tech["roast"]["risks"]
    # every card carries tags (the card shape the UI renders)
    for c in cards:
        assert c["tags"], f"{c['technique']} has no tags"


# 4. Component Explorer resolves roasted_tomato_component.
def test_component_card_resolves_roasted_tomato(conn):
    d = query.component_card(conn, "roasted_tomato_component")
    assert d is not None
    producers = [(p["ingredient"], p["technique"]) for p in d["produced_by"]]
    assert ("tomato", "roast") in producers
    assert d["uses"]                      # has dish contexts
    assert d["missing"]                   # carries the after-state's gaps
    # risks live on the component card too (guardrail visible in Tab 2)
    braised = query.component_card(conn, "braised_cabbage_component")
    assert braised is not None
    assert "sulfurous_if_overcooked" in braised["risks"]


# 5. Plate Balance returns missing roles for mashed_potatoes + roasted_chickpea_patty.
def test_plate_balance_returns_missing_roles(conn):
    r = query.plate_balance_detail(
        conn, "I have mashed potatoes and roasted chickpea patties. what is missing?")
    # both items resolved as profiles (not unknown)
    kinds = {it["kind"] for it in r["items"]}
    assert "unknown" not in kinds
    # chickpea_patty flags acid/herb/crunch; mashed potatoes is rich — the
    # plate should report hard gaps among the TARGET_ROLES.
    assert r["target_gap"], "expected hard gaps for this plate"
    assert {"acid", "herb", "crunch"} <= set(r["target_gap"])
    # suggested fillers come back grouped by role (Cook mode, non-experimental)
    for role in ("acid", "herb", "crunch"):
        assert r["suggested_fillers"].get(role), f"no filler suggested for {role}"


# 6. Filler Profile resolves sauerkraut as filler, not cabbage ferment.
def test_filler_profile_sauerkraut_is_filler_not_cabbage(conn):
    d = query.filler_profile_detail(conn, "sauerkraut")
    assert d["found"]
    assert d["kind"] == "filler"          # NOT full/both — no technique tree
    assert "acid" in d["roles"]
    # sauerkraut has Cook pairings (potato), so it is Cook-suggestable
    assert d["n_cook"] >= 1
    # cabbage, by contrast, is full and owns the ferment tree
    cab = query.filler_profile_detail(conn, "cabbage")
    assert cab["kind"] == "full"


# 7. Scout cabbage returns 3 experimental pairings.
def test_scout_cabbage_returns_three_experimental(conn):
    rows = query.scout_rows(conn, ingredient="cabbage")
    assert len(rows) == 3
    fillers = {r["filler"] for r in rows}
    assert fillers == {"lingonberry_vinegar", "rye_crumbs", "smoked_yogurt"}
    # every scout row is genuinely experimental
    # (scout_rows filters on confidence='experimental' already; double-check
    # none of these appear in Cook suggestions for cabbage)
    cards = query.all_branch_cards(conn, "cabbage")
    cook_fillers = set()
    for c in cards:
        for role_fillers in c["fillers_by_role"].values():
            cook_fillers.update(f["filler"] for f in role_fillers)
    assert fillers.isdisjoint(cook_fillers), "scout filler leaked into Cook view"


# 8. Cook mode does not show Scout-only pairings.
def test_cook_mode_excludes_scout_only(conn):
    # The three Scout pairings for cabbage (experimental-only for cabbage) must
    # never leak into Cook-mode suggestions. Cook plate-balance suggestions:
    r = query.plate_balance_detail(
        conn, "I have grilled fish and rice. what is missing?")
    for role, fillers in r["suggested_fillers"].items():
        assert "lingonberry_vinegar" not in fillers, (
            f"experimental filler leaked into Cook suggestions for {role}")
        assert "smoked_yogurt" not in fillers
    # ...and none of the three appear in any cabbage branch's Cook filler list.
    scout_only = {"lingonberry_vinegar", "rye_crumbs", "smoked_yogurt"}
    for c in query.all_branch_cards(conn, "cabbage"):
        for fillers in c["fillers_by_role"].values():
            names = {f["filler"] for f in fillers}
            assert names.isdisjoint(scout_only), (
                f"Scout-only filler leaked into cabbage Cook view: {names & scout_only}")