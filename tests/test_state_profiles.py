from foodprep import query


def test_journey_states_own_profiles_without_shadow_rows(conn):
    expected = {
        "steamed_broccoli_component",
        "roasted_broccoli_component",
        "stir_fried_broccoli_component",
        "raw_rutabaga_slaw_component",
        "roasted_rutabaga_component",
        "mashed_rutabaga_component",
        "raw_cucumber_component",
        "salted_cucumber_component",
        "quick_pickled_cucumber_component",
        "massaged_kale_component",
        "crisped_kale_component",
        "sauteed_kale_component",
        "braised_kale_component",
        "ripe_mango_component",
        "green_mango_slaw_component",
        "mango_salsa_component",
        "mango_lassi_base",
        "fresh_apricot_component",
        "roasted_apricot_component",
        "dried_apricot_component",
        "apricot_compote_component",
        "raw_cabbage_slaw_component",
        "salted_cabbage_component",
        "stir_fried_cabbage_component",
        "roasted_cabbage_component",
        "braised_cabbage_component",
        "cabbage_soup_base",
        "pickled_cabbage_component",
        "fermented_cabbage_component",
    }

    rows = conn.execute(
        "SELECT c.name FROM component_state_profiles sp "
        "JOIN components c ON c.component_id = sp.component_id"
    ).fetchall()
    assert {row[0] for row in rows} == expected
    shadows = conn.execute(
        "SELECT name FROM component_profiles "
        "WHERE name LIKE '%broccoli%' OR name LIKE '%rutabaga%' "
        "OR name LIKE '%cucumber%' OR name LIKE '%kale%' "
        "OR name LIKE '%mango%' OR name LIKE '%apricot%'"
    ).fetchall()
    # pickled_cucumber predates the journey system: it is the hand-typed
    # Plate Balance alias for shop pickles, not a shadow of the new
    # quick_pickled_cucumber_component state.
    assert {row[0] for row in shadows} == {"pickled_cucumber"}


def test_journey_state_enters_destination_reasoning_directly(conn):
    journey = query.ingredient_journey(conn, "broccoli", "roasted_florets")
    result = query.plate_balance_detail(
        conn, journey["primary_component"], destination_id="side_dish"
    )

    assert result["items"][0]["name"] == "roasted_broccoli_component"
    assert result["items"][0]["profile_source"] == "component_state"
    assert {"body", "crunch", "umami"} <= set(result["provided"])
    assert result["plate_dryness"] == 3
    assert result["target_gap"] == ["salt"]


def test_component_card_exposes_direct_plate_profile(conn):
    card = query.component_card(conn, "steamed_broccoli_component")

    assert card["plate_profile"]["component_id"] > 0
    assert card["plate_profile"]["provides_roles"] == ["body"]
    assert card["plate_profile"]["texture_tags"] == ["tender", "juicy"]
